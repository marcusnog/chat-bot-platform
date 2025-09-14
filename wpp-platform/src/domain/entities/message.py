"""
Entidade Message - Representa uma mensagem do WhatsApp
"""
from dataclasses import dataclass
from datetime import datetime
from typing import Optional
from uuid import UUID, uuid4

from ..value_objects.message_content import MessageContent, MessageType, MessageDirection


@dataclass
class Message:
    """
    Entidade Message - Representa uma mensagem em uma conversa
    """
    id: Optional[UUID]
    conversation_id: UUID
    user_id: UUID
    whatsapp_message_id: str
    content: MessageContent
    is_processed: bool
    created_at: datetime
    
    def __post_init__(self):
        """Validações da entidade Message"""
        if not self.whatsapp_message_id or not self.whatsapp_message_id.strip():
            raise ValueError("ID da mensagem WhatsApp não pode ser vazio")
    
    @classmethod
    def create_new(
        cls,
        conversation_id: UUID,
        user_id: UUID,
        whatsapp_message_id: str,
        content: MessageContent
    ) -> 'Message':
        """
        Factory method para criar uma nova mensagem
        """
        return cls(
            id=uuid4(),
            conversation_id=conversation_id,
            user_id=user_id,
            whatsapp_message_id=whatsapp_message_id.strip(),
            content=content,
            is_processed=False,
            created_at=datetime.utcnow()
        )
    
    def mark_as_processed(self) -> None:
        """Marca a mensagem como processada"""
        self.is_processed = True
    
    def is_incoming(self) -> bool:
        """Verifica se é uma mensagem recebida"""
        return self.content.direction == MessageDirection.INCOMING
    
    def is_outgoing(self) -> bool:
        """Verifica se é uma mensagem enviada"""
        return self.content.direction == MessageDirection.OUTGOING
    
    def is_text_message(self) -> bool:
        """Verifica se é uma mensagem de texto"""
        return self.content.is_text_message()
    
    def is_media_message(self) -> bool:
        """Verifica se é uma mensagem de mídia"""
        return self.content.is_media_message()
    
    def get_display_text(self) -> str:
        """Retorna texto para exibição"""
        return self.content.get_display_text()
    
    def get_message_type(self) -> MessageType:
        """Retorna o tipo da mensagem"""
        return self.content.message_type
    
    def get_direction(self) -> MessageDirection:
        """Retorna a direção da mensagem"""
        return self.content.direction
    
    def get_metadata(self) -> Optional[dict]:
        """Retorna metadados da mensagem"""
        return self.content.metadata
    
    def __str__(self) -> str:
        direction = "→" if self.is_outgoing() else "←"
        return f"Message({direction} {self.get_display_text()})"
    
    def __repr__(self) -> str:
        return f"Message(id={self.id}, conversation_id={self.conversation_id}, type={self.content.message_type.value})"
