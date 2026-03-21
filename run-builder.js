// ===== INTERACTIVE DUCT RUN BUILDER =====
// Replaces the old branch form with a tap-to-build piece chain.
// Each start collar from the plenum = one run to build.

// --- Data ---
var RB = {
  runs: [],          // array of Run objects
  activeRun: 0,      // which run tab is selected
  editingPiece: -1   // index of piece being configured (-1 = none)
};

// Piece type definitions
var RB_PIECE_TYPES = {
  straight: { name: 'Straight Duct', icon: 'straight', hasLength: true, hasMaterial: true, hasSize: true },
  elbow90:  { name: '90° Elbow',     icon: 'elbow90',  eqFn: function(d){ return d<=6?10:d<=8?15:d<=10?20:25; } },
  elbow45:  { name: '45° Elbow',     icon: 'elbow45',  eqFn: function(){ return 5; } },
  reducer:  { name: 'Reducer',       icon: 'reducer',  eqFn: function(){ return 5; }, hasSize: true },
  wye:      { name: 'Wye Split',     icon: 'wye',      eqFn: function(){ return 15; } },
  tee:      { name: 'Tee Split',     icon: 'tee',      eqFn: function(){ return 35; } },
  dbox:     { name: 'Dist. Box',     icon: 'dbox',     eqFn: function(){ return 50; } },
  boot:     { name: 'Boot/Register', icon: 'boot',     isEnd: true }
};

var RB_BOOT_TYPES = {
  '90boot':       { name: '90° Boot',              eq: 55 },
  'straightboot': { name: 'Straight Boot',          eq: 35 },
  'ceilTop':      { name: 'Ceiling Diff (top)',     eq: 10 },
  'ceilSide':     { name: 'Ceiling Diff (side)',    eq: 40 },
  'floorReg':     { name: 'Floor Register',         eq: 35 },
  'wallReg':      { name: 'Wall Register',          eq: 40 }
};

// --- Initialize runs from collars ---
function rbInitRuns() {
  RB.runs = [];
  var supplyCollars = (typeof SS !== 'undefined' && SS.collars) ? SS.collars : [];
  var returnCollars = (typeof SS !== 'undefined' && SS.retCollars) ? SS.retCollars : [];
  var rooms = typeof getRoomsList === 'function' ? getRoomsList() : [];
  var supplyTrunks = WIZ.trunks.filter(function(t){ return t.airPath === 'supply'; });
  var returnTrunks = WIZ.trunks.filter(function(t){ return t.airPath === 'return'; });

  // Distribute rooms across supply collars
  var roomIdx = 0;
  supplyCollars.forEach(function(col, ci) {
    // Find which trunk this collar belongs to (first supply trunk for now)
    var trunkIdx = supplyTrunks.length > 0 ? WIZ.trunks.indexOf(supplyTrunks[Math.min(ci, supplyTrunks.length - 1)]) : 0;
    var roomsPerCollar = supplyCollars.length > 0 ? Math.ceil(rooms.length / supplyCollars.length) : rooms.length;
    
    // For now, one room per collar (user will assign)
    var rm = roomIdx < rooms.length ? rooms[roomIdx] : null;
    roomIdx++;
    
    RB.runs.push({
      collarIdx: ci,
      collarType: 'supply',
      collarSize: parseInt(col.size) || 8,
      airPath: 'supply',
      trunkIdx: trunkIdx,
      pieces: [],
      totalCFM: rm ? (rm.cfm || 0) : 0,
      room: rm ? rm.name : 'Supply Run ' + (ci + 1),
      complete: false
    });
  });

  // Return collars
  var totalCfm = typeof getRoomsTotalCFM === 'function' ? getRoomsTotalCFM() : 0;
  returnCollars.forEach(function(col, ci) {
    var trunkIdx = returnTrunks.length > 0 ? WIZ.trunks.indexOf(returnTrunks[Math.min(ci, returnTrunks.length - 1)]) : 0;
    var retCfm = returnCollars.length > 0 ? Math.round(totalCfm / returnCollars.length) : totalCfm;
    RB.runs.push({
      collarIdx: ci,
      collarType: 'return',
      collarSize: parseInt(col.size) || 14,
      airPath: 'return',
      trunkIdx: trunkIdx,
      pieces: [],
      totalCFM: retCfm,
      room: 'Return ' + (ci + 1),
      complete: false
    });
  });

  // Fallback: if no collars defined, create runs from rooms
  if (RB.runs.length === 0 && rooms.length > 0) {
    rooms.forEach(function(rm, i) {
      var trunkIdx = supplyTrunks.length > 0 ? WIZ.trunks.indexOf(supplyTrunks[i % supplyTrunks.length]) : 0;
      RB.runs.push({
        collarIdx: i,
        collarType: 'supply',
        collarSize: 8,
        airPath: 'supply',
        trunkIdx: trunkIdx,
        pieces: [],
        totalCFM: rm.cfm || 0,
        room: rm.name,
        complete: false
      });
    });
  }

  RB.activeRun = 0;
  RB.editingPiece = -1;
}

// --- Auto-size recommendation ---
function rbRecommendSize(cfm, upstreamSize, material, compression) {
  if (!cfm || cfm <= 0) return upstreamSize || 6;
  var comp = (material === 'flex') ? (compression || 10) : 0;
  var ff = (material === 'flex') ? (typeof wizFlexFactor === 'function' ? wizFlexFactor(comp) : 1.67) : 1;
  var maxFR = 0.08; // IWC/100ft target
  
  var sizes = [4,5,6,7,8,9,10,12,14,16,18,20,22,24];
  for (var i = 0; i < sizes.length; i++) {
    var d = sizes[i];
    if (upstreamSize && d > upstreamSize) break; // can't be bigger than upstream
    var area = Math.PI * Math.pow(d / 12 / 2, 2);
    var vel = cfm / area;
    if (vel > (material === 'flex' ? 700 : 900)) continue;
    var fr = typeof frictionLoss === 'function' ? frictionLoss(d, cfm) : 0.08;
    if (fr * ff <= maxFR) return d;
  }
  return upstreamSize || 6;
}

// --- Get current upstream size at end of piece chain ---
function rbGetUpstreamSize(run, upToIdx) {
  var size = run.collarSize;
  var pieces = run.pieces;
  var end = (typeof upToIdx === 'number') ? upToIdx : pieces.length;
  for (var i = 0; i < end; i++) {
    var p = pieces[i];
    if (p.size) size = p.size;
  }
  return size;
}

// --- Check if run is complete (ends with a boot) ---
function rbIsRunComplete(run) {
  if (run.pieces.length === 0) return false;
  var last = run.pieces[run.pieces.length - 1];
  return last.type === 'boot';
}

// --- Render the full builder UI ---
function rbRender() {
  var run = RB.runs[RB.activeRun];
  if (!run) return;
  
  var h = '';
  
  // --- Run selector tabs ---
  h += '<div class="rb-run-tabs">';
  RB.runs.forEach(function(r, i) {
    var isActive = i === RB.activeRun;
    var isDone = rbIsRunComplete(r);
    var tagCls = r.airPath === 'return' ? 'rb-tag-return' : 'rb-tag-supply';
    h += '<div class="rb-run-tab' + (isActive ? ' active' : '') + (isDone ? ' done' : '') + '" data-rb-tab="' + i + '">';
    h += '<span class="rb-tab-num">' + (i + 1) + '</span>';
    h += '<span class="rb-tab-name">' + r.room + '</span>';
    h += '<span class="rb-tag ' + tagCls + '">' + (r.airPath === 'return' ? 'RTN' : 'SUP') + '</span>';
    if (isDone) h += '<span class="rb-tab-check">&#x2713;</span>';
    h += '</div>';
  });
  h += '</div>';
  
  // --- Run header ---
  h += '<div class="rb-run-header">';
  h += '<div class="rb-run-title">' + run.room + '</div>';
  h += '<div class="rb-run-meta">';
  h += '<span class="rb-meta-chip">' + run.collarSize + '&#x2033; collar</span>';
  h += '<span class="rb-meta-chip">' + (run.totalCFM || '—') + ' CFM</span>';
  h += '<span class="rb-meta-chip ' + (run.airPath === 'return' ? 'rb-chip-return' : 'rb-chip-supply') + '">' + (run.airPath === 'return' ? 'Return' : 'Supply') + '</span>';
  h += '</div>';
  // Room assignment
  h += '<div class="rb-room-assign">';
  h += '<label class="input-label">Room / Destination</label>';
  h += '<input type="text" class="input-field" value="' + run.room + '" data-rb-room="' + RB.activeRun + '" placeholder="Room name">';
  h += '<label class="input-label" style="margin-top:6px">CFM</label>';
  h += '<input type="number" class="input-field" value="' + (run.totalCFM || '') + '" data-rb-cfm="' + RB.activeRun + '" placeholder="CFM" min="0" max="9999">';
  h += '</div>';
  h += '</div>';
  
  // --- Piece chain visualization ---
  h += '<div class="rb-chain">';
  
  // Start collar
  h += '<div class="rb-piece rb-piece-start">';
  h += '<div class="rb-piece-icon">';
  h += '<svg viewBox="0 0 32 32" width="28" height="28"><circle cx="16" cy="16" r="10" fill="none" stroke="var(--accent)" stroke-width="2"/><circle cx="16" cy="16" r="4" fill="var(--accent)"/></svg>';
  h += '</div>';
  h += '<div class="rb-piece-info">';
  h += '<div class="rb-piece-name">Start Collar</div>';
  h += '<div class="rb-piece-detail">' + run.collarSize + '&#x2033; ' + (run.collarType === 'supply' ? 'supply' : 'return') + '</div>';
  h += '</div>';
  h += '</div>';
  
  // Connector line
  if (run.pieces.length > 0 || !rbIsRunComplete(run)) {
    h += '<div class="rb-connector"></div>';
  }
  
  // Each piece
  run.pieces.forEach(function(piece, pi) {
    var ptype = RB_PIECE_TYPES[piece.type] || {};
    var isEditing = pi === RB.editingPiece;
    var upSize = rbGetUpstreamSize(run, pi);
    var eq = piece.eqLength || 0;
    
    h += '<div class="rb-piece' + (isEditing ? ' rb-piece-editing' : '') + '" data-rb-piece="' + pi + '">';
    
    // Icon
    h += '<div class="rb-piece-icon">';
    h += rbPieceIcon(piece.type);
    h += '</div>';
    
    // Info
    h += '<div class="rb-piece-info">';
    h += '<div class="rb-piece-name">' + (ptype.name || piece.type) + '</div>';
    h += '<div class="rb-piece-detail">';
    if (piece.type === 'straight') {
      h += (piece.size || '?') + '&#x2033; ' + (piece.material || 'flex');
      h += ' &middot; ' + (piece.length || 0) + ' ft';
      if (piece.material === 'flex' && piece.compression) h += ' &middot; ' + piece.compression + '% comp';
    } else if (piece.type === 'reducer') {
      h += upSize + '&#x2033; → ' + (piece.size || '?') + '&#x2033;';
    } else if (piece.type === 'boot') {
      var bt = RB_BOOT_TYPES[piece.bootType] || {};
      h += (bt.name || 'Boot') + ' (+' + (bt.eq || 0) + 'ft)';
    } else {
      h += '+' + eq + ' ft EQ';
      if (piece.size) h += ' &middot; ' + piece.size + '&#x2033;';
    }
    h += '</div>';
    h += '</div>';
    
    // Delete button
    h += '<div class="rb-piece-delete" data-rb-delete="' + pi + '">&times;</div>';
    
    h += '</div>'; // /rb-piece
    
    // Inline edit form (if editing this piece)
    if (isEditing) {
      h += rbRenderEditForm(run, piece, pi);
    }
    
    // Connector line (unless it's the last piece and it's a boot)
    if (pi < run.pieces.length - 1 || piece.type !== 'boot') {
      h += '<div class="rb-connector"></div>';
    }
  });
  
  // Live calculation summary
  var calcResult = rbCalcRunTEL(run);
  h += '<div class="rb-live-calc">';
  h += '<div class="rb-calc-row"><span>Total EQ Length</span><span class="rb-calc-val">' + Math.round(calcResult.tel) + ' ft</span></div>';
  if (calcResult.fr > 0) {
    var frClass = calcResult.fr <= 0.05 ? 'rb-fr-good' : calcResult.fr <= 0.08 ? 'rb-fr-ok' : 'rb-fr-bad';
    h += '<div class="rb-calc-row"><span>Friction Rate</span><span class="rb-calc-val ' + frClass + '">' + calcResult.fr.toFixed(3) + ' IWC/100ft</span></div>';
  }
  h += '</div>';
  
  h += '</div>'; // /rb-chain
  
  // --- Parts palette (only show if run is not complete) ---
  if (!rbIsRunComplete(run)) {
    h += '<div class="rb-palette">';
    h += '<div class="rb-palette-title">Tap to add piece</div>';
    h += '<div class="rb-palette-grid">';
    
    var paletteItems = ['straight', 'elbow90', 'elbow45', 'reducer', 'wye', 'dbox', 'boot'];
    paletteItems.forEach(function(typeKey) {
      var pt = RB_PIECE_TYPES[typeKey];
      h += '<div class="rb-palette-btn" data-rb-add="' + typeKey + '">';
      h += '<div class="rb-palette-icon">' + rbPieceIcon(typeKey) + '</div>';
      h += '<div class="rb-palette-label">' + pt.name + '</div>';
      h += '</div>';
    });
    
    h += '</div>';
    h += '</div>';
  } else {
    h += '<div class="rb-complete-banner">';
    h += '<svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="var(--green)" stroke-width="2"><path d="M22 11.08V12a10 10 0 1 1-5.93-9.14"/><polyline points="22 4 12 14.01 9 11.01"/></svg>';
    h += '<span>Run complete — ends at register</span>';
    h += '</div>';
  }
  
  var el = document.getElementById('wizBranchArea');
  if (el) el.innerHTML = h;
}

// --- Render inline edit form for a piece ---
function rbRenderEditForm(run, piece, idx) {
  var h = '<div class="rb-edit-form">';
  var upSize = rbGetUpstreamSize(run, idx);
  var recSize = rbRecommendSize(run.totalCFM, upSize, piece.material || WIZ.material, piece.compression || 10);
  
  if (piece.type === 'straight') {
    // Material
    h += '<div class="rb-edit-row">';
    h += '<label class="input-label">Material</label>';
    h += '<div class="rb-seg-toggle">';
    h += '<div class="rb-seg-btn' + (piece.material !== 'flex' ? ' active' : '') + '" data-rb-set="material" data-rb-val="metal" data-rb-idx="' + idx + '">Metal</div>';
    h += '<div class="rb-seg-btn' + (piece.material === 'flex' ? ' active' : '') + '" data-rb-set="material" data-rb-val="flex" data-rb-idx="' + idx + '">Flex</div>';
    h += '</div>';
    h += '</div>';
    
    // Size
    h += '<div class="rb-edit-row">';
    h += '<label class="input-label">Size <span class="rb-rec">(rec: ' + recSize + '&#x2033;)</span></label>';
    h += '<select class="input-field" data-rb-set="size" data-rb-idx="' + idx + '">';
    var sizes = [4,5,6,7,8,9,10,12,14,16,18,20,22,24];
    sizes.forEach(function(s) {
      if (s > upSize) return; // Can't be bigger than upstream
      h += '<option value="' + s + '"' + (piece.size == s ? ' selected' : '') + '>' + s + '&#x2033;' + (s == recSize ? ' ← rec' : '') + '</option>';
    });
    h += '</select>';
    h += '</div>';
    
    // Length
    h += '<div class="rb-edit-row">';
    h += '<label class="input-label">Length (ft)</label>';
    h += '<input type="number" class="input-field" value="' + (piece.length || 12) + '" min="1" max="200" data-rb-set="length" data-rb-idx="' + idx + '">';
    h += '</div>';
    
    // Compression (flex only)
    if (piece.material === 'flex') {
      h += '<div class="rb-edit-row">';
      h += '<label class="input-label">Compression %</label>';
      h += '<div style="display:flex;gap:4px;flex-wrap:wrap">';
      [4,5,10,15,20,25,30].forEach(function(c) {
        h += '<div class="compression-preset-btn' + (piece.compression == c ? ' active' : '') + '" data-rb-set="compression" data-rb-val="' + c + '" data-rb-idx="' + idx + '" style="cursor:pointer;padding:5px 9px;border-radius:6px;font-size:11px;font-weight:600;border:1.5px solid ' + (piece.compression == c ? 'var(--accent)' : 'var(--surface-4)') + ';background:' + (piece.compression == c ? 'var(--accent)' : 'var(--surface)') + ';color:' + (piece.compression == c ? '#fff' : 'var(--text-2)') + '">' + c + '%</div>';
      });
      h += '</div>';
      h += '</div>';
    }
  }
  
  if (piece.type === 'reducer') {
    h += '<div class="rb-edit-row">';
    h += '<label class="input-label">Reduce from ' + upSize + '&#x2033; to:</label>';
    h += '<select class="input-field" data-rb-set="size" data-rb-idx="' + idx + '">';
    var sizes = [4,5,6,7,8,9,10,12,14,16,18,20,22,24];
    sizes.forEach(function(s) {
      if (s >= upSize) return; // Must be smaller
      h += '<option value="' + s + '"' + (piece.size == s ? ' selected' : '') + '>' + s + '&#x2033;</option>';
    });
    h += '</select>';
    h += '</div>';
  }
  
  if (piece.type === 'boot') {
    h += '<div class="rb-edit-row">';
    h += '<label class="input-label">Boot Type</label>';
    h += '<select class="input-field" data-rb-set="bootType" data-rb-idx="' + idx + '">';
    Object.keys(RB_BOOT_TYPES).forEach(function(k) {
      var bt = RB_BOOT_TYPES[k];
      h += '<option value="' + k + '"' + (piece.bootType === k ? ' selected' : '') + '>' + bt.name + ' (+' + bt.eq + 'ft)</option>';
    });
    h += '</select>';
    h += '</div>';
  }
  
  // Done button
  h += '<div class="rb-edit-row" style="margin-top:4px">';
  h += '<button class="rb-done-btn" data-rb-done="' + idx + '">Done</button>';
  h += '</div>';
  
  h += '</div>';
  return h;
}

// --- Piece SVG icons ---
function rbPieceIcon(type) {
  switch (type) {
    case 'straight':
      return '<svg viewBox="0 0 32 32" width="24" height="24"><rect x="10" y="4" width="12" height="24" rx="2" fill="none" stroke="currentColor" stroke-width="1.5"/><line x1="12" y1="10" x2="20" y2="10" stroke="currentColor" stroke-width="0.5" opacity="0.4"/><line x1="12" y1="16" x2="20" y2="16" stroke="currentColor" stroke-width="0.5" opacity="0.4"/><line x1="12" y1="22" x2="20" y2="22" stroke="currentColor" stroke-width="0.5" opacity="0.4"/></svg>';
    case 'elbow90':
      return '<svg viewBox="0 0 32 32" width="24" height="24"><path d="M10 4 L10 18 Q10 24 16 24 L28 24" fill="none" stroke="currentColor" stroke-width="1.5" stroke-linecap="round"/></svg>';
    case 'elbow45':
      return '<svg viewBox="0 0 32 32" width="24" height="24"><path d="M12 4 L12 14 L24 26" fill="none" stroke="currentColor" stroke-width="1.5" stroke-linecap="round"/></svg>';
    case 'reducer':
      return '<svg viewBox="0 0 32 32" width="24" height="24"><path d="M8 4 L8 12 L12 20 L12 28 M24 4 L24 12 L20 20 L20 28" fill="none" stroke="currentColor" stroke-width="1.5"/></svg>';
    case 'wye':
      return '<svg viewBox="0 0 32 32" width="24" height="24"><line x1="16" y1="4" x2="16" y2="16" stroke="currentColor" stroke-width="1.5"/><line x1="16" y1="16" x2="6" y2="28" stroke="currentColor" stroke-width="1.5"/><line x1="16" y1="16" x2="26" y2="28" stroke="currentColor" stroke-width="1.5"/></svg>';
    case 'tee':
      return '<svg viewBox="0 0 32 32" width="24" height="24"><line x1="16" y1="4" x2="16" y2="28" stroke="currentColor" stroke-width="1.5"/><line x1="4" y1="16" x2="28" y2="16" stroke="currentColor" stroke-width="1.5"/></svg>';
    case 'dbox':
      return '<svg viewBox="0 0 32 32" width="24" height="24"><rect x="6" y="8" width="20" height="16" rx="3" fill="none" stroke="currentColor" stroke-width="1.5"/><circle cx="12" cy="24" r="2" fill="currentColor"/><circle cx="20" cy="24" r="2" fill="currentColor"/><line x1="16" y1="4" x2="16" y2="8" stroke="currentColor" stroke-width="1.5"/></svg>';
    case 'boot':
      return '<svg viewBox="0 0 32 32" width="24" height="24"><rect x="10" y="4" width="12" height="10" rx="1" fill="none" stroke="currentColor" stroke-width="1.5"/><path d="M10 14 L4 22 L28 22 L22 14" fill="none" stroke="currentColor" stroke-width="1.5"/><line x1="8" y1="26" x2="24" y2="26" stroke="currentColor" stroke-width="2"/></svg>';
    default:
      return '<svg viewBox="0 0 32 32" width="24" height="24"><circle cx="16" cy="16" r="8" fill="none" stroke="currentColor" stroke-width="1.5"/></svg>';
  }
}

// --- Calculate TEL for a run ---
function rbCalcRunTEL(run) {
  var tel = 0;
  var trunk = WIZ.trunks[run.trunkIdx] || WIZ.trunks[0];
  
  // Plenum EQ
  var isReturn = run.airPath === 'return';
  var plTypeEl = isReturn ? document.getElementById('retPlType') : document.getElementById('plType');
  var plTypeVal = plTypeEl ? plTypeEl.value : (isReturn ? 'box' : 'tapered');
  var plenumEQ = WIZ_PLENUM_EQ[plTypeVal] || 10;
  tel += plenumEQ;
  
  // Trunk EQ (same as existing)
  if (trunk && !trunk.isRadial) {
    var tLen = parseFloat(trunk.length) || 0;
    var tDia = typeof wizEffDia === 'function' ? wizEffDia(trunk) : 12;
    var tIsFlex = trunk.material === 'flex';
    var tIsDuctboard = trunk.material === 'ductboard';
    var tFF = tIsDuctboard ? 1.2 : (tIsFlex && typeof wizFlexFactor === 'function' ? wizFlexFactor(trunk.compression) : 1);
    var tEffLen = tLen * tFF;
    var t90eq = (trunk.elbows90 || 0) * (tDia <= 6 ? 10 : tDia <= 8 ? 15 : tDia <= 10 ? 20 : 25);
    var t45eq = (trunk.elbows45 || 0) * 5;
    var tDboxEq = (trunk.distBoxes || 0) * 50;
    tel += tEffLen + t90eq + t45eq + tDboxEq;
  }
  
  // Pieces
  run.pieces.forEach(function(p) {
    var ptype = RB_PIECE_TYPES[p.type];
    if (p.type === 'straight') {
      var len = parseFloat(p.length) || 0;
      var ff = 1;
      if (p.material === 'flex') {
        ff = typeof wizFlexFactor === 'function' ? wizFlexFactor(p.compression || 10) : 1.67;
      } else if (p.material === 'ductboard') {
        ff = 1.2;
      }
      tel += len * ff;
    } else if (p.type === 'boot') {
      var bt = RB_BOOT_TYPES[p.bootType] || { eq: 35 };
      tel += bt.eq;
      p.eqLength = bt.eq;
    } else if (ptype && ptype.eqFn) {
      var dia = p.size || rbGetUpstreamSize(run, run.pieces.indexOf(p));
      var eq = ptype.eqFn(dia);
      tel += eq;
      p.eqLength = eq;
    }
  });
  
  // Friction rate
  var asp = 0; // available static pressure
  var espEl = document.getElementById('wizESP');
  var coilEl = document.getElementById('wizCoilPD');
  var esp = espEl ? parseFloat(espEl.value) : 0.5;
  var coilPD = coilEl ? parseFloat(coilEl.value) : 0.07;
  asp = esp - coilPD;
  var fr = tel > 0 ? (asp / tel * 100) : 0;
  
  return { tel: tel, fr: fr };
}

// --- Add a piece to the current run ---
function rbAddPiece(typeKey) {
  var run = RB.runs[RB.activeRun];
  if (!run || rbIsRunComplete(run)) return;
  
  var upSize = rbGetUpstreamSize(run, run.pieces.length);
  var recSize = rbRecommendSize(run.totalCFM, upSize, WIZ.material, 10);
  
  var piece = { type: typeKey };
  
  if (typeKey === 'straight') {
    piece.material = WIZ.material || 'flex';
    piece.size = recSize;
    piece.length = 12;
    piece.compression = piece.material === 'flex' ? 10 : 0;
    piece.shape = 'round';
  } else if (typeKey === 'reducer') {
    // Reduce to next smaller standard size
    var nextSmaller = null;
    var sizes = [4,5,6,7,8,9,10,12,14,16,18,20,22,24];
    for (var i = sizes.length - 1; i >= 0; i--) {
      if (sizes[i] < upSize) { nextSmaller = sizes[i]; break; }
    }
    piece.size = nextSmaller || upSize - 1;
  } else if (typeKey === 'boot') {
    piece.bootType = '90boot';
  } else if (typeKey === 'dbox') {
    piece.dboxCollars = [];
  }
  
  run.pieces.push(piece);
  RB.editingPiece = run.pieces.length - 1; // open edit form
  run.complete = rbIsRunComplete(run);
  rbRender();
}

// --- Delete a piece ---
function rbDeletePiece(idx) {
  var run = RB.runs[RB.activeRun];
  if (!run) return;
  run.pieces.splice(idx, 1);
  if (RB.editingPiece >= run.pieces.length) RB.editingPiece = -1;
  if (RB.editingPiece === idx) RB.editingPiece = -1;
  run.complete = rbIsRunComplete(run);
  rbRender();
}

// --- Update a piece property ---
function rbSetPieceProperty(idx, prop, value) {
  var run = RB.runs[RB.activeRun];
  if (!run || !run.pieces[idx]) return;
  var piece = run.pieces[idx];
  
  if (prop === 'size' || prop === 'length' || prop === 'compression') {
    piece[prop] = parseInt(value) || 0;
  } else {
    piece[prop] = value;
  }
  
  // If material changed to flex, set defaults
  if (prop === 'material') {
    if (value === 'flex') {
      piece.compression = piece.compression || 10;
      piece.shape = 'round';
    } else {
      piece.compression = 0;
    }
  }
  
  run.complete = rbIsRunComplete(run);
  rbRender();
}

// --- Event handler ---
function rbHandleClick(e) {
  var t = e.target;
  
  // Tab switch
  var tab = t.closest('[data-rb-tab]');
  if (tab) {
    rbSaveCurrentRun();
    RB.activeRun = parseInt(tab.dataset.rbTab);
    RB.editingPiece = -1;
    rbRender();
    return;
  }
  
  // Add piece
  var add = t.closest('[data-rb-add]');
  if (add) {
    rbAddPiece(add.dataset.rbAdd);
    return;
  }
  
  // Delete piece
  var del = t.closest('[data-rb-delete]');
  if (del) {
    rbDeletePiece(parseInt(del.dataset.rbDelete));
    return;
  }
  
  // Tap piece to edit
  var piece = t.closest('[data-rb-piece]');
  if (piece && !t.closest('[data-rb-delete]') && !t.closest('.rb-edit-form')) {
    var idx = parseInt(piece.dataset.rbPiece);
    RB.editingPiece = (RB.editingPiece === idx) ? -1 : idx;
    rbRender();
    return;
  }
  
  // Set property (segment toggle)
  var setBtn = t.closest('[data-rb-set]');
  if (setBtn && setBtn.dataset.rbVal !== undefined) {
    rbSetPieceProperty(parseInt(setBtn.dataset.rbIdx), setBtn.dataset.rbSet, setBtn.dataset.rbVal);
    return;
  }
  
  // Done editing
  var done = t.closest('[data-rb-done]');
  if (done) {
    RB.editingPiece = -1;
    rbRender();
    return;
  }
}

function rbHandleChange(e) {
  var t = e.target;
  
  // Select/input changes
  if (t.dataset.rbSet) {
    rbSetPieceProperty(parseInt(t.dataset.rbIdx), t.dataset.rbSet, t.value);
    return;
  }
  
  // Room name
  if (t.dataset.rbRoom !== undefined) {
    var run = RB.runs[parseInt(t.dataset.rbRoom)];
    if (run) run.room = t.value;
  }
  
  // CFM
  if (t.dataset.rbCfm !== undefined) {
    var run = RB.runs[parseInt(t.dataset.rbCfm)];
    if (run) run.totalCFM = parseInt(t.value) || 0;
  }
}

// --- Save current run inputs from DOM ---
function rbSaveCurrentRun() {
  // room and cfm are saved via change handler
}

// --- Translate runs into WIZ.branches format for calc engine ---
function rbTranslateToBranches() {
  WIZ.branches = [];
  var num = 1;
  
  RB.runs.forEach(function(run, ri) {
    // Aggregate straight duct info
    var totalLength = 0;
    var material = WIZ.material;
    var compression = 0;
    var size = run.collarSize;
    var fittings = [];
    var bootType = '90boot';
    var takeoffType = 'straight90';
    var shape = 'round';
    var width = '8';
    var height = '8';
    
    run.pieces.forEach(function(p, pi) {
      if (p.type === 'straight') {
        totalLength += parseFloat(p.length) || 0;
        material = p.material || material;
        compression = p.compression || compression;
        if (p.size) size = p.size;
        shape = p.shape || 'round';
      } else if (p.type === 'boot') {
        bootType = p.bootType || '90boot';
      } else if (p.type === 'reducer') {
        if (p.size) size = p.size;
        fittings.push({ type: 'reducer' });
      } else if (p.type === 'dbox') {
        fittings.push({ type: 'dbox' });
      } else {
        // elbow90, elbow45, wye, tee
        fittings.push({ type: p.type });
      }
    });
    
    WIZ.branches.push({
      trunkIdx: run.trunkIdx,
      num: num,
      room: run.room,
      cfm: run.totalCFM || '',
      shape: shape,
      size: String(size),
      width: width,
      height: height,
      material: material,
      compression: compression,
      length: String(totalLength),
      fittings: fittings,
      bootType: bootType,
      takeoffType: takeoffType,
      done: rbIsRunComplete(run),
      recommended: String(size),
      runouts: []
    });
    num++;
  });
}
