"""
DTOs para mensagens
"""
from dataclasses import dataclass
from datetime import datetime
from typing import Optional, Dict, Any
from uuid import UUID


@dataclass
class CreateMessageDTO:
    """DTO para criação de mensagem"""
    conversation_id: UUID
    user_id: UUID
    whatsapp_message_id: str
    content: str
    message_type: str
    direction: str
    metadata: Optional[Dict[str, Any]] = None


@dataclass
class SendMessageDTO:
    """DTO para envio de mensagem"""
    phone_number: str
    message: str
    message_type: str = "text"


@dataclass
class MessageResponseDTO:
    """DTO de resposta para mensagem"""
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
    
    @classmethod
    def from_entity(cls, message) -> 'MessageResponseDTO':
        """Cria DTO a partir da entidade"""
        return cls(
            id=message.id,
            conversation_id=message.conversation_id,
            user_id=message.user_id,
            whatsapp_message_id=message.whatsapp_message_id,
            content=message.content.text,
            display_text=message.get_display_text(),
            message_type=message.content.message_type.value,
            direction=message.content.direction.value,
            is_processed=message.is_processed,
            metadata=message.content.metadata,
            created_at=message.created_at
        )


@dataclass
class MessageListDTO:
    """DTO para lista de mensagens"""
    messages: list[MessageResponseDTO]
    total: int
    skip: int
    limit: int


@dataclass
class ProcessMessageDTO:
    """DTO para processamento de mensagem"""
    message_id: UUID
    should_escalate: bool
    ai_response: Optional[str] = None
    sentiment: Optional[Dict[str, Any]] = None
    intent: Optional[Dict[str, Any]] = None
