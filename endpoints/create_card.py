from models import Card
import json
import uuid

def lambda_handler(event: dict[str, any], context: any) -> dict[str, any]:
    try:
        body = event['body']

        card_id = str(uuid.uuid4())

        new_card = Card(
            id=card_id,
            name=body['name'],
            image=body['image'],
            attack=body['attack'],
            defense=body['defense'],
            ability=body['ability'],
            grade=body['grade'],
            reach=body['reach']
        )

        new_card.save()

        return {
            'statusCode': 201,
            'body': new_card.to_simple_dict(),
            'headers': {
                'Content-Type': 'application/json'
            }
        }
    except ValueError as ve:
        return {
            'statusCode': 400,
            'body': json.dumps({'error': str(ve)}),
            'headers': {
                'Content-Type': 'application/json'
            }
        }
    except KeyError as ke:
        return {
            'statusCode': 400,
            'body': json.dumps({'error': f'Missing required field: {str(ke)}'}),
            'headers': {
                'Content-Type': 'application/json'
            }
        }
    except Exception as e:
        return {
            'statusCode': 500,
            'body': json.dumps({'error': str(e)}),
            'headers': {
                'Content-Type': 'application/json'
            }
        }

if __name__ == '__main__':
    lambda_handler({'body': {'name': 'test', 'image': 'test', 'attack': 1, 'defense': 1, 'ability': 'test', 'grade': 'test', 'reach': 1}}, None)