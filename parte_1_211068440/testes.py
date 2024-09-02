import numpy as np
from AES_cifracao import *
from AES_decifracao import *
from Crypto.Cipher import AES
from Crypto.Util import Counter

print()
print("--------------------------------------------------CIFRAÇÃO----------------------------------------------------")
print()
# -------------------------------------------------------------------------------------------------------
"""
Teste de cifração da implementação manual (ECB)

Observação: se mudar as rodadas aqui não vai obter com o resultado da biblioteca.
"""

numero_rodadas = 10
texto_original = 'abcdefghijklmnop'
chave_original = [[23, 40, 231, 72], [52, 126, 128, 63], [11, 222, 53, 168], [6, 127, 45, 99]]

subchaves_geradas = gerar_subchaves(chave_original)
matrizes_texto = obter_matrizes_do_texto(texto_original)

resultados_criptografia = []
for matriz in matrizes_texto:
    resultados_criptografia.append(criptografar_texto(matriz, subchaves_geradas, numero_rodadas))

print("Resultado da criptografia no modo ECB (manual):")
print(resultados_criptografia[0])
print()
# -------------------------------------------------------------------------------------------------------


# -------------------------------------------------------------------------------------------------------
"""
Teste de cifração usando biblioteca (ECB)

Observação: por padrão a biblioteca usa 10 rodadas.
"""

texto_original = 'abcdefghijklmnop'
chave_bytes = bytes([23, 40, 231, 72, 52, 126, 128, 63, 11, 222, 53, 168, 6, 127, 45, 99])

texto_bytes = texto_original.encode('utf-8')
cipher = AES.new(chave_bytes, AES.MODE_ECB)
bloco_encriptado = cipher.encrypt(texto_bytes)
matriz_encriptada = np.array(list(bloco_encriptado)).reshape(-1, 4).tolist()

print("Resultado da criptografia no modo ECB (manual):")
print(matriz_encriptada)
print()

# -------------------------------------------------------------------------------------------------------


# -------------------------------------------------------------------------------------------------------
"""
Teste de cifração da implementação manual (CTR)

Observação: se mudar as rodadas aqui não vai obter com o resultado da biblioteca.
"""

numero_rodadas = 10
texto_original = 'abcdefghijklmnop'
contador_inicial = '0000000000000000'
chave_original = [[23, 40, 231, 72], [52, 126, 128, 63], [11, 222, 53, 168], [6, 127, 45, 99]]

texto_criptografado_manual = criptografar_texto_ctr(texto_original, chave_original, contador_inicial, numero_rodadas)
print("Resultado da criptografia no modo CTR (biblioteca):")
print(np.array(texto_criptografado_manual).reshape(-1, 4).tolist())
print()
# -------------------------------------------------------------------------------------------------------


# -------------------------------------------------------------------------------------------------------
"""
Teste de cifração usando biblioteca (CTR)

Observação: por padrão a biblioteca usa 10 rodadas.
"""

texto_original = 'abcdefghijklmnop'
chave = bytes([23, 40, 231, 72, 52, 126, 128, 63, 11, 222, 53, 168, 6, 127, 45, 99])
contador_inicial = '0000000000000000'

cipher = AES.new(chave, AES.MODE_CTR, counter=Counter.new(128, initial_value=int(contador_inicial, 16)))
texto_original_bytes = texto_original.encode('utf-8')
texto_criptografado_biblioteca = cipher.encrypt(texto_original_bytes)

print("Resultado da criptografia no modo CTR (biblioteca):")
texto_criptografado_biblioteca_matriz = np.frombuffer(texto_criptografado_biblioteca, dtype=np.uint8).reshape(-1, 4).tolist()
print(texto_criptografado_biblioteca_matriz)
print()
print("------------------------------------------------DECIFRAÇÃO----------------------------------------------------")
print()
# -------------------------------------------------------------------------------------------------------


# -------------------------------------------------------------------------------------------------------
"""
Teste de decifração da implementação manual (ECB)
"""

matriz_encriptada = [[[91, 177, 3, 134], [83, 221, 167, 17], [139, 41, 112, 136], [9, 217, 36, 46]]]
chave_inicial = "segurança computacional"
subchaves = expandir_chave(chave_inicial)
resultados = [decifrar_matriz(matriz, subchaves) for matriz in matriz_encriptada]
print("Resultado da descriptografia no modo ECB (manual):")
print(resultados[0])
print()
# -------------------------------------------------------------------------------------------------------


# -------------------------------------------------------------------------------------------------------
"""
Teste de decifração usando biblioteca (ECB)
"""

# Definindo a chave e a matriz encriptada
chave_bytes = "segurança computacional".encode('utf-8')[:16]
matriz = [[[91, 177, 3, 134], [83, 221, 167, 17], [139, 41, 112, 136], [9, 217, 36, 46]]]
bloco_encriptado = bytes([matriz[0][i][j] for i in range(4) for j in range(4)])
cipher = AES.new(chave_bytes, AES.MODE_ECB)
bloco_decifrado = cipher.decrypt(bloco_encriptado)
matriz_decifrada = np.array(list(bloco_decifrado)).reshape(4, 4).tolist()
print("Resultado da descriptografia no modo ECB (biblioteca):")
print(matriz_decifrada)
print()
# -------------------------------------------------------------------------------------------------------


# -------------------------------------------------------------------------------------------------------
"""
Teste de decifração da implementação manual (CTR)
"""

numero_rodadas = 10
contador_inicial = '0000000000000000'
texto_criptografado = [94, 33, 50, 210, 41, 57, 144, 146, 94, 148, 140, 51, 47, 144, 120, 233]
chave_original = [[23, 40, 231, 72], [52, 126, 128, 63], [11, 222, 53, 168], [6, 127, 45, 99]]

texto_decifrado = decifrar_texto_ctr(texto_criptografado, chave_original, contador_inicial, numero_rodadas)
print("Resultado da descriptografia no modo CTR (manual):")
print(texto_decifrado)
print()
# -------------------------------------------------------------------------------------------------------


# -------------------------------------------------------------------------------------------------------
"""
Teste de decifração usando biblioteca (CTR)
"""

contador_inicial = '0000000000000000'
texto_criptografado = [94, 33, 50, 210, 41, 57, 144, 146, 94, 148, 140, 51, 47, 144, 120, 233]
chave_original = [[23, 40, 231, 72], [52, 126, 128, 63], [11, 222, 53, 168], [6, 127, 45, 99]]

contador_inicial_bytes = bytes.fromhex(contador_inicial)
contador_inicial_bytes = contador_inicial_bytes.ljust(16, b'\x00')
chave_original_bytes = bytes([item for sublista in chave_original for item in sublista])
texto_criptografado_bytes = bytes(texto_criptografado)
cifrador = AES.new(chave_original_bytes, AES.MODE_CTR, nonce=b'', initial_value=contador_inicial_bytes)
texto_descriptografado_bytes = cifrador.decrypt(texto_criptografado_bytes)
texto_descriptografado = texto_descriptografado_bytes.decode('utf-8')
print("Resultado da descriptografia no modo CTR (biblioteca):")
print(texto_descriptografado)
# -------------------------------------------------------------------------------------------------------
print()