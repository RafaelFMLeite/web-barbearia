# Documentação do Projeto: Agendamento de Barbearia

---

## Resumo

Este trabalho consiste no desenvolvimento de uma aplicação web de **agendamento para barbearias**, utilizando **FastAPI** para o backend. O objetivo é proporcionar uma plataforma intuitiva onde usuários possam se cadastrar, visualizar serviços e profissionais disponíveis, e agendar, consultar ou cancelar seus horários de forma eficiente. O foco principal é na **modelagem de dados** e na criação de uma **API robusta** para gerenciar agendamentos, usuários, profissionais e serviços, demonstrando as capacidades do FastAPI para construir aplicações web modernas e escaláveis.

---

## 1. Tema

O trabalho final tem como tema o desenvolvimento de um **sistema de agendamento online para barbearias**, visando otimizar a gestão de horários e a experiência do cliente através de uma interface de programação de aplicações (API) bem definida e estruturada.

---

## 2. Escopo

Este projeto terá as seguintes funcionalidades:

* **Autenticação de Usuários**: Permite o registro e login de novos usuários na plataforma.
* **Gestão de Profissionais**: Permite a visualização de profissionais disponíveis na barbearia, com suas especialidades.
* **Gestão de Serviços**: Permite a visualização dos serviços oferecidos, com detalhes como nome, descrição, duração e preço.
* **Agendamento de Serviços**: Usuários logados podem agendar serviços com profissionais específicos em horários disponíveis.
* **Consulta de Agendamentos**: Usuários podem visualizar os detalhes de seus agendamentos futuros e passados.
* **Cancelamento de Agendamentos**: Usuários podem cancelar agendamentos, com validações para evitar cancelamentos de última hora.

---

## 3. Restrições

Neste trabalho não serão considerados:

* **Integração com Banco de Dados Persistente**: Para fins de protótipo, os dados são armazenados em memória e serão perdidos ao reiniciar a aplicação.
* **Interface de Usuário (Frontend)**: O foco é exclusivamente no desenvolvimento da API de backend.
* **Pagamentos Online**: Não há integração com sistemas de pagamento para os serviços agendados.
* **Autenticação e Autorização Completas**: A implementação de login é simplificada, sem uso de JWTs ou gerenciamento de sessões complexo, e não há controle de acesso baseado em perfis (roles) para administradores ou profissionais.
* **Lógica de Disponibilidade Complexa**: A verificação de horários disponíveis é básica e não considera intervalos de almoço, folgas de profissionais, ou múltiplas salas/cadeiras.
* **Notificações**: Não há implementação de envio de e-mails, SMS ou notificações push sobre agendamentos.

---

## 4. Protótipo

Protótipos para as seguintes páginas/funcionalidades da API (endpoints) foram elaborados:

* **Usuários**:
    * `POST /users/register`: Registro de novos usuários.
    * `POST /users/login`: Autenticação de usuários.
* **Profissionais**:
    * `POST /professionals`: Criação de um novo profissional (para administração interna, exemplificativo).
    * `GET /professionals`: Listagem de todos os profissionais.
* **Serviços**:
    * `POST /services`: Criação de um novo serviço (para administração interna, exemplificativo).
    * `GET /services`: Listagem de todos os serviços disponíveis.
* **Agendamentos**:
    * `POST /appointments`: Criação de um novo agendamento.
    * `GET /appointments/{appointment_id}`: Detalhes de um agendamento específico.
    * `GET /users/{user_id}/appointments`: Listagem de agendamentos de um usuário.
    * `PUT /appointments/{appointment_id}/cancel`: Cancelamento de um agendamento.

Os protótipos completos, incluindo a modelagem de dados (Pydantic) e a implementação dos endpoints FastAPI, podem ser encontrados nos arquivos `models.py` e `main.py` da estrutura do projeto. A documentação interativa da API (Swagger UI) está disponível ao executar a aplicação em `http://127.0.0.1:8000/docs`.

---

## 5. Referências

Não aplicável no momento, mas referências a documentações do FastAPI, Pydantic, Uvicorn e quaisquer bibliotecas adicionais utilizadas seriam incluídas aqui, seguindo o padrão ABNT, caso o projeto utilizasse fontes externas específicas de forma mais aprofundada.
