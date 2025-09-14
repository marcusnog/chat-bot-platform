"""
Value Object para número de telefone
"""
from dataclasses import dataclass
import re

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