# Gerador de Arquivo de Metadados para Verificação de Integridade

Programa de geração de arquivo de metadados (48 *bytes*) contendo um cabeçalho e um *fingerprint* (16 *bytes*), para verificar se o arquivo original foi modificado, o ultimo bloco da criptografia AES (_Advanced Encryption Standard_) no modo CBC (_Cipher Block Chaining_).

## Instruções
1. **Cabeçalho do Arquivo de Metadados (48 bytes)**: O arquivo de metadados deve conter exatamente 48 bytes, dispostos assim::

    | Campo| Tamanho (bytes) | Descrição
    |:--------|:--------:|:--------
    | Identificador | 2 | Sequência fixa, ex: ==b'CF'==, para indicar “*Crypto Fingerprint*”
    | Versão | 1 | Versão do formato (ex: ==1==)
    | Algoritmo | 1 | ==1== para AES
    | Modo | 1 | ==1== para CBC
    | IV | 16 | Vetor de inicialização (aleatório)
    | Fingerprint | 16 | Último bloco do ciphertext gerado a partir do arquivo original (garante integridade)
    | Reversado | 11 | Reservado para uso futuro (preencher com ==0x00==)

2. **Geração do arquivo de metadados**:
   1. **Entrada do Usuário**:
   - Solicitar o caminho do arquivo original a ser protegido
   2. **Chave e IV**:
   - Gerar (ou solicitar) uma chave AES de 256 bits.
   - Gerar um IV aleatório de 16 bytes.
   3. **Cálculo do Fingerprint**:
   - Ler todo o conteúdo do arquivo original.
   - Aplicar AES-CBC com paadding PKCS7 sobre esse conteúdo somente em memória  (não salvar o texto cifrado em disco).
   - Extrair os últimos 16 bytes do ciphertext gerado como *fingerprint*.
   4. **Montagem do Cabeçalho**:
   - Empacotar, em ordem:
   - Identificador (2 bytes)
   - Versão (1 byte)
   - Algoritmo (1 byte)
   - Modo (1 byte)
   - IV (16 bytes)
   - *Fingerprint* (16 bytes)
   - Reserved (11 bytes de ==0x00==)
   5. **Gravação do Arquivo de Metadados**:
   - Salvar esses 48 bytes em um novo arquivo (por exemplo, com extensão .==meta==).

3. **Verificação de Integridade**:
   1. **Leitura do Arquivo de Metadados**:
   - Extrair cada campo do cabeçalho e validar.
   2. **Reprodução do *Fingerprint**:
   - Ler o mesmo arquivo original.
   - Executar AES‑CBC in‑memory com a chave e IV extraídos.
   - Extrair os últimos 16 bytes do ciphertext.
   3. **Comparação**:
   - Se o fingerprint recalculado for igual ao fingerprint armazenado no cabeçalho, o arquivo não foi alterado.
   - Caso contrário, sinalizar “Arquivo modificado ou corrompido”.