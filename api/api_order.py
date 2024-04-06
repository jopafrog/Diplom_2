import requests
import request_address
from random import choice


class ApiOrder:
    @staticmethod
    def create_order(ingredients: list):
        payload = {"ingredients": ingredients}

        response = requests.post(request_address.CREATE_ORDER, data=payload)
        return response

    @staticmethod
    def create_order_authorization_user(ingredients: list, token):
        payload = {"ingredients": ingredients}
        header = {"Authorization": token}

        response = requests.post(request_address.CREATE_ORDER, data=payload, headers=header)
        return response


    @staticmethod
    def get_random_ingredients():
        response = requests.get(request_address.GET_INGREDIENTS)
        ingredients = []

        for i in response.json()['data']:
            ingredients.append(i['_id'])

        random_ingredients = []
        for i in range(3):
            random_ingredients.append(choice(ingredients))

        return random_ingredients
