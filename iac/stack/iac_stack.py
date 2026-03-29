from aws_cdk import (
    # Duration,
    Stack,
    # aws_sqs as sqs,
)
from constructs import Construct

from components.lambda_construct import LambdaConstruct
from components.dynamo_construct import DynamoConstruct
from components.apigw_construct import ApigwConstruct
from components.ssm_construct import SsmConstruct

import os

class IacStack(Stack):

    def __init__(self, scope: Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        self.aws_region = os.environ.get("AWS_REGION")

        self.github_ref = os.environ.get('GITHUB_REF_NAME')
        stage = ''
        if 'prod' in self.github_ref:
            stage = 'PROD'
        elif 'homolog' in self.github_ref:
            stage = 'HOMOLOG'
        else:
            stage = 'DEV'
            
        self.apigw_construct = ApigwConstruct(
            self,
            construct_id="ReservationMssUserApiGateway",
            stage=stage
        )
        
        self.dynamo_construct = DynamoConstruct(
            self,
            construct_id="ReservationMssUserDynamo",
            stage=stage,
        )
        
        self.ssm_construct = SsmConstruct(
            self,
            construct_id="ReservationMssUserSsm",
            stage=stage,
            mss_name_identification_for_path="reservationmssuser",
            api=self.apigw_construct.rest_api,
            api_gateway_resource=self.apigw_construct.api_gateway_resource
        )

        ENVIRONMENT_VARIABLES = {
            "STAGE": stage,
            "DYNAMO_TABLE_NAME": self.dynamo_construct.table.table_name,
            "DYNAMO_PARTITION_KEY": "PK",
            "DYNAMO_SORT_KEY": "SK",
            "REGION": self.aws_region,
            
            # essa variável vem do github actions como um secret
            
            "GRAPH_MICROSOFT_ENDPOINT": os.getenv("GRAPH_MICROSOFT_ENDPOINT")
        }

        self.lambda_construct = LambdaConstruct(
            self,
            construct_id="ReservationMssUserLambda",
            api_gateway_resource=self.apigw_construct.api_gateway_resource,
            environment_variables=ENVIRONMENT_VARIABLES,
        )

        for function in self.lambda_construct.functions_that_need_dynamo_permissions:
            self.dynamo_construct.table.grant_read_write_data(function)

        