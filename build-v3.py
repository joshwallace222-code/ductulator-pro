#!/usr/bin/env python3
"""Build the V3 redesign of DuctCalc Pro."""

# Read the original script blocks
with open('/home/user/workspace/ductulator-pro/script-main-body.txt', 'r') as f:
    main_script = f.read()

with open('/home/user/workspace/ductulator-pro/script-second-body.txt', 'r') as f:
    second_script = f.read()

# Build the new file
html = r'''<!DOCTYPE html>
<html lang="en" data-theme="dark">
<head>
<!--
   ______                            __
  / ____/___  ____ ___  ____  __  __/ /____  _____
 / /   / __ \/ __ `__ \/ __ \/ / / / __/ _ \/ ___/
/ /___/ /_/ / / / / / / /_/ / /_/ / /_/  __/ /
\____/\____/_/ /_/ /_/ .___/\__,_/\__/\___/_/
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
<meta http-equiv="Pragma" content="no-cache">
<meta http-equiv="Expires" content="0">
<title>DuctCalc Pro — HVAC Duct Design Tool</title>
<script src="https://cdnjs.cloudflare.com/ajax/libs/jspdf/2.5.1/jspdf.umd.min.js"></script>
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&family=Space+Mono:wght@400;700&display=swap" rel="stylesheet">

<style>
/* ============================================================
   DuctCalc Pro V3 — Warm Forge Design System
   Ground-up redesign with gold/amber accent palette
   ============================================================ */

:root {
  /* Surfaces — warm charcoal */
  --surface-0: #111113;
  --surface-1: #19191d;
  --surface-2: #222228;
  --surface-3: #2c2c34;
  --surface-4: #37373f;

  /* Text */
  --text-primary: #ececf0;
  --text-secondary: #9898a8;
  --text-muted: #606070;

  /* Accent — warm amber/gold */
  --accent: #e8a838;
  --accent-light: #f0c060;
  --accent-dim: rgba(232,168,56,0.15);
  --accent-glow: 0 0 24px rgba(232,168,56,0.2);

  /* Semantic */
  --pass: #4ade80;
  --warn: #fbbf24;
  --fail: #f87171;
  --info: #60a5fa;

  /* Supply/Return */
  --supply-color: #f87171;
  --return-color: #60a5fa;
  --airflow-color: #4ade80;

  /* Effects */
  --glass: rgba(25,25,29,0.8);
  --glass-border: rgba(255,255,255,0.08);
  --shadow-sm: 0 2px 8px rgba(0,0,0,0.3);
  --shadow-md: 0 8px 24px rgba(0,0,0,0.4);
  --shadow-lg: 0 16px 48px rgba(0,0,0,0.5);
  --radius-sm: 10px;
  --radius-md: 16px;
  --radius-lg: 24px;
  --radius-xl: 32px;

  /* Type scale */
  --text-xs: 10px;
  --text-sm: 12px;
  --text-base: 14px;
  --text-lg: 16px;
  --text-xl: 18px;
  --text-2xl: 24px;
  --text-3xl: 32px;

  /* Legacy aliases — JS uses these in inline styles */
  --bg-0: #111113;
  --bg-1: #19191d;
  --bg-2: #222228;
  --bg-3: #2c2c34;
  --bg-4: #37373f;
  --bg-primary: #111113;
  --bg-card: #222228;
  --bg-elevated: #2c2c34;
  --bg-input: #19191d;
  --border-subtle: rgba(255,255,255,0.06);
  --border-default: rgba(255,255,255,0.10);
  --border-strong: rgba(255,255,255,0.16);
  --border: rgba(255,255,255,0.10);
  --border-focus: #e8a838;
  --border-light: rgba(255,255,255,0.16);
  --text-0: #ececf0;
  --text-1: #c8c8d4;
  --text-2: #9898a8;
  --text-3: #606070;
  --text: #ececf0;
  --text-muted: #9898a8;
  --text-dim: #606070;
  --accent-strong: #d49020;
  --accent-subtle: rgba(232,168,56,0.12);
  --accent-hover: #d49020;
  --accent-glow-legacy: rgba(232,168,56,0.15);
  --green: #4ade80;
  --green-subtle: rgba(74,222,128,0.12);
  --amber: #fbbf24;
  --amber-subtle: rgba(251,191,36,0.12);
  --red: #f87171;
  --red-subtle: rgba(248,113,113,0.12);
  --success: #4ade80;
  --warning: #fbbf24;
  --danger: #f87171;
  --supply: #f87171;
  --return: #60a5fa;
  --airflow: #4ade80;
  --red-glow: #e8a838;
  --red-dark: #d49020;
  --bg: #111113;
  --surface: #222228;
  --surface-2: #2c2c34;
  --surface-3: #37373f;
  --yellow: #fbbf24;
  --orange: #fbbf24;
  --blue: #60a5fa;
  --card-shadow: none;
  --glow-red: 0 0 20px rgba(232,168,56,0.15);
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
  background: var(--surface-0);
  color: var(--text-primary);
  min-height: 100dvh;
  overflow-x: hidden;
  padding-bottom: 76px;
  line-height: 1.5;
  -webkit-tap-highlight-color: transparent;
  overscroll-behavior: none;
}

/* Mono for numbers — Space Mono */
.mono, [class*="result-val"], [class*="cfm"], input[type="number"],
.slider-value-input, .fr-input, .fr-result, .wiz-result-val,
.compression-readout-value, .dial-readout-value {
  font-family: 'Space Mono', monospace;
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
  padding: 10px 20px;
  background: rgba(17,17,19,0.85);
  backdrop-filter: blur(24px);
  -webkit-backdrop-filter: blur(24px);
  border-bottom: 1px solid var(--glass-border);
  display: flex;
  align-items: center;
  min-height: 56px;
  cursor: pointer;
}

.app-header-brand {
  display: flex;
  align-items: center;
  gap: 12px;
}

.app-logo {
  width: 36px;
  height: 36px;
  flex-shrink: 0;
}

.app-header-text {
  display: flex;
  flex-direction: column;
}

.app-header-name {
  font-size: var(--text-lg);
  font-weight: 800;
  color: var(--text-primary);
  letter-spacing: -0.03em;
  line-height: 1.2;
}

.app-header-tagline {
  font-size: 9px;
  color: var(--accent);
  text-transform: uppercase;
  letter-spacing: 0.12em;
  font-weight: 700;
}

/* ===== OLD NAV (hidden) ===== */
.nav { display: none !important; }
.nav-tabs { display: none; }
.nav-tab { display: none; }

/* ===== HOME PAGE ===== */
#page-home {
  display: none;
  padding: 24px 20px 40px;
  max-width: 480px;
  margin: 0 auto;
  animation: fadeSlideIn 0.4s ease;
}
#page-home.active { display: block; }

@keyframes fadeSlideIn {
  from { opacity: 0; transform: translateY(12px); }
  to { opacity: 1; transform: translateY(0); }
}

.home-hero {
  text-align: center;
  padding: 32px 0 28px;
}

.home-logo-mark {
  width: 80px;
  height: 80px;
  margin: 0 auto 16px;
}

.home-title {
  font-size: 28px;
  font-weight: 800;
  letter-spacing: -0.04em;
  color: var(--text-primary);
  margin-bottom: 4px;
}

.home-subtitle {
  font-size: 13px;
  color: var(--text-secondary);
  font-weight: 500;
}

.home-cards {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 12px;
  margin-bottom: 24px;
}

.home-card {
  background: var(--surface-2);
  border-radius: 24px;
  padding: 28px 16px 24px;
  text-align: center;
  cursor: pointer;
  transition: transform 0.15s, box-shadow 0.15s;
  position: relative;
  overflow: hidden;
}
.home-card::before {
  content: '';
  position: absolute;
  inset: 0;
  border-radius: 24px;
  border: 1.5px solid transparent;
  transition: border-color 0.2s;
}
.home-card:active {
  transform: scale(0.97);
}
.home-card:hover::before {
  border-color: var(--accent);
}

.home-card-icon {
  width: 48px;
  height: 48px;
  border-radius: 16px;
  display: flex;
  align-items: center;
  justify-content: center;
  margin: 0 auto 14px;
}
.home-card-icon svg { width: 24px; height: 24px; }

.home-card-icon.design {
  background: linear-gradient(135deg, rgba(232,168,56,0.2), rgba(232,168,56,0.05));
  color: var(--accent);
}
.home-card-icon.calc {
  background: linear-gradient(135deg, rgba(96,165,250,0.2), rgba(96,165,250,0.05));
  color: var(--info);
}

.home-card-title {
  font-size: 15px;
  font-weight: 700;
  color: var(--text-primary);
  margin-bottom: 4px;
}

.home-card-desc {
  font-size: 11px;
  color: var(--text-secondary);
  line-height: 1.4;
}

.home-tools-label {
  font-size: 10px;
  font-weight: 700;
  text-transform: uppercase;
  letter-spacing: 0.1em;
  color: var(--text-muted);
  margin-bottom: 10px;
}

.home-tools-row {
  display: grid;
  grid-template-columns: repeat(4, 1fr);
  gap: 8px;
}

.home-tool {
  background: var(--surface-1);
  border-radius: 16px;
  padding: 14px 6px 12px;
  text-align: center;
  cursor: pointer;
  transition: all 0.15s;
  border: 1px solid transparent;
}
.home-tool:active { transform: scale(0.95); }
.home-tool:hover { border-color: var(--glass-border); }

.home-tool-icon {
  width: 32px;
  height: 32px;
  border-radius: 10px;
  display: flex;
  align-items: center;
  justify-content: center;
  margin: 0 auto 6px;
}
.home-tool-icon svg { width: 16px; height: 16px; }

.home-tool-icon.eqlen { background: rgba(251,191,36,0.12); color: var(--warn); }
.home-tool-icon.frwork { background: rgba(248,113,113,0.12); color: var(--fail); }
.home-tool-icon.filter { background: rgba(74,222,128,0.12); color: var(--pass); }
.home-tool-icon.psychro { background: rgba(96,165,250,0.12); color: var(--info); }

.home-tool-name {
  font-size: 9px;
  font-weight: 600;
  color: var(--text-secondary);
  letter-spacing: 0.02em;
}

/* ===== BOTTOM NAVIGATION ===== */
.bottom-nav {
  position: fixed;
  bottom: 0;
  left: 0;
  right: 0;
  height: 64px;
  background: var(--glass);
  backdrop-filter: blur(24px);
  -webkit-backdrop-filter: blur(24px);
  border-top: 1px solid var(--glass-border);
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
  color: var(--text-muted);
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
  padding: 8px 20px;
  font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif;
  min-width: 56px;
  min-height: 56px;
  justify-content: center;
}

.bottom-nav-item.active { color: var(--accent); }
.bottom-nav-item.active svg {
  filter: drop-shadow(0 0 8px rgba(232,168,56,0.4));
}
.bottom-nav-item svg { width: 22px; height: 22px; stroke-width: 1.5; }

/* ===== MORE PANEL — iOS Control Center style ===== */
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
  -webkit-tap-highlight-color: transparent;
}

.more-panel-sheet {
  position: absolute;
  bottom: 0;
  left: 0;
  right: 0;
  background: var(--surface-2);
  border-radius: 28px 28px 0 0;
  padding: 12px 20px 40px;
  max-height: 55vh;
  transform: translateY(100%);
  transition: transform 0.35s cubic-bezier(0.32, 0.72, 0, 1);
  padding-bottom: calc(40px + env(safe-area-inset-bottom, 0));
  overflow-y: auto;
}
.more-panel.open .more-panel-sheet { transform: translateY(0); }

.more-panel-handle {
  width: 40px;
  height: 4px;
  border-radius: 2px;
  background: var(--surface-4);
  margin: 0 auto 20px;
}

.more-panel-title {
  font-size: var(--text-sm);
  font-weight: 700;
  color: var(--text-secondary);
  letter-spacing: 0.08em;
  text-transform: uppercase;
  margin-bottom: 16px;
}

.more-panel-grid {
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  gap: 10px;
}

.more-tool {
  background: var(--surface-3);
  border: none;
  border-radius: 20px;
  padding: 22px 12px 18px;
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 8px;
  transition: all 0.15s;
  cursor: pointer;
  -webkit-tap-highlight-color: transparent;
  touch-action: manipulation;
  color: var(--text-secondary);
}
.more-tool:active { transform: scale(0.95); }
.more-tool svg { width: 24px; height: 24px; opacity: 0.8; }
.more-tool span { font-size: 11px; font-weight: 600; }

/* ===== APP CONTAINER ===== */
.app-container {
  max-width: 480px;
  margin: 0 auto;
  padding: 0 16px;
}

/* ===== PAGE SYSTEM ===== */
.page { display: none; padding-top: 8px; padding-bottom: 24px; }
.page.active { display: block; animation: pageEnter 0.3s ease; }
@keyframes pageEnter {
  from { opacity: 0; transform: translateY(8px); }
  to { opacity: 1; transform: translateY(0); }
}

/* ===== CARDS / PANELS ===== */
.panel {
  background: var(--surface-2);
  border-radius: 20px;
  padding: 18px;
  margin-bottom: 12px;
  box-shadow: var(--shadow-sm);
}

.panel-title {
  font-size: 13px;
  font-weight: 700;
  color: var(--text-primary);
  margin-bottom: 12px;
  display: flex;
  align-items: center;
  gap: 8px;
  letter-spacing: -0.01em;
}
.panel-title svg { width: 18px; height: 18px; color: var(--accent); flex-shrink: 0; }

/* ===== INPUT FIELDS ===== */
.input-field, select.input-field {
  background: var(--surface-0);
  border: 1.5px solid transparent;
  border-radius: 14px;
  padding: 0 16px;
  height: 52px;
  font-size: 15px;
  color: var(--text-primary);
  box-shadow: inset 0 2px 4px rgba(0,0,0,0.2);
  transition: border-color 0.2s, box-shadow 0.2s;
  font-family: 'Space Mono', monospace;
  width: 100%;
  outline: none;
  -webkit-appearance: none;
  appearance: none;
}
.input-field:focus, select.input-field:focus {
  border-color: var(--accent);
  box-shadow: inset 0 2px 4px rgba(0,0,0,0.2), var(--accent-glow);
}

.input-label, .config-label {
  font-size: 10px;
  font-weight: 700;
  text-transform: uppercase;
  letter-spacing: 0.08em;
  color: var(--text-secondary);
  margin-bottom: 6px;
  display: block;
}

.input-group { margin-bottom: 8px; }

/* ===== SEGMENTED CONTROLS ===== */
.seg-control {
  background: var(--surface-0);
  border-radius: 14px;
  padding: 4px;
  display: flex;
  gap: 2px;
  box-shadow: inset 0 2px 4px rgba(0,0,0,0.15);
}
.seg-btn {
  flex: 1;
  height: 44px;
  border-radius: 11px;
  border: none;
  font-size: 13px;
  font-weight: 600;
  color: var(--text-muted);
  background: transparent;
  transition: all 0.2s;
  cursor: pointer;
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 5px;
  -webkit-tap-highlight-color: transparent;
  font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif;
  touch-action: manipulation;
}
.seg-btn.active {
  background: var(--surface-3);
  color: var(--text-primary);
  box-shadow: 0 2px 8px rgba(0,0,0,0.2);
}
.seg-btn:active { transform: scale(0.96); }

/* ===== OPTION BUTTONS (Wizard) ===== */
.opt-grid { display: grid; grid-template-columns: 1fr 1fr; gap: 10px; margin-bottom: 14px; }
.opt-btn {
  background: var(--surface-2);
  border: 2px solid transparent;
  border-radius: 20px;
  padding: 20px 14px;
  text-align: center;
  cursor: pointer;
  transition: all 0.2s;
  position: relative;
  overflow: hidden;
  min-height: 88px;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  -webkit-tap-highlight-color: transparent;
}
.opt-btn:active { transform: scale(0.96); }
.opt-btn.active {
  border-color: var(--accent);
  background: var(--accent-dim);
  box-shadow: var(--accent-glow);
}
.opt-btn .opt-icon { margin-bottom: 8px; display: flex; justify-content: center; align-items: center; }
.opt-btn .opt-icon svg { width: 24px; height: 24px; }
.opt-btn .opt-label { font-size: 13px; font-weight: 600; color: var(--text-primary); }
.opt-btn.active .opt-label { color: var(--accent); }
.opt-btn .opt-note { font-size: 11px; color: var(--text-secondary); margin-top: 4px; }
.opt-btn.active .opt-note { color: var(--accent-light); }

/* ===== BUTTONS ===== */
.btn-primary, .wiz-btn-primary {
  height: 56px;
  background: linear-gradient(135deg, var(--accent) 0%, #d49020 100%);
  color: #111;
  font-weight: 700;
  font-size: 15px;
  border: none;
  border-radius: 16px;
  box-shadow: 0 4px 16px rgba(232,168,56,0.3);
  transition: transform 0.12s, box-shadow 0.12s;
  cursor: pointer;
  width: 100%;
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 8px;
  margin-top: 8px;
  font-family: 'Inter', -apple-system, sans-serif;
  -webkit-tap-highlight-color: transparent;
}
.btn-primary:active, .wiz-btn-primary:active {
  transform: scale(0.96);
  box-shadow: 0 2px 8px rgba(232,168,56,0.2);
}

.wiz-btn-secondary {
  background: transparent;
  color: var(--accent);
  border: 1.5px solid rgba(232,168,56,0.3);
  border-radius: 14px;
  padding: 12px 16px;
  font-size: 13px;
  font-weight: 600;
  width: 100%;
  cursor: pointer;
  margin-top: 8px;
  min-height: 48px;
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 6px;
  transition: all .15s;
  -webkit-tap-highlight-color: transparent;
  font-family: 'Inter', -apple-system, sans-serif;
}
.wiz-btn-secondary:active { background: var(--accent-dim); }

.wiz-btn-add, .sys-add-step-btn {
  background: transparent;
  border: 1.5px dashed var(--surface-4);
  border-radius: 16px;
  padding: 12px;
  font-size: 14px;
  font-weight: 600;
  color: var(--text-secondary);
  width: 100%;
  cursor: pointer;
  margin-top: 6px;
  min-height: 52px;
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 6px;
  transition: all .15s;
  -webkit-tap-highlight-color: transparent;
}
.wiz-btn-add:active, .sys-add-step-btn:active { border-color: var(--accent); color: var(--accent); }
.wiz-btn-add svg { width: 15px; height: 15px; }

/* ===== RESULTS GRID ===== */
.results-grid {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 8px;
}
.result-card {
  background: var(--surface-1);
  border-radius: 16px;
  padding: 16px 14px;
  text-align: center;
  transition: all 0.15s;
}
.result-card.success { border-left: 3px solid var(--pass); }
.result-value {
  font-family: 'Space Mono', monospace;
  font-size: 24px;
  font-weight: 700;
  color: var(--text-primary);
  line-height: 1;
  letter-spacing: -0.02em;
}
.result-unit {
  font-size: 10px;
  font-weight: 700;
  text-transform: uppercase;
  letter-spacing: 0.08em;
  color: var(--accent);
  margin-top: 4px;
}
.result-label {
  font-size: 10px;
  color: var(--text-muted);
  margin-top: 4px;
  font-weight: 500;
}

/* Hero number style for important values */
.hero-number {
  font-family: 'Space Mono', monospace;
  font-size: 36px;
  font-weight: 700;
  line-height: 1;
  letter-spacing: -0.02em;
}

/* ===== ROOM CFM STYLES ===== */
.tightness-panel {
  background: var(--surface-1);
  border-radius: 16px;
  padding: 14px;
  margin-top: 8px;
}

.tightness-title {
  font-size: 12px;
  font-weight: 700;
  color: var(--text-primary);
  display: flex;
  align-items: center;
  gap: 6px;
  margin-bottom: 10px;
}
.tightness-title svg { width: 16px; height: 16px; color: var(--accent); }

.tightness-selector {
  display: flex;
  gap: 6px;
  overflow-x: auto;
  padding-bottom: 4px;
  -webkit-overflow-scrolling: touch;
  scrollbar-width: none;
}
.tightness-selector::-webkit-scrollbar { display: none; }

.tightness-desc {
  font-size: 11px;
  color: var(--text-secondary);
  margin-top: 6px;
  line-height: 1.5;
}

/* Room list header + items */
.room-cfm-header {
  display: flex;
  align-items: center;
  padding: 8px 12px;
  font-size: 10px;
  font-weight: 700;
  text-transform: uppercase;
  letter-spacing: 0.08em;
  color: var(--text-muted);
  border-bottom: 1px solid var(--glass-border);
  margin-bottom: 4px;
}

/* Summary bar */
.room-summary-bar {
  position: sticky;
  bottom: 76px;
  background: var(--glass);
  backdrop-filter: blur(20px);
  -webkit-backdrop-filter: blur(20px);
  border-radius: 20px;
  padding: 14px 18px;
  display: flex;
  align-items: center;
  justify-content: space-between;
  margin-top: 12px;
  border: 1px solid var(--glass-border);
  z-index: 50;
}

/* FAB for adding rooms */
.fab-add {
  position: fixed;
  bottom: 84px;
  right: 20px;
  width: 56px;
  height: 56px;
  border-radius: 50%;
  background: linear-gradient(135deg, var(--accent) 0%, #d49020 100%);
  border: none;
  color: #111;
  display: flex;
  align-items: center;
  justify-content: center;
  box-shadow: 0 4px 20px rgba(232,168,56,0.4);
  cursor: pointer;
  z-index: 60;
  transition: transform 0.15s;
  -webkit-tap-highlight-color: transparent;
}
.fab-add:active { transform: scale(0.9); }
.fab-add svg { width: 24px; height: 24px; stroke-width: 2.5; }

/* ===== MODE TOGGLE ===== */
.mode-toggle {
  background: var(--surface-0);
  border-radius: 16px;
  padding: 4px;
  display: flex;
  gap: 2px;
  box-shadow: inset 0 2px 4px rgba(0,0,0,0.15);
  margin-bottom: 14px;
}
.mode-btn {
  flex: 1;
  height: 48px;
  border-radius: 13px;
  border: none;
  font-size: 14px;
  font-weight: 700;
  color: var(--text-muted);
  background: transparent;
  transition: all 0.2s;
  cursor: pointer;
  -webkit-tap-highlight-color: transparent;
  font-family: 'Inter', -apple-system, sans-serif;
}
.mode-btn.active {
  background: linear-gradient(135deg, var(--accent) 0%, #d49020 100%);
  color: #111;
  box-shadow: 0 2px 12px rgba(232,168,56,0.3);
}
.mode-btn:active { transform: scale(0.97); }

/* ===== SLIDER PANELS ===== */
.slider-panel {
  background: var(--surface-2);
  border-radius: 20px;
  padding: 16px 18px;
  margin-bottom: 10px;
}

.slider-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 10px;
}
.slider-label { font-size: 13px; font-weight: 600; color: var(--text-primary); }
.slider-value-wrap {
  display: flex;
  align-items: center;
  gap: 4px;
}
.slider-value-input {
  background: var(--surface-0);
  border: 1.5px solid transparent;
  border-radius: 10px;
  padding: 6px 8px;
  width: 64px;
  text-align: center;
  font-size: 14px;
  font-weight: 700;
  color: var(--accent);
  font-family: 'Space Mono', monospace;
  outline: none;
  transition: border-color 0.2s;
}
.slider-value-input:focus { border-color: var(--accent); }
.slider-value-unit {
  font-size: 11px;
  font-weight: 600;
  color: var(--text-secondary);
}

/* Range inputs */
input[type="range"], .cfm-slider, .compression-slider {
  -webkit-appearance: none;
  appearance: none;
  width: 100%;
  height: 8px;
  border-radius: 4px;
  background: var(--surface-0);
  outline: none;
  cursor: pointer;
}
input[type="range"]::-webkit-slider-thumb {
  -webkit-appearance: none;
  appearance: none;
  width: 28px;
  height: 28px;
  border-radius: 50%;
  background: linear-gradient(135deg, var(--accent) 0%, #d49020 100%);
  box-shadow: 0 2px 8px rgba(232,168,56,0.3);
  cursor: pointer;
  border: 3px solid var(--surface-2);
  transition: transform 0.1s;
}
input[type="range"]::-webkit-slider-thumb:active {
  transform: scale(1.15);
}
input[type="range"]::-moz-range-thumb {
  width: 24px;
  height: 24px;
  border-radius: 50%;
  background: var(--accent);
  cursor: pointer;
  border: 3px solid var(--surface-2);
}

.slider-range-labels {
  display: flex;
  justify-content: space-between;
  font-size: 10px;
  color: var(--text-muted);
  margin-top: 6px;
  padding: 0 2px;
}

/* ===== COMPRESSION PANEL ===== */
.compression-panel {
  background: var(--surface-1);
  border-radius: 16px;
  padding: 14px;
  margin-bottom: 10px;
}
.compression-panel-title {
  font-size: 12px;
  font-weight: 700;
  color: var(--text-primary);
  display: flex;
  align-items: center;
  gap: 6px;
  margin-bottom: 10px;
}
.compression-panel-title svg { width: 16px; height: 16px; color: var(--warn); }

.compression-presets {
  display: flex;
  gap: 4px;
  flex-wrap: wrap;
  margin-bottom: 10px;
}
.compression-preset-btn {
  height: 36px;
  padding: 0 12px;
  border-radius: 10px;
  border: 1.5px solid var(--surface-4);
  background: transparent;
  color: var(--text-secondary);
  font-size: 12px;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.15s;
  font-family: 'Space Mono', monospace;
  -webkit-tap-highlight-color: transparent;
}
.compression-preset-btn.active {
  border-color: var(--warn);
  background: var(--amber-subtle);
  color: var(--warn);
}
.compression-preset-btn:active { transform: scale(0.95); }

.compression-impact {
  font-size: 11px;
  padding: 8px 12px;
  border-radius: 10px;
  margin-top: 6px;
  font-weight: 500;
}
.compression-impact.low { background: var(--green-subtle); color: var(--pass); }
.compression-impact.mid { background: var(--amber-subtle); color: var(--warn); }
.compression-impact.high { background: var(--red-subtle); color: var(--fail); }

/* ===== CONFIG ROWS (calculator controls) ===== */
.config-row {
  display: flex;
  gap: 10px;
  margin-bottom: 10px;
}
.config-group { flex: 1; }
.size-panel { 
  background: var(--surface-2);
  border-radius: 20px;
  padding: 16px;
  margin-bottom: 10px;
}

/* ===== STATUS BAR ===== */
.status-bar {
  display: flex;
  align-items: center;
  gap: 8px;
  padding: 12px 14px;
  border-radius: 14px;
  margin-top: 10px;
  font-size: 12px;
  font-weight: 500;
}
.status-bar.ok { background: var(--green-subtle); color: var(--pass); }
.status-bar.warn { background: var(--amber-subtle); color: var(--warn); }
.status-bar.bad { background: var(--red-subtle); color: var(--fail); }
.status-dot {
  width: 8px;
  height: 8px;
  border-radius: 50%;
  flex-shrink: 0;
  background: currentColor;
}

/* ===== REVERSE CAPACITY ===== */
.rev-capacity-bar { margin-bottom: 10px; }
.rev-bar-track {
  display: flex;
  height: 14px;
  border-radius: 7px;
  overflow: hidden;
  background: var(--surface-0);
}
.rev-bar-zone { transition: width 0.4s ease; }
.rev-bar-low { background: linear-gradient(90deg, var(--text-muted), var(--warn)); }
.rev-bar-ok { background: linear-gradient(90deg, var(--warn), var(--pass)); }
.rev-bar-high { background: linear-gradient(90deg, var(--pass), var(--fail)); }
.rev-bar-labels {
  display: flex;
  justify-content: space-between;
  margin-top: 6px;
  font-size: 14px;
  font-weight: 700;
  font-family: 'Space Mono', monospace;
  color: var(--text-secondary);
}
.rev-bar-captions {
  display: flex;
  justify-content: space-between;
  font-size: 10px;
  color: var(--text-muted);
  margin-top: 2px;
}

/* ===== TOGGLE SWITCH ===== */
.toggle-switch {
  position: relative;
  display: inline-block;
  width: 48px;
  height: 28px;
  cursor: pointer;
}
.toggle-switch input { opacity: 0; width: 0; height: 0; }
.toggle-slider {
  position: absolute;
  inset: 0;
  border-radius: 28px;
  background: var(--surface-4);
  transition: all 0.3s;
}
.toggle-slider::before {
  content: '';
  position: absolute;
  height: 22px;
  width: 22px;
  left: 3px;
  bottom: 3px;
  background: white;
  border-radius: 50%;
  transition: transform 0.3s;
}
.toggle-switch input:checked + .toggle-slider {
  background: var(--accent);
}
.toggle-switch input:checked + .toggle-slider::before {
  transform: translateX(20px);
}

/* ===== INFO NOTE ===== */
.info-note {
  background: var(--surface-1);
  border-radius: 14px;
  padding: 12px 14px;
  display: flex;
  align-items: flex-start;
  gap: 8px;
  font-size: 11px;
  color: var(--text-secondary);
  line-height: 1.5;
}
.info-note svg { width: 16px; height: 16px; flex-shrink: 0; margin-top: 1px; color: var(--accent); }

/* ===== EQUIVALENT LENGTH PAGE ===== */
.eq-category {
  font-size: 12px;
  font-weight: 700;
  color: var(--accent);
  text-transform: uppercase;
  letter-spacing: 0.06em;
  padding: 10px 0 6px;
  border-bottom: 1px solid var(--glass-border);
  margin-bottom: 0;
}
.eq-table-container { overflow-x: auto; -webkit-overflow-scrolling: touch; margin-bottom: 16px; }
.eq-table {
  width: 100%;
  border-collapse: collapse;
  font-size: 11px;
}
.eq-table th {
  background: var(--surface-3);
  color: var(--text-secondary);
  font-weight: 700;
  padding: 8px 6px;
  text-align: center;
  white-space: nowrap;
  position: sticky;
  top: 0;
}
.eq-table th:first-child { text-align: left; padding-left: 10px; }
.eq-table td {
  padding: 8px 6px;
  text-align: center;
  border-bottom: 1px solid rgba(255,255,255,0.04);
  color: var(--text-primary);
}
.eq-table td:first-child {
  text-align: left;
  padding-left: 10px;
  color: var(--text-secondary);
  font-weight: 500;
}
.eq-table tr:hover td { background: rgba(232,168,56,0.04); }

/* ===== SECTION TOGGLE (system page collapsibles) ===== */
.section-toggle {
  display: flex;
  align-items: center;
  justify-content: space-between;
  cursor: pointer;
  -webkit-tap-highlight-color: transparent;
  padding: 4px 0;
}
.toggle-arrow {
  font-size: 12px;
  color: var(--text-muted);
  transition: transform 0.3s;
}
.section-toggle.collapsed .toggle-arrow { transform: rotate(-90deg); }
.section-body { transition: all 0.3s; }
.section-body.collapsed { display: none; }

.plenum-grid {
  display: grid;
  grid-template-columns: 1fr 1fr 1fr;
  gap: 8px;
  margin-top: 8px;
}
.plenum-grid .input-field { height: 44px; font-size: 14px; text-align: center; }
.plenum-svg-wrap { display: flex; justify-content: center; padding: 8px 0; }
.plenum-svg-wrap svg { max-width: 200px; max-height: 120px; width: 100%; }
.collar-chips {
  display: flex;
  flex-wrap: wrap;
  gap: 4px;
  margin-top: 6px;
  min-height: 28px;
}
.add-fitting-btn {
  background: var(--accent);
  color: #111;
  border: none;
  border-radius: 10px;
  font-size: 12px;
  font-weight: 700;
  cursor: pointer;
  min-height: 44px;
  padding: 8px 14px;
  transition: transform 0.15s;
  -webkit-tap-highlight-color: transparent;
}
.add-fitting-btn:active { transform: scale(0.95); }

/* ===== FILTER PAGES ===== */
.section-card { 
  background: var(--surface-2);
  border-radius: 20px;
  padding: 18px;
}
.section-title {
  font-size: 14px;
  font-weight: 800;
  color: var(--text-primary);
  letter-spacing: 0.04em;
  display: flex;
  align-items: center;
  gap: 8px;
  margin-bottom: 4px;
}
.section-title svg { flex-shrink: 0; }

.filter-mfg-btns {
  display: flex;
  gap: 4px;
  flex-wrap: wrap;
}

.filter-inline-panel {
  background: var(--surface-1);
  border-radius: 16px;
  padding: 14px;
  margin-top: 10px;
}
.filter-inline-title {
  font-size: 12px;
  font-weight: 700;
  color: var(--text-primary);
  display: flex;
  align-items: center;
  gap: 6px;
  margin-bottom: 10px;
}
.filter-toggle-row {
  display: flex;
  align-items: center;
  gap: 8px;
  padding: 4px 0;
}
.filter-toggle-label { flex: 1; font-size: 13px; font-weight: 500; color: var(--text-primary); }
.filter-select-row {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 8px;
  margin-top: 8px;
}
.filter-inline-grid {
  display: grid;
  grid-template-columns: 1fr 1fr 1fr;
  gap: 6px;
}

.filter-result-card {
  background: var(--surface-1);
  border-radius: 16px;
  padding: 16px;
}
.filter-result-grid {
  display: grid;
  grid-template-columns: 1fr 1fr 1fr;
  gap: 8px;
}
.filter-result-item { text-align: center; }
.filter-result-value {
  font-family: 'Space Mono', monospace;
  font-size: 22px;
  font-weight: 700;
  color: var(--text-primary);
}
.filter-result-unit {
  font-size: 10px;
  color: var(--accent);
  text-transform: uppercase;
  font-weight: 700;
  letter-spacing: 0.06em;
}
.filter-result-label {
  font-size: 10px;
  color: var(--text-muted);
  margin-top: 2px;
}
.filter-note {
  margin-top: 10px;
  padding: 10px 12px;
  background: var(--amber-subtle);
  border-radius: 10px;
  font-size: 11px;
  color: var(--warn);
  line-height: 1.5;
}
.filter-apply-btn {
  width: 100%;
  height: 48px;
  margin-top: 12px;
  background: linear-gradient(135deg, var(--accent) 0%, #d49020 100%);
  color: #111;
  border: none;
  border-radius: 14px;
  font-size: 14px;
  font-weight: 700;
  cursor: pointer;
  transition: transform 0.12s;
  -webkit-tap-highlight-color: transparent;
}
.filter-apply-btn:active { transform: scale(0.96); }

.filter-warning-banner {
  display: flex;
  align-items: flex-start;
  gap: 8px;
  padding: 12px 14px;
  background: var(--amber-subtle);
  border-radius: 14px;
  font-size: 11px;
  color: var(--warn);
  margin-top: 10px;
  line-height: 1.5;
}
.filter-warning-banner svg { flex-shrink: 0; margin-top: 1px; }
.filter-impact-card {
  background: var(--surface-0);
  border-radius: 14px;
  padding: 12px;
  margin-top: 8px;
}
.filter-impact-title {
  font-size: 11px;
  font-weight: 700;
  color: var(--accent);
  margin-bottom: 6px;
}
.filter-impact-row {
  display: flex;
  justify-content: space-between;
  padding: 4px 0;
  font-size: 11px;
}
.filter-impact-label { color: var(--text-secondary); }
.filter-impact-value {
  font-family: 'Space Mono', monospace;
  font-weight: 600;
  color: var(--text-primary);
}

/* ===== PSYCHROMETRIC PAGE ===== */
.psych-mode-sel {
  display: flex;
  background: var(--surface-0);
  border-radius: 14px;
  padding: 4px;
  gap: 2px;
  box-shadow: inset 0 2px 4px rgba(0,0,0,0.15);
  margin-bottom: 14px;
}
.psych-mode-btn {
  flex: 1;
  height: 44px;
  border-radius: 11px;
  border: none;
  font-size: 12px;
  font-weight: 600;
  color: var(--text-muted);
  background: transparent;
  cursor: pointer;
  transition: all 0.2s;
  -webkit-tap-highlight-color: transparent;
  font-family: 'Inter', -apple-system, sans-serif;
}
.psych-mode-btn.active {
  background: var(--surface-3);
  color: var(--text-primary);
  box-shadow: 0 2px 8px rgba(0,0,0,0.2);
}

.psych-inputs { margin-bottom: 0; }
.psych-input-row {
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 10px 0;
  border-bottom: 1px solid rgba(255,255,255,0.04);
}
.psych-input-row label {
  font-size: 13px;
  font-weight: 500;
  color: var(--text-secondary);
}
.psych-input-wrap {
  display: flex;
  align-items: center;
  gap: 6px;
}
.psych-input-wrap .input-field {
  width: 90px;
  height: 44px;
  text-align: center;
  font-size: 15px;
}
.psych-input-unit {
  font-size: 12px;
  color: var(--text-muted);
  font-weight: 600;
  min-width: 32px;
}

.psych-results { }
.psych-result-row {
  display: flex;
  align-items: center;
  padding: 10px 0;
  border-bottom: 1px solid rgba(255,255,255,0.04);
  font-size: 13px;
}
.psych-result-row span:first-child {
  flex: 1;
  color: var(--text-secondary);
  font-weight: 500;
}
.psych-result-row span:nth-child(2) {
  font-family: 'Space Mono', monospace;
  font-weight: 700;
  color: var(--text-primary);
  font-size: 14px;
  min-width: 60px;
  text-align: right;
}
.psych-result-row span:last-child {
  font-size: 11px;
  color: var(--text-muted);
  min-width: 40px;
  text-align: right;
  margin-left: 4px;
}

/* ===== FR WORKSHEET ===== */
.fr-step {
  margin-bottom: 16px;
  padding-bottom: 14px;
  border-bottom: 1px solid rgba(255,255,255,0.04);
}
.fr-step:last-child { border-bottom: none; }
.fr-step-header {
  display: flex;
  align-items: center;
  gap: 10px;
  margin-bottom: 12px;
}
.fr-step-num {
  width: 28px;
  height: 28px;
  border-radius: 50%;
  background: var(--accent);
  color: #111;
  font-size: 13px;
  font-weight: 800;
  display: flex;
  align-items: center;
  justify-content: center;
  flex-shrink: 0;
}
.fr-step-title {
  font-size: 14px;
  font-weight: 700;
  color: var(--text-primary);
}
.fr-row {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 10px;
}
.fr-field { }
.fr-label {
  font-size: 10px;
  font-weight: 700;
  text-transform: uppercase;
  letter-spacing: 0.06em;
  color: var(--text-secondary);
  margin-bottom: 5px;
  display: block;
}
.fr-input-wrap {
  display: flex;
  align-items: center;
  gap: 6px;
}
.fr-input {
  background: var(--surface-0);
  border: 1.5px solid transparent;
  border-radius: 12px;
  padding: 0 12px;
  height: 44px;
  font-size: 14px;
  color: var(--text-primary);
  font-family: 'Space Mono', monospace;
  outline: none;
  width: 100%;
  box-shadow: inset 0 2px 4px rgba(0,0,0,0.15);
  transition: border-color 0.2s;
}
.fr-input:focus { border-color: var(--accent); }
.fr-select { -webkit-appearance: none; appearance: none; cursor: pointer; }
.fr-unit {
  font-size: 11px;
  color: var(--text-muted);
  font-weight: 600;
  white-space: nowrap;
  flex-shrink: 0;
}
.fr-input-sm { }
.fr-input-sm .fr-input { height: 38px; font-size: 13px; }
.fr-losses-grid { display: flex; flex-direction: column; gap: 2px; }
.fr-loss-row {
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 8px 0;
  border-bottom: 1px solid rgba(255,255,255,0.03);
}
.fr-loss-label {
  font-size: 12px;
  color: var(--text-secondary);
  font-weight: 500;
}
.fr-total-row {
  border-top: 2px solid var(--accent);
  border-bottom: none;
  padding-top: 10px;
  margin-top: 4px;
}
.fr-cpl-input { width: 70px; }
.fr-formula {
  background: var(--surface-1);
  border-radius: 12px;
  padding: 10px 14px;
  font-size: 13px;
  color: var(--accent);
  font-weight: 600;
  margin-bottom: 8px;
  font-family: 'Space Mono', monospace;
}
.fr-calc-display {
  display: flex;
  align-items: baseline;
  gap: 8px;
  flex-wrap: wrap;
  font-family: 'Space Mono', monospace;
  font-size: 16px;
  color: var(--text-secondary);
  font-weight: 600;
  padding: 10px 0;
}
.fr-op { color: var(--text-muted); }
.fr-result { font-weight: 700; color: var(--accent); font-size: 16px; }
.fr-result-big { font-weight: 700; color: var(--accent); font-size: 22px; }
.fr-unit-big { font-size: 12px; color: var(--text-secondary); }

.fr-result-card {
  border-radius: 16px;
  padding: 16px;
  margin-top: 12px;
}
.fr-result-card.fr-result-ok { background: var(--green-subtle); border-left: 4px solid var(--pass); }
.fr-result-card.fr-result-warn { background: var(--amber-subtle); border-left: 4px solid var(--warn); }
.fr-result-card.fr-result-bad { background: var(--red-subtle); border-left: 4px solid var(--fail); }
.fr-result-header {
  display: flex;
  align-items: center;
  gap: 8px;
  margin-bottom: 6px;
  font-size: 14px;
  font-weight: 800;
  color: var(--text-primary);
  font-family: 'Space Mono', monospace;
}
.fr-result-msg {
  font-size: 12px;
  color: var(--text-secondary);
  line-height: 1.5;
}
.fr-chart-wrap {
  background: var(--surface-0);
  border-radius: 14px;
  padding: 8px;
  overflow: hidden;
}
.fr-chart-wrap canvas { width: 100% !important; border-radius: 10px; }
.fr-factor-display {
  background: var(--surface-0);
  border-radius: 12px;
  padding: 10px 14px;
  font-family: 'Space Mono', monospace;
  font-size: 16px;
  font-weight: 700;
  color: var(--accent);
}

/* ===== WIZARD STYLES ===== */
.wiz-step-bar {
  display: flex; align-items: center; justify-content: space-between;
  padding: 14px 20px 8px; gap: 0;
}
.wiz-pill {
  display: flex; align-items: center; gap: 5px;
  padding: 6px 10px; border-radius: 20px;
  border: 1px solid var(--border-default);
  background: var(--surface-3); cursor: pointer;
  transition: all .2s; min-height: 36px; min-width: 44px; justify-content: center;
}
.wiz-pill.active {
  background: var(--accent); border-color: var(--accent);
  box-shadow: 0 2px 12px rgba(232,168,56,.3);
}
.wiz-pill.done { background: var(--green-subtle); border-color: var(--pass); }
.wiz-pill-num { font-size: 11px; font-weight: 700; color: var(--text-muted); line-height: 1; min-width: 14px; text-align: center; }
.wiz-pill.active .wiz-pill-num { color: #111; }
.wiz-pill.done .wiz-pill-num { color: var(--pass); }
.wiz-pill-lbl { font-size: 11px; font-weight: 600; color: var(--text-muted); white-space: nowrap; }
.wiz-pill.active .wiz-pill-lbl { color: #111; }
.wiz-pill.done .wiz-pill-lbl { color: var(--pass); }
.wiz-pill-sep { color: var(--border-default); display: flex; align-items: center; flex-shrink: 0; }

.wiz-progress-track { height: 3px; background: var(--surface-1); margin: 0 20px 12px; border-radius: 2px; overflow: hidden; }
.wiz-progress-fill { height: 100%; border-radius: 2px; background: linear-gradient(90deg, var(--accent), var(--accent-light)); width: 25%; transition: width .5s cubic-bezier(.4,0,.2,1); }

/* SVG Fitting Animations */
@keyframes svgFadeSlide { from { opacity: 0; transform: translateY(8px); } to { opacity: 1; transform: translateY(0); } }
.wiz-fitting-svg { animation: svgFadeSlide 0.3s ease-out; display: flex; justify-content: center; padding: 8px 0; }
.wiz-fitting-svg svg { max-width: 120px; max-height: 80px; }
@keyframes flowDash { to { stroke-dashoffset: -20; } }
.plenum-flow { stroke-dasharray: 8 6; animation: flowDash 0.8s linear infinite; }

/* Wizard Steps */
.wiz-step { display: none; padding: 0 20px 16px; }
.wiz-step.active { display: block; animation: wizFadeIn .3s ease forwards; }
@keyframes wizFadeIn { from { opacity:0; transform:translateY(6px); } to { opacity:1; transform:translateY(0); } }

/* Prompt Boxes */
.wiz-prompt {
  background: var(--surface-3);
  border-left: 3px solid var(--accent);
  border-radius: 0 16px 16px 0;
  padding: 14px 16px;
  margin-bottom: 12px;
}
.wiz-prompt-q {
  font-size: 14px; font-weight: 700; color: var(--text-primary);
  display: flex; align-items: center; gap: 8px; margin-bottom: 4px;
}
.wiz-prompt-q svg { color: var(--accent); flex-shrink: 0; }
.wiz-prompt-help { font-size: 11px; color: var(--text-secondary); line-height: 1.5; }

/* Info Banner */
.wiz-info-banner {
  background: var(--accent-dim); border: 1px solid rgba(232,168,56,.2);
  border-radius: 16px; padding: 14px 16px; margin-bottom: 14px;
  display: flex; align-items: flex-start; gap: 8px;
}
.wiz-info-banner svg { flex-shrink: 0; color: var(--accent); margin-top: 1px; }
.wiz-info-banner p { font-size: 12px; color: var(--text-primary); line-height: 1.5; }
.wiz-info-banner strong { color: var(--accent); }

/* Trunk Cards */
.wiz-trunk-card {
  background: var(--surface-2); border: 1px solid var(--glass-border);
  border-left: 3px solid var(--accent); border-radius: 18px;
  padding: 18px; margin-bottom: 12px; position: relative;
}
.wiz-trunk-label-row { display: flex; align-items: center; justify-content: space-between; margin-bottom: 10px; }
.wiz-trunk-label {
  font-size: 12px; font-weight: 700; color: var(--accent);
  text-transform: uppercase; letter-spacing: 0.06em;
  display: flex; align-items: center; gap: 6px;
}
.wiz-trunk-remove {
  width: 32px; height: 32px; border-radius: 10px;
  background: var(--surface-3); border: none;
  display: flex; align-items: center; justify-content: center;
  cursor: pointer; transition: all .15s; flex-shrink: 0;
}
.wiz-trunk-remove:hover { background: var(--red-subtle); }
.wiz-trunk-remove svg { width: 13px; height: 13px; color: var(--text-secondary); }
.wiz-trunk-remove:hover svg { color: var(--fail); }

.wiz-shape-toggle {
  display: flex;
  background: var(--surface-0);
  border-radius: 12px;
  padding: 3px;
  overflow: hidden;
  margin-bottom: 10px;
}
.wiz-shape-btn {
  flex: 1; padding: 10px 6px; text-align: center; font-size: 12px; font-weight: 600;
  color: var(--text-secondary); background: transparent; cursor: pointer;
  min-height: 44px; display: flex; align-items: center; justify-content: center;
  gap: 4px; transition: all .15s; -webkit-tap-highlight-color: transparent;
  border: none; border-radius: 10px;
  font-family: 'Inter', -apple-system, sans-serif;
}
.wiz-shape-btn.active {
  background: linear-gradient(135deg, var(--accent), #d49020);
  color: #111;
  font-weight: 700;
}
.wiz-shape-btn svg { width: 13px; height: 13px; }

/* Input Rows */
.wiz-input-row { display: flex; gap: 8px; align-items: flex-end; margin-bottom: 10px; }
.wiz-input-group { flex: 1; }
.wiz-input-label {
  font-size: 10px; color: var(--text-secondary); text-transform: uppercase;
  letter-spacing: 0.06em; margin-bottom: 4px; font-weight: 600;
}

/* Branch Area */
.wiz-trunk-group { margin-bottom: 18px; }
.wiz-trunk-group-hdr {
  display: flex; align-items: center; gap: 7px;
  padding: 7px 0; margin-bottom: 6px; border-bottom: 1px solid var(--glass-border);
}
.wiz-trunk-group-hdr svg { width: 15px; height: 15px; color: var(--accent); flex-shrink: 0; }
.wiz-trunk-group-lbl { font-size: 12px; font-weight: 700; color: var(--accent); text-transform: uppercase; letter-spacing: 0.06em; }
.wiz-add-branch-btn {
  display: flex; align-items: center; justify-content: center; gap: 6px;
  width: 100%; min-height: 48px; padding: 8px;
  background: transparent; border: 1.5px dashed var(--surface-4);
  border-radius: 14px; color: var(--text-muted);
  font-size: 13px; font-weight: 600; cursor: pointer;
  transition: all .15s; margin-top: 6px; -webkit-tap-highlight-color: transparent;
}
.wiz-add-branch-btn:hover { border-color: var(--accent); color: var(--accent); }
.wiz-add-branch-btn svg { width: 13px; height: 13px; }

/* Branch Items */
.wiz-branch-item {
  background: var(--surface-2); border: 1px solid var(--glass-border);
  border-radius: 14px; padding: 12px 14px; margin-bottom: 8px;
  display: flex; align-items: center; gap: 10px;
  cursor: pointer; transition: all .15s; min-height: 56px;
  -webkit-tap-highlight-color: transparent;
}
.wiz-branch-item:active { transform: scale(0.98); }
.wiz-branch-item.editing { border-color: var(--accent); background: var(--surface-3); }
.wiz-branch-num {
  width: 28px; height: 28px; background: var(--accent); border-radius: 50%;
  display: flex; align-items: center; justify-content: center;
  font-size: 12px; font-weight: 700; color: #111; flex-shrink: 0;
}
.wiz-branch-info { flex: 1; min-width: 0; }
.wiz-branch-name { font-size: 13px; font-weight: 600; color: var(--text-primary); white-space: nowrap; overflow: hidden; text-overflow: ellipsis; }
.wiz-branch-detail { font-size: 11px; color: var(--text-secondary); margin-top: 2px; }
.wiz-branch-badge { font-size: 10px; padding: 3px 8px; border-radius: 8px; font-weight: 600; flex-shrink: 0; }
.wiz-branch-badge.pending { background: var(--surface-3); color: var(--text-muted); }
.wiz-branch-badge.done { background: var(--green-subtle); color: var(--pass); }
.wiz-branch-badge.editing { background: var(--accent-dim); color: var(--accent); }

/* Branch Edit Form */
.wiz-branch-form {
  background: var(--surface-3); border: 1px solid var(--accent);
  border-radius: 18px; padding: 16px; margin: 6px 0 10px;
}
.wiz-fittings-lbl { font-size: 10px; color: var(--text-secondary); text-transform: uppercase; letter-spacing: 0.06em; margin-bottom: 6px; font-weight: 600; }
.wiz-fit-btns { display: flex; gap: 5px; flex-wrap: wrap; margin-bottom: 8px; }
.wiz-fit-btn {
  background: var(--surface-2); border: 1px solid var(--glass-border);
  border-radius: 10px; padding: 8px 10px; font-size: 11px;
  color: var(--text-primary); cursor: pointer;
  display: flex; align-items: center; gap: 4px;
  min-height: 38px; transition: all .12s; -webkit-tap-highlight-color: transparent;
  font-family: 'Inter', -apple-system, sans-serif;
}
.wiz-fit-btn:active { background: var(--accent); border-color: var(--accent); color: #111; }
.wiz-fit-btn svg { width: 13px; height: 13px; flex-shrink: 0; }
.wiz-fit-list { margin-top: 6px; }
.wiz-fit-item {
  display: flex; align-items: center; gap: 7px;
  padding: 6px 10px; background: var(--surface-1);
  border-radius: 10px; margin-bottom: 4px; font-size: 12px; color: var(--text-primary);
}
.wiz-fit-item-name { flex: 1; }
.wiz-fit-item-eq { color: var(--warn); font-weight: 600; font-family: 'Space Mono', monospace; font-size: 11px; }
.wiz-fit-item-rm {
  width: 22px; height: 22px; border-radius: 50%;
  background: var(--surface-2); border: none;
  display: flex; align-items: center; justify-content: center;
  cursor: pointer; flex-shrink: 0; -webkit-tap-highlight-color: transparent;
}
.wiz-fit-item-rm:hover { background: var(--red-subtle); }
.wiz-fit-item-rm svg { width: 10px; height: 10px; color: var(--text-secondary); }
.wiz-compression-box {
  background: var(--surface-1); border: 1px solid var(--glass-border);
  border-radius: 12px; padding: 10px 12px; margin-bottom: 10px;
}
.wiz-compression-val { font-size: 12px; font-weight: 600; color: var(--warn); font-family: 'Space Mono', monospace; margin-top: 4px; }
.wiz-save-row { display: flex; gap: 8px; margin-top: 10px; }
.wiz-btn-save {
  flex: 1; background: linear-gradient(135deg, var(--accent) 0%, #d49020 100%);
  color: #111; border: none; border-radius: 14px; padding: 10px;
  font-size: 14px; font-weight: 700; cursor: pointer; min-height: 48px;
  display: flex; align-items: center; justify-content: center; gap: 5px;
  transition: transform .15s; -webkit-tap-highlight-color: transparent;
  box-shadow: 0 4px 12px rgba(232,168,56,0.25);
  font-family: 'Inter', -apple-system, sans-serif;
}
.wiz-btn-save:active { transform: scale(0.97); }
.wiz-btn-rm {
  width: 48px; flex-shrink: 0; background: transparent;
  border: 1px solid var(--glass-border); border-radius: 14px;
  display: flex; align-items: center; justify-content: center;
  cursor: pointer; min-height: 48px; transition: all .15s; -webkit-tap-highlight-color: transparent;
}
.wiz-btn-rm:hover { background: var(--red-subtle); border-color: var(--fail); }
.wiz-btn-rm svg { width: 15px; height: 15px; color: var(--text-secondary); }

/* Results */
.wiz-card-title {
  font-size: 12px; font-weight: 700; color: var(--accent);
  text-transform: uppercase; letter-spacing: 0.08em; margin-bottom: 12px;
  display: flex; align-items: center; gap: 7px;
}
.wiz-card-title svg { width: 15px; height: 15px; flex-shrink: 0; }
.wiz-results-grid { display: grid; grid-template-columns: 1fr 1fr; gap: 8px; margin-bottom: 6px; }
.wiz-result-cell {
  background: var(--surface-1); border-radius: 14px; padding: 14px; text-align: center;
}
.wiz-result-val { font-size: 22px; font-weight: 700; font-family: 'Space Mono', monospace; }
.wiz-result-val.ok { color: var(--pass); }
.wiz-result-val.warn { color: var(--warn); }
.wiz-result-val.bad { color: var(--fail); }
.wiz-result-lbl { font-size: 9px; color: var(--text-secondary); text-transform: uppercase; letter-spacing: 0.04em; margin-top: 2px; }
.wiz-gauge-wrap { margin: 4px 0 8px; }
.wiz-gauge-label { font-size: 10px; color: var(--text-secondary); display: flex; justify-content: space-between; margin-bottom: 6px; font-weight: 600; }
.wiz-gauge-track { height: 14px; background: var(--surface-1); border-radius: 7px; overflow: hidden; }
.wiz-gauge-fill { height: 100%; border-radius: 7px; transition: width .6s cubic-bezier(.4,0,.2,1); }
.wiz-gauge-fill.green { background: linear-gradient(90deg, #059669, var(--pass)); }
.wiz-gauge-fill.yellow { background: linear-gradient(90deg, var(--pass), var(--warn)); }
.wiz-gauge-fill.red { background: linear-gradient(90deg, var(--warn), var(--fail)); }
.wiz-gauge-markers { display: flex; justify-content: space-between; margin-top: 3px; font-size: 9px; color: var(--text-muted); font-family: 'Space Mono', monospace; }

.wiz-path-step { display: flex; align-items: flex-start; gap: 8px; padding: 5px 0; position: relative; }
.wiz-path-step-line { position: absolute; left: 11px; top: 28px; width: 2px; bottom: -5px; background: var(--glass-border); z-index: 0; }
.wiz-path-step:last-child .wiz-path-step-line { display: none; }
.wiz-path-dot {
  width: 24px; height: 24px; border-radius: 50%;
  display: flex; align-items: center; justify-content: center;
  font-size: 9px; font-weight: 700; color: #fff; flex-shrink: 0; z-index: 1;
}
.wiz-path-dot.start { background: var(--accent); }
.wiz-path-dot.duct { background: var(--text-muted); }
.wiz-path-dot.fitting { background: var(--warn); }
.wiz-path-dot.end { background: var(--pass); }
.wiz-path-info { flex: 1; min-width: 0; }
.wiz-path-name { font-size: 12px; font-weight: 600; color: var(--text-primary); }
.wiz-path-eq { font-size: 11px; color: var(--warn); font-weight: 600; font-family: 'Space Mono', monospace; flex-shrink: 0; margin-top: 3px; }
.wiz-run-item { background: var(--surface-2); border: 1px solid var(--glass-border); border-radius: 14px; padding: 12px 14px; margin-bottom: 8px; }
.wiz-run-header { display: flex; align-items: center; gap: 8px; margin-bottom: 4px; }
.wiz-run-name { font-size: 13px; font-weight: 600; color: var(--text-primary); flex: 1; }
.wiz-run-tel { font-size: 12px; font-weight: 700; font-family: 'Space Mono', monospace; }
.wiz-run-fr { font-size: 11px; font-weight: 600; font-family: 'Space Mono', monospace; }
.wiz-tel-bar-wrap { height: 6px; background: var(--surface-1); border-radius: 3px; overflow: hidden; }
.wiz-tel-bar { height: 100%; border-radius: 3px; transition: width .4s ease; }
.wiz-trunk-result-hdr {
  display: flex; align-items: center; gap: 7px;
  padding: 6px 0; margin-bottom: 6px; border-bottom: 1px solid var(--glass-border);
}
.wiz-trunk-result-hdr svg { width: 14px; height: 14px; color: var(--accent); }
.wiz-trunk-result-lbl { font-size: 11px; font-weight: 700; color: var(--accent); text-transform: uppercase; letter-spacing: 0.06em; flex: 1; }
.wiz-trunk-result-maxtel { font-size: 10px; color: var(--warn); font-family: 'Space Mono', monospace; }
.wiz-crit-label { font-size: 12px; font-weight: 600; color: var(--warn); display: flex; align-items: center; gap: 5px; margin-bottom: 10px; }

/* ===== FOOTER ===== */
footer {
  text-align: center;
  padding: 16px;
  margin-bottom: 10px;
}
footer a {
  color: var(--text-muted);
  text-decoration: none;
  font-size: 11px;
}
footer a:hover { color: var(--accent); }

/* ===== MICRO-INTERACTIONS ===== */
@keyframes highlight-flash {
  0% { background: rgba(232,168,56,0.2); }
  100% { background: transparent; }
}
.num-flash { animation: highlight-flash 0.6s ease; }

</style>
</head>
<body>

<!-- ===== APP HEADER ===== -->
<header class="app-header" id="appHeaderHome">
  <div class="app-header-brand">
    <svg class="app-logo" viewBox="0 0 36 36" fill="none" xmlns="http://www.w3.org/2000/svg">
      <rect width="36" height="36" rx="10" fill="#e8a838" fill-opacity="0.12"/>
      <path d="M10 18h16M18 10v16" stroke="#e8a838" stroke-width="2.5" stroke-linecap="round"/>
      <circle cx="18" cy="18" r="7" stroke="#e8a838" stroke-width="1.5" fill="none"/>
      <circle cx="18" cy="18" r="3" fill="#e8a838" fill-opacity="0.6"/>
    </svg>
    <div class="app-header-text">
      <span class="app-header-name">DuctCalc Pro</span>
      <span class="app-header-tagline">HVAC Duct Design</span>
    </div>
  </div>
</header>

<!-- Hidden nav-tabs for JS compatibility (showPage references .nav-tab[data-page]) -->
<div style="display:none">
  <button class="nav-tab active" data-page="roomcfm"></button>
  <button class="nav-tab" data-page="system"></button>
  <button class="nav-tab" data-page="calculator"></button>
  <button class="nav-tab" data-page="eqlen"></button>
  <button class="nav-tab" data-page="frworksheet"></button>
  <button class="nav-tab" data-page="filters"></button>
  <button class="nav-tab" data-page="psychro"></button>
</div>

<!-- ===== HOME SCREEN ===== -->
<div id="page-home" class="active">
  <div class="home-hero">
    <svg class="home-logo-mark" viewBox="0 0 80 80" fill="none" xmlns="http://www.w3.org/2000/svg">
      <rect width="80" height="80" rx="24" fill="#e8a838" fill-opacity="0.08"/>
      <circle cx="40" cy="40" r="18" stroke="#e8a838" stroke-width="2" fill="none" opacity="0.4"/>
      <circle cx="40" cy="40" r="10" stroke="#e8a838" stroke-width="2.5" fill="none"/>
      <circle cx="40" cy="40" r="4" fill="#e8a838"/>
      <path d="M22 40h8M50 40h8M40 22v8M40 50v8" stroke="#e8a838" stroke-width="2" stroke-linecap="round"/>
      <path d="M28 28l5.5 5.5M46.5 46.5L52 52M28 52l5.5-5.5M46.5 33.5L52 28" stroke="#e8a838" stroke-width="1.5" stroke-linecap="round" opacity="0.5"/>
    </svg>
    <div class="home-title">DuctCalc Pro</div>
    <div class="home-subtitle">Professional HVAC Duct Design</div>
  </div>

  <div class="home-cards">
    <div class="home-card" data-home-nav="roomcfm">
      <div class="home-card-icon design">
        <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M3 9l9-7 9 7v11a2 2 0 01-2 2H5a2 2 0 01-2-2z"/><polyline points="9 22 9 12 15 12 15 22"/></svg>
      </div>
      <div class="home-card-title">Design a System</div>
      <div class="home-card-desc">Room-by-room CFM, wizard, full duct layout</div>
    </div>
    <div class="home-card" data-home-nav="calculator">
      <div class="home-card-icon calc">
        <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><rect x="4" y="2" width="16" height="20" rx="2"/><line x1="8" y1="6" x2="16" y2="6"/><line x1="8" y1="10" x2="10" y2="10"/><line x1="14" y1="10" x2="16" y2="10"/><line x1="8" y1="14" x2="10" y2="14"/><line x1="14" y1="14" x2="16" y2="14"/><line x1="8" y1="18" x2="16" y2="18"/></svg>
      </div>
      <div class="home-card-title">Quick Calculator</div>
      <div class="home-card-desc">Duct size, velocity, friction rate</div>
    </div>
  </div>

  <div class="home-tools-label">Tools</div>
  <div class="home-tools-row">
    <div class="home-tool" data-home-nav="eqlen">
      <div class="home-tool-icon eqlen"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M21 16V8a2 2 0 00-1-1.73l-7-4a2 2 0 00-2 0l-7 4A2 2 0 003 8v8a2 2 0 001 1.73l7 4a2 2 0 002 0l7-4A2 2 0 0021 16z"/></svg></div>
      <div class="home-tool-name">EQ Length</div>
    </div>
    <div class="home-tool" data-home-nav="frworksheet">
      <div class="home-tool-icon frwork"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M14 2H6a2 2 0 00-2 2v16a2 2 0 002 2h12a2 2 0 002-2V8z"/><polyline points="14 2 14 8 20 8"/></svg></div>
      <div class="home-tool-name">FR Sheet</div>
    </div>
    <div class="home-tool" data-home-nav="filters">
      <div class="home-tool-icon filter"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><polygon points="22 3 2 3 10 12.46 10 19 14 21 14 12.46 22 3"/></svg></div>
      <div class="home-tool-name">Filters</div>
    </div>
    <div class="home-tool" data-home-nav="psychro">
      <div class="home-tool-icon psychro"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M14 14.76V3.5a2.5 2.5 0 00-5 0v11.26a4.5 4.5 0 105 0z"/></svg></div>
      <div class="home-tool-name">Psychro</div>
    </div>
  </div>
</div>
'''

# Now read the HTML body from the original file (lines 1712-3732)
with open('/home/user/workspace/ductulator-pro/index.html', 'r') as f:
    lines = f.readlines()

# Room CFM page: lines 1712-1785 (0-indexed: 1711-1784)
roomcfm_html = ''.join(lines[1711:1785])

# Calculator page: lines 1787-2202 (0-indexed: 1786-2201)
calculator_html = ''.join(lines[1786:2202])

# EQ Length page: lines 2204-2303 (0-indexed: 2203-2302)
eqlen_html = ''.join(lines[2203:2302])

# System page: lines 2305-3233 (0-indexed: 2304-3232)
system_html = ''.join(lines[2304:3232])

# FR Worksheet page: lines 3235-3524 (0-indexed: 3234-3523)
frworksheet_html = ''.join(lines[3234:3523])

# Filters page: lines 3527-3616 (0-indexed: 3526-3615)
filters_html = ''.join(lines[3526:3615])

# Psychro page: lines 3618-3723 (0-indexed: 3617-3722)
psychro_html = ''.join(lines[3617:3722])

# Footer: lines 3727-3731 (0-indexed: 3726-3730)
footer_html = ''.join(lines[3726:3731])

# Assemble
html += '\n'
html += roomcfm_html
html += '\n'
html += calculator_html
html += '\n'
html += eqlen_html
html += '\n'
html += system_html
html += '\n'
html += frworksheet_html
html += '\n'
html += filters_html
html += '\n'
html += psychro_html
html += '\n'
html += footer_html

# Main script
html += '\n<script>\n'
html += main_script
html += '</script>\n\n'

# Bottom nav
html += r'''
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

# Second script
html += '<script>\n'
html += second_script
html += '</script>\n\n'

# Home page navigation script
html += r'''<script>
// ===== DuctCalc Pro V3 — Home Page & Navigation Enhancement =====
(function() {
  var pageHome = document.getElementById('page-home');
  var appHeader = document.getElementById('appHeaderHome');
  var bottomNav = document.getElementById('bottomNav');

  function showHomePage() {
    // Hide all .page divs
    document.querySelectorAll('.page').forEach(function(p) {
      p.classList.remove('active');
    });
    // Show home
    pageHome.classList.add('active');
    // Deactivate bottom nav
    bottomNav.querySelectorAll('.bottom-nav-item').forEach(function(b) {
      b.classList.remove('active');
    });
  }

  function navigateToPage(pageName) {
    // Hide home
    pageHome.classList.remove('active');
    // Use existing showPage
    if (typeof showPage === 'function') {
      showPage(pageName);
    }
    // Sync bottom nav
    bottomNav.querySelectorAll('.bottom-nav-item').forEach(function(b) {
      b.classList.remove('active');
      if (b.getAttribute('data-page') === pageName) b.classList.add('active');
    });
    // Close more panel if open
    var mp = document.getElementById('morePanel');
    if (mp) mp.classList.remove('open');
  }

  // Home card clicks
  document.querySelectorAll('[data-home-nav]').forEach(function(el) {
    el.addEventListener('click', function() {
      navigateToPage(this.getAttribute('data-home-nav'));
    });
  });

  // App header logo -> home
  if (appHeader) {
    appHeader.addEventListener('click', showHomePage);
  }

  // Override bottom nav to also hide home
  bottomNav.querySelectorAll('.bottom-nav-item[data-page]').forEach(function(btn) {
    btn.addEventListener('click', function() {
      var pg = this.getAttribute('data-page');
      if (pg) navigateToPage(pg);
    }, true);
  });

  // More panel tools also navigate
  document.querySelectorAll('.more-tool[data-page]').forEach(function(btn) {
    btn.addEventListener('click', function() {
      var pg = this.getAttribute('data-page');
      if (pg) navigateToPage(pg);
    }, true);
  });
})();
</script>

</body>
</html>'''

# Write the file
with open('/home/user/workspace/ductulator-pro/index.html', 'w') as f:
    f.write(html)

print("V3 build complete!")
print(f"File size: {len(html)} bytes")
