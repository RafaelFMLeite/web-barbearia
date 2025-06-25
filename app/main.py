from fastapi import FastAPI, HTTPException, status
from typing import List, Dict
from datetime import datetime, timedelta
from models import (
    User, UserCreate, UserLogin, LoginResponse,
    Professional, ProfessionalCreate,
    Service, ServiceCreate,
    Appointment, AppointmentCreate, AppointmentCancel
)

app = FastAPI(
    title="Barber Shop Scheduling API",
    description="API para agendamento de serviços em uma barbearia.",
    version="1.0.0"
)

# --- Banco de Dados em Memória (Para fins de protótipo) ---
# Em uma aplicação real, você usaria um ORM como SQLAlchemy com um banco de dados.
users_db: Dict[int, User] = {}
professionals_db: Dict[int, Professional] = {}
services_db: Dict[int, Service] = {}
appointments_db: Dict[int, Appointment] = {}

# Contadores de ID para simular o autoincremento do banco de dados
next_user_id = 1
next_professional_id = 1
next_service_id = 1
next_appointment_id = 1

# --- Endpoints de Usuários ---
@app.post("/users/register", response_model=User, status_code=status.HTTP_201_CREATED)
async def register_user(user_data: UserCreate):
    global next_user_id
    # Simula verificação de email existente
    if any(user.email == user_data.email for user in users_db.values()):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Email já registrado.")

    # Em uma aplicação real, user_data.password seria hashada aqui (ex: bcrypt.hashpw)
    new_user = User(id=next_user_id, name=user_data.name, email=user_data.email)
    users_db[next_user_id] = new_user
    next_user_id += 1
    return new_user

@app.post("/users/login", response_model=LoginResponse)
async def login_user(user_data: UserLogin):
    # Simula autenticação
    for user_id, user in users_db.items():
        if user.email == user_data.email:
            # Em uma aplicação real, você compararia o hash da senha:
            # if bcrypt.checkpw(user_data.password.encode('utf-8'), user.hashed_password.encode('utf-8')):
            # Para o protótipo, assumimos uma senha "fixa" para simular o login após o registro.
            if user_data.password == "password123": # <--- ATENÇÃO: Substitua por hash real em produção!
                 return LoginResponse(
                    message="Login bem-sucedido!",
                    user_id=user.id,
                    token="mock-jwt-token-for-user-" + str(user.id) # Em um ambiente real, um JWT seria gerado
                )
            else:
                raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Credenciais inválidas")
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Usuário não encontrado")


# --- Endpoints de Profissionais ---
@app.post("/professionals", response_model=Professional, status_code=status.HTTP_201_CREATED)
async def create_professional(professional_data: ProfessionalCreate):
    global next_professional_id
    new_professional = Professional(id=next_professional_id, **professional_data.model_dump()) # .model_dump() para Pydantic v2
    professionals_db[next_professional_id] = new_professional
    next_professional_id += 1
    return new_professional

@app.get("/professionals", response_model=List[Professional])
async def get_professionals():
    return list(professionals_db.values())

# --- Endpoints de Serviços ---
@app.post("/services", response_model=Service, status_code=status.HTTP_201_CREATED)
async def create_service(service_data: ServiceCreate):
    global next_service_id
    new_service = Service(id=next_service_id, **service_data.model_dump()) # .model_dump() para Pydantic v2
    services_db[next_service_id] = new_service
    next_service_id += 1
    return new_service

@app.get("/services", response_model=List[Service])
async def get_services():
    return list(services_db.values())

# --- Endpoints de Agendamentos ---
@app.post("/appointments", response_model=Appointment, status_code=status.HTTP_201_CREATED)
async def create_appointment(appointment_data: AppointmentCreate):
    global next_appointment_id

    # Validações de existência de entidades
    if appointment_data.user_id not in users_db:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Usuário não encontrado.")
    if appointment_data.professional_id not in professionals_db:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Profissional não encontrado.")
    if appointment_data.service_id not in services_db:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Serviço não encontrado.")

    service = services_db[appointment_data.service_id]
    end_time = appointment_data.start_time + timedelta(minutes=service.duration_minutes)

    # Regra de Negócio: Não permite agendar no passado
    if appointment_data.start_time < datetime.now():
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Não é possível agendar um serviço no passado.")

    # Simula verificação de disponibilidade (muito básica para o protótipo)
    # Em uma aplicação real, você teria uma lógica de agendamento mais robusta,
    # considerando janelas de tempo, breaks, etc.
    for existing_appt in appointments_db.values():
        if (existing_appt.professional_id == appointment_data.professional_id and
            existing_appt.status == "Agendado" and
            # Verifica sobreposição de horários
            not (end_time <= existing_appt.start_time or appointment_data.start_time >= existing_appt.end_time)):
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="Horário já ocupado para este profissional. Escolha outro horário."
            )

    new_appointment = Appointment(
        id=next_appointment_id,
        user_id=appointment_data.user_id,
        professional_id=appointment_data.professional_id,
        service_id=appointment_data.service_id,
        start_time=appointment_data.start_time,
        end_time=end_time,
        status="Agendado"
    )
    appointments_db[next_appointment_id] = new_appointment
    next_appointment_id += 1
    return new_appointment

@app.get("/appointments/{appointment_id}", response_model=Appointment)
async def get_appointment_details(appointment_id: int):
    appointment = appointments_db.get(appointment_id)
    if not appointment:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Agendamento não encontrado.")
    return appointment

@app.get("/users/{user_id}/appointments", response_model=List[Appointment])
async def get_user_appointments(user_id: int):
    if user_id not in users_db:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Usuário não encontrado.")
    
    user_appointments = [appt for appt in appointments_db.values() if appt.user_id == user_id]
    return user_appointments

@app.put("/appointments/{appointment_id}/cancel", response_model=Appointment)
async def cancel_appointment(appointment_id: int, cancellation_data: AppointmentCancel):
    appointment = appointments_db.get(appointment_id)
    if not appointment:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Agendamento não encontrado.")
    
    # Valida se o usuário que está tentando cancelar é o dono do agendamento
    # Em um sistema real, isso seria feito com base no JWT do usuário autenticado.
    if appointment.user_id != cancellation_data.user_id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Você não tem permissão para cancelar este agendamento.")

    if appointment.status == "Cancelado":
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Agendamento já está cancelado.")
    
    # Regra de negócio: Não permite cancelar agendamentos que estão muito próximos (ex: menos de 2 horas de antecedência)
    if appointment.start_time - datetime.now() < timedelta(hours=2):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Não é possível cancelar agendamentos com menos de 2 horas de antecedência.")

    appointment.status = "Cancelado"
    return appointment

# --- Exemplo de dados iniciais (opcional, para testes rápidos) ---
@app.on_event("startup")
async def startup_event():
    print("Preenchendo dados iniciais para protótipo...")
    global next_user_id, next_professional_id, next_service_id

    # Usuários
    users_db[next_user_id] = User(id=next_user_id, name="João Silva", email="joao@example.com")
    next_user_id += 1
    users_db[next_user_id] = User(id=next_user_id, name="Maria Souza", email="maria@example.com")
    next_user_id += 1

    # Profissionais
    professionals_db[next_professional_id] = Professional(id=next_professional_id, name="Carlos O Barbeiro", specialty="Cortes Clássicos e Barba")
    next_professional_id += 1
    professionals_db[next_professional_id] = Professional(id=next_professional_id, name="Ana Estilista", specialty="Cortes Femininos e Colorimetria")
    next_professional_id += 1

    # Serviços
    services_db[next_service_id] = Service(id=next_service_id, name="Corte Masculino", description="Corte de cabelo masculino clássico.", duration_minutes=45, price=50.00)
    next_service_id += 1
    services_db[next_service_id] = Service(id=next_service_id, name="Barba Completa", description="Barba, toalha quente e finalização.", duration_minutes=30, price=40.00)
    next_service_id += 1
    services_db[next_service_id] = Service(id=next_service_id, name="Corte Feminino", description="Corte de cabelo feminino com lavagem.", duration_minutes=60, price=80.00)
    next_service_id += 1

    print("Dados iniciais preenchidos.")