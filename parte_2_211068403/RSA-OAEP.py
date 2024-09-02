import os
import sys
import random
import math
import numpy
import hashlib
from MGF1mask import mgf1


# Função para calcular a potência no teste de primalidade de Miller-Rabin
def power(base, exponent, modulus):
    result = 1
    base = base % modulus
    while exponent > 0:
        if exponent & 1:
            result = (result * base) % modulus
        exponent = exponent >> 1
        base = (base * base) % modulus
    return result


# Teste de primalidade de Miller-Rabin
def miller_rabin_test(d, candidate):
    random_base = 2 + random.randint(1, candidate - 4)
    x = power(random_base, d, candidate)

    if x == 1 or x == candidate - 1:
        return True

    while d != candidate - 1:
        x = (x * x) % candidate
        d *= 2

        if x == 1:
            return False
        if x == candidate - 1:
            return True

    return False


# Verifica se um número é primo usando Miller-Rabin
def is_prime(number, iterations):
    if number <= 1 or number == 4:
        return False
    if number <= 3:
        return True

    d = number - 1
    while d % 2 == 0:
        d //= 2

    for _ in range(iterations):
        if not miller_rabin_test(d, number):
            return False

    return True


x_coefficient, y_coefficient = 0, 1


# Calcula o máximo divisor comum (MDC) estendido
def extended_gcd(a, b):
    global x_coefficient, y_coefficient

    if a == 0:
        x_coefficient = 0
        y_coefficient = 1
        return b

    gcd = extended_gcd(b % a, a)
    x_temp = x_coefficient
    y_temp = y_coefficient

    x_coefficient = y_temp - (b // a) * x_temp
    y_coefficient = x_temp

    return gcd


# Calcula o inverso modular de A módulo M
def modular_inverse(A, M):
    gcd = extended_gcd(A, M)
    if gcd != 1:
        return None
    else:
        return (x_coefficient % M + M) % M


# Lista de números primos já testados
tested_primes = []  
# Número de iterações do teste de primalidade de Miller-Rabin
prime_test_iterations = 1000  

# Gera dois números primos grandes de 1024 bits
while True:
    p_prime = os.urandom(128)
    if p_prime not in tested_primes:
        if is_prime(int.from_bytes(p_prime, sys.byteorder), prime_test_iterations):
            print(f"p_prime :\n{int.from_bytes(p_prime, sys.byteorder)}\n")
            while True:
                q_prime = os.urandom(128)
                if p_prime != q_prime:
                    if q_prime not in tested_primes:
                        if is_prime(int.from_bytes(q_prime, sys.byteorder), prime_test_iterations):
                            print(f"q_prime :\n{int.from_bytes(q_prime, sys.byteorder)}\n")
                            break
                        tested_primes.append(q_prime)
            break
        tested_primes.append(p_prime)

# Converte os números primos para inteiros
p_prime = int.from_bytes(p_prime, sys.byteorder)
q_prime = int.from_bytes(q_prime, sys.byteorder)

# Módulo RSA
rsa_modulus_n = p_prime * q_prime  

print(f"rsa_modulus_n :\n{rsa_modulus_n}\n")

p_minus_1 = p_prime - 1
q_minus_1 = q_prime - 1

# Mínimo múltiplo comum de (p-1) e (q-1)
lcm_phi_n = numpy.lcm(p_minus_1, q_minus_1)  

found_coprime = False

# Encontrando um 'e' que seja coprimo com lcm_phi_n
for e_public_exponent in range(65537, lcm_phi_n):
    if math.gcd(e_public_exponent, lcm_phi_n) == 1:
        found_coprime = True
        break

# Caso não encontre, tenta valores menores
if not found_coprime:
    for e_public_exponent in range(2, 65537, -1):
        if math.gcd(e_public_exponent, lcm_phi_n) == 1:
            found_coprime = True
            break

print(f'e_public_exponent :\n{e_public_exponent}\n')

# Inverso modular de e
d_private_exponent = modular_inverse(e_public_exponent, lcm_phi_n)  

print(f'd_private_exponent :\n{d_private_exponent}\n')


# Gera a string de padding para OAEP
def generate_padding_string(k_length, message_length, hash_length):
    padding_length = k_length - message_length - 2 * hash_length - 2
    return b'\x00' * padding_length


# OAEP e RSA combinados
k_length = math.ceil(rsa_modulus_n.bit_length() / 8)
print(f'O tamanho em bytes do módulo RSA :\n{k_length}\n')
message = input('Message to be encrypted: ').encode()
message_length = len(message)
print(f'tamanho mensagem:\n{message_length}\n')

# Label para o hash do bloco de dados do OAEP
label = "atumalaca".encode()  

label_hash = hashlib.sha3_256(label).digest() 

hash_length = len(label_hash)

padding_string = generate_padding_string(k_length, message_length, hash_length) 

data_block = label_hash + padding_string + b'\x01' + message 

seed = os.urandom(hash_length)

data_block_mask = mgf1(seed, k_length - hash_length - 1)

masked_data_block = bytes([a ^ b for a, b in zip(data_block, data_block_mask)])

seed_mask = mgf1(masked_data_block, hash_length)

masked_seed = bytes([a ^ b for a, b in zip(seed, seed_mask)])

# Mensagem Codificada
encoded_message = b'\x00' + masked_seed + masked_data_block  

encoded_message_length = len(encoded_message)

# Transforma a mensagem codificada com OAEP em inteiro
integer_encoded_message = int.from_bytes(encoded_message, byteorder='big')  

ciphertext = pow(integer_encoded_message, e_public_exponent, rsa_modulus_n)

print(f'Texto cifrado:\n{ciphertext}\n')

decrypted_integer_message = pow(ciphertext, d_private_exponent, rsa_modulus_n)

# Transforma o inteiro decifrado em bytes
decrypted_message_bytes = decrypted_integer_message.to_bytes(encoded_message_length, byteorder='big')  

# Recuperando o hash com SHA3-256
label_hash = hashlib.sha3_256(label).digest()  

masked_seed = decrypted_message_bytes[1:hash_length + 1]
masked_data_block = decrypted_message_bytes[hash_length + 1:]

seed_mask = mgf1(masked_data_block, hash_length)

seed = bytes([a ^ b for a, b in zip(masked_seed, seed_mask)])

data_block_mask = mgf1(seed, k_length - hash_length - 1)

data_block = bytes([a ^ b for a, b in zip(masked_data_block, data_block_mask)])

label_hash_verify = data_block[:hash_length]

# Verifica se o Hash é o mesmo no bloco de dados após a decifração
if label_hash_verify != label_hash:
    print('ERRO')
    sys.exit(1)

remainder = data_block[hash_length:]

counter = 0

# Encontrando o byte 0x01
for byte in remainder:
    if byte == 1:
        counter += 1
        break
    counter += 1

# Recolhe a mensagem do restante do bloco de dados
message = remainder[counter:] 

print(f'message:\n {message.decode()}')