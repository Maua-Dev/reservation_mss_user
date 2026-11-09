from src.modules.delete_session.app.delete_session_viewmodel import DeleteSessionViewmodel
from src.shared.domain.entities.session import Session


class TestDeleteSessionViewmodel:

    def test_to_dict(self):
        session = Session(
            refresh_token="refresh_token_1",
            user_id="00000000-0000-0000-0000-000000000001"
        )

        viewmodel = DeleteSessionViewmodel(session)

        assert viewmodel.to_dict() == {
            'session': {
                'refresh_token': "refresh_token_1",
                'user_id': "00000000-0000-0000-0000-000000000001"
            },
            'message': "the session was deleted successfully"
        }