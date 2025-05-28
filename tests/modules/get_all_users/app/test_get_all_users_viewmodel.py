from src.modules.get_all_users.app.get_all_users_usecase import GetAllUserUsecase
from src.modules.get_all_users.app.get_all_users_viewmodel import GetAllUsersViewModel
from src.shared.infra.repositories.user_repository_mock import UserRepositoryMock


class Test_GetAllUsersViewmodel:
    def test_get_all_users_viewmodel(self):
        repo = UserRepositoryMock()
        usecase = GetAllUserUsecase(repo)
        users = usecase()
        viewmodel = GetAllUsersViewModel(users)

        assert viewmodel.to_dict() == {
            'users': [
                {
                    'name': 'Rodas Rodas',
                    'email': 'rodas@gmail.com',
                    'user_id': '93bc6ada-c0d1-7054-26ab-e17414c48ae3',
                    'ra': None,
                    'role': 'ADMIN',
                    'confirm_user': True
                },
                {
                    'name': 'Rubio Rosa',
                    'email': '26.96379-5@maua.br',
                    'user_id': '93bc6ada-c0d1-7054-26ab-e17414c48ae5',
                    'ra': '26.96379-5',
                    'role': 'ADMIN',
                    'confirm_user': False
                },
                {
                    'name': 'Leo Iorio',
                    'email': '29.91279-6@maua.br',
                    'user_id': '93bc6ada-c0d1-7054-26ab-e17414c98ae4',
                    'ra': '29.91279-6',
                    'role': 'STUDENT',
                    'confirm_user': True
                },
                {
                    'name': 'Giovanna Ehobeckas',
                    'email': 'gi@hotmail.com',
                    'user_id': '93bc6ada-c0d1-7054-26ab-e17454c48ae6',
                    'ra': None,
                    'role': 'PROFESSOR',
                    'confirm_user': True
                },
                {
                    'name': 'Vini Berti',
                    'email': 'berti@gmail.com',
                    'user_id': '93bc6ada-c0d1-8754-26ab-e17414c48ae7',
                    'ra': None,
                    'role': 'PROFESSOR',
                    'confirm_user': False
                },
                {
                    'name': 'Gustavo Gus',
                    'email': 'timao@gmail.com',
                    'user_id': '77bc6ada-c0d1-8754-26ab-e17414c48ae8',
                    'ra': None,
                    'role': 'ADMIN',
                    'confirm_user': False
                },
                {
                    'name': 'Relâmpago Marquinhos',
                    'email': '12.12345-8@maua.br',
                    'user_id': '93bc6ada-c0e1-7054-26ab-e17414c48ae9',
                    'ra': '12.12345-8',
                    'role': 'PROFESSOR',
                    'confirm_user': False
                },
                {
                    'name': 'Bart Simpson',
                    'email': 'springfield@gmail.com',
                    'user_id': '93bc6ada-c0d1-7054-26ab-e17414c98aa7',
                    'ra': '29.89779-6',
                    'role': 'STUDENT',
                    'confirm_user': False
                }
            ],
            'message': 'All users returned successfully'
        }
