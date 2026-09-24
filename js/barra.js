/* barra da home nas paginas internas. Gerado por _ferramentas/barra.py a
   partir do index.html: a home continua a fonte. */
// scramble do modelo (chars "x&im" da marca; 0,5s no hover, do "_" na entrada)
function scramble(alvoNo, texto, dur){
  var chars = 'x&im';
  var t0 = null, alvo = texto;
  function tique(ts){
    if(!t0) t0 = ts;
    var p = Math.min(1, (ts - t0) / dur);
    var n = Math.round(p * alvo.length);
    var s = alvo.slice(0, n);
    for(var i = n; i < alvo.length; i++)
      s += alvo[i] === ' ' ? ' ' : chars[Math.floor(Math.random() * chars.length)];
    alvoNo.nodeValue = s;
    if(p < 1) requestAnimationFrame(tique);
  }
  requestAnimationFrame(tique);
}
/* escreve so no no de texto, para nao apagar seta em SVG nem camada de
   hover que viva dentro do mesmo botao */
function noDeTexto(el){
  for(var i = 0; i < el.childNodes.length; i++)
    if(el.childNodes[i].nodeType === 3 && el.childNodes[i].nodeValue.trim()) return el.childNodes[i];
  return null;
}
document.querySelectorAll('.js-scramble').forEach(function(el){
  var no = noDeTexto(el);
  if(!no) return;
  var texto = no.nodeValue;
  el.addEventListener('mouseenter', function(){ scramble(no, texto, 500); });
});

// menu véu
(function(){
  var veu = document.getElementById('veuMenu');
  if(!veu) return;
  /* o botao vive na barra de topo desde 07/09; o id antigo continua aceito */
  ['abreMenu2','abreMenu'].forEach(function(id){
    var b = document.getElementById(id);
    if(b) b.addEventListener('click', function(){ veu.classList.add('aberto'); });
  });
  var f = document.getElementById('fechaMenu');
  if(f) f.addEventListener('click', function(){ veu.classList.remove('aberto'); });
  /* 24/09: «Todos os servicos» abre um painel DENTRO do veu (js/busca.js), entao nao fecha o veu */
  veu.querySelectorAll('a').forEach(function(a){ if(a.id === 'veuTodos') return; a.addEventListener('click', function(){ veu.classList.remove('aberto'); }); });
})();

// ===== a placa da marca encolhe ao rolar =====
(function(){
  var barra = document.querySelector('.barra');
  if (!barra) return;
  var agendado = false;
  function atualizar(){
    agendado = false;
    barra.classList.toggle('rolou', window.scrollY > 40);
  }
  function pedir(){
    if (!agendado){ agendado = true; requestAnimationFrame(atualizar); }
  }
  window.addEventListener('scroll', pedir, {passive:true});
  atualizar();
})();
/* tarja: data do dia, dd.mm.aaaa */(function(){var e=document.getElementById('tarja-data');if(!e)return;var d=new Date(),z=function(n){return(n<10?'0':'')+n};e.textContent=z(d.getDate())+'.'+z(d.getMonth()+1)+'.'+d.getFullYear();})();
