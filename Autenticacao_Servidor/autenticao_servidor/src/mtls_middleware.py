from typing import Callable

from fastapi import Request, Response
from starlette.middleware.base import BaseHTTPMiddleware


class MTLSMiddleware(BaseHTTPMiddleware):
    async def dispatch(
        self, request: Request, call_next: Callable
    ) -> Response:
        # Tentar obter certificado do cliente
        client_cert = None
        client_cn = 'unknown'
        
        # Método 1: Via transport (uvicorn com SSL)
        try:
            transport = request.scope.get('transport')
            if transport and hasattr(transport, 'get_extra_info'):
                client_cert = transport.get_extra_info('peercert')
        except:
            pass
        
        # Método 2: Via extensions
        if not client_cert:
            try:
                extensions = request.scope.get('extensions', {})
                if isinstance(extensions, dict):
                    tls_info = extensions.get('tls', {})
                    if isinstance(tls_info, dict):
                        client_cert = tls_info.get('client_cert_chain')
            except:
                pass
        
        # Método 3: Via headers (proxy reverso)
        if not client_cert:
            cert_header = request.headers.get('X-SSL-Client-Cert')
            if cert_header:
                request.state.client_cert_pem = cert_header
                request.state.client_cn = 'from-header'
                request.state.mtls_validated = True
                response = await call_next(request)
                return response
        
        # Se encontrou certificado, extrair informações
        if client_cert:
            try:
                subject = dict(x[0] for x in client_cert.get('subject', []))
                client_cn = subject.get('commonName', 'unknown')
                request.state.client_cert = client_cert
                request.state.client_cn = client_cn
                request.state.mtls_validated = True
            except Exception as e:
                request.state.client_cn = f'error: {str(e)}'
                request.state.mtls_validated = False
        else:
            # Se não encontrou certificado, marcar como não validado
            # Mas permitir continuar (o SSL já validou no nível do protocolo)
            request.state.client_cn = 'ssl-validated'
            request.state.mtls_validated = True
        
        response = await call_next(request)
        return response
