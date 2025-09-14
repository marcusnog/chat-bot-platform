"""
Value Object para número de telefone
"""
import re
from typing import Optional
from dataclasses import dataclass


@dataclass(frozen=True)
class PhoneNumber:
    """
    Value Object para representar um número de telefone do WhatsApp
    """
    value: str
    
    def __post_init__(self):
        """Valida o formato do número de telefone"""
        if not self._is_valid_phone_number(self.value):
            raise ValueError(f"Número de telefone inválido: {self.value}")
    
    @staticmethod
    def _is_valid_phone_number(phone: str) -> bool:
        """
        Valida se o número de telefone está no formato correto
        Formato esperado: +5511999999999 (código do país + DDD + número)
        """
        # Remove espaços e caracteres especiais
        cleaned_phone = re.sub(r'[^\d+]', '', phone)
        
        # Verifica se começa com + e tem pelo menos 10 dígitos
        pattern = r'^\+\d{10,15}$'
        return bool(re.match(pattern, cleaned_phone))
    
    def to_whatsapp_format(self) -> str:
        """
        Converte para formato usado pela API do WhatsApp
        Remove o + e mantém apenas os números
        """
        return self.value.replace('+', '')
    
    def to_display_format(self) -> str:
        """
        Converte para formato de exibição amigável
        """
        if self.value.startswith('+55'):
            # Formato brasileiro: +55 (11) 99999-9999
            country_code = self.value[:3]
            area_code = self.value[3:5]
            number = self.value[5:]
            
            if len(number) == 9:
                return f"{country_code} ({area_code}) {number[:5]}-{number[5:]}"
            else:
                return f"{country_code} ({area_code}) {number}"
        
        return self.value
    
    def __str__(self) -> str:
        return self.value
    
    def __repr__(self) -> str:
        return f"PhoneNumber('{self.value}')"
