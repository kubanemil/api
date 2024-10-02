import json
import logging

from models import Card

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
