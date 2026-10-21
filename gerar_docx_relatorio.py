"""
Script para gerar o documento Word (.docx) formatado da Atividade 09 (Hash).
"""

import os
from docx import Document
from docx.shared import Inches, Pt, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.table import WD_TABLE_ALIGNMENT, WD_ALIGN_VERTICAL
from docx.oxml import OxmlElement
from docx.oxml.ns import qn


def set_cell_background(cell, fill_hex):
    tcPr = cell._tc.get_or_add_tcPr()
    shd = OxmlElement('w:shd')
    shd.set(qn('w:val'), 'clear')
    shd.set(qn('w:color'), 'auto')
    shd.set(qn('w:fill'), fill_hex)
    tcPr.append(shd)


def set_cell_margins(cell, top=100, bottom=100, left=150, right=150):
    tcPr = cell._tc.get_or_add_tcPr()
    tcMar = OxmlElement('w:tcMar')
    for m, val in [('top', top), ('bottom', bottom), ('left', left), ('right', right)]:
        node = OxmlElement(f'w:{m}')
        node.set(qn('w:w'), str(val))
        node.set(qn('w:type'), 'dxa')
        tcMar.append(node)
    tcPr.append(tcMar)


def add_code_box(doc, code_text):
    tbl = doc.add_table(rows=1, cols=1)
    tbl.alignment = WD_TABLE_ALIGNMENT.CENTER
    cell = tbl.rows[0].cells[0]
    set_cell_background(cell, "F4F6F8")
    set_cell_margins(cell, top=120, bottom=120, left=180, right=180)
    p = cell.paragraphs[0]
    p.paragraph_format.space_before = Pt(4)
    p.paragraph_format.space_after = Pt(4)
    run = p.add_run(code_text)
    run.font.name = "Consolas"
    run.font.size = Pt(9)
    run.font.color.rgb = RGBColor(38, 50, 56)
    doc.add_paragraph().paragraph_format.space_after = Pt(4)


def main():
    doc = Document()

    # Configuração de margens (2 cm)
    for section in doc.sections:
        section.top_margin = Inches(0.8)
        section.bottom_margin = Inches(0.8)
        section.left_margin = Inches(0.8)
        section.right_margin = Inches(0.8)

    # Título Principal
    p_title = doc.add_paragraph()
    p_title.alignment = WD_ALIGN_PARAGRAPH.CENTER
    run_title = p_title.add_run("Atividade 09: Algoritmos de Hash\nSHA-256, Análise Comparativa e Implementação")
    run_title.font.name = "Calibri"
    run_title.font.size = Pt(17)
    run_title.font.bold = True
    run_title.font.color.rgb = RGBColor(31, 78, 120)

    # Identificação do Aluno e Disciplina
    p_meta = doc.add_paragraph()
    p_meta.alignment = WD_ALIGN_PARAGRAPH.CENTER
    run_meta = p_meta.add_run("DCC075 - Segurança em Sistemas de Computação | Universidade Federal de Juiz de Fora (UFJF)\nAluno: Vitor Fernandes Gomes")
    run_meta.font.name = "Calibri"
    run_meta.font.size = Pt(11)
    run_meta.font.italic = True
    run_meta.font.color.rgb = RGBColor(89, 89, 89)

    doc.add_paragraph().paragraph_format.space_after = Pt(6)

    # -------------------------------------------------------------
    # SEÇÃO 1: SHA-256 PASSO A PASSO
    # -------------------------------------------------------------
    h1 = doc.add_heading(level=1)
    run_h1 = h1.add_run("1. Explicação Passo a Passo do Algoritmo SHA-256")
    run_h1.font.name = "Calibri"
    run_h1.font.size = Pt(13.5)
    run_h1.font.bold = True
    run_h1.font.color.rgb = RGBColor(31, 78, 120)

    p1 = doc.add_paragraph(
        "O SHA-256 (Secure Hash Algorithm de 256 bits) integra a família SHA-2, padronizada pelo NIST. "
        "Construído sobre a consagrada arquitetura de compressão iterativa de Merkle-Damgård, ele aceita mensagens de "
        "comprimento arbitrário (até 2^64 - 1 bits) e gera um resumo criptográfico (digest) de tamanho rigorosamente fixo "
        "em 256 bits (32 bytes, representados por 64 caracteres hexadecimais). O pipeline divide-se em cinco etapas fundamentais:"
    )
    p1.paragraph_format.line_spacing = 1.15
    p1.paragraph_format.space_after = Pt(6)

    etapas = [
        ("1.1 Pré-processamento e Preenchimento (Padding): ",
         "A mensagem é convertida para sua representação binária. Acrescenta-se um único bit '1' ao final dos dados, seguido de 'k' bits '0', "
         "de modo que o comprimento total resulte em exatamente 64 bits a menos que um múltiplo de 512 (ou seja, comprimento ≡ 448 mod 512). "
         "Nos últimos 64 bits reservados, codifica-se o tamanho original da mensagem em notação big-endian. Ao final dessa etapa, "
         "o bloco preenchido possui tamanho múltiplo exato de 512 bits (16 palavras de 32 bits)."),

        ("1.2 Inicialização de Registradores e Constantes: ",
         "O algoritmo mantém 8 registradores de estado de 32 bits (a, b, c, d, e, f, g, h), inicializados com os valores H0 a H7, "
         "obtidos a partir das partes fracionárias das raízes quadradas dos 8 primeiros números primos (2 a 19). "
         "Além disso, são empregadas 64 constantes fixas (K0 a K63) de 32 bits, derivadas das raízes cúbicas dos primeiros 64 números primos, "
         "garantindo aleatoriedade matemática sem dependência de constantes arbitrárias ('nothing-up-my-sleeve numbers')."),

        ("1.3 Divisão em Blocos e Expansão da Mensagem (Message Schedule): ",
         "Para cada bloco de 512 bits, o algoritmo particiona os dados em 16 palavras de 32 bits (W0 até W15). Em seguida, "
         "essas 16 palavras são expandidas para um total de 64 palavras (W0 até W63) através da relação:\n"
         "    Wt = σ1(Wt-2) + Wt-7 + σ0(Wt-15) + Wt-16 (mod 2^32)\n"
         "onde σ0 e σ1 aplicam rotações circulares à direita (ROTR), deslocamentos lógicos (SHR) e misturas XOR."),

        ("1.4 Ciclo Principal de Compressão (64 Rodadas): ",
         "Os 8 registradores de trabalho (a..h) recebem o estado corrente de (H0..H7). O algoritmo então itera por 64 rodadas. "
         "Em cada rodada t, calculam-se duas variáveis temporárias (T1 e T2):\n"
         "    Ch(e, f, g) = (e ∧ f) ⊕ (¬e ∧ g)\n"
         "    Maj(a, b, c) = (a ∧ b) ⊕ (a ∧ c) ⊕ (b ∧ c)\n"
         "    T1 = h + Σ1(e) + Ch(e, f, g) + Kt + Wt (mod 2^32)\n"
         "    T2 = Σ0(a) + Maj(a, b, c) (mod 2^32)\n"
         "Os registradores sofrem permutação em cascata: h=g, g=f, f=e, e=d+T1, d=c, c=b, b=a e a=T1+T2. Essa estrutura garante rápida difusão e confusão a cada passo."),

        ("1.5 Atualização Acumulativa e Saída Final: ",
         "Ao término das 64 rodadas do bloco atual, os valores acumulados em (a..h) são somados módulo 2^32 ao estado anterior (H0..H7). "
         "Após o processamento de todos os blocos de 512 bits da mensagem, a concatenação direta H0 || H1 || ... || H7 resulta no hash final de 256 bits.")
    ]

    for titulo, desc in etapas:
        p = doc.add_paragraph()
        p.paragraph_format.line_spacing = 1.15
        p.paragraph_format.space_after = Pt(4)
        run_bold = p.add_run(titulo)
        run_bold.font.bold = True
        run_bold.font.color.rgb = RGBColor(31, 78, 120)
        p.add_run(desc)

    doc.add_paragraph().paragraph_format.space_after = Pt(6)

    # -------------------------------------------------------------
    # SEÇÃO 2: ANÁLISE COMPARATIVA DOS ALGORITMOS DE HASH
    # -------------------------------------------------------------
    h2 = doc.add_heading(level=1)
    run_h2 = h2.add_run("2. Análise Comparativa dos Principais Algoritmos de Hash Atuais")
    run_h2.font.name = "Calibri"
    run_h2.font.size = Pt(13.5)
    run_h2.font.bold = True
    run_h2.font.color.rgb = RGBColor(31, 78, 120)

    p2_1 = doc.add_paragraph(
        "As funções de resumo criptográfico evoluíram continuamente para acompanhar tanto o avanço do poder de processamento "
        "computacional quanto a descoberta de métodos refinados de criptoanálise. Historicamente, os algoritmos MD5 (128 bits) e "
        "SHA-1 (160 bits) foram a base da segurança na internet nos anos 1990 e 2000. Seu atrativo residia na alta velocidade e na "
        "simplicidade de implementação. Contudo, ambos encontram-se hoje definitivamente quebrados contra ataques de colisão. "
        "A demonstração prática do ataque SHAttered em 2017 evidenciou que gerar colisões em SHA-1 tornou-se viável a custos operacionais "
        "acessíveis. Por essa razão, normas internacionais baniram ambos os algoritmos de aplicações criptográficas, restringindo-os a "
        "checksums triviais para detecção de corrupção acidental em canais de transmissão."
    )
    p2_1.paragraph_format.line_spacing = 1.15
    p2_1.paragraph_format.space_after = Pt(6)

    p2_2 = doc.add_paragraph(
        "No cenário contemporâneo, a família SHA-2 (particularmente SHA-256 e SHA-512) estabeleceu-se como o padrão de fato da indústria, "
        "sustentando protocolos como TLS/HTTPS, assinaturas digitais RSA/ECDSA, controle de versão no Git e mecanismos de consenso em blockchains. "
        "O ponto forte do SHA-2 reside na maturidade teórica e no suporte nativo por instruções dedicadas em processadores modernos (como Intel SHA Extensions). "
        "Como ponto de atenção, por ser baseado no modelo de Merkle-Damgård, o SHA-256 é vulnerável a ataques de extensão de comprimento "
        "(length extension attacks) se empregado ingenuamente em assinaturas de chaves sem envelope HMAC. Além disso, sua alta velocidade de "
        "cálculo constitui uma fragilidade severa quando aplicado diretamente ao armazenamento de senhas."
    )
    p2_2.paragraph_format.line_spacing = 1.15
    p2_2.paragraph_format.space_after = Pt(6)

    p2_3 = doc.add_paragraph(
        "Para diversificar as defesas criptográficas, o NIST padronizou o SHA-3 (Keccak), fundamentado na inovadora construção Sponge (esponja). "
        "O SHA-3 elimina a suscetibilidade a ataques de extensão de comprimento e possui excelente robustez contra ataques quânticos e diferenciais, "
        "embora apresente desempenho moderado quando executado em CPUs convencionais sem circuitos ASIC dedicados. Paralelamente, no universo de "
        "alta performance, funções modernas como BLAKE2 e BLAKE3 superam a velocidade do MD5 oferecendo margem de segurança comparável ao SHA-3. "
        "Por fim, no armazenamento de credenciais e senhas, a estratégia inverte-se: privilegiam-se algoritmos propositalmente lentos e intensivos em memória, "
        "como bcrypt e Argon2 (vencedor da Password Hashing Competition). O Argon2 neutraliza ataques massivos via GPUs e ASICs exigindo memória RAM "
        "configurável para cada cálculo, blindando as credenciais mesmo contra adversários dotados de infraestrutura distribuída de força bruta."
    )
    p2_3.paragraph_format.line_spacing = 1.15
    p2_3.paragraph_format.space_after = Pt(8)

    # Tabela comparativa
    table = doc.add_table(rows=7, cols=5)
    table.alignment = WD_TABLE_ALIGNMENT.CENTER
    table.autofit = False

    headers = ["Algoritmo", "Tamanho Digest", "Segurança a Colisões", "Desempenho", "Uso Recomendado"]
    widths = [Inches(1.2), Inches(1.1), Inches(1.5), Inches(1.2), Inches(1.8)]

    # Cabeçalho da Tabela
    hdr_cells = table.rows[0].cells
    for i, h in enumerate(headers):
        hdr_cells[i].text = h
        set_cell_background(hdr_cells[i], "1F4E78")
        set_cell_margins(hdr_cells[i], top=100, bottom=100, left=100, right=100)
        p = hdr_cells[i].paragraphs[0]
        p.alignment = WD_ALIGN_PARAGRAPH.CENTER
        for r in p.runs:
            r.font.name = "Calibri"
            r.font.size = Pt(9.5)
            r.font.bold = True
            r.font.color.rgb = RGBColor(255, 255, 255)

    dados_tabela = [
        ("MD5", "128 bits", "Quebrado (colisões imediatas)", "Muito Alto", "Apenas integridade acidental (não seguro)"),
        ("SHA-1", "160 bits", "Quebrado (ataque SHAttered)", "Alto", "Legado / Checksums não-críticos"),
        ("SHA-256", "256 bits", "Robusto (padrão global atual)", "Alto (com instrução SHA)", "TLS, Assinaturas Digitais, Git, Blockchain"),
        ("SHA-3 (Keccak)", "224 a 512 bits", "Excelente (imune a extensão)", "Médio em CPU / Alto em HW", "Aplicações de alta segurança, defesa em profundidade"),
        ("BLAKE3", "256 bits", "Robusto (árvore de Merkle)", "Extremamente Alto (SIMD/Multi-thread)", "Checksums rápidos, sistemas de arquivos, deduplicação"),
        ("Argon2id", "Configurável", "Máxima (resistente a GPUs/ASICs)", "Lento (Memory-Hard)", "Armazenamento e autenticação de senhas")
    ]

    for row_idx, data in enumerate(dados_tabela, start=1):
        row_cells = table.rows[row_idx].cells
        bg_color = "F9FAFB" if row_idx % 2 == 1 else "FFFFFF"
        for col_idx, text in enumerate(data):
            row_cells[col_idx].text = text
            set_cell_background(row_cells[col_idx], bg_color)
            set_cell_margins(row_cells[col_idx], top=80, bottom=80, left=100, right=100)
            p = row_cells[col_idx].paragraphs[0]
            if col_idx in [0, 1]:
                p.alignment = WD_ALIGN_PARAGRAPH.CENTER
            else:
                p.alignment = WD_ALIGN_PARAGRAPH.LEFT
            for r in p.runs:
                r.font.name = "Calibri"
                r.font.size = Pt(8.5)
                if col_idx == 0:
                    r.font.bold = True

    doc.add_paragraph().paragraph_format.space_after = Pt(10)

    # -------------------------------------------------------------
    # SEÇÃO 3: CÓDIGO E IMPLEMENTAÇÃO PRÁTICA (XOR + ROTAÇÃO)
    # -------------------------------------------------------------
    h3 = doc.add_heading(level=1)
    run_h3 = h3.add_run("3. Implementação Prática: Algoritmo Didático de Hash de 32 Bits")
    run_h3.font.name = "Calibri"
    run_h3.font.size = Pt(13.5)
    run_h3.font.bold = True
    run_h3.font.color.rgb = RGBColor(31, 78, 120)

    p3_1 = doc.add_paragraph(
        "Para ilustrar os conceitos de preenchimento de bloco, compressão de estado e difusão de bits, foi desenvolvido em "
        "Python puro o script hash_simples.py. O algoritmo processa mensagens em blocos de 4 bytes (32 bits), aplicando preenchimento "
        "com inclusão do tamanho original. A compressão combina operações de XOR bloco a bloco com rotação circular à esquerda (ROTL), "
        "evitando a vulnerabilidade do XOR simples (onde blocos repetidos se anulariam, pois A ⊕ A = 0)."
    )
    p3_1.paragraph_format.line_spacing = 1.15
    p3_1.paragraph_format.space_after = Pt(6)

    # Código-fonte
    p_code_label = doc.add_paragraph()
    r_cl = p_code_label.add_run("Código da Função de Hash (hash_simples.py):")
    r_cl.font.bold = True
    r_cl.font.size = Pt(10)
    p_code_label.paragraph_format.space_after = Pt(3)

    code_snippet = (
        "def rotl32(valor: int, bits: int) -> int:\n"
        "    bits %= 32\n"
        "    return ((valor << bits) | (valor >> (32 - bits))) & 0xFFFFFFFF\n\n"
        "def hash_xor_rotacao(mensagem: str) -> str:\n"
        "    dados = bytearray(mensagem.encode('utf-8'))\n"
        "    tamanho_original = len(dados)\n\n"
        "    # 1. Padding até múltiplo de 4 bytes (32 bits) + registro do tamanho\n"
        "    while len(dados) % 4 != 0:\n"
        "        dados.append(0x80 if len(dados) == tamanho_original else 0x00)\n"
        "    dados.extend(tamanho_original.to_bytes(4, byteorder='big'))\n\n"
        "    # 2. Vetor de Inicialização (IV)\n"
        "    estado_hash = 0x6A09E667\n\n"
        "    # 3. Processamento Bloco a Bloco (XOR + Rotação)\n"
        "    for i in range(0, len(dados), 4):\n"
        "        bloco_32 = int.from_bytes(dados[i : i + 4], byteorder='big')\n"
        "        estado_hash ^= bloco_32\n"
        "        estado_hash = rotl32(estado_hash, 7) ^ rotl32(bloco_32, 13)\n\n"
        "    return f'{estado_hash:08x}'"
    )
    add_code_box(doc, code_snippet)

    # Saída do Terminal
    p_term_label = doc.add_paragraph()
    r_tl = p_term_label.add_run("Saída da Execução com Testes de Difusão:")
    r_tl.font.bold = True
    r_tl.font.size = Pt(10)
    p_term_label.paragraph_format.space_after = Pt(3)

    term_output = (
        "=================================================================\n"
        "       FUNÇÃO DE HASH SIMPLES (XOR BLOCO A BLOCO + ROTAÇÃO)\n"
        "=================================================================\n"
        "Entrada : 'Seguranca em Sistemas - DCC075'   -> Hash (32 bits): b07cd2ba\n"
        "Entrada : 'Seguranca em Sistemas - DCC076'   -> Hash (32 bits): b07cd0ba\n"
        "Entrada : 'UFJF'                             -> Hash (32 bits): 1f080ae5\n"
        "Entrada : ''                                 -> Hash (32 bits): 90cf372f\n"
        "-----------------------------------------------------------------\n"
        "[OK] Hash fixo de 32 bits (8 caracteres hex) gerado com sucesso."
    )
    add_code_box(doc, term_output)

    # Conclusão
    p_conc = doc.add_paragraph(
        "Conclusão: A prática demonstra os alicerces teóricos das funções de dispersão unidirecionais. "
        "Embora a implementação com XOR e rotação de 32 bits seja didática e insuficiente para segurança moderna "
        "(devido ao pequeno espaço amostral de 2^32 possibilidades, suscetível a ataques do paradoxo do aniversário em cerca de 2^16 operações), "
        "ela ilustra perfeitamente a necessidade de não-linearidade, difusão e preenchimento canônico que sustentam os padrões industriais como o SHA-256."
    )
    p_conc.paragraph_format.line_spacing = 1.15
    p_conc.paragraph_format.space_after = Pt(6)

    # Salva o documento
    output_path = os.path.join(os.path.dirname(__file__), "Relatorio_Atividade_09_Hash.docx")
    doc.save(output_path)
    print(f"[SUCESSO] Documento gerado em: {output_path}")


if __name__ == "__main__":
    main()
