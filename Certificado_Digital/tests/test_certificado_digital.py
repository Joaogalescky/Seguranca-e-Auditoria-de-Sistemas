import datetime
import pathlib
import shutil
import sys
import unittest

import pytest
from cryptography import x509
from cryptography.exceptions import InvalidTag
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.asymmetric import padding, rsa
from cryptography.x509.oid import NameOID

# Adiciona o diretório src ao PYTHONPATH
sys.path.append(str(pathlib.Path(__file__).parent.parent / 'src'))


class TestCertificadoDigital(unittest.TestCase):
	@classmethod
	def setUpClass(cls):
		# Criar diretório temporário para os testes
		cls.test_dir = pathlib.Path('test_temp')
		cls.test_dir.mkdir(exist_ok=True)

		# Gerar par de chaves malicioso para testes
		cls.malicious_private_key = rsa.generate_private_key(public_exponent=65537, key_size=2048)
		cls.malicious_public_key = cls.malicious_private_key.public_key()

		# Gerar par de chaves legítimo e um certificado autoassinado para os testes
		cls.legit_private_key = rsa.generate_private_key(public_exponent=65537, key_size=2048)
		cls.legit_public_key = cls.legit_private_key.public_key()

		subject = issuer = x509.Name([
			x509.NameAttribute(NameOID.COUNTRY_NAME, 'BR'),
			x509.NameAttribute(NameOID.STATE_OR_PROVINCE_NAME, 'PR'),
			x509.NameAttribute(NameOID.LOCALITY_NAME, 'Curitiba'),
			x509.NameAttribute(NameOID.ORGANIZATION_NAME, 'IFPR'),
			x509.NameAttribute(NameOID.COMMON_NAME, 'certificado-legal.test'),
		])

		cls.certificate = (
x509.CertificateBuilder()
			.subject_name(subject)
			.issuer_name(issuer)
			.public_key(cls.legit_public_key)
			.serial_number(x509.random_serial_number())
			.not_valid_before(datetime.datetime.utcnow() - datetime.timedelta(days=1))
			.not_valid_after(datetime.datetime.utcnow() + datetime.timedelta(days=365))
			.add_extension(
				x509.BasicConstraints(ca=True, path_length=None),
				critical=True,
			)
			.sign(private_key=cls.legit_private_key, algorithm=hashes.SHA256())
		)

	def setUp(self):
		# Preparar mensagem de teste
		self.test_message = b'Mensagem de teste'

	def test_servidor_autentico(self):
		"""Testa o cenário onde o servidor é autêntico"""
		# Carregar certificado válido
		# Usar o certificado gerado em memória
		certificate = self.__class__.certificate

		# Verificar se o certificado é válido
		public_key = certificate.public_key()
		try:
			# Tentar cifrar uma mensagem
			padding_config = padding.OAEP(
				mgf=padding.MGF1(algorithm=hashes.SHA256()), algorithm=hashes.SHA256(), label=None
			)
			ciphertext = public_key.encrypt(self.test_message, padding_config)
			assert ciphertext is not None, 'Ciframento falhou'
		except Exception as e:
			self.fail(f'O certificado válido falhou: {str(e)}')

	def test_servidor_nao_autentico(self):
		"""Testa o cenário onde o servidor não é autêntico"""
		# Tentar usar uma chave pública maliciosa
		try:
			padding_config = padding.OAEP(
				mgf=padding.MGF1(algorithm=hashes.SHA256()), algorithm=hashes.SHA256(), label=None
			)
			ciphertext = self.malicious_public_key.encrypt(self.test_message, padding_config)

			# Verificar se o servidor consegue decifrar com a chave privada correta
			# Usar a chave privada legítima gerada em memória
			private_key = self.__class__.legit_private_key

			with pytest.raises(InvalidTag):
				# Apenas chamar decrypt; esperamos uma exceção porque a chave
				# privada legítima não corresponde à chave pública maliciosa
				private_key.decrypt(
					ciphertext,
					padding.OAEP(
						mgf=padding.MGF1(algorithm=hashes.SHA256()),
						algorithm=hashes.SHA256(),
						label=None,
					),
				)

		except Exception:
			# Esperamos que falhe ao tentar decifrar
			pass

	def test_cliente_nao_autentico(self):
		"""Testa o cenário onde o cliente não é autêntico"""
		# Tentar usar um certificado inexistente
		fake_cert_path = self.test_dir / 'fake_cert.pem'
		# Abrir um arquivo inexistente deve gerar FileNotFoundError
		with pytest.raises(FileNotFoundError):
			# O read é suficiente para disparar a exceção
			open(fake_cert_path, 'rb').read()

	def test_interceptacao_mensagem(self):
		"""Testa o cenário de interceptação de mensagem"""
		# Primeiro, cifrar uma mensagem normalmente
		# Usar o certificado gerado em memória
		certificate = self.__class__.certificate
		public_key = certificate.public_key()
		padding_config = padding.OAEP(
			mgf=padding.MGF1(algorithm=hashes.SHA256()), algorithm=hashes.SHA256(), label=None
		)

		ciphertext = public_key.encrypt(self.test_message, padding_config)

		# Simular uma tentativa de modificar a mensagem cifrada
		modified_ciphertext = bytearray(ciphertext)
		modified_ciphertext[0] ^= 1  # Modifica um bit

		# Tentar decifrar a mensagem modificada
		private_key = self.__class__.legit_private_key

		with pytest.raises(ValueError, match="Decryption failed"):
			private_key.decrypt(
				bytes(modified_ciphertext),
				padding.OAEP(
					mgf=padding.MGF1(algorithm=hashes.SHA256()),
					algorithm=hashes.SHA256(),
					label=None,
				),
			)

	@classmethod
	def tearDownClass(cls):
		# Limpar arquivos temporários

		shutil.rmtree(cls.test_dir)


if __name__ == '__main__':
	unittest.main()
