from src.modules.refresh.app.refresh_viewmodel import RefreshViewmodel


class TestRefreshViewmodel:
    def test_refresh_viewmodel(self):
        response = RefreshViewmodel(access_token="signed.access.token").to_dict()

        expected = {
            "access_token": "signed.access.token",
            "message": "Tokens refreshed successfully",
        }

        assert response == expected
        assert "refresh_token" not in response
