/* js/trama.js: o motor da trama Bayer ao vivo, tirado do index.html em 22/09/2026
   para as paginas internas (banner) usarem o mesmo efeito. A home carrega este
   arquivo e mantem so as chamadas por peca. Expoe window.ditherVivo. */
/* ===== trama Bayer AO VIVO, com trilha do mouse ==============================
   O mecanismo e o de oci.madebybuzzworthy.com, lido no codigo deles (three.js la,
   WebGL puro aqui): a foto entra como LUMINANCIA e o fragment shader faz o dither
   ordenado por pixel de DISPOSITIVO. Uma segunda textura, a TRILHA, guarda por
   onde o ponteiro passou: um segmento de reta carimbado entre a posicao anterior
   e a atual, com forca proporcional a velocidade, decaindo a cada quadro. Onde a
   trilha esta acesa o shader engrossa a celula da luminancia (3,2x; no OCI sao
   7,7x, que numa coluna estreita vira quadriculado grande demais), troca a
   matriz 4x4 pela 8x8 e desloca o limiar. A foto nao e deslocada nem desfocada:
   ela e RE-TRAMADA. Os numeros da trilha sao os deles, reescalados da altura da
   janela (900) para a altura da peca.

   Por que isto serve melhor a Ideal Metrics que o fluido que havia aqui: o fluido
   deslocava uma foto JA tramada, e deslocar reamostra, o que borrava o ponto de
   1 px justamente onde o efeito acontecia. Agora a trama nasce no shader: o ponto
   sai cravado em 1 px de dispositivo em qualquer DPR e em qualquer largura de
   coluna, com ou sem mouse. A receita e a MESMA da casa, conta por conta: gama
   0,86, sigmoide de contraste 1,55, brilho +0,35, quatro niveis, limiar de Bayer
   (m+0,5)/n2 e as quatro cores da rampa creme nos indices 0, 85, 170 e 255.

   HOVER DA TIRA: a chapa de creme que clareia a coluna (12% em repouso, 88% no
   hover) mudou de lugar, do CSS para o shader. No CSS ela cobria a coluna inteira
   com desfoque, e como trilha e chapa moram no mesmo gesto, a chapa apagava
   exatamente o que o mouse acabava de desenhar. No shader a chapa cede ate 60%
   onde a trilha passa: a coluna vira papel para se ler, e a foto reaparece,
   re-tramada em celula grossa, no caminho do ponteiro.

   Sem WebGL, em file:// (o navegador recusa foto local como textura), em ponteiro
   grosso ou com prefers-reduced-motion, nada disto roda e ficam as <img> ja
   tramadas e a chapa de vidro do CSS, que continuam no arquivo para isso. */
(function(){
  if(!window.matchMedia('(pointer:fine)').matches) return;
  if(window.matchMedia('(prefers-reduced-motion: reduce)').matches) return;
  if(location.protocol === 'file:') return;

  /* `#dv-direto` na URL pula a revelacao: serve para fotografar o estado final */
  var DIRETO = /dv-direto/.test(location.hash);

  var VERT = 'attribute vec2 p;void main(){gl_Position=vec4(p,0.,1.);}';

  var FRAG_TRILHA =
    'precision highp float;' +
    'uniform sampler2D t;uniform vec2 res;uniform vec2 pt;uniform vec2 ptAnt;uniform float aspecto;' +
    'uniform float vel;uniform float raio;uniform float borda;uniform float fica;' +
    'float segmento(vec2 p, vec2 a, vec2 b, float r, float bd){' +
    '  p.x*=aspecto; a.x*=aspecto; b.x*=aspecto;' +
    '  vec2 pa=p-a, ba=b-a; float d=dot(ba,ba);' +
    '  float h = d>1e-9 ? clamp(dot(pa,ba)/d,0.,1.) : 0.;' +
    '  return smoothstep(r+bd, r-bd, length(pa-ba*h));}' +
    'void main(){' +
    '  vec2 uv = gl_FragCoord.xy/res;' +
    '  float c = texture2D(t, uv).r;' +
    '  c += segmento(uv, ptAnt, pt, raio, borda) * vel;' +
    '  c *= fica;' +
    '  gl_FragColor = vec4(vec3(clamp(c,0.,1.)),1.);}';

  var FRAG_FOTO =
    'precision highp float;' +
    'uniform sampler2D uLum;uniform sampler2D uTrilha;uniform sampler2D uB4;uniform sampler2D uB8;' +
    'uniform vec2 uTela;uniform vec4 uCol;uniform vec2 uTex;uniform float uAx;uniform float uEspelha;uniform float uZoom;' +
    'uniform float uTempo;uniform vec3 uC0;uniform vec3 uC1;uniform vec3 uC2;uniform vec3 uC3;uniform vec3 uCreme;' +
    'uniform float uGama;uniform float uCtr;uniform float uBrilho;' +
    'uniform float uPix;uniform float uPixMul;uniform float uTrailMul;uniform float uBias;uniform float uBiasReacao;' +
    'uniform float uRespiro;uniform float uLava;uniform float uRevela;uniform float uOpac;' +
    /* 22/09: uSoFigura > 0 -> a trilha do mouse so vale onde a imagem TEM figura.
       Na vaga da piramide o branco em volta acendia com o cometa e desenhava a
       quina do retangulo; com isto o cometa anda sobre os bonecos e some no
       branco. O corte e no tom JA revelado, medido na celula parada. */
    'uniform float uSoFigura;' +
    /* ruido de valor: bem mais barato que o Perlin 3D do OCI e, na amplitude em
       que entra (3% do limiar), indistinguivel dele */
    'float h(vec3 p){return fract(sin(dot(p, vec3(127.1,311.7,74.7)))*43758.5453);}' +
    'float ru(vec3 p){vec3 i=floor(p), f=fract(p); f=f*f*(3.-2.*f);' +
    '  return mix(mix(mix(h(i),h(i+vec3(1,0,0)),f.x),mix(h(i+vec3(0,1,0)),h(i+vec3(1,1,0)),f.x),f.y),' +
    '             mix(mix(h(i+vec3(0,0,1)),h(i+vec3(1,0,1)),f.x),mix(h(i+vec3(0,1,1)),h(i+vec3(1,1,1)),f.x),f.y),f.z);}' +
    'float tom(float g){' +
    '  float v = clamp(pow(max(g,0.), uGama), 1e-6, 1.-1e-6);' +
    '  float a = pow(v,uCtr), b = pow(1.-v,uCtr);' +
    '  return clamp(a/(a+b) + uBrilho, 0., 1.);}' +
    'void main(){' +
    '  vec2 frag = gl_FragCoord.xy;' +
    '  float tr = clamp(texture2D(uTrilha, frag/uTela).r * uTrailMul, 0., 1.);' +
    /* object-fit cover, nas mesmas contas de baixo, para medir o tom parado */
    '  float aC0 = uCol.z/uCol.w, aT0 = uTex.x/uTex.y; vec2 sc0 = vec2(1.), of0 = vec2(0.);' +
    '  if(aT0>aC0){ float s=aC0/aT0; sc0.x=s; of0.x=(1.-s)*uAx; } else { float s=aT0/aC0; sc0.y=s; of0.y=(1.-s)*.5; }' +
    '  if(uSoFigura > .5){' +
    '    vec2 q1 = (floor((frag - uCol.xy)/max(uPix,1.))+.5)*max(uPix,1.);' +
    '    vec2 p1 = q1/uCol.zw; if(uEspelha>.5) p1.x = 1.-p1.x; p1 = (p1-.5)/uZoom + .5;' +
    '    float v1 = tom(texture2D(uLum, clamp(p1*sc0+of0, 0., 1.)).r);' +
    '    tr *= 1. - smoothstep(.90, .995, v1);' +
    '  }' +
    /* a celula da luminancia engrossa com a trilha, em px de DISPOSITIVO e
       ancorada no canto da peca, para o quadriculado nao escorregar */
    '  float px = mix(uPix, uPix*uPixMul, tr);' +
    '  vec2 q = (floor((frag - uCol.xy)/px)+.5)*px;' +
    '  vec2 p = q/uCol.zw;' +
    '  if(uEspelha>.5) p.x = 1.-p.x;' +
    '  p = (p-.5)/uZoom + .5;' +
    /* object-fit: cover, com a ancora X da peca */
    '  vec2 sc = sc0, of = of0;' +
    '  float v = tom(texture2D(uLum, clamp(p*sc+of, 0., 1.)).r);' +
    /* limiar: 4x4 em repouso, 8x8 onde a trilha passa de meio, como no OCI */
    '  float T = tr < .5 ? texture2D(uB4, (floor(frag)+.5)/4.).r : texture2D(uB8, (floor(frag)+.5)/8.).r;' +
    '  float n = ru(vec3(frag/uTela.y*2.6, uTempo*.11)) - .5;' +
    '  float bias = uBias + n*uRespiro + uBiasReacao*tr;' +
    '  float k = clamp(floor((v - bias)*3. + T), 0., 3.);' +
    '  vec3 c = k<.5 ? uC0 : (k<1.5 ? uC1 : (k<2.5 ? uC2 : uC3));' +
    /* a chapa de creme do hover, que cede onde a trilha passa */
    '  c = mix(c, uCreme, uLava*(1. - uRevela*tr));' +
    '  gl_FragColor = vec4(c, uOpac);}';

  var PINCEL_GERAL = .5;   /* tamanho do cometa do mouse em todas as pecas; ver o uso */
  var RASTRO_GERAL = 1;    /* comprimento da cauda do cometa em todas as pecas; 22/09: de 0,4 para 1, «mais longo, nao mais largo» */
  var RAIO_GERAL = .8, BORDA_GERAL = .3;   /* espessura do cometa; ver o uso */

  /* curvas: as mesmas que o OCI usa no GSAP, em forma fechada */
  var CURVA = {
    p4out:   function(t){ return 1 - Math.pow(1-t, 5); },
    p4inout: function(t){ return t < .5 ? 16*t*t*t*t*t : 1 - Math.pow(-2*t+2, 5)/2; },
    suave:   function(t){ return t < .5 ? 4*t*t*t : 1 - Math.pow(-2*t+2, 3)/2; }
  };

  function ditherVivo(cfg){
    var raiz = cfg.raiz; if(!raiz) return null;
    var cv = document.createElement('canvas');
    cv.className = cfg.classeCanvas; cv.setAttribute('aria-hidden', 'true');
    /* failIfMajorPerformanceCaveat: sem aceleracao de hardware o shader roda na CPU
       e fica mais lento que a <img> que ele substitui. Melhor nem comecar. */
    var op = {antialias:false, depth:false, stencil:false, alpha:false, premultipliedAlpha:false,
              powerPreference:'high-performance', failIfMajorPerformanceCaveat:true};
    var gl = cv.getContext('webgl', op) || cv.getContext('experimental-webgl', op);
    if(!gl) return null;

    /* CONTEXTO PERDIDO (reset de driver, volta do sono, troca de GPU, limite de
       contextos do navegador). Sem isto o canvas sumia da composicao, `gl-on`
       continuava escondendo as <img> de reserva e o laco seguia desenhando num
       contexto morto: a peca ficava so creme para sempre. Agora a peca volta
       inteira ao caminho sem WebGL. */
    var morto = false;
    cv.addEventListener('webglcontextlost', function(e){
      e.preventDefault();          /* sem isto o navegador nem tenta restaurar */
      morto = true; ligado = false;
      raiz.classList.remove('gl-on');
      if(cv.parentNode) cv.parentNode.removeChild(cv);
    });

    function shader(tipo, src){
      var s = gl.createShader(tipo); gl.shaderSource(s, src); gl.compileShader(s);
      if(!gl.getShaderParameter(s, gl.COMPILE_STATUS)){ console.warn('dither-vivo:', gl.getShaderInfoLog(s)); return null; }
      return s;
    }
    function programa(fs){
      var a = shader(gl.VERTEX_SHADER, VERT), b = shader(gl.FRAGMENT_SHADER, fs); if(!a||!b) return null;
      var pr = gl.createProgram(); gl.attachShader(pr,a); gl.attachShader(pr,b);
      gl.bindAttribLocation(pr, 0, 'p'); gl.linkProgram(pr);
      return gl.getProgramParameter(pr, gl.LINK_STATUS) ? pr : null;
    }
    var pT = programa(FRAG_TRILHA), pF = programa(FRAG_FOTO);
    if(!pT || !pF) return null;
    function uni(pr, nomes){ var o = {}; nomes.forEach(function(n){ o[n] = gl.getUniformLocation(pr, n); }); return o; }
    var uT = uni(pT, ['t','res','pt','ptAnt','aspecto','vel','raio','borda','fica']);
    var uF = uni(pF, ['uLum','uTrilha','uB4','uB8','uTela','uCol','uTex','uAx','uEspelha','uZoom','uTempo','uC0','uC1','uC2','uC3','uCreme',
      'uGama','uCtr','uBrilho','uPix','uPixMul','uTrailMul','uBias','uBiasReacao','uRespiro','uLava','uRevela','uOpac','uSoFigura']);

    var quad = gl.createBuffer();
    gl.bindBuffer(gl.ARRAY_BUFFER, quad);
    gl.bufferData(gl.ARRAY_BUFFER, new Float32Array([-1,-1, 3,-1, -1,3]), gl.STATIC_DRAW);
    gl.enableVertexAttribArray(0); gl.vertexAttribPointer(0, 2, gl.FLOAT, false, 0, 0);

    /* matrizes de Bayer como texturas minusculas (WebGL1 nao tem array constante).
       O limiar e (m+0,5)/n2, o mesmo do gerador em Python. */
    function bayer(n){
      var m = [[0]];
      while(m.length < n){ var k = m.length, o = [], y, x;
        for(y=0;y<2*k;y++) o.push(new Array(2*k));
        for(y=0;y<k;y++) for(x=0;x<k;x++){ var v = m[y][x]*4;
          o[y][x]=v; o[y][x+k]=v+2; o[y+k][x]=v+3; o[y+k][x+k]=v+1; }
        m = o; }
      var d = new Uint8Array(n*n), yy, xx;
      for(yy=0;yy<n;yy++) for(xx=0;xx<n;xx++) d[yy*n+xx] = Math.round((m[yy][xx]+0.5)/(n*n)*255);
      var tx = gl.createTexture(); gl.bindTexture(gl.TEXTURE_2D, tx);
      gl.pixelStorei(gl.UNPACK_ALIGNMENT, 1);
      gl.texImage2D(gl.TEXTURE_2D, 0, gl.LUMINANCE, n, n, 0, gl.LUMINANCE, gl.UNSIGNED_BYTE, d);
      gl.texParameteri(gl.TEXTURE_2D, gl.TEXTURE_MIN_FILTER, gl.NEAREST);
      gl.texParameteri(gl.TEXTURE_2D, gl.TEXTURE_MAG_FILTER, gl.NEAREST);
      gl.texParameteri(gl.TEXTURE_2D, gl.TEXTURE_WRAP_S, gl.REPEAT);
      gl.texParameteri(gl.TEXTURE_2D, gl.TEXTURE_WRAP_T, gl.REPEAT);
      return tx;
    }
    var txB4 = bayer(4), txB8 = bayer(8);

    /* ---- os planos: cada foto e um retangulo do DOM com a sua luminancia ---- */
    function anima(v){ return {v:v, de:v, para:v, t0:0, dur:0, curva:CURVA.suave}; }
    function vai(a, para, dur, curva, agora){ if(a.para === para) return; a.de = a.v; a.para = para; a.t0 = agora; a.dur = dur; a.curva = curva; }
    function anda(a, agora){
      if(a.v === a.para) return false;
      /* t preso em 0..1 nas DUAS pontas: o t0 vem de performance.now() dentro de um
         evento, e o relogio do quadro pode estar alguns ms ATRAS dele. Sem o piso, t
         sai negativo, a curva extrapola e o zoom vira numero absurdo por um quadro. */
      var t = a.dur > 0 ? Math.max(0, Math.min(1, (agora - a.t0)/a.dur)) : 1;
      a.v = t >= 1 ? a.para : a.de + (a.para - a.de)*a.curva(t);
      return true;
    }
    var planos = cfg.planos.map(function(pl, i){
      return {el:pl.el, src:pl.lum, ax:pl.ax == null ? .5 : pl.ax, espelha:pl.espelha ? 1 : 0, tx:null, w:1, h:1,
              zoom:anima(1), lava:anima(cfg.lavaRepouso || 0), opac:anima(cfg.empilhado ? (i === 0 ? 1 : 0) : 1)};
    });
    if(planos.some(function(pl){ return !pl.src || !pl.el; })) return null;

    var pix = anima(20), bias = anima(-1), revelado = false;   /* a entrada: celula 20->1 e limiar -1->0 */
    var ligado = false, prontas = 0;
    function carrega(){ planos.forEach(function(pl){
      var im = new Image();
      im.onload = function(){
        var tx = gl.createTexture(); gl.bindTexture(gl.TEXTURE_2D, tx);
        gl.pixelStorei(gl.UNPACK_FLIP_Y_WEBGL, true);
        try { gl.texImage2D(gl.TEXTURE_2D, 0, gl.LUMINANCE, gl.LUMINANCE, gl.UNSIGNED_BYTE, im); }
        catch(e){ gl.pixelStorei(gl.UNPACK_FLIP_Y_WEBGL, false); return; }
        gl.pixelStorei(gl.UNPACK_FLIP_Y_WEBGL, false);
        gl.texParameteri(gl.TEXTURE_2D, gl.TEXTURE_MIN_FILTER, gl.LINEAR);
        gl.texParameteri(gl.TEXTURE_2D, gl.TEXTURE_MAG_FILTER, gl.LINEAR);
        gl.texParameteri(gl.TEXTURE_2D, gl.TEXTURE_WRAP_S, gl.CLAMP_TO_EDGE);
        gl.texParameteri(gl.TEXTURE_2D, gl.TEXTURE_WRAP_T, gl.CLAMP_TO_EDGE);
        pl.tx = tx; pl.w = im.naturalWidth; pl.h = im.naturalHeight;
        if(++prontas === planos.length) liga();
      };
      im.src = pl.src;
    }); }
    /* as luminancias da moldura de noticias pesam meio mega e ela fica a 7 mil px
       do topo: so baixam quando a secao se aproxima, com a mesma folga de 150%
       que o script das noticias ja usa para as fotos de reserva. */
    if(cfg.revelar === 'visivel' && 'IntersectionObserver' in window){
      var obsL = new IntersectionObserver(function(es){
        if(es.some(function(e){ return e.isIntersecting; })){ obsL.disconnect(); carrega(); }
      }, {rootMargin:'150% 0px 150% 0px'});
      obsL.observe(raiz);
    } else carrega();

    /* ---- trilha em ping-pong, na resolucao CSS (1/dpr do canvas), como no OCI ---- */
    var TW = 2, TH = 2, trilha = null, idx = 0;
    function alvo(w, h){
      var tx = gl.createTexture(); gl.bindTexture(gl.TEXTURE_2D, tx);
      gl.texImage2D(gl.TEXTURE_2D, 0, gl.RGBA, w, h, 0, gl.RGBA, gl.UNSIGNED_BYTE, null);
      gl.texParameteri(gl.TEXTURE_2D, gl.TEXTURE_MIN_FILTER, gl.LINEAR);
      gl.texParameteri(gl.TEXTURE_2D, gl.TEXTURE_MAG_FILTER, gl.LINEAR);
      gl.texParameteri(gl.TEXTURE_2D, gl.TEXTURE_WRAP_S, gl.CLAMP_TO_EDGE);
      gl.texParameteri(gl.TEXTURE_2D, gl.TEXTURE_WRAP_T, gl.CLAMP_TO_EDGE);
      var fb = gl.createFramebuffer(); gl.bindFramebuffer(gl.FRAMEBUFFER, fb);
      gl.framebufferTexture2D(gl.FRAMEBUFFER, gl.COLOR_ATTACHMENT0, gl.TEXTURE_2D, tx, 0);
      gl.disable(gl.SCISSOR_TEST); gl.clearColor(0,0,0,1); gl.clear(gl.COLOR_BUFFER_BIT);
      return {tx:tx, fb:fb};
    }
    function refazTrilha(){
      if(trilha) trilha.forEach(function(a){ gl.deleteTexture(a.tx); gl.deleteFramebuffer(a.fb); });
      TW = Math.max(2, Math.round(cv.width/dpr)); TH = Math.max(2, Math.round(cv.height/dpr));
      trilha = [alvo(TW,TH), alvo(TW,TH)]; idx = 0;
    }

    var dpr = 1, R = null, calmo = 0, rodando = false;
    /* o laco so existe enquanto ha o que desenhar. Antes ele reagendava o proximo
       quadro na PRIMEIRA linha, entao as duas instancias acordavam a thread a cada
       vsync durante a visita inteira, mesmo fora da tela. Agora dorme sem nenhum
       rAF pendente (o canvas guarda o ultimo quadro) e acorda() o religa. */
    function acorda(){ calmo = 0; if(ligado && !morto && !rodando){ rodando = true; antes = performance.now(); requestAnimationFrame(passo); } }
    function mede(){
      R = raiz.getBoundingClientRect();
      dpr = Math.min(window.devicePixelRatio || 1, 2);
      var w = Math.max(2, Math.round(R.width*dpr)), h = Math.max(2, Math.round(R.height*dpr));
      if(cv.width !== w || cv.height !== h){ cv.width = w; cv.height = h; refazTrilha(); desenhou = false; acorda(); }
    }

    /* ---- ponteiro: ouvido na JANELA, como no OCI, para a trilha entrar pela borda
       em vez de nascer no meio da peca ---- */
    var alvoPt = [0,0], pt = [0,0], ptAnt = [0,0], temPt = false, perto = false, vel = 0, ultimoXY = null, dxy = 0;
    window.addEventListener('pointermove', function(e){
      if(e.pointerType && e.pointerType !== 'mouse') return;
      if(!R) return;
      var x = (e.clientX - R.left)/R.width, y = 1 - (e.clientY - R.top)/R.height;
      var folga = .35;
      perto = x > -folga && x < 1+folga && y > -folga && y < 1+folga;
      if(ultimoXY) dxy += Math.sqrt(Math.pow((e.clientX-ultimoXY[0])/window.innerWidth, 2) + Math.pow((e.clientY-ultimoXY[1])/window.innerHeight, 2));
      ultimoXY = [e.clientX, e.clientY];
      alvoPt[0] = x; alvoPt[1] = y;
      if(!temPt){ pt[0]=ptAnt[0]=x; pt[1]=ptAnt[1]=y; temPt = true; dxy = 0; }
      if(perto) acorda();
    }, {passive:true});
    function some(){ temPt = false; ultimoXY = null; dxy = 0; }
    document.documentElement.addEventListener('mouseleave', some);
    window.addEventListener('blur', some);

    planos.forEach(function(pl, i){
      var g = cfg.empilhado ? raiz : pl.el;
      if(cfg.empilhado && i > 0) return;
      /* UNIAO de mouse e foco, e nao "o ultimo evento manda". Como o CSS mostra a
         lista tanto em :hover quanto em :focus-within, um focusout com o mouse
         ainda dentro apagava a chapa de creme e deixava a lista de 13px sobre a
         foto crua. Agora a chapa so cai quando os DOIS estados saem. */
      var sobre = false, foco = false;
      function aplica(){ var t = performance.now(), on = sobre || foco;
        (cfg.empilhado ? planos : [pl]).forEach(function(q){
          vai(q.zoom, on ? (cfg.zoomHover || 1) : 1, 850, CURVA.p4out, t);
          if(cfg.lavaHover != null) vai(q.lava, on ? cfg.lavaHover : (cfg.lavaRepouso || 0), 500, CURVA.suave, t); });
        acorda(); }
      g.addEventListener('mouseenter', function(){ sobre = true; aplica(); });
      g.addEventListener('mouseleave', function(){ sobre = false; aplica(); });
      g.addEventListener('focusin',  function(){ foco = true; aplica(); });
      g.addEventListener('focusout', function(e){ foco = !!(e.relatedTarget && g.contains(e.relatedTarget)); aplica(); });
    });
    window.addEventListener('resize', function(){ if(ligado){ mede(); acorda(); } });

    /* dois observadores, porque sao duas perguntas: "vale a pena desenhar?" (com
       200px de folga, para a peca ja chegar desenhada) e "ja entrou o bastante
       para revelar?" (o `start: top 85%` do OCI). */
    var visivel = true, desenhou = false, obsR = null;
    if('IntersectionObserver' in window){
      new IntersectionObserver(function(es){ es.forEach(function(e){ visivel = e.isIntersecting; if(visivel) acorda(); }); },
        {rootMargin:'200px 0px 200px 0px'}).observe(raiz);
      if(cfg.revelar === 'visivel'){
        obsR = new IntersectionObserver(function(es){ es.forEach(function(e){ if(e.isIntersecting){ revela(); if(revelado) obsR.disconnect(); } }); },
          {rootMargin:'0px 0px -15% 0px'});
        obsR.observe(raiz);
      }
    }
    document.addEventListener('visibilitychange', function(){ if(!document.hidden) acorda(); });

    function seco(){ revelado = true; pix.v = pix.de = pix.para = 1; bias.v = bias.de = bias.para = 0; acorda(); }
    function revela(){
      if(revelado || !ligado) return; revelado = true;
      var t = performance.now();
      vai(pix, 1, 2000, CURVA.p4out, t); vai(bias, 0, 2000, CURVA.p4out, t); acorda();
    }

    function liga(){
      if(ligado) return; ligado = true;
      raiz.insertBefore(cv, raiz.firstChild);
      raiz.classList.add('gl-on');
      mede();
      if(DIRETO) seco();
      /* CORRIDA que deixava a moldura em branco: o observador de revelacao fala
         uma vez, logo que e criado, e quase sempre ANTES de as luminancias
         chegarem. Naquele instante revela() saia por `!ligado` e o observador so
         voltaria a falar se a intersecao MUDASSE: com a secao ja na tela, nunca.
         Ficava pix=20 e bias=-1, e nesse estado todo pixel cai na cor 3, creme
         chapado, com as <img> de reserva escondidas pelo gl-on.
         observe() de novo entrega a entrada inicial outra vez, agora com a
         textura na mao. Sem IntersectionObserver, revela direto. */
      else if(cfg.revelar === 'visivel'){ if(obsR){ obsR.unobserve(raiz); obsR.observe(raiz); } else revela(); }
      else if(cfg.revelar === 'pronta'){
        /* a revelacao (celula 20->1, limiar -1->0 em 2s) e para quando a trama fica
           pronta ATRAS do loader. Se ela chegar depois de a pagina ja estar a vista, a
           troca e seca: <img> tramada por canvas tramado, sem apagar a foto para revelar. */
        if(document.body.classList.contains('pronta')) seco();
        else { window.addEventListener('im:pronta', revela, {once:true}); setTimeout(revela, 4200); }
      } else revela();
      acorda();
    }

    var t0 = performance.now(), antes = t0;
    var C = cfg.cores, CR = cfg.creme || [250,249,245];
    function passo(){
      var agora = performance.now();     /* um relogio so, o mesmo dos eventos */
      /* dorme. O primeiro quadro sai de qualquer jeito: canvas sem alfa nasce PRETO. */
      if(morto) { rodando = false; return; }
      if(desenhou && (!visivel || document.hidden || calmo > 150)){ rodando = false; return; }
      requestAnimationFrame(passo);
      if(desenhou) ++calmo;
      var dt = Math.min(100, agora - antes); antes = agora;
      var f60 = dt/16.667;
      mede();

      /* ponteiro e velocidade, nas contas do OCI: vel += (d - vel)*0,63 e satura em d = 1/32 da tela por quadro */
      ptAnt[0] = pt[0]; ptAnt[1] = pt[1];
      if(temPt){ pt[0] = alvoPt[0]; pt[1] = alvoPt[1]; }
      var d = (temPt && perto) ? dxy/Math.max(f60, .25) : 0; dxy = 0;
      vel += (d - vel)*(1 - Math.pow(1-.63, f60));
      var v = Math.min(1, vel*32);
      if(v > .004) acorda();

      var mexeu = false;
      if(anda(pix, agora)) mexeu = true;
      if(anda(bias, agora)) mexeu = true;
      planos.forEach(function(pl){
        if(anda(pl.zoom, agora)) mexeu = true;
        if(anda(pl.lava, agora)) mexeu = true;
        if(anda(pl.opac, agora)) mexeu = true;
      });
      var soma = cfg.empilhado ? (planos.reduce(function(a, q){ return a + Math.max(0, q.opac.v); }, 0) || 1) : 1;

      /* 1. trilha. Raio e borda do OCI (0,066+0,015v e 0,129+0,054v da ALTURA DA JANELA de 900)
            reescalados para a altura desta peca. */
      var esc = 900/Math.max(200, R.height), asp = cv.width/cv.height;
      var prox = 1 - idx;
      gl.useProgram(pT);
      gl.bindFramebuffer(gl.FRAMEBUFFER, trilha[prox].fb);
      gl.viewport(0,0,TW,TH); gl.disable(gl.SCISSOR_TEST); gl.disable(gl.BLEND);
      gl.activeTexture(gl.TEXTURE0); gl.bindTexture(gl.TEXTURE_2D, trilha[idx].tx);
      gl.uniform1i(uT.t, 0); gl.uniform2f(uT.res, TW, TH);
      gl.uniform2f(uT.pt, pt[0], pt[1]); gl.uniform2f(uT.ptAnt, ptAnt[0], ptAnt[1]);
      gl.uniform1f(uT.aspecto, asp); gl.uniform1f(uT.vel, v);
      /* 21/09: PINCEL_GERAL encolhe o cometa em TODAS as pecas de uma vez (tira da
         1a secao, folha Demandas, manchas Conhecimento, moldura de noticias). Com
         1,0 ele media 180 px de altura na secao Conhecimento, e o Leandro achou
         grande demais. O rastro que fica para tras (fica) nao muda. */
      var pinc = esc*(cfg.pincel || 1)*PINCEL_GERAL;
      /* 21/09: o cometa estava «gordo». A espessura na tela e (raio+borda) x 900 x
         pincel x PINCEL_GERAL, e a BORDA suave (0,129) era o dobro do raio: era ela
         o halo largo. RAIO_GERAL 0,8 e BORDA_GERAL 0,3 levam a espessura parada de
         ~123 px para ~58 px na secao Conhecimento, com o miolo mais firme. */
      gl.uniform1f(uT.raio, (.066 + v*.015)*pinc*RAIO_GERAL); gl.uniform1f(uT.borda, (.129 + v*.054)*pinc*BORDA_GERAL);
      /* 21/09: RASTRO_GERAL encurta a cauda do cometa em todas as pecas. Com 1,0 a
         trama engrossada guardava 96% por quadro, cauda de 240 px na secao
         Conhecimento; o Leandro pediu 60% menor. Dividir o expoente por 0,4
         encolhe a constante de tempo para 40%. */
      gl.uniform1f(uT.fica, Math.pow(1-.040, f60/RASTRO_GERAL));
      gl.drawArrays(gl.TRIANGLES, 0, 3);
      idx = prox;

      /* 2. as fotos */
      gl.useProgram(pF);
      gl.bindFramebuffer(gl.FRAMEBUFFER, null);
      gl.viewport(0,0,cv.width,cv.height);
      gl.disable(gl.SCISSOR_TEST);
      /* EMPILHADO: soma ponderada, e nao uma camada por cima da outra. Com
         SRC_ALPHA/ONE_MINUS_SRC_ALPHA sobre um fundo creme, no meio da fusao o
         pixel ficava e*B + (1-e)^2*A + e(1-e)*creme, ou seja um quarto de papel
         vazando: a trama de quatro cores dissolvia num clarao a cada troca de
         cartao. Somando com peso normalizado sobre preto, a soma dos alfas e
         sempre 1 e a cor anda de A para B sem passar pelo papel. */
      if(cfg.empilhado){ gl.clearColor(0,0,0,1); gl.clear(gl.COLOR_BUFFER_BIT);
        gl.enable(gl.BLEND); gl.blendFunc(gl.SRC_ALPHA, gl.ONE); }
      else { gl.clearColor(CR[0]/255, CR[1]/255, CR[2]/255, 1); gl.clear(gl.COLOR_BUFFER_BIT); gl.disable(gl.BLEND); }
      gl.enable(gl.SCISSOR_TEST);
      gl.activeTexture(gl.TEXTURE1); gl.bindTexture(gl.TEXTURE_2D, trilha[idx].tx); gl.uniform1i(uF.uTrilha, 1);
      gl.activeTexture(gl.TEXTURE2); gl.bindTexture(gl.TEXTURE_2D, txB4); gl.uniform1i(uF.uB4, 2);
      gl.activeTexture(gl.TEXTURE3); gl.bindTexture(gl.TEXTURE_2D, txB8); gl.uniform1i(uF.uB8, 3);
      gl.uniform2f(uF.uTela, cv.width, cv.height);
      gl.uniform1f(uF.uTempo, (agora - t0)/1000);
      gl.uniform3f(uF.uC0, C[0][0]/255, C[0][1]/255, C[0][2]/255);
      gl.uniform3f(uF.uC1, C[1][0]/255, C[1][1]/255, C[1][2]/255);
      gl.uniform3f(uF.uC2, C[2][0]/255, C[2][1]/255, C[2][2]/255);
      gl.uniform3f(uF.uC3, C[3][0]/255, C[3][1]/255, C[3][2]/255);
      gl.uniform3f(uF.uCreme, CR[0]/255, CR[1]/255, CR[2]/255);
      gl.uniform1f(uF.uGama, .86); gl.uniform1f(uF.uCtr, 1.55); gl.uniform1f(uF.uBrilho, .35);
      gl.uniform1f(uF.uPix, Math.max(1, pix.v)); gl.uniform1f(uF.uPixMul, cfg.pixMul || 3.3); gl.uniform1f(uF.uTrailMul, 1.27);
      gl.uniform1f(uF.uBias, bias.v);
      /* quanto o rastro ESCURECE a trama. 0,13 ate 21/09; 0,20 desde 22/09 («um
         pouco mais escura»). Cada peca pode baixar: na secao Conhecimento o rastro
         escuro atrapalhava a leitura das etiquetas por baixo dele. */
      gl.uniform1f(uF.uBiasReacao, cfg.biasReacao == null ? .20 : cfg.biasReacao); gl.uniform1f(uF.uRespiro, cfg.respiro == null ? .012 : cfg.respiro);
      gl.uniform1f(uF.uRevela, cfg.revelaNaTrilha == null ? 0 : cfg.revelaNaTrilha);
      gl.uniform1f(uF.uSoFigura, cfg.trilhaSoNaFigura ? 1 : 0);

      planos.forEach(function(pl){
        if(pl.opac.v < .002) return;
        var r = pl.el.getBoundingClientRect();
        var x0 = Math.round((r.left - R.left)*dpr), x1 = Math.round((r.right - R.left)*dpr);
        var y1 = Math.round((r.top - R.top)*dpr), y2 = Math.round((r.bottom - R.top)*dpr);
        var w = x1 - x0, h = y2 - y1, y = cv.height - y2;
        if(w < 1 || h < 1) return;
        gl.scissor(x0, y, w, h);
        gl.activeTexture(gl.TEXTURE0); gl.bindTexture(gl.TEXTURE_2D, pl.tx); gl.uniform1i(uF.uLum, 0);
        gl.uniform4f(uF.uCol, x0, y, w, h); gl.uniform2f(uF.uTex, pl.w, pl.h);
        gl.uniform1f(uF.uAx, pl.espelha ? 1 - pl.ax : pl.ax); gl.uniform1f(uF.uEspelha, pl.espelha);
        gl.uniform1f(uF.uZoom, pl.zoom.v); gl.uniform1f(uF.uLava, pl.lava.v); gl.uniform1f(uF.uOpac, pl.opac.v/soma);
        gl.drawArrays(gl.TRIANGLES, 0, 3);
      });
      if(mexeu) acorda();
      desenhou = true;
    }

    return {
      /* fusao cruzada entre camadas empilhadas: 0,8 s em power4.inOut, como no OCI */
      fundir: function(para){
        var t = performance.now();
        planos.forEach(function(pl, i){ vai(pl.opac, i === para ? 1 : 0, 800, CURVA.p4inout, t); });
        acorda();
      }
    };
  }

  window.ditherVivo = ditherVivo;
})();
