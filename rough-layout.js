// ===== ROUGH LAYOUT HELPER =====
// Rule-of-thumb first-pass duct layout from system CFM and room clusters.
// Reuses frictionLoss() from the main app for accurate sizing.

var RL = {
  clusters: [
    { name: 'Master Suite', runs: 2, weight: 1.2 },
    { name: 'Living / Kitchen', runs: 3, weight: 1.0 },
    { name: 'Secondary Bedrooms', runs: 2, weight: 0.8 }
  ],
  lastResult: null // structured JSON for other app features
};

// ---- Duct sizing helper (wraps existing frictionLoss) ----
function sizeDuctForRunCFM(runCFM, options) {
  var targetFR = options.targetFR || 0.08;
  var frRange = options.frRange || 0.02;
  var minVel = options.minVel || 400;
  var maxVel = options.maxVel || 700;
  var material = options.material || 'metal';

  var candidates = [4, 5, 6, 7, 8, 9, 10, 12, 14, 16, 18, 20, 22, 24];
  var best = null;
  var bestScore = Infinity;
  var warnings = [];

  for (var i = 0; i < candidates.length; i++) {
    var d = candidates[i];
    var A = Math.PI * Math.pow(d / 12 / 2, 2); // sq ft
    var vel = runCFM / A; // FPM
    var fr = 0;

    // Use existing frictionLoss if available
    if (typeof frictionLoss === 'function') {
      fr = frictionLoss(d, runCFM, material, false);
    } else {
      // Fallback: Darcy-Weisbach approximation
      var D_ft = d / 12;
      var V_fps = vel / 60;
      var rho = 0.075;
      var rough = material === 'flex' ? 0.003 : 0.0003;
      var Re = V_fps * D_ft / (1.6e-4);
      if (Re < 1) continue;
      var fDarcy = 0.11 * Math.pow(rough / D_ft + 68 / Re, 0.25);
      fr = fDarcy * (100 / D_ft) * (rho * V_fps * V_fps) / (2 * 32.174) / 5.192;
    }

    // Score: lower is better
    var frDiff = Math.abs(fr - targetFR);
    var velOk = vel >= minVel && vel <= maxVel;
    var frOk = fr >= (targetFR - frRange) && fr <= (targetFR + frRange);

    var score = frDiff * 100;
    if (!velOk) score += 50;
    if (!frOk) score += 20;
    // Prefer smaller duct that meets constraints
    if (frOk && velOk) score -= 10;

    var w = [];
    if (vel > maxVel) w.push('velocity high (' + Math.round(vel) + ' FPM)');
    if (vel < minVel) w.push('velocity low (' + Math.round(vel) + ' FPM)');
    if (fr > targetFR + frRange) w.push('friction high (' + fr.toFixed(3) + ')');
    if (fr < targetFR - frRange && d > 4) w.push('friction low (' + fr.toFixed(3) + ')');

    if (frOk && velOk) {
      // Perfect match — take smallest that works
      if (!best || d < best.size) {
        best = { size: d, velocity: Math.round(vel), friction: fr, warnings: w, score: score };
      }
      break; // smallest that works
    }

    if (score < bestScore) {
      bestScore = score;
      best = { size: d, velocity: Math.round(vel), friction: fr, warnings: w, score: score };
    }
  }

  if (!best) {
    best = { size: 6, velocity: 0, friction: 0, warnings: ['no suitable size found'] };
  }

  return best;
}

// ---- Compute the full layout ----
function rlComputeLayout() {
  var totalCFM = parseFloat(document.getElementById('rlTotalCFM').value) || 0;
  if (totalCFM <= 0) return null;

  var targetFR = parseFloat(document.getElementById('rlTargetFR').value) || 0.08;
  var frRange = parseFloat(document.getElementById('rlFRRange').value) || 0.02;
  var minVel = parseFloat(document.getElementById('rlMinVel').value) || 400;
  var maxVel = parseFloat(document.getElementById('rlMaxVel').value) || 700;

  // Sum weights
  var totalWeight = 0;
  RL.clusters.forEach(function(c) { totalWeight += (c.weight || 1); });
  if (totalWeight <= 0) totalWeight = 1;

  var result = {
    totalCFM: totalCFM,
    targetFR: targetFR,
    frRange: frRange,
    minVel: minVel,
    maxVel: maxVel,
    clusters: []
  };

  RL.clusters.forEach(function(cluster) {
    var clusterCFM = Math.round(totalCFM * (cluster.weight / totalWeight));
    var numRuns = Math.max(1, cluster.runs || 1);
    var runCFM = Math.round(clusterCFM / numRuns);

    var runs = [];
    for (var r = 0; r < numRuns; r++) {
      var sizing = sizeDuctForRunCFM(runCFM, {
        targetFR: targetFR,
        frRange: frRange,
        minVel: minVel,
        maxVel: maxVel,
        material: 'metal' // default to metal for rough layout
      });
      runs.push({
        index: r + 1,
        cfm: runCFM,
        size: sizing.size,
        velocity: sizing.velocity,
        friction: sizing.friction,
        warnings: sizing.warnings
      });
    }

    result.clusters.push({
      name: cluster.name,
      totalCFM: clusterCFM,
      numRuns: numRuns,
      weight: cluster.weight,
      runs: runs
    });
  });

  RL.lastResult = result;
  return result;
}

// ---- Render clusters input ----
function rlRenderClusters() {
  var el = document.getElementById('rlClusters');
  if (!el) return;
  var h = '';
  RL.clusters.forEach(function(c, ci) {
    h += '<div style="background:var(--surface-2);border-radius:10px;padding:10px;margin-bottom:6px;border:1px solid var(--surface-4)">';
    h += '<div style="display:flex;align-items:center;gap:6px;margin-bottom:6px">';
    h += '<input type="text" class="input-field" value="' + c.name + '" data-rl-cname="' + ci + '" style="flex:1;font-weight:600">';
    h += '<div style="cursor:pointer;color:var(--text-3);font-size:16px;padding:4px" data-rl-del="' + ci + '">&times;</div>';
    h += '</div>';
    h += '<div style="display:flex;gap:6px">';
    h += '<div style="flex:1"><label class="input-label">Runs</label>';
    h += '<input type="number" class="input-field" value="' + (c.runs || 1) + '" min="1" max="20" data-rl-cruns="' + ci + '"></div>';
    h += '<div style="flex:1"><label class="input-label">Weight</label>';
    h += '<input type="number" class="input-field" value="' + (c.weight || 1) + '" min="0.1" max="3" step="0.1" data-rl-cweight="' + ci + '"></div>';
    h += '</div>';
    h += '</div>';
  });
  el.innerHTML = h;
}

// ---- Render results ----
function rlRenderResults(result) {
  var el = document.getElementById('rlResults');
  if (!el || !result) return;

  var h = '';
  h += '<div style="font-size:11px;font-weight:700;color:var(--text-2);text-transform:uppercase;letter-spacing:0.5px;margin-bottom:8px">Layout Results \u2014 ' + result.totalCFM + ' CFM System</div>';

  result.clusters.forEach(function(cluster) {
    h += '<div class="panel" style="margin-bottom:8px">';
    h += '<div style="display:flex;justify-content:space-between;align-items:center;margin-bottom:8px">';
    h += '<div style="font-size:13px;font-weight:700;color:var(--text)">' + cluster.name + '</div>';
    h += '<div style="font-size:12px;font-family:\'DM Mono\',monospace;color:var(--accent);font-weight:600">' + cluster.totalCFM + ' CFM</div>';
    h += '</div>';
    h += '<div style="font-size:10px;color:var(--text-3);margin-bottom:6px">' + cluster.numRuns + ' runs \u00D7 ~' + (cluster.runs && cluster.runs[0] ? cluster.runs[0].cfm : 0) + ' CFM each | Weight: ' + cluster.weight + '</div>';

    // Run table
    h += '<div style="overflow-x:auto">';
    h += '<table style="width:100%;border-collapse:collapse;font-size:11px">';
    h += '<thead><tr style="background:var(--accent);color:#fff;text-align:left">';
    h += '<th style="padding:4px 6px;border-radius:4px 0 0 0">Run</th>';
    h += '<th style="padding:4px 6px">CFM</th>';
    h += '<th style="padding:4px 6px">Size</th>';
    h += '<th style="padding:4px 6px">Velocity</th>';
    h += '<th style="padding:4px 6px">FR</th>';
    h += '<th style="padding:4px 6px;border-radius:0 4px 0 0">Status</th>';
    h += '</tr></thead><tbody>';

    cluster.runs.forEach(function(run, ri) {
      var bg = ri % 2 === 1 ? 'background:var(--surface-2)' : '';
      var frColor = run.friction > 0.10 ? 'var(--red)' : run.friction > 0.08 ? 'var(--amber)' : 'var(--green)';
      var velColor = run.velocity > 700 ? 'var(--red)' : run.velocity > 600 ? 'var(--amber)' : 'var(--green)';
      var status = run.warnings.length === 0 ? '<span style="color:var(--green)">\u2713 OK</span>' :
                   '<span style="color:var(--amber)">\u26A0 ' + run.warnings.join(', ') + '</span>';

      h += '<tr style="' + bg + '">';
      h += '<td style="padding:4px 6px;font-weight:600">' + run.index + '</td>';
      h += '<td style="padding:4px 6px;font-family:\'DM Mono\',monospace">' + run.cfm + '</td>';
      h += '<td style="padding:4px 6px;font-family:\'DM Mono\',monospace;font-weight:700;color:var(--accent)">' + run.size + '&#x2033;</td>';
      h += '<td style="padding:4px 6px;font-family:\'DM Mono\',monospace;color:' + velColor + '">' + run.velocity + '</td>';
      h += '<td style="padding:4px 6px;font-family:\'DM Mono\',monospace;color:' + frColor + '">' + run.friction.toFixed(3) + '</td>';
      h += '<td style="padding:4px 6px;font-size:10px">' + status + '</td>';
      h += '</tr>';
    });
    h += '</tbody></table></div>';
    h += '</div>';
  });

  // Disclaimer
  h += '<div class="info-note" style="margin-top:8px">';
  h += '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" style="flex-shrink:0"><circle cx="12" cy="12" r="10"/><path d="M12 16v-4M12 8h.01"/></svg>';
  h += '<span style="font-size:10px">This is a rough estimate only. Actual duct design must account for total equivalent length, fitting losses, trunk sizing, and return path. Use the System Design wizard for a complete Manual D-based layout.</span>';
  h += '</div>';

  el.innerHTML = h;
}

// ---- Event handling ----
document.addEventListener('click', function(e) {
  var t = e.target;

  // Tonnage calc
  if (t.closest('#rlCalcFromTon')) {
    var ton = parseFloat(document.getElementById('rlTonnage').value) || 0;
    var perTon = parseFloat(document.getElementById('rlCfmPerTonInput').value) || 400;
    if (ton > 0) {
      document.getElementById('rlTotalCFM').value = Math.round(ton * perTon);
    }
    return;
  }

  // Add cluster
  if (t.closest('#rlAddCluster')) {
    RL.clusters.push({ name: 'New Cluster', runs: 1, weight: 1.0 });
    rlRenderClusters();
    return;
  }

  // Delete cluster
  var del = t.closest('[data-rl-del]');
  if (del) {
    RL.clusters.splice(parseInt(del.dataset.rlDel), 1);
    rlRenderClusters();
    return;
  }

  // Calculate
  if (t.closest('#rlCalculate')) {
    // Save cluster inputs from DOM
    RL.clusters.forEach(function(c, ci) {
      var nameEl = document.querySelector('[data-rl-cname="' + ci + '"]');
      var runsEl = document.querySelector('[data-rl-cruns="' + ci + '"]');
      var weightEl = document.querySelector('[data-rl-cweight="' + ci + '"]');
      if (nameEl) c.name = nameEl.value;
      if (runsEl) c.runs = parseInt(runsEl.value) || 1;
      if (weightEl) c.weight = parseFloat(weightEl.value) || 1;
    });

    // Try to auto-fill total CFM from Rooms tab
    if (!document.getElementById('rlTotalCFM').value && typeof getRoomsTotalCFM === 'function') {
      var roomsCfm = getRoomsTotalCFM();
      if (roomsCfm > 0) document.getElementById('rlTotalCFM').value = roomsCfm;
    }

    var result = rlComputeLayout();
    if (result) {
      rlRenderResults(result);
      // Scroll to results
      var resEl = document.getElementById('rlResults');
      if (resEl) resEl.scrollIntoView({ behavior: 'smooth', block: 'start' });
    } else {
      document.getElementById('rlResults').innerHTML = '<div style="color:var(--red);font-size:12px;padding:10px">Enter a total system CFM above to calculate.</div>';
    }
    return;
  }
});

// Also handle change events for CFM/ton label
document.addEventListener('change', function(e) {
  if (e.target.id === 'rlCfmPerTonInput') {
    var span = document.getElementById('rlCfmPerTon');
    if (span) span.textContent = e.target.value;
  }
});

// Init clusters on page load
if (document.getElementById('rlClusters')) {
  rlRenderClusters();
} else {
  // Defer if DOM not ready
  document.addEventListener('DOMContentLoaded', function() {
    rlRenderClusters();
  });
}
