from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.asymmetric import padding
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives.asymmetric import rsa
import os
import tkinter as tk
from tkinter import filedialog, messagebox

# Geração de par de chaves
private_key = rsa.generate_private_key(public_exponent=65537, key_size=3072, backend=default_backend(), )
# 65537: número primo; poucos bits 1; grande o suficiente
public_key = private_key.public_key()

# Serializando chave privada
# Formato: Privacy-Enhanced Mail (PEM)
private_bytes = private_key.private_bytes(
        encoding=serialization.Encoding.PEM,
        format=serialization.PrivateFormat.PKCS8,
        encryption_algorithm=serialization.NoEncryption(), )

with open('private_key.pem', 'xb') as private_file:
  private_file.write(private_bytes)

public_bytes = public_key.public_bytes(
        encoding=serialization.Encoding.PEM,
        format=serialization.PublicFormat.SubjectPublicKeyInfo, )

with open('public_key.pem', 'xb') as public_file:
  public_file.write(public_bytes)

# Arquivos gerados
with open('public_key.pem', 'r') as arquivo:
    conteudo = arquivo.read()
    print(conteudo)

with open('private_key.pem', 'r') as arquivo:
    conteudo = arquivo.read()
    print(conteudo)
    
# Deserializando
with open('private_key.pem', 'rb') as private_file:
  loaded_private_key = serialization.load_pem_private_key(
                            private_file.read(),
                            password=None,
                            backend=default_backend()
                          )

with open('public_key.pem', 'rb') as public_file:
  loaded_public_key = serialization.load_pem_public_key(
                          public_file.read(),
                          backend=default_backend()
                         )

# Criptografando
padding_config = padding.OAEP(
                    mgf=padding.MGF1(algorithm=hashes.SHA256()),
                    algorithm=hashes.SHA256(),
                    label=None, )

plaintext = b'Bob, este eh um segredo. Nao conte para ninguem. Ass: Alice'

ciphertext = loaded_public_key.encrypt(
                    plaintext=plaintext,
                    padding=padding_config, )

print("Texto cifrado (hex):", ciphertext.hex())
print("Tamanho:", len(ciphertext), "bytes" )
print("Tamanho:", len(ciphertext)*8, "bits (!)" )

# Descriptografando
decrypted_by_private_key = loaded_private_key.decrypt(
                            ciphertext=ciphertext,
                            padding=padding_config)

print("Texto descriptografado (hex):", decrypted_by_private_key.hex())
print("Tamanho:", len(decrypted_by_private_key), "bytes" )
print('Text:', decrypted_by_private_key)

