# Instruções para o Claude Code

- Este é o site da **Ideal Metrics** (segunda marca do Leandro; reflete os serviços da CQT e acrescenta serviços de emissões de carbono).
- Sempre que fizer qualquer edição em arquivos, faça automaticamente git add e commit com mensagem descritiva em português.
- Nunca pergunte se deve fazer commit, sempre faça automaticamente.
- **PUSH SÓ QUANDO O LEANDRO PEDIR** (regra de 23/09/2026). Cada push dispara uma reconstrução no Netlify e consome 15 dos 300 créditos mensais do plano grátis; publicar a cada ajuste estourou a cota em dois dias e deixou o domínio parado até a virada do ciclo. Commitar sempre, acumular, e subir quando ele mandar.
- Repositório: `leandrocentomo-arch/ideal-metrics-site`.
- O site está hospedado no GitHub Pages em https://leandrocentomo-arch.github.io/ideal-metrics-site/
- O repositório é PÚBLICO, e precisa ser: no plano gratuito o GitHub Pages só publica repositório público. Tornar privado derruba o site, e voltar a público não religa o Pages sozinho (Settings > Pages, branch `main`, pasta raiz). Por isso só o site de verdade entra no repositório: rascunho, página de teste e artefato interno ficam no disco e no `.gitignore`. Nunca versionar chave, senha, dado de cliente ou proposta.
- As peças da marca em `img/` trocam de conteúdo mantendo o nome, então levam `?v=<data>` na URL para o navegador não servir a versão antiga do cache. A cada troca de logo, mudar esse número em todas as páginas.
- A seção «Conhecimento» da home (esquema por arcos) é gerada: editar `_ferramentas/arcos/arcos.py` e rodar `python _ferramentas/arcos/monta.py site`, que reinsere de forma idempotente. O gerador recusa colisão de pílula, de título e de aro. Não editar o SVG à mão no `index.html`.
- Visual, layout e fontes seguem o mesmo padrão da CQT (IBM Plex Sans Condensed). O que muda entre as marcas é só o logo e o nome.
- Rodapé legal: IDEAL METRICS LTDA · CNPJ 69.202.916/0001-20 (empresa aberta em 16/09/2026; trocado no site em 18/09/2026). A experiência desde 1998 é da equipe, não do CNPJ: escrever "equipe em atuação desde 1998", nunca "fundada em 1998".
- Arquitetura do site (mapa estratégico v1.1): duas divisões. **Padrões e Conformidade**, com dez temas, e **Estudos e Pesquisa Aplicada**, com quatro. Consultoria, auditoria, inspeção e treinamento são modos de prestar um tema, não temas, e por isso não têm página própria.
- Menu do topo, menu do celular, navegação lateral e colunas do rodapé são copiados página a página. A fonte única é `_ferramentas/blocos.py` (uma lista só, `MENU`, para os três menus); depois de editar, rodar `python _ferramentas/menu.py`. Desde 02/10/2026 a home entra na regravação (o menu dela é o mesmo das outras).
- Nunca publicar no site: onde o serviço já aconteceu, nomes de clientes fora da página de clientes, preços, estado comercial de um tema e CNAE.
- PROIBIDO em qualquer texto da marca: o argumento "não emitimos certificado", "quem implanta não certifica" e o diferencial "Independência real". O diferencial é trajetória: equipe em atuação desde 1998.
- Contato (e-mail info@cqt-br.com, WhatsApp e LinkedIn): reaproveitados da CQT por enquanto, até a Ideal Metrics ter canais próprios.
- Mantenha todos os textos em português com acentuação correta.
- As imagens ficam na pasta img/ (logos da Ideal Metrics em `img/ideal-metrics-*.svg`).
- O CSS principal fica em css/style.css.

## Padrões canônicos (definidos pelo Leandro; valem para toda página nova e para toda revisão)

Regra da casa: o que o Leandro corrige numa página vira padrão do site inteiro. Ao receber uma correção, aplicar em todas as páginas que têm o mesmo elemento e registrar aqui.

### Página de serviço
- **Ordem de toda página:** (1) frase de abertura que diz o serviço, maior que o texto (`<p class="abre">`, 22 px, peso 500, na cor do texto); (2) um texto curto, de dois parágrafos no máximo, sobre como o trabalho é feito e o que a organização ganha; (3) os diagramas, em linha fina; (4) o conteúdo em seções. A abertura começa por «A Ideal Metrics ...» e nomeia a norma, não «a norma».
- Vende consultoria, não ensina a norma. Quem entra quer saber se a Ideal Metrics presta o serviço de apoio à implantação para a certificação. Abrir pelo serviço, tópicos de uma linha, parágrafo de uma ou duas frases, sem seção que explique a norma.
- A Ideal Metrics implanta e prepara para a certificação. Nunca escrever «auditoria de certificação» nem algo que sugira que ela audita para certificar.
- Sem palavra de trocadilho com o tema («percurso», «caminho», «ponto de partida») e sem usar o objeto do tema como diagrama. Diagrama em linha fina, como o da página do IFC.
- Credencial sem floreio («Consultores: formação internacional de Auditor Líder (Lead Auditor) em ISO 39001»). Norma de apoio só a que ele usa (na segurança viária, a ISO 39002).
- **Sujeito sempre nomeado:** frase nunca começa por pronome («Ela organiza...», «Ele estabelece...») nem com o sujeito oculto que retoma a frase anterior («... no mundo. Organiza processos...»). Escrever o sujeito, e o sujeito é o sistema, não «a norma»: «Um sistema de gestão da qualidade traz processos organizados, menos retrabalho e menos falhas...» (correções de 02/10/2026).
- Nunca «auditoria de certificação», nem como «preparação para a auditoria de certificação»: escrever «preparação para a certificação».
- **Faixa do topo (banner):** o título é o tema da gestão e o subtítulo é a norma. «Gestão da Qualidade» / «ISO 9001»; «Gestão Ambiental» / «ISO 14001»; «Gestão da Saúde e Segurança Ocupacional» / «ISO 45001»; «Gestão da Segurança Viária» / «ISO 39001»; «Gestão da Segurança de Alimentos» / «ISO 22000 · FSSC 22000». O `<title>` vira «Tema | Norma | Ideal Metrics» e a trilha usa o tema (combinado em 02/10/2026).
- Título de seção «Aplicação», não «Para quem é». Título da página de segurança viária: «Gestão da Segurança Viária», não «de».
- Molde: `seguranca-viaria.html`, gerada por `_ferramentas/pagina_viaria.py`.
- **Página nova entra no menu na mesma entrega, sem ele pedir.** Com norma, o rótulo leva tema e norma na mesma linha: «Qualidade · ISO 9001», «Segurança viária · ISO 39001». Sistema de gestão ISO fica em «Sistemas de gestão». Editar `MENU` em `_ferramentas/blocos.py` e rodar `python _ferramentas/menu.py` (regrava menu do topo, do celular e lateral em todas as páginas, home incluída); depois `cp index.html index-azul.html` e `python _ferramentas/busca.py`. Entra também no card de `servicos.html`.

### Fotos
- Tingimento azul oficial do site, tom padrão em `_ferramentas/tom_azul.json` (brilho 0,35, gama 0,88, contraste 1,55, escuro 0,35, véu 0,12). O banner das páginas internas tem o tom dele (0,35 · 0,86 · 1,55), salvo `data-tom`.
- Toda foto posta no site leva o efeito de mouse (motor `ditherVivo`, `pincel:.7, zoomHover:1.035`).
- Foto de tema de infraestrutura: aérea, aberta, a obra enchendo o quadro, sem gente, fora de área urbana e sem mato dominando. Imagem nova ou edição: Google Flow.
- Banner: passagem suave da foto para o creme. Foto, enquadramento e tom saem da aba [ 08 ] do Spirit; a receita colada vira o arquivo por `_ferramentas/banner/foto_banner.py --receita` (banner) ou `_ferramentas/foto_azul.py --receita` (foto do corpo da página).
- ODS da ONU: ícones oficiais em português, sem alteração, com clique que abre meta e indicador, e o aviso de uso da ONU.

### Layout
- **Card:** solto, nunca colado no vizinho nem separado por fio; borda fina própria `rgba(20,48,76,.14)`, canto de 3 px, vão de 8 px na grade. Classes que seguem: `.ifc-cel`, `.pos-card`, `.numbered-item`, `.cl-cel` da home. O acordeão de serviços e a malha de notícias da home não são cards.
- **Entrelinha:** texto que quebra sozinho dentro de card, 1,35; título de card, 1,25. O espaço entre título e texto (o «enter») não muda. Texto corrido da página, 1,5.
- **Espaçamento:** seção a seção, 56 px até o fio (`.section-divider`) e 44 px do fio ao título; título de seção (`.content h3`) a 44 px do bloco de cima; `h2` a 56 px. Bloco (grade de cards, fotos, números, figura, ícones) até o texto ou o bloco seguinte: 28 px. A linha de fonte fica colada nos números e a 28 px da lista que vem depois.
- **Cor do texto:** o escuro da Ideal Metrics, `#14304C` (`--text-light`), no texto corrido, nas listas, nos cards, na abertura e na navegação lateral (era `#315275`). Rótulos e títulos pequenos de seção continuam em `--mid-gray`.
- **Título da faixa:** entrelinha 1,04 (era 1,16), para o título de duas linhas ficar junto.
- **Monograma (cartão do topo e rodapé):** o pássaro do 18Asset 13 a 88% e centrado sobre o «ideal·m™», o nome intacto (02/10/2026, «repare que no logo que eu coloquei o pássaro é menor»). Grupo `#passaro-proporcao` em `img/monograma-ideal-m-limpo.svg` e `img/monograma-ideal-m.svg`.
- Canto de 3 px em campo, botão e card.
- **Rodapé:** 352 px de branco entre o fim do conteúdo e o rodapé (`.page-layout`, padding de baixo).
- **Diagrama:** SVG em linha fina com `viewBox` de 900 de largura (a coluna de texto tem ~890 px), para o texto do desenho sair no tamanho de leitura. Desenho mais largo encolhe a letra.
- CSS novo: subir `css/style.css?v=` em todas as páginas.
