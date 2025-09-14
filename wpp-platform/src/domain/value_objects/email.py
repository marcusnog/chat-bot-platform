"""
Value Object para email
"""
from dataclasses import dataclass
import re

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
