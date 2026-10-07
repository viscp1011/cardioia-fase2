# CardioIA — Fase 2: Diagnóstico Automatizado (IA no Estetoscópio Digital)

**Curso:** Inteligência Artificial — FIAP
**Fase 2:** Início da IA avançada — Cap. 1: Desafio Integrador: IA entre Robôs, Sinapses e Medicina
**Grupo:** 88
**Integrante:** Vitorio Stevanatto Compri Paciulo — vitorioscp@gmail.com


---

## 1. Sobre esta fase

O **CardioIA** simula o ecossistema digital de uma cardiologia moderna. Na
[Fase 1](https://github.com/viscp1011/cardioia-fase1) reunimos e documentamos os dados
(numéricos, textuais e visuais). Nesta Fase 2 o projeto passa a **interpretar texto clínico**:

| Parte | O que faz | Técnica |
|---|---|---|
| **Parte 1** | Lê relatos de pacientes, identifica sintomas e sugere um diagnóstico | Regras sobre um mapa de conhecimento (ontologia simples) |
| **Parte 2** | Classifica uma frase como **alto risco** ou **baixo risco** | TF-IDF + Regressão Logística (Scikit-learn) |

As duas abordagens são complementares: a Parte 1 é transparente e auditável, mas só reconhece o
que está no mapa; a Parte 2 generaliza a partir de exemplos, mas herda os vieses deles.

> **Aviso:** todos os dados desta fase são **simulados**, escritos pelo grupo para fins
> acadêmicos. Nada aqui é ferramenta clínica nem substitui avaliação médica.

---

## 2. Estrutura do repositório

```
cardioia-fase2/
├── README.md
├── requirements.txt
├── parte1_extracao_sintomas/
│   ├── sintomas_pacientes.txt      # 10 relatos de pacientes
│   ├── mapa_conhecimento.csv       # 43 linhas: sintomas -> 12 doenças
│   └── extrair_sintomas.py         # extração de sintomas e sugestão de diagnóstico
├── parte2_classificador_risco/
│   ├── frases_risco.csv            # 100 frases rotuladas (50 alto / 50 baixo risco)
│   └── classificador_risco.ipynb   # TF-IDF, treino, avaliação e análise de vieses
└── docs/
    └── roteiro_video.md            # roteiro do vídeo de demonstração
```

---

## 3. Como executar

Requer Python 3.10 ou superior.

```bash
git clone https://github.com/viscp1011/cardioia-fase2.git
cd cardioia-fase2
pip install -r requirements.txt

# Parte 1 (usa só a biblioteca padrão do Python)
python parte1_extracao_sintomas/extrair_sintomas.py

# Parte 2
jupyter notebook parte2_classificador_risco/classificador_risco.ipynb
```

O notebook já está versionado **com as saídas**, então os resultados podem ser lidos direto no
GitHub. A semente aleatória é fixa (42), a mesma da Fase 1.

---

## 4. Parte 1 — Frases de sintomas e extração de informações

### 4.1 Relatos (`sintomas_pacientes.txt`)

Dez frases completas, uma por linha, cada uma com **o que o paciente sente, quando começou e
como afeta a rotina**. Os relatos cobrem nove quadros diferentes e incluem, de propósito, uma
frase com negação ("não tenho falta de ar") para testar o extrator.

### 4.2 Mapa de conhecimento (`mapa_conhecimento.csv`)

Colunas `Sintoma 1 | Sintoma 2 | Doença Associada`, como pede o enunciado. Cada linha traz duas
formas de dizer o mesmo achado (ou dois achados do mesmo quadro) e a doença relacionada.

- **43 linhas, 85 expressões distintas, 12 doenças:** infarto agudo do miocárdio, angina,
  insuficiência cardíaca, arritmia cardíaca, hipertensão arterial, pericardite, doença arterial
  periférica, embolia pulmonar, acidente vascular cerebral, endocardite, estenose aórtica e
  miocardite.
- **Um sintoma pode apontar para mais de uma doença.** "Falta de ar" aparece em angina e em
  insuficiência cardíaca, como na clínica: o sintoma isolado não fecha diagnóstico.

### 4.3 Extrator (`extrair_sintomas.py`)

1. **Normaliza** frase e expressões (minúsculas, sem acentos).
2. **Procura** cada expressão do mapa na frase, respeitando limite de palavra.
3. **Detecta negação:** se houver "não", "sem", "nunca" ou "nem" nas três palavras anteriores,
   dentro da mesma oração, o sintoma é registrado como negado e não pontua.
4. **Pontua** cada doença somando o número de palavras das expressões encontradas, de modo que o
   achado específico ("falta de ar súbita") pese mais do que o genérico ("falta de ar").
5. **Sugere** a doença de maior pontuação e lista as demais como outras hipóteses.

### 4.4 Resultado nas 10 frases

| Paciente | Sintomas identificados | Diagnóstico sugerido | Outras hipóteses |
|---|---|---|---|
| 01 | dor no peito, piora quando faço esforço, melhora quando paro | **Angina** | Infarto |
| 02 | cansaço constante, tornozelos inchados | **Insuficiência cardíaca** | — |
| 03 | aperto no tórax, dor que irradia para o braço esquerdo, suor frio | **Infarto agudo do miocárdio** | — |
| 04 | palpitações, coração disparado, tontura | **Arritmia cardíaca** | — |
| 05 | dor na nuca, visão embaçada, sangramento no nariz | **Hipertensão arterial** | — |
| 06 | dor aguda no peito, piora ao deitar, melhora quando me inclino para frente, febre baixa (negado: falta de ar) | **Pericardite** | Miocardite |
| 07 | dor na panturrilha ao caminhar, pés frios | **Doença arterial periférica** | Embolia pulmonar |
| 08 | falta de ar súbita, dor ao respirar, inchaço em uma perna | **Embolia pulmonar** | Angina, Insuficiência cardíaca |
| 09 | boca torta, fala enrolada, fraqueza em um lado do corpo | **Acidente vascular cerebral** | — |
| 10 | febre persistente, calafrios | **Endocardite** | Miocardite |

**Limitação conhecida:** o extrator só reconhece expressões escritas como no mapa. "Inchaço nas
pernas" é encontrado; "minhas pernas incharam" não. Ampliar o mapa melhora a cobertura, mas não
resolve variação livre de linguagem, que é o que motiva a Parte 2.

---

## 5. Parte 2 — Classificador de risco por texto

### 5.1 Dataset (`frases_risco.csv`)

100 frases no formato `frase,situacao`, **balanceadas** (50 alto risco, 50 baixo risco). Para o
problema não ficar trivial, a base inclui frases de baixo risco que citam termos "graves"
(dor muscular no peito, palpitação isolada após café) e frases de alto risco sem os termos
clássicos (AVC, isquemia de membro, síncope).

### 5.2 Método

- **Vetorização:** `TfidfVectorizer` com unigramas e bigramas, sem acentos e **sem remoção de
  stop words**, porque "não" e "sem" mudam o sentido clínico.
- **Modelo:** Regressão Logística, escolhida por ser interpretável (um coeficiente por termo).
- **Avaliação:** divisão estratificada 75 % treino / 25 % teste, validação cruzada em 5 partes e
  comparação com Árvore de Decisão e Naive Bayes.

### 5.3 Resultados

| Métrica | Valor |
|---|---|
| Acurácia no teste (25 frases) | **92 %** (23 acertos) |
| Precisão / recall para alto risco | 100 % / 84,6 % |
| Alto risco classificado como baixo | 2 casos |
| Validação cruzada — Regressão Logística | 89 % ± 6 % |
| Validação cruzada — Naive Bayes | 89 % ± 2 % |
| Validação cruzada — Árvore de Decisão | 81 % ± 6 % |

Os dois erros do teste foram na direção mais perigosa para triagem: quadros graves descritos
sem as palavras "peito" e "falta de ar".

### 5.4 Padrões e distorções observados

Os coeficientes mostram que o modelo decide por poucos termos: "peito", "falta de ar" e
"de repente" puxam para alto risco; "leve", "um pouco" e "depois de" puxam para baixo risco.
Para medir o efeito disso, o notebook aplica 20 frases novas em quatro testes de estresse:

| Teste | Acerto | O que revela |
|---|---|---|
| Negação ("não tenho dor no peito") | 0 de 5 | TF-IDF conta palavras e ignora o "não" |
| Atenuadores ("um leve aperto no peito") | 2 de 5 | Quem minimiza o sintoma é subtriado |
| Linguagem coloquial | 3 de 5 | Vocabulário fora do treino derruba o modelo |
| Apresentação atípica de infarto | 2 de 5 | Sem "dor no peito", o caso grave vira baixo risco |
| **Total** | **7 de 20 (35 %)** | |

A queda de 92 % para 35 % é o principal achado desta fase: **a acurácia medida em frases
parecidas com as do treino não descreve o comportamento do modelo em uso real.**

---

## 6. Governança de dados e viés

Continuidade dos compromissos assumidos na seção 7.3 da Fase 1.

- **Viés de apresentação clínica.** A apresentação atípica de infarto (cansaço, enjoo, dor nas
  costas ou na mandíbula) é mais frequente em mulheres, idosos e diabéticos. Um triador que
  depende da "dor no peito" clássica erra sistematicamente contra esses grupos, o mesmo
  mecanismo do viés de sexo da base UCI documentado na Fase 1.
- **Viés de linguagem.** As frases foram escritas por uma única pessoa, em um único registro.
  Quem descreve o sintoma de forma coloquial ou regional é pior classificado.
- **Viés de rotulagem.** Os rótulos de risco foram atribuídos pelo grupo, sem validação por
  profissional de saúde.
- **Dado simulado, rotulado como tal.** Nenhuma frase vem de paciente real; não há dado pessoal
  neste repositório.
- **Erros assimétricos.** Em triagem, liberar um caso grave custa mais do que um falso alarme.
  Um uso real exigiria baixar o limiar de decisão para privilegiar a sensibilidade.
- **Decisão final humana.** As duas partes são apoio à priorização, não diagnóstico.

---

## 7. Limitações e próximos passos

1. Ampliar e diversificar a base de frases, com rótulos revisados por profissional de saúde.
2. Tratar negação antes da vetorização na Parte 2, reaproveitando a lógica da Parte 1.
3. Reportar métricas por subgrupo quando houver metadados de sexo e idade.
4. Combinar as duas abordagens: regras para sinais de alarme inequívocos e modelo estatístico
   para o restante.

---

## 8. Referências

- Pedregosa, F. et al. **Scikit-learn: Machine Learning in Python.** JMLR, 2011. https://scikit-learn.org
- Detrano, R. et al. **Heart Disease Data Set.** UCI Machine Learning Repository, 1989 (base da Fase 1).
- Repositório da Fase 1: https://github.com/viscp1011/cardioia-fase1

---

*Fase 2 do projeto CardioIA — FIAP, 2026.*
