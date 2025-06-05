from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.primitives import padding
from cryptography.hazmat.backends import default_backend
import secrets
import os
import tkinter as tk
from tkinter import filedialog, messagebox


def aes_cbc_cifrar(chave, iv, dados):
    # Criptografa os dados usando AES-CBC com padding PKCS7
    padder = padding.PKCS7(128).padder()
    padded = padder.update(dados) + padder.finalize()
    cifrar = Cipher(algorithms.AES(chave), modes.CBC(iv), backend=default_backend())
    cifrador = cifrar.encryptor()
    texto_cifrado = cifrador.update(padded) + cifrador.finalize()
    return texto_cifrado


def gerar_metadados(caminho_arquivo, chave):
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


def visualizar_meta(caminho_arquivo):
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
    fingerprint = dados[21:37]
    reservado = dados[37:48]

    info = (
        f"Identificador: {ident.decode(errors='ignore')}\n"
        f"Versão: {versao}\n"
        f"Algoritmo: {algoritmo} (1 = AES)\n"
        f"Modo: {modo} (1 = CBC)\n"
        f"IV: {iv.hex()}\n"
        f"Fingerprint: {fingerprint.hex()}\n"
        f"Reservado: {reservado.hex()}"
    )

    return info


class AppMeta:
    def __init__(self, master):
        self.master = master
        master.title(
            "Verificação de Integridade - Criptografia AES - Modo CBC")
        master.geometry("200x200")
        self.arquivo = None
        self.chave = bytes(range(1, 33))  # 256 bits

        self.label = tk.Label(
            master, text="Nenhum arquivo selecionado", fg="blue")
        self.label.pack(pady=10)

        self.botao_abrir = tk.Button(
            master, text="Selecionar Arquivo", command=self.selecionar_arquivo)
        self.botao_abrir.pack(pady=5)

        self.botao_gerar = tk.Button(
            master, text="Gerar .meta", command=self.gerar_metadados)
        self.botao_gerar.pack(pady=5)

        self.botao_verificar = tk.Button(
            master, text="Verificar Integridade", command=self.verificar)
        self.botao_verificar.pack(pady=5)
        
        self.botao_visualizar = tk.Button(
            master, text="Visualizar Metadados", command=self.visualizar_metadados)
        self.botao_visualizar.pack(pady=5)

    def selecionar_arquivo(self):
        caminho = filedialog.askopenfilename()
        if caminho:
            self.arquivo = caminho
            self.label.config(text=os.path.basename(caminho))

    def gerar_metadados(self):
        if not self.arquivo:
            messagebox.showwarning("[AVISO]", "Selecione um arquivo!")
            return
        try:
            saida = gerar_metadados(self.arquivo, self.chave)
            messagebox.showinfo("[SUCESSO]", f"Arquivo .meta gerado:\n{saida}")
        except Exception as e:
            messagebox.showerror("[ERRO]", f"Erro ao gerar .meta:\n{e}")

    def verificar(self):
        if not self.arquivo:
            messagebox.showwarning("[AVISO]", "Selecione um arquivo!")
            return
        try:
            resultado = verificar_integridade(self.arquivo, self.chave)
            if "ATENÇÃO" in resultado:
                messagebox.showwarning("Integridade", resultado)
            else:
                messagebox.showinfo("Integridade", resultado)
        except Exception as e:
            messagebox.showerror("[ERRO]", f"Erro na verificação:\n{e}")

    def visualizar_metadados(self):
        if not self.arquivo:
            messagebox.showwarning("[AVISO]", "Selecione um arquivo!")
            return
        try:
            info = visualizar_meta(self.arquivo)
            messagebox.showinfo("Conteúdo do .meta", info)
        except Exception as e:
            messagebox.showerror("[ERRO]", f"Erro ao ler .meta:\n{e}")


if __name__ == "__main__":
    root = tk.Tk()
    app = AppMeta(root)
    root.mainloop()
