"""
Script para inicializar banco de dados com usuários de autenticação
"""
import sys
import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from datetime import datetime

# Adicionar o diretório raiz ao path
sys.path.append(os.path.dirname(os.path.dirname(__file__)))

from config import settings
from src.infrastructure.database.auth_models import AuthUser, Base
from src.infrastructure.services.auth_service import AuthService

def init_auth_db():
    """Inicializa banco de dados com usuários de autenticação"""
    
    # Criar engine
    engine = create_engine(settings.DATABASE_URL)
    
    # Criar tabelas
    Base.metadata.create_all(bind=engine)
    
    # Criar sessão
    SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
    db = SessionLocal()
    
    try:
        # Criar serviço de autenticação
        auth_service = AuthService(db)
        
        # Verificar se já existem usuários
        existing_users = db.query(AuthUser).count()
        if existing_users > 0:
            print("✅ Usuários já existem no banco de dados")
            return
        
        # Criar usuário administrador
        admin_user = auth_service.create_user(
            email="admin@whatsapp-platform.com",
            password="admin123",
            name="Administrador",
            is_admin=True
        )
        print(f"✅ Usuário administrador criado: {admin_user.email}")
        
        # Criar usuário demo
        demo_user = auth_service.create_user(
            email="demo@whatsapp-platform.com",
            password="demo123",
            name="Usuário Demo",
            is_admin=False
        )
        print(f"✅ Usuário demo criado: {demo_user.email}")
        
        # Criar usuário teste
        test_user = auth_service.create_user(
            email="teste@whatsapp-platform.com",
            password="teste123",
            name="Usuário Teste",
            is_admin=False
        )
        print(f"✅ Usuário teste criado: {test_user.email}")
        
        print("\n🎉 Banco de dados de autenticação inicializado com sucesso!")
        print("\n📋 Usuários criados:")
        print("   👤 admin@whatsapp-platform.com / admin123 (Admin)")
        print("   👤 demo@whatsapp-platform.com / demo123 (User)")
        print("   👤 teste@whatsapp-platform.com / teste123 (User)")
        
    except Exception as e:
        print(f"❌ Erro ao inicializar banco de dados: {e}")
        db.rollback()
    finally:
        db.close()

if __name__ == "__main__":
    init_auth_db()
