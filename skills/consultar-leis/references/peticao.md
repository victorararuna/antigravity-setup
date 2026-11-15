# Estrutura da peça e checklists

Pressuposto: cada afirmação jurídica tem um caminho do acervo por trás. O que não tem, sai.

## Ordem dos blocos

1. **Endereçamento** — juízo competente, por extenso. Competência se confere, não se presume:
   matéria, pessoa, território, valor.
2. **Qualificação** — nome completo, nacionalidade, estado civil, profissão, CPF/CNPJ, endereço,
   e-mail. Para pessoa jurídica: razão social, CNPJ, endereço da sede, representante.
3. **Nome da peça** — "PETIÇÃO INICIAL", "CONTESTAÇÃO", "RECURSO DE APELAÇÃO", "EMBARGOS DE
   DECLARAÇÃO". Nome errado não é vício sanável de graça.
4. **Síntese / fatos** — cronologia verificável, datas e documentos. Sem adjetivo.
5. **Fundamentos** — dispositivo → interpretação → precedente vinculante → (doutrina, opcional).
6. **Pedidos** — certo e determinado, na ordem que o juízo consegue decidir.
7. **Provas** — o que se pretende produzir e por quê.
8. **Valor da causa** — quando exigido, com memória de cálculo.
9. **Fecho** — local, data, assinatura, OAB.

## Fundamentos: a sequência que funciona

1. **Norma constitucional/infralegal** aplicável, com artigo lido no acervo.
2. **Enquadramento do fato** na hipótese da norma — diga qual elemento do suporte fático está
   preenchido e por qual documento.
3. **Precedente vinculante**, se houver: súmula vinculante, tese de repercussão geral ou de
   repetitivo, controle concentrado. Cite a **tese**, não só o número do tema.
4. **Norma revogada** — só para fato anterior à revogação, com a redação da época
   (`versao_texto` da publicação original) e a lei revogadora citada.

## Pedidos: o que derruba a peça

| Vício | Conserto |
| --- | --- |
| Pedido genérico ("que se faça justiça") | Pedido determinado, com valor e base legal |
| Falta de pedido de citação do réu | Incluir, é requisito do art. 319, VII, do CPC |
| Pedido sem fundamento correspondente | Cada pedido aponta para o dispositivo que o sustenta |
| Cumulação sem compatibilidade | Verificar compatibilidade dos pedidos entre si e com o procedimento |
| Valor da causa ausente ou arbitrário | Art. 292 do CPC, com memória de cálculo |
| Tutela de urgência sem os dois requisitos | Art. 300 do CPC: probabilidade do direito **e** perigo de dano, cada um demonstrado |

## Checklists por etapa

**Antes de escrever**

- [ ] Competência definida e conferida (não só "foro do domicílio do réu").
- [ ] Prazo conferido no regimento/lei processual e contado da intimação correta.
- [ ] Prescrição/decadência checada, com a norma e a data do fato.
- [ ] Legitimidade ativa e passiva mapeada (quem assina, quem representa).
- [ ] Documentos indispensáveis reunidos (art. 320 do CPC).

**Ao fundamentar**

- [ ] Cada norma aberta no acervo, com `caminho` anotado.
- [ ] `revogada: true` verificado — nenhuma norma revogada usada como vigente.
- [ ] `versao_texto` conferida contra a data do fato.
- [ ] Número do artigo conferido no texto, não de memória.
- [ ] Súmula/precedente procurado em `jurisprudencia/`; se não estiver lá, buscado na fonte
      oficial e dito de onde veio.
- [ ] Súmula cancelada ou superada não citada como vigente.

**Ao revisar**

- [ ] Toda citação do corpo tem linha correspondente no registro de auditoria.
- [ ] Nenhuma frase jurídica sem dispositivo, súmula ou fato por trás.
- [ ] Pedidos respondem, um a um, aos fundamentos.
- [ ] Nomes, números, datas e valores conferidos contra os documentos.
- [ ] Transcrição literal conferida (OCR pode ter alterado ordinal ou número).

## Onde consultar cada coisa

| Preciso de | Onde está |
| --- | --- |
| Norma constitucional | `constituicao.md`, `federal/emendas-constitucionais/` |
| Lei federal, complementar, delegada | `federal/leis-ordinarias/`, `federal/leis-complementares/`, `federal/leis-delegadas/` |
| Decreto regulamentar | `federal/decretos/`, `federal/decretos-nao-numerados/`, `federal/regulamentos/` |
| Ato de agência (ANVISA, CONTRAN, RFB, BCB…) | `reguladores/<orgao>/` |
| Lei estadual, constituição estadual | `estaduais/<UF>/` |
| Lei municipal, lei orgânica, plano diretor | `municipais/<UF>/<municipio>/` |
| Súmula, tema repetitivo, ADI/ADPF | `jurisprudencia/<tribunal>/` |
| Tratado internalizado | `tratados/` |

## Limites do acervo (diga isso na peça? não; diga ao cliente)

- Cobertura parcial: municipal e tratados são os mais incompletos. `status` mostra o que existe.
- Texto convertido/OCR não substitui o Diário Oficial.
- O acervo não tem jurisprudência de mérito de segunda instância em massa: para tese local, a
  fonte é o site do tribunal.
- Se a norma não estiver no acervo, a peça pode citá-la — mas só depois de lida na fonte oficial,
  e o registro de auditoria aponta a URL oficial em vez do caminho local.
