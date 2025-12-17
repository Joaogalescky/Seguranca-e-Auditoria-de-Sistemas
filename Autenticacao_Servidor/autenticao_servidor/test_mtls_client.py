#!/usr/bin/env python3
"""Cliente Python para testar autenticação mTLS"""

import requests
from pathlib import Path

BASE_DIR = Path(__file__).parent
CERTS_DIR = BASE_DIR / 'certs'

def test_without_cert():
    """Teste sem certificado - deve falhar"""
    print("=== Teste 1: Conexão SEM certificado ===")
    try:
        response = requests.get('https://localhost:8443/', verify=False)
        print(f"Status: {response.status_code}")
        print(f"Response: {response.text}")
    except Exception as e:
        print(f"Erro esperado: {e}")

def test_with_cert():
    """Teste com certificado - deve funcionar"""
    print("\n=== Teste 2: Conexão COM certificado ===")
    try:
        response = requests.get(
            'https://localhost:8443/',
            cert=(str(CERTS_DIR / 'client-cert.pem'), str(CERTS_DIR / 'client-key.pem')),
            verify=str(CERTS_DIR / 'ca-cert.pem')
        )
        print(f"Status: {response.status_code}")
        print(f"Response: {response.json()}")
    except Exception as e:
        print(f"Erro: {e}")

def test_cert_info():
    """Verificar informações do certificado"""
    print("\n=== Teste 3: Informações do certificado ===")
    try:
        response = requests.get(
            'https://localhost:8443/cert-info',
            cert=(str(CERTS_DIR / 'client-cert.pem'), str(CERTS_DIR / 'client-key.pem')),
            verify=str(CERTS_DIR / 'ca-cert.pem')
        )
        print(f"Status: {response.status_code}")
        print(f"Response: {response.json()}")
    except Exception as e:
        print(f"Erro: {e}")

def test_create_user():
    """Criar usuário com mTLS"""
    print("\n=== Teste 4: Criar usuário com mTLS ===")
    try:
        response = requests.post(
            'https://localhost:8443/users/',
            cert=(str(CERTS_DIR / 'client-cert.pem'), str(CERTS_DIR / 'client-key.pem')),
            verify=str(CERTS_DIR / 'ca-cert.pem'),
            json={
                'username': 'mtls_python_user',
                'password': 'senha123',
                'email': 'mtls_python@test.com'
            }
        )
        print(f"Status: {response.status_code}")
        print(f"Response: {response.json()}")
    except Exception as e:
        print(f"Erro: {e}")

def test_login():
    """Login com mTLS"""
    print("\n=== Teste 5: Login com mTLS ===")
    try:
        response = requests.post(
            'https://localhost:8443/auth/token',
            cert=(str(CERTS_DIR / 'client-cert.pem'), str(CERTS_DIR / 'client-key.pem')),
            verify=str(CERTS_DIR / 'ca-cert.pem'),
            data={
                'username': 'mtls_python@test.com',
                'password': 'senha123'
            }
        )
        print(f"Status: {response.status_code}")
        print(f"Response: {response.json()}")
        
        if response.status_code == 200:
            token = response.json()['access_token']
            print(f"\nToken obtido: {token[:50]}...")
            
            # Testar acesso com token
            print("\n=== Teste 6: Acessar recurso protegido ===")
            response = requests.get(
                'https://localhost:8443/users/',
                cert=(str(CERTS_DIR / 'client-cert.pem'), str(CERTS_DIR / 'client-key.pem')),
                verify=str(CERTS_DIR / 'ca-cert.pem'),
                headers={'Authorization': f'Bearer {token}'}
            )
            print(f"Status: {response.status_code}")
            print(f"Response: {response.json()}")
    except Exception as e:
        print(f"Erro: {e}")

if __name__ == '__main__':
    print("Testando autenticação mTLS\n")
    test_without_cert()
    test_with_cert()
    test_cert_info()
    test_create_user()
    test_login()
    print("\n=== Testes concluídos ===")
