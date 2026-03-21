#!/usr/bin/env python3
"""
DuctCalc Pro — Premium Redesign V2 
Replaces CSS while preserving all HTML structure, IDs, data attributes, and scripts.
"""
import re

with open('index.html', 'r') as f:
    content = f.read()

# ============================================================
# STEP 1: Extract and preserve script blocks
# ============================================================
# We need to find the two script blocks and preserve them exactly

# ============================================================  
# STEP 2: Replace the first <style> block (lines 28-2346)
# ============================================================
# Find the first style block
first_style_start = content.index('<style>\n/* ===== DuctCalc Pro')
first_style_end = content.index('</style>\n</head>') + len('</style>')

# Find the second style block (wizard styles)
second_style_start = content.index('<style>\n/* ===== WIZARD STEP BAR')
second_style_end = content.index('.wiz-crit-label {')
# Find the end of the second style block
second_style_end = content.index('</style>', second_style_start) + len('</style>')

# ============================================================
# STEP 3: Build new CSS
# ============================================================
new_css_1 = '''<style>
/* ===== DuctCalc Pro V2 — Midnight Forge Design System ===== */
:root {
  /* Surfaces */
  --bg-0: #08090c;
  --bg-1: #0e1017;
  --bg-2: #151821;
  --bg-3: #1c1f2b;
  --bg-4: #252936;

  /* Borders */
  --border-subtle: rgba(255,255,255,0.06);
  --border-default: rgba(255,255,255,0.10);
  --border-strong: rgba(255,255,255,0.16);

  /* Text */
  --text-0: #f0f0f5;
  --text-1: #c8c8d4;
  --text-2: #8888a0;
  --text-3: #555570;

  /* Accent — Cobalt Blue */
  --accent: #4f8cff;
  --accent-strong: #3b7bff;
  --accent-subtle: rgba(79,140,255,0.12);
  --accent-glow: 0 0 20px rgba(79,140,255,0.15);

  /* Semantic */
  --green: #34d399;
  --green-subtle: rgba(52,211,153,0.12);
  --amber: #fbbf24;
  --amber-subtle: rgba(251,191,36,0.12);
  --red: #f87171;
  --red-subtle: rgba(248,113,113,0.12);

  /* Supply/Return */
  --supply-color: #f87171;
  --return-color: #fbbf24;
  --airflow-color: #34d399;

  /* Type scale */
  --text-xs: 10px;
  --text-sm: 12px;
  --text-base: 14px;
  --text-lg: 16px;
  --text-xl: 18px;
  --text-2xl: 24px;
  --text-3xl: 32px;

  /* Legacy aliases — JS uses these in inline styles */
  --bg-primary: #08090c;
  --bg-card: #151821;
  --bg-elevated: #1c1f2b;
  --bg-input: #0e1017;
  --border: rgba(255,255,255,0.10);
  --border-focus: #4f8cff;
  --text-primary: #f0f0f5;
  --text-secondary: #8888a0;
  --text-tertiary: #555570;
  --accent-hover: #3b7bff;
  --accent-glow-legacy: rgba(79,140,255,0.15);
  --success: #34d399;
  --warning: #fbbf24;
  --danger: #f87171;
  --supply: #f87171;
  --return: #fbbf24;
  --airflow: #34d399;
  --red-glow: #4f8cff;
  --red-dark: #3b7bff;
  --bg: #08090c;
  --surface: #151821;
  --surface-2: #1c1f2b;
  --surface-3: #252936;
  --border-light: rgba(255,255,255,0.16);
  --text: #f0f0f5;
  --text-muted: #8888a0;
  --text-dim: #555570;
  --yellow: #fbbf24;
  --orange: #fbbf24;
  --blue: #4f8cff;
  --card-shadow: none;
  --glow-red: 0 0 20px rgba(79,140,255,0.15);
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
  background: var(--bg-0);
  color: var(--text-0);
  min-height: 100dvh;
  overflow-x: hidden;
  padding-bottom: 72px;
  line-height: 1.5;
}

/* Mono for numbers */
.mono, [class*="result-val"], [class*="cfm"], input[type="number"],
.slider-value-input, .fr-input, .fr-result, .wiz-result-val,
.compression-readout-value, .dial-readout-value {
  font-family: 'JetBrains Mono', monospace;
  font-feature-settings: 'tnum';
}

/* ===== SCROLLBAR ===== */
::-webkit-scrollbar { width: 4px; }
::-webkit-scrollbar-track { background: transparent; }
::-webkit-scrollbar-thumb { background: rgba(255,255,255,0.08); border-radius: 2px; }
::-webkit-scrollbar-thumb:hover { background: rgba(255,255,255,0.14); }

/* ===== APP HEADER ===== */
.app-header {
  position: sticky;
  top: 0;
  z-index: 100;
  padding: 12px 20px;
  background: rgba(8,9,12,0.8);
  backdrop-filter: blur(16px);
  -webkit-backdrop-filter: blur(16px);
  border-bottom: 1px solid var(--border-subtle);
  display: flex;
  align-items: center;
  min-height: 52px;
}

.app-header-brand {
  display: flex;
  flex-direction: column;
}

.app-header-name {
  font-size: var(--text-lg);
  font-weight: 700;
  color: var(--text-0);
  letter-spacing: -0.02em;
  line-height: 1.2;
}

.app-header-tagline {
  font-size: var(--text-xs);
  color: var(--text-3);
  text-transform: uppercase;
  letter-spacing: 0.08em;
  font-weight: 600;
}

/* ===== OLD NAV (hidden) ===== */
.nav { display: none !important; }
.nav-tabs { display: none; }
.nav-tab { display: none; }

/* ===== BOTTOM NAV ===== */
.bottom-nav {
  position: fixed;
  bottom: 0;
  left: 0;
  right: 0;
  height: 56px;
  background: rgba(8,9,12,0.85);
  backdrop-filter: blur(20px);
  -webkit-backdrop-filter: blur(20px);
  border-top: 1px solid var(--border-subtle);
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
  font-size: 10px;
  font-weight: 600;
  letter-spacing: 0.04em;
  text-transform: uppercase;
  transition: color 0.2s;
  -webkit-tap-highlight-color: transparent;
  touch-action: manipulation;
  cursor: pointer;
  background: none;
  border: none;
  padding: 6px 20px;
  font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif;
}

.bottom-nav-item.active { color: var(--accent); }
.bottom-nav-item svg { width: 22px; height: 22px; stroke-width: 1.5; }

/* ===== MORE PANEL ===== */
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
  backdrop-filter: blur(4px);
  -webkit-backdrop-filter: blur(4px);
  -webkit-tap-highlight-color: transparent;
}

.more-panel-sheet {
  position: absolute;
  bottom: 0;
  left: 0;
  right: 0;
  background: var(--bg-2);
  border-radius: 24px 24px 0 0;
  padding: 12px 20px 40px;
  max-height: 60vh;
  transform: translateY(100%);
  transition: transform 0.3s cubic-bezier(0.32, 0.72, 0, 1);
  padding-bottom: calc(40px + env(safe-area-inset-bottom, 0));
  overflow-y: auto;
}
.more-panel.open .more-panel-sheet { transform: translateY(0); }

.more-panel-handle {
  width: 36px;
  height: 4px;
  border-radius: 2px;
  background: var(--text-3);
  margin: 0 auto 16px;
}

.more-panel-title {
  font-size: var(--text-sm);
  font-weight: 700;
  color: var(--text-0);
  letter-spacing: 0.04em;
  text-transform: uppercase;
  margin-bottom: 16px;
}

.more-panel-grid {
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  gap: 10px;
}

.more-tool {
  background: var(--bg-3);
  border: 1px solid var(--border-subtle);
  border-radius: 16px;
  padding: 20px 12px;
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 8px;
  transition: all 0.15s;
  cursor: pointer;
  -webkit-tap-highlight-color: transparent;
  touch-action: manipulation;
  color: var(--text-1);
  font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif;
  font-size: 11px;
  font-weight: 600;
  border: 1px solid var(--border-default);
}
.more-tool:active {
  transform: scale(0.95);
  background: var(--bg-4);
  border-color: var(--accent);
  color: var(--accent);
}
.more-tool svg { width: 24px; height: 24px; }

/* ===== PAGE VIEWS ===== */
.page {
  display: none;
  opacity: 0;
  transform: translateY(6px);
  will-change: transform, opacity;
}
.page.active {
  display: block;
  animation: pageIn 0.3s ease-out forwards;
}
@keyframes pageIn {
  from { opacity: 0; transform: translateY(6px); }
  to { opacity: 1; transform: translateY(0); }
}

/* ===== CARDS (iOS-style grouped sections) ===== */
.section-card, .panel {
  background: var(--bg-2);
  border: 1px solid var(--border-subtle);
  border-radius: 20px;
  padding: 20px;
  margin-bottom: 12px;
}

.section-title, .panel-title {
  font-size: var(--text-sm);
  font-weight: 600;
  text-transform: uppercase;
  letter-spacing: 0.08em;
  color: var(--accent);
  margin-bottom: 12px;
  display: flex;
  align-items: center;
  gap: 8px;
}
.section-title svg, .panel-title svg { width: 18px; height: 18px; }

/* ===== MAIN LAYOUT ===== */
.app-container {
  max-width: 900px;
  margin: 0 auto;
  padding: 16px 20px;
}

/* ===== DIAL / RESULTS HEADER ===== */
.dial-section {
  display: flex;
  flex-direction: column;
  align-items: center;
  margin-bottom: 20px;
}
.dial-container {
  position: relative;
  width: 280px;
  height: 280px;
  touch-action: none;
  user-select: none;
  margin-bottom: 12px;
}
.dial-svg { width: 100%; height: 100%; }
.dial-readout { text-align: center; }
.dial-readout-value {
  font-family: 'JetBrains Mono', monospace;
  font-size: 42px;
  font-weight: 700;
  color: var(--accent);
  line-height: 1;
}
.dial-readout-label {
  font-size: var(--text-sm);
  color: var(--text-2);
  letter-spacing: 0.02em;
  text-transform: uppercase;
  margin-top: 2px;
}
.dial-param-select { display: flex; gap: 6px; margin-top: 10px; }
.dial-param-btn {
  padding: 6px 14px;
  border-radius: 20px;
  font-size: 11px;
  font-weight: 600;
  color: var(--text-2);
  background: var(--bg-3);
  border: 1px solid var(--border-default);
  cursor: pointer;
  transition: all 0.2s;
  -webkit-tap-highlight-color: transparent;
  touch-action: manipulation;
}
.dial-param-btn.active {
  color: #fff;
  background: var(--accent);
  border-color: var(--accent);
  box-shadow: 0 2px 8px rgba(79,140,255,0.3);
}

/* ===== INPUT FIELDS ===== */
.input-grid {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 10px;
}
.input-group {
  display: flex;
  flex-direction: column;
  gap: 6px;
}
.input-group.full-width { grid-column: 1 / -1; }

.input-label {
  font-size: var(--text-xs);
  font-weight: 600;
  text-transform: uppercase;
  letter-spacing: 0.06em;
  color: var(--text-2);
  display: block;
}

.input-field {
  background: var(--bg-1);
  border: 1.5px solid var(--border-default);
  border-radius: 14px;
  padding: 14px 16px;
  font-size: var(--text-base);
  color: var(--text-0);
  width: 100%;
  height: 48px;
  transition: border-color 0.2s, box-shadow 0.2s;
  outline: none;
  -webkit-appearance: none;
  font-family: 'JetBrains Mono', monospace;
  font-weight: 500;
}
.input-field:focus {
  border-color: var(--accent);
  box-shadow: var(--accent-glow);
}
.input-field::placeholder { color: var(--text-3); }

select.input-field {
  cursor: pointer;
  appearance: none;
  font-family: 'Inter', -apple-system, sans-serif;
  background-image: url("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' width='12' height='12' viewBox='0 0 24 24' fill='none' stroke='%238888a0' stroke-width='2'%3E%3Cpolyline points='6,9 12,15 18,9'/%3E%3C/svg%3E");
  background-repeat: no-repeat;
  background-position: right 14px center;
  padding-right: 36px;
}

/* ===== TOGGLE SWITCHES ===== */
.toggle-row {
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 8px 0;
}
.toggle-label {
  font-size: 13px;
  font-weight: 500;
  color: var(--text-0);
}
.toggle-switch {
  position: relative;
  width: 44px;
  height: 24px;
  cursor: pointer;
  touch-action: manipulation;
  -webkit-tap-highlight-color: transparent;
}
.toggle-switch input { opacity: 0; width: 0; height: 0; }
.toggle-slider {
  position: absolute;
  inset: 0;
  background: var(--bg-3);
  border-radius: 24px;
  transition: 0.3s;
  border: 1px solid var(--border-default);
}
.toggle-slider::before {
  content: '';
  position: absolute;
  height: 18px;
  width: 18px;
  left: 2px;
  bottom: 2px;
  background: var(--text-2);
  border-radius: 50%;
  transition: 0.3s;
}
.toggle-switch input:checked + .toggle-slider {
  background: var(--accent);
  border-color: var(--accent);
}
.toggle-switch input:checked + .toggle-slider::before {
  transform: translateX(20px);
  background: #fff;
}

/* ===== SEGMENTED CONTROL ===== */
.seg-control {
  display: flex;
  background: var(--bg-1);
  border: 1px solid var(--border-subtle);
  border-radius: 12px;
  padding: 3px;
  gap: 2px;
}
.seg-btn {
  flex: 1;
  padding: 10px 0;
  border-radius: 10px;
  font-size: var(--text-sm);
  font-weight: 500;
  color: var(--text-2);
  background: transparent;
  border: none;
  cursor: pointer;
  transition: all 0.2s;
  text-align: center;
  -webkit-tap-highlight-color: transparent;
  touch-action: manipulation;
  min-height: 44px;
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 4px;
  font-family: 'Inter', -apple-system, sans-serif;
}
.seg-btn.active {
  background: var(--accent);
  color: white;
  box-shadow: 0 2px 8px rgba(79,140,255,0.3);
}

/* ===== RESULTS ===== */
.results-grid {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 10px;
}

.result-card {
  background: var(--bg-2);
  border: 1px solid var(--border-subtle);
  border-radius: 16px;
  padding: 16px;
  text-align: center;
  position: relative;
  overflow: hidden;
}
.result-card::before {
  content: '';
  position: absolute;
  top: 0; left: 0; right: 0;
  height: 3px;
  background: var(--border-subtle);
}
.result-card.highlight {
  border-color: var(--accent);
}
.result-card.highlight::before { background: var(--accent); }
.result-card.success::before { background: var(--green); }
.result-card.warning::before { background: var(--amber); }
.result-card.danger::before { background: var(--red); }
.result-card.warning { border-color: rgba(251,191,36,0.3); }
.result-card.danger { border-color: rgba(248,113,113,0.3); background: rgba(248,113,113,0.04); }
.result-card.success { border-color: rgba(52,211,153,0.3); }

.result-value {
  font-family: 'JetBrains Mono', monospace;
  font-size: var(--text-2xl);
  font-weight: 600;
  color: var(--text-0);
  line-height: 1;
}
.result-value.red { color: var(--red); }
.result-value.green { color: var(--green); }
.result-value.yellow { color: var(--amber); }

.result-unit {
  font-size: var(--text-xs);
  color: var(--text-2);
  text-transform: uppercase;
  letter-spacing: 0.06em;
  margin-top: 4px;
  font-family: 'JetBrains Mono', monospace;
}
.result-label {
  font-size: var(--text-xs);
  color: var(--text-3);
  text-transform: uppercase;
  letter-spacing: 0.04em;
  margin-top: 2px;
}

/* ===== STATUS BAR ===== */
.status-bar {
  display: flex;
  align-items: center;
  gap: 8px;
  padding: 12px 16px;
  border-radius: 14px;
  margin-top: 12px;
  font-size: 13px;
  font-weight: 600;
}
.status-bar.ok {
  background: var(--green-subtle);
  border: 1px solid rgba(52,211,153,0.3);
  color: var(--green);
}
.status-bar.warn {
  background: var(--amber-subtle);
  border: 1px solid rgba(251,191,36,0.3);
  color: var(--amber);
}
.status-bar.error {
  background: var(--red-subtle);
  border: 1px solid rgba(248,113,113,0.3);
  color: var(--red);
}
.status-dot { width: 8px; height: 8px; border-radius: 50%; flex-shrink: 0; }
.status-bar.ok .status-dot { background: var(--green); }
.status-bar.warn .status-dot { background: var(--amber); }
.status-bar.error .status-dot { background: var(--red); }

/* ===== COMPRESSION PANEL ===== */
.compression-panel {
  margin-top: 12px;
  background: var(--bg-1);
  border: 2px solid rgba(251,191,36,0.3);
  border-radius: 16px;
  padding: 16px;
}
.compression-panel-title {
  font-size: var(--text-sm);
  font-weight: 700;
  color: var(--amber);
  letter-spacing: 0.06em;
  text-transform: uppercase;
  margin-bottom: 10px;
  display: flex;
  align-items: center;
  gap: 6px;
}
.compression-panel-title svg { width: 16px; height: 16px; }
.compression-readout { text-align: center; margin-bottom: 12px; }
.compression-readout-value {
  font-family: 'JetBrains Mono', monospace;
  font-size: 36px;
  font-weight: 700;
  color: var(--amber);
  line-height: 1;
}
.compression-readout-label {
  font-size: 11px;
  color: var(--text-2);
  margin-top: 2px;
}
.compression-presets {
  display: flex;
  gap: 6px;
  margin-bottom: 12px;
  flex-wrap: wrap;
}
.compression-preset-btn {
  flex: 1;
  min-width: 40px;
  padding: 10px 4px;
  border-radius: 12px;
  font-family: 'JetBrains Mono', monospace;
  font-size: 13px;
  font-weight: 700;
  color: var(--text-2);
  background: var(--bg-3);
  border: 1.5px solid var(--border-default);
  cursor: pointer;
  transition: all 0.2s;
  text-align: center;
  -webkit-tap-highlight-color: transparent;
  touch-action: manipulation;
  min-height: 44px;
}
.compression-preset-btn:hover {
  border-color: var(--amber);
  color: var(--text-0);
}
.compression-preset-btn.active {
  background: var(--amber);
  border-color: var(--amber);
  color: #000;
}
.compression-slider-wrap { margin-top: 8px; }
.compression-slider {
  width: 100%;
  height: 8px;
  -webkit-appearance: none;
  appearance: none;
  background: linear-gradient(to right, var(--green), var(--amber), var(--red));
  border-radius: 4px;
  outline: none;
}
.compression-slider::-webkit-slider-thumb {
  -webkit-appearance: none;
  appearance: none;
  width: 24px;
  height: 24px;
  border-radius: 50%;
  background: #fff;
  cursor: pointer;
  box-shadow: 0 2px 8px rgba(0,0,0,0.3);
}
.compression-slider::-moz-range-thumb {
  width: 24px;
  height: 24px;
  border-radius: 50%;
  background: #fff;
  cursor: pointer;
  box-shadow: 0 2px 8px rgba(0,0,0,0.3);
  border: none;
}
.compression-slider-labels {
  display: flex;
  justify-content: space-between;
  font-size: 10px;
  color: var(--text-3);
  margin-top: 6px;
}
.compression-impact {
  margin-top: 10px;
  padding: 10px 12px;
  border-radius: 12px;
  font-size: var(--text-sm);
  font-weight: 600;
  text-align: center;
}
.compression-impact.low {
  background: var(--green-subtle);
  color: var(--green);
  border: 1px solid rgba(52,211,153,0.3);
}
.compression-impact.medium {
  background: var(--amber-subtle);
  color: var(--amber);
  border: 1px solid rgba(251,191,36,0.3);
}
.compression-impact.high {
  background: rgba(251,191,36,0.15);
  color: var(--amber);
  border: 1px solid rgba(251,191,36,0.3);
}
.compression-impact.extreme {
  background: var(--red-subtle);
  color: var(--red);
  border: 1px solid rgba(248,113,113,0.3);
}

/* ===== EQUIVALENT LENGTH TABLE ===== */
.eq-table-container { overflow-x: auto; margin-top: 12px; border-radius: 12px; }
.eq-table { width: 100%; border-collapse: collapse; font-size: 13px; }
.eq-table th {
  background: var(--bg-3);
  color: var(--accent);
  padding: 10px 12px;
  text-align: left;
  font-size: 11px;
  font-weight: 700;
  letter-spacing: 0.04em;
  text-transform: uppercase;
  border-bottom: 2px solid var(--accent);
  white-space: nowrap;
}
.eq-table td {
  padding: 8px 12px;
  border-bottom: 1px solid var(--border-subtle);
  color: var(--text-0);
  font-family: 'JetBrains Mono', monospace;
  font-size: 13px;
  white-space: nowrap;
}
.eq-table tr:hover td { background: rgba(79,140,255,0.04); }
.eq-table td:first-child {
  font-family: 'Inter', -apple-system, sans-serif;
  font-weight: 500;
  color: var(--text-1);
}
.eq-category {
  font-size: 13px;
  font-weight: 700;
  color: var(--accent);
  margin: 20px 0 8px 0;
  padding-bottom: 4px;
  border-bottom: 1px solid var(--border-subtle);
}
.eq-category:first-child { margin-top: 0; }

/* ===== FRICTION LIMIT WARNING ===== */
.friction-limit-badge {
  display: inline-flex;
  align-items: center;
  gap: 4px;
  padding: 4px 8px;
  border-radius: 8px;
  font-size: 10px;
  font-weight: 700;
  letter-spacing: 0.02em;
  background: var(--red-subtle);
  color: var(--red);
  border: 1px solid rgba(248,113,113,0.3);
}

/* ===== BRANCH HIERARCHY ===== */
.branch-indent {
  margin-left: 12px;
  padding-left: 8px;
  border-left: 2px solid var(--border-default);
}
.branch-indent .sys-run-tab { font-size: 10px; padding: 5px 8px; }

.sys-branch-btn {
  padding: 4px 10px;
  border-radius: 8px;
  font-size: 11px;
  font-weight: 600;
  color: var(--accent);
  background: var(--accent-subtle);
  border: 1px solid rgba(79,140,255,0.3);
  cursor: pointer;
  -webkit-tap-highlight-color: transparent;
  touch-action: manipulation;
}
.sys-branch-btn:active { background: rgba(79,140,255,0.2); }

.branch-ctx-bar {
  display: flex;
  align-items: center;
  gap: 6px;
  padding: 6px 10px;
  background: var(--accent-subtle);
  border: 1px solid rgba(79,140,255,0.15);
  border-radius: 10px;
  margin-bottom: 8px;
  font-size: 11px;
  color: var(--text-2);
}
.branch-ctx-bar strong { color: var(--accent); }

.branch-children-section {
  margin-top: 12px;
  padding-top: 10px;
  border-top: 1px dashed var(--border-default);
}
.branch-child-card {
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 8px 10px;
  background: var(--bg-3);
  border: 1px solid var(--border-subtle);
  border-radius: 10px;
  margin-bottom: 4px;
  cursor: pointer;
  transition: border-color 0.2s;
  -webkit-tap-highlight-color: transparent;
  touch-action: manipulation;
}
.branch-child-card:active { border-color: var(--accent); }
.branch-child-label { font-size: 12px; font-weight: 600; color: var(--accent); }
.branch-child-info {
  font-size: 10px;
  color: var(--text-3);
  font-family: 'JetBrains Mono', monospace;
}

.sys-run-tabs-wrap {
  display: flex;
  gap: 4px;
  margin-bottom: 12px;
  overflow-x: auto;
  -webkit-overflow-scrolling: touch;
  padding-bottom: 2px;
}
.sys-run-tab {
  padding: 7px 10px;
  border-radius: 10px;
  font-size: 11px;
  font-weight: 600;
  color: var(--text-2);
  background: var(--bg-3);
  border: 1px solid var(--border-default);
  cursor: pointer;
  white-space: nowrap;
  transition: all 0.2s;
  -webkit-tap-highlight-color: transparent;
  touch-action: manipulation;
  min-height: 36px;
  flex-shrink: 0;
}
.sys-run-tab.active {
  color: #fff;
  background: var(--accent);
  border-color: var(--accent);
  box-shadow: 0 2px 8px rgba(79,140,255,0.25);
}
.sys-run-tab.branch-tab {
  font-size: 10px;
  padding: 5px 8px;
  min-height: 30px;
  border-style: dashed;
}
.sys-run-tab.branch-tab.active { border-style: solid; }
.sys-run-tab.has-data {
  border-color: var(--green);
  color: var(--text-0);
}
.sys-run-tab.has-data.active {
  border-color: var(--accent);
  color: #fff;
}

.sys-add-btn {
  padding: 7px 10px;
  border-radius: 10px;
  font-size: 11px;
  font-weight: 700;
  color: var(--green);
  background: var(--green-subtle);
  border: 1px dashed var(--green);
  cursor: pointer;
  white-space: nowrap;
  -webkit-tap-highlight-color: transparent;
  touch-action: manipulation;
  min-height: 36px;
  flex-shrink: 0;
}
.sys-divider {
  width: 1px;
  background: var(--border-default);
  align-self: stretch;
  flex-shrink: 0;
  margin: 4px 2px;
}

/* Path Step List */
.path-step { display: flex; align-items: stretch; gap: 0; position: relative; margin-bottom: 2px; }
.path-step-line { width: 28px; display: flex; flex-direction: column; align-items: center; flex-shrink: 0; }
.path-step-dot { width: 10px; height: 10px; border-radius: 50%; background: var(--accent); flex-shrink: 0; margin-top: 12px; }
.path-step-dot.straight { background: var(--text-3); }
.path-step-dot.fitting { background: var(--amber); }
.path-step-dot.branch { background: var(--accent); }
.path-step-dot.terminal { background: var(--green); }
.path-step-connector { width: 2px; flex: 1; background: var(--border-default); min-height: 8px; }
.path-step-body {
  flex: 1; min-width: 0; padding: 8px 10px;
  background: var(--bg-1);
  border: 1px solid var(--border-subtle);
  border-radius: 10px;
  display: flex; align-items: center; gap: 8px;
}
.path-step-body:active { border-color: var(--border-strong); }
.path-step-info { flex: 1; min-width: 0; }
.path-step-name { font-size: 12px; font-weight: 600; color: var(--text-0); white-space: nowrap; overflow: hidden; text-overflow: ellipsis; }
.path-step-detail { font-size: 10px; color: var(--text-2); font-family: 'JetBrains Mono', monospace; }
.path-step-note { font-size: 10px; color: var(--amber); margin-top: 1px; }
.path-step-eq {
  font-family: 'JetBrains Mono', monospace;
  font-size: 13px; font-weight: 700;
  color: var(--accent); white-space: nowrap; flex-shrink: 0;
}
.path-step-remove {
  width: 28px; height: 28px; border-radius: 8px;
  background: var(--red-subtle); color: var(--red);
  border: none; cursor: pointer;
  display: flex; align-items: center; justify-content: center;
  flex-shrink: 0; font-size: 14px; font-weight: 700;
  -webkit-tap-highlight-color: transparent; touch-action: manipulation;
}

/* Quick Add Grid */
.add-step-header { font-size: 12px; font-weight: 700; color: var(--accent); text-transform: uppercase; letter-spacing: 0.06em; margin-bottom: 8px; }
.quick-add-section { margin-bottom: 8px; }
.quick-add-label { font-size: 10px; font-weight: 600; color: var(--text-3); text-transform: uppercase; letter-spacing: 0.06em; margin-bottom: 6px; }
.quick-add-grid { display: grid; grid-template-columns: repeat(3, 1fr); gap: 8px; }
.quick-add-btn {
  display: flex; flex-direction: column; align-items: center; gap: 4px;
  padding: 12px 4px 10px;
  background: var(--bg-2);
  border: 1px solid var(--border-default);
  border-radius: 14px;
  color: var(--text-2);
  font-size: 10px; font-weight: 600;
  cursor: pointer;
  -webkit-tap-highlight-color: transparent;
  transition: all 0.15s;
}
.quick-add-btn:active {
  background: var(--accent-subtle);
  border-color: var(--accent);
  color: var(--accent);
  transform: scale(0.96);
}
.quick-add-icon { width: 32px; height: 32px; color: var(--text-0); }
.quick-add-icon svg { width: 100%; height: 100%; }
.quick-add-btn:active .quick-add-icon { color: var(--accent); }
.add-divider-line { height: 1px; background: var(--border-subtle); margin: 10px 0; }

.add-step-area { margin-top: 10px; }
.add-step-type-row { display: flex; gap: 6px; margin-bottom: 8px; }
.add-step-type-btn {
  flex: 1; padding: 8px 6px; border-radius: 10px;
  font-size: 11px; font-weight: 600;
  color: var(--text-2);
  background: var(--bg-3);
  border: 1px solid var(--border-default);
  cursor: pointer; text-align: center;
  -webkit-tap-highlight-color: transparent; touch-action: manipulation;
  min-height: 38px;
}
.add-step-type-btn.active {
  color: #fff; background: var(--accent); border-color: var(--accent);
}

/* Fitting Search */
.fitting-search-input {
  width: 100%; background: var(--bg-1);
  border: 1.5px solid var(--border-default);
  border-radius: 14px; padding: 12px 14px 12px 38px;
  color: var(--text-0); font-size: var(--text-base); font-weight: 500;
  background-image: url("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' width='16' height='16' viewBox='0 0 24 24' fill='none' stroke='%238888a0' stroke-width='2'%3E%3Ccircle cx='11' cy='11' r='8'/%3E%3Cpath d='M21 21l-4.35-4.35'/%3E%3C/svg%3E");
  background-repeat: no-repeat; background-position: 12px center;
}
.fitting-search-input:focus { outline: none; border-color: var(--accent); box-shadow: var(--accent-glow); }
.fitting-search-input::placeholder { color: var(--text-3); }
.fitting-results { max-height: 280px; overflow-y: auto; -webkit-overflow-scrolling: touch; margin-top: 6px; }
.fitting-cat-header {
  font-size: 10px; font-weight: 700;
  color: var(--accent); letter-spacing: 0.06em; text-transform: uppercase;
  padding: 8px 0 4px; position: sticky; top: 0; background: var(--bg-2); z-index: 1;
}
.fitting-icon { width: 36px; height: 36px; flex-shrink: 0; color: var(--accent); opacity: 0.8; }
.fitting-icon svg { width: 100%; height: 100%; }
.fitting-result-card {
  display: flex; align-items: center; gap: 10px;
  padding: 12px; background: var(--bg-2);
  border: 1px solid var(--border-subtle); border-radius: 14px;
  margin-bottom: 6px; cursor: pointer;
  -webkit-tap-highlight-color: transparent;
}
.fitting-result-card:active { background: var(--bg-3); border-color: var(--accent); }
.fitting-result-info { flex: 1; min-width: 0; }
.fitting-result-name { font-size: 12px; font-weight: 600; color: var(--text-0); }
.fitting-result-note { font-size: 10px; color: var(--text-2); margin-top: 1px; }
.fitting-result-eq {
  font-family: 'JetBrains Mono', monospace; font-size: 13px; font-weight: 700;
  color: var(--accent); white-space: nowrap; flex-shrink: 0;
}

/* Run header config */
.sys-config-grid { display: grid; grid-template-columns: 1fr 1fr; gap: 8px; }
.sys-run-header-bar { display: flex; align-items: center; justify-content: space-between; margin-bottom: 10px; }
.sys-run-title { font-size: 14px; font-weight: 700; color: var(--text-0); }
.sys-run-label { font-size: 11px; color: var(--text-2); font-weight: 500; }
.sys-remove-btn {
  padding: 5px 10px; border-radius: 10px; font-size: 11px; font-weight: 600;
  color: var(--red); background: var(--red-subtle);
  border: 1px solid rgba(248,113,113,0.2); cursor: pointer;
  -webkit-tap-highlight-color: transparent; touch-action: manipulation; min-height: 32px;
}

/* Totals */
.sys-totals-grid { display: grid; grid-template-columns: 1fr 1fr; gap: 8px; }
.sys-total-card {
  background: var(--bg-1); border: 1px solid var(--border-subtle);
  border-radius: 14px; padding: 12px; text-align: center;
}
.sys-total-card.hl { border-color: var(--accent); }
.sys-total-card.full { grid-column: 1 / -1; }
.sys-total-value {
  font-family: 'JetBrains Mono', monospace; font-size: 20px; font-weight: 700;
  color: var(--text-0); line-height: 1;
}
.sys-total-unit { font-size: 10px; color: var(--text-2); margin-top: 2px; }
.sys-total-label { font-size: 9px; color: var(--text-3); text-transform: uppercase; letter-spacing: 0.04em; margin-top: 4px; }

/* Run summary row */
.sys-run-row {
  display: flex; align-items: center; gap: 8px;
  padding: 10px 12px; background: var(--bg-1);
  border: 1px solid var(--border-subtle); border-radius: 12px;
  margin-bottom: 4px; cursor: pointer;
  -webkit-tap-highlight-color: transparent; touch-action: manipulation;
}
.sys-run-row:active { border-color: var(--accent); }
.sys-run-row-num {
  width: 22px; height: 22px; border-radius: 50%;
  background: var(--accent); color: #fff;
  font-size: 10px; font-weight: 700;
  display: flex; align-items: center; justify-content: center; flex-shrink: 0;
}
.sys-run-row-info { flex: 1; min-width: 0; }
.sys-run-row-name { font-size: 11px; font-weight: 600; color: var(--text-0); white-space: nowrap; overflow: hidden; text-overflow: ellipsis; }
.sys-run-row-stats { font-size: 10px; color: var(--text-2); font-family: 'JetBrains Mono', monospace; }
.sys-run-row-cfm { font-family: 'JetBrains Mono', monospace; font-size: 12px; font-weight: 700; color: var(--green); flex-shrink: 0; }
.sys-critical-badge {
  font-size: 8px; font-weight: 700; color: var(--red);
  background: var(--red-subtle); padding: 2px 5px; border-radius: 6px;
  text-transform: uppercase; letter-spacing: 0.02em; flex-shrink: 0;
}

/* Run Summary Grid */
.run-summary-grid { display: grid; grid-template-columns: 1fr 1fr; gap: 8px; }
.run-summary-card {
  background: var(--bg-1); border: 1px solid var(--border-subtle);
  border-radius: 14px; padding: 12px 8px; text-align: center;
}
.run-summary-value { font-family: 'JetBrains Mono', monospace; font-size: 20px; font-weight: 700; color: var(--text-0); line-height: 1.2; }
.run-summary-value.green { color: var(--green); }
.run-summary-value.red { color: var(--red); }
.run-summary-value.yellow { color: var(--amber); }
.run-summary-unit { font-family: 'JetBrains Mono', monospace; font-size: 10px; color: var(--text-3); text-transform: uppercase; letter-spacing: 0.02em; }
.run-summary-label { font-size: 9px; color: var(--text-2); text-transform: uppercase; letter-spacing: 0.04em; margin-top: 2px; }

.add-fitting-btn {
  background: var(--bg-3); border: 1px solid var(--border-default);
  color: var(--text-0); border-radius: 10px;
  font-size: 12px; font-weight: 600; cursor: pointer; white-space: nowrap;
}
.add-fitting-btn:active { background: var(--accent); border-color: var(--accent); color: #fff; }

/* Manual J compare */
.mj-row {
  display: flex; align-items: center; gap: 8px;
  padding: 10px; background: var(--bg-1);
  border: 1px solid var(--border-subtle); border-radius: 14px; margin-top: 8px;
}
.mj-row label { font-size: 11px; font-weight: 600; color: var(--text-2); white-space: nowrap; }
.mj-row input {
  width: 80px; background: var(--bg-3);
  border: 1px solid var(--border-default); border-radius: 10px;
  padding: 6px 8px; color: var(--text-0);
  font-family: 'JetBrains Mono', monospace; font-size: 13px; font-weight: 600; text-align: center;
}
.mj-row input:focus { outline: none; border-color: var(--accent); }
.mj-result { font-family: 'JetBrains Mono', monospace; font-size: 12px; font-weight: 700; flex: 1; text-align: right; }

/* House Tightness Panel */
.tightness-panel {
  background: var(--bg-1); border: 1px solid var(--border-subtle);
  border-radius: 14px; padding: 12px; margin-bottom: 10px;
}
.tightness-title {
  display: flex; align-items: center; gap: 6px;
  font-size: 11px; font-weight: 700; color: var(--accent);
  text-transform: uppercase; letter-spacing: 0.06em; margin-bottom: 8px;
}
.tightness-title svg { width: 16px; height: 16px; flex-shrink: 0; }
.tightness-selector { display: flex; gap: 4px; flex-wrap: wrap; margin-bottom: 6px; }
.tightness-btn {
  flex: 1; min-width: 60px; padding: 6px 4px;
  background: var(--bg-2); border: 1px solid var(--border-default);
  border-radius: 10px; color: var(--text-2); font-size: 10px;
  cursor: pointer; text-align: center; -webkit-tap-highlight-color: transparent;
}
.tightness-btn.active {
  background: var(--accent); border-color: var(--accent); color: #fff;
  box-shadow: 0 2px 8px rgba(79,140,255,0.25);
}
.tightness-btn-label { font-weight: 700; font-size: 10px; }
.tightness-btn-ach { font-family: 'JetBrains Mono', monospace; font-size: 8px; margin-top: 2px; opacity: 0.7; }
.tightness-desc { font-size: 10px; color: var(--text-3); line-height: 1.3; margin-bottom: 4px; }
.tightness-ach { font-family: 'JetBrains Mono', monospace; font-size: 10px; color: var(--text-2); }

/* CFM Est Room v2 */
.cfm-est-room-header {
  display: grid; grid-template-columns: 24px 1fr 120px 50px;
  gap: 4px; align-items: center; padding: 4px 0;
  font-size: 9px; font-weight: 700; color: var(--text-3);
  text-transform: uppercase; letter-spacing: 0.04em;
  border-bottom: 1px solid var(--border-subtle); margin-bottom: 2px;
}
.cfm-est-room-v2 {
  display: grid; grid-template-columns: 24px 1fr 50px;
  gap: 4px; align-items: center; padding: 8px 0;
  border-bottom: 1px solid var(--border-subtle);
}
.cfm-est-room-v2:last-child { border-bottom: none; }
.cfm-est-room-inputs { min-width: 0; }
.cfm-est-dims { display: flex; align-items: center; gap: 4px; margin-top: 4px; }
.cfm-est-sqft-input, .cfm-est-ht-input {
  width: 60px; background: var(--bg-3);
  border: 1px solid var(--border-default); border-radius: 8px;
  padding: 4px 6px; color: var(--text-0);
  font-family: 'JetBrains Mono', monospace; font-size: 12px; font-weight: 600; text-align: center;
}
.cfm-est-ht-input { width: 44px; }
.cfm-est-sqft-input:focus, .cfm-est-ht-input:focus { outline: none; border-color: var(--accent); }
.cfm-est-x { font-size: 10px; color: var(--text-3); font-weight: 700; }
.cfm-est-unit { font-size: 9px; color: var(--text-3); }
.cfm-est-vol { font-family: 'JetBrains Mono', monospace; font-size: 9px; color: var(--text-3); margin-top: 2px; }
.cfm-est-cfm { font-family: 'JetBrains Mono', monospace; font-size: 16px; font-weight: 700; color: var(--green); text-align: right; }
.cfm-est-cfm-unit { font-size: 8px; font-weight: 600; display: block; color: var(--text-3); }

.cfm-est-room {
  display: grid; grid-template-columns: 24px 1fr 70px 60px;
  gap: 4px; align-items: center; padding: 6px 0;
  border-bottom: 1px solid var(--border-subtle);
}
.cfm-est-room:last-child { border-bottom: none; }
.cfm-est-remove {
  width: 20px; height: 20px; border-radius: 6px;
  background: var(--red-subtle); color: var(--red);
  border: none; cursor: pointer; font-size: 11px; font-weight: 700;
  display: flex; align-items: center; justify-content: center;
  -webkit-tap-highlight-color: transparent; touch-action: manipulation;
}
.cfm-est-name-input {
  background: none; border: none; color: var(--text-0);
  font-size: 11px; font-weight: 600; padding: 2px; width: 100%; min-width: 0;
}
.cfm-est-name-input:focus { outline: none; color: var(--accent); }
.cfm-est-sqft-input {
  width: 100%; background: var(--bg-1);
  border: 1px solid var(--border-subtle); border-radius: 8px;
  padding: 5px 6px; color: var(--text-0);
  font-family: 'JetBrains Mono', monospace; font-size: 12px; font-weight: 600; text-align: center;
}
.cfm-est-sqft-input:focus { outline: none; border-color: var(--accent); }
.cfm-est-cfm { font-family: 'JetBrains Mono', monospace; font-size: 12px; font-weight: 700; color: var(--green); text-align: right; }
.cfm-est-total {
  display: flex; align-items: center; justify-content: space-between;
  padding: 12px; background: var(--accent-subtle);
  border: 1px solid rgba(79,140,255,0.2);
  border-radius: 14px; margin-top: 10px;
}
.cfm-est-total-label { font-size: 12px; font-weight: 700; color: var(--text-0); }
.cfm-est-total-value { font-family: 'JetBrains Mono', monospace; font-size: 18px; font-weight: 700; color: var(--accent); }

/* Section toggle */
.section-toggle {
  display: flex; align-items: center; justify-content: space-between;
  cursor: pointer; -webkit-tap-highlight-color: transparent; touch-action: manipulation;
}
.section-toggle .toggle-arrow { transition: transform 0.2s; color: var(--text-2); font-size: 13px; }
.section-toggle.collapsed .toggle-arrow { transform: rotate(-90deg); }
.section-body { display: block; }
.section-body.collapsed { display: none; }

.sys-add-step-btn {
  width: 100%; padding: 12px; border-radius: 14px;
  font-size: 12px; font-weight: 600;
  color: var(--green); background: var(--green-subtle);
  border: 1px dashed rgba(52,211,153,0.4);
  cursor: pointer; -webkit-tap-highlight-color: transparent; touch-action: manipulation;
  min-height: 44px; margin-top: 8px;
  transition: all 0.15s;
}
.sys-add-step-btn:active { background: rgba(52,211,153,0.2); }

.straight-input-row { display: flex; align-items: center; gap: 8px; }
.straight-input-row input {
  width: 70px; background: var(--bg-1);
  border: 1px solid var(--border-default); border-radius: 10px;
  padding: 8px; color: var(--text-0);
  font-family: 'JetBrains Mono', monospace; font-size: 14px; font-weight: 600; text-align: center;
}
.straight-input-row input:focus { outline: none; border-color: var(--accent); }

/* Plenum */
.plenum-grid { display: grid; grid-template-columns: 1fr 1fr 1fr; gap: 8px; }
.collar-chips { display: flex; flex-wrap: wrap; gap: 4px; margin-top: 6px; }
.collar-chip {
  display: flex; align-items: center; gap: 3px;
  padding: 4px 8px; border-radius: 14px;
  font-size: 11px; font-weight: 600;
  color: var(--text-0); background: var(--bg-3);
  border: 1px solid var(--border-default);
}
.collar-chip-x {
  width: 16px; height: 16px; border-radius: 50%;
  background: var(--red-subtle); color: var(--red);
  border: none; cursor: pointer; font-size: 10px; font-weight: 700;
  display: flex; align-items: center; justify-content: center;
  -webkit-tap-highlight-color: transparent; touch-action: manipulation;
}

/* ===== CALC RESULTS HEADER ===== */
.calc-results-header {
  display: flex; gap: 6px; padding: 10px 12px;
  background: var(--bg-2); border: 1px solid var(--border-subtle);
  border-radius: 16px; margin-bottom: 12px;
}
.calc-result-pill {
  flex: 1; text-align: center; padding: 8px 4px;
  background: var(--bg-1); border-radius: 12px;
  border: 1px solid var(--border-subtle);
}
.calc-result-pill.accent { border-color: var(--accent); }
.calc-result-pill-val {
  display: block; font-family: 'JetBrains Mono', monospace;
  font-size: 16px; font-weight: 700; color: var(--text-0); line-height: 1.2;
}
.calc-result-pill.accent .calc-result-pill-val { color: var(--accent); }
.calc-result-pill-label { display: block; font-size: 9px; color: var(--text-2); text-transform: uppercase; letter-spacing: 0.04em; margin-top: 2px; }

/* ===== BRANCH TREE MAP ===== */
.branch-tree { padding: 8px 0; }
.tree-node { position: relative; padding-left: 20px; margin-bottom: 2px; }
.tree-node::before { content: ''; position: absolute; left: 6px; top: 0; width: 1px; height: 100%; background: var(--border-default); }
.tree-node:last-child::before { height: 12px; }
.tree-node::after { content: ''; position: absolute; left: 6px; top: 12px; width: 12px; height: 1px; background: var(--border-default); }
.tree-trunk { padding-left: 0; margin-bottom: 4px; }
.tree-trunk::before, .tree-trunk::after { display: none; }
.tree-item {
  display: flex; align-items: center; gap: 6px;
  padding: 6px 8px; background: var(--bg-2);
  border-radius: 10px; border: 1px solid var(--border-subtle);
  font-size: 11px; color: var(--text-0); cursor: pointer; min-height: 32px;
}
.tree-item:active { background: rgba(255,255,255,0.03); }
.tree-trunk .tree-item { background: var(--accent-subtle); border-color: rgba(79,140,255,0.2); font-weight: 600; }
.tree-item-icon { width: 18px; height: 18px; flex-shrink: 0; }
.tree-item-icon svg { width: 14px; height: 14px; color: var(--accent); }
.tree-item-label { flex: 1; overflow: hidden; text-overflow: ellipsis; white-space: nowrap; }
.tree-item-size { font-family: 'JetBrains Mono', monospace; font-size: 10px; color: var(--text-2); white-space: nowrap; }
.tree-branch-label { font-size: 9px; font-weight: 700; color: var(--accent); text-transform: uppercase; letter-spacing: 0.06em; padding: 4px 0 2px 20px; }
.tree-children { padding-left: 16px; }

/* ===== ENVELOPE / DUCT LOC SELECTORS ===== */
.cfm-envelope-sel { display: flex; gap: 4px; margin-bottom: 8px; }
.cfm-envelope-btn {
  flex: 1; padding: 6px 4px; font-size: 10px; text-align: center;
  border-radius: 10px; background: var(--bg-2); border: 1px solid var(--border-default);
  color: var(--text-2); cursor: pointer;
}
.cfm-envelope-btn.active { background: var(--accent-subtle); border-color: var(--accent); color: var(--text-0); }
.cfm-envelope-btn div:first-child { font-weight: 600; }
.cfm-envelope-btn div:last-child { font-size: 8px; margin-top: 2px; color: var(--text-3); }

/* ===== MODE TOGGLE ===== */
.mode-toggle {
  display: flex; gap: 4px; margin-bottom: 12px;
  background: var(--bg-2); border-radius: 14px;
  padding: 4px; border: 1px solid var(--border-subtle);
}
.mode-btn {
  flex: 1; padding: 10px; text-align: center; font-size: var(--text-sm);
  font-weight: 600; border-radius: 12px; border: none;
  background: transparent; color: var(--text-2); cursor: pointer;
  font-family: 'Inter', -apple-system, sans-serif;
  transition: all 0.2s;
}
.mode-btn.active {
  background: var(--accent); color: #fff;
  box-shadow: 0 2px 8px rgba(79,140,255,0.3);
}

/* ===== CFM SLIDER ===== */
.slider-panel {
  background: var(--bg-2);
  border: 1px solid var(--border-subtle);
  border-radius: 20px; padding: 20px; margin-bottom: 12px;
}
.slider-header {
  display: flex; justify-content: space-between; align-items: center;
  margin-bottom: 12px;
}
.slider-label { font-size: var(--text-sm); color: var(--text-2); font-weight: 500; }
.slider-value-wrap { display: flex; align-items: baseline; gap: 4px; }
.slider-value-input {
  font-family: 'JetBrains Mono', monospace; font-size: var(--text-2xl);
  font-weight: 700; color: var(--accent); background: none; border: none;
  text-align: right; width: 80px; outline: none;
  -moz-appearance: textfield;
}
.slider-value-input::-webkit-inner-spin-button,
.slider-value-input::-webkit-outer-spin-button { -webkit-appearance: none; }
.slider-value-unit { font-size: var(--text-sm); color: var(--text-2); font-weight: 600; }
.cfm-slider {
  width: 100%; height: 6px; -webkit-appearance: none; appearance: none;
  background: linear-gradient(to right, var(--green), var(--amber), var(--red));
  border-radius: 3px; outline: none;
}
.cfm-slider::-webkit-slider-thumb {
  -webkit-appearance: none; width: 24px; height: 24px;
  background: white; border-radius: 50%;
  box-shadow: 0 2px 8px rgba(0,0,0,0.3); cursor: pointer;
}
.cfm-slider::-moz-range-thumb {
  width: 24px; height: 24px;
  background: white; border-radius: 50%;
  box-shadow: 0 2px 8px rgba(0,0,0,0.3); cursor: pointer; border: none;
}
.slider-range-labels {
  display: flex; justify-content: space-between;
  font-size: 9px; color: var(--text-3); margin-top: 6px;
}

/* ===== CONFIG ROWS ===== */
.config-row { display: flex; gap: 8px; margin-bottom: 10px; }
.config-group { flex: 1; }
.config-label {
  font-size: var(--text-xs); color: var(--text-2); text-transform: uppercase;
  letter-spacing: 0.06em; font-weight: 600; margin-bottom: 4px; display: block;
}
.size-panel {
  background: var(--bg-2); border: 1px solid var(--border-subtle);
  border-radius: 16px; padding: 16px; margin-bottom: 10px;
}

/* ===== REVERSE MODE ===== */
.rev-capacity-bar { padding: 8px 0; }
.rev-bar-track { display: flex; height: 16px; border-radius: 8px; overflow: hidden; margin-bottom: 6px; }
.rev-bar-zone { height: 100%; }
.rev-bar-low { background: rgba(248,113,113,0.25); flex: 1; }
.rev-bar-ok { background: var(--green); flex: 2; }
.rev-bar-high { background: rgba(251,191,36,0.25); flex: 1; }
.rev-bar-labels {
  display: flex; justify-content: space-between;
  font-family: 'JetBrains Mono', monospace; font-size: 14px; font-weight: 700; color: var(--text-0);
}
.rev-bar-captions { display: flex; justify-content: space-between; font-size: 9px; color: var(--text-3); margin-top: 2px; }

/* ===== PSYCHROMETRICS ===== */
.psych-mode-sel { display: flex; gap: 4px; margin-bottom: 12px; }
.psych-mode-btn {
  flex: 1; padding: 6px 4px; font-size: 10px; text-align: center;
  border-radius: 10px; background: var(--bg-2); border: 1px solid var(--border-default);
  color: var(--text-2); cursor: pointer; font-weight: 600;
}
.psych-mode-btn.active { background: var(--accent-subtle); border-color: var(--accent); color: var(--text-0); }
.psych-inputs { margin-bottom: 8px; }
.psych-input-row {
  display: flex; justify-content: space-between; align-items: center;
  padding: 8px 0; border-bottom: 1px solid rgba(255,255,255,0.04);
}
.psych-input-row label { font-size: 12px; color: var(--text-0); }
.psych-input-wrap { display: flex; align-items: center; gap: 4px; }
.psych-input-wrap .input-field { width: 70px; text-align: right; padding: 6px 8px; }
.psych-input-unit { font-size: 10px; color: var(--text-2); width: 30px; }
.psych-result-row {
  display: flex; align-items: center; padding: 7px 0;
  border-bottom: 1px solid rgba(255,255,255,0.04); font-size: 12px;
}
.psych-result-row span:first-child { flex: 1; color: var(--text-2); }
.psych-result-row span:nth-child(2) { font-family: 'JetBrains Mono', monospace; font-weight: 600; color: var(--text-0); min-width: 70px; text-align: right; }
.psych-result-row span:last-child { font-size: 10px; color: var(--text-3); width: 40px; text-align: right; }

/* ===== ROOM CFM TAB ===== */
.room-cfm-header {
  display: flex; align-items: center; padding: 4px 0;
  font-size: 9px; text-transform: uppercase; letter-spacing: 0.06em;
  color: var(--text-3); font-weight: 600; border-bottom: 1px solid var(--border-subtle);
  margin-bottom: 6px;
}
.room-card {
  background: var(--bg-2); border: 1px solid var(--border-subtle);
  border-radius: 16px; padding: 16px; margin-bottom: 8px;
  transition: border-color 0.2s;
}
.room-card:focus-within { border-color: var(--accent); }
.room-card-header { display: flex; align-items: center; gap: 12px; margin-bottom: 12px; }
.room-card-remove {
  width: 28px; height: 28px; border-radius: 8px;
  background: var(--red-subtle); color: var(--red);
  border: none; font-size: 16px;
  display: flex; align-items: center; justify-content: center;
  cursor: pointer;
}
.room-card-remove:hover { background: rgba(248,113,113,0.2); }
.room-card-name {
  flex: 1; background: var(--bg-1);
  border: 1px solid var(--border-subtle); border-radius: 10px;
  padding: 8px 12px; color: var(--text-0);
  font-size: var(--text-base); font-weight: 500;
}
.room-card-cfm {
  font-family: 'JetBrains Mono', monospace;
  font-size: 20px; font-weight: 600;
  color: var(--green); min-width: 80px; text-align: right;
}
.room-card-cfm-unit { font-size: 10px; color: var(--text-2); font-weight: 500; }
.room-card-body { display: grid; grid-template-columns: 1fr 1fr; gap: 8px; }
.room-input-group { display: flex; flex-direction: column; gap: 4px; }
.room-input-label { font-size: var(--text-xs); text-transform: uppercase; letter-spacing: 0.06em; color: var(--text-3); font-weight: 600; }
.room-input-field {
  background: var(--bg-3); border: 1px solid var(--border-default);
  border-radius: 10px; padding: 8px 10px; color: var(--text-0);
  font-size: 12px; font-family: 'JetBrains Mono', monospace; width: 100%;
}
.room-type-select {
  background: var(--bg-3); border: 1px solid var(--border-default);
  border-radius: 10px; padding: 8px 10px; color: var(--text-0);
  font-size: 11px; width: 100%; grid-column: 1 / -1;
}
.room-card-info {
  display: flex; justify-content: space-between;
  font-size: 10px; color: var(--text-3); margin-top: 8px;
  padding-top: 8px; border-top: 1px solid var(--border-subtle);
}
.room-card-info span { font-family: 'JetBrains Mono', monospace; }

@media (max-width: 600px) {
  .sys-config-grid { grid-template-columns: 1fr; }
  .plenum-grid { grid-template-columns: 1fr 1fr; }
  .sys-totals-grid { grid-template-columns: 1fr 1fr; }
  .cfm-est-room { grid-template-columns: 20px 1fr 60px 50px; }
  .input-grid { grid-template-columns: 1fr; }
  .results-grid { grid-template-columns: 1fr 1fr; }
  .result-value { font-size: 22px; }
}

/* ===== FOOTER ===== */
footer { text-align: center; padding: 24px; margin-top: 20px; border-top: 1px solid var(--border-subtle); }
footer a { color: var(--text-3); font-size: 11px; text-decoration: none; }
footer a:hover { color: var(--text-2); }

/* ===== Duct Graphic ===== */
.duct-visual { display: flex; align-items: center; justify-content: center; gap: 20px; margin: 16px 0; flex-wrap: wrap; }
.duct-cross-section { width: 120px; height: 120px; position: relative; }

/* ===== Info note ===== */
.info-note {
  display: flex; align-items: flex-start; gap: 8px;
  padding: 12px 14px; border-radius: 14px;
  background: var(--accent-subtle);
  border: 1px solid rgba(79,140,255,0.2);
  margin-top: 12px; font-size: 12px;
  color: var(--accent); line-height: 1.5;
}
.info-note svg { width: 16px; height: 16px; flex-shrink: 0; margin-top: 1px; }

/* ===== FRICTION RATE WORKSHEET ===== */
.fr-step {
  background: var(--bg-2); border: 1px solid var(--border-subtle);
  border-radius: 20px; padding: 20px; margin-bottom: 12px;
}
.fr-step-header { display: flex; align-items: center; gap: 10px; margin-bottom: 12px; }
.fr-step-num {
  background: var(--accent); color: #fff;
  width: 26px; height: 26px; border-radius: 50%;
  display: flex; align-items: center; justify-content: center;
  font-size: 13px; font-weight: 700; flex-shrink: 0;
}
.fr-step-title { font-size: 13px; font-weight: 700; letter-spacing: 0.04em; text-transform: uppercase; color: var(--text-0); }
.fr-row { display: grid; grid-template-columns: 1fr 1fr; gap: 10px; margin-bottom: 8px; }
.fr-field { display: flex; flex-direction: column; gap: 6px; }
.fr-label { font-size: 11px; color: var(--text-2); font-weight: 500; letter-spacing: 0.04em; }
.fr-input-wrap { display: flex; align-items: center; gap: 6px; }
.fr-input {
  background: var(--bg-3); border: 1.5px solid var(--border-default);
  border-radius: 12px; color: var(--text-0);
  font-family: 'JetBrains Mono', monospace; font-size: 14px;
  padding: 10px 12px; width: 100%; outline: none;
  transition: border-color 0.2s; -webkit-appearance: none; touch-action: manipulation;
}
.fr-input:focus { border-color: var(--accent); box-shadow: var(--accent-glow); }
.fr-select { cursor: pointer; }
.fr-unit { font-size: 11px; color: var(--text-3); white-space: nowrap; min-width: 30px; }
.fr-losses-grid { display: flex; flex-direction: column; gap: 6px; }
.fr-loss-row {
  display: flex; align-items: center; justify-content: space-between;
  gap: 8px; padding: 4px 0; border-bottom: 1px solid var(--border-subtle);
}
.fr-loss-row:last-child { border-bottom: none; }
.fr-loss-label { font-size: 12px; color: var(--text-2); flex: 1; }
.fr-input-sm { max-width: 130px; }
.fr-input-sm .fr-input { padding: 6px 8px; font-size: 13px; text-align: right; }
.fr-total-row { border-top: 2px solid var(--accent); border-bottom: none; padding-top: 8px; margin-top: 4px; }
.fr-result { font-family: 'JetBrains Mono', monospace; font-size: 14px; font-weight: 700; color: var(--accent); min-width: 60px; text-align: right; }
.fr-formula {
  font-family: 'JetBrains Mono', monospace; font-size: 12px; color: var(--text-2);
  background: var(--bg-3); padding: 8px 10px; border-radius: 10px; margin-bottom: 10px; text-align: center;
}
.fr-calc-display {
  display: flex; align-items: baseline; justify-content: center; gap: 8px;
  font-family: 'JetBrains Mono', monospace; font-size: 16px; color: var(--text-0);
  padding: 12px; background: var(--bg-3); border-radius: 14px; flex-wrap: wrap;
}
.fr-op { color: var(--text-3); font-size: 14px; }
.fr-result-big { font-size: 22px; font-weight: 700; color: var(--accent); }
.fr-unit-big { font-size: 12px; color: var(--text-3); }
.fr-result-card { border-radius: 16px; padding: 16px; margin-bottom: 12px; }
.fr-result-card.fr-result-ok { background: var(--green-subtle); border: 1px solid rgba(52,211,153,0.3); }
.fr-result-card.fr-result-warn { background: var(--amber-subtle); border: 1px solid rgba(251,191,36,0.3); }
.fr-result-card.fr-result-bad { background: var(--red-subtle); border: 1px solid rgba(248,113,113,0.3); }
.fr-result-header { display: flex; align-items: center; gap: 10px; font-size: 14px; font-weight: 700; letter-spacing: 0.02em; }
.fr-result-ok .fr-result-header { color: var(--green); }
.fr-result-warn .fr-result-header { color: var(--amber); }
.fr-result-bad .fr-result-header { color: var(--red); }
.fr-result-msg { font-size: 12px; color: var(--text-2); margin-top: 6px; line-height: 1.5; }
.fr-chart-wrap { background: var(--bg-3); border-radius: 14px; padding: 12px; overflow-x: auto; -webkit-overflow-scrolling: touch; }
.fr-chart-wrap canvas { display: block; margin: 0 auto; max-width: 100%; height: auto; }
.fr-factor-display {
  font-family: 'JetBrains Mono', monospace; font-size: 18px; font-weight: 700;
  color: var(--text-0); background: var(--bg-3); border-radius: 10px; padding: 8px 10px; text-align: center;
}

@media (max-width: 600px) {
  .fr-row { grid-template-columns: 1fr; }
  .fr-calc-display { font-size: 14px; gap: 5px; }
  .fr-result-big { font-size: 18px; }
  .fr-loss-label { font-size: 11px; }
  .fr-input-sm { max-width: 110px; }
}

/* ===== FILTER PD CALCULATOR ===== */
.filter-mfg-btns { display: flex; flex-wrap: wrap; gap: 6px; }
.filter-mfg-btns .seg-btn { flex: 1; min-width: 80px; text-align: center; }
.filter-result-card { background: var(--bg-3); border: 1px solid var(--border-subtle); border-radius: 16px; padding: 16px; }
.filter-result-grid { display: grid; grid-template-columns: repeat(3, 1fr); gap: 12px; text-align: center; }
.filter-result-item { padding: 8px 4px; }
.filter-result-value { font-family: 'JetBrains Mono', monospace; font-size: 22px; font-weight: 700; color: var(--accent); }
.filter-result-unit { font-size: 10px; color: var(--text-2); text-transform: uppercase; letter-spacing: 0.04em; }
.filter-result-label { font-size: 11px; color: var(--text-3); margin-top: 2px; }
.filter-note {
  margin-top: 12px; padding: 10px;
  background: var(--amber-subtle); border: 1px solid rgba(251,191,36,0.25);
  border-radius: 12px; font-size: 12px; color: var(--amber); line-height: 1.4;
}
.filter-apply-btn {
  display: flex; align-items: center; justify-content: center;
  width: 100%; margin-top: 14px; padding: 14px;
  background: linear-gradient(135deg, var(--accent) 0%, var(--accent-strong) 100%);
  color: #fff; border: none; border-radius: 14px;
  font-size: var(--text-base); font-weight: 700; cursor: pointer;
  -webkit-tap-highlight-color: transparent; touch-action: manipulation;
  height: 52px; box-shadow: 0 4px 12px rgba(79,140,255,0.25);
  transition: transform 0.15s, box-shadow 0.15s;
}
.filter-apply-btn:active { transform: scale(0.97); box-shadow: 0 2px 8px rgba(79,140,255,0.15); }

/* ===== RETURN PLENUM ===== */
.ret-plenum-title { color: var(--amber); }

/* ===== FILTER WARNING BANNERS ===== */
.filter-warning-banner {
  display: flex; align-items: flex-start; gap: 8px;
  padding: 12px 14px; background: var(--amber-subtle);
  border: 1px solid rgba(251,191,36,0.25); border-radius: 14px;
  margin: 8px 0; font-size: 12px; line-height: 1.5; color: var(--amber);
}
.filter-warning-banner svg { flex-shrink: 0; margin-top: 1px; }
.filter-warning-banner.danger { background: var(--red-subtle); border-color: rgba(248,113,113,0.25); color: var(--red); }
.filter-inline-panel {
  background: var(--bg-3); border: 1px solid var(--border-subtle);
  border-radius: 14px; padding: 14px; margin: 8px 0;
}
.filter-inline-title { font-size: 12px; font-weight: 700; color: var(--text-0); margin-bottom: 8px; display: flex; align-items: center; gap: 6px; }
.filter-inline-title svg { width: 14px; height: 14px; }
.filter-inline-grid { display: grid; grid-template-columns: 1fr 1fr; gap: 6px; }
.filter-inline-stat { background: var(--bg-2); padding: 8px; border-radius: 10px; text-align: center; }
.filter-inline-stat-val { font-family: 'JetBrains Mono', monospace; font-size: 16px; font-weight: 700; }
.filter-inline-stat-val.ok { color: var(--green); }
.filter-inline-stat-val.warn { color: var(--amber); }
.filter-inline-stat-val.danger { color: var(--red); }
.filter-inline-stat-label { font-size: 9px; color: var(--text-2); text-transform: uppercase; letter-spacing: 0.04em; }
.filter-toggle-row { display: flex; align-items: center; gap: 8px; padding: 8px 0; }
.filter-toggle-label { font-size: 12px; font-weight: 600; color: var(--text-0); flex: 1; }
.filter-select-row { display: grid; grid-template-columns: 1fr 1fr; gap: 6px; margin-top: 6px; }
.filter-select-row select, .filter-select-row input { font-size: 12px; }
.filter-impact-card { background: var(--bg-2); border: 1px solid var(--border-subtle); border-radius: 14px; padding: 12px; margin-top: 8px; }
.filter-impact-title { font-size: 11px; font-weight: 700; color: var(--amber); margin-bottom: 6px; text-transform: uppercase; letter-spacing: 0.06em; }
.filter-impact-row {
  display: flex; justify-content: space-between; align-items: center;
  font-size: 12px; padding: 3px 0; border-bottom: 1px solid var(--border-subtle);
}
.filter-impact-row:last-child { border: none; }
.filter-impact-label { color: var(--text-2); }
.filter-impact-value { font-family: 'JetBrains Mono', monospace; font-weight: 600; }

/* ===== STATUS PILLS ===== */
.pill-sup { background: var(--red-subtle); color: var(--red); padding: 2px 8px; border-radius: 8px; font-size: 10px; font-weight: 600; }
.pill-rtn { background: var(--amber-subtle); color: var(--amber); padding: 2px 8px; border-radius: 8px; font-size: 10px; font-weight: 600; }
.pill-pass { background: var(--green-subtle); color: var(--green); padding: 2px 8px; border-radius: 8px; font-size: 10px; font-weight: 600; }
.pill-fail { background: var(--red-subtle); color: var(--red); padding: 2px 8px; border-radius: 8px; font-size: 10px; font-weight: 600; }
</style>'''

# ============================================================
# STEP 4: Build new second CSS block (wizard styles)
# ============================================================
new_css_2 = '''<style>
/* ===== WIZARD STEP BAR ===== */
.wiz-step-bar {
  display: flex; align-items: center; justify-content: space-between;
  padding: 14px 20px 8px; gap: 0;
}
.wiz-pill {
  display: flex; align-items: center; gap: 5px;
  padding: 6px 10px; border-radius: 20px;
  border: 1px solid var(--border-default);
  background: var(--bg-3); cursor: pointer;
  transition: all .2s; min-height: 36px; min-width: 44px; justify-content: center;
}
.wiz-pill.active {
  background: var(--accent); border-color: var(--accent);
  box-shadow: 0 2px 12px rgba(79,140,255,.3);
}
.wiz-pill.done { background: var(--green-subtle); border-color: var(--green); }
.wiz-pill-num { font-size: 11px; font-weight: 700; color: var(--text-3); line-height: 1; min-width: 14px; text-align: center; }
.wiz-pill.active .wiz-pill-num, .wiz-pill.done .wiz-pill-num { color: #fff; }
.wiz-pill.done .wiz-pill-num { color: var(--green); }
.wiz-pill-lbl { font-size: 11px; font-weight: 600; color: var(--text-3); white-space: nowrap; }
.wiz-pill.active .wiz-pill-lbl { color: #fff; }
.wiz-pill.done .wiz-pill-lbl { color: var(--green); }
.wiz-pill-sep { color: var(--border-default); display: flex; align-items: center; flex-shrink: 0; }
.wiz-progress-track { height: 3px; background: var(--bg-2); margin: 0 20px 12px; border-radius: 2px; overflow: hidden; }
.wiz-progress-fill { height: 100%; border-radius: 2px; background: linear-gradient(90deg, var(--accent), #7aadff); width: 25%; transition: width .5s cubic-bezier(.4,0,.2,1); }

/* SVG Fitting Animations */
@keyframes svgFadeSlide { from { opacity: 0; transform: translateY(8px); } to { opacity: 1; transform: translateY(0); } }
.wiz-fitting-svg { animation: svgFadeSlide 0.3s ease-out; display: flex; justify-content: center; padding: 8px 0; }
.wiz-fitting-svg svg { max-width: 120px; max-height: 80px; }
@keyframes flowDash { to { stroke-dashoffset: -20; } }
.plenum-flow { stroke-dasharray: 8 6; animation: flowDash 0.8s linear infinite; }
.plenum-svg-wrap { animation: svgFadeSlide 0.3s ease-out; display: flex; justify-content: center; padding: 6px 0; }
.plenum-svg-wrap svg { max-width: 200px; max-height: 120px; width: 100%; }

/* Wizard Steps */
.wiz-step { display: none; padding: 0 20px 16px; }
.wiz-step.active { display: block; animation: wizFadeIn .3s ease forwards; }
@keyframes wizFadeIn { from { opacity:0; transform:translateY(6px); } to { opacity:1; transform:translateY(0); } }

/* Prompt Boxes */
.wiz-prompt {
  background: var(--bg-3); border-left: 3px solid var(--accent);
  border-radius: 0 12px 12px 0; padding: 12px 14px; margin-bottom: 10px;
}
.wiz-prompt-q {
  font-size: 13px; font-weight: 600; color: var(--text-0);
  display: flex; align-items: center; gap: 7px; margin-bottom: 4px;
}
.wiz-prompt-q svg { color: var(--accent); flex-shrink: 0; }
.wiz-prompt-help { font-size: 11px; color: var(--text-2); line-height: 1.5; }

/* Option Grid */
.opt-grid { display: grid; grid-template-columns: 1fr 1fr; gap: 8px; margin-bottom: 12px; }
.opt-btn {
  background: var(--bg-2); border: 1.5px solid var(--border-default);
  border-radius: 16px; padding: 16px 12px; text-align: center;
  cursor: pointer; transition: all 0.2s; position: relative; overflow: hidden;
  min-height: 84px; display: flex; flex-direction: column;
  align-items: center; justify-content: center;
  -webkit-tap-highlight-color: transparent;
}
.opt-btn:active { transform: scale(.96); }
.opt-btn.active {
  border-color: var(--accent); background: var(--accent-subtle);
  box-shadow: inset 0 0 0 1px var(--accent), var(--accent-glow);
}
.opt-btn .opt-icon { margin-bottom: 6px; display: flex; justify-content: center; align-items: center; }
.opt-btn .opt-icon svg { width: 24px; height: 24px; }
.opt-btn .opt-label { font-size: var(--text-sm); font-weight: 600; color: var(--text-0); }
.opt-btn.active .opt-label { color: var(--accent); }
.opt-btn .opt-note { font-size: var(--text-xs); color: var(--text-2); margin-top: 4px; }
.opt-btn.active .opt-note { color: var(--accent); opacity: 0.8; }

/* Info Banner */
.wiz-info-banner {
  background: var(--accent-subtle); border: 1px solid rgba(79,140,255,.2);
  border-radius: 14px; padding: 12px 14px; margin-bottom: 14px;
  display: flex; align-items: flex-start; gap: 8px;
}
.wiz-info-banner svg { flex-shrink: 0; color: var(--accent); margin-top: 1px; }
.wiz-info-banner p { font-size: 11px; color: var(--text-1); line-height: 1.5; }
.wiz-info-banner strong { color: var(--accent); }

/* Trunk Cards */
.wiz-trunk-card {
  background: var(--bg-2); border: 1px solid var(--border-subtle);
  border-left: 3px solid var(--accent); border-radius: 14px;
  padding: 16px; margin-bottom: 12px; position: relative;
}
.wiz-trunk-label-row { display: flex; align-items: center; justify-content: space-between; margin-bottom: 10px; }
.wiz-trunk-label {
  font-size: 12px; font-weight: 700; color: var(--accent);
  text-transform: uppercase; letter-spacing: 0.06em;
  display: flex; align-items: center; gap: 6px;
}
.wiz-trunk-remove {
  width: 30px; height: 30px; border-radius: 8px;
  background: var(--bg-3); border: 1px solid var(--border-default);
  display: flex; align-items: center; justify-content: center;
  cursor: pointer; transition: all .15s; flex-shrink: 0;
}
.wiz-trunk-remove:hover { background: var(--red-subtle); border-color: var(--red); }
.wiz-trunk-remove svg { width: 13px; height: 13px; color: var(--text-2); }
.wiz-trunk-remove:hover svg { color: var(--red); }
.wiz-shape-toggle {
  display: flex; border: 1px solid var(--border-default);
  border-radius: 10px; overflow: hidden; margin-bottom: 10px;
}
.wiz-shape-btn {
  flex: 1; padding: 9px 6px; text-align: center; font-size: 11px; font-weight: 600;
  color: var(--text-2); background: var(--bg-2); cursor: pointer;
  min-height: 44px; display: flex; align-items: center; justify-content: center;
  gap: 4px; transition: all .15s; -webkit-tap-highlight-color: transparent;
}
.wiz-shape-btn.active { background: var(--accent); color: #fff; }
.wiz-shape-btn svg { width: 13px; height: 13px; }

/* Input Rows */
.wiz-input-row { display: flex; gap: 8px; align-items: flex-end; margin-bottom: 10px; }
.wiz-input-group { flex: 1; }
.wiz-input-label {
  font-size: 10px; color: var(--text-2); text-transform: uppercase;
  letter-spacing: 0.06em; margin-bottom: 4px; font-weight: 600;
}

/* Branch Area */
.wiz-trunk-group { margin-bottom: 18px; }
.wiz-trunk-group-hdr {
  display: flex; align-items: center; gap: 7px;
  padding: 7px 0; margin-bottom: 6px; border-bottom: 1px solid var(--bg-2);
}
.wiz-trunk-group-hdr svg { width: 15px; height: 15px; color: var(--accent); flex-shrink: 0; }
.wiz-trunk-group-lbl { font-size: 12px; font-weight: 700; color: var(--accent); text-transform: uppercase; letter-spacing: 0.06em; }
.wiz-add-branch-btn {
  display: flex; align-items: center; justify-content: center; gap: 6px;
  width: 100%; min-height: 44px; padding: 8px;
  background: transparent; border: 1px dashed var(--border-default);
  border-radius: 12px; color: var(--text-3);
  font-size: 12px; font-weight: 600; cursor: pointer;
  transition: all .15s; margin-top: 6px; -webkit-tap-highlight-color: transparent;
}
.wiz-add-branch-btn:hover { border-color: var(--accent); color: var(--accent); }
.wiz-add-branch-btn svg { width: 13px; height: 13px; }

/* Branch Items */
.wiz-branch-item {
  background: var(--bg-2); border: 1px solid var(--border-subtle);
  border-radius: 12px; padding: 10px 12px; margin-bottom: 6px;
  display: flex; align-items: center; gap: 8px;
  cursor: pointer; transition: all .15s; min-height: 52px;
  -webkit-tap-highlight-color: transparent;
}
.wiz-branch-item.editing { border-color: var(--accent); background: var(--bg-3); }
.wiz-branch-num {
  width: 26px; height: 26px; background: var(--accent); border-radius: 50%;
  display: flex; align-items: center; justify-content: center;
  font-size: 11px; font-weight: 700; color: #fff; flex-shrink: 0;
}
.wiz-branch-info { flex: 1; min-width: 0; }
.wiz-branch-name { font-size: 12px; font-weight: 600; color: var(--text-0); white-space: nowrap; overflow: hidden; text-overflow: ellipsis; }
.wiz-branch-detail { font-size: 10px; color: var(--text-2); margin-top: 1px; }
.wiz-branch-badge { font-size: 10px; padding: 2px 7px; border-radius: 6px; font-weight: 600; flex-shrink: 0; }
.wiz-branch-badge.pending { background: var(--bg-2); color: var(--text-3); border: 1px solid var(--border-default); }
.wiz-branch-badge.done { background: var(--green-subtle); color: var(--green); border: 1px solid rgba(52,211,153,.2); }
.wiz-branch-badge.editing { background: var(--accent-subtle); color: var(--accent); border: 1px solid rgba(79,140,255,.2); }

/* Branch Edit Form */
.wiz-branch-form {
  background: var(--bg-3); border: 1px solid var(--accent);
  border-radius: 14px; padding: 14px; margin: 4px 0 10px;
}
.wiz-fittings-lbl { font-size: 10px; color: var(--text-2); text-transform: uppercase; letter-spacing: 0.06em; margin-bottom: 6px; font-weight: 600; }
.wiz-fit-btns { display: flex; gap: 5px; flex-wrap: wrap; margin-bottom: 8px; }
.wiz-fit-btn {
  background: var(--bg-2); border: 1px solid var(--border-default);
  border-radius: 10px; padding: 6px 9px; font-size: 11px;
  color: var(--text-0); cursor: pointer;
  display: flex; align-items: center; gap: 4px;
  min-height: 36px; transition: all .12s; -webkit-tap-highlight-color: transparent;
}
.wiz-fit-btn:active { background: var(--accent); border-color: var(--accent); color: #fff; }
.wiz-fit-btn svg { width: 13px; height: 13px; flex-shrink: 0; }
.wiz-fit-list { margin-top: 6px; }
.wiz-fit-item {
  display: flex; align-items: center; gap: 7px;
  padding: 5px 8px; background: var(--bg-1);
  border-radius: 8px; margin-bottom: 4px; font-size: 11px; color: var(--text-0);
}
.wiz-fit-item-name { flex: 1; }
.wiz-fit-item-eq { color: var(--amber); font-weight: 600; font-family: 'JetBrains Mono', monospace; font-size: 11px; }
.wiz-fit-item-rm {
  width: 20px; height: 20px; border-radius: 50%;
  background: var(--bg-2); border: 1px solid var(--border-default);
  display: flex; align-items: center; justify-content: center;
  cursor: pointer; flex-shrink: 0; -webkit-tap-highlight-color: transparent;
}
.wiz-fit-item-rm:hover { background: var(--red-subtle); border-color: var(--red); }
.wiz-fit-item-rm svg { width: 10px; height: 10px; color: var(--text-2); }
.wiz-compression-box {
  background: var(--bg-1); border: 1px solid var(--border-default);
  border-radius: 10px; padding: 8px 10px; margin-bottom: 10px;
}
.wiz-compression-val { font-size: 12px; font-weight: 600; color: var(--amber); font-family: 'JetBrains Mono', monospace; margin-top: 4px; }
.wiz-save-row { display: flex; gap: 8px; margin-top: 10px; }
.wiz-btn-save {
  flex: 1; background: linear-gradient(135deg, var(--accent) 0%, var(--accent-strong) 100%);
  color: #fff; border: none; border-radius: 12px; padding: 10px;
  font-size: 13px; font-weight: 600; cursor: pointer; min-height: 44px;
  display: flex; align-items: center; justify-content: center; gap: 5px;
  transition: transform .15s; -webkit-tap-highlight-color: transparent;
  box-shadow: 0 4px 12px rgba(79,140,255,0.25);
}
.wiz-btn-save:active { transform: scale(0.97); }
.wiz-btn-rm {
  width: 44px; flex-shrink: 0; background: transparent;
  border: 1px solid var(--border-default); border-radius: 12px;
  display: flex; align-items: center; justify-content: center;
  cursor: pointer; min-height: 44px; transition: all .15s; -webkit-tap-highlight-color: transparent;
}
.wiz-btn-rm:hover { background: var(--red-subtle); border-color: var(--red); }
.wiz-btn-rm svg { width: 15px; height: 15px; color: var(--text-2); }

/* Nav Buttons */
.wiz-btn-primary {
  background: linear-gradient(135deg, var(--accent) 0%, var(--accent-strong) 100%);
  color: #fff; border: none; border-radius: 14px; padding: 14px 16px;
  font-size: var(--text-base); font-weight: 600; width: 100%;
  cursor: pointer; margin-top: 8px; min-height: 52px;
  display: flex; align-items: center; justify-content: center; gap: 8px;
  transition: transform 0.15s, box-shadow 0.15s;
  box-shadow: 0 4px 12px rgba(79,140,255,0.25);
  -webkit-tap-highlight-color: transparent;
  font-family: 'Inter', -apple-system, sans-serif;
}
.wiz-btn-primary:active { transform: scale(0.97); box-shadow: 0 2px 8px rgba(79,140,255,0.15); }
.wiz-btn-secondary {
  background: transparent; color: var(--accent);
  border: 1.5px solid rgba(79,140,255,0.3); border-radius: 14px;
  padding: 12px 16px; font-size: 13px; font-weight: 600; width: 100%;
  cursor: pointer; margin-top: 8px; min-height: 48px;
  display: flex; align-items: center; justify-content: center; gap: 6px;
  transition: all .15s; -webkit-tap-highlight-color: transparent;
  font-family: 'Inter', -apple-system, sans-serif;
}
.wiz-btn-secondary:active { background: var(--accent-subtle); }
.wiz-btn-add {
  background: transparent; border: 1px dashed var(--border-default);
  border-radius: 14px; padding: 11px; font-size: 13px; font-weight: 600;
  color: var(--text-2); width: 100%; cursor: pointer;
  margin-top: 4px; min-height: 48px;
  display: flex; align-items: center; justify-content: center; gap: 6px;
  transition: all .15s; -webkit-tap-highlight-color: transparent;
}
.wiz-btn-add:hover { border-color: var(--accent); color: var(--accent); }
.wiz-btn-add svg { width: 15px; height: 15px; }

/* Results */
.wiz-card-title {
  font-size: 12px; font-weight: 700; color: var(--accent);
  text-transform: uppercase; letter-spacing: 0.08em; margin-bottom: 12px;
  display: flex; align-items: center; gap: 7px;
}
.wiz-card-title svg { width: 15px; height: 15px; flex-shrink: 0; }
.wiz-results-grid { display: grid; grid-template-columns: 1fr 1fr; gap: 6px; margin-bottom: 4px; }
.wiz-result-cell {
  background: var(--bg-3); border: 1px solid var(--border-subtle);
  border-radius: 12px; padding: 12px; text-align: center;
}
.wiz-result-val { font-size: 20px; font-weight: 700; font-family: 'JetBrains Mono', monospace; }
.wiz-result-val.ok { color: var(--green); }
.wiz-result-val.warn { color: var(--amber); }
.wiz-result-val.bad { color: var(--red); }
.wiz-result-lbl { font-size: 9px; color: var(--text-2); text-transform: uppercase; letter-spacing: 0.04em; margin-top: 2px; }
.wiz-gauge-wrap { margin: 4px 0 8px; }
.wiz-gauge-label { font-size: 10px; color: var(--text-2); display: flex; justify-content: space-between; margin-bottom: 6px; font-weight: 600; }
.wiz-gauge-track { height: 14px; background: var(--bg-2); border-radius: 7px; overflow: hidden; }
.wiz-gauge-fill { height: 100%; border-radius: 7px; transition: width .6s cubic-bezier(.4,0,.2,1); }
.wiz-gauge-fill.green { background: linear-gradient(90deg, #059669, var(--green)); }
.wiz-gauge-fill.yellow { background: linear-gradient(90deg, var(--green), var(--amber)); }
.wiz-gauge-fill.red { background: linear-gradient(90deg, var(--amber), var(--red)); }
.wiz-gauge-markers { display: flex; justify-content: space-between; margin-top: 3px; font-size: 9px; color: var(--text-3); font-family: 'JetBrains Mono', monospace; }
.wiz-path-step { display: flex; align-items: flex-start; gap: 8px; padding: 5px 0; position: relative; }
.wiz-path-step-line { position: absolute; left: 11px; top: 28px; width: 2px; bottom: -5px; background: var(--border-default); z-index: 0; }
.wiz-path-step:last-child .wiz-path-step-line { display: none; }
.wiz-path-dot {
  width: 24px; height: 24px; border-radius: 50%;
  display: flex; align-items: center; justify-content: center;
  font-size: 9px; font-weight: 700; color: #fff; flex-shrink: 0; z-index: 1;
}
.wiz-path-dot.start { background: var(--accent); }
.wiz-path-dot.duct { background: var(--text-3); }
.wiz-path-dot.fitting { background: var(--amber); }
.wiz-path-dot.end { background: var(--green); }
.wiz-path-info { flex: 1; min-width: 0; }
.wiz-path-name { font-size: 12px; font-weight: 600; color: var(--text-0); }
.wiz-path-eq { font-size: 11px; color: var(--amber); font-weight: 600; font-family: 'JetBrains Mono', monospace; flex-shrink: 0; margin-top: 3px; }
.wiz-run-item { background: var(--bg-2); border: 1px solid var(--border-subtle); border-radius: 12px; padding: 10px 12px; margin-bottom: 6px; }
.wiz-run-header { display: flex; align-items: center; gap: 8px; margin-bottom: 4px; }
.wiz-run-name { font-size: 12px; font-weight: 600; color: var(--text-0); flex: 1; }
.wiz-run-tel { font-size: 11px; font-weight: 700; font-family: 'JetBrains Mono', monospace; }
.wiz-run-fr { font-size: 10px; font-weight: 600; font-family: 'JetBrains Mono', monospace; }
.wiz-tel-bar-wrap { height: 5px; background: var(--bg-1); border-radius: 3px; overflow: hidden; }
.wiz-tel-bar { height: 100%; border-radius: 3px; transition: width .4s ease; }
.wiz-trunk-result-hdr {
  display: flex; align-items: center; gap: 7px;
  padding: 6px 0; margin-bottom: 6px; border-bottom: 1px solid var(--bg-2);
}
.wiz-trunk-result-hdr svg { width: 14px; height: 14px; color: var(--accent); }
.wiz-trunk-result-lbl { font-size: 11px; font-weight: 700; color: var(--accent); text-transform: uppercase; letter-spacing: 0.06em; flex: 1; }
.wiz-trunk-result-maxtel { font-size: 10px; color: var(--amber); font-family: 'JetBrains Mono', monospace; }
.wiz-crit-label { font-size: 12px; font-weight: 600; color: var(--amber); display: flex; align-items: center; gap: 5px; margin-bottom: 10px; }
</style>'''

# ============================================================
# STEP 5: Apply replacements
# ============================================================
# Replace first style block
new_content = content[:first_style_start] + new_css_1 + content[first_style_end:]

# Recalculate second style position after replacement
offset_diff = len(new_css_1) - (first_style_end - first_style_start)
second_start_new = content.index('<style>\n/* ===== WIZARD STEP BAR') + offset_diff
second_end_new = content.index('</style>', content.index('<style>\n/* ===== WIZARD STEP BAR')) + len('</style>') + offset_diff

# Replace in the new content
second_style_start_new = new_content.index('<style>\n/* ===== WIZARD STEP BAR')
second_style_end_new = new_content.index('</style>', second_style_start_new) + len('</style>')
new_content = new_content[:second_style_start_new] + new_css_2 + new_content[second_style_end_new:]

# Write the file
with open('index.html', 'w') as f:
    f.write(new_content)

# Verify
with open('index.html', 'r') as f:
    result = f.read()
    
print(f"Original length: {len(content)}")
print(f"New length: {len(result)}")
print(f"Script blocks intact: {'<script>' in result}")
print(f"Page IDs present: {all(f'id=\"page-{p}\"' in result for p in ['roomcfm','calculator','eqlen','system','frworksheet','filters','psychro'])}")

# Verify no script blocks were modified
import re
orig_scripts = re.findall(r'<script[^>]*>.*?</script>', content, re.DOTALL)
new_scripts = re.findall(r'<script[^>]*>.*?</script>', result, re.DOTALL)
print(f"Original script blocks: {len(orig_scripts)}")
print(f"New script blocks: {len(new_scripts)}")
for i, (o, n) in enumerate(zip(orig_scripts, new_scripts)):
    if o == n:
        print(f"  Script block {i+1}: IDENTICAL ✓")
    else:
        print(f"  Script block {i+1}: DIFFERENT ✗")
        
# Check all data attributes
orig_data = set(re.findall(r'data-[a-z-]+="[^"]*"', content))
new_data = set(re.findall(r'data-[a-z-]+="[^"]*"', result))
missing_data = orig_data - new_data
if missing_data:
    print(f"Missing data attributes: {missing_data}")
else:
    print(f"All {len(orig_data)} data attributes preserved ✓")
    
# Check all IDs
orig_ids = set(re.findall(r'id="[^"]*"', content))
new_ids = set(re.findall(r'id="[^"]*"', result))
missing_ids = orig_ids - new_ids
if missing_ids:
    print(f"Missing IDs: {missing_ids}")
else:
    print(f"All {len(orig_ids)} IDs preserved ✓")
