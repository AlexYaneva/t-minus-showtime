import os

from dotenv import load_dotenv

base_dir = os.path.abspath(os.path.dirname(__file__))
load_dotenv(os.path.join(base_dir, ".env"))
API_key = os.environ.get("API_KEY")


class Config:

    SECRET_KEY = os.environ.get("SECRET_KEY") or "han-shot-first"
    MAIL_SERVER = os.environ.get("MAIL_SERVER")
    MAIL_PORT = int(os.environ.get("MAIL_PORT") or 25)
    MAIL_USERNAME = os.environ.get("MAIL_USERNAME")
    MAIL_PASSWORD = os.environ.get("MAIL_PASSWORD")
    MAIL_USE_TLS = False
    MAIL_USE_SSL = True
    CELERY_BROKER_URL = 'redis://localhost:6379'
    CELERY_RESULT_BACKEND = 'redis://localhost:6379'
    CACHE_TYPE = "simple"
    CACHE_DEFAULT_TIMEOUT = 300
    DYNAMO_TABLES = [
        # dict(
        #     TableName="Users",
        #     KeySchema=[dict(AttributeName="Email", KeyType="HASH")],
        #     AttributeDefinitions=[dict(AttributeName="Email", AttributeType="S")],
        #     ProvisionedThroughput=dict(ReadCapacityUnits=5, WriteCapacityUnits=5),
        # )
            dict(
                TableName="User_table",
                KeySchema=[dict(AttributeName="Email", KeyType="HASH"),
                            dict(AttributeName="Tracked_id", KeyType="RANGE")],
                AttributeDefinitions=[dict(AttributeName="Email", AttributeType="S"),
                                    dict(AttributeName="Tracked_id", AttributeType="N"),
                                    dict(AttributeName="Countdown", AttributeType="N")],
                GlobalSecondaryIndexes=[dict(
                                            IndexName="Tracked",
                                            KeySchema=[dict(AttributeName="Countdown", KeyType="HASH")],
                                            Projection=dict(ProjectionType="ALL"),
                                            ProvisionedThroughput=dict(ReadCapacityUnits=5, WriteCapacityUnits=5)
                                            )
                                        ],
                ProvisionedThroughput=dict(ReadCapacityUnits=5, WriteCapacityUnits=5)
                )
            ]

