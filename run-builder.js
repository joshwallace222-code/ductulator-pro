// ===== DUCT RUN BUILDER v3 =====
// Tree model: Collar → Trunk → Multiple Branches → Rooms
// One trunk per collar. User adds branches off each trunk.

var RB = { trunks: [], idx: 0, editBranch: -1, editPiece: -1 };

// Piece types
var RB_PIECES = {
  straight: { name:'Straight Duct', eqFn: null },
  elbow90:  { name:'90\u00B0 Elbow', eqFn:function(d){return d<=6?10:d<=8?15:d<=10?20:25;} },
  elbow45:  { name:'45\u00B0 Elbow', eqFn:function(){return 5;} },
  reducer:  { name:'Reducer',    eqFn:function(){return 5;} },
  dbox:     { name:'Dist Box',   eqFn:function(){return 50;} }
};
var RB_BOOTS = {
  '90boot':{name:'90\u00B0 Boot',eq:55},'straightboot':{name:'Straight Boot',eq:35},
  'ceilTop':{name:'Ceiling (top)',eq:10},'ceilSide':{name:'Ceiling (side)',eq:40},
  'floorReg':{name:'Floor Reg',eq:35},'wallReg':{name:'Wall Reg',eq:40}
};
var RB_TAKEOFFS = {
  'straight90':{name:'90\u00B0 Straight',eq:35},
  'conical':{name:'Conical',eq:10},
  'angle45':{name:'45\u00B0 Angled',eq:20},
  'wye':{name:'Wye',eq:15}
};

// --- Init from wizard trunks ---
function rbInit() {
  RB.trunks = []; RB.idx = 0; RB.editBranch = -1; RB.editPiece = -1;
  var rooms = typeof getRoomsList==='function'?getRoomsList():[];
  var availRooms = rooms.map(function(r,i){ return {name:r.name, cfm:r.cfm, idx:i, assigned:false}; });

  WIZ.trunks.forEach(function(t,ti) {
    RB.trunks.push({
      wizIdx: ti,
      label: t.label,
      airPath: t.airPath || 'supply',
      size: parseInt(t.size) || 12,
      length: parseFloat(t.length) || 0,
      material: t.material || 'metal',
      compression: t.compression || 0,
      branches: []
    });
  });

  // Auto-create one branch per room, distributed across supply trunks
  var supTrunks = RB.trunks.filter(function(t){return t.airPath==='supply';});
  var ri = 0;
  if (supTrunks.length > 0 && rooms.length > 0) {
    rooms.forEach(function(rm, i) {
      var trunk = supTrunks[i % supTrunks.length];
      var recSize = rbRecSize(rm.cfm, trunk.size, trunk.material==='flex'?'flex':'metal', 10);
      trunk.branches.push({
        room: rm.name,
        cfm: rm.cfm || 0,
        roomIdx: i,
        takeoff: 'straight90',
        material: WIZ.material || 'flex',
        size: recSize,
        length: 12,
        compression: (WIZ.material==='flex') ? 10 : 0,
        bootType: '90boot',
        pieces: [], // extra fittings (elbows, reducers)
        complete: false
      });
    });
  }

  // Auto-create return branches
  var retTrunks = RB.trunks.filter(function(t){return t.airPath==='return';});
  var totalCfm = typeof getRoomsTotalCFM==='function'?getRoomsTotalCFM():0;
  retTrunks.forEach(function(trunk, ri) {
    var retCfm = retTrunks.length > 0 ? Math.round(totalCfm / retTrunks.length) : totalCfm;
    var recSize = rbRecSize(retCfm, trunk.size, trunk.material==='flex'?'flex':'metal', 10);
    trunk.branches.push({
      room: 'Return ' + (ri + 1),
      cfm: retCfm,
      roomIdx: -1,
      takeoff: 'straight90',
      material: WIZ.material || 'flex',
      size: recSize,
      length: 10,
      compression: (WIZ.material==='flex') ? 10 : 0,
      bootType: 'wallReg',
      pieces: [],
      complete: false
    });
  });
}

// --- Helpers ---
function rbRecSize(cfm, upSize, mat, comp) {
  if (!cfm || cfm <= 0) return Math.min(upSize || 6, 8);
  var ff = (mat==='flex' && typeof wizFlexFactor==='function') ? wizFlexFactor(comp||10) : (mat==='flex'?1.67:1);
  var sizes = [4,5,6,7,8,9,10,12,14,16,18,20,22,24];
  for (var i=0; i<sizes.length; i++) {
    var d=sizes[i]; if(upSize && d>upSize) break;
    var A=Math.PI*Math.pow(d/12/2,2); var v=cfm/A;
    if (v > (mat==='flex'?700:900)) continue;
    var fr = typeof frictionLoss==='function'?frictionLoss(d,cfm):0.08;
    if (fr*ff <= 0.08) return d;
  }
  return Math.min(upSize||6, 8);
}

function rbIcon(t) {
  var s={
    straight:'<svg viewBox="0 0 24 24" w="18" h="18"><rect x="8" y="3" width="8" height="18" rx="1.5" fill="none" stroke="currentColor" stroke-width="1.5"/></svg>',
    elbow90:'<svg viewBox="0 0 24 24" w="18" h="18"><path d="M8 3v10a5 5 0 005 5h8" fill="none" stroke="currentColor" stroke-width="1.5" stroke-linecap="round"/></svg>',
    elbow45:'<svg viewBox="0 0 24 24" w="18" h="18"><path d="M9 3v7l8 11" fill="none" stroke="currentColor" stroke-width="1.5" stroke-linecap="round"/></svg>',
    reducer:'<svg viewBox="0 0 24 24" w="18" h="18"><path d="M6 3v7l4 4v7M18 3v7l-4 4v7" fill="none" stroke="currentColor" stroke-width="1.5"/></svg>',
    dbox:'<svg viewBox="0 0 24 24" w="18" h="18"><rect x="4" y="6" width="16" height="12" rx="2" fill="none" stroke="currentColor" stroke-width="1.5"/><circle cx="8" cy="18" r="1.5" fill="currentColor"/><circle cx="16" cy="18" r="1.5" fill="currentColor"/></svg>',
    boot:'<svg viewBox="0 0 24 24" w="18" h="18"><rect x="8" y="3" width="8" height="8" rx="1" fill="none" stroke="currentColor" stroke-width="1.5"/><path d="M8 11L4 17h16l-4-6" fill="none" stroke="currentColor" stroke-width="1.5"/><line x1="6" y1="20" x2="18" y2="20" stroke="currentColor" stroke-width="2"/></svg>'
  };
  return (s[t]||'<svg viewBox="0 0 24 24" w="18" h="18"><circle cx="12" cy="12" r="6" fill="none" stroke="currentColor" stroke-width="1.5"/></svg>').replace(/w="/g,'width="').replace(/h="/g,'height="');
}

// ============ RENDER ============
function rbRender() {
  var el = document.getElementById('wizBranchArea');
  if (!el) return;
  if (RB.trunks.length === 0) rbInit();
  if (RB.trunks.length === 0) { el.innerHTML='<div style="text-align:center;padding:20px;color:var(--text-3)">No trunks defined. Go back to Trunks step.</div>'; return; }

  var supTrunks = RB.trunks.filter(function(t){return t.airPath==='supply';});
  var retTrunks = RB.trunks.filter(function(t){return t.airPath==='return';});
  var trunk = RB.trunks[RB.idx];
  var isSupply = trunk.airPath === 'supply';
  var section = isSupply ? supTrunks : retTrunks;
  var sIdx = section.indexOf(trunk);

  var rooms = typeof getRoomsList==='function'?getRoomsList():[];
  var h = '';

  // Section toggle
  if (supTrunks.length>0 && retTrunks.length>0) {
    h+='<div class="rb-seg" style="margin-bottom:8px">';
    h+='<div class="rb-seg-btn'+(isSupply?' active':'')+'" data-rb-section="supply">Supply ('+supTrunks.length+')</div>';
    h+='<div class="rb-seg-btn'+(!isSupply?' active':'')+'" data-rb-section="return">Return ('+retTrunks.length+')</div>';
    h+='</div>';
  }

  // Trunk selector dots
  if (section.length > 1) {
    h+='<div class="rb-dots">';
    section.forEach(function(t,i){
      h+='<div class="rb-dot'+(i===sIdx?' active':'')+'" data-rb-trunk-dot="'+RB.trunks.indexOf(t)+'"></div>';
    });
    h+='</div>';
  }

  // ---- TRUNK CARD ----
  h+='<div class="rb-run-card">';
  
  // Trunk header
  h+='<div class="rb-run-hdr">';
  h+='<div class="rb-run-title">'+trunk.label+'</div>';
  h+='<div class="rb-run-badges">';
  h+='<span class="rb-badge '+(isSupply?'rb-badge-sup':'rb-badge-ret')+'">'+(isSupply?'SUP':'RTN')+'</span>';
  h+='<span class="rb-badge rb-badge-size">'+trunk.size+'&#x2033;</span>';
  if (trunk.length) h+='<span class="rb-badge" style="background:var(--surface-2);color:var(--text-2)">'+trunk.length+'ft</span>';
  h+='</div></div>';

  // Trunk info
  h+='<div style="font-size:11px;color:var(--text-3);margin-bottom:12px">';
  h+=trunk.size+'&#x2033; '+trunk.material+' trunk &middot; '+trunk.length+'ft';
  if (trunk.material==='flex'&&trunk.compression) h+=' &middot; '+trunk.compression+'% compression';
  h+='</div>';

  // ---- BRANCHES off this trunk ----
  h+='<div style="font-size:11px;font-weight:700;color:var(--text-2);text-transform:uppercase;letter-spacing:0.5px;margin-bottom:6px">Branches ('+trunk.branches.length+')</div>';

  trunk.branches.forEach(function(br, bi) {
    var isEditing = bi === RB.editBranch;
    var takeoff = RB_TAKEOFFS[br.takeoff] || RB_TAKEOFFS['straight90'];
    var boot = RB_BOOTS[br.bootType] || RB_BOOTS['90boot'];

    h+='<div class="rb-branch-card'+(isEditing?' editing':'')+'" data-rb-branch="'+bi+'">';
    
    // Branch header
    h+='<div class="rb-branch-hdr">';
    h+='<div class="rb-branch-num">'+(bi+1)+'</div>';
    h+='<div class="rb-branch-info">';
    h+='<div class="rb-branch-room">'+br.room+'</div>';
    h+='<div class="rb-branch-meta">';
    h+=br.size+'&#x2033; '+(br.material||'flex')+' &middot; '+br.length+'ft &middot; '+(br.cfm||'?')+' CFM';
    h+='</div>';
    h+='</div>';
    h+='<div class="rb-branch-boot-badge">'+boot.name+'</div>';
    h+='</div>';

    // Expanded edit form
    if (isEditing) {
      h+='<div class="rb-branch-edit">';

      // Room picker
      h+='<div class="rb-edit-row"><label class="input-label">Room (destination)</label>';
      h+='<select class="input-field" data-rb-br-room="'+bi+'">';
      h+='<option value="">— Select Room —</option>';
      rooms.forEach(function(rm,ri){
        h+='<option value="'+ri+'"'+(br.roomIdx===ri?' selected':'')+'>'+rm.name+' ('+rm.cfm+' CFM)</option>';
      });
      h+='<option value="-1"'+(br.roomIdx===-1?' selected':'')+'>Custom (manual CFM)</option>';
      h+='</select></div>';

      // CFM (read-only if room selected, editable if custom)
      if (br.roomIdx >= 0 && rooms[br.roomIdx]) {
        h+='<div class="rb-edit-row" style="font-size:11px;color:var(--accent);font-weight:600">'+rooms[br.roomIdx].cfm+' CFM from '+rooms[br.roomIdx].name+'</div>';
      } else {
        h+='<div class="rb-edit-row"><label class="input-label">CFM</label>';
        h+='<input type="number" class="input-field" value="'+(br.cfm||'')+'" data-rb-br-cfm="'+bi+'" placeholder="CFM"></div>';
      }

      // Takeoff type
      h+='<div class="rb-edit-row"><label class="input-label">Takeoff from Trunk</label>';
      h+='<select class="input-field" data-rb-br-takeoff="'+bi+'">';
      Object.keys(RB_TAKEOFFS).forEach(function(k){
        h+='<option value="'+k+'"'+(br.takeoff===k?' selected':'')+'>'+RB_TAKEOFFS[k].name+' (+'+RB_TAKEOFFS[k].eq+'ft)</option>';
      });
      h+='</select></div>';

      // Material
      h+='<div class="rb-edit-row"><label class="input-label">Branch Material</label>';
      h+='<div class="rb-seg">';
      h+='<div class="rb-seg-btn'+(br.material!=='flex'?' active':'')+'" data-rb-br-mat="'+bi+'" data-rb-matv="metal">Metal</div>';
      h+='<div class="rb-seg-btn'+(br.material==='flex'?' active':'')+'" data-rb-br-mat="'+bi+'" data-rb-matv="flex">Flex</div>';
      h+='</div></div>';

      // Size
      var recSz = rbRecSize(br.cfm, trunk.size, br.material, br.compression);
      h+='<div class="rb-edit-row"><label class="input-label">Size <span class="rb-rec-tag">rec: '+recSz+'&#x2033;</span></label>';
      h+='<select class="input-field" data-rb-br-size="'+bi+'">';
      [4,5,6,7,8,9,10,12,14,16,18,20,22,24].forEach(function(s){
        if(s>trunk.size) return;
        h+='<option value="'+s+'"'+(br.size==s?' selected':'')+'>'+s+'&#x2033;'+(s==recSz?' \u2190 rec':'')+'</option>';
      });
      h+='</select></div>';

      // Length
      h+='<div class="rb-edit-row"><label class="input-label">Branch Length (ft)</label>';
      h+='<input type="number" class="input-field" value="'+(br.length||12)+'" min="1" max="200" data-rb-br-len="'+bi+'"></div>';

      // Compression
      if (br.material==='flex') {
        h+='<div class="rb-edit-row"><label class="input-label">Compression %</label>';
        h+='<div class="rb-comp-chips">';
        [4,5,10,15,20,25,30].forEach(function(c){
          h+='<div class="rb-comp-chip'+(br.compression==c?' active':'')+'" data-rb-br-comp="'+bi+'" data-rb-cv="'+c+'">'+c+'%</div>';
        });
        h+='</div></div>';
      }

      // Boot type
      h+='<div class="rb-edit-row"><label class="input-label">Ends At (Boot/Register)</label>';
      h+='<select class="input-field" data-rb-br-boot="'+bi+'">';
      Object.keys(RB_BOOTS).forEach(function(k){
        h+='<option value="'+k+'"'+(br.bootType===k?' selected':'')+'>'+RB_BOOTS[k].name+' (+'+RB_BOOTS[k].eq+'ft)</option>';
      });
      h+='</select></div>';

      // CFM capacity check
      if (br.cfm > 0 && br.size > 0) {
        var maxCFM = typeof wizMaxCFM==='function'? wizMaxCFM(br.size, br.material, br.compression) : 999;
        var ok = maxCFM >= br.cfm;
        h+='<div style="font-size:11px;padding:6px 8px;border-radius:6px;margin-top:4px;';
        h+=ok?'background:var(--green-soft);color:var(--green)':'background:var(--red-soft);color:var(--red)';
        h+='">';
        h+=ok ? '\u2713 '+br.size+'&#x2033; can deliver '+maxCFM+' CFM (need '+br.cfm+')' :
               '\u26A0 '+br.size+'&#x2033; max '+maxCFM+' CFM \u2014 need '+br.cfm+'. Upsize to '+rbRecSize(br.cfm,trunk.size,br.material,br.compression)+'&#x2033;';
        h+='</div>';
      }

      h+='<button class="rb-btn-done" data-rb-br-done>Done</button>';
      h+='</div>'; // /edit
    }

    h+='</div>'; // /branch-card
  });

  // Add Branch button
  h+='<button class="sys-add-btn" data-rb-add-branch style="width:100%;margin-top:8px;justify-content:center">';
  h+='<svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><line x1="12" y1="5" x2="12" y2="19"/><line x1="5" y1="12" x2="19" y2="12"/></svg>';
  h+='Add Branch to '+trunk.label+'</button>';

  // Navigation arrows
  if (section.length > 1) {
    h+='<div style="display:flex;justify-content:space-between;margin-top:10px">';
    if (sIdx > 0) h+='<button class="wiz-btn-secondary" data-rb-prev style="border-radius:10px;padding:8px 16px">\u2039 Prev Trunk</button>';
    else h+='<div></div>';
    if (sIdx < section.length-1) h+='<button class="wiz-btn-secondary" data-rb-next style="border-radius:10px;padding:8px 16px">Next Trunk \u203A</button>';
    else h+='<div></div>';
    h+='</div>';
  }

  h+='</div>'; // /run-card

  el.innerHTML = h;
}

// ============ EVENTS ============
function rbHandleClick(e) {
  var t = e.target;

  // Section toggle
  var sec=t.closest('[data-rb-section]');
  if(sec){
    var ap=sec.dataset.rbSection;
    var section=RB.trunks.filter(function(tr){return tr.airPath===ap;});
    if(section.length>0){RB.idx=RB.trunks.indexOf(section[0]); RB.editBranch=-1; rbRender();}
    return;
  }
  // Trunk dots
  var dot=t.closest('[data-rb-trunk-dot]');
  if(dot){RB.idx=parseInt(dot.dataset.rbTrunkDot); RB.editBranch=-1; rbRender(); return;}
  // Nav
  if(t.closest('[data-rb-prev]')){rbNavTrunk(-1);return;}
  if(t.closest('[data-rb-next]')){rbNavTrunk(1);return;}
  // Tap branch to edit
  var brCard=t.closest('[data-rb-branch]');
  if(brCard && !t.closest('.rb-branch-edit') && !t.closest('[data-rb-br-done]')){
    var bi=parseInt(brCard.dataset.rbBranch);
    RB.editBranch=(RB.editBranch===bi)?-1:bi;
    rbRender();
    if(RB.editBranch>=0) setTimeout(function(){
      var ed=document.querySelector('.rb-branch-card.editing');
      if(ed) ed.scrollIntoView({behavior:'smooth',block:'start'});
    },50);
    return;
  }
  // Material toggle
  var mat=t.closest('[data-rb-br-mat]');
  if(mat){
    var bi2=parseInt(mat.dataset.rbBrMat);
    var mv=mat.dataset.rbMatv;
    var trunk=RB.trunks[RB.idx];
    if(trunk&&trunk.branches[bi2]){
      trunk.branches[bi2].material=mv;
      if(mv==='flex'){trunk.branches[bi2].compression=trunk.branches[bi2].compression||10;}
      else trunk.branches[bi2].compression=0;
    }
    rbRender(); return;
  }
  // Compression chip
  var comp=t.closest('[data-rb-br-comp]');
  if(comp){
    var bi3=parseInt(comp.dataset.rbBrComp);
    var cv=parseInt(comp.dataset.rbCv);
    var trunk2=RB.trunks[RB.idx];
    if(trunk2&&trunk2.branches[bi3]) trunk2.branches[bi3].compression=cv;
    rbRender(); return;
  }
  // Done
  if(t.closest('[data-rb-br-done]')){RB.editBranch=-1; rbRender(); return;}
  // Add branch
  if(t.closest('[data-rb-add-branch]')){
    var trunk3=RB.trunks[RB.idx];
    if(!trunk3) return;
    trunk3.branches.push({
      room:'', cfm:0, roomIdx:-1, takeoff:'straight90',
      material:WIZ.material||'flex', size:rbRecSize(0,trunk3.size,WIZ.material,10),
      length:12, compression:(WIZ.material==='flex')?10:0,
      bootType:'90boot', pieces:[], complete:false
    });
    RB.editBranch=trunk3.branches.length-1;
    rbRender();
    setTimeout(function(){
      var ed=document.querySelector('.rb-branch-card.editing');
      if(ed) ed.scrollIntoView({behavior:'smooth',block:'start'});
    },50);
    return;
  }
}

function rbHandleChange(e) {
  var t=e.target;
  var trunk=RB.trunks[RB.idx];
  if(!trunk) return;

  // Room picker
  if(t.dataset.rbBrRoom!==undefined){
    var bi=parseInt(t.dataset.rbBrRoom);
    var br=trunk.branches[bi]; if(!br) return;
    var ri=parseInt(t.value);
    br.roomIdx=ri;
    var rooms=typeof getRoomsList==='function'?getRoomsList():[];
    if(ri>=0 && rooms[ri]){
      br.room=rooms[ri].name;
      br.cfm=rooms[ri].cfm;
      br.size=rbRecSize(br.cfm,trunk.size,br.material,br.compression);
    } else {
      br.roomIdx=-1;
    }
    rbRender(); return;
  }
  // CFM
  if(t.dataset.rbBrCfm!==undefined){
    var bi2=parseInt(t.dataset.rbBrCfm);
    var br2=trunk.branches[bi2]; if(!br2) return;
    br2.cfm=parseInt(t.value)||0;
    return; // don't re-render on every keystroke
  }
  // Takeoff
  if(t.dataset.rbBrTakeoff!==undefined){
    var bi3=parseInt(t.dataset.rbBrTakeoff);
    var br3=trunk.branches[bi3]; if(!br3) return;
    br3.takeoff=t.value;
    rbRender(); return;
  }
  // Size
  if(t.dataset.rbBrSize!==undefined){
    var bi4=parseInt(t.dataset.rbBrSize);
    var br4=trunk.branches[bi4]; if(!br4) return;
    br4.size=parseInt(t.value)||6;
    rbRender(); return;
  }
  // Length
  if(t.dataset.rbBrLen!==undefined){
    var bi5=parseInt(t.dataset.rbBrLen);
    var br5=trunk.branches[bi5]; if(!br5) return;
    br5.length=parseInt(t.value)||12;
    return;
  }
  // Boot
  if(t.dataset.rbBrBoot!==undefined){
    var bi6=parseInt(t.dataset.rbBrBoot);
    var br6=trunk.branches[bi6]; if(!br6) return;
    br6.bootType=t.value;
    rbRender(); return;
  }
}

function rbNavTrunk(dir) {
  var trunk=RB.trunks[RB.idx];
  var isS=trunk.airPath==='supply';
  var section=RB.trunks.filter(function(t){return t.airPath===(isS?'supply':'return');});
  var si=section.indexOf(trunk);
  var newSi=si+dir;
  if(newSi>=0&&newSi<section.length){
    RB.idx=RB.trunks.indexOf(section[newSi]);
    RB.editBranch=-1;
    rbRender();
  }
}

// ============ TRANSLATE TO WIZ.branches ============
function rbTranslateToBranches() {
  WIZ.branches = [];
  var num = 1;
  RB.trunks.forEach(function(trunk) {
    trunk.branches.forEach(function(br) {
      var fittings = br.pieces ? br.pieces.map(function(p){return {type:p.type};}) : [];
      WIZ.branches.push({
        trunkIdx: trunk.wizIdx,
        num: num++,
        room: br.room || 'Branch',
        cfm: br.cfm || '',
        shape: 'round',
        size: String(br.size || 6),
        width: '8', height: '8',
        material: br.material || 'flex',
        compression: br.compression || 0,
        length: String(br.length || 12),
        fittings: fittings,
        bootType: br.bootType || '90boot',
        takeoffType: br.takeoff || 'straight90',
        done: true,
        recommended: String(br.size || 6),
        runouts: []
      });
    });
  });
}

// Legacy compat
function rbInitRuns() { rbInit(); }
