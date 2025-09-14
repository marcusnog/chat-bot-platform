"""
Interface do repositório de conversas
"""
from abc import ABC, abstractmethod
from typing import List, Optional
from uuid import UUID

from ..entities.conversation import Conversation
from ..value_objects.conversation_status import ConversationStatus


class ConversationRepository(ABC):
    """
    Interface para repositório de conversas
    """
    
    @abstractmethod
    async def save(self, conversation: Conversation) -> Conversation:
        """Salva uma conversa"""
        pass
    
    @abstractmethod
    async def find_by_id(self, conversation_id: UUID) -> Optional[Conversation]:
        """Busca conversa por ID"""
        pass
    
    @abstractmethod
    async def find_by_whatsapp_id(self, whatsapp_conversation_id: str) -> Optional[Conversation]:
        """Busca conversa por ID do WhatsApp"""
        pass
    
    @abstractmethod
    async def find_by_user_id(self, user_id: UUID) -> List[Conversation]:
        """Busca conversas de um usuário"""
        pass
    
    @abstractmethod
    async def find_active_by_user_id(self, user_id: UUID) -> Optional[Conversation]:
        """Busca conversa ativa de um usuário"""
        pass
    
    @abstractmethod
    async def find_by_status(
        self, 
        status: ConversationStatus, 
        skip: int = 0, 
        limit: int = 100
    ) -> List[Conversation]:
        """Busca conversas por status"""
        pass
    
    @abstractmethod
    async def find_by_agent_id(self, agent_id: UUID) -> List[Conversation]:
        """Busca conversas de um agente"""
        pass
    
    @abstractmethod
    async def find_all(self, skip: int = 0, limit: int = 100) -> List[Conversation]:
        """Lista todas as conversas"""
        pass
    
    @abstractmethod
    async def delete(self, conversation_id: UUID) -> bool:
        """Remove uma conversa"""
        pass
    
    @abstractmethod
    async def count_by_user_id(self, user_id: UUID) -> int:
        """Conta conversas de um usuário"""
        pass
