// ===== DUCT ESTIMATOR v2 =====
// Two modes: (1) Rough Estimate — quick ballpark from tonnage + layout profile
//            (2) Duct Estimator — detailed trunk/branch with material/shape/fittings
// Aligned with ACCA Manual D principles. Flags zoning per Manual Z/EWC/Resideo.
// NOT a Manual D or Manual Z replacement — realistic simplified field tool.

var DE = {
  mode: 'rough',       // 'rough' or 'detailed'
  lastResult: null,
  // Layout profiles: default assumptions for common residential systems
  PROFILES: {
    plenum_flex: {
      id: 'plenum_flex', label: 'Short Plenum + Flex Branches',
      desc: 'Most common residential — short metal/ductboard plenum off the unit with several flex runs.',
      trunkMat: 'metal', branchMat: 'flex', trunkShape: 'rect',
      plenumEQ: 15, avgBranchLen: 25, elbowsPer: 1, elbowEQ: 15,
      targetFR: 0.08, flexCompress: 10
    },
    extended_trunk: {
      id: 'extended_trunk', label: 'Extended Metal Trunk + Flex Runouts',
      desc: 'Metal trunk runs through the attic/crawl with flex takeoffs to each room.',
      trunkMat: 'metal', branchMat: 'flex', trunkShape: 'rect',
      plenumEQ: 15, avgBranchLen: 15, elbowsPer: 1, elbowEQ: 15,
      trunkLen: 30, trunkElbows: 1, trunkElbowEQ: 35,
      targetFR: 0.08, flexCompress: 10
    },
    octopus: {
      id: 'octopus', label: 'All-Flex Octopus',
      desc: 'All flex duct from plenum box — no metal trunk. Common in tract homes and mobile homes.',
      trunkMat: 'flex', branchMat: 'flex', trunkShape: 'round',
      plenumEQ: 10, avgBranchLen: 30, elbowsPer: 1.5, elbowEQ: 15,
      targetFR: 0.08, flexCompress: 10
    },
    rect_metal_round: {
      id: 'rect_metal_round', label: 'Rectangular Metal Trunk + Round Metal Branches',
      desc: 'Rectangular main trunk with round metal branch runs. Traditional high-quality install.',
      trunkMat: 'metal', branchMat: 'metal', trunkShape: 'rect',
      plenumEQ: 15, avgBranchLen: 20, elbowsPer: 2, elbowEQ: 12,
      trunkLen: 25, trunkElbows: 1, trunkElbowEQ: 25,
      targetFR: 0.08, flexCompress: 0
    }
  },
  // Plenum types with equivalent length presets
  PLENUM_TYPES: {
    straight: { label: 'Straight Plenum', eqLen: 10, teach: 'Lowest resistance. Air flows straight from equipment into trunk/branches.' },
    turn_vanes: { label: '90° Plenum w/ Turning Vanes', eqLen: 20, teach: 'Turning vanes guide airflow around the corner, cutting turbulence. Adds about 20 ft equivalent length.' },
    turn_no_vanes: { label: '90° Plenum — No Turning Vanes', eqLen: 50, teach: 'A 90° turn without vanes is very high resistance — about 50 ft equivalent length. Turbulence starves the far branches.' }
  },
  // Zoning config
  ZONING: {
    none: { label: 'No Zoning', staticMult: 1.0 },
    two: { label: '2 Zones', staticMult: 1.35 },
    three_plus: { label: '3+ Zones', staticMult: 1.5 }
  }
};

// ===========================
// CORE SIZING ENGINE
// ===========================

// Size a round duct for given CFM and material
function deSize(cfm, material, targetFR) {
  if (!targetFR) targetFR = 0.08;
  var candidates = [4, 5, 6, 7, 8, 9, 10, 12, 14, 16, 18, 20, 22, 24, 26, 28, 30];
  var best = null;
  var bestScore = Infinity;

  for (var i = 0; i < candidates.length; i++) {
    var d = candidates[i];
    var A = Math.PI * Math.pow(d / 12 / 2, 2); // sq ft
    var vel = cfm / A; // FPM
    var fr = 0;

    if (typeof frictionLoss === 'function') {
      fr = frictionLoss(d, cfm, material, false);
    } else {
      // Fallback Darcy-Weisbach
      var D_ft = d / 12;
      var V_fps = vel / 60;
      var rho = 0.075;
      var rough = material === 'flex' ? 0.003 : (material === 'ductboard' ? 0.002 : 0.0003);
      var Re = V_fps * D_ft / (1.63e-4);
      if (Re < 100) continue;
      var term1 = rough / (3.7 * D_ft);
      var term2 = 5.74 / Math.pow(Re, 0.9);
      var fD = 0.25 / Math.pow(Math.log10(term1 + term2), 2);
      fr = fD * (100 / D_ft) * (rho * V_fps * V_fps) / (2 * 32.174) / 5.192;
    }

    // Apply flex compression factor
    if (material === 'flex' && typeof flexFactor === 'function') {
      fr = fr * flexFactor(10);
    } else if (material === 'flex') {
      fr = fr * 2.0; // conservative fallback: 10% compression ~doubles FR
    }

    // Score: want FR ≤ targetFR, velocity 300-900 for supply
    var score = Math.abs(fr - targetFR * 0.8) * 100;
    if (fr > targetFR) score += (fr - targetFR) * 800;
    if (vel > 900) score += (vel - 900) * 0.2;
    if (vel < 200) score += (200 - vel) * 0.8;

    if (fr <= targetFR && vel <= 900 && vel >= 100) {
      if (score < bestScore) {
        bestScore = score;
        best = { size: d, velocity: Math.round(vel), friction: parseFloat(fr.toFixed(4)), area: A };
      }
      break; // smallest acceptable
    }
    if (score < bestScore) {
      bestScore = score;
      best = { size: d, velocity: Math.round(vel), friction: parseFloat(fr.toFixed(4)), area: A };
    }
  }
  if (!best) best = { size: 6, velocity: 0, friction: 0, area: 0 };
  return best;
}

// Rectangular equivalent for round duct (ASHRAE)
function deRectEquiv(roundDia) {
  // Common rect equivalents for residential trunks
  var map = {
    6: '8x6', 7: '8x6', 8: '10x6', 9: '10x8', 10: '12x8',
    12: '14x8', 14: '16x10', 16: '20x10', 18: '22x10',
    20: '24x12', 22: '26x12', 24: '28x14', 26: '30x14', 28: '32x16', 30: '36x16'
  };
  return map[roundDia] || (roundDia + '" round');
}

// Static pressure estimate
function deEstimateStatic(totalEQ, frictionRate, filterPD, coilPD, extras) {
  // Total duct PD = (TEL / 100) * FR
  var ductPD = (totalEQ / 100) * frictionRate;
  var total = ductPD + (filterPD || 0.1) + (coilPD || 0.2) + (extras || 0);
  return { ductPD: ductPD, filterPD: filterPD || 0.1, coilPD: coilPD || 0.2, total: total };
}

// Risk assessment
function deRiskLevel(totalStatic, zoning) {
  var threshold = zoning === 'none' ? 0.5 : (zoning === 'two' ? 0.45 : 0.4);
  var marginal = zoning === 'none' ? 0.4 : (zoning === 'two' ? 0.35 : 0.3);
  if (totalStatic <= marginal) return { level: 'ok', label: 'OK', color: 'var(--green)', desc: 'Static pressure is within a comfortable range for standard equipment.' };
  if (totalStatic <= threshold) return { level: 'marginal', label: 'Marginal', color: 'var(--amber)', desc: 'Static is getting close to equipment limits. Review longest runs and fitting losses.' };
  return { level: 'high', label: 'High Risk', color: 'var(--red)', desc: 'Static pressure exceeds typical equipment capacity. Oversized ducts, fewer fittings, or a high-static blower may be needed.' };
}


// ===========================
// MODE 1: ROUGH ESTIMATE
// ===========================

function deRoughEstimate() {
  // Read inputs
  var tons = parseFloat(document.getElementById('deRoughTons').value) || 0;
  var cfmPerTon = parseFloat(document.getElementById('deRoughCfmPerTon').value) || 400;
  var profileId = document.getElementById('deRoughProfile').value || 'plenum_flex';
  var plenumType = document.getElementById('deRoughPlenum').value || 'straight';
  var zoning = document.getElementById('deRoughZoning').value || 'none';
  var smallZone = document.getElementById('deRoughSmallZone') ? document.getElementById('deRoughSmallZone').value : 'no';
  var approxLen = parseFloat(document.getElementById('deRoughTotalLen').value) || 60;

  if (tons <= 0) return { error: true, message: 'Enter system tonnage to get started.' };

  var totalCFM = Math.round(tons * cfmPerTon);
  var profile = DE.PROFILES[profileId] || DE.PROFILES.plenum_flex;
  var plenum = DE.PLENUM_TYPES[plenumType] || DE.PLENUM_TYPES.straight;

  // Estimate branch count from CFM (rule of thumb: ~120-180 CFM per branch for flex)
  var cfmPerBranch = profile.branchMat === 'flex' ? 140 : 160;
  var estBranches = Math.max(2, Math.round(totalCFM / cfmPerBranch));

  // Size trunk
  var trunkSizing = deSize(totalCFM, profile.trunkMat, profile.targetFR);
  var trunkRect = profile.trunkShape === 'rect' ? deRectEquiv(trunkSizing.size) : null;

  // Size average branch
  var branchCFM = Math.round(totalCFM / estBranches);
  var branchSizing = deSize(branchCFM, profile.branchMat, profile.targetFR);

  // Total equivalent length estimate
  var supplyTEL = plenum.eqLen + approxLen + (profile.elbowsPer * profile.elbowEQ * estBranches / estBranches);
  if (profile.trunkLen) supplyTEL += profile.trunkLen + (profile.trunkElbows || 0) * (profile.trunkElbowEQ || 25);
  var returnTEL = supplyTEL * 0.7; // returns are typically shorter
  var totalTEL = supplyTEL + returnTEL;

  // Static estimate
  var frRate = Math.max(trunkSizing.friction, branchSizing.friction, profile.targetFR);
  var staticEst = deEstimateStatic(totalTEL, frRate, 0.10, 0.20, 0.05);
  
  // Apply zoning multiplier
  var zoneMult = DE.ZONING[zoning] ? DE.ZONING[zoning].staticMult : 1.0;
  var zonedStatic = { ductPD: staticEst.ductPD * zoneMult, filterPD: staticEst.filterPD, coilPD: staticEst.coilPD, total: staticEst.total * zoneMult };
  
  var risk = deRiskLevel(zonedStatic.total, zoning);

  // Material estimate (rough)
  var flexBags = profile.branchMat === 'flex' ? Math.ceil(estBranches * profile.avgBranchLen / 25) : 0;
  var metalSections = 0;
  if (profile.trunkMat === 'metal') {
    metalSections = Math.ceil((profile.trunkLen || 8) / 5); // 5ft sections
  }
  if (profile.branchMat === 'metal') {
    metalSections += Math.ceil(estBranches * profile.avgBranchLen / 5);
  }

  return {
    mode: 'rough',
    totalCFM: totalCFM,
    tons: tons,
    profile: profile,
    plenum: plenum,
    plenumType: plenumType,
    zoning: zoning,
    smallZone: smallZone,
    estBranches: estBranches,
    branchCFM: branchCFM,
    trunk: { sizing: trunkSizing, rect: trunkRect },
    branch: { sizing: branchSizing },
    tel: { supply: Math.round(supplyTEL), return: Math.round(returnTEL), total: Math.round(totalTEL) },
    static: zonedStatic,
    risk: risk,
    material: { flexBags: flexBags, metalSections: metalSections },
    frRate: frRate
  };
}


// ===========================
// MODE 2: DETAILED ESTIMATOR
// ===========================

function deDetailedEstimate() {
  // Read system inputs
  var totalCFM = 0;
  var rooms = [];
  if (typeof getRoomsList === 'function') rooms = getRoomsList();
  rooms.forEach(function(r) { totalCFM += r.cfm; });

  // Fallback: manual CFM entry
  var manualCFM = parseFloat(document.getElementById('deDetailCFM').value) || 0;
  if (totalCFM === 0 && manualCFM > 0) totalCFM = manualCFM;
  if (totalCFM <= 0) return { error: true, message: 'Add rooms in the Rooms tab, or enter total system CFM above.' };

  var strategy = document.getElementById('deDetailStrategy').value || 'metal_flex';
  var trunkShape = document.getElementById('deDetailTrunkShape').value || 'rect';
  var plenumType = document.getElementById('deDetailPlenum').value || 'straight';
  var plenumMat = document.getElementById('deDetailPlenumMat').value || 'metal';
  var zoning = document.getElementById('deDetailZoning').value || 'none';
  var smallZone = document.getElementById('deDetailSmallZone') ? document.getElementById('deDetailSmallZone').value : 'no';
  
  // Trunk inputs
  var trunkLen = parseFloat(document.getElementById('deDetailTrunkLen').value) || 15;
  var trunkElbows90 = parseInt(document.getElementById('deDetailTrunk90s').value) || 0;
  var trunkElbows90Vane = parseInt(document.getElementById('deDetailTrunk90sVane').value) || 0;
  var trunkTrans = parseInt(document.getElementById('deDetailTrunkTrans').value) || 0;

  // Branch inputs
  var numBranches = parseInt(document.getElementById('deDetailBranches').value) || 0;
  if (numBranches === 0 && rooms.length > 0) numBranches = rooms.length;
  if (numBranches === 0) numBranches = Math.max(2, Math.round(totalCFM / 140));
  var avgBranchLen = parseFloat(document.getElementById('deDetailBranchLen').value) || 20;
  var branchElbows = parseFloat(document.getElementById('deDetailBranchElbows').value) || 1;

  // Determine materials from strategy
  var trunkMat = 'metal', branchMat = 'flex';
  if (strategy === 'all_flex') { trunkMat = 'flex'; branchMat = 'flex'; }
  else if (strategy === 'all_metal') { trunkMat = 'metal'; branchMat = 'metal'; }
  else if (strategy === 'rect_round') { trunkMat = 'metal'; branchMat = 'metal'; }
  // else metal_flex is default

  if (plenumMat === 'ductboard') trunkMat = 'ductboard';

  var plenum = DE.PLENUM_TYPES[plenumType] || DE.PLENUM_TYPES.straight;

  // Size trunk
  var trunkSizing = deSize(totalCFM, trunkMat, 0.08);
  var trunkRect = (trunkShape === 'rect') ? deRectEquiv(trunkSizing.size) : null;

  // Size branches
  var branchCFM = Math.round(totalCFM / numBranches);
  var branchSizing = deSize(branchCFM, branchMat, 0.08);

  // Per-room sizing (if rooms available)
  var roomSizes = [];
  if (rooms.length > 0) {
    // Enrich with types
    if (typeof roomCfmData !== 'undefined') {
      rooms = rooms.map(function(rm, i) {
        var data = roomCfmData[i] || {};
        return { name: rm.name, cfm: rm.cfm, type: data.type || 'bedroom' };
      });
    }
    rooms.forEach(function(rm) {
      var sz = deSize(rm.cfm, branchMat, 0.08);
      roomSizes.push({ name: rm.name, cfm: rm.cfm, type: rm.type || 'bedroom', size: sz.size, vel: sz.velocity, fr: sz.friction });
    });
  }

  // Calculate TEL
  // Supply side: plenum + trunk + trunk fittings + (avg branch + branch fittings)
  var trunkEQ = trunkLen;
  trunkEQ += trunkElbows90 * 55;      // 90° elbow no vanes
  trunkEQ += trunkElbows90Vane * 15;   // 90° with turning vanes
  trunkEQ += trunkTrans * 5;           // transitions
  var supplyTEL = plenum.eqLen + trunkEQ + avgBranchLen + (branchElbows * 15);
  var returnTEL = supplyTEL * 0.7;
  var totalTEL = supplyTEL + returnTEL;

  // Static estimate
  var frRate = 0.08;
  var staticEst = deEstimateStatic(totalTEL, frRate, 0.10, 0.20, 0.05);
  var zoneMult = DE.ZONING[zoning] ? DE.ZONING[zoning].staticMult : 1.0;
  var zonedStatic = { ductPD: staticEst.ductPD * zoneMult, filterPD: staticEst.filterPD, coilPD: staticEst.coilPD, total: (staticEst.ductPD * zoneMult) + staticEst.filterPD + staticEst.coilPD + 0.05 };

  var risk = deRiskLevel(zonedStatic.total, zoning);

  // Material estimate
  var flexBags = branchMat === 'flex' ? Math.ceil(numBranches * avgBranchLen / 25) : 0;
  var metalSections = 0;
  if (trunkMat === 'metal') metalSections += Math.ceil(trunkLen / 5);
  if (branchMat === 'metal') metalSections += Math.ceil(numBranches * avgBranchLen / 5);
  var ductboardSheets = 0;
  if (trunkMat === 'ductboard' || plenumMat === 'ductboard') {
    ductboardSheets = Math.ceil(trunkLen / 6); // ~6ft per 4x8 sheet
  }

  return {
    mode: 'detailed',
    totalCFM: totalCFM,
    rooms: rooms,
    roomSizes: roomSizes,
    numBranches: numBranches,
    strategy: strategy,
    trunkShape: trunkShape,
    trunkMat: trunkMat,
    branchMat: branchMat,
    plenum: plenum,
    plenumType: plenumType,
    plenumMat: plenumMat,
    zoning: zoning,
    smallZone: smallZone,
    trunk: { sizing: trunkSizing, rect: trunkRect, len: trunkLen, elbows90: trunkElbows90, elbows90Vane: trunkElbows90Vane, trans: trunkTrans, eq: trunkEQ },
    branch: { sizing: branchSizing, cfm: branchCFM, len: avgBranchLen, elbows: branchElbows },
    tel: { supply: Math.round(supplyTEL), return: Math.round(returnTEL), total: Math.round(totalTEL) },
    static: zonedStatic,
    risk: risk,
    material: { flexBags: flexBags, metalSections: metalSections, ductboardSheets: ductboardSheets },
    frRate: frRate
  };
}


// ===========================
// RENDERING
// ===========================

function deRenderResults(result) {
  var el = document.getElementById('deResults');
  if (!el) return;

  if (result.error) {
    el.innerHTML = '<div class="info-note" style="margin-top:8px;border-color:var(--amber)">' +
      '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" style="flex-shrink:0;color:var(--amber)"><circle cx="12" cy="12" r="10"/><path d="M12 16v-4M12 8h.01"/></svg>' +
      '<span style="font-size:12px">' + result.message + '</span></div>';
    return;
  }

  var h = '';

  // === ZONING BANNER (always first if zoned) ===
  if (result.zoning !== 'none') {
    var isSmall = result.zoning === 'three_plus' && result.smallZone === 'yes';
    var bannerBg = isSmall ? '#8b1a1a' : '#7a5c00';
    var bannerIcon = isSmall ? '\u26D4' : '\u26A0\uFE0F';
    h += '<div style="background:' + bannerBg + ';color:#fff;border-radius:10px;padding:12px 14px;margin-bottom:12px;font-size:11px;line-height:1.5">';
    h += '<div style="font-size:13px;font-weight:700;margin-bottom:4px">' + bannerIcon + ' ZONED SYSTEM</div>';
    if (isSmall) {
      h += '<div style="margin-bottom:6px"><strong>SMALL ZONE PRESENT</strong> — High risk of excessive static and comfort issues when that zone runs alone. Consider bypass or other excess air strategies per Manual Zr, EWC, and Honeywell zoning guidance.</div>';
    }
    h += '<div>This tool provides only rough duct and static guidance. Actual performance depends on zone design, control strategy, and bypass/relief. Use <strong>ACCA Manual Zr</strong> and manufacturer zoning guides (<strong>EWC</strong>, <strong>Honeywell/Resideo</strong>) for proper zoning design and adjustment.</div>';
    h += '</div>';
  }

  // === SUMMARY HEADER ===
  h += '<div style="background:linear-gradient(135deg,var(--accent),#a37524);border-radius:12px;padding:14px 16px;margin-bottom:12px;color:#fff">';
  h += '<div style="font-size:15px;font-weight:700;margin-bottom:4px">' + (result.mode === 'rough' ? 'Rough Estimate' : 'Duct Estimate') + '</div>';
  h += '<div style="display:flex;flex-wrap:wrap;gap:10px;font-size:11px;opacity:0.92">';
  h += '<span>' + result.totalCFM + ' CFM</span>';
  if (result.tons) h += '<span>' + result.tons + ' ton</span>';
  if (result.profile) h += '<span>' + result.profile.label + '</span>';
  if (result.numBranches) h += '<span>' + result.numBranches + ' branches</span>';
  h += '</div></div>';

  // === STATIC PRESSURE RISK ===
  h += '<div class="panel" style="margin-bottom:10px;border-left:4px solid ' + result.risk.color + '">';
  h += '<div style="display:flex;justify-content:space-between;align-items:center;margin-bottom:6px">';
  h += '<div style="font-size:13px;font-weight:700;color:var(--text)">Static Pressure Risk</div>';
  h += '<div style="font-size:13px;font-weight:800;color:' + result.risk.color + ';font-family:\'DM Mono\',monospace">' + result.risk.label + '</div>';
  h += '</div>';

  // Static breakdown
  h += '<div style="display:flex;gap:6px;flex-wrap:wrap;margin-bottom:8px">';
  h += deStatChip('Duct PD', result.static.ductPD.toFixed(2) + '" WC');
  h += deStatChip('Filter', result.static.filterPD.toFixed(2) + '" WC');
  h += deStatChip('Coil', result.static.coilPD.toFixed(2) + '" WC');
  h += deStatChip('Total', result.static.total.toFixed(2) + '" WC', result.risk.color);
  h += '</div>';

  h += '<div style="font-size:10px;color:var(--text-3);line-height:1.4">' + result.risk.desc + '</div>';

  if (result.zoning !== 'none') {
    h += '<div style="font-size:10px;color:var(--amber);margin-top:4px;font-weight:600">Zoning increases worst-case static when fewer zones call. This estimate includes a ' + Math.round((DE.ZONING[result.zoning].staticMult - 1) * 100) + '% zoning safety factor on duct pressure drop.</div>';
  }
  h += '</div>';

  // === TEL BREAKDOWN ===
  h += '<div class="panel" style="margin-bottom:10px">';
  h += '<div style="font-size:12px;font-weight:700;color:var(--text);margin-bottom:6px">Equivalent Length</div>';
  h += '<div style="display:flex;gap:6px;flex-wrap:wrap">';
  h += deStatChip('Supply TEL', result.tel.supply + ' ft');
  h += deStatChip('Return TEL', result.tel.return + ' ft');
  h += deStatChip('Total TEL', result.tel.total + ' ft', 'var(--accent)');
  h += '</div>';
  if (result.plenumType) {
    var pl = DE.PLENUM_TYPES[result.plenumType];
    if (pl) {
      h += '<div style="font-size:10px;color:var(--text-3);margin-top:6px">' + pl.label + ': ' + pl.eqLen + ' ft EQ — ' + pl.teach + '</div>';
    }
  }
  h += '</div>';

  // === TRUNK SIZING ===
  h += '<div class="panel" style="margin-bottom:10px;border-left:3px solid var(--accent)">';
  h += '<div style="font-size:12px;font-weight:700;color:var(--text);margin-bottom:6px">Trunk</div>';
  h += '<div style="display:flex;gap:6px;flex-wrap:wrap;margin-bottom:6px">';
  h += deStatChip('Round', result.trunk.sizing.size + '"', 'var(--accent)');
  if (result.trunk.rect) h += deStatChip('Rect Equiv', result.trunk.rect, 'var(--accent)');
  h += deStatChip('Velocity', result.trunk.sizing.velocity + ' FPM');
  h += deStatChip('FR', result.trunk.sizing.friction.toFixed(3) + ' IWC/100ft');
  h += '</div>';
  var trunkMatLabel = result.trunkMat === 'ductboard' ? 'Ductboard' : (result.trunkMat === 'flex' ? 'Flex' : 'Metal');
  h += '<div style="font-size:10px;color:var(--text-3)">Material: ' + trunkMatLabel + (result.trunkShape === 'rect' ? ' (rectangular)' : ' (round)') + '</div>';
  h += '</div>';

  // === BRANCH SIZING ===
  h += '<div class="panel" style="margin-bottom:10px;border-left:3px solid var(--accent)">';
  h += '<div style="font-size:12px;font-weight:700;color:var(--text);margin-bottom:6px">Typical Branch</div>';
  h += '<div style="display:flex;gap:6px;flex-wrap:wrap;margin-bottom:6px">';
  h += deStatChip('Size', result.branch.sizing.size + '"', 'var(--accent)');
  h += deStatChip('CFM/branch', (result.branch.cfm || result.branchCFM) + '');
  h += deStatChip('Velocity', result.branch.sizing.velocity + ' FPM');
  h += deStatChip('FR', result.branch.sizing.friction.toFixed(3));
  h += '</div>';
  var branchMatLabel = result.branchMat === 'flex' ? 'Flex' : 'Metal';
  h += '<div style="font-size:10px;color:var(--text-3)">Material: ' + branchMatLabel;
  if (result.branchMat === 'flex') h += ' (10% compression assumed — pull tight!)';
  h += '</div></div>';

  // === PER-ROOM TABLE (detailed mode only) ===
  if (result.roomSizes && result.roomSizes.length > 0) {
    h += '<div class="panel" style="margin-bottom:10px">';
    h += '<div style="font-size:12px;font-weight:700;color:var(--text);margin-bottom:6px">Per-Room Duct Sizes</div>';
    h += '<div style="overflow-x:auto"><table style="width:100%;border-collapse:collapse;font-size:10px">';
    h += '<thead><tr style="background:var(--accent);color:#fff;text-align:left">';
    h += '<th style="padding:5px 6px;border-radius:4px 0 0 0">Room</th>';
    h += '<th style="padding:5px 6px">CFM</th>';
    h += '<th style="padding:5px 6px">Duct</th>';
    h += '<th style="padding:5px 6px">Vel</th>';
    h += '<th style="padding:5px 6px;border-radius:0 4px 0 0">FR</th>';
    h += '</tr></thead><tbody>';
    result.roomSizes.forEach(function(rm, ri) {
      var bg = ri % 2 === 1 ? 'background:var(--surface-2)' : '';
      var frColor = rm.fr > 0.10 ? 'var(--red)' : rm.fr > 0.08 ? 'var(--amber)' : 'var(--green)';
      h += '<tr style="' + bg + '">';
      h += '<td style="padding:5px 6px;font-weight:600">' + rm.name + '</td>';
      h += '<td style="padding:5px 6px;font-family:\'DM Mono\',monospace">' + rm.cfm + '</td>';
      h += '<td style="padding:5px 6px;font-family:\'DM Mono\',monospace;font-weight:700;color:var(--accent)">' + rm.size + '"</td>';
      h += '<td style="padding:5px 6px;font-family:\'DM Mono\',monospace">' + rm.vel + '</td>';
      h += '<td style="padding:5px 6px;font-family:\'DM Mono\',monospace;color:' + frColor + '">' + rm.fr.toFixed(3) + '</td>';
      h += '</tr>';
    });
    h += '</tbody></table></div></div>';
  }

  // === MATERIAL ESTIMATE ===
  h += '<div class="panel" style="margin-bottom:10px">';
  h += '<div style="font-size:12px;font-weight:700;color:var(--text);margin-bottom:6px">Rough Material Estimate</div>';
  h += '<div style="display:flex;gap:6px;flex-wrap:wrap">';
  if (result.material.flexBags > 0) h += deStatChip('Flex', result.material.flexBags + ' bag' + (result.material.flexBags > 1 ? 's' : '') + ' (25ft)');
  if (result.material.metalSections > 0) h += deStatChip('Metal', result.material.metalSections + ' section' + (result.material.metalSections > 1 ? 's' : '') + ' (5ft)');
  if (result.material.ductboardSheets > 0) h += deStatChip('Ductboard', result.material.ductboardSheets + ' sheet' + (result.material.ductboardSheets > 1 ? 's' : '') + ' (4x8)');
  h += '</div>';
  h += '<div style="font-size:9px;color:var(--text-3);margin-top:4px">Always round up. Flex in 25ft bags, metal in 5ft sections, ductboard in 4x8 sheets.</div>';
  h += '</div>';

  // === ZONING GUIDANCE (if zoned) ===
  if (result.zoning !== 'none') {
    h += deRenderZoningGuidance(result);
  }

  // === DISCLAIMER ===
  h += '<div class="info-note" style="margin-top:10px">';
  h += '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" style="flex-shrink:0"><circle cx="12" cy="12" r="10"/><path d="M12 16v-4M12 8h.01"/></svg>';
  h += '<span style="font-size:10px">This is an estimator aligned with ACCA Manual D principles, not a full Manual D calculation. Actual duct design must account for equipment location, room positions, attic/crawl constraints, and measured static pressure. Use the System Design wizard for a production layout.</span>';
  h += '</div>';

  el.innerHTML = h;
  DE.lastResult = result;
}

// Stat chip helper
function deStatChip(label, value, accent) {
  var col = accent || 'var(--text)';
  return '<div style="background:var(--surface-2);border-radius:8px;padding:5px 10px;display:inline-flex;flex-direction:column;align-items:flex-start">' +
    '<div style="font-size:8px;color:var(--text-3);text-transform:uppercase;letter-spacing:0.3px">' + label + '</div>' +
    '<div style="font-size:13px;font-weight:700;color:' + col + ';font-family:\'DM Mono\',monospace;white-space:nowrap">' + value + '</div></div>';
}


// ===========================
// ZONING GUIDANCE RENDERER
// ===========================

function deRenderZoningGuidance(result) {
  var h = '';
  h += '<div class="panel" style="margin-bottom:10px;border-left:3px solid #5b8def">';
  h += '<div style="font-size:12px;font-weight:700;color:var(--text);margin-bottom:8px">\u26A0\uFE0F Zoning Guidance</div>';

  if (result.zoning === 'two') {
    h += '<div style="font-size:11px;color:var(--text-2);line-height:1.5;margin-bottom:8px">';
    h += '<strong>2-Zone System Considerations:</strong><br>';
    h += '\u2022 Each zone handles roughly half the total load when calling alone.<br>';
    h += '\u2022 When only one zone calls, the blower pushes full CFM into half the ductwork — expect higher static pressure.<br>';
    h += '\u2022 Ensure the larger zone can handle at least 60-70% of system CFM safely.<br>';
    h += '\u2022 Consider a static-pressure-controlled bypass damper (CPRD/MARD) if static exceeds 0.5" WC in single-zone operation.';
    h += '</div>';
  }

  if (result.zoning === 'three_plus') {
    h += '<div style="font-size:11px;color:var(--text-2);line-height:1.5;margin-bottom:8px">';
    h += '<strong>3+ Zone System Considerations:</strong><br>';
    h += '\u2022 More zones = more potential for high static when only 1-2 zones call.<br>';
    h += '\u2022 Worst-case scenario: smallest zone calling alone while system delivers full CFM.<br>';
    h += '</div>';

    if (result.smallZone === 'yes') {
      h += '<div style="background:#3a1818;color:#ffb4b4;border-radius:8px;padding:10px;margin-bottom:8px;font-size:11px;line-height:1.5">';
      h += '<strong>\u26D4 Small Zone Detected — Bypass Likely Needed</strong><br>';
      h += '\u2022 Consider bypass when the smallest zone cannot safely handle ~60% of system CFM.<br>';
      h += '\u2022 Bypass sizing should be based on the difference between equipment CFM and smallest-zone CFM under worst-case single-zone operation.<br>';
      h += '\u2022 Options: bypass to return duct or dump zone — keep mixing distance in mind to avoid cold air complaints.<br>';
      h += '\u2022 Static-pressure-controlled bypass dampers (EWC EBD/PRD, Honeywell/Resideo CPRD/MARD) should be adjusted with the smallest zone calling alone.';
      h += '</div>';
    } else {
      h += '<div style="font-size:11px;color:var(--text-2);line-height:1.5;margin-bottom:8px">';
      h += '\u2022 No very small zone — lower bypass risk, but still monitor static when fewer zones call.<br>';
      h += '\u2022 A bypass damper or variable-speed blower can help manage excess pressure.';
      h += '</div>';
    }
  }

  // Reference section
  h += '<div style="background:var(--surface-2);border-radius:8px;padding:8px 10px;font-size:10px;color:var(--text-3);line-height:1.4">';
  h += '<strong style="color:var(--text-2)">References for Proper Zoning Design:</strong><br>';
  h += '\u2022 <strong>ACCA Manual Zr</strong> — Residential zoning system design procedures, bypass sizing, and zone damper selection.<br>';
  h += '\u2022 <strong>EWC Controls</strong> — Zoning panel setup, bypass factor, worst-case smallest-zone operation, EBD/PRD damper guides.<br>';
  h += '\u2022 <strong>Honeywell/Resideo</strong> — Static bypass damper usage (CPRD/MARD), adjustment procedures with smallest zone calling.<br>';
  h += '<em>This tool does not replace these procedures. Use them for final design and adjustment.</em>';
  h += '</div>';

  h += '</div>';
  return h;
}


// ===========================
// UI TAB SWITCHING
// ===========================

function deSetMode(mode) {
  DE.mode = mode;
  var roughTab = document.getElementById('deTabRough');
  var detailTab = document.getElementById('deTabDetail');
  var roughPanel = document.getElementById('deRoughPanel');
  var detailPanel = document.getElementById('deDetailPanel');

  // Style active/inactive tabs
  if (roughTab) {
    roughTab.style.background = mode === 'rough' ? '' : 'var(--surface-3)';
    roughTab.style.color = mode === 'rough' ? '' : 'var(--text-2)';
    roughTab.classList.toggle('active', mode === 'rough');
  }
  if (detailTab) {
    detailTab.style.background = mode === 'detailed' ? '' : 'var(--surface-3)';
    detailTab.style.color = mode === 'detailed' ? '' : 'var(--text-2)';
    detailTab.classList.toggle('active', mode === 'detailed');
  }
  if (roughPanel) roughPanel.style.display = mode === 'rough' ? '' : 'none';
  if (detailPanel) detailPanel.style.display = mode === 'detailed' ? '' : 'none';
  // Clear results
  var resEl = document.getElementById('deResults');
  if (resEl) resEl.innerHTML = '';
}

// Zoning small-zone question visibility
function deUpdateZoningUI(selectEl, smallZoneId) {
  var val = selectEl ? selectEl.value : 'none';
  var szEl = document.getElementById(smallZoneId);
  if (szEl) {
    szEl.closest('.de-small-zone-wrap').style.display = val === 'three_plus' ? '' : 'none';
  }
}


// ===========================
// EVENT DELEGATION
// ===========================

document.addEventListener('click', function(e) {
  var t = e.target;

  // Tab switching
  if (t.closest('#deTabRough')) { deSetMode('rough'); return; }
  if (t.closest('#deTabDetail')) { deSetMode('detailed'); return; }

  // Run estimation
  if (t.closest('#deRunBtn')) {
    var result;
    if (DE.mode === 'rough') {
      result = deRoughEstimate();
    } else {
      result = deDetailedEstimate();
    }
    deRenderResults(result);
    var resEl = document.getElementById('deResults');
    if (resEl) {
      setTimeout(function() { resEl.scrollIntoView({ behavior: 'smooth', block: 'start' }); }, 100);
    }
    return;
  }
});

document.addEventListener('change', function(e) {
  var t = e.target;
  // Zoning dropdown changes
  if (t.id === 'deRoughZoning') deUpdateZoningUI(t, 'deRoughSmallZone');
  if (t.id === 'deDetailZoning') deUpdateZoningUI(t, 'deDetailSmallZone');

  // Profile change — update description
  if (t.id === 'deRoughProfile') {
    var prof = DE.PROFILES[t.value];
    var descEl = document.getElementById('deRoughProfileDesc');
    if (descEl && prof) descEl.textContent = prof.desc;
  }
});
