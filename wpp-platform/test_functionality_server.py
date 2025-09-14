"""
Servidor simplificado para teste da funcionalidade
"""
from fastapi import FastAPI, HTTPException, Depends, Request, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from sqlalchemy.orm import Session
from typing import Dict, Any, List
import logging
import uvicorn
from datetime import datetime
import sys
import os

# Adicionar o diretório raiz ao path
sys.path.append(os.path.dirname(os.path.dirname(__file__)))

from config import settings

# Configurar logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Criar aplicação FastAPI
app = FastAPI(
    title="WhatsApp Platform API - Teste Funcionalidade",
    description="API para teste da plataforma de atendimento automático via WhatsApp",
    version="2.0.0"
)

# Configurar CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Security
security = HTTPBearer()

# Função de autenticação simples
async def verify_token(credentials: HTTPAuthorizationCredentials = Depends(security)):
    if credentials.credentials != "admin-token-example":
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token inválido",
            headers={"WWW-Authenticate": "Bearer"},
        )
    return credentials.credentials

# Rotas básicas
@app.get("/")
async def root():
    """Endpoint raiz"""
    return {
        "message": "WhatsApp Platform API - Teste Funcionalidade",
        "version": "2.0.0",
        "status": "online",
        "timestamp": datetime.now().isoformat(),
        "architecture": "DDD + SOLID + Clean Code",
        "test_number": "+5585987049663"
    }

@app.get("/health")
async def health_check():
    """Verificação de saúde da API"""
    return {
        "status": "healthy",
        "timestamp": datetime.now().isoformat(),
        "version": "2.0.0",
        "architecture": "DDD",
        "test_number": "+5585987049663"
    }

@app.get("/test")
async def test_endpoint():
    """Endpoint de teste"""
    return {
        "message": "Teste funcionando!",
        "test_number": "+5585987049663",
        "formatted_number": "5585987049663",
        "display_format": "+55 (85) 98704-9663",
        "status": "ready_for_whatsapp_test"
    }

# Rotas do Webhook (simplificadas)
@app.get("/webhook")
async def verify_webhook(
    hub_mode: str,
    hub_challenge: str,
    hub_verify_token: str
):
    """Verifica o webhook do WhatsApp"""
    if hub_mode == "subscribe" and hub_verify_token == settings.WHATSAPP_WEBHOOK_VERIFY_TOKEN:
        logger.info("Webhook verificado com sucesso")
        return int(hub_challenge)
    else:
        logger.error("Falha na verificação do webhook")
        raise HTTPException(status_code=403, detail="Token de verificação inválido")

@app.post("/webhook")
async def receive_webhook(request: Request):
    """Recebe webhooks do WhatsApp"""
    try:
        webhook_data = await request.json()
        logger.info(f"Webhook recebido: {webhook_data}")
        
        # Processar webhook (implementação simplificada)
        return {"status": "success", "message": "Webhook received", "data": webhook_data}
        
    except Exception as e:
        logger.error(f"Erro ao processar webhook: {e}")
        raise HTTPException(status_code=500, detail=str(e))

# Rota de teste para envio de mensagem (simulada)
@app.post("/test/send-message")
async def test_send_message(
    phone_number: str = "+5585987049663",
    message: str = "Teste da plataforma WhatsApp!",
    token: str = Depends(verify_token)
):
    """Testa envio de mensagem (simulado)"""
    
    # Validação básica do número
    if not phone_number.startswith("+55"):
        raise HTTPException(status_code=400, detail="Número deve começar com +55")
    
    # Simular envio de mensagem
    result = {
        "status": "success",
        "message": "Mensagem simulada enviada",
        "phone_number": phone_number,
        "whatsapp_format": phone_number.replace("+", ""),
        "content": message,
        "timestamp": datetime.now().isoformat(),
        "note": "Para envio real, configure WhatsApp Business API"
    }
    
    logger.info(f"Mensagem simulada enviada para {phone_number}: {message}")
    
    return result

# Rota para criar usuário de teste
@app.post("/test/create-user")
async def test_create_user(
    phone_number: str = "+5585987049663",
    name: str = "Usuário Teste",
    email: str = "teste@example.com",
    token: str = Depends(verify_token)
):
    """Cria usuário de teste"""
    
    user_data = {
        "id": "test-user-id-123",
        "phone_number": phone_number,
        "name": name,
        "email": email,
        "is_active": True,
        "created_at": datetime.now().isoformat(),
        "whatsapp_id": phone_number.replace("+", ""),
        "display_format": f"+55 ({phone_number[3:5]}) {phone_number[5:10]}-{phone_number[10:]}"
    }
    
    logger.info(f"Usuário de teste criado: {name} - {phone_number}")
    
    return user_data

@app.get("/architecture")
async def get_architecture_info():
    """Informações sobre a arquitetura"""
    return {
        "architecture": "Domain-Driven Design (DDD)",
        "layers": {
            "domain": "Entidades, Value Objects, Domain Services, Repository Interfaces",
            "application": "Use Cases, DTOs, Application Interfaces",
            "infrastructure": "Repository Implementations, External Services, Database",
            "presentation": "Controllers, Schemas, Dependencies"
        },
        "principles": {
            "SOLID": "Single Responsibility, Open/Closed, Liskov Substitution, Interface Segregation, Dependency Inversion",
            "Clean Code": "Meaningful Names, Small Functions, No Duplication, Error Handling",
            "DDD": "Ubiquitous Language, Bounded Contexts, Domain Models"
        },
        "test_number": "+5585987049663",
        "status": "ready_for_testing"
    }

if __name__ == "__main__":
    print("🚀 Iniciando servidor de teste da Plataforma WhatsApp")
    print("📱 Número de teste: +5585987049663")
    print("🌐 Servidor: http://localhost:8000")
    print("📚 Documentação: http://localhost:8000/docs")
    
    uvicorn.run(
        "test_functionality_server:app",
        host=settings.HOST,
        port=settings.PORT,
        reload=settings.DEBUG
    )
