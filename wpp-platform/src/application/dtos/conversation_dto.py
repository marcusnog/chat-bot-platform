"""
DTOs para conversas
"""
from dataclasses import dataclass
from datetime import datetime
from typing import Optional, Dict, Any
from uuid import UUID


@dataclass
class CreateConversationDTO:
    """DTO para criação de conversa"""
    user_id: UUID
    whatsapp_conversation_id: str
    context: Optional[Dict[str, Any]] = None


@dataclass
class UpdateConversationStatusDTO:
    """DTO para atualização de status de conversa"""
    status: str
    reason: Optional[str] = None
    agent_id: Optional[UUID] = None


@dataclass
class ConversationResponseDTO:
    """DTO de resposta para conversa"""
    id: UUID
    user_id: UUID
    whatsapp_conversation_id: str
    status: str
    status_description: str
    context: Dict[str, Any]
    agent_id: Optional[UUID]
    created_at: datetime
    updated_at: Optional[datetime]
    
    @classmethod
    def from_entity(cls, conversation) -> 'ConversationResponseDTO':
        """Cria DTO a partir da entidade"""
        return cls(
            id=conversation.id,
            user_id=conversation.user_id,
            whatsapp_conversation_id=conversation.whatsapp_conversation_id,
            status=conversation.status.status.value,
            status_description=conversation.get_status_description(),
            context=conversation.context,
            agent_id=conversation.agent_id,
            created_at=conversation.created_at,
            updated_at=conversation.updated_at
        )


@dataclass
class ConversationListDTO:
    """DTO para lista de conversas"""
    conversations: list[ConversationResponseDTO]
    total: int
    skip: int
    limit: int


@dataclass
class ConversationSummaryDTO:
    """DTO resumido para conversa"""
    id: UUID
    user_name: str
    user_phone: str
    status: str
    last_message: Optional[str]
    message_count: int
    created_at: datetime
