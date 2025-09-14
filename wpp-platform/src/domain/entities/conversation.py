"""
Entidade Conversation - Representa uma conversa do WhatsApp
"""
from dataclasses import dataclass, field
from datetime import datetime
from typing import Optional, List, Dict, Any
from uuid import UUID, uuid4

from ..value_objects.conversation_status import ConversationStatusValue, ConversationStatus


@dataclass
class Conversation:
    """
    Entidade Conversation - Representa uma conversa entre usuário e sistema
    """
    id: Optional[UUID]
    user_id: UUID
    whatsapp_conversation_id: str
    status: ConversationStatusValue
    context: Dict[str, Any]
    created_at: datetime
    updated_at: Optional[datetime] = None
    agent_id: Optional[UUID] = None
    
    def __post_init__(self):
        """Validações da entidade Conversation"""
        if not self.whatsapp_conversation_id or not self.whatsapp_conversation_id.strip():
            raise ValueError("ID da conversa WhatsApp não pode ser vazio")
    
    @classmethod
    def create_new(
        cls, 
        user_id: UUID, 
        whatsapp_conversation_id: str,
        context: Optional[Dict[str, Any]] = None
    ) -> 'Conversation':
        """
        Factory method para criar uma nova conversa
        """
        now = datetime.utcnow()
        return cls(
            id=uuid4(),
            user_id=user_id,
            whatsapp_conversation_id=whatsapp_conversation_id.strip(),
            status=ConversationStatusValue(
                status=ConversationStatus.ACTIVE,
                timestamp=now
            ),
            context=context or {},
            created_at=now
        )
    
    def update_status(
        self, 
        new_status: ConversationStatus, 
        reason: Optional[str] = None,
        agent_id: Optional[UUID] = None
    ) -> None:
        """Atualiza o status da conversa"""
        self.status = ConversationStatusValue(
            status=new_status,
            timestamp=datetime.utcnow(),
            reason=reason,
            agent_id=agent_id
        )
        self.updated_at = datetime.utcnow()
        
        if agent_id:
            self.agent_id = agent_id
    
    def close(self, reason: Optional[str] = None) -> None:
        """Fecha a conversa"""
        self.update_status(ConversationStatus.CLOSED, reason)
    
    def transfer_to_agent(self, agent_id: UUID, reason: Optional[str] = None) -> None:
        """Transfere a conversa para um agente"""
        self.update_status(ConversationStatus.TRANSFERRED, reason, agent_id)
    
    def escalate(self, reason: str) -> None:
        """Escala a conversa"""
        self.update_status(ConversationStatus.ESCALATED, reason)
    
    def set_waiting_for_agent(self) -> None:
        """Define como aguardando agente"""
        self.update_status(ConversationStatus.WAITING_AGENT, "Aguardando agente disponível")
    
    def update_context(self, new_context: Dict[str, Any]) -> None:
        """Atualiza o contexto da conversa"""
        self.context.update(new_context)
        self.updated_at = datetime.utcnow()
    
    def add_context_key(self, key: str, value: Any) -> None:
        """Adiciona uma chave ao contexto"""
        self.context[key] = value
        self.updated_at = datetime.utcnow()
    
    def get_context_value(self, key: str, default: Any = None) -> Any:
        """Obtém um valor do contexto"""
        return self.context.get(key, default)
    
    def can_receive_messages(self) -> bool:
        """Verifica se pode receber mensagens"""
        return self.status.can_receive_messages()
    
    def requires_human_agent(self) -> bool:
        """Verifica se requer agente humano"""
        return self.status.requires_human_agent()
    
    def is_active(self) -> bool:
        """Verifica se está ativa"""
        return self.status.is_active()
    
    def is_closed(self) -> bool:
        """Verifica se está fechada"""
        return self.status.is_closed()
    
    def get_status_description(self) -> str:
        """Retorna descrição do status"""
        return self.status.get_status_description()
    
    def __str__(self) -> str:
        return f"Conversation({self.whatsapp_conversation_id}, {self.get_status_description()})"
    
    def __repr__(self) -> str:
        return f"Conversation(id={self.id}, user_id={self.user_id}, status={self.status.status.value})"
