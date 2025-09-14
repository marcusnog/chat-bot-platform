"""
Value Object para status de conversa
"""
from dataclasses import dataclass
from enum import Enum
from datetime import datetime
from typing import Optional


class ConversationStatus(Enum):
    """Status possíveis de uma conversa"""
    ACTIVE = "active"
    CLOSED = "closed"
    TRANSFERRED = "transferred"
    WAITING_AGENT = "waiting_agent"
    ESCALATED = "escalated"


@dataclass(frozen=True)
class ConversationStatusValue:
    """
    Value Object para representar o status de uma conversa
    """
    status: ConversationStatus
    timestamp: datetime
    reason: Optional[str] = None
    agent_id: Optional[int] = None
    
    def __post_init__(self):
        """Valida o status da conversa"""
        if not isinstance(self.status, ConversationStatus):
            raise ValueError("Status deve ser uma instância de ConversationStatus")
    
    def is_active(self) -> bool:
        """Verifica se a conversa está ativa"""
        return self.status == ConversationStatus.ACTIVE
    
    def is_closed(self) -> bool:
        """Verifica se a conversa está fechada"""
        return self.status == ConversationStatus.CLOSED
    
    def is_transferred(self) -> bool:
        """Verifica se a conversa foi transferida"""
        return self.status == ConversationStatus.TRANSFERRED
    
    def can_receive_messages(self) -> bool:
        """Verifica se a conversa pode receber mensagens"""
        return self.status in [
            ConversationStatus.ACTIVE,
            ConversationStatus.WAITING_AGENT,
            ConversationStatus.ESCALATED
        ]
    
    def requires_human_agent(self) -> bool:
        """Verifica se a conversa requer agente humano"""
        return self.status in [
            ConversationStatus.TRANSFERRED,
            ConversationStatus.WAITING_AGENT,
            ConversationStatus.ESCALATED
        ]
    
    def get_status_description(self) -> str:
        """Retorna descrição amigável do status"""
        descriptions = {
            ConversationStatus.ACTIVE: "Ativa",
            ConversationStatus.CLOSED: "Fechada",
            ConversationStatus.TRANSFERRED: "Transferida",
            ConversationStatus.WAITING_AGENT: "Aguardando Agente",
            ConversationStatus.ESCALATED: "Escalada"
        }
        
        base_description = descriptions.get(self.status, "Desconhecido")
        
        if self.reason:
            return f"{base_description} - {self.reason}"
        
        return base_description
    
    def __str__(self) -> str:
        return self.get_status_description()
    
    def __repr__(self) -> str:
        return f"ConversationStatusValue(status={self.status.value}, timestamp={self.timestamp})"
