import base64
import json
import time

from cryptography.exceptions import InvalidSignature
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.asymmetric import padding as asypadding
from cryptography.hazmat.primitives.asymmetric import rsa

usuarios = {}
transacoes = []


""" usuario {
    "nome": "string",
    "saldo": "float",
    "chave_publica": "chave_publica" }
"""

""" transacao {
    "remetente": "string",
    "destinatario": "string",
    "valor": "float",
    "timestamp": 1694029421,
    # adicionado depois
    "assinatura": "base64"
    "status": "valida" ou "invalida" }
"""


def cadastrar_usuario(nome, saldo):
    chave_privada, chave_publica = gerar_chaves_rsa()
    usuarios[nome] = {
        'nome': nome,
        'saldo': saldo,
        'chave_publica': chave_publica,
    }
    print(
        f'Usuário {nome} cadastrado com sucesso!\n'
        + f'Saldo inicial de R$ {saldo} reais!\n'
    )
    return chave_privada


def criar_transacao(remetente, destinatario, valor, chave_privada):
    if remetente not in usuarios:
        print('Remetente inexistente!')
        return None
    if destinatario not in usuarios:
        print('Destinatário inexistente!')
        return None

    if usuarios[remetente]['saldo'] < valor:
        print('Saldo insuficiente!')
        return None

    transacao = {
        'remetente': remetente,
        'destinatario': destinatario,
        'valor': valor,
        'timestamp': int(time.time()),
    }

    # sort_keys: ordena alfabeticamente
    mensagem_serializada = json.dumps(transacao, sort_keys=True).encode()
    msg_json = assinatura(mensagem_serializada, chave_privada)
    return msg_json


def processar_transacao(msg_json):
    dados = json.loads(msg_json)
    transacao = json.loads(base64.b64decode(dados['mensagem']).decode())

    remetente = transacao['remetente']
    destinatario = transacao['destinatario']
    valor = transacao['valor']

    chave_publica = usuarios[remetente]['chave_publica']
    try:
        checar_assinatura(msg_json, chave_publica)
        usuarios[remetente]['saldo'] -= valor
        usuarios[destinatario]['saldo'] += valor
        status = 'valida'
        print(
            f'Transação processada: {remetente}'
            + f' enviou R$ {valor:.2f} reais para {destinatario}\n'
        )
    except InvalidSignature:
        status = 'invalida'
        print('Transação rejeitada: assinatura inválida\n')

    # Desempacota o dicionario e adiciona novos valores ao final
    transacoes.append({
        **transacao,
        'assinatura': dados['assinatura'],
        'status': status,
    })


def exibir_historico():
    print('\nHistórico de transações:')
    for t in transacoes:
        # t: representa um dicionário dentro de transacoes
        print(
            f'{t["remetente"]} enviou '
            + f'para {t["destinatario"]} '
            + f'| R$ {t["valor"]} '
            + f'| {time.ctime(t["timestamp"])} '
            + f' {t["assinatura"]}'
            f'| {t["status"]}\n'
        )


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
    # print('Mensagem assinada: ', msg_json)
    # print('Assinatura (hex):', assinatura.hex())
    # print('Tamanho:', len(assinatura), 'bytes')
    # print('Tamanho:', len(assinatura) * 8, 'bits (!)\n')

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
        return True
        # print('Mensagem: ', mensagem)
        # print('Assinatura: ', assinatura, '\n')
    except InvalidSignature:
        # Se falhar, captura a exceção InvalidSignature
        # e imprime que a assinatura é inválida
        print('Assinatura inválida\n')
        raise
        # print('Mensagem: ', mensagem)
        # print('Assinatura: ', assinatura, '\n')


# Inicialização
if __name__ == '__main__':
    chave_privada_Alice = cadastrar_usuario('Alice', 1000)
    chave_privada_Bob = cadastrar_usuario('Bob', 1000)

    msg_json = criar_transacao('Alice', 'Bob', 100, chave_privada_Alice)

    if msg_json:  # Se verdadeiro, processa a transacao
        processar_transacao(msg_json)

    exibir_historico()

    # Ver saldos
    print('Saldos: ')
    for u in usuarios.values():
        print(f'{u["nome"]}: R$ {u["saldo"]:.2f}')
