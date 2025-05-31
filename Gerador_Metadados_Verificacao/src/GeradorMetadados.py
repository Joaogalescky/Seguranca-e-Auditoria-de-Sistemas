from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.primitives import padding
from cryptography.hazmat.backends import default_backend
import secrets
import os

def aes_cbc_cifrar(chave, iv, dados):
    # Criptografa os dados usando AES-CBC com padding PKCS7
    padder = padding.PKCS7(128).padder()
    padded = padder.update(dados) + padder.finalize()

    cifrar = Cipher(algorithms.AES(chave), modes.CBC(iv),
                    backend=default_backend())
    cifrador = cifrar.encryptor()
    texto_cifrado = cifrador.update(padded) + cifrador.finalize()

    return texto_cifrado

def gerar_arquivos(caminho_arquivo, chave):
    with open(caminho_arquivo, "rb") as f:
        conteudo = f.read()
        
    iv = secrets.token_bytes(16)
    texto_cifrado = aes_cbc_cifrar(chave, iv, conteudo)
    fingerprint = texto_cifrado[-16:]
    
    header = bytearray()
    header += b'CF'             # Identificador
    header += bytes([0x01])     # Versão
    header += bytes([0x01])     # Algoritmo AES
    header += bytes([0x01])     # Modo CBC
    header += iv                # IV
    header += fingerprint       # Fingerprint
    header += bytes(11)         # Reservado
    
    saida = caminho_arquivo + ".meta"
    with open(saida, "wb") as f:
        f.write(header)
        
    return saida

def verificar_integridade(caminho_arquivo, chave):
    caminho_metadados = caminho_arquivo + ".meta"
    
    if not os.path.exists(caminho_metadados):
        return "[ERRO] Arquivo .meta não encontrado!"
    
    with open(caminho_metadados, "rb") as f:
        dados = f.read(48)
        
    if len(dados) != 48:
        return "[ERRO] Arquivo .meta inválido!"
    
    ident = dados[0:2]
    versao = dados[2]
    algoritmo = dados[3]
    modo = dados[4]
    iv = dados[5:21]
    fingerprint_armazenado = dados[21:37]
    
    if ident != b'CF' or versao != 1 or algoritmo != 1 or modo != 1:
        return "[ERRO] Cabeçalho inválido ou incompátivel!"
    
    with open(caminho_arquivo, "rb") as f:
        conteudo = f.read()
        
    novo_cifrar = aes_cbc_cifrar(chave, iv, conteudo)
    novo_fingerprint = novo_cifrar[-16:]
    
    if novo_fingerprint == fingerprint_armazenado:
        return "[SUCESSO] Integridade verificada: arquivo não foi modificado"
    else:
        return "[ATENÇÃO]! Arquivo foi modificado ou corrompido!"