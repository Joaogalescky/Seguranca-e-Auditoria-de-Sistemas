# Sistema de Certificados Digitais
Este projeto implementa um sistema de certificados digitais com uma Autoridade Certificadora (CA) raiz e emissão de certificados pessoais. O sistema demonstra o uso de criptografia assimétrica (RSA) para cifrar e decifrar mensagens usando certificados X.509.

## Arquitetura
![Diagrama da Arquitetura](../Certificado_Digital/assets/diagrama_de_sequencia.svg)

## Requisitos
- Python 3.13+
- Poetry (gerenciador de dependências)
- Bibliotecas (instaladas automaticamente pelo Poetry):
  - cryptography
  - pytest
  - pytest-cov
  - ruff

## Instalação
1. Clone o repositório:
```bash
git clone https://github.com/Joaogalescky/Seguranca-e-Auditoria-de-Sistemas.git
cd Certificado_Digital
```

2. Instale as dependências usando Poetry:
```bash
poetry install
```

3. Ative o ambiente virtual:
```bash
poetry shell
```

## Como Usar

### 1. Gerar Certificado Raiz (CA)
Primeiro, gere o certificado raiz da CA:
```bash
task raiz
```
Isso irá gerar:
- `private_key_raiz_ifpr.pem`: Chave privada da CA
- `certificado_raiz_ifpr.pem`: Certificado público da CA

### 2. Gerar Certificado Pessoal
Em seguida, gere um certificado pessoal assinado pela CA:
```bash
task pessoal
```
Isso irá gerar:
- `private_key_joaogalescky.pem`: Sua chave privada
- `certificado_joaogalescky.pem`: Seu certificado público

### 3. Enviar Mensagem Cifrada (Cliente)
Para cifrar uma mensagem usando o certificado:
```bash
task cliente
```
Isso irá gerar:
- `mensagem_cifrada.txt`: Mensagem cifrada em base64

### 4. Decifrar Mensagem (Servidor)
Para decifrar a mensagem usando a chave privada:
```bash
task servidor
```
Isso irá gerar:
- `mensagem_decifrada.txt`: Mensagem original decifrada

## Testes

Execute os testes automatizados:
```bash
task test
```

## Cenários de Teste

O sistema inclui tratamento de vários cenários de erro que podem ser testados:

### Cliente
1. **Certificado não encontrado**: 
   - Renomeie ou apague `certificado_joaogalescky.pem`

2. **Certificado inválido/corrompido**: 
   - Modifique o conteúdo do arquivo `certificado_joaogalescky.pem`

3. **Certificado expirado**: 
   - O sistema verifica automaticamente a data de validade

4. **Erro na cifragem**: 
   - Tente cifrar uma mensagem muito grande
   
5. **Erro ao salvar arquivo**: 
   - Remova permissões de escrita do diretório

### Servidor
1. **Chave privada não encontrada**: 
   - Renomeie ou apague `private_key_joaogalescky.pem`

2. **Chave privada inválida**: 
   - Modifique o conteúdo do arquivo `private_key_joaogalescky.pem`

3. **Mensagem cifrada corrompida**: 
   - Modifique o conteúdo do arquivo `mensagem_cifrada.txt`

4. **Erro na decifragem**: 
   - Use uma chave privada diferente para tentar decifrar

## Estrutura do Projeto
```
Certificado_Digital/
├── src/
│   ├── certificado_pessoal.py    # Geração de certificado pessoal
│   ├── certificado_raiz.py       # Geração de certificado raiz (CA)
│   ├── cliente.py               # Cifra mensagens
│   └── servidor.py              # Decifra mensagens
├── tests/
│   └── test_certificado_digital.py
├── pyproject.toml               # Configurações do projeto
└── README.md                    # Este arquivo
```

### 1. Gerar o Certificado Raiz (CA)
cd src/Certificado_Raiz  
python certificado_raiz.py

---

### 2. Gerar o Certificado Breno & João
cd ../Certificado  
python CertificadoBrenoJoao.py

---

### 3. Executar o Cliente (Gerar Mensagem Cifrada)
cd ../Cliente  
python ClienteHello.py

---

### 4. Executar o Servidor (Decifrar Mensagem)
cd ../Servidor  
python ServidorDecifrar.py

---

### 5. Verificar a Mensagem Decifrada
cat mensagemDesafioDecifrado.txt

## Considerações de Segurança
- As chaves privadas não devem ser compartilhadas
- Mantenha os arquivos .pem seguros
- Em produção, use proteção por senha nas chaves privadas
- Implemente uma política de renovação de certificados
- Considere usar uma infraestrutura de PKI completa em produção

## Autores
- [João Vitor Campõe Galescky](https://github.com/Joaogalescky) 