import requests
import allure
from config import BASE_URL
from helpers import get_fake_credentials

@allure.feature("Авторизация курьера")
@allure.story("Негативные сценарии")
@allure.title("Проверка ошибки при входе под несуществующим пользователем")
def test_courier_login_nonexistent_user():
    with allure.step("Подготовка: получение данных несуществующего пользователя"):
        credentials = get_fake_credentials()
        fake_login = credentials["login"]
        fake_password = credentials["password"]

    payload = {
        "login": fake_login,
        "password": fake_password
    }

    with allure.step("Действие: отправка запроса на авторизацию"):
        response = requests.post(f"{BASE_URL}/courier/login", json=payload)

    with allure.step("Проверка статуса ответа (должен быть не 200)"):
        assert response.status_code != 200, f"Ожидалась ошибка авторизации, но получен статус {response.status_code}"

    with allure.step("Проверка тела ответа на наличие сообщения об ошибке"):
        response_body = response.json()
        assert "message" in response_body or "error" in response_body, \
            "В ответе отсутствует сообщение об ошибке."