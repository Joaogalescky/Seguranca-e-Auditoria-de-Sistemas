import tkinter as tk
from tkinter import messagebox

def caesar_cipher(text, shift, decrypt=False):
    result = ""
    if decrypt:
        shift = -shift
    for char in text:
        if char.isalpha():
            shift_base = ord('A') if char.isupper() else ord('a')
            result += chr((ord(char) - shift_base + shift) % 26 + shift_base)
        else:
            result += char
    return result

def encrypt():
    text = entry_text.get()
    try:
        shift = int(entry_shift.get())
        encrypted_text.set(caesar_cipher(text, shift))
    except ValueError:
        messagebox.showerror("Erro", "O deslocamento deve ser um número inteiro.")

def decrypt():
    text = entry_text.get()
    try:
        shift = int(entry_shift.get())
        decrypted_text.set(caesar_cipher(text, shift, decrypt=True))
    except ValueError:
        messagebox.showerror("Erro", "O deslocamento deve ser um número inteiro.")

# Configuração da interface gráfica
root = tk.Tk()
root.title("Cifra de César")

tk.Label(root, text="Texto:").grid(row=0, column=0, padx=10, pady=5)
entry_text = tk.Entry(root, width=40)
entry_text.grid(row=0, column=1, padx=10, pady=5)

tk.Label(root, text="Deslocamento:").grid(row=1, column=0, padx=10, pady=5)
entry_shift = tk.Entry(root, width=10)
entry_shift.grid(row=1, column=1, padx=10, pady=5, sticky='w')

tk.Button(root, text="Criptografar", command=encrypt).grid(row=2, column=0, padx=10, pady=5)
tk.Button(root, text="Descriptografar", command=decrypt).grid(row=2, column=1, padx=10, pady=5)

encrypted_text = tk.StringVar()
decrypted_text = tk.StringVar()

tk.Label(root, text="Texto Criptografado:").grid(row=3, column=0, padx=10, pady=5)
tk.Entry(root, textvariable=encrypted_text, width=40, state='readonly').grid(row=3, column=1, padx=10, pady=5)

tk.Label(root, text="Texto Descriptografado:").grid(row=4, column=0, padx=10, pady=5)
tk.Entry(root, textvariable=decrypted_text, width=40, state='readonly').grid(row=4, column=1, padx=10, pady=5)

root.mainloop()
