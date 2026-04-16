# DES Algorithm 
'''
KeySchedule 
M = P(M)
M = L0|R0
16 rodadas:
    L(r) = R(r-1)
    R(r) = f(K(r), R(r-1)) XOR L(r-1)
C = P^-1 (L(16) | R(16))
'''

# ==========================================
# 1. PERMUTAÇÕES INICIAIS E FINAIS DO BLOCO
# ==========================================

# Permutação Inicial (IP)
IP = [
    58, 50, 42, 34, 26, 18, 10, 2,
    60, 52, 44, 36, 28, 20, 12, 4,
    62, 54, 46, 38, 30, 22, 14, 6,
    64, 56, 48, 40, 32, 24, 16, 8,
    57, 49, 41, 33, 25, 17, 9,  1,
    59, 51, 43, 35, 27, 19, 11, 3,
    61, 53, 45, 37, 29, 21, 13, 5,
    63, 55, 47, 39, 31, 23, 15, 7
]

# Permutação Inversa / Final (IP^-1)
IP_INV = [
    40, 8, 48, 16, 56, 24, 64, 32,
    39, 7, 47, 15, 55, 23, 63, 31,
    38, 6, 46, 14, 54, 22, 62, 30,
    37, 5, 45, 13, 53, 21, 61, 29,
    36, 4, 44, 12, 52, 20, 60, 28,
    35, 3, 43, 11, 51, 19, 59, 27,
    34, 2, 42, 10, 50, 18, 58, 26,
    33, 1, 41, 9,  49, 17, 57, 25
]

# ==========================================
# 2. GERAÇÃO DE CHAVES (KEY SCHEDULE)
# ==========================================

# Permuted Choice 1 (PC-1) - Reduz chave de 64 para 56 bits (reordena bits paridade)
PC_1 = [
    57, 49, 41, 33, 25, 17, 9,
    1,  58, 50, 42, 34, 26, 18,
    10, 2,  59, 51, 43, 35, 27,
    19, 11, 3,  60, 52, 44, 36,
    63, 55, 47, 39, 31, 23, 15,
    7,  62, 54, 46, 38, 30, 22,
    14, 6,  61, 53, 45, 37, 29,
    21, 13, 5,  28, 20, 12, 4
]

# Permuted Choice 2 (PC-2) - Reduz chave de 56 para 48 bits na subchave da rodada 
PC_2 = [
    14, 17, 11, 24, 1,  5,
    3,  28, 15, 6,  21, 10,
    23, 19, 12, 4,  26, 8,
    16, 7,  27, 20, 13, 2,
    41, 52, 31, 37, 47, 55,
    30, 40, 51, 45, 33, 48,
    44, 49, 39, 56, 34, 53,
    46, 42, 50, 36, 29, 32
]

# ==========================================
# 3. FUNÇÃO FEISTEL (RODADAS INTERNAS)
# ==========================================

# Tabela de Expansão (E) - Expande de 32 para 48 bits
E = [
    32, 1,  2,  3,  4,  5,
    4,  5,  6,  7,  8,  9,
    8,  9,  10, 11, 12, 13,
    12, 13, 14, 15, 16, 17,
    16, 17, 18, 19, 20, 21,
    20, 21, 22, 23, 24, 25,
    24, 25, 26, 27, 28, 29,
    28, 29, 30, 31, 32, 1
]

# Permutação Interna (P) - Permuta os 32 bits de saída das S-Boxes
P = [

    16, 7,  20, 21,
    29, 12, 28, 17,
    1,  15, 23, 26,
    5,  18, 31, 10,
    2,  8,  24, 14,
    32, 27, 3,  9,
    19, 13, 30, 6,
    22, 11, 4,  25
]

# ==========================================
# 4. TABELAS DE SUBSTITUIÇÃO (S-BOXES)
# ==========================================

S_BOXES = [
    # S-Box 1 (S1)
    [
        [14, 4,  13, 1,  2,  15, 11, 8,  3,  10, 6,  12, 5,  9,  0,  7],
        [0,  15, 7,  4,  14, 2,  13, 1,  10, 6,  12, 11, 9,  5,  3,  8],
        [4,  1,  14, 8,  13, 6,  2,  11, 15, 12, 9,  7,  3,  10, 5,  0],
        [15, 12, 8,  2,  4,  9,  1,  7,  5,  11, 3,  14, 10, 0,  6,  13]
    ],
    # S-Box 2 (S2)
    [
        [15, 1,  8,  14, 6,  11, 3,  4,  9,  7,  2,  13, 12, 0,  5,  10],
        [3,  13, 4,  7,  15, 2,  8,  14, 12, 0,  1,  10, 6,  9,  11, 5],
        [0,  14, 7,  11, 10, 4,  13, 1,  5,  8,  12, 6,  9,  3,  2,  15],
        [13, 8,  10, 1,  3,  15, 4,  2,  11, 6,  7,  12, 0,  5,  14, 9]
    ],
    # S-Box 3 (S3)
    [
        [10, 0,  9,  14, 6,  3,  15, 5,  1,  13, 12, 7,  11, 4,  2,  8],
        [13, 7,  0,  9,  3,  4,  6,  10, 2,  8,  5,  14, 12, 11, 15, 1],
        [13, 6,  4,  9,  8,  15, 3,  0,  11, 1,  2,  12, 5,  10, 14, 7],
        [1,  10, 13, 0,  6,  9,  8,  7,  4,  15, 14, 3,  11, 5,  2,  12]
    ],
    # S-Box 4 (S4)
    [
        [7,  13, 14, 3,  0,  6,  9,  10, 1,  2,  8,  5,  11, 12, 4,  15],
        [13, 8,  11, 5,  6,  15, 0,  3,  4,  7,  2,  12, 1,  10, 14, 9],
        [10, 6,  9,  0,  12, 11, 7,  13, 15, 1,  3,  14, 5,  2,  8,  4],
        [3,  15, 0,  6,  10, 1,  13, 8,  9,  4,  5,  11, 12, 7,  2,  14]
    ],
    # S-Box 5 (S5)
    [
        [2,  12, 4,  1,  7,  10, 11, 6,  8,  5,  3,  15, 13, 0,  14, 9],
        [14, 11, 2,  12, 4,  7,  13, 1,  5,  0,  15, 10, 3,  9,  8,  6],
        [4,  2,  1,  11, 10, 13, 7,  8,  15, 9,  12, 5,  6,  3,  0,  14],
        [11, 8,  12, 7,  1,  14, 2,  13, 6,  15, 0,  9,  10, 4,  5,  3]
    ],
    # S-Box 6 (S6)
    [
        [12, 1,  10, 15, 9,  2,  6,  8,  0,  13, 3,  4,  14, 7,  5,  11],
        [10, 15, 4,  2,  7,  12, 9,  5,  6,  1,  13, 14, 0,  11, 3,  8],
        [9,  14, 15, 5,  2,  8,  12, 3,  7,  0,  4,  10, 1,  13, 11, 6],
        [4,  3,  2,  12, 9,  5,  15, 10, 11, 14, 1,  7,  6,  0,  8,  13]
    ],
    # S-Box 7 (S7)
    [
        [4,  11, 2,  14, 15, 0,  8,  13, 3,  12, 9,  7,  5,  10, 6,  1],
        [13, 0,  11, 7,  4,  9,  1,  10, 14, 3,  5,  12, 2,  15, 8,  6],
        [1,  4,  11, 13, 12, 3,  7,  14, 10, 15, 6,  8,  0,  5,  9,  2],
        [6,  11, 13, 8,  1,  4,  10, 7,  9,  5,  0,  15, 14, 2,  3,  12]
    ],
    # S-Box 8 (S8)
    [
        [13, 2,  8,  4,  6,  15, 11, 1,  10, 9,  3,  14, 5,  0,  12, 7],
        [1,  15, 13, 8,  10, 3,  7,  4,  12, 5,  6,  11, 0,  14, 9,  2],
        [7,  11, 4,  1,  9,  12, 14, 2,  0,  6,  10, 13, 15, 3,  5,  8],
        [2,  1,  14, 7,  4,  10, 8,  13, 15, 12, 9,  0,  3,  5,  6,  11]
    ]
]

def left_shift(k, n):
    return k[n:] + k[:n]

def permutation(A, M): 
    return [A[m-1] for m in M]

def KeySchedule(key):
    K_permuted = []
    # L[i] = K[b-q]; 
    for b in PC_1:
        q = b // 8
        idx_1_based = b - q
        K_permuted.append(key[idx_1_based - 1])

    C = K_permuted[:28]  # Metade esquerda (28 bits)
    D = K_permuted[28:]  # Metade direita (28 bits)

    all_keys = []
    for i in range(1,17):
        j = 1 if i in(1,2,9, 16) else 2
        C = left_shift(C, j)
        D = left_shift(D, j)
    
        CD = C + D  # Combina C e D para formar chave de 56 bits
        K_i = permutation(CD, PC_2)  # Aplica PC-2 para obter subchave de 48 bits para a rodada i

        all_keys.append(K_i)

    return all_keys

def binary_to_int(binary):
    for i in range(len(binary)):
        binary[i] = str(binary[i])
    
    return int(''.join(binary), 2)


def function_f(K,R):
    R_expanded = permutation(R, E)
    R_nova = [R_expanded[i]^K[i] for i in range(len(K))]
    
    # Separação do R em 8 blocos de 6 bits 
    R_total = []
    for r in range(8):
        R_r = R_nova[r*6 : (r+1)*6]
        for element in R_r:
            str(element)
        linha = R_r[0:2]
        coluna = R_r[2:6]
        
        linha_int = binary_to_int(linha)
        coluna_int = binary_to_int(coluna)
        s_box_value = S_BOXES[r][linha_int][coluna_int]
        bits_str = format(s_box_value, '04b')
        bits_int = [int(b) for b in bits_str]
        R_total.append(bits_int)


    R_total_int = [bit for linha in R_total for bit in linha] # Achata a lista de listas em uma única lista de bits
    R_final = permutation(R_total_int, P)
    
    return R_final

def cifrar(key, message):
    K = [int(b) for b in key]
    M = [int(b) for b in message]

    K_total = KeySchedule(K)  # Gera as 16 subchaves para as rodadas

    M_permuted = permutation(M, IP)  # Aplica permutação inicial
    L_anterior = M_permuted[:32]  # Metade esquerda
    R_anterior = M_permuted[32:]  # Metade direita
    
    for r in range(1,17):
        L_novo = R_anterior
        R_saida_f = function_f(K_total[r-1], R_anterior)  # Aplica função f com a subchave da rodada r
        R_novo = [R_saida_f[i] ^ L_anterior[i] for i in range(32)]  # XOR com a metade esquerda anterior

        R_anterior = R_novo
        L_anterior = L_novo

    C_permuted = permutation(R_anterior + L_anterior, IP_INV)  # Combina R16 e L16 e aplica permutação inversa
    return C_permuted

def main():
    chave_str1 = "10010010010010010010010010010010010010010010010010010010"
    msg_str1 = "1001001001001001001001001001001001001001001001001001001001001001"

    msg_cifrado = cifrar(chave_str1, msg_str1)
    print(f"\nCifrando a mensagem: {msg_str1} com a chave: {chave_str1}")
    print("Mensagem cifrada 1:", ''.join(str(bit) for bit in msg_cifrado))

    print("=" * 50, end="\n\n")
    chave_str2 = "10111011101111011110101110111101110111101011011101110111"
    msg_str2 = "1001001001001001001001001001001001001001001001001001001001001001"

    msg_cifrado2 = cifrar(chave_str2, msg_str2)
    print(f"Cifrando a mensagem: {msg_str2} com a chave: {chave_str2}")
    print("Mensagem cifrada 2:", ''.join(str(bit) for bit in msg_cifrado2))

if __name__ == "__main__":
    main()