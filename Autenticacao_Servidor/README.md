# Sistema de Autenticação de Servidor

Projeto desenvolvido para a disciplina de Segurança e Auditoria de Sistemas do curso de Tecnologia em Análise e Desenvolvimento de Sistemas (TADS) - IFPR.

## Descrição

Sistema de autenticação baseado em tokens JWT (JSON Web Tokens) implementado com FastAPI. O projeto demonstra conceitos fundamentais de segurança em aplicações web, incluindo hash de senhas, autenticação stateless e controle de acesso baseado em tokens.

## Tecnologias Utilizadas

- **FastAPI**: Framework web moderno e de alto desempenho
- **SQLAlchemy**: ORM para manipulação de banco de dados
- **Alembic**: Gerenciamento de migrações de banco de dados
- **PyJWT**: Implementação de JSON Web Tokens
- **Pwdlib**: Biblioteca para hash de senhas com Argon2
- **Pydantic**: Validação de dados e serialização
- **Ruff**: Linter e formatador de código Python
- **Taskipy**: Gerenciador de tarefas para automação

## Arquitetura

O projeto segue uma arquitetura em camadas:

```
src/
├── routers/          # Endpoints da API
│   ├── auth.py       # Rotas de autenticação
│   └── user.py       # Rotas de gerenciamento de usuários
├── database.py       # Configuração do banco de dados
├── models.py         # Modelos de dados (ORM)
├── schemas.py        # Schemas de validação (Pydantic)
├── security.py       # Funções de segurança (JWT, hash)
├── settings.py       # Configurações da aplicação
└── main.py           # Ponto de entrada da aplicação
```

## Requisitos

- Python 3.12 ou superior
- pip ou poetry para gerenciamento de dependências

## Instalação

### 1. Clone o repositório

```bash
git clone <url-do-repositorio>
cd Autenticacao_Servidor/autenticao_servidor
```

### 2. Instale as dependências

```bash
pip install -r requirements.txt
```

Ou com Poetry:

```bash
poetry install
```

### 3. Configure as variáveis de ambiente

Crie um arquivo `.env` na raiz do projeto:

```env
DATABASE_URL=sqlite:///./database.db
SECRET_KEY=sua-chave-secreta-aqui
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30
```

**Importante**: Em produção, utilize uma chave secreta forte e única.

### 4. Execute as migrações do banco de dados

```bash
alembic upgrade head
```

## Execução

### Modo desenvolvimento

```bash
fastapi dev src/main.py
```

Ou utilizando taskipy:

```bash
task run
```

### Modo produção

```bash
fastapi run src/main.py
```

A aplicação estará disponível em `http://localhost:8000`

## Documentação da API

Após iniciar o servidor, acesse:

- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc

## Endpoints Principais

### Autenticação

- `POST /auth/token` - Autenticação de usuário (retorna token JWT)

### Usuários

- `POST /users/` - Criar novo usuário
- `GET /users/` - Listar usuários (requer autenticação)
- `GET /users/{id}` - Buscar usuário por ID
- `PUT /users/{id}` - Atualizar usuário (requer autenticação)
- `PATCH /users/{id}` - Atualizar parcialmente usuário (requer autenticação)
- `DELETE /users/{id}` - Deletar usuário (requer autenticação)

## Fluxo de Autenticação

1. **Registro**: Usuário cria conta via `POST /users/`
2. **Login**: Usuário autentica via `POST /auth/token` fornecendo email e senha
3. **Acesso**: Sistema retorna token JWT válido por 30 minutos
4. **Requisições**: Cliente inclui token no header `Authorization: Bearer <token>`
5. **Validação**: Servidor valida token em cada requisição protegida

## Segurança Implementada

- **Hash de Senhas**: Argon2 (algoritmo recomendado pela OWASP)
- **Tokens JWT**: Assinados com HS256
- **Validação de Dados**: Pydantic schemas com validação de email
- **Controle de Acesso**: Usuários só podem modificar seus próprios dados
- **Expiração de Tokens**: Tokens com tempo de vida limitado

## Comandos de Desenvolvimento

### Formatação de código

```bash
task format
```

### Verificação de código (linting)

```bash
task lint
```

### Correção automática de problemas

```bash
task pre_format
```

## Estrutura do Banco de Dados

### Tabela: usuarios

| Campo      | Tipo     | Descrição                    |
|------------|----------|------------------------------|
| id         | INTEGER  | Chave primária               |
| username   | VARCHAR  | Nome de usuário (único)      |
| password   | VARCHAR  | Senha hasheada               |
| email      | VARCHAR  | Email do usuário (único)     |
| created_at | DATETIME | Data de criação do registro  |

## Migrações

### Criar nova migração

```bash
alembic revision --autogenerate -m "descrição da migração"
```

### Aplicar migrações

```bash
alembic upgrade head
```

### Reverter última migração

```bash
alembic downgrade -1
```

## Testes

Para testar a API, utilize a documentação interativa em `/docs` ou ferramentas como:

- cURL
- Postman
- HTTPie
- Insomnia

### Exemplo de uso com cURL

```bash
# Criar usuário
curl -X POST "http://localhost:8000/users/" \
  -H "Content-Type: application/json" \
  -d '{"username":"joao","password":"senha123","email":"joao@email.com"}'

# Fazer login
curl -X POST "http://localhost:8000/auth/token" \
  -H "Content-Type: application/x-www-form-urlencoded" \
  -d "username=joao@email.com&password=senha123"

# Acessar rota protegida
curl -X GET "http://localhost:8000/users/" \
  -H "Authorization: Bearer <seu-token-aqui>"
```

## Autor

João Vitor Campõe Galescky

## Instituição

Instituto Federal do Paraná (IFPR)  
Curso: Tecnologia em Análise e Desenvolvimento de Sistemas  
Disciplina: Segurança e Auditoria de Sistemas

## Licença

Este projeto foi desenvolvido para fins educacionais.
