from .models import Card
import json
import uuid
import logging

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
    except ValueError as ve:
        return {
            "statusCode": 400,
            "headers": {"Content-Type": "application/json"},
            "body": json.dumps({"error": str(ve)}),
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


if __name__ == "__main__":
    event = {
        "resource": "/",
        "path": "/",
        "httpMethod": "POST",
        "queryStringParameters": None,
        "multiValueQueryStringParameters": None,
        "pathParameters": None,
        "stageVariables": None,
        "body": '{\r\n    "name": "Gojo",\r\n    "image": "https://static.wikia.nocookie.net/jujutsu-kaisen/images/e/ef/Satoru_Gojo_%28Anime_2%29.png/revision/latest?cb=20240622022211",\r\n    "attack": 100,\r\n    "defense": 100,\r\n    "ability": "Inifinte void",\r\n    "grade": "Special",\r\n    "reach": "Melee"\r\n}',
        "isBase64Encoded": False,
    }
    print(event["body"])
    response = lambda_handler(
        event,
        None,
    )
    print(response)
