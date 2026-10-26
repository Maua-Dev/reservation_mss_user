from aws_cdk import Resource, aws_apigateway as apigateway
from constructs import Construct
from aws_cdk.aws_apigateway import RestApi, Cors, CorsOptions, GatewayResponse, ResponseType


CORS_ORIGIN_BY_STAGE = {
    "dev": "https://reservation.dev.devmaua.com",
    "homolog": "https://reservation.hml.devmaua.com",
    "prod": "https://reservation.prod.devmaua.com",
}


def cors_origin_for_stage(stage: str) -> str:
    return CORS_ORIGIN_BY_STAGE.get(stage.lower(), "")


class ApigwConstruct(Construct):
    rest_api: RestApi
    api_gateway_resource: Resource
    cors_allow_origin: str
    
    def __init__(
        self, 
        scope: Construct, 
        construct_id: str, 
        stage: str, 
        stack_name: str,
        **kwargs
    ):
        
        super().__init__(scope, construct_id, **kwargs)
        
        self.cors_allow_origin = cors_origin_for_stage(stage)
        # Gateway Response header values must be single-quoted literals.
        quoted_origin = f"'{self.cors_allow_origin}'" if self.cors_allow_origin else "'*'"
        
        cors_options = CorsOptions(
            allow_origins=[self.cors_allow_origin] if self.cors_allow_origin else Cors.ALL_ORIGINS,
            allow_methods=["GET", "POST", "PUT", "DELETE", "OPTIONS"],
            allow_headers=Cors.DEFAULT_HEADERS,
            allow_credentials=bool(self.cors_allow_origin),
        )
        
        self.rest_api = RestApi(
            self, 
            id=f"{stack_name}_RestApi_{stage}",
            rest_api_name=f"{stack_name}_RestApi_{stage}",
            description=f"This is the ReservationMssUser RestApi for {stage}",
            deploy_options=apigateway.StageOptions(
                stage_name=stage.lower(),
                logging_level=apigateway.MethodLoggingLevel.OFF,
                data_trace_enabled=False,
                metrics_enabled=True,
            ),
            default_cors_preflight_options=cors_options,
        )
        
        self.api_gateway_resource = self.rest_api.root.add_resource(
            path_part="reservation-mss-user",
            default_cors_preflight_options=cors_options
        )
        
        gateway_cors_headers = {
            "Access-Control-Allow-Origin": quoted_origin,
            "Access-Control-Allow-Headers": "'" + ",".join(Cors.DEFAULT_HEADERS) + "'",
            "Access-Control-Allow-Methods": "'GET,POST,PUT,DELETE,OPTIONS'",
            "Access-Control-Allow-Credentials": "'true'" if cors_options.allow_credentials else "'false'",
        }
        
        GatewayResponse(
            self,
            "AuthorizerDenyResponse",
            rest_api=self.rest_api,
            type=ResponseType.ACCESS_DENIED,
            response_headers=gateway_cors_headers,
            status_code="403"
        )
        
        GatewayResponse(
            self,
            "AuthorizerUnauthorizedResponse",
            rest_api=self.rest_api,
            type=ResponseType.UNAUTHORIZED,
            response_headers=gateway_cors_headers,
            status_code="401"
        )
