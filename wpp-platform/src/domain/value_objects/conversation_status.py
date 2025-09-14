"""
Value Object para status da conversa
"""
from dataclasses import dataclass

@dataclass(frozen=True)
class ConversationStatus:
    """Value Object para status da conversa"""
    value: str
    
    def __post_init__(self):
        valid_statuses = ["pending", "active", "closed", "resolved"]
        if self.value not in valid_statuses:
            raise ValueError(f"Status deve ser um de: {', '.join(valid_statuses)}")