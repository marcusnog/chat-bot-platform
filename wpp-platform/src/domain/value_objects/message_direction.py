"""
Value Object para direção da mensagem
"""
from dataclasses import dataclass

@dataclass(frozen=True)
class MessageDirection:
    """Value Object para direção da mensagem"""
    value: str
    
    def __post_init__(self):
        valid_directions = ["inbound", "outbound"]
        if self.value not in valid_directions:
            raise ValueError(f"Direção deve ser uma de: {', '.join(valid_directions)}")
