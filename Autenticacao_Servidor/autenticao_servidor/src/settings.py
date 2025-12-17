from pathlib import Path

from pydantic_settings import BaseSettings, SettingsConfigDict

BASE_DIR = Path(__file__).parent.parent


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=BASE_DIR / '.env',
        env_file_encoding='utf-8',
    )

    DATABASE_URL: str
    SECRET_KEY: str
    ALGORITHM: str
    ACCESS_TOKEN_EXPIRE_MINUTES: int
    REFRESH_TOKEN_EXPIRE_DAYS: int = 7
    
    # Configurações mTLS
    SSL_KEYFILE: str = 'certs/server-key.pem'
    SSL_CERTFILE: str = 'certs/server-cert.pem'
    SSL_CA_CERTS: str = 'certs/ca-cert.pem'
    SSL_CERT_REQS: int = 2  # ssl.CERT_REQUIRED