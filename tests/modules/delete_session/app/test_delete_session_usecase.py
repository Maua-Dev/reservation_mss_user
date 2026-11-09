import uuid

import pytest

from src.modules.delete_session.app.delete_session_usecase import DeleteSessionUsecase
from src.shared.helpers.errors.domain_errors import EntityError
from src.shared.helpers.errors.usecase_errors import NoItemsFound
from src.shared.infra.repositories.session_repository_mock import SessionRepositoryMock


class TestDeleteSessionUsecase:

    def test_delete_session_usecase(self):
        repo = SessionRepositoryMock()
        usecase = DeleteSessionUsecase(repo=repo)
        len_before = len(repo.sessions)

        user_id = "00000000-0000-0000-0000-000000000001"

        session = usecase(user_id=user_id)

        assert len(repo.sessions) == len_before - 1
        assert session.user_id == user_id
        assert session.refresh_token == "refresh_token_1"

    def test_delete_session_invalid_type(self):
        repo = SessionRepositoryMock()
        usecase = DeleteSessionUsecase(repo=repo)

        with pytest.raises(EntityError):
            usecase(user_id=3)

    def test_delete_session_invalid_uuid(self):
        repo = SessionRepositoryMock()
        usecase = DeleteSessionUsecase(repo=repo)

        with pytest.raises(EntityError):
            usecase(user_id="not-a-uuid")

    def test_delete_session_no_session(self):
        repo = SessionRepositoryMock()
        usecase = DeleteSessionUsecase(repo=repo)

        with pytest.raises(NoItemsFound):
            usecase(user_id=str(uuid.uuid4()))