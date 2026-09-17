import pytest
import requests
import allure
from config import BASE_URL
from helpers import register_new_courier

@allure.feature("Создание заказа")
@allure.story("Позитивные сценарии")
@allure.title("Проверка создания заказа с различными вариантами цветов")
@pytest.mark.parametrize("color_param", [
    ["BLACK"],
    ["GREY"],
    ["BLACK", "GREY"],
    []
])
def test_create_order_with_colors(color_param):
    with allure.step("Подготовка: создание тестового курьера"):
        courier = register_new_courier()
        assert courier is not None, "Не удалось создать тестового курьера"

    payload = {
        "street": "Lenina",
        "from": "10",
        "to": "20",
        "comment": "Test order",
        "color": color_param
    }

    with allure.step(f"Действие: отправка запроса на создание заказа (цвет: {color_param})"):
        response = requests.post(f"{BASE_URL}/orders", json=payload)

    with allure.step("Проверка статуса ответа (ожидается 201)"):
        assert response.status_code == 201, f"Ожидался статус 201, но получен {response.status_code}"

    response_data = response.json()

    with allure.step("Проверка наличия поля 'track' в ответе"):
        assert "track" in response_data, "В ответе отсутствует обязательное поле 'track'"
        assert response_data["track"] is not None, "Поле 'track' пустое"