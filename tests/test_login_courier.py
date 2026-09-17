import requests
import allure
from config import BASE_URL
from helpers import register_new_courier

@allure.feature("Авторизация курьера")
@allure.story("Позитивные сценарии")
@allure.title("Проверка успешной авторизации курьера и получения ID")
def test_courier_login_success():
    with allure.step("Подготовка: создание тестового курьера"):
        courier = register_new_courier()
        assert courier is not None
    
    payload = {
        "login": courier["login"],
        "password": courier["password"]
    }
    
    with allure.step("Действие: отправка запроса на авторизацию"):
        response = requests.post(f"{BASE_URL}/courier/login", json=payload)
    
    with allure.step("Проверка статуса ответа (ожидается 200)"):
        assert response.status_code == 200
    
    response_data = response.json()
    
    with allure.step("Проверка наличия поля 'id' в ответе"):
        assert "id" in response_data
        assert response_data["id"] is not None