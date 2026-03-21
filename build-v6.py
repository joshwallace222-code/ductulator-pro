#!/usr/bin/env python3
"""Build DuctCalc Pro V6 — ServiceTitan-Inspired Complete Rebuild"""

# Read the JS script blocks
with open('/home/user/workspace/ductulator-pro/script-block-1.js', 'r') as f:
    js_block_1 = f.read()
with open('/home/user/workspace/ductulator-pro/script-block-2.js', 'r') as f:
    js_block_2 = f.read()
with open('/home/user/workspace/ductulator-pro/script-block-3.js', 'r') as f:
    js_block_3 = f.read()

html = '''<!DOCTYPE html>
<html lang="en" data-theme="dark">
<head>
<!--
   ______                            __
  / ____/___  ____ ___  ____  __  __/ /____  _____
 / /   / __ \\/ __ `__ \\/ __ \\/ / / / __/ _ \\/ ___/
/ /___/ /_/ / / / / / / /_/ / /_/ / /_/  __/ /
\\____/\\____/_/ /_/ /_/ .___/\\__,_/\\__/\\___/_/
                    /_/
        Created with Perplexity Computer
        https://www.perplexity.ai/computer
-->
<meta name="generator" content="Perplexity Computer">
<meta name="author" content="Perplexity Computer">
<meta property="og:see_also" content="https://www.perplexity.ai/computer">
<link rel="author" href="https://www.perplexity.ai/computer">
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0, user-scalable=no">
<meta http-equiv="Cache-Control" content="no-cache, no-store, must-revalidate">
<title>DuctCalc Pro — HVAC Duct Design Tool</title>
<script src="https://cdnjs.cloudflare.com/ajax/libs/jspdf/2.5.1/jspdf.umd.min.js"></script>
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&family=DM+Mono:wght@400;500&display=swap" rel="stylesheet">

<style>
/* ============================================================
   DuctCalc Pro V6 — ServiceTitan-Inspired Rebuild
   Champagne/gold accent, instrument panel aesthetic
   COMPLETELY NEW LAYOUT — dashboard home, dial calculator,
   expandable rooms, full-screen wizard steps, report card results
   ============================================================ */

:root {
  --bg: #0a0a0c;
  --surface: #151517;
  --surface-2: #1c1c20;
  --surface-3: #252528;
  --surface-4: #2e2e32;
  --surface-5: #38383d;

  --text: #f0f0f2;
  --text-2: #9898a0;
  --text-3: #58585f;

  --accent: #d4a853;
  --accent-soft: rgba(212,168,83,0.08);
  --accent-medium: rgba(212,168,83,0.15);
  --accent-strong: #e6bc6a;
  --accent-glow: 0 0 16px rgba(212,168,83,0.12);

  --green: #2dd4a8;
  --green-soft: rgba(45,212,168,0.1);
  --amber: #f0b429;
  --amber-soft: rgba(240,180,41,0.1);
  --red: #ef5350;
  --red-soft: rgba(239,83,80,0.1);
  --blue: #5c9cf5;
  --blue-soft: rgba(92,156,245,0.1);

  --shadow: 0 2px 12px rgba(0,0,0,0.4);
  --shadow-lg: 0 8px 32px rgba(0,0,0,0.5);
  --border: rgba(255,255,255,0.06);
  --border-2: rgba(255,255,255,0.1);

  --r-sm: 10px;
  --r-md: 14px;
  --r-lg: 20px;
  --r-xl: 28px;
  --r-pill: 100px;

  /* Legacy aliases — JS uses these in inline styles */
  --bg-0: var(--bg);
  --bg-1: var(--surface);
  --bg-2: var(--surface-2);
  --bg-3: var(--surface-3);
  --bg-4: var(--surface-4);
  --bg-primary: var(--bg);
  --bg-card: var(--surface);
  --bg-elevated: var(--surface-3);
  --bg-input: var(--bg);
  --surface-0: var(--bg);
  --surface-1: var(--surface);
  --surface-2: #1c1c20;
  --surface-3: #252528;
  --surface-4: #2e2e32;
  --border-subtle: var(--border);
  --border-default: var(--border);
  --border-strong: var(--border-2);
  --border-focus: var(--accent);
  --border-light: var(--border-2);
  --glass: rgba(10,10,12,0.92);
  --glass-border: var(--border);
  --text-primary: var(--text);
  --text-0: var(--text);
  --text-1: #d4d4d8;
  --text-2: #9898a0;
  --text-3: #58585f;
  --text-secondary: var(--text-2);
  --text-muted: var(--text-3);
  --text-dim: var(--text-3);
  --accent-subtle: var(--accent-soft);
  --accent-dim: var(--accent-soft);
  --accent-hover: #c49a48;
  --accent-light: var(--accent-strong);
  --accent-glow-legacy: rgba(212,168,83,0.15);
  --green-subtle: var(--green-soft);
  --amber-subtle: var(--amber-soft);
  --red-subtle: var(--red-soft);
  --pass: var(--green);
  --warn: var(--amber);
  --fail: var(--red);
  --info: var(--blue);
  --success: var(--green);
  --warning: var(--amber);
  --danger: var(--red);
  --supply: var(--red);
  --supply-color: var(--red);
  --return: var(--blue);
  --return-color: var(--blue);
  --airflow: var(--green);
  --airflow-color: var(--green);
  --red-glow: var(--accent);
  --red-dark: var(--accent-hover);
  --yellow: var(--amber);
  --orange: var(--amber);
  --gold: var(--accent);
  --gold-soft: var(--accent-soft);
  --card: var(--surface);
  --card-hover: var(--surface-2);
  --card-elevated: var(--surface-3);
  --card-shadow: var(--shadow);
  --glow-red: var(--accent-glow);
  --shadow-sm: var(--shadow);
  --shadow-md: var(--shadow-lg);
  --shadow-card: var(--shadow);
  --shadow-elevated: var(--shadow-lg);
  --shadow-button: 0 2px 8px rgba(212,168,83,0.3);
  --radius-sm: var(--r-sm);
  --radius-md: var(--r-md);
  --radius-lg: var(--r-lg);
  --radius-xl: var(--r-xl);

  --text-xs: 10px;
  --text-sm: 12px;
  --text-base: 14px;
  --text-lg: 16px;
  --text-xl: 18px;
  --text-2xl: 24px;
  --text-3xl: 32px;
}

*, *::before, *::after { box-sizing: border-box; margin: 0; padding: 0; }

html {
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  scroll-behavior: smooth;
}

body {
  font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif;
  font-feature-settings: 'cv01', 'cv02', 'cv03', 'cv04';
  background: var(--bg);
  color: var(--text);
  min-height: 100dvh;
  overflow-x: hidden;
  padding-bottom: 72px;
  line-height: 1.5;
  -webkit-tap-highlight-color: transparent;
  overscroll-behavior: none;
  margin: 0;
}

/* Mono for numbers */
.mono, [class*="result-val"], [class*="cfm"], input[type="number"],
.slider-value-input, .fr-input, .fr-result, .wiz-result-val,
.compression-readout-value, .dial-readout-value {
  font-family: 'DM Mono', monospace;
  font-feature-settings: 'tnum';
}

::-webkit-scrollbar { width: 3px; }
::-webkit-scrollbar-track { background: transparent; }
::-webkit-scrollbar-thumb { background: rgba(255,255,255,0.06); border-radius: 2px; }

/* ===== ANIMATIONS ===== */
@keyframes fadeIn {
  from { opacity: 0; transform: translateY(12px); }
  to { opacity: 1; transform: translateY(0); }
}
@keyframes slideUp {
  from { opacity: 0; transform: translateY(20px); }
  to { opacity: 1; transform: translateY(0); }
}
@keyframes pulse {
  0%, 100% { opacity: 1; }
  50% { opacity: 0.5; }
}

/* ===== TOP BAR — Thin, minimal ===== */
.topbar {
  position: sticky;
  top: 0;
  z-index: 100;
  background: rgba(10,10,12,0.88);
  backdrop-filter: blur(20px);
  -webkit-backdrop-filter: blur(20px);
  border-bottom: 1px solid var(--border);
  height: 48px;
  display: flex;
  align-items: center;
  padding: 0 16px;
  gap: 10px;
  cursor: pointer;
}

.topbar-logo {
  width: 28px;
  height: 28px;
  flex-shrink: 0;
}

.topbar-title {
  font-size: 15px;
  font-weight: 700;
  letter-spacing: -0.02em;
  color: var(--text);
}

.topbar-badge {
  font-size: 8px;
  font-weight: 700;
  text-transform: uppercase;
  letter-spacing: 0.12em;
  color: var(--accent);
  background: var(--accent-soft);
  padding: 2px 6px;
  border-radius: 4px;
}

/* Old nav (hidden for JS compat) */
.nav { display: none !important; }
.nav-tabs { display: none; }
.nav-tab { display: none; }

/* ===== PAGE SYSTEM ===== */
.page { display: none; }
.page.active { display: block; animation: fadeIn 0.2s ease-out; }

.app-container {
  max-width: 480px;
  margin: 0 auto;
  padding: 0 16px 24px;
}

/* ===== HOME PAGE — Dashboard Layout ===== */
#page-home .app-container {
  padding-top: 20px;
}

/* Status summary card */
.dash-status {
  background: linear-gradient(135deg, var(--surface) 0%, var(--surface-2) 100%);
  border: 1px solid var(--border);
  border-radius: var(--r-lg);
  padding: 20px;
  margin-bottom: 20px;
  position: relative;
  overflow: hidden;
}
.dash-status::before {
  content: '';
  position: absolute;
  top: 0; left: 0; right: 0;
  height: 2px;
  background: linear-gradient(90deg, var(--accent) 0%, transparent 100%);
}
.dash-status-label {
  font-size: 10px;
  font-weight: 700;
  text-transform: uppercase;
  letter-spacing: 0.1em;
  color: var(--text-3);
  margin-bottom: 6px;
}
.dash-status-value {
  font-size: 15px;
  font-weight: 600;
  color: var(--text-2);
}
.dash-status-value .highlight {
  color: var(--accent);
}

/* Quick actions — large pill buttons */
.dash-section-label {
  font-size: 10px;
  font-weight: 700;
  text-transform: uppercase;
  letter-spacing: 0.1em;
  color: var(--text-3);
  margin-bottom: 10px;
  padding-left: 4px;
}

.dash-actions {
  display: flex;
  flex-direction: column;
  gap: 10px;
  margin-bottom: 24px;
}

.dash-action {
  display: flex;
  align-items: center;
  gap: 14px;
  background: var(--surface);
  border: 1px solid var(--border);
  border-radius: var(--r-lg);
  padding: 16px 18px;
  cursor: pointer;
  transition: all 0.15s ease;
  -webkit-tap-highlight-color: transparent;
}
.dash-action:active {
  transform: scale(0.98);
  background: var(--surface-2);
}
.dash-action-icon {
  width: 44px;
  height: 44px;
  border-radius: 12px;
  display: flex;
  align-items: center;
  justify-content: center;
  flex-shrink: 0;
}
.dash-action-icon svg { width: 22px; height: 22px; }
.dash-action-icon.design { background: var(--accent-medium); color: var(--accent); }
.dash-action-icon.calc { background: var(--blue-soft); color: var(--blue); }

.dash-action-text {
  flex: 1;
  min-width: 0;
}
.dash-action-title {
  font-size: 15px;
  font-weight: 700;
  color: var(--text);
  margin-bottom: 2px;
}
.dash-action-desc {
  font-size: 12px;
  color: var(--text-3);
  line-height: 1.3;
}
.dash-action-arrow {
  color: var(--text-3);
  flex-shrink: 0;
}
.dash-action-arrow svg { width: 18px; height: 18px; }

/* Tools grid */
.dash-tools {
  display: grid;
  grid-template-columns: repeat(2, 1fr);
  gap: 10px;
  margin-bottom: 24px;
}

.dash-tool {
  background: var(--surface);
  border: 1px solid var(--border);
  border-radius: var(--r-md);
  padding: 16px 14px;
  cursor: pointer;
  transition: all 0.15s ease;
  -webkit-tap-highlight-color: transparent;
}
.dash-tool:active { transform: scale(0.97); background: var(--surface-2); }

.dash-tool-icon {
  width: 36px;
  height: 36px;
  border-radius: 10px;
  display: flex;
  align-items: center;
  justify-content: center;
  margin-bottom: 10px;
}
.dash-tool-icon svg { width: 18px; height: 18px; }
.dash-tool-icon.eqlen { background: var(--amber-soft); color: var(--amber); }
.dash-tool-icon.frwork { background: var(--red-soft); color: var(--red); }
.dash-tool-icon.filter { background: var(--green-soft); color: var(--green); }
.dash-tool-icon.psychro { background: var(--blue-soft); color: var(--blue); }

.dash-tool-name {
  font-size: 13px;
  font-weight: 600;
  color: var(--text);
  margin-bottom: 2px;
}
.dash-tool-desc {
  font-size: 10px;
  color: var(--text-3);
  line-height: 1.3;
}

/* Recent projects placeholder */
.dash-recent {
  background: var(--surface);
  border: 1px dashed rgba(255,255,255,0.08);
  border-radius: var(--r-md);
  padding: 24px;
  text-align: center;
}
.dash-recent-icon {
  width: 40px;
  height: 40px;
  border-radius: 12px;
  background: var(--surface-3);
  display: flex;
  align-items: center;
  justify-content: center;
  margin: 0 auto 10px;
  color: var(--text-3);
}
.dash-recent-icon svg { width: 20px; height: 20px; }
.dash-recent-title {
  font-size: 13px;
  font-weight: 600;
  color: var(--text-2);
  margin-bottom: 4px;
}
.dash-recent-desc {
  font-size: 11px;
  color: var(--text-3);
}

/* Footer */
.dash-footer {
  text-align: center;
  padding: 20px 0 8px;
}
.dash-footer a {
  font-size: 10px;
  color: var(--text-3);
  text-decoration: none;
}

/* ===== ROOM CFM PAGE — Expandable List ===== */
.room-header-bar {
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 16px 0 12px;
}
.room-header-title {
  font-size: 18px;
  font-weight: 800;
  letter-spacing: -0.03em;
}
.room-header-btn {
  background: var(--accent);
  color: #000;
  border: none;
  border-radius: var(--r-pill);
  padding: 8px 16px;
  font-size: 12px;
  font-weight: 700;
  cursor: pointer;
  font-family: inherit;
}
.room-header-btn:active { opacity: 0.8; }

/* Tightness panel */
.tightness-panel {
  background: var(--surface);
  border: 1px solid var(--border);
  border-radius: var(--r-md);
  padding: 14px;
  margin-bottom: 12px;
}
.tightness-title {
  display: flex;
  align-items: center;
  gap: 8px;
  font-size: 12px;
  font-weight: 700;
  color: var(--text-2);
  margin-bottom: 8px;
}
.tightness-title svg { width: 16px; height: 16px; color: var(--accent); }
.tightness-selector { margin-bottom: 6px; }
.tightness-desc {
  font-size: 10px;
  color: var(--text-3);
  line-height: 1.4;
}
.tightness-btn {
  display: inline-flex;
  flex-direction: column;
  align-items: center;
  padding: 8px 12px;
  border-radius: var(--r-sm);
  border: 1px solid var(--border);
  background: var(--surface-2);
  color: var(--text-2);
  cursor: pointer;
  font-family: inherit;
  font-size: 11px;
  font-weight: 600;
  margin-right: 6px;
  margin-bottom: 4px;
  transition: all 0.15s;
}
.tightness-btn.active {
  border-color: var(--accent);
  background: var(--accent-soft);
  color: var(--accent);
}
.tightness-btn-label { font-size: 11px; font-weight: 600; }
.tightness-btn-ach { font-size: 9px; color: var(--text-3); font-family: 'DM Mono', monospace; }

/* Room list — expandable rows */
#roomCfmList {
  display: flex;
  flex-direction: column;
  gap: 2px;
}

.room-cfm-card {
  background: var(--surface);
  border: 1px solid var(--border);
  border-radius: var(--r-md);
  overflow: hidden;
  transition: all 0.2s ease;
  margin-bottom: 2px;
}
.room-cfm-header {
  display: flex;
  align-items: center;
  gap: 8px;
  padding: 12px 14px;
  cursor: pointer;
  -webkit-tap-highlight-color: transparent;
}
.room-cfm-header span { font-size: 12px; }
.room-cfm-name {
  flex: 1;
  font-size: 14px;
  font-weight: 600;
  color: var(--text);
}
.room-cfm-value {
  font-family: 'DM Mono', monospace;
  font-size: 14px;
  font-weight: 600;
  color: var(--accent);
  min-width: 60px;
  text-align: right;
}
.room-cfm-unit {
  font-size: 10px;
  color: var(--text-3);
  margin-left: 2px;
}
.room-cfm-expand {
  color: var(--text-3);
  transition: transform 0.2s;
}
.room-cfm-expand svg { width: 16px; height: 16px; }
.room-cfm-body {
  padding: 0 14px 14px;
  display: none;
}
.room-cfm-card.expanded .room-cfm-body { display: block; }
.room-cfm-card.expanded .room-cfm-expand { transform: rotate(180deg); }

/* Room inputs inside expanded body */
.room-input-grid {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 8px;
}
.room-input-group {
  display: flex;
  flex-direction: column;
  gap: 4px;
}
.room-input-label {
  font-size: 10px;
  font-weight: 600;
  color: var(--text-3);
  text-transform: uppercase;
  letter-spacing: 0.06em;
}
.room-input-field {
  background: var(--bg);
  border: 1px solid var(--border);
  border-radius: 8px;
  padding: 8px 10px;
  color: var(--text);
  font-family: 'DM Mono', monospace;
  font-size: 13px;
  outline: none;
  width: 100%;
}
.room-input-field:focus { border-color: var(--accent); }

.room-type-select {
  background: var(--bg);
  border: 1px solid var(--border);
  border-radius: 8px;
  padding: 8px 10px;
  color: var(--text);
  font-family: inherit;
  font-size: 12px;
  outline: none;
  width: 100%;
  -webkit-appearance: none;
  appearance: none;
}

.room-delete-btn {
  background: var(--red-soft);
  color: var(--red);
  border: none;
  border-radius: 8px;
  padding: 8px;
  font-size: 11px;
  font-weight: 600;
  cursor: pointer;
  margin-top: 8px;
  width: 100%;
  font-family: inherit;
}

/* Room summary bar — sticky bottom */
.room-summary-bar {
  position: fixed;
  bottom: 72px;
  left: 0;
  right: 0;
  background: rgba(21,21,23,0.95);
  backdrop-filter: blur(12px);
  -webkit-backdrop-filter: blur(12px);
  border-top: 1px solid var(--border);
  padding: 10px 16px;
  display: none;
  z-index: 50;
}
#page-roomcfm.active ~ .room-summary-bar,
.room-summary-bar.visible { display: flex; }

.room-summary-bar .summary-items {
  display: flex;
  justify-content: space-around;
  width: 100%;
  max-width: 480px;
  margin: 0 auto;
}
.room-summary-item {
  text-align: center;
}
.room-summary-value {
  font-family: 'DM Mono', monospace;
  font-size: 16px;
  font-weight: 700;
  color: var(--accent);
}
.room-summary-label {
  font-size: 9px;
  font-weight: 600;
  color: var(--text-3);
  text-transform: uppercase;
  letter-spacing: 0.08em;
}

/* ===== CALCULATOR PAGE — Dial Design ===== */
.calc-header {
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 16px 0 12px;
}
.calc-title {
  font-size: 18px;
  font-weight: 800;
  letter-spacing: -0.03em;
}

/* Mode toggle — pill shape */
.mode-toggle {
  display: flex;
  background: var(--surface);
  border-radius: var(--r-pill);
  padding: 3px;
  margin-bottom: 16px;
  border: 1px solid var(--border);
}
.mode-toggle-btn {
  flex: 1;
  padding: 10px 0;
  text-align: center;
  font-size: 13px;
  font-weight: 600;
  color: var(--text-3);
  background: none;
  border: none;
  border-radius: var(--r-pill);
  cursor: pointer;
  transition: all 0.2s;
  font-family: inherit;
}
.mode-toggle-btn.active {
  background: var(--accent);
  color: #000;
  box-shadow: 0 2px 8px rgba(212,168,83,0.3);
}

/* Dial container — the BIG visual change */
.dial-container {
  position: relative;
  width: 200px;
  height: 200px;
  margin: 16px auto;
  display: flex;
  align-items: center;
  justify-content: center;
}
.dial-ring {
  position: absolute;
  inset: 0;
  width: 100%;
  height: 100%;
}
.dial-ring-bg {
  fill: none;
  stroke: var(--surface-3);
  stroke-width: 8;
}
.dial-ring-fill {
  fill: none;
  stroke: var(--accent);
  stroke-width: 8;
  stroke-linecap: round;
  transition: stroke-dashoffset 0.15s ease;
  filter: drop-shadow(0 0 6px rgba(212,168,83,0.3));
}
.dial-value {
  position: relative;
  z-index: 1;
  text-align: center;
}
.dial-number {
  display: block;
  font-family: 'DM Mono', monospace;
  font-size: 36px;
  font-weight: 700;
  color: var(--text);
  line-height: 1;
}
.dial-unit {
  display: block;
  font-size: 12px;
  font-weight: 600;
  color: var(--text-3);
  text-transform: uppercase;
  letter-spacing: 0.1em;
  margin-top: 4px;
}

/* The slider under the dial */
.dial-slider-wrap {
  padding: 0 8px;
  margin-bottom: 16px;
}

/* Config pills — inline controls */
.config-row {
  display: flex;
  flex-wrap: wrap;
  gap: 8px;
  margin-bottom: 12px;
}
.config-label {
  font-size: 10px;
  font-weight: 700;
  text-transform: uppercase;
  letter-spacing: 0.08em;
  color: var(--text-3);
  width: 100%;
  margin-bottom: 2px;
  padding-left: 2px;
}

/* Segmented controls — smaller, pill-shaped */
.seg-control {
  display: inline-flex;
  background: var(--surface);
  border-radius: var(--r-pill);
  padding: 2px;
  border: 1px solid var(--border);
  gap: 1px;
}
.seg-btn {
  padding: 6px 14px;
  font-size: 11px;
  font-weight: 600;
  color: var(--text-3);
  background: none;
  border: none;
  border-radius: var(--r-pill);
  cursor: pointer;
  transition: all 0.15s;
  font-family: inherit;
  white-space: nowrap;
}
.seg-btn.active {
  background: var(--surface-3);
  color: var(--text);
}

/* Slider panels */
.slider-panel {
  background: var(--surface);
  border: 1px solid var(--border);
  border-radius: var(--r-md);
  padding: 14px;
  margin-bottom: 10px;
}
.slider-header {
  display: flex;
  align-items: center;
  justify-content: space-between;
  margin-bottom: 8px;
}
.slider-label {
  font-size: 11px;
  font-weight: 700;
  color: var(--text-2);
  text-transform: uppercase;
  letter-spacing: 0.06em;
}
.slider-value-input {
  background: var(--bg);
  border: 1px solid var(--border);
  border-radius: 8px;
  padding: 5px 8px;
  color: var(--accent);
  font-family: 'DM Mono', monospace;
  font-size: 14px;
  font-weight: 600;
  outline: none;
  text-align: center;
  width: 64px;
}
.slider-value-input:focus { border-color: var(--accent); }

/* Range sliders */
input[type="range"],
.cfm-slider,
.compression-slider {
  -webkit-appearance: none;
  appearance: none;
  width: 100%;
  height: 6px;
  background: var(--surface-3);
  border-radius: 3px;
  outline: none;
  cursor: pointer;
}
input[type="range"]::-webkit-slider-thumb,
.cfm-slider::-webkit-slider-thumb,
.compression-slider::-webkit-slider-thumb {
  -webkit-appearance: none;
  appearance: none;
  width: 22px;
  height: 22px;
  border-radius: 50%;
  background: var(--accent);
  box-shadow: 0 2px 6px rgba(0,0,0,0.3);
  cursor: pointer;
}

/* Compression section */
.compression-section {
  background: var(--surface);
  border: 1px solid var(--border);
  border-radius: var(--r-md);
  padding: 14px;
  margin-bottom: 10px;
}
.compression-presets {
  display: flex;
  gap: 4px;
  margin-bottom: 8px;
}
.compression-presets button {
  padding: 4px 10px;
  font-size: 10px;
  font-weight: 600;
  border-radius: var(--r-pill);
  border: 1px solid var(--border);
  background: var(--surface-2);
  color: var(--text-3);
  cursor: pointer;
  font-family: inherit;
}
.compression-presets button.active {
  border-color: var(--accent);
  background: var(--accent-soft);
  color: var(--accent);
}
.compression-impact {
  font-size: 10px;
  padding: 6px 10px;
  border-radius: 8px;
  margin-top: 6px;
}
.compression-impact.low { background: var(--green-soft); color: var(--green); }
.compression-impact.medium { background: var(--amber-soft); color: var(--amber); }
.compression-impact.high { background: var(--red-soft); color: var(--red); }

/* Config group / insulated toggle */
.config-group {
  display: flex;
  align-items: center;
  gap: 8px;
}
.config-group label { font-size: 12px; font-weight: 600; color: var(--text-2); }

/* Results cards — grid */
.results-grid {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 8px;
  margin-bottom: 10px;
}
.result-card {
  background: var(--surface);
  border: 1px solid var(--border);
  border-radius: var(--r-md);
  padding: 14px;
  text-align: center;
}
.result-value {
  font-family: 'DM Mono', monospace;
  font-size: 22px;
  font-weight: 700;
  color: var(--text);
  line-height: 1.1;
}
.result-value.green { color: var(--green); }
.result-value.amber, .result-value.warn { color: var(--amber); }
.result-value.red { color: var(--red); }
.result-unit {
  font-size: 10px;
  color: var(--text-3);
  font-weight: 600;
  text-transform: uppercase;
  letter-spacing: 0.06em;
  margin-top: 2px;
}
.result-label {
  font-size: 10px;
  color: var(--text-3);
  margin-top: 4px;
}

/* Status bar */
.status-bar {
  display: flex;
  align-items: center;
  gap: 8px;
  padding: 10px 14px;
  border-radius: var(--r-md);
  font-size: 12px;
  font-weight: 600;
  margin-bottom: 10px;
}
.status-bar svg { width: 16px; height: 16px; flex-shrink: 0; }
.status-bar.ok { background: var(--green-soft); color: var(--green); }
.status-bar.warn { background: var(--amber-soft); color: var(--amber); }
.status-bar.fail { background: var(--red-soft); color: var(--red); }

/* Header results row */
.calc-hdr-results {
  display: flex;
  justify-content: space-around;
  padding: 8px 0;
  margin-bottom: 4px;
}
.hdr-stat {
  text-align: center;
}
.hdr-stat-value {
  font-family: 'DM Mono', monospace;
  font-size: 16px;
  font-weight: 700;
  color: var(--text);
}
.hdr-stat-label {
  font-size: 9px;
  color: var(--text-3);
  text-transform: uppercase;
  letter-spacing: 0.08em;
}

/* ===== PANEL — Generic card ===== */
.panel {
  background: var(--surface);
  border: 1px solid var(--border);
  border-radius: var(--r-md);
  padding: 16px;
  margin-bottom: 12px;
}
.panel-title {
  display: flex;
  align-items: center;
  gap: 8px;
  font-size: 14px;
  font-weight: 700;
  color: var(--text);
  margin-bottom: 12px;
}
.panel-title svg { width: 18px; height: 18px; color: var(--accent); }

/* Input fields */
.input-label {
  font-size: 11px;
  font-weight: 600;
  color: var(--text-2);
  margin-bottom: 4px;
  display: block;
}
.input-field {
  background: var(--bg);
  border: 1px solid var(--border);
  border-radius: 8px;
  padding: 8px 10px;
  color: var(--text);
  font-family: inherit;
  font-size: 13px;
  outline: none;
  width: 100%;
}
.input-field:focus { border-color: var(--accent); }
.input-group { margin-bottom: 8px; }
select.input-field { -webkit-appearance: none; }

/* Checkbox / toggle */
input[type="checkbox"] {
  accent-color: var(--accent);
  width: 16px;
  height: 16px;
}

/* Info notes */
.info-note {
  display: flex;
  gap: 8px;
  padding: 10px 12px;
  background: var(--accent-soft);
  border-radius: var(--r-sm);
  border-left: 3px solid var(--accent);
  font-size: 11px;
  color: var(--text-2);
  line-height: 1.5;
}
.info-note svg { width: 16px; height: 16px; flex-shrink: 0; color: var(--accent); margin-top: 1px; }

/* ===== EQ LENGTH TABLE ===== */
.eq-category {
  font-size: 12px;
  font-weight: 700;
  color: var(--accent);
  margin: 16px 0 8px;
  text-transform: uppercase;
  letter-spacing: 0.06em;
}
.eq-table-container {
  overflow-x: auto;
  -webkit-overflow-scrolling: touch;
  margin-bottom: 8px;
  border-radius: var(--r-sm);
  border: 1px solid var(--border);
}
.eq-table {
  width: 100%;
  border-collapse: collapse;
  font-size: 11px;
}
.eq-table th {
  background: var(--surface-2);
  padding: 8px 6px;
  font-weight: 700;
  color: var(--text-2);
  text-align: left;
  position: sticky;
  top: 0;
  font-size: 10px;
  text-transform: uppercase;
  letter-spacing: 0.04em;
}
.eq-table td {
  padding: 7px 6px;
  border-top: 1px solid var(--border);
  color: var(--text);
  white-space: nowrap;
}
.eq-table td:first-child { color: var(--text-2); white-space: normal; }
.eq-table td:not(:first-child) { font-family: 'DM Mono', monospace; text-align: center; }
.eq-table tr:hover td { background: rgba(255,255,255,0.02); }

/* ===== SYSTEM PAGE (Wizard + Runs) ===== */
.sys-page-header {
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 16px 0 8px;
}
.sys-page-title {
  font-size: 18px;
  font-weight: 800;
  letter-spacing: -0.03em;
}

/* Section collapsible */
.section-header {
  display: flex;
  align-items: center;
  gap: 8px;
  padding: 12px 14px;
  cursor: pointer;
  -webkit-tap-highlight-color: transparent;
  background: var(--surface);
  border: 1px solid var(--border);
  border-radius: var(--r-md);
  margin-bottom: 2px;
}
.section-header svg { width: 18px; height: 18px; color: var(--accent); }
.section-header-title {
  flex: 1;
  font-size: 14px;
  font-weight: 700;
}
.section-header-toggle {
  color: var(--text-3);
  transition: transform 0.2s;
}
.section-header-toggle svg { width: 16px; height: 16px; }
.section-header.collapsed .section-header-toggle { transform: rotate(-90deg); }

.section-body {
  background: var(--surface);
  border: 1px solid var(--border);
  border-top: none;
  border-radius: 0 0 var(--r-md) var(--r-md);
  padding: 14px;
  margin-bottom: 12px;
}
.section-body.collapsed { display: none; }

/* System config grid */
.sys-config-grid {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 8px;
}

/* Collar chips */
.collar-chips {
  display: flex;
  flex-wrap: wrap;
  gap: 4px;
  margin-top: 6px;
}
.collar-chip {
  display: inline-flex;
  align-items: center;
  gap: 4px;
  padding: 4px 8px;
  border-radius: var(--r-pill);
  background: var(--surface-3);
  font-size: 10px;
  font-weight: 600;
  color: var(--text-2);
}
.collar-chip .x {
  cursor: pointer;
  color: var(--text-3);
  font-size: 12px;
}

/* Plenum SVG */
.plenum-svg-wrap {
  margin: 8px 0;
  text-align: center;
}
.plenum-svg-wrap svg { max-width: 100%; height: auto; }

/* ===== WIZARD STEPS — Full-screen style ===== */
.wiz-progress-track {
  height: 3px;
  background: var(--surface-3);
  width: 100%;
}
.wiz-progress-fill {
  height: 100%;
  background: var(--accent);
  transition: width 0.3s ease;
  width: 25%;
  border-radius: 0 2px 2px 0;
}

.wiz-step-bar {
  display: flex;
  align-items: center;
  gap: 2px;
  padding: 8px 16px;
  background: var(--surface);
  border-bottom: 1px solid var(--border);
}
.wiz-pill {
  display: flex;
  align-items: center;
  gap: 4px;
  padding: 6px 10px;
  font-size: 11px;
  font-weight: 600;
  color: var(--text-3);
  cursor: pointer;
  border-radius: var(--r-pill);
  transition: all 0.15s;
  -webkit-tap-highlight-color: transparent;
}
.wiz-pill.active {
  color: var(--accent);
  background: var(--accent-soft);
}
.wiz-pill.done {
  color: var(--green);
}
.wiz-pill-num {
  width: 20px;
  height: 20px;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 10px;
  font-weight: 700;
  background: var(--surface-3);
  color: var(--text-3);
}
.wiz-pill.active .wiz-pill-num {
  background: var(--accent);
  color: #000;
}
.wiz-pill.done .wiz-pill-num {
  background: var(--green-soft);
  color: var(--green);
}
.wiz-pill-label { display: none; }
@media (min-width: 380px) { .wiz-pill-label { display: inline; } }

/* Wizard step content */
.wiz-step {
  display: none;
  padding: 16px;
  max-width: 480px;
  margin: 0 auto;
  animation: slideUp 0.25s ease-out;
}
.wiz-step.active { display: block; }

.wiz-step-title {
  font-size: 18px;
  font-weight: 800;
  letter-spacing: -0.03em;
  margin-bottom: 4px;
}
.wiz-step-desc {
  font-size: 12px;
  color: var(--text-3);
  margin-bottom: 16px;
  line-height: 1.5;
}

/* Option grid — wizard choices */
.opt-grid {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 8px;
  margin-bottom: 16px;
}
.opt-card {
  background: var(--surface);
  border: 1.5px solid var(--border);
  border-radius: var(--r-md);
  padding: 14px;
  text-align: center;
  cursor: pointer;
  transition: all 0.15s;
  -webkit-tap-highlight-color: transparent;
}
.opt-card:active { transform: scale(0.97); }
.opt-card.active {
  border-color: var(--accent);
  background: var(--accent-soft);
}
.opt-card .opt-label {
  font-size: 12px;
  font-weight: 700;
  color: var(--text);
  margin-top: 6px;
}
.opt-card .opt-desc {
  font-size: 10px;
  color: var(--text-3);
  margin-top: 2px;
}
.opt-card svg { width: 28px; height: 28px; color: var(--accent); margin: 0 auto; display: block; }
.opt-card.active svg { color: var(--accent-strong); }

/* Wizard primary button */
.wiz-btn-primary {
  display: block;
  width: 100%;
  padding: 14px;
  background: var(--accent);
  color: #000;
  border: none;
  border-radius: var(--r-md);
  font-size: 14px;
  font-weight: 700;
  cursor: pointer;
  font-family: inherit;
  margin-top: 12px;
  transition: opacity 0.15s;
}
.wiz-btn-primary:active { opacity: 0.8; }

.wiz-btn-add {
  display: block;
  width: 100%;
  padding: 12px;
  background: var(--surface);
  border: 1px dashed var(--border-2);
  border-radius: var(--r-md);
  color: var(--text-2);
  font-size: 13px;
  font-weight: 600;
  cursor: pointer;
  font-family: inherit;
  margin-top: 8px;
}

/* Wizard fitting SVG container */
.wiz-fitting-svg {
  text-align: center;
}
.wiz-fitting-svg svg { max-width: 100%; }

/* Wizard shape toggle */
.wiz-shape-toggle {
  display: flex;
  gap: 4px;
}
.wiz-shape-toggle button {
  padding: 5px 12px;
  font-size: 11px;
  font-weight: 600;
  border-radius: var(--r-pill);
  border: 1px solid var(--border);
  background: var(--surface-2);
  color: var(--text-3);
  cursor: pointer;
  font-family: inherit;
}
.wiz-shape-toggle button.active {
  border-color: var(--accent);
  background: var(--accent-soft);
  color: var(--accent);
}

/* Wizard trunk cards */
.wiz-trunk-card {
  background: var(--surface);
  border: 1px solid var(--border);
  border-radius: var(--r-md);
  padding: 14px;
  margin-bottom: 8px;
}
.wiz-trunk-header {
  display: flex;
  align-items: center;
  justify-content: space-between;
  margin-bottom: 8px;
}
.wiz-trunk-title {
  font-size: 13px;
  font-weight: 700;
}
.wiz-trunk-badge {
  font-size: 9px;
  font-weight: 700;
  padding: 2px 8px;
  border-radius: var(--r-pill);
  text-transform: uppercase;
  letter-spacing: 0.06em;
}

/* Wizard results */
.wiz-result-val {
  font-family: 'DM Mono', monospace;
  font-weight: 700;
}

/* Wizard branch area */
.wiz-branch-group {
  margin-bottom: 12px;
}
.wiz-branch-trunk-label {
  font-size: 11px;
  font-weight: 700;
  color: var(--accent);
  margin-bottom: 6px;
  text-transform: uppercase;
  letter-spacing: 0.06em;
}

/* Wizard fit buttons */
.wiz-fit-btn {
  display: inline-flex;
  align-items: center;
  gap: 6px;
  padding: 6px 12px;
  font-size: 11px;
  font-weight: 600;
  border-radius: var(--r-pill);
  border: 1px solid var(--border);
  background: var(--surface-2);
  color: var(--text-2);
  cursor: pointer;
  margin: 2px;
  font-family: inherit;
}
.wiz-fit-btn svg { width: 14px; height: 14px; }

/* Wizard duct tree / summary */
.wiz-tree-svg { text-align: center; }
.wiz-tree-svg svg { max-width: 100%; }

/* Summary cards in results */
.wiz-summary-card {
  background: var(--surface);
  border: 1px solid var(--border);
  border-radius: var(--r-md);
  padding: 12px;
  margin-bottom: 6px;
}

/* Friction gauge */
.wiz-friction-gauge {
  padding: 12px;
  text-align: center;
}

/* Budget breakdown */
.wiz-budget-bar {
  height: 12px;
  border-radius: 6px;
  overflow: hidden;
  background: var(--surface-3);
  margin: 8px 0;
}

/* ===== FRICTION RATE WORKSHEET ===== */
.fr-section {
  background: var(--surface);
  border: 1px solid var(--border);
  border-radius: var(--r-md);
  padding: 14px;
  margin-bottom: 10px;
}
.fr-section-title {
  font-size: 12px;
  font-weight: 700;
  color: var(--text);
  margin-bottom: 10px;
  display: flex;
  align-items: center;
  gap: 6px;
}
.fr-section-title svg { width: 16px; height: 16px; color: var(--accent); }

.fr-row {
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 6px 0;
  border-bottom: 1px solid var(--border);
}
.fr-row:last-child { border-bottom: none; }
.fr-row-label {
  font-size: 12px;
  color: var(--text-2);
}
.fr-input {
  background: var(--bg);
  border: 1px solid var(--border);
  border-radius: 8px;
  padding: 6px 8px;
  color: var(--text);
  font-family: 'DM Mono', monospace;
  font-size: 13px;
  outline: none;
  text-align: right;
  width: 80px;
}
.fr-input:focus { border-color: var(--accent); }
.fr-select {
  -webkit-appearance: none;
  appearance: none;
  width: 120px;
  text-align: left;
}
.fr-cpl-input { width: 70px; }
.fr-result {
  font-family: 'DM Mono', monospace;
  font-weight: 700;
  color: var(--accent);
}
.fr-result-big {
  font-family: 'DM Mono', monospace;
  font-size: 20px;
  font-weight: 700;
  color: var(--accent);
}

/* FR calc row */
.fr-calc-row {
  display: flex;
  align-items: center;
  gap: 6px;
  padding: 8px 0;
  font-size: 12px;
  color: var(--text-2);
}
.fr-calc-row span { font-family: 'DM Mono', monospace; }

/* FR result card */
.fr-result-card {
  border-radius: var(--r-md);
  padding: 16px;
  margin-top: 12px;
}
.fr-result-card .fr-result-badge {
  display: inline-flex;
  align-items: center;
  gap: 6px;
  padding: 4px 12px;
  border-radius: var(--r-pill);
  font-size: 12px;
  font-weight: 700;
  margin-bottom: 8px;
}
.fr-result-card .fr-result-msg {
  font-size: 12px;
  line-height: 1.5;
  opacity: 0.85;
}
.fr-result-pass { background: var(--green-soft); color: var(--green); }
.fr-result-warn { background: var(--amber-soft); color: var(--amber); }
.fr-result-fail { background: var(--red-soft); color: var(--red); }

/* FR chart */
.fr-chart-wrap {
  background: var(--surface);
  border: 1px solid var(--border);
  border-radius: var(--r-md);
  padding: 12px;
  margin-top: 10px;
}

/* ===== FILTER PAGE ===== */
.filter-mfg-btns {
  display: flex;
  flex-wrap: wrap;
  gap: 6px;
  margin-bottom: 10px;
}
.filter-mfg-btn {
  padding: 6px 12px;
  font-size: 11px;
  font-weight: 600;
  border-radius: var(--r-pill);
  border: 1px solid var(--border);
  background: var(--surface);
  color: var(--text-2);
  cursor: pointer;
  font-family: inherit;
}
.filter-mfg-btn.active {
  border-color: var(--accent);
  background: var(--accent-soft);
  color: var(--accent);
}
.filter-result-card {
  background: var(--surface);
  border: 1px solid var(--border);
  border-radius: var(--r-md);
  padding: 14px;
  margin-top: 10px;
}
.filter-result-value {
  font-family: 'DM Mono', monospace;
  font-size: 18px;
  font-weight: 700;
  color: var(--text);
}
.filter-result-label {
  font-size: 10px;
  color: var(--text-3);
}
.filter-note {
  font-size: 11px;
  color: var(--text-2);
  padding: 8px 0;
  line-height: 1.4;
}
.filter-apply-btn {
  display: block;
  width: 100%;
  padding: 10px;
  background: var(--accent);
  color: #000;
  border: none;
  border-radius: var(--r-md);
  font-size: 13px;
  font-weight: 700;
  cursor: pointer;
  font-family: inherit;
  margin-top: 8px;
}

/* Filter inline */
.filter-inline-grid {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 6px;
}
.filter-inline-stat { text-align: center; padding: 8px; background: var(--surface-2); border-radius: 8px; }
.filter-inline-stat-val { font-family: 'DM Mono', monospace; font-size: 14px; font-weight: 700; }
.filter-inline-stat-label { font-size: 9px; color: var(--text-3); }
.filter-inline-value { font-family: 'DM Mono', monospace; font-weight: 700; }
.filter-impact-card {
  background: var(--surface);
  border: 1px solid var(--border);
  border-radius: var(--r-sm);
  padding: 10px;
  margin-top: 8px;
}
.filter-impact-row {
  display: flex;
  justify-content: space-between;
  padding: 4px 0;
  font-size: 11px;
}
.filter-impact-label { color: var(--text-2); }
.filter-impact-value { font-family: 'DM Mono', monospace; font-weight: 600; color: var(--text); }
.filter-warning-banner {
  background: var(--amber-soft);
  border-radius: var(--r-sm);
  padding: 10px 12px;
  font-size: 11px;
  color: var(--amber);
  margin-top: 8px;
  display: flex;
  align-items: center;
  gap: 8px;
}

/* ===== PSYCHROMETRIC ===== */
.psych-input-row {
  display: flex;
  align-items: center;
  gap: 8px;
  margin-bottom: 6px;
}
.psych-input-row label {
  font-size: 12px;
  color: var(--text-2);
  min-width: 100px;
}
.psych-mode-btns {
  display: flex;
  gap: 4px;
  flex-wrap: wrap;
  margin-bottom: 10px;
}
.psych-mode-btn {
  padding: 5px 10px;
  font-size: 10px;
  font-weight: 600;
  border-radius: var(--r-pill);
  border: 1px solid var(--border);
  background: var(--surface);
  color: var(--text-3);
  cursor: pointer;
  font-family: inherit;
}
.psych-mode-btn.active {
  border-color: var(--accent);
  background: var(--accent-soft);
  color: var(--accent);
}
.psych-result-row {
  display: flex;
  justify-content: space-between;
  padding: 6px 0;
  border-bottom: 1px solid var(--border);
  font-size: 12px;
}
.psych-result-row:last-child { border-bottom: none; }
.psych-result-row span:first-child { color: var(--text-2); }
.psych-result-row span:nth-child(2) { font-family: 'DM Mono', monospace; font-weight: 600; color: var(--text); }
.psych-result-row span:last-child { color: var(--text-3); font-size: 10px; }

/* ===== SYSTEM RUNS ===== */
.sys-add-btn, .sys-add-step-btn, .add-fitting-btn {
  display: inline-flex;
  align-items: center;
  gap: 4px;
  padding: 8px 14px;
  font-size: 12px;
  font-weight: 600;
  border-radius: var(--r-pill);
  border: 1px dashed var(--border-2);
  background: var(--surface);
  color: var(--text-2);
  cursor: pointer;
  font-family: inherit;
}
.sys-add-btn:hover, .sys-add-step-btn:hover, .add-fitting-btn:hover {
  border-color: var(--accent);
  color: var(--accent);
}

/* Run tabs */
.sys-run-tabs {
  display: flex;
  gap: 4px;
  overflow-x: auto;
  padding-bottom: 4px;
  margin-bottom: 8px;
}
.sys-run-tab {
  padding: 6px 14px;
  font-size: 11px;
  font-weight: 600;
  border-radius: var(--r-pill);
  border: 1px solid var(--border);
  background: var(--surface);
  color: var(--text-3);
  cursor: pointer;
  white-space: nowrap;
  font-family: inherit;
}
.sys-run-tab.active {
  border-color: var(--accent);
  background: var(--accent-soft);
  color: var(--accent);
}

/* Run area */
.run-step-row {
  display: flex;
  align-items: center;
  gap: 8px;
  padding: 8px 10px;
  border-bottom: 1px solid var(--border);
  font-size: 12px;
}
.run-step-dot {
  width: 8px;
  height: 8px;
  border-radius: 50%;
  flex-shrink: 0;
}
.run-step-dot.straight { background: var(--green); }
.run-step-dot.fitting { background: var(--amber); }
.run-step-dot.branch { background: var(--red); }

.run-step-name { flex: 1; color: var(--text-2); }
.run-step-eq {
  font-family: 'DM Mono', monospace;
  font-weight: 600;
  color: var(--text);
}
.run-step-actions { display: flex; gap: 4px; }
.run-step-del {
  padding: 4px 8px;
  font-size: 10px;
  border-radius: 6px;
  border: 1px solid var(--border);
  background: var(--surface-2);
  color: var(--text-3);
  cursor: pointer;
  font-family: inherit;
}

/* Run summary grid */
.run-summary-grid {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 6px;
}
.run-summary-card {
  background: var(--surface);
  border: 1px solid var(--border);
  border-radius: var(--r-sm);
  padding: 10px;
  text-align: center;
}
.run-summary-value {
  font-family: 'DM Mono', monospace;
  font-size: 18px;
  font-weight: 700;
  color: var(--text);
}
.run-summary-unit {
  font-size: 9px;
  color: var(--text-3);
  text-transform: uppercase;
}
.run-summary-label {
  font-size: 9px;
  color: var(--text-3);
}

/* Quick add buttons */
.quick-add-btns {
  display: flex;
  gap: 6px;
  margin: 8px 0;
}
.quick-add-btn {
  padding: 6px 14px;
  font-size: 11px;
  font-weight: 600;
  border-radius: var(--r-pill);
  border: 1px solid var(--border);
  background: var(--surface);
  color: var(--text-2);
  cursor: pointer;
  font-family: inherit;
}
.quick-add-btn:active { background: var(--surface-2); }
.quick-add-btn.active {
  border-color: var(--accent);
  background: var(--accent-soft);
  color: var(--accent);
}

/* Straight input row */
.straight-input-row {
  display: flex;
  align-items: center;
  gap: 6px;
  padding: 8px 0;
}
.straight-input-row input {
  width: 60px;
  background: var(--bg);
  border: 1px solid var(--border);
  border-radius: 8px;
  padding: 6px 8px;
  color: var(--text);
  font-family: 'DM Mono', monospace;
  font-size: 13px;
  outline: none;
  text-align: center;
}

/* Fitting search */
.fitting-search-input {
  width: 100%;
  background: var(--bg);
  border: 1px solid var(--border);
  border-radius: var(--r-md);
  padding: 10px 12px;
  color: var(--text);
  font-family: inherit;
  font-size: 13px;
  outline: none;
  margin-bottom: 8px;
}
.fitting-search-input:focus { border-color: var(--accent); }

.fitting-results {
  max-height: 300px;
  overflow-y: auto;
}
.fitting-result-card {
  display: flex;
  align-items: center;
  gap: 10px;
  padding: 10px;
  border-bottom: 1px solid var(--border);
  cursor: pointer;
  transition: background 0.1s;
}
.fitting-result-card:active { background: var(--surface-2); }
.fitting-icon {
  width: 36px;
  height: 36px;
  display: flex;
  align-items: center;
  justify-content: center;
  flex-shrink: 0;
}
.fitting-icon svg { width: 28px; height: 28px; }
.fitting-result-info { flex: 1; min-width: 0; }
.fitting-result-name { font-size: 12px; font-weight: 600; color: var(--text); }
.fitting-result-note { font-size: 10px; color: var(--text-3); }
.fitting-result-eq {
  font-family: 'DM Mono', monospace;
  font-size: 12px;
  font-weight: 600;
  color: var(--accent);
  white-space: nowrap;
}

/* CFM Estimator inside system page */
.cfm-est-room {
  display: flex;
  align-items: center;
  gap: 6px;
  padding: 6px 0;
  border-bottom: 1px solid var(--border);
  font-size: 12px;
}

/* Branch tree panel */
.branch-tree-panel {
  background: var(--surface);
  border: 1px solid var(--border);
  border-radius: var(--r-md);
  padding: 14px;
  margin-top: 12px;
}

/* Reverse calc mode */
.rev-bar-container {
  display: flex;
  height: 12px;
  border-radius: 6px;
  overflow: hidden;
  margin: 8px 0;
}
.rev-bar-zone { height: 100%; }
.rev-bar-low { background: var(--blue); }
.rev-bar-ok { background: var(--green); }
.rev-bar-high { background: var(--red); }

/* ===== BOTTOM NAVIGATION — Refined ===== */
.bottom-nav {
  position: fixed;
  bottom: 0;
  left: 0;
  right: 0;
  height: 64px;
  background: rgba(10,10,12,0.94);
  backdrop-filter: blur(24px);
  -webkit-backdrop-filter: blur(24px);
  border-top: 1px solid var(--border);
  display: flex;
  align-items: center;
  justify-content: space-around;
  padding-bottom: env(safe-area-inset-bottom, 0);
  z-index: 1000;
}

.bottom-nav-item {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 3px;
  color: var(--text-3);
  font-size: 9px;
  font-weight: 700;
  letter-spacing: 0.06em;
  text-transform: uppercase;
  -webkit-tap-highlight-color: transparent;
  transition: color 0.15s;
  touch-action: manipulation;
  cursor: pointer;
  background: none;
  border: none;
  padding: 8px 20px;
  font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif;
  min-width: 56px;
  min-height: 56px;
  justify-content: center;
}

.bottom-nav-item.active { color: var(--accent); }
.bottom-nav-item.active svg {
  filter: drop-shadow(0 0 6px rgba(212,168,83,0.4));
}
.bottom-nav-item svg { width: 22px; height: 22px; stroke-width: 1.5; }

/* ===== MORE PANEL — Bottom sheet ===== */
.more-panel {
  position: fixed;
  inset: 0;
  z-index: 2000;
  pointer-events: none;
  opacity: 0;
  transition: opacity 0.25s ease;
}
.more-panel.open { pointer-events: auto; opacity: 1; }

.more-panel-overlay {
  position: absolute;
  inset: 0;
  background: rgba(0,0,0,0.6);
  backdrop-filter: blur(8px);
  -webkit-backdrop-filter: blur(8px);
}

.more-panel-sheet {
  position: absolute;
  bottom: 0;
  left: 0;
  right: 0;
  background: var(--surface);
  border-radius: var(--r-xl) var(--r-xl) 0 0;
  padding: 12px 20px calc(20px + env(safe-area-inset-bottom, 0));
  max-height: 55vh;
  transform: translateY(100%);
  transition: transform 0.35s cubic-bezier(0.32, 0.72, 0, 1);
  overflow-y: auto;
  box-shadow: 0 -8px 32px rgba(0,0,0,0.5);
}
.more-panel.open .more-panel-sheet { transform: translateY(0); }

.more-panel-handle {
  width: 40px;
  height: 4px;
  border-radius: 2px;
  background: var(--surface-4);
  margin: 0 auto 16px;
}

.more-panel-title {
  font-size: 12px;
  font-weight: 700;
  color: var(--text-2);
  text-transform: uppercase;
  letter-spacing: 0.08em;
  margin-bottom: 12px;
}

.more-panel-grid {
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  gap: 8px;
}

.more-tool {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 6px;
  padding: 14px 8px;
  background: var(--surface-2);
  border: 1px solid var(--border);
  border-radius: var(--r-md);
  cursor: pointer;
  transition: all 0.15s;
  font-family: inherit;
  color: var(--text-2);
  font-size: 10px;
  font-weight: 600;
}
.more-tool:active { background: var(--surface-3); }
.more-tool svg { width: 22px; height: 22px; color: var(--accent); }
</style>
</head>
<body>

<!-- ===== TOP BAR ===== -->
<header class="topbar" id="appHeaderHome">
  <svg class="topbar-logo" viewBox="0 0 28 28" fill="none" xmlns="http://www.w3.org/2000/svg">
    <rect width="28" height="28" rx="7" fill="rgba(212,168,83,0.12)"/>
    <circle cx="14" cy="14" r="6" stroke="#d4a853" stroke-width="1.5" fill="none"/>
    <circle cx="14" cy="14" r="2.5" fill="#d4a853"/>
    <path d="M8 14h3M17 14h3M14 8v3M14 17v3" stroke="#d4a853" stroke-width="1.5" stroke-linecap="round"/>
  </svg>
  <span class="topbar-title">DuctCalc Pro</span>
  <span class="topbar-badge">V6</span>
</header>

<!-- Hidden nav-tabs for JS compatibility -->
<div style="display:none">
  <button class="nav-tab active" data-page="roomcfm"></button>
  <button class="nav-tab" data-page="system"></button>
  <button class="nav-tab" data-page="calculator"></button>
  <button class="nav-tab" data-page="eqlen"></button>
  <button class="nav-tab" data-page="frworksheet"></button>
  <button class="nav-tab" data-page="filters"></button>
  <button class="nav-tab" data-page="psychro"></button>
</div>

<!-- ========================================
     HOME PAGE — Dashboard Design
     ======================================== -->
<div id="page-home" class="page active">
<div class="app-container">

  <!-- Status summary -->
  <div class="dash-status">
    <div class="dash-status-label">Current Project</div>
    <div class="dash-status-value">No active project — <span class="highlight">start designing</span></div>
  </div>

  <!-- Quick Actions -->
  <div class="dash-section-label">Quick Actions</div>
  <div class="dash-actions">
    <div class="dash-action" data-home-nav="roomcfm">
      <div class="dash-action-icon design">
        <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M3 9l9-7 9 7v11a2 2 0 01-2 2H5a2 2 0 01-2-2z"/><polyline points="9 22 9 12 15 12 15 22"/></svg>
      </div>
      <div class="dash-action-text">
        <div class="dash-action-title">Design a System</div>
        <div class="dash-action-desc">Room-by-room CFM, full duct layout wizard</div>
      </div>
      <div class="dash-action-arrow"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M9 18l6-6-6-6"/></svg></div>
    </div>
    <div class="dash-action" data-home-nav="calculator">
      <div class="dash-action-icon calc">
        <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><rect x="4" y="2" width="16" height="20" rx="2"/><line x1="8" y1="6" x2="16" y2="6"/><line x1="8" y1="10" x2="10" y2="10"/><line x1="14" y1="10" x2="16" y2="10"/><line x1="8" y1="14" x2="10" y2="14"/><line x1="14" y1="14" x2="16" y2="14"/><line x1="8" y1="18" x2="16" y2="18"/></svg>
      </div>
      <div class="dash-action-text">
        <div class="dash-action-title">Quick Calculator</div>
        <div class="dash-action-desc">Duct size, velocity, friction rate lookup</div>
      </div>
      <div class="dash-action-arrow"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M9 18l6-6-6-6"/></svg></div>
    </div>
  </div>

  <!-- Tools Grid -->
  <div class="dash-section-label">Tools</div>
  <div class="dash-tools">
    <div class="dash-tool" data-home-nav="eqlen">
      <div class="dash-tool-icon eqlen"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M21 16V8a2 2 0 00-1-1.73l-7-4a2 2 0 00-2 0l-7 4A2 2 0 003 8v8a2 2 0 001 1.73l7 4a2 2 0 002 0l7-4A2 2 0 0021 16z"/></svg></div>
      <div class="dash-tool-name">EQ Length Tables</div>
      <div class="dash-tool-desc">Fitting equivalent lengths per Manual D</div>
    </div>
    <div class="dash-tool" data-home-nav="frworksheet">
      <div class="dash-tool-icon frwork"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M14 2H6a2 2 0 00-2 2v16a2 2 0 002 2h12a2 2 0 002-2V8z"/><polyline points="14 2 14 8 20 8"/></svg></div>
      <div class="dash-tool-name">FR Worksheet</div>
      <div class="dash-tool-desc">Friction rate calculation sheet</div>
    </div>
    <div class="dash-tool" data-home-nav="filters">
      <div class="dash-tool-icon filter"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><polygon points="22 3 2 3 10 12.46 10 19 14 21 14 12.46 22 3"/></svg></div>
      <div class="dash-tool-name">Filter Database</div>
      <div class="dash-tool-desc">Pressure drop by manufacturer &amp; model</div>
    </div>
    <div class="dash-tool" data-home-nav="psychro">
      <div class="dash-tool-icon psychro"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M14 14.76V3.5a2.5 2.5 0 00-5 0v11.26a4.5 4.5 0 105 0z"/></svg></div>
      <div class="dash-tool-name">Psychrometric</div>
      <div class="dash-tool-desc">Air properties calculator &amp; chart</div>
    </div>
  </div>

  <!-- Recent Projects -->
  <div class="dash-section-label">Recent Projects</div>
  <div class="dash-recent">
    <div class="dash-recent-icon"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M13 2H6a2 2 0 00-2 2v16a2 2 0 002 2h12a2 2 0 002-2V9z"/><polyline points="13 2 13 9 20 9"/></svg></div>
    <div class="dash-recent-title">No projects yet</div>
    <div class="dash-recent-desc">Your completed system designs will appear here</div>
  </div>

  <div class="dash-footer">
    <a href="https://www.perplexity.ai/computer" target="_blank" rel="noopener noreferrer">Created with Perplexity Computer</a>
  </div>

</div>
</div>

<!-- ========================================
     ROOM CFM PAGE — Expandable List
     ======================================== -->
<div id="page-roomcfm" class="page">
<div class="app-container">

  <div class="room-header-bar">
    <div class="room-header-title">Rooms</div>
    <button class="room-header-btn" id="roomAddBtn">+ Add Room</button>
  </div>

  <!-- House Tightness -->
  <div class="tightness-panel">
    <div class="tightness-title">
      <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M3 12a9 9 0 1 0 18 0 9 9 0 0 0-18 0M12 8v4M12 16h.01"/></svg>
      House Tightness
    </div>
    <div class="tightness-selector" id="roomTightnessSelect"></div>
    <div class="tightness-desc" id="roomTightnessDesc"></div>
  </div>

  <!-- Room List -->
  <div id="roomCfmList"></div>

  <!-- Totals -->
  <div class="panel" style="margin-top:12px">
    <div class="panel-title">
      <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M22 12h-4l-3 9L9 3l-3 9H2"/></svg>
      System Summary
    </div>
    <div class="results-grid">
      <div class="result-card">
        <div class="result-value" id="roomTotalCfm">0</div>
        <div class="result-unit">CFM</div>
        <div class="result-label">Total Airflow</div>
      </div>
      <div class="result-card">
        <div class="result-value" id="roomTotalTons">0</div>
        <div class="result-unit">tons</div>
        <div class="result-label">Est. System Size</div>
      </div>
    </div>
    <div class="results-grid">
      <div class="result-card">
        <div class="result-value" id="roomTotalSqft">0</div>
        <div class="result-unit">ft²</div>
        <div class="result-label">Total Area</div>
      </div>
      <div class="result-card">
        <div class="result-value" id="roomTotalVol">0</div>
        <div class="result-unit">ft³</div>
        <div class="result-label">Total Volume</div>
      </div>
    </div>
  </div>

  <div class="info-note" style="margin-top:8px">
    <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><circle cx="12" cy="12" r="10"/><path d="M12 16v-4M12 8h.01"/></svg>
    <span>CFM per room based on ACCA guidelines: Bedrooms ~0.7-0.8 CFM/ft², Living/Great ~1.0 CFM/ft², Kitchen ~1.2 CFM/ft². Adjusted by house tightness.</span>
  </div>

</div>
</div>

'''

# Now continue with the calculator page
html += '''
<!-- ========================================
     CALCULATOR PAGE — Dial Design
     ======================================== -->
<div id="page-calculator" class="page">
<div class="app-container">

  <!-- Mode Toggle -->
  <div class="mode-toggle">
    <button class="mode-toggle-btn active" id="modeForwardBtn" onclick="document.getElementById('forwardMode').style.display='';document.getElementById('reverseMode').style.display='none';document.getElementById('forwardResults').style.display='';this.classList.add('active');document.getElementById('modeReverseBtn').classList.remove('active');">Forward</button>
    <button class="mode-toggle-btn" id="modeReverseBtn" onclick="document.getElementById('forwardMode').style.display='none';document.getElementById('reverseMode').style.display='';document.getElementById('forwardResults').style.display='none';this.classList.add('active');document.getElementById('modeForwardBtn').classList.remove('active');">Reverse</button>
  </div>

  <input type="hidden" id="cfmInput" value="400">
  <div id="forwardMode">

    <!-- Config row -->
    <div class="config-row">
      <div class="seg-control" id="shapeControl">
        <button class="seg-btn active" data-shape="round">Round</button>
        <button class="seg-btn" data-shape="rect">Rect</button>
      </div>
      <div class="seg-control" id="airPathControl">
        <button class="seg-btn active" data-airpath="supply">Supply</button>
        <button class="seg-btn" data-airpath="return">Return</button>
      </div>
      <div class="seg-control" id="materialControl">
        <button class="seg-btn active" data-material="metal">Metal</button>
        <button class="seg-btn" data-material="flex">Flex</button>
      </div>
    </div>

    <div class="config-row">
      <div class="config-group" id="insulatedGroup">
        <input type="checkbox" id="insulatedToggle">
        <label for="insulatedToggle">Insulated / Lined</label>
      </div>
      <div class="seg-control" id="segmentControl">
        <button class="seg-btn active" data-segment="trunk">Trunk</button>
        <button class="seg-btn" data-segment="branch">Branch</button>
        <button class="seg-btn" data-segment="runout">Runout</button>
      </div>
    </div>

    <!-- Compression Section -->
    <div id="compressionSection" style="display:none">
      <div class="compression-section">
        <div class="slider-header">
          <span class="slider-label">Flex Compression</span>
          <div style="display:flex;align-items:center;gap:4px">
            <input type="range" class="compression-slider" id="compressionSlider" min="4" max="30" value="4" step="1" style="width:100px">
            <input type="number" class="slider-value-input" id="compressionInput" value="4" min="4" max="30" step="1" style="width:52px;text-align:center">
            <span style="font-size:10px;color:var(--text-3)">%</span>
          </div>
        </div>
        <div class="compression-presets">
          <button data-compression="4" class="active">4% min</button>
          <button data-compression="10">10%</button>
          <button data-compression="15">15%</button>
          <button data-compression="20">20%</button>
          <button data-compression="30">30%</button>
        </div>
        <div class="compression-impact low" id="compressionImpact">4% compressed — minimum realistic install</div>
      </div>
    </div>

    <!-- DIAL — CFM -->
    <div class="dial-container">
      <svg class="dial-ring" viewBox="0 0 200 200">
        <circle class="dial-ring-bg" cx="100" cy="100" r="88"/>
        <circle class="dial-ring-fill" id="dialRingFill" cx="100" cy="100" r="88"
                stroke-dasharray="553" stroke-dashoffset="456"
                transform="rotate(-90 100 100)"/>
      </svg>
      <div class="dial-value">
        <input type="number" class="dial-number slider-value-input" id="cfmSliderVal" value="400" min="50" max="5000" step="25" style="width:100px;background:transparent;border:none;text-align:center;font-size:36px;color:var(--text);font-weight:700">
        <span class="dial-unit">CFM</span>
      </div>
    </div>
    <div class="dial-slider-wrap">
      <input type="range" class="cfm-slider" id="cfmSlider" min="50" max="2000" value="400" step="25">
    </div>

    <!-- Size controls -->
    <div class="slider-panel" id="roundSizeGroup">
      <div class="slider-header">
        <span class="slider-label">Duct Diameter</span>
        <div style="display:flex;align-items:center;gap:4px">
          <input type="number" class="slider-value-input" id="roundSizeVal" value="10" min="4" max="24" step="1">
          <span style="font-size:10px;color:var(--text-3)">in</span>
        </div>
      </div>
      <input type="range" class="cfm-slider" id="roundSizeSlider" min="0" max="13" value="6" step="1">
    </div>

    <div id="rectWGroup" style="display:none">
      <div class="slider-panel">
        <div class="slider-header">
          <span class="slider-label">Width</span>
          <div style="display:flex;align-items:center;gap:4px">
            <input type="number" class="slider-value-input" id="rectWVal" value="10" min="4" max="30" step="1">
            <span style="font-size:10px;color:var(--text-3)">in</span>
          </div>
        </div>
        <input type="range" class="cfm-slider" id="rectWSlider" min="0" max="11" value="2" step="1">
      </div>
      <div class="slider-panel">
        <div class="slider-header">
          <span class="slider-label">Height</span>
          <div style="display:flex;align-items:center;gap:4px">
            <input type="number" class="slider-value-input" id="rectHVal" value="8" min="4" max="20" step="1">
            <span style="font-size:10px;color:var(--text-3)">in</span>
          </div>
        </div>
        <input type="range" class="cfm-slider" id="rectHSlider" min="0" max="9" value="2" step="1">
      </div>
    </div>

    <!-- Friction Rate slider -->
    <div class="slider-panel">
      <div class="slider-header">
        <span class="slider-label">Friction Rate</span>
        <div style="display:flex;align-items:center;gap:4px">
          <input type="number" class="slider-value-input" id="frictionInput" value="0.05" min="0.01" max="0.08" step="0.005" style="width:70px">
          <span style="font-size:10px;color:var(--text-3)">IWC/100ft</span>
        </div>
      </div>
      <input type="range" class="cfm-slider" id="frictionSlider" min="10" max="80" value="50" step="1">
    </div>

    <!-- Calc filter section -->
    <div id="calcFilterSection" style="display:none">
      <div class="panel">
        <div style="display:flex;align-items:center;gap:8px;margin-bottom:8px">
          <input type="checkbox" id="calcFilterToggle">
          <label for="calcFilterToggle" style="font-size:12px;font-weight:600;color:var(--text-2)">Include Filter PD</label>
        </div>
        <div id="calcFilterConfig" style="display:none">
          <div class="input-group"><label class="input-label">Manufacturer</label>
            <select class="input-field" id="calcFilterMfg" style="width:100%">
              <option value="">Select...</option>
            </select>
          </div>
          <div class="input-group"><label class="input-label">Model</label>
            <select class="input-field" id="calcFilterModel" style="width:100%"></select>
          </div>
          <div class="input-group"><label class="input-label">Grille Config</label>
            <select class="input-field" id="calcFilterGrille" style="width:100%">
              <option value="open">Open (no grille)</option>
              <option value="return_grille">Return Grille</option>
              <option value="stamped">Stamped Face</option>
            </select>
          </div>
          <div class="input-group"><label class="input-label">System CFM</label>
            <input type="number" class="input-field" id="calcFilterCFM" value="1200" min="200" max="5000" step="50" style="width:100%">
          </div>
          <div id="calcFilterResults" class="filter-inline-grid" style="margin-top:8px"></div>
          <div id="calcFilterWarn" style="display:none"></div>
        </div>
      </div>
    </div>
  </div>

  <!-- Reverse Mode -->
  <div id="reverseMode" style="display:none">
    <div class="config-row">
      <div class="seg-control" id="revShapeControl">
        <button class="seg-btn active" data-shape="round">Round</button>
        <button class="seg-btn" data-shape="rect">Rect</button>
      </div>
      <div class="seg-control" id="revPathControl">
        <button class="seg-btn active" data-airpath="supply">Supply</button>
        <button class="seg-btn" data-airpath="return">Return</button>
      </div>
      <div class="seg-control" id="revMaterialControl">
        <button class="seg-btn active" data-material="metal">Metal</button>
        <button class="seg-btn" data-material="flex">Flex</button>
      </div>
    </div>
    <div class="config-row">
      <div class="config-group" id="revLinedGroup">
        <input type="checkbox" id="revInsulatedToggle">
        <label for="revInsulatedToggle">Insulated / Lined</label>
      </div>
    </div>

    <div id="revRoundGroup">
      <div class="input-group"><label class="input-label">Duct Size (round)</label>
        <select class="input-field" id="revDuctSize" style="width:100%">
          <option value="4">4"</option><option value="5">5"</option><option value="6">6"</option>
          <option value="7">7"</option><option value="8">8"</option><option value="9">9"</option>
          <option value="10" selected>10"</option><option value="12">12"</option><option value="14">14"</option>
          <option value="16">16"</option><option value="18">18"</option><option value="20">20"</option>
          <option value="24">24"</option>
        </select>
      </div>
    </div>
    <div id="revRectGroup" style="display:none">
      <div style="display:flex;gap:8px">
        <div class="input-group" style="flex:1"><label class="input-label">Width</label>
          <select class="input-field" id="revRectW" style="flex:1">
            <option value="6">6"</option><option value="8">8"</option><option value="10" selected>10"</option>
            <option value="12">12"</option><option value="14">14"</option><option value="16">16"</option>
            <option value="18">18"</option><option value="20">20"</option><option value="24">24"</option>
            <option value="28">28"</option><option value="30">30"</option>
          </select>
        </div>
        <div class="input-group" style="flex:1"><label class="input-label">Height</label>
          <select class="input-field" id="revRectH" style="flex:1">
            <option value="4">4"</option><option value="6">6"</option><option value="8" selected>8"</option>
            <option value="10">10"</option><option value="12">12"</option><option value="14">14"</option>
            <option value="16">16"</option><option value="18">18"</option><option value="20">20"</option>
          </select>
        </div>
      </div>
    </div>
    <div id="revCompressionSection" style="display:none;margin-top:8px">
      <div class="compression-section">
        <div class="slider-header">
          <span class="slider-label">Compression</span>
        </div>
        <div class="compression-presets" id="revCompPresets">
          <button data-compression="4" class="active">4%</button>
          <button data-compression="10">10%</button>
          <button data-compression="15">15%</button>
          <button data-compression="20">20%</button>
          <button data-compression="30">30%</button>
        </div>
        <div style="display:flex;align-items:center;gap:4px;margin-top:4px">
          <input type="range" class="compression-slider" id="revCompSlider" min="4" max="30" value="4" step="1" style="flex:1">
          <input type="number" class="slider-value-input" id="revCompInput" value="4" min="4" max="30" step="1" style="width:52px;text-align:center">
        </div>
        <div class="compression-impact low" id="revCompImpact">4% compressed — minimum realistic install</div>
      </div>
    </div>

    <div class="panel" id="revResults" style="margin-top:10px">
      <div class="panel-title">CFM Range for Selected Duct</div>
      <div class="rev-bar-container">
        <div class="rev-bar-zone rev-bar-low" id="revBarLow"></div>
        <div class="rev-bar-zone rev-bar-ok" id="revBarOk"></div>
        <div class="rev-bar-zone rev-bar-high" id="revBarHigh"></div>
      </div>
      <div style="display:flex;justify-content:space-between;font-family:'DM Mono',monospace;font-size:12px;margin-bottom:12px">
        <span id="revMinCfm">--</span>
        <span id="revIdealCfm" style="color:var(--green);font-weight:700">--</span>
        <span id="revMaxCfm">--</span>
      </div>
      <div class="results-grid">
        <div class="result-card">
          <div class="result-value" id="revVelocityMin">--</div>
          <div class="result-unit">FPM</div>
          <div class="result-label">Min Velocity</div>
        </div>
        <div class="result-card">
          <div class="result-value green" id="revVelocityIdeal">--</div>
          <div class="result-unit">FPM</div>
          <div class="result-label">Ideal Velocity</div>
        </div>
        <div class="result-card" style="grid-column:span 2">
          <div class="result-value" id="revVelocityMax">--</div>
          <div class="result-unit">FPM</div>
          <div class="result-label">Max Velocity</div>
        </div>
      </div>
    </div>
  </div>

  <!-- Forward Results -->
  <div id="forwardResults">
    <div class="results-grid">
      <div class="result-card" id="velocityCard">
        <div class="result-value" id="velocityResult">--</div>
        <div class="result-unit">FPM</div>
        <div class="result-label">Velocity</div>
      </div>
      <div class="result-card" id="frictionCard">
        <div class="result-value" id="frictionResult">--</div>
        <div class="result-unit">IWC/100ft</div>
        <div class="result-label">Friction Loss</div>
      </div>
      <div class="result-card" id="maxCfmCard">
        <div class="result-value" id="maxCfmResult">--</div>
        <div class="result-unit">CFM</div>
        <div class="result-label">Max CFM</div>
      </div>
      <div class="result-card" id="suggestedCard">
        <div class="result-value" id="suggestedResult">--</div>
        <div class="result-unit" id="suggestedUnit">round</div>
        <div class="result-label">Suggested Size</div>
      </div>
    </div>
    <div class="results-grid">
      <div class="result-card" id="maxRunCard">
        <div class="result-value" id="maxRunResult">--</div>
        <div class="result-unit">ft</div>
        <div class="result-label">Max Run</div>
      </div>
      <div class="result-card">
        <div class="result-value" id="areaDisplay">--</div>
        <div class="result-unit">in²</div>
        <div class="result-label">Duct Area</div>
      </div>
    </div>

    <div id="statusBar" class="status-bar ok">
      <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M22 11.08V12a10 10 0 1 1-5.93-9.14"/><polyline points="22 4 12 14.01 9 11.01"/></svg>
      <span id="statusText">Enter values above</span>
    </div>
  </div>

  <div class="filter-warning-banner" id="calcFilterDisclaimer" style="display:none">
    <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" style="width:16px;height:16px;flex-shrink:0"><path d="M10.29 3.86L1.82 18a2 2 0 001.71 3h16.94a2 2 0 001.71-3L13.71 3.86a2 2 0 00-3.42 0z"/><line x1="12" y1="9" x2="12" y2="13"/><line x1="12" y1="17" x2="12.01" y2="17"/></svg>
    <span>Filter pressure drop reduces available static pressure</span>
  </div>

</div>
</div>
'''

# EQ Length page - same content, new styling already applied via CSS
html += '''
<!-- ========================================
     EQ LENGTH PAGE
     ======================================== -->
<div id="page-eqlen" class="page">
<div class="app-container">
  <div style="padding:16px 0 8px"><span style="font-size:18px;font-weight:800;letter-spacing:-0.03em">EQ Length Tables</span></div>
  <div class="panel">
    <div style="font-size:12px;color:var(--text-2);margin-bottom:12px;line-height:1.5">
      Values based on Manual D Appendix 3 tables at reference conditions (0.08 IWC friction rate, 900 FPM supply / 700 FPM return). All values in equivalent feet of straight duct.
    </div>

    <div class="eq-category">Elbows &amp; Turns</div>
    <div class="eq-table-container">
    <table class="eq-table">
      <thead><tr><th>Fitting</th><th>4"</th><th>5"</th><th>6"</th><th>7"</th><th>8"</th><th>9"</th><th>10"</th><th>12"</th><th>14"</th></tr></thead>
      <tbody>
        <tr><td>Round elbow, R/D=1.5 (smooth)</td><td>5</td><td>5</td><td>10</td><td>10</td><td>10</td><td>15</td><td>15</td><td>15</td><td>20</td></tr>
        <tr><td>Round elbow, R/D=1.0 (short)</td><td>10</td><td>10</td><td>15</td><td>15</td><td>20</td><td>20</td><td>25</td><td>30</td><td>35</td></tr>
        <tr><td>Mitered elbow, no vanes</td><td>20</td><td>25</td><td>30</td><td>35</td><td>40</td><td>50</td><td>55</td><td>65</td><td>75</td></tr>
        <tr><td>Mitered elbow, w/vanes</td><td>10</td><td>10</td><td>10</td><td>15</td><td>15</td><td>15</td><td>20</td><td>25</td><td>25</td></tr>
        <tr><td>Flex duct 90° bend (R/D≥1)</td><td>15</td><td>20</td><td>25</td><td>25</td><td>30</td><td>35</td><td>40</td><td>50</td><td>55</td></tr>
        <tr><td>Flex duct 45° bend</td><td>5</td><td>5</td><td>10</td><td>10</td><td>10</td><td>15</td><td>15</td><td>20</td><td>25</td></tr>
      </tbody>
    </table>
    </div>

    <div class="eq-category">Supply Boots &amp; Register Connections</div>
    <div class="eq-table-container">
    <table class="eq-table">
      <thead><tr><th>Fitting</th><th>EQ Length (ft)</th></tr></thead>
      <tbody>
        <tr><td>Boot, straight (round to rectangular)</td><td>35</td></tr>
        <tr><td>Boot, 90° (round to rectangular)</td><td>55</td></tr>
        <tr><td>Boot, 90° w/ext plenum</td><td>40</td></tr>
        <tr><td>Boot, side takeoff (straight)</td><td>35</td></tr>
        <tr><td>Ceiling diffuser box, top entry</td><td>10</td></tr>
        <tr><td>Ceiling diffuser box, side entry</td><td>40</td></tr>
        <tr><td>Register face (2x10, 2x12, 2x14)</td><td>40 - 50</td></tr>
        <tr><td>4x10 floor register</td><td>30</td></tr>
        <tr><td>4x12 floor register</td><td>35</td></tr>
        <tr><td>4x14 floor register</td><td>40</td></tr>
        <tr><td>6x10 return grille</td><td>15</td></tr>
        <tr><td>6x12 return grille</td><td>15</td></tr>
        <tr><td>8x14 return grille</td><td>10</td></tr>
        <tr><td>10x10 return grille</td><td>10</td></tr>
        <tr><td>12x12 return grille</td><td>5</td></tr>
        <tr><td>14x6 return grille</td><td>15</td></tr>
        <tr><td>14x20 return grille</td><td>5</td></tr>
        <tr><td>20x20 return grille</td><td>5</td></tr>
        <tr><td>20x25 return/filter grille</td><td>5</td></tr>
        <tr><td>25x16 return/filter grille</td><td>5</td></tr>
        <tr><td>25x20 return/filter grille</td><td>5</td></tr>
      </tbody>
    </table>
    </div>

    <div class="eq-category">Transitions &amp; Takeoffs</div>
    <div class="eq-table-container">
    <table class="eq-table">
      <thead><tr><th>Fitting</th><th>EQ Length (ft)</th></tr></thead>
      <tbody>
        <tr><td>Trunk reducer (gradual)</td><td>Negligible</td></tr>
        <tr><td>Trunk reducer (abrupt)</td><td>10 - 15</td></tr>
        <tr><td>Branch takeoff, conical (round)</td><td>5 - 15</td></tr>
        <tr><td>Branch takeoff, 90° straight (round)</td><td>35</td></tr>
        <tr><td>Branch takeoff, 45° angle (round)</td><td>20</td></tr>
        <tr><td>Wye branch, 45°</td><td>10</td></tr>
        <tr><td>Tee (straight through)</td><td>10</td></tr>
        <tr><td>Tee (branch)</td><td>35</td></tr>
        <tr><td>Starting collar (plenum)</td><td>5 - 10</td></tr>
        <tr><td>Damper (fully open)</td><td>10</td></tr>
      </tbody>
    </table>
    </div>

    <div class="eq-category">Return Fittings</div>
    <div class="eq-table-container">
    <table class="eq-table">
      <thead><tr><th>Fitting</th><th>EQ Length (ft)</th></tr></thead>
      <tbody>
        <tr><td>Return air drop, straight down</td><td>5</td></tr>
        <tr><td>Return air drop, 90° turn</td><td>50</td></tr>
        <tr><td>Filter grille to plenum (straight)</td><td>5</td></tr>
        <tr><td>Filter grille to plenum (90° turn)</td><td>40</td></tr>
        <tr><td>Return grille, flush (large)</td><td>5</td></tr>
        <tr><td>Joist panning (per 14ft section)</td><td>55</td></tr>
        <tr><td>Return box / platform return</td><td>30</td></tr>
      </tbody>
    </table>
    </div>

    <div class="info-note" style="margin-top:16px">
      <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><circle cx="12" cy="12" r="10"/><path d="M12 16v-4M12 8h.01"/></svg>
      <span>These are reference values from Manual D Appendix 3. Actual equivalent lengths vary with velocity and friction rate.</span>
    </div>
  </div>
</div>
</div>
'''

# Now read the system page, frworksheet, filters, psychro from the backup (lines 3254 onward)
# We need to reproduce them with all their IDs intact but with new CSS classes applied
# The system page is huge — let's read it from the backup

import re

with open('/home/user/workspace/ductulator-pro/index-v4-backup.html', 'r') as f:
    backup = f.read()

# Extract system page section
sys_start = backup.index('<div id="page-system" class="page">')
# Find the end - it's before page-frworksheet
sys_end = backup.index('<div id="page-frworksheet" class="page">')
system_html = backup[sys_start:sys_end]

# Extract frworksheet section
fr_start = backup.index('<div id="page-frworksheet" class="page">')
fr_end = backup.index('<div id="page-filters" class="page">')
frworksheet_html = backup[fr_start:fr_end]

# Extract filters section
filt_start = backup.index('<div id="page-filters" class="page">')
filt_end = backup.index('<div id="page-psychro" class="page">')
filters_html = backup[filt_start:filt_end]

# Extract psychro section
psychro_start = backup.index('<div id="page-psychro" class="page">')
# Find the end of page-psychro - it ends before the next closing div that isn't part of it
# Let's find the script block that follows
psychro_end_marker = '<!-- ===== BOTTOM NAV ====='
psychro_end = backup.index(psychro_end_marker)
psychro_html = backup[psychro_start:psychro_end]

html += '\n\n<!-- ========================================\n     SYSTEM PAGE\n     ======================================== -->\n'
html += system_html
html += '\n\n<!-- ========================================\n     FR WORKSHEET PAGE\n     ======================================== -->\n'
html += frworksheet_html
html += '\n\n<!-- ========================================\n     FILTERS PAGE\n     ======================================== -->\n'
html += filters_html
html += '\n\n<!-- ========================================\n     PSYCHROMETRIC PAGE\n     ======================================== -->\n'
html += psychro_html

# Bottom nav
html += '''

<!-- ===== BOTTOM NAV ===== -->
<nav class="bottom-nav" id="bottomNav">
  <button class="bottom-nav-item active" data-page="roomcfm">
    <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M3 9l9-7 9 7v11a2 2 0 01-2 2H5a2 2 0 01-2-2z"/><polyline points="9 22 9 12 15 12 15 22"/></svg>
    <span>Rooms</span>
  </button>
  <button class="bottom-nav-item" data-page="system">
    <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><circle cx="12" cy="12" r="3"/><path d="M19.4 15a1.65 1.65 0 00.33 1.82l.06.06a2 2 0 010 2.83 2 2 0 01-2.83 0l-.06-.06a1.65 1.65 0 00-1.82-.33 1.65 1.65 0 00-1 1.51V21a2 2 0 01-2 2 2 2 0 01-2-2v-.09A1.65 1.65 0 009 19.4a1.65 1.65 0 00-1.82.33l-.06.06a2 2 0 01-2.83 0 2 2 0 010-2.83l.06-.06A1.65 1.65 0 004.68 15a1.65 1.65 0 00-1.51-1H3a2 2 0 01-2-2 2 2 0 012-2h.09A1.65 1.65 0 004.6 9a1.65 1.65 0 00-.33-1.82l-.06-.06a2 2 0 010-2.83 2 2 0 012.83 0l.06.06A1.65 1.65 0 009 4.68a1.65 1.65 0 001-1.51V3a2 2 0 012-2 2 2 0 012 2v.09a1.65 1.65 0 001 1.51 1.65 1.65 0 001.82-.33l.06-.06a2 2 0 012.83 0 2 2 0 010 2.83l-.06.06a1.65 1.65 0 00-.33 1.82V9a1.65 1.65 0 001.51 1H21a2 2 0 012 2 2 2 0 01-2 2h-.09a1.65 1.65 0 00-1.51 1z"/></svg>
    <span>System</span>
  </button>
  <button class="bottom-nav-item" id="moreNavBtn">
    <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><circle cx="12" cy="12" r="1"/><circle cx="12" cy="5" r="1"/><circle cx="12" cy="19" r="1"/></svg>
    <span>More</span>
  </button>
</nav>

<!-- ===== MORE PANEL ===== -->
<div class="more-panel" id="morePanel">
  <div class="more-panel-overlay" id="morePanelOverlay"></div>
  <div class="more-panel-sheet">
    <div class="more-panel-handle"></div>
    <div class="more-panel-title">Tools</div>
    <div class="more-panel-grid">
      <button class="more-tool" data-page="calculator">
        <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><rect x="4" y="2" width="16" height="20" rx="2"/><line x1="8" y1="6" x2="16" y2="6"/><line x1="8" y1="10" x2="10" y2="10"/><line x1="14" y1="10" x2="16" y2="10"/><line x1="8" y1="14" x2="10" y2="14"/><line x1="14" y1="14" x2="16" y2="14"/><line x1="8" y1="18" x2="16" y2="18"/></svg>
        <span>Calculator</span>
      </button>
      <button class="more-tool" data-page="eqlen">
        <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M21 16V8a2 2 0 00-1-1.73l-7-4a2 2 0 00-2 0l-7 4A2 2 0 003 8v8a2 2 0 001 1.73l7 4a2 2 0 002 0l7-4A2 2 0 0021 16z"/><polyline points="3.27 6.96 12 12.01 20.73 6.96"/><line x1="12" y1="22.08" x2="12" y2="12"/></svg>
        <span>EQ Length</span>
      </button>
      <button class="more-tool" data-page="frworksheet">
        <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M14 2H6a2 2 0 00-2 2v16a2 2 0 002 2h12a2 2 0 002-2V8z"/><polyline points="14 2 14 8 20 8"/><line x1="16" y1="13" x2="8" y2="13"/><line x1="16" y1="17" x2="8" y2="17"/><polyline points="10 9 9 9 8 9"/></svg>
        <span>FR Worksheet</span>
      </button>
      <button class="more-tool" data-page="filters">
        <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><polygon points="22 3 2 3 10 12.46 10 19 14 21 14 12.46 22 3"/></svg>
        <span>Filters</span>
      </button>
      <button class="more-tool" data-page="psychro">
        <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M14 14.76V3.5a2.5 2.5 0 00-5 0v11.26a4.5 4.5 0 105 0z"/></svg>
        <span>Psychrometric</span>
      </button>
    </div>
  </div>
</div>
'''

# Add the JS blocks
html += '\n<script>\n'
html += js_block_1
html += '\n</script>\n'

# Add the dial sync script BEFORE the nav handler
html += '''
<script>
// ===== Dial Ring Sync =====
(function() {
  var cfmSlider = document.getElementById('cfmSlider');
  var cfmSliderVal = document.getElementById('cfmSliderVal');
  var dialRingFill = document.getElementById('dialRingFill');
  var circumference = 2 * Math.PI * 88; // r=88

  function updateDialRing() {
    var min = parseFloat(cfmSlider.min);
    var max = parseFloat(cfmSlider.max);
    var val = parseFloat(cfmSlider.value);
    var pct = (val - min) / (max - min);
    var offset = circumference * (1 - pct);
    if (dialRingFill) {
      dialRingFill.setAttribute('stroke-dasharray', circumference);
      dialRingFill.setAttribute('stroke-dashoffset', offset);
    }
  }

  // Sync cfmSlider -> dial ring
  if (cfmSlider) {
    cfmSlider.addEventListener('input', updateDialRing);
    // Also listen for programmatic changes
    var origCfmSliderSet = Object.getOwnPropertyDescriptor(HTMLInputElement.prototype, 'value').set;
    // Initial update
    updateDialRing();
  }

  // Also sync when cfmSliderVal changes (from typing)
  if (cfmSliderVal) {
    cfmSliderVal.addEventListener('input', function() {
      setTimeout(updateDialRing, 50);
    });
  }

  // Observe slider value changes
  setInterval(updateDialRing, 200);
})();
</script>
'''

html += '\n<script>\n'
html += js_block_2
html += '\n</script>\n'

html += '\n<script>\n'
html += js_block_3
html += '\n</script>\n'

html += '\n</body>\n</html>'

# Write the output
with open('/home/user/workspace/ductulator-pro/index.html', 'w') as f:
    f.write(html)

print(f"Written {len(html)} bytes to index.html")
print(f"Total lines: {html.count(chr(10))}")
