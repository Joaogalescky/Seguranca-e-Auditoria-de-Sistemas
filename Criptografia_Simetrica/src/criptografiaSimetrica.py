# Bibliotecas
import secrets
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import padding

def cifrar_AES_CBC(chave, iv, texto_claro):
    padder = padding.PKCS7(128).padder()
    padded = padder.update(texto_claro) + padder.finalize()
    cifrar = Cipher(algorithms.AES(chave), modes.CBC(iv), backend=default_backend())
    encriptar = cifrar.encryptor()
    return encriptar.update(padded) + encriptar.finalize()

def cifrarArquivo(caminho_arquivo, chave):
    # Ler conteúdo
    with open(caminho_arquivo, "rb") as f:
        conteudo = f.read()
        
    # Gerar IV aleatório
    iv = secrets.token_bytes(16)
    
    # Criptografar conteúdo
    conteudo_cifrado = cifrar_AES_CBC(chave, iv, conteudo)
    
    # Construir cabeçalho/metadados de 32 bytes
    header = bytearray()
    header += b'ED' # Identificador (2 bytes)
    header += bytes([0x01]) # Versão (1 byte)
    header += bytes([0x01]) # Algoritmo (1 byte)
    header += bytes([0x01]) # Modo (1 byte)
    header += iv # IV (16 bytes)
    header += bytes(11) # Reservado (11 bytes)
    
    # Escrever novo arquivo com cabeçalho + conteúdo cifrado
    saida = caminho_arquivo + ".enc"
    with open(saida, "wb") as f:
        f.write(header + conteudo_cifrado)
    print(f"[SUCESSO] Arquivo cifrado salvo em: {saida}")
    
def decifrar_AES_CBC(chave, iv, texto_cifrado):
    # Decifrar e remover padding
    cifrar = Cipher(algorithms.AES(chave), modes.CBC(iv), backend=default_backend())
    decifrar = cifrar.decryptor()
    padded_texto_claro = decifrar.update(texto_cifrado) + decifrar.finalize()
    unpadder = padding.PKCS7(128).unpadder()
    return unpadder.update(padded_texto_claro) + unpadder.finalize()

def decifrarArquivo(caminho_arquivo, chave):
    # Lê arquivo '.enc', valida o cabeçalho, extrai IV, decifra o conteúdo e salva arquivo original
    with open(caminho_arquivo, "rb") as f:
        conteudo = f.read()

    header = conteudo[:32]
    identificador = header[0:2]
    versao = header[2]
    algoritmo = header[3]
    modo = header[4]
    iv = header[5:21]

    iv = header[5:21]
    conteudo_cifrado = conteudo[32:]
    conteudo_decifrado = decifrar_AES_CBC(chave, iv, conteudo_cifrado)
    
    # Salvar em novo arquivo
    saida = caminho_arquivo.replace(".enc", "decifrado.txt")
    with open(saida, "wb") as f:
        f.write(conteudo_decifrado)
        
    print(f"[SUCESSO] Arquivo decifrado salvo em: {saida}")
    
    #====================================================================== 
    # Criar um arquivo de teste
    with open("mensagem.txt", "wb") as f:
        f.write(b"Exemplo de conteudo super secreto.")

    # Chave AES de 256 bits
    chave = bytes(range(1, 33))

    # Cifrar
    cifrarArquivo("mensagem.txt", chave)
    
    chave = bytes(range(1, 33))
    decifrarArquivo("mensagem.txt.enc", chave)