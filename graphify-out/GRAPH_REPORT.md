# Graph Report - Ideal Metrics/ideal-metrics-site  (2026-07-11)

## Corpus Check
- 45 files · ~137,809 words
- Verdict: corpus is large enough that graph structure adds value.

## Summary
- 72 nodes · 110 edges · 9 communities
- Extraction: 93% EXTRACTED · 7% INFERRED · 0% AMBIGUOUS · INFERRED: 8 edges (avg confidence: 0.81)
- Token cost: 0 input · 323,695 output

## Community Hubs (Navigation)
- Gestão de Carbono
- Núcleo do Site & Serviços
- Home & Posicionamento
- Sistemas ISO & Setores
- ESG & SMETA
- Segurança de Alimentos
- SST & Energia

## God Nodes (most connected - your core abstractions)
1. `Page: Todos os Serviços` - 14 edges
2. `Página Inicial (index.html)` - 11 edges
3. `css/style.css (shared site stylesheet v29)` - 11 edges
4. `Gestão de Carbono (hub)` - 9 edges
5. `Page: SEDEX/SMETA` - 8 edges
6. `Page: Segurança de Alimentos` - 7 edges
7. `Page: STAL Homepage (Mulish/Roboto alt design)` - 7 edges
8. `Page: Normas Regulamentadoras / Apoio Técnico` - 6 edges
9. `Page: ISO 45001 (Ideal Metrics)` - 5 edges
10. `Page: Padrões de Mercado` - 5 edges

## Surprising Connections (you probably didn't know these)
- `Página Inicial variante Swiss (index-swiss.html)` --semantically_similar_to--> `Página Inicial (index.html)`  [INFERRED] [semantically similar]
  index-swiss.html → index.html
- `Page: Setor Alimentos` --semantically_similar_to--> `Page: Segurança de Alimentos`  [INFERRED] [semantically similar]
  setor-alimentos.html → seguranca-alimentos.html
- `Page: Suporte ao sistema de gestão` --references--> `css/style.css (shared site stylesheet v29)`  [INFERRED]
  suporte.html → servicos.html
- `Ideal Metrics site — Claude Code instructions` --rationale_for--> `Página Inicial (index.html)`  [INFERRED]
  CLAUDE.md → index.html
- `Page: Todos os Serviços` --references--> `IATF 16949 (Automotive Quality)`  [EXTRACTED]
  servicos.html → setor-industria.html

## Import Cycles
- None detected.

## Hyperedges (group relationships)
- **Hub Gestão de Carbono e 8 páginas dedicadas** — gestao_carbono, carbono_inventario_gee, carbono_pegada_produto, carbono_neutralizacao, carbono_descarbonizacao, carbono_creditos, carbono_mercado_regulado, carbono_agro [EXTRACTED 1.00]
- **Normas de contabilização de carbono** — gestao_carbono_ghg_protocol, gestao_carbono_iso_14064_1, gestao_carbono_iso_14067, gestao_carbono_iso_14068_1 [INFERRED 0.85]
- **SGI — Integrated Management System (ISO 9001+14001+45001)** — iso_9001, iso_14001, iso_45001, sgi [EXTRACTED 1.00]
- **Food Safety standards cluster** — iso_22000, fssc_22000, haccp_appcc, seguranca_alimentos [EXTRACTED 0.95]
- **Shared page template (stylesheet + nav script)** — css_style, js_site_nav, servicos [INFERRED 0.85]

## Communities (9 total, 0 thin omitted)

### Community 0 - "Gestão de Carbono"
Cohesion: 0.15
Nodes (18): Carbono no Agronegócio, Créditos de Carbono, Descarbonização e Metas, Inventário de GEE, SBCE e CBAM (mercado regulado), Carbono Neutro, Pegada de Carbono de Produto, Gestão de Carbono (hub) (+10 more)

### Community 1 - "Núcleo do Site & Serviços"
Cohesion: 0.30
Nodes (14): css/style.css (shared site stylesheet v29), GHG Protocol (Greenhouse Gas inventory / carbon footprint), Page: ISO 45001 (Ideal Metrics), Page: ISO 9001 (Ideal Metrics), Normas Regulamentadoras (NRs, Brazilian OHS regs), Page: Normas Regulamentadoras / Apoio Técnico, Page: Padrões de Mercado, Page: Mensuração de Carbono (+6 more)

### Community 2 - "Home & Posicionamento"
Cohesion: 0.17
Nodes (13): Conteúdo de destaque (blog), Ideal Metrics site — Claude Code instructions, Clientes de destaque, Como trabalhamos, Independência: quem implanta não certifica, Contato, Ideal Metrics (brand), Implantação normas ISO (+5 more)

### Community 3 - "Sistemas ISO & Setores"
Cohesion: 0.20
Nodes (10): IATF 16949 (Automotive Quality), ISO 14001 (Environmental Management), ISO 27001 (Information Security), ISO 9001 (Quality Management), Page: Setor Indústria, Page: Setor Logística, Page: Setor Saúde, Page: Setor Tecnologia (+2 more)

### Community 4 - "ESG & SMETA"
Cohesion: 0.60
Nodes (5): ESG, SEDEX (Supplier Ethical Data Exchange), Page: SEDEX/SMETA, Page: SEDEX/SMETA Roteiro Completo (SMETA 7.0), SMETA (Sedex Members Ethical Trade Audit)

### Community 5 - "Segurança de Alimentos"
Cohesion: 0.70
Nodes (5): FSSC 22000 Ver. 6 (GFSI-recognized food safety scheme), HACCP / APPCC (Hazard Analysis Critical Control Points), ISO 22000:2019 (Food Safety Management), Page: Segurança de Alimentos, Page: Setor Alimentos

### Community 6 - "SST & Energia"
Cohesion: 0.67
Nodes (3): ISO 45001 (Occupational Health & Safety), ISO 50001 (Energy Management), Page: Setor Energia

## Knowledge Gaps
- **18 isolated node(s):** `ideal-metrics-site README`, `Página Inicial variante Swiss (index-swiss.html)`, `Conteúdo de destaque (blog)`, `Clientes de destaque`, `Contato` (+13 more)
  These have ≤1 connection - possible missing edges or undocumented components.

## Suggested Questions
_Questions this graph is uniquely positioned to answer:_

- **Why does `Página Inicial (index.html)` connect `Home & Posicionamento` to `Gestão de Carbono`, `ESG & SMETA`?**
  _High betweenness centrality (0.570) - this node is a cross-community bridge._
- **Why does `ESG` connect `ESG & SMETA` to `Núcleo do Site & Serviços`, `Home & Posicionamento`?**
  _High betweenness centrality (0.462) - this node is a cross-community bridge._
- **Why does `Page: Todos os Serviços` connect `Núcleo do Site & Serviços` to `Sistemas ISO & Setores`, `ESG & SMETA`, `Segurança de Alimentos`?**
  _High betweenness centrality (0.457) - this node is a cross-community bridge._
- **Are the 2 inferred relationships involving `Página Inicial (index.html)` (e.g. with `Ideal Metrics site — Claude Code instructions` and `Página Inicial variante Swiss (index-swiss.html)`) actually correct?**
  _`Página Inicial (index.html)` has 2 INFERRED edges - model-reasoned connections that need verification._
- **What connects `ideal-metrics-site README`, `Página Inicial variante Swiss (index-swiss.html)`, `Conteúdo de destaque (blog)` to the rest of the system?**
  _18 weakly-connected nodes found - possible documentation gaps or missing edges._