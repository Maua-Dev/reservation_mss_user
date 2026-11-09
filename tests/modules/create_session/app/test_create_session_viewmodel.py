from src.modules.create_session.app.create_session_viewmodel import CreateSessionViewmodel
from src.shared.domain.entities.session import Session


class TestCreateSessionViewmodel:

    def test_to_dict(self):
        session = Session(
            refresh_token="refresh_token_1",
            user_id="00000000-0000-0000-0000-000000000001"
        )

        viewmodel = CreateSessionViewmodel(session)

        assert viewmodel.to_dict() == {
            'session': {
                'refresh_token': "refresh_token_1",
                'user_id': "00000000-0000-0000-0000-000000000001"
            },
            'message': "the session was created successfully"
        }