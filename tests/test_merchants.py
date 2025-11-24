import pytest


@pytest.mark.asyncio
async def test_create_merchant(client):
    response = await client.post(
        "/merchants/",
        json={"name": "test_merchant", "percent_fee": "2.5"},
    )

    assert response.status_code == 200
    data = response.json()
    assert data["status"] == 200
    assert data["result"]["name"] == "test_merchant"
    assert data["result"]["percent_fee"] == "2.50"


@pytest.mark.asyncio
async def test_create_merchant_duplicate(client, merchant_a):
    response = await client.post(
        "/merchants/",
        json={"name": "alice", "percent_fee": "1.0"},
    )

    assert response.status_code == 409


@pytest.mark.asyncio
async def test_get_merchant(client, merchant_a, a_merchant_btc_balance, a_merchant_usd_balance):
    response = await client.get(f"/merchants/{merchant_a['name']}")

    assert response.status_code == 200
    data = response.json()["result"]
    assert data["name"] == merchant_a['name']
    assert "balances" in data
    assert len(data["balances"]) == 2

    currencies = [b["currency"] for b in data["balances"]]
    assert "BTC" in currencies
    assert "USD" in currencies


@pytest.mark.asyncio
async def test_get_merchant_not_found(client):
    response = await client.get("/merchants/123")

    assert response.status_code == 404


@pytest.mark.asyncio
async def test_get_all_merchants(client, merchant_a, merchant_b):
    response = await client.get("/merchants/")

    assert response.status_code == 200
    data = response.json()["result"]
    assert len(data) >= 2

    names = {m["name"] for m in data}
    assert merchant_a["name"] in names
    assert merchant_b["name"] in names
