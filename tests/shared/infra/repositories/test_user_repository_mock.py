from src.shared.infra.repositories.user_repository_mock import UserRepositoryMock
from src.shared.domain.enums.role_enum import ROLE
from src.shared.domain.entities.user import User

class TestUserRespositoryMock:
    def test_create_user(self):
        repo_mock = UserRepositoryMock()
        new_user = User(
            name="FrontFlop",
            email="front.flop@gmail.com",
            user_id="12345678-1234-1234-1234-123456789abc",
            ra="12.34567-8",
            role=ROLE.STUDENT,
            confirm_user=True
        )
        len_before = len(repo_mock.users_list)

        created_user = repo_mock.create_user(new_user)
        assert len(repo_mock.users_list) == len_before + 1
        assert created_user == new_user
    
    def test_get_user(self):
        repo_mock = UserRepositoryMock()
        user_id = "93bc6ada-c0d1-7054-26ab-e17414c98ae4"
        
        user = repo_mock.get_user(user_id)
        
        assert user is not None
        assert user.user_id == user_id
        assert user.name == "Leo Iorio"
        assert user.role == ROLE.STUDENT
        assert user.confirm_user is True
    
    def test_update_user(self):
        repo_mock = UserRepositoryMock()
        user_id = "93bc6ada-c0d1-7054-26ab-e17414c98ae4"
        
        updated_user = repo_mock.update_user(
            user_id=user_id,
            new_name="Leonardo Iorio",
            new_email="leonardo.iorio@maua.br",
            new_ra="12.34567-8"
        )

        assert updated_user is not None
        assert updated_user.name == "Leonardo Iorio"
        assert updated_user.email == "leonardo.iorio@maua.br"
        assert updated_user.ra == "12.34567-8"
    
    def test_delete_user(self):
        repo_mock = UserRepositoryMock()
        user_id = "93bc6ada-c0d1-7054-26ab-e17414c48ae3"
        
        len_before = len(repo_mock.users_list)
        deleted_user = repo_mock.delete_user(user_id)
        
        assert deleted_user is not None
        assert deleted_user.user_id == user_id
        assert len(repo_mock.users_list) == len_before - 1
        assert repo_mock.get_user(user_id) is None

    def test_get_all_users(self):
        repo_mock = UserRepositoryMock()
        users = repo_mock.get_all_users()
        
        assert users is not None
        assert len(users) == len(repo_mock.users_list)
        assert all([isinstance(user, User) for user in users])

    def test_get_user_not_found(self):
        repo_mock = UserRepositoryMock()
        user_id = "nonexistent-id"
        
        user = repo_mock.get_user(user_id)
        
        assert user is None

    def test_update_user_not_found(self):
        repo_mock = UserRepositoryMock()
        user_id = "nonexistent-id"
        
        updated_user = repo_mock.update_user(
            user_id=user_id,
            new_name="Nonexistent User"
        )
        
        assert updated_user is None

    def test_delete_user_not_found(self):
        repo_mock = UserRepositoryMock()
        user_id = "nonexistent-id"
        
        deleted_user = repo_mock.delete_user(user_id)
        
        assert deleted_user is None