import pytest
import requests
from config import BASE_URL
from helpers import get_fake_credentials

@pytest.fixture
def created_courier():
    credentials = get_fake_credentials()
    create_payload = {
        "login": credentials["login"],
        "password": credentials["password"]
    }
    
    create_response = requests.post(f"{BASE_URL}/courier", json=create_payload)
    assert create_response.status_code in [200, 201], f"Не удалось создать курьера: {create_response.text}"
   
    login_payload = {
        "login": credentials["login"],
        "password": credentials["password"]
    }
    
    login_response = requests.post(f"{BASE_URL}/courier/login", json=login_payload)
    assert login_response.status_code == 200, f"Не удалось залогиниться для получения ID: {login_response.text}"
    
    login_data = login_response.json()
    courier_id = login_data.get("id")
    
    assert courier_id is not None, "Не удалось получить ID курьера даже через авторизацию!"

    yield {
        "id": courier_id,
        "login": credentials["login"],
        "password": credentials["password"]
    }
    delete_payload = {"id": courier_id}
    
    try:
        delete_response = requests.delete(f"{BASE_URL}/courier", json=delete_payload)
        if delete_response.status_code not in [200, 204]:
            pass 
    except Exception as e:
        pass
    