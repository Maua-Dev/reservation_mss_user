from src.shared.domain.entities.user import User
from src.shared.domain.repositories.user_repository_interface import IUserRepository
from src.shared.helpers.errors.usecase_errors import NoItemsFound

class GetAllUserUsecase:
    def __init__(self, repo: IUserRepository):
        self.repo = repo

    def __call__(self):

        users = self.repo.get_all_users()

        if not users:
            raise NoItemsFound("users")

        return users   
