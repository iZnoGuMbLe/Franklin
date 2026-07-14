import pytest
from httpx import AsyncClient


async def test_create_cat(client:AsyncClient):

    response = await client.post('api/v1/categories', json={
        "name": "Products"
    })

    assert response.status_code == 201, response.text
    assert response.json()["name"] is not None


async def test_get_cat_by_id(client:AsyncClient):

    new_data = await client.post('api/v1/categories', json={
        "name": "Products"
    })

    transaction_id = new_data.json()["id"]

    response = await client.get(f'/api/v1/categories/{transaction_id}')

    assert response.status_code == 200, response.text
    assert response.json()["name"] is not None


async def test_update_cat(client:AsyncClient):
    new_data = await client.post('api/v1/categories', json={
        "name": "Products"
    })

    transaction_id = new_data.json()["id"]

    response = await client.patch(f'/api/v1/categories/{transaction_id}',json={
        "name": "Groceries"
    })

    assert response.status_code == 200
    assert response.json()["name"] == "Groceries"


async def test_delete_cat(client:AsyncClient):
    new_data = await client.post('api/v1/categories', json={
        "name": "Products"
    })

    transaction_id = new_data.json()["id"]

    response = await client.delete(f'/api/v1/categories/{transaction_id}')
    assert response.status_code == 204, response.text
    one_more = await client.get(f'/api/v1/categories/{transaction_id}')
    assert one_more.status_code == 404, one_more.text


@pytest.mark.parametrize(
    "method, url",[
        ("get", "/api/v1/categories/999999"),
        ("patch","/api/v1/categories/999999"),
        ("delete","/api/v1/categories/999999")
    ])
async def test_categories_404(client:AsyncClient, method, url):

    response = await client.request(method, url, json={
        "amount": "1550"
    })

    assert response.status_code == 404, response.text

async def test_list_of_cat(client:AsyncClient):
    payloads = [
        {"name": "first"},
          {"name": "second"}
    ]

    for p in payloads:
        data = await client.post('api/v1/categories', json=p)
        assert data.status_code == 201


    response = await client.get("api/v1/categories")
    assert response.status_code == 200
    assert len(response.json()) == 2
    descriptions = {t["name"] for t in response.json()}
    assert descriptions == {"first", "second"}

