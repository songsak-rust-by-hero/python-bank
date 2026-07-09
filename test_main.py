from fastapi.testclient import TestClient
from main import app
from db import Base, engine
import pytest


@pytest.fixture(autouse=True, scope="session")
def setup_db():
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)
    yield

client = TestClient(app)

def test_create_account_success():
    response = client.post(
        "/accounts/",
        json={
            "name": "ก้อง",
            "balance": "1000.00"
        }
    )

    assert response.status_code == 200


def test_create_duplicate_account():
    client.post(
        "/accounts/",
        json={
            "name": "ซ้ำ",
            "balance": "100"
        }
    )

    response = client.post(
        "/accounts/",
        json={
            "name": "ซ้ำ",
            "balance": "100"
        }
    )

    assert response.status_code == 400


def test_deposit_success():
    client.post(
        "/accounts/",
        json={
            "name": "ฝาก",
            "balance": "100"
        }
    )

    response = client.post(
        "/accounts/ฝาก/deposit",
        json={
            "amount": "200"
        }
    )

    assert response.status_code == 200
    assert response.json()["account"]["balance"] == "300.00"


def test_withdraw_over_balance():
    client.post(
        "/accounts/",
        json={
            "name": "ถอน",
            "balance": "100"
        }
    )

    response = client.post(
        "/accounts/ถอน/withdraw",
        json={
            "amount": "500"
        }
    )

    assert response.status_code == 400


def test_transfer_success():
    client.post(
        "/accounts/",
        json={
            "name": "A",
            "balance": "500"
        }
    )

    client.post(
        "/accounts/",
        json={
            "name": "B",
            "balance": "100"
        }
    )

    response = client.post(
        "/accounts/A/transfer?to_name=B",
        json={
            "amount": "200"
        }
    )

    assert response.status_code == 200


def test_get_history():
    client.post(
        "/accounts/",
        json={
            "name": "history",
            "balance": "100"
        }
    )

    client.post(
        "/accounts/history/deposit",
        json={
            "amount": "50"
        }
    )

    response = client.get("/accounts/history")

    assert response.status_code == 200