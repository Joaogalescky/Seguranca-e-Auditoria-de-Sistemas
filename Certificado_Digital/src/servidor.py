"""
Servidor que lê uma mensagem cifrada de um arquivo,
decifra usando a chave privada e salva o resultado em outro arquivo.
"""

import base64
import pathlib

from cryptography.hazmat.primitives import hashes, serialization
from cryptography.hazmat.primitives.asymmetric import padding


def decifrar_mensagem():
	try:
		# Verificar se a chave privada existe
		private_key_path = pathlib.Path(__file__).parent / 'private_key_joaogalescky.pem'
		if not private_key_path.exists():
			raise FileNotFoundError("Chave privada não encontrada")

		input_path = pathlib.Path(__file__).parent / 'mensagem_cifrada.txt'
		if not input_path.exists():
			raise FileNotFoundError("Arquivo com mensagem cifrada não encontrado")

		output_path = pathlib.Path(__file__).parent / 'mensagem_decifrada.txt'

		# Carregar chave privada
		try:
			with open(private_key_path, 'rb') as key_file:
				private_key = serialization.load_pem_private_key(
					key_file.read(),
					password=None,
				)
		except ValueError:
			raise ValueError("Chave privada inválida ou corrompida")

		# Ler mensagem cifrada (Base64)
		try:
			with open(input_path, 'r', encoding='utf-8') as f:
				cipher_base64 = f.read()
			ciphertext = base64.b64decode(cipher_base64)
		except Exception:
			raise ValueError("Mensagem cifrada corrompida ou formato inválido")

		# Decifrar
		try:
			plaintext = private_key.decrypt(
				ciphertext,
				padding.OAEP(
					mgf=padding.MGF1(algorithm=hashes.SHA256()),
					algorithm=hashes.SHA256(),
					label=None
				)
			)
		except ValueError:
			raise ValueError("Erro na decifragem: a mensagem pode ter sido alterada")
		except Exception as e:
			raise Exception(f"Erro inesperado na decifragem: {str(e)}")

		# Salvar resultado
		try:
			with open(output_path, 'wb') as f:
				f.write(plaintext)
			print(f'Mensagem decifrada salva em: {output_path}')
		except IOError as e:
			raise IOError(f"Erro ao salvar arquivo decifrado: {str(e)}")

	except Exception as e:
		print(f'Erro: {str(e)}')
		return  # Encerra a função se houver erro


if __name__ == '__main__':
	decifrar_mensagem()
