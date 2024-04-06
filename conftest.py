import pytest
import data
from api.api_user import ApiUser


@pytest.fixture(scope='function')
def random_user():
    payload = ApiUser.create_random_user()

    yield payload

    response = ApiUser.login_user(email=payload['email'], password=payload['password'])
    token = response.json()['accessToken']
    ApiUser.delete_user(token)
