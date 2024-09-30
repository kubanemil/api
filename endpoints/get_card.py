from models import Card
import logging
import json
import pytest

logger = logging.getLogger()
logger.setLevel(logging.INFO)


def lambda_handler(event: dict[str, any], context: any) -> dict[str, any]:
    logger.info(f"Event: {event}")
    logger.info(f"Context: {context}")
    try:
        card_id = event["queryStringParameters"]["card_id"]

        card = Card.get(card_id)
        logger.info(f"card info: {card.to_simple_dict()}")

        card_data = json.dumps(card.to_simple_dict())

        logger.info("200 OK")
        return {
            "statusCode": 200,
            "headers": {"Content-Type": "application/json"},
            "body": card_data,
        }
    except Card.DoesNotExist:
        logger.info("404 Not Found, bro")
        return {
            "statusCode": 404,
            "headers": {"Content-Type": "application/json"},
            "body": json.dumps({"error": "Card not found"}),
        }
    except Exception as e:
        logger.exception(e)
        return {
            "statusCode": 500,
            "headers": {"Content-Type": "application/json"},
            "body": json.dumps({"error": str(e)}),
        }


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
    response = lambda_handler(test_event, None)
    assert response["statusCode"] == 200, "Wrong status code"
    assert response["headers"] == {"Content-Type": "application/json"}, "Wrong headers"

    body: dict = json.loads(response["body"])
    assert body.keys() == set(
        ["id", "ability", "image", "name", "attack", "defense", "grade", "reach"]
    )


def test_get_card_not_found(test_event):
    test_event["queryStringParameters"] = {"card_id": "666"}

    response = lambda_handler(test_event, None)
    assert response["statusCode"] == 404, "Wrong status code"
    assert response["headers"] == {"Content-Type": "application/json"}, "Wrong headers"

    body: dict = json.loads(response["body"])
    assert body == {"error": "Card not found"}


def test_get_card_internal_error(test_event):
    del test_event["queryStringParameters"]["card_id"]

    response = lambda_handler(test_event, None)
    assert response["statusCode"] == 500, "Wrong status code"
    assert response["headers"] == {"Content-Type": "application/json"}, "Wrong headers"

    body: dict = json.loads(response["body"])
    assert "error" in body
