from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.primitives import padding
from cryptography.hazmat.backends import default_backend
import secrets

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