"""
Aplicação principal reorganizada seguindo DDD, SOLID e Clean Code
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
sys.path.append(os.path.dirname(os.path.dirname(__file__)))

from config import settings
from src.infrastructure.database.database import get_db
from src.presentation.controllers.user_controller import router as user_router
from src.presentation.controllers.message_controller import router as message_router

# Configurar logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Criar aplicação FastAPI
app = FastAPI(
    title="WhatsApp Platform API - DDD Architecture",
    description="API para plataforma de atendimento automático via WhatsApp com arquitetura DDD",
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

# Incluir routers
app.include_router(user_router)
app.include_router(message_router)

# Função de autenticação simples
async def verify_token(credentials: HTTPAuthorizationCredentials = Depends(security)):
    if credentials.credentials != "admin-token-example":
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token inválido",
            headers={"WWW-Authenticate": "Bearer"},
        )
    return credentials.credentials

# Rotas do Webhook (mantidas para compatibilidade)
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
async def receive_webhook(
    request: Request,
    db: Session = Depends(get_db)
):
    """Recebe webhooks do WhatsApp"""
    try:
        webhook_data = await request.json()
        logger.info(f"Webhook recebido: {webhook_data}")
        
        # TODO: Implementar processamento usando a nova arquitetura
        # Por enquanto, apenas log
        return {"status": "success", "message": "Webhook received"}
        
    except Exception as e:
        logger.error(f"Erro ao processar webhook: {e}")
        raise HTTPException(status_code=500, detail=str(e))

# Rotas básicas
@app.get("/")
async def root():
    """Endpoint raiz"""
    return {
        "message": "WhatsApp Platform API - DDD Architecture",
        "version": "2.0.0",
        "status": "online",
        "timestamp": datetime.now().isoformat(),
        "architecture": "DDD + SOLID + Clean Code"
    }

@app.get("/health")
async def health_check():
    """Verificação de saúde da API"""
    return {
        "status": "healthy",
        "timestamp": datetime.now().isoformat(),
        "version": "2.0.0",
        "architecture": "DDD"
    }

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
        "benefits": [
            "Separation of Concerns",
            "Testability",
            "Maintainability",
            "Scalability",
            "Flexibility"
        ]
    }

if __name__ == "__main__":
    print("🚀 Iniciando servidor da Plataforma WhatsApp - DDD Architecture")
    print(f"🌐 Servidor: http://{settings.HOST}:{settings.PORT}")
    print("📚 Documentação: http://localhost:8000/docs")
    
    uvicorn.run(
        "main:app",
        host=settings.HOST,
        port=settings.PORT,
        reload=settings.DEBUG
    )
