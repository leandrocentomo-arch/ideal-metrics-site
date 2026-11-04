/* 04/11/2026: grade setor x norma da home deitada em isometrico e interativa. Desenho em canvas: sao 630 casas, e a troca de
   tema anima a largura de cada coluna e a escala do desenho juntas. Os dados vem do grafico da home (monta.py). */
(function(){
  var elDados = document.getElementById('smMdD'); if(!elDados) return;
  var DADOS = JSON.parse(elDados.textContent);
  [].forEach.call(document.querySelectorAll('.md'), function(raiz){ grade(raiz, DADOS, raiz.hasAttribute('data-plano')); });

function grade(raiz, D, plano){
  var cv = raiz.querySelector('canvas'), ctx = cv.getContext('2d');
  var C = Math.cos(Math.PI / 6), S = .5, nS = D.S.length, nN = D.N.length;
  var quieto = window.matchMedia && matchMedia('(prefers-reduced-motion: reduce)').matches;
  var mix = function(a, b, t){ return a + (b - a) * t; };
  var clamp = function(v, a, b){ return Math.max(a, Math.min(b, v)); };
  var ease = function(t){ return 1 - Math.pow(1 - t, 3); };
  var W = 0, H = 0, dpr = 1, movel = false;

  /* ----- estado */
  var cel = [], rowF = [], colF = [], cw = [], cwA = [], cwB = [];
  for(var i = 0; i < nS; i++){
    rowF.push({v:0, a:0});
    var lin = [];
    for(var j = 0; j < nN; j++) lin.push({k:+D.M[i].charAt(j), ent:0, entD:0, lift:0, liftA:0, liftD:0, dim:0, dimA:0, lit:0, litA:0, foc:0, focA:0});
    cel.push(lin);
  }
  for(j = 0; j < nN; j++){ colF.push({v:0, a:0}); cw.push(1); cwA.push(1); cwB.push(1); }
  var vista = -1, t = 0, tA = 0, tB = 0, mIni = -1e9, DUR = 760, tv = 1, tvA = 1;
  var foco = null, fixo = false, entrada = 0, btS = null;
  var geo = {}, maxS = 170, maxN = 130, lanes = [], nLanes = 1;

  /* ----- cores: vem das variaveis da pagina, para o seletor de acento valer aqui tambem */
  function hex(s){
    s = s.trim();
    if(s.charAt(0) === '#'){
      if(s.length === 4) s = '#' + s[1] + s[1] + s[2] + s[2] + s[3] + s[3];
      return [parseInt(s.slice(1, 3), 16), parseInt(s.slice(3, 5), 16), parseInt(s.slice(5, 7), 16)];
    }
    var m = s.match(/[\d.]+/g); return m ? [+m[0], +m[1], +m[2]] : [0, 0, 0];
  }
  var P = {};
  function cores(){
    var cs = getComputedStyle(document.body), v = function(n){ return hex(cs.getPropertyValue(n)); };
    P = {ac:v('--sm-ac'), ac2:v('--sm-ac2'), ac3:v('--sm-ac3'), ta:v('--sm-ta'), tx:v('--sm-tx-ac'), bg:v('--sm-cr'),
         flT:[244,244,242], flF:[233,233,230], flL:[199,201,202], brT:[251,251,250], brF:[169,178,188], brL:[139,150,162]};
  }
  var rgb = function(c, a){ return 'rgba(' + Math.round(c[0]) + ',' + Math.round(c[1]) + ',' + Math.round(c[2]) + ',' + (a === undefined ? 1 : a) + ')'; };
  var mistura = function(a, b, q){ return [mix(a[0], b[0], q), mix(a[1], b[1], q), mix(a[2], b[2], q)]; };

  /* ----- geometria do quadro */
  function folgaN(q){ return movel ? 6 : plano ? 12 : mix(26, 32, q); }
  function folgaS(q){ return movel ? 6 : plano ? 12 : mix(14, 22, q); }
  function fonteBase(q){ return movel ? mix(8.5, 10.5, q) : mix(10.5, 13, q); }
  function mede(){
    ctx.setTransform(1, 0, 0, 1, 0, 0);
    ctx.font = '600 13px "IBM Plex Mono", monospace';
    maxS = 0; maxN = 0;
    D.S.forEach(function(s, i){ s.t = movel ? String(i + 1) : s.c; s.w = ctx.measureText(s.t).width; maxS = Math.max(maxS, s.w); });
    D.N.forEach(function(n){ n.w = ctx.measureText(n.l).width; maxN = Math.max(maxN, n.w); });
    D.G.forEach(function(g){ g.w = ctx.measureText(g.n).width * .86; });
  }
  function calcula(){
    var q = t, by = mix(1.7, .86, q), L = 0, X = [];
    for(var j = 0; j < nN; j++){ X.push(L); L += cw[j]; }
    X.push(L);
    var Dy = nS * by, fs = fonteBase(q), wS = maxS * fs / 13, wN = maxN * fs / 13;
    var hD = plano ? 0 : mix(1.25, .62, q), hT = plano ? 0 : mix(.36, .17, q);
    var x1 = movel ? W : W - mix(0, 330, q), bot = mix(nLanes * 15 + 18, 10, q), topo = Math.max(wS + 22, wN + folgaN(q)) * S + 10;
    var uW = (x1 - (movel ? 0 : mix(0, 76, q)) - (wS + wN) * C - 16) / ((L + Dy) * C), uH = (H - topo - bot - 10) / ((L + Dy) * S + hD * .4);
    var u = Math.min(uW, uH, movel ? 40 : 58);
    var tw = (L + Dy) * C * u + (wS + wN) * C, th = (L + Dy) * S * u + topo + bot, x0 = movel ? 0 : mix(0, 76, q);
    var ox = x0 + (x1 - x0 - tw) / 2 + wS * C + Dy * C * u, oy = (H - th) / 2 + topo;
    geo = {by:by, L:L, X:X, Dy:Dy, fs:fs, hD:hD, hT:hT, u:u, ox:ox, oy:oy, fx:mix(.76, .66, q), fy:mix(.68, .74, q), esp:plano ? 0 : mix(9, 18, q) / u};
  }
  var sx = function(x, y){ return geo.ox + (x - y) * C * geo.u; };
  var sy = function(x, y, z){ return geo.oy + (x + y) * S * geo.u - (z || 0) * geo.u; };
  function faixas(){   /* nome de cada tema na borda da frente; o que nao cabe desce uma linha, como os rotulos da grade da home */
    calcula();
    var fim = [], X = geo.X, u = geo.u, g0 = 0;
    lanes = [];
    D.G.forEach(function(g, k){
      var a = g0, b = g0; while(b < nN && D.N[b].g === k) b++;
      g0 = b;
      var ini = a * u, fimT = ini + g.w, l = 0;
      while(fim[l] !== undefined && fim[l] > ini - 6) l++;
      fim[l] = Math.max(fimT, b * u);
      lanes.push({g:k, a:a, b:b, l:l});
    });
    nLanes = fim.length;
  }

  /* ----- desenho */
  function poly(p, fill){ ctx.beginPath(); ctx.moveTo(p[0], p[1]); for(var n = 2; n < p.length; n += 2) ctx.lineTo(p[n], p[n + 1]); ctx.closePath(); ctx.fillStyle = fill; ctx.fill(); }
  function piso(x0, y0, x1, y1){ return [sx(x0, y0), sy(x0, y0), sx(x1, y0), sy(x1, y0), sx(x1, y1), sy(x1, y1), sx(x0, y1), sy(x0, y1)]; }
  function linha(a, b, c, d){ ctx.beginPath(); ctx.moveTo(a, b); ctx.lineTo(c, d); ctx.stroke(); }
  function texto(txt, X, Y, sen, alin, fs, peso, cor, alfa){
    ctx.setTransform(dpr * C, dpr * sen, 0, dpr, dpr * X, dpr * Y);
    ctx.font = peso + ' ' + fs + 'px "IBM Plex Mono", monospace';
    ctx.textAlign = alin; ctx.textBaseline = 'middle'; ctx.fillStyle = rgb(cor, alfa);
    ctx.fillText(txt, 0, 0);
    ctx.setTransform(dpr, 0, 0, dpr, 0, 0);
  }
  /* versao plana: os quadrados de canto redondo da grade da home, deitados no mesmo plano, sem altura */
  function quadrados(){
    var g = geo, X = g.X, u = g.u, by = g.by, i, j;
    ctx.setTransform(dpr * C * u, dpr * S * u, -dpr * C * u, dpr * S * u, dpr * g.ox, dpr * g.oy);
    for(i = 0; i < nS; i++){
      for(j = 0; j < nN; j++){
        var w = cw[j]; if(w < .015) continue;
        var c = cel[i][j];
        if(c.k === 0 || (c.k === 1 && tv < .04)){
          var pt = Math.min(.05, w * .05);
          ctx.fillStyle = rgb(c.lit > .02 ? P.ta : [120, 134, 150], c.lit > .02 ? mix(.3, .8, c.lit) : mix(.55, .15, c.dim));
          ctx.fillRect(X[j] + w / 2 - pt, i * by + by / 2 - pt, pt * 2, pt * 2);
          continue;
        }
        if(c.ent < .02) continue;
        var lado = Math.min(w * .68, by * .8) * c.ent, x = X[j] + (w - lado) / 2, y = i * by + (by - lado) / 2, r = Math.min(.13, lado * .23);
        var cor = c.k === 2 ? P.ac : mistura(P.bg, P.ac, .42 * tv);
        cor = mistura(cor, P.ta, c.lit * (1 - c.foc));
        if(c.foc > .01) cor = mistura(cor, P.ac, c.foc);
        if(c.dim > .01) cor = mistura(cor, P.bg, c.dim * .84);
        ctx.beginPath();
        if(ctx.roundRect) ctx.roundRect(x, y, lado, lado, r); else ctx.rect(x, y, lado, lado);
        ctx.fillStyle = rgb(cor); ctx.fill();
        if(c.foc > .01){ ctx.strokeStyle = rgb(P.ta, c.foc); ctx.lineWidth = .1; ctx.stroke(); }
      }
    }
    ctx.setTransform(dpr, 0, 0, dpr, 0, 0);
  }
  function desenha(){
    calcula();
    var g = geo, X = g.X, u = g.u, by = g.by, L = g.L, Dy = g.Dy, i, j;
    ctx.setTransform(dpr, 0, 0, dpr, 0, 0);
    ctx.clearRect(0, 0, W, H);
    if(L < .01) return;

    /* laje */
    var A = [sx(0, 0), sy(0, 0)], B = [sx(L, 0), sy(L, 0)], E = [sx(L, Dy), sy(L, Dy)], F = [sx(0, Dy), sy(0, Dy)], esp = g.esp * u;
    if(!plano){
    ctx.save(); ctx.shadowColor = 'rgba(20,48,76,.3)'; ctx.shadowBlur = movel ? 12 : 34; ctx.shadowOffsetX = movel ? 3 : 8; ctx.shadowOffsetY = movel ? 8 : 22;
    poly([F[0], F[1], E[0], E[1], B[0], B[1] + esp, E[0], E[1] + esp, F[0], F[1] + esp], rgb(P.flF));
    ctx.restore();
    poly([F[0], F[1], E[0], E[1], E[0], E[1] + esp, F[0], F[1] + esp], rgb(P.flF));
    poly([E[0], E[1], B[0], B[1], B[0], B[1] + esp, E[0], E[1] + esp], rgb(P.flL));
    poly([A[0], A[1], B[0], B[1], E[0], E[1], F[0], F[1]], rgb(P.flT));
    }

    /* faixas dos temas, linha e coluna acesas no piso */
    if(t < 1) lanes.forEach(function(l){ if(l.g % 2) poly(piso(X[l.a], 0, X[l.b], Dy), 'rgba(20,48,76,' + (.035 * (1 - t)) + ')'); });
    for(i = 0; i < nS; i++) if(rowF[i].v > .01) poly(piso(0, i * by, L, (i + 1) * by), rgb(P.ac, .17 * rowF[i].v));
    for(j = 0; j < nN; j++) if(colF[j].v > .01 && cw[j] > .01) poly(piso(X[j], 0, X[j + 1], Dy), rgb(P.ac, .17 * colF[j].v));

    /* grade */
    ctx.lineWidth = .5; ctx.strokeStyle = 'rgba(20,48,76,.17)';
    for(j = 0; j <= nN; j++){ if(j < nN && cw[j] < .01) continue; linha(sx(X[j], 0), sy(X[j], 0), sx(X[j], Dy), sy(X[j], Dy)); }
    for(i = 0; i <= nS; i++) linha(sx(0, i * by), sy(0, i * by), sx(L, i * by), sy(L, i * by));
    if(t < 1){
      ctx.strokeStyle = 'rgba(20,48,76,' + (.42 * (1 - t)) + ')';
      lanes.forEach(function(l){ linha(sx(X[l.a], 0), sy(X[l.a], 0), sx(X[l.a], Dy), sy(X[l.a], Dy)); });
    }

    /* blocos, de tras para a frente */
    if(plano) quadrados();
    else for(i = 0; i < nS; i++){
      for(j = 0; j < nN; j++){
        var w = cw[j]; if(w < .015) continue;
        var c = cel[i][j], x0 = X[j] + w * (1 - g.fx) / 2, dx = w * g.fx, y0 = i * by + by * (1 - g.fy) / 2, dy = by * g.fy;
        var base = c.k === 2 ? g.hD : c.k === 1 ? g.hT * tv : 0, h = base * c.ent;
        if(base > .001) h += c.lift * (t ? mix(1, .62, t) : 1);
        if(c.k === 0 || (c.k === 1 && tv < .04) || c.ent < .02){
          var pa = sx(x0 + dx / 2, y0 + dy / 2), pb = sy(x0 + dx / 2, y0 + dy / 2), r = Math.max(.8, mix(1, 1.7, t));
          ctx.fillStyle = rgb(c.lit > .02 ? P.ta : [120, 134, 150], c.lit > .02 ? mix(.3, .8, c.lit) : mix(.5, .15, c.dim));
          ctx.fillRect(pa - r, pb - r * .5, r * 2, r);
          continue;
        }
        var cT, cF, cL;
        if(c.k === 2){ cT = P.ac; cF = P.ac2; cL = P.ac3; }
        else {
          var qa = c.lit * .55;
          cT = mistura(P.brT, P.ac, qa); cF = mistura(P.brF, P.ac2, qa); cL = mistura(P.brL, P.ac3, qa);
        }
        if(c.foc > .01){ cT = mistura(cT, P.ta, c.foc); cF = mistura(cF, [12, 30, 48], c.foc); cL = mistura(cL, [8, 22, 36], c.foc); }
        if(c.dim > .01){ var qd = c.dim * .74; cT = mistura(cT, P.flT, qd); cF = mistura(cF, P.flF, qd); cL = mistura(cL, P.flL, qd); }
        var x1 = x0 + dx, y1 = y0 + dy;
        var ax = sx(x0, y0), ay = sy(x0, y0, h), bx = sx(x1, y0), by_ = sy(x1, y0, h), mx = sx(x1, y1), my = sy(x1, y1, h), dx_ = sx(x0, y1), dy_ = sy(x0, y1, h), zh = h * u;
        poly([dx_, dy_, mx, my, mx, my + zh, dx_, dy_ + zh], rgb(cF));
        poly([bx, by_, mx, my, mx, my + zh, bx, by_ + zh], rgb(cL));
        poly([ax, ay, bx, by_, mx, my, dx_, dy_], rgb(cT));
      }
    }

    /* rotulos por ultimo, para nenhum bloco cobrir */
    var fs = g.fs, gap = folgaS(t) / u, gapN = folgaN(t) / u, tem = !!foco;
    for(i = 0; i < nS; i++){
      var ls = rowF[i].v, ys = (i + .5) * by;
      texto(D.S[i].t, sx(-gap, ys) - 5 * ls * C, sy(-gap, ys) - 5 * ls * S, S, 'right', fs, ls > .5 ? 600 : 500, ls > .5 ? P.tx : P.ta, tem && ls < .5 ? .36 : 1);
    }
    for(j = 0; j < nN; j++){
      if(cw[j] < .04) continue;
      var ln = colF[j].v, xs = X[j] + cw[j] / 2;
      texto(D.N[j].l, sx(xs, -gapN) + 5 * ln * C, sy(xs, -gapN) - 5 * ln * S, -S, 'left', fs, ln > .5 ? 600 : 500, ln > .5 ? P.tx : P.ta, Math.min(1, cw[j] * 1.4) * (tem && ln < .5 ? .36 : 1));
    }

    /* nomes dos temas na borda da frente */
    if(t < .98){
      var al = 1 - t, passo = 15, fg = 10.5;
      lanes.forEach(function(l){
        var ini = X[l.a], fimx = X[l.b], desc = 9 + l.l * passo, ax = sx(ini, Dy), ay = sy(ini, Dy) + esp;
        var off = function(d){ return [ax - d * C, ay + d * S]; }, o = off(desc);
        var aceso = foco && foco.g === l.g;
        ctx.strokeStyle = rgb(aceso ? P.tx : P.ta, al * (aceso ? 1 : .55)); ctx.lineWidth = .6;
        var ex = sx(fimx, Dy), ey = sy(fimx, Dy) + esp;
        linha(ax - 3 * C, ay + 3 * S, ex - 3 * C, ey + 3 * S);
        if(l.l) linha(ax - 3 * C, ay + 3 * S, o[0], o[1]);
        texto(D.G[l.g].n, o[0] - 5 * C + 2, o[1] + 5 * S + 3, S, 'left', fg, aceso ? 600 : 500, aceso ? P.tx : P.ta, al * (tem && !aceso ? .4 : 1));
      });
    }
  }

  /* ----- animacao */
  var raf = 0, ult = 0;
  function pede(){ if(!raf){ ult = performance.now(); raf = requestAnimationFrame(quadro); } }
  function vai(o, k, alvo, q){ var v = o[k]; if(Math.abs(v - alvo) < .002){ o[k] = alvo; return false; } o[k] = v + (alvo - v) * q; return true; }
  function quadro(agora){
    raf = 0;
    var dt = Math.min(60, agora - ult); ult = agora;
    var rap = quieto ? 1 : 1 - Math.exp(-dt / 70), len = quieto ? 1 : 1 - Math.exp(-dt / 120), mov = false, i, j;

    var pm = quieto ? 1 : clamp((agora - mIni) / DUR, 0, 1), em = ease(pm);
    if(pm < 1) mov = true;
    for(j = 0; j < nN; j++) cw[j] = mix(cwA[j], cwB[j], em);
    t = mix(tA, tB, em);
    if(vai({v:tv}, 'v', tvA, 0)) { tv += (tvA - tv) * len; if(Math.abs(tv - tvA) < .004) tv = tvA; else mov = true; }

    for(i = 0; i < nS; i++){
      if(vai(rowF[i], 'v', rowF[i].a, rap)) mov = true;
      for(j = 0; j < nN; j++){
        var c = cel[i][j];
        if(entrada && agora >= c.entD && c.ent < 1){ c.ent = Math.min(1, quieto ? 1 : c.ent + (1.02 - c.ent) * len * 1.4); if(c.ent > .995) c.ent = 1; mov = true; }
        else if(entrada && c.ent < 1) mov = true;
        if(vai(c, 'dim', c.dimA, rap)) mov = true;
        if(vai(c, 'lit', c.litA, rap)) mov = true;
        if(vai(c, 'foc', c.focA, rap)) mov = true;
        if(agora >= c.liftD){ if(vai(c, 'lift', c.liftA, len)) mov = true; } else mov = true;
      }
    }
    for(j = 0; j < nN; j++) if(vai(colF[j], 'v', colF[j].a, rap)) mov = true;
    desenha();
    if(mov) pede();
  }

  /* ----- foco */
  function poeFoco(f){
    foco = f;
    var agora = performance.now(), passo = t > .5 ? 22 : 7;
    for(var i = 0; i < nS; i++){
      rowF[i].a = f && f.s === i ? 1 : 0;
      for(var j = 0; j < nN; j++){
        var c = cel[i][j], fs = !!f && f.s === i, fn = !!f && f.n === j, fg = !!f && f.g !== undefined && D.N[j].g === f.g;
        var lit = fs || fn || fg, cruz = fs && fn;
        c.litA = lit ? 1 : 0;
        c.dimA = f && !lit ? 1 : 0;
        c.focA = cruz ? 1 : 0;
        c.liftA = cruz ? .62 : lit ? (f.g !== undefined ? .14 : .22) : 0;
        var dist = !f ? 0 : f.s !== undefined && f.n !== undefined ? Math.abs(i - f.s) + Math.abs(j - f.n) : f.s !== undefined ? j : i;
        if(f && f.s !== undefined && f.n === undefined && vista >= 0) dist = j;
        c.liftD = lit ? agora + Math.min(dist * passo, 320) : agora;
      }
    }
    for(j = 0; j < nN; j++) colF[j].a = (f && f.n === j) || (f && f.g !== undefined && D.N[j].g === f.g) ? 1 : 0;
    ficha();
    if(btS){ btS.forEach(function(b, n){ b.setAttribute('aria-selected', !!(f && f.s === n)); }); desliza(setL); }
    pede();
  }

  /* ----- ficha */
  var el = function(id){ return raiz.querySelector('[data-f="' + id + '"]'); };
  var fSetor = el('setor'), fNorma = el('norma'), fRev = el('rev'), fTit = el('tit'), fRel = el('rel'), fLisR = el('lisr'), fLis = el('lis'), lS = el('ls'), lN = el('ln'), bSolta = el('solta'), fDica = el('dica');
  function escreve(n, v){ if(n.textContent !== v){ n.textContent = v; n.title = v; } }
  function ficha(){
    var f = foco || {}, s = f.s !== undefined ? D.S[f.s] : null, n = f.n !== undefined ? D.N[f.n] : null, g = f.g !== undefined ? D.G[f.g] : null;
    escreve(fSetor, s ? s.n : '');
    escreve(fNorma, n ? n.l : g ? g.n : '');
    escreve(fRev, n ? n.rev : '');
    escreve(fTit, n ? n.tit : s ? s.r : '');
    var rel = '';
    if(s && n){ var k = +D.M[f.s].charAt(f.n); rel = k === 2 ? 'Destaque do setor' : k === 1 ? 'Vale para qualquer setor' : 'Sem relação na grade'; }
    else if(n){ rel = D.S.every(function(_, i){ return +D.M[i].charAt(f.n) > 0; }) ? 'Vale para qualquer setor' : 'Destaque em setores específicos'; }
    escreve(fRel, rel);
    var rot = '', lista = '';
    if(n){ rot = 'Setores em destaque'; lista = D.S.filter(function(_, i){ return +D.M[i].charAt(f.n) === 2; }).map(function(x){ return x.c; }).join(' · '); }
    else if(s){ rot = 'Normas em destaque'; lista = D.N.filter(function(_, j){ return +D.M[f.s].charAt(j) === 2; }).map(function(x){ return x.l; }).join(' · '); }
    else if(g){ rot = 'Normas do tema'; lista = D.N.filter(function(x){ return x.g === f.g; }).map(function(x){ return x.l; }).join(' · '); }
    fLisR.textContent = rot || 'Relacionados';
    escreve(fLis, lista);
    lS.style.visibility = s ? 'visible' : 'hidden'; if(s) lS.href = s.p;
    lN.style.visibility = n && n.p ? 'visible' : 'hidden'; if(n && n.p) lN.href = n.p;
    bSolta.hidden = !fixo; fDica.hidden = fixo;
  }

  /* ----- temas */
  var lado = raiz.querySelector('.md-temas'), bts = [].slice.call(lado.querySelectorAll('button')), setL = raiz.querySelector('.md-set');
  setL.insertAdjacentHTML('beforeend', D.S.map(function(s, i){ return '<button type="button" data-s="' + i + '" aria-selected="false"><b>' + (i + 1) + '</b>' + s.n + '</button>'; }).join(''));
  btS = [].slice.call(setL.querySelectorAll('button'));
  btS.forEach(function(b, i){
    b.addEventListener('click', function(){
      if(fixo && foco && foco.s === i && foco.n === undefined){ fixo = false; poeFoco(null); return; }
      fixo = true; poeFoco({s:i});
    });
  });
  function desliza(caixa){
    var b = caixa.querySelector('button[aria-selected=true]'), d = caixa.querySelector('.md-desl');
    d.style.opacity = b ? 1 : 0; if(!b) return;
    d.style.width = b.offsetWidth + 'px'; d.style.height = b.offsetHeight + 'px';
    d.style.transform = 'translate(' + b.offsetLeft + 'px,' + b.offsetTop + 'px)';
  }
  function moveDesl(){ desliza(lado); desliza(setL); }
  function poeVista(v, seco){
    vista = v;
    bts.forEach(function(b){ b.setAttribute('aria-selected', +b.getAttribute('data-g') === v); });
    moveDesl();
    for(var j = 0; j < nN; j++){ cwA[j] = cw[j]; cwB[j] = v < 0 || D.N[j].g === v ? 1 : 0; }
    tA = t; tB = v < 0 ? 0 : 1; mIni = performance.now();
    if(seco || quieto){ mIni = -1e9; for(j = 0; j < nN; j++) cw[j] = cwB[j]; t = tB; }
    if(fixo && foco && foco.n !== undefined && cwB[foco.n] === 0){ fixo = false; poeFoco(null); }
    pede();
  }
  bts.forEach(function(b){
    b.addEventListener('click', function(){ fixo = false; poeVista(+b.getAttribute('data-g')); poeFoco(null); });
    b.addEventListener('mouseenter', function(){ var v = +b.getAttribute('data-g'); if(!fixo && v >= 0 && vista < 0) poeFoco({g:v}); });
    b.addEventListener('mouseleave', function(){ if(!fixo && foco && foco.g !== undefined) poeFoco(null); });
  });

  /* modo: todas as relacoes ou so o destaque do setor */
  var modo = raiz.querySelector('.md-modo'), bm = [].slice.call(modo.querySelectorAll('button'));
  bm.forEach(function(b, n){
    b.addEventListener('click', function(){
      bm.forEach(function(o){ o.setAttribute('aria-selected', o === b); });
      modo.style.setProperty('--i', n);
      tvA = n ? 0 : 1;
      pede();
    });
  });

  /* ----- mouse: bloco de cima primeiro, depois rotulo, depois piso */
  function acerta(mx, my){
    var g = geo, X = g.X, u = g.u, by = g.by, i, j;
    if(!plano) for(i = nS - 1; i >= 0; i--) for(j = nN - 1; j >= 0; j--){
      var c = cel[i][j]; if(c.k === 0 || cw[j] < .03 || (c.k === 1 && tv < .04)) continue;
      var w = cw[j], x0 = X[j] + w * (1 - g.fx) / 2, x1 = x0 + w * g.fx, y0 = i * by + by * (1 - g.fy) / 2, y1 = y0 + by * g.fy;
      var h = (c.k === 2 ? g.hD : g.hT) * c.ent + c.lift;
      if(dentroHex(mx, my, x0, x1, y0, y1, h)) return {s:i, n:j};
    }
    var fs = g.fs, gap = folgaS(t) / u, gapN = folgaN(t) / u;
    for(i = 0; i < nS; i++){
      var sxx = sx(-gap, (i + .5) * by), syy = sy(-gap, (i + .5) * by), lx = (mx - sxx) / C, ly = (my - syy) - S * lx, wS = D.S[i].w * fs / 13;
      if(lx <= 8 && lx >= -wS - 8 && Math.abs(ly) < Math.max(fs * .7, by * u * C * .42)) return {s:i};
    }
    for(j = 0; j < nN; j++){
      if(cw[j] < .04) continue;
      var xs = X[j] + cw[j] / 2, nxx = sx(xs, -gapN), nyy = sy(xs, -gapN), lx2 = (mx - nxx) / C, ly2 = (my - nyy) + S * lx2, wN = D.N[j].w * fs / 13;
      if(lx2 >= -8 && lx2 <= wN + 8 && Math.abs(ly2) < Math.max(fs * .6, cw[j] * u * .5)) return {n:j};
    }
    if(t < .5){
      for(var k = 0; k < lanes.length; k++){
        var l = lanes[k], ax = sx(X[l.a], g.Dy), ay = sy(X[l.a], g.Dy) + g.esp * u, d = 9 + l.l * 15, ox = ax - d * C - 5 * C + 2, oy = ay + d * S + 5 * S + 3;
        var lx3 = (mx - ox) / C, ly3 = (my - oy) - S * lx3;
        if(lx3 >= -3 && lx3 <= D.G[l.g].w + 4 && Math.abs(ly3) < 7) return {g:l.g};
      }
    }
    var dxx = (mx - g.ox) / (C * u), dyy = (my - g.oy) / (S * u), a = (dxx + dyy) / 2, b = (dyy - dxx) / 2;
    if(a >= 0 && a <= g.L && b >= 0 && b <= g.Dy){
      for(j = 0; j < nN; j++) if(a >= X[j] && a <= X[j + 1] && cw[j] > .03) return {s:clamp(Math.floor(b / by), 0, nS - 1), n:j};
    }
    return null;
  }
  function dentroHex(mx, my, x0, x1, y0, y1, h){
    var u = geo.u, zh = h * u;
    var p = [sx(x0, y0), sy(x0, y0, h), sx(x1, y0), sy(x1, y0, h), sx(x1, y1 - y1 + y0), sy(x1, y0, 0), sx(x1, y1), sy(x1, y1, 0), sx(x0, y1), sy(x0, y1, 0), sx(x0, y1), sy(x0, y1, h)];
    var ok = false, n = p.length / 2;
    for(var a = 0, b = n - 1; a < n; b = a++){
      var xa = p[a * 2], ya = p[a * 2 + 1], xb = p[b * 2], yb = p[b * 2 + 1];
      if((ya > my) !== (yb > my) && mx < (xb - xa) * (my - ya) / (yb - ya) + xa) ok = !ok;
    }
    return ok;
  }
  var igual = function(a, b){ return (!a && !b) || (a && b && a.s === b.s && a.n === b.n && a.g === b.g); };
  cv.addEventListener('pointermove', function(e){
    var r = cv.getBoundingClientRect(), a = acerta(e.clientX - r.left, e.clientY - r.top);
    cv.style.cursor = a ? 'pointer' : 'default';
    if(fixo || e.pointerType === 'touch') return;
    if(!igual(a, foco)) poeFoco(a);
  });
  cv.addEventListener('pointerleave', function(){ if(!fixo && foco) poeFoco(null); cv.style.cursor = 'default'; });
  cv.addEventListener('click', function(e){
    var r = cv.getBoundingClientRect(), a = acerta(e.clientX - r.left, e.clientY - r.top);
    if(a && a.g !== undefined){ fixo = false; poeVista(a.g); poeFoco(null); return; }
    if(!a){ fixo = false; poeFoco(null); return; }
    if(fixo && igual(a, foco)){ fixo = false; poeFoco(a); return; }
    fixo = true; poeFoco(a);
  });
  bSolta.addEventListener('click', function(){ fixo = false; poeFoco(null); });
  cv.addEventListener('keydown', function(e){
    var f = foco && foco.s !== undefined && foco.n !== undefined ? foco : null, vis = [];
    for(var j = 0; j < nN; j++) if(cwB[j] > 0) vis.push(j);
    var s = f ? f.s : 0, p = f ? vis.indexOf(f.n) : 0;
    if(e.key === 'ArrowDown') s = Math.min(nS - 1, s + (f ? 1 : 0));
    else if(e.key === 'ArrowUp') s = Math.max(0, s - (f ? 1 : 0));
    else if(e.key === 'ArrowRight') p = Math.min(vis.length - 1, p + (f ? 1 : 0));
    else if(e.key === 'ArrowLeft') p = Math.max(0, p - (f ? 1 : 0));
    else if(e.key === 'Enter' && foco){ fixo = !fixo; ficha(); e.preventDefault(); return; }
    else if(e.key === 'Escape'){ fixo = false; poeFoco(null); return; }
    else return;
    e.preventDefault();
    poeFoco({s:s, n:vis[p]});
  });
  document.addEventListener('keydown', function(e){ if(e.key === 'Escape' && fixo){ fixo = false; poeFoco(null); } });

  /* ----- entrada: os blocos sobem em onda toda vez que a grade entra na tela */
  function entra(){
    var agora = performance.now();
    entrada = 1;
    for(var i = 0; i < nS; i++) for(var j = 0; j < nN; j++){ var c = cel[i][j]; c.ent = 0; c.entD = agora + (quieto ? 0 : ((j / nN) * 800 + (i / nS) * 340)); }
    pede();
  }
  if('IntersectionObserver' in window){
    var fora = true;
    new IntersectionObserver(function(es){
      es.forEach(function(e){
        if(e.isIntersecting && e.intersectionRatio >= .18 && fora){ fora = false; entra(); }
        else if(!e.isIntersecting && !fora){ fora = true; }
      });
    }, {threshold:[0, .18]}).observe(raiz);
  } else entra();

  /* ----- tamanho, cor e fonte */
  function ajusta(){
    var r = cv.getBoundingClientRect();
    W = r.width; H = r.height; dpr = Math.min(2, window.devicePixelRatio || 1);
    cv.width = Math.round(W * dpr); cv.height = Math.round(H * dpr);
    var era = movel; movel = window.innerWidth <= 760;
    lado.classList.toggle('sem-todas', movel);
    if(movel && vista < 0) poeVista(0, true);
    if(era && !movel) moveDesl();
    mede(); faixas(); moveDesl(); desenha();
  }
  cores(); ajusta(); ficha();
  if('ResizeObserver' in window) new ResizeObserver(function(){ ajusta(); }).observe(cv); else window.addEventListener('resize', ajusta);
  if(document.fonts && document.fonts.ready) document.fonts.ready.then(function(){ mede(); faixas(); pede(); });
  new MutationObserver(function(){ cores(); pede(); }).observe(document.body, {attributes:true, attributeFilter:['data-acento']});
}
})();
