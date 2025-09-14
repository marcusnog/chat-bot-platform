"""
Inicialização do banco de dados para a nova arquitetura DDD
"""
from sqlalchemy import create_engine
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(__file__)))))

from config import settings
from src.infrastructure.database.models import Base
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def init_database():
    """Inicializa o banco de dados"""
    try:
        engine = create_engine(settings.DATABASE_URL)
        
        # Criar todas as tabelas
        Base.metadata.create_all(bind=engine)
        
        logger.info("Banco de dados inicializado com sucesso!")
        
        # Inserir dados iniciais
        insert_initial_data(engine)
        
    except Exception as e:
        logger.error(f"Erro ao inicializar banco de dados: {e}")
        raise

def insert_initial_data(engine):
    """Insere dados iniciais no banco"""
    from sqlalchemy.orm import sessionmaker
    from src.infrastructure.database.models import BotResponseModel, AgentModel
    
    Session = sessionmaker(bind=engine)
    session = Session()
    
    try:
        # Verificar se já existem dados
        if session.query(BotResponseModel).count() == 0:
            # Inserir respostas automáticas iniciais
            initial_responses = [
                BotResponseModel(
                    trigger_keywords=["oi", "olá", "bom dia", "boa tarde", "boa noite"],
                    response_text="Olá! 👋 Como posso ajudá-lo hoje?",
                    response_type="text",
                    priority=10
                ),
                BotResponseModel(
                    trigger_keywords=["ajuda", "help", "suporte"],
                    response_text="Claro! Estou aqui para ajudar. Qual é sua dúvida?",
                    response_type="text",
                    priority=9
                ),
                BotResponseModel(
                    trigger_keywords=["preço", "valor", "custo", "quanto"],
                    response_text="Para informações sobre preços, posso conectá-lo com nosso time comercial. Aguarde um momento!",
                    response_type="text",
                    priority=8
                ),
                BotResponseModel(
                    trigger_keywords=["obrigado", "valeu", "thanks"],
                    response_text="De nada! 😊 Foi um prazer ajudar. Precisa de mais alguma coisa?",
                    response_type="text",
                    priority=7
                ),
                BotResponseModel(
                    trigger_keywords=["tchau", "até logo", "bye"],
                    response_text="Até logo! 👋 Foi um prazer conversar com você. Volte sempre!",
                    response_type="text",
                    priority=6
                )
            ]
            
            for response in initial_responses:
                session.add(response)
            
            logger.info("Respostas automáticas iniciais inseridas")
        
        if session.query(AgentModel).count() == 0:
            # Inserir agentes iniciais
            initial_agents = [
                AgentModel(
                    name="João Silva",
                    email="joao@example.com",
                    phone_number="+5511999999999",
                    max_conversations=15,
                    current_conversations=0
                ),
                AgentModel(
                    name="Maria Santos",
                    email="maria@example.com",
                    phone_number="+5511888888888",
                    max_conversations=15,
                    current_conversations=0
                )
            ]
            
            for agent in initial_agents:
                session.add(agent)
            
            logger.info("Agentes iniciais inseridos")
        
        session.commit()
        logger.info("Dados iniciais inseridos com sucesso!")
        
    except Exception as e:
        session.rollback()
        logger.error(f"Erro ao inserir dados iniciais: {e}")
        raise
    finally:
        session.close()

if __name__ == "__main__":
    init_database()
