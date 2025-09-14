#!/usr/bin/env python3
"""
Teste de funcionalidade completa da plataforma
"""

import requests
import json
from datetime import datetime

# Configurações
BASE_URL = "http://localhost:8000"
TEST_PHONE = "+5585987049663"

def test_server_health():
    """Testa se o servidor está funcionando"""
    print("🏥 Testando health check...")
    
    try:
        response = requests.get(f"{BASE_URL}/health", timeout=5)
        if response.status_code == 200:
            data = response.json()
            print(f"   ✅ Servidor online: {data.get('status', 'unknown')}")
            return True
        else:
            print(f"   ❌ Erro: {response.status_code}")
            return False
    except Exception as e:
        print(f"   ❌ Erro de conexão: {e}")
        return False

def test_root_endpoint():
    """Testa endpoint raiz"""
    print("\n🏠 Testando endpoint raiz...")
    
    try:
        response = requests.get(f"{BASE_URL}/", timeout=5)
        if response.status_code == 200:
            data = response.json()
            print(f"   ✅ API funcionando: {data.get('message', 'unknown')}")
            print(f"   📱 Número de teste: {data.get('test_number', 'unknown')}")
            return True
        else:
            print(f"   ❌ Erro: {response.status_code}")
            return False
    except Exception as e:
        print(f"   ❌ Erro: {e}")
        return False

def test_docs():
    """Testa documentação da API"""
    print("\n📚 Testando documentação...")
    
    try:
        response = requests.get(f"{BASE_URL}/docs", timeout=5)
        if response.status_code == 200:
            print("   ✅ Documentação disponível")
            return True
        else:
            print(f"   ❌ Erro: {response.status_code}")
            return False
    except Exception as e:
        print(f"   ❌ Erro: {e}")
        return False

def test_openapi():
    """Testa especificação OpenAPI"""
    print("\n🔧 Testando especificação OpenAPI...")
    
    try:
        response = requests.get(f"{BASE_URL}/openapi.json", timeout=5)
        if response.status_code == 200:
            data = response.json()
            print(f"   ✅ OpenAPI disponível: {data.get('info', {}).get('title', 'unknown')}")
            return True
        else:
            print(f"   ❌ Erro: {response.status_code}")
            return False
    except Exception as e:
        print(f"   ❌ Erro: {e}")
        return False

def test_user_endpoints():
    """Testa endpoints de usuário"""
    print(f"\n👤 Testando endpoints de usuário...")
    
    headers = {
        "Authorization": "Bearer admin-token-example",
        "Content-Type": "application/json"
    }
    
    # Teste criação de usuário
    try:
        user_data = {
            "phone_number": TEST_PHONE,
            "name": "Usuário Teste",
            "email": "teste@example.com"
        }
        
        response = requests.post(
            f"{BASE_URL}/users/",
            json=user_data,
            headers=headers,
            timeout=5
        )
        
        if response.status_code in [200, 201]:
            data = response.json()
            print(f"   ✅ Usuário criado: {data.get('name', 'unknown')}")
            return True
        else:
            print(f"   ❌ Erro ao criar usuário: {response.status_code}")
            print(f"   📝 Resposta: {response.text[:100]}...")
            return False
            
    except Exception as e:
        print(f"   ❌ Erro: {e}")
        return False

def test_message_endpoints():
    """Testa endpoints de mensagem"""
    print(f"\n💬 Testando endpoints de mensagem...")
    
    headers = {
        "Authorization": "Bearer admin-token-example",
        "Content-Type": "application/json"
    }
    
    # Teste envio de mensagem
    try:
        message_data = {
            "phone_number": TEST_PHONE,
            "content": "Teste da plataforma WhatsApp!",
            "message_type": "text"
        }
        
        response = requests.post(
            f"{BASE_URL}/messages/send",
            json=message_data,
            headers=headers,
            timeout=5
        )
        
        if response.status_code in [200, 201]:
            data = response.json()
            print(f"   ✅ Mensagem enviada: {data.get('status', 'unknown')}")
            return True
        else:
            print(f"   ❌ Erro ao enviar mensagem: {response.status_code}")
            print(f"   📝 Resposta: {response.text[:100]}...")
            return False
            
    except Exception as e:
        print(f"   ❌ Erro: {e}")
        return False

def test_webhook():
    """Testa webhook"""
    print(f"\n🔗 Testando webhook...")
    
    try:
        params = {
            "hub_mode": "subscribe",
            "hub_challenge": "12345",
            "hub_verify_token": "seu_webhook_verify_token_aqui"
        }
        
        response = requests.get(f"{BASE_URL}/webhook", params=params, timeout=5)
        
        if response.status_code == 200:
            print("   ✅ Webhook funcionando")
            return True
        else:
            print(f"   ❌ Erro no webhook: {response.status_code}")
            return False
            
    except Exception as e:
        print(f"   ❌ Erro: {e}")
        return False

def main():
    """Função principal de teste"""
    print("🚀 Teste de Funcionalidade Completa - Plataforma WhatsApp")
    print("=" * 60)
    print(f"📱 Número de teste: {TEST_PHONE}")
    print(f"🌐 Servidor: {BASE_URL}")
    print("=" * 60)
    
    tests = [
        ("Health Check", test_server_health),
        ("Endpoint Raiz", test_root_endpoint),
        ("Documentação", test_docs),
        ("OpenAPI", test_openapi),
        ("Usuários", test_user_endpoints),
        ("Mensagens", test_message_endpoints),
        ("Webhook", test_webhook)
    ]
    
    passed = 0
    total = len(tests)
    
    for test_name, test_func in tests:
        try:
            if test_func():
                passed += 1
        except Exception as e:
            print(f"   ❌ Erro inesperado em {test_name}: {e}")
    
    print("\n" + "=" * 60)
    print(f"📊 Resultado: {passed}/{total} testes passaram")
    
    if passed == total:
        print("🎉 TODOS OS TESTES PASSARAM!")
        print("✅ A plataforma está 100% funcional!")
        
        print("\n📋 Funcionalidades Confirmadas:")
        print("   ✅ Servidor online e respondendo")
        print("   ✅ API endpoints funcionando")
        print("   ✅ Documentação disponível")
        print("   ✅ Criação de usuários")
        print("   ✅ Envio de mensagens")
        print("   ✅ Webhook configurado")
        
        print(f"\n🎯 Pronto para teste real com número: {TEST_PHONE}")
        print("🌐 Documentação: http://localhost:8000/docs")
        
    else:
        print("❌ Alguns testes falharam.")
        print("🔧 Verifique os erros acima e corrija antes de prosseguir.")
    
    return passed == total

if __name__ == "__main__":
    success = main()
    exit(0 if success else 1)
