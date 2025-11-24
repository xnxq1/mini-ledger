from decimal import Decimal
from typing import AsyncGenerator

import pytest_asyncio
from httpx import ASGITransport, AsyncClient

from app.infra.db.connection import get_async_engine
from app.infra.db.utils import metadata
from app.infra.redis.connection import get_redis_client
from app.main import create_app


@pytest_asyncio.fixture(scope="function")
async def db_engine():
    engine = get_async_engine()

    async with engine.begin() as conn:
        await conn.run_sync(metadata.drop_all)
        await conn.run_sync(metadata.create_all)

    yield engine

    async with engine.begin() as conn:
        await conn.run_sync(metadata.drop_all)

    await engine.dispose()


@pytest_asyncio.fixture(scope="function")
async def redis_client():
    client = await get_redis_client()
    await client.flushdb()
    yield client
    await client.flushdb()
    await client.close()


@pytest_asyncio.fixture(scope="function")
async def client(db_engine, redis_client) -> AsyncGenerator[AsyncClient, None]:
    app = create_app()

    async with AsyncClient(
        transport=ASGITransport(app=app),
        base_url="http://test",
        follow_redirects=True,
    ) as ac:
        yield ac


@pytest_asyncio.fixture
async def merchant_a(client):
    response = await client.post(
        "/merchants",
        json={"name": "alice", "percent_fee": "2.0"},
    )
    assert response.status_code == 200
    return response.json()["result"]


@pytest_asyncio.fixture
async def merchant_b(client):
    response = await client.post(
        "/merchants",
        json={"name": "bob", "percent_fee": "1.5"},
    )
    assert response.status_code == 200
    return response.json()["result"]


@pytest_asyncio.fixture
async def a_merchant_btc_balance(client, merchant_a):
    response = await client.post(
        "/merchants/balance",
        json={
            "merchant_id": merchant_a["id"],
            "currency": "BTC",
            "initial_amount": "1.0",
        },
    )
    assert response.status_code == 200
    return response.json()["result"]


@pytest_asyncio.fixture
async def a_merchant_usd_balance(client, merchant_a):
    response = await client.post(
        "/merchants/balance",
        json={
            "merchant_id": merchant_a["id"],
            "currency": "USD",
            "initial_amount": "1000.0",
        },
    )
    assert response.status_code == 200
    return response.json()["result"]


@pytest_asyncio.fixture
async def b_merchant_btc_balance(client, merchant_b):
    response = await client.post(
        "/merchants/balance",
        json={
            "merchant_id": merchant_b["id"],
            "currency": "BTC",
            "initial_amount": "0.5",
        },
    )
    assert response.status_code == 200
    return response.json()["result"]


async def get_balance(client, merchant_name: str, currency: str) -> Decimal:
    response = await client.get(f"/merchants/{merchant_name}/balance")
    assert response.status_code == 200
    balances = response.json()["result"]

    for balance in balances:
        if balance["currency"] == currency:
            return Decimal(balance["amount"])

    return Decimal("0")


async def create_transfer(
    client,
    from_merchant: str,
    to_merchant: str,
    amount: str,
    currency: str,
    idempotency_key: str,
):
    return await client.post(
        "/transfers",
        json={
            "from_merchant": from_merchant,
            "to_merchant": to_merchant,
            "amount": amount,
            "currency": currency,
        },
        headers={"Idempotency-Key": idempotency_key},
    )
