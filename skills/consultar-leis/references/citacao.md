# Citação e metadados

## O que cada campo do cabeçalho significa

| Campo | Como usar |
| --- | --- |
| `titulo` | Nome oficial da norma como a fonte publica. Use no corpo, não invente epígrafe. |
| `tipo` | Vocabulário fechado (`Lei Ordinária`, `Lei Complementar`, `Decreto`, `Súmula Vinculante`…). Não escreva "Lei Federal 10.406": o tipo é `Lei Ordinária` e a esfera é federal. |
| `numero` | Só dígitos. Formate com separador de milhar na citação (`10406` → `10.406`). |
| `data` | Data da norma (aprovação/publicação conforme a fonte). É ela que entra na referência, não a data do DOU. |
| `data_publicacao` | Data do Diário Oficial, quando a fonte distingue. Use atrás do veículo. |
| `uf` | Ausente em normas federais. Presente em estaduais e municipais — muda a referência. |
| `situacao` | Texto livre da fonte ("Em vigor", "Revogada", "Vetada"). Não trate como certificado: é o que a fonte diz na captura. |
| `revogada` | Booleano do acervo. `true` → só cite como direito intertemporal, dizendo isso. |
| `versao_texto` | **Campo mais importante depois do texto.** "compilada (texto vigente)" ≠ "publicação original". A redação que vale hoje pode não ser a que valia no fato. |
| `publicacao` | Veículo e data como a fonte escreve ("DOU de 11/01/2002"). Reaproveite literalmente. |
| `urn` | Identificador `urn:lex`. Estável, serve para o sistema do tribunal e para deduplicar. |
| `fonte` | URL oficial consultada. Vai no "Disponível em". |
| `baixado_em` | Data da captura no acervo — use como "Acesso em" quando você não consultou a fonte naquele dia. |

## Referência (ABNT NBR 6023, adaptada a norma)

Federal:

```
BRASIL. Lei nº 10.406, de 10 de janeiro de 2002. Institui o Código Civil.
Diário Oficial da União: seção 1, Brasília, DF, 11 jan. 2002.
Disponível em: https://normas.leg.br/?urn=urn:lex:br:federal:lei:2002-01-10;10406.
Acesso em: 14 nov. 2026.
```

Estadual (troque o autor e o veículo):

```
SÃO PAULO. Lei nº 10.000, de 1º de janeiro de 1998. Ementa da norma.
Diário Oficial do Estado de São Paulo, São Paulo, 2 jan. 1998.
```

Municipal:

```
FORTALEZA. Lei nº 1.234, de 5 de março de 2019. Ementa.
Diário Oficial do Município de Fortaleza, Fortaleza, 6 mar. 2019.
```

Súmula:

```
BRASIL. Supremo Tribunal Federal. Súmula Vinculante 11. Só é lícito o uso de algemas
em casos de resistência e de fundado receio de fuga ou de perigo à integridade física
própria ou alheia. Brasília, DF: STF, 2008.
```

Acórdão em controle concentrado:

```
BRASIL. Supremo Tribunal Federal. Ação Direta de Inconstitucionalidade nº 4.277/DF.
Relator: Min. Ayres Britto. Julgamento: 5 maio 2011. Publicação: 14 out. 2011.
```

## Citação no corpo da peça

- Dispositivo: `art. 1.583, caput, do Código Civil` — artigo, parágrafo/inciso/alínea, e o nome
  da lei por extenso na primeira menção; depois, `CC`, `CPC`, `CF`.
- Com alteração: `art. 1.634 do Código Civil, com a redação dada pela Lei nº 13.058/2014`.
- Súmula: `Súmula Vinculante 11 do STF` ou `Súmula 331, item II, do TST`.
- Tema: `Tema 550 da repercussão geral` / `Tema 1.234 dos repetitivos do STJ`.
- Nunca cite artigo "e seguintes" sem ter lido onde termina o bloco.

## Transcrição literal

Ao transcrever, copie do arquivo aberto, preserve a pontuação original e marque a origem:

> "Art. 1.583. A guarda será unilateral ou compartilhada." (BRASIL, 2002, art. 1.583)

Texto vindo de OCR pode ter erro de reconhecimento em ordinais (`19` por `1º`) e em números.
Transcrição longa → confira na `fonte` antes de protocolar.

## Registro de auditoria da peça

Guarde, para cada norma citada, o bloco do `citar --json`:

```json
{"referencia": "...", "urn": "...", "fonte": "...", "versao_texto": "...",
 "data": "...", "caminho": "federal/leis-ordinarias/2002/lei-10406-2002-01-10.md"}
```

`caminho` é o que permite reabrir exatamente o texto que você leu, mesmo depois de o acervo
mudar. Em caso de impugnação da citação, é a sua prova de origem.
