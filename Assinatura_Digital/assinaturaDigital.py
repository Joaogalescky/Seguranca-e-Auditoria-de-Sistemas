import hmac, hashlib, time, uuid, json, secrets, os
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import serialization, hashes
from cryptography.hazmat.primitives.asymmetric import rsa
from cryptography.hazmat.primitives.asymmetric import padding as asypadding
import tkinter as tk
from tkinter import filedialog, messagebox

# Hash
def gerar_mensagem_autenticada(dados, chave_secreta):
    timestamp = int(
        time.time())  # Gerar um 'carimbo de data/hora' (validade temporal)
    nonce = str(uuid.uuid4())  # nonce = id único aleatório

    mensagem = {
        "dados": dados,
        "timestamp": timestamp,
        "nonce": nonce
    }

    # Serializar a mensagem para string Json ordenada
    mensagem_serializada = json.dumps(mensagem, sort_keys=True).encode()
    assinatura = hmac.new(chave_secreta.encode(),
                          # Gera o HMAC da mensagem com SHA-256, retornando como string hexadecimal
                          mensagem_serializada, hashlib.sha256).hexdigest()
    mensagem["hmac"] = assinatura  # Add assinatura HMAC
    return mensagem

# Geração de par de chaves
def gerar_chaves_rsa(bits: int = 4096):
    chave_privada = rsa.generate_private_key(public_exponent=65537, key_size=bits, backend=default_backend(), )
    chave_publica = chave_privada.public_key()

    return chave_privada, chave_publica

# Processo de assinatura
def assinatura():

    mensagem = b'Ana, compre 100 acoes da PETR4. Ass. Pedro'

    # [...]


# Inicialização
if __name__ == "__main__":
    chave = "S3gur4nca!"
    dados = {
        "Emissor": "Pedro",
        "Remetente": "Ana",
        "Titulo das Ações": "PETR4",
        "Quantidade": 100
    }

    mensagem = gerar_mensagem_autenticada(dados, chave)
    print("Mensagem enviada:", mensagem)