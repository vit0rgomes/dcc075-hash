"""
DCC075 - Segurança em Sistemas de Computação
Atividade 09 - Item 3: Algoritmo Simples de Hash (XOR Bloco a Bloco + Rotação)

Descrição:
Implementação didática de uma função de Hash de 32 bits em Python puro.
A função divide a mensagem de entrada em blocos de 4 bytes (32 bits), realiza
preenchimento (padding), e comprime cada bloco no estado acumulador utilizando
operações de XOR bloco a bloco combinadas com rotação circular à esquerda (ROTL).

Como executar:
    python hash_simples.py
"""

MASK_32 = 0xFFFFFFFF  # Mantém o estado fixo em 32 bits (8 dígitos hexadecimais)


def rotl32(valor: int, bits: int) -> int:
    """Rotação circular à esquerda em um inteiro de 32 bits."""
    bits %= 32
    return ((valor << bits) | (valor >> (32 - bits))) & MASK_32


def hash_xor_rotacao(mensagem: str) -> str:
    """
    Calcula um resumo (hash) de 32 bits para uma mensagem usando XOR bloco a bloco e rotação.
    """
    dados = bytearray(mensagem.encode("utf-8"))
    tamanho_original = len(dados)

    # 1. Padding simples: completa com bytes até ser múltiplo de 4 bytes (32 bits)
    while len(dados) % 4 != 0:
        dados.append(0x80 if len(dados) == tamanho_original else 0x00)

    # Acrescenta o tamanho original da mensagem como último bloco de 32 bits
    dados.extend(tamanho_original.to_bytes(4, byteorder="big"))

    # 2. Vetor de Inicialização (IV) de 32 bits
    estado_hash = 0x6A09E667  # Constante inicial (inspirada no H0 do SHA-256)

    # 3. Processamento Bloco a Bloco (XOR + Rotação de bits)
    for i in range(0, len(dados), 4):
        bloco_32 = int.from_bytes(dados[i : i + 4], byteorder="big")

        # Mistura o bloco atual com o estado via XOR
        estado_hash ^= bloco_32

        # Aplica rotação circular de 7 bits e soma/XOR com o bloco rotacionado
        # para evitar que blocos iguais se anulem (como ocorreria num XOR puro: A ^ A = 0)
        estado_hash = rotl32(estado_hash, 7) ^ rotl32(bloco_32, 13)

    # Retorna o resumo final em hexadecimal de tamanho fixo (8 caracteres hex = 32 bits)
    return f"{estado_hash:08x}"


if __name__ == "__main__":
    print("=" * 65)
    print("       FUNÇÃO DE HASH SIMPLES (XOR BLOCO A BLOCO + ROTAÇÃO)")
    print("=" * 65)

    exemplos = [
        "Seguranca em Sistemas - DCC075",
        "Seguranca em Sistemas - DCC076",  # Apenas 1 caractere diferente
        "UFJF",
        "",
    ]

    for texto in exemplos:
        resumo = hash_xor_rotacao(texto)
        print(f"Entrada : {texto!r:<34} -> Hash (32 bits): {resumo}")

    print("-" * 65)
    entrada_usuario = input("Digite um texto para gerar o Hash (ou Enter para sair): ").strip()
    if entrada_usuario:
        print(f"Hash gerado: {hash_xor_rotacao(entrada_usuario)}")
