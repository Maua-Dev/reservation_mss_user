from src.shared.domain.entities.user import User
from src.shared.domain.enums.role_enum import ROLE
from src.shared.infra.dto.user_dynamo_dto import UserDynamoDTO
from src.shared.infra.repositories.user_repository_dynamo import UserRepositoryDynamo
from src.shared.infra.repositories.user_repository_mock import UserRepositoryMock


class TestUserRepositoryDynamo:

    def test_dynamo_get_all_members(self):

        repo = UserRepositoryDynamo()
        repo_mock = UserRepositoryMock()

        mock_users = repo_mock.users_list
        dynamo_users = repo.get_all_users()

        sorted_mock_users = sorted(mock_users, key=lambda x: x.user_id)
        sorted_dynamo_users = sorted(dynamo_users, key=lambda x: x.user_id)

        for m_user, d_user in zip(sorted_mock_users, sorted_dynamo_users):
            assert m_user.__dict__ == d_user.__dict__

    def test_dynamo_create_user(self):

        repo = UserRepositoryDynamo()

        user = User(
            user_id="93bc6adb-c0d1-7054-26ab-e17454c477e9",
            email="23.00847-4@maua.br",
            ra="23.00847-4",
            name="Memphis Depay",
            role=ROLE.STUDENT,
            confirm_user=True
        )

        new_user = repo.create_user(new_user=user)

        assert new_user == user

    def test_dynamo_get_user(self):

        repo = UserRepositoryDynamo()
        mock_repo = UserRepositoryMock()

        user_from_mock = mock_repo.get_user("93bc6ada-c0d1-7054-26ab-e17414c98aa7")
        user_from_dynamo = repo.get_user("93bc6ada-c0d1-7054-26ab-e17414c98aa7")

        assert user_from_mock.__dict__ == user_from_dynamo.__dict__

    def test_dynamo_delete_user(self):

        repo = UserRepositoryDynamo()
        mock_repo = UserRepositoryMock()

        user_from_dynamo = repo.get_user("93bc6adb-c0d1-7054-26ab-e17454c477e9")

        deleted_user = repo.delete_user(user_id=user_from_dynamo.user_id)

        assert user_from_dynamo.__dict__ == deleted_user.__dict__

    def test_dynamo_update_user(self):

        repo = UserRepositoryDynamo()

        prev_user = repo.get_user(user_id="93bc6ada-c0d1-7054-26ab-e17414c98ae4")

        updated_user = repo.update_user(
            user_id="93bc6ada-c0d1-7054-26ab-e17414c98ae4",
            new_confirm_user=True
        )

        assert updated_user.confirm_user is True
        assert updated_user.role == prev_user.role

