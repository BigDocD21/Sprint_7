import requests
import allure
from config import BASE_URL
from helpers import register_new_courier

@allure.feature("Создание курьера")
@allure.story("Позитивные сценарии")
@allure.title("Проверка успешного создания курьера")
def test_create_courier_success():
    with allure.step("Подготовка: создание курьера через вспомогательную функцию"):
        courier = register_new_courier()
        assert courier is not None, "Не удалось создать курьера (сервер не вернул 201)"

    with allure.step("Проверка наличия ID в данных курьера"):
        assert "id" in courier, "В ответе отсутствует ID курьера"