// ===== SWIPE-BASED DUCT RUN BUILDER =====
// One run at a time, full screen. Swipe between runs.
// Supply section first, then Return section.

var RB = { runs: [], idx: 0, editPiece: -1 };

// Piece catalog
var RB_PIECES = {
  straight: { name:'Straight Duct', hasLen:true, hasMat:true, hasSize:true },
  elbow90:  { name:'90\u00B0 Elbow', eqFn:function(d){return d<=6?10:d<=8?15:d<=10?20:25;} },
  elbow45:  { name:'45\u00B0 Elbow', eqFn:function(){return 5;} },
  reducer:  { name:'Reducer',    eqFn:function(){return 5;}, hasSize:true },
  wye:      { name:'Wye',        eqFn:function(){return 15;} },
  dbox:     { name:'Dist Box',   eqFn:function(){return 50;} },
  boot:     { name:'Boot',       isEnd:true }
};
var RB_BOOTS = {
  '90boot':{name:'90\u00B0 Boot',eq:55},'straightboot':{name:'Straight Boot',eq:35},
  'ceilTop':{name:'Ceiling (top)',eq:10},'ceilSide':{name:'Ceiling (side)',eq:40},
  'floorReg':{name:'Floor Register',eq:35},'wallReg':{name:'Wall Register',eq:40}
};

// --- Init runs from collars + rooms ---
function rbInit() {
  RB.runs = []; RB.idx = 0; RB.editPiece = -1;
  var supCollars = (typeof SS!=='undefined'&&SS.collars)||[];
  var retCollars = (typeof SS!=='undefined'&&SS.retCollars)||[];
  var rooms = typeof getRoomsList==='function'?getRoomsList():[];
  var supTrunks = WIZ.trunks.filter(function(t){return t.airPath==='supply';});
  var retTrunks = WIZ.trunks.filter(function(t){return t.airPath==='return';});

  // Supply: one run per collar, assign rooms round-robin
  var ri = 0;
  supCollars.forEach(function(col,ci){
    var ti = supTrunks.length>0?WIZ.trunks.indexOf(supTrunks[ci%supTrunks.length]):0;
    var rm = ri<rooms.length?rooms[ri]:null; ri++;
    RB.runs.push({
      collar:col, collarSize:parseInt(col.size)||8, airPath:'supply',
      trunkIdx:ti, pieces:[], room:rm?rm.name:'Supply '+(ci+1),
      cfm:rm?(rm.cfm||0):0
    });
  });
  // Return: one run per collar
  var totalCfm = typeof getRoomsTotalCFM==='function'?getRoomsTotalCFM():0;
  retCollars.forEach(function(col,ci){
    var ti = retTrunks.length>0?WIZ.trunks.indexOf(retTrunks[ci%retTrunks.length]):0;
    var retCfm = retCollars.length>0?Math.round(totalCfm/retCollars.length):totalCfm;
    RB.runs.push({
      collar:col, collarSize:parseInt(col.size)||14, airPath:'return',
      trunkIdx:ti, pieces:[], room:'Return '+(ci+1), cfm:retCfm
    });
  });
  // Fallback if no collars
  if (RB.runs.length===0 && rooms.length>0) {
    rooms.forEach(function(rm,i){
      var ti = supTrunks.length>0?WIZ.trunks.indexOf(supTrunks[i%supTrunks.length]):0;
      RB.runs.push({
        collar:{size:'8',type:'tab'}, collarSize:8, airPath:'supply',
        trunkIdx:ti, pieces:[], room:rm.name, cfm:rm.cfm||0
      });
    });
  }
}

// --- Helpers ---
function rbUpSize(run,upTo) {
  var s=run.collarSize; var p=run.pieces;
  var end=typeof upTo==='number'?upTo:p.length;
  for(var i=0;i<end;i++) if(p[i].size) s=p[i].size;
  return s;
}
function rbRecSize(cfm,upSize,mat,comp) {
  if(!cfm||cfm<=0) return upSize||6;
  var c=(mat==='flex')?(comp||10):0;
  var ff=(mat==='flex'&&typeof wizFlexFactor==='function')?wizFlexFactor(c):((mat==='flex')?1.67:1);
  var sizes=[4,5,6,7,8,9,10,12,14,16,18,20,22,24];
  for(var i=0;i<sizes.length;i++){
    var d=sizes[i]; if(upSize&&d>upSize) break;
    var A=Math.PI*Math.pow(d/12/2,2); var v=cfm/A;
    if(v>(mat==='flex'?700:900)) continue;
    var fr=typeof frictionLoss==='function'?frictionLoss(d,cfm):0.08;
    if(fr*ff<=0.08) return d;
  }
  return upSize||6;
}
function rbRunDone(run){
  return run.pieces.length>0&&run.pieces[run.pieces.length-1].type==='boot';
}
function rbCalcTEL(run) {
  var tel=0;
  var trunk=WIZ.trunks[run.trunkIdx]||WIZ.trunks[0];
  // Plenum EQ
  var isRet=run.airPath==='return';
  var plEl=isRet?document.getElementById('retPlType'):document.getElementById('plType');
  var plVal=plEl?plEl.value:(isRet?'box':'tapered');
  tel+=WIZ_PLENUM_EQ[plVal]||10;
  // Trunk
  if(trunk&&!trunk.isRadial){
    var tLen=parseFloat(trunk.length)||0;
    var tDia=typeof wizEffDia==='function'?wizEffDia(trunk):12;
    var tFF=trunk.material==='ductboard'?1.2:(trunk.material==='flex'&&typeof wizFlexFactor==='function'?wizFlexFactor(trunk.compression):1);
    tel+=tLen*tFF;
    tel+=(trunk.elbows90||0)*(tDia<=6?10:tDia<=8?15:tDia<=10?20:25);
    tel+=(trunk.elbows45||0)*5;
    tel+=(trunk.distBoxes||0)*50;
  }
  // Pieces
  run.pieces.forEach(function(p){
    var pt=RB_PIECES[p.type];
    if(p.type==='straight'){
      var len=parseFloat(p.length)||0;
      var ff=p.material==='flex'?(typeof wizFlexFactor==='function'?wizFlexFactor(p.compression||10):1.67):(p.material==='ductboard'?1.2:1);
      tel+=len*ff;
    } else if(p.type==='boot'){
      tel+=(RB_BOOTS[p.bootType]||{eq:35}).eq;
    } else if(pt&&pt.eqFn){
      tel+=pt.eqFn(p.size||rbUpSize(run,run.pieces.indexOf(p)));
    }
  });
  return tel;
}

// --- Piece icons (compact SVGs) ---
function rbIcon(t) {
  var s = {
    straight:'<svg viewBox="0 0 24 24" width="18" height="18"><rect x="8" y="3" width="8" height="18" rx="1.5" fill="none" stroke="currentColor" stroke-width="1.5"/></svg>',
    elbow90:'<svg viewBox="0 0 24 24" width="18" height="18"><path d="M8 3v10a5 5 0 005 5h8" fill="none" stroke="currentColor" stroke-width="1.5" stroke-linecap="round"/></svg>',
    elbow45:'<svg viewBox="0 0 24 24" width="18" height="18"><path d="M9 3v7l8 11" fill="none" stroke="currentColor" stroke-width="1.5" stroke-linecap="round"/></svg>',
    reducer:'<svg viewBox="0 0 24 24" width="18" height="18"><path d="M6 3v7l4 4v7M18 3v7l-4 4v7" fill="none" stroke="currentColor" stroke-width="1.5"/></svg>',
    wye:'<svg viewBox="0 0 24 24" width="18" height="18"><line x1="12" y1="3" x2="12" y2="12" stroke="currentColor" stroke-width="1.5"/><line x1="12" y1="12" x2="5" y2="21" stroke="currentColor" stroke-width="1.5"/><line x1="12" y1="12" x2="19" y2="21" stroke="currentColor" stroke-width="1.5"/></svg>',
    dbox:'<svg viewBox="0 0 24 24" width="18" height="18"><rect x="4" y="6" width="16" height="12" rx="2" fill="none" stroke="currentColor" stroke-width="1.5"/><line x1="12" y1="2" x2="12" y2="6" stroke="currentColor" stroke-width="1.5"/><circle cx="8" cy="18" r="1.5" fill="currentColor"/><circle cx="16" cy="18" r="1.5" fill="currentColor"/></svg>',
    boot:'<svg viewBox="0 0 24 24" width="18" height="18"><rect x="8" y="3" width="8" height="8" rx="1" fill="none" stroke="currentColor" stroke-width="1.5"/><path d="M8 11L4 17h16l-4-6" fill="none" stroke="currentColor" stroke-width="1.5"/><line x1="6" y1="20" x2="18" y2="20" stroke="currentColor" stroke-width="2"/></svg>'
  };
  return s[t]||'<svg viewBox="0 0 24 24" width="18" height="18"><circle cx="12" cy="12" r="6" fill="none" stroke="currentColor" stroke-width="1.5"/></svg>';
}

// ============ RENDER ============
function rbRender() {
  var el=document.getElementById('wizBranchArea');
  if(!el) return;
  // Auto-init if needed
  if(RB.runs.length===0) rbInit();
  if(RB.runs.length===0){ el.innerHTML='<div style="text-align:center;padding:20px;color:var(--text-3)">No start collars defined. Go back to Trunks and add collars on the plenum.</div>'; return; }

  var supRuns=RB.runs.filter(function(r){return r.airPath==='supply';});
  var retRuns=RB.runs.filter(function(r){return r.airPath==='return';});
  var run=RB.runs[RB.idx];
  var isSupply=run.airPath==='supply';
  var sectionRuns=isSupply?supRuns:retRuns;
  var sectionIdx=sectionRuns.indexOf(run);

  var h='';

  // Section toggle (Supply / Return)
  if(supRuns.length>0&&retRuns.length>0){
    h+='<div class="rb-seg" style="margin-bottom:10px">';
    h+='<div class="rb-seg-btn'+(isSupply?' active':'')+'" data-rb-section="supply">Supply ('+supRuns.length+')</div>';
    h+='<div class="rb-seg-btn'+(!isSupply?' active':'')+'" data-rb-section="return">Return ('+retRuns.length+')</div>';
    h+='</div>';
  }

  // Counter + dots
  h+='<div class="rb-counter"><strong>'+(sectionIdx+1)+'</strong> of '+sectionRuns.length+' '+(isSupply?'supply':'return')+' runs</div>';
  h+='<div class="rb-dots">';
  sectionRuns.forEach(function(r,i){
    var cls='rb-dot';
    if(i===sectionIdx) cls+=' active';
    else if(rbRunDone(r)) cls+=' done';
    h+='<div class="'+cls+'" data-rb-go-dot="'+RB.runs.indexOf(r)+'"></div>';
  });
  h+='</div>';

  // Swipe area with arrows
  h+='<div class="rb-swipe-wrap">';
  if(sectionIdx>0) h+='<div class="rb-arrow rb-arrow-left" data-rb-prev>&#x2039;</div>';
  if(sectionIdx<sectionRuns.length-1) h+='<div class="rb-arrow rb-arrow-right" data-rb-next>&#x203A;</div>';

  // The run card
  h+='<div class="rb-run-card">';

  // Header
  h+='<div class="rb-run-hdr">';
  h+='<div class="rb-run-title">'+run.room+'</div>';
  h+='<div class="rb-run-badges">';
  h+='<span class="rb-badge '+(isSupply?'rb-badge-sup':'rb-badge-ret')+'">'+(isSupply?'SUP':'RTN')+'</span>';
  h+='<span class="rb-badge rb-badge-size">'+run.collarSize+'&#x2033;</span>';
  h+='</div></div>';

  // Room + CFM fields
  h+='<div class="rb-fields">';
  h+='<div class="rb-field"><label>Room</label><input type="text" class="input-field" value="'+run.room+'" data-rb-room></div>';
  h+='<div class="rb-field" style="max-width:90px"><label>CFM</label><input type="number" class="input-field" value="'+(run.cfm||'')+'" placeholder="CFM" data-rb-cfm></div>';
  h+='</div>';

  // Piece chain
  h+='<div class="rb-chain">';

  // Start collar node
  h+='<div class="rb-node rb-node-start">';
  h+='<div class="rb-node-card">';
  h+='<div class="rb-node-icon">'+rbIcon('straight')+'</div>';
  h+='<div class="rb-node-body"><div class="rb-node-name">Start Collar</div>';
  h+='<div class="rb-node-detail">'+run.collarSize+'&#x2033; '+(run.collar?run.collar.type:'')+'</div></div>';
  h+='</div></div>';

  // Each placed piece
  run.pieces.forEach(function(p,pi){
    var pt=RB_PIECES[p.type]||{};
    var isActive=pi===RB.editPiece;
    var isEnd=p.type==='boot';
    var upSz=rbUpSize(run,pi);

    h+='<div class="rb-node'+(isActive?' rb-node-active':'')+(isEnd?' rb-node-end':'')+'" data-rb-tap="'+pi+'">';
    h+='<div class="rb-node-card">';
    h+='<div class="rb-node-icon">'+rbIcon(p.type)+'</div>';
    h+='<div class="rb-node-body"><div class="rb-node-name">'+(pt.name||p.type)+'</div>';
    h+='<div class="rb-node-detail">';
    if(p.type==='straight'){
      h+=(p.size||'?')+'&#x2033; '+(p.material||'flex')+' &middot; '+(p.length||0)+'ft';
      if(p.material==='flex'&&p.compression) h+=' &middot; '+p.compression+'%';
    } else if(p.type==='reducer'){
      h+=upSz+'&#x2033; &#x2192; '+(p.size||'?')+'&#x2033; (+5ft)';
    } else if(p.type==='boot'){
      var bt=RB_BOOTS[p.bootType]||{};
      h+=(bt.name||'Boot')+' (+'+((bt.eq||0))+'ft)';
    } else {
      var eq=pt.eqFn?pt.eqFn(p.size||upSz):0;
      h+='+'+eq+'ft EQ';
    }
    h+='</div></div>';
    h+='<div class="rb-node-x" data-rb-del="'+pi+'">&times;</div>';
    h+='</div></div>';

    // Edit panel
    if(isActive) h+=rbEditHTML(run,p,pi);
  });

  h+='</div>'; // /chain

  // Stats bar
  var tel=rbCalcTEL(run);
  var frNum=0;
  var espEl=document.getElementById('wizESP');
  var coilEl=document.getElementById('wizCoilPD');
  var asp=(espEl?parseFloat(espEl.value):0.5)-(coilEl?parseFloat(coilEl.value):0.07);
  if(tel>0) frNum=asp/tel*100;
  var frCls=frNum<=0.05?'good':frNum<=0.08?'warn':'bad';

  h+='<div class="rb-stats">';
  h+='<div class="rb-stat"><div class="rb-stat-val">'+Math.round(tel)+'</div><div class="rb-stat-lbl">TEL (ft)</div></div>';
  h+='<div class="rb-stat"><div class="rb-stat-val '+(tel>0?frCls:'')+'">'+frNum.toFixed(3)+'</div><div class="rb-stat-lbl">FR (IWC/100ft)</div></div>';
  h+='<div class="rb-stat"><div class="rb-stat-val">'+(run.cfm||'—')+'</div><div class="rb-stat-lbl">CFM</div></div>';
  h+='</div>';

  // Add piece palette (or done banner)
  if(!rbRunDone(run)){
    h+='<div class="rb-add-section">';
    h+='<div class="rb-add-title">Add next piece</div>';
    h+='<div class="rb-add-grid">';
    ['straight','elbow90','elbow45','reducer','wye','dbox','boot'].forEach(function(k){
      h+='<div class="rb-add-btn" data-rb-add="'+k+'">';
      h+=rbIcon(k);
      h+='<div class="rb-add-lbl">'+RB_PIECES[k].name+'</div></div>';
    });
    h+='</div></div>';
  } else {
    h+='<div class="rb-done-banner">';
    h+='<svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M22 11.08V12a10 10 0 1 1-5.93-9.14"/><polyline points="22 4 12 14.01 9 11.01"/></svg>';
    h+=' Run complete';
    // Auto-advance prompt
    if(sectionIdx<sectionRuns.length-1){
      h+=' &mdash; <span data-rb-next style="text-decoration:underline;cursor:pointer">next run &#x203A;</span>';
    }
    h+='</div>';
  }

  h+='</div>'; // /run-card
  h+='</div>'; // /swipe-wrap

  el.innerHTML=h;
}

// --- Edit HTML for a piece ---
function rbEditHTML(run,p,idx) {
  var h='<div class="rb-edit">';
  var up=rbUpSize(run,idx);
  var rec=rbRecSize(run.cfm,up,p.material||WIZ.material,p.compression||10);

  if(p.type==='straight'){
    // Material
    h+='<div class="rb-edit-row"><label class="input-label">Material</label>';
    h+='<div class="rb-seg">';
    h+='<div class="rb-seg-btn'+(p.material!=='flex'?' active':'')+'" data-rb-set="material" data-rb-v="metal" data-rb-i="'+idx+'">Metal</div>';
    h+='<div class="rb-seg-btn'+(p.material==='flex'?' active':'')+'" data-rb-set="material" data-rb-v="flex" data-rb-i="'+idx+'">Flex</div>';
    h+='</div></div>';
    // Size
    h+='<div class="rb-edit-row"><label class="input-label">Size <span class="rb-rec-tag">rec: '+rec+'&#x2033;</span></label>';
    h+='<select class="input-field" data-rb-sel="size" data-rb-i="'+idx+'">';
    [4,5,6,7,8,9,10,12,14,16,18,20,22,24].forEach(function(s){
      if(s>up) return;
      h+='<option value="'+s+'"'+(p.size==s?' selected':'')+'>'+s+'&#x2033;'+(s==rec?' \u2190 rec':'')+'</option>';
    });
    h+='</select></div>';
    // Length
    h+='<div class="rb-edit-row"><label class="input-label">Length (ft)</label>';
    h+='<input type="number" class="input-field" value="'+(p.length||12)+'" min="1" max="200" data-rb-inp="length" data-rb-i="'+idx+'"></div>';
    // Compression
    if(p.material==='flex'){
      h+='<div class="rb-edit-row"><label class="input-label">Compression %</label>';
      h+='<div class="rb-comp-chips">';
      [4,5,10,15,20,25,30].forEach(function(c){
        h+='<div class="rb-comp-chip'+(p.compression==c?' active':'')+'" data-rb-set="compression" data-rb-v="'+c+'" data-rb-i="'+idx+'">'+c+'%</div>';
      });
      h+='</div></div>';
    }
  }
  if(p.type==='reducer'){
    h+='<div class="rb-edit-row"><label class="input-label">Reduce from '+up+'&#x2033; to:</label>';
    h+='<select class="input-field" data-rb-sel="size" data-rb-i="'+idx+'">';
    [4,5,6,7,8,9,10,12,14,16,18,20,22,24].forEach(function(s){
      if(s>=up) return;
      h+='<option value="'+s+'"'+(p.size==s?' selected':'')+'>'+s+'&#x2033;</option>';
    });
    h+='</select></div>';
  }
  if(p.type==='boot'){
    h+='<div class="rb-edit-row"><label class="input-label">Boot Type</label>';
    h+='<select class="input-field" data-rb-sel="bootType" data-rb-i="'+idx+'">';
    Object.keys(RB_BOOTS).forEach(function(k){
      var b=RB_BOOTS[k];
      h+='<option value="'+k+'"'+(p.bootType===k?' selected':'')+'>'+b.name+' (+'+b.eq+'ft)</option>';
    });
    h+='</select></div>';
  }
  h+='<button class="rb-btn-done" data-rb-done>Done</button>';
  h+='</div>';
  return h;
}

// ============ ACTIONS ============
function rbAddPiece(type){
  var run=RB.runs[RB.idx]; if(!run||rbRunDone(run)) return;
  var up=rbUpSize(run,run.pieces.length);
  var rec=rbRecSize(run.cfm,up,WIZ.material,10);
  var p={type:type};
  if(type==='straight'){
    p.material=WIZ.material||'flex'; p.size=rec; p.length=12;
    p.compression=p.material==='flex'?10:0; p.shape='round';
  } else if(type==='reducer'){
    var sizes=[4,5,6,7,8,9,10,12,14,16,18,20,22,24];
    var ns=up; for(var i=sizes.length-1;i>=0;i--){if(sizes[i]<up){ns=sizes[i];break;}}
    p.size=ns;
  } else if(type==='boot'){
    p.bootType='90boot';
  }
  run.pieces.push(p);
  RB.editPiece=run.pieces.length-1;
  rbRender();
  // Scroll edit into view
  setTimeout(function(){
    var ed=document.querySelector('.rb-edit');
    if(ed) ed.scrollIntoView({behavior:'smooth',block:'center'});
  },50);
}

function rbSetProp(idx,prop,val){
  var run=RB.runs[RB.idx]; if(!run||!run.pieces[idx]) return;
  var p=run.pieces[idx];
  if(prop==='size'||prop==='length'||prop==='compression') p[prop]=parseInt(val)||0;
  else p[prop]=val;
  if(prop==='material'){
    if(val==='flex'){p.compression=p.compression||10;p.shape='round';}
    else p.compression=0;
  }
  rbRender();
}

function rbNav(dir){
  var run=RB.runs[RB.idx];
  var isS=run.airPath==='supply';
  var section=RB.runs.filter(function(r){return r.airPath===(isS?'supply':'return');});
  var si=section.indexOf(run);
  var newSi=si+dir;
  if(newSi>=0&&newSi<section.length){
    RB.idx=RB.runs.indexOf(section[newSi]);
    RB.editPiece=-1;
    rbRender();
    document.getElementById('wizBranchArea').scrollIntoView({behavior:'smooth',block:'start'});
  }
}

function rbSwitchSection(airPath){
  var section=RB.runs.filter(function(r){return r.airPath===airPath;});
  if(section.length>0){
    RB.idx=RB.runs.indexOf(section[0]);
    RB.editPiece=-1;
    rbRender();
  }
}

// ============ EVENT HANDLERS ============
function rbHandleClick(e){
  var t=e.target;
  // Section toggle
  var sec=t.closest('[data-rb-section]'); if(sec){rbSwitchSection(sec.dataset.rbSection);return;}
  // Dot nav
  var dot=t.closest('[data-rb-go-dot]'); if(dot){RB.idx=parseInt(dot.dataset.rbGoDot);RB.editPiece=-1;rbRender();return;}
  // Arrow nav
  if(t.closest('[data-rb-prev]')){rbNav(-1);return;}
  if(t.closest('[data-rb-next]')){rbNav(1);return;}
  // Add piece
  var add=t.closest('[data-rb-add]'); if(add){rbAddPiece(add.dataset.rbAdd);return;}
  // Delete piece
  var del=t.closest('[data-rb-del]');
  if(del){var di=parseInt(del.dataset.rbDel);var run=RB.runs[RB.idx];if(run){run.pieces.splice(di,1);if(RB.editPiece>=run.pieces.length)RB.editPiece=-1;if(RB.editPiece===di)RB.editPiece=-1;rbRender();}return;}
  // Tap piece to edit
  var tap=t.closest('[data-rb-tap]');
  if(tap&&!t.closest('[data-rb-del]')&&!t.closest('.rb-edit')){
    var pi=parseInt(tap.dataset.rbTap);
    RB.editPiece=(RB.editPiece===pi)?-1:pi;
    rbRender(); return;
  }
  // Segment btn
  var seg=t.closest('[data-rb-set]');
  if(seg&&seg.dataset.rbV!==undefined){rbSetProp(parseInt(seg.dataset.rbI),seg.dataset.rbSet,seg.dataset.rbV);return;}
  // Done
  if(t.closest('[data-rb-done]')){RB.editPiece=-1;rbRender();return;}
}

function rbHandleChange(e){
  var t=e.target;
  // Select
  if(t.dataset.rbSel){rbSetProp(parseInt(t.dataset.rbI),t.dataset.rbSel,t.value);return;}
  // Input
  if(t.dataset.rbInp){rbSetProp(parseInt(t.dataset.rbI),t.dataset.rbInp,t.value);return;}
  // Room
  if(t.hasAttribute('data-rb-room')){var r=RB.runs[RB.idx];if(r)r.room=t.value;}
  // CFM
  if(t.hasAttribute('data-rb-cfm')){var r=RB.runs[RB.idx];if(r)r.cfm=parseInt(t.value)||0;}
}

// ============ TRANSLATE TO WIZ.branches ============
function rbTranslateToBranches(){
  WIZ.branches=[];
  var num=1;
  RB.runs.forEach(function(run){
    var totLen=0, mat=WIZ.material, comp=0, sz=run.collarSize;
    var fittings=[], bootType='90boot', shape='round';
    run.pieces.forEach(function(p){
      if(p.type==='straight'){
        totLen+=parseFloat(p.length)||0;
        mat=p.material||mat; comp=p.compression||comp;
        if(p.size) sz=p.size;
      } else if(p.type==='boot'){
        bootType=p.bootType||'90boot';
      } else if(p.type==='reducer'){
        if(p.size) sz=p.size;
        fittings.push({type:'reducer'});
      } else {
        fittings.push({type:p.type});
      }
    });
    WIZ.branches.push({
      trunkIdx:run.trunkIdx, num:num++, room:run.room, cfm:run.cfm||'',
      shape:shape, size:String(sz), width:'8', height:'8',
      material:mat, compression:comp, length:String(totLen),
      fittings:fittings, bootType:bootType, takeoffType:'straight90',
      done:rbRunDone(run), recommended:String(sz), runouts:[]
    });
  });
}

// Legacy compat
function rbInitRuns(){ rbInit(); }
