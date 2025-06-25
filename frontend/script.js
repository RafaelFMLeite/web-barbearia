// script.js
const API_BASE_URL = 'http://localhost:8000'; // Endereço do seu backend FastAPI

// --- Variáveis Globais para o Estado do Frontend ---
let currentUserId = null;
let currentToken = null; // Em uma aplicação real, você usaria isso para autenticação
let professionals = [];
let services = [];

// --- Funções Auxiliares ---
function showMessage(elementId, message, type) {
    const element = document.getElementById(elementId);
    element.textContent = message;
    element.className = `message ${type}`;
    setTimeout(() => {
        element.textContent = '';
        element.className = 'message';
    }, 5000); // Esconde a mensagem após 5 segundos
}

function saveAuthData(userId, token) {
    localStorage.setItem('userId', userId);
    localStorage.setItem('token', token);
    currentUserId = userId;
    currentToken = token;
}

function clearAuthData() {
    localStorage.removeItem('userId');
    localStorage.removeItem('token');
    currentUserId = null;
    currentToken = null;
}

function checkAuthAndRedirect() {
    currentUserId = localStorage.getItem('userId');
    currentToken = localStorage.getItem('token');

    if (currentUserId && currentToken) {
        if (window.location.pathname.endsWith('index.html') || window.location.pathname === '/') {
            window.location.href = 'dashboard.html';
        }
    } else {
        if (window.location.pathname.endsWith('dashboard.html')) {
            window.location.href = 'index.html';
        }
    }
}

// --- Funções de Requisição ao Backend ---

// Autenticação
async function registerUser(name, email, password) {
    try {
        const response = await fetch(`${API_BASE_URL}/users/register`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ name, email, password })
        });
        const data = await response.json();
        if (response.ok) {
            showMessage('register-message', 'Registro bem-sucedido! Faça login agora.', 'success');
        } else {
            showMessage('register-message', data.detail || 'Erro ao registrar.', 'error');
        }
    } catch (error) {
        showMessage('register-message', 'Erro de conexão.', 'error');
        console.error('Erro de rede:', error);
    }
}

async function loginUser(email, password) {
    try {
        const response = await fetch(`${API_BASE_URL}/users/login`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ email, password })
        });
        const data = await response.json();
        if (response.ok) {
            saveAuthData(data.user_id, data.token);
            showMessage('login-message', 'Login bem-sucedido! Redirecionando...', 'success');
            setTimeout(() => {
                window.location.href = 'dashboard.html';
            }, 1000);
        } else {
            showMessage('login-message', data.detail || 'Credenciais inválidas.', 'error');
        }
    } catch (error) {
        showMessage('login-message', 'Erro de conexão.', 'error');
        console.error('Erro de rede:', error);
    }
}

// Carregar Dados do Dashboard
async function loadProfessionals() {
    try {
        const response = await fetch(`${API_BASE_URL}/professionals`);
        const data = await response.json();
        professionals = data; // Salva para uso no select
        const list = document.getElementById('professionals-list');
        const select = document.getElementById('prof-select');
        list.innerHTML = '';
        select.innerHTML = '<option value="">Selecione um profissional</option>'; // Opção default

        data.forEach(prof => {
            const li = document.createElement('li');
            li.textContent = `${prof.name} (${prof.specialty})`;
            list.appendChild(li);

            const option = document.createElement('option');
            option.value = prof.id;
            option.textContent = prof.name;
            select.appendChild(option);
        });
    } catch (error) {
        console.error('Erro ao carregar profissionais:', error);
    }
}

async function loadServices() {
    try {
        const response = await fetch(`${API_BASE_URL}/services`);
        const data = await response.json();
        services = data; // Salva para uso no select
        const list = document.getElementById('services-list');
        const select = document.getElementById('service-select');
        list.innerHTML = '';
        select.innerHTML = '<option value="">Selecione um serviço</option>'; // Opção default

        data.forEach(service => {
            const li = document.createElement('li');
            li.textContent = `${service.name} (${service.duration_minutes} min) - R$ ${service.price.toFixed(2)}`;
            list.appendChild(li);

            const option = document.createElement('option');
            option.value = service.id;
            option.textContent = `${service.name} (R$ ${service.price.toFixed(2)})`;
            select.appendChild(option);
        });
    } catch (error) {
        console.error('Erro ao carregar serviços:', error);
    }
}

async function loadAppointments() {
    if (!currentUserId) return; // Não carrega se não houver usuário logado
    try {
        const response = await fetch(`${API_BASE_URL}/users/${currentUserId}/appointments`);
        const data = await response.json();
        const list = document.getElementById('appointments-list');
        list.innerHTML = '';

        if (data.length === 0) {
            document.getElementById('appointments-message').textContent = "Você não possui agendamentos.";
            document.getElementById('appointments-message').className = "message";
            return;
        } else {
             document.getElementById('appointments-message').textContent = "";
        }


        data.sort((a, b) => new Date(a.start_time) - new Date(b.start_time)); // Ordena por data

        data.forEach(appt => {
            const li = document.createElement('li');
            
            const professional = professionals.find(p => p.id === appt.professional_id);
            const service = services.find(s => s.id === appt.service_id);

            const startTime = new Date(appt.start_time).toLocaleString('pt-BR', { dateStyle: 'short', timeStyle: 'short' });
            const endTime = new Date(appt.end_time).toLocaleString('pt-BR', { timeStyle: 'short' });

            li.innerHTML = `
                <div>
                    <strong>Serviço:</strong> ${service ? service.name : 'N/A'}<br>
                    <strong>Profissional:</strong> ${professional ? professional.name : 'N/A'}<br>
                    <strong>Quando:</strong> ${startTime} - ${endTime}<br>
                    <strong>Status:</strong> <span class="${appt.status.toLowerCase()}">${appt.status}</span>
                </div>
            `;

            if (appt.status === "Agendado") {
                const cancelButton = document.createElement('button');
                cancelButton.textContent = 'Cancelar';
                cancelButton.className = 'cancel-btn';
                cancelButton.onclick = () => cancelAppointment(appt.id);
                li.appendChild(cancelButton);
            } else if (appt.status === "Cancelado") {
                li.classList.add('cancelled'); // Adiciona classe para estilização de cancelado
            }
            list.appendChild(li);
        });

    } catch (error) {
        console.error('Erro ao carregar agendamentos:', error);
        document.getElementById('appointments-message').textContent = "Erro ao carregar agendamentos.";
        document.getElementById('appointments-message').className = "message error";
    }
}


// Gerenciamento de Agendamentos
async function scheduleAppointment(professionalId, serviceId, dateTime) {
    try {
        const response = await fetch(`${API_BASE_URL}/appointments`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({
                user_id: currentUserId,
                professional_id: professionalId,
                service_id: serviceId,
                start_time: dateTime
            })
        });
        const data = await response.json();
        if (response.ok) {
            showMessage('schedule-message', 'Agendamento realizado com sucesso!', 'success');
            loadAppointments(); // Recarrega a lista de agendamentos
        } else {
            showMessage('schedule-message', data.detail || 'Erro ao agendar.', 'error');
        }
    } catch (error) {
        showMessage('schedule-message', 'Erro de conexão.', 'error');
        console.error('Erro de rede:', error);
    }
}

async function cancelAppointment(appointmentId) {
    if (!confirm("Tem certeza que deseja cancelar este agendamento?")) {
        return;
    }
    try {
        const response = await fetch(`${API_BASE_URL}/appointments/${appointmentId}/cancel`, {
            method: 'PUT',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ user_id: currentUserId }) // Envia o user_id para validação no backend
        });
        const data = await response.json();
        if (response.ok) {
            alert('Agendamento cancelado com sucesso!'); // Usar alert simples para feedback rápido
            loadAppointments(); // Recarrega a lista de agendamentos
        } else {
            alert(data.detail || 'Erro ao cancelar agendamento.');
        }
    } catch (error) {
        alert('Erro de conexão ao cancelar agendamento.');
        console.error('Erro de rede:', error);
    }
}

// --- Event Listeners ---
document.addEventListener('DOMContentLoaded', () => {
    checkAuthAndRedirect(); // Verifica autenticação ao carregar qualquer página

    // Lógica para index.html
    if (document.getElementById('register-form')) {
        document.getElementById('register-form').addEventListener('submit', (e) => {
            e.preventDefault();
            const name = document.getElementById('register-name').value;
            const email = document.getElementById('register-email').value;
            const password = document.getElementById('register-password').value;
            registerUser(name, email, password);
        });

        document.getElementById('login-form').addEventListener('submit', (e) => {
            e.preventDefault();
            const email = document.getElementById('login-email').value;
            const password = document.getElementById('login-password').value;
            loginUser(email, password);
        });
    }

    // Lógica para dashboard.html
    if (document.getElementById('logout-button')) {
        document.getElementById('logout-button').addEventListener('click', () => {
            clearAuthData();
            window.location.href = 'index.html'; // Redireciona para a página de login
        });

        // Carrega dados iniciais para o dashboard
        loadProfessionals();
        loadServices();
        loadAppointments(); // Agendamentos dependem de user_id
        
        document.getElementById('schedule-form').addEventListener('submit', (e) => {
            e.preventDefault();
            const professionalId = parseInt(document.getElementById('prof-select').value);
            const serviceId = parseInt(document.getElementById('service-select').value);
            const date = document.getElementById('date-input').value;
            const time = document.getElementById('time-input').value;

            if (!professionalId || !serviceId || !date || !time) {
                showMessage('schedule-message', 'Por favor, preencha todos os campos.', 'error');
                return;
            }

            const dateTime = new Date(`${date}T${time}`); // Cria um objeto Date

            scheduleAppointment(professionalId, serviceId, dateTime.toISOString()); // Converte para ISO string para o backend
        });
    }
});