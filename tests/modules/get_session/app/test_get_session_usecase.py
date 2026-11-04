import uuid

import pytest

from src.modules.get_session.app.get_session_usecase import GetSessionUsecase
from src.shared.domain.entities.session import Session
from src.shared.helpers.errors.domain_errors import EntityError
from src.shared.helpers.errors.usecase_errors import NoItemsFound
from src.shared.infra.repositories.session_repository_mock import SessionRepositoryMock


class TestGetSessionUsecase:

    def test_get_session_success(self):
        repo = SessionRepositoryMock()
        usecase = GetSessionUsecase(repo)

        session = usecase(user_id="00000000-0000-0000-0000-000000000001")

        assert isinstance(session, Session)
        assert session.user_id == "00000000-0000-0000-0000-000000000001"
        assert session.refresh_token == "refresh_token_1"

    def test_get_session_not_found(self):
        repo = SessionRepositoryMock()
        usecase = GetSessionUsecase(repo)

        with pytest.raises(NoItemsFound):
            usecase(user_id=str(uuid.uuid4()))

    def test_get_session_invalid_uuid(self):
        repo = SessionRepositoryMock()
        usecase = GetSessionUsecase(repo)

        with pytest.raises(EntityError):
            usecase(user_id="not-a-uuid")

    def test_get_session_wrong_type(self):
        repo = SessionRepositoryMock()
        usecase = GetSessionUsecase(repo)

        with pytest.raises(EntityError):
            usecase(user_id=123)