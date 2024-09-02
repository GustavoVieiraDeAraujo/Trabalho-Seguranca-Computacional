from constantes import *

# -------------------------------------------------------------------------------------------------------
"""
Função para obter as matrizes 4x4 representando os estados de entrada a partir de um texto.

Parâmetros:
- texto: string com o texto a ser convertido.

Retorno:
- Lista de matrizes 4x4 representando os estados de entrada do texto.
"""
def obter_matrizes_do_texto(texto):
    matrizes_4x4 = []
    byte_array = bytearray(texto, 'utf-8')
    num_matrizes = len(byte_array) // 16

    for i in range(num_matrizes):
        matriz_4x4 = []
        for j in range(4):
            linha = []
            for k in range(4):
                linha.append(byte_array[i * 16 + j * 4 + k])
            matriz_4x4.append(linha)
        matrizes_4x4.append(matriz_4x4)

    return matrizes_4x4
# -------------------------------------------------------------------------------------------------------

# -------------------------------------------------------------------------------------------------------
"""
Função que executa um XOR bit a bit entre duas matrizes 4x4.

Parâmetros:
- matriz_texto: primeira matriz 4x4 para o XOR.
- matriz_chave: segunda matriz 4x4 para o XOR.

Retorno:
- Matriz 4x4 resultante do XOR bit a bit.
"""
def aplicar_xor_entre_matrizes(matriz_texto, matriz_chave):
    matriz_resultado = []
    for i in range(4):
        linha_resultado = []
        for j in range(4):
            linha_resultado.append(matriz_texto[i][j] ^ matriz_chave[i][j])
        matriz_resultado.append(linha_resultado)
    return matriz_resultado
# -------------------------------------------------------------------------------------------------------


# -------------------------------------------------------------------------------------------------------
"""
Função para realizar um XOR bit a bit entre duas palavras.

Parâmetros:
- palavra1: primeira palavra para o XOR.
- palavra2: segunda palavra para o XOR.

Retorno:
- Palavra resultante do XOR bit a bit.
"""
def xor_entre_palavras(palavra1, palavra2):
    palavra_resultado = []
    for i in range(4):
        palavra_resultado.append(int(palavra1[i]) ^ int(palavra2[i]))
    return palavra_resultado
# -------------------------------------------------------------------------------------------------------


# -------------------------------------------------------------------------------------------------------
"""
Função para realizar um XOR entre uma palavra e um valor inteiro.

Parâmetros:
- palavra: palavra para o XOR.
- valor_inteiro: valor inteiro para o XOR.

Retorno:
- Palavra resultante do XOR entre a palavra e o valor inteiro.
"""
def xor_palavra_com_valor_inteiro(palavra, valor_inteiro):
    palavra_resultado = []
    binario_valor = bin(valor_inteiro)
    s = ''
    for byte in palavra:
        binario_byte = bin(byte)[2:]
        while len(binario_byte) != 8:
            binario_byte = '0' + binario_byte
        s += binario_byte
    s = int(s, 2)
    resultado_xor = int(bin(s ^ int(binario_valor, 2)), 2)
    hexadecimal_resultado = hex(resultado_xor)[2:].zfill(8)
    
    for i in range(4):
        temp_hex = hexadecimal_resultado[i*2:2+i*2]
        palavra_resultado.append(int(temp_hex, 16))
    return palavra_resultado
# -------------------------------------------------------------------------------------------------------


# -------------------------------------------------------------------------------------------------------
"""
Função que gera um array com sub-chaves a partir de uma chave.

Parâmetros:
- chave: matriz 4x4 representando a chave original.

Retorno:
- Lista de matrizes 4x4 representando as sub-chaves.
"""
def gerar_subchaves(chave):
    subchaves = []
    palavras = []
    subchaves.append(chave)
    for i in range(4):
        palavras.append(chave[i])

    for i in range(4, 44):
        palavra_temp = palavras[i-1]
        palavra_anterior = palavras[i-4]

        if (i % 4 == 0):
            palavra_temp = substituir_bytes_chave(rotacionar_palavra(palavra_temp))
            palavra_temp = xor_palavra_com_valor_inteiro(palavra_temp, RCON[int(i / 4)])
        palavras.append(xor_entre_palavras(palavra_anterior, palavra_temp))
    
    for i in range(4, len(palavras), 4):
        subchaves.append([palavras[i], palavras[i+1], palavras[i+2], palavras[i+3]])
    return subchaves
# -------------------------------------------------------------------------------------------------------


# -------------------------------------------------------------------------------------------------------
"""
Função de rotação de palavras.

Parâmetros:
- palavra: lista de bytes representando uma palavra.

Retorno:
- Nova palavra com os bytes rotacionados para a esquerda.
"""
def rotacionar_palavra(palavra):
    return [palavra[1], palavra[2], palavra[3], palavra[0]]
# -------------------------------------------------------------------------------------------------------


# -------------------------------------------------------------------------------------------------------
"""
Função de substituição de palavra com base na S_BOX.

Parâmetros:
- palavra: lista de bytes representando uma palavra.

Retorno:
- Nova palavra com os valores substituídos conforme a S_BOX.
"""
def substituir_bytes_chave(palavra):
    palavra_substituida = []
    for byte in palavra:
        palavra_substituida.append(int(S_BOX[hex(byte)[2:4]], 16))
    return palavra_substituida
# -------------------------------------------------------------------------------------------------------


# -------------------------------------------------------------------------------------------------------
"""
Função de substituição de matriz com base na S_BOX.

Parâmetros:
- matriz: matriz 4x4 a ser substituída.

Retorno:
- Nova matriz com os valores substituídos conforme a S_BOX.
"""
def substituir_bytes_matriz(matriz):
    matriz_substituida = []
    for i in range(4):
        coluna_substituida = []
        for j in range(4):
            coluna_substituida.append(int(S_BOX[hex(matriz[i][j])[2:4]], 16))
        matriz_substituida.append(coluna_substituida)
    return matriz_substituida
# -------------------------------------------------------------------------------------------------------


# -------------------------------------------------------------------------------------------------------
"""
Função de permutação das linhas de uma matriz 4x4.

Parâmetros:
- matriz: matriz 4x4 a ser permutada.

Retorno:
- Nova matriz com as linhas permutadas conforme o algoritmo.
"""
def permutar_linhas_matriz(matriz):
    matriz_permutada = []

    matriz_permutada.append([matriz[0][0], matriz[1][1], matriz[2][2], matriz[3][3]])
    matriz_permutada.append([matriz[1][0], matriz[2][1], matriz[3][2], matriz[0][3]])
    matriz_permutada.append([matriz[2][0], matriz[3][1], matriz[0][2], matriz[1][3]])
    matriz_permutada.append([matriz[3][0], matriz[0][1], matriz[1][2], matriz[2][3]])

    return matriz_permutada
# -------------------------------------------------------------------------------------------------------


# -------------------------------------------------------------------------------------------------------
"""
Função de multiplicação no campo de Galois.

Parâmetros:
- a: primeiro número a ser multiplicado.
- b: segundo número a ser multiplicado.

Retorno:
- Resultado da multiplicação no campo de Galois entre os dois números.
"""
def multiplicar_no_campo_galois(a, b):
    if b == 1:
        return a
    temp = (a << 1) & 0xff
    if b == 2:
        return temp if a < 128 else temp ^ 0x1b
    if b == 3:
        return multiplicar_no_campo_galois(a, 2) ^ a
# -------------------------------------------------------------------------------------------------------


# -------------------------------------------------------------------------------------------------------
"""
Função de embaralhamento de colunas de uma matriz 4x4.

Parâmetros:
- matriz: matriz 4x4 a ser embaralhada.

Retorno:
- Nova matriz com colunas embaralhadas.
"""
def embaralhar_colunas(matriz):
    matriz_embaralhada = [[], [], [], []]
    
    for i in range(4):
        matriz_embaralhada[i].append(
            multiplicar_no_campo_galois(matriz[i][0], 2) ^
            multiplicar_no_campo_galois(matriz[i][1], 3) ^
            multiplicar_no_campo_galois(matriz[i][2], 1) ^
            multiplicar_no_campo_galois(matriz[i][3], 1)
        )
        matriz_embaralhada[i].append(
            multiplicar_no_campo_galois(matriz[i][1], 2) ^
            multiplicar_no_campo_galois(matriz[i][2], 3) ^
            multiplicar_no_campo_galois(matriz[i][3], 1) ^
            multiplicar_no_campo_galois(matriz[i][0], 1)
        )
        matriz_embaralhada[i].append(
            multiplicar_no_campo_galois(matriz[i][2], 2) ^
            multiplicar_no_campo_galois(matriz[i][3], 3) ^
            multiplicar_no_campo_galois(matriz[i][0], 1) ^
            multiplicar_no_campo_galois(matriz[i][1], 1)
        )
        matriz_embaralhada[i].append(
            multiplicar_no_campo_galois(matriz[i][3], 2) ^
            multiplicar_no_campo_galois(matriz[i][0], 3) ^
            multiplicar_no_campo_galois(matriz[i][1], 1) ^
            multiplicar_no_campo_galois(matriz[i][2], 1)
        )

    return matriz_embaralhada
# -------------------------------------------------------------------------------------------------------


# -------------------------------------------------------------------------------------------------------
"""
Função de criptografia usando AES.

Parâmetros:
- matriz_texto: matriz 4x4 do texto a ser criptografado.
- subchaves: lista de matrizes 4x4 representando as sub-chaves.

Retorno:
- Matriz 4x4 criptografada.
"""
def criptografar_texto(matriz_texto, subchaves, numero_rodadas):
    estado_atual = aplicar_xor_entre_matrizes(matriz_texto, subchaves[0])
    for i in range(1, len(subchaves)):
        estado_atual = substituir_bytes_matriz(estado_atual)
        estado_atual = permutar_linhas_matriz(estado_atual)
        if i != numero_rodadas:
            estado_atual = embaralhar_colunas(estado_atual)
        estado_atual = aplicar_xor_entre_matrizes(estado_atual, subchaves[i])
    return estado_atual
# -------------------------------------------------------------------------------------------------------


# -------------------------------------------------------------------------------------------------------
"""
Função para converter uma lista de matrizes 4x4 em texto.

Parâmetros:
- matrizes_4x4: lista de matrizes 4x4 a serem convertidas.

Retorno:
- String representando o texto correspondente.
"""
def converter_para_texto(matrizes_4x4):
    texto = ""
    for matriz in matrizes_4x4:
        for i in range(4):
            for j in range(4):
                texto += chr(matriz[i][j])
    return texto
# -------------------------------------------------------------------------------------------------------

# -------------------------------------------------------------------------------------------------------
"""
Função de conversão de uma lista de bytes para uma string de caracteres.

Parâmetros:
- byte_list: lista de bytes a ser convertida.

Retorno:
- String resultante da conversão dos bytes.
"""
def converter_lista_para_texto(byte_list):
    return ''.join(chr(byte) for byte in byte_list)
# -------------------------------------------------------------------------------------------------------


# -------------------------------------------------------------------------------------------------------
"""
Função de conversão de uma string de caracteres para uma lista de bytes.

Parâmetros:
- texto: string a ser convertida.

Retorno:
- Lista de bytes resultante da conversão dos caracteres.
"""
def converter_texto_para_lista(texto):
    return [ord(char) for char in texto]
# -------------------------------------------------------------------------------------------------------


# -------------------------------------------------------------------------------------------------------
"""
Função de incremento de um contador de 128 bits (16 bytes) representado como uma lista de bytes.

Parâmetros:
- contador: lista de bytes representando o contador.

Retorno:
- Lista de bytes com o contador incrementado.
"""
def incrementar_contador(contador):
    for i in reversed(range(len(contador))):
        contador[i] += 1
        if contador[i] != 0:
            break
    return contador
# -------------------------------------------------------------------------------------------------------


# -------------------------------------------------------------------------------------------------------
"""
Função de criptografia de texto no modo CTR.

Parâmetros:
- texto_original: texto a ser criptografado.
- chave: chave usada para criptografia.
- contador_inicial: valor inicial do contador em formato hexadecimal.

Retorno:
- Lista de bytes do texto criptografado.
"""
def criptografar_texto_ctr(texto_original, chave, contador_inicial, numero_rodadas):
    bloco_tamanho = 16
    texto_criptografado = []
    subchaves_geradas = gerar_subchaves(chave)
    contador = [int(contador_inicial[i:i+2], 16) for i in range(0, len(contador_inicial), 2)]
    num_blocos = len(texto_original) // bloco_tamanho + (1 if len(texto_original) % bloco_tamanho != 0 else 0)
    
    for i in range(num_blocos):
        contador_bytes = bytearray(contador)
        while len(contador_bytes) < bloco_tamanho:
            contador_bytes.append(0)

        matriz_contador = obter_matrizes_do_texto(converter_lista_para_texto(contador_bytes))[0]
        bloco_criptografado = criptografar_texto(matriz_contador, subchaves_geradas, numero_rodadas)
        bloco_criptografado = [item for sublist in bloco_criptografado for item in sublist] 
        
        start = i * bloco_tamanho
        end = start + bloco_tamanho
        bloco_texto = texto_original[start:end]
        bloco_texto_bytes = converter_texto_para_lista(bloco_texto)
        bloco_resultado = [b ^ c for b, c in zip(bloco_texto_bytes, bloco_criptografado)]
        texto_criptografado.extend(bloco_resultado)
        contador = incrementar_contador(contador)
    return texto_criptografado
# -------------------------------------------------------------------------------------------------------


# -------------------------------------------------------------------------------------------------------
"""
Função de decodificação de texto no modo CTR.

Parâmetros:
- texto_criptografado: texto criptografado a ser decifrado, em formato de lista de bytes.
- chave: chave usada para criptografia.
- contador_inicial: valor inicial do contador em formato hexadecimal.
- numero_rodadas: número de rodadas usadas na criptografia.

Retorno:
- Texto decifrado em formato de string.
"""
def decifrar_texto_ctr(texto_criptografado, chave, contador_inicial, numero_rodadas):
    bloco_tamanho = 16
    texto_decifrado = []
    subchaves_geradas = gerar_subchaves(chave)
    contador = [int(contador_inicial[i:i+2], 16) for i in range(0, len(contador_inicial), 2)]
    num_blocos = len(texto_criptografado) // bloco_tamanho + (1 if len(texto_criptografado) % bloco_tamanho != 0 else 0)
    
    for i in range(num_blocos):
        contador_bytes = bytearray(contador)
        while len(contador_bytes) < bloco_tamanho:
            contador_bytes.append(0)

        matriz_contador = obter_matrizes_do_texto(converter_lista_para_texto(contador_bytes))[0]
        bloco_criptografado = criptografar_texto(matriz_contador, subchaves_geradas, numero_rodadas)
        bloco_criptografado = [item for sublist in bloco_criptografado for item in sublist]
        
        start = i * bloco_tamanho
        end = start + bloco_tamanho
        bloco_criptografado_atual = texto_criptografado[start:end]
        bloco_resultado = [b ^ c for b, c in zip(bloco_criptografado_atual, bloco_criptografado)]
        texto_decifrado.extend(bloco_resultado)
        contador = incrementar_contador(contador)
    
    return converter_lista_para_texto(texto_decifrado).rstrip('\x00')
# -------------------------------------------------------------------------------------------------------