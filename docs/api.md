# API e endpoints

Documentação dos endpoints REST expostos pelo API Integrator.

## Base URL

`http://localhost:8000` (desenvolvimento)

## Endpoints gerais

### Root

```http
GET /
```

Retorna informações básicas (nome, versão, status e links para docs e health).

### Health check

```http
GET /health
```

Retorna o status de saúde da aplicação.

## Items

### Listar items

```http
GET /items
```

### Buscar item por ID

```http
GET /items/{item_id}
```

### Criar item

```http
POST /items
Content-Type: application/json

{
  "name": "Nome do item",
  "description": "Descrição opcional"
}
```

### Atualizar item

```http
PUT /items/{item_id}
Content-Type: application/json

{
  "name": "Nome atualizado",
  "description": "Nova descrição"
}
```

### Deletar item

```http
DELETE /items/{item_id}
```

## Autenticação

O cliente HTTP interno usa JWT automático via `JWTManager`. Tokens são gerados, validados e renovados automaticamente nas requisições à API externa.
