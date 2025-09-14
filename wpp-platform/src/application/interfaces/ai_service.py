"""
Interface para serviço de IA
"""
from abc import ABC, abstractmethod
from typing import Dict, Any, List


class AIService(ABC):
    """
    Interface para serviços de IA
    """
    
    @abstractmethod
    async def generate_response(
        self, 
        user_message: str, 
        conversation_history: List[Dict], 
        context: Optional[Dict] = None
    ) -> str:
        """Gera uma resposta usando IA"""
        pass
    
    @abstractmethod
    async def analyze_sentiment(self, text: str) -> Dict[str, Any]:
        """Analisa o sentimento do texto"""
        pass
    
    @abstractmethod
    async def extract_intent(self, text: str) -> Dict[str, Any]:
        """Extrai a intenção do usuário"""
        pass
    
    @abstractmethod
    async def should_escalate_to_human(
        self, 
        conversation_history: List[Dict], 
        current_message: str
    ) -> bool:
        """Determina se a conversa deve ser escalada para um humano"""
        pass
