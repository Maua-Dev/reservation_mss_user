from src.modules.create_user.app.create_user_presenter import usecase
from src.shared.environments import Environments
from src.shared.domain.entities.user import User
from src.shared.domain.repositories.user_repository_interface import IUserRepository
from src.shared.domain.enums.role_enum import ROLE
from src.modules.create_user.app.create_user_usecase import CreateUserUseCase
from src.shared.helpers.errors.domain_errors import EntityError
from src.shared.helpers.external_interfaces.external_interface import IResponse, IRequest
from src.shared.helpers.errors.controller_errors import BaseError, MissingParameters
from src.shared.helpers.external_interfaces.http_codes import BadRequest, InternalServerError


class CreateUserController:

    def __init__(self, usecase: CreateUserUseCase):
        self.CreateUserUseCase = usecase

    def __call__(self, request: IRequest) -> IResponse:

        id_from_request = request.data.get("Authorizer").get("user").get("id")
        user_repo = Environments.get_user_repo()

        try:
            if request.data.get("Authorizer").get("user") is None:
                raise MissingParameters('user data from authorizer')

            user = self.CreateUserUseCase(
                name=request.data.get("name"),
                email=request.data.get("mail"),
                user_id=request.data.get("id"),
            )

        except MissingParameters as err:
            return BadRequest(body=err.message)

        except EntityError as err:
            return BadRequest(body=err.message)

        except Exception as err:
            return InternalServerError(body=err.args[0])
