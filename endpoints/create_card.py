import json
import logging
import uuid

from models import Card

logger = logging.getLogger()
logger.setLevel(logging.DEBUG)


def lambda_handler(event: dict[str, any], context: any) -> dict[str, any]:
    logger.info(f"Event: {event}")
    logger.info(f"Context: {context}")
    try:
        body = json.loads(event["body"])

        card_id = str(uuid.uuid4())

        new_card = Card(
            id=card_id,
            name=body["name"],
            image=body["image"],
            attack=body["attack"],
            defense=body["defense"],
            ability=body["ability"],
            grade=body["grade"],
            reach=body["reach"],
        )

        new_card.save()

        logger.info(f"card info: {new_card}")
        return {
            "statusCode": 200,
            "headers": {"Content-Type": "application/json"},
            "body": json.dumps(new_card.to_simple_dict()),
        }
    except KeyError as ke:
        return {
            "statusCode": 400,
            "headers": {"Content-Type": "application/json"},
            "body": json.dumps({"error": f"Missing required field: {str(ke)}"}),
        }
    except Exception as e:
        logger.exception(e)
        return {
            "statusCode": 500,
            "headers": {"Content-Type": "application/json"},
            "body": json.dumps({"error": str(e)}),
        }
