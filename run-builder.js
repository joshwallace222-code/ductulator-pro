// ===== DUCT RUN BUILDER v5 =====
// Tree structure: each trunk has a chain of nodes.
// Splits (wye/tee/dbox) create child chains.
// You build from collar to boots, piece by piece.

var RB = { trunks: [], idx: 0, activePath: null, activeNode: -1 };

// Node types
var RB_TYPES = {
  trunk:     { name: 'Trunk', isTrunk: true },
  straight:  { name: 'Straight Duct' },
  elbow90:   { name: '90\u00B0 Elbow', eq: function(d){return d<=6?10:d<=8?15:d<=10?20:25;} },
  elbow45:   { name: '45\u00B0 Elbow', eq: function(){return 5;} },
  reducer:   { name: 'Reducer', eq: function(){return 5;} },
  wye:       { name: 'Wye Split', eq: function(){return 15;}, splits: 2 },
  tee:       { name: 'Tee Split', eq: function(){return 35;}, splits: 2 },
  dbox:      { name: 'Dist Box', eq: function(){return 50;}, splits: 3 },
  bullhead:  { name: 'Bullhead Tee', eq: function(){return 120;}, splits: 2 },
  boot:      { name: 'Boot/Register', isEnd: true }
};
var RB_BOOTS = {
  '90boot':{name:'90\u00B0 Boot',eq:55},'straightboot':{name:'Straight Boot',eq:35},
  'ceilTop':{name:'Ceiling (top)',eq:10},'ceilSide':{name:'Ceiling (side)',eq:40},
  'floorReg':{name:'Floor Reg',eq:35},'wallReg':{name:'Wall Reg',eq:40}
};
var RB_REG_STYLES = ['Bar Grille','Stamped Face','High Sidewall','Linear Slot','Eggcrate','Perforated'];

// ---- Init ----
function rbInit() {
  RB.trunks = []; RB.idx = 0; RB.activePath = null; RB.activeNode = -1;
  WIZ.trunks.forEach(function(t, ti) {
    RB.trunks.push({
      wizIdx: ti, label: t.label, airPath: t.airPath||'supply',
      size: parseInt(t.size)||12, length: parseFloat(t.length)||0,
      material: t.material||'metal', compression: t.compression||0,
      // The chain: first node is always the trunk itself, then user adds pieces
      chain: [{
        type: 'trunk', size: parseInt(t.size)||12, length: parseFloat(t.length)||0,
        material: t.material||'metal', compression: t.compression||0
      }]
      // When a split is added, that node gets a 'children' array of sub-chains
    });
  });
}

// ---- Helpers ----
function rbRecSize(cfm,up,mat,comp){
  if(!cfm||cfm<=0)return Math.min(up||6,8);
  var ff=(mat==='flex'&&typeof wizFlexFactor==='function')?wizFlexFactor(comp||10):(mat==='flex'?1.67:1);
  var szs=[4,5,6,7,8,9,10,12,14,16,18,20,22,24];
  for(var i=0;i<szs.length;i++){var d=szs[i];if(up&&d>up)break;
    var A=Math.PI*Math.pow(d/12/2,2);var v=cfm/A;if(v>(mat==='flex'?700:900))continue;
    var fr=typeof frictionLoss==='function'?frictionLoss(d,cfm):0.08;if(fr*ff<=0.08)return d;}
  return Math.min(up||6,8);
}
function rbMaxCFM(sz,mat,comp){return typeof wizMaxCFM==='function'?wizMaxCFM(sz,mat,comp):999;}

// Get the current duct size at a point in the chain
function rbSizeAt(chain, upTo) {
  var sz = chain[0] ? chain[0].size : 12;
  for (var i=0; i<(upTo||chain.length); i++) {
    if (chain[i] && chain[i].size) sz = chain[i].size;
  }
  return sz;
}

// Count total CFM downstream of a point (sum all boots in this chain + children)
function rbDownstreamCFM(chain, fromIdx) {
  var total = 0;
  for (var i=(fromIdx||0); i<chain.length; i++) {
    var n = chain[i];
    if (n.type === 'boot') total += (n.cfm || 0);
    if (n.children) {
      n.children.forEach(function(subChain) { total += rbDownstreamCFM(subChain, 0); });
    }
  }
  return total;
}

// Check if chain is complete (all paths end at boots)
function rbChainComplete(chain) {
  if (!chain || chain.length === 0) return false;
  var last = chain[chain.length - 1];
  if (last.type === 'boot') return true;
  if (last.children) {
    return last.children.every(function(sub) { return rbChainComplete(sub); });
  }
  return false;
}

// Get unassigned rooms
function rbGetUnassignedRooms() {
  var rooms = typeof getRoomsList === 'function' ? getRoomsList() : [];
  var assigned = {};
  // Walk all chains and find assigned room indices
  RB.trunks.forEach(function(trunk) {
    rbWalkChain(trunk.chain, function(node) {
      if (node.type === 'boot' && node.roomIdx >= 0) assigned[node.roomIdx] = true;
    });
  });
  return rooms.map(function(r, i) {
    return { name: r.name, cfm: r.cfm, idx: i, assigned: !!assigned[i] };
  }).filter(function(r) { return !r.assigned; });
}

function rbWalkChain(chain, fn) {
  chain.forEach(function(node) {
    fn(node);
    if (node.children) node.children.forEach(function(sub) { rbWalkChain(sub, fn); });
  });
}

// ============ RENDER ============
function rbRender() {
  var el = document.getElementById('wizBranchArea');
  if (!el) return;
  if (RB.trunks.length === 0) rbInit();
  if (RB.trunks.length === 0) { el.innerHTML='<div style="text-align:center;padding:20px;color:var(--text-3)">No trunks. Go back to step 2.</div>'; return; }

  var supTrunks = RB.trunks.filter(function(t){return t.airPath==='supply';});
  var retTrunks = RB.trunks.filter(function(t){return t.airPath==='return';});
  var trunk = RB.trunks[RB.idx];
  var isSupply = trunk.airPath === 'supply';
  var section = isSupply ? supTrunks : retTrunks;
  var sIdx = section.indexOf(trunk);
  var trunkCFM = rbDownstreamCFM(trunk.chain, 0);
  var trunkMaxCFM = rbMaxCFM(trunk.size, trunk.material, trunk.compression);
  var isComplete = rbChainComplete(trunk.chain);

  var h = '';

  // Section toggle
  if (supTrunks.length > 0 && retTrunks.length > 0) {
    h += '<div class="rb-seg" style="margin-bottom:8px">';
    h += '<div class="rb-seg-btn' + (isSupply ? ' active' : '') + '" data-rb-section="supply">Supply (' + supTrunks.length + ')</div>';
    h += '<div class="rb-seg-btn' + (!isSupply ? ' active' : '') + '" data-rb-section="return">Return (' + retTrunks.length + ')</div>';
    h += '</div>';
  }

  // Trunk dots
  if (section.length > 1) {
    h += '<div class="rb-dots">';
    section.forEach(function(t, i) {
      var cls = 'rb-dot';
      if (i === sIdx) cls += ' active';
      else if (rbChainComplete(t.chain)) cls += ' done';
      h += '<div class="' + cls + '" data-rb-trunk-dot="' + RB.trunks.indexOf(t) + '"></div>';
    });
    h += '</div>';
  }

  // ===== TRUNK CARD =====
  h += '<div class="rb-run-card">';

  // Header
  h += '<div class="rb-run-hdr">';
  h += '<div class="rb-run-title">' + trunk.label + '</div>';
  h += '<div class="rb-run-badges">';
  h += '<span class="rb-badge ' + (isSupply ? 'rb-badge-sup' : 'rb-badge-ret') + '">' + (isSupply ? 'SUP' : 'RTN') + '</span>';
  h += '<span class="rb-badge rb-badge-size">' + trunk.size + '&#x2033;</span>';
  h += '</div></div>';

  // Trunk CFM load
  h += '<div style="margin-bottom:8px">';
  h += '<div style="display:flex;justify-content:space-between;font-size:10px;margin-bottom:2px">';
  h += '<span style="color:var(--text-3)">Downstream CFM</span>';
  var cfmOk = trunkCFM <= trunkMaxCFM;
  h += '<span style="font-family:\'DM Mono\',monospace;font-weight:600;color:' + (cfmOk ? 'var(--green)' : 'var(--red)') + '">' + trunkCFM + ' / ' + trunkMaxCFM + ' CFM</span>';
  h += '</div>';
  var pct = trunkMaxCFM > 0 ? Math.min(trunkCFM / trunkMaxCFM * 100, 100) : 0;
  h += '<div style="height:6px;border-radius:3px;background:var(--surface-3);overflow:hidden">';
  h += '<div style="height:100%;width:' + pct + '%;border-radius:3px;background:' + (cfmOk ? 'var(--green)' : 'var(--red)') + ';transition:width 0.3s"></div>';
  h += '</div></div>';

  // ===== CHAIN BUILDER =====
  h += '<div style="font-size:11px;font-weight:700;color:var(--text-2);text-transform:uppercase;letter-spacing:0.5px;margin-bottom:6px">Build the Run</div>';
  h += rbRenderChain(trunk.chain, 'root', 0, trunk);

  // Status
  if (isComplete) {
    h += '<div class="rb-done-banner" style="margin-top:8px">';
    h += '<svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M22 11.08V12a10 10 0 1 1-5.93-9.14"/><polyline points="22 4 12 14.01 9 11.01"/></svg>';
    h += ' All paths complete';
    if (sIdx < section.length - 1) h += ' \u2014 <span data-rb-next style="text-decoration:underline;cursor:pointer">next trunk \u203A</span>';
    h += '</div>';
  }

  // Nav
  if (section.length > 1) {
    h += '<div style="display:flex;justify-content:space-between;margin-top:10px">';
    h += (sIdx > 0 ? '<button class="wiz-btn-secondary" data-rb-prev style="border-radius:10px;padding:8px 16px">\u2039 Prev</button>' : '<div></div>');
    h += (sIdx < section.length - 1 ? '<button class="wiz-btn-secondary" data-rb-next style="border-radius:10px;padding:8px 16px">Next \u203A</button>' : '<div></div>');
    h += '</div>';
  }

  h += '</div>'; // /run-card
  el.innerHTML = h;
  // Auto-save
  if (typeof wizAutoSave === 'function') wizAutoSave();
}

// Render a chain (recursive for sub-chains after splits)
function rbRenderChain(chain, pathId, indent, trunk) {
  var h = '';
  var indentPx = indent * 20;
  var rooms = rbGetUnassignedRooms();
  var allRooms = typeof getRoomsList === 'function' ? getRoomsList() : [];

  chain.forEach(function(node, ni) {
    var nodeId = pathId + '-' + ni;
    var isActive = RB.activePath === pathId && RB.activeNode === ni;
    var curSize = rbSizeAt(chain, ni);
    var isSplit = RB_TYPES[node.type] && RB_TYPES[node.type].splits;

    // Node card
    h += '<div class="rb-node' + (isActive ? ' rb-node-active' : '') + (node.type === 'boot' ? ' rb-node-end' : '') + (node.type === 'trunk' ? ' rb-node-start' : '') + '" style="margin-left:' + indentPx + 'px" data-rb-node="' + nodeId + '">';
    h += '<div class="rb-node-card">';
    h += '<div class="rb-node-icon" style="color:' + (node.type === 'boot' ? 'var(--green)' : node.type === 'trunk' ? 'var(--accent)' : isSplit ? 'var(--amber)' : 'var(--text-2)') + '">';
    h += rbNodeIcon(node.type);
    h += '</div>';
    h += '<div class="rb-node-body"><div class="rb-node-name">' + (RB_TYPES[node.type] ? RB_TYPES[node.type].name : node.type) + '</div>';
    h += '<div class="rb-node-detail">';
    if (node.type === 'trunk') {
      h += node.size + '&#x2033; ' + node.material + ' &middot; ' + node.length + 'ft';
    } else if (node.type === 'straight') {
      h += (node.size || curSize) + '&#x2033; ' + (node.material || 'flex') + ' &middot; ' + (node.length || 0) + 'ft';
      if (node.material === 'flex' && node.compression) h += ' &middot; ' + node.compression + '%';
    } else if (node.type === 'reducer') {
      h += curSize + '&#x2033; \u2192 ' + (node.size || '?') + '&#x2033;';
    } else if (node.type === 'boot') {
      var bt = RB_BOOTS[node.bootType] || { name: 'Boot' };
      h += bt.name + (node.room ? ' \u2192 ' + node.room : '') + (node.cfm ? ' (' + node.cfm + ' CFM)' : '');
    } else if (isSplit) {
      var eq = RB_TYPES[node.type].eq ? RB_TYPES[node.type].eq(curSize) : 0;
      h += '+' + eq + 'ft EQ \u2014 splits into ' + (RB_TYPES[node.type].splits || 2) + ' paths';
    } else {
      var eq2 = RB_TYPES[node.type] && RB_TYPES[node.type].eq ? RB_TYPES[node.type].eq(curSize) : 0;
      h += '+' + eq2 + 'ft EQ';
    }
    h += '</div></div>';
    // Delete (not trunk)
    if (node.type !== 'trunk') {
      h += '<div class="rb-node-x" data-rb-del="' + nodeId + '">&times;</div>';
    }
    h += '</div></div>'; // /node-card, /node

    // If this node is being edited, show edit form
    if (isActive) {
      h += rbEditForm(node, nodeId, curSize, trunk, rooms, allRooms);
    }

    // Connector
    if (ni < chain.length - 1 || (!node.children && node.type !== 'boot')) {
      h += '<div class="rb-connector" style="margin-left:' + (indentPx + 11) + 'px"></div>';
    }

    // If this is a split node with children, render each sub-chain
    if (node.children) {
      node.children.forEach(function(subChain, sci) {
        var subPath = pathId + '-' + ni + '-c' + sci;
        var subLabel = isSplit ? (RB_TYPES[node.type].name + ' Leg ' + (sci + 1)) : 'Path ' + (sci + 1);
        h += '<div style="margin-left:' + (indentPx + 10) + 'px;border-left:2px solid var(--surface-4);padding-left:8px;margin-top:4px;margin-bottom:4px">';
        h += '<div style="font-size:10px;font-weight:600;color:var(--amber);margin-bottom:4px">' + subLabel + '</div>';
        h += rbRenderChain(subChain, subPath, indent + 1, trunk);
        // Add piece button for this sub-chain (if not complete)
        if (!rbChainComplete(subChain)) {
          h += rbAddPieceButtons(subPath, rbSizeAt(subChain, subChain.length), trunk);
        }
        h += '</div>';
      });
    }
  });

  // Add piece buttons at the end (only for root-level chains that aren't complete)
  var lastNode = chain[chain.length - 1];
  if (!lastNode || (!lastNode.children && lastNode.type !== 'boot')) {
    h += rbAddPieceButtons(pathId, rbSizeAt(chain, chain.length), trunk);
  }

  return h;
}

// Add piece buttons
function rbAddPieceButtons(pathId, curSize, trunk) {
  var h = '<div class="rb-add-section" style="margin-top:6px">';
  h += '<div class="rb-add-title">Add next piece</div>';
  h += '<div class="rb-add-grid">';
  var pieces = ['straight', 'elbow90', 'elbow45', 'reducer', 'wye', 'tee', 'dbox', 'boot'];
  pieces.forEach(function(k) {
    h += '<div class="rb-add-btn" data-rb-add="' + k + '" data-rb-path="' + pathId + '">';
    h += rbNodeIcon(k);
    h += '<div class="rb-add-lbl">' + RB_TYPES[k].name + '</div></div>';
  });
  h += '</div></div>';
  return h;
}

// Edit form for a node
function rbEditForm(node, nodeId, curSize, trunk, unassignedRooms, allRooms) {
  var h = '<div class="rb-edit" style="margin-left:' + 0 + 'px">';

  if (node.type === 'straight') {
    // Material
    h += '<div class="rb-edit-row"><label class="input-label">Material</label>';
    h += '<div class="rb-seg">';
    h += '<div class="rb-seg-btn' + (node.material !== 'flex' ? ' active' : '') + '" data-rb-set="material" data-rb-v="metal" data-rb-nid="' + nodeId + '">Metal</div>';
    h += '<div class="rb-seg-btn' + (node.material === 'flex' ? ' active' : '') + '" data-rb-set="material" data-rb-v="flex" data-rb-nid="' + nodeId + '">Flex</div>';
    h += '</div></div>';
    // Size
    var recSz = rbRecSize(rbDownstreamCFM([node], 0) || 100, curSize, node.material, node.compression);
    h += '<div class="rb-edit-row"><label class="input-label">Size <span class="rb-rec-tag">rec: ' + recSz + '&#x2033;</span></label>';
    h += '<select class="input-field" data-rb-sel="size" data-rb-nid="' + nodeId + '">';
    [4,5,6,7,8,9,10,12,14,16,18,20,22,24].forEach(function(s) {
      if (s > trunk.size) return;
      h += '<option value="' + s + '"' + (node.size == s ? ' selected' : '') + '>' + s + '&#x2033;' + (s == recSz ? ' \u2190 rec' : '') + '</option>';
    });
    h += '</select></div>';
    // Length
    h += '<div class="rb-edit-row"><label class="input-label">Length (ft)</label>';
    h += '<input type="number" class="input-field" value="' + (node.length || 12) + '" min="1" max="200" data-rb-inp="length" data-rb-nid="' + nodeId + '"></div>';
    // Compression
    if (node.material === 'flex') {
      h += '<div class="rb-edit-row"><label class="input-label">Compression %</label>';
      h += '<div class="rb-comp-chips">';
      [4,5,10,15,20,25,30].forEach(function(c) {
        h += '<div class="rb-comp-chip' + (node.compression == c ? ' active' : '') + '" data-rb-set="compression" data-rb-v="' + c + '" data-rb-nid="' + nodeId + '">' + c + '%</div>';
      });
      h += '</div></div>';
    }
  }

  if (node.type === 'reducer') {
    h += '<div class="rb-edit-row"><label class="input-label">Reduce to:</label>';
    h += '<select class="input-field" data-rb-sel="size" data-rb-nid="' + nodeId + '">';
    [4,5,6,7,8,9,10,12,14,16,18,20,22,24].forEach(function(s) {
      if (s >= curSize) return;
      h += '<option value="' + s + '"' + (node.size == s ? ' selected' : '') + '>' + s + '&#x2033;</option>';
    });
    h += '</select></div>';
  }

  if (node.type === 'boot') {
    // Room picker (only unassigned rooms)
    h += '<div class="rb-edit-row"><label class="input-label">Room (destination)</label>';
    h += '<select class="input-field" data-rb-sel="roomIdx" data-rb-nid="' + nodeId + '">';
    h += '<option value="-1">\u2014 Pick a Room \u2014</option>';
    unassignedRooms.forEach(function(r) {
      h += '<option value="' + r.idx + '"' + (node.roomIdx === r.idx ? ' selected' : '') + '>' + r.name + ' (' + r.cfm + ' CFM)</option>';
    });
    // Also show the currently assigned room if it's already assigned
    if (node.roomIdx >= 0 && allRooms[node.roomIdx]) {
      var alreadyInList = unassignedRooms.some(function(r) { return r.idx === node.roomIdx; });
      if (!alreadyInList) {
        h += '<option value="' + node.roomIdx + '" selected>' + allRooms[node.roomIdx].name + ' (' + allRooms[node.roomIdx].cfm + ' CFM) \u2713</option>';
      }
    }
    h += '<option value="-2">Custom / Home Run</option>';
    h += '</select></div>';

    if (node.roomIdx >= 0 && allRooms[node.roomIdx]) {
      h += '<div style="font-size:11px;color:var(--accent);font-weight:600;margin-bottom:6px">' + allRooms[node.roomIdx].cfm + ' CFM \u2192 ' + allRooms[node.roomIdx].name + '</div>';
    } else if (node.roomIdx === -2) {
      h += '<div class="rb-edit-row"><label class="input-label">CFM</label><input type="number" class="input-field" value="' + (node.cfm||'') + '" data-rb-inp="cfm" data-rb-nid="' + nodeId + '"></div>';
      h += '<div class="rb-edit-row"><label class="input-label">Name</label><input type="text" class="input-field" value="' + (node.room||'') + '" data-rb-inp="room" data-rb-nid="' + nodeId + '"></div>';
    }

    // Mount type (default from system config)
    var defaultMount = WIZ.bootPosition || 'floor';
    if (!node.mountType) node.mountType = defaultMount;
    h += '<div class="rb-edit-row"><label class="input-label">Register Location</label>';
    h += '<div class="rb-seg">';
    ['floor','wall','ceiling'].forEach(function(mt) {
      h += '<div class="rb-seg-btn' + (node.mountType === mt ? ' active' : '') + '" data-rb-set="mountType" data-rb-v="' + mt + '" data-rb-nid="' + nodeId + '">' + mt.charAt(0).toUpperCase() + mt.slice(1) + '</div>';
    });
    h += '</div></div>';

    // Boot type
    h += '<div class="rb-edit-row"><label class="input-label">Boot Type</label>';
    h += '<select class="input-field" data-rb-sel="bootType" data-rb-nid="' + nodeId + '">';
    Object.keys(RB_BOOTS).forEach(function(k) {
      h += '<option value="' + k + '"' + (node.bootType === k ? ' selected' : '') + '>' + RB_BOOTS[k].name + ' (+' + RB_BOOTS[k].eq + 'ft)</option>';
    });
    h += '</select></div>';

    // Boot SVG
    h += '<div style="text-align:center;margin:6px 0">' + rbBootSVG(node.bootType, node.mountType) + '</div>';

    // Boot size
    if (typeof getBootSizes === 'function') {
      var cat = node.mountType === 'ceiling' ? 'ceiling' : (node.mountType === 'wall' ? 'wall' : 'floor');
      var bSizes = getBootSizes(curSize, cat);
      if (bSizes.length > 0) {
        h += '<div class="rb-edit-row"><label class="input-label">Boot/Register Size</label>';
        h += '<select class="input-field" data-rb-sel="bootSize" data-rb-nid="' + nodeId + '">';
        h += '<option value="">\u2014 Select \u2014</option>';
        bSizes.forEach(function(bs) { h += '<option value="' + bs.reg + '"' + (node.bootSize === bs.reg ? ' selected' : '') + '>' + bs.reg + '</option>'; });
        h += '</select></div>';
      }
    }

    // Register style
    h += '<div class="rb-edit-row"><label class="input-label">Register Style</label>';
    h += '<select class="input-field" data-rb-sel="regStyle" data-rb-nid="' + nodeId + '">';
    RB_REG_STYLES.forEach(function(s) { h += '<option value="' + s + '"' + (node.regStyle === s ? ' selected' : '') + '>' + s + '</option>'; });
    h += '</select></div>';

    // CFM check
    if (node.cfm > 0) {
      var brMax = rbMaxCFM(curSize, node.material || 'flex', node.compression || 0);
      var ok = brMax >= node.cfm;
      h += '<div style="font-size:11px;padding:6px 8px;border-radius:6px;margin-top:4px;background:' + (ok ? 'var(--green-soft)' : 'var(--red-soft)') + ';color:' + (ok ? 'var(--green)' : 'var(--red)') + '">';
      h += ok ? '\u2713 ' + curSize + '&#x2033; ' + (node.material||'flex') + ' delivers ' + brMax + ' CFM (need ' + node.cfm + ')' :
                '\u26A0 ' + curSize + '&#x2033; ' + (node.material||'flex') + ' max ' + brMax + ' CFM \u2014 need ' + node.cfm + '. Upsize to ' + rbRecSize(node.cfm, trunk.size, node.material||'flex', node.compression||10) + '&#x2033;';
      h += '</div>';
    }
  }

  h += '<button class="rb-btn-done" data-rb-done>Done</button>';
  h += '</div>';
  return h;
}

// Node icons
function rbNodeIcon(t) {
  var i = {
    trunk:'<svg viewBox="0 0 24 24" width="16" height="16"><rect x="7" y="2" width="10" height="20" rx="2" fill="none" stroke="currentColor" stroke-width="1.5"/></svg>',
    straight:'<svg viewBox="0 0 24 24" width="16" height="16"><rect x="9" y="3" width="6" height="18" rx="1" fill="none" stroke="currentColor" stroke-width="1.5"/></svg>',
    elbow90:'<svg viewBox="0 0 24 24" width="16" height="16"><path d="M9 3v9a4 4 0 004 4h8" fill="none" stroke="currentColor" stroke-width="1.5" stroke-linecap="round"/></svg>',
    elbow45:'<svg viewBox="0 0 24 24" width="16" height="16"><path d="M10 3v6l7 10" fill="none" stroke="currentColor" stroke-width="1.5" stroke-linecap="round"/></svg>',
    reducer:'<svg viewBox="0 0 24 24" width="16" height="16"><path d="M7 3v7l3 4v7M17 3v7l-3 4v7" fill="none" stroke="currentColor" stroke-width="1.5"/></svg>',
    wye:'<svg viewBox="0 0 24 24" width="16" height="16"><line x1="12" y1="3" x2="12" y2="12" stroke="currentColor" stroke-width="1.5"/><line x1="12" y1="12" x2="5" y2="21" stroke="currentColor" stroke-width="1.5"/><line x1="12" y1="12" x2="19" y2="21" stroke="currentColor" stroke-width="1.5"/></svg>',
    tee:'<svg viewBox="0 0 24 24" width="16" height="16"><line x1="12" y1="3" x2="12" y2="21" stroke="currentColor" stroke-width="1.5"/><line x1="4" y1="12" x2="20" y2="12" stroke="currentColor" stroke-width="1.5"/></svg>',
    dbox:'<svg viewBox="0 0 24 24" width="16" height="16"><rect x="4" y="6" width="16" height="12" rx="2" fill="none" stroke="currentColor" stroke-width="1.5"/><circle cx="8" cy="18" r="1.5" fill="currentColor"/><circle cx="12" cy="18" r="1.5" fill="currentColor"/><circle cx="16" cy="18" r="1.5" fill="currentColor"/></svg>',
    bullhead:'<svg viewBox="0 0 24 24" width="16" height="16"><line x1="12" y1="3" x2="12" y2="12" stroke="currentColor" stroke-width="1.5"/><line x1="4" y1="12" x2="20" y2="12" stroke="currentColor" stroke-width="2.5"/><line x1="6" y1="12" x2="6" y2="21" stroke="currentColor" stroke-width="1.5"/><line x1="18" y1="12" x2="18" y2="21" stroke="currentColor" stroke-width="1.5"/></svg>',
    boot:'<svg viewBox="0 0 24 24" width="16" height="16"><rect x="8" y="2" width="8" height="7" rx="1" fill="none" stroke="currentColor" stroke-width="1.5"/><path d="M8 9L4 16h16l-4-7" fill="none" stroke="currentColor" stroke-width="1.5"/><line x1="6" y1="19" x2="18" y2="19" stroke="currentColor" stroke-width="2"/></svg>'
  };
  return i[t] || '<svg viewBox="0 0 24 24" width="16" height="16"><circle cx="12" cy="12" r="5" fill="none" stroke="currentColor" stroke-width="1.5"/></svg>';
}

// Boot SVG visual (Manual D inspired cross-section)
function rbBootSVG(bootType, mountType) {
  var w = 140, ht = 90;
  var s = '<svg viewBox="0 0 ' + w + ' ' + ht + '" width="' + w + '" height="' + ht + '">';
  // Duct
  s += '<rect x="50" y="0" width="24" height="32" rx="2" fill="var(--surface-3)" stroke="var(--text-3)" stroke-width="1"/>';
  s += '<text x="62" y="18" text-anchor="middle" fill="var(--text-3)" font-size="8" font-weight="600">Duct</text>';

  if (bootType === '90boot' || bootType === 'wallReg') {
    // 90° bend to register
    s += '<path d="M54 32 C54 50, 62 54, 80 54" fill="none" stroke="var(--accent)" stroke-width="3" stroke-linecap="round"/>';
    s += '<path d="M70 32 C70 44, 74 48, 80 48" fill="none" stroke="var(--accent)" stroke-width="3" stroke-linecap="round"/>';
    s += '<rect x="80" y="42" width="8" height="18" rx="1" fill="var(--accent)" fill-opacity="0.2" stroke="var(--accent)" stroke-width="1.5"/>';
    s += '<text x="80" y="72" fill="var(--text-2)" font-size="7" font-weight="600">' + (mountType === 'wall' ? 'Wall Reg' : '90\u00B0 Boot') + '</text>';
    // Airflow arrow
    s += '<path d="M62 10 L62 26" stroke="var(--green)" stroke-width="1" marker-end="url(#arrowG)"/>';
    s += '<path d="M72 52 L78 52" stroke="var(--green)" stroke-width="1" marker-end="url(#arrowG)"/>';
  } else if (bootType === 'straightboot' || bootType === 'floorReg') {
    // Straight down transition
    s += '<line x1="54" y1="32" x2="48" y2="60" stroke="var(--accent)" stroke-width="2.5"/>';
    s += '<line x1="70" y1="32" x2="76" y2="60" stroke="var(--accent)" stroke-width="2.5"/>';
    s += '<rect x="44" y="60" width="36" height="7" rx="1" fill="var(--accent)" fill-opacity="0.2" stroke="var(--accent)" stroke-width="1.5"/>';
    s += '<text x="62" y="78" text-anchor="middle" fill="var(--text-2)" font-size="7" font-weight="600">' + (mountType === 'floor' ? 'Floor Reg' : 'Straight') + '</text>';
    s += '<path d="M62 10 L62 56" stroke="var(--green)" stroke-width="1" marker-end="url(#arrowG)"/>';
  } else if (bootType === 'ceilTop' || bootType === 'ceilSide') {
    // Ceiling mount
    s += '<line x1="54" y1="32" x2="54" y2="52" stroke="var(--accent)" stroke-width="2.5"/>';
    s += '<line x1="70" y1="32" x2="70" y2="52" stroke="var(--accent)" stroke-width="2.5"/>';
    s += '<rect x="38" y="52" width="48" height="5" fill="var(--surface-4)" stroke="var(--text-3)" stroke-width="1"/>';
    s += '<text x="62" y="55" text-anchor="middle" fill="var(--text-3)" font-size="5">CEILING</text>';
    s += '<ellipse cx="62" cy="70" rx="14" ry="6" fill="var(--accent)" fill-opacity="0.15" stroke="var(--accent)" stroke-width="1.5"/>';
    s += '<text x="62" y="73" text-anchor="middle" fill="var(--accent)" font-size="7" font-weight="600">Diff</text>';
    s += '<path d="M62 10 L62 48" stroke="var(--green)" stroke-width="1" marker-end="url(#arrowG)"/>';
  } else {
    s += '<line x1="58" y1="32" x2="58" y2="58" stroke="var(--accent)" stroke-width="2"/>';
    s += '<line x1="66" y1="32" x2="66" y2="58" stroke="var(--accent)" stroke-width="2"/>';
    s += '<rect x="50" y="58" width="24" height="7" rx="1" fill="var(--accent)" fill-opacity="0.2" stroke="var(--accent)" stroke-width="1.5"/>';
  }
  // Arrow marker
  s += '<defs><marker id="arrowG" markerWidth="6" markerHeight="6" refX="5" refY="3" orient="auto"><path d="M0 0 L6 3 L0 6Z" fill="var(--green)"/></marker></defs>';
  s += '</svg>';
  return s;
}

// ============ EVENTS ============
function rbHandleClick(e) {
  var t = e.target;
  // Section
  var sec = t.closest('[data-rb-section]');
  if (sec) { var ap=sec.dataset.rbSection; var s=RB.trunks.filter(function(x){return x.airPath===ap;}); if(s.length>0){RB.idx=RB.trunks.indexOf(s[0]);RB.activePath=null;RB.activeNode=-1;rbRender();} return; }
  // Dots
  var dot = t.closest('[data-rb-trunk-dot]');
  if (dot) { RB.idx=parseInt(dot.dataset.rbTrunkDot); RB.activePath=null; RB.activeNode=-1; rbRender(); return; }
  // Nav
  if (t.closest('[data-rb-prev]')) { rbNavTrunk(-1); return; }
  if (t.closest('[data-rb-next]')) { rbNavTrunk(1); return; }

  // Add piece
  var add = t.closest('[data-rb-add]');
  if (add) {
    var type = add.dataset.rbAdd;
    var pathId = add.dataset.rbPath || add.closest('[data-rb-path]')?.dataset.rbPath || 'root';
    rbAddNode(type, pathId);
    return;
  }

  // Tap node to edit
  var nodeEl = t.closest('[data-rb-node]');
  if (nodeEl && !t.closest('[data-rb-del]') && !t.closest('.rb-edit')) {
    var nid = nodeEl.dataset.rbNode;
    var parts = nid.split('-');
    var pathParts = parts.slice(0, -1).join('-');
    var nodeIdx = parseInt(parts[parts.length - 1]);
    if (RB.activePath === pathParts && RB.activeNode === nodeIdx) {
      RB.activePath = null; RB.activeNode = -1;
    } else {
      RB.activePath = pathParts; RB.activeNode = nodeIdx;
    }
    rbRender();
    if (RB.activePath !== null) setTimeout(function(){ var ed=document.querySelector('.rb-edit'); if(ed)ed.scrollIntoView({behavior:'smooth',block:'center'});},50);
    return;
  }

  // Delete node
  var del = t.closest('[data-rb-del]');
  if (del) { rbDeleteNode(del.dataset.rbDel); return; }

  // Set property (segment buttons)
  var setBtn = t.closest('[data-rb-set]');
  if (setBtn) { rbSetNodeProp(setBtn.dataset.rbNid, setBtn.dataset.rbSet, setBtn.dataset.rbV); return; }

  // Done
  if (t.closest('[data-rb-done]')) { RB.activePath=null; RB.activeNode=-1; rbRender(); return; }
}

function rbHandleChange(e) {
  var t = e.target;
  if (t.dataset.rbSel) { rbSetNodeProp(t.dataset.rbNid, t.dataset.rbSel, t.value); return; }
  if (t.dataset.rbInp) { rbSetNodeProp(t.dataset.rbNid, t.dataset.rbInp, t.value); return; }
}

// ---- Resolve a nodeId to the actual chain + index ----
function rbResolveNode(nodeId) {
  var trunk = RB.trunks[RB.idx];
  if (!trunk) return null;
  var parts = nodeId.replace('root-', '').split('-');
  var chain = trunk.chain;
  var idx = 0;
  for (var i = 0; i < parts.length; i++) {
    if (parts[i].charAt(0) === 'c') {
      // Sub-chain index
      var sci = parseInt(parts[i].substring(1));
      var parentNode = chain[idx];
      if (!parentNode || !parentNode.children || !parentNode.children[sci]) return null;
      chain = parentNode.children[sci];
      idx = 0;
    } else {
      idx = parseInt(parts[i]);
    }
  }
  return { chain: chain, idx: idx, node: chain[idx] };
}

function rbAddNode(type, pathId) {
  var trunk = RB.trunks[RB.idx];
  if (!trunk) return;

  // Resolve the chain to append to
  var chain = trunk.chain;
  if (pathId !== 'root') {
    var parts = pathId.replace('root-', '').split('-');
    for (var i = 0; i < parts.length; i++) {
      if (parts[i].charAt(0) === 'c') {
        var sci = parseInt(parts[i].substring(1));
        var parentIdx = parseInt(parts[i-1] || 0);
        var parent = chain[parentIdx];
        if (parent && parent.children && parent.children[sci]) {
          chain = parent.children[sci];
        }
      }
    }
  }

  var curSize = rbSizeAt(chain, chain.length);
  var node = { type: type };

  if (type === 'straight') {
    node.material = WIZ.material || 'flex';
    node.size = curSize;
    node.length = 12;
    node.compression = (node.material === 'flex') ? 10 : 0;
  } else if (type === 'reducer') {
    var sizes = [4,5,6,7,8,9,10,12,14,16,18,20,22,24];
    var ns = curSize;
    for (var j = sizes.length-1; j >= 0; j--) { if (sizes[j] < curSize) { ns = sizes[j]; break; } }
    node.size = ns;
  } else if (type === 'boot') {
    node.bootType = '90boot';
    node.mountType = WIZ.bootPosition || 'floor';
    node.roomIdx = -1;
    node.room = '';
    node.cfm = 0;
    node.bootSize = '';
    node.regStyle = 'Stamped Face';
  }

  // If it's a split type, create children arrays
  if (RB_TYPES[type] && RB_TYPES[type].splits) {
    var numSplits = RB_TYPES[type].splits || 2;
    node.children = [];
    for (var s = 0; s < numSplits; s++) {
      node.children.push([]); // empty sub-chains
    }
  }

  chain.push(node);

  // Activate edit for this node
  var newIdx = chain.length - 1;
  // Build the path ID for this new node
  RB.activePath = pathId;
  RB.activeNode = newIdx;

  rbRender();
  setTimeout(function(){
    var ed = document.querySelector('.rb-edit');
    if (ed) ed.scrollIntoView({behavior:'smooth',block:'center'});
  }, 50);
}

function rbDeleteNode(nodeId) {
  var resolved = rbResolveNode(nodeId);
  if (!resolved || resolved.node.type === 'trunk') return;
  resolved.chain.splice(resolved.idx, 1);
  RB.activePath = null; RB.activeNode = -1;
  rbRender();
}

function rbSetNodeProp(nodeId, prop, value) {
  var resolved = rbResolveNode(nodeId);
  if (!resolved || !resolved.node) return;
  var node = resolved.node;
  var rooms = typeof getRoomsList === 'function' ? getRoomsList() : [];

  if (prop === 'size' || prop === 'length' || prop === 'compression' || prop === 'cfm') {
    node[prop] = parseInt(value) || 0;
  } else if (prop === 'roomIdx') {
    var ri = parseInt(value);
    node.roomIdx = ri;
    if (ri >= 0 && rooms[ri]) {
      node.room = rooms[ri].name;
      node.cfm = rooms[ri].cfm;
    }
  } else {
    node[prop] = value;
  }

  if (prop === 'material') {
    if (value === 'flex') { node.compression = node.compression || 10; }
    else { node.compression = 0; }
  }

  rbRender();
}

function rbNavTrunk(dir) {
  var trunk = RB.trunks[RB.idx];
  var isS = trunk.airPath === 'supply';
  var section = RB.trunks.filter(function(t) { return t.airPath === (isS ? 'supply' : 'return'); });
  var si = section.indexOf(trunk);
  var ns = si + dir;
  if (ns >= 0 && ns < section.length) {
    RB.idx = RB.trunks.indexOf(section[ns]);
    RB.activePath = null; RB.activeNode = -1;
    rbRender();
  }
}

// ============ TRANSLATE ============
function rbTranslateToBranches() {
  WIZ.branches = [];
  var num = 1;
  RB.trunks.forEach(function(trunk) {
    // Walk the chain and collect all boot endpoints as branches
    rbWalkChain(trunk.chain, function(node) {
      if (node.type === 'boot') {
        WIZ.branches.push({
          trunkIdx: trunk.wizIdx, num: num++, room: node.room || 'Branch',
          cfm: node.cfm || '', shape: 'round', size: String(node.size || 6),
          width: '8', height: '8', material: node.material || 'flex',
          compression: node.compression || 0, length: '12',
          fittings: [], bootType: node.bootType || '90boot',
          takeoffType: 'straight90', done: true, recommended: String(node.size || 6),
          runouts: [], mountType: node.mountType || 'floor',
          bootSize: node.bootSize || '', regStyle: node.regStyle || ''
        });
      }
    });
  });
}

function rbInitRuns() { rbInit(); }
