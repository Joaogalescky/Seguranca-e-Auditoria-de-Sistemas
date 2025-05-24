# Criptografia Simétrica

Programa de criptografia simétrica utilizando a criptografia AES (_Advanced Encryption Standard_) no modo CBC (_Cipher Block Chaining_) em um cabeçalho de 32 bytes com metadados sobre o arquivo cifrado.

## Instruções
1. **Cabeçalho do Arquivo Cifrado (32 bytes)**: o início do arquivo criptografado deve conter um cabeçalho com os seguintes campos:

    | Campo| Tamanho (bytes) | Descrição
    |:--------|:--------:|:--------
    | Identificador | 2 | Deve conter uma sequência fixa, ex: ==b'ED'==, para indicar um arquivo cifrado
    | Versão | 1 | Versão do formato de cabeçalho (ex: ==1==)
    | Algoritmo | 1 | ==1== para AES (reservado para futuras extensões com outros algoritmos)
    | Modo | 1 | ==1== para modo CBC
    | IV | 16 | Vetor de inicialização (gerado aleatoriamente na criptografia)
    | Reversado | 11 | Reservado para uso futuro (preencher com ==0x00==)

2. **Etapas do Programa (Encrypt)**:
   - Solicitar ao usuário o caminho de um arquivo para criptografar.
   - Gerar uma chave de 256 bits (pode ser fixa ou pedida ao usuário).
   - Gerar o IV (Initialization Vector) aleatoriamente.
   - Criar o cabeçalho conforme especificado.
   - Criptografar o conteúdo do arquivo usando AES-CBC.
   - Escrever o cabeçalho + dados criptografados em um novo arquivo.
   - Salvar o arquivo concatenando ".enc" no final do nome do arquivo.

3. **Descriptografia (Decrypt)**:
   - Ler o cabeçalho do arquivo cifrado.
   - Verificar se o identificador, versão e algoritmo estão corretos (validação).
   - Extrair o IV.
   - Usar a chave (a mesma da criptografia) para decifrar o conteúdo.
   - Salvar o arquivo original.