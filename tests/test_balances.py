import pytest


@pytest.mark.asyncio
async def test_create_balance(client, merchant_a):
    response = await client.post(
        "/merchants/balance",
        json={
            "merchant_id": merchant_a["id"],
            "currency": "ETH",
            "initial_amount": "10.5",
        },
    )

    assert response.status_code == 200
    data = response.json()["result"]
    assert data["currency"] == "ETH"
    assert data["amount"] == "10.50000000"
    assert data["merchant_id"] == merchant_a["id"]


@pytest.mark.asyncio
async def test_create_balance_negative_amount(client, merchant_a):
    response = await client.post(
        "/merchants/balance",
        json={
            "merchant_id": merchant_a["id"],
            "currency": "BTC",
            "initial_amount": "-1.0",
        },
    )

    assert response.status_code == 422


@pytest.mark.asyncio
async def test_create_balance_nonexistent_merchant(client):
    response = await client.post(
        "/merchants/balance",
        json={
            "merchant_id": "00000000-0000-0000-0000-000000000000",
            "currency": "BTC",
            "initial_amount": "1.0",
        },
    )

    assert response.status_code == 404


@pytest.mark.asyncio
async def test_get_merchant_balances(
    client, merchant_a, a_merchant_btc_balance, a_merchant_usd_balance
):
    response = await client.get(f"/merchants/{merchant_a['name']}/balance")

    assert response.status_code == 200
    data = response.json()["result"]
    assert len(data) == 2

    currencies = {b["currency"] for b in data}
    assert currencies == {"BTC", "USD"}


@pytest.mark.asyncio
async def test_get_balances_merchant_not_found(client):
    response = await client.get("/merchants/123/balance")
    assert response.status_code == 404
