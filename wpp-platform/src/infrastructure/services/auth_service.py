"""
Serviço de autenticação
"""
import jwt
from datetime import datetime, timedelta
from passlib.context import CryptContext
from sqlalchemy.orm import Session
from src.infrastructure.database.auth_models import AuthUser
from config import settings
import logging

logger = logging.getLogger(__name__)

# Configuração de hash de senhas
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

class AuthService:
    """Serviço de autenticação"""
    
    def __init__(self, db: Session):
        self.db = db
    
    def verify_password(self, plain_password: str, hashed_password: str) -> bool:
        """Verifica se a senha está correta"""
        return pwd_context.verify(plain_password, hashed_password)
    
    def get_password_hash(self, password: str) -> str:
        """Gera hash da senha"""
        return pwd_context.hash(password)
    
    def create_access_token(self, data: dict, expires_delta: timedelta = None) -> str:
        """Cria token JWT"""
        to_encode = data.copy()
        if expires_delta:
            expire = datetime.utcnow() + expires_delta
        else:
            expire = datetime.utcnow() + timedelta(hours=24)
        
        to_encode.update({"exp": expire})
        encoded_jwt = jwt.encode(to_encode, settings.SECRET_KEY, algorithm="HS256")
        return encoded_jwt
    
    def verify_token(self, token: str) -> dict:
        """Verifica e decodifica token JWT"""
        try:
            payload = jwt.decode(token, settings.SECRET_KEY, algorithms=["HS256"])
            return payload
        except jwt.ExpiredSignatureError:
            raise Exception("Token expirado")
        except jwt.JWTError:
            raise Exception("Token inválido")
    
    def authenticate_user(self, email: str, password: str) -> AuthUser:
        """Autentica usuário com email e senha"""
        user = self.db.query(AuthUser).filter(AuthUser.email == email).first()
        
        if not user:
            raise Exception("Email ou senha incorretos")
        
        if not user.is_active:
            raise Exception("Usuário inativo")
        
        if not self.verify_password(password, user.password_hash):
            raise Exception("Email ou senha incorretos")
        
        # Atualizar último login
        user.last_login = datetime.utcnow()
        self.db.commit()
        
        return user
    
    def get_user_by_id(self, user_id: str) -> AuthUser:
        """Busca usuário por ID"""
        user = self.db.query(AuthUser).filter(AuthUser.id == user_id).first()
        if not user:
            raise Exception("Usuário não encontrado")
        return user
    
    def create_user(self, email: str, password: str, name: str, is_admin: bool = False) -> AuthUser:
        """Cria novo usuário"""
        # Verificar se email já existe
        existing_user = self.db.query(AuthUser).filter(AuthUser.email == email).first()
        if existing_user:
            raise Exception("Email já cadastrado")
        
        # Criar usuário
        user = AuthUser(
            email=email,
            password_hash=self.get_password_hash(password),
            name=name,
            is_admin=is_admin,
            is_active=True
        )
        
        self.db.add(user)
        self.db.commit()
        self.db.refresh(user)
        
        return user
    
    def update_user(self, user_id: str, **kwargs) -> AuthUser:
        """Atualiza dados do usuário"""
        user = self.get_user_by_id(user_id)
        
        for key, value in kwargs.items():
            if hasattr(user, key) and key != 'id':
                setattr(user, key, value)
        
        user.updated_at = datetime.utcnow()
        self.db.commit()
        self.db.refresh(user)
        
        return user
    
    def change_password(self, user_id: str, old_password: str, new_password: str) -> bool:
        """Altera senha do usuário"""
        user = self.get_user_by_id(user_id)
        
        if not self.verify_password(old_password, user.password_hash):
            raise Exception("Senha atual incorreta")
        
        user.password_hash = self.get_password_hash(new_password)
        user.updated_at = datetime.utcnow()
        self.db.commit()
        
        return True
