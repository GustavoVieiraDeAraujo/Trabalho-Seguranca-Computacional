import hashlib

def mgf1(seed, mask_len, hash_func=hashlib.sha3_256):
    # Inicializa a máscara como uma sequência de bytes vazia
    mask = b''  
    counter = 0 
    # Tamanho do hash (32 bytes para SHA3-256)
    hash_len = hash_func().digest_size  

    while len(mask) < mask_len:
        # Converte o contador para bytes (4 bytes, big-endian)
        counter_bytes = counter.to_bytes(4, 'big')  
        # Concatena a semente com o contador em bytes
        data = seed + counter_bytes  
        # Gera o hash SHA3-256 do valor concatenado
        hash_output = hash_func(data).digest()  
        mask += hash_output  
        counter += 1  

    return mask[:mask_len] 