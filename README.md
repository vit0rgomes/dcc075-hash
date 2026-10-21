# DCC075 - Segurança em Sistemas de Computação
## Atividade 09 — Algoritmos de Hash (SHA-256, Análise Comparativa e Implementação)

**Aluno:** Vitor Fernandes Gomes  
**Instituição:** Universidade Federal de Juiz de Fora (UFJF)  

Este repositório contém a documentação técnica sobre o funcionamento interno do **SHA-256**, a análise comparativa entre as principais funções de hash criptográficas da atualidade e a implementação em Python de um algoritmo didático de hash de 32 bits utilizando operações de **XOR bloco a bloco** combinadas com **rotação circular de bits**.

O relatório completo formatado em Word está disponível neste repositório em [`Relatorio_Atividade_09_Hash.docx`](Relatorio_Atividade_09_Hash.docx).

---

## 1. Funcionamento Passo a Passo do SHA-256

O **SHA-256** (*Secure Hash Algorithm* de 256 bits), pertencente à família SHA-2 e baseado na estrutura de **Merkle–Damgård**, recebe uma mensagem de qualquer tamanho (até $2^{64}-1$ bits) e gera um resumo criptográfico (*digest*) de **256 bits (32 bytes / 64 caracteres hexadecimais)**:

1. **Pré-processamento e Preenchimento (*Padding*):**
   - A mensagem é convertida para binário.
   - Concatena-se um bit `1`, seguido de $k$ bits `0`, até que o comprimento total seja congruente a $448 \pmod{512}$.
   - Os últimos 64 bits registram o tamanho original da mensagem em formato *big-endian*, totalizando um múltiplo exato de 512 bits.

2. **Inicialização das Variáveis de Estado e Constantes:**
   - 8 registradores de 32 bits ($a, b, c, d, e, f, g, h$, derivados de $H_0 \dots H_7$) baseados nas partes fracionárias das raízes quadradas dos 8 primeiros números primos (2 a 19).
   - 64 constantes de rodada ($K_0 \dots K_{63}$) de 32 bits, derivadas das raízes cúbicas dos 64 primeiros primos.

3. **Expansão da Mensagem (*Message Schedule*):**
   - Cada bloco de 512 bits é dividido em 16 palavras ($W_0 \dots W_{15}$) e expandido para 64 palavras ($W_0 \dots W_{63}$):
     $$W_t = \sigma_1(W_{t-2}) + W_{t-7} + \sigma_0(W_{t-15}) + W_{t-16} \pmod{2^{32}}$$

4. **Loop de Compressão (64 Rodadas):**
   - Para cada rodada $t \in [0, 63]$, calculam-se variáveis temporárias via funções booleanas de confusão e difusão:
     $$\text{Ch}(e, f, g) = (e \land f) \oplus (\neg e \land g)$$
     $$\text{Maj}(a, b, c) = (a \land b) \oplus (a \land c) \oplus (b \land c)$$
     $$T_1 = h + \Sigma_1(e) + \text{Ch}(e, f, g) + K_t + W_t \pmod{2^{32}}$$
     $$T_2 = \Sigma_0(a) + \text{Maj}(a, b, c) \pmod{2^{32}}$$
   - Permutação de registradores: $h=g, g=f, f=e, e=d+T_1, d=c, c=b, b=a, a=T_1+T_2$.

5. **Atualização Acumulativa e Concatenação:**
   - O estado $(a \dots h)$ é somado módulo $2^{32}$ ao estado anterior $(H_0 \dots H_7)$ do bloco.
   - O hash final de 256 bits resulta da concatenação de $H_0 \parallel H_1 \parallel \dots \parallel H_7$.

---

## 2. Análise Comparativa dos Algoritmos de Hash

As funções de resumo criptográfico evoluíram continuamente para responder ao avanço computacional e a novas técnicas de criptoanálise. Historicamente, **MD5** (128 bits) e **SHA-1** (160 bits) foram pilares da internet, valorizados pela alta velocidade. Contudo, ambos estão **definitivamente quebrados** contra colisões (o ataque prático *SHAttered* em 2017 selou o fim do SHA-1), sendo banidos de usos de segurança e restritos hoje a *checksums* não-maliciosos para detectar corrupção de mídia.

Atualmente, o padrão dominante é a família **SHA-2** (em especial **SHA-256** e **SHA-512**), adotada em TLS/HTTPS, assinaturas digitais, Git e blockchains. Seu ponto forte é a maturidade matemática e a aceleração nativa por hardware (*SHA Extensions*). Como limitação teórica, sua estrutura Merkle–Damgård exige o uso de construções HMAC para evitar ataques de extensão de comprimento (*length extension*). Além disso, sua rapidez é prejudicial para senhas.

Para superar essas limitações, o NIST padronizou o **SHA-3 (Keccak)**, que usa a inovadora construção *Sponge* (esponja), imune a ataques de extensão de comprimento. Paralelamente, funções modernas como **BLAKE2** e **BLAKE3** superam a velocidade do MD5 com nível de segurança do SHA-3. Por fim, para senhas, utilizam-se funções intencionalmente lentas e pesadas em memória, como **bcrypt** e **Argon2** (vencedor da *Password Hashing Competition*), que impedem ataques massivos via GPUs e ASICs distribuídos.

| Algoritmo | Digest | Resistência a Colisões | Desempenho | Casos de Uso Recomendados |
| :--- | :---: | :---: | :---: | :--- |
| **MD5** | 128 bits | Quebrado (colisões triviais) | Muito Alto | Checksum acidental |
| **SHA-1** | 160 bits | Quebrado (ataque SHAttered) | Alto | Legado |
| **SHA-256** | 256 bits | Robusto (padrão global) | Alto (com SHA-NI) | TLS/HTTPS, Git, Assinaturas Digitais |
| **SHA-3** | 224-512 bits | Excelente (construção esponja) | Médio em CPU | Defesa em profundidade |
| **BLAKE3** | 256 bits | Robusto (Merkle Tree) | Altíssimo (SIMD) | Deduplicação, sistemas de arquivos |
| **Argon2id** | Ajustável | Máxima (Memory-Hard) | Lento (configurável) | Armazenamento seguro de senhas |

---

## 3. Implementação Didática de Hash de 32 Bits (`hash_simples.py`)

O script [`hash_simples.py`](hash_simples.py) demonstra na prática o funcionamento de uma função de compressão de 32 bits utilizando:
- **Preenchimento de blocos** com o byte delimitador `0x80`, preenchimento com `0x00` e inclusão do tamanho original da mensagem.
- **Vetor de Inicialização (IV)** fixo de 32 bits (`0x6A09E667`).
- **XOR bloco a bloco** combinado com **rotação circular de bits à esquerda (`rotl32`)**, garantindo que blocos repetidos não se anulem ($A \oplus A = 0$).

### Como Executar

```bash
# Execução direta:
python hash_simples.py

# No Windows via Python Launcher:
py hash_simples.py
```

### Exemplo de Saída:

```text
=================================================================
       FUNÇÃO DE HASH SIMPLES (XOR BLOCO A BLOCO + ROTAÇÃO)
=================================================================
Entrada : 'Seguranca em Sistemas - DCC075'   -> Hash (32 bits): b07cd2ba
Entrada : 'Seguranca em Sistemas - DCC076'   -> Hash (32 bits): b07cd0ba
Entrada : 'UFJF'                             -> Hash (32 bits): 1f080ae5
Entrada : ''                                 -> Hash (32 bits): 90cf372f
-----------------------------------------------------------------
Digite um texto para gerar o Hash (ou Enter para sair):
```
