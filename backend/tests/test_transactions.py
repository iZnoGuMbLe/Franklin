
import pytest
from httpx import AsyncClient


async def test_create_transaction(client: AsyncClient):
    response = await client.post('api/v1/transactions', json={
        "date": "2026-07-11",
        "amount": "1500",
        "description": "Test transaction",
        "currency": 'RUB'
    })
    assert response.status_code == 201, response.text
    data = response.json()
    assert data["description"] == "Test transaction"
    assert data["id"] is not None


async def test_get_transaction_by_id(client:AsyncClient):

    new_data = await client.post('/api/v1/transactions', json={
        "date": "2026-07-11",
        "amount": "1500",
        "description": "Test transaction"
    })
    transaction_id = new_data.json()['id']

    response = await client.get(f'/api/v1/transactions/{transaction_id}')
    assert response.status_code == 200
    data = response.json()
    assert data["amount"] is not None


async def test_update_transaction(client:AsyncClient):

    new_data = await client.post('/api/v1/transactions', json={
        "date": "2026-07-11",
        "amount": "1500",
        "description": "Test transaction"
    })

    transaction_id = int(new_data.json()['id'])

    response = await client.patch(f'/api/v1/transactions/{transaction_id}', json={
        "amount": "5500",
        "description": "update"
    })
    assert response.status_code == 200, response.text
    data = response.json()
    assert data["amount"] == "5500"


async def test_delete_transaction(client:AsyncClient):
    new_data = await client.post('/api/v1/transactions', json={
        "date": "2026-07-11",
        "amount": "1500",
        "description": "Test transaction"
    })

    transaction_id = int(new_data.json()['id'])

    response = await client.delete(f'/api/v1/transactions/{transaction_id}')
    assert response.status_code == 204, response.text
    one_more = await client.get(f'/api/v1/transactions/{transaction_id}')
    assert one_more.status_code == 404



@pytest.mark.parametrize(
    "method, url", [
        ("patch", "/api/v1/transactions/999999"),
        ("get", "/api/v1/transactions/999999"),
        ("delete", "/api/v1/transactions/999999")
    ]
)
async def test_transactions_404(client:AsyncClient, method, url):

    response = await client.request(method, url, json={
        "description": "Test transaction"
    })

    assert response.status_code == 404

async def test_list_of_t(client:AsyncClient):
    payloads = [
        {"date": "2026-07-11", "amount": "1500", "description": "First", "is_income": "True"},
          {"date": "2026-07-12", "amount": "300", "description": "Second", "is_income": "False"}
    ]

    for p in payloads:
        data = await client.post('api/v1/transactions', json=p)
        assert data.status_code == 201


    response = await client.get("api/v1/transactions")
    assert response.status_code == 200
    assert len(response.json()) == 2
    descriptions = {t["description"] for t in response.json()}
    assert descriptions == {"First", "Second"}

async def test_list_of_t_income(client:AsyncClient):
    payloads = [
        {"date": "2026-07-11", "amount": "1500", "description": "First", "is_income": "True"},
        {"date": "2026-07-12", "amount": "300", "description": "Second", "is_income": "False"}
    ]

    for p in payloads:
        data = await client.post('api/v1/transactions', json=p)
        assert data.status_code == 201

    response = await client.get('api/v1/transactions', params={"is_income":True})
    assert response.status_code == 200
    assert len(response.json()) == 1
    once_more = await client.get(url='api/v1/transactions')
    assert once_more.status_code == 200
    assert len(once_more.json()) == 2


async def test_tlist_period(client:AsyncClient):
    payloads = [
        {"date": "2026-07-11", "amount": "1500", "description": "First", "is_income": "True"},
        {"date": "2026-07-14", "amount": "300", "description": "Second", "is_income": "False"},
        {"date": "2026-08-14", "amount": "3040", "description": "Third", "is_income": "False"}
    ]

    for p in payloads:
        data = await client.post(url='api/v1/transactions', json=p)
        assert data.status_code == 201


    response = await client.get(url='api/v1/transactions', params={"date_to":"2026-07-14"})
    assert response.status_code == 200
    assert len(response.json()) == 2

    once_more = await client.get(url='api/v1/transactions', params={"date_from":"2026-07-14", "date_to":"2026-07-14"})
    assert once_more.status_code == 200
    assert len(once_more.json()) == 1


async def test_tlist_sort_newest(client:AsyncClient):
    payloads = [
        {"date": "2026-07-11", "amount": "1500", "description": "First", "is_income": "True"},
        {"date": "2026-07-12", "amount": "300", "description": "Second", "is_income": "False"},
        {"date": "2026-07-13", "amount": "3040", "description": "Third", "is_income": "False"}
    ]

    for p in payloads:
        data = await client.post(url='api/v1/transactions', json=p)
        assert data.status_code == 201

    response = await client.get(url='api/v1/transactions')
    assert response.status_code == 200
    assert response.json()[0]["date"] == "2026-07-13"
