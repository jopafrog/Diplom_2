import allure
import data
import pytest
from api.api_user import ApiUser


class TestUser:
    @allure.title('Проверка регистрации пользователя')
    def test_registration_user_success(self, random_user):
        response = ApiUser.registration_user(random_user['email'], random_user['password'], random_user['name'])

        assert response.status_code == 200 and response.json()['success'] is True, \
            f'status code = {response.status_code} and success = {response.json()['success']}'

    @allure.title('Проверка регистрации, уже зарегистрированного пользователя')
    def test_registration_two_user_error_creation(self, random_user):
        ApiUser.registration_user(random_user['email'], random_user['password'], random_user['name'])
        response = ApiUser.registration_user(random_user['email'], random_user['password'], random_user['name'])

        assert response.status_code == 403 and response.json()['success'] is False, \
            f'status code = {response.status_code} and success = {response.json()['success']}'

    @allure.title('Проверка регистрации, одно из полей не заполнено')
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

    @allure.title('Проверка входа пользователя')
    def test_login_user_success(self, random_user):
        ApiUser.registration_user(random_user['email'], random_user['password'], random_user['name'])
        response = ApiUser.login_user(random_user['email'], random_user['password'])

        assert response.status_code == 200 and response.json()['success'] is True, \
            f'status code = {response.status_code} and success = {response.json()['success']}'

    @allure.title('Проверка входа с не правильным email')
    def test_login_bed_email_error_login(self, random_user):
        ApiUser.registration_user(random_user['email'], random_user['password'], random_user['name'])
        response = ApiUser.login_user('bed_email', random_user['password'])

        assert response.status_code == 401 and response.json()['success'] is False, \
            f'status code = {response.status_code} and success = {response.json()['success']}'

    @allure.title('Проверка входа с не правильным password')
    def test_login_bed_password_error_login(self, random_user):
        ApiUser.registration_user(random_user['email'], random_user['password'], random_user['name'])
        response = ApiUser.login_user(random_user['email'], 'bed_pass')

        assert response.status_code == 401 and response.json()['success'] is False, \
            f'status code = {response.status_code} and success = {response.json()['success']}'

    @allure.title('Проверка изменения email, с авторизацией')
    def test_modify_email_authorization_user_success(self, random_user):
        response = ApiUser.registration_user(random_user['email'], random_user['password'], random_user['name'])
        token = response.json()['accessToken']

        random_user['email'] = 'new_email_qwe123@yandex.ru'

        response = ApiUser.modify_user(random_user['email'], random_user['password'], token)

        assert response.status_code == 200 and response.json()['success'] is True, \
            f'status code = {response.status_code} and success = {response.json()['success']}'

    @allure.title('Проверка изменения password, с авторизацией')
    def test_modify_password_authorization_user_success(self, random_user):
        response = ApiUser.registration_user(random_user['email'], random_user['password'], random_user['name'])
        token = response.json()['accessToken']

        random_user['password'] = 'new_pass_QWERTY12345'

        response = ApiUser.modify_user(random_user['email'], random_user['password'], token)

        assert response.status_code == 200 and response.json()['success'] is True, \
            f'status code = {response.status_code} and success = {response.json()['success']}'

    @allure.title('Проверка изменения email и password, с авторизацией')
    def test_modify_email_and_password_authorization_user_success(self, random_user):
        response = ApiUser.registration_user(random_user['email'], random_user['password'], random_user['name'])
        token = response.json()['accessToken']

        random_user['email'] = 'new_email_qwe123@yandex.ru'
        random_user['password'] = 'new_pass_QWERTY12345'

        response = ApiUser.modify_user(random_user['email'], random_user['password'], token)

        assert response.status_code == 200 and response.json()['success'] is True, \
            f'status code = {response.status_code} and success = {response.json()['success']}'

    @allure.title('Проверка изменения email, БЕЗ авторизации')
    def test_modify_email_not_authorization_user_error_modify(self, random_user):
        ApiUser.registration_user(random_user['email'], random_user['password'], random_user['name'])

        token = 'no_token'
        new_email = 'newemail123456@yandex.ru'

        response = ApiUser.modify_user(new_email, random_user['password'], token)

        assert response.status_code == 401 and response.json()['success'] is False, \
            f'status code = {response.status_code} and success = {response.json()['success']}'

    @allure.title('Проверка изменения password, БЕЗ авторизации')
    def test_modify_pass_not_authorization_user_error_modify(self, random_user):
        ApiUser.registration_user(random_user['email'], random_user['password'], random_user['name'])

        token = 'no_token'
        new_pass = 'new_pass_QWERTY12345'

        response = ApiUser.modify_user(random_user['email'], new_pass, token)

        assert response.status_code == 401 and response.json()['success'] is False, \
            f'status code = {response.status_code} and success = {response.json()['success']}'

    @allure.title('Проверка изменения email и password, БЕЗ авторизации')
    def test_modify_email_and_pass_not_authorization_user_error_modify(self, random_user):
        ApiUser.registration_user(random_user['email'], random_user['password'], random_user['name'])

        token = 'no_token'
        new_email = 'newemail123456@yandex.ru'
        new_pass = 'new_pass_QWERTY12345'

        response = ApiUser.modify_user(new_email, new_pass, token)

        assert response.status_code == 401 and response.json()['success'] is False, \
            f'status code = {response.status_code} and success = {response.json()['success']}'
