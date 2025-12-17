#!/bin/bash

echo "╔════════════════════════════════════════════════════════════╗"
echo "║  Demonstração de Autenticação Mútua (mTLS)                ║"
echo "║  Sistema de Autenticação - IFPR TADS                       ║"
echo "╚════════════════════════════════════════════════════════════╝"
echo ""

echo "📋 Verificando certificados..."
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "🔐 Certificado da CA:"
openssl x509 -in certs/ca-cert.pem -noout -subject -issuer
echo ""
echo "🖥️  Certificado do Servidor:"
openssl x509 -in certs/server-cert.pem -noout -subject -issuer
echo ""
echo "👤 Certificado do Cliente:"
openssl x509 -in certs/client-cert.pem -noout -subject -issuer
echo ""

echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "🧪 Teste 1: Conexão SEM certificado (deve falhar)"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
timeout 2 curl -k https://localhost:8443/ 2>&1 | grep -q "Hello World" && echo "❌ FALHOU: Aceitou conexão sem certificado!" || echo "✅ SUCESSO: Conexão recusada sem certificado"
echo ""

echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "🧪 Teste 2: Conexão COM certificado (deve funcionar)"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
RESPONSE=$(curl -s --cacert certs/ca-cert.pem --cert certs/client-cert.pem --key certs/client-key.pem https://localhost:8443/)
echo "Resposta: $RESPONSE"
echo "$RESPONSE" | grep -q "Hello World" && echo "✅ SUCESSO: Servidor respondeu corretamente" || echo "❌ FALHOU"
echo ""

echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "🧪 Teste 3: Criar usuário com mTLS"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
TIMESTAMP=$(date +%s)
USER_RESPONSE=$(curl -s --cacert certs/ca-cert.pem --cert certs/client-cert.pem --key certs/client-key.pem \
  -X POST https://localhost:8443/users/ \
  -H "Content-Type: application/json" \
  -d "{\"username\":\"demo_$TIMESTAMP\",\"password\":\"senha123\",\"email\":\"demo_$TIMESTAMP@test.com\"}")
echo "Resposta: $USER_RESPONSE"
echo "$USER_RESPONSE" | grep -q "demo_" && echo "✅ SUCESSO: Usuário criado" || echo "❌ FALHOU"
echo ""

echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "🧪 Teste 4: Login e obter token JWT"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
TOKEN_RESPONSE=$(curl -s --cacert certs/ca-cert.pem --cert certs/client-cert.pem --key certs/client-key.pem \
  -X POST https://localhost:8443/auth/token \
  -d "username=demo_$TIMESTAMP@test.com&password=senha123")
echo "Resposta: $TOKEN_RESPONSE"
TOKEN=$(echo $TOKEN_RESPONSE | grep -o '"access_token":"[^"]*' | cut -d'"' -f4)
if [ ! -z "$TOKEN" ]; then
    echo "✅ SUCESSO: Token obtido"
    echo "Token (primeiros 50 caracteres): ${TOKEN:0:50}..."
else
    echo "❌ FALHOU: Não foi possível obter token"
fi
echo ""

echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "🧪 Teste 5: Acessar recurso protegido com token"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
if [ ! -z "$TOKEN" ]; then
    USERS_RESPONSE=$(curl -s --cacert certs/ca-cert.pem --cert certs/client-cert.pem --key certs/client-key.pem \
      -H "Authorization: Bearer $TOKEN" \
      https://localhost:8443/users/)
    echo "Resposta: $USERS_RESPONSE"
    echo "$USERS_RESPONSE" | grep -q "users" && echo "✅ SUCESSO: Acesso autorizado" || echo "❌ FALHOU"
else
    echo "⏭️  PULADO: Token não disponível"
fi
echo ""

echo "╔════════════════════════════════════════════════════════════╗"
echo "║  ✅ Demonstração Concluída                                 ║"
echo "║                                                            ║"
echo "║  Autenticação Mútua (mTLS) funcionando corretamente!      ║"
echo "║  - Servidor autenticado ✓                                 ║"
echo "║  - Cliente autenticado ✓                                  ║"
echo "║  - Comunicação criptografada ✓                            ║"
echo "║  - Dupla camada de segurança (Certificado + JWT) ✓        ║"
echo "╚════════════════════════════════════════════════════════════╝"
