"""
Interface do repositório de usuários
"""
from abc import ABC, abstractmethod
from typing import List, Optional
from uuid import UUID

from ..entities.user import User
from ..value_objects.phone_number import PhoneNumber


class UserRepository(ABC):
    """
    Interface para repositório de usuários
    """
    
    @abstractmethod
    async def save(self, user: User) -> User:
        """Salva um usuário"""
        pass
    
    @abstractmethod
    async def find_by_id(self, user_id: UUID) -> Optional[User]:
        """Busca usuário por ID"""
        pass
    
    @abstractmethod
    async def find_by_phone_number(self, phone_number: PhoneNumber) -> Optional[User]:
        """Busca usuário por número de telefone"""
        pass
    
    @abstractmethod
    async def find_all(self, skip: int = 0, limit: int = 100) -> List[User]:
        """Lista todos os usuários"""
        pass
    
    @abstractmethod
    async def find_active_users(self, skip: int = 0, limit: int = 100) -> List[User]:
        """Lista usuários ativos"""
        pass
    
    @abstractmethod
    async def delete(self, user_id: UUID) -> bool:
        """Remove um usuário"""
        pass
    
    @abstractmethod
    async def exists_by_phone_number(self, phone_number: PhoneNumber) -> bool:
        """Verifica se usuário existe pelo número de telefone"""
        pass
