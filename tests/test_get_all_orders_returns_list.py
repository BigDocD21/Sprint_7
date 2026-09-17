import requests
import allure
from config import BASE_URL

@allure.feature("Список заказов")
@allure.story("Позитивные сценарии")
@allure.title("Проверка возврата списка заказов")
def test_get_all_orders_returns_list():
    with allure.step("Действие: отправка GET-запроса для получения списка заказов"):
        response = requests.get(f"{BASE_URL}/orders")

    with allure.step("Проверка статуса ответа (ожидается 200)"):
        assert response.status_code == 200

    with allure.step("Извлечение списка заказов из ответа сервера"):
        data = response.json()
        orders_list = data["orders"]

    with allure.step("Проверка: извлеченные данные являются списком"):
        assert isinstance(orders_list, list)

    with allure.step("Проверка: первый элемент списка является объектом (словарем)"):
        assert isinstance(orders_list[0], dict)