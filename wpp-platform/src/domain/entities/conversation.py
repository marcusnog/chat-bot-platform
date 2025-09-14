"""
Entidade Conversation - Representa uma conversa do WhatsApp
"""
from dataclasses import dataclass
from datetime import datetime
from typing import Optional
from uuid import UUID, uuid4

from ..value_objects.conversation_status import ConversationStatus


@dataclass
class Conversation:
    """
    Entidade Conversation - Representa uma conversa entre usuário e sistema
    """
    id: Optional[UUID]
    user_id: UUID
    status: ConversationStatus
    created_at: datetime
    updated_at: Optional[datetime] = None
    last_message_at: Optional[datetime] = None
    
    def __post_init__(self):
        """Validações da entidade Conversation"""
        if not self.user_id:
            raise ValueError("ID do usuário não pode ser vazio")
    
    @classmethod
    def create_new(
        cls, 
        user_id: UUID
    ) -> 'Conversation':
        """
        Factory method para criar uma nova conversa
        """
        now = datetime.utcnow()
        return cls(
            id=uuid4(),
            user_id=user_id,
            status=ConversationStatus("pending"),
            created_at=now
        )
    
    def update_status(self, new_status: str) -> None:
        """Atualiza o status da conversa"""
        self.status = ConversationStatus(new_status)
        self.updated_at = datetime.utcnow()
    
    def close(self) -> None:
        """Fecha a conversa"""
        self.update_status("closed")
    
    def activate(self) -> None:
        """Ativa a conversa"""
        self.update_status("active")
    
    def resolve(self) -> None:
        """Resolve a conversa"""
        self.update_status("resolved")
    
    def update_last_message(self) -> None:
        """Atualiza timestamp da última mensagem"""
        self.last_message_at = datetime.utcnow()
        self.updated_at = datetime.utcnow()
    
    def is_active(self) -> bool:
        """Verifica se está ativa"""
        return self.status.value == "active"
    
    def is_closed(self) -> bool:
        """Verifica se está fechada"""
        return self.status.value == "closed"
    
    def is_pending(self) -> bool:
        """Verifica se está pendente"""
        return self.status.value == "pending"
    
    def is_resolved(self) -> bool:
        """Verifica se está resolvida"""
        return self.status.value == "resolved"
    
    def __str__(self) -> str:
        return f"Conversation({self.id}, {self.status.value})"
    
    def __repr__(self) -> str:
        return f"Conversation(id={self.id}, user_id={self.user_id}, status={self.status.value})"