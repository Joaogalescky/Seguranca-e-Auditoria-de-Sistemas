import ssl
import uvicorn
from pathlib import Path

from src.settings import Settings

settings = Settings()
BASE_DIR = Path(__file__).parent

if __name__ == '__main__':
    print(f"Servidor mTLS iniciado em https://0.0.0.0:8443")
    print(f"Certificado do servidor: {BASE_DIR / settings.SSL_CERTFILE}")
    print(f"CA: {BASE_DIR / settings.SSL_CA_CERTS}")
    print(f"Modo de verificação: CERT_REQUIRED")
    print(f"\nPara testar, use:")
    print(f"curl --cacert certs/ca-cert.pem --cert certs/client-cert.pem --key certs/client-key.pem https://localhost:8443/")
    
    uvicorn.run(
        'src.main:app',
        host='0.0.0.0',
        port=8443,
        ssl_keyfile=str(BASE_DIR / settings.SSL_KEYFILE),
        ssl_certfile=str(BASE_DIR / settings.SSL_CERTFILE),
        ssl_ca_certs=str(BASE_DIR / settings.SSL_CA_CERTS),
        ssl_cert_reqs=ssl.CERT_REQUIRED,
        reload=False
    )
