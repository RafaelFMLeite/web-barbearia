from pydantic import BaseModel, EmailStr, Field
from datetime import datetime, timedelta
from typing import List, Optional

# --- Modelos Base (Representação de Dados) ---

class UserBase(BaseModel):
    name: str
    email: EmailStr

class ProfessionalBase(BaseModel):
    name: str
    specialty: str # Ex: 'Corte de Cabelo', 'Barba', 'Pigmentação'

class ServiceBase(BaseModel):
    name: str
    description: Optional[str] = None
    duration_minutes: int = Field(..., gt=0, description="Duração do serviço em minutos")
    price: float = Field(..., gt=0, description="Preço do serviço")

class AppointmentBase(BaseModel):
    user_id: int
    professional_id: int
    service_id: int
    start_time: datetime
    # end_time será calculada automaticamente ou pode ser incluída se necessário para validação

# --- Modelos de Criação (Requisições POST) ---

class UserCreate(UserBase):
    password: str # Em um ambiente real, esta senha seria hashada com bcrypt, por exemplo.

class ProfessionalCreate(ProfessionalBase):
    pass

class ServiceCreate(ServiceBase):
    pass

class AppointmentCreate(AppointmentBase):
    pass

# --- Modelos de Resposta (Retorno das APIs) ---

class User(UserBase):
    id: int
    # Para segurança, a senha nunca deve ser retornada em uma resposta.
    class Config:
        from_attributes = True # Permite a criação do modelo a partir de atributos de ORM/objetos

class Professional(ProfessionalBase):
    id: int
    class Config:
        from_attributes = True

class Service(ServiceBase):
    id: int
    class Config:
        from_attributes = True

class Appointment(AppointmentBase):
    id: int
    status: str = "Agendado" # 'Agendado', 'Cancelado', 'Concluído'
    end_time: datetime # Calculado com base em start_time e service.duration_minutes
    class Config:
        from_attributes = True

# --- Modelos Específicos para Login/Cancelamento ---

class UserLogin(BaseModel):
    email: EmailStr
    password: str

class LoginResponse(BaseModel):
    message: str
    user_id: Optional[int] = None
    token: Optional[str] = None # Em um ambiente real, um JWT seria retornado aqui

class AppointmentCancel(BaseModel):
    user_id: int # Para validação de quem está cancelando