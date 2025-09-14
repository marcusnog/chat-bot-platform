"""
Value Object para status da mensagem
"""
from dataclasses import dataclass

@dataclass(frozen=True)
class MessageStatus:
    """Value Object para status da mensagem"""
    value: str
    
    def __post_init__(self):
        valid_statuses = ["pending", "sent", "delivered", "read", "failed"]
        if self.value not in valid_statuses:
            raise ValueError(f"Status deve ser um de: {', '.join(valid_statuses)}")
