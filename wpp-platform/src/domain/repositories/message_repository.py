"""
Interface do repositório de mensagens
"""
from abc import ABC, abstractmethod
from typing import List, Optional
from uuid import UUID

from ..entities.message import Message
from ..value_objects.message_content import MessageDirection


class MessageRepository(ABC):
    """
    Interface para repositório de mensagens
    """
    
    @abstractmethod
    async def save(self, message: Message) -> Message:
        """Salva uma mensagem"""
        pass
    
    @abstractmethod
    async def find_by_id(self, message_id: UUID) -> Optional[Message]:
        """Busca mensagem por ID"""
        pass
    
    @abstractmethod
    async def find_by_whatsapp_id(self, whatsapp_message_id: str) -> Optional[Message]:
        """Busca mensagem por ID do WhatsApp"""
        pass
    
    @abstractmethod
    async def find_by_conversation_id(
        self, 
        conversation_id: UUID, 
        skip: int = 0, 
        limit: int = 50
    ) -> List[Message]:
        """Busca mensagens de uma conversa"""
        pass
    
    @abstractmethod
    async def find_by_user_id(
        self, 
        user_id: UUID, 
        skip: int = 0, 
        limit: int = 50
    ) -> List[Message]:
        """Busca mensagens de um usuário"""
        pass
    
    @abstractmethod
    async def find_unprocessed_messages(self) -> List[Message]:
        """Busca mensagens não processadas"""
        pass
    
    @abstractmethod
    async def find_by_direction(
        self, 
        direction: MessageDirection, 
        skip: int = 0, 
        limit: int = 50
    ) -> List[Message]:
        """Busca mensagens por direção"""
        pass
    
    @abstractmethod
    async def count_by_conversation_id(self, conversation_id: UUID) -> int:
        """Conta mensagens de uma conversa"""
        pass
    
    @abstractmethod
    async def delete(self, message_id: UUID) -> bool:
        """Remove uma mensagem"""
        pass
    
    @abstractmethod
    async def exists_by_whatsapp_id(self, whatsapp_message_id: str) -> bool:
        """Verifica se mensagem existe pelo ID do WhatsApp"""
        pass
