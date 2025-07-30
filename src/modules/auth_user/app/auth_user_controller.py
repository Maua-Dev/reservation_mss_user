import json

from .auth_user_viewmodel import AuthUserViewmodel
from .auth_user_usecase import AuthUserUsecase
from src.shared.helpers.errors.domain_errors import EntityError
from src.shared.helpers.errors.usecase_errors import DuplicatedItem
from src.shared.helpers.external_interfaces.external_interface import IResponse, IRequest
from src.shared.helpers.errors.controller_errors import Denied
from src.shared.helpers.external_interfaces.http_codes import BadRequest, InternalServerError, NotFound, OK


class AuthUserController:

    def __init__(self, usecase: AuthUserUsecase):
        self.AuthUserUseCase = usecase

    def __call__(self, request: IRequest) -> IResponse:

        try:
            if request.data.get('user_from_authorizer') is None:
                raise Denied()

            user_to_create = request.data.get('user_from_authorizer')

            if not isinstance(request.data.get('user_from_authorizer'), dict):

                user_to_create = json.loads(request.data.get('user_from_authorizer'))

            # ????
            user = self.AuthUserUseCase(
                name=user_to_create.get('displayName'),
                email=user_to_create['mail'],
                user_id=user_to_create['id'],
            )

            viewmodel = AuthUserViewmodel(user[0], user[1])

            return OK(viewmodel.to_dict())

        except EntityError as err:
            return BadRequest(body=err.message)

        except Denied as err:
            return NotFound(body=err.message)

        except Exception as err:
            return InternalServerError(body=err.args[0])
