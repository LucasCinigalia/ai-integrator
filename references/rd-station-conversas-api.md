# RD Station Conversas API v2 - Referência

**Fonte**: https://developers.rdstation.com/reference/conversas-v2-introduction  
**Data de consulta**: 23/03/2026  
**Método**: Context7 MCP

---

## 📋 Índice

1. [Visão Geral](#visão-geral)
2. [Autenticação](#autenticação)
3. [Endpoints Principais](#endpoints-principais)
4. [Recursos Disponíveis](#recursos-disponíveis)
5. [Integração com o Projeto](#integração-com-o-projeto)

---

## 🎯 Visão Geral

A **RD Station Conversas API v2** é uma API REST que permite integração com a plataforma de conversas do RD Station, possibilitando:

- Gerenciamento de contatos
- Envio e recebimento de mensagens
- Integração com WhatsApp Business
- Automação de workflows
- Gerenciamento de campos personalizados
- Relatórios e análises

**Base URL**: A ser confirmada na documentação oficial  
**Formato**: JSON  
**Protocolo**: HTTPS

---

## 🔐 Autenticação

A API do RD Station Conversas v2 utiliza **OAuth 2.0** para autenticação.

### Fluxo de Autenticação

1. **Criar aplicativo** na App Store do RD Station
2. **Obter credenciais**: `client_id` e `client_secret`
3. **Gerar código de autorização** (authorization code)
4. **Trocar código por tokens**: `access_token` e `refresh_token`
5. **Renovar token** quando expirar usando `refresh_token`

### Endpoints de Autenticação

```
POST /auth/token - Obter access_token
POST /auth/token - Renovar access_token (usando refresh_token)
POST /auth/revoke - Revogar token
```

### Headers de Autenticação

```http
Authorization: Bearer {access_token}
Content-Type: application/json
```

---

## 📡 Endpoints Principais

### Contatos

| Método | Endpoint | Descrição |
|--------|----------|-----------|
| `GET` | `/contacts` | Listar contatos |
| `POST` | `/contacts` | Criar contato |
| `POST` | `/contacts/bulk` | Criar múltiplos contatos |
| `GET` | `/contacts/phone/{phone}` | Obter contato por telefone |
| `GET` | `/contacts/cpf/{cpf}` | Obter contato por CPF |
| `PATCH` | `/contacts/phone/{phone}` | Atualizar contato por telefone |
| `DELETE` | `/contacts` | Deletar múltiplos contatos |
| `POST` | `/contacts/whatsapp` | Criar contato WhatsApp Business |
| `PUT` | `/contacts/whatsapp` | Atualizar contato WhatsApp Business |
| `POST` | `/contacts/portfolio/delete` | Deletar contatos da carteira |

### Mensagens

| Método | Endpoint | Descrição |
|--------|----------|-----------|
| `POST` | `/messages` | Enviar mensagem |
| `POST` | `/messages/forward` | Encaminhar mensagem |
| `POST` | `/messages/template` | Enviar mensagem via template |
| `POST` | `/messages/template/filled` | Enviar mensagem via template preenchido |
| `GET` | `/messages/history` | Listar histórico de conversas |

### Templates

| Método | Endpoint | Descrição |
|--------|----------|-----------|
| `GET` | `/templates` | Listar templates de mensagens |
| `POST` | `/templates/send` | Enviar mensagem a partir de template |

### Campos Personalizados

| Método | Endpoint | Descrição |
|--------|----------|-----------|
| `GET` | `/custom-fields` | Listar campos personalizados |
| `POST` | `/custom-fields` | Criar campo personalizado |
| `GET` | `/custom-fields/{id}` | Obter campo personalizado |
| `PUT` | `/custom-fields/{id}` | Atualizar campo personalizado |
| `DELETE` | `/custom-fields/{id}` | Deletar campo personalizado |

### Funcionários

| Método | Endpoint | Descrição |
|--------|----------|-----------|
| `GET` | `/employees` | Listar funcionários |
| `PUT` | `/employees/{id}/activate` | Ativar funcionário |
| `PUT` | `/employees/{id}/deactivate` | Desativar funcionário |
| `POST` | `/employees/bulk` | Criar múltiplos funcionários |
| `PATCH` | `/employees/bulk/deactivate` | Desativar múltiplos funcionários |

### Workflows e Flows

| Método | Endpoint | Descrição |
|--------|----------|-----------|
| `GET` | `/workflows` | Listar workflows |
| `GET` | `/flows` | Listar fluxos |
| `POST` | `/flows/restart` | Reiniciar fluxos |

### Carteiras

| Método | Endpoint | Descrição |
|--------|----------|-----------|
| `GET` | `/portfolios` | Listar carteiras |
| `POST` | `/portfolios/contacts` | Adicionar contato na carteira |
| `PATCH` | `/portfolios/contacts` | Deletar contato da carteira |

### WhatsApp

| Método | Endpoint | Descrição |
|--------|----------|-----------|
| `GET` | `/whatsapp/integrations` | Listar integrações de WhatsApp |
| `GET` | `/whatsapp/integrations/official` | Listar integrações oficiais |

### Relatórios

| Método | Endpoint | Descrição |
|--------|----------|-----------|
| `GET` | `/reports` | Listar relatórios |

### Jobs

| Método | Endpoint | Descrição |
|--------|----------|-----------|
| `GET` | `/jobs/{id}` | Obter status de job |

---

## 🔧 Recursos Disponíveis

### 1. Contatos
- Criação individual ou em lote
- Busca por telefone, CPF ou outros identificadores
- Atualização de dados
- Exclusão individual ou em lote
- Integração com WhatsApp Business
- Gerenciamento de carteiras

### 2. Mensagens
- Envio de mensagens diretas
- Envio via templates
- Encaminhamento de mensagens
- Histórico de conversas
- Suporte a WhatsApp Business

### 3. Templates
- Listagem de templates disponíveis
- Envio de mensagens usando templates
- Templates preenchidos dinamicamente

### 4. Campos Personalizados
- CRUD completo de campos personalizados
- Personalização de dados de contatos

### 5. Automação
- Workflows
- Fluxos (Flows)
- Reinicialização de fluxos

### 6. Integrações
- WhatsApp Business (oficial e broker)
- Criptografia de dados
- Webhooks (via API multiproduto)

### 7. Relatórios
- Análises de conversas
- Métricas de atendimento

---

## 🔗 Integração com o Projeto

### Arquitetura Proposta

```
app/
├── models/
│   └── rd_conversas_schemas.py    # Pydantic models para API Conversas
├── clients/
│   └── rd_conversas_client.py     # HTTP client para API Conversas
├── services/
│   └── rd_conversas_service.py    # Lógica de negócio
└── api/
    └── routes/
        └── rd_conversas.py         # FastAPI endpoints
```

### Configurações Necessárias (.env)

```env
# RD Station Conversas API
RD_CONVERSAS_CLIENT_ID=seu_client_id
RD_CONVERSAS_CLIENT_SECRET=seu_client_secret
RD_CONVERSAS_BASE_URL=https://api.rdstation.com/conversas/v2
RD_CONVERSAS_AUTH_URL=https://api.rdstation.com/auth
```

### Modelos Pydantic Sugeridos

```python
# app/models/rd_conversas_schemas.py

from pydantic import BaseModel, Field
from typing import Optional, List
from datetime import datetime

class ConversasContact(BaseModel):
    """Modelo de contato do RD Conversas."""
    phone: str = Field(..., description="Telefone do contato")
    name: Optional[str] = None
    email: Optional[str] = None
    cpf: Optional[str] = None
    custom_fields: Optional[dict] = None

class ConversasMessage(BaseModel):
    """Modelo de mensagem do RD Conversas."""
    contact_phone: str = Field(..., description="Telefone do destinatário")
    message: str = Field(..., description="Conteúdo da mensagem")
    template_id: Optional[str] = None

class ConversasTemplate(BaseModel):
    """Modelo de template de mensagem."""
    id: str
    name: str
    content: str
    variables: Optional[List[str]] = None
```

### Client HTTP Sugerido

```python
# app/clients/rd_conversas_client.py

from typing import Optional, List, Dict, Any
import httpx
from app.core.config import settings
from app.core.auth import JWTManager

class RDConversasClient:
    """Cliente HTTP para API do RD Station Conversas v2."""
    
    def __init__(self):
        self.base_url = settings.rd_conversas_base_url
        self.auth_manager = JWTManager(
            client_id=settings.rd_conversas_client_id,
            client_secret=settings.rd_conversas_client_secret,
            token_url=f"{settings.rd_conversas_auth_url}/token"
        )
    
    async def _get_headers(self) -> Dict[str, str]:
        """Retorna headers com token de autenticação."""
        token = await self.auth_manager.get_token()
        return {
            "Authorization": f"Bearer {token}",
            "Content-Type": "application/json"
        }
    
    async def get_contacts(self, limit: int = 100) -> List[Dict[str, Any]]:
        """Lista contatos."""
        async with httpx.AsyncClient() as client:
            headers = await self._get_headers()
            response = await client.get(
                f"{self.base_url}/contacts",
                headers=headers,
                params={"limit": limit}
            )
            response.raise_for_status()
            return response.json()
    
    async def create_contact(self, contact_data: Dict[str, Any]) -> Dict[str, Any]:
        """Cria novo contato."""
        async with httpx.AsyncClient() as client:
            headers = await self._get_headers()
            response = await client.post(
                f"{self.base_url}/contacts",
                headers=headers,
                json=contact_data
            )
            response.raise_for_status()
            return response.json()
    
    async def send_message(self, message_data: Dict[str, Any]) -> Dict[str, Any]:
        """Envia mensagem."""
        async with httpx.AsyncClient() as client:
            headers = await self._get_headers()
            response = await client.post(
                f"{self.base_url}/messages",
                headers=headers,
                json=message_data
            )
            response.raise_for_status()
            return response.json()
```

---

## 📚 Recursos Adicionais

### Links Importantes

- **Documentação oficial**: https://developers.rdstation.com/reference/conversas-v2-introduction
- **App Store RD Station**: https://appstore.rdstation.com/
- **Suporte**: https://ajuda.rdstation.com/
- **Status da API**: https://status.rdstation.com/

### Outras APIs RD Station

- **RD Station Marketing API**: Para gestão de leads e automação de marketing
- **RD Station CRM API v1**: Para gestão de vendas (versão antiga)
- **RD Station CRM API v2**: Para gestão de vendas (versão nova)
- **Webhook Service**: Para receber notificações de eventos

### Próximos Passos

1. ✅ Documentação da API adicionada
2. ⏳ Criar modelos Pydantic (`rd_conversas_schemas.py`)
3. ⏳ Implementar client HTTP (`rd_conversas_client.py`)
4. ⏳ Implementar service layer (`rd_conversas_service.py`)
5. ⏳ Criar endpoints FastAPI (`rd_conversas.py`)
6. ⏳ Adicionar testes unitários
7. ⏳ Adicionar testes de integração
8. ⏳ Documentar no README.md

---

## 🔄 Histórico de Atualizações

| Data | Versão | Mudanças |
|------|--------|----------|
| 2026-03-23 | 1.0.0 | Criação inicial via Context7 MCP |

---

**Nota**: Esta documentação foi gerada automaticamente usando o MCP Context7 para consultar a documentação oficial do RD Station. Para informações mais detalhadas e atualizadas, sempre consulte a [documentação oficial](https://developers.rdstation.com/reference/conversas-v2-introduction).
