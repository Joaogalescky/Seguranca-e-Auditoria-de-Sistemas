#!/bin/bash

echo "=== Teste 1: Verificar certificados ==="
echo "Verificando certificado do servidor:"
openssl x509 -in certs/server-cert.pem -noout -subject -issuer

echo -e "\nVerificando certificado do cliente:"
openssl x509 -in certs/client-cert.pem -noout -subject -issuer

echo -e "\nVerificando certificado da CA:"
openssl x509 -in certs/ca-cert.pem -noout -subject -issuer

echo -e "\n=== Teste 2: Conexão SEM certificado do cliente ==="
curl -k https://localhost:8443/ 2>&1 | head -5

echo -e "\n=== Teste 3: Conexão COM certificado do cliente ==="
curl --cacert certs/ca-cert.pem \
     --cert certs/client-cert.pem \
     --key certs/client-key.pem \
     https://localhost:8443/

echo -e "\n=== Teste 4: Verificar informações do certificado ==="
curl --cacert certs/ca-cert.pem \
     --cert certs/client-cert.pem \
     --key certs/client-key.pem \
     https://localhost:8443/cert-info

echo -e "\n=== Teste 5: Criar usuário com mTLS ==="
curl --cacert certs/ca-cert.pem \
     --cert certs/client-cert.pem \
     --key certs/client-key.pem \
     -X POST https://localhost:8443/users/ \
     -H "Content-Type: application/json" \
     -d '{"username":"mtls_user","password":"senha123","email":"mtls@test.com"}'

echo -e "\n\n=== Testes concluídos ==="
