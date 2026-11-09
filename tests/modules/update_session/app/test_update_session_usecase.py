import uuid

import pytest

from src.modules.update_session.app.update_session_usecase import UpdateSessionUsecase
from src.shared.domain.entities.session import Session
from src.shared.helpers.errors.domain_errors import EntityError
from src.shared.helpers.errors.usecase_errors import NoItemsFound
from src.shared.infra.repositories.session_repository_mock import SessionRepositoryMock


class TestUpdateSessionUsecase:

    def test_update_session_success(self):
        repo = SessionRepositoryMock()
        usecase = UpdateSessionUsecase(repo=repo)

        updated_session = usecase(
            user_id="00000000-0000-0000-0000-000000000001",
            new_refresh_token="token_novo"
        )

        assert isinstance(updated_session, Session)
        assert updated_session.user_id == "00000000-0000-0000-0000-000000000001"
        assert updated_session.refresh_token == "token_novo"
        assert repo.sessions[0].refresh_token == "token_novo"

    def test_update_session_no_items_found(self):
        repo = SessionRepositoryMock()
        usecase = UpdateSessionUsecase(repo=repo)

        with pytest.raises(NoItemsFound):
            usecase(user_id=str(uuid.uuid4()), new_refresh_token="token_novo")

    def test_update_session_invalid_refresh_token(self):
        repo = SessionRepositoryMock()
        usecase = UpdateSessionUsecase(repo=repo)

        with pytest.raises(EntityError, match='Field refresh_token is not valid'):
            usecase(user_id="00000000-0000-0000-0000-000000000001", new_refresh_token=123)

    def test_update_session_invalid_user_id(self):
        repo = SessionRepositoryMock()
        usecase = UpdateSessionUsecase(repo=repo)

        with pytest.raises(EntityError, match='Field user_id is not valid'):
            usecase(user_id="invalid-user-id", new_refresh_token="token_novo")