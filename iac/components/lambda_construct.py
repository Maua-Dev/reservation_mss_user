from typing import Optional

from aws_cdk import (
    aws_lambda as lambda_,
    Duration,
    aws_apigateway as apigw,
)
from constructs import Construct
from aws_cdk.aws_apigateway import Resource, LambdaIntegration, TokenAuthorizer


class LambdaConstruct(Construct):
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
            self, 
            id=module_name.title(),
            code=lambda_.Code.from_asset(f"../src/modules/{module_name}"),
            handler=f"app.{module_name}_presenter.lambda_handler",
            runtime=lambda_.Runtime("python3.13"),
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
            authorization_type=apigw.AuthorizationType.CUSTOM if authorizer else apigw.AuthorizationType.NONE,
            authorizer=authorizer
        )

        return function

    def __init__(
        self,
        scope: Construct,
        construct_id: str,
        api_gateway_resource: Resource,
        environment_variables: dict,
        **kargs,
    ) -> None:
        super().__init__(scope, construct_id, **kargs)

        self.lambda_layer = lambda_.LayerVersion(
            self, 
            id="ReservationMssUser_Layer",
            code=lambda_.Code.from_asset("./lambda_layer_out_temp"),
            compatible_runtimes=[lambda_.Runtime("python3.13")]
        )

        self.lambda_region = environment_variables.get("REGION", 'sa-east-1')
        
        self.lambda_power_tools = lambda_.LayerVersion.from_layer_version_arn(
            self, 
            "Lambda_Power_Tools",
            layer_version_arn=f"arn:aws:lambda:{self.lambda_region}:017000801446:layer:AWSLambdaPowertoolsPythonV2:22"
        )

        authorizer_lambda = lambda_.Function(
            self, 
            id="LambdaAuthorizerReservationMssUser",
            code=lambda_.Code.from_asset("../src/shared/authorizer"),
            handler="authorizer.lambda_handler",
            runtime=lambda_.Runtime("python3.13"),
            layers=[self.lambda_layer, self.lambda_power_tools],
            environment=environment_variables,
            timeout=Duration.seconds(15)
        )

        token_authorizer_lambda = apigw.TokenAuthorizer(
            self,
            id="TokenAuthorizerReservationMssUser",
            handler=authorizer_lambda,
            identity_source=apigw.IdentitySource.header("Authorization"),
            authorizer_name="LambdaAuthorizerReservationMssUser",
            results_cache_ttl=Duration.seconds(0),
        )

        self.auth_user_function = self.create_lambda_api_gateway_integration(
            module_name="auth_user",
            method="GET",
            mss_student_api_resource=api_gateway_resource,
            environment_variables=environment_variables,
            authorizer=token_authorizer_lambda,
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
            authorizer=token_authorizer_lambda,
        )

        self.delete_user_function = self.create_lambda_api_gateway_integration(
            module_name="delete_user",
            method="POST", # precisa mudar isso pra DEL
            mss_student_api_resource=api_gateway_resource,
            environment_variables=environment_variables,
            authorizer=token_authorizer_lambda
        )

        self.update_user_function = self.create_lambda_api_gateway_integration(
            module_name="update_user",
            method="POST", # precisa mudar isso para um PUT
            mss_student_api_resource=api_gateway_resource,
            environment_variables=environment_variables,
            authorizer=token_authorizer_lambda
        )

        self.get_all_users_function = self.create_lambda_api_gateway_integration(
            module_name="get_all_users",
            method="GET",
            mss_student_api_resource=api_gateway_resource,
            environment_variables=environment_variables,
            authorizer=None
        )

        self.functions_that_need_dynamo_permissions = [
            self.get_user_function, 
            self.create_user_function,
            self.get_all_users_function,
            self.delete_user_function, 
            self.update_user_function,
            self.auth_user_function,
            authorizer_lambda,
        ]
