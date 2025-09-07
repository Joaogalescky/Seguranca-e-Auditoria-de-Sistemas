import base64
import hashlib
import hmac
import json
import secrets
import time
import uuid

from cryptography.exceptions import InvalidSignature
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import hashes, serialization
from cryptography.hazmat.primitives.asymmetric import padding as asypadding
from cryptography.hazmat.primitives.asymmetric import rsa


# Hash
def gerar_mensagem_autenticada(mensagem, chave):
    timestamp = int(
        time.time()
    )  # Gerar um 'carimbo de data/hora' (validade temporal)
    nonce = str(uuid.uuid4())  # nonce = id único aleatório

    mensagem_autenticada = {
        'dados': mensagem,
        'timestamp': timestamp,
        'nonce': nonce,
    }

    # Serializar a mensagem para string Json ordenada
    mensagem_serializada = json.dumps(
        mensagem_autenticada, sort_keys=True
    ).encode()
    assinatura = hmac.new(
        chave.encode(),
        # Gera o HMAC da mensagem com SHA-256,
        # retornando como string hexadecimal
        mensagem_serializada,
        hashlib.sha256,
    ).hexdigest()
    mensagem_autenticada['hmac'] = assinatura  # Add assinatura HMAC

    print('Mensagem autenticada: ', mensagem_autenticada, '\n')

    return mensagem_autenticada


# Geração de par de chaves
def gerar_chaves_rsa(bits: int = 4096):
    chave_privada = rsa.generate_private_key(
        public_exponent=65537,
        key_size=bits,
        backend=default_backend(),
    )
    chave_publica = chave_privada.public_key()

    return chave_privada, chave_publica


# Processo de assinatura
def assinatura(mensagem, chave_privada):
    # Configuração do esquema de preenchimento (padding)
    # Usando PSS (Probabilistic Signature Scheme) com MGF1 e SHA-256
    padding_config = asypadding.PSS(
        mgf=asypadding.MGF1(hashes.SHA256()),
        salt_length=asypadding.PSS.MAX_LENGTH,
    )

    # Assinatura da mensagem usando a chave privada
    # com a configuração de padding e SHA-256
    assinatura = chave_privada.sign(
        mensagem,
        padding_config,
        hashes.SHA256(),
        # A função hash utilizada
        # para gerar o resumo da mensagem
    )

    # Criação de um dicionário com a mensagem e a assinatura
    mensagem_assinada = {
        'mensagem': base64.b64encode(mensagem).decode(),
        'assinatura': base64.b64encode(assinatura).decode(),
    }

    # Convertida em formato JSON
    msg_json = json.dumps(mensagem_assinada)
    print('Mensagem assinada: ', msg_json)
    print('Assinatura (hex):', assinatura.hex())
    print('Tamanho:', len(assinatura), 'bytes')
    print('Tamanho:', len(assinatura) * 8, 'bits (!)\n')

    return msg_json


# Checar assinatura
def checar_assinatura(msg_json, chave_publica):
    # A mensagem assinada em string JSON é convertida para um dicionário Python
    mensagem_assinada = json.loads(msg_json)

    # A mensagem original e a assinatura são decodificadas
    # do dicionário em Base64 e são convertidas em bytes
    mensagem = base64.b64decode(mensagem_assinada['mensagem'])
    assinatura = base64.b64decode(mensagem_assinada['assinatura'])

    # Configuração do preenchimento PSS para verificação da assinatura digital
    padding_config = asypadding.PSS(
        mgf=asypadding.MGF1(hashes.SHA256()),
        salt_length=asypadding.PSS.MAX_LENGTH,
    )
    # Validando a assinatura
    try:
        # O método verify da chave pública é chamado
        # para verificar a assinatura
        chave_publica.verify(
            assinatura,  # A assinatura a ser verificada
            mensagem,  # A mensagem original que foi assinada
            padding_config,  # Configuração de preenchimento PSS
            hashes.SHA256(),  # A mesma função hash usada
        )
        # Se for bem-sucedida, imprime que a assinatura é válida
        print('Assinatura válida')
        print('Mensagem: ', mensagem)
        print('Assinatura: ', assinatura, '\n')
    except InvalidSignature:
        # Se falhar, captura a exceção InvalidSignature
        # e imprime que a assinatura é inválida
        print('Assinatura inválida\n')
        print('Mensagem: ', mensagem)
        print('Assinatura: ', assinatura, '\n')


# Inicialização
if __name__ == '__main__':
    chave = base64.urlsafe_b64encode(secrets.token_bytes(32)).decode()
    print('Chave: ', chave + '\n')

    msg = {
        'Emissor': 'Pedro',
        'Remetente': 'Ana',
        'Titulo das Acoes': 'PETR4',
        'Quantidade': 100,
    }

    mensagem_autenticada = gerar_mensagem_autenticada(msg, chave)
    mensagem_serializada = json.dumps(
        mensagem_autenticada, sort_keys=True
    ).encode()

    # Gerar par de chaves
    chave_privada, chave_publica = gerar_chaves_rsa()

    # Assinar mensagem
    msg_json = assinatura(mensagem_serializada, chave_privada)

    # Verificar mensagem
    checar_assinatura(msg_json, chave_publica)
    print(
        'Chave publica: ',
        chave_publica.public_bytes(
            encoding=serialization.Encoding.PEM,
            format=serialization.PublicFormat.SubjectPublicKeyInfo,
        ).decode('utf-8'),
    )

    # Forçar erro
    # Alterar a mensagem
    dados = json.loads(msg_json)
    dados['mensagem'] = base64.b64encode(b'Mensagem adulterada!').decode()

    msg_json_adulterada = json.dumps(dados)
    print('Teste - Mensagem adulterada')
    checar_assinatura(msg_json_adulterada, chave_publica)

    # Alterar a assinatura
    dados = json.loads(msg_json)
    assinatura_bytes = base64.b64decode(dados['assinatura'])

    assinatura_bytes = assinatura_bytes[:-1] + b'\x00'
    dados['assinatura'] = base64.b64encode(assinatura_bytes).decode()

    msg_json_falso = json.dumps(dados)
    print('Teste - Assinatura adulterada')
    checar_assinatura(msg_json_falso, chave_publica)

    # Chave publica diferente
    outra_privada, outra_publica = gerar_chaves_rsa()

    print('Teste - Chave publica diferente')
    checar_assinatura(msg_json, outra_publica)
    print(
        'Chave publica diferente: ',
        outra_publica.public_bytes(
            encoding=serialization.Encoding.PEM,
            format=serialization.PublicFormat.SubjectPublicKeyInfo,
        ).decode('utf-8'),
    )
