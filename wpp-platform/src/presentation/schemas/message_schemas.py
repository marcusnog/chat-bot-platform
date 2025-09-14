"""
Schemas Pydantic para mensagens
"""
from pydantic import BaseModel, Field
from typing import Optional, Dict, Any
from datetime import datetime
from uuid import UUID


class SendMessageRequest(BaseModel):
    """Schema para envio de mensagem"""
    phone_number: str = Field(..., description="Número de telefone do destinatário")
    message: str = Field(..., min_length=1, max_length=4096, description="Conteúdo da mensagem")
    message_type: str = Field("text", description="Tipo da mensagem")


class CreateMessageRequest(BaseModel):
    """Schema para criação de mensagem"""
    conversation_id: UUID = Field(..., description="ID da conversa")
    user_id: UUID = Field(..., description="ID do usuário")
    whatsapp_message_id: str = Field(..., description="ID da mensagem no WhatsApp")
    content: str = Field(..., description="Conteúdo da mensagem")
    message_type: str = Field("text", description="Tipo da mensagem")
    direction: str = Field(..., description="Direção da mensagem")
    metadata: Optional[Dict[str, Any]] = Field(None, description="Metadados da mensagem")


class MessageResponse(BaseModel):
    """Schema de resposta para mensagem"""
    id: UUID
    conversation_id: UUID
    user_id: UUID
    whatsapp_message_id: str
    content: str
    display_text: str
    message_type: str
    direction: str
    is_processed: bool
    metadata: Optional[Dict[str, Any]]
    created_at: datetime
    
    class Config:
        from_attributes = True


class MessageListResponse(BaseModel):
    """Schema de resposta para lista de mensagens"""
    messages: list[MessageResponse]
    total: int
    skip: int
    limit: int


class ProcessMessageResponse(BaseModel):
    """Schema de resposta para processamento de mensagem"""
    message_id: UUID
    should_escalate: bool
    ai_response: Optional[str]
    sentiment: Optional[Dict[str, Any]]
    intent: Optional[Dict[str, Any]]
