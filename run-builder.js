// ===== DUCT RUN BUILDER v4 =====
// Tree: Collar → Trunk → Split Fitting → Branches → Runoffs → Boots/Rooms
// Enforces Manual D: downstream CFM cannot exceed duct capacity

var RB = { trunks: [], idx: 0, editNode: null };

// Manual D split fitting types
var RB_SPLITS = {
  'wye':        { name: 'Wye (Y-split)', eq: 15 },
  'tee':        { name: 'Tee (T-split)', eq: 35 },
  'straight90': { name: '90\u00B0 Takeoff', eq: 35 },
  'conical':    { name: 'Conical Takeoff', eq: 10 },
  'angle45':    { name: '45\u00B0 Angled', eq: 20 },
  'dbox':       { name: 'Distribution Box', eq: 50 }
};
var RB_FITTINGS = {
  'elbow90': { name: '90\u00B0 Elbow', eqFn: function(d){return d<=6?10:d<=8?15:d<=10?20:25;} },
  'elbow45': { name: '45\u00B0 Elbow', eqFn: function(){return 5;} },
  'reducer':  { name: 'Reducer', eqFn: function(){return 5;} }
};
var RB_BOOTS = {
  '90boot':{name:'90\u00B0 Boot',eq:55},'straightboot':{name:'Straight Boot',eq:35},
  'ceilTop':{name:'Ceiling (top)',eq:10},'ceilSide':{name:'Ceiling (side)',eq:40},
  'floorReg':{name:'Floor Register',eq:35},'wallReg':{name:'Wall Register',eq:40}
};
var RB_MOUNT_TYPES = {floor:'Floor',wall:'Wall',ceiling:'Ceiling'};

// ---- Init from wizard trunks ----
function rbInit() {
  RB.trunks = []; RB.idx = 0; RB.editNode = null;
  var rooms = typeof getRoomsList==='function' ? getRoomsList() : [];
  var ri = 0;

  WIZ.trunks.forEach(function(t, ti) {
    var isReturn = t.airPath === 'return';
    var trunk = {
      wizIdx: ti, label: t.label, airPath: t.airPath||'supply',
      size: parseInt(t.size)||12, length: parseFloat(t.length)||0,
      material: t.material||'metal', compression: t.compression||0,
      // Children: branches off this trunk
      children: []
    };

    if (!isReturn) {
      // Auto-assign rooms to supply trunks
      var supTrunks = WIZ.trunks.filter(function(x){return x.airPath==='supply';});
      var myRooms = [];
      var perTrunk = Math.ceil(rooms.length / Math.max(supTrunks.length,1));
      for (var b=0; b<perTrunk && ri<rooms.length; b++, ri++) {
        myRooms.push(rooms[ri]);
      }
      // Create one branch per room (home run style as default)
      myRooms.forEach(function(rm) {
        var recSize = rbRecSize(rm.cfm, trunk.size, WIZ.material, 10);
        trunk.children.push({
          type: 'branch',
          room: rm.name, cfm: rm.cfm||0, roomIdx: rooms.indexOf(rm),
          splitType: 'straight90',
          material: WIZ.material||'flex', size: recSize,
          length: 12, compression: (WIZ.material==='flex')?10:0,
          bootType: '90boot', mountType: 'floor', bootSize: '',
          fittings: [] // extra elbows etc
        });
      });
    } else {
      // Return trunk
      var totalCfm = typeof getRoomsTotalCFM==='function' ? getRoomsTotalCFM() : 0;
      var retTrunks = WIZ.trunks.filter(function(x){return x.airPath==='return';});
      var retCfm = retTrunks.length>0 ? Math.round(totalCfm/retTrunks.length) : totalCfm;
      var recSize = rbRecSize(retCfm, trunk.size, WIZ.material, 10);
      trunk.children.push({
        type: 'branch',
        room: 'Return', cfm: retCfm, roomIdx: -1,
        splitType: 'straight90',
        material: WIZ.material||'flex', size: recSize,
        length: 10, compression: (WIZ.material==='flex')?10:0,
        bootType: 'wallReg', mountType: 'wall', bootSize: '',
        fittings: []
      });
    }
    RB.trunks.push(trunk);
  });
}

// ---- Helpers ----
function rbRecSize(cfm, upSize, mat, comp) {
  if (!cfm||cfm<=0) return Math.min(upSize||6, 8);
  var ff = (mat==='flex'&&typeof wizFlexFactor==='function') ? wizFlexFactor(comp||10) : (mat==='flex'?1.67:1);
  var sizes=[4,5,6,7,8,9,10,12,14,16,18,20,22,24];
  for(var i=0;i<sizes.length;i++){
    var d=sizes[i]; if(upSize&&d>upSize) break;
    var A=Math.PI*Math.pow(d/12/2,2); var v=cfm/A;
    if(v>(mat==='flex'?700:900)) continue;
    var fr=typeof frictionLoss==='function'?frictionLoss(d,cfm):0.08;
    if(fr*ff<=0.08) return d;
  }
  return Math.min(upSize||6, 8);
}
function rbMaxCFM(size, mat, comp) {
  return typeof wizMaxCFM==='function' ? wizMaxCFM(size, mat, comp) : 999;
}
function rbTrunkTotalCFM(trunk) {
  var total = 0;
  trunk.children.forEach(function(ch){ total += (ch.cfm||0); });
  return total;
}

// ---- SVG Icons ----
function rbSvg(type) {
  var icons = {
    trunk: '<svg viewBox="0 0 20 20" width="16" height="16"><rect x="4" y="2" width="12" height="16" rx="2" fill="none" stroke="currentColor" stroke-width="1.5"/></svg>',
    branch: '<svg viewBox="0 0 20 20" width="16" height="16"><line x1="10" y1="2" x2="10" y2="10" stroke="currentColor" stroke-width="1.5"/><line x1="10" y1="10" x2="4" y2="18" stroke="currentColor" stroke-width="1.5"/><line x1="10" y1="10" x2="16" y2="18" stroke="currentColor" stroke-width="1.5"/></svg>',
    boot: '<svg viewBox="0 0 20 20" width="16" height="16"><rect x="6" y="2" width="8" height="6" rx="1" fill="none" stroke="currentColor" stroke-width="1.5"/><path d="M6 8L3 14h14l-3-6" fill="none" stroke="currentColor" stroke-width="1.5"/><line x1="5" y1="17" x2="15" y2="17" stroke="currentColor" stroke-width="2"/></svg>',
    homerun: '<svg viewBox="0 0 20 20" width="16" height="16"><line x1="10" y1="2" x2="10" y2="18" stroke="currentColor" stroke-width="1.5"/><circle cx="10" cy="4" r="2" fill="currentColor"/><rect x="6" y="14" width="8" height="4" rx="1" fill="none" stroke="currentColor" stroke-width="1.5"/></svg>'
  };
  return icons[type] || '';
}

// ============ RENDER ============
function rbRender() {
  var el = document.getElementById('wizBranchArea');
  if(!el) return;
  if(RB.trunks.length===0) rbInit();
  if(RB.trunks.length===0){ el.innerHTML='<div style="text-align:center;padding:20px;color:var(--text-3)">No trunks. Go back to Trunks step.</div>'; return; }

  var supTrunks = RB.trunks.filter(function(t){return t.airPath==='supply';});
  var retTrunks = RB.trunks.filter(function(t){return t.airPath==='return';});
  var trunk = RB.trunks[RB.idx];
  var isSupply = trunk.airPath==='supply';
  var section = isSupply ? supTrunks : retTrunks;
  var sIdx = section.indexOf(trunk);
  var rooms = typeof getRoomsList==='function' ? getRoomsList() : [];
  var trunkMaxCFM = rbMaxCFM(trunk.size, trunk.material, trunk.compression);
  var trunkUsedCFM = rbTrunkTotalCFM(trunk);

  var h = '';

  // Section toggle
  if(supTrunks.length>0 && retTrunks.length>0){
    h+='<div class="rb-seg" style="margin-bottom:8px">';
    h+='<div class="rb-seg-btn'+(isSupply?' active':'')+'" data-rb-section="supply">Supply ('+supTrunks.length+')</div>';
    h+='<div class="rb-seg-btn'+(!isSupply?' active':'')+'" data-rb-section="return">Return ('+retTrunks.length+')</div>';
    h+='</div>';
  }

  // Trunk dots
  if(section.length>1){
    h+='<div class="rb-dots">';
    section.forEach(function(t,i){ h+='<div class="rb-dot'+(i===sIdx?' active':'')+'" data-rb-trunk-dot="'+RB.trunks.indexOf(t)+'"></div>'; });
    h+='</div>';
  }

  // ===== TRUNK CARD =====
  h+='<div class="rb-run-card">';

  // Trunk header
  h+='<div class="rb-run-hdr">';
  h+='<div class="rb-run-title">'+trunk.label+'</div>';
  h+='<div class="rb-run-badges">';
  h+='<span class="rb-badge '+(isSupply?'rb-badge-sup':'rb-badge-ret')+'">'+(isSupply?'SUP':'RTN')+'</span>';
  h+='<span class="rb-badge rb-badge-size">'+trunk.size+'&#x2033;</span>';
  h+='</div></div>';

  // Trunk details
  h+='<div style="font-size:11px;color:var(--text-3);margin-bottom:4px">';
  h+=trunk.size+'&#x2033; '+trunk.material+' &middot; '+trunk.length+'ft';
  if(trunk.material==='flex'&&trunk.compression) h+=' &middot; '+trunk.compression+'%';
  h+='</div>';

  // Trunk CFM capacity bar
  var cfmPct = trunkMaxCFM>0 ? Math.min(trunkUsedCFM/trunkMaxCFM*100, 100) : 0;
  var cfmOk = trunkUsedCFM <= trunkMaxCFM;
  h+='<div style="margin-bottom:10px">';
  h+='<div style="display:flex;justify-content:space-between;font-size:10px;margin-bottom:2px">';
  h+='<span style="color:var(--text-3)">Trunk CFM Load</span>';
  h+='<span style="font-family:\'DM Mono\',monospace;font-weight:600;color:'+(cfmOk?'var(--green)':'var(--red)')+'">'+trunkUsedCFM+' / '+trunkMaxCFM+' CFM</span>';
  h+='</div>';
  h+='<div style="height:6px;border-radius:3px;background:var(--surface-3);overflow:hidden">';
  h+='<div style="height:100%;width:'+cfmPct+'%;border-radius:3px;background:'+(cfmOk?'var(--green)':'var(--red)')+';transition:width 0.3s"></div>';
  h+='</div>';
  if(!cfmOk) h+='<div style="font-size:10px;color:var(--red);margin-top:2px">\u26A0 Trunk overloaded \u2014 reduce branches or upsize trunk</div>';
  h+='</div>';

  // ===== VISUAL DIAGRAM =====
  h+='<div class="rb-diagram">';
  h+='<div class="rb-diagram-trunk">';
  h+='<div class="rb-dia-collar">'+trunk.size+'&#x2033;</div>';
  h+='<div class="rb-dia-line" style="height:'+ Math.max(20, Math.min(trunk.length*2, 60)) +'px"></div>';
  // Show branches splitting off
  if(trunk.children.length>0){
    h+='<div class="rb-dia-branches">';
    trunk.children.forEach(function(ch,ci){
      var bootLabel = RB_BOOTS[ch.bootType] ? RB_BOOTS[ch.bootType].name : 'Boot';
      h+='<div class="rb-dia-branch'+(ci===RB.editNode?' active':'')+'">';
      h+='<div class="rb-dia-split"></div>';
      h+='<div class="rb-dia-duct" style="height:'+Math.max(16, Math.min(ch.length*1.5,40))+'px">'+ch.size+'&#x2033;</div>';
      h+='<div class="rb-dia-boot" title="'+bootLabel+'">'+rbSvg('boot')+'</div>';
      h+='<div class="rb-dia-room">'+(ch.room||'?')+'</div>';
      h+='</div>';
    });
    h+='</div>';
  }
  h+='</div></div>';

  // ===== BRANCH LIST =====
  h+='<div style="font-size:11px;font-weight:700;color:var(--text-2);text-transform:uppercase;letter-spacing:0.5px;margin:10px 0 6px">Branches ('+trunk.children.length+')</div>';

  trunk.children.forEach(function(ch, ci){
    var isEd = ci === RB.editNode;
    var boot = RB_BOOTS[ch.bootType]||{name:'Boot',eq:35};
    var split = RB_SPLITS[ch.splitType]||{name:'Takeoff',eq:35};
    var brMaxCFM = rbMaxCFM(ch.size, ch.material, ch.compression);
    var cfmOk2 = !ch.cfm || brMaxCFM >= ch.cfm;

    h+='<div class="rb-branch-card'+(isEd?' editing':'')+'" data-rb-branch="'+ci+'">';
    h+='<div class="rb-branch-hdr">';
    h+='<div class="rb-branch-num">'+(ci+1)+'</div>';
    h+='<div class="rb-branch-info">';
    h+='<div class="rb-branch-room">'+(ch.room||'<em style="color:var(--text-3)">Select room</em>')+'</div>';
    h+='<div class="rb-branch-meta">';
    h+=ch.size+'&#x2033; '+(ch.material||'flex')+' &middot; '+ch.length+'ft &middot; '+(ch.cfm||'?')+' CFM';
    if(!cfmOk2) h+=' <span style="color:var(--red)">\u26A0</span>';
    h+='</div></div>';
    h+='<div class="rb-branch-boot-badge">'+boot.name+'</div>';
    // Delete button
    h+='<div class="rb-node-x" data-rb-del-branch="'+ci+'" style="margin-left:4px">&times;</div>';
    h+='</div>';

    // Edit form
    if(isEd){
      h+='<div class="rb-branch-edit">';

      // Room picker
      h+='<div class="rb-edit-row"><label class="input-label">Room (where does this branch end?)</label>';
      h+='<select class="input-field" data-rb-br-room="'+ci+'">';
      h+='<option value="">— Pick a Room —</option>';
      rooms.forEach(function(rm,ri2){
        h+='<option value="'+ri2+'"'+(ch.roomIdx===ri2?' selected':'')+'>'+rm.name+' ('+rm.cfm+' CFM)</option>';
      });
      h+='<option value="-2">Home Run (custom)</option>';
      h+='</select></div>';

      if(ch.roomIdx>=0 && rooms[ch.roomIdx]){
        h+='<div style="font-size:11px;color:var(--accent);font-weight:600;margin-bottom:6px">'+rooms[ch.roomIdx].cfm+' CFM \u2192 '+ch.room+'</div>';
      } else if(ch.roomIdx===-2||ch.roomIdx===-1){
        h+='<div class="rb-edit-row"><label class="input-label">CFM</label>';
        h+='<input type="number" class="input-field" value="'+(ch.cfm||'')+'" data-rb-br-cfm="'+ci+'" placeholder="CFM"></div>';
        h+='<div class="rb-edit-row"><label class="input-label">Name</label>';
        h+='<input type="text" class="input-field" value="'+(ch.room||'')+'" data-rb-br-name="'+ci+'" placeholder="Room name"></div>';
      }

      // Split/takeoff type
      h+='<div class="rb-edit-row"><label class="input-label">How does it connect to trunk?</label>';
      h+='<select class="input-field" data-rb-br-split="'+ci+'">';
      Object.keys(RB_SPLITS).forEach(function(k){
        h+='<option value="'+k+'"'+(ch.splitType===k?' selected':'')+'>'+RB_SPLITS[k].name+' (+'+RB_SPLITS[k].eq+'ft)</option>';
      });
      h+='</select></div>';

      // Material
      h+='<div class="rb-edit-row"><label class="input-label">Material</label>';
      h+='<div class="rb-seg">';
      h+='<div class="rb-seg-btn'+(ch.material!=='flex'?' active':'')+'" data-rb-br-mat="'+ci+'" data-rb-matv="metal">Metal</div>';
      h+='<div class="rb-seg-btn'+(ch.material==='flex'?' active':'')+'" data-rb-br-mat="'+ci+'" data-rb-matv="flex">Flex</div>';
      h+='</div></div>';

      // Size
      var recSz = rbRecSize(ch.cfm, trunk.size, ch.material, ch.compression);
      h+='<div class="rb-edit-row"><label class="input-label">Size <span class="rb-rec-tag">rec: '+recSz+'&#x2033;</span></label>';
      h+='<select class="input-field" data-rb-br-size="'+ci+'">';
      [4,5,6,7,8,9,10,12,14,16,18,20,22,24].forEach(function(s){
        if(s>trunk.size) return;
        h+='<option value="'+s+'"'+(ch.size==s?' selected':'')+'>'+s+'&#x2033;'+(s==recSz?' \u2190 rec':'')+'</option>';
      });
      h+='</select></div>';

      // Length
      h+='<div class="rb-edit-row"><label class="input-label">Branch length (ft)</label>';
      h+='<input type="number" class="input-field" value="'+(ch.length||12)+'" min="1" max="200" data-rb-br-len="'+ci+'"></div>';

      // Compression
      if(ch.material==='flex'){
        h+='<div class="rb-edit-row"><label class="input-label">Compression %</label>';
        h+='<div class="rb-comp-chips">';
        [4,5,10,15,20,25,30].forEach(function(c){
          h+='<div class="rb-comp-chip'+(ch.compression==c?' active':'')+'" data-rb-br-comp="'+ci+'" data-rb-cv="'+c+'">'+c+'%</div>';
        });
        h+='</div></div>';
      }

      // Boot type + mount type
      h+='<div class="rb-edit-row"><label class="input-label">Register Mount</label>';
      h+='<div class="rb-seg">';
      ['floor','wall','ceiling'].forEach(function(mt){
        h+='<div class="rb-seg-btn'+(ch.mountType===mt?' active':'')+'" data-rb-br-mount="'+ci+'" data-rb-mv="'+mt+'">'+RB_MOUNT_TYPES[mt]+'</div>';
      });
      h+='</div></div>';

      // Boot type selector
      h+='<div class="rb-edit-row"><label class="input-label">Boot Type</label>';
      h+='<select class="input-field" data-rb-br-boot="'+ci+'">';
      Object.keys(RB_BOOTS).forEach(function(k){
        h+='<option value="'+k+'"'+(ch.bootType===k?' selected':'')+'>'+RB_BOOTS[k].name+' (+'+RB_BOOTS[k].eq+'ft)</option>';
      });
      h+='</select></div>';

      // Boot SVG visual
      h+='<div class="rb-boot-visual" id="rbBootVis'+ci+'">';
      h+=rbBootSVG(ch.bootType, ch.mountType);
      h+='</div>';

      // Boot size picker
      if(typeof getBootSizes==='function'){
        var bootSizes = getBootSizes(ch.size, ch.mountType==='ceiling'?'ceiling':(ch.mountType==='wall'?'wall':'floor'));
        if(bootSizes.length>0){
          h+='<div class="rb-edit-row"><label class="input-label">Boot/Register Size</label>';
          h+='<select class="input-field" data-rb-br-bsize="'+ci+'">';
          h+='<option value="">— Select Size —</option>';
          bootSizes.forEach(function(bs){
            h+='<option value="'+bs.reg+'"'+(ch.bootSize===bs.reg?' selected':'')+'>'+bs.reg+'</option>';
          });
          h+='</select></div>';
        }
      }

      // CFM check
      if(ch.cfm>0 && ch.size>0){
        h+='<div style="font-size:11px;padding:6px 8px;border-radius:6px;margin-top:4px;';
        h+=cfmOk2?'background:var(--green-soft);color:var(--green)':'background:var(--red-soft);color:var(--red)';
        h+='">';
        h+=cfmOk2?'\u2713 '+ch.size+'&#x2033; delivers '+brMaxCFM+' CFM (need '+ch.cfm+')':
                  '\u26A0 '+ch.size+'&#x2033; max '+brMaxCFM+' CFM \u2014 need '+ch.cfm+'. Upsize to '+recSz+'&#x2033;';
        h+='</div>';
      }

      h+='<button class="rb-btn-done" data-rb-br-done>Done</button>';
      h+='</div>'; // /edit
    }
    h+='</div>'; // /branch-card
  });

  // Add branch button
  h+='<button class="sys-add-btn" data-rb-add-branch style="width:100%;margin-top:8px;justify-content:center">';
  h+='<svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><line x1="12" y1="5" x2="12" y2="19"/><line x1="5" y1="12" x2="19" y2="12"/></svg>';
  h+='Add Branch</button>';

  // Nav
  if(section.length>1){
    h+='<div style="display:flex;justify-content:space-between;margin-top:10px">';
    h+=(sIdx>0?'<button class="wiz-btn-secondary" data-rb-prev style="border-radius:10px;padding:8px 16px">\u2039 Prev</button>':'<div></div>');
    h+=(sIdx<section.length-1?'<button class="wiz-btn-secondary" data-rb-next style="border-radius:10px;padding:8px 16px">Next \u203A</button>':'<div></div>');
    h+='</div>';
  }

  h+='</div>'; // /run-card
  el.innerHTML = h;
}

// ---- Boot SVG visual ----
function rbBootSVG(bootType, mountType) {
  var w=120, h=80;
  var svg = '<svg viewBox="0 0 '+w+' '+h+'" width="'+w+'" height="'+h+'" style="display:block;margin:6px auto">';
  // Duct coming in
  svg += '<rect x="45" y="0" width="30" height="30" rx="2" fill="var(--surface-3)" stroke="var(--text-3)" stroke-width="1"/>';
  svg += '<text x="60" y="20" text-anchor="middle" fill="var(--text-2)" font-size="8" font-weight="600">Duct</text>';

  if(bootType==='90boot' || bootType==='wallReg'){
    // 90° turn
    svg += '<path d="M50 30 L50 45 Q50 55 60 55 L85 55" fill="none" stroke="var(--accent)" stroke-width="2"/>';
    svg += '<path d="M70 30 L70 40 Q70 50 80 50 L85 50" fill="none" stroke="var(--accent)" stroke-width="2"/>';
    // Register face
    svg += '<rect x="85" y="44" width="8" height="16" rx="1" fill="var(--accent)" opacity="0.3" stroke="var(--accent)" stroke-width="1"/>';
    svg += '<text x="99" y="55" fill="var(--text-2)" font-size="7">Register</text>';
  } else if(bootType==='straightboot' || bootType==='floorReg'){
    // Straight down
    svg += '<line x1="50" y1="30" x2="45" y2="60" stroke="var(--accent)" stroke-width="2"/>';
    svg += '<line x1="70" y1="30" x2="75" y2="60" stroke="var(--accent)" stroke-width="2"/>';
    // Register face
    svg += '<rect x="40" y="60" width="40" height="6" rx="1" fill="var(--accent)" opacity="0.3" stroke="var(--accent)" stroke-width="1"/>';
    svg += '<text x="60" y="75" text-anchor="middle" fill="var(--text-2)" font-size="7">'+
      (mountType==='floor'?'Floor':'Register')+'</text>';
  } else if(bootType==='ceilTop'){
    // Top mount ceiling
    svg += '<line x1="50" y1="30" x2="50" y2="50" stroke="var(--accent)" stroke-width="2"/>';
    svg += '<line x1="70" y1="30" x2="70" y2="50" stroke="var(--accent)" stroke-width="2"/>';
    svg += '<rect x="35" y="50" width="50" height="6" rx="1" fill="var(--surface-4)" stroke="var(--text-3)" stroke-width="1"/>';
    svg += '<text x="60" y="53" text-anchor="middle" fill="var(--text-2)" font-size="5">CEILING</text>';
    svg += '<circle cx="60" cy="65" r="8" fill="var(--accent)" opacity="0.2" stroke="var(--accent)" stroke-width="1"/>';
    svg += '<text x="60" y="68" text-anchor="middle" fill="var(--text-2)" font-size="6">Diff</text>';
  } else {
    // Generic
    svg += '<line x1="55" y1="30" x2="55" y2="55" stroke="var(--accent)" stroke-width="2"/>';
    svg += '<line x1="65" y1="30" x2="65" y2="55" stroke="var(--accent)" stroke-width="2"/>';
    svg += '<rect x="45" y="55" width="30" height="8" rx="1" fill="var(--accent)" opacity="0.3" stroke="var(--accent)" stroke-width="1"/>';
  }
  svg += '</svg>';
  return svg;
}

// ============ EVENTS ============
function rbHandleClick(e) {
  var t = e.target;
  var sec=t.closest('[data-rb-section]');
  if(sec){ var ap=sec.dataset.rbSection; var s=RB.trunks.filter(function(x){return x.airPath===ap;}); if(s.length>0){RB.idx=RB.trunks.indexOf(s[0]);RB.editNode=null;rbRender();} return; }
  var dot=t.closest('[data-rb-trunk-dot]');
  if(dot){RB.idx=parseInt(dot.dataset.rbTrunkDot);RB.editNode=null;rbRender();return;}
  if(t.closest('[data-rb-prev]')){rbNavTrunk(-1);return;}
  if(t.closest('[data-rb-next]')){rbNavTrunk(1);return;}

  // Branch tap
  var brCard=t.closest('[data-rb-branch]');
  if(brCard && !t.closest('.rb-branch-edit') && !t.closest('[data-rb-br-done]') && !t.closest('[data-rb-del-branch]')){
    var bi=parseInt(brCard.dataset.rbBranch);
    RB.editNode=(RB.editNode===bi)?null:bi;
    rbRender();
    if(RB.editNode!==null) setTimeout(function(){ var ed=document.querySelector('.rb-branch-card.editing'); if(ed)ed.scrollIntoView({behavior:'smooth',block:'start'});},50);
    return;
  }
  // Delete branch
  var del=t.closest('[data-rb-del-branch]');
  if(del){ var di=parseInt(del.dataset.rbDelBranch); var trunk=RB.trunks[RB.idx]; if(trunk){trunk.children.splice(di,1);if(RB.editNode===di)RB.editNode=null;else if(RB.editNode>di)RB.editNode--;rbRender();} return; }
  // Material
  var mat=t.closest('[data-rb-br-mat]');
  if(mat){var bi2=parseInt(mat.dataset.rbBrMat);var mv=mat.dataset.rbMatv;var tr=RB.trunks[RB.idx];if(tr&&tr.children[bi2]){tr.children[bi2].material=mv;if(mv==='flex')tr.children[bi2].compression=tr.children[bi2].compression||10;else tr.children[bi2].compression=0;}rbRender();return;}
  // Mount type
  var mnt=t.closest('[data-rb-br-mount]');
  if(mnt){var bi3=parseInt(mnt.dataset.rbBrMount);var mt=mnt.dataset.rbMv;var tr2=RB.trunks[RB.idx];if(tr2&&tr2.children[bi3])tr2.children[bi3].mountType=mt;rbRender();return;}
  // Compression
  var cmp=t.closest('[data-rb-br-comp]');
  if(cmp){var bi4=parseInt(cmp.dataset.rbBrComp);var cv=parseInt(cmp.dataset.rbCv);var tr3=RB.trunks[RB.idx];if(tr3&&tr3.children[bi4])tr3.children[bi4].compression=cv;rbRender();return;}
  // Done
  if(t.closest('[data-rb-br-done]')){RB.editNode=null;rbRender();return;}
  // Add branch
  if(t.closest('[data-rb-add-branch]')){
    var tr4=RB.trunks[RB.idx]; if(!tr4)return;
    tr4.children.push({
      type:'branch',room:'',cfm:0,roomIdx:-1,splitType:'straight90',
      material:WIZ.material||'flex',size:rbRecSize(0,tr4.size,WIZ.material,10),
      length:12,compression:(WIZ.material==='flex')?10:0,
      bootType:'90boot',mountType:'floor',bootSize:'',fittings:[]
    });
    RB.editNode=tr4.children.length-1;
    rbRender();
    setTimeout(function(){var ed=document.querySelector('.rb-branch-card.editing');if(ed)ed.scrollIntoView({behavior:'smooth',block:'start'});},50);
    return;
  }
}

function rbHandleChange(e) {
  var t=e.target; var trunk=RB.trunks[RB.idx]; if(!trunk)return;
  // Room
  if(t.dataset.rbBrRoom!==undefined){
    var bi=parseInt(t.dataset.rbBrRoom);var br=trunk.children[bi];if(!br)return;
    var ri=parseInt(t.value);var rooms=typeof getRoomsList==='function'?getRoomsList():[];
    if(ri>=0&&rooms[ri]){br.roomIdx=ri;br.room=rooms[ri].name;br.cfm=rooms[ri].cfm;br.size=rbRecSize(br.cfm,trunk.size,br.material,br.compression);}
    else{br.roomIdx=ri;}
    rbRender();return;
  }
  if(t.dataset.rbBrCfm!==undefined){var bi2=parseInt(t.dataset.rbBrCfm);var br2=trunk.children[bi2];if(br2)br2.cfm=parseInt(t.value)||0;return;}
  if(t.dataset.rbBrName!==undefined){var bi3=parseInt(t.dataset.rbBrName);var br3=trunk.children[bi3];if(br3)br3.room=t.value;return;}
  if(t.dataset.rbBrSplit!==undefined){var bi4=parseInt(t.dataset.rbBrSplit);var br4=trunk.children[bi4];if(br4)br4.splitType=t.value;rbRender();return;}
  if(t.dataset.rbBrSize!==undefined){var bi5=parseInt(t.dataset.rbBrSize);var br5=trunk.children[bi5];if(br5)br5.size=parseInt(t.value)||6;rbRender();return;}
  if(t.dataset.rbBrLen!==undefined){var bi6=parseInt(t.dataset.rbBrLen);var br6=trunk.children[bi6];if(br6)br6.length=parseInt(t.value)||12;return;}
  if(t.dataset.rbBrBoot!==undefined){var bi7=parseInt(t.dataset.rbBrBoot);var br7=trunk.children[bi7];if(br7)br7.bootType=t.value;rbRender();return;}
  if(t.dataset.rbBrBsize!==undefined){var bi8=parseInt(t.dataset.rbBrBsize);var br8=trunk.children[bi8];if(br8)br8.bootSize=t.value;return;}
}

function rbNavTrunk(dir){
  var trunk=RB.trunks[RB.idx]; var isS=trunk.airPath==='supply';
  var section=RB.trunks.filter(function(t){return t.airPath===(isS?'supply':'return');});
  var si=section.indexOf(trunk); var ns=si+dir;
  if(ns>=0&&ns<section.length){RB.idx=RB.trunks.indexOf(section[ns]);RB.editNode=null;rbRender();}
}

// ============ TRANSLATE ============
function rbTranslateToBranches(){
  WIZ.branches=[];var num=1;
  RB.trunks.forEach(function(trunk){
    trunk.children.forEach(function(ch){
      var fittings=ch.fittings?ch.fittings.map(function(f){return{type:f};}):[]; 
      WIZ.branches.push({
        trunkIdx:trunk.wizIdx, num:num++, room:ch.room||'Branch',
        cfm:ch.cfm||'', shape:'round', size:String(ch.size||6),
        width:'8',height:'8', material:ch.material||'flex',
        compression:ch.compression||0, length:String(ch.length||12),
        fittings:fittings, bootType:ch.bootType||'90boot',
        takeoffType:ch.splitType||'straight90',
        done:true, recommended:String(ch.size||6), runouts:[],
        mountType:ch.mountType||'floor', bootSize:ch.bootSize||''
      });
    });
  });
}

function rbInitRuns(){rbInit();}
