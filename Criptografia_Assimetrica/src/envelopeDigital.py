import os
import secrets
import tkinter as tk
from tkinter import filedialog, messagebox
from typing import Union

from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import hashes, padding, serialization
from cryptography.hazmat.primitives.asymmetric import padding as asympadding
from cryptography.hazmat.primitives.asymmetric import rsa
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes

# Envelope digital: cifra com AES-CBC + PKCS7 e cifra a chave AES com RSA-OAEP.
""" Formato do envelope:
Tamanho: 22 bytes
 - 2 bytes: magic = b'ED' (identificador)
 - 1 byte : versão = 0x01
 - 1 byte : len_chave_aes_bytes (16/24/32)
 - 2 bytes: len_chave_cifrada_rsa (big-endian)
 - 16 bytes: iv (AES CBC IV)

len_chave_cifrada_rsa bytes: chave AES cifrada com RSA-OAEP
resto: texto cifrado AES-CBC (padded PKCS7)
"""

# Formato do envelope
MAGIC = b'ED'  # 2 bytes
VERSION = 0x01


def aes_cbc_cifrar(chave: bytes, iv: bytes, texto_claro: bytes):
    padder = padding.PKCS7(128).padder()  # 128 = 16 bytes
    padded = padder.update(texto_claro) + padder.finalize()  # Aplica o padder ao texo_claro
    cifrar = Cipher(algorithms.AES(chave), modes.CBC(iv), backend=default_backend())  # Prepara para a criptografia
    # backend = motor criptografico
    cifrador = cifrar.encryptor()
    texto_cifrado = cifrador.update(padded) + cifrador.finalize()
    return texto_cifrado


def aes_cbc_decifrar(chave: bytes, iv: bytes, texto_cifrado: bytes):
    # Decifrar e remover padding
    cifrar = Cipher(algorithms.AES(chave), modes.CBC(iv), backend=default_backend())
    decifrar = cifrar.decryptor()
    padded_texto_claro = decifrar.update(texto_cifrado) + decifrar.finalize()
    unpadder = padding.PKCS7(128).unpadder()
    texto_decifrado = unpadder.update(padded_texto_claro) + unpadder.finalize()
    return texto_decifrado


def gerar_chaves_rsa(bits: int = 4096):
    chave_privada = rsa.generate_private_key(public_exponent=65537, key_size=bits, backend=default_backend(), )
    chave_publica = chave_privada.public_key()

    chave_privada_pem = chave_privada.private_bytes(
        encoding=serialization.Encoding.PEM,
        format=serialization.PrivateFormat.PKCS8,
        encryption_algorithm=serialization.NoEncryption(), )

    chave_publica_pem = chave_publica.public_bytes(
        encoding=serialization.Encoding.PEM,
        format=serialization.PublicFormat.SubjectPublicKeyInfo, )

    return chave_privada_pem, chave_publica_pem


def gerar_arquivos_pem_de_chaves_rsa(chave_privada_pem: bytes, chave_publica_pem: bytes):
    # Gera (ou sobrescreve) as chaves no diretório atual
    with open('private_key.pem', 'wb') as arquivo_privado:
        arquivo_privado.write(chave_privada_pem)

    with open('public_key.pem', 'wb') as arquivo_publico:
        arquivo_publico.write(chave_publica_pem) 
    
    print("[SUCESSO] Chaves geradas e salvas em 'private_key.pem' e 'public_key.pem'")

        
def deserializando_arquivos_pem_de_chaves_rsa():
    with open('private_key.pem', 'rb') as arquivo_privado:
        loaded_private_key = serialization.load_pem_private_key(
                                    arquivo_privado.read(),
                                    password=None,
                                    backend=default_backend()
                                )

    with open('public_key.pem', 'rb') as arquivo_publico:
        loaded_public_key = serialization.load_pem_public_key(
                                arquivo_publico.read(),
                                backend=default_backend()
                            )
    return loaded_private_key, loaded_public_key


def carregar_chave_publica(chave_publica_pem: Union[bytes, str]):
    if isinstance(chave_publica_pem, str):
        with open(chave_publica_pem, 'rb') as f:
                data = f.read()
    else:
        data = chave_publica_pem
    return serialization.load_pem_public_key(data, backend=default_backend())


def carregar_chave_privada(chave_privada_pem: Union[bytes, str]):
    if isinstance(chave_privada_pem, str):
        with open(chave_privada_pem, 'rb') as f:
                data = f.read()
    else:
        data = chave_privada_pem
    return serialization.load_pem_private_key(data, password=None, backend=default_backend())


def cifrar_rsa_publica(chave_publica, conteudo: bytes):
    return chave_publica.encrypt(
        conteudo,
        asympadding.OAEP(
            mgf=asympadding.MGF1(algorithm=hashes.SHA256()),
            algorithm=hashes.SHA256(),
            label=None
        )
    )


def cifrar_rsa_privada(chave_privada, texto_cifrado: bytes):
    return chave_privada.decrypt(
        texto_cifrado,
        asympadding.OAEP(
            mgf=asympadding.MGF1(algorithm=hashes.SHA256()),
            algorithm=hashes.SHA256(),
            label=None
        )
    )


def criar_envelope_bytes(texto_limpo: bytes, recipiente_publico_pem: bytes, len_chave_aes_bytes: int = 32):
    # Retorna bytes do envelope.
    if len_chave_aes_bytes not in (16, 24, 32):
        raise ValueError("[ERRO], Tamanho da Chave AES deve ser de 16, 24 ou 32 bytes")

    # Gerar chave AES e IV
    chave_aes = secrets.token_bytes(len_chave_aes_bytes)
    iv = secrets.token_bytes(16)

    # Cifrar com AES-CBC + PKCS7
    texto_cifrado = aes_cbc_cifrar(chave_aes, iv, texto_limpo)

    # Cifrar a chave AES com RSA-OAEP
    chave_publica = carregar_chave_publica(recipiente_publico_pem)
    chave_cifrada_rsa = cifrar_rsa_publica(chave_publica, chave_aes)

    # Envelope/Cabeçalho
    len_chave_cifrada_rsa = len(chave_cifrada_rsa)
    header = bytearray()
    header += MAGIC
    header += bytes([VERSION])
    header += bytes([len_chave_aes_bytes])
    header += len_chave_cifrada_rsa.to_bytes(2, 'big')  # 65535 bytes
    header += iv
    envelope = bytes(header) + chave_cifrada_rsa + texto_cifrado
    return envelope


def abrir_envelope_bytes(envelope: bytes, recipiente_privado_pem: bytes):
    # Decifra envelope bytes e retorna plaintext.
    # MAGIC + versão + len AES + len RSA + IV
    tamanho_cabecalho = 2 + 1 + 1 + 2 + 16
    if len(envelope) < tamanho_cabecalho:
       raise ValueError("[ERRO] Tamanho de envelope inválido!")

    idx_bytes = 0
    if envelope[idx_bytes:idx_bytes + 2] != MAGIC:
        raise ValueError("[ERRO] Magic inválido! Não é um envelope ED!.")
    idx_bytes += 2

    versao = envelope[idx_bytes]; idx_bytes += 1
    if versao != VERSION:
        raise ValueError(f"[ERRO] Versão do envelope não suportada: {versao}")

    len_chave_aes = envelope[idx_bytes]; idx_bytes += 1
    len_chave_cifrada_rsa = int.from_bytes(envelope[idx_bytes:idx_bytes + 2], 'big'); idx_bytes += 2
    iv = envelope[idx_bytes:idx_bytes + 16]; idx_bytes += 16

    chave_cifrada_rsa = envelope[idx_bytes:idx_bytes + len_chave_cifrada_rsa]; idx_bytes += len_chave_cifrada_rsa
    texto_cifrado = envelope[idx_bytes:]

    '''
    ALTERAR para que carregue, deserialize o private_key.pem criado localmente
    '''
    chave_privada = carregar_chave_privada(recipiente_privado_pem)
    chave_aes = cifrar_rsa_privada(chave_privada, chave_cifrada_rsa)

    if len(chave_aes) != len_chave_aes:
        raise ValueError("[ERRO] Tamanho de chave AES não confere com o indicado no cabeçalho!")

    texto_limpo = aes_cbc_decifrar(chave_aes, iv, texto_cifrado)
    return texto_limpo


# Funções para trabalhar com arquivos
def criar_envelope_arquivo(caminho_arquivo: str, recipiente_publico_pem: bytes, len_chave_aes_bytes: int = 32):
    with open(caminho_arquivo, 'rb') as f:
        conteudo = f.read()
    envelope = criar_envelope_bytes(conteudo, recipiente_publico_pem, len_chave_aes_bytes=len_chave_aes_bytes)

    saida = caminho_arquivo + ".envelope"
    with open(saida, 'wb') as f:
        f.write(envelope)
    print(f"[SUCESSO] Envelope salvo em: {saida}")
    return saida


def abrir_envelope_arquivo(envelope_path: str, caminho_saida: str, recipiente_privado_pem: bytes):
    with open(envelope_path, 'rb') as f:
        envelope = f.read()
    texto_claro = abrir_envelope_bytes(envelope, recipiente_privado_pem)
    with open(caminho_saida, 'wb') as f:
        f.write(texto_claro)
    print(f"[SUCESSO] Envelope aberto! Conteúdo salvo em: {caminho_saida}")


def visualizar_cabecalho(caminho_arquivo: str):
    try:
        with open(caminho_arquivo, "rb") as f:
            conteudo = f.read(22)
            if len(conteudo) < 22:
                raise ValueError("[ERRO] Envelope inválido/corrompido!")

        """ Formato 
        - 2 bytes: magic = b'ED' (identificador)
        - 1 byte : versão = 0x01
        - 1 byte : len_chave_aes_bytes (16/24/32)
        - 2 bytes: len_chave_cifrada_rsa (big-endian)
        - 16 bytes: iv (AES CBC IV)
        """

        idx_bytes = 0
        magic = conteudo[idx_bytes:idx_bytes + 2]; idx_bytes += 2
        versao = conteudo[idx_bytes]; idx_bytes += 1
        aes_len = conteudo[idx_bytes]; idx_bytes += 1
        rsa_len = int.from_bytes(conteudo[idx_bytes:idx_bytes + 2], "big"); idx_bytes += 2
        iv = conteudo[idx_bytes:idx_bytes + 16]

        info = (
            f"Magic: {magic}\n"
            f"Versão: {versao}\n"
            f"Tamanho da chave AES: {aes_len} bytes ({aes_len * 8} bits)\n"
            f"Tamanho da chave RSA cifrada: {rsa_len} bytes\n"
            f"IV: {iv.hex()}"
        )
        return info

    except Exception as e:
        return f"[ERRO] Não foi possivel ler o envelope: {str(e)}"


def testes(caminho_privado=None, caminho_publico=None):
    """
    Executa testes de cifragem/decifragem.
    Se receber caminhos de chave privada/pública, usa eles.
    Caso contrário, tenta usar 'private_key.pem' e 'public_key.pem' no diretório atual.
    Se não existirem, gera novas chaves e salva antes de rodar os testes.
    """

    if caminho_privado and caminho_publico:
        chave_privada_path = caminho_privado
        chave_publica_path = caminho_publico
    else:
        chave_privada_path = "private_key.pem"
        chave_publica_path = "public_key.pem"

    if not (os.path.exists(chave_privada_path) and os.path.exists(chave_publica_path)):
        print("[INFO] Não foram encontradas chaves PEM. Gerando novas...")
        chave_privada_pem, chave_publica_pem = gerar_chaves_rsa(4096)
        gerar_arquivos_pem_de_chaves_rsa(chave_privada_pem, chave_publica_pem)

    # Mensagens de teste: 1 byte, 16 bytes, 1024 bytes, 1MB (aprox)
    mensagens_teste = [
        b'A',
        b'B' * 16,
        b'C' * 1024,
        b'D' * (1024 * 512)  # 128/192/256 bits
    ]
    aes_tamanho = [16, 24, 32]

    for i, msg in enumerate(mensagens_teste, start=1):
        print(f"\n--- Teste {i}: mensagem {len(msg)} bytes ---")
        for k in aes_tamanho:
            print(f"AES key = {k * 8} bits")
            envelope = criar_envelope_bytes(msg, chave_publica_path, len_chave_aes_bytes=k)
            recuperado = abrir_envelope_bytes(envelope, chave_privada_path)
            ok = recuperado == msg
            print(f"-> OK: {ok} (envelope size {len(envelope)} bytes)")
            if not ok:
                raise RuntimeError("Falha ao recuperar a mensagem exatamente.")

    print("\nTodos os testes passaram.")


class AppEnvelope:
    # Janela
    def __init__(self, master):
        self.master = master
        master.title("Envelope Digital AES-CBC | RSA-OAEP")
        master.geometry("400x350")
        
        self.arquivo = None
        self.caminho_chave_publica = None
        self.caminho_chave_privada = None

        self.label = tk.Label(master, text="Nenhum arquivo selecionado", fg="blue")
        self.label.pack(pady=10)

        self.botao_abrir = tk.Button(master, text="Selecionar Arquivo", command=self.selecionar_arquivo)
        self.botao_abrir.pack(pady=5)
        
        self.botao_gerar_chaves = tk.Button(master, text="Gerar Par de Chaves", command=self.gerar_chaves)
        self.botao_gerar_chaves.pack(pady=5)
        
        self.botao_chave_publica = tk.Button(master, text="Selecionar Chave Pública", command=self.selecionar_chave_publica)
        self.botao_chave_publica.pack(pady=5)

        self.botao_chave_privada = tk.Button(master, text="Selecionar Chave Privada", command=self.selecionar_chave_privada)
        self.botao_chave_privada.pack(pady=5)

        self.botao_cifrar = tk.Button(master, text="Cifrar (Criar Envelope)", command=self.cifrar)
        self.botao_cifrar.pack(pady=5)

        self.botao_decifrar = tk.Button(master, text="Decifrar (Abrir Envelope)", command=self.decifrar)
        self.botao_decifrar.pack(pady=5)

        self.botao_cabecalho = tk.Button(master, text="Ver Cabeçalho", command=self.mostrar_cabecalho)
        self.botao_cabecalho.pack(pady=5)

        self.botao_teste = tk.Button(master, text="Testar", command=self.testar)
        self.botao_teste.pack(pady=5)

    def selecionar_arquivo(self):
        caminho = filedialog.askopenfilename()
        if caminho:
            self.arquivo = caminho
            self.label.config(text=os.path.basename(caminho))
    
    def gerar_chaves(self):
        try:
            # Se já existe, pergunte
            existe_privada = os.path.exists("private_key.pem")
            existe_publica = os.path.exists("public_key.pem")
            
            if existe_privada or existe_publica:
                resposta = messagebox.askyesno(
                    "Confirmação",
                    "Já existem chaves 'private_key.pem' e/ou 'public_key.pem\n"
                    "Deseja sobrescrevê-las?"
                )
                if not resposta:
                    messagebox.showinfo("[INFO]", "Geração de chaves cancelada")
                    return
            
            # Se não existe, gere
            chave_privada_pem, chave_publica_pem = gerar_chaves_rsa(4096)
            gerar_arquivos_pem_de_chaves_rsa(chave_privada_pem, chave_publica_pem)
                
            if existe_privada or existe_publica:
                messagebox.showinfo("[SUCESSO]", "Chaves foram regeneradas com sucesso!")
            else:
                messagebox.showinfo("[SUCESSO]", "Chaves foram geradas com sucesso!")
        except Exception as e:
            messagebox.showerror("[ERRO]", f"Erro ao gerar chaves: {str(e)}")
      
    def selecionar_chave_publica(self):
        try:
            caminho = filedialog.askopenfilename(
            title="Escolha a chave pública (PEM)",
            filetypes=[("PEM files", "*.pem"), ("All files", "*.*")])
            if caminho:
                self.caminho_chave_publica = caminho
                self.label.config(text=f"{os.path.basename(self.arquivo) if self.arquivo else 'Nenhum arquivo selecionado'}\nChave pública: {os.path.basename(caminho)}")
        except Exception as e:
            messagebox.showerror("[ERRO]", f"Falha ao selecionar uma chave publica: {str(e)}")
            
    def selecionar_chave_privada(self):
        try:
            caminho = filedialog.askopenfilename(
            title="Escolha a chave privada (PEM)",
            filetypes=[("PEM files", "*.pem"), ("All files", "*.*")])
            if caminho:
                self.caminho_chave_privada = caminho
                self.label.config(text=f"{os.path.basename(self.arquivo) if self.arquivo else 'Nenhum arquivo selecionado'}\nChave privada: {os.path.basename(caminho)}")
        except Exception as e:
            messagebox.showerror("[ERRO]", f"Falha ao selecionar uma chave privada: {str(e)}")

    def cifrar(self):
        if not self.arquivo:
            messagebox.showwarning("[AVISO]", "Selecione um arquivo.")
            return
        if self.arquivo.endswith(".envelope"):
            messagebox.showwarning("[AVISO]", "Arquivo já cifrado!")
            return
        if not self.caminho_chave_publica:
            messagebox.showwarning("[AVISO]", "Selecione uma chave pública (.pem) antes de cifrar.")
            return
        try:
            saida = criar_envelope_arquivo(self.arquivo, self.caminho_chave_publica, len_chave_aes_bytes=32)
            messagebox.showinfo("[SUCESSO]", f"Envelope criado com sucesso em: {saida}")
        except Exception as e:
            messagebox.showerror("[ERRO]", f"Falha ao cifrar: {str(e)}")

    def decifrar(self):
        if not self.arquivo:
            messagebox.showwarning("[AVISO]", "Selecione um arquivo.")
            return
        if not self.arquivo.endswith(".envelope"):
            messagebox.showwarning("[AVISO]", "Selecione um arquivo .envelope para abrir.")
            return
        if not self.caminho_chave_privada:
            messagebox.showwarning("[AVISO]", "Selecione uma chave privada (.pem) antes de decifrar.")
            return
        try:
            saida = self.arquivo.replace(".envelope", "_decifrado")
            abrir_envelope_arquivo(self.arquivo, saida, self.caminho_chave_privada)
            messagebox.showinfo("[SUCESSO]", f"Envelope aberto. Arquivo salvo em: {saida}")
        except Exception as e:
            messagebox.showerror("[ERRO]", f"Falha ao decifrar: {str(e)}")

    def mostrar_cabecalho(self):
        if not self.arquivo:
            messagebox.showwarning("[AVISO]", "Selecione um arquivo.")
            return
        if not self.arquivo.endswith(".envelope"):
            messagebox.showwarning("[AVISO]", "Selecione um arquivo .envelope válido.")
            return
        try:
            info = visualizar_cabecalho(self.arquivo)
            messagebox.showinfo("Cabecalho do Arquivo", info)
        except Exception as e:
            messagebox.showerror("[ERRO]", f"Falha ao ler cabeçalho: {str(e)}")

    def testar(self):
        try:
            testes(self.caminho_chave_privada, self.caminho_chave_publica)
            messagebox.showinfo("[SUCESSO]", "Visualize o terminal para ver o resultado!")
        except Exception as e:
            messagebox.showerror("[ERRO]", f"Não foi possível realizar o teste!: {str(e)}")


# Inicialização
if __name__ == "__main__":
    root = tk.Tk()
    app = AppEnvelope(root)
    root.mainloop()
