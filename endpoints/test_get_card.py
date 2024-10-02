import get_card
import pytest
import json

@pytest.fixture
def test_event():
    return {
        "resource": "/",
        "path": "/",
        "httpMethod": "GET",
        "queryStringParameters": {"card_id": "123"},
        "multiValueQueryStringParameters": {"card_id": ["123"]},
        "pathParameters": None,
        "stageVariables": None,
        "requestContext": {
            "resourceId": "z5arjv47tl",
            "resourcePath": "/",
            "operationName": "getCards",
            "httpMethod": "GET",
            "extendedRequestId": "e6bsLFbJBcwEMsA=",
            "requestTime": "30/Sep/2024:09:44:58 +0000",
            "path": "/dev",
            "accountId": "010046428417",
            "protocol": "HTTP/1.1",
            "stage": "dev",
            "domainPrefix": "yk5bfx14nh",
            "requestTimeEpoch": 1727689498453,
            "requestId": "4809643d-6e83-414d-820f-6e59ffb1043d",
            "domainName": "yk5bfx14nh.execute-api.ap-south-1.amazonaws.com",
            "deploymentId": "ps9dx4",
            "apiId": "yk5bfx14nh",
        },
        "body": None,
        "isBase64Encoded": False,
    }


def test_get_card_success(test_event):
    response = get_card.lambda_handler(test_event, None)
    assert response["statusCode"] == 200, "Wrong status code"
    assert response["headers"] == {"Content-Type": "application/json"}, "Wrong headers"

    body: dict = json.loads(response["body"])
    assert body.keys() == set(
        ["id", "ability", "image", "name", "attack", "defense", "grade", "reach"]
    )


def test_get_card_not_found(test_event):
    test_event["queryStringParameters"] = {"card_id": "666"}

    response = get_card.lambda_handler(test_event, None)
    assert response["statusCode"] == 404, "Wrong status code"
    assert response["headers"] == {"Content-Type": "application/json"}, "Wrong headers"

    body: dict = json.loads(response["body"])
    assert body == {"error": "Card not found"}


def test_get_card_internal_error(test_event):
    del test_event["queryStringParameters"]["card_id"]

    response = get_card.lambda_handler(test_event, None)
    assert response["statusCode"] == 500, "Wrong status code"
    assert response["headers"] == {"Content-Type": "application/json"}, "Wrong headers"

    body: dict = json.loads(response["body"])
    assert "error" in body
