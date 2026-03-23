# Guia de instalação

Este guia descreve como configurar o ambiente local para executar o API Integrator.

## Pré-requisitos

- Python 3.10 ou superior
- pip (gerenciador de pacotes Python)

## Instalação

### 1. Clone o repositório

```bash
git clone <repository-url>
cd ai-integrator
```

### 2. Crie um ambiente virtual

```bash
# Windows
python -m venv venv
venv\Scripts\activate

# Linux/Mac
python3 -m venv venv
source venv/bin/activate
```

### 3. Instale as dependências

```bash
pip install -r requirements.txt
```

### 4. Configure as variáveis de ambiente

Copie o arquivo de exemplo e edite com suas configurações:

```bash
# Linux/Mac
cp .env.example .env

# Windows (PowerShell)
copy .env.example .env
```

Variáveis principais: `API_BASE_URL`, `JWT_SECRET`, `JWT_ALGORITHM`, `TOKEN_EXPIRY_MINUTES`, `HOST`, `PORT`.

## Execução

### Desenvolvimento

```bash
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

### Produção

```bash
uvicorn main:app --host 0.0.0.0 --port 8000 --workers 4
```

A API fica disponível em http://localhost:8000, com Swagger em `/docs` e ReDoc em `/redoc`.
