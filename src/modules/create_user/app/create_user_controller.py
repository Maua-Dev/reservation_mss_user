import json

from src.modules.create_user.app.create_user_viewmodel import CreateUserViewmodel
from src.modules.create_user.app.create_user_usecase import CreateUserUsecase
from src.shared.helpers.errors.domain_errors import EntityError
from src.shared.helpers.errors.usecase_errors import DuplicatedItem
from src.shared.helpers.external_interfaces.external_interface import IResponse, IRequest
from src.shared.helpers.errors.controller_errors import MissingParameters, Denied
from src.shared.helpers.external_interfaces.http_codes import BadRequest, InternalServerError, Created, NotFound, \
    Conflict


class CreateUserController:

    def __init__(self, usecase: CreateUserUsecase):
        self.CreateUserUseCase = usecase

    def __call__(self, request: IRequest) -> IResponse:

        try:
            if request.data.get('user_from_authorizer') is None:
                raise Denied()

            if isinstance(request.data.get('user_from_authorizer'), str):

                user_to_create = json.loads(request.data.get('user_from_authorizer'))

            else:

                user_to_create = request.data.get('user_from_authorizer')

            user = self.CreateUserUseCase(
                name=user_to_create['name'],
                email=user_to_create['mail'],
                user_id=user_to_create['id'],
            )

            viewmodel = CreateUserViewmodel(user)

            return Created(viewmodel.to_dict())

        except DuplicatedItem as err:
            return BadRequest(body=err.message)

        except EntityError as err:
            return BadRequest(body=err.message)

        except Denied as err:
            return NotFound(body=err.message)

        except Exception as err:
            return InternalServerError(body=err.args[0])
