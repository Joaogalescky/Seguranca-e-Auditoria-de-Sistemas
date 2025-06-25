from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.primitives import padding
from cryptography.hazmat.backends import default_backend
import secrets
import os
import tkinter as tk
from tkinter import filedialog, messagebox

def aes_cbc_cifrar(chave, iv, texto_claro):
    padder = padding.PKCS7(128).padder() # 128 = 16 bytes
    padded = padder.update(texto_claro) + padder.finalize() # Aplica o padder ao texo_claro
    cifrar = Cipher(algorithms.AES(chave), modes.CBC(iv), backend=default_backend()) # Prepara para a criptografia 
    # backend = motor criptografico
    cifrador = cifrar.encryptor() 
    texto_cifrado = cifrador.update(padded) + cifrador.finalize()
    return texto_cifrado

def cifrar_arquivo(caminho_arquivo, chave):
    # Ler conteúdo
    with open(caminho_arquivo, "rb") as f: #rb = read binary
        conteudo = f.read()
        
    # Gerar IV aleatório
    iv = secrets.token_bytes(16)
    
    # Criptografar conteúdo
    conteudo_cifrado = aes_cbc_cifrar(chave, iv, conteudo)
    
    # Construir cabeçalho/metadados de 32 bytes
    header = bytearray()
    header += b'ED' # Identificador (2 bytes)
    header += bytes([0x01]) # Versão (1 byte) [0x01] = Hexadecimal, cria um objeto de tamanho de 1 byte
    header += bytes([0x01]) # Algoritmo (1 byte)
    header += bytes([0x01]) # Modo (1 byte)
    header += iv # IV (16 bytes)
    header += bytes(11) # Reservado (11 bytes)
    
    # Escrever novo arquivo com cabeçalho + conteúdo cifrado
    saida = caminho_arquivo + ".enc"
    with open(saida, "wb") as f:
        f.write(header + conteudo_cifrado)
    print(f"[SUCESSO] Arquivo cifrado salvo em: {saida}")
    
def aes_cbc_decifrar(chave, iv, texto_cifrado):
    # Decifrar e remover padding
    cifrar = Cipher(algorithms.AES(chave), modes.CBC(iv), backend=default_backend())
    decifrar = cifrar.decryptor()
    padded_texto_claro = decifrar.update(texto_cifrado) + decifrar.finalize()
    unpadder = padding.PKCS7(128).unpadder()
    texto_decifrado = unpadder.update(padded_texto_claro) + unpadder.finalize()
    return texto_decifrado

def decifrar_arquivo(caminho_arquivo, chave):
    # Lê arquivo '.enc', valida o cabeçalho, extrai IV, decifra o conteúdo e salva arquivo original
    with open(caminho_arquivo, "rb") as f:
        conteudo = f.read()
        
    if len(conteudo) < 32:
        raise ValueError("Tamanho de arquivo incompátivel para gerar cabeçalho válido.")

    header = conteudo[:32] # Ir até o 32
    identificador = header[0:2]
    versao = header[2]
    algoritmo = header[3]
    modo = header[4]
    iv = header[5:21]
    conteudo_cifrado = conteudo[32:] # Começar por 32
    
    if identificador != b'ED':
        raise ValueError("Arquivo não possui identificador válido.")
    if versao != 0x01:
        raise ValueError(f"Versão de cabeçalho não suportada: {versao}")
    if algoritmo != 0x01:
        raise ValueError(f"Algoritmo não suportado (esperado AES): {algoritmo}")
    if modo != 0x01:
        raise ValueError(f"Modo de operação não suportado (esperado CBC): {modo}")
    
    conteudo_decifrado = aes_cbc_decifrar(chave, iv, conteudo_cifrado)
    
    # Salvar em novo arquivo
    saida = caminho_arquivo.replace(".enc", "decifrado.txt")
    with open(saida, "wb") as f:
        f.write(conteudo_decifrado)
        
    print(f"[SUCESSO] Arquivo decifrado salvo em: {saida}")

def visualizar_cabecalho(caminho_arquivo):
    try:
        with open(caminho_arquivo, "rb") as f:
            conteudo = f.read(32)
        
        identificador = conteudo[0:2]
        versao = conteudo[2]
        algoritmo = conteudo[3]
        modo = conteudo[4]
        iv = conteudo[5:21]
        reservado = conteudo[21:32]

        info = (
            f"Identificador: {identificador.decode(errors='ignore')}\n"
            f"Versão: {versao}\n"
            f"Algoritmo: {algoritmo} (1 = AES)\n"
            f"Modo: {modo} (1 = CBC)\n"
            f"IV: {iv.hex()}\n"
            f"Reservado: {reservado.hex()}"
        )
        return info
    except Exception as e:
        return f"Erro ao ler cabeçalho: {str(e)}"
    
class AppCripto:
    # Janela
    def __init__(self, master):
        self.master = master
        master.title("Criptografia AES-CBC")
        master.geometry("400x250")

        self.arquivo = None
        self.chave = bytes(range(1, 33))  # chave padrão de 256 bits

        self.label = tk.Label(master, text="Nenhum arquivo selecionado", fg="blue")
        self.label.pack(pady=10)

        self.botao_abrir = tk.Button(master, text="Selecionar Arquivo", command=self.selecionar_arquivo)
        self.botao_abrir.pack(pady=5)

        self.botao_cifrar = tk.Button(master, text="Cifrar Arquivo", command=self.cifrar)
        self.botao_cifrar.pack(pady=5)

        self.botao_decifrar = tk.Button(master, text="Decifrar Arquivo", command=self.decifrar)
        self.botao_decifrar.pack(pady=5)
        
        self.botao_cabecalho = tk.Button(master, text="Ver Cabeçalho", command=self.mostrar_cabecalho)
        self.botao_cabecalho.pack(pady=5)

    def selecionar_arquivo(self):
        caminho = filedialog.askopenfilename()
        if caminho:
            self.arquivo = caminho
            self.label.config(text=os.path.basename(caminho))

    def cifrar(self):
        if not self.arquivo:
            messagebox.showwarning("Aviso", "Selecione um arquivo primeiro.")
            return
        try:
            cifrar_arquivo(self.arquivo, self.chave)
            messagebox.showinfo("Sucesso", "Arquivo cifrado com sucesso!")
        except Exception as e:
            messagebox.showerror("Erro", str(e))

    def decifrar(self):
        if not self.arquivo:
            messagebox.showwarning("Aviso", "Selecione um arquivo primeiro.")
            return
        
        if not self.arquivo.endswith(".enc"):
            messagebox.showwarning("Aviso", "Selecione um arquivo com extensão .enc para decifrar.")
            return
    
        try:
            decifrar_arquivo(self.arquivo, self.chave)
            messagebox.showinfo("Sucesso", "Arquivo decifrado com sucesso!")
        except Exception as e:
            messagebox.showerror("Erro", f"Falha ao decifrar: {str(e)}")
            
    def mostrar_cabecalho(self):
        if not self.arquivo:
            messagebox.showwarning("Aviso", "Selecione um arquivo primeiro.")
            return 
        info = visualizar_cabecalho(self.arquivo)
        messagebox.showinfo("Cabeçalho do Arquivo", info)

# Inicialização
if __name__ == "__main__":
    root = tk.Tk()
    app = AppCripto(root)
    root.mainloop()
