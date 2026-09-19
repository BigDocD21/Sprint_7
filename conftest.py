import pytest
import requests
import allure
from config import BASE_URL
from helpers import get_fake_credentials

@pytest.fixture
def created_courier():
    credentials = get_fake_credentials()

    with allure.step("Фикстура: создание курьера"):
        create_payload = {
            "login": credentials["login"],
            "password": credentials["password"]
        }
        
        try:
            create_response = requests.post(f"{BASE_URL}/courier", json=create_payload)
        except requests.ConnectionError:
            pytest.fail("Не удалось подключиться к серверу при создании курьера.")

        if create_response.status_code not in [200, 201]:
            pytest.fail(
                f"Не удалось создать курьера. Статус: {create_response.status_code}. "
                f"Ответ: {create_response.text}"
            )

    with allure.step("Фикстура: авторизация для получения ID курьера"):
        login_payload = {
            "login": credentials["login"],
            "password": credentials["password"]
        }
        
        try:
            login_response = requests.post(f"{BASE_URL}/courier/login", json=login_payload)
        except requests.ConnectionError:
            pytest.fail("Не удалось подключиться к серверу при получении ID курьера.")

        if login_response.status_code != 200:
            pytest.fail(
                f"Не удалось залогиниться для получения ID. Статус: {login_response.status_code}. "
                f"Ответ: {login_response.text}"
            )
        
        login_data = login_response.json()
        courier_id = login_data.get("id")

        if courier_id is None:
            pytest.fail("В ответе на авторизацию отсутствует поле 'id'.")

    yield {
        "id": courier_id,
        "login": credentials["login"],
        "password": credentials["password"]
    }

    with allure.step("Фикстура: удаление курьера"):
        delete_payload = {"id": courier_id}
        
        try:
            delete_response = requests.delete(f"{BASE_URL}/courier", json=delete_payload)
            if delete_response.status_code not in [200, 204]:
                pass
        except Exception:
            pass
