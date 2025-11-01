"""
Certificado Pessoal Digital assinado pela CA do IFPR
Gerar chave privada e certificado assinado pela CA
"""

import pathlib
from datetime import datetime, timedelta

from cryptography import x509
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import hashes, serialization
from cryptography.hazmat.primitives.asymmetric import ec, rsa
from cryptography.x509 import (
	CertificateBuilder,
	KeyUsage,
)


def gerar_certificado_pessoal():
	ca_cert_path = pathlib.Path('certificado_raiz_ifpr.pem')
	ca_key_path = pathlib.Path('private_key_raiz_ifpr.pem')
	new_private_key_path = pathlib.Path('private_key_joaogalescky.pem')
	new_certificate_path = pathlib.Path('certificado_joaogalescky.pem')

	# Carregar a chave privada da CA
	with open(ca_key_path, 'rb') as f:
		ca_private_key = serialization.load_pem_private_key(
			f.read(),
			password=None,
		)

	# Carregar o certificado da CA
	with open(ca_cert_path, 'rb') as f:
		ca_certificate = x509.load_pem_x509_certificate(f.read(), default_backend())

	# Criar um novo par de chaves para o certificado assinado
	new_private_key = rsa.generate_private_key(
		public_exponent=65537,
		key_size=2048,
		backend=default_backend()
	)

	# Salvar a nova chave privada em um arquivo (sem criptografia)
	with open(new_private_key_path, 'wb') as f:
		f.write(
			new_private_key.private_bytes(
				encoding=serialization.Encoding.PEM,
				format=serialization.PrivateFormat.TraditionalOpenSSL,
				encryption_algorithm=serialization.NoEncryption(),
			)
		)

	# Gerar a chave pública para o novo certificado
	new_public_key = new_private_key.public_key()

	# Criar o novo certificado
	new_subject = x509.Name([
		x509.NameAttribute(x509.oid.NameOID.COUNTRY_NAME, 'BR'),
		x509.NameAttribute(x509.oid.NameOID.STATE_OR_PROVINCE_NAME, 'PR'),
		x509.NameAttribute(x509.oid.NameOID.LOCALITY_NAME, 'Cascavel'),
		x509.NameAttribute(x509.oid.NameOID.ORGANIZATION_NAME, 'IFPR'),
		x509.NameAttribute(x509.oid.NameOID.EMAIL_ADDRESS, 'joao.galescky@ifpr.edu.br'),
		x509.NameAttribute(x509.oid.NameOID.BUSINESS_CATEGORY, 'Educacao'),
		x509.NameAttribute(x509.oid.NameOID.TITLE, 'Aluno'),
		x509.NameAttribute(x509.oid.NameOID.COMMON_NAME, 'Joao Vitor Campoe Galescky'),
	])

	# Definir a validade do novo certificado
	valid_from_new = datetime.utcnow()
	valid_until_new = valid_from_new + timedelta(days=365)

	# Criar a extensão KEY_USAGE
	key_usage = KeyUsage(
		# Permite a assinatura digital
		digital_signature=True,
		# Não permite compromisso de conteúdo
		content_commitment=False,
		# Permite a criptografia de chaves
		key_encipherment=True,
		# Não permite a criptografia de dados
		data_encipherment=False,
		# Não permite acordo de chave
		key_agreement=False,
		# Não permite assinatura de certificados
		key_cert_sign=False,
		# Não permite assinatura de CRL (Certificados Revogados)
		crl_sign=False,
		# Não permite somente cifragem
		encipher_only=False,
		# Não permite somente decifração
		decipher_only=False,
	)

	# Criar o novo certificado assinado pela CA
	new_certificate = (
		CertificateBuilder()
		.subject_name(new_subject)
		.issuer_name(
			ca_certificate.subject  # O emissor é o certificado da CA
		)
		.public_key(new_public_key)
		.serial_number(x509.random_serial_number())
		.not_valid_before(valid_from_new)
		.not_valid_after(valid_until_new)
		.add_extension(
			key_usage,
			# A extensão é crítica, deve ser verificada para validar o certificado
			critical=True,
			# Assinar com a chave privada da CA
		)
		.sign(ca_private_key, hashes.SHA256(), default_backend())
	)

	# Salvar o novo certificado em um arquivo
	with open(new_certificate_path, 'wb') as f:
		f.write(new_certificate.public_bytes(serialization.Encoding.PEM))

	print('Novo certificado assinado pela CA gerado com sucesso!')


if __name__ == '__main__':
	gerar_certificado_pessoal()
