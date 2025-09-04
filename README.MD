# SISSUP - Sistema de Suporte ao Faturamento e Auditoria de Diálise

> **Visão:** Construir um núcleo sólido, juridicamente defensável e escalável, que reduza retrabalho, elimine perdas por glosas e sirva de ponte natural para um prontuário 100% digital.

**Status do Projeto:** MVP (Etapa 1) - Backend API funcional, Frontend em desenvolvimento.

---

## 1. Funcionalidades Essenciais (MVP Etapa 1)

O núcleo do backend foi projetado para suportar as seguintes funcionalidades:

1.  **Gestão Multi-Clínica:** Isola os dados por unidade de negócio (Clínica), com um sistema de permissões que associa usuários a uma ou mais clínicas.
2.  **Digitalização e Armazenamento Seguro:** Upload de documentos para um storage de objetos (MinIO), com separação por buckets (`pacientes`, `guias`) e cálculo de hash `SHA-256` para garantir a integridade.
3.  **Dossiês de Faturamento Genéricos:** Um modelo de `Guia` flexível para representar diferentes tipos de faturamento (APAC, SADT, Consulta, etc.), servindo como contêiner para os documentos de procedimento.
4.  **Parâmetros de Negócio Modulares:** Um sistema de regras que permite configurar a obrigatoriedade de documentos com base na combinação de Convênio, Tipo de Guia e Natureza (Crônico/Agudo).
5.  **Trilha de Auditoria Robusta:** Um modelo `AuditDecision` que registra as decisões de auditoria (Aprovado/Recusado) com uma "assinatura eletrônica" (hash da carga probatória), registrando quem fez, quando e o que foi auditado.
6.  **Ciclo de Vida do Paciente:** Gestão do status do paciente (Em Tratamento, Alta, Óbito, Transferido).

---

## 2. Arquitetura (API-First)

O projeto segue uma arquitetura moderna e desacoplada, preparando o caminho para futuras aplicações desktop (Tauri) e mobile (Capacitor).

### Backend (API)
-   **Framework:** Django + Django REST Framework (DRF)
-   **Responsabilidade:** Servir como uma API RESTful segura, gerenciando todas as regras de negócio, autenticação e persistência de dados.
-   **Banco de Dados:** PostgreSQL
-   **Armazenamento de Objetos:** MinIO

### Frontend (SPA - Single Page Application)
-   **Framework:** Vue.js
-   **UI Library:** Vuetify
-   **Responsabilidade:** Consumir a API do Django para construir uma interface de usuário rica, rápida e interativa. (Em desenvolvimento)

### Ambiente de Desenvolvimento
-   **Orquestração:** Docker & Docker Compose

---

## 3. Como Rodar o Ambiente de Desenvolvimento

Siga estes passos para configurar e executar o projeto localmente.

### Pré-requisitos
-   Git
-   Docker
-   Docker Compose

### 3.1. Configuração Inicial

1.  **Clone o repositório:**
    ```bash
    git clone https://github.com/TI-Nefron/projeto-sissup.git
    cd projeto-sissup
    ```

2.  **Crie o arquivo de ambiente:**
    Copie o arquivo de exemplo para criar seu arquivo de configuração local.
    ```bash
    cp .env.example .env
    ```
    *Nota: Se o `.env.example` não existir, crie um arquivo `.env` na raiz do projeto com o seguinte conteúdo:*
    ```env
    # Chave Secreta do Django (gere uma nova para produção)
    DJANGO_SECRET_KEY="substitua-por-uma-chave-aleatoria-e-longa"
    DJANGO_DEBUG=1

    # Hosts permitidos
    ALLOWED_HOSTS="127.0.0.1,localhost"

    # Configurações do Banco de Dados
    POSTGRES_DB=sissup_db
    POSTGRES_USER=sissup_user
    POSTGRES_PASSWORD=sissup_password

    # URL de Conexão para o Django (usa as variáveis acima)
    DATABASE_URL="postgres://${POSTGRES_USER}:${POSTGRES_PASSWORD}@db:5432/${POSTGRES_DB}"

    # Configurações do MinIO
    MINIO_ROOT_USER=minioadmin
    MINIO_ROOT_PASSWORD=minioadmin
    MINIO_ENDPOINT=minio:9000
    MINIO_BUCKET_PATIENT_DOCS=pacientes
    MINIO_BUCKET_GUIDE_DOCS=guias
    MINIO_USE_HTTPS=0
    ```

### 3.2. Iniciando o Backend (Django API)

**Importante:** Devido a uma dependência circular na criação inicial das migrações do Django (`AUTH_USER_MODEL`), o processo de inicialização de um banco de dados limpo deve seguir uma sequência específica.

#### Para a Primeira Vez ou Após um Reset Completo (`docker-compose down -v`)

1.  **Suba apenas o serviço de banco de dados:**
    ```bash
    docker-compose up -d db
    ```
    *Aguarde cerca de 10-15 segundos para o PostgreSQL inicializar completamente.*

2.  **Crie e aplique as migrações na ordem correta:**
    -   Primeiro, crie todos os arquivos de migração:
        ```bash
        docker-compose run --rm web python manage.py makemigrations accounts audit billing dialysis documents organization parameters
        ```
    -   Depois, aplique a migração do `accounts` para criar a tabela de usuário:
        ```bash
        docker-compose run --rm web python manage.py migrate accounts
        ```
    -   Finalmente, aplique todas as outras migrações:
        ```bash
        docker-compose run --rm web python manage.py migrate
        ```

3.  **Suba todos os serviços:**
    ```bash
    docker-compose up -d --build
    ```

4.  **Crie um superusuário** para acessar a Área Administrativa e a API:
    ```bash
    docker-compose exec web python manage.py createsuperuser
    ```

#### Para Iniciar e Parar no Dia a Dia

-   **Para iniciar:** `docker-compose up -d`
-   **Para parar:** `docker-compose down`

### 3.3. Acessando os Serviços

-   **Backend API (Django):**
    -   **Admin:** [http://localhost:8001/admin/](http://localhost:8001/admin/)
    -   **API (Exemplo Pacientes):** [http://localhost:8001/api/pacientes/](http://localhost:8001/api/pacientes/)
-   **Armazenamento (MinIO):**
    -   **Console:** [http://localhost:9091/](http://localhost:9091/)
    -   *Use as credenciais `MINIO_ROOT_USER` e `MINIO_ROOT_PASSWORD` do seu arquivo `.env`.*

### 3.4. (Futuro) Iniciando o Frontend (Vue.js)

1.  **Navegue até a pasta do frontend:**
    ```bash
    cd frontend
    ```
2.  **Instale as dependências:**
    ```bash
    npm install
    ```
3.  **Inicie o servidor de desenvolvimento:**
    ```bash
    npm run dev
    ```
    *O frontend estará acessível em um endereço como `http://localhost:5173/`.*

---

## 4. Próximos Passos

-   [ ] Desenvolver os componentes Vue.js para o dashboard e o fluxo de recepção.
-   [ ] Conectar o frontend aos endpoints da API do Django.
-   [ ] Implementar a lógica de permissões no frontend (ex: esconder/mostrar menus com base nos grupos do usuário).
-   [ ] Construir as telas de gestão de parâmetros e auditoria.