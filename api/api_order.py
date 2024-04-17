import allure
import requests
import request_address
from random import choice


class ApiOrder:
    @staticmethod
    @allure.step('Создать заказ')
    def create_order(ingredients: list):
        payload = {"ingredients": ingredients}

        response = requests.post(request_address.CREATE_ORDER, data=payload)
        return response

    @staticmethod
    @allure.step('Создать заказ под авторизованным пользователем')
    def create_order_authorization_user(ingredients: list, token):
        payload = {"ingredients": ingredients}
        header = {"Authorization": token}

        response = requests.post(request_address.CREATE_ORDER, data=payload, headers=header)
        return response

    @staticmethod
    @allure.step('Получить список случайных ингредиентов')
    def get_random_ingredients():
        response = requests.get(request_address.GET_INGREDIENTS)
        ingredients = []

        for i in response.json()['data']:
            ingredients.append(i['_id'])

        random_ingredients = []
        for i in range(3):
            random_ingredients.append(choice(ingredients))

        return random_ingredients

    @staticmethod
    @allure.step('Получить заказы пользователя')
    def get_orders_owner(token: str):
        header = {"Authorization": token}

        response = requests.get(request_address.CREATE_ORDER, headers=header)
        return response
