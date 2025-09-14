"""
DTOs para usuários
"""
from dataclasses import dataclass
from datetime import datetime
from typing import Optional
from uuid import UUID


@dataclass
class CreateUserDTO:
    """DTO para criação de usuário"""
    phone_number: str
    name: str
    email: Optional[str] = None


@dataclass
class UpdateUserDTO:
    """DTO para atualização de usuário"""
    name: Optional[str] = None
    email: Optional[str] = None
    is_active: Optional[bool] = None


@dataclass
class UserResponseDTO:
    """DTO de resposta para usuário"""
    id: UUID
    phone_number: str
    name: str
    email: Optional[str]
    is_active: bool
    created_at: datetime
    updated_at: Optional[datetime]
    
    @classmethod
    def from_entity(cls, user) -> 'UserResponseDTO':
        """Cria DTO a partir da entidade"""
        return cls(
            id=user.id,
            phone_number=str(user.phone_number),
            name=user.name,
            email=user.email,
            is_active=user.is_active,
            created_at=user.created_at,
            updated_at=user.updated_at
        )


@dataclass
class UserListDTO:
    """DTO para lista de usuários"""
    users: list[UserResponseDTO]
    total: int
    skip: int
    limit: int
