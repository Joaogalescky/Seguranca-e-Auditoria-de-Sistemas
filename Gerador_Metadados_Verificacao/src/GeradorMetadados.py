from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.primitives import padding
from cryptography.hazmat.backends import default_backend

def aes_cbc_cifrar(chave, iv, dados):
    # Criptografa os dados usando AES-CBC com padding PKCS7
    padder = padding.PKCS7(128).padder()
    padded = padder.update(dados) + padder.finalize()

    cifrar = Cipher(algorithms.AES(chave), modes.CBC(iv),
                    backend=default_backend())
    cifrador = cifrar.encryptor()
    texto_cifrado = cifrador.update(padded) + cifrador.finalize()

    return texto_cifrado
