import asyncio
from decimal import Decimal

import pytest

from tests.conftest import create_transfer, get_balance


@pytest.mark.asyncio
async def test_basic_transfer(
    client, merchant_a, merchant_b, a_merchant_btc_balance, b_merchant_btc_balance
):
    response = await create_transfer(
        client,
        from_merchant=merchant_a["name"],
        to_merchant=merchant_b["name"],
        amount="0.1",
        currency="BTC",
        idempotency_key="test-transfer-1",
    )

    assert response.status_code == 200
    data = response.json()["result"]

    assert data["amount"] == "0.10000000"
    assert data["currency"] == "BTC"
    assert data["percent_fee"] == "2.00000000"

    a_balance = await get_balance(client, merchant_a["name"], "BTC")
    b_balance = await get_balance(client, merchant_b["name"], "BTC")

    assert a_balance == Decimal("1.0") - Decimal("0.102")  # 0.898
    assert b_balance == Decimal("0.5") + Decimal("0.1")  # 0.6


@pytest.mark.asyncio
async def test_transfer_with_fee_calculation(
    client, merchant_a, merchant_b, a_merchant_usd_balance
):
    response = await create_transfer(
        client,
        from_merchant=merchant_a["name"],
        to_merchant=merchant_b["name"],
        amount="100",
        currency="USD",
        idempotency_key="test-fee-1",
    )

    assert response.status_code == 200

    alice_balance = await get_balance(client, merchant_a["name"], "USD")
    bob_balance = await get_balance(client, merchant_b["name"], "USD")

    assert alice_balance == Decimal("1000") - Decimal("102")
    assert bob_balance == Decimal("100")


@pytest.mark.asyncio
async def test_transfer_insufficient_funds(client, merchant_a, merchant_b, a_merchant_btc_balance):
    response = await create_transfer(
        client,
        from_merchant=merchant_a["name"],
        to_merchant=merchant_b["name"],
        amount="0.99",
        currency="BTC",
        idempotency_key="test-insufficient-1",
    )

    assert response.status_code == 400
    assert "insufficient" in response.json()["error"].lower()


@pytest.mark.asyncio
async def test_transfer_nonexistent_merchant(client, merchant_a, a_merchant_btc_balance):
    response = await create_transfer(
        client,
        from_merchant=merchant_a["name"],
        to_merchant="123",
        amount="0.1",
        currency="BTC",
        idempotency_key="test-nonexistent-1",
    )

    assert response.status_code == 404


@pytest.mark.asyncio
async def test_transfer_nonexistent_balance(client, merchant_a, merchant_b):
    response = await create_transfer(
        client,
        from_merchant=merchant_a["name"],
        to_merchant=merchant_b["name"],
        amount="0.1",
        currency="BTC",
        idempotency_key="test-no-balance-1",
    )

    assert response.status_code == 404
    assert "balance" in response.json()["error"].lower()


@pytest.mark.asyncio
async def test_transfer_to_self(client, merchant_a, a_merchant_btc_balance):
    response = await create_transfer(
        client,
        from_merchant=merchant_a["name"],
        to_merchant=merchant_a["name"],
        amount="0.1",
        currency="BTC",
        idempotency_key="test-self-transfer-1",
    )

    assert response.status_code == 422
    assert "same merchant" in response.json()["error"][0].lower()


@pytest.mark.asyncio
async def test_idempotency_same_result(client, merchant_a, merchant_b, a_merchant_btc_balance):
    idempotency_key = "idempotent-test-1"

    response1 = await create_transfer(
        client,
        from_merchant=merchant_a["name"],
        to_merchant=merchant_b["name"],
        amount="0.1",
        currency="BTC",
        idempotency_key=idempotency_key,
    )

    response2 = await create_transfer(
        client,
        from_merchant=merchant_a["name"],
        to_merchant=merchant_b["name"],
        amount="0.1",
        currency="BTC",
        idempotency_key=idempotency_key,
    )

    assert response1.status_code == 200
    assert response2.status_code == 200

    result1 = response1.json()["result"]
    result2 = response2.json()["result"]

    assert result1["id"] == result2["id"]
    assert result1["amount"] == result2["amount"]
    assert result1["idempotency_key"] == result2["idempotency_key"]


@pytest.mark.asyncio
async def test_idempotency_balance_changed_once(
    client, merchant_a, merchant_b, a_merchant_btc_balance
):
    idempotency_key = "idempotent-test-2"

    initial_a = await get_balance(client, merchant_a["name"], "BTC")

    for _ in range(3):
        response = await create_transfer(
            client,
            from_merchant=merchant_a["name"],
            to_merchant=merchant_b["name"],
            amount="0.1",
            currency="BTC",
            idempotency_key=idempotency_key,
        )
        assert response.status_code == 200

    final_a = await get_balance(client, merchant_a["name"], "BTC")
    final_b = await get_balance(client, merchant_b["name"], "BTC")

    assert final_a == initial_a - Decimal("0.102")
    assert final_b == Decimal("0.1")


@pytest.mark.asyncio
async def test_concurrent_transfers_no_negative_balance(
    client, merchant_a, merchant_b, a_merchant_usd_balance
):
    transfer_amount = "250"

    async def make_transfer(index):
        return await create_transfer(
            client,
            from_merchant=merchant_a["name"],
            to_merchant=merchant_b["name"],
            amount=transfer_amount,
            currency="USD",
            idempotency_key=f"concurrent-{index}",
        )

    results = await asyncio.gather(*[make_transfer(i) for i in range(5)])

    successful = [r for r in results if r.status_code == 200]
    failed = [r for r in results if r.status_code == 400]

    assert len(successful) > 0
    assert len(failed) > 0

    a_balance = await get_balance(client, merchant_a["name"], "USD")
    assert a_balance >= 0


@pytest.mark.asyncio
async def test_get_transfers_filtered_currency(
    client, merchant_a, merchant_b, a_merchant_btc_balance, a_merchant_usd_balance
):
    await create_transfer(
        client, merchant_a["name"], merchant_b["name"], "0.1", "BTC", "filter-cur-1"
    )
    await create_transfer(
        client, merchant_a["name"], merchant_b["name"], "100", "USD", "filter-cur-2"
    )

    response = await client.get("/transfers?currency=BTC")

    assert response.status_code == 200
    data = response.json()["result"]
    assert all(t["currency"] == "BTC" for t in data)


@pytest.mark.asyncio
async def test_transfer_missing_idempotency_key(
    client, merchant_a, merchant_b, a_merchant_btc_balance
):
    response = await client.post(
        "/transfers",
        json={
            "from_merchant": merchant_a["name"],
            "to_merchant": merchant_b["name"],
            "amount": "0.1",
            "currency": "BTC",
        },
    )

    assert response.status_code == 422
