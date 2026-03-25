// ===== ROUGH DUCT ESTIMATOR =====
// Educational tool: reads actual room data + collar data and suggests a complete
// conceptual duct layout with teaching explanations for beginner techs.
// Different from rough-layout.js (generic CFM splitter). This one uses YOUR rooms.

var DE = {
  lastResult: null
};

// ---- Room clustering logic ----
// Groups rooms into intelligent clusters based on room type
function deClusterRooms(rooms) {
  // Define cluster groups by room type
  var clusterDefs = [
    { id: 'master', label: 'Master Suite', types: ['master_bed', 'master_bath'], minSupply: 2, minReturn: 1,
      teach: 'Master bedrooms are usually the largest bedroom and farthest from the unit. They need more airflow and their own dedicated branch to avoid starving other rooms.' },
    { id: 'living', label: 'Living / Kitchen Area', types: ['living', 'great_room', 'kitchen', 'dining'], minSupply: 2, minReturn: 1,
      teach: 'Living areas and kitchens are high-traffic, open spaces with more heat gain (windows, appliances, people). They get the most CFM and often need multiple supply runs.' },
    { id: 'guest', label: 'Guest Bedrooms', types: ['bedroom', 'office', 'bonus'], minSupply: 1, minReturn: 1,
      teach: 'Guest bedrooms and offices are typically smaller and closer together. They can often share a common branch off the trunk, with individual takeoffs to each room.' },
    { id: 'utility', label: 'Utility / Other', types: ['bathroom', 'laundry', 'hallway', 'garage', 'closet'], minSupply: 1, minReturn: 0,
      teach: 'Bathrooms, laundry rooms, and hallways need less airflow. They are usually served by short takeoffs near the trunk — keep duct runs short to minimize pressure loss.' }
  ];

  var clusters = [];
  var assigned = {};

  clusterDefs.forEach(function(def) {
    var clusterRooms = [];
    rooms.forEach(function(rm, idx) {
      if (assigned[idx]) return;
      if (def.types.indexOf(rm.type) !== -1) {
        clusterRooms.push({ idx: idx, name: rm.name, cfm: rm.cfm, type: rm.type });
        assigned[idx] = true;
      }
    });
    if (clusterRooms.length > 0) {
      var totalCfm = 0;
      clusterRooms.forEach(function(r) { totalCfm += r.cfm; });
      clusters.push({
        id: def.id,
        label: def.label,
        rooms: clusterRooms,
        totalCfm: totalCfm,
        minSupply: def.minSupply,
        minReturn: def.minReturn,
        teach: def.teach
      });
    }
  });

  // Catch any unassigned rooms
  var unassigned = [];
  rooms.forEach(function(rm, idx) {
    if (!assigned[idx]) {
      unassigned.push({ idx: idx, name: rm.name, cfm: rm.cfm, type: rm.type });
    }
  });
  if (unassigned.length > 0) {
    var uCfm = 0;
    unassigned.forEach(function(r) { uCfm += r.cfm; });
    clusters.push({
      id: 'other',
      label: 'Other Rooms',
      rooms: unassigned,
      totalCfm: uCfm,
      minSupply: 1,
      minReturn: 0,
      teach: 'These rooms did not fit a standard cluster. They will be served by the nearest available branch.'
    });
  }

  return clusters;
}

// ---- Assign collars to clusters ----
function deAssignCollars(clusters, supplyCollars, returnCollars) {
  var totalCfm = 0;
  clusters.forEach(function(c) { totalCfm += c.totalCfm; });
  if (totalCfm <= 0) totalCfm = 1;

  var numSupply = supplyCollars.length;
  var numReturn = returnCollars.length;

  // Distribute supply collars proportionally by CFM share
  // Every cluster with rooms gets at least 1 collar
  var supplyAssign = [];
  var remainingCollars = numSupply;

  // First: give each cluster with rooms at least 1 collar
  clusters.forEach(function(c) {
    if (c.rooms.length > 0 && remainingCollars > 0) {
      supplyAssign.push(1);
      remainingCollars--;
    } else {
      supplyAssign.push(0);
    }
  });

  // Second: distribute remaining collars to clusters with the highest CFM-per-collar
  while (remainingCollars > 0) {
    var bestIdx = -1;
    var bestRatio = 0;
    clusters.forEach(function(c, i) {
      if (supplyAssign[i] === 0) return;
      var ratio = c.totalCfm / supplyAssign[i];
      if (ratio > bestRatio) { bestRatio = ratio; bestIdx = i; }
    });
    if (bestIdx < 0) break;
    supplyAssign[bestIdx]++;
    remainingCollars--;
  }

  // Return collars: if only 1, it goes to the largest area (living/great room)
  var returnAssign = clusters.map(function() { return 0; });

  if (numReturn === 1) {
    // Single return — find the living area cluster, or the largest cluster
    var livingIdx = -1;
    var maxCfmIdx = 0;
    clusters.forEach(function(c, i) {
      if (c.id === 'living') livingIdx = i;
      if (c.totalCfm > clusters[maxCfmIdx].totalCfm) maxCfmIdx = i;
    });
    returnAssign[livingIdx >= 0 ? livingIdx : maxCfmIdx] = 1;
  } else if (numReturn > 1) {
    // Multiple returns — distribute proportionally
    var retRemaining = numReturn;
    clusters.forEach(function(c, i) {
      var min = Math.min(c.minReturn, retRemaining);
      returnAssign[i] = min;
      retRemaining -= min;
    });
    if (retRemaining > 0) {
      var retScores = clusters.map(function(c, i) {
        return { idx: i, cfmPerRet: c.totalCfm / Math.max(1, returnAssign[i] || 0.01) };
      });
      retScores.sort(function(a, b) { return b.cfmPerRet - a.cfmPerRet; });
      while (retRemaining > 0) {
        returnAssign[retScores[0].idx]++;
        retScores[0].cfmPerRet = clusters[retScores[0].idx].totalCfm / returnAssign[retScores[0].idx];
        retScores.sort(function(a, b) { return b.cfmPerRet - a.cfmPerRet; });
        retRemaining--;
      }
    }
  }

  // Build enriched cluster data with collar assignments
  return clusters.map(function(c, i) {
    var numSup = supplyAssign[i];
    var numRet = returnAssign[i];
    // Pick collar sizes from the actual collar arrays
    var supCollarSizes = [];
    var collarOffset = 0;
    for (var ci = 0; ci < i; ci++) collarOffset += supplyAssign[ci];
    for (var s = 0; s < numSup; s++) {
      var idx = collarOffset + s;
      if (idx < supplyCollars.length) {
        supCollarSizes.push(supplyCollars[idx]);
      } else {
        // Fallback: use the most common collar size
        supCollarSizes.push(supplyCollars[supplyCollars.length - 1] || { size: '10', type: 'tab' });
      }
    }

    return {
      id: c.id,
      label: c.label,
      rooms: c.rooms,
      totalCfm: c.totalCfm,
      teach: c.teach,
      supplyCollars: numSup,
      supplyCollarSizes: supCollarSizes,
      returnCollars: numRet
    };
  });
}

// ---- Size ducts for a cluster ----
function deSizeCluster(cluster) {
  var totalCfm = cluster.totalCfm;
  var numCollars = cluster.supplyCollars;

  // If no collars assigned, these rooms will be served from the nearest trunk
  if (numCollars <= 0) {
    return [{
      collarIndex: 0,
      collarSize: 0,
      branchCfm: totalCfm,
      trunkSize: 0,
      trunkVel: 0,
      trunkFR: 0,
      noCollar: true,
      rooms: cluster.rooms,
      takeoffs: cluster.rooms.map(function(rm) {
        var takeoffSize = deFindDuctSize(rm.cfm, 'flex');
        var bootSize = deRecommendBoot(takeoffSize.size, rm.cfm);
        return {
          room: rm.name, roomCfm: rm.cfm,
          takeoffSize: takeoffSize.size, takeoffVel: takeoffSize.velocity, takeoffFR: takeoffSize.friction,
          fittingType: 'takeoff from trunk', fittingEQ: 15,
          bootSize: bootSize, trunkBefore: 0, trunkAfter: null, trunkAfterCfm: 0
        };
      })
    }];
  }

  // CFM per collar (trunk branch)
  var cfmPerCollar = Math.round(totalCfm / numCollars);

  var branches = [];

  for (var c = 0; c < numCollars; c++) {
    var collarSize = parseInt(cluster.supplyCollarSizes[c] ? cluster.supplyCollarSizes[c].size : 10);
    var branchCfm = cfmPerCollar;
    // Adjust last branch to absorb rounding
    if (c === numCollars - 1) {
      branchCfm = totalCfm - (cfmPerCollar * (numCollars - 1));
    }

    // Determine rooms served by this branch
    var roomsPerCollar = Math.ceil(cluster.rooms.length / numCollars);
    var startIdx = c * roomsPerCollar;
    var endIdx = Math.min(startIdx + roomsPerCollar, cluster.rooms.length);
    if (c === numCollars - 1) endIdx = cluster.rooms.length; // last collar gets remainder
    var branchRooms = cluster.rooms.slice(startIdx, endIdx);

    // Size the trunk/branch from collar
    var trunkSize = deFindDuctSize(branchCfm, 'metal');

    // Build the run: collar → trunk → takeoffs to rooms
    var takeoffs = [];
    var remainingCfm = branchCfm;
    var currentSize = trunkSize.size;

    branchRooms.forEach(function(rm, ri) {
      var takeoffSize = deFindDuctSize(rm.cfm, 'flex');
      var fittingType = 'straight-through wye';
      var fittingEQ = 15;

      // If this is the last room, it's the end of the run (no split needed)
      if (ri === branchRooms.length - 1) {
        fittingType = 'end cap / direct';
        fittingEQ = 0;
      }

      // After this takeoff, remaining CFM decreases
      var afterCfm = remainingCfm - rm.cfm;
      var afterSize = afterCfm > 0 ? deFindDuctSize(afterCfm, 'metal') : null;

      // Boot recommendation
      var bootSize = deRecommendBoot(takeoffSize.size, rm.cfm);

      takeoffs.push({
        room: rm.name,
        roomCfm: rm.cfm,
        takeoffSize: takeoffSize.size,
        takeoffVel: takeoffSize.velocity,
        takeoffFR: takeoffSize.friction,
        fittingType: fittingType,
        fittingEQ: fittingEQ,
        bootSize: bootSize,
        trunkBefore: currentSize,
        trunkAfter: afterSize ? afterSize.size : null,
        trunkAfterCfm: afterCfm
      });

      remainingCfm = afterCfm;
      if (afterSize && afterSize.size < currentSize) {
        currentSize = afterSize.size; // Reduce trunk after takeoff
      }
    });

    branches.push({
      collarIndex: c + 1,
      collarSize: collarSize,
      branchCfm: branchCfm,
      trunkSize: trunkSize.size,
      trunkVel: trunkSize.velocity,
      trunkFR: trunkSize.friction,
      rooms: branchRooms,
      takeoffs: takeoffs
    });
  }

  return branches;
}

// ---- Find best duct size for given CFM ----
function deFindDuctSize(cfm, material) {
  var candidates = [4, 5, 6, 7, 8, 9, 10, 12, 14, 16, 18, 20, 22, 24];
  var best = null;
  var bestScore = Infinity;

  for (var i = 0; i < candidates.length; i++) {
    var d = candidates[i];
    var A = Math.PI * Math.pow(d / 12 / 2, 2);
    var vel = cfm / A;
    var fr = 0;

    if (typeof frictionLoss === 'function') {
      fr = frictionLoss(d, cfm, material, false);
    }

    // Apply flex factor for flex duct (10% compression default)
    if (material === 'flex' && typeof flexFactor === 'function') {
      fr = fr * flexFactor(10);
    }

    // Score the candidate: want FR ≤ 0.08 and velocity 300-900
    var score = 0;
    if (fr > 0.08) score += (fr - 0.08) * 500; // penalize high friction
    if (vel > 900) score += (vel - 900) * 0.1;  // penalize high velocity
    if (vel < 200) score += (200 - vel) * 0.5;  // penalize very low velocity
    score += Math.abs(fr - 0.06) * 100; // prefer FR around 0.06

    // For flex, add slight upsize preference
    if (material === 'flex' && fr > 0.06) score += 5;

    if (fr <= 0.08 && vel <= 900) {
      // Acceptable candidate
      if (score < bestScore) {
        bestScore = score;
        best = { size: d, velocity: Math.round(vel), friction: fr };
      }
      // Take the smallest acceptable duct
      break;
    }

    // Track best fallback
    if (score < bestScore) {
      bestScore = score;
      best = { size: d, velocity: Math.round(vel), friction: fr };
    }
  }

  if (!best) best = { size: 4, velocity: 0, friction: 0 };
  return best;
}

// ---- Boot recommendation ----
function deRecommendBoot(ductDia, cfm) {
  // Common residential boot sizes by duct diameter
  var bootMap = {
    4: '6x4 floor',
    5: '8x4 floor',
    6: '10x4 floor or 10x6 floor',
    7: '10x6 floor or 12x4 floor',
    8: '12x6 floor or 10x8 ceiling',
    9: '12x6 floor or 14x6 floor',
    10: '14x6 floor or 12x8 ceiling',
    12: '14x8 floor or 12x10 ceiling',
    14: '14x10 floor or 16x8 ceiling'
  };
  return bootMap[ductDia] || (ductDia + ' inch round to register');
}

// ---- Generate return layout ----
function deReturnLayout(clusters, returnCollars, totalCfm) {
  var numReturn = returnCollars.length;
  var layout = [];

  if (numReturn === 0) {
    layout.push({
      label: 'No Return Collars',
      teach: 'No return collars are configured. Every system needs a return path. Without returns, the system creates negative pressure, causing air infiltration and reduced efficiency.',
      size: null,
      cfm: 0
    });
    return layout;
  }

  if (numReturn === 1) {
    var retSize = deFindDuctSize(totalCfm, 'metal');
    var retCollar = returnCollars[0];
    layout.push({
      label: 'Central Return — Living Area',
      teach: 'With a single return, place it in the largest open area (usually the living room or hallway). This creates a central return point. Door undercuts (1 inch) or transfer grilles help air return from closed bedrooms.',
      size: parseInt(retCollar.size),
      cfm: totalCfm,
      velocity: retSize.velocity,
      bootSize: 'Large filter grille (20x25 or 25x20 typical)',
      trunkSize: retSize.size
    });
  } else {
    // Multiple returns — assign to clusters by CFM priority
    // Sort clusters by CFM descending and assign returns
    var sortedClusters = clusters.slice().sort(function(a, b) { return b.totalCfm - a.totalCfm; });
    var cfmPerReturn = Math.round(totalCfm / numReturn);
    returnCollars.forEach(function(col, i) {
      var retCfm = (i === numReturn - 1) ? totalCfm - (cfmPerReturn * (numReturn - 1)) : cfmPerReturn;
      var retSize = deFindDuctSize(retCfm, 'metal');
      var servingCluster = i < sortedClusters.length ? sortedClusters[i].label : 'General Area';
      layout.push({
        label: 'Return ' + (i + 1) + ' — ' + servingCluster,
        teach: i === 0 ?
          'Multiple returns help balance pressure across the house. Each return should be sized for its share of total airflow. This prevents one area from starving another.' :
          'This return serves a separate zone. Keep return grilles away from supply registers to avoid short-circuiting the airflow.',
        size: parseInt(col.size),
        cfm: retCfm,
        velocity: retSize.velocity,
        bootSize: retCfm > 300 ? 'Filter grille (20x20 or 16x25)' : 'Return grille (14x14 or 12x12)',
        trunkSize: retSize.size
      });
    });
  }

  return layout;
}

// ---- Main estimation function ----
function deEstimate() {
  // Get room data
  var rooms = [];
  if (typeof getRoomsList === 'function') {
    rooms = getRoomsList(); // [{name, cfm}, ...]
  }
  if (rooms.length === 0) {
    return { error: 'norooms', message: 'Add rooms in the Rooms tab first. The estimator reads your room data to build a layout suggestion.' };
  }

  // Enrich rooms with type info
  if (typeof roomCfmData !== 'undefined') {
    rooms = rooms.map(function(rm, i) {
      var data = roomCfmData[i] || {};
      return {
        name: rm.name,
        cfm: rm.cfm,
        type: data.type || 'bedroom',
        sqft: (data.length || 0) * (data.width || 0)
      };
    });
  }

  // Get collars
  var supplyCollars = (typeof SS !== 'undefined' && SS.collars) ? SS.collars : [];
  var returnCollars = (typeof SS !== 'undefined' && SS.retCollars) ? SS.retCollars : [];

  var totalCfm = 0;
  rooms.forEach(function(r) { totalCfm += r.cfm; });

  if (supplyCollars.length === 0) {
    return { error: 'nocollars', message: 'No supply collars found. Go to the System tab and add your plenum collars, then come back here.' };
  }

  // Step 1: Cluster rooms
  var clusters = deClusterRooms(rooms);

  // Step 2: Assign collars to clusters
  var enriched = deAssignCollars(clusters, supplyCollars, returnCollars);

  // Step 3: Size ducts for each cluster
  var clusterResults = enriched.map(function(cluster) {
    var branches = deSizeCluster(cluster);
    return {
      label: cluster.label,
      id: cluster.id,
      totalCfm: cluster.totalCfm,
      supplyCollars: cluster.supplyCollars,
      returnCollars: cluster.returnCollars,
      teach: cluster.teach,
      rooms: cluster.rooms,
      branches: branches
    };
  });

  // Step 4: Return layout
  var returnLayout = deReturnLayout(enriched, returnCollars, totalCfm);

  var result = {
    totalCfm: totalCfm,
    totalRooms: rooms.length,
    supplyCollars: supplyCollars.length,
    returnCollars: returnCollars.length,
    clusters: clusterResults,
    returns: returnLayout,
    timestamp: new Date().toLocaleString()
  };

  DE.lastResult = result;
  return result;
}

// ---- Render the estimation ----
function deRender(result) {
  var el = document.getElementById('deResults');
  if (!el) return;

  if (result.error) {
    el.innerHTML = '<div class="info-note" style="margin-top:8px;border-color:var(--amber)">' +
      '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" style="flex-shrink:0;color:var(--amber)"><circle cx="12" cy="12" r="10"/><path d="M12 16v-4M12 8h.01"/></svg>' +
      '<span style="font-size:12px">' + result.message + '</span></div>';
    return;
  }

  var h = '';

  // Summary header
  h += '<div style="background:linear-gradient(135deg,var(--accent),#a37524);border-radius:12px;padding:14px 16px;margin-bottom:12px;color:#fff">';
  h += '<div style="font-size:15px;font-weight:700;margin-bottom:4px">Rough Duct Estimate</div>';
  h += '<div style="display:flex;gap:12px;font-size:11px;opacity:0.9">';
  h += '<span>' + result.totalCfm + ' CFM</span>';
  h += '<span>' + result.totalRooms + ' rooms</span>';
  h += '<span>' + result.supplyCollars + ' supply collar' + (result.supplyCollars !== 1 ? 's' : '') + '</span>';
  h += '<span>' + result.returnCollars + ' return' + (result.returnCollars !== 1 ? 's' : '') + '</span>';
  h += '</div></div>';

  // Important note
  h += '<div class="info-note" style="margin-bottom:12px">';
  h += '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" style="flex-shrink:0"><circle cx="12" cy="12" r="10"/><path d="M12 16v-4M12 8h.01"/></svg>';
  h += '<span style="font-size:10px">This is a conceptual starting point, not a Manual D design. Actual duct routes depend on where the furnace and rooms are located. Use this to understand how rooms group together and what sizes to expect.</span>';
  h += '</div>';

  // Supply clusters
  h += '<div style="font-size:11px;font-weight:700;color:var(--text-2);text-transform:uppercase;letter-spacing:0.5px;margin-bottom:8px">Supply Layout</div>';

  result.clusters.forEach(function(cluster) {
    if (cluster.rooms.length === 0) return;

    h += '<div class="panel" style="margin-bottom:10px;border-left:3px solid var(--accent)">';

    // Cluster header
    h += '<div style="display:flex;justify-content:space-between;align-items:center;margin-bottom:6px">';
    h += '<div style="font-size:14px;font-weight:700;color:var(--text)">' + cluster.label + '</div>';
    h += '<div style="font-size:12px;font-family:\'DM Mono\',monospace;color:var(--accent);font-weight:700">' + cluster.totalCfm + ' CFM</div>';
    h += '</div>';

    // Room list
    h += '<div style="display:flex;flex-wrap:wrap;gap:4px;margin-bottom:8px">';
    cluster.rooms.forEach(function(rm) {
      h += '<span style="background:var(--surface-2);border-radius:6px;padding:3px 8px;font-size:10px;color:var(--text-2)">';
      h += rm.name + ' <span style="font-family:\'DM Mono\',monospace;color:var(--accent);font-weight:600">' + rm.cfm + '</span>';
      h += '</span>';
    });
    h += '</div>';

    // Teaching blurb
    h += '<div style="background:var(--surface-2);border-radius:8px;padding:8px 10px;margin-bottom:10px;border-left:2px solid var(--accent)">';
    h += '<div style="font-size:10px;font-weight:700;color:var(--accent);margin-bottom:2px">WHY THIS GROUPING</div>';
    h += '<div style="font-size:11px;color:var(--text-2);line-height:1.4">' + cluster.teach + '</div>';
    h += '</div>';

    // Collar assignments
    h += '<div style="font-size:10px;color:var(--text-3);margin-bottom:6px">' +
      cluster.supplyCollars + ' supply collar' + (cluster.supplyCollars !== 1 ? 's' : '') +
      (cluster.returnCollars > 0 ? ' + ' + cluster.returnCollars + ' return' : '') + '</div>';

    // Branch details
    cluster.branches.forEach(function(branch) {
      h += '<div style="background:var(--surface-2);border-radius:8px;padding:10px;margin-bottom:6px">';

      if (branch.noCollar) {
        // No dedicated collar — rooms served from nearest trunk
        h += '<div style="font-size:12px;font-weight:600;color:var(--text-2);margin-bottom:6px">';
        h += '<span style="font-style:italic">No dedicated collar — served from nearest trunk branch</span>';
        h += '</div>';
      } else {
        // Branch header
        h += '<div style="display:flex;justify-content:space-between;align-items:center;margin-bottom:6px">';
        h += '<div style="font-size:12px;font-weight:700;color:var(--text)">';
        h += '<span style="color:var(--accent)">Collar ' + branch.collarIndex + '</span>';
        h += ' \u2014 ' + branch.collarSize + '\u2033 start';
        h += '</div>';
        h += '<div style="font-size:11px;font-family:\'DM Mono\',monospace;color:var(--text-2)">' + branch.branchCfm + ' CFM</div>';
        h += '</div>';

        // Trunk info
        h += '<div style="font-size:10px;color:var(--text-3);margin-bottom:8px">';
        h += 'Trunk: <strong style="color:var(--text)">' + branch.trunkSize + '\u2033</strong> metal';
        h += ' \u00B7 ' + branch.trunkVel + ' FPM';
        h += ' \u00B7 ' + branch.trunkFR.toFixed(3) + ' IWC/100ft';
        h += '</div>';
      }

      // Takeoff table
      h += '<div style="overflow-x:auto">';
      h += '<table style="width:100%;border-collapse:collapse;font-size:10px">';
      h += '<thead><tr style="background:var(--accent);color:#fff;text-align:left">';
      h += '<th style="padding:4px 6px;border-radius:4px 0 0 0">Room</th>';
      h += '<th style="padding:4px 6px">CFM</th>';
      h += '<th style="padding:4px 6px">Flex</th>';
      h += '<th style="padding:4px 6px">Fitting</th>';
      h += '<th style="padding:4px 6px;border-radius:0 4px 0 0">Boot</th>';
      h += '</tr></thead><tbody>';

      branch.takeoffs.forEach(function(to, ti) {
        var bg = ti % 2 === 1 ? 'background:var(--surface-3)' : '';
        h += '<tr style="' + bg + '">';
        h += '<td style="padding:5px 6px;font-weight:600;color:var(--text)">' + to.room + '</td>';
        h += '<td style="padding:5px 6px;font-family:\'DM Mono\',monospace">' + to.roomCfm + '</td>';
        h += '<td style="padding:5px 6px;font-family:\'DM Mono\',monospace;font-weight:700;color:var(--accent)">' + to.takeoffSize + '\u2033</td>';
        h += '<td style="padding:5px 6px;font-size:9px;color:var(--text-2)">' + to.fittingType + '</td>';
        h += '<td style="padding:5px 6px;font-size:9px;color:var(--text-2)">' + to.bootSize + '</td>';
        h += '</tr>';
      });
      h += '</tbody></table></div>';

      // Trunk reduction note
      var reductions = branch.takeoffs.filter(function(to) { return to.trunkAfter !== null && to.trunkAfter < to.trunkBefore; });
      if (reductions.length > 0) {
        h += '<div style="margin-top:6px;background:var(--surface-3);border-radius:6px;padding:6px 8px">';
        h += '<div style="font-size:9px;font-weight:700;color:var(--accent);margin-bottom:2px">TRUNK REDUCES</div>';
        reductions.forEach(function(rd) {
          h += '<div style="font-size:10px;color:var(--text-2)">After ' + rd.room + ': ' + rd.trunkBefore + '\u2033 \u2192 ' + rd.trunkAfter + '\u2033 (' + rd.trunkAfterCfm + ' CFM remaining)</div>';
        });
        h += '</div>';
      }

      h += '</div>'; // branch panel
    });

    h += '</div>'; // cluster panel
  });

  // Return layout section
  h += '<div style="font-size:11px;font-weight:700;color:var(--text-2);text-transform:uppercase;letter-spacing:0.5px;margin:16px 0 8px">Return Layout</div>';

  result.returns.forEach(function(ret) {
    h += '<div class="panel" style="margin-bottom:8px;border-left:3px solid #5b8def">';
    h += '<div style="display:flex;justify-content:space-between;align-items:center;margin-bottom:6px">';
    h += '<div style="font-size:13px;font-weight:700;color:var(--text)">' + ret.label + '</div>';
    if (ret.cfm > 0) {
      h += '<div style="font-size:12px;font-family:\'DM Mono\',monospace;color:#5b8def;font-weight:700">' + ret.cfm + ' CFM</div>';
    }
    h += '</div>';

    if (ret.size) {
      h += '<div style="font-size:10px;color:var(--text-3);margin-bottom:6px">';
      h += 'Collar: <strong>' + ret.size + '\u2033</strong>';
      h += ' \u00B7 Trunk: <strong>' + ret.trunkSize + '\u2033</strong>';
      h += ' \u00B7 ' + ret.velocity + ' FPM';
      h += ' \u00B7 ' + ret.bootSize;
      h += '</div>';
    }

    // Teaching blurb
    h += '<div style="background:var(--surface-2);border-radius:8px;padding:8px 10px;border-left:2px solid #5b8def">';
    h += '<div style="font-size:10px;font-weight:700;color:#5b8def;margin-bottom:2px">RETURN TIP</div>';
    h += '<div style="font-size:11px;color:var(--text-2);line-height:1.4">' + ret.teach + '</div>';
    h += '</div>';

    h += '</div>';
  });

  // General teaching section
  h += '<div style="font-size:11px;font-weight:700;color:var(--text-2);text-transform:uppercase;letter-spacing:0.5px;margin:16px 0 8px">Good Habits for Installers</div>';

  h += '<div class="panel" style="margin-bottom:8px">';
  var tips = [
    { icon: '\u{1F4CF}', title: 'Pull Flex Tight', text: 'Flex duct must be pulled tight with no sag. Even 5% compression doubles friction loss. Always support flex every 4 feet.' },
    { icon: '\u{1F527}', title: 'Size Down After Splits', text: 'After each takeoff, the trunk can reduce in size because there is less CFM to carry. This saves material and keeps velocity in a good range.' },
    { icon: '\u{1F3AF}', title: 'Target 0.08 IWC/100ft', text: 'Manual D says 0.08 IWC per 100 feet of duct is the maximum friction rate for residential. Lower is better — it means your fan works less hard.' },
    { icon: '\u26A1', title: 'Keep Runs Short', text: 'Every foot of duct and every fitting adds resistance. The shorter and straighter the run, the more airflow the room gets.' },
    { icon: '\u{1F6AA}', title: 'Return Air Path', text: 'Air pushed into a room must have a path back to the return. Door undercuts (1 inch minimum) or transfer grilles keep rooms from pressurizing.' },
    { icon: '\u2696\uFE0F', title: 'Balance Supply + Return', text: 'Total return CFM should roughly equal total supply CFM. If returns are undersized, the house goes negative pressure, pulling in hot/humid attic or crawl air.' }
  ];

  tips.forEach(function(tip) {
    h += '<div style="display:flex;gap:8px;align-items:flex-start;padding:8px 0;border-bottom:1px solid var(--surface-3)">';
    h += '<div style="font-size:18px;flex-shrink:0;width:24px;text-align:center">' + tip.icon + '</div>';
    h += '<div>';
    h += '<div style="font-size:11px;font-weight:700;color:var(--text)">' + tip.title + '</div>';
    h += '<div style="font-size:10px;color:var(--text-3);line-height:1.3">' + tip.text + '</div>';
    h += '</div></div>';
  });
  h += '</div>';

  // Disclaimer
  h += '<div class="info-note" style="margin-top:8px">';
  h += '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" style="flex-shrink:0"><circle cx="12" cy="12" r="10"/><path d="M12 16v-4M12 8h.01"/></svg>';
  h += '<span style="font-size:10px">This is a rough estimate for educational purposes. Actual duct design must account for equipment location, room positions, attic/crawl routing constraints, and a full Manual D calculation. Use the System Design wizard for a production layout.</span>';
  h += '</div>';

  // Timestamp
  h += '<div style="font-size:9px;color:var(--text-3);text-align:center;margin-top:8px">';
  h += 'Estimated ' + result.timestamp;
  h += '</div>';

  el.innerHTML = h;
}

// ---- Event delegation ----
document.addEventListener('click', function(e) {
  var t = e.target;

  // Run estimation
  if (t.closest('#deRunEstimate')) {
    var result = deEstimate();
    deRender(result);
    var resEl = document.getElementById('deResults');
    if (resEl) {
      setTimeout(function() {
        resEl.scrollIntoView({ behavior: 'smooth', block: 'start' });
      }, 100);
    }
    return;
  }
});
