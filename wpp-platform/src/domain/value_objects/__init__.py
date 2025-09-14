"""
Value Objects do domínio
"""
from dataclasses import dataclass
from typing import Optional
import re

@dataclass(frozen=True)
class UserName:
    """Value Object para nome de usuário"""
    value: str
    
    def __post_init__(self):
        if not self.value or not self.value.strip():
            raise ValueError("Nome não pode ser vazio")
        if len(self.value.strip()) < 2:
            raise ValueError("Nome deve ter pelo menos 2 caracteres")
        if len(self.value.strip()) > 100:
            raise ValueError("Nome deve ter no máximo 100 caracteres")

@dataclass(frozen=True)
class Email:
    """Value Object para email"""
    value: str
    
    def __post_init__(self):
        if not self.value or not self.value.strip():
            raise ValueError("Email não pode ser vazio")
        
        # Validação básica de email
        email_pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        if not re.match(email_pattern, self.value.strip()):
            raise ValueError("Email inválido")
        
        if len(self.value.strip()) > 255:
            raise ValueError("Email deve ter no máximo 255 caracteres")

@dataclass(frozen=True)
class PhoneNumber:
    """Value Object para número de telefone"""
    value: str
    
    def __post_init__(self):
        if not self.value or not self.value.strip():
            raise ValueError("Número de telefone não pode ser vazio")
        
        # Remove caracteres não numéricos para validação
        clean_number = re.sub(r'[^\d]', '', self.value)
        
        if len(clean_number) < 10:
            raise ValueError("Número de telefone deve ter pelo menos 10 dígitos")
        if len(clean_number) > 15:
            raise ValueError("Número de telefone deve ter no máximo 15 dígitos")

@dataclass(frozen=True)
class MessageContent:
    """Value Object para conteúdo de mensagem"""
    value: str
    
    def __post_init__(self):
        if not self.value or not self.value.strip():
            raise ValueError("Conteúdo da mensagem não pode ser vazio")
        if len(self.value.strip()) > 4096:
            raise ValueError("Conteúdo da mensagem deve ter no máximo 4096 caracteres")

@dataclass(frozen=True)
class MessageDirection:
    """Value Object para direção da mensagem"""
    value: str
    
    def __post_init__(self):
        valid_directions = ["inbound", "outbound"]
        if self.value not in valid_directions:
            raise ValueError(f"Direção deve ser uma de: {', '.join(valid_directions)}")

@dataclass(frozen=True)
class MessageStatus:
    """Value Object para status da mensagem"""
    value: str
    
    def __post_init__(self):
        valid_statuses = ["pending", "sent", "delivered", "read", "failed"]
        if self.value not in valid_statuses:
            raise ValueError(f"Status deve ser um de: {', '.join(valid_statuses)}")

@dataclass(frozen=True)
class ConversationStatus:
    """Value Object para status da conversa"""
    value: str
    
    def __post_init__(self):
        valid_statuses = ["pending", "active", "closed", "resolved"]
        if self.value not in valid_statuses:
            raise ValueError(f"Status deve ser um de: {', '.join(valid_statuses)}")