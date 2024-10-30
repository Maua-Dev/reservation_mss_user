import os
from typing import Optional

from aws_cdk import (
    aws_lambda as lambda_,
    NestedStack, Duration,
    aws_apigateway as apigw,
)
from constructs import Construct
from aws_cdk.aws_apigateway import Resource, LambdaIntegration, TokenAuthorizer


class LambdaStack(Construct):
    functions_that_need_dynamo_permissions = []

    def create_lambda_api_gateway_integration(
            self,
            module_name: str,
            method: str,
            mss_student_api_resource: Resource,
            environment_variables: dict = {"STAGE": "TEST"},
            authorizer: Optional[TokenAuthorizer] = None
    ):
        function = lambda_.Function(
            self, module_name.title(),
            code=lambda_.Code.from_asset(f"../src/modules/{module_name}"),
            handler=f"app.{module_name}_presenter.lambda_handler",
            runtime=lambda_.Runtime.PYTHON_3_9,
            layers=[self.lambda_layer, self.lambda_power_tools],
            environment=environment_variables,
            timeout=Duration.seconds(15)
        )

        mss_student_api_resource.add_resource(
            module_name.replace("_", "-")
        ).add_method(
            method,
            integration=LambdaIntegration(
                function
            ),
            authorizer=authorizer
        )

        return function

    def __init__(self, scope: Construct, api_gateway_resource: Resource, environment_variables: dict) -> None:
        super().__init__(scope, "ReservationMssUser")

        self.lambda_layer = lambda_.LayerVersion(self, "ReservationMssUser_Layer",
                                                 code=lambda_.Code.from_asset("./lambda_layer_ReservationMssUser"),
                                                 compatible_runtimes=[lambda_.Runtime.PYTHON_3_9]
                                                 )

        self.lambda_power_tools = lambda_.LayerVersion.from_layer_version_arn(self, "Lambda_Power_Tools",
                                                                              layer_version_arn="arn:aws:lambda:us-east-2:017000801446:layer:AWSLambdaPowertoolsPythonV2:22")

        authorizer_lambda = lambda_.Function(
            self, "LambdaAuthorizerReservationMssUser",
            code = lambda_.Code.from_asset("../src/functions"),
            handler = "authorizer.lambda_handler",
            runtime=lambda_.Runtime.PYTHON_3_9,
            layers = [self.lambda_layer, self.lambda_power_tools],
            environment = environment_variables,
            timeout=Duration.seconds(15)
        )

        token_authorizer_lambda = apigw.TokenAuthorizer(
            self, "TokenAuthorizerReservationMssUser",
            handler=authorizer_lambda,
            identity_source=apigw.IdentitySource.header("Authorization"),
            authorizer_name="LambdaAuthorizerReservationMssUser",
            results_cache_ttl=Duration.minutes(5)
        )

        self.get_user_function = self.create_lambda_api_gateway_integration(
            module_name="get_user",
            method="GET",
            mss_student_api_resource=api_gateway_resource,
            environment_variables=environment_variables,
            authorizer=token_authorizer_lambda
        )

        self.create_user_function = self.create_lambda_api_gateway_integration(
            module_name="create_user",
            method="POST",
            mss_student_api_resource=api_gateway_resource,
            environment_variables=environment_variables,
            authorizer=token_authorizer_lambda
        )

        self.delete_user_function = self.create_lambda_api_gateway_integration(
            module_name="delete_user",
            method="POST",
            mss_student_api_resource=api_gateway_resource,
            environment_variables=environment_variables,
            authorizer=token_authorizer_lambda
        )

        self.update_user_function = self.create_lambda_api_gateway_integration(
            module_name="update_user",
            method="POST",
            mss_student_api_resource=api_gateway_resource,
            environment_variables=environment_variables,
            authorizer=token_authorizer_lambda
        )

        self.functions_that_need_dynamo_permissions = [self.get_user_function, self.create_user_function,
                                                       self.delete_user_function, self.update_user_function]
