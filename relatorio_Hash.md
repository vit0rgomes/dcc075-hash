# Atividade 09 — Algoritmos de Hash (SHA-256, Análise Comparativa e Implementação)

**Disciplina:** DCC075 - Segurança em Sistemas de Computação  
**Aluno:** Vitor Fernandes Gomes  

---

## 1) Explicação Passo a Passo do Algoritmo SHA-256

O **SHA-256** (*Secure Hash Algorithm* de 256 bits), pertencente à família SHA-2 e construído sobre a estrutura de **Merkle–Damgård**, recebe uma mensagem de qualquer tamanho (até $2^{64}-1$ bits) e produz um resumo criptográfico (*digest*) de tamanho fixo de **256 bits (32 bytes / 64 caracteres hexadecimais)**. O seu funcionamento passo a passo divide-se em cinco etapas principais:

1. **Pré-processamento e Preenchimento (*Padding*):**
   - A mensagem original é convertida em binário.
   - Adiciona-se um único bit `1` ao final da mensagem, seguido por $k$ bits `0`, até que o comprimento total seja congruente a $448 \pmod{512}$.
   - Nos últimos **64 bits** do bloco, grava-se o tamanho original da mensagem (em bits) como um inteiro *big-endian* de 64 bits. Assim, a mensagem preenchida passa a ter um tamanho exato múltiplo de **512 bits**.

2. **Inicialização das Variáveis de Estado ($H_0$ a $H_7$) e Constantes ($K_0$ a $K_{63}$):**
   - O algoritmo define 8 registradores iniciais de 32 bits ($a, b, c, d, e, f, g, h$, derivados de $H_0 \dots H_7$), formados pelas partes fracionárias das raízes quadradas dos 8 primeiros números primos ($2, 3, 5, 7, 11, 13, 17, 19$).
   - Define também 64 constantes de rodada ($K_0 \dots K_{63}$) de 32 bits, obtidas das partes fracionárias das raízes cúbicas dos 64 primeiros números primos.

3. **Divisão em Blocos e Expansão da Mensagem (*Message Schedule*):**
   - A mensagem preenchida é processada em blocos de **512 bits**.
   - Cada bloco de 512 bits é inicialmente dividido em 16 palavras de 32 bits ($W_0, W_1, \dots, W_{15}$).
   - Essas 16 palavras são expandidas para **64 palavras** ($W_0 \dots W_{63}$) através da fórmula:
     $$W_t = \sigma_1(W_{t-2}) + W_{t-7} + \sigma_0(W_{t-15}) + W_{t-16} \pmod{2^{32}}$$
     onde $\sigma_0$ e $\sigma_1$ realizam rotações circulares à direita (*ROTR*), deslocamentos (*SHR*) e operações XOR.

4. **Loop Principal de Compressão (64 Rodadas):**
   - Os registradores de trabalho $(a, b, c, d, e, f, g, h)$ são inicializados com o valor atual do hash $(H_0 \dots H_7)$.
   - Para cada uma das **64 rodadas** ($t = 0$ até $63$), calculam-se duas palavras temporárias ($T_1$ e $T_2$) utilizando quatro funções lógicas bit a bit:
     - **$\text{Ch}(e, f, g) = (e \land f) \oplus (\neg e \land g)$** (*Choice*: o bit de $e$ escolhe entre $f$ ou $g$).
     - **$\text{Maj}(a, b, c) = (a \land b) \oplus (a \land c) \oplus (b \land c)$** (*Majority*: voto majoritário dos bits de $a, b, c$).
     - **$\Sigma_0(a)$** e **$\Sigma_1(e)$**: somas XOR de três rotações circulares à direita.
     - $T_1 = h + \Sigma_1(e) + \text{Ch}(e, f, g) + K_t + W_t \pmod{2^{32}}$
     - $T_2 = \Sigma_0(a) + \text{Maj}(a, b, c) \pmod{2^{32}}$
   - Os registradores são então deslocados ($h=g, g=f, f=e, e=d+T_1, d=c, c=b, b=a, a=T_1+T_2$).

5. **Atualização do Estado e Concatenação Final:**
   - Ao final das 64 rodadas de um bloco, os valores de $(a \dots h)$ são somados módulo $2^{32}$ ao estado anterior $(H_0 \dots H_7)$.
   - Após processar todos os blocos de 512 bits da mensagem, a concatenação final de $H_0 \parallel H_1 \parallel H_2 \parallel H_3 \parallel H_4 \parallel H_5 \parallel H_6 \parallel H_7$ gera o hash SHA-256 de 256 bits.

---

## 2) Principais Algoritmos de Hash Utilizados Atualmente: Pontos Fortes e Fracos

As funções de resumo criptográfico (*hash*) evoluíram significativamente nas últimas décadas para responder ao aumento do poder computacional e ao avanço das técnicas de criptoanálise diferencial. Historicamente, o **MD5** (128 bits) e o **SHA-1** (160 bits) foram amplamente empregados em verificação de integridade e certificados digitais. Seu principal ponto forte ainda é a altíssima velocidade de processamento e o baixo custo computacional; contudo, seu ponto fraco é crítico: ambos estão **criptograficamente quebrados** quanto à resistência a colisões (como demonstrado pelo ataque *SHAttered* contra o SHA-1), sendo inadequados para segurança e restritos hoje apenas a *checksums* não-maliciosos de integridade acidental.

Atualmente, o padrão dominante da indústria é a família **SHA-2** (especialmente **SHA-256** e **SHA-512**), utilizada em TLS/HTTPS, assinaturas digitais, Git e redes Blockchain. Seus pontos fortes incluem a segurança amplamente testada e o suporte de aceleração via hardware (instruções *SHA Extensions* em processadores modernos). Como pontos fracos, por utilizarem a construção de Merkle–Damgård, o SHA-256 é teoricamente suscetível a ataques de extensão de comprimento (*length extension attacks*) caso usado de forma ingênua sem HMAC, além de ser excessivamente rápido para armazenamento direto de senhas.

Para superar limitações estruturais do SHA-2, o NIST padronizou o **SHA-3 (Keccak)**, baseado na construção *Sponge* (esponja). Seu grande ponto forte é ter uma arquitetura interna totalmente distinta do SHA-2, sendo imune a ataques de extensão de comprimento, embora seja mais lento em software comum quando comparado a alternativas modernas como o **BLAKE2** e **BLAKE3**, que oferecem velocidade superior ao MD5 com segurança equivalente ao SHA-3. Por fim, especificamente para o armazenamento de senhas, algoritmos rápidos são vulneráveis a força bruta em GPUs/ASICs; por isso, utilizam-se funções de hash lentas e intensivas em memória como **bcrypt** e **Argon2** (vencedor da *Password Hashing Competition*). O ponto forte do Argon2 é resistir a ataques de hardware dedicado consumindo memória RAM configurável, tendo como contrapartida o maior consumo de recursos do servidor durante picos de autenticação.

---

## 3) Código Simples de Hash (XOR Bloco a Bloco com Rotação)

O arquivo [`hash_simples.py`](file:///c:/Users/vitin/OneDrive/Documentos/ufjf/cc_integral/DCC075-Seguranca-de-sistemas/09-Hash/hash_simples.py) implementa uma função de hash de 32 bits utilizando preenchimento de blocos, operação **XOR bloco a bloco** e **rotação circular de bits à esquerda (`rotl32`)** para evitar que blocos idênticos se anulem ($A \oplus A = 0$).

### Saída da Execução:
```text
=================================================================
       FUNÇÃO DE HASH SIMPLES (XOR BLOCO A BLOCO + ROTAÇÃO)
=================================================================
Entrada : 'Seguranca em Sistemas - DCC075'   -> Hash (32 bits): b07cd2ba
Entrada : 'Seguranca em Sistemas - DCC076'   -> Hash (32 bits): b07cd0ba
Entrada : 'UFJF'                             -> Hash (32 bits): 1f080ae5
Entrada : ''                                 -> Hash (32 bits): 90cf372f
```
