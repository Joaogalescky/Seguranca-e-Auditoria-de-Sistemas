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

def validar_mensagem(mensagem_recebida, chave_secreta, nonces_usados=set(), janela_tempo=60):
    """
    Valida a autenticidade e integridade da mensagem recebida.

    Parâmetros:
    - mensagem_recebida (dict): Mensagem com dados, timestamp, nonce e HMAC.
    - chave_secreta (str): Chave secreta usada na geração do HMAC.
    - nonces_usados (set): Conjunto de nonces já usados para prevenir replay.
    - janela_tempo (int): Tempo máximo (em segundos) para aceitar a mensagem.

    Retorna:
    - bool: True se for válida e autêntica, False caso contrário.
    """
    hmac_recebido = mensagem_recebida.get("hmac")
    nonce = mensagem_recebida.get("nonce")
    timestamp = mensagem_recebida.get("timestamp")

    if nonce in nonces_usados:
        print("Nonce já utilizado.")
        return False

    tempo_atual = int(time.time())
    if abs(tempo_atual - timestamp) > janela_tempo:
        print("Mensagem fora da janela de tempo.")
        return False

    mensagem_para_verificar = {
        "dados": mensagem_recebida.get("dados"),
        "timestamp": timestamp,
        "nonce": nonce
    }

    mensagem_serializada = json.dumps(
        mensagem_para_verificar, sort_keys=True).encode()
    hmac_calculado = hmac.new(chave_secreta.encode(
    ), mensagem_serializada, hashlib.sha256).hexdigest()

    if hmac.compare_digest(hmac_calculado, hmac_recebido):
        nonces_usados.add(nonce)
        return True
    else:
        print("HMAC inválido.")
        return False

# Inicialização
if __name__ == "__main__":
    chave = "segredo_super_secreto_123"
    dados_estacao = {
        "temperatura": 22.5,
        "umidade": 60,
        "pressao": 1012
    }

    mensagem = gerar_mensagem_autenticada(dados_estacao, chave)
    print("Mensagem enviada:", mensagem)

    nonces_usados = set()
    valido = validar_mensagem(mensagem, chave, nonces_usados)
    print("Mensagem válida?", valido)
