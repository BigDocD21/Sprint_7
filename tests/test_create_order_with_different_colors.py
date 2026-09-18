import pytest
import requests
import allure
from config import BASE_URL

class TestOrderCreationPositive:
    @allure.feature("Создание заказа")
    @allure.story("Позитивные сценарии")
    @allure.title("Проверка создания заказа с различными вариантами цветов")
    @pytest.mark.parametrize("color_param", [
        ["BLACK"],
        ["GREY"],
        ["BLACK", "GREY"],
        []
    ])
    def test_create_order_with_colors(self, created_courier, color_param):
        with allure.step("Подготовка: получение данных тестового курьера из фикстуры"):
            courier = created_courier
        payload = {
            "street": "Lenina",
            "from": "10",
            "to": "20",
            "comment": "Test order",
            "color": color_param
        }
        with allure.step(f"Действие: отправка запроса на создание заказа (цвет: {color_param})"):
            response = requests.post(f"{BASE_URL}/orders", json=payload)
        try:
            response_data = response.json()
        except ValueError:
            response_data = {}
        assert response.status_code == 201, f"Ожидался статус 201, но получен {response.status_code}. Тело: {response.text}"
        
        assert "track" in response_data, "В ответе отсутствует обязательное поле 'track'"
        assert response_data["track"] is not None, "Поле 'track' пустое или равно None"
