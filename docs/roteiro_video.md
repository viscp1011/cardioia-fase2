# Roteiro do vídeo de demonstração (até 4 minutos)

Gravação de tela com narração. Sugestão: OBS Studio ou a gravação do Windows (Win + Alt + R).
Deixe abertos antes de gravar: o repositório no GitHub, o terminal na pasta do projeto e o
notebook já executado.

| Tempo | Tela | Fala |
|---|---|---|
| 0:00 – 0:20 | README no GitHub | "Sou Vitorio Paciulo, Grupo 88. Esta é a Fase 2 do CardioIA: diagnóstico automatizado por texto. São duas partes: um extrator de sintomas por regras e um classificador de risco com TF-IDF." |
| 0:20 – 0:50 | `sintomas_pacientes.txt` e `mapa_conhecimento.csv` | "Na Parte 1 escrevi 10 relatos de pacientes, cada um com o sintoma, quando começou e o impacto na rotina. O mapa de conhecimento tem 43 linhas e relaciona pares de expressões a 12 doenças cardiovasculares." |
| 0:50 – 1:40 | Terminal: `python parte1_extracao_sintomas/extrair_sintomas.py` | "O script normaliza o texto, procura as expressões do mapa e pontua cada doença. Expressões mais específicas valem mais. No paciente 1, dor no peito que piora ao esforço e melhora ao parar sugere angina, com infarto como segunda hipótese. No paciente 6, o script percebe que 'não tenho falta de ar' é uma negação e não conta esse sintoma." |
| 1:40 – 2:10 | Notebook, seções 1 e 2 | "Na Parte 2 montei 100 frases rotuladas, 50 de alto e 50 de baixo risco. O TF-IDF transforma cada frase em um vetor. Mantive as stop words porque 'não' e 'sem' mudam o sentido clínico." |
| 2:10 – 2:50 | Notebook, seções 3 e 4 | "Treinei uma Regressão Logística com 75 frases e testei com 25. A acurácia foi de 92 %, e na validação cruzada 89 %. Os dois erros foram casos de alto risco classificados como baixo, o erro mais grave em triagem." |
| 2:50 – 3:40 | Notebook, seções 5 e 6 | "Os coeficientes mostram que o modelo se apoia em poucas palavras, como 'peito' e 'leve'. Por isso criei testes de estresse: com negação ele erra as 5 frases, e em sintomas atípicos de infarto, mais comuns em mulheres, acerta só 2 de 5. No total, 35 % de acerto. É o mesmo viés que apontei na base da Fase 1." |
| 3:40 – 4:00 | Notebook, seção 7 | "Conclusão: a acurácia sozinha esconde distorções. Antes de qualquer uso real seria preciso ampliar a base, tratar negação, priorizar sensibilidade e manter a decisão final com um profissional. Obrigado." |

## Depois de gravar

1. Enviar ao YouTube com visibilidade **Não listado**.
2. Colar o link na seção "Vídeo de demonstração" do `README.md`.
3. Fazer commit e push dessa alteração antes de entregar o link do repositório na FIAP.
