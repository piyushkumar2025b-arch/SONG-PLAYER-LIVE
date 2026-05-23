import sys
sys.stdout.reconfigure(encoding='utf-8')

import os
file_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "player_component.py")

with open(file_path, "r", encoding="utf-8") as f:
    content = f.read()
    lines = content.splitlines(keepends=True)

print(f"Loaded {len(lines)} lines")

# ─────────────────────────────────────────────────────────────────
# SECTION 38 — Global CSS Variable Neon Token Additions
# INJECT: at the very top of <style> block (after opening <style> tag on line 56)
# ─────────────────────────────────────────────────────────────────

CSS_ROOT_TOKENS = """
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
"""

# ─────────────────────────────────────────────────────────────────
# SECTIONS 1-21, 26-32, 35, 37, 39, 40 — All CSS additions
# INJECT: AFTER the last existing @keyframes (scanline, around line 293)
# ─────────────────────────────────────────────────────────────────

CSS_NEON_ADDITIONS = """
        /* ═══════════════════════════════════════════════════════════════
           ⚡ NEON ADDITIONS — KEYFRAME LIBRARY v2.0
           Inject AFTER last existing @keyframes in <style> block
           ═══════════════════════════════════════════════════════════════ */

        @keyframes neonBorderRotate {
            0%   { background-position: 0% 50%; }
            50%  { background-position: 100% 50%; }
            100% { background-position: 0% 50%; }
        }

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

        @keyframes neonHaloBreathe {
            0%   { box-shadow: 0 0 8px 2px var(--accent, #f43f5e), 0 0 20px 4px rgba(244,63,94,0.3), 0 0 40px 8px rgba(244,63,94,0.1); }
            50%  { box-shadow: 0 0 16px 4px var(--accent, #f43f5e), 0 0 40px 10px rgba(244,63,94,0.5), 0 0 80px 20px rgba(244,63,94,0.2); }
            100% { box-shadow: 0 0 8px 2px var(--accent, #f43f5e), 0 0 20px 4px rgba(244,63,94,0.3), 0 0 40px 8px rgba(244,63,94,0.1); }
        }

        @keyframes lightningStreak {
            0%   { transform: translateX(-120%) skewX(-20deg); opacity: 0; }
            10%  { opacity: 1; }
            30%  { transform: translateX(120%) skewX(-20deg); opacity: 0.8; }
            100% { transform: translateX(120%) skewX(-20deg); opacity: 0; }
        }

        @keyframes neonTextShimmer {
            0%   { text-shadow: 0 0 10px #f43f5e, 0 0 20px #f43f5e, 0 0 40px rgba(244,63,94,0.5); color: #ffffff; }
            25%  { text-shadow: 0 0 10px #a855f7, 0 0 20px #a855f7, 0 0 40px rgba(168,85,247,0.5); color: #f5f0ff; }
            50%  { text-shadow: 0 0 10px #06b6d4, 0 0 20px #06b6d4, 0 0 40px rgba(6,182,212,0.5); color: #f0feff; }
            75%  { text-shadow: 0 0 10px #a855f7, 0 0 20px #a855f7, 0 0 40px rgba(168,85,247,0.5); color: #f5f0ff; }
            100% { text-shadow: 0 0 10px #f43f5e, 0 0 20px #f43f5e, 0 0 40px rgba(244,63,94,0.5); color: #ffffff; }
        }

        @keyframes conicNeonSweep {
            0%   { --conic-angle: 0deg; }
            100% { --conic-angle: 360deg; }
        }

        @keyframes neonDropIn {
            0%   { transform: translateY(-30px) scale(0.9); opacity: 0; filter: blur(10px); box-shadow: 0 0 0px transparent; }
            60%  { transform: translateY(4px) scale(1.02); opacity: 1; filter: blur(0px); box-shadow: 0 0 30px rgba(244,63,94,0.6); }
            100% { transform: translateY(0) scale(1); opacity: 1; box-shadow: 0 0 15px rgba(244,63,94,0.3); }
        }

        @keyframes neonScanCross {
            0%   { transform: scaleX(0); opacity: 0.8; }
            100% { transform: scaleX(1); opacity: 0; }
        }

        @keyframes neonRingExpand {
            0%   { transform: scale(0.85); opacity: 0.9; }
            100% { transform: scale(1.8); opacity: 0; }
        }

        @keyframes electricPulse {
            0%   { transform: scale(1); box-shadow: 0 0 0 0 rgba(244,63,94,0.7); }
            70%  { transform: scale(1.05); box-shadow: 0 0 0 10px rgba(244,63,94,0); }
            100% { transform: scale(1); box-shadow: 0 0 0 0 rgba(244,63,94,0); }
        }

        @keyframes neonWipeSweep {
            0%   { left: -60%; }
            100% { left: 120%; }
        }

        @keyframes cornerLightningPulse {
            0%, 100% { opacity: 0.7; filter: drop-shadow(0 0 4px #f43f5e) drop-shadow(0 0 8px #f43f5e); }
            50%       { opacity: 1;   filter: drop-shadow(0 0 8px #f43f5e) drop-shadow(0 0 20px #a855f7) drop-shadow(0 0 30px #06b6d4); }
        }

        @keyframes neonLyricShimmer {
            0%   { border-color: rgba(244,63,94,0.8); box-shadow: 0 0 12px rgba(244,63,94,0.5), inset 0 0 8px rgba(244,63,94,0.1); }
            33%  { border-color: rgba(168,85,247,0.8); box-shadow: 0 0 12px rgba(168,85,247,0.5), inset 0 0 8px rgba(168,85,247,0.1); }
            66%  { border-color: rgba(6,182,212,0.8);  box-shadow: 0 0 12px rgba(6,182,212,0.5),  inset 0 0 8px rgba(6,182,212,0.1);  }
            100% { border-color: rgba(244,63,94,0.8); box-shadow: 0 0 12px rgba(244,63,94,0.5), inset 0 0 8px rgba(244,63,94,0.1); }
        }

        @keyframes bpmTickFlash {
            0%   { background: rgba(244,63,94,0.8); box-shadow: 0 0 15px rgba(244,63,94,0.9), 0 0 30px rgba(244,63,94,0.4); }
            100% { background: rgba(244,63,94,0.0); box-shadow: 0 0 0px transparent; }
        }

        @keyframes neonFullscreenBurst {
            0%   { opacity: 1; transform: scale(1); }
            50%  { opacity: 0.7; transform: scale(1.05); box-shadow: 0 0 60px rgba(244,63,94,0.6), 0 0 120px rgba(168,85,247,0.4); }
            100% { opacity: 0; transform: scale(1.15); }
        }

        @keyframes lyricStripeFlow {
            0%   { background-position: 0% 0%; }
            100% { background-position: 0% 100%; }
        }

        @keyframes spectrumNeonBar {
            0%, 100% { box-shadow: 0 0 4px var(--accent, #f43f5e), 0 -2px 8px var(--accent, #f43f5e); }
            50%       { box-shadow: 0 0 8px var(--accent, #f43f5e), 0 -4px 16px var(--accent, #f43f5e), 0 -8px 24px rgba(168,85,247,0.4); }
        }

        @keyframes cursorSparkFade {
            0%   { transform: scale(1) translate(-50%, -50%); opacity: 1; }
            100% { transform: scale(0) translate(-50%, -50%); opacity: 0; }
        }

        @keyframes albumNeonHaloSpin {
            0%   { transform: rotate(0deg) scale(1); opacity: 0.6; }
            50%  { transform: rotate(180deg) scale(1.05); opacity: 1; }
            100% { transform: rotate(360deg) scale(1); opacity: 0.6; }
        }

        @keyframes neonPillActiveBounce {
            0%, 100% { transform: scale(1); }
            50%       { transform: scale(1.06); }
        }

        /* ═══════════════════════════════════════════════════════════════
           ⚡ NEON BORDER SYSTEM — All Panel Containers
           ═══════════════════════════════════════════════════════════════ */

        .glass-panel {
            isolation: isolate;
        }

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

        /* ═══════════════════════════════════════════════════════════════
           ⚡ GLASS PANEL NEON AURA — Inner ambient neon radial glow
           ═══════════════════════════════════════════════════════════════ */

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

        body[data-theme="rose"]      #neon-inner-aura { background-image: radial-gradient(ellipse 70% 50% at 30% 50%, rgba(244,63,94,0.06) 0%, transparent 70%); }
        body[data-theme="cyberpunk"] #neon-inner-aura { background-image: radial-gradient(ellipse 70% 50% at 30% 50%, rgba(240,50,255,0.07) 0%, transparent 70%); }
        body[data-theme="ocean"]     #neon-inner-aura { background-image: radial-gradient(ellipse 70% 50% at 30% 50%, rgba(79,100,255,0.06) 0%, transparent 70%); }
        body[data-theme="aurora"]    #neon-inner-aura { background-image: radial-gradient(ellipse 70% 50% at 30% 50%, rgba(16,185,129,0.06) 0%, transparent 70%); }
        body[data-theme="matrix"]    #neon-inner-aura { background-image: radial-gradient(ellipse 70% 50% at 30% 50%, rgba(0,255,80,0.06) 0%, transparent 70%); }
        body[data-theme="ice"]       #neon-inner-aura { background-image: radial-gradient(ellipse 70% 50% at 30% 50%, rgba(100,220,255,0.06) 0%, transparent 70%); }
        body[data-theme="lava"]      #neon-inner-aura { background-image: radial-gradient(ellipse 70% 50% at 30% 50%, rgba(255,120,0,0.07) 0%, transparent 70%); }

        /* ═══════════════════════════════════════════════════════════════
           ⚡ VINYL NEON HALO RINGS — 3 Concentric Breathing Rings
           ═══════════════════════════════════════════════════════════════ */

        .vinyl-neon-halo-wrapper {
            position: absolute;
            inset: -18px;
            border-radius: 50%;
            pointer-events: none;
            z-index: 1;
        }

        .vinyl-neon-ring-1 {
            position: absolute;
            inset: 0;
            border-radius: 50%;
            border: 1.5px solid rgba(244,63,94,0.7);
            box-shadow: 0 0 8px rgba(244,63,94,0.5), 0 0 20px rgba(244,63,94,0.2), inset 0 0 8px rgba(244,63,94,0.1);
            animation: neonHaloBreathe 1.8s ease-in-out infinite, albumNeonHaloSpin 8s linear infinite;
        }

        .vinyl-neon-ring-2 {
            position: absolute;
            inset: -10px;
            border-radius: 50%;
            border: 1px solid rgba(168,85,247,0.45);
            box-shadow: 0 0 12px rgba(168,85,247,0.35), 0 0 30px rgba(168,85,247,0.15);
            animation: neonHaloBreathe 2.6s ease-in-out infinite 0.4s, albumNeonHaloSpin 12s linear infinite reverse;
        }

        .vinyl-neon-ring-3 {
            position: absolute;
            inset: -22px;
            border-radius: 50%;
            border: 0.5px solid rgba(6,182,212,0.3);
            box-shadow: 0 0 16px rgba(6,182,212,0.25), 0 0 40px rgba(6,182,212,0.1);
            animation: neonHaloBreathe 3.4s ease-in-out infinite 0.8s, albumNeonHaloSpin 16s linear infinite;
        }

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

        /* ═══════════════════════════════════════════════════════════════
           ⚡ PLAY/PAUSE LIGHTNING CROWN
           ═══════════════════════════════════════════════════════════════ */

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

        /* ═══════════════════════════════════════════════════════════════
           ⚡ PROGRESS BAR NEON LASER TRAIL
           ═══════════════════════════════════════════════════════════════ */

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

        /* ═══════════════════════════════════════════════════════════════
           ⚡ ACTIVE LYRIC LINE ELECTRIC ARC — ADDITIONS ONLY
           ═══════════════════════════════════════════════════════════════ */

        .lyric-line.active {
            animation: neonLyricShimmer 2s ease-in-out infinite !important;
            position: relative;
            overflow: hidden;
        }

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

        /* ═══════════════════════════════════════════════════════════════
           ⚡ LYRICS HEADER NEON ADDITIONS
           ═══════════════════════════════════════════════════════════════ */

        .lyrics-header-glow {
            animation: neonTextShimmer 4s ease-in-out infinite !important;
            letter-spacing: 0.12em !important;
        }

        #lyrics-panel .border-b.border-white\\/5 {
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

        #lyrics-panel .border-b.border-white\\/5::after {
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

        /* ═══════════════════════════════════════════════════════════════
           ⚡ CONTROL BUTTONS NEON HOVER SPARKS
           ═══════════════════════════════════════════════════════════════ */

        #music-panel button:not(#play-pause-btn) {
            position: relative;
            overflow: hidden;
            transition: color 0.2s ease, filter 0.2s ease, transform 0.15s ease !important;
        }

        #music-panel button:not(#play-pause-btn):hover {
            filter: drop-shadow(0 0 6px var(--accent, #f43f5e)) drop-shadow(0 0 12px rgba(168,85,247,0.5)) !important;
            transform: scale(1.12) !important;
        }

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

        button[title="Previous Song"]:hover,
        button[title="Next Song"]:hover {
            color: var(--accent, #f43f5e) !important;
            filter: drop-shadow(0 0 8px var(--accent, #f43f5e)) !important;
        }

        #shuffle-btn.active {
            color: var(--accent, #f43f5e) !important;
            filter: drop-shadow(0 0 6px var(--accent, #f43f5e)) drop-shadow(0 0 15px rgba(168,85,247,0.4)) !important;
            animation: electricPulse 2s ease infinite !important;
        }

        #repeat-btn.active,
        #repeat-btn[data-state="one"],
        #repeat-btn[data-state="all"] {
            color: var(--accent, #f43f5e) !important;
            filter: drop-shadow(0 0 6px var(--accent, #f43f5e)) !important;
        }

        /* ═══════════════════════════════════════════════════════════════
           ⚡ VISUALIZER PILL BUTTONS — NEON OUTLINE ADDITIONS
           ═══════════════════════════════════════════════════════════════ */

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

        [id^="viz-btn-"].bg-white\\/10 {
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

        [id^="viz-btn-"].bg-white\\/10::before {
            content: '';
            position: absolute;
            inset: 0;
            background: linear-gradient(to right, transparent, rgba(255,255,255,0.1), transparent);
            animation: lightningStreak 3s ease-in-out infinite;
            border-radius: inherit;
            pointer-events: none;
        }

        /* ═══════════════════════════════════════════════════════════════
           ⚡ THEME DOT BUTTONS — NEON PULSE RINGS
           ═══════════════════════════════════════════════════════════════ */

        [id^="theme-btn-"] {
            position: relative;
            transition: transform 0.2s ease, box-shadow 0.2s ease, opacity 0.2s ease !important;
        }

        [id^="theme-btn-"]:hover {
            transform: scale(1.4) !important;
            opacity: 1 !important;
        }

        #theme-btn-rose:hover, #theme-btn-rose.ring-2 {
            box-shadow: 0 0 0 2px rgba(244,63,94,0.3), 0 0 8px rgba(244,63,94,0.6), 0 0 16px rgba(244,63,94,0.3) !important;
            animation: electricPulse 1.5s ease infinite !important;
        }
        #theme-btn-aurora:hover, #theme-btn-aurora.ring-2 {
            box-shadow: 0 0 0 2px rgba(16,185,129,0.3), 0 0 8px rgba(16,185,129,0.6), 0 0 16px rgba(16,185,129,0.3) !important;
            animation: electricPulse 1.5s ease infinite !important;
        }
        #theme-btn-cyberpunk:hover, #theme-btn-cyberpunk.ring-2 {
            box-shadow: 0 0 0 2px rgba(240,50,255,0.3), 0 0 8px rgba(240,50,255,0.6), 0 0 16px rgba(240,50,255,0.3) !important;
            animation: electricPulse 1.5s ease infinite !important;
        }
        #theme-btn-ocean:hover, #theme-btn-ocean.ring-2 {
            box-shadow: 0 0 0 2px rgba(79,100,255,0.3), 0 0 8px rgba(79,100,255,0.6), 0 0 16px rgba(79,100,255,0.3) !important;
            animation: electricPulse 1.5s ease infinite !important;
        }
        #theme-btn-matrix:hover, #theme-btn-matrix.ring-2 {
            box-shadow: 0 0 0 2px rgba(0,255,80,0.3), 0 0 8px rgba(0,255,80,0.6), 0 0 16px rgba(0,255,80,0.3) !important;
            animation: electricPulse 1.5s ease infinite !important;
        }
        #theme-btn-ice:hover, #theme-btn-ice.ring-2 {
            box-shadow: 0 0 0 2px rgba(100,220,255,0.3), 0 0 8px rgba(100,220,255,0.6), 0 0 16px rgba(100,220,255,0.3) !important;
            animation: electricPulse 1.5s ease infinite !important;
        }
        #theme-btn-lava:hover, #theme-btn-lava.ring-2 {
            box-shadow: 0 0 0 2px rgba(255,120,0,0.3), 0 0 8px rgba(255,120,0,0.6), 0 0 16px rgba(255,120,0,0.3) !important;
            animation: electricPulse 1.5s ease infinite !important;
        }
        #theme-btn-holo:hover, #theme-btn-holo.ring-2 {
            box-shadow: 0 0 0 2px rgba(168,85,247,0.3), 0 0 8px rgba(244,63,94,0.5), 0 0 16px rgba(6,182,212,0.3) !important;
            animation: electricPulse 1.5s ease infinite !important;
        }
        #theme-btn-amber:hover, #theme-btn-amber.ring-2 {
            box-shadow: 0 0 0 2px rgba(251,191,36,0.3), 0 0 8px rgba(251,191,36,0.6), 0 0 16px rgba(251,191,36,0.3) !important;
            animation: electricPulse 1.5s ease infinite !important;
        }

        /* ═══════════════════════════════════════════════════════════════
           ⚡ VOLUME SLIDER NEON GLOW — ADDITION
           ═══════════════════════════════════════════════════════════════ */

        #volume-slider {
            -webkit-appearance: none;
            appearance: none;
            background: transparent !important;
            position: relative;
        }

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

        /* ═══════════════════════════════════════════════════════════════
           ⚡ HEADER SECTION — NEON TICKER LINE ADDITION
           ═══════════════════════════════════════════════════════════════ */

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

        #music-panel .text-xs.uppercase.tracking-wider.text-white\\/50 {
            animation: neonTextShimmer 6s ease-in-out infinite !important;
            opacity: 0.9 !important;
        }

        #music-panel .animate-ping {
            background: var(--accent, #f43f5e) !important;
            box-shadow: 0 0 6px var(--accent, #f43f5e) !important;
        }

        /* ═══════════════════════════════════════════════════════════════
           ⚡ NOW PLAYING DOT — TRIPLE CONCENTRIC NEON RINGS
           ═══════════════════════════════════════════════════════════════ */

        #music-panel .flex.h-2.w-2.relative::before,
        #music-panel .flex.h-2.w-2.relative::after {
            content: '';
            position: absolute;
            border-radius: 50%;
            pointer-events: none;
        }

        #music-panel .flex.h-2.w-2.relative::before {
            inset: -4px;
            border: 1px solid rgba(244,63,94,0.4);
            box-shadow: 0 0 4px rgba(244,63,94,0.4);
            animation: neonRingExpand 2s ease-out infinite;
        }

        #music-panel .flex.h-2.w-2.relative::after {
            inset: -4px;
            border: 1px solid rgba(168,85,247,0.3);
            box-shadow: 0 0 4px rgba(168,85,247,0.3);
            animation: neonRingExpand 2s ease-out infinite 0.7s;
        }

        /* ═══════════════════════════════════════════════════════════════
           ⚡ BEAT FLASH — NEON MULTI-LAYER BURST ADDITION
           ═══════════════════════════════════════════════════════════════ */

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

        /* ═══════════════════════════════════════════════════════════════
           ⚡ AMBIENT ORBS — NEON INTENSITY BOOST + 2 NEW NEON ORBS
           ═══════════════════════════════════════════════════════════════ */

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

        /* ═══════════════════════════════════════════════════════════════
           ⚡ PLAYER CARD OUTER NEON FRAME
           ═══════════════════════════════════════════════════════════════ */

        #player-fullscreen-wrapper::before {
            content: '';
            position: absolute;
            inset: -2px;
            border-radius: 28px;
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

        /* ═══════════════════════════════════════════════════════════════
           ⚡ LYRICS PANEL RIGHT EDGE — NEON STRIPE
           ═══════════════════════════════════════════════════════════════ */

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

        /* ═══════════════════════════════════════════════════════════════
           ⚡ LYRICS HEADER PILL BUTTONS — NEON HOVER ADDITIONS
           ═══════════════════════════════════════════════════════════════ */

        #lyrics-search-btn:hover {
            border-color: rgba(251,191,36,0.7) !important;
            box-shadow: 0 0 10px rgba(251,191,36,0.5), 0 0 20px rgba(251,191,36,0.25), inset 0 0 6px rgba(251,191,36,0.1) !important;
            color: rgba(251,191,36,1) !important;
        }
        #lyrics-search-btn:hover i { filter: drop-shadow(0 0 4px rgba(251,191,36,0.9)); }

        #queue-drawer-btn:hover {
            border-color: rgba(6,182,212,0.7) !important;
            box-shadow: 0 0 10px rgba(6,182,212,0.5), 0 0 20px rgba(6,182,212,0.25), inset 0 0 6px rgba(6,182,212,0.1) !important;
            color: rgba(6,182,212,1) !important;
        }
        #queue-drawer-btn:hover i { filter: drop-shadow(0 0 4px rgba(6,182,212,0.9)); }

        #focus-toggle-btn:hover {
            border-color: rgba(244,63,94,0.7) !important;
            box-shadow: 0 0 10px rgba(244,63,94,0.5), 0 0 20px rgba(244,63,94,0.25), inset 0 0 6px rgba(244,63,94,0.1) !important;
        }

        #fullscreen-btn:hover {
            border-color: rgba(168,85,247,0.7) !important;
            box-shadow: 0 0 10px rgba(168,85,247,0.6), 0 0 24px rgba(168,85,247,0.3), inset 0 0 8px rgba(168,85,247,0.12) !important;
            color: rgba(168,85,247,1) !important;
        }
        #fullscreen-btn:hover i { filter: drop-shadow(0 0 6px rgba(168,85,247,1)); }

        #lyrics-search-btn, #queue-drawer-btn, #focus-toggle-btn, #fullscreen-btn {
            position: relative;
            overflow: hidden;
            transition: all 0.25s ease !important;
        }

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

        /* ═══════════════════════════════════════════════════════════════
           ⚡ SYNCED / PLAIN / GENIUS BADGE — NEON FLICKER
           ═══════════════════════════════════════════════════════════════ */

        #lyrics-type-badge {
            position: relative;
            animation: electricArcFlicker 4s ease-in-out infinite !important;
            box-shadow: 0 0 8px rgba(244,63,94,0.5), 0 0 16px rgba(244,63,94,0.25), inset 0 0 4px rgba(244,63,94,0.1) !important;
            text-shadow: 0 0 6px rgba(244,63,94,0.8) !important;
            letter-spacing: 0.08em !important;
        }

        #lyrics-type-badge::before {
            content: '';
            position: absolute;
            inset: 0;
            background: linear-gradient(90deg, transparent, rgba(255,255,255,0.2), transparent);
            border-radius: inherit;
            animation: lightningStreak 3s ease-in-out infinite;
            pointer-events: none;
        }

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

        .neon-corner-arc.tl {
            top: 8px;
            left: 8px;
            border-top: 2px solid rgba(244,63,94,0.9);
            border-left: 2px solid rgba(244,63,94,0.9);
            border-radius: 6px 0 0 0;
            box-shadow: -2px -2px 8px rgba(244,63,94,0.6), -4px -4px 16px rgba(244,63,94,0.3);
            animation-delay: 0s;
        }

        .neon-corner-arc.tr {
            top: 8px;
            right: 8px;
            border-top: 2px solid rgba(168,85,247,0.9);
            border-right: 2px solid rgba(168,85,247,0.9);
            border-radius: 0 6px 0 0;
            box-shadow: 2px -2px 8px rgba(168,85,247,0.6), 4px -4px 16px rgba(168,85,247,0.3);
            animation-delay: 0.5s;
        }

        .neon-corner-arc.bl {
            bottom: 8px;
            left: 8px;
            border-bottom: 2px solid rgba(6,182,212,0.9);
            border-left: 2px solid rgba(6,182,212,0.9);
            border-radius: 0 0 0 6px;
            box-shadow: -2px 2px 8px rgba(6,182,212,0.6), -4px 4px 16px rgba(6,182,212,0.3);
            animation-delay: 1s;
        }

        .neon-corner-arc.br {
            bottom: 8px;
            right: 8px;
            border-bottom: 2px solid rgba(251,191,36,0.8);
            border-right: 2px solid rgba(251,191,36,0.8);
            border-radius: 0 0 6px 0;
            box-shadow: 2px 2px 8px rgba(251,191,36,0.6), 4px 4px 16px rgba(251,191,36,0.3);
            animation-delay: 1.5s;
        }

        /* ═══════════════════════════════════════════════════════════════
           ⚡ FULLSCREEN NEON ENTRANCE ANIMATION
           ═══════════════════════════════════════════════════════════════ */

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

        body.fullscreen-active #player-fullscreen-wrapper::before {
            opacity: 0.85 !important;
            filter: blur(0px) !important;
        }

        body.fullscreen-active #neon-inner-aura {
            opacity: 1.5 !important;
            mix-blend-mode: lighten !important;
        }

        /* ═══════════════════════════════════════════════════════════════
           ⚡ FULLSCREEN LAYOUT NEON ADDITIONS
           ═══════════════════════════════════════════════════════════════ */

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

        body.fullscreen-active #music-panel .flex-grow {
            border: 1px solid rgba(244,63,94,0.25) !important;
            box-shadow:
                inset 0 0 20px rgba(244,63,94,0.08),
                0 0 20px rgba(244,63,94,0.15) !important;
            border-radius: 18px !important;
            animation: neonLyricShimmer 3s ease-in-out infinite !important;
        }

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

        body.fullscreen-active #lyrics-panel {
            background: rgba(5, 8, 18, 0.9) !important;
            box-shadow: inset 0 0 60px rgba(244,63,94,0.05), inset 0 0 120px rgba(168,85,247,0.04) !important;
        }

        body.fullscreen-active #seek-bar,
        body.fullscreen-active #neon-progress-layer {
            height: 6px !important;
        }
        body.fullscreen-active #neon-progress-fill::after {
            width: 14px !important;
            height: 14px !important;
        }

        body.fullscreen-active #music-panel > div:last-child {
            background: rgba(0,0,0,0.4) !important;
            border-top: 1px solid rgba(244,63,94,0.15) !important;
            padding-bottom: 12px !important;
        }

        /* ═══════════════════════════════════════════════════════════════
           ⚡ FULLSCREEN EXIT BUTTON — NEON GLOW
           ═══════════════════════════════════════════════════════════════ */

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

        /* ═══════════════════════════════════════════════════════════════
           ⚡ SPECTRUM BARS — NEON INTENSIFY (ADDITION)
           ═══════════════════════════════════════════════════════════════ */

        .spectrum-icon {
            gap: 3px !important;
        }

        .spectrum-icon span {
            animation: spectrumNeonBar 0.7s ease-in-out infinite alternate !important;
            min-height: 4px !important;
            border-radius: 2px !important;
            position: relative;
        }

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

        body.is-playing .spectrum-icon span {
            animation-duration: 0.4s !important;
        }

        /* ═══════════════════════════════════════════════════════════════
           ⚡ DSP EQ BUTTONS — NEON ACTIVE STATE ADDITIONS
           ═══════════════════════════════════════════════════════════════ */

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

        [id^="eq-btn-"].bg-white\\/10 {
            background: rgba(16,185,129,0.15) !important;
            border-color: rgba(16,185,129,0.7) !important;
            box-shadow: 0 0 10px rgba(16,185,129,0.5), 0 0 20px rgba(16,185,129,0.25), inset 0 0 6px rgba(16,185,129,0.1) !important;
            color: #fff !important;
            text-shadow: 0 0 8px rgba(16,185,129,0.8) !important;
        }

        #eq-btn-night.bg-white\\/10 {
            background: rgba(168,85,247,0.15) !important;
            border-color: rgba(168,85,247,0.7) !important;
            box-shadow: 0 0 10px rgba(168,85,247,0.5) !important;
            text-shadow: 0 0 8px rgba(168,85,247,0.8) !important;
        }

        /* ═══════════════════════════════════════════════════════════════
           ⚡ ALBUM ART — NEON BREATHING RING ADDITION
           ═══════════════════════════════════════════════════════════════ */

        #album-art-img {
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

        /* ═══════════════════════════════════════════════════════════════
           ⚡ WAVEFORM / 2D VISUALIZER CANVAS — NEON COLOR LAYER
           ═══════════════════════════════════════════════════════════════ */

        #visualizer-canvas {
            filter: saturate(2) brightness(1.4) contrast(1.1) !important;
            opacity: 0.65 !important;
            mix-blend-mode: screen !important;
        }

        #three-visualizer-container {
            filter: saturate(1.8) brightness(1.3) !important;
        }

        #three-visualizer-container canvas {
            mix-blend-mode: screen !important;
        }

        /* ═══════════════════════════════════════════════════════════════
           ⚡ SCROLLBAR NEON GLOW — LYRICS CONTAINER ADDITION
           ═══════════════════════════════════════════════════════════════ */

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

        /* ═══════════════════════════════════════════════════════════════
           ⚡ NEON BPM DISPLAY WIDGET — NEW ELEMENT
           ═══════════════════════════════════════════════════════════════ */

        #neon-bpm-widget {
            position: absolute;
            bottom: 56px;
            left: 12px;
            display: flex;
            align-items: center;
            gap: 6px;
            pointer-events: none;
            z-index: 50;
            opacity: 0;
            transition: opacity 0.5s ease;
        }

        body.is-playing #neon-bpm-widget {
            opacity: 1;
        }

        #neon-bpm-dot {
            width: 8px;
            height: 8px;
            border-radius: 50%;
            background: rgba(244,63,94,0);
            flex-shrink: 0;
        }

        #neon-bpm-dot.flash {
            animation: bpmTickFlash 0.25s ease-out forwards !important;
        }

        #neon-bpm-label {
            font-size: 9px;
            font-family: 'Outfit', monospace;
            color: rgba(255,255,255,0.35);
            letter-spacing: 0.1em;
            text-transform: uppercase;
        }

        #neon-bpm-value {
            font-size: 10px;
            font-family: 'Outfit', monospace;
            font-weight: 600;
            color: rgba(244,63,94,0.8);
            text-shadow: 0 0 6px rgba(244,63,94,0.6);
            min-width: 28px;
            text-align: right;
        }

        /* ═══════════════════════════════════════════════════════════════
           ⚡ BACKGROUND NOISE TEXTURE + NEON TINT OVERLAY
           ═══════════════════════════════════════════════════════════════ */

        .glass-panel > #neon-grain-overlay {
            position: absolute;
            inset: 0;
            border-radius: inherit;
            pointer-events: none;
            z-index: 0;
            background-image: url("data:image/svg+xml,%3Csvg viewBox='0 0 256 256' xmlns='http://www.w3.org/2000/svg'%3E%3Cfilter id='noise'%3E%3CfeTurbulence type='fractalNoise' baseFrequency='0.9' numOctaves='4' stitchTiles='stitch'/%3E%3C/filter%3E%3Crect width='100%25' height='100%25' filter='url(%23noise)' opacity='0.06'/%3E%3C/svg%3E");
            background-repeat: repeat;
            background-size: 128px 128px;
            mix-blend-mode: overlay;
            opacity: 0.4;
        }

        body[data-theme="rose"]      .glass-panel > #neon-grain-overlay { background-color: rgba(244,63,94,0.015); }
        body[data-theme="cyberpunk"] .glass-panel > #neon-grain-overlay { background-color: rgba(240,50,255,0.015); }
        body[data-theme="matrix"]    .glass-panel > #neon-grain-overlay { background-color: rgba(0,255,80,0.015);  }
        body[data-theme="ocean"]     .glass-panel > #neon-grain-overlay { background-color: rgba(79,100,255,0.015); }
        body[data-theme="ice"]       .glass-panel > #neon-grain-overlay { background-color: rgba(100,220,255,0.015); }

        /* ═══════════════════════════════════════════════════════════════
           ⚡ MOBILE NEON — RESPONSIVE ADDITIONS
           ═══════════════════════════════════════════════════════════════ */

        @media (max-width: 768px) {
            .neon-border-ring::before {
                animation-duration: 6s !important;
                opacity: 0.35 !important;
            }

            #player-fullscreen-wrapper::before {
                animation: none !important;
                opacity: 0.3 !important;
            }

            #neon-three-particles {
                opacity: 0.3 !important;
            }

            .neon-corner-arc {
                width: 24px !important;
                height: 24px !important;
            }

            #neon-lightning-canvas {
                opacity: 0.5 !important;
            }

            .lyric-line.active {
                animation-duration: 4s !important;
            }

            .vinyl-neon-ring-3 {
                display: none !important;
            }

            #neon-bpm-widget {
                display: none !important;
            }
        }

        @media (max-width: 480px) {
            .vinyl-neon-ring-2 { display: none !important; }
            #neon-parallax-aura { display: none !important; }
            #neon-inner-aura { opacity: 0.5 !important; }
            #neon-lightning-canvas { display: none !important; }
        }

        @media (hover: none) {
            #neon-parallax-aura { display: none !important; }
        }

        /* ═══════════════════════════════════════════════════════════════
           ⚡ Z-INDEX NEON LAYER MAP — Documentation + enforcement
           ═══════════════════════════════════════════════════════════════ */

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
"""

# ─────────────────────────────────────────────────────────────────
# JS ADDITIONS — All JS blocks
# ─────────────────────────────────────────────────────────────────

JS_NEON_ADDITIONS = """
        // ═══════════════════════════════════════════════════════════════
        // ⚡ NEON ADDITIONS — All JS blocks injected together
        // ═══════════════════════════════════════════════════════════════

        // ⚡ NEON ADDITION: Apply rotating neon border class to main glass panel
        (function applyNeonBorderRing() {
            const gp = document.querySelector('.glass-panel');
            if (gp) {
                gp.classList.add('neon-border-ring');
                let angle = 0;
                setInterval(() => {
                    angle = (angle + 1) % 360;
                    gp.style.setProperty('--neon-border-angle', angle + 'deg');
                }, 16);
            }
        })();

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

        // ═══════════════════════════════════════════════════════════════
        // ⚡ NEON LIGHTNING CANVAS — Full bolt lightning system
        // ═══════════════════════════════════════════════════════════════
        (function initNeonLightningCanvas() {
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

            function drawLightningBolt(ctx, x1, y1, x2, y2, branches, depth, color) {
                if (depth === 0) return;
                const dx = x2 - x1;
                const dy = y2 - y1;
                const len = Math.sqrt(dx * dx + dy * dy);
                const midX = (x1 + x2) / 2 + (Math.random() - 0.5) * len * 0.35;
                const midY = (y1 + y2) / 2 + (Math.random() - 0.5) * len * 0.35;
                ctx.beginPath();
                ctx.moveTo(x1, y1);
                ctx.lineTo(midX, midY);
                ctx.strokeStyle = color;
                ctx.lineWidth = Math.max(0.5, depth * 0.6);
                ctx.shadowColor = color;
                ctx.shadowBlur = 8 + depth * 4;
                ctx.globalAlpha = 0.4 + depth * 0.12;
                ctx.stroke();
                ctx.beginPath();
                ctx.moveTo(midX, midY);
                ctx.lineTo(x2, y2);
                ctx.stroke();
                drawLightningBolt(ctx, x1, y1, midX, midY, branches, depth - 1, color);
                drawLightningBolt(ctx, midX, midY, x2, y2, branches, depth - 1, color);
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

            function fireLightningBolt() {
                ctx.clearRect(0, 0, W, H);
                const style = Math.random();
                const color = neonColors[Math.floor(Math.random() * neonColors.length)];
                if (style < 0.33) {
                    const y = Math.random() * H * 0.8 + H * 0.1;
                    drawLightningBolt(ctx, 0, y, W, y + (Math.random() - 0.5) * 80, 3, 6, color);
                } else if (style < 0.66) {
                    const fromTop = Math.random() > 0.5;
                    drawLightningBolt(ctx,
                        Math.random() * W * 0.3,
                        fromTop ? 0 : H,
                        W * 0.7 + Math.random() * W * 0.3,
                        fromTop ? H : 0,
                        4, 7, color
                    );
                } else {
                    const edge = Math.floor(Math.random() * 4);
                    let x1, y1, x2, y2;
                    if (edge === 0) { x1 = Math.random() * W; y1 = 0; x2 = x1 + (Math.random() - 0.5) * 200; y2 = 100 + Math.random() * 150; }
                    else if (edge === 1) { x1 = W; y1 = Math.random() * H; x2 = W - 100 - Math.random() * 150; y2 = y1 + (Math.random() - 0.5) * 200; }
                    else if (edge === 2) { x1 = Math.random() * W; y1 = H; x2 = x1 + (Math.random() - 0.5) * 200; y2 = H - 100 - Math.random() * 150; }
                    else { x1 = 0; y1 = Math.random() * H; x2 = 100 + Math.random() * 150; y2 = y1 + (Math.random() - 0.5) * 200; }
                    drawLightningBolt(ctx, x1, y1, x2, y2, 2, 5, color);
                }
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

            function scheduleLightning() {
                const delay = 2000 + Math.random() * 6000;
                setTimeout(() => {
                    fireLightningBolt();
                    scheduleLightning();
                }, delay);
            }
            scheduleLightning();
            window.fireNeonLightning = fireLightningBolt;
        })();

        // ═══════════════════════════════════════════════════════════════
        // ⚡ THREE.JS NEON AMBIENT PARTICLE FIELD
        // ═══════════════════════════════════════════════════════════════
        (function initNeonThreeParticleField() {
            if (typeof THREE === 'undefined') return;

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

            const neonRenderer_ = new THREE.WebGLRenderer({
                canvas: neonThreeCanvas,
                alpha: true,
                antialias: false
            });
            neonRenderer_.setPixelRatio(Math.min(window.devicePixelRatio, 1.5));
            neonRenderer_.setSize(glassPanel.clientWidth, glassPanel.clientHeight);
            neonRenderer_.setClearColor(0x000000, 0);

            const neonScene_ = new THREE.Scene();
            const neonCamera_ = new THREE.PerspectiveCamera(60, glassPanel.clientWidth / glassPanel.clientHeight, 0.1, 1000);
            neonCamera_.position.z = 5;

            const neonPalette_ = [
                new THREE.Color(0xf43f5e),
                new THREE.Color(0xa855f7),
                new THREE.Color(0x06b6d4),
                new THREE.Color(0xfbbf24),
                new THREE.Color(0xffffff)
            ];

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

            let neonFrame_ = 0;
            function animateNeonParticles() {
                requestAnimationFrame(animateNeonParticles);
                neonFrame_++;
                neonParticles_.rotation.y += 0.0008;
                neonParticles_.rotation.x += 0.0003;
                pMat_.size = 0.04 + Math.sin(neonFrame_ * 0.02) * 0.015;
                pMat_.opacity = 0.5 + Math.sin(neonFrame_ * 0.015) * 0.25;
                if (document.body.classList.contains('is-playing')) {
                    neonParticles_.rotation.y += 0.001;
                }
                neonRenderer_.render(neonScene_, neonCamera_);
            }
            animateNeonParticles();

            window.addEventListener('resize', () => {
                if (!glassPanel) return;
                neonRenderer_.setSize(glassPanel.clientWidth, glassPanel.clientHeight);
                neonCamera_.aspect = glassPanel.clientWidth / glassPanel.clientHeight;
                neonCamera_.updateProjectionMatrix();
            });

            window.updateNeonParticleTheme = function(hexColor) {
                if (!hexColor) return;
                const c = new THREE.Color(hexColor);
                for (let i = 0; i < particleCount_ / 3; i++) {
                    colors_[i * 3]     = c.r;
                    colors_[i * 3 + 1] = c.g;
                    colors_[i * 3 + 2] = c.b;
                }
                pGeo_.attributes.color.needsUpdate = true;
            };
        })();

        // ═══════════════════════════════════════════════════════════════
        // ⚡ TRUE BROWSER FULLSCREEN API — ADDITION WRAPPER
        // ═══════════════════════════════════════════════════════════════
        (function extendFullscreenWithBrowserAPI() {
            const _originalToggleFullscreen = window.toggleFullscreen;

            window.toggleFullscreen = function() {
                if (typeof _originalToggleFullscreen === 'function') {
                    _originalToggleFullscreen();
                }

                const wrapper = document.getElementById('player-fullscreen-wrapper');
                if (!wrapper) return;

                const goingFullscreen = document.body.classList.contains('fullscreen-active');

                if (goingFullscreen) {
                    const requestFS =
                        wrapper.requestFullscreen ||
                        wrapper.webkitRequestFullscreen ||
                        wrapper.mozRequestFullScreen ||
                        wrapper.msRequestFullscreen;

                    if (requestFS) {
                        requestFS.call(wrapper).then(() => {
                            triggerNeonFullscreenEntrance();
                        }).catch(() => {
                            console.info('Browser fullscreen blocked, using CSS fallback');
                            triggerNeonFullscreenEntrance();
                        });
                    } else {
                        triggerNeonFullscreenEntrance();
                    }
                } else {
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

            function onBrowserFullscreenChange() {
                const isNowFullscreen = !!(
                    document.fullscreenElement ||
                    document.webkitFullscreenElement ||
                    document.mozFullScreenElement ||
                    document.msFullscreenElement
                );

                if (!isNowFullscreen && document.body.classList.contains('fullscreen-active')) {
                    document.body.classList.remove('fullscreen-active');
                    const btn = document.getElementById('fullscreen-btn');
                    const btnIcon = btn ? btn.querySelector('i[data-lucide]') : null;
                    const btnSpan = btn ? btn.querySelector('span') : null;
                    if (btnIcon) { btnIcon.setAttribute('data-lucide', 'expand'); if (typeof lucide !== 'undefined') lucide.createIcons(); }
                    if (btnSpan) btnSpan.textContent = 'Full Screen';
                    if (btn) { btn.title = 'Toggle Fullscreen'; btn.classList.remove('border-rose-500/50'); }

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

        // ⚡ NEON ADDITION: Fullscreen entrance burst trigger
        function triggerNeonFullscreenEntrance() {
            const existing = document.getElementById('fullscreen-neon-burst');
            if (existing) existing.remove();
            const burst = document.createElement('div');
            burst.id = 'fullscreen-neon-burst';
            document.body.appendChild(burst);
            if (window.fireNeonLightning) {
                window.fireNeonLightning();
                setTimeout(window.fireNeonLightning, 200);
                setTimeout(window.fireNeonLightning, 400);
            }
            setTimeout(() => burst.remove(), 700);
        }

        // ═══════════════════════════════════════════════════════════════
        // ⚡ NEON CURSOR SPARK TRAIL — Mouse follower
        // ═══════════════════════════════════════════════════════════════
        (function initNeonCursorSparks() {
            const glassPanel = document.querySelector('.glass-panel');
            if (!glassPanel) return;

            const sparkColors = ['#f43f5e','#a855f7','#06b6d4','#fbbf24','#ffffff'];
            let lastSparkTime = 0;

            glassPanel.addEventListener('mousemove', (e) => {
                const now = Date.now();
                if (now - lastSparkTime < 35) return;
                lastSparkTime = now;

                const rect = glassPanel.getBoundingClientRect();
                const x = e.clientX - rect.left;
                const y = e.clientY - rect.top;

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

        // ═══════════════════════════════════════════════════════════════
        // ⚡ MOUSE PARALLAX NEON AURA INTENSIFIER — ADDITION
        // ═══════════════════════════════════════════════════════════════
        (function initNeonParallaxAura() {
            const wrapper = document.getElementById('player-fullscreen-wrapper');
            if (!wrapper) return;

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
                neonAura.style.left = x + 'px';
                neonAura.style.top = y + 'px';
                neonAura.style.opacity = '1';
            });

            wrapper.addEventListener('mouseleave', () => {
                neonAura.style.opacity = '0';
            });
        })();

        // ⚡ NEON ADDITION: BPM tracker and widget updater
        (function initNeonBpmTracker() {
            let beatTimes_ = [];
            const bpmDot = document.getElementById('neon-bpm-dot');
            const bpmVal = document.getElementById('neon-bpm-value');

            window.neonBpmOnBeat = function() {
                const now = performance.now();
                beatTimes_.push(now);
                if (beatTimes_.length > 8) beatTimes_.shift();

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

                if (bpmDot) {
                    bpmDot.classList.remove('flash');
                    void bpmDot.offsetWidth;
                    bpmDot.classList.add('flash');
                }
            };
        })();
"""

# ─────────────────────────────────────────────────────────────────
# Now apply all changes to the content
# ─────────────────────────────────────────────────────────────────

# 1) Inject :root CSS tokens right after the opening <style> tag (line 56)
STYLE_TAG = "        <style>"
# The <style> tag is at line 56. We inject :root tokens right after it.
content = content.replace(
    "    <style>\n        html, body {",
    "    <style>" + CSS_ROOT_TOKENS + "\n        html, body {"
)

# 2) Inject all neon CSS after the scanline @keyframes block (after line ~293)
# The scanline keyframe ends with its closing brace. We find the .scanline-overlay block
# and inject before it.
SCANLINE_OVERLAY_MARKER = "        .scanline-overlay {\n            position: fixed; inset: 0; pointer-events: none; z-index: 9998;"
content = content.replace(
    SCANLINE_OVERLAY_MARKER,
    CSS_NEON_ADDITIONS + "\n" + SCANLINE_OVERLAY_MARKER
)

# 3) HTML INJECTION — glass-panel top/bottom edge + corners + neon-inner-aura + beat flash corners + orb-6/7 + BPM widget + grain overlay + fullscreen-exit-hint
# 
# 3a) FIRST TWO child elements inside .glass-panel (before #beat-flash)
OLD_GLASS_PANEL_OPEN = '        <div class="glass-panel w-full h-full rounded-3xl overflow-hidden flex flex-col md:flex-row shadow-2xl relative">\n            \n            <!-- NEW: Beat flash overlay -->'
NEW_GLASS_PANEL_OPEN = '        <div class="glass-panel w-full h-full rounded-3xl overflow-hidden flex flex-col md:flex-row shadow-2xl relative">\n\n            <!-- ⚡ NEON ADDITION: Top & Bottom edge glow lines -->\n            <div class="neon-top-edge"></div>\n            <div class="neon-bottom-edge"></div>\n\n            <!-- ⚡ NEON ADDITION: Corner arc lightning decorators -->\n            <div class="neon-corner-arc tl" aria-hidden="true"></div>\n            <div class="neon-corner-arc tr" aria-hidden="true"></div>\n            <div class="neon-corner-arc bl" aria-hidden="true"></div>\n            <div class="neon-corner-arc br" aria-hidden="true"></div>\n\n            <!-- NEW: Beat flash overlay -->'
content = content.replace(OLD_GLASS_PANEL_OPEN, NEW_GLASS_PANEL_OPEN)

# 3b) Corner beat flash sparks after #beat-flash
OLD_BEAT_FLASH = '        <div id="beat-flash" class="absolute inset-0 rounded-3xl pointer-events-none z-50 opacity-0 transition-opacity duration-75" style="background: radial-gradient(ellipse at center, rgba(244,63,94,0.18) 0%, transparent 70%);"></div>\n\n        <!-- Interactive Parallax Cursor Glow Spot -->'
NEW_BEAT_FLASH = '        <div id="beat-flash" class="absolute inset-0 rounded-3xl pointer-events-none z-50 opacity-0 transition-opacity duration-75" style="background: radial-gradient(ellipse at center, rgba(244,63,94,0.18) 0%, transparent 70%);"></div>\n\n            <!-- ⚡ NEON ADDITION: Corner beat flash sparks -->\n            <div id="beat-flash-corner-tl" aria-hidden="true"></div>\n            <div id="beat-flash-corner-tr" aria-hidden="true"></div>\n            <div id="beat-flash-corner-bl" aria-hidden="true"></div>\n            <div id="beat-flash-corner-br" aria-hidden="true"></div>\n\n        <!-- Interactive Parallax Cursor Glow Spot -->'
content = content.replace(OLD_BEAT_FLASH, NEW_BEAT_FLASH)

# 3c) neon-inner-aura AFTER #interactive-cursor-glow
OLD_CURSOR_GLOW = '        <div id="interactive-cursor-glow" class="absolute w-[350px] h-[350px] rounded-full pointer-events-none -z-5 opacity-0 blur-[80px] transition-opacity duration-500" style="background: radial-gradient(circle, rgba(255,255,255,0.08) 0%, transparent 70%);"></div>'
NEW_CURSOR_GLOW = '        <div id="interactive-cursor-glow" class="absolute w-[350px] h-[350px] rounded-full pointer-events-none -z-5 opacity-0 blur-[80px] transition-opacity duration-500" style="background: radial-gradient(circle, rgba(255,255,255,0.08) 0%, transparent 70%);"></div>\n\n            <!-- ⚡ NEON ADDITION: Inner ambient neon aura overlay -->\n            <div id="neon-inner-aura"></div>\n\n            <!-- ⚡ NEON ADDITION: Grain texture neon tint overlay -->\n            <div id="neon-grain-overlay" aria-hidden="true"></div>'
content = content.replace(OLD_CURSOR_GLOW, NEW_CURSOR_GLOW)

# 3d) Vinyl neon halo rings — inside the .relative.group div that wraps vinyl-record
# The wrapper is: <div class="relative group vinyl-enter-active" style="transform:scale(0.85);">
OLD_VINYL_WRAPPER = '                    <div class="relative group vinyl-enter-active" style="transform:scale(0.85);">\n                        <!-- Vinyl Record Background Frame -->\n                        <div id="vinyl-record"'
NEW_VINYL_WRAPPER = '                    <div class="relative group vinyl-enter-active" style="transform:scale(0.85);">\n                        <!-- ⚡ NEON ADDITION: Vinyl neon halo rings -->\n                        <div class="vinyl-neon-halo-wrapper" aria-hidden="true">\n                            <div class="vinyl-neon-ring-1"></div>\n                            <div class="vinyl-neon-ring-2"></div>\n                            <div class="vinyl-neon-ring-3"></div>\n                        </div>\n\n                        <!-- Vinyl Record Background Frame -->\n                        <div id="vinyl-record"'
content = content.replace(OLD_VINYL_WRAPPER, NEW_VINYL_WRAPPER)

# 3e) Play/pause button lightning crown wrapper
OLD_PLAY_BTN = '                    <!-- Play/Pause -->\n                    <button id="play-pause-btn" onclick="togglePlayState()" class="w-12 h-12 rounded-full bg-rose-600 hover:bg-rose-500 text-white flex items-center justify-center shadow-lg shadow-rose-600/20 hover:scale-105 active:scale-95 transition-all">\n                        <i id="play-icon" data-lucide="play" class="w-5 h-5 fill-white"></i>\n                    </button>'
NEW_PLAY_BTN = '                    <!-- Play/Pause -->\n                    <!-- ⚡ NEON ADDITION: Lightning crown wrapper for play button -->\n                    <div class="relative flex items-center justify-center">\n                        <div id="play-pause-neon-crown" aria-hidden="true"></div>\n                        <button id="play-pause-btn" onclick="togglePlayState()" class="w-12 h-12 rounded-full bg-rose-600 hover:bg-rose-500 text-white flex items-center justify-center shadow-lg shadow-rose-600/20 hover:scale-105 active:scale-95 transition-all">\n                            <i id="play-icon" data-lucide="play" class="w-5 h-5 fill-white"></i>\n                        </button>\n                    </div>'
content = content.replace(OLD_PLAY_BTN, NEW_PLAY_BTN)

# 3f) Neon progress layer — AFTER the progress-bar input inside waveform container
OLD_PROGRESS_INPUT = '                    <input id="progress-bar" type="range" min="0" max="{duration_seconds}" value="0" oninput="onProgressSeek(this.value)" class="w-full h-1 relative z-10" style="margin-top:17px;background:transparent;">\n                </div>'
NEW_PROGRESS_INPUT = '                    <input id="progress-bar" type="range" min="0" max="{duration_seconds}" value="0" oninput="onProgressSeek(this.value)" class="w-full h-1 relative z-10" style="margin-top:17px;background:transparent;">\n                    <!-- ⚡ NEON ADDITION: Neon laser trail overlay for progress bar -->\n                    <div id="neon-progress-layer" aria-hidden="true">\n                        <div id="neon-progress-fill" style="width: 0%;"></div>\n                        <div id="neon-progress-sweep"></div>\n                    </div>\n                </div>'
content = content.replace(OLD_PROGRESS_INPUT, NEW_PROGRESS_INPUT)

# 3g) Orb-6 and Orb-7 after orb-5 inside the ambient orbs container
OLD_ORB5 = '        <div id="orb-5" class="absolute bottom-1/4 left-1/4 w-64 h-64 rounded-full bg-fuchsia-900/15 blur-[90px]"></div>\n    </div>'
NEW_ORB5 = '        <div id="orb-5" class="absolute bottom-1/4 left-1/4 w-64 h-64 rounded-full bg-fuchsia-900/15 blur-[90px]"></div>\n        <!-- ⚡ NEON ADDITION: Two new intense neon orbs -->\n        <div id="orb-6"></div>\n        <div id="orb-7"></div>\n    </div>'
content = content.replace(OLD_ORB5, NEW_ORB5)

# 3h) BPM widget — add as last child inside #music-panel, just before its closing </div>
# The music panel closes before </div> for lyrics panel. We'll add the BPM widget
# just inside the music-panel, right before the </div> that closes #music-panel
# We find the closing tag of music-panel by looking for the comment before lyrics-panel
OLD_MUSIC_PANEL_END = '        </div>\n        \n        <!-- Right Side: Lyrics Panel -->'
NEW_MUSIC_PANEL_END = '        </div>\n\n            <!-- ⚡ NEON ADDITION: BPM Ticker Widget -->\n            <div id="neon-bpm-widget" aria-hidden="true">\n                <div id="neon-bpm-dot"></div>\n                <span id="neon-bpm-label">BPM</span>\n                <span id="neon-bpm-value">—</span>\n            </div>\n        \n        <!-- Right Side: Lyrics Panel -->'
content = content.replace(OLD_MUSIC_PANEL_END, NEW_MUSIC_PANEL_END)

# 3i) Fullscreen exit hint — at the very end of body content (before </body> or before main script)
# We add it just before the closing </div> of body content at around line 807
OLD_BODY_MAIN_END = '</div>\n\n    <!-- YouTube API and Player scripts -->'
NEW_BODY_MAIN_END = '</div>\n\n    <!-- ⚡ NEON ADDITION: Fullscreen exit hint label -->\n    <div id="fullscreen-exit-hint" aria-hidden="true">⚡ Press Esc to exit fullscreen</div>\n\n    <!-- YouTube API and Player scripts -->'
content = content.replace(OLD_BODY_MAIN_END, NEW_BODY_MAIN_END, 1)  # Only replace first occurrence

# ─────────────────────────────────────────────────────────────────
# JS INJECTIONS into existing functions
# ─────────────────────────────────────────────────────────────────

# 4) Section 2 JS — After first lucide.createIcons() call in initApp
OLD_LUCIDE_FIRST = '        lucide.createIcons();\n        initApp._done = true;'
NEW_LUCIDE_FIRST = '''        lucide.createIcons();
        initApp._done = true;'''
# The initApp function starts at line 1033. We inject after the first lucide.createIcons() inside it.
# initApp() looks like: lucide.createIcons(); initApp._done = true;
# Based on the actual code, line 1037 is lucide.createIcons(), line 1034 is if (initApp._done) return;
# line 1035 is initApp._done = true;  Let's check exactly...
# From search: line 1037: lucide.createIcons(); line 1035: initApp._done = true;
# So the order is:
# 1034: if (initApp._done) return;
# 1035: initApp._done = true;
# ...
# 1037: lucide.createIcons();
# We inject after line 1037 lucide.createIcons()
# Find: initApp._done = true; then a bit later lucide.createIcons();
# Let's find that specific lucide.createIcons inside initApp
OLD_INIT_CREATEICONS = '        function initApp() {\n        if (initApp._done) return;\n        initApp._done = true;'
NEW_INIT_CREATEICONS = '        function initApp() {\n        if (initApp._done) return;\n        initApp._done = true;'
# Actually let's find around line 1037 with the unique context
OLD_NEON_INJECT_POINT = '            lucide.createIcons();\n            initWaveformCanvas();'
NEW_NEON_INJECT_POINT = '            lucide.createIcons();\n\n' + JS_NEON_ADDITIONS + '\n            initWaveformCanvas();'
content = content.replace(OLD_NEON_INJECT_POINT, NEW_NEON_INJECT_POINT)

# 5) Section 4 JS — inside togglePlayState() at the very end
# Find the closing brace of togglePlayState
OLD_TOGGLE_PLAY_END = '                startLyricsSync();\n            }\n        }\n        \n        function skipTime(seconds) {'
NEW_TOGGLE_PLAY_END = '                startLyricsSync();\n            }\n\n            // ⚡ NEON ADDITION: Sync body class with play state for neon halo intensity\n            document.body.classList.toggle(\'is-playing\', isPlaying);\n        }\n        \n        function skipTime(seconds) {'
content = content.replace(OLD_TOGGLE_PLAY_END, NEW_TOGGLE_PLAY_END)

# 6) Section 6 JS — updateProgressBar function — add neon fill update
OLD_UPDATE_PROGRESS = '        function updateProgressBar(time) {\n            const progress = document.getElementById(\'progress-bar\');\n            progress.value = time;\n            document.getElementById(\'time-current\').innerText = formatTime(time);\n            const dur = currentSongDuration || 1;\n            drawWaveformScrubber(Math.min(1, time / dur));\n        }'
NEW_UPDATE_PROGRESS = '        function updateProgressBar(time) {\n            const progress = document.getElementById(\'progress-bar\');\n            progress.value = time;\n            document.getElementById(\'time-current\').innerText = formatTime(time);\n            const dur = currentSongDuration || 1;\n            drawWaveformScrubber(Math.min(1, time / dur));\n\n            // ⚡ NEON ADDITION: Update neon laser trail fill width\n            (function updateNeonProgressFill() {\n                const neonFill = document.getElementById(\'neon-progress-fill\');\n                const sb = document.getElementById(\'progress-bar\');\n                if (neonFill && sb) {\n                    const pct = (parseFloat(sb.value) / parseFloat(sb.max || 100)) * 100;\n                    neonFill.style.width = pct + \'%\';\n                }\n            })();\n        }'
content = content.replace(OLD_UPDATE_PROGRESS, NEW_UPDATE_PROGRESS)

# 7) Section 16 JS — beat flash trigger — add corner flash + lightning + BPM
OLD_BEAT_FLASH_TRIGGER = '            const el = document.getElementById(\'beat-flash\');'
NEW_BEAT_FLASH_TRIGGER = '            const el = document.getElementById(\'beat-flash\');\n\n            // ⚡ NEON ADDITION: Corner beat flash sparks\n            (function triggerCornerBeatFlash() {\n                const corners = [\'tl\',\'tr\',\'bl\',\'br\'];\n                corners.forEach((c, i) => {\n                    const elc = document.getElementById(\'beat-flash-corner-\' + c);\n                    if (elc) {\n                        elc.style.opacity = (0.4 + Math.random() * 0.4).toString();\n                        setTimeout(() => { elc.style.opacity = \'0\'; }, 80 + i * 15);\n                    }\n                });\n            })();\n\n            // ⚡ NEON ADDITION: Fire lightning on strong beats\n            if (Math.random() > 0.7 && window.fireNeonLightning) {\n                window.fireNeonLightning();\n            }\n\n            // ⚡ NEON ADDITION: Notify BPM tracker on beat\n            if (window.neonBpmOnBeat) window.neonBpmOnBeat();'
content = content.replace(OLD_BEAT_FLASH_TRIGGER, NEW_BEAT_FLASH_TRIGGER)

# 8) Section 24 JS — setTheme function — add neon particle theme update at the end
OLD_SET_THEME_END = "            if (themeName === 'ice') document.body.classList.add('theme-ice');\n        }\n        \n        function setEqualizerPreset(preset) {"
NEW_SET_THEME_END = ("            if (themeName === 'ice') document.body.classList.add('theme-ice');\n\n"
    "            // ⚡ NEON ADDITION: Update Three.js particle field colors on theme change\n"
    "            if (window.updateNeonParticleTheme) {\n"
    "                const themeAccents = {\n"
    "                    rose: '#f43f5e', aurora: '#10b981', cyberpunk: '#d946ef',\n"
    "                    ocean: '#6366f1', amber: '#f59e0b', matrix: '#00ff50',\n"
    "                    ice: '#67e8f9', holo: '#a855f7', lava: '#f97316'\n"
    "                };\n"
    "                window.updateNeonParticleTheme(themeAccents[themeName] || '#f43f5e');\n"
    "            }\n"
    "        }\n        \n        function setEqualizerPreset(preset) {")
content = content.replace(OLD_SET_THEME_END, NEW_SET_THEME_END)

# Write the modified content back
with open(file_path, "w", encoding="utf-8") as f:
    f.write(content)

print("✅ All neon additions applied successfully!")
print(f"New file length: {len(content.splitlines())} lines")