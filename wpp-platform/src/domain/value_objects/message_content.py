"""
Value Object para conteúdo de mensagem
"""
from dataclasses import dataclass

@dataclass(frozen=True)
class MessageContent:
    """Value Object para conteúdo de mensagem"""
    value: str
    
    def __post_init__(self):
        if not self.value or not self.value.strip():
            raise ValueError("Conteúdo da mensagem não pode ser vazio")
        if len(self.value.strip()) > 4096:
            raise ValueError("Conteúdo da mensagem deve ter no máximo 4096 caracteres")