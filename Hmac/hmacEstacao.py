import hmac
import hashlib
import time
import uuid
import json

# Variável
ESTACAO = True

# Funções
def gerar_mensagem_autenticada(dados, chave_secreta):
    """
    Gera uma mensagem autenticada com HMAC com SHA-256.

    Parâmetros:
    - dados (dict): Dados da estação meteorológica.
    - chave_secreta (str): Chave secreta compartilhada.

    Retorna:
    - dict: Mensagem contendo os dados, timestamp, nonce e HMAC.
    """
    timestamp = int(time.time())
    nonce = str(uuid.uuid4())

    mensagem = {
        "dados": dados,
        "timestamp": timestamp,
        "nonce": nonce
    }

    mensagem_serializada = json.dumps(mensagem, sort_keys=True).encode()
    assinatura = hmac.new(chave_secreta.encode(), mensagem_serializada, hashlib.sha256).hexdigest()
    mensagem["hmac"] = assinatura

    return mensagem