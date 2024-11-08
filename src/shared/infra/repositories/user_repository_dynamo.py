from src.shared.domain.repositories.user_repository_interface import IUserRepository


class UserRepositoryDynamo(IUserRepository):
    def __init__(self):
        pass

    def create_user(self, user):
        pass

    def get_user(self, user_id):
        pass

    def list_users(self):
        pass

    def update_user(self, user):
        pass

    def delete_user(self, user_id):
        pass