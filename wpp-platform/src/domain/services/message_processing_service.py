"""
Domain Service para processamento de mensagens
"""
from abc import ABC, abstractmethod
from typing import List, Optional, Dict, Any
from datetime import datetime

from ..entities.message import Message
from ..entities.conversation import Conversation
from ..entities.user import User
from ..value_objects.message_content import MessageContent, MessageDirection, MessageType


class MessageProcessingService(ABC):
    """
    Interface para serviços de processamento de mensagens
    """
    
    @abstractmethod
    async def should_escalate_to_human(
        self, 
        message: Message, 
        conversation: Conversation,
        message_history: List[Message]
    ) -> bool:
        """
        Determina se uma mensagem deve ser escalada para um agente humano
        """
        pass
    
    @abstractmethod
    async def analyze_sentiment(self, message_content: str) -> Dict[str, Any]:
        """
        Analisa o sentimento de uma mensagem
        """
        pass
    
    @abstractmethod
    async def extract_intent(self, message_content: str) -> Dict[str, Any]:
        """
        Extrai a intenção de uma mensagem
        """
        pass
    
    @abstractmethod
    async def generate_ai_response(
        self, 
        message: Message, 
        conversation: Conversation,
        message_history: List[Message]
    ) -> str:
        """
        Gera uma resposta usando IA
        """
        pass


class DefaultMessageProcessingService(MessageProcessingService):
    """
    Implementação padrão do serviço de processamento de mensagens
    """
    
    def __init__(self):
        self.escalation_keywords = [
            "falar com humano", "atendente", "supervisor", "reclamação",
            "problema sério", "não resolve", "cancelar", "devolução",
            "quero falar com alguém", "preciso de ajuda humana"
        ]
        
        self.negative_keywords = [
            "péssimo", "terrível", "horrível", "odiei", "detesto",
            "raiva", "irritado", "frustrado", "insatisfeito"
        ]
    
    async def should_escalate_to_human(
        self, 
        message: Message, 
        conversation: Conversation,
        message_history: List[Message]
    ) -> bool:
        """
        Determina se deve escalar para humano baseado em regras de negócio
        """
        message_text = message.content.text.lower()
        
        # Verifica palavras-chave de escalação
        if any(keyword in message_text for keyword in self.escalation_keywords):
            return True
        
        # Verifica palavras negativas
        negative_count = sum(1 for keyword in self.negative_keywords if keyword in message_text)
        if negative_count >= 2:
            return True
        
        # Verifica se muitas mensagens sem resolução
        if len(message_history) > 20:
            return True
        
        # Verifica se já foi escalada antes
        if conversation.status.status.value in ["transferred", "escalated"]:
            return True
        
        return False
    
    async def analyze_sentiment(self, message_content: str) -> Dict[str, Any]:
        """
        Análise simples de sentimento baseada em palavras-chave
        """
        text_lower = message_content.lower()
        
        positive_words = ["obrigado", "valeu", "thanks", "ótimo", "bom", "excelente", "perfeito"]
        negative_words = ["ruim", "péssimo", "terrível", "horrível", "problema", "erro"]
        
        positive_count = sum(1 for word in positive_words if word in text_lower)
        negative_count = sum(1 for word in negative_words if word in text_lower)
        
        if positive_count > negative_count:
            sentiment = "positive"
            confidence = min(0.9, 0.5 + (positive_count * 0.1))
        elif negative_count > positive_count:
            sentiment = "negative"
            confidence = min(0.9, 0.5 + (negative_count * 0.1))
        else:
            sentiment = "neutral"
            confidence = 0.5
        
        return {
            "sentiment": sentiment,
            "confidence": confidence,
            "emotions": self._extract_emotions(text_lower)
        }
    
    def _extract_emotions(self, text: str) -> List[str]:
        """Extrai emoções do texto"""
        emotions = []
        
        emotion_keywords = {
            "happy": ["feliz", "alegre", "contente", "satisfeito"],
            "angry": ["raiva", "irritado", "furioso", "bravo"],
            "sad": ["triste", "deprimido", "chateado", "melancólico"],
            "excited": ["animado", "empolgado", "entusiasmado"],
            "frustrated": ["frustrado", "irritado", "incomodado"]
        }
        
        for emotion, keywords in emotion_keywords.items():
            if any(keyword in text for keyword in keywords):
                emotions.append(emotion)
        
        return emotions
    
    async def extract_intent(self, message_content: str) -> Dict[str, Any]:
        """
        Extrai intenção da mensagem baseada em padrões
        """
        text_lower = message_content.lower()
        
        intent_patterns = {
            "greeting": ["oi", "olá", "bom dia", "boa tarde", "boa noite", "hello", "hi"],
            "question": ["como", "quando", "onde", "por que", "qual", "quanto", "?"],
            "complaint": ["reclamação", "problema", "erro", "falha", "defeito"],
            "compliment": ["parabéns", "excelente", "ótimo", "perfeito", "muito bom"],
            "goodbye": ["tchau", "até logo", "bye", "até mais", "falou"],
            "help": ["ajuda", "help", "suporte", "dúvida", "não sei"]
        }
        
        detected_intent = "other"
        confidence = 0.5
        
        for intent, patterns in intent_patterns.items():
            matches = sum(1 for pattern in patterns if pattern in text_lower)
            if matches > 0:
                detected_intent = intent
                confidence = min(0.9, 0.5 + (matches * 0.1))
                break
        
        return {
            "intent": detected_intent,
            "confidence": confidence,
            "entities": self._extract_entities(text_lower)
        }
    
    def _extract_entities(self, text: str) -> List[str]:
        """Extrai entidades do texto"""
        entities = []
        
        # Padrões simples para extrair entidades
        import re
        
        # Emails
        email_pattern = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
        emails = re.findall(email_pattern, text)
        entities.extend([f"email:{email}" for email in emails])
        
        # Números de telefone
        phone_pattern = r'\b\d{2,3}\s?\d{4,5}\s?\d{4}\b'
        phones = re.findall(phone_pattern, text)
        entities.extend([f"phone:{phone}" for phone in phones])
        
        # Valores monetários
        money_pattern = r'R\$\s?\d+[,.]?\d*'
        money = re.findall(money_pattern, text)
        entities.extend([f"money:{m}" for m in money])
        
        return entities
    
    async def generate_ai_response(
        self, 
        message: Message, 
        conversation: Conversation,
        message_history: List[Message]
    ) -> str:
        """
        Gera resposta usando IA (implementação simplificada)
        """
        # Implementação básica - em produção seria integrada com OpenAI
        intent_result = await self.extract_intent(message.content.text)
        intent = intent_result["intent"]
        
        responses = {
            "greeting": "Olá! 👋 Como posso ajudá-lo hoje?",
            "question": "Ótima pergunta! Deixe-me ajudá-lo com isso.",
            "complaint": "Entendo sua preocupação. Vou fazer o possível para resolver isso.",
            "compliment": "Muito obrigado pelo feedback positivo! 😊",
            "goodbye": "Até logo! Foi um prazer conversar com você. 👋",
            "help": "Claro! Estou aqui para ajudar. Qual é sua dúvida?",
            "other": "Entendi. Como posso ajudá-lo melhor?"
        }
        
        return responses.get(intent, responses["other"])
