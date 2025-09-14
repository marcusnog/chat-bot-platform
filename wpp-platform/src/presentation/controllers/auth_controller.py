"""
Endpoints de autenticação
"""
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from sqlalchemy.orm import Session
from pydantic import BaseModel, EmailStr
from typing import Optional
from datetime import timedelta

from src.infrastructure.database.database import get_db
from src.infrastructure.services.auth_service import AuthService
from src.infrastructure.database.auth_models import AuthUser
from config import settings

router = APIRouter(prefix="/auth", tags=["authentication"])
security = HTTPBearer()

# Schemas
class LoginRequest(BaseModel):
    email: EmailStr
    password: str

class LoginResponse(BaseModel):
    token: str
    user: dict
    token_type: str = "bearer"

class UserResponse(BaseModel):
    id: str
    email: str
    name: str
    is_active: bool
    is_admin: bool
    created_at: Optional[str] = None
    last_login: Optional[str] = None

class ChangePasswordRequest(BaseModel):
    old_password: str
    new_password: str

# Dependências
def get_auth_service(db: Session = Depends(get_db)) -> AuthService:
    return AuthService(db)

def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(security),
    auth_service: AuthService = Depends(get_auth_service)
):
    """Obtém usuário atual através do token"""
    try:
        payload = auth_service.verify_token(credentials.credentials)
        user_id = payload.get("sub")
        if user_id is None:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Token inválido"
            )
        user = auth_service.get_user_by_id(user_id)
        return user
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=str(e)
        )

# Endpoints
@router.post("/login", response_model=LoginResponse)
async def login(
    login_data: LoginRequest,
    auth_service: AuthService = Depends(get_auth_service)
):
    """Endpoint de login"""
    try:
        user = auth_service.authenticate_user(login_data.email, login_data.password)
        
        # Criar token
        access_token = auth_service.create_access_token(
            data={"sub": user.id, "email": user.email},
            expires_delta=timedelta(hours=24)
        )
        
        return LoginResponse(
            token=access_token,
            user=user.to_dict(),
            token_type="bearer"
        )
        
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=str(e)
        )

@router.get("/me", response_model=UserResponse)
async def get_current_user_info(
    current_user: AuthUser = Depends(get_current_user)
):
    """Obtém informações do usuário atual"""
    return UserResponse(**current_user.to_dict())

@router.post("/change-password")
async def change_password(
    password_data: ChangePasswordRequest,
    current_user: AuthUser = Depends(get_current_user),
    auth_service: AuthService = Depends(get_auth_service)
):
    """Altera senha do usuário atual"""
    try:
        auth_service.change_password(
            current_user.id,
            password_data.old_password,
            password_data.new_password
        )
        return {"message": "Senha alterada com sucesso"}
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )

@router.post("/logout")
async def logout():
    """Endpoint de logout (client-side)"""
    return {"message": "Logout realizado com sucesso"}

@router.get("/verify-token")
async def verify_token(
    current_user: AuthUser = Depends(get_current_user)
):
    """Verifica se o token é válido"""
    return {"valid": True, "user": current_user.to_dict()}
