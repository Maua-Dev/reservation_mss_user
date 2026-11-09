from src.modules.update_session.app.update_session_viewmodel import UpdateSessionViewmodel
from src.shared.domain.entities.session import Session


class TestUpdateSessionViewmodel:

    def test_update_session_viewmodel(self):
        session = Session(
            refresh_token="token_novo",
            user_id="00000000-0000-0000-0000-000000000001"
        )

        viewmodel = UpdateSessionViewmodel(session)

        assert viewmodel.to_dict() == {
            'updated_session': {
                'refresh_token': "token_novo",
                'user_id': "00000000-0000-0000-0000-000000000001"
            },
            'message': 'the session was updated'
        }