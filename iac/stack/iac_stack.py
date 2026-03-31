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

    def __init__(
        self, 
        scope: Construct, 
        stack_id: str, 
        stage: str,
        stack_name,
        **kwargs
    ) -> None:
        super().__init__(scope, stack_id, **kwargs)
            
        self.apigw_construct = ApigwConstruct(
            self,
            construct_id=f"{stack_name}_Apigw",
            stage=stage,
            stack_name=stack_name
        )
        
        self.dynamo_construct = DynamoConstruct(
            self,
            construct_id=f"{stack_name}_Dynamo",
            stage=stage,
            stack_name=stack_name
        )
        
        self.ssm_construct = SsmConstruct(
            self,
            construct_id=f"{stack_name}Ssm",
            stage=stage,
            stack_name=stack_name,
            # atenção para esse próximo parâmetro. de preferencia deixe tudo minusculo sem _
            # isso deve corresponder ao prefixo de caminho passado no CD dos outros mss (inclusive front)
            # que acessam os parametros no ssm.
            mss_name_identification_for_path="reservationmssuser",
            api=self.apigw_construct.rest_api,
            api_gateway_resource=self.apigw_construct.api_gateway_resource
        )

        ENVIRONMENT_VARIABLES = {
            "STAGE": stage.upper(),
            "DYNAMO_TABLE_NAME": self.dynamo_construct.table.table_name,
            "DYNAMO_PARTITION_KEY": "PK",
            "DYNAMO_SORT_KEY": "SK",
            "REGION": self.aws_region,
            
            # essa variável vem do github actions como um secret
            
            "GRAPH_MICROSOFT_ENDPOINT": os.getenv("GRAPH_MICROSOFT_ENDPOINT")
        }

        self.lambda_construct = LambdaConstruct(
            self,
            construct_id=f"{stack_name}_Lambda",
            stage=stage,
            stack_name=stack_name,
            api_gateway_resource=self.apigw_construct.api_gateway_resource,
            environment_variables=ENVIRONMENT_VARIABLES,
        )

        for function in self.lambda_construct.functions_that_need_dynamo_permissions:
            self.dynamo_construct.table.grant_read_write_data(function)

        