from models import Card
import logging
import json

logger = logging.getLogger()
logger.setLevel(logging.INFO)


def lambda_handler(event: dict[str, any], context: any) -> dict[str, any]:
    logger.info(f"Event: {event}")
    try:
        card_id = event["queryStringParameters"]["card_id"]

        card = Card.get(card_id)

        card_data = card.to_simple_dict()

        return {
            "statusCode": 200,
            "body": card_data,
            "headers": {"Content-Type": "application/json"},
        }
    except Card.DoesNotExist:
        return {
            "statusCode": 404,
            "body": {"error": "Card not found"},
            "headers": {"Content-Type": "application/json"},
        }
    except Exception as e:
        logging.exception(e)
        return {
            "statusCode": 500,
            "body": {"error": str(e)},
            "headers": {"Content-Type": "application/json"},
        }


if __name__ == "__main__":
    event = {'resource': '/', 'path': '/', 'httpMethod': 'GET', 'headers': {'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7', 'accept-encoding': 'gzip, deflate, br, zstd', 'accept-language': 'en-US,en;q=0.9', 'cache-control': 'max-age=0', 'Host': 'yk5bfx14nh.execute-api.ap-south-1.amazonaws.com', 'priority': 'u=0, i', 'sec-ch-ua': '"Microsoft Edge";v="129", "Not=A?Brand";v="8", "Chromium";v="129"', 'sec-ch-ua-mobile': '?0', 'sec-ch-ua-platform': '"Windows"', 'sec-fetch-dest': 'document', 'sec-fetch-mode': 'navigate', 'sec-fetch-site': 'none', 'sec-fetch-user': '?1', 'upgrade-insecure-requests': '1', 'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/129.0.0.0 Safari/537.36 Edg/129.0.0.0', 'X-Amzn-Trace-Id': 'Root=1-66fa731a-200e2c67096e1d362cf1a45a', 'X-Forwarded-For': '212.112.113.186', 'X-Forwarded-Port': '443', 'X-Forwarded-Proto': 'https'}, 'multiValueHeaders': {'accept': ['text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7'], 'accept-encoding': ['gzip, deflate, br, zstd'], 'accept-language': ['en-US,en;q=0.9'], 'cache-control': ['max-age=0'], 'Host': ['yk5bfx14nh.execute-api.ap-south-1.amazonaws.com'], 'priority': ['u=0, i'], 'sec-ch-ua': ['"Microsoft Edge";v="129", "Not=A?Brand";v="8", "Chromium";v="129"'], 'sec-ch-ua-mobile': ['?0'], 'sec-ch-ua-platform': ['"Windows"'], 'sec-fetch-dest': ['document'], 'sec-fetch-mode': ['navigate'], 'sec-fetch-site': ['none'], 'sec-fetch-user': ['?1'], 'upgrade-insecure-requests': ['1'], 'User-Agent': ['Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/129.0.0.0 Safari/537.36 Edg/129.0.0.0'], 'X-Amzn-Trace-Id': ['Root=1-66fa731a-200e2c67096e1d362cf1a45a'], 'X-Forwarded-For': ['212.112.113.186'], 'X-Forwarded-Port': ['443'], 'X-Forwarded-Proto': ['https']}, 'queryStringParameters': {'card_id': '"13"'}, 'multiValueQueryStringParameters': {'card_id': ['"13"']}, 'pathParameters': None, 'stageVariables': None, 'requestContext': {'resourceId': 'z5arjv47tl', 'resourcePath': '/', 'operationName': 'getCards', 'httpMethod': 'GET', 'extendedRequestId': 'e6bsLFbJBcwEMsA=', 'requestTime': '30/Sep/2024:09:44:58 +0000', 'path': '/dev', 'accountId': '010046428417', 'protocol': 'HTTP/1.1', 'stage': 'dev', 'domainPrefix': 'yk5bfx14nh', 'requestTimeEpoch': 1727689498453, 'requestId': '4809643d-6e83-414d-820f-6e59ffb1043d', 'identity': {'cognitoIdentityPoolId': None, 'accountId': None, 'cognitoIdentityId': None, 'caller': None, 'sourceIp': '212.112.113.186', 'principalOrgId': None, 'accessKey': None, 'cognitoAuthenticationType': None, 'cognitoAuthenticationProvider': None, 'userArn': None, 'userAgent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/129.0.0.0 Safari/537.36 Edg/129.0.0.0', 'user': None}, 'domainName': 'yk5bfx14nh.execute-api.ap-south-1.amazonaws.com', 'deploymentId': 'ps9dx4', 'apiId': 'yk5bfx14nh'}, 'body': None, 'isBase64Encoded': False}
    print(json.dumps(event, indent=" "))
    lambda_handler(event)
