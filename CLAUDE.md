# Instruções para o Claude Code

- Este é o site da **Ideal Metrics** (segunda marca do Leandro; reflete os serviços da CQT e acrescenta serviços de emissões de carbono).
- Sempre que fizer qualquer edição em arquivos, faça automaticamente git add, commit com mensagem descritiva em português, e push para o GitHub.
- Nunca pergunte se deve fazer commit, sempre faça automaticamente.
- Repositório: `leandrocentomo-arch/ideal-metrics-site`.
- O site está hospedado no GitHub Pages em https://leandrocentomo-arch.github.io/ideal-metrics-site/
- Visual, layout e fontes seguem o mesmo padrão da CQT (IBM Plex Sans Condensed). O que muda entre as marcas é só o logo e o nome.
- Rodapé legal: IDEAL METRICS LTDA · CNPJ 69.202.916/0001-20 (empresa aberta em 16/09/2026; trocado no site em 18/09/2026). A experiência desde 1998 é da equipe, não do CNPJ: escrever "equipe em atuação desde 1998", nunca "fundada em 1998".
- Arquitetura do site (mapa estratégico v1.1): duas divisões. **Padrões e Conformidade**, com dez temas, e **Estudos e Pesquisa Aplicada**, com quatro. Consultoria, auditoria, inspeção e treinamento são modos de prestar um tema, não temas, e por isso não têm página própria.
- Menu, navegação lateral e colunas do rodapé são copiados página a página. A fonte única é `_ferramentas/blocos.py`; depois de editar, rodar `python _ferramentas/menu.py`. A home tem menu próprio e fica de fora.
- Nunca publicar no site: onde o serviço já aconteceu, nomes de clientes fora da página de clientes, preços, estado comercial de um tema e CNAE.
- PROIBIDO em qualquer texto da marca: o argumento "não emitimos certificado", "quem implanta não certifica" e o diferencial "Independência real". O diferencial é trajetória: equipe em atuação desde 1998.
- Contato (e-mail info@cqt-br.com, WhatsApp e LinkedIn): reaproveitados da CQT por enquanto, até a Ideal Metrics ter canais próprios.
- Mantenha todos os textos em português com acentuação correta.
- As imagens ficam na pasta img/ (logos da Ideal Metrics em `img/ideal-metrics-*.svg`).
- O CSS principal fica em css/style.css.
