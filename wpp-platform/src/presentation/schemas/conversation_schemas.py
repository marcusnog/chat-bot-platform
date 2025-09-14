"""
Schemas Pydantic para conversas
"""
from pydantic import BaseModel, Field
from typing import Optional, Dict, Any
from datetime import datetime
from uuid import UUID


class CreateConversationRequest(BaseModel):
    """Schema para criação de conversa"""
    user_id: UUID = Field(..., description="ID do usuário")
    whatsapp_conversation_id: str = Field(..., description="ID da conversa no WhatsApp")
    context: Optional[Dict[str, Any]] = Field(None, description="Contexto da conversa")


class UpdateConversationStatusRequest(BaseModel):
    """Schema para atualização de status de conversa"""
    status: str = Field(..., description="Novo status da conversa")
    reason: Optional[str] = Field(None, description="Motivo da mudança de status")
    agent_id: Optional[UUID] = Field(None, description="ID do agente")


class ConversationResponse(BaseModel):
    """Schema de resposta para conversa"""
    id: UUID
    user_id: UUID
    whatsapp_conversation_id: str
    status: str
    status_description: str
    context: Dict[str, Any]
    agent_id: Optional[UUID]
    created_at: datetime
    updated_at: Optional[datetime]
    
    class Config:
        from_attributes = True


class ConversationListResponse(BaseModel):
    """Schema de resposta para lista de conversas"""
    conversations: list[ConversationResponse]
    total: int
    skip: int
    limit: int


class ConversationSummaryResponse(BaseModel):
    """Schema de resposta resumida para conversa"""
    id: UUID
    user_name: str
    user_phone: str
    status: str
    last_message: Optional[str]
    message_count: int
    created_at: datetime
