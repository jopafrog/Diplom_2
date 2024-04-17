import string
from random import choice
import allure
import requests
import request_address


class ApiUser:
    @staticmethod
    @allure.step('Создать случайные данные пользователя')
    def create_random_user():
        def generate_random_string(length):
            letters = string.ascii_lowercase
            random_string = ''.join(choice(letters) for i in range(length))
            return random_string

        payload = {
            "email": generate_random_string(6) + '@yandex.ru',
            "password": generate_random_string(6),
            "name": generate_random_string(6)
        }

        return payload

    @staticmethod
    @allure.step('Регистрация пользователя')
    def registration_user(email: str, password: str, name: str):
        payload = {
            "email": email,
            "password": password,
            "name": name
        }

        response = requests.post(request_address.USER_REGISTRATION, data=payload)
        return response

    @staticmethod
    @allure.step('Вход пользователя в систему')
    def login_user(email: str, password: str):
        payload = {
            "email": email,
            "password": password
        }

        response = requests.post(request_address.USER_LOGIN, data=payload)
        return response

    @staticmethod
    @allure.step('Удаление пользователя')
    def delete_user(token: str):
        headers = {"Authorization": token}

        response = requests.delete(request_address.USER, headers=headers)
        return response

    @staticmethod
    @allure.step('Изменение данных пользователя')
    def modify_user(email: str, password: str, token: str):
        payload = {
            "email": email,
            "password": password
        }
        header = {"Authorization": token}

        response = requests.patch(request_address.USER, data=payload, headers=header)
        return response
