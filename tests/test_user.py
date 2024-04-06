import data
import pytest
from api.api_user import ApiUser


class TestUser:
    def test_registration_user_success(self, random_user):
        response = ApiUser.registration_user(random_user['email'], random_user['password'], random_user['name'])

        assert response.status_code == 200 and response.json()['success'] is True, \
            f'status code = {response.status_code} and success = {response.json()['success']}'

    def test_registration_two_user_error_creation(self, random_user):
        ApiUser.registration_user(random_user['email'], random_user['password'], random_user['name'])
        response = ApiUser.registration_user(random_user['email'], random_user['password'], random_user['name'])

        assert response.status_code == 403 and response.json()['success'] is False, \
            f'status code = {response.status_code} and success = {response.json()['success']}'

    @pytest.mark.parametrize(
        'email, password, name',
        [
            (data.TEST_USER_EMAIL, data.TEST_USER_PASS, ''),
            (data.TEST_USER_EMAIL, '', data.TEST_USER_NAME),
            ('', data.TEST_USER_PASS, data.TEST_USER_NAME)
        ]
    )
    def test_registration_bed_parameter_error_creation(self, email, password, name):
        response = ApiUser.registration_user(email, password, name)

        assert response.status_code == 403 and response.json()['success'] is False, \
            f'status code = {response.status_code} and success = {response.json()['success']}'

    # Этот тест нужно удалить
    def test_delete_user(self):
        email = data.TEST_USER_EMAIL
        password = data.TEST_USER_PASS
        name = data.TEST_USER_NAME

        response = ApiUser.registration_user(email=email, password=password, name=name)
        print(response.json())
        token = response.json()['accessToken']

        response = ApiUser.delete_user(token)

        assert response.status_code == 202 and response.json()['success'] is True

    def test_login_user_success(self, random_user):
        ApiUser.registration_user(random_user['email'], random_user['password'], random_user['name'])
        response = ApiUser.login_user(random_user['email'], random_user['password'])

        assert response.status_code == 200 and response.json()['success'] is True, \
            f'status code = {response.status_code} and success = {response.json()['success']}'

    @pytest.mark.parametrize('param', ['bed_email', 'bed_pass'])
    def test_login_bed_parameters_error_login(self, random_user, param):
        ApiUser.registration_user(random_user['email'], random_user['password'], random_user['name'])
        response = 0

        if param == 'bed_email':
            response = ApiUser.login_user(param, random_user['password'])
        elif param == 'bed_pass':
            response = ApiUser.login_user(random_user['email'], param)

        assert response.status_code == 401 and response.json()['success'] is False, \
            f'status code = {response.status_code} and success = {response.json()['success']}'

    @pytest.mark.parametrize('param', ['new_email', 'new_password', 'all_modify'])
    def test_modify_authorization_user_success(self, random_user, param):
        response = ApiUser.registration_user(random_user['email'], random_user['password'], random_user['name'])
        token = response.json()['accessToken']

        if param == 'new_email':
            random_user['email'] = 'newemail123456@yandex.ru'
        elif param == 'new_password':
            random_user['password'] = 'newpassQWERTY12345'
        elif param == 'all_modify':
            random_user['email'] = 'newemail123456@yandex.ru'
            random_user['password'] = 'newpassQWERTY12345'

        response = ApiUser.modify_user(random_user['email'], random_user['password'], token)

        assert response.status_code == 200 and response.json()['success'] is True, \
            f'status code = {response.status_code} and success = {response.json()['success']}'

    @pytest.mark.parametrize('param', ['new_email', 'new_password', 'all_modify'])
    def test_modify_not_authorization_user_error_modify(self, random_user, param):
        ApiUser.registration_user(random_user['email'], random_user['password'], random_user['name'])

        token = 'notoken'
        new_email = random_user['email']
        new_pass = random_user['password']

        if param == 'new_email':
            new_email = 'newemail123456@yandex.ru'
        elif param == 'new_password':
            new_pass = 'newpassQWERTY12345'
        elif param == 'all_modify':
            new_email = 'newemail123456@yandex.ru'
            new_pass = 'newpassQWERTY12345'

        response = ApiUser.modify_user(new_email, new_pass, token)

        assert response.status_code == 401 and response.json()['success'] is False, \
            f'status code = {response.status_code} and success = {response.json()['success']}'
