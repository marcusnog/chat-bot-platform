"""
Teste de autenticação
"""
import requests
import json

def test_login():
    """Testa o endpoint de login"""
    url = "http://localhost:8000/auth/login"
    
    # Dados de teste
    test_users = [
        {"email": "admin@whatsapp-platform.com", "password": "admin123"},
        {"email": "demo@whatsapp-platform.com", "password": "demo123"},
        {"email": "teste@whatsapp-platform.com", "password": "teste123"}
    ]
    
    for user_data in test_users:
        try:
            print(f"\n🔐 Testando login: {user_data['email']}")
            response = requests.post(url, json=user_data)
            
            if response.status_code == 200:
                data = response.json()
                print(f"✅ Login bem-sucedido!")
                print(f"   Token: {data['token'][:50]}...")
                print(f"   Usuário: {data['user']['name']}")
                print(f"   Admin: {data['user']['is_admin']}")
            else:
                print(f"❌ Erro no login: {response.status_code}")
                print(f"   Resposta: {response.text}")
                
        except Exception as e:
            print(f"❌ Erro de conexão: {e}")

if __name__ == "__main__":
    test_login()
