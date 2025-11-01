"""
Certificado Raiz Digital do IFPR
Gerar chave privada e certificado autoassinado
"""

import pathlib
from datetime import datetime, timedelta

from cryptography import x509
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import hashes, serialization
from cryptography.hazmat.primitives.asymmetric import rsa
from cryptography.x509 import CertificateBuilder, SubjectAlternativeName


def certificado_raiz():
	# Gerar uma chave privada RSA
	private_key = rsa.generate_private_key(
		public_exponent=65537,
		key_size=2048,
		backend=default_backend()
	)

	# Salvar a chave privada em um arquivo PEM
	with open('private_key_raiz_ifpr.pem', 'wb') as f:
		f.write(
			private_key.private_bytes(
				encoding=serialization.Encoding.PEM,
				format=serialization.PrivateFormat.TraditionalOpenSSL,
				encryption_algorithm=serialization.NoEncryption(),
			)
		)

	# Gerar a chave pública
	public_key = private_key.public_key()

	# Criar certificado autoassinado
	subject = x509.Name([
		x509.NameAttribute(x509.oid.NameOID.COUNTRY_NAME, 'BR'),
		x509.NameAttribute(x509.oid.NameOID.STATE_OR_PROVINCE_NAME, 'PR'),
		x509.NameAttribute(x509.oid.NameOID.LOCALITY_NAME, 'Cascavel'),
		x509.NameAttribute(x509.oid.NameOID.ORGANIZATION_NAME, 'IFPR'),
		x509.NameAttribute(x509.oid.NameOID.EMAIL_ADDRESS, 'ifpr.cascavel@ifpr.edu.br'),
		x509.NameAttribute(x509.oid.NameOID.BUSINESS_CATEGORY, 'Educacao'),
		x509.NameAttribute(x509.oid.NameOID.COMMON_NAME, 'ifpr.edu.br'),
	])

	# Autoassinado
	issuer = subject

	# Definir validade do certificado
	valid_from = datetime.utcnow()
	valid_until = valid_from + timedelta(days=365 * 2)

	# Criar e assinar certificado
	certificate = (
		CertificateBuilder()
		.subject_name(subject)
		.issuer_name(issuer)
		.public_key(public_key)
		.serial_number(x509.random_serial_number())
		.not_valid_before(valid_from)
		.not_valid_after(valid_until)
		.add_extension(
			SubjectAlternativeName([x509.DNSName('alternativo.ifpr.edu.br')]),
			critical=False,
		)
		.sign(private_key, hashes.SHA256(), default_backend())
	)

	# Salvar o certificado em um arquivo PEM
	certificate_path = pathlib.Path('certificado_raiz_ifpr.pem')
	private_key_path = pathlib.Path('private_key_raiz_ifpr.pem')

	with open(certificate_path, 'wb') as f:
		f.write(certificate.public_bytes(serialization.Encoding.PEM))

	print('Chaves e certificado gerados com sucesso!')
	print(f'Chave privada salva em: {pathlib.Path(private_key_path).resolve()}')
	print(f'Certificado salvo em: {pathlib.Path(certificate_path).resolve()}')


if __name__ == '__main__':
	certificado_raiz()
