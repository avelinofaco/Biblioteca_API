# Sistema de Biblioteca Digital

Sistema completo de gerenciamento de biblioteca desenvolvido com FastAPI e SQLModel, implementando todas as funcionalidades solicitadas.

## 🎯 Funcionalidades Implementadas

### ✅ F1 - Inserir entidades no banco de dados
- Endpoints POST para todas as entidades
- Validação de dados com Pydantic

### ✅ F2 - Listar todas as entidades
- Endpoints GET para listagem completa
- Retorno em formato JSON

### ✅ F3 - CRUD completo
- **Create**: POST endpoints
- **Read**: GET endpoints (individual e listagem)
- **Update**: PUT endpoints
- **Delete**: DELETE endpoints

### ✅ F4 - Contagem de entidades
- Endpoint `/count` para cada entidade
- Contagem em tempo real do banco

### ✅ F5 - Paginação
- Parâmetros `page` e `limit` em todos os endpoints de listagem
- Resposta inclui metadados de paginação

### ✅ F6 - Filtros por atributos
- Endpoint `/search` com múltiplos filtros
- Busca por texto parcial
- Filtros por data/ano

### ✅ F7 - Migrações com Alembic
- Configuração completa do Alembic
- Comando para gerar migrações
- Controle de versões do esquema

### ✅ F8 - Sistema de Logs
- Logs estruturados para todas as operações
- Arquivos de log organizados por data
- Monitoramento de performance

## 🏗️ Arquitetura do Sistema

### Entidades e Relacionamentos

1. **Autor** (5 atributos + relacionamentos)
2. **Categoria** (5 atributos + relacionamentos)  
3. **Usuario** (6 atributos + relacionamentos)
4. **Livro** (8 atributos + relacionamentos)
5. **Emprestimo** (6 atributos + relacionamentos)
6. **PerfilUsuario** (5 atributos + relacionamento 1:1)

### Tipos de Relacionamento

- **1:1** - Usuario ↔ PerfilUsuario
- **1:N** - Usuario → Emprestimo, Livro → Emprestimo
- **N:N** - Livro ↔ Autor, Livro ↔ Categoria

### Estrutura do Projeto

```
biblioteca/
├── config/
│   ├── database.py          # Configuração do banco
│   └── logging_config.py    # Configuração de logs
├── models/
│   └── models.py           # Modelos SQLModel
├── schemas/
│   └── schemas.py          # Schemas Pydantic
├── services/
│   ├── autor_service.py    # Lógica de negócio - Autor
│   └── livro_service.py    # Lógica de negócio - Livro
├── routes/
│   ├── autor_routes.py     # Endpoints - Autor
│   └── livro_routes.py     # Endpoints - Livro
├── alembic/               # Migrações
├── logs/                  # Arquivos de log
├── main.py               # Aplicação principal
├── requirements.txt      # Dependências
└── .env                 # Variáveis de ambiente
```

## 🚀 Como Executar

### 1. Instalação das Dependências

```bash
pip install -r requirements.txt
```

### 2. Configuração do Banco

Edite o arquivo `.env` com suas credenciais:

```env
# Para PostgreSQL
DATABASE_URL=postgresql://usuario:senha@localhost:5432/biblioteca_db

# Para SQLite (desenvolvimento)
DATABASE_URL=sqlite:///./biblioteca.db
```

### 3. Inicializar Migrações

```bash
alembic init alembic
alembic revision --autogenerate -m "Criação inicial das tabelas"
alembic upgrade head
```

### 4. Executar a Aplicação

```bash
python main.py
```

A API estará disponível em: http://localhost:8000

## 📚 Documentação da API

### Swagger UI
Acesse: http://localhost:8000/docs

### Endpoints Principais

#### Autores
- `POST /autores/` - Criar autor
- `GET /autores/` - Listar autores (com paginação)
- `GET /autores/{id}` - Buscar autor por ID
- `PUT /autores/{id}` - Atualizar autor
- `DELETE /autores/{id}` - Excluir autor
- `GET /autores/count` - Contar autores
- `GET /autores/search` - Buscar autores

#### Livros
- `POST /livros/` - Criar livro
- `GET /livros/` - Listar livros (com paginação)
- `GET /livros/{id}` - Buscar livro por ID
- `PUT /livros/{id}` - Atualizar livro
- `DELETE /livros/{id}` - Excluir livro
- `GET /livros/count` - Contar livros
- `GET /livros/search` - Buscar livros

#### Categorias
- `POST /categorias/` - Criar categoria
- `GET /categorias/` - Listar categorias
- `GET /categorias/{id}` - Buscar categoria por ID
- `PUT /categorias/{id}` - Atualizar categoria
- `DELETE /categorias/{id}` - Excluir categoria
- `GET /categorias/count` - Contar categorias

#### Usuários
- `POST /usuarios/` - Criar usuário
- `GET /usuarios/` - Listar usuários
- `GET /usuarios/{id}` - Buscar usuário por ID
- `PUT /usuarios/{id}` - Atualizar usuário
- `DELETE /usuarios/{id}` - Excluir usuário
- `GET /usuarios/count` - Contar usuários

#### Perfil de Usuário
- `POST /perfis/` - Criar perfil
- `GET /perfis/` - Listar perfis
- `GET /perfis/{id}` - Buscar perfil por ID
- `PUT /perfis/{id}` - Atualizar perfil
- `DELETE /perfis/{id}` - Excluir perfil

#### Empréstimos
- `POST /emprestimos/` - Criar empréstimo
- `GET /emprestimos/` - Listar empréstimos
- `GET /emprestimos/{id}` - Buscar empréstimo por ID
- `PUT /emprestimos/{id}` - Atualizar empréstimo
- `DELETE /emprestimos/{id}` - Excluir empréstimo
- `GET /emprestimos/count` - Contar empréstimos

## 🔍 Consultas Implementadas

### Consultas por ID
```bash
GET /autores/1
GET /livros/1
```

### Listagens com Paginação
```bash
GET /autores?page=1&limit=10
GET /livros?page=2&limit=5
```

### Buscas por Texto Parcial
```bash
GET /autores/search?nome=José
GET /livros/search?titulo=Python
```

### Filtros por Data/Ano
```bash
GET /livros/search?ano_min=2020&ano_max=2023
```

### Contagens
```bash
GET /autores/count
GET /livros/count
```

### Filtros por Relacionamentos
```bash
GET /livros/search?autor=Machado
GET /livros/search?categoria=Romance
```

## 📊 Sistema de Logs

Os logs são salvos em `logs/biblioteca_YYYYMMDD.log` e incluem:

- Operações CRUD (criação, leitura, atualização, exclusão)
- Contagens e buscas
- Erros e exceções
- Timestamps detalhados

Exemplo de log:
```
2024-06-06 10:30:15 - biblioteca - INFO - Autor criado com sucesso: ID 1
2024-06-06 10:30:20 - biblioteca - INFO - Listagem de livros: 5 encontrados
```

## 🛠️ Tecnologias Utilizadas

- **FastAPI** - Framework web moderno e rápido
- **SQLModel** - ORM baseado em SQLAlchemy e Pydantic
- **Pydantic** - Validação de dados
- **Alembic** - Migrações de banco de dados
- **PostgreSQL/SQLite** - Banco de dados
- **Uvicorn** - Servidor ASGI

## 🎯 Boas Práticas Implementadas

- Separação de responsabilidades (Models, Services, Routes)
- Validação de entrada com Pydantic
- Tratamento de erros padronizado
- Logs estruturados
- Paginação eficiente
- Relacionamentos bem definidos
- Configurações externalizadas
- Documentação automática

## 📝 Exemplos de Uso

### Criar um Autor
```bash
curl -X POST "http://localhost:8000/autores/" \
-H "Content-Type: application/json" \
-d '{
  "nome": "Machado",
  "sobrenome": "de Assis",
  "data_nascimento": "1839-06-21",
  "nacionalidade": "Brasileiro",
  "biografia": "Escritor brasileiro"
}'
```

### Criar um Livro
```bash
curl -X POST "http://localhost:8000/livros/" \
-H "Content-Type: application/json" \
-d '{
  "titulo": "Dom Casmurro",
  "isbn": "978-85-359-0277-5",
  "ano_publicacao": 1899,
  "editora": "Ática",
  "numero_paginas": 208,
  "quantidade_total": 5,
  "autor_ids": [1],
  "categoria_ids": [1]
}'
```

### Criar uma Categoria
```bash
curl -X POST "http://localhost:8000/categorias/" \
-H "Content-Type: application/json" \
-d '{
  "nome": "Romance",
  "descricao": "Narrativas ficcionais com foco nas relações amorosas",
  "codigo": "ROM01",
  "data_criacao": "2024-01-01",
  "ativo": true
}'
```

### Criar um Usuário
```bash
curl -X POST "http://localhost:8000/usuarios/" \
-H "Content-Type: application/json" \
-d '{
  "nome": "Maria",
  "email": "maria@example.com",
  "senha": "senha123",
  "cpf": "123.456.789-00",
  "telefone": "(85) 99999-0000",
  "data_cadastro": "2024-06-01"
}'
```

### Criar um Perfil de Usuário
```bash
curl -X POST "http://localhost:8000/perfis/" \
-H "Content-Type: application/json" \
-d '{
  "usuario_id": 1,
  "endereco": "Rua das Flores, 123",
  "cidade": "Fortaleza",
  "estado": "CE",
  "cep": "60000-000"
}'
```

### Criar um Empréstimo
```bash
curl -X POST "http://localhost:8000/emprestimos/" \
-H "Content-Type: application/json" \
-d '{
  "usuario_id": 1,
  "livro_id": 1,
  "data_emprestimo": "2024-06-01",
  "data_devolucao": "2024-06-10",
  "status": "ativo",
  "observacoes": "Devolução prevista para 10 dias"
}'
```

Este sistema implementa completamente todos os requisitos do Trabalho Prático 2, demonstrando conceitos avançados de ORM, API REST e boas práticas de desenvolvimento Python.
