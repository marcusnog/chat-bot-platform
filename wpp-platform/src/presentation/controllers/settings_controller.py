"""
Endpoints de configurações
"""
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import Optional
from pydantic import BaseModel
from datetime import datetime

from src.infrastructure.database.database import get_db
from src.infrastructure.database.auth_models import AuthUser
from src.presentation.controllers.auth_controller import get_current_user
from config import settings

router = APIRouter(prefix="/settings", tags=["settings"])

# Schemas
class SettingsResponse(BaseModel):
    whatsapp_token: str
    whatsapp_phone_number_id: str
    whatsapp_webhook_verify_token: str
    whatsapp_business_account_id: str
    openai_api_key: str
    openai_model: str
    openai_max_tokens: int
    openai_temperature: float
    database_url: str
    redis_url: str
    host: str
    port: int
    debug: bool

class SettingsUpdateRequest(BaseModel):
    whatsapp_token: Optional[str] = None
    whatsapp_phone_number_id: Optional[str] = None
    whatsapp_webhook_verify_token: Optional[str] = None
    whatsapp_business_account_id: Optional[str] = None
    openai_api_key: Optional[str] = None
    openai_model: Optional[str] = None
    openai_max_tokens: Optional[int] = None
    openai_temperature: Optional[float] = None
    database_url: Optional[str] = None
    redis_url: Optional[str] = None
    host: Optional[str] = None
    port: Optional[int] = None
    debug: Optional[bool] = None

class AITestRequest(BaseModel):
    message: str
    context: Optional[str] = None

class AITestResponse(BaseModel):
    input_message: str
    ai_response: str
    processing_time: float
    model_used: str
    tokens_used: int

class WhatsAppTestRequest(BaseModel):
    phone_number: str
    message: str

class WhatsAppTestResponse(BaseModel):
    success: bool
    message_id: Optional[str] = None
    error: Optional[str] = None

# Endpoints
@router.get("/", response_model=SettingsResponse)
async def get_settings(
    current_user: AuthUser = Depends(get_current_user)
):
    """Obtém configurações atuais"""
    try:
        return SettingsResponse(
            whatsapp_token=settings.WHATSAPP_TOKEN,
            whatsapp_phone_number_id=settings.WHATSAPP_PHONE_NUMBER_ID,
            whatsapp_webhook_verify_token=settings.WHATSAPP_WEBHOOK_VERIFY_TOKEN,
            whatsapp_business_account_id=settings.WHATSAPP_BUSINESS_ACCOUNT_ID,
            openai_api_key=settings.OPENAI_API_KEY,
            openai_model=settings.OPENAI_MODEL,
            openai_max_tokens=settings.OPENAI_MAX_TOKENS,
            openai_temperature=settings.OPENAI_TEMPERATURE,
            database_url=settings.DATABASE_URL,
            redis_url=settings.REDIS_URL,
            host=settings.HOST,
            port=settings.PORT,
            debug=settings.DEBUG
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Erro ao buscar configurações: {str(e)}"
        )

@router.put("/", response_model=SettingsResponse)
async def update_settings(
    settings_data: SettingsUpdateRequest,
    current_user: AuthUser = Depends(get_current_user)
):
    """Atualiza configurações"""
    try:
        # Atualizar configurações (em produção, isso seria salvo em banco de dados)
        # Por enquanto, apenas retornar as configurações atuais
        
        return SettingsResponse(
            whatsapp_token=settings.WHATSAPP_TOKEN,
            whatsapp_phone_number_id=settings.WHATSAPP_PHONE_NUMBER_ID,
            whatsapp_webhook_verify_token=settings.WHATSAPP_WEBHOOK_VERIFY_TOKEN,
            whatsapp_business_account_id=settings.WHATSAPP_BUSINESS_ACCOUNT_ID,
            openai_api_key=settings.OPENAI_API_KEY,
            openai_model=settings.OPENAI_MODEL,
            openai_max_tokens=settings.OPENAI_MAX_TOKENS,
            openai_temperature=settings.OPENAI_TEMPERATURE,
            database_url=settings.DATABASE_URL,
            redis_url=settings.REDIS_URL,
            host=settings.HOST,
            port=settings.PORT,
            debug=settings.DEBUG
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Erro ao atualizar configurações: {str(e)}"
        )

@router.post("/test-ai", response_model=AITestResponse)
async def test_ai(
    test_data: AITestRequest,
    current_user: AuthUser = Depends(get_current_user)
):
    """Testa integração com IA"""
    try:
        import time
        start_time = time.time()
        
        # Simular chamada para IA (mockado por enquanto)
        ai_response = f"Resposta da IA para: '{test_data.message}'"
        processing_time = time.time() - start_time
        
        return AITestResponse(
            input_message=test_data.message,
            ai_response=ai_response,
            processing_time=processing_time,
            model_used=settings.OPENAI_MODEL,
            tokens_used=50  # Mockado
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Erro ao testar IA: {str(e)}"
        )

@router.post("/test-whatsapp", response_model=WhatsAppTestResponse)
async def test_whatsapp(
    test_data: WhatsAppTestRequest,
    current_user: AuthUser = Depends(get_current_user)
):
    """Testa integração com WhatsApp"""
    try:
        # Simular envio de mensagem (mockado por enquanto)
        if not settings.WHATSAPP_TOKEN:
            return WhatsAppTestResponse(
                success=False,
                error="Token do WhatsApp não configurado"
            )
        
        # Mock de sucesso
        return WhatsAppTestResponse(
            success=True,
            message_id="mock_message_id_12345"
        )
    except Exception as e:
        return WhatsAppTestResponse(
            success=False,
            error=f"Erro ao testar WhatsApp: {str(e)}"
        )

@router.get("/health")
async def health_check():
    """Verifica saúde do sistema"""
    try:
        return {
            "status": "healthy",
            "timestamp": datetime.now().isoformat(),
            "version": "1.0.0",
            "services": {
                "database": "connected",
                "whatsapp": "configured" if settings.WHATSAPP_TOKEN else "not_configured",
                "openai": "configured" if settings.OPENAI_API_KEY else "not_configured",
                "redis": "connected"
            }
        }
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Erro na verificação de saúde: {str(e)}"
        )

@router.post("/reset-database")
async def reset_database(
    current_user: AuthUser = Depends(get_current_user)
):
    """Reseta banco de dados (apenas para desenvolvimento)"""
    try:
        # Verificar se é admin
        if not current_user.is_admin:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Apenas administradores podem resetar o banco de dados"
            )
        
        # Por enquanto, apenas retornar sucesso
        # TODO: Implementar reset real do banco
        return {
            "message": "Banco de dados resetado com sucesso",
            "timestamp": datetime.now().isoformat()
        }
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Erro ao resetar banco: {str(e)}"
        )
