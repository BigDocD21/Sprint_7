import requests
import allure
from config import BASE_URL
from helpers import register_new_courier

@allure.feature("Авторизация курьера")
@allure.story("Негативные сценарии")
@allure.title("Проверка ошибки при неверном пароле")
def test_courier_login_wrong_password():
    with allure.step("Подготовка: создание валидного курьера"):
        courier = register_new_courier()
        assert courier is not None

    payload = {
        "login": courier["login"],
        "password": "wrong_password_123"
    }

    with allure.step("Действие: отправка запроса на авторизацию с неверным паролем"):
        response = requests.post(f"{BASE_URL}/courier/login", json=payload)

    with allure.step("Проверка статуса ответа (ожидается 404)"):
        assert response.status_code == 404

    with allure.step("Проверка тела ответа на соответствие тексту ошибки"):
        response_body = response.json()
        assert "message" in response_body
        assert response_body["message"] == "Учетная запись не найдена"