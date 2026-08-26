# Skills aplicadas ao site da Ideal Metrics

Guia prático das skills instaladas, escrito para este site especificamente. Levantado em 26/08/2026.

---

## Antes de tudo: três fatos deste repositório

**1. Toda edição vira commit e push automático.**
O `CLAUDE.md` deste repositório manda: *"Sempre que fizer qualquer edição em arquivos, faça automaticamente git add, commit e push. Nunca pergunte."*

Consequência que muda como usar as skills: **qualquer skill que escreva arquivo publica no ar na hora.** O site está em `https://leandrocentomo-arch.github.io/ideal-metrics-site/`. Não existe rascunho.

Por isso a regra abaixo, que é o macete mais importante deste documento:

> **Use primeiro as skills que só leem. Só depois as que escrevem.**

**2. São 37 páginas HTML dividindo um único `css/style.css` de 3.493 linhas.**
Mexer no CSS atinge as 37 de uma vez. Audite em uma página, aplique no CSS, confira em duas ou três.

**3. Existem duas paletas convivendo no CSS.**
A original e uma segunda, comentada como *"Hero Refined — Corporate palette"*:

| Original | Hero Refined |
|---|---|
| `--blue-medium: #7190AB` | `--color-primary: #0B1D33` |
| `--dark-gray: #3D394A` | `--color-primary-light: #152E4A` |
| `--mid-gray: #50687B` | `--color-accent: #B8952A` |
| `--accent-red: #EF4545` | `--color-accent-light: #D4B04A` |
| `--light-gray: #D1DEE8` | `--color-text: #1A1A2E` |

Isso é dívida de design, não decisão. Resolver qual vale é o primeiro trabalho a fazer, e há uma skill para exatamente isso (ver `distill` abaixo).

Tipografia real em uso: **IBM Plex Sans Condensed** no texto e **IBM Plex Mono** nos detalhes.

---

## As que só leem: comece por aqui

Nenhuma destas altera arquivo. Rode à vontade.

### `/taste <url>` — engenharia reversa de um site que você admira

Abre o site num navegador real e devolve dois arquivos: o **Design Map** com as medidas (hex, escala tipográfica, espaçamentos, raios, sombras, grid) e o **Taste DNA**, que explica cada escolha no formato Gatilho → Decisão → Razão → Evidência.

**Macete:** rode também **no próprio site da Ideal Metrics**. Comparar o inventário dele com o de uma referência mostra a distância em número, não em opinião.

```
/taste https://leandrocentomo-arch.github.io/ideal-metrics-site/
```

Ela pergunta a plataforma de destino e se quer uma página só ou 2 a 3 ligadas. Para referência externa, peça 3 páginas: home, um serviço e o contato. É onde a coerência aparece ou se quebra.

Requer o Playwright MCP, que já está instalado.

### `/impeccable audit` e `/impeccable critique`

`audit` aponta defeito concreto. `critique` discute direção. As duas são leitura.

```
/impeccable audit gestao-carbono.html
/impeccable critique index.html
```

**Macete:** não rode nas 37 páginas. Rode em três representativas (a home, uma de serviço, e a de contato) e trate o resultado como diagnóstico do sistema, porque o CSS é compartilhado.

### `find-animation-opportunities`

Varre e diz onde falta movimento, **e onde não deveria ter**. A segunda metade vale mais que a primeira.

### `improve-animations` e `review-animations`

`improve-animations` audita todo o movimento do código e devolve plano priorizado. `review-animations` critica uma animação específica contra um padrão rigoroso.

**Macete:** `improve-animations` é read-only por design, ela planeja e não aplica. É a forma segura de saber o tamanho do trabalho antes de autorizar qualquer edição num repositório que publica sozinho.

### `animation-vocabulary`

Glossário reverso. Você descreve o efeito e ela dá o nome exato.

> "aquele pulinho quando o menu abre" → **Pop in**
> "aquele elástico quando chega no fim da rolagem" → **Rubber-banding**

**Macete:** use antes de me pedir animação. Pedir "Pop in de 180 ms com ease-out" produz resultado muito melhor que "faz aparecer bonitinho".

---

## As que escrevem: só depois de decidir a direção

### `/impeccable prototype` e a skill `prototype`

Constrói **várias versões genuinamente diferentes** da mesma peça, atrás de um seletor para você alternar lado a lado.

**Macete:** é a melhor ferramenta para as decisões que ainda estão abertas neste site. Em vez de eu entregar uma home e você reagir, ela entrega três direções comparáveis. Numa marca nova, comparar é mais produtivo que aprovar no escuro.

### `/impeccable craft`

Constrói interface do zero, com opinião forte.

### `/impeccable polish`

Acabamento fino no que já existe.

### `/impeccable distill`

Tira o excesso. **É a indicada para o problema das duas paletas.** Ela força a escolha em vez de deixar as duas convivendo.

### `/impeccable bolder` e `/impeccable quieter`

Sobem ou baixam o tom visual com uma palavra. Úteis quando o resultado está quase certo e falta calibrar intensidade.

### `/impeccable typeset`, `colorize`, `layout`, `animate`

Recortes por dimensão: tipografia, cor, estrutura, movimento. Preferíveis ao `polish` genérico quando você sabe o que quer atacar.

### `animate` (Emil Kowalski)

Constrói a animação decidindo na ordem que importa: se deve animar, com que propósito, qual propriedade, qual curva, qual duração, como interrompe e como sai.

### `emil-design-eng`

A filosofia por trás: polimento, design de componente, e os detalhes invisíveis. **Macete:** invoque junto com `craft` ou `polish`, para o resultado sair com acabamento em vez de só estrutura.

### `apple-design`

Princípios de interface e movimento físico da Apple, traduzidos para web. Útil para gesto, rolagem, profundidade e tipografia ótica.

---

## Fora do design, mas que servem a este site

### `humanizer`

Tira marcas de texto gerado por IA. Detecta adjetivo vago, tríade decorativa, voz passiva, travessão em excesso, abertura formulaica.

**Macete:** rode em todo texto de página antes de publicar. Ela cobre exatamente as regras de escrita que você já exige, e pega o que passa despercebido.

### `defuddle`

Extrai o conteúdo limpo de uma página web em markdown, sem menu e sem rodapé.

**Macete:** use para ler a página de um concorrente antes de escrever a sua. Custa uma fração do que custa carregar a página inteira.

### `graphify`

Já existe uma pasta `graphify-out/` neste repositório. Ela responde pergunta sobre estrutura e relação entre arquivos sem abrir cada um.

**Macete:** com 37 páginas, pergunte a ela "quais páginas usam o componente X" em vez de eu varrer o repositório.

### `mermaid` e `design-doc-mermaid`

Diagramas. Servem para o material de apoio dos serviços de carbono, não para o site em si.

### `pdf-creator` e `ppt-creator`

Para proposta e apresentação, fora do site.

---

## Sequência recomendada para uma frente de trabalho

1. **`/taste`** em duas ou três referências, mais no próprio site. Você sai com vocabulário e números
2. **`/impeccable audit`** em três páginas representativas. Você sai com a lista de defeitos
3. **`/impeccable distill`** para resolver as duas paletas. Sem isso, todo o resto é construído sobre base ambígua
4. **`prototype`** nas telas onde a direção ainda está aberta
5. **`craft`** ou **`polish`** na direção escolhida, com `emil-design-eng` junto
6. **`animate`** só depois que a estrutura estiver aprovada
7. **`find-animation-opportunities`** no fim, para ver o que falta
8. **`humanizer`** em todo o texto antes de publicar

---

## Cuidados

**A opinião delas não é a sua marca.** A `impeccable` e as do Emil têm direção própria e forte. A Ideal Metrics já tem tipografia, cor e tratamento de foto definidos. Rode `audit` e `critique` antes de `craft` e `polish`, e trate a sugestão como proposta, não como ordem.

**O tratamento das fotos é regra fechada.** Toda foto do site passa pelo filtro da marca: preto e branco com tint `#8999B1`, curva `(180→248)`. Ferramentas em `Ideal Metrics/_tingir-fotos/`. Nenhuma skill sabe disso. Se alguma sugerir foto colorida, está errada.

**O rodapé legal ainda é da CQT.** CNPJ `02.569.436/0001-21`, CENTOMO & CONSULTORES LTDA. Trocar quando a Ideal Metrics tiver CNPJ próprio. Contato também é reaproveitado da CQT.

**Considere criar um `DESIGN.md`.** A `impeccable` tem o comando `/impeccable init`, que lê o projeto e monta um arquivo de contexto de design. Alimentado com os tokens reais deste site, ele faz todas as skills trabalharem dentro da sua identidade em vez da opinião delas. É o investimento com melhor retorno antes de começar.

---

## Inventário completo

Skills instaladas em `~/.claude/skills/`, 27 no total:

`animate` · `animation-vocabulary` · `apple-design` · `defuddle` · `design-doc-mermaid` · `emil-design-eng` · `find-animation-opportunities` · `frontend-design` · `graphify` · `humanizer` · `impeccable` · `improve-animations` · `interface-design` · `json-canvas` · `mermaid` · `mermaid-tools` · `notebooklm` · `obsidian-bases` · `obsidian-cli` · `obsidian-markdown` · `pdf-creator` · `ppt-creator` · `prototype` · `review-animations` · `task-observer` · `taste` · `ui-designer`

As `obsidian-*` valem para o vault, não para este site.

A `impeccable` foi instalada **sem os hooks**, que rodariam um processo a cada edição de arquivo e fariam chamadas de rede. Você tem os 29 comandos, sem execução em segundo plano.
