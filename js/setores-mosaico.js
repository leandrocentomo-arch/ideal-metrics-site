/* Mosaico de normas e padroes da home (09/10/2026): o botao de um setor acende as normas dele (quadro escuro) e as que
   valem para qualquer setor (contorno). O desenho e estatico, gerado por _ferramentas/setores.py. */
(function(){
  var fig = document.getElementById('qcMos'); if(!fig) return;
  var bts = fig.querySelectorAll('.qc-mos-bt button');
  [].forEach.call(bts, function(b){
    b.addEventListener('click', function(){
      var s = b.getAttribute('data-s');
      if(s) fig.setAttribute('data-sel', s); else fig.removeAttribute('data-sel');
      [].forEach.call(bts, function(o){ o.setAttribute('aria-pressed', o === b ? 'true' : 'false'); });
    });
  });
})();
