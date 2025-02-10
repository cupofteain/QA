import requests
import pytest

def test_get_reviews():

    print("Тестирование GET-запроса для получения списка отзывов.Начало url = https://api-stage.ecar.kz/review/list?PageNum=1&PageSize=20&OrderBy=asc") 
    """Тестирование GET-запроса для получения списка отзывов."""
    url = "https://api-stage.ecar.kz/review/list?PageNum=1&PageSize=20&OrderBy=asc"
    
    response = requests.get(url)

    print(f"Status Code: {response.status_code}")

    message = response.json().get('message', 'Сообщение не найдено')
    print(f"Response Message: {message}")
    
    assert response.status_code == 200, "Статус код не равен 200"

    json_data = response.json()
    assert "result" in json_data, "Ключ 'result' отсутствует в ответе"
    print("Тестирование GET-запроса для получения списка отзывов.Конец")

#/////////////////////////////////////////////////////////////////////////////////////
   
    print("Тестирование GET-запроса для получения списка отзывов.Начало url = https://api-stage.ecar.kz/review/list?PageNum=1&PageSize=20&OrderBy=desc")
    url = "https://api-stage.ecar.kz/review/list?PageNum=1&PageSize=20&OrderBy=desc" 
    
    response = requests.get(url)

    print(f"Status Code: {response.status_code}")
    message = response.json().get('message', 'Сообщение не найдено')
    print(f"Response Message: {message}")
    assert response.status_code == 200, "Статус код не равен 200"

    json_data = response.json()
    assert "result" in json_data, "Ключ 'result' отсутствует в ответе"
    print("Тестирование GET-запроса для получения списка отзывов.Конец")

#/////////////////////////////////////////////////////////////////////////////////////

    print("Тестирование GET-запроса для получения списка отзывов.Начало url = https://api-stage.ecar.kz/review/list?PageNum=1&PageSize=20&OrderBy=Status")
    url = "https://api-stage.ecar.kz/review/list?PageNum=1&PageSize=20&OrderBy=Status"
    
    response = requests.get(url)

    print(f"Status Code: {response.status_code}")
    message = response.json().get('message', 'Сообщение не найдено')
    print(f"Response Message: {message}")
    assert response.status_code == 200, "Статус код не равен 200"

    json_data = response.json()
    assert "result" in json_data, "Ключ 'result' отсутствует в ответе"
    print("Тестирование GET-запроса для получения списка отзывов.Конец")

#/////////////////////////////////////////////////////////////////////////////////////

    print("Тестирование GET-запроса для получения списка отзывов.Начало url = https://api-stage.ecar.kz/review/list?PageNum=1&PageSize=20&OrderBy=DatePlaced")
    url = "https://api-stage.ecar.kz/review/list?PageNum=1&PageSize=20&OrderBy=DatePlaced"
    
    
    response = requests.get(url)

    print(f"Status Code: {response.status_code}")
    message = response.json().get('message', 'Сообщение не найдено')
    print(f"Response Message: {message}")
    assert response.status_code == 200, "Статус код не равен 200"

    json_data = response.json()
    assert "result" in json_data, "Ключ 'result' отсутствует в ответе"
    print("Тестирование GET-запроса для получения списка отзывов.Конец")