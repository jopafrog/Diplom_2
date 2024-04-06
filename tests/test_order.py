import pytest
from api.api_order import ApiOrder
from api.api_user import ApiUser


class TestOrder:
    def test_create_order_success(self):
        ingredients = ApiOrder.get_random_ingredients()
        response = ApiOrder.create_order(ingredients)

        print(ingredients)

        assert response.status_code == 200 and response.json()['success'] is True, \
            f'status code = {response.status_code} and success = {response.json()['success']}'

    @pytest.mark.parametrize(
        'ingredients',
        [
            ['sdofns', 'slkfgkmse'],
            ['', '  ']
        ]
    )
    def test_create_order_incorrect_ingredient_error_creation(self, ingredients):
        response = ApiOrder.create_order(ingredients)

        assert response.status_code == 500

    def test_create_order_empty_ingredients_error_creation(self):
        ingredients = []
        response = ApiOrder.create_order(ingredients)

        assert response.status_code == 400 and response.json()['success'] is False, \
            f'status code = {response.status_code} and success = {response.json()['success']}'

    def test_create_order_authorization_user_success(self, random_user):
        response = ApiUser.registration_user(random_user['email'], random_user['password'], random_user['name'])
        token = response.json()['accessToken']
        ingredients = ApiOrder.get_random_ingredients()

        response = ApiOrder.create_order_authorization_user(ingredients, token)
        assert response.status_code == 200 and response.json()['order']['owner']['name'] == random_user['name'], \
            f'status code = {response.status_code} and Owner name = {response.json()['order']['owner']['name']}'
