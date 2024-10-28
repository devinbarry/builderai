from pytest import fail

from tests.helpers import json_of_response


def test_create_trade(client, app):
    trade_params = dict(
        type="buy",
        user_id=1,
        symbol="USD",
        shares=30,  # Valid: exactly at upper bound
        price=90,
        timestamp=1531522701000
    )

    response = client.post("/trades", json=trade_params)
    assert response.status_code == 201
    assert json_of_response(response) == dict(id=1, **trade_params)


def test_create_trade_with_minimum_shares(client, app):
    trade_params = dict(
        type="buy",
        user_id=1,
        symbol="USD",
        shares=10,  # Valid: exactly at lower bound
        price=90,
        timestamp=1531522701000
    )

    response = client.post("/trades", json=trade_params)
    assert response.status_code == 201
    assert json_of_response(response) == dict(id=1, **trade_params)


def test_create_trade_with_invalid_shares_below_minimum(client, app):
    trade_params = dict(
        type="buy",
        user_id=1,
        symbol="USD",
        shares=9,  # Invalid: below minimum
        price=90,
        timestamp=1531522701000
    )

    response = client.post("/trades", json=trade_params)
    assert response.status_code == 400
    assert json_of_response(response) == {'error': 'shares must be between 10 and 30 inclusive'}


def test_create_trade_with_invalid_shares_above_maximum(client, app):
    trade_params = dict(
        type="buy",
        user_id=1,
        symbol="USD",
        shares=31,  # Invalid: above maximum
        price=90,
        timestamp=1531522701000
    )

    response = client.post("/trades", json=trade_params)
    assert response.status_code == 400
    assert json_of_response(response) == {'error': 'shares must be between 10 and 30 inclusive'}


def test_all_trades_returns_all_trades_json_ordered_by_id(client, app):
    trades_params = [
        dict(
            type="buy",
            user_id=1,
            symbol="USD",
            shares=30,
            price=90,
            timestamp=1531522701000
        ),
        dict(
            type="sell",
            user_id=2,
            symbol="EUR",
            shares=20,
            price=95,
            timestamp=1531522701001
        )
    ]

    for trade_params in trades_params:
        response = client.post("/trades", json=trade_params)

        if response.status_code != 201:
            fail('POST /trades is not implemented')

    response = client.get("/trades")

    expected = [dict(id=index, **trade_params) for index, trade_params in enumerate(trades_params, start=1)]

    assert response.status_code == 200
    assert json_of_response(response) == expected


def test_all_trades_returns_empty_list_when_no_trades_in_database(client, app):
    response = client.get("/trades")
    assert response.status_code == 200
    assert json_of_response(response) == []


def test_get_trade_returns_trade_json_when_exists(client, app):
    trade_params = dict(
        type="buy",
        user_id=25,
        symbol="USD",
        shares=15,
        price=250,
        timestamp=1531522702301
    )

    post_response = client.post("/trades", json=trade_params)

    if post_response.status_code != 201:
        fail('POST /trades is not implemented')

    get_response = client.get(f"/trades/{json_of_response(post_response).get('id')}")

    expected = dict(id=1, **trade_params)
    assert get_response.status_code == 200
    assert json_of_response(get_response) == expected


def test_get_trade_returns_status_404_when_does_not_exist(client, app):
    trade_params = dict(
        type="buy",
        user_id=25,
        symbol="USD",
        shares=15,
        price=250,
        timestamp=1531522702301
    )

    post_response = client.post("/trades", json=trade_params)

    if post_response.status_code != 201:
        fail('POST /trades is not implemented')

    response = client.get("/trades/999")
    assert response.status_code == 404


def test_patch_trade_returns_status_405(client, app):
    trade_params = dict(
        type="buy",
        user_id=25,
        symbol="USD",
        shares=15,
        price=250,
        timestamp=1531522702301
    )

    post_response = client.post("/trades", json=trade_params)

    if post_response.status_code != 201:
        fail('POST /trades is not implemented')

    response = client.patch(f"/trades/{json_of_response(post_response).get('id')}")
    assert response.status_code == 405


def test_put_trade_returns_status_405(client, app):
    trade_params = dict(
        type="buy",
        user_id=25,
        symbol="USD",
        shares=15,
        price=250,
        timestamp=1531522702301
    )

    post_response = client.post("/trades", json=trade_params)

    if post_response.status_code != 201:
        fail('POST /trades is not implemented')

    response = client.put(f"/trades/{json_of_response(post_response).get('id')}")
    assert response.status_code == 405


def test_delete_trade_returns_status_405(client, app):
    trade_params = dict(
        type="buy",
        user_id=25,
        symbol="USD",
        shares=15,
        price=250,
        timestamp=1531522702301
    )

    post_response = client.post("/trades", json=trade_params)

    if post_response.status_code != 201:
        fail('POST /trades is not implemented')

    response = client.delete(f"/trades/{json_of_response(post_response).get('id')}")
    assert response.status_code == 405
