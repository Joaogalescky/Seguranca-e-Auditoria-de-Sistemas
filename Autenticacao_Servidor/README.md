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

### Autenticação Básica (JWT)

- **Hash de Senhas**: Argon2 (algoritmo recomendado pela OWASP)
- **Tokens JWT**: Assinados com HS256
- **Validação de Dados**: Pydantic schemas com validação de email
- **Controle de Acesso**: Usuários só podem modificar seus próprios dados
- **Expiração de Tokens**: Tokens com tempo de vida limitado

### Autenticação Mútua (mTLS)

O sistema implementa autenticação mútua através de certificados SSL/TLS, onde tanto o servidor quanto o cliente se autenticam mutuamente antes de estabelecer a comunicação.

#### Arquitetura de Segurança mTLS

```
┌─────────────┐                                    ┌─────────────┐
│   Cliente   │                                    │  Servidor   │
│             │                                    │             │
│ ┌─────────┐ │                                    │ ┌─────────┐ │
│ │ Cert    │ │  1. ClientHello + Certificado     │ │ Cert    │ │
│ │ Cliente │ ├───────────────────────────────────>│ │ Servidor│ │
│ └─────────┘ │                                    │ └─────────┘ │
│             │  2. ServerHello + Certificado      │             │
│             │<───────────────────────────────────┤             │
│             │                                    │             │
│             │  3. Validação Mútua (CA)           │             │
│             │<──────────────────────────────────>│             │
│             │                                    │             │
│             │  4. Handshake TLS Completo         │             │
│             │<══════════════════════════════════>│             │
│             │                                    │             │
│             │  5. Requisição Criptografada       │             │
│             │  (Certificado + JWT)               │             │
│             ├───────────────────────────────────>│             │
│             │                                    │ ┌─────────┐ │
│             │  6. Resposta Criptografada         │ │Middleware│ │
│             │<───────────────────────────────────┤ │  mTLS   │ │
│             │                                    │ └─────────┘ │
└─────────────┘                                    └─────────────┘
```

#### Estrutura de Certificados

```
certs/
├── ca-cert.pem          # Certificado da Autoridade Certificadora
├── ca-key.pem           # Chave privada da CA
├── server-cert.pem      # Certificado do servidor (CN=localhost)
├── server-key.pem       # Chave privada do servidor
├── client-cert.pem      # Certificado do cliente (CN=client)
└── client-key.pem       # Chave privada do cliente
```

#### Hierarquia de Confiança

```
┌──────────────────────────────────┐
│  CA (IFPR-CA)                    │
│  Autoridade Certificadora        │
└────────────┬─────────────────────┘
             │
      ┌──────┴──────┐
      │             │
      ▼             ▼
┌──────────┐  ┌──────────┐
│ Servidor │  │ Cliente  │
│ (signed) │  │ (signed) │
└──────────┘  └──────────┘
```

#### Camadas de Segurança

| Camada | Tecnologia | Proteção |
|--------|-----------|----------|
| 1 | TLS 1.2+ | Criptografia de transporte |
| 2 | Certificado Servidor | Autenticação do servidor |
| 3 | Certificado Cliente | Autenticação do cliente |
| 4 | JWT Token | Autorização de usuário |
| 5 | Hash Argon2 | Proteção de senhas |

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

### Testes de Autenticação Básica (JWT)

Para testar a API, utilize a documentação interativa em `/docs` ou ferramentas como cURL, Postman, HTTPie ou Insomnia.

#### Exemplo de uso com cURL

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

### Testes de Autenticação Mútua (mTLS)

#### Iniciar Servidor mTLS

```bash
cd autenticao_servidor
python run_mtls.py
```

O servidor estará disponível em `https://localhost:8443`

#### Testes com cURL

```bash
# Teste 1: Conexão básica com certificado
curl --cacert certs/ca-cert.pem \
     --cert certs/client-cert.pem \
     --key certs/client-key.pem \
     https://localhost:8443/
```

**Resultado esperado:**
```json
{"message":"Hello World"}
```

```bash
# Teste 2: Criar usuário com mTLS
curl --cacert certs/ca-cert.pem \
     --cert certs/client-cert.pem \
     --key certs/client-key.pem \
     -X POST https://localhost:8443/users/ \
     -H "Content-Type: application/json" \
     -d '{"username":"usuario_mtls","password":"senha123","email":"usuario@mtls.com"}'
```

**Resultado esperado:**
```json
{"id":1,"username":"usuario_mtls","email":"usuario@mtls.com"}
```

```bash
# Teste 3: Login com mTLS
curl --cacert certs/ca-cert.pem \
     --cert certs/client-cert.pem \
     --key certs/client-key.pem \
     -X POST https://localhost:8443/auth/token \
     -d "username=usuario@mtls.com&password=senha123"
```

**Resultado esperado:**
```json
{
  "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "refresh_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "token_type": "bearer"
}
```

```bash
# Teste 4: Acessar recurso protegido com mTLS + JWT
TOKEN="seu-token-aqui"
curl --cacert certs/ca-cert.pem \
     --cert certs/client-cert.pem \
     --key certs/client-key.pem \
     -H "Authorization: Bearer $TOKEN" \
     https://localhost:8443/users/
```

**Resultado esperado:**
```json
{"users":[{"id":1,"username":"usuario_mtls","email":"usuario@mtls.com"}]}
```

```bash
# Teste 5: Conexão SEM certificado (deve falhar)
curl -k https://localhost:8443/
```

**Resultado esperado:** Conexão recusada (SSL handshake falhou)

#### Demonstração Automatizada

Execute o script de demonstração completa:

```bash
bash demo_mtls.sh
```

Este script executa todos os testes de autenticação mútua e exibe os resultados de forma organizada.

#### Validação de Certificados

```bash
# Verificar detalhes do certificado do cliente
openssl x509 -in certs/client-cert.pem -text -noout

# Verificar validade do certificado
openssl x509 -in certs/client-cert.pem -noout -dates

# Verificar Common Name (CN)
openssl x509 -in certs/client-cert.pem -noout -subject

# Testar handshake SSL
openssl s_client -connect localhost:8443 \
  -cert certs/client-cert.pem \
  -key certs/client-key.pem \
  -CAfile certs/ca-cert.pem
```

## Resultados dos Testes mTLS

### Teste 1: Conexão SEM Certificado
- **Status:** Bloqueado
- **Descrição:** O servidor recusa conexões que não apresentam certificado válido do cliente
- **Segurança:** Comprova que o servidor exige autenticação mútua

### Teste 2: Conexão COM Certificado
- **Status:** Sucesso
- **Resposta:** `{"message":"Hello World"}`
- **Descrição:** Servidor aceita e processa requisições com certificado válido

### Teste 3: Criar Usuário com mTLS
- **Status:** Sucesso
- **Descrição:** Usuário criado com sucesso utilizando autenticação mútua
- **Segurança:** Operação protegida por certificado SSL

### Teste 4: Login e Obtenção de Token JWT
- **Status:** Sucesso
- **Descrição:** Token JWT obtido com sucesso após validação de certificado e credenciais
- **Segurança:** Dupla camada de autenticação (certificado + senha)

### Teste 5: Acesso a Recurso Protegido
- **Status:** Sucesso
- **Descrição:** Acesso autorizado utilizando certificado SSL e token JWT
- **Segurança:** Tripla validação (certificado + token + permissões)

## Diferenças: Autenticação Unilateral vs Mútua

### Autenticação Unilateral (JWT apenas)
```
Cliente → [Valida Servidor] → Servidor
Cliente → [Envia Senha] → Servidor
```

### Autenticação Mútua (mTLS + JWT)
```
Cliente ↔ [Validam Mutuamente] ↔ Servidor
Cliente → [Certificado + Senha] → Servidor
```

## Casos de Uso da Autenticação Mútua

1. **APIs Corporativas**: Comunicação segura entre microserviços
2. **Dispositivos IoT**: Autenticação de dispositivos em redes industriais
3. **Sistemas Bancários**: Transações financeiras de alto valor
4. **Saúde Digital**: Proteção de dados sensíveis de pacientes
5. **Sistemas Governamentais**: Comunicação entre órgãos públicos

## Autor

João Vitor Campõe Galescky

## Instituição

Instituto Federal do Paraná (IFPR)  
Curso: Tecnologia em Análise e Desenvolvimento de Sistemas  
Disciplina: Segurança e Auditoria de Sistemas

## Licença

Este projeto foi desenvolvido para fins educacionais.
