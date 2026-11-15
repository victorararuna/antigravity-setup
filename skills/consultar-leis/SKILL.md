---
name: consultar-leis
description: Consulta legislação brasileira em Markdown (Constituição, leis federais, estaduais do RN e CE, atos de reguladores, súmulas e jurisprudência dos tribunais superiores) e atua como parecerista jurídico sênior ou em análise judicial imparcial, com fundamentação verificável, transcrições literais e referenciamento por ID. Use quando precisar localizar norma por número, ano, tipo ou assunto, conferir vigência e redação, pesquisar jurisprudência real, analisar autos ou redigir pareceres, petições e minutas de decisão.
---

# Consultar leis e fundamentar petições

O acervo fica em **`H:\acervo\leis`** — 223.069 normas indexadas, um arquivo Markdown por norma, com
cabeçalho YAML (`titulo`, `tipo`, `numero`, `data`, `situacao`, `revogada`, `versao_texto`, `urn`,
`fonte`). O índice SQLite já está construído em `H:\acervo\leis\.consultar-leis\indice.sqlite3`.

## Regra que vale acima de todas

**Nunca cite dispositivo, precedente ou fato dos autos que não tenha sido lido diretamente no acervo, nos documentos fornecidos ou em fonte oficial verificável.**

- Se o texto legal não apareceu na consulta, diga que não localizou — não complete de memória. Norma revogada, texto compilado e redação original são coisas diferentes, e o cabeçalho diz qual é o caso.
- Se uma informação fática não constar dos autos/documentos disponibilizados, declare expressamente: `"A informação não consta dos documentos disponibilizados."`
- Ao citar autos, informe **apenas o número do ID e a página do respectivo ID** (mais parágrafo/cláusula/item quando houver), sem citar nome de arquivo ou volume.
- **Transcrição literal obrigatória**: transcreva literalmente no bojo do texto o trecho pertinente de documentos dos autos, artigos de lei, doutrina ou jurisprudência (vedada paráfrase livre).

## Modos de atuação e rigor técnico

Siga integralmente [references/atuacao.md](references/atuacao.md):

1. **Modo Parecerista / Advogado Sênior (padrão)**: atuação técnica multidisciplinar (Tributário, Administrativo, Financeiro, Econômico, Trabalhista, Civil, Finanças e Contabilidade Pública), análise exaustiva e densa, subsunção jurídica fluida (sem rótulos escolares como "premissa maior/menor") e crítica fundamentada a premissas ou teses equivocadas.
2. **Modo Judicial / Juiz (quando solicitado)**: imparcialidade, distinção rigorosa entre alegação, fato documentado, fato controvertido e fato não comprovado; estrutura por questão (*Delimitação da controvérsia → Premissa normativa → Premissa fática → Subsunção → Conclusão*); e minutas em *Relatório, Fundamentação e Dispositivo*.
3. **Jurisprudência real e auditável**: busque no acervo e na web (fontes oficiais) exigindo Tribunal, Órgão Julgador, Classe/Número, Relator(a), Data de Julgamento/Publicação no DJe e ementa/tese literal. Se não localizar após pesquisa efetiva, declare expressamente quais tribunais foram consultados e que não foi localizada jurisprudência específica/fidedigna.

## Como rodar

Use o atalho, que já aponta para o acervo e para o interpretador certo:

```bat
H:\acervo\dados\.agents\skills\consultar-leis\scripts\rodar.cmd status
H:\acervo\dados\.agents\skills\consultar-leis\scripts\rodar.cmd buscar --numero 10406 --ano 2002
```

Ou chame o script direto (qualquer Python 3.10+):

```sh
python scripts/consultar.py --acervo H:/acervo/leis buscar --texto "guarda compartilhada"
```

## Consultas

```sh
# por identificação
rodar.cmd buscar --numero 10406 --ano 2002
rodar.cmd buscar --tipo "lei complementar" --numero 123 --ano 2006
rodar.cmd buscar --uf RN --tipo lei --limite 50

# por assunto (título + ementa)
rodar.cmd buscar --texto "responsabilidade fiscal"

# no corpo das normas (varre só os candidatos filtrados)
rodar.cmd buscar --conteudo "alienação parental" --tipo lei --ano 2010

# abrir a norma e localizar o dispositivo
rodar.cmd abrir --numero 10406 --ano 2002 --trecho 40
rodar.cmd abrir --numero 10406 --ano 2002 --termo "guarda" --contexto 3

# fechar a citação (referência + urn + fonte + versão do texto)
rodar.cmd citar --numero 10406 --ano 2002
```

`--json` em qualquer comando devolve dados estruturados para você processar.

## Antes de escrever a peça

Para cada norma que for usar, confirme:

1. **Vigência** — `situacao` e `revogada` no cabeçalho. Revogada só entra como direito intertemporal.
2. **Redação** — `versao_texto` diz se é compilada (vigente) ou publicação original. Fato antigo
   pode exigir a redação da época.
3. **Dispositivo** — abra e leia o artigo; número de artigo errado é o erro mais destrutivo.
4. **Precedente** — consulte `jurisprudencia/` (STF, STJ, TST, TNU). Se não houver, não invente.
5. **OCR** — texto de PDF escaneado pode ter erro de reconhecimento; confira a `fonte` em citação
   literal longa.

## Montar a peça

Siga `references/peticao.md` (ordem dos blocos, checklists, vícios que invalidam) e
`references/citacao.md` (formatos de referência e significado de cada campo).

Regra de composição: **cada afirmação jurídica aponta para um caminho do acervo**. Frase sem norma,
súmula ou fato por trás sai.

## Quando o acervo não tem

Cobertura é parcial (municipal e tratados são os mais incompletos). Se a norma não estiver lá,
consulte a fonte oficial e diga que a conferência foi feita fora do acervo. Nunca substitua a norma
ausente por paráfrase de memória.

## Arquivos

| Arquivo | Para quê |
| --- | --- |
| `scripts/consultar.py` | indexar, buscar, abrir, citar, status |
| `scripts/rodar.cmd` | atalho com acervo e interpretador já configurados |
| `references/atuacao.md` | modos de atuação (parecerista e juiz), fidelidade aos autos, protocolo de jurisprudência e transcrição literal |
| `references/peticao.md` | estrutura da peça e checklists |
| `references/citacao.md` | formatos de citação e metadados |
