"""
Value Object para nome de usuário
"""
from dataclasses import dataclass

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
