import json

from create_card import lambda_handler

import pytest


@pytest.fixture
def test_event():
    return {
        "resource": "/",
        "path": "/",
        "httpMethod": "POST",
        "queryStringParameters": None,
        "multiValueQueryStringParameters": None,
        "pathParameters": None,
        "stageVariables": None,
        "requestContext": {
            "resourceId": "z5arjv47tl",
            "resourcePath": "/",
            "operationName": "createCard",
            "httpMethod": "POST",
            "extendedRequestId": "e6pB1GKFBcwEL-Q=",
            "requestTime": "30/Sep/2024:11:16:01 +0000",
            "path": "/dev",
            "accountId": "010046428417",
            "protocol": "HTTP/1.1",
            "stage": "dev",
            "domainPrefix": "yk5bfx14nh",
            "requestTimeEpoch": 1727694961854,
            "requestId": "04b2c83e-2a5d-4be3-89f3-5d33e9d273cf",
            "domainName": "yk5bfx14nh.execute-api.ap-south-1.amazonaws.com",
            "deploymentId": "qvmk14",
            "apiId": "yk5bfx14nh",
        },
        "body": '{\r\n    "name": "Gojo",\r\n    "image": "https://static.wikia.nocookie.net/jujutsu-kaisen/images/e/ef/Satoru_Gojo_%28Anime_2%29.png/revision/latest?cb=20240622022211",\r\n    "attack": 100,\r\n    "defense": 100,\r\n    "ability": "Inifinte void",\r\n    "grade": "Special",\r\n    "reach": "Melee"\r\n}',
        "isBase64Encoded": False,
    }


def test_get_card_success(test_event):
    response = lambda_handler(test_event, None)
    assert response["statusCode"] == 200, "Wrong status code"
    assert response["headers"] == {"Content-Type": "application/json"}, "Wrong headers"

    body: dict = json.loads(response["body"])
    assert body.keys() == set(
        ["id", "ability", "image", "name", "attack", "defense", "grade", "reach"]
    )


def test_get_card_key_error(test_event):
    body: dict = json.loads(test_event["body"])
    del body["image"]
    test_event["body"] = json.dumps(body)

    response = lambda_handler(test_event, None)
    assert response["statusCode"] == 400, "Wrong status code"
    assert response["headers"] == {"Content-Type": "application/json"}, "Wrong headers"

    body: dict = json.loads(response["body"])
    assert "Missing required field:" in body["error"]


def test_get_card_internal_error(test_event):
    body: dict = json.loads(test_event["body"])
    body["grade"] = "Fourth"
    test_event["body"] = json.dumps(body)

    response = lambda_handler(test_event, None)
    assert response["statusCode"] == 500, "Wrong status code"
    assert response["headers"] == {"Content-Type": "application/json"}, "Wrong headers"

    body: dict = json.loads(response["body"])
    assert "error" in body
