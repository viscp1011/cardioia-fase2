"""CardioIA - Fase 2 - Parte 1: extração de sintomas e sugestão de diagnóstico.

Lê as frases de pacientes (.txt), procura nelas as expressões do mapa de
conhecimento (.csv) e sugere o diagnóstico mais compatível.

Uso:
    python extrair_sintomas.py
    python extrair_sintomas.py outras_frases.txt outro_mapa.csv

Aviso: protótipo acadêmico com dados simulados. Não é ferramenta clínica.
"""

import csv
import re
import sys
import unicodedata
from collections import defaultdict
from pathlib import Path

PASTA = Path(__file__).parent
ARQUIVO_FRASES = PASTA / "sintomas_pacientes.txt"
ARQUIVO_MAPA = PASTA / "mapa_conhecimento.csv"

# Palavras que, logo antes do sintoma, indicam que o paciente o está negando
NEGADORES = {"nao", "sem", "nunca", "nem", "nenhum", "nenhuma"}
JANELA_NEGACAO = 3  # quantas palavras antes do sintoma são verificadas


def normalizar(texto):
    """Minúsculas e sem acentos, para 'tórax' casar com 'torax'."""
    sem_acentos = unicodedata.normalize("NFKD", texto)
    sem_acentos = "".join(c for c in sem_acentos if not unicodedata.combining(c))
    return sem_acentos.lower().strip()


def carregar_mapa(caminho):
    """Devolve {expressão normalizada: (expressão original, {doenças})}.

    Uma mesma expressão pode apontar para mais de uma doença (ex.: falta de ar),
    como acontece na clínica: o sintoma isolado não fecha diagnóstico.
    """
    mapa = {}
    with open(caminho, encoding="utf-8", newline="") as arquivo:
        for linha in csv.DictReader(arquivo):
            doenca = linha["Doença Associada"].strip()
            for coluna in ("Sintoma 1", "Sintoma 2"):
                expressao = linha[coluna].strip()
                if expressao:
                    chave = normalizar(expressao)
                    mapa.setdefault(chave, (expressao, set()))[1].add(doenca)
    return mapa


def carregar_frases(caminho):
    with open(caminho, encoding="utf-8") as arquivo:
        return [linha.strip() for linha in arquivo if linha.strip()]


def esta_negado(frase_normalizada, posicao_inicio):
    """Verifica se há um negador nas palavras imediatamente antes do sintoma.

    Só olha dentro da mesma oração: a busca para na última pontuação, para que
    'não tenho falta de ar, mas tive febre' não negue também a febre.
    """
    oracao = re.split(r"[,.;:]", frase_normalizada[:posicao_inicio])[-1]
    palavras_anteriores = oracao.split()[-JANELA_NEGACAO:]
    return any(palavra in NEGADORES for palavra in palavras_anteriores)


def extrair_sintomas(frase, mapa):
    """Devolve (sintomas presentes, sintomas negados) encontrados na frase."""
    frase_normalizada = normalizar(frase)
    presentes, negados = [], []
    for chave, (expressao, _) in mapa.items():
        # \b evita casar dentro de outra palavra (ex.: 'febre' em 'febrea')
        ocorrencia = re.search(rf"\b{re.escape(chave)}\b", frase_normalizada)
        if not ocorrencia:
            continue
        if esta_negado(frase_normalizada, ocorrencia.start()):
            negados.append(expressao)
        else:
            presentes.append(expressao)
    return presentes, negados


def pontuar_doencas(sintomas, mapa):
    """Soma, por doença, o número de palavras de cada sintoma encontrado.

    Pesar pelo tamanho da expressão favorece o achado mais específico:
    'falta de ar súbita' vale mais do que 'falta de ar' sozinha.
    """
    pontos = defaultdict(int)
    for sintoma in sintomas:
        for doenca in mapa[normalizar(sintoma)][1]:
            pontos[doenca] += len(sintoma.split())
    return sorted(pontos.items(), key=lambda item: (-item[1], item[0]))


def analisar_frase(frase, mapa):
    presentes, negados = extrair_sintomas(frase, mapa)
    return {
        "frase": frase,
        "sintomas": presentes,
        "negados": negados,
        "ranking": pontuar_doencas(presentes, mapa),
    }


def imprimir_resultado(numero, resultado):
    print(f"\nPaciente {numero:02d}: {resultado['frase']}")
    print(f"  Sintomas identificados: {', '.join(resultado['sintomas']) or 'nenhum'}")
    if resultado["negados"]:
        print(f"  Sintomas negados:       {', '.join(resultado['negados'])}")
    if not resultado["ranking"]:
        print("  Diagnóstico sugerido:   inconclusivo (nenhum sintoma do mapa)")
        return
    doenca, pontos = resultado["ranking"][0]
    print(f"  Diagnóstico sugerido:   {doenca} (pontuação {pontos})")
    outras = [f"{nome} ({valor})" for nome, valor in resultado["ranking"][1:]]
    if outras:
        print(f"  Outras hipóteses:       {', '.join(outras)}")


def main():
    caminho_frases = Path(sys.argv[1]) if len(sys.argv) > 1 else ARQUIVO_FRASES
    caminho_mapa = Path(sys.argv[2]) if len(sys.argv) > 2 else ARQUIVO_MAPA

    mapa = carregar_mapa(caminho_mapa)
    frases = carregar_frases(caminho_frases)
    print(f"Mapa de conhecimento: {len(mapa)} expressões | Frases: {len(frases)}")

    for numero, frase in enumerate(frases, start=1):
        imprimir_resultado(numero, analisar_frase(frase, mapa))

    print("\nAviso: sugestões geradas por regras sobre dados simulados; "
          "não substituem avaliação médica.")


if __name__ == "__main__":
    main()
