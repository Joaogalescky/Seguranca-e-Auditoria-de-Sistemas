"""
Cliente que lê um certificado digital, extrai a chave pública,
cifra uma mensagem e salva o resultado em um arquivo.
"""

import base64
import pathlib
from datetime import datetime

from cryptography import x509
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.asymmetric import padding


def hello():
	print('Olá, servidor!')

	try:
		# Verificar se o certificado existe
		cert_path = pathlib.Path('certificado_joaogalescky.pem')
		if not cert_path.exists():
			raise FileNotFoundError("Erro: Certificado não encontrado")

		message = b'Ola, cliente!'

		# Tentar ler e validar o certificado
		try:
			with open(cert_path, 'rb') as cert_file:
				cert_data = cert_file.read()
				certificate = x509.load_pem_x509_certificate(cert_data, default_backend())
		except ValueError:
			raise ValueError("Erro: Certificado inválido ou corrompido")

		# Verificar data de validade do certificado
		current_time = datetime.utcnow()
		if certificate.not_valid_before > current_time or certificate.not_valid_after < current_time:
			raise ValueError("Erro: Certificado expirado ou ainda não válido")

		# Obter a chave pública do certificado
		try:
			public_key = certificate.public_key()
		except Exception:
			raise ValueError("Erro: Não foi possível extrair a chave pública do certificado")

		# Configurar o padding
		padding_config = padding.OAEP(
			mgf=padding.MGF1(algorithm=hashes.SHA256()),
			algorithm=hashes.SHA256(),
			label=None
		)

		# Cifrar a mensagem
		try:
			ciphertext = public_key.encrypt(message, padding_config)
		except Exception as e:
			raise Exception(f"Erro ao cifrar mensagem: {str(e)}")

		# Codificar a mensagem cifrada em base64
		try:
			ciphertext_base64 = base64.b64encode(ciphertext).decode('utf-8')
		except Exception:
			raise ValueError("Erro: Falha ao codificar mensagem em base64")

		# Salvar o arquivo
		output_path = pathlib.Path('mensagem_cifrada.txt')
		try:
			with open(output_path, 'w', encoding='utf-8') as f:
				f.write(ciphertext_base64)
			print(f'Mensagem cifrada salva em: {output_path}')
		except IOError as e:
			raise IOError(f"Erro ao salvar arquivo cifrado: {str(e)}")

	except Exception as e:
		print(f"Erro: {str(e)}")
		return  # Encerra a função em caso de erro


if __name__ == '__main__':
	hello()
