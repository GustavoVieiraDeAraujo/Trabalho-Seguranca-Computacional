import numpy as np
from constantes import *
from Crypto.Cipher import AES
from AES_cifracao import decifrar_texto_ctr

# -------------------------------------------------------------------------------------------------------
"""
Função para obter as matrizes de estado de entrada de um texto.

Parâmetros:
- texto: string a ser convertida em matrizes de estado.

Retorno:
- Lista de matrizes 4x4 representando os estados de entrada.
"""
def obter_matrizes_estado(texto):
    matrizes_estado = []
    bytes_texto = bytearray(texto, 'utf-8')
    num_matrizes = len(bytes_texto) // 16
    for i in range(num_matrizes):
        matriz_estado = [[bytes_texto[i * 16 + j * 4 + k] for k in range(4)] for j in range(4)]
        matrizes_estado.append(matriz_estado)
    return matrizes_estado
# -------------------------------------------------------------------------------------------------------


# -------------------------------------------------------------------------------------------------------
"""
Função para executar um XOR bit a bit entre duas matrizes 4x4.

Parâmetros:
- matriz_texto: matriz 4x4 do texto.
- matriz_chave: matriz 4x4 da chave.

Retorno:
- Matriz 4x4 resultante do XOR.
"""
def aplicar_xor_chave_rodada(matriz_texto, matriz_chave):
    return [[matriz_texto[i][j] ^ matriz_chave[i][j] for j in range(4)] for i in range(4)]
# -------------------------------------------------------------------------------------------------------


# -------------------------------------------------------------------------------------------------------
"""
Função para realizar XOR entre duas palavras de 4 bytes.

Parâmetros:
- palavra1: lista de 4 inteiros representando a primeira palavra.
- palavra2: lista de 4 inteiros representando a segunda palavra.

Retorno:
- Lista de 4 inteiros representando o resultado do XOR.
"""
def xor_palavras(palavra1, palavra2):
    return [palavra1[i] ^ palavra2[i] for i in range(4)]
# -------------------------------------------------------------------------------------------------------


# -------------------------------------------------------------------------------------------------------
"""
Função para realizar XOR entre uma palavra de 4 bytes e um inteiro.

Parâmetros:
- palavra: lista de 4 inteiros representando a palavra.
- inteiro: inteiro para realizar o XOR.

Retorno:
- Lista de 4 inteiros representando o resultado do XOR.
"""
def xor_palavra_com_inteiro(palavra, inteiro):
    binario_inteiro = bin(inteiro)[2:]
    bin_palavra = ''.join([bin(byte)[2:].zfill(8) for byte in palavra])
    xor_binario = int(bin_palavra, 2) ^ int(binario_inteiro, 2)
    hex_xor = hex(xor_binario)[2:].zfill(8)
    return [int(hex_xor[i*2:2+i*2], 16) for i in range(4)]
# -------------------------------------------------------------------------------------------------------


# -------------------------------------------------------------------------------------------------------
"""
Função para gerar subchaves expandindo a chave inicial.

Parâmetros:
- chave: string representando a chave inicial.

Retorno:
- Lista de 11 matrizes 4x4 representando as subchaves.
"""
def expandir_chave(chave):
    subchaves = []
    palavras = []
    matriz_chave_inicial = obter_matrizes_estado(chave)[0]
    subchaves.append(matriz_chave_inicial)
    palavras.extend(matriz_chave_inicial)
    for i in range(4, 44):
        palavra_temp = palavras[i-1]
        if i % 4 == 0:
            palavra_temp = xor_palavra_com_inteiro(substituir_bytes_palavra(rotacionar_bytes_palavra(palavra_temp)), RCON[i // 4])
        palavras.append(xor_palavras(palavras[i-4], palavra_temp))

    for i in range(4, len(palavras), 4):
        subchaves.append([palavras[i], palavras[i+1], palavras[i+2], palavras[i+3]])
    return subchaves
# -------------------------------------------------------------------------------------------------------


# -------------------------------------------------------------------------------------------------------
"""
Função para rotacionar os bytes de uma palavra para a esquerda.

Parâmetros:
- palavra: lista de 4 inteiros representando a palavra.

Retorno:
- Lista de 4 inteiros com os bytes rotacionados.
"""
def rotacionar_bytes_palavra(palavra):
    return palavra[1:] + palavra[:1]
# -------------------------------------------------------------------------------------------------------


# -------------------------------------------------------------------------------------------------------
"""
Função para substituir os bytes de uma palavra usando a S_BOX.

Parâmetros:
- palavra: lista de 4 inteiros representando a palavra.

Retorno:
- Lista de 4 inteiros com os bytes substituídos.
"""
def substituir_bytes_palavra(palavra):
    return [int(S_BOX[hex(byte)[2:4]], 16) for byte in palavra]
# -------------------------------------------------------------------------------------------------------


# -------------------------------------------------------------------------------------------------------
"""
Função para substituir os bytes de uma matriz usando a INVERTED_S_BOX.

Parâmetros:
- matriz: matriz 4x4 a ser substituída.

Retorno:
- Matriz 4x4 com os bytes substituídos.
"""
def substituir_bytes_invertidos(matriz):
    return [[int(INVERTED_S_BOX[hex(matriz[i][j])[2:4]], 16) for j in range(4)] for i in range(4)]
# -------------------------------------------------------------------------------------------------------


# -------------------------------------------------------------------------------------------------------
"""
Função para permutar as linhas de uma matriz.

Parâmetros:
- matriz: matriz 4x4 a ser permutada.

Retorno:
- Matriz 4x4 com as linhas permutadas.
"""
def permutar_linhas_invertidas(matriz):
    return [
        [matriz[0][0], matriz[3][1], matriz[2][2], matriz[1][3]],
        [matriz[1][0], matriz[0][1], matriz[3][2], matriz[2][3]],
        [matriz[2][0], matriz[1][1], matriz[0][2], matriz[3][3]],
        [matriz[3][0], matriz[2][1], matriz[1][2], matriz[0][3]]
    ]
# -------------------------------------------------------------------------------------------------------


# -------------------------------------------------------------------------------------------------------
"""
Função para multiplicar dois números no campo de Galois.

Parâmetros:
- a: inteiro representando o primeiro número.
- b: inteiro representando o segundo número.

Retorno:
- Resultado da multiplicação no campo de Galois.
"""
def multiplicar_galois(a, b):
    if b == 1:
        return a
    resultado_temp = (a << 1) & 0xff
    if b == 2:
        return resultado_temp if a < 128 else resultado_temp ^ 0x1b
    if b == 3:
        return multiplicar_galois(a, 2) ^ a

def multiplicar_galois_09(a): return multiplicar_galois(multiplicar_galois(multiplicar_galois(a, 2), 2), 2) ^ a
def multiplicar_galois_11(a): return multiplicar_galois((multiplicar_galois(multiplicar_galois(a, 2), 2) ^ a), 2) ^ a
def multiplicar_galois_13(a): return multiplicar_galois(multiplicar_galois((multiplicar_galois(a, 2) ^ a), 2), 2) ^ a
def multiplicar_galois_14(a): return multiplicar_galois((multiplicar_galois((multiplicar_galois(a, 2) ^ a), 2) ^ a), 2)
# -------------------------------------------------------------------------------------------------------


# -------------------------------------------------------------------------------------------------------
"""
Função para embaralhar as colunas de uma matriz.

Parâmetros:
- matriz: matriz 4x4 a ser embaralhada.

Retorno:
- Matriz 4x4 com as colunas embaralhadas.
"""
def embaralhar_colunas_invertidas(matriz):
    nova_matriz = [[] for _ in range(4)]
    for i in range(4):
        nova_matriz[i].append(multiplicar_galois_14(matriz[i][0]) ^ multiplicar_galois_11(matriz[i][1]) ^ multiplicar_galois_13(matriz[i][2]) ^ multiplicar_galois_09(matriz[i][3]))
        nova_matriz[i].append(multiplicar_galois_09(matriz[i][0]) ^ multiplicar_galois_14(matriz[i][1]) ^ multiplicar_galois_11(matriz[i][2]) ^ multiplicar_galois_13(matriz[i][3]))
        nova_matriz[i].append(multiplicar_galois_13(matriz[i][0]) ^ multiplicar_galois_09(matriz[i][1]) ^ multiplicar_galois_14(matriz[i][2]) ^ multiplicar_galois_11(matriz[i][3]))
        nova_matriz[i].append(multiplicar_galois_11(matriz[i][0]) ^ multiplicar_galois_13(matriz[i][1]) ^ multiplicar_galois_09(matriz[i][2]) ^ multiplicar_galois_14(matriz[i][3]))
    return nova_matriz
# -------------------------------------------------------------------------------------------------------


# -------------------------------------------------------------------------------------------------------
"""
Função para decifrar uma matriz 4x4.

Parâmetros:
- matriz_texto: matriz 4x4 do texto cifrado.
- subchaves: lista de subchaves a serem utilizadas na decifração.

Retorno:
- Matriz 4x4 decifrada.
"""
def decifrar_matriz(matriz_texto, subchaves):
    estado = aplicar_xor_chave_rodada(matriz_texto, subchaves[-1])
    for i in range(len(subchaves)-1, 0, -1):
        estado = permutar_linhas_invertidas(estado)
        estado = substituir_bytes_invertidos(estado)
        estado = aplicar_xor_chave_rodada(estado, subchaves[i-1])
        if i != 1:
            estado = embaralhar_colunas_invertidas(estado)
    return estado
# -------------------------------------------------------------------------------------------------------