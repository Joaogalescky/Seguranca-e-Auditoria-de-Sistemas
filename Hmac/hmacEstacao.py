import hmac  # Código de autenticação em chave
import hashlib  # Biblioteca Hash
import time  # Timestamp
import uuid  # Identificadores únicos universais
import json  # Dicionário em String

# Variável
ESTACAO = True


# Funções
def gerar_mensagem_autenticada(dados, chave_secreta):
    """
    Gerar uma mensagem autenticada com HMAC, usando SHA-256.

    Parâmetros:
    - dados (dicionário/dict): dados da estação meteorológica.
    - chave_secreta (str): chave secreta compartilhada.

    Retorna:
    - Mensagem contendo os dados, timestamp, nonce e HMAC.
    """
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


def validar_mensagem(mensagem_recebida, chave_secreta, nonces_usados=set(), janela_tempo=60):
    """
    Validar a autenticidade e integridade da mensagem recebida.

    Parâmetros:
    - mensagem_recebida (dict): mensagem com dados, timestamp, nonce e HMAC.
    - chave_secreta (str): chave secreta usada na geração do HMAC.
    - nonces_usados (set): conjunto de nonces já usados para prevenir replay.
    - janela_tempo (int): tempo máximo (em segundos) para aceitar a mensagem.

    Retorna:
    - bool: True se for válida e autêntica ou False caso não.
    """
    # Extrair valores
    hmac_recebido = mensagem_recebida.get("hmac")
    nonce = mensagem_recebida.get("nonce")
    timestamp = mensagem_recebida.get("timestamp")

    # Se nonce foi usado
    if nonce in nonces_usados:
        print("[ERRO]! Nonce já utilizado!")
        return False

    # Se o tempo está dentro do intervalo
    tempo_atual = int(time.time())
    if abs(tempo_atual - timestamp) > janela_tempo:
        print("[ERRO]! Mensagem fora da janela de tempo!")
        return False

    # Retirar o HMAC da mensagem para verificar se são os mesmos dados
    mensagem_para_verificar = {
        "dados": mensagem_recebida.get("dados"),
        "timestamp": timestamp,
        "nonce": nonce
    }

    # Serializar como na geração do HMAC
    mensagem_serializada = json.dumps(
        mensagem_para_verificar, sort_keys=True).encode()
    hmac_calculado = hmac.new(chave_secreta.encode(
        # Calcula com os dados recebidos
    ), mensagem_serializada, hashlib.sha256).hexdigest()

    # Compara se são iguais
    # compare_digest = contra timing attacks
    if hmac.compare_digest(hmac_calculado, hmac_recebido):
        nonces_usados.add(nonce)
        return True
    else:
        print("[ERRO]! HMAC inválido!")
        return False


# Inicialização
if __name__ == "__main__":
    chave = "S3gur4nca!"
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

    # === Teste de Ataques ===
    print("\n------- Teste de Ataques -------")

    mensagem_original = gerar_mensagem_autenticada(dados_estacao, chave)
    nonces_usados = set()
    print("Mensagem original válida?", validar_mensagem(
        mensagem_original, chave, nonces_usados))

    # Replay
    print("\nAtaque de replay!")
    print("Mensagem replay válida?", validar_mensagem(
        mensagem_original, chave, nonces_usados))

    # Modificado
    print("\nAtaque de modificação de dados!")
    mensagem_modificada = mensagem_original.copy()
    mensagem_modificada["dados"]["temperatura"] = 99.9
    print("Mensagem modificada válida?", validar_mensagem(
        mensagem_modificada, chave, nonces_usados))

    # Expirado
    print("\nAtaque de mensagem expirada!")
    mensagem_expirada = gerar_mensagem_autenticada(dados_estacao, chave)
    mensagem_expirada["timestamp"] -= 9999
    print("Mensagem expirada válida?", validar_mensagem(
        mensagem_expirada, chave, nonces_usados))

    # Sem chave
    print("\nAtaque de geração de mensagem sem chave válida!")
    chave_falsa = "Segurança"
    mensagem_falsa = gerar_mensagem_autenticada(dados_estacao, chave_falsa)
    print("Mensagem com chave falsa válida?",
          validar_mensagem(mensagem_falsa, chave, nonces_usados))
