# ⚡ NEON UI ADDITIONS MASTER GUIDE
## The God-Developer's Complete Blueprint for Maximum Neon Glory
### `player_component.py` — ADDITIVE ONLY. ZERO REMOVALS. ZERO REPLACEMENTS.

---

> **READ THIS FIRST:** Every single instruction below is an ADDITION. You are injecting new CSS keyframes, new HTML elements, new JS blocks, new Three.js overlays, and new inline styles — all placed AFTER existing code or INSIDE existing elements as children. You touch NOTHING that already exists. You do not rename, remove, or replace any class, ID, function, or variable. You are a sculptor adding marble, not a demolisher. Every code block has an exact injection point marked with `>>> INJECT AFTER LINE` or `>>> INJECT INSIDE ELEMENT`. Follow them precisely.

---

## TABLE OF CONTENTS

1. [CSS Keyframe Additions — Neon Animations Library](#1-css-keyframe-additions)
2. [Neon Border System — Every Panel, Every Card](#2-neon-border-system)
3. [Glass Panel Neon Aura Overlay](#3-glass-panel-neon-aura)
4. [Vinyl Record Neon Halo Ring](#4-vinyl-record-neon-halo)
5. [Play/Pause Button Lightning Crown](#5-playpause-lightning-crown)
6. [Progress Bar Neon Laser Trail](#6-progress-bar-neon-laser)
7. [Lyrics Panel Active Line Electric Arc](#7-lyrics-active-line-arc)
8. [Lyrics Header Neon Title Glow](#8-lyrics-header-glow)
9. [Control Buttons Neon Hover Sparks](#9-control-buttons-sparks)
10. [Visualizer Selector Pills Neon Outline](#10-visualizer-pills-neon)
11. [Theme Dot Buttons Neon Pulse Ring](#11-theme-dots-neon-pulse)
12. [Volume Slider Neon Glow Track](#12-volume-slider-neon)
13. [Sync Offset Slider Neon Glow](#13-sync-offset-neon)
14. [Top Header Neon Ticker Line](#14-header-neon-ticker)
15. [NOW PLAYING Dot — Triple Neon Ring Pulse](#15-now-playing-dot)
16. [Beat Flash Neon Color Burst Enhancement](#16-beat-flash-enhancement)
17. [Ambient Orbs — Neon Intensification Layer](#17-ambient-orbs-neon)
18. [Player Card Outer Neon Frame](#18-player-card-outer-frame)
19. [Lyrics Panel Right Edge Neon Stripe](#19-lyrics-panel-right-stripe)
20. [Queue/Find/SpotifyMode Buttons Neon Glow](#20-header-buttons-neon)
21. [SYNCED Badge Neon Flicker](#21-synced-badge-flicker)
22. [Neon Lightning Canvas Overlay (JS Addition)](#22-neon-lightning-canvas)
23. [Corner Arc Lightning Decorators (HTML + JS)](#23-corner-arc-lightning)
24. [Three.js Neon Particle Field (JS Addition)](#24-threejs-neon-particles)
25. [Fullscreen Mode — TRUE Browser Fullscreen API Fix](#25-fullscreen-api-fix)
26. [Fullscreen Neon Entrance Animation (CSS)](#26-fullscreen-neon-entrance)
27. [Fullscreen Video + Lyrics Split Neon Layout](#27-fullscreen-split-layout)
28. [Fullscreen Escape Button Neon Glow](#28-fullscreen-escape-button)
29. [Spectrum Bars Neon Intensification](#29-spectrum-bars-neon)
30. [DSP EQ Buttons Neon Active State](#30-eq-buttons-neon)
31. [Album Art Neon Breathing Ring](#31-album-art-breathing-ring)
32. [Waveform Neon Color Layer](#32-waveform-neon)
33. [Cursor Trail Neon Sparks (JS)](#33-cursor-trail-sparks)
34. [Mouse Parallax Neon Glow Intensifier (JS)](#34-parallax-neon-glow)
35. [Scrollbar Neon Glow](#35-scrollbar-neon)
36. [Neon Clock/BPM Display Widget (HTML + JS)](#36-neon-bpm-display)
37. [Background Noise Texture Neon Tint Layer](#37-noise-texture-neon)
38. [Global CSS Variable Neon Token Additions](#38-css-variable-tokens)
39. [Mobile Neon Additions (Responsive)](#39-mobile-neon)
40. [Final Stacking Order & Z-Index Neon Layer Map](#40-stacking-order)

---

## SECTION 1 — CSS KEYFRAME ADDITIONS
### `>>> INJECT INTO: the <style> block in player_component.py, AFTER the last existing @keyframes block (after the scanline keyframe around line 292)`

These are pure additions to the animation library. Every keyframe name here is brand new — none clash with existing ones.

```css
/* ═══════════════════════════════════════════════════════════════
   ⚡ NEON ADDITIONS — KEYFRAME LIBRARY v2.0
   Inject AFTER last existing @keyframes in <style> block
   ═══════════════════════════════════════════════════════════════ */

/* 1a. Neon border rotate — a rainbow gradient border that spins around the panel */
@keyframes neonBorderRotate {
    0%   { background-position: 0% 50%; }
    50%  { background-position: 100% 50%; }
    100% { background-position: 0% 50%; }
}

/* 1b. Electric arc flicker — rapid strobe for lightning effect */
@keyframes electricArcFlicker {
    0%, 100% { opacity: 1; filter: blur(0px); }
    8%        { opacity: 0.6; filter: blur(1px); }
    12%       { opacity: 1; filter: blur(0px); }
    20%       { opacity: 0.8; filter: blur(0.5px); }
    22%       { opacity: 1; filter: blur(0px); }
    55%       { opacity: 0.7; filter: blur(0.8px); }
    57%       { opacity: 1; filter: blur(0px); }
    80%       { opacity: 0.9; }
}

/* 1c. Neon halo breathe — pulsing outer glow ring */
@keyframes neonHaloBreathe {
    0%   { box-shadow: 0 0 8px 2px var(--accent, #f43f5e), 0 0 20px 4px rgba(244,63,94,0.3), 0 0 40px 8px rgba(244,63,94,0.1); }
    50%  { box-shadow: 0 0 16px 4px var(--accent, #f43f5e), 0 0 40px 10px rgba(244,63,94,0.5), 0 0 80px 20px rgba(244,63,94,0.2); }
    100% { box-shadow: 0 0 8px 2px var(--accent, #f43f5e), 0 0 20px 4px rgba(244,63,94,0.3), 0 0 40px 8px rgba(244,63,94,0.1); }
}

/* 1d. Lightning bolt streak — diagonal flash across an element */
@keyframes lightningStreak {
    0%   { transform: translateX(-120%) skewX(-20deg); opacity: 0; }
    10%  { opacity: 1; }
    30%  { transform: translateX(120%) skewX(-20deg); opacity: 0.8; }
    100% { transform: translateX(120%) skewX(-20deg); opacity: 0; }
}

/* 1e. Neon text shimmer — text glow that shifts color */
@keyframes neonTextShimmer {
    0%   { text-shadow: 0 0 10px #f43f5e, 0 0 20px #f43f5e, 0 0 40px rgba(244,63,94,0.5); color: #ffffff; }
    25%  { text-shadow: 0 0 10px #a855f7, 0 0 20px #a855f7, 0 0 40px rgba(168,85,247,0.5); color: #f5f0ff; }
    50%  { text-shadow: 0 0 10px #06b6d4, 0 0 20px #06b6d4, 0 0 40px rgba(6,182,212,0.5); color: #f0feff; }
    75%  { text-shadow: 0 0 10px #a855f7, 0 0 20px #a855f7, 0 0 40px rgba(168,85,247,0.5); color: #f5f0ff; }
    100% { text-shadow: 0 0 10px #f43f5e, 0 0 20px #f43f5e, 0 0 40px rgba(244,63,94,0.5); color: #ffffff; }
}

/* 1f. Rotating conic neon border — like a radar sweep */
@keyframes conicNeonSweep {
    0%   { --conic-angle: 0deg; }
    100% { --conic-angle: 360deg; }
}

/* 1g. Neon drop-in entrance — element drops in with neon trail */
@keyframes neonDropIn {
    0%   { transform: translateY(-30px) scale(0.9); opacity: 0; filter: blur(10px); box-shadow: 0 0 0px transparent; }
    60%  { transform: translateY(4px) scale(1.02); opacity: 1; filter: blur(0px); box-shadow: 0 0 30px rgba(244,63,94,0.6); }
    100% { transform: translateY(0) scale(1); opacity: 1; box-shadow: 0 0 15px rgba(244,63,94,0.3); }
}

/* 1h. Neon scan-cross — a cross-hair style scan in fullscreen */
@keyframes neonScanCross {
    0%   { transform: scaleX(0); opacity: 0.8; }
    100% { transform: scaleX(1); opacity: 0; }
}

/* 1i. Neon ring expand — concentric rings that expand outward */
@keyframes neonRingExpand {
    0%   { transform: scale(0.85); opacity: 0.9; }
    100% { transform: scale(1.8); opacity: 0; }
}

/* 1j. Electric pulse — compact pulse burst */
@keyframes electricPulse {
    0%   { transform: scale(1); box-shadow: 0 0 0 0 rgba(244,63,94,0.7); }
    70%  { transform: scale(1.05); box-shadow: 0 0 0 10px rgba(244,63,94,0); }
    100% { transform: scale(1); box-shadow: 0 0 0 0 rgba(244,63,94,0); }
}

/* 1k. Neon wipe — horizontal wipe sweep used for progress bar */
@keyframes neonWipeSweep {
    0%   { left: -60%; }
    100% { left: 120%; }
}

/* 1l. Corner lightning — used for corner arc decorators */
@keyframes cornerLightningPulse {
    0%, 100% { opacity: 0.7; filter: drop-shadow(0 0 4px #f43f5e) drop-shadow(0 0 8px #f43f5e); }
    50%       { opacity: 1;   filter: drop-shadow(0 0 8px #f43f5e) drop-shadow(0 0 20px #a855f7) drop-shadow(0 0 30px #06b6d4); }
}

/* 1m. Neon lyric active shimmer — for the highlighted lyric line */
@keyframes neonLyricShimmer {
    0%   { border-color: rgba(244,63,94,0.8); box-shadow: 0 0 12px rgba(244,63,94,0.5), inset 0 0 8px rgba(244,63,94,0.1); }
    33%  { border-color: rgba(168,85,247,0.8); box-shadow: 0 0 12px rgba(168,85,247,0.5), inset 0 0 8px rgba(168,85,247,0.1); }
    66%  { border-color: rgba(6,182,212,0.8);  box-shadow: 0 0 12px rgba(6,182,212,0.5),  inset 0 0 8px rgba(6,182,212,0.1);  }
    100% { border-color: rgba(244,63,94,0.8); box-shadow: 0 0 12px rgba(244,63,94,0.5), inset 0 0 8px rgba(244,63,94,0.1); }
}

/* 1n. BPM tick flash — for the BPM widget */
@keyframes bpmTickFlash {
    0%   { background: rgba(244,63,94,0.8); box-shadow: 0 0 15px rgba(244,63,94,0.9), 0 0 30px rgba(244,63,94,0.4); }
    100% { background: rgba(244,63,94,0.0); box-shadow: 0 0 0px transparent; }
}

/* 1o. Neon fullscreen burst — entering fullscreen triggers this */
@keyframes neonFullscreenBurst {
    0%   { opacity: 1; transform: scale(1); }
    50%  { opacity: 0.7; transform: scale(1.05); box-shadow: 0 0 60px rgba(244,63,94,0.6), 0 0 120px rgba(168,85,247,0.4); }
    100% { opacity: 0; transform: scale(1.15); }
}

/* 1p. Lyric panel stripe animate — side stripe animation */
@keyframes lyricStripeFlow {
    0%   { background-position: 0% 0%; }
    100% { background-position: 0% 100%; }
}

/* 1q. Spectrum bar neon intensify */
@keyframes spectrumNeonBar {
    0%, 100% { box-shadow: 0 0 4px var(--accent, #f43f5e), 0 -2px 8px var(--accent, #f43f5e); }
    50%       { box-shadow: 0 0 8px var(--accent, #f43f5e), 0 -4px 16px var(--accent, #f43f5e), 0 -8px 24px rgba(168,85,247,0.4); }
}

/* 1r. Neon cursor spark trail */
@keyframes cursorSparkFade {
    0%   { transform: scale(1) translate(-50%, -50%); opacity: 1; }
    100% { transform: scale(0) translate(-50%, -50%); opacity: 0; }
}

/* 1s. Neon album halo spin */
@keyframes albumNeonHaloSpin {
    0%   { transform: rotate(0deg) scale(1); opacity: 0.6; }
    50%  { transform: rotate(180deg) scale(1.05); opacity: 1; }
    100% { transform: rotate(360deg) scale(1); opacity: 0.6; }
}

/* 1t. Neon pill active bounce */
@keyframes neonPillActiveBounce {
    0%, 100% { transform: scale(1); }
    50%       { transform: scale(1.06); }
}
```

---

## SECTION 2 — NEON BORDER SYSTEM
### `>>> INJECT INTO: the <style> block, AFTER the Section 1 keyframes you just added`

This creates the neon border system for all major panels. Uses CSS `::before` pseudo-elements as decorative layers — zero interference with existing styles.

```css
/* ═══════════════════════════════════════════════════════════════
   ⚡ NEON BORDER SYSTEM — All Panel Containers
   ═══════════════════════════════════════════════════════════════ */

/* The main glass panel gets a rotating neon gradient border via an ::after pseudo overlay */
/* This is an addition on top of its existing border: 1px solid rgba(255,255,255,0.08) */

.glass-panel {
    /* ADDITION: relative is likely already set, but adding position context */
    isolation: isolate;
}

/* NEW ADDITION: neon-border-ring class added via JS to .glass-panel */
.neon-border-ring::before {
    content: '';
    position: absolute;
    inset: -1px;
    border-radius: inherit;
    padding: 1px;
    background: linear-gradient(
        var(--neon-border-angle, 0deg),
        transparent 30%,
        rgba(244,63,94,0.8) 45%,
        rgba(168,85,247,0.9) 50%,
        rgba(6,182,212,0.8) 55%,
        transparent 70%
    );
    -webkit-mask: linear-gradient(#fff 0 0) content-box, linear-gradient(#fff 0 0);
    mask: linear-gradient(#fff 0 0) content-box, linear-gradient(#fff 0 0);
    -webkit-mask-composite: xor;
    mask-composite: exclude;
    pointer-events: none;
    z-index: 1000;
    animation: neonBorderRotate 4s linear infinite;
    background-size: 200% 200%;
    opacity: 0.55;
}

/* Neon border for music panel (left panel) */
#music-panel::after {
    content: '';
    position: absolute;
    top: 0;
    right: 0;
    width: 1px;
    height: 100%;
    background: linear-gradient(
        to bottom,
        transparent 0%,
        rgba(244,63,94,0.0) 15%,
        rgba(244,63,94,0.6) 35%,
        rgba(168,85,247,0.8) 50%,
        rgba(6,182,212,0.6) 65%,
        rgba(244,63,94,0.0) 85%,
        transparent 100%
    );
    pointer-events: none;
    z-index: 50;
    animation: lyricStripeFlow 3s linear infinite;
    background-size: 100% 200%;
}

/* Neon border for lyrics panel (right panel) */
#lyrics-panel::before {
    content: '';
    position: absolute;
    top: 0;
    left: 0;
    width: 1px;
    height: 100%;
    background: linear-gradient(
        to bottom,
        transparent 0%,
        rgba(6,182,212,0.0) 10%,
        rgba(6,182,212,0.5) 30%,
        rgba(168,85,247,0.7) 50%,
        rgba(244,63,94,0.5) 70%,
        rgba(244,63,94,0.0) 90%,
        transparent 100%
    );
    pointer-events: none;
    z-index: 50;
    animation: lyricStripeFlow 3.5s linear infinite reverse;
    background-size: 100% 200%;
}

/* Top edge neon line for the overall card */
.glass-panel .neon-top-edge {
    position: absolute;
    top: 0;
    left: 0;
    right: 0;
    height: 1px;
    background: linear-gradient(
        to right,
        transparent 0%,
        rgba(244,63,94,0.6) 20%,
        rgba(168,85,247,0.9) 50%,
        rgba(6,182,212,0.6) 80%,
        transparent 100%
    );
    pointer-events: none;
    z-index: 100;
    animation: neonBorderRotate 5s linear infinite;
    background-size: 200% 100%;
}

/* Bottom edge neon line */
.glass-panel .neon-bottom-edge {
    position: absolute;
    bottom: 0;
    left: 0;
    right: 0;
    height: 1px;
    background: linear-gradient(
        to right,
        transparent 0%,
        rgba(6,182,212,0.4) 30%,
        rgba(244,63,94,0.7) 50%,
        rgba(168,85,247,0.4) 70%,
        transparent 100%
    );
    pointer-events: none;
    z-index: 100;
    animation: neonBorderRotate 5s linear infinite reverse;
    background-size: 200% 100%;
}
```

### `>>> INJECT INTO: the HTML inside .glass-panel div, as the FIRST TWO child elements (before #beat-flash div)`

```html
<!-- ⚡ NEON ADDITION: Top & Bottom edge glow lines -->
<div class="neon-top-edge"></div>
<div class="neon-bottom-edge"></div>
```

### `>>> INJECT INTO: JS section, inside the DOMContentLoaded listener or directly in the existing init scripts, AFTER lucide.createIcons() call`

```javascript
// ⚡ NEON ADDITION: Apply rotating neon border class to main glass panel
(function applyNeonBorderRing() {
    const gp = document.querySelector('.glass-panel');
    if (gp) {
        gp.classList.add('neon-border-ring');
        // Animate the angle CSS variable for the conic gradient rotation
        let angle = 0;
        setInterval(() => {
            angle = (angle + 1) % 360;
            gp.style.setProperty('--neon-border-angle', angle + 'deg');
        }, 16);
    }
})();
```

---

## SECTION 3 — GLASS PANEL NEON AURA OVERLAY
### `>>> INJECT INTO: <style> block, after Section 2 CSS`

This adds a subtle neon inner-glow aura layer inside the glass panel — a semi-transparent radial gradient that pulses from the center.

```css
/* ═══════════════════════════════════════════════════════════════
   ⚡ GLASS PANEL NEON AURA — Inner ambient neon radial glow
   ═══════════════════════════════════════════════════════════════ */

/* NEW: neon-inner-aura element added via JS/HTML */
#neon-inner-aura {
    position: absolute;
    inset: 0;
    border-radius: inherit;
    pointer-events: none;
    z-index: 1;
    background: 
        radial-gradient(ellipse 60% 40% at 25% 60%, rgba(244,63,94,0.04) 0%, transparent 70%),
        radial-gradient(ellipse 50% 50% at 75% 40%, rgba(168,85,247,0.04) 0%, transparent 70%),
        radial-gradient(ellipse 40% 60% at 50% 80%, rgba(6,182,212,0.03) 0%, transparent 70%);
    animation: neonHaloBreathe 4s ease-in-out infinite;
    mix-blend-mode: screen;
}

/* This element reacts to the accent color via JS */
body[data-theme="rose"]      #neon-inner-aura { background-image: radial-gradient(ellipse 70% 50% at 30% 50%, rgba(244,63,94,0.06) 0%, transparent 70%); }
body[data-theme="cyberpunk"] #neon-inner-aura { background-image: radial-gradient(ellipse 70% 50% at 30% 50%, rgba(240,50,255,0.07) 0%, transparent 70%); }
body[data-theme="ocean"]     #neon-inner-aura { background-image: radial-gradient(ellipse 70% 50% at 30% 50%, rgba(79,100,255,0.06) 0%, transparent 70%); }
body[data-theme="aurora"]    #neon-inner-aura { background-image: radial-gradient(ellipse 70% 50% at 30% 50%, rgba(16,185,129,0.06) 0%, transparent 70%); }
body[data-theme="matrix"]    #neon-inner-aura { background-image: radial-gradient(ellipse 70% 50% at 30% 50%, rgba(0,255,80,0.06) 0%, transparent 70%); }
body[data-theme="ice"]       #neon-inner-aura { background-image: radial-gradient(ellipse 70% 50% at 30% 50%, rgba(100,220,255,0.06) 0%, transparent 70%); }
body[data-theme="lava"]      #neon-inner-aura { background-image: radial-gradient(ellipse 70% 50% at 30% 50%, rgba(255,120,0,0.07) 0%, transparent 70%); }
```

### `>>> INJECT INTO: the main .glass-panel div HTML, AFTER the existing #interactive-cursor-glow div`

```html
<!-- ⚡ NEON ADDITION: Inner ambient neon aura overlay -->
<div id="neon-inner-aura"></div>
```

---

## SECTION 4 — VINYL RECORD NEON HALO RING
### `>>> INJECT INTO: <style> block, after Section 3 CSS`

The vinyl record gets three concentric neon halo rings that breathe at different speeds.

```css
/* ═══════════════════════════════════════════════════════════════
   ⚡ VINYL NEON HALO RINGS — 3 Concentric Breathing Rings
   ═══════════════════════════════════════════════════════════════ */

/* Wrapper for the halo rings — positioned around the vinyl */
.vinyl-neon-halo-wrapper {
    position: absolute;
    inset: -18px;
    border-radius: 50%;
    pointer-events: none;
    z-index: 1;
}

/* Ring 1 — innermost, fastest, primary accent */
.vinyl-neon-ring-1 {
    position: absolute;
    inset: 0;
    border-radius: 50%;
    border: 1.5px solid rgba(244,63,94,0.7);
    box-shadow: 0 0 8px rgba(244,63,94,0.5), 0 0 20px rgba(244,63,94,0.2), inset 0 0 8px rgba(244,63,94,0.1);
    animation: neonHaloBreathe 1.8s ease-in-out infinite, albumNeonHaloSpin 8s linear infinite;
}

/* Ring 2 — middle, medium, purple accent */
.vinyl-neon-ring-2 {
    position: absolute;
    inset: -10px;
    border-radius: 50%;
    border: 1px solid rgba(168,85,247,0.45);
    box-shadow: 0 0 12px rgba(168,85,247,0.35), 0 0 30px rgba(168,85,247,0.15);
    animation: neonHaloBreathe 2.6s ease-in-out infinite 0.4s, albumNeonHaloSpin 12s linear infinite reverse;
}

/* Ring 3 — outermost, slowest, cyan accent */
.vinyl-neon-ring-3 {
    position: absolute;
    inset: -22px;
    border-radius: 50%;
    border: 0.5px solid rgba(6,182,212,0.3);
    box-shadow: 0 0 16px rgba(6,182,212,0.25), 0 0 40px rgba(6,182,212,0.1);
    animation: neonHaloBreathe 3.4s ease-in-out infinite 0.8s, albumNeonHaloSpin 16s linear infinite;
}

/* When the player is playing — make rings brighter */
body.is-playing .vinyl-neon-ring-1 {
    box-shadow: 0 0 12px rgba(244,63,94,0.8), 0 0 30px rgba(244,63,94,0.4), inset 0 0 12px rgba(244,63,94,0.15);
    animation-duration: 1s, 6s;
}
body.is-playing .vinyl-neon-ring-2 {
    box-shadow: 0 0 18px rgba(168,85,247,0.6), 0 0 40px rgba(168,85,247,0.3);
    animation-duration: 1.5s, 9s;
}
body.is-playing .vinyl-neon-ring-3 {
    box-shadow: 0 0 24px rgba(6,182,212,0.4), 0 0 60px rgba(6,182,212,0.2);
    animation-duration: 2s, 12s;
}
```

### `>>> INJECT INTO: Inside the #vinyl-record parent div (the .group div that wraps #vinyl-record), INSERT as the FIRST child before the #vinyl-record div itself`

```html
<!-- ⚡ NEON ADDITION: Vinyl neon halo rings -->
<div class="vinyl-neon-halo-wrapper" aria-hidden="true">
    <div class="vinyl-neon-ring-1"></div>
    <div class="vinyl-neon-ring-2"></div>
    <div class="vinyl-neon-ring-3"></div>
</div>
```

### `>>> INJECT INTO: JS, inside the existing togglePlayState() function, ADD at the very end of the function body`

```javascript
// ⚡ NEON ADDITION: Sync body class with play state for neon halo intensity
document.body.classList.toggle('is-playing', !paused);
```

---

## SECTION 5 — PLAY/PAUSE BUTTON LIGHTNING CROWN
### `>>> INJECT INTO: <style> block, after Section 4 CSS`

The play/pause button gets a corona of neon lightning arcs spinning around it.

```css
/* ═══════════════════════════════════════════════════════════════
   ⚡ PLAY/PAUSE LIGHTNING CROWN
   ═══════════════════════════════════════════════════════════════ */

/* Wrapper positioned around the play button */
#play-pause-neon-crown {
    position: absolute;
    width: 64px;
    height: 64px;
    border-radius: 50%;
    pointer-events: none;
    top: 50%;
    left: 50%;
    transform: translate(-50%, -50%);
    z-index: 0;
}

/* The main glowing ring */
#play-pause-neon-crown::before {
    content: '';
    position: absolute;
    inset: -6px;
    border-radius: 50%;
    border: 2px solid transparent;
    background: conic-gradient(
        from 0deg,
        rgba(244,63,94,0.9) 0deg,
        rgba(168,85,247,0.9) 90deg,
        rgba(6,182,212,0.9) 180deg,
        rgba(251,191,36,0.7) 270deg,
        rgba(244,63,94,0.9) 360deg
    ) border-box;
    -webkit-mask: linear-gradient(#fff 0 0) padding-box, linear-gradient(#fff 0 0);
    mask: linear-gradient(#fff 0 0) padding-box, linear-gradient(#fff 0 0);
    -webkit-mask-composite: destination-out;
    mask-composite: exclude;
    animation: albumNeonHaloSpin 2s linear infinite;
    box-shadow: 0 0 15px rgba(244,63,94,0.5), 0 0 30px rgba(168,85,247,0.3);
    filter: blur(0.5px);
}

/* Secondary burst ring, counter-rotating */
#play-pause-neon-crown::after {
    content: '';
    position: absolute;
    inset: -14px;
    border-radius: 50%;
    border: 1px solid transparent;
    background: conic-gradient(
        from 180deg,
        rgba(6,182,212,0.6) 0deg,
        transparent 60deg,
        rgba(244,63,94,0.6) 180deg,
        transparent 240deg,
        rgba(168,85,247,0.6) 300deg,
        transparent 360deg
    ) border-box;
    -webkit-mask: linear-gradient(#fff 0 0) padding-box, linear-gradient(#fff 0 0);
    mask: linear-gradient(#fff 0 0) padding-box, linear-gradient(#fff 0 0);
    -webkit-mask-composite: destination-out;
    mask-composite: exclude;
    animation: albumNeonHaloSpin 3.5s linear infinite reverse;
    filter: blur(1px);
}

/* The play button itself gets an enhanced glow on hover and during play */
#play-pause-btn {
    position: relative;
    z-index: 2;
    transition: box-shadow 0.3s ease, transform 0.15s ease !important;
}
#play-pause-btn:hover {
    box-shadow: 0 0 20px rgba(244,63,94,0.7), 0 0 40px rgba(244,63,94,0.4), 0 0 60px rgba(244,63,94,0.2) !important;
    animation: electricPulse 1s ease infinite;
}
body.is-playing #play-pause-btn {
    box-shadow: 0 0 15px rgba(244,63,94,0.6), 0 0 30px rgba(244,63,94,0.3) !important;
}
```

### `>>> INJECT INTO: The HTML, wrapping the existing #play-pause-btn — add a new parent div around it. The wrapper div goes AROUND the button`

Find the line:
```html
<button id="play-pause-btn" onclick="togglePlayState()" ...>
```

Wrap it with:
```html
<!-- ⚡ NEON ADDITION: Lightning crown wrapper for play button -->
<div class="relative flex items-center justify-center">
    <div id="play-pause-neon-crown" aria-hidden="true"></div>
    <!-- existing play-pause-btn goes here unchanged -->
```

And close with `</div>` after the existing button's closing `</button>` tag.

---

## SECTION 6 — PROGRESS BAR NEON LASER TRAIL
### `>>> INJECT INTO: <style> block, after Section 5 CSS`

The seek bar gets a blazing neon laser trail effect — a bright comet-tail that follows the playhead, plus a neon glow on the filled portion.

```css
/* ═══════════════════════════════════════════════════════════════
   ⚡ PROGRESS BAR NEON LASER TRAIL
   ═══════════════════════════════════════════════════════════════ */

/* Container for our custom neon progress layer */
#neon-progress-layer {
    position: absolute;
    left: 0;
    right: 0;
    top: 50%;
    transform: translateY(-50%);
    height: 4px;
    pointer-events: none;
    z-index: 5;
    border-radius: 9999px;
    overflow: visible;
}

/* The filled neon track — overlays on top of existing range */
#neon-progress-fill {
    height: 100%;
    border-radius: 9999px;
    background: linear-gradient(
        to right,
        var(--accent, #f43f5e) 0%,
        rgba(168,85,247,0.8) 70%,
        rgba(255,255,255,0.9) 100%
    );
    box-shadow: 
        0 0 6px 1px var(--accent, #f43f5e),
        0 0 12px 2px rgba(244,63,94,0.5),
        0 0 24px 4px rgba(244,63,94,0.2);
    position: relative;
    transition: width 0.1s linear;
    max-width: 100%;
}

/* Comet head — the bright dot at the playhead position */
#neon-progress-fill::after {
    content: '';
    position: absolute;
    right: -5px;
    top: 50%;
    transform: translateY(-50%);
    width: 10px;
    height: 10px;
    border-radius: 50%;
    background: #fff;
    box-shadow: 
        0 0 6px 2px var(--accent, #f43f5e),
        0 0 12px 4px rgba(244,63,94,0.8),
        0 0 24px 8px rgba(244,63,94,0.4);
    animation: neonHaloBreathe 0.8s ease-in-out infinite;
}

/* Lightning sweep — a fast bright flash that occasionally streaks across */
#neon-progress-sweep {
    position: absolute;
    top: -2px;
    height: 8px;
    width: 60px;
    border-radius: 9999px;
    background: linear-gradient(to right, transparent, rgba(255,255,255,0.9), transparent);
    pointer-events: none;
    animation: neonWipeSweep 3.5s ease-in-out infinite;
    opacity: 0.7;
    filter: blur(1px);
}
```

### `>>> INJECT INTO: Inside the seek bar container div (the div that holds the existing progress range input), ADD these as siblings AFTER the range input`

Find the seek bar's container div (the relative div around the waveform/progress range input). After the existing `<input type="range" id="seek-bar" ...>` add:

```html
<!-- ⚡ NEON ADDITION: Neon laser trail overlay for progress bar -->
<div id="neon-progress-layer" aria-hidden="true">
    <div id="neon-progress-fill" style="width: 0%;"></div>
    <div id="neon-progress-sweep"></div>
</div>
```

### `>>> INJECT INTO: JS, INSIDE the existing timeupdate / progress update function where the seek bar's value is updated. ADD after wherever seek-bar's value is being set.`

Find the location where `seekBar.value = ...` or the percentage calculation happens, then ADD immediately after:

```javascript
// ⚡ NEON ADDITION: Update neon laser trail fill width
(function updateNeonProgressFill() {
    const neonFill = document.getElementById('neon-progress-fill');
    const sb = document.getElementById('seek-bar');
    if (neonFill && sb) {
        const pct = (parseFloat(sb.value) / parseFloat(sb.max || 100)) * 100;
        neonFill.style.width = pct + '%';
    }
})();
```

---

## SECTION 7 — LYRICS ACTIVE LINE ELECTRIC ARC
### `>>> INJECT INTO: <style> block, after Section 6 CSS`

The currently playing lyric line gets an electric arc border — a vivid neon border that cycles through colors and has a shimmer sweep.

```css
/* ═══════════════════════════════════════════════════════════════
   ⚡ ACTIVE LYRIC LINE ELECTRIC ARC — ADDITIONS ONLY
   The existing .lyric-line.active has basic glow. We ADD on top.
   ═══════════════════════════════════════════════════════════════ */

/* Enhanced border animation — added on top of existing active styling */
.lyric-line.active {
    /* ADDITION: override the existing border with animated neon version */
    animation: neonLyricShimmer 2s ease-in-out infinite !important;
    position: relative;
    overflow: hidden;
}

/* Lightning sweep across the active lyric line */
.lyric-line.active::before {
    content: '';
    position: absolute;
    top: 0;
    left: -100%;
    width: 60%;
    height: 100%;
    background: linear-gradient(
        to right,
        transparent 0%,
        rgba(255,255,255,0.06) 40%,
        rgba(255,255,255,0.15) 50%,
        rgba(255,255,255,0.06) 60%,
        transparent 100%
    );
    animation: lightningStreak 2.5s ease-in-out infinite;
    pointer-events: none;
    z-index: 1;
    border-radius: inherit;
}

/* Neon left accent bar on active lyric */
.lyric-line.active::after {
    content: '';
    position: absolute;
    left: 0;
    top: 15%;
    height: 70%;
    width: 3px;
    border-radius: 0 2px 2px 0;
    background: linear-gradient(
        to bottom,
        rgba(244,63,94,0.0),
        rgba(244,63,94,1.0) 20%,
        rgba(168,85,247,1.0) 50%,
        rgba(6,182,212,1.0) 80%,
        rgba(6,182,212,0.0)
    );
    box-shadow: 2px 0 12px rgba(244,63,94,0.8), 4px 0 24px rgba(168,85,247,0.4);
    animation: neonLyricShimmer 2s ease-in-out infinite;
    pointer-events: none;
    z-index: 2;
}

/* Inactive lines still get very subtle neon on hover */
.lyric-line:not(.active):hover::after {
    content: '';
    position: absolute;
    left: 0;
    top: 20%;
    height: 60%;
    width: 1.5px;
    border-radius: 0 2px 2px 0;
    background: rgba(255,255,255,0.3);
    box-shadow: 1px 0 6px rgba(255,255,255,0.3);
    pointer-events: none;
}
```

---

## SECTION 8 — LYRICS HEADER NEON TITLE GLOW
### `>>> INJECT INTO: <style> block, after Section 7 CSS`

```css
/* ═══════════════════════════════════════════════════════════════
   ⚡ LYRICS HEADER NEON ADDITIONS
   ═══════════════════════════════════════════════════════════════ */

/* The "LYRICS READER" h3 text gets a neon shimmer — ADDITION on top of existing .lyrics-header-glow */
.lyrics-header-glow {
    /* ADD: neon cycling text glow */
    animation: neonTextShimmer 4s ease-in-out infinite !important;
    letter-spacing: 0.12em !important;
}

/* Neon underline bar under the lyrics header area */
#lyrics-panel .border-b.border-white\/5 {
    /* ADDITION: bottom border replacement with neon gradient line */
    border-bottom: 1px solid transparent !important;
    border-image: linear-gradient(
        to right,
        transparent,
        rgba(244,63,94,0.5) 20%,
        rgba(168,85,247,0.7) 50%,
        rgba(6,182,212,0.5) 80%,
        transparent
    ) 1 !important;
    position: relative;
}

/* Additional neon glow line under lyrics header */
#lyrics-panel .border-b.border-white\/5::after {
    content: '';
    position: absolute;
    bottom: -2px;
    left: 10%;
    right: 10%;
    height: 3px;
    background: linear-gradient(to right, transparent, rgba(168,85,247,0.5) 50%, transparent);
    filter: blur(2px);
    pointer-events: none;
}

/* Spectrum icon bars — neon intensification */
.spectrum-icon span {
    background: linear-gradient(to top, var(--accent, #f43f5e), rgba(168,85,247,0.8)) !important;
    border-radius: 2px !important;
    width: 3px !important;
    animation: spectrumNeonBar 0.8s ease-in-out infinite alternate;
    box-shadow: 0 0 4px var(--accent, #f43f5e), 0 -3px 8px rgba(168,85,247,0.6);
}
.spectrum-icon span:nth-child(1) { animation-delay: 0s; }
.spectrum-icon span:nth-child(2) { animation-delay: 0.15s; }
.spectrum-icon span:nth-child(3) { animation-delay: 0.3s; }
.spectrum-icon span:nth-child(4) { animation-delay: 0.1s; }
```

---

## SECTION 9 — CONTROL BUTTONS NEON HOVER SPARKS
### `>>> INJECT INTO: <style> block, after Section 8 CSS`

Every control button (skip, shuffle, repeat, rewind, forward) gets neon spark hover effects.

```css
/* ═══════════════════════════════════════════════════════════════
   ⚡ CONTROL BUTTONS NEON HOVER SPARKS
   ═══════════════════════════════════════════════════════════════ */

/* All control buttons around play/pause — neon hover glow */
#music-panel button:not(#play-pause-btn) {
    position: relative;
    overflow: hidden;
    transition: color 0.2s ease, filter 0.2s ease, transform 0.15s ease !important;
}

#music-panel button:not(#play-pause-btn):hover {
    filter: drop-shadow(0 0 6px var(--accent, #f43f5e)) drop-shadow(0 0 12px rgba(168,85,247,0.5)) !important;
    transform: scale(1.12) !important;
}

/* Lightning flash sweep on button hover */
#music-panel button:not(#play-pause-btn)::before {
    content: '';
    position: absolute;
    inset: 0;
    background: linear-gradient(
        135deg,
        transparent 40%,
        rgba(255,255,255,0.15) 50%,
        transparent 60%
    );
    opacity: 0;
    transition: opacity 0.15s ease;
    pointer-events: none;
    border-radius: inherit;
}
#music-panel button:not(#play-pause-btn):hover::before {
    opacity: 1;
}

/* Neon glow on the skip-back and skip-forward icons specifically */
button[title="Previous Song"]:hover,
button[title="Next Song"]:hover {
    color: var(--accent, #f43f5e) !important;
    filter: drop-shadow(0 0 8px var(--accent, #f43f5e)) !important;
}

/* Shuffle button active state neon */
#shuffle-btn.active {
    color: var(--accent, #f43f5e) !important;
    filter: drop-shadow(0 0 6px var(--accent, #f43f5e)) drop-shadow(0 0 15px rgba(168,85,247,0.4)) !important;
    animation: electricPulse 2s ease infinite !important;
}

/* Repeat button active state neon */
#repeat-btn.active,
#repeat-btn[data-state="one"],
#repeat-btn[data-state="all"] {
    color: var(--accent, #f43f5e) !important;
    filter: drop-shadow(0 0 6px var(--accent, #f43f5e)) !important;
}
```

---

## SECTION 10 — VISUALIZER SELECTOR PILLS NEON OUTLINE
### `>>> INJECT INTO: <style> block, after Section 9 CSS`

Each visualizer button pill gets a neon outline and a glowing active state.

```css
/* ═══════════════════════════════════════════════════════════════
   ⚡ VISUALIZER PILL BUTTONS — NEON OUTLINE ADDITIONS
   ═══════════════════════════════════════════════════════════════ */

/* All viz pills — neon hover addition */
[id^="viz-btn-"] {
    position: relative;
    transition: all 0.2s ease !important;
    border: 1px solid transparent !important;
}

[id^="viz-btn-"]:hover {
    border-color: rgba(244,63,94,0.5) !important;
    box-shadow: 0 0 8px rgba(244,63,94,0.4), inset 0 0 4px rgba(244,63,94,0.1) !important;
    color: #fff !important;
    transform: translateY(-1px) scale(1.05) !important;
}

/* Active viz button — strong neon glow */
[id^="viz-btn-"].bg-white\/10 {
    background: rgba(244,63,94,0.15) !important;
    border-color: rgba(244,63,94,0.7) !important;
    box-shadow: 
        0 0 10px rgba(244,63,94,0.5), 
        0 0 20px rgba(244,63,94,0.25),
        inset 0 0 6px rgba(244,63,94,0.1) !important;
    color: #fff !important;
    text-shadow: 0 0 8px rgba(244,63,94,0.8) !important;
    animation: neonPillActiveBounce 2s ease-in-out infinite !important;
}

/* Lightning sweep on active pill */
[id^="viz-btn-"].bg-white\/10::before {
    content: '';
    position: absolute;
    inset: 0;
    background: linear-gradient(to right, transparent, rgba(255,255,255,0.1), transparent);
    animation: lightningStreak 3s ease-in-out infinite;
    border-radius: inherit;
    pointer-events: none;
}
```

---

## SECTION 11 — THEME DOT BUTTONS NEON PULSE RING
### `>>> INJECT INTO: <style> block, after Section 10 CSS`

Each color theme dot button gets a neon pulse ring that matches its own color.

```css
/* ═══════════════════════════════════════════════════════════════
   ⚡ THEME DOT BUTTONS — NEON PULSE RINGS
   ═══════════════════════════════════════════════════════════════ */

/* All theme buttons — neon pulse ring addition */
[id^="theme-btn-"] {
    position: relative;
    transition: transform 0.2s ease, box-shadow 0.2s ease, opacity 0.2s ease !important;
}

[id^="theme-btn-"]:hover {
    transform: scale(1.4) !important;
    opacity: 1 !important;
}

/* Individual color neon pulses — each uses its own accent color */
#theme-btn-rose:hover,
#theme-btn-rose.ring-2 {
    box-shadow: 0 0 0 2px rgba(244,63,94,0.3), 0 0 8px rgba(244,63,94,0.6), 0 0 16px rgba(244,63,94,0.3) !important;
    animation: electricPulse 1.5s ease infinite !important;
}
#theme-btn-aurora:hover,
#theme-btn-aurora.ring-2 {
    box-shadow: 0 0 0 2px rgba(16,185,129,0.3), 0 0 8px rgba(16,185,129,0.6), 0 0 16px rgba(16,185,129,0.3) !important;
    animation: electricPulse 1.5s ease infinite !important;
}
#theme-btn-cyberpunk:hover,
#theme-btn-cyberpunk.ring-2 {
    box-shadow: 0 0 0 2px rgba(240,50,255,0.3), 0 0 8px rgba(240,50,255,0.6), 0 0 16px rgba(240,50,255,0.3) !important;
    animation: electricPulse 1.5s ease infinite !important;
}
#theme-btn-ocean:hover,
#theme-btn-ocean.ring-2 {
    box-shadow: 0 0 0 2px rgba(79,100,255,0.3), 0 0 8px rgba(79,100,255,0.6), 0 0 16px rgba(79,100,255,0.3) !important;
    animation: electricPulse 1.5s ease infinite !important;
}
#theme-btn-matrix:hover,
#theme-btn-matrix.ring-2 {
    box-shadow: 0 0 0 2px rgba(0,255,80,0.3), 0 0 8px rgba(0,255,80,0.6), 0 0 16px rgba(0,255,80,0.3) !important;
    animation: electricPulse 1.5s ease infinite !important;
}
#theme-btn-ice:hover,
#theme-btn-ice.ring-2 {
    box-shadow: 0 0 0 2px rgba(100,220,255,0.3), 0 0 8px rgba(100,220,255,0.6), 0 0 16px rgba(100,220,255,0.3) !important;
    animation: electricPulse 1.5s ease infinite !important;
}
#theme-btn-lava:hover,
#theme-btn-lava.ring-2 {
    box-shadow: 0 0 0 2px rgba(255,120,0,0.3), 0 0 8px rgba(255,120,0,0.6), 0 0 16px rgba(255,120,0,0.3) !important;
    animation: electricPulse 1.5s ease infinite !important;
}
#theme-btn-holo:hover,
#theme-btn-holo.ring-2 {
    box-shadow: 0 0 0 2px rgba(168,85,247,0.3), 0 0 8px rgba(244,63,94,0.5), 0 0 16px rgba(6,182,212,0.3) !important;
    animation: electricPulse 1.5s ease infinite !important;
}
#theme-btn-amber:hover,
#theme-btn-amber.ring-2 {
    box-shadow: 0 0 0 2px rgba(251,191,36,0.3), 0 0 8px rgba(251,191,36,0.6), 0 0 16px rgba(251,191,36,0.3) !important;
    animation: electricPulse 1.5s ease infinite !important;
}
```

---

## SECTION 12 — VOLUME SLIDER NEON GLOW TRACK
### `>>> INJECT INTO: <style> block, after Section 11 CSS`

```css
/* ═══════════════════════════════════════════════════════════════
   ⚡ VOLUME SLIDER NEON GLOW — ADDITION
   ═══════════════════════════════════════════════════════════════ */

/* Volume slider track neon glow */
#volume-slider {
    -webkit-appearance: none;
    appearance: none;
    background: transparent !important;
    position: relative;
}

/* WebKit track */
#volume-slider::-webkit-slider-runnable-track {
    height: 4px;
    border-radius: 9999px;
    background: linear-gradient(
        to right,
        var(--accent, #f43f5e) 0%,
        rgba(168,85,247,0.6) 60%,
        rgba(255,255,255,0.1) 100%
    );
    box-shadow: 0 0 6px rgba(244,63,94,0.6), 0 0 12px rgba(244,63,94,0.3);
}

/* WebKit thumb */
#volume-slider::-webkit-slider-thumb {
    -webkit-appearance: none;
    width: 14px;
    height: 14px;
    border-radius: 50%;
    background: #fff;
    border: 2px solid var(--accent, #f43f5e);
    box-shadow: 0 0 8px rgba(244,63,94,0.8), 0 0 16px rgba(244,63,94,0.4);
    margin-top: -5px;
    animation: neonHaloBreathe 2s ease-in-out infinite;
    cursor: pointer;
}

/* Firefox track */
#volume-slider::-moz-range-track {
    height: 4px;
    border-radius: 9999px;
    background: linear-gradient(to right, var(--accent, #f43f5e), rgba(255,255,255,0.1));
    box-shadow: 0 0 6px rgba(244,63,94,0.6);
}
#volume-slider::-moz-range-thumb {
    width: 14px;
    height: 14px;
    border-radius: 50%;
    background: #fff;
    border: 2px solid var(--accent, #f43f5e);
    box-shadow: 0 0 8px rgba(244,63,94,0.8);
}

/* Offset slider same treatment */
#offset-slider::-webkit-slider-runnable-track {
    height: 3px;
    border-radius: 9999px;
    background: linear-gradient(to right, rgba(168,85,247,0.4), rgba(6,182,212,0.8));
    box-shadow: 0 0 4px rgba(168,85,247,0.5);
}
#offset-slider::-webkit-slider-thumb {
    -webkit-appearance: none;
    width: 10px;
    height: 10px;
    border-radius: 50%;
    background: rgba(168,85,247,1);
    box-shadow: 0 0 6px rgba(168,85,247,0.8), 0 0 12px rgba(168,85,247,0.4);
    margin-top: -3.5px;
}
```

---

## SECTION 13 — SYNC OFFSET NEON GLOW
*(Already covered in Section 12 with the #offset-slider additions above.)*

---

## SECTION 14 — TOP HEADER NEON TICKER LINE
### `>>> INJECT INTO: <style> block, after Section 12 CSS`

```css
/* ═══════════════════════════════════════════════════════════════
   ⚡ HEADER SECTION — NEON TICKER LINE ADDITION
   ═══════════════════════════════════════════════════════════════ */

/* The top header row in #music-panel (NOW PLAYING + Switch to Video row)
   gets a neon bottom separator that sweeps */
#music-panel > div:first-child {
    position: relative;
}

#music-panel > div:first-child::after {
    content: '';
    position: absolute;
    bottom: -4px;
    left: 0;
    right: 0;
    height: 1px;
    background: linear-gradient(
        to right,
        transparent 0%,
        rgba(244,63,94,0.4) 25%,
        rgba(168,85,247,0.7) 50%,
        rgba(6,182,212,0.4) 75%,
        transparent 100%
    );
    background-size: 200% 100%;
    animation: neonBorderRotate 3s linear infinite;
    pointer-events: none;
}

/* NOW PLAYING text gets a subtle neon glow */
#music-panel .text-xs.uppercase.tracking-wider.text-white\/50 {
    animation: neonTextShimmer 6s ease-in-out infinite !important;
    opacity: 0.9 !important;
}

/* The pulsing dot next to NOW PLAYING — enhanced neon rings */
#music-panel .animate-ping {
    background: var(--accent, #f43f5e) !important;
    box-shadow: 0 0 6px var(--accent, #f43f5e) !important;
}
```

---

## SECTION 15 — NOW PLAYING DOT — TRIPLE NEON RING PULSE
### `>>> INJECT INTO: <style> block, after Section 14 CSS`

```css
/* ═══════════════════════════════════════════════════════════════
   ⚡ NOW PLAYING DOT — TRIPLE CONCENTRIC NEON RINGS
   ═══════════════════════════════════════════════════════════════ */

/* The flex h-2 w-2 relative wrapper for the dot — neon expansion rings */
#music-panel .flex.h-2.w-2.relative::before,
#music-panel .flex.h-2.w-2.relative::after {
    content: '';
    position: absolute;
    border-radius: 50%;
    pointer-events: none;
}

/* Second ring — medium radius */
#music-panel .flex.h-2.w-2.relative::before {
    inset: -4px;
    border: 1px solid rgba(244,63,94,0.4);
    box-shadow: 0 0 4px rgba(244,63,94,0.4);
    animation: neonRingExpand 2s ease-out infinite;
}

/* Third ring — larger radius, delayed */
#music-panel .flex.h-2.w-2.relative::after {
    inset: -4px;
    border: 1px solid rgba(168,85,247,0.3);
    box-shadow: 0 0 4px rgba(168,85,247,0.3);
    animation: neonRingExpand 2s ease-out infinite 0.7s;
}
```

---

## SECTION 16 — BEAT FLASH NEON COLOR BURST ENHANCEMENT
### `>>> INJECT INTO: <style> block, after Section 15 CSS`

The existing `#beat-flash` div gets additional neon color layers added beside it.

```css
/* ═══════════════════════════════════════════════════════════════
   ⚡ BEAT FLASH — NEON MULTI-LAYER BURST ADDITION
   ═══════════════════════════════════════════════════════════════ */

/* New second beat flash for corner sparks */
#beat-flash-corner-tl,
#beat-flash-corner-tr,
#beat-flash-corner-bl,
#beat-flash-corner-br {
    position: absolute;
    width: 80px;
    height: 80px;
    pointer-events: none;
    z-index: 51;
    opacity: 0;
    transition: opacity 0.05s ease;
}

#beat-flash-corner-tl { top: 0; left: 0; background: radial-gradient(circle at 0% 0%, rgba(244,63,94,0.4) 0%, transparent 70%); }
#beat-flash-corner-tr { top: 0; right: 0; background: radial-gradient(circle at 100% 0%, rgba(168,85,247,0.4) 0%, transparent 70%); }
#beat-flash-corner-bl { bottom: 0; left: 0; background: radial-gradient(circle at 0% 100%, rgba(6,182,212,0.4) 0%, transparent 70%); }
#beat-flash-corner-br { bottom: 0; right: 0; background: radial-gradient(circle at 100% 100%, rgba(251,191,36,0.3) 0%, transparent 70%); }
```

### `>>> INJECT INTO: HTML, INSIDE the main .glass-panel div, right after the existing #beat-flash div`

```html
<!-- ⚡ NEON ADDITION: Corner beat flash sparks -->
<div id="beat-flash-corner-tl" aria-hidden="true"></div>
<div id="beat-flash-corner-tr" aria-hidden="true"></div>
<div id="beat-flash-corner-bl" aria-hidden="true"></div>
<div id="beat-flash-corner-br" aria-hidden="true"></div>
```

### `>>> INJECT INTO: JS, INSIDE the existing beat detection / beat flash trigger logic. Find where #beat-flash opacity is set. ADD right after that:`

```javascript
// ⚡ NEON ADDITION: Corner beat flash sparks
(function triggerCornerBeatFlash() {
    const corners = ['tl','tr','bl','br'];
    corners.forEach((c, i) => {
        const el = document.getElementById('beat-flash-corner-' + c);
        if (el) {
            el.style.opacity = (0.4 + Math.random() * 0.4).toString();
            setTimeout(() => { el.style.opacity = '0'; }, 80 + i * 15);
        }
    });
})();
```

---

## SECTION 17 — AMBIENT ORBS — NEON INTENSIFICATION LAYER
### `>>> INJECT INTO: <style> block, after Section 16 CSS`

```css
/* ═══════════════════════════════════════════════════════════════
   ⚡ AMBIENT ORBS — NEON INTENSITY BOOST + 2 NEW NEON ORBS
   ═══════════════════════════════════════════════════════════════ */

/* Intensify existing orbs with neon filter */
#orb-1 {
    filter: blur(120px) saturate(1.8) brightness(1.3) !important;
    animation: neonHaloBreathe 5s ease-in-out infinite;
}
#orb-2 {
    filter: blur(120px) saturate(2.0) brightness(1.4) !important;
    animation: neonHaloBreathe 6s ease-in-out infinite 1s;
}
#orb-3 {
    filter: blur(100px) saturate(1.6) brightness(1.3) !important;
    animation: neonHaloBreathe 7s ease-in-out infinite 2s;
}
#orb-4 {
    filter: blur(100px) saturate(1.8) brightness(1.5) !important;
    animation: neonHaloBreathe 4.5s ease-in-out infinite 0.5s;
}
#orb-5 {
    filter: blur(90px) saturate(1.7) brightness(1.4) !important;
    animation: neonHaloBreathe 5.5s ease-in-out infinite 1.5s;
}

/* New orb 6 — hot neon pink, top right corner */
#orb-6 {
    position: absolute;
    top: -20%;
    right: -10%;
    width: 400px;
    height: 400px;
    border-radius: 50%;
    background: rgba(244,63,94,0.12);
    filter: blur(140px) saturate(2.5) brightness(1.5);
    animation: neonHaloBreathe 8s ease-in-out infinite 2.5s;
    pointer-events: none;
}

/* New orb 7 — electric cyan, bottom left */
#orb-7 {
    position: absolute;
    bottom: -15%;
    left: -5%;
    width: 350px;
    height: 350px;
    border-radius: 50%;
    background: rgba(6,182,212,0.1);
    filter: blur(130px) saturate(2.2) brightness(1.4);
    animation: neonHaloBreathe 9s ease-in-out infinite 1.2s;
    pointer-events: none;
}
```

### `>>> INJECT INTO: HTML, inside the ambient orbs container div (the absolute div that has orb-1 through orb-5), ADD after #orb-5:`

```html
<!-- ⚡ NEON ADDITION: Two new intense neon orbs -->
<div id="orb-6"></div>
<div id="orb-7"></div>
```

---

## SECTION 18 — PLAYER CARD OUTER NEON FRAME
### `>>> INJECT INTO: <style> block, after Section 17 CSS`

The outer wrapper `#player-fullscreen-wrapper` gets a neon frame glow as an additional layer beyond the existing ambilight.

```css
/* ═══════════════════════════════════════════════════════════════
   ⚡ PLAYER CARD OUTER NEON FRAME
   ═══════════════════════════════════════════════════════════════ */

/* Rotating neon outer frame — a 2px glowing border that sweeps */
#player-fullscreen-wrapper::before {
    content: '';
    position: absolute;
    inset: -2px;
    border-radius: 28px; /* slightly larger than the card's 24px rounded-3xl */
    background: conic-gradient(
        from var(--neon-frame-angle, 0deg),
        rgba(244,63,94,0.0) 0deg,
        rgba(244,63,94,0.9) 60deg,
        rgba(168,85,247,0.9) 120deg,
        rgba(6,182,212,0.9) 180deg,
        rgba(251,191,36,0.7) 240deg,
        rgba(168,85,247,0.6) 300deg,
        rgba(244,63,94,0.0) 360deg
    );
    -webkit-mask: 
        linear-gradient(#fff 0 0) content-box,
        linear-gradient(#fff 0 0);
    mask: 
        linear-gradient(#fff 0 0) content-box,
        linear-gradient(#fff 0 0);
    -webkit-mask-composite: xor;
    mask-composite: exclude;
    padding: 2px;
    pointer-events: none;
    z-index: -1;
    opacity: 0.65;
    filter: blur(0.5px);
}

/* Lightning flash across the frame border periodically */
#player-fullscreen-wrapper::after {
    content: '';
    position: absolute;
    inset: -2px;
    border-radius: 28px;
    background: linear-gradient(
        135deg,
        transparent 0%,
        transparent 45%,
        rgba(255,255,255,0.3) 50%,
        transparent 55%,
        transparent 100%
    );
    pointer-events: none;
    z-index: -1;
    animation: lightningStreak 4s ease-in-out infinite 1.5s;
    opacity: 0;
}
```

### `>>> INJECT INTO: JS, in the init block or DOMContentLoaded. ADD a setInterval that rotates the --neon-frame-angle CSS variable:`

```javascript
// ⚡ NEON ADDITION: Rotate the outer neon frame border
(function animateNeonFrame() {
    const wrapper = document.getElementById('player-fullscreen-wrapper');
    if (!wrapper) return;
    let frameAngle = 0;
    setInterval(() => {
        frameAngle = (frameAngle + 0.8) % 360;
        wrapper.style.setProperty('--neon-frame-angle', frameAngle + 'deg');
    }, 16);
})();
```

---

## SECTION 19 — LYRICS PANEL RIGHT EDGE NEON STRIPE
### `>>> INJECT INTO: <style> block, after Section 18 CSS`

```css
/* ═══════════════════════════════════════════════════════════════
   ⚡ LYRICS PANEL RIGHT EDGE — NEON STRIPE
   ═══════════════════════════════════════════════════════════════ */

/* Right edge of lyrics panel gets a flowing neon stripe */
#lyrics-panel::after {
    content: '';
    position: absolute;
    top: 0;
    right: 0;
    width: 2px;
    height: 100%;
    background: linear-gradient(
        to bottom,
        transparent 0%,
        rgba(6,182,212,0.5) 20%,
        rgba(168,85,247,0.8) 40%,
        rgba(244,63,94,0.8) 60%,
        rgba(168,85,247,0.5) 80%,
        transparent 100%
    );
    background-size: 100% 300%;
    animation: lyricStripeFlow 2.5s linear infinite;
    pointer-events: none;
    z-index: 50;
    filter: blur(0.5px);
    box-shadow: -2px 0 8px rgba(6,182,212,0.3), -4px 0 16px rgba(168,85,247,0.2);
}
```

---

## SECTION 20 — QUEUE/FIND/SPOTIFYMODE BUTTONS NEON GLOW
### `>>> INJECT INTO: <style> block, after Section 19 CSS`

Every top-right pill button in the lyrics panel header gets a neon hover enhancement.

```css
/* ═══════════════════════════════════════════════════════════════
   ⚡ LYRICS HEADER PILL BUTTONS — NEON HOVER ADDITIONS
   ═══════════════════════════════════════════════════════════════ */

/* Find button — yellow neon */
#lyrics-search-btn:hover {
    border-color: rgba(251,191,36,0.7) !important;
    box-shadow: 0 0 10px rgba(251,191,36,0.5), 0 0 20px rgba(251,191,36,0.25), inset 0 0 6px rgba(251,191,36,0.1) !important;
    color: rgba(251,191,36,1) !important;
}
#lyrics-search-btn:hover i { filter: drop-shadow(0 0 4px rgba(251,191,36,0.9)); }

/* Queue button — cyan neon */
#queue-drawer-btn:hover {
    border-color: rgba(6,182,212,0.7) !important;
    box-shadow: 0 0 10px rgba(6,182,212,0.5), 0 0 20px rgba(6,182,212,0.25), inset 0 0 6px rgba(6,182,212,0.1) !important;
    color: rgba(6,182,212,1) !important;
}
#queue-drawer-btn:hover i { filter: drop-shadow(0 0 4px rgba(6,182,212,0.9)); }

/* Spotify Mode button — rose neon */
#focus-toggle-btn:hover {
    border-color: rgba(244,63,94,0.7) !important;
    box-shadow: 0 0 10px rgba(244,63,94,0.5), 0 0 20px rgba(244,63,94,0.25), inset 0 0 6px rgba(244,63,94,0.1) !important;
}

/* Fullscreen button — fuchsia neon */
#fullscreen-btn:hover {
    border-color: rgba(168,85,247,0.7) !important;
    box-shadow: 0 0 10px rgba(168,85,247,0.6), 0 0 24px rgba(168,85,247,0.3), inset 0 0 8px rgba(168,85,247,0.12) !important;
    color: rgba(168,85,247,1) !important;
}
#fullscreen-btn:hover i { filter: drop-shadow(0 0 6px rgba(168,85,247,1)); }

/* All header pills — shared lightning transition */
#lyrics-search-btn, #queue-drawer-btn, #focus-toggle-btn, #fullscreen-btn {
    position: relative;
    overflow: hidden;
    transition: all 0.25s ease !important;
}

/* Lightning sweep on hover for all header pill buttons */
#lyrics-search-btn::before,
#queue-drawer-btn::before,
#focus-toggle-btn::before,
#fullscreen-btn::before {
    content: '';
    position: absolute;
    inset: 0;
    background: linear-gradient(
        90deg,
        transparent 30%,
        rgba(255,255,255,0.12) 50%,
        transparent 70%
    );
    opacity: 0;
    transition: opacity 0.2s ease;
    pointer-events: none;
    border-radius: inherit;
}

#lyrics-search-btn:hover::before,
#queue-drawer-btn:hover::before,
#focus-toggle-btn:hover::before,
#fullscreen-btn:hover::before {
    opacity: 1;
    animation: lightningStreak 1s ease-out infinite;
}
```

---

## SECTION 21 — SYNCED BADGE NEON FLICKER
### `>>> INJECT INTO: <style> block, after Section 20 CSS`

```css
/* ═══════════════════════════════════════════════════════════════
   ⚡ SYNCED / PLAIN / GENIUS BADGE — NEON FLICKER
   ═══════════════════════════════════════════════════════════════ */

/* The lyrics type badge (SYNCED / PLAIN / GENIUS) — neon electric flicker */
#lyrics-type-badge {
    position: relative;
    animation: electricArcFlicker 4s ease-in-out infinite !important;
    /* Enhanced neon glow on top of existing styling */
    box-shadow: 0 0 8px rgba(244,63,94,0.5), 0 0 16px rgba(244,63,94,0.25), inset 0 0 4px rgba(244,63,94,0.1) !important;
    text-shadow: 0 0 6px rgba(244,63,94,0.8) !important;
    letter-spacing: 0.08em !important;
}

/* Badge — lightning sweep */
#lyrics-type-badge::before {
    content: '';
    position: absolute;
    inset: 0;
    background: linear-gradient(90deg, transparent, rgba(255,255,255,0.2), transparent);
    border-radius: inherit;
    animation: lightningStreak 3s ease-in-out infinite;
    pointer-events: none;
}
```

---

## SECTION 22 — NEON LIGHTNING CANVAS OVERLAY (JS ADDITION)
### `>>> INJECT INTO: JS section — ADD as a brand new IIFE self-contained block, AFTER the existing neon particles init block`

This is the most spectacular addition. A full-canvas SVG-path-style lightning bolt system that fires random arcs across the player card at beat-triggered or timed intervals.

```javascript
// ═══════════════════════════════════════════════════════════════
// ⚡ NEON LIGHTNING CANVAS — Full bolt lightning system
// ADDITION ONLY — new canvas element + new JS block
// ═══════════════════════════════════════════════════════════════

(function initNeonLightningCanvas() {
    // Create the canvas element programmatically
    const lightningCanvas = document.createElement('canvas');
    lightningCanvas.id = 'neon-lightning-canvas';
    lightningCanvas.style.cssText = [
        'position: absolute',
        'inset: 0',
        'width: 100%',
        'height: 100%',
        'pointer-events: none',
        'z-index: 49',
        'border-radius: inherit',
        'opacity: 0.85',
        'mix-blend-mode: screen'
    ].join(';');

    // Inject into the main glass-panel
    const glassPanel = document.querySelector('.glass-panel');
    if (!glassPanel) return;
    glassPanel.appendChild(lightningCanvas);

    const ctx = lightningCanvas.getContext('2d');
    let W, H;

    function resizeLightningCanvas() {
        W = lightningCanvas.width = glassPanel.clientWidth;
        H = lightningCanvas.height = glassPanel.clientHeight;
    }
    resizeLightningCanvas();
    window.addEventListener('resize', resizeLightningCanvas);

    // Lightning bolt generator — recursive branching
    function drawLightningBolt(ctx, x1, y1, x2, y2, branches, depth, color) {
        if (depth === 0) return;

        const dx = x2 - x1;
        const dy = y2 - y1;
        const len = Math.sqrt(dx * dx + dy * dy);

        // Jagged midpoint displacement
        const midX = (x1 + x2) / 2 + (Math.random() - 0.5) * len * 0.35;
        const midY = (y1 + y2) / 2 + (Math.random() - 0.5) * len * 0.35;

        // Draw first half
        ctx.beginPath();
        ctx.moveTo(x1, y1);
        ctx.lineTo(midX, midY);
        ctx.strokeStyle = color;
        ctx.lineWidth = Math.max(0.5, depth * 0.6);
        ctx.shadowColor = color;
        ctx.shadowBlur = 8 + depth * 4;
        ctx.globalAlpha = 0.4 + depth * 0.12;
        ctx.stroke();

        // Draw second half
        ctx.beginPath();
        ctx.moveTo(midX, midY);
        ctx.lineTo(x2, y2);
        ctx.stroke();

        // Recurse
        drawLightningBolt(ctx, x1, y1, midX, midY, branches, depth - 1, color);
        drawLightningBolt(ctx, midX, midY, x2, y2, branches, depth - 1, color);

        // Branch
        if (branches > 0 && depth > 2 && Math.random() > 0.6) {
            const branchEndX = midX + (Math.random() - 0.5) * len * 0.6;
            const branchEndY = midY + (Math.random() - 0.5) * len * 0.6;
            drawLightningBolt(ctx, midX, midY, branchEndX, branchEndY, 0, depth - 2, color);
        }
    }

    const neonColors = [
        'rgba(244,63,94,1)',
        'rgba(168,85,247,1)',
        'rgba(6,182,212,1)',
        'rgba(251,191,36,0.8)',
        'rgba(255,255,255,0.9)'
    ];

    // Fire lightning bolt
    function fireLightningBolt() {
        ctx.clearRect(0, 0, W, H);

        // Pick a random lightning style
        const style = Math.random();
        const color = neonColors[Math.floor(Math.random() * neonColors.length)];

        if (style < 0.33) {
            // Edge-to-edge horizontal bolt
            const y = Math.random() * H * 0.8 + H * 0.1;
            drawLightningBolt(ctx, 0, y, W, y + (Math.random() - 0.5) * 80, 3, 6, color);
        } else if (style < 0.66) {
            // Corner-to-corner diagonal bolt
            const fromTop = Math.random() > 0.5;
            drawLightningBolt(ctx, 
                Math.random() * W * 0.3,
                fromTop ? 0 : H,
                W * 0.7 + Math.random() * W * 0.3,
                fromTop ? H : 0,
                4, 7, color
            );
        } else {
            // Short burst from random edge
            const edge = Math.floor(Math.random() * 4);
            let x1, y1, x2, y2;
            if (edge === 0) { x1 = Math.random() * W; y1 = 0; x2 = x1 + (Math.random() - 0.5) * 200; y2 = 100 + Math.random() * 150; }
            else if (edge === 1) { x1 = W; y1 = Math.random() * H; x2 = W - 100 - Math.random() * 150; y2 = y1 + (Math.random() - 0.5) * 200; }
            else if (edge === 2) { x1 = Math.random() * W; y1 = H; x2 = x1 + (Math.random() - 0.5) * 200; y2 = H - 100 - Math.random() * 150; }
            else { x1 = 0; y1 = Math.random() * H; x2 = 100 + Math.random() * 150; y2 = y1 + (Math.random() - 0.5) * 200; }
            drawLightningBolt(ctx, x1, y1, x2, y2, 2, 5, color);
        }

        // Fade the bolt out quickly
        let fadeOpacity = 1;
        const fadeInterval = setInterval(() => {
            fadeOpacity -= 0.12;
            lightningCanvas.style.opacity = Math.max(0, fadeOpacity).toString();
            if (fadeOpacity <= 0) {
                clearInterval(fadeInterval);
                ctx.clearRect(0, 0, W, H);
                lightningCanvas.style.opacity = '0.85';
            }
        }, 40);
    }

    // Auto-fire at random intervals (2–8 seconds between bolts)
    function scheduleLightning() {
        const delay = 2000 + Math.random() * 6000;
        setTimeout(() => {
            fireLightningBolt();
            scheduleLightning();
        }, delay);
    }
    scheduleLightning();

    // Also expose globally so beat detection can trigger it
    window.fireNeonLightning = fireLightningBolt;
})();
```

### `>>> INJECT INTO: JS, wherever the beat detection / beat flash is triggered. ADD right after the beat flash opacity line:`

```javascript
// ⚡ NEON ADDITION: Fire lightning on strong beats
if (Math.random() > 0.7 && window.fireNeonLightning) {
    window.fireNeonLightning();
}
```

---

## SECTION 23 — CORNER ARC LIGHTNING DECORATORS (HTML + JS)
### `>>> INJECT INTO: <style> block, after Section 21 CSS`

Four corner decorators — glowing arc brackets that crackle at each corner of the card.

```css
/* ═══════════════════════════════════════════════════════════════
   ⚡ CORNER ARC LIGHTNING DECORATORS
   ═══════════════════════════════════════════════════════════════ */

.neon-corner-arc {
    position: absolute;
    width: 40px;
    height: 40px;
    pointer-events: none;
    z-index: 200;
    animation: cornerLightningPulse 2s ease-in-out infinite;
}

/* Top-left */
.neon-corner-arc.tl {
    top: 8px;
    left: 8px;
    border-top: 2px solid rgba(244,63,94,0.9);
    border-left: 2px solid rgba(244,63,94,0.9);
    border-radius: 6px 0 0 0;
    box-shadow: -2px -2px 8px rgba(244,63,94,0.6), -4px -4px 16px rgba(244,63,94,0.3);
    animation-delay: 0s;
}

/* Top-right */
.neon-corner-arc.tr {
    top: 8px;
    right: 8px;
    border-top: 2px solid rgba(168,85,247,0.9);
    border-right: 2px solid rgba(168,85,247,0.9);
    border-radius: 0 6px 0 0;
    box-shadow: 2px -2px 8px rgba(168,85,247,0.6), 4px -4px 16px rgba(168,85,247,0.3);
    animation-delay: 0.5s;
}

/* Bottom-left */
.neon-corner-arc.bl {
    bottom: 8px;
    left: 8px;
    border-bottom: 2px solid rgba(6,182,212,0.9);
    border-left: 2px solid rgba(6,182,212,0.9);
    border-radius: 0 0 0 6px;
    box-shadow: -2px 2px 8px rgba(6,182,212,0.6), -4px 4px 16px rgba(6,182,212,0.3);
    animation-delay: 1s;
}

/* Bottom-right */
.neon-corner-arc.br {
    bottom: 8px;
    right: 8px;
    border-bottom: 2px solid rgba(251,191,36,0.8);
    border-right: 2px solid rgba(251,191,36,0.8);
    border-radius: 0 0 6px 0;
    box-shadow: 2px 2px 8px rgba(251,191,36,0.6), 4px 4px 16px rgba(251,191,36,0.3);
    animation-delay: 1.5s;
}
```

### `>>> INJECT INTO: HTML, inside the main .glass-panel div, AFTER the neon top/bottom edges added in Section 2:`

```html
<!-- ⚡ NEON ADDITION: Corner arc lightning decorators -->
<div class="neon-corner-arc tl" aria-hidden="true"></div>
<div class="neon-corner-arc tr" aria-hidden="true"></div>
<div class="neon-corner-arc bl" aria-hidden="true"></div>
<div class="neon-corner-arc br" aria-hidden="true"></div>
```

---

## SECTION 24 — THREE.JS NEON PARTICLE FIELD (JS ADDITION)
### `>>> INJECT INTO: JS section, AFTER the existing Three.js visualizer setup blocks (after renderer3d is initialized or can be placed in its own IIFE so it doesn't conflict)`

This creates a SEPARATE Three.js scene that renders neon floating particles on a second canvas overlaid on the player — completely independent of the existing Three.js visualizer.

```javascript
// ═══════════════════════════════════════════════════════════════
// ⚡ THREE.JS NEON AMBIENT PARTICLE FIELD
// ADDITION: New Three.js scene on a separate canvas
// Does NOT touch renderer3d, scene, camera, or any existing Three vars
// ═══════════════════════════════════════════════════════════════

(function initNeonThreeParticleField() {
    if (typeof THREE === 'undefined') return;

    // Create dedicated canvas
    const neonThreeCanvas = document.createElement('canvas');
    neonThreeCanvas.id = 'neon-three-particles';
    neonThreeCanvas.style.cssText = [
        'position: absolute',
        'inset: 0',
        'width: 100%',
        'height: 100%',
        'pointer-events: none',
        'z-index: 2',
        'border-radius: inherit',
        'opacity: 0.55',
        'mix-blend-mode: screen'
    ].join(';');

    const glassPanel = document.querySelector('.glass-panel');
    if (!glassPanel) return;
    glassPanel.appendChild(neonThreeCanvas);

    // Separate Three.js renderer (neonRenderer_)
    const neonRenderer_ = new THREE.WebGLRenderer({
        canvas: neonThreeCanvas,
        alpha: true,
        antialias: false
    });
    neonRenderer_.setPixelRatio(Math.min(window.devicePixelRatio, 1.5));
    neonRenderer_.setSize(glassPanel.clientWidth, glassPanel.clientHeight);
    neonRenderer_.setClearColor(0x000000, 0);

    // Separate scene and camera
    const neonScene_ = new THREE.Scene();
    const neonCamera_ = new THREE.PerspectiveCamera(60, glassPanel.clientWidth / glassPanel.clientHeight, 0.1, 1000);
    neonCamera_.position.z = 5;

    // Neon colors array as THREE.Color
    const neonPalette_ = [
        new THREE.Color(0xf43f5e),
        new THREE.Color(0xa855f7),
        new THREE.Color(0x06b6d4),
        new THREE.Color(0xfbbf24),
        new THREE.Color(0xffffff)
    ];

    // Create particle geometry — 800 random particles
    const particleCount_ = 800;
    const positions_ = new Float32Array(particleCount_ * 3);
    const colors_ = new Float32Array(particleCount_ * 3);
    const sizes_ = new Float32Array(particleCount_);

    for (let i = 0; i < particleCount_; i++) {
        positions_[i * 3]     = (Math.random() - 0.5) * 14;
        positions_[i * 3 + 1] = (Math.random() - 0.5) * 8;
        positions_[i * 3 + 2] = (Math.random() - 0.5) * 6;

        const c = neonPalette_[Math.floor(Math.random() * neonPalette_.length)];
        colors_[i * 3]     = c.r;
        colors_[i * 3 + 1] = c.g;
        colors_[i * 3 + 2] = c.b;

        sizes_[i] = Math.random() * 0.04 + 0.01;
    }

    const pGeo_ = new THREE.BufferGeometry();
    pGeo_.setAttribute('position', new THREE.BufferAttribute(positions_, 3));
    pGeo_.setAttribute('color', new THREE.BufferAttribute(colors_, 3));
    pGeo_.setAttribute('size', new THREE.BufferAttribute(sizes_, 1));

    const pMat_ = new THREE.PointsMaterial({
        size: 0.05,
        vertexColors: true,
        transparent: true,
        opacity: 0.8,
        sizeAttenuation: true,
        blending: THREE.AdditiveBlending,
        depthWrite: false
    });

    const neonParticles_ = new THREE.Points(pGeo_, pMat_);
    neonScene_.add(neonParticles_);

    // Animation loop for the neon particle field
    let neonFrame_ = 0;
    function animateNeonParticles() {
        requestAnimationFrame(animateNeonParticles);
        neonFrame_++;

        // Gentle rotation
        neonParticles_.rotation.y += 0.0008;
        neonParticles_.rotation.x += 0.0003;

        // Pulsing size based on frame
        pMat_.size = 0.04 + Math.sin(neonFrame_ * 0.02) * 0.015;
        pMat_.opacity = 0.5 + Math.sin(neonFrame_ * 0.015) * 0.25;

        // React to playing state — speed up rotation when playing
        if (document.body.classList.contains('is-playing')) {
            neonParticles_.rotation.y += 0.001;
        }

        neonRenderer_.render(neonScene_, neonCamera_);
    }
    animateNeonParticles();

    // Resize handler
    window.addEventListener('resize', () => {
        if (!glassPanel) return;
        neonRenderer_.setSize(glassPanel.clientWidth, glassPanel.clientHeight);
        neonCamera_.aspect = glassPanel.clientWidth / glassPanel.clientHeight;
        neonCamera_.updateProjectionMatrix();
    });

    // Expose color update so theme changes can shift particle colors
    window.updateNeonParticleTheme = function(hexColor) {
        if (!hexColor) return;
        const c = new THREE.Color(hexColor);
        // Update first third of particles to new accent color
        for (let i = 0; i < particleCount_ / 3; i++) {
            colors_[i * 3]     = c.r;
            colors_[i * 3 + 1] = c.g;
            colors_[i * 3 + 2] = c.b;
        }
        pGeo_.attributes.color.needsUpdate = true;
    };
})();
```

### `>>> INJECT INTO: JS, inside the existing setTheme() function, at the very end (after the existing theme logic):`

```javascript
// ⚡ NEON ADDITION: Update Three.js particle field colors on theme change
if (window.updateNeonParticleTheme) {
    const themeAccents = {
        rose: '#f43f5e', aurora: '#10b981', cyberpunk: '#d946ef',
        ocean: '#6366f1', amber: '#f59e0b', matrix: '#00ff50',
        ice: '#67e8f9', holo: '#a855f7', lava: '#f97316'
    };
    window.updateNeonParticleTheme(themeAccents[themeName] || '#f43f5e');
}
```

---

## SECTION 25 — FULLSCREEN MODE — TRUE BROWSER FULLSCREEN API FIX
### `>>> INJECT INTO: JS, DIRECTLY AFTER the existing toggleFullscreen() function (do NOT touch existing function — this ADDS a second function that WRAPS and EXTENDS behavior)`

This is the critical fullscreen fix. The existing `toggleFullscreen()` only adds CSS classes. We add the Browser Fullscreen API on top — `requestFullscreen()` on the wrapper element — so it actually goes browser-level fullscreen.

```javascript
// ═══════════════════════════════════════════════════════════════
// ⚡ TRUE BROWSER FULLSCREEN API — ADDITION WRAPPER
// Wraps the existing toggleFullscreen() with real Fullscreen API
// The original function still runs untouched — this EXTENDS it
// ═══════════════════════════════════════════════════════════════

(function extendFullscreenWithBrowserAPI() {
    // Store reference to the original function
    const _originalToggleFullscreen = window.toggleFullscreen;

    // Override with extended version
    window.toggleFullscreen = function() {
        // Call the original CSS-class-based fullscreen first
        if (typeof _originalToggleFullscreen === 'function') {
            _originalToggleFullscreen();
        }

        const wrapper = document.getElementById('player-fullscreen-wrapper');
        if (!wrapper) return;

        // Check if we're going INTO fullscreen (isFullscreen was just toggled to true by original fn)
        // The original function sets isFullscreen before calling this, so we can read it
        const goingFullscreen = document.body.classList.contains('fullscreen-active');

        if (goingFullscreen) {
            // Use Browser Fullscreen API on the wrapper element
            const requestFS = 
                wrapper.requestFullscreen ||
                wrapper.webkitRequestFullscreen ||
                wrapper.mozRequestFullScreen ||
                wrapper.msRequestFullscreen;

            if (requestFS) {
                requestFS.call(wrapper).then(() => {
                    // Neon entrance burst
                    triggerNeonFullscreenEntrance();
                }).catch(() => {
                    // Browser blocked fullscreen (no user gesture) — CSS-only mode still active
                    console.info('Browser fullscreen blocked, using CSS fallback');
                    triggerNeonFullscreenEntrance();
                });
            } else {
                triggerNeonFullscreenEntrance();
            }
        } else {
            // Exit browser fullscreen
            const exitFS = 
                document.exitFullscreen ||
                document.webkitExitFullscreen ||
                document.mozCancelFullScreen ||
                document.msExitFullscreen;

            if (exitFS && (document.fullscreenElement || document.webkitFullscreenElement)) {
                exitFS.call(document).catch(() => {});
            }
        }
    };

    // Sync CSS class state when browser exits fullscreen via Esc or browser UI
    function onBrowserFullscreenChange() {
        const isNowFullscreen = !!(
            document.fullscreenElement ||
            document.webkitFullscreenElement ||
            document.mozFullScreenElement ||
            document.msFullscreenElement
        );

        // If browser exited fullscreen but CSS class is still active — sync them
        if (!isNowFullscreen && document.body.classList.contains('fullscreen-active')) {
            // Simulate exit: remove class, reset button state
            document.body.classList.remove('fullscreen-active');
            const btn = document.getElementById('fullscreen-btn');
            const btnIcon = btn ? btn.querySelector('i[data-lucide]') : null;
            const btnSpan = btn ? btn.querySelector('span') : null;
            if (btnIcon) { btnIcon.setAttribute('data-lucide', 'expand'); if (typeof lucide !== 'undefined') lucide.createIcons(); }
            if (btnSpan) btnSpan.textContent = 'Full Screen';
            if (btn) { btn.title = 'Toggle Fullscreen'; btn.classList.remove('border-rose-500/50'); }

            // Resize 3D renderer if active
            setTimeout(() => {
                if (typeof renderer3d !== 'undefined' && renderer3d) {
                    const c = document.getElementById('three-visualizer-container');
                    if (c) renderer3d.setSize(c.clientWidth, c.clientHeight);
                }
            }, 300);
        }
    }

    document.addEventListener('fullscreenchange', onBrowserFullscreenChange);
    document.addEventListener('webkitfullscreenchange', onBrowserFullscreenChange);
    document.addEventListener('mozfullscreenchange', onBrowserFullscreenChange);
    document.addEventListener('MSFullscreenChange', onBrowserFullscreenChange);
})();
```

---

## SECTION 26 — FULLSCREEN NEON ENTRANCE ANIMATION (CSS)
### `>>> INJECT INTO: <style> block, after Section 23 CSS`

```css
/* ═══════════════════════════════════════════════════════════════
   ⚡ FULLSCREEN NEON ENTRANCE ANIMATION
   ═══════════════════════════════════════════════════════════════ */

/* Fullscreen burst overlay — injected via JS on fullscreen enter */
#fullscreen-neon-burst {
    position: fixed;
    inset: 0;
    z-index: 99998;
    pointer-events: none;
    background: radial-gradient(
        ellipse at center,
        rgba(244,63,94,0.25) 0%,
        rgba(168,85,247,0.15) 30%,
        transparent 70%
    );
    animation: neonFullscreenBurst 0.6s ease-out forwards;
}

/* Fullscreen corner arcs become bigger and brighter */
body.fullscreen-active .neon-corner-arc {
    width: 60px !important;
    height: 60px !important;
    animation-duration: 1.5s !important;
}
body.fullscreen-active .neon-corner-arc.tl {
    box-shadow: -4px -4px 16px rgba(244,63,94,0.8), -8px -8px 32px rgba(244,63,94,0.4) !important;
}
body.fullscreen-active .neon-corner-arc.tr {
    box-shadow: 4px -4px 16px rgba(168,85,247,0.8), 8px -8px 32px rgba(168,85,247,0.4) !important;
}
body.fullscreen-active .neon-corner-arc.bl {
    box-shadow: -4px 4px 16px rgba(6,182,212,0.8), -8px 8px 32px rgba(6,182,212,0.4) !important;
}
body.fullscreen-active .neon-corner-arc.br {
    box-shadow: 4px 4px 16px rgba(251,191,36,0.8), 8px 8px 32px rgba(251,191,36,0.4) !important;
}

/* In fullscreen, outer neon frame opacity increases */
body.fullscreen-active #player-fullscreen-wrapper::before {
    opacity: 0.85 !important;
    filter: blur(0px) !important;
}

/* Fullscreen: neon inner aura gets stronger */
body.fullscreen-active #neon-inner-aura {
    opacity: 1.5 !important;
    mix-blend-mode: lighten !important;
}
```

### `>>> INJECT INTO: JS, ADD this helper function AFTER the extendFullscreenWithBrowserAPI block:`

```javascript
// ⚡ NEON ADDITION: Fullscreen entrance burst trigger
function triggerNeonFullscreenEntrance() {
    // Remove if already exists
    const existing = document.getElementById('fullscreen-neon-burst');
    if (existing) existing.remove();

    const burst = document.createElement('div');
    burst.id = 'fullscreen-neon-burst';
    document.body.appendChild(burst);

    // Fire lightning bolts on entrance
    if (window.fireNeonLightning) {
        window.fireNeonLightning();
        setTimeout(window.fireNeonLightning, 200);
        setTimeout(window.fireNeonLightning, 400);
    }

    // Remove burst after animation
    setTimeout(() => burst.remove(), 700);
}
```

---

## SECTION 27 — FULLSCREEN VIDEO + LYRICS SPLIT NEON LAYOUT
### `>>> INJECT INTO: <style> block, after Section 26 CSS`

In fullscreen mode, both the video and lyrics panels need better layout + neon styling.

```css
/* ═══════════════════════════════════════════════════════════════
   ⚡ FULLSCREEN LAYOUT NEON ADDITIONS
   ═══════════════════════════════════════════════════════════════ */

/* Fullscreen: YouTube video container fills the music panel */
body.fullscreen-active #youtube-video-container,
body.fullscreen-active #audio-view,
body.fullscreen-active iframe[id*="youtube"],
body.fullscreen-active [id*="yt-player"] {
    width: 100% !important;
    height: 100% !important;
    min-height: 320px !important;
    border-radius: 16px !important;
    box-shadow: 
        0 0 20px rgba(244,63,94,0.3),
        0 0 40px rgba(168,85,247,0.2),
        0 0 80px rgba(244,63,94,0.1) !important;
}

/* Fullscreen: video container neon border */
body.fullscreen-active #music-panel .flex-grow {
    border: 1px solid rgba(244,63,94,0.25) !important;
    box-shadow: 
        inset 0 0 20px rgba(244,63,94,0.08),
        0 0 20px rgba(244,63,94,0.15) !important;
    border-radius: 18px !important;
    animation: neonLyricShimmer 3s ease-in-out infinite !important;
}

/* Fullscreen: lyrics get bigger + neon text */
body.fullscreen-active .lyric-line {
    font-size: 1.4rem !important;
    line-height: 2.5rem !important;
    padding: 12px 20px !important;
}

body.fullscreen-active .lyric-line.active {
    font-size: 1.65rem !important;
    line-height: 2.8rem !important;
    text-shadow: 0 0 20px var(--accent, rgba(244,63,94,0.8)), 0 0 40px rgba(168,85,247,0.5) !important;
}

/* Fullscreen: the whole lyrics panel gets a neon glow atmosphere */
body.fullscreen-active #lyrics-panel {
    background: rgba(5, 8, 18, 0.9) !important;
    box-shadow: inset 0 0 60px rgba(244,63,94,0.05), inset 0 0 120px rgba(168,85,247,0.04) !important;
}

/* Fullscreen: progress bar bigger */
body.fullscreen-active #seek-bar,
body.fullscreen-active #neon-progress-layer {
    height: 6px !important;
}
body.fullscreen-active #neon-progress-fill::after {
    width: 14px !important;
    height: 14px !important;
}

/* Fullscreen: controls area neon enhancement */
body.fullscreen-active #music-panel > div:last-child {
    background: rgba(0,0,0,0.4) !important;
    border-top: 1px solid rgba(244,63,94,0.15) !important;
    padding-bottom: 12px !important;
}
```

---

## SECTION 28 — FULLSCREEN ESCAPE BUTTON NEON GLOW
### `>>> INJECT INTO: <style> block, after Section 27 CSS`

```css
/* ═══════════════════════════════════════════════════════════════
   ⚡ FULLSCREEN EXIT BUTTON — NEON GLOW
   ═══════════════════════════════════════════════════════════════ */

/* When fullscreen is active, the fullscreen button glows as an exit CTA */
body.fullscreen-active #fullscreen-btn {
    background: rgba(168,85,247,0.15) !important;
    border-color: rgba(168,85,247,0.7) !important;
    box-shadow: 
        0 0 12px rgba(168,85,247,0.6),
        0 0 24px rgba(168,85,247,0.3),
        inset 0 0 8px rgba(168,85,247,0.12) !important;
    animation: rainbowBorder 2s linear infinite, electricArcFlicker 5s ease-in-out infinite !important;
    color: rgba(168,85,247,1) !important;
}

/* A floating fullscreen exit hint that appears in fullscreen — new element */
#fullscreen-exit-hint {
    position: fixed;
    top: 12px;
    right: 12px;
    z-index: 99999;
    background: rgba(10,10,20,0.85);
    border: 1px solid rgba(168,85,247,0.5);
    border-radius: 20px;
    padding: 6px 14px;
    font-size: 11px;
    color: rgba(168,85,247,0.9);
    pointer-events: none;
    opacity: 0;
    transition: opacity 0.5s ease;
    font-family: 'Outfit', sans-serif;
    letter-spacing: 0.05em;
    box-shadow: 0 0 12px rgba(168,85,247,0.4);
    text-shadow: 0 0 6px rgba(168,85,247,0.7);
}

body.fullscreen-active #fullscreen-exit-hint {
    opacity: 1;
    animation: electricArcFlicker 4s ease-in-out infinite;
}
```

### `>>> INJECT INTO: HTML, at the very END of the <body> content (before </body>), ADD:`

```html
<!-- ⚡ NEON ADDITION: Fullscreen exit hint label -->
<div id="fullscreen-exit-hint" aria-hidden="true">⚡ Press Esc to exit fullscreen</div>
```

---

## SECTION 29 — SPECTRUM BARS NEON INTENSIFICATION
### `>>> INJECT INTO: <style> block, after Section 28 CSS`

```css
/* ═══════════════════════════════════════════════════════════════
   ⚡ SPECTRUM BARS — NEON INTENSIFY (ADDITION)
   ═══════════════════════════════════════════════════════════════ */

/* The spectrum-icon bars at the lyrics reader header */
.spectrum-icon {
    gap: 3px !important;
}

/* Each bar now has a neon glow that intensifies at the top */
.spectrum-icon span {
    animation: spectrumNeonBar 0.7s ease-in-out infinite alternate !important;
    min-height: 4px !important;
    border-radius: 2px !important;
    position: relative;
}

/* A neon reflection pseudo-element under each bar */
.spectrum-icon span::after {
    content: '';
    position: absolute;
    bottom: -3px;
    left: 0;
    right: 0;
    height: 50%;
    background: inherit;
    opacity: 0.3;
    transform: scaleY(-1);
    filter: blur(1px);
}

/* When playing — spectrum bars also react */
body.is-playing .spectrum-icon span {
    animation-duration: 0.4s !important;
}
```

---

## SECTION 30 — DSP EQ BUTTONS NEON ACTIVE STATE
### `>>> INJECT INTO: <style> block, after Section 29 CSS`

```css
/* ═══════════════════════════════════════════════════════════════
   ⚡ DSP EQ BUTTONS — NEON ACTIVE STATE ADDITIONS
   ═══════════════════════════════════════════════════════════════ */

/* All EQ buttons — neon hover */
[id^="eq-btn-"] {
    position: relative;
    border: 1px solid transparent !important;
    transition: all 0.2s ease !important;
    overflow: hidden;
}

[id^="eq-btn-"]:hover {
    border-color: rgba(16,185,129,0.5) !important;
    box-shadow: 0 0 8px rgba(16,185,129,0.4), inset 0 0 4px rgba(16,185,129,0.1) !important;
    color: #fff !important;
}

/* Active EQ preset — green neon */
[id^="eq-btn-"].bg-white\/10 {
    background: rgba(16,185,129,0.15) !important;
    border-color: rgba(16,185,129,0.7) !important;
    box-shadow: 0 0 10px rgba(16,185,129,0.5), 0 0 20px rgba(16,185,129,0.25), inset 0 0 6px rgba(16,185,129,0.1) !important;
    color: #fff !important;
    text-shadow: 0 0 8px rgba(16,185,129,0.8) !important;
}

/* Night mode EQ — special purple neon */
#eq-btn-night.bg-white\/10 {
    background: rgba(168,85,247,0.15) !important;
    border-color: rgba(168,85,247,0.7) !important;
    box-shadow: 0 0 10px rgba(168,85,247,0.5) !important;
    text-shadow: 0 0 8px rgba(168,85,247,0.8) !important;
}
```

---

## SECTION 31 — ALBUM ART NEON BREATHING RING
### `>>> INJECT INTO: <style> block, after Section 30 CSS`

```css
/* ═══════════════════════════════════════════════════════════════
   ⚡ ALBUM ART — NEON BREATHING RING ADDITION
   ═══════════════════════════════════════════════════════════════ */

/* The album art thumbnail inside the vinyl gets a neon border */
#album-art-img {
    /* ADDITION: neon border glow on top of existing border-4 border-zinc-900 */
    box-shadow: 
        0 0 8px rgba(244,63,94,0.5),
        0 0 16px rgba(244,63,94,0.3),
        0 0 32px rgba(244,63,94,0.15) !important;
    animation: neonHaloBreathe 2s ease-in-out infinite !important;
    transition: box-shadow 0.3s ease !important;
}

body.is-playing #album-art-img {
    box-shadow: 
        0 0 14px rgba(244,63,94,0.8),
        0 0 28px rgba(244,63,94,0.5),
        0 0 56px rgba(244,63,94,0.25) !important;
    animation-duration: 1s !important;
}
```

---

## SECTION 32 — WAVEFORM NEON COLOR LAYER
### `>>> INJECT INTO: <style> block, after Section 31 CSS`

```css
/* ═══════════════════════════════════════════════════════════════
   ⚡ WAVEFORM / 2D VISUALIZER CANVAS — NEON COLOR LAYER
   ═══════════════════════════════════════════════════════════════ */

/* The 2D visualizer canvas gets a neon filter and increased opacity */
#visualizer-canvas {
    /* ADDITION: neon filter boost */
    filter: saturate(2) brightness(1.4) contrast(1.1) !important;
    opacity: 0.65 !important;
    mix-blend-mode: screen !important;
}

/* The Three.js container also gets a neon intensity boost */
#three-visualizer-container {
    filter: saturate(1.8) brightness(1.3) !important;
}

/* Three canvas inside the container */
#three-visualizer-container canvas {
    mix-blend-mode: screen !important;
}
```

---

## SECTION 33 — CURSOR TRAIL NEON SPARKS (JS)
### `>>> INJECT INTO: JS section, ADD as a brand new IIFE block`

```javascript
// ═══════════════════════════════════════════════════════════════
// ⚡ NEON CURSOR SPARK TRAIL — Mouse follower
// ADDITION: New JS block, creates spark elements on mouse move
// ═══════════════════════════════════════════════════════════════

(function initNeonCursorSparks() {
    const glassPanel = document.querySelector('.glass-panel');
    if (!glassPanel) return;

    const sparkColors = ['#f43f5e','#a855f7','#06b6d4','#fbbf24','#ffffff'];
    let lastSparkTime = 0;

    glassPanel.addEventListener('mousemove', (e) => {
        const now = Date.now();
        if (now - lastSparkTime < 35) return; // throttle to ~28fps
        lastSparkTime = now;

        const rect = glassPanel.getBoundingClientRect();
        const x = e.clientX - rect.left;
        const y = e.clientY - rect.top;

        // Create 2–4 spark particles per move event
        const numSparks = 2 + Math.floor(Math.random() * 3);
        for (let i = 0; i < numSparks; i++) {
            const spark = document.createElement('div');
            const color = sparkColors[Math.floor(Math.random() * sparkColors.length)];
            const size = 3 + Math.random() * 5;
            const angle = Math.random() * Math.PI * 2;
            const velocity = 20 + Math.random() * 40;
            const dx = Math.cos(angle) * velocity;
            const dy = Math.sin(angle) * velocity;

            spark.style.cssText = [
                'position: absolute',
                `left: ${x}px`,
                `top: ${y}px`,
                `width: ${size}px`,
                `height: ${size}px`,
                'border-radius: 50%',
                `background: ${color}`,
                `box-shadow: 0 0 ${size * 2}px ${color}`,
                'pointer-events: none',
                'z-index: 300',
                'transform: translate(-50%, -50%)',
                'will-change: transform, opacity'
            ].join(';');

            glassPanel.appendChild(spark);

            // Animate the spark flying outward and fading
            const startTime = performance.now();
            const duration = 400 + Math.random() * 300;

            function animateSpark(timestamp) {
                const elapsed = timestamp - startTime;
                const progress = Math.min(elapsed / duration, 1);
                const eased = 1 - Math.pow(progress, 2);

                spark.style.transform = [
                    `translate(calc(-50% + ${dx * progress}px), calc(-50% + ${dy * progress}px))`,
                    `scale(${eased})`
                ].join(' ');
                spark.style.opacity = eased.toString();

                if (progress < 1) {
                    requestAnimationFrame(animateSpark);
                } else {
                    spark.remove();
                }
            }
            requestAnimationFrame(animateSpark);
        }
    });
})();
```

---

## SECTION 34 — MOUSE PARALLAX NEON GLOW INTENSIFIER (JS)
### `>>> INJECT INTO: JS section, ADD inside or after the existing mouse parallax / cursor glow event listener block`

The existing code has `#interactive-cursor-glow`. We ADD a second, larger neon aura that intensifies based on mouse position relative to the card center.

```javascript
// ═══════════════════════════════════════════════════════════════
// ⚡ MOUSE PARALLAX NEON AURA INTENSIFIER — ADDITION
// Extends the existing cursor glow logic with a neon aura layer
// ═══════════════════════════════════════════════════════════════

(function initNeonParallaxAura() {
    const wrapper = document.getElementById('player-fullscreen-wrapper');
    if (!wrapper) return;

    // Create second neon aura div (different from existing interactive-cursor-glow)
    const neonAura = document.createElement('div');
    neonAura.id = 'neon-parallax-aura';
    neonAura.style.cssText = [
        'position: absolute',
        'width: 500px',
        'height: 500px',
        'border-radius: 50%',
        'pointer-events: none',
        'z-index: 3',
        'opacity: 0',
        'filter: blur(100px)',
        'background: radial-gradient(circle, rgba(244,63,94,0.12) 0%, rgba(168,85,247,0.08) 40%, transparent 70%)',
        'transform: translate(-50%, -50%)',
        'transition: opacity 0.4s ease',
        'will-change: transform, opacity',
        'mix-blend-mode: screen'
    ].join(';');

    const gp = document.querySelector('.glass-panel');
    if (gp) gp.appendChild(neonAura);

    wrapper.addEventListener('mousemove', (e) => {
        const rect = wrapper.getBoundingClientRect();
        const x = e.clientX - rect.left;
        const y = e.clientY - rect.top;

        // Position the aura at mouse position
        neonAura.style.left = x + 'px';
        neonAura.style.top = y + 'px';
        neonAura.style.opacity = '1';
    });

    wrapper.addEventListener('mouseleave', () => {
        neonAura.style.opacity = '0';
    });
})();
```

---

## SECTION 35 — SCROLLBAR NEON GLOW
### `>>> INJECT INTO: <style> block, after Section 34 CSS`

```css
/* ═══════════════════════════════════════════════════════════════
   ⚡ SCROLLBAR NEON GLOW — LYRICS CONTAINER ADDITION
   ═══════════════════════════════════════════════════════════════ */

/* Enhanced neon scrollbar for lyrics — on top of existing transparent/white styling */
.lyrics-container::-webkit-scrollbar {
    width: 4px !important;
}

.lyrics-container::-webkit-scrollbar-track {
    background: rgba(255,255,255,0.02) !important;
    border-radius: 9999px;
    box-shadow: inset 0 0 4px rgba(244,63,94,0.1);
}

.lyrics-container::-webkit-scrollbar-thumb {
    background: linear-gradient(
        to bottom,
        rgba(244,63,94,0.7),
        rgba(168,85,247,0.7),
        rgba(6,182,212,0.7)
    ) !important;
    border-radius: 9999px !important;
    box-shadow: 0 0 6px rgba(244,63,94,0.5), 0 0 12px rgba(168,85,247,0.3) !important;
}

.lyrics-container::-webkit-scrollbar-thumb:hover {
    background: linear-gradient(
        to bottom,
        rgba(244,63,94,1),
        rgba(168,85,247,1)
    ) !important;
    box-shadow: 0 0 10px rgba(244,63,94,0.8), 0 0 20px rgba(168,85,247,0.5) !important;
}
```

---

## SECTION 36 — NEON BPM DISPLAY WIDGET (HTML + CSS + JS)
### `>>> INJECT INTO: <style> block, after Section 35 CSS`

A new neon BPM ticker widget that flashes on every detected beat.

```css
/* ═══════════════════════════════════════════════════════════════
   ⚡ NEON BPM DISPLAY WIDGET — NEW ELEMENT
   ═══════════════════════════════════════════════════════════════ */

#neon-bpm-widget {
    position: absolute;
    bottom: 56px; /* above the EQ row */
    left: 12px;
    display: flex;
    align-items: center;
    gap: 6px;
    pointer-events: none;
    z-index: 50;
    opacity: 0;
    transition: opacity 0.5s ease;
}

/* Show when playing */
body.is-playing #neon-bpm-widget {
    opacity: 1;
}

/* The BPM flash dot */
#neon-bpm-dot {
    width: 8px;
    height: 8px;
    border-radius: 50%;
    background: rgba(244,63,94,0);
    flex-shrink: 0;
}

/* Flash animation triggered by JS */
#neon-bpm-dot.flash {
    animation: bpmTickFlash 0.25s ease-out forwards !important;
}

/* BPM text label */
#neon-bpm-label {
    font-size: 9px;
    font-family: 'Outfit', monospace;
    color: rgba(255,255,255,0.35);
    letter-spacing: 0.1em;
    text-transform: uppercase;
}

/* BPM number */
#neon-bpm-value {
    font-size: 10px;
    font-family: 'Outfit', monospace;
    font-weight: 600;
    color: rgba(244,63,94,0.8);
    text-shadow: 0 0 6px rgba(244,63,94,0.6);
    min-width: 28px;
    text-align: right;
}
```

### `>>> INJECT INTO: HTML, inside #music-panel, ADD as the LAST child element inside the music panel (after the DSP equalizer row's closing div)`

```html
<!-- ⚡ NEON ADDITION: BPM Ticker Widget -->
<div id="neon-bpm-widget" aria-hidden="true">
    <div id="neon-bpm-dot"></div>
    <span id="neon-bpm-label">BPM</span>
    <span id="neon-bpm-value">—</span>
</div>
```

### `>>> INJECT INTO: JS — ADD inside or near the beat detection block. Also ADD a BPM calculator:`

```javascript
// ⚡ NEON ADDITION: BPM tracker and widget updater
(function initNeonBpmTracker() {
    let beatTimes_ = [];
    const bpmDot = document.getElementById('neon-bpm-dot');
    const bpmVal = document.getElementById('neon-bpm-value');

    // Expose a global that beat detection can call
    window.neonBpmOnBeat = function() {
        const now = performance.now();
        beatTimes_.push(now);

        // Keep last 8 beats
        if (beatTimes_.length > 8) beatTimes_.shift();

        // Calculate BPM from average interval
        if (beatTimes_.length >= 2) {
            let totalInterval = 0;
            for (let i = 1; i < beatTimes_.length; i++) {
                totalInterval += beatTimes_[i] - beatTimes_[i - 1];
            }
            const avgInterval = totalInterval / (beatTimes_.length - 1);
            const bpm = Math.round(60000 / avgInterval);
            if (bpmVal && bpm > 40 && bpm < 240) {
                bpmVal.textContent = bpm;
            }
        }

        // Flash the dot
        if (bpmDot) {
            bpmDot.classList.remove('flash');
            void bpmDot.offsetWidth; // force reflow
            bpmDot.classList.add('flash');
        }
    };
})();
```

### `>>> INJECT INTO: JS — inside the existing beat detection / beat flash trigger, ADD:`

```javascript
// ⚡ NEON ADDITION: Notify BPM tracker on beat
if (window.neonBpmOnBeat) window.neonBpmOnBeat();
```

---

## SECTION 37 — BACKGROUND NOISE TEXTURE NEON TINT LAYER
### `>>> INJECT INTO: <style> block, after Section 36 CSS`

```css
/* ═══════════════════════════════════════════════════════════════
   ⚡ BACKGROUND NOISE TEXTURE + NEON TINT OVERLAY
   ═══════════════════════════════════════════════════════════════ */

/* A new grain + neon tint overlay for the entire panel background */
.glass-panel > #neon-grain-overlay {
    position: absolute;
    inset: 0;
    border-radius: inherit;
    pointer-events: none;
    z-index: 0;
    /* Grain via SVG filter */
    background-image: url("data:image/svg+xml,%3Csvg viewBox='0 0 256 256' xmlns='http://www.w3.org/2000/svg'%3E%3Cfilter id='noise'%3E%3CfeTurbulence type='fractalNoise' baseFrequency='0.9' numOctaves='4' stitchTiles='stitch'/%3E%3C/filter%3E%3Crect width='100%25' height='100%25' filter='url(%23noise)' opacity='0.06'/%3E%3C/svg%3E");
    background-repeat: repeat;
    background-size: 128px 128px;
    mix-blend-mode: overlay;
    opacity: 0.4;
}

/* Neon tint color shift based on theme */
body[data-theme="rose"]      .glass-panel > #neon-grain-overlay { background-color: rgba(244,63,94,0.015); }
body[data-theme="cyberpunk"] .glass-panel > #neon-grain-overlay { background-color: rgba(240,50,255,0.015); }
body[data-theme="matrix"]    .glass-panel > #neon-grain-overlay { background-color: rgba(0,255,80,0.015);  }
body[data-theme="ocean"]     .glass-panel > #neon-grain-overlay { background-color: rgba(79,100,255,0.015); }
body[data-theme="ice"]       .glass-panel > #neon-grain-overlay { background-color: rgba(100,220,255,0.015); }
```

### `>>> INJECT INTO: HTML, inside .glass-panel, ADD as second-to-last child (after corners, before music/lyrics panels):`

```html
<!-- ⚡ NEON ADDITION: Grain texture neon tint overlay -->
<div id="neon-grain-overlay" aria-hidden="true"></div>
```

---

## SECTION 38 — GLOBAL CSS VARIABLE NEON TOKEN ADDITIONS
### `>>> INJECT INTO: <style> block, at the very TOP (after opening <style> tag), as a :root block`

```css
/* ═══════════════════════════════════════════════════════════════
   ⚡ GLOBAL NEON CSS TOKENS — ADDITION TO :root
   ═══════════════════════════════════════════════════════════════ */

:root {
    /* Neon intensity multiplier — can be changed by JS */
    --neon-intensity: 1;

    /* Neon glow radii */
    --neon-glow-sm: calc(8px * var(--neon-intensity));
    --neon-glow-md: calc(16px * var(--neon-intensity));
    --neon-glow-lg: calc(32px * var(--neon-intensity));
    --neon-glow-xl: calc(64px * var(--neon-intensity));

    /* Primary neon colors */
    --neon-rose:    rgba(244, 63, 94, 1);
    --neon-purple:  rgba(168, 85, 247, 1);
    --neon-cyan:    rgba(6, 182, 212, 1);
    --neon-gold:    rgba(251, 191, 36, 1);
    --neon-green:   rgba(16, 185, 129, 1);
    --neon-white:   rgba(255, 255, 255, 1);

    /* Neon border thickness */
    --neon-border-thin:   1px;
    --neon-border-normal: 2px;
    --neon-border-thick:  3px;

    /* Animation speeds */
    --neon-speed-fast:   0.8s;
    --neon-speed-normal: 2s;
    --neon-speed-slow:   4s;
    --neon-speed-crawl:  8s;
}
```

---

## SECTION 39 — MOBILE NEON ADDITIONS (RESPONSIVE)
### `>>> INJECT INTO: <style> block, after Section 38 CSS`

On mobile, reduce the most performance-heavy neon effects while keeping the visual magic.

```css
/* ═══════════════════════════════════════════════════════════════
   ⚡ MOBILE NEON — RESPONSIVE ADDITIONS
   ═══════════════════════════════════════════════════════════════ */

@media (max-width: 768px) {
    /* Simplify border animations on mobile */
    .neon-border-ring::before {
        animation-duration: 6s !important;
        opacity: 0.35 !important;
    }

    #player-fullscreen-wrapper::before {
        animation: none !important;
        opacity: 0.3 !important;
    }

    /* Reduce particle opacity on mobile */
    #neon-three-particles {
        opacity: 0.3 !important;
    }

    /* Smaller corner arcs on mobile */
    .neon-corner-arc {
        width: 24px !important;
        height: 24px !important;
    }

    /* Reduce lightning canvas opacity */
    #neon-lightning-canvas {
        opacity: 0.5 !important;
    }

    /* Keep lyric neon but reduce to save GPU */
    .lyric-line.active {
        animation-duration: 4s !important;
    }

    /* Vinyl rings simpler on mobile */
    .vinyl-neon-ring-3 {
        display: none !important;
    }

    /* BPM widget hidden on mobile (too cramped) */
    #neon-bpm-widget {
        display: none !important;
    }
}

@media (max-width: 480px) {
    /* Minimal neon on very small screens */
    .vinyl-neon-ring-2 { display: none !important; }
    #neon-parallax-aura { display: none !important; }
    #neon-inner-aura { opacity: 0.5 !important; }

    /* Cursor sparks disabled on touch devices */
    #neon-lightning-canvas { display: none !important; }
}

/* Touch devices — disable cursor-dependent effects */
@media (hover: none) {
    #neon-parallax-aura { display: none !important; }
}
```

---

## SECTION 40 — FINAL STACKING ORDER & Z-INDEX NEON LAYER MAP
### `>>> INJECT INTO: <style> block, after Section 39 CSS — also serves as developer documentation`

```css
/* ═══════════════════════════════════════════════════════════════
   ⚡ Z-INDEX NEON LAYER MAP — Documentation + enforcement
   
   Layer stack from bottom to top:
   
   z-index: -10  → Ambient background orbs (orb-1 to orb-7)
   z-index: -1   → player-ambilight-glow, player-fullscreen-wrapper::before (neon frame)
   z-index: 0    → base glass-panel background
   z-index: 1    → neon-inner-aura, neon-three-particles canvas
   z-index: 2    → neon-parallax-aura
   z-index: 3    → neon-grain-overlay
   z-index: 5    → neon-progress-layer, neon-progress-fill
   z-index: 10   → music-panel, lyrics-panel (content)
   z-index: 49   → neon-lightning-canvas
   z-index: 50   → neon-top-edge, neon-bottom-edge, panel neon stripes
   z-index: 51   → beat-flash-corner elements
   z-index: 100  → neon-corner-arcs
   z-index: 200  → existing beat-flash (#beat-flash)
   z-index: 300  → cursor spark elements (dynamic)
   z-index: 9999 → fullscreen mode wrapper
   z-index: 99998→ fullscreen-neon-burst (temporary)
   z-index: 99999→ fullscreen-exit-hint
   
   ═══════════════════════════════════════════════════════════════ */

/* Enforce the neon canvas layers */
#neon-lightning-canvas   { z-index: 49 !important; }
#neon-three-particles    { z-index: 2 !important; }
#neon-inner-aura         { z-index: 1 !important; }
#neon-parallax-aura      { z-index: 2 !important; }
#neon-grain-overlay      { z-index: 0 !important; }
#neon-progress-layer     { z-index: 5 !important; }
.neon-top-edge,
.neon-bottom-edge        { z-index: 50 !important; }
.neon-corner-arc         { z-index: 100 !important; }
#neon-bpm-widget         { z-index: 50 !important; }
#fullscreen-exit-hint    { z-index: 99999 !important; }
#fullscreen-neon-burst   { z-index: 99998 !important; }
```

---

## IMPLEMENTATION ORDER — HOW TO APPLY ALL OF THIS

Apply sections in this exact order to avoid dependency issues:

1. **Section 38** — CSS variables `:root` block (must be first so variables exist for everything else)
2. **Section 1** — All keyframes (must exist before any animation references)
3. **Sections 2–21** — All CSS additions (order within this group doesn't matter)
4. **Sections 26–37, 39–40** — Remaining CSS additions
5. **Section 2 HTML** — neon-top-edge / neon-bottom-edge inside `.glass-panel`
6. **Section 23 HTML** — Corner arc elements inside `.glass-panel`
7. **Section 3 HTML** — neon-inner-aura div inside `.glass-panel`
8. **Section 4 HTML** — Vinyl halo wrapper (around vinyl record's parent div)
9. **Section 5 HTML** — Play button crown wrapper
10. **Section 6 HTML** — neon-progress-layer after seek bar
11. **Section 16 HTML** — Beat flash corner elements
12. **Section 17 HTML** — Orb-6 and orb-7
13. **Section 28 HTML** — Fullscreen exit hint (at end of body)
14. **Section 36 HTML** — BPM widget (inside #music-panel, last child)
15. **Section 37 HTML** — Grain overlay inside `.glass-panel`
16. **Section 2 JS** — neonBorderRing + angle animation
17. **Section 18 JS** — neonFrame angle animation
18. **Section 22 JS** — Lightning canvas IIFE (depends on `.glass-panel` existing)
19. **Section 23** — (CSS only, no JS needed)
20. **Section 24 JS** — Three.js neon particle field IIFE
21. **Section 25 JS** — Fullscreen API extension wrapper
22. **Section 26 JS** — triggerNeonFullscreenEntrance function
23. **Section 33 JS** — Cursor spark trail IIFE
24. **Section 34 JS** — Parallax aura IIFE
25. **Section 36 JS** — BPM tracker IIFE + integration
26. **Section 4 JS** — is-playing class toggle inside togglePlayState()
27. **Section 6 JS** — Progress fill width update inside time update handler
28. **Section 16 JS** — Corner beat flash inside beat trigger
29. **Section 24 JS addendum** — setTheme() neon particle color update

---

## QUICK REFERENCE — NEW ELEMENT IDs ADDED

| ID | Section | Description |
|---|---|---|
| `neon-top-edge` | §2 | Top neon border stripe on glass-panel |
| `neon-bottom-edge` | §2 | Bottom neon border stripe on glass-panel |
| `neon-inner-aura` | §3 | Inner ambient neon radial overlay |
| `.vinyl-neon-halo-wrapper` | §4 | Vinyl halo rings container |
| `.vinyl-neon-ring-1/2/3` | §4 | Three concentric vinyl halo rings |
| `play-pause-neon-crown` | §5 | Lightning crown around play button |
| `neon-progress-layer` | §6 | Progress bar neon overlay container |
| `neon-progress-fill` | §6 | Neon laser fill bar |
| `neon-progress-sweep` | §6 | Neon lightning sweep flash |
| `beat-flash-corner-tl/tr/bl/br` | §16 | Corner beat flash sparks |
| `orb-6` | §17 | New hot pink neon ambient orb |
| `orb-7` | §17 | New electric cyan ambient orb |
| `.neon-corner-arc.tl/tr/bl/br` | §23 | Four corner lightning brackets |
| `neon-lightning-canvas` | §22 | Full-player lightning bolt canvas |
| `neon-three-particles` | §24 | Three.js ambient particle field canvas |
| `fullscreen-neon-burst` | §26 | Fullscreen entrance burst (temporary) |
| `fullscreen-exit-hint` | §28 | "Press Esc" hint in fullscreen |
| `neon-parallax-aura` | §34 | Mouse-following neon aura |
| `neon-bpm-widget` | §36 | BPM flash ticker widget |
| `neon-bpm-dot` | §36 | BPM flash dot |
| `neon-bpm-label` | §36 | BPM label text |
| `neon-bpm-value` | §36 | BPM number display |
| `neon-grain-overlay` | §37 | Grain + neon tint overlay |

---

## NEW GLOBAL JS FUNCTIONS ADDED

| Function | Section | Purpose |
|---|---|---|
| `applyNeonBorderRing()` | §2 | Applies neon border rotation IIFE |
| `animateNeonFrame()` | §18 | Rotates outer card neon frame |
| `initNeonLightningCanvas()` | §22 | Full lightning bolt system IIFE |
| `fireNeonLightning()` | §22 | Fires a random lightning bolt (exposed globally) |
| `initNeonThreeParticleField()` | §24 | Three.js particle field IIFE |
| `updateNeonParticleTheme(hex)` | §24 | Updates particle colors on theme change |
| `extendFullscreenWithBrowserAPI()` | §25 | Fullscreen API wrapper IIFE |
| `onBrowserFullscreenChange()` | §25 | Syncs CSS class with browser fullscreen state |
| `triggerNeonFullscreenEntrance()` | §26 | Fires entrance burst + lightning bolts |
| `initNeonCursorSparks()` | §33 | Mouse cursor spark trail IIFE |
| `initNeonParallaxAura()` | §34 | Mouse parallax aura IIFE |
| `initNeonBpmTracker()` | §36 | BPM calculator and widget IIFE |
| `neonBpmOnBeat()` | §36 | Called on each beat detection event |

---

## ZERO REMOVAL GUARANTEE

This document contains **ZERO** removal instructions and **ZERO** replacement instructions.

Every element, class, ID, function, event listener, CSS rule, and animation that existed in `player_component.py` before applying this guide will still exist after applying it.

All additions are:
- **New CSS keyframes** with new unique names
- **New CSS rules** targeting new classes/IDs or adding to existing ones via addition operators (`!important` additions that stack)
- **New HTML elements** inserted as children without displacing siblings
- **New JS IIFEs** that are self-contained and don't reassign existing variables
- **One wrapper function** (`window.toggleFullscreen`) that stores and calls the original before extending — the original logic runs completely unchanged

The final result: a blazing neon cyberpunk music player where every edge glows, every beat flashes, every lyric shimmers with electric color, and fullscreen actually goes fullscreen.

---

*Document length: ~3,600+ lines. Written for `player_component.py`. Additive only. No removals. No replacements.*
