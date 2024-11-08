import boto3
from src.shared.infra.repositories.user_repository_mock import UserRepositoryMock
from src.shared.infra.repositories.user_repository_dynamo import UserRepositoryDynamo

def setup_dynamo_table():
    print("Setting up dynamo table")
    dynamo_client = boto3.client('dynamodb', endpoint_url='http://localhost:8000', region_name='sa-east-1')
    tables = dynamo_client.list_tables()['TableNames']
    table_name = "reservation_mss_user_table"

    if not table_name in tables:
        print("Creating table")
        dynamo_client.create_table(
            TableName=table_name,
            KeySchema=[
                {
                    'AttributeName': 'PK',
                    'KeyType': 'HASH'
                },
                {
                    'AttributeName': 'SK',
                    'KeyType': 'RANGE'
                }
            ],
            AttributeDefinitions=[
                {
                    'AttributeName': 'PK',
                    'AttributeType': 'S'
                },
                {
                    'AttributeName': 'SK',
                    'AttributeType': 'S'
                }
            ],
            BillingMode='PAY_PER_REQUEST',

        )
        print('Table "reservation_mss_user_table" created!\n')
    else:
        print('Table already exists!\n')

def load_mock_to_local_dynamo():
    repo_dynamo = UserRepositoryDynamo()
    repo_mock = UserRepositoryMock()

    print('Loading mock to data to dynamo...')

    print("Loading users...")
    user_count = 0
    for user in repo_mock.users_list:
        print(f'Loading user {user.name}...')
        repo_dynamo.create_user(new_user=user)
        user_count += 1
    print(f'{user_count} courts loaded\n')

    print("Done!")

def load_mock_to_real_dynamo():
    repo_dynamo = UserRepositoryDynamo()
    repo_mock = UserRepositoryMock()

    print('Loading mock data to dynamo...')

    print("Loading users")
    user_count = 0
    for user in repo_mock.users_list:
        print(f'Loading user {user.name}...')
        repo_dynamo.create_user(new_user=user)
        user_count += 1
    print(f'{user_count} courts loaded\n')

    print("Done!")


if __name__ == '__main__':
    setup_dynamo_table()
    load_mock_to_local_dynamo()