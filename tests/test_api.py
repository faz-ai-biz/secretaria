import requests
import json
from datetime import datetime, timedelta

# Configuração base
BASE_URL = "http://localhost:8000/api/v1"
HEADERS = {
    "Content-Type": "application/json"
}

def test_create_cliente():
    """Testa a criação de um novo cliente"""
    email = "teste@exemplo.com"
    data = {
        "email": email,
        "credentials": None
    }
    
    response = requests.post(
        f"{BASE_URL}/clientes/{email}",
        headers=HEADERS,
        json=data
    )
    print("Criar Cliente:", response.status_code)
    print(response.json())
    return response.json()

def test_get_cliente(email):
    """Testa a busca de um cliente"""
    response = requests.get(
        f"{BASE_URL}/clientes/{email}",
        headers=HEADERS
    )
    print("Buscar Cliente:", response.status_code)
    print(response.json())
    return response.json()

def test_list_clientes():
    """Testa a listagem de clientes"""
    response = requests.get(
        f"{BASE_URL}/clientes/",
        headers=HEADERS
    )
    print("Listar Clientes:", response.status_code)
    print(response.json())
    return response.json()

def test_update_cliente(email):
    """Testa a atualização de um cliente"""
    data = {
        "credentials": {"token": "teste_token"},
        "expiry": (datetime.now() + timedelta(days=7)).isoformat()
    }
    
    response = requests.put(
        f"{BASE_URL}/clientes/{email}",
        headers=HEADERS,
        json=data
    )
    print("Atualizar Cliente:", response.status_code)
    print(response.json())
    return response.json()

def test_google_calendar_auth(email):
    """Testa a autorização do Google Calendar"""
    response = requests.get(
        f"{BASE_URL}/calendar/authorize/{email}",
        headers=HEADERS
    )
    print("Autorização Google Calendar:", response.status_code)
    print(response.json())
    return response.json()

if __name__ == "__main__":
    # Email para teste
    test_email = "teste@exemplo.com"
    
    # Executar testes
    print("\n1. Criando novo cliente...")
    cliente = test_create_cliente()
    
    print("\n2. Buscando cliente...")
    cliente = test_get_cliente(test_email)
    
    print("\n3. Listando todos os clientes...")
    clientes = test_list_clientes()
    
    print("\n4. Atualizando cliente...")
    cliente = test_update_cliente(test_email)
    
    print("\n5. Testando autorização Google Calendar...")
    auth = test_google_calendar_auth(test_email) 