from src.shared.domain.entities.user import User
from src.shared.domain.repositories.user_repository_interface import IUserRepository
from src.shared.domain.enums.role_enum import ROLE
from src.shared.helpers.errors.usecase_errors import DuplicatedItem
from src.modules.create_user.app.create_user_usecase import CreateUserUseCase
from src.shared.helpers.external_interfaces.external_interface import IResponse, IRequest


class CreateUserController:

    def __init__(self, usecase: CreateUserUseCase):
        self.CreateUserUseCase = usecase

    def __call__(self, request: IRequest) -> IResponse:

        print(request.data)