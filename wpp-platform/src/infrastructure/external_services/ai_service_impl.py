"""
Implementação do serviço de IA
"""
import openai
from typing import Dict, List, Optional, Any
from config import settings
import logging
import json

from ...application.interfaces.ai_service import AIService

logger = logging.getLogger(__name__)


class AIServiceImpl(AIService):
    """
    Implementação do serviço de IA usando OpenAI
    """
    
    def __init__(self):
        openai.api_key = settings.OPENAI_API_KEY
        self.client = openai.OpenAI(api_key=settings.OPENAI_API_KEY)
    
    async def generate_response(
        self, 
        user_message: str, 
        conversation_history: List[Dict], 
        context: Optional[Dict] = None
    ) -> str:
        """Gera uma resposta usando IA baseada na mensagem do usuário e histórico"""
        
        # Construir o contexto da conversa
        system_prompt = self._build_system_prompt(context)
        messages = [{"role": "system", "content": system_prompt}]
        
        # Adicionar histórico da conversa
        for msg in conversation_history[-10:]:  # Últimas 10 mensagens
            role = "user" if msg["direction"] == "incoming" else "assistant"
            messages.append({"role": role, "content": msg["content"]})
        
        # Adicionar mensagem atual
        messages.append({"role": "user", "content": user_message})
        
        try:
            response = await self.client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=messages,
                max_tokens=500,
                temperature=0.7
            )
            return response.choices[0].message.content.strip()
        except Exception as e:
            logger.error(f"Erro ao gerar resposta com IA: {e}")
            return "Desculpe, ocorreu um erro ao processar sua mensagem. Tente novamente."
    
    def _build_system_prompt(self, context: Optional[Dict] = None) -> str:
        """Constrói o prompt do sistema para a IA"""
        base_prompt = """
        Você é um assistente virtual especializado em atendimento ao cliente via WhatsApp.
        Suas características:
        
        1. Seja sempre cordial, prestativo e profissional
        2. Responda de forma clara e concisa
        3. Use linguagem natural e amigável
        4. Se não souber algo, seja honesto e ofereça alternativas
        5. Mantenha o foco em resolver o problema do cliente
        6. Use emojis moderadamente para tornar a conversa mais amigável
        7. Seja proativo em oferecer ajuda adicional
        
        Diretrizes específicas:
        - Sempre cumprimente o cliente de forma calorosa
        - Identifique a necessidade do cliente rapidamente
        - Ofereça soluções práticas e específicas
        - Se necessário, peça mais informações de forma educada
        - Encerre conversas de forma positiva
        
        Responda sempre em português brasileiro.
        """
        
        if context:
            context_info = f"\nInformações do contexto:\n{json.dumps(context, ensure_ascii=False)}"
            base_prompt += context_info
        
        return base_prompt
    
    async def analyze_sentiment(self, text: str) -> Dict[str, Any]:
        """Analisa o sentimento do texto"""
        try:
            response = await self.client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[
                    {
                        "role": "system", 
                        "content": "Analise o sentimento do texto e retorne apenas um JSON com: sentiment (positive/negative/neutral), confidence (0-1), emotions (lista de emoções detectadas)"
                    },
                    {"role": "user", "content": text}
                ],
                max_tokens=100,
                temperature=0.3
            )
            
            result = json.loads(response.choices[0].message.content)
            return result
        except Exception as e:
            logger.error(f"Erro ao analisar sentimento: {e}")
            return {"sentiment": "neutral", "confidence": 0.5, "emotions": []}
    
    async def extract_intent(self, text: str) -> Dict[str, Any]:
        """Extrai a intenção do usuário"""
        try:
            response = await self.client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[
                    {
                        "role": "system",
                        "content": """
                        Analise o texto e identifique a intenção do usuário. 
                        Retorne apenas um JSON com: intent (greeting/question/complaint/compliment/goodbye/other), 
                        entities (lista de entidades mencionadas), confidence (0-1)
                        """
                    },
                    {"role": "user", "content": text}
                ],
                max_tokens=150,
                temperature=0.3
            )
            
            result = json.loads(response.choices[0].message.content)
            return result
        except Exception as e:
            logger.error(f"Erro ao extrair intenção: {e}")
            return {"intent": "other", "entities": [], "confidence": 0.5}
    
    async def should_escalate_to_human(
        self, 
        conversation_history: List[Dict], 
        current_message: str
    ) -> bool:
        """Determina se a conversa deve ser escalada para um humano"""
        try:
            # Analisar sentimento
            sentiment = await self.analyze_sentiment(current_message)
            
            # Se sentimento muito negativo, escalar
            if sentiment["sentiment"] == "negative" and sentiment["confidence"] > 0.8:
                return True
            
            # Verificar palavras-chave que indicam necessidade de humano
            escalation_keywords = [
                "falar com humano", "atendente", "supervisor", "reclamação",
                "problema sério", "não resolve", "cancelar", "devolução"
            ]
            
            message_lower = current_message.lower()
            if any(keyword in message_lower for keyword in escalation_keywords):
                return True
            
            # Se muitas mensagens sem resolução, escalar
            if len(conversation_history) > 20:
                return True
            
            return False
        except Exception as e:
            logger.error(f"Erro ao determinar escalação: {e}")
            return False
