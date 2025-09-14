"""
Entidade User - Representa um usuário do sistema
"""
from dataclasses import dataclass
from datetime import datetime
from typing import Optional, List
from uuid import UUID, uuid4

from ..value_objects.phone_number import PhoneNumber


@dataclass
class User:
    """
    Entidade User - Representa um usuário do WhatsApp
    """
    id: Optional[UUID]
    phone_number: PhoneNumber
    name: str
    email: Optional[str]
    is_active: bool
    created_at: datetime
    updated_at: Optional[datetime] = None
    
    def __post_init__(self):
        """Validações da entidade User"""
        if not self.name or not self.name.strip():
            raise ValueError("Nome do usuário não pode ser vazio")
        
        if self.email and not self._is_valid_email(self.email):
            raise ValueError("Email inválido")
    
    @staticmethod
    def _is_valid_email(email: str) -> bool:
        """Valida formato do email"""
        import re
        pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        return bool(re.match(pattern, email))
    
    @classmethod
    def create_new(
        cls, 
        phone_number: PhoneNumber, 
        name: str, 
        email: Optional[str] = None
    ) -> 'User':
        """
        Factory method para criar um novo usuário
        """
        now = datetime.utcnow()
        return cls(
            id=uuid4(),
            phone_number=phone_number,
            name=name.strip(),
            email=email.strip() if email else None,
            is_active=True,
            created_at=now
        )
    
    def update_name(self, new_name: str) -> None:
        """Atualiza o nome do usuário"""
        if not new_name or not new_name.strip():
            raise ValueError("Nome não pode ser vazio")
        
        self.name = new_name.strip()
        self.updated_at = datetime.utcnow()
    
    def update_email(self, new_email: Optional[str]) -> None:
        """Atualiza o email do usuário"""
        if new_email and not self._is_valid_email(new_email):
            raise ValueError("Email inválido")
        
        self.email = new_email.strip() if new_email else None
        self.updated_at = datetime.utcnow()
    
    def activate(self) -> None:
        """Ativa o usuário"""
        self.is_active = True
        self.updated_at = datetime.utcnow()
    
    def deactivate(self) -> None:
        """Desativa o usuário"""
        self.is_active = False
        self.updated_at = datetime.utcnow()
    
    def get_display_name(self) -> str:
        """Retorna nome para exibição"""
        if self.name:
            return self.name
        return self.phone_number.to_display_format()
    
    def get_whatsapp_id(self) -> str:
        """Retorna ID do WhatsApp (número sem formatação)"""
        return self.phone_number.to_whatsapp_format()
    
    def __str__(self) -> str:
        return f"User({self.get_display_name()}, {self.phone_number})"
    
    def __repr__(self) -> str:
        return f"User(id={self.id}, phone={self.phone_number}, name='{self.name}')"
