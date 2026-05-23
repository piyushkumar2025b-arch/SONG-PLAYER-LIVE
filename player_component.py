import json
from typing import List, Dict, Any, Optional

def render_player_html(
    video_id: str,
    song_title: str,
    artist: str,
    thumbnail_url: str,
    duration_seconds: int,
    synced_lyrics: List[Dict[str, Any]],
    plain_lyrics: str = "",
    queue_json: str = "[]",
    current_index: int = 0
) -> str:
    """
    Generates a complete, beautiful HTML page containing the YouTube Iframe Player,
    Three.js 3D Audio Visualizers, and a synchronized lyrics reader with a playlist queue.
    """
    
    # Serialize synced lyrics for JS
    synced_lyrics_json = json.dumps(synced_lyrics)
    
    # Format duration for display
    def format_time(seconds):
        m, s = divmod(int(seconds), 60)
        return f"{m:02d}:{s:02d}"
        
    duration_str = format_time(duration_seconds)
    
    # Raw string to avoid f-string brace escaping AND invalid escape sequence warnings.
    # We will use .replace() for all key template variables.
    html_template = r"""<!DOCTYPE html>
<html lang="en" style="height:100%;overflow:hidden;">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <script src="https://cdn.tailwindcss.com"></script>
    <script>
        tailwind.config = {
            theme: {
                extend: {
                    fontFamily: {
                        sans: ['Outfit', 'sans-serif'],
                    },
                    colors: {
                        accent: '#f43f5e',
                    }
                }
            }
        }
    </script>
    <link href="https://fonts.googleapis.com/css2?family=Outfit:wght@300;400;500;600;700&display=swap" rel="stylesheet">
    <script src="https://unpkg.com/lucide@latest"></script>
    <!-- Include Three.js for 3D Visualizations -->
    <script src="https://cdnjs.cloudflare.com/ajax/libs/three.js/r128/three.min.js"></script>
    <style>
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

        html, body {
            height: 100%;
            width: 100%;
        }
        body {
            font-family: 'Outfit', sans-serif;
            background: transparent;
            margin: 0;
            padding: 0;
            overflow: hidden;
            color: #f3f4f6;
        }
        .glass-panel {
            background: rgba(10, 16, 30, 0.45);
            backdrop-filter: blur(24px);
            -webkit-backdrop-filter: blur(24px);
            border: 1px solid rgba(255, 255, 255, 0.08);
        }
        .glass-panel-sidebar {
            background: rgba(10, 15, 28, 0.85);
            backdrop-filter: blur(30px);
            -webkit-backdrop-filter: blur(30px);
            border-left: 1px solid rgba(255, 255, 255, 0.1);
        }
        .lyrics-container::-webkit-scrollbar {
            width: 6px;
        }
        .lyrics-container::-webkit-scrollbar-track {
            background: transparent;
        }
        .lyrics-container::-webkit-scrollbar-thumb {
            background: rgba(255, 255, 255, 0.12);
            border-radius: 9999px;
        }
        .lyrics-container::-webkit-scrollbar-thumb:hover {
            background: rgba(255, 255, 255, 0.25);
        }
        .lyrics-container {
            mask-image: linear-gradient(to bottom, transparent 0%, black 15%, black 85%, transparent 100%);
            -webkit-mask-image: linear-gradient(to bottom, transparent 0%, black 15%, black 85%, transparent 100%);
        }
        .lyric-line {
            transition: all 0.4s cubic-bezier(0.25, 0.8, 0.25, 1);
            transform-origin: center center;
            cursor: pointer;
            padding: 10px 18px;
            border-radius: 14px;
            margin: 6px 0;
            border: 1px solid transparent;
            display: inline-block;
            width: 100%;
            box-sizing: border-box;
            background: transparent;
        }
        .lyric-line:hover {
            color: rgba(255, 255, 255, 1) !important;
            transform: scale(1.02) !important;
            background: rgba(255, 255, 255, 0.02);
            border-color: rgba(255, 255, 255, 0.05);
        }
        .lyric-line.active {
            background: rgba(255, 255, 255, 0.06) !important;
            border: 1px solid rgba(255, 255, 255, 0.15) !important;
            backdrop-filter: blur(8px) !important;
            -webkit-backdrop-filter: blur(8px) !important;
            box-shadow: 0 8px 24px rgba(0, 0, 0, 0.25), 0 0 15px var(--active-glow, rgba(244, 63, 94, 0.2));
            transform: scale(1.04) !important;
        }
        @keyframes neonPulse {
            0% { color: #f43f5e; text-shadow: 0 0 15px rgba(244, 63, 94, 0.7), 0 0 30px rgba(244, 63, 94, 0.4); }
            33% { color: #a855f7; text-shadow: 0 0 15px rgba(168, 85, 247, 0.7), 0 0 30px rgba(168, 85, 247, 0.4); }
            66% { color: #06b6d4; text-shadow: 0 0 15px rgba(6, 182, 212, 0.7), 0 0 30px rgba(6, 182, 212, 0.4); }
            100% { color: #f43f5e; text-shadow: 0 0 15px rgba(244, 63, 94, 0.7), 0 0 30px rgba(244, 63, 94, 0.4); }
        }
        @keyframes cardEnter {
            from { opacity: 0; transform: translateY(20px) scale(0.98); }
            to { opacity: 1; transform: translateY(0) scale(1); }
        }
        .card-enter {
            animation: cardEnter 0.8s cubic-bezier(0.16, 1, 0.3, 1) forwards;
        }
        @keyframes vinylEnter {
            from { opacity: 0; transform: scale(0.6) rotate(-180deg); }
            to { opacity: 1; transform: scale(1) rotate(0deg); }
        }
        .vinyl-enter-active {
            animation: vinylEnter 1.2s cubic-bezier(0.34, 1.56, 0.64, 1) forwards;
        }
        /* Glitch lyric effect */
        @keyframes glitchShift {
            0%,100%{clip-path:inset(0 0 95% 0);transform:translate(-3px,0) skewX(-2deg);}
            10%{clip-path:inset(15% 0 70% 0);transform:translate(3px,0) skewX(2deg);}
            20%{clip-path:inset(50% 0 40% 0);transform:translate(-2px,0);}
            30%{clip-path:inset(80% 0 5% 0);transform:translate(2px,0) skewX(-1deg);}
            40%,60%{clip-path:inset(0 0 0 0);transform:translate(0,0);opacity:0;}
            50%{opacity:1;}
        }
        @keyframes glitchMain {
            0%,90%,100%{text-shadow:none;}
            91%{text-shadow:-3px 0 #f43f5e, 3px 0 #06b6d4;}
            93%{text-shadow:3px 0 #f43f5e, -3px 0 #a855f7;}
            95%{text-shadow:-2px 0 #06b6d4, 2px 0 #f43f5e;}
        }
        .lyric-glitch-active {
            animation: glitchMain 3s infinite;
            position: relative;
        }
        .lyric-glitch-active::before,
        .lyric-glitch-active::after {
            content: attr(data-text);
            position: absolute;
            left: 0; top: 0; right: 0;
            pointer-events: none;
            animation: glitchShift 3s infinite;
        }
        .lyric-glitch-active::after {
            animation-delay: 0.12s;
            color: #06b6d4;
        }
        /* Wave Pulse lyric effect */
        @keyframes wavePulse {
            0%,100%{transform:translateY(0) scale(1.05);}
            25%{transform:translateY(-4px) scale(1.08);}
            75%{transform:translateY(4px) scale(1.04);}
        }
        /* Gold Slide lyric effect */
        @keyframes goldSlide {
            0%{background-position:200% center;}
            100%{background-position:-200% center;}
        }
        .lyric-gold-active {
            background: linear-gradient(90deg,#fbbf24,#f59e0b,#fde68a,#f59e0b,#fbbf24);
            background-size: 200% auto;
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            background-clip: text;
            animation: goldSlide 2s linear infinite;
        }
        input[type="range"] {
            -webkit-appearance: none;
            appearance: none;
            background: transparent;
            cursor: pointer;
        }
        input[type="range"]::-webkit-slider-runnable-track {
            background: rgba(255, 255, 255, 0.15);
            height: 5px;
            border-radius: 9999px;
        }
        input[type="range"]::-webkit-slider-thumb {
            -webkit-appearance: none;
            appearance: none;
            margin-top: -5px;
            background-color: #f43f5e;
            height: 15px;
            width: 15px;
            border-radius: 50%;
            box-shadow: 0 0 10px rgba(244, 63, 94, 0.5);
            transition: transform 0.1s;
        }
        input[type="range"]::-webkit-slider-thumb:hover {
            transform: scale(1.2);
        }

        /* ── Switch to Video neon highlight (until clicked) ── */
        @keyframes switchToVideoGlow {
            0%   { box-shadow: 0 0 6px rgba(244,63,94,0.7), 0 0 14px rgba(244,63,94,0.4), inset 0 0 6px rgba(244,63,94,0.15); border-color: rgba(244,63,94,0.8); }
            25%  { box-shadow: 0 0 8px rgba(168,85,247,0.7), 0 0 18px rgba(168,85,247,0.4), inset 0 0 6px rgba(168,85,247,0.15); border-color: rgba(168,85,247,0.8); }
            50%  { box-shadow: 0 0 8px rgba(6,182,212,0.7),  0 0 18px rgba(6,182,212,0.4),  inset 0 0 6px rgba(6,182,212,0.15);  border-color: rgba(6,182,212,0.8); }
            75%  { box-shadow: 0 0 8px rgba(168,85,247,0.7), 0 0 18px rgba(168,85,247,0.4), inset 0 0 6px rgba(168,85,247,0.15); border-color: rgba(168,85,247,0.8); }
            100% { box-shadow: 0 0 6px rgba(244,63,94,0.7), 0 0 14px rgba(244,63,94,0.4), inset 0 0 6px rgba(244,63,94,0.15); border-color: rgba(244,63,94,0.8); }
        }
        @keyframes switchToVideoPulseText {
            0%,100% { color: rgba(255,255,255,0.95); text-shadow: 0 0 8px rgba(244,63,94,0.8); }
            33%     { color: #c4b5fd; text-shadow: 0 0 8px rgba(168,85,247,0.9); }
            66%     { color: #67e8f9; text-shadow: 0 0 8px rgba(6,182,212,0.9); }
        }
        #mode-toggle-btn.neon-cta {
            animation: switchToVideoGlow 2s ease-in-out infinite;
            background: rgba(244,63,94,0.08) !important;
            border-width: 1px;
        }
        #mode-toggle-btn.neon-cta span,
        #mode-toggle-btn.neon-cta i {
            animation: switchToVideoPulseText 2s ease-in-out infinite;
        }

        /* Neon border shimmer on panel hover */
        .glass-panel {
            transition: box-shadow 0.5s ease;
        }
        .glass-panel:hover {
            box-shadow: 0 0 0 1px rgba(244, 63, 94, 0.15), 0 0 40px rgba(244, 63, 94, 0.08), 0 30px 80px rgba(0,0,0,0.5);
        }

        /* Neon pill button glow on hover */
        .neon-pill {
            position: relative;
            overflow: hidden;
        }
        .neon-pill::after {
            content: '';
            position: absolute;
            inset: 0;
            border-radius: inherit;
            background: linear-gradient(135deg, rgba(244,63,94,0.15), rgba(168,85,247,0.15), rgba(6,182,212,0.15));
            opacity: 0;
            transition: opacity 0.3s;
        }
        .neon-pill:hover::after { opacity: 1; }

        /* Rainbow border sweep animation */
        @keyframes rainbowBorder {
            0%   { border-color: rgba(244,63,94,0.6); box-shadow: 0 0 12px rgba(244,63,94,0.4); }
            25%  { border-color: rgba(168,85,247,0.6); box-shadow: 0 0 12px rgba(168,85,247,0.4); }
            50%  { border-color: rgba(6,182,212,0.6); box-shadow: 0 0 12px rgba(6,182,212,0.4); }
            75%  { border-color: rgba(251,191,36,0.6); box-shadow: 0 0 12px rgba(251,191,36,0.4); }
            100% { border-color: rgba(244,63,94,0.6); box-shadow: 0 0 12px rgba(244,63,94,0.4); }
        }

        /* Neon scan line animation */
        @keyframes scanline {
            0%   { transform: translateY(-100%); opacity: 0.6; }
            100% { transform: translateY(100vh); opacity: 0; }
        }

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

        #lyrics-panel .border-b.border-white\/5 {
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

        [id^="viz-btn-"].bg-white\/10::before {
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

        #music-panel .text-xs.uppercase.tracking-wider.text-white\/50 {
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

        [id^="eq-btn-"].bg-white\/10 {
            background: rgba(16,185,129,0.15) !important;
            border-color: rgba(16,185,129,0.7) !important;
            box-shadow: 0 0 10px rgba(16,185,129,0.5), 0 0 20px rgba(16,185,129,0.25), inset 0 0 6px rgba(16,185,129,0.1) !important;
            color: #fff !important;
            text-shadow: 0 0 8px rgba(16,185,129,0.8) !important;
        }

        #eq-btn-night.bg-white\/10 {
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

        .scanline-overlay {
            position: fixed; inset: 0; pointer-events: none; z-index: 9998;
            overflow: hidden;
        }
        .scanline-overlay::after {
            content: '';
            position: absolute;
            left: 0; right: 0;
            height: 3px;
            background: linear-gradient(90deg, transparent, rgba(244,63,94,0.3), rgba(168,85,247,0.3), transparent);
            animation: scanline 6s linear infinite;
        }

        /* Fullscreen mode */
        #player-fullscreen-wrapper {
            transition: all 0.45s cubic-bezier(0.16, 1, 0.3, 1);
        }
        body.fullscreen-active {
            overflow: hidden;
        }
        body.fullscreen-active #player-fullscreen-wrapper {
            position: fixed !important;
            inset: 0 !important;
            z-index: 9999 !important;
            max-width: 100vw !important;
            width: 100vw !important;
            height: 100vh !important;
            padding: 0 !important;
            border-radius: 0 !important;
            display: flex;
            align-items: stretch;
        }
        body.fullscreen-active #player-fullscreen-wrapper .glass-panel {
            border-radius: 0 !important;
            height: 100vh !important;
        }
        body.fullscreen-active #player-fullscreen-wrapper .relative {
            height: 100vh !important;
            max-width: 100vw !important;
            width: 100vw !important;
        }
        body.fullscreen-active #music-panel {
            width: 42% !important;
        }
        body.fullscreen-active #lyrics-panel {
            width: 58% !important;
        }
        body.fullscreen-active #lyrics-scroll-pane {
            font-size: 1.35rem !important;
            line-height: 2.4rem !important;
        }
        #fullscreen-btn {
            transition: all 0.25s ease;
        }
        #fullscreen-btn:hover {
            animation: rainbowBorder 1.5s linear infinite;
            transform: scale(1.08);
        }
        body.fullscreen-active #fullscreen-btn {
            background: rgba(244,63,94,0.15) !important;
            border-color: rgba(244,63,94,0.5) !important;
            animation: rainbowBorder 2s linear infinite;
        }

        /* Neon corner brackets decoration */
        .neon-bracket-box {
            position: relative;
        }
        .neon-bracket-box::before, .neon-bracket-box::after {
            content: '';
            position: absolute;
            width: 14px; height: 14px;
            border-color: rgba(244,63,94,0.5);
            border-style: solid;
            pointer-events: none;
            transition: border-color 0.4s;
        }
        .neon-bracket-box::before {
            top: 4px; left: 4px;
            border-width: 2px 0 0 2px;
            border-top-left-radius: 4px;
        }
        .neon-bracket-box::after {
            bottom: 4px; right: 4px;
            border-width: 0 2px 2px 0;
            border-bottom-right-radius: 4px;
        }

        /* Spectrum bar animation for header icons */
        @keyframes spectrumBar {
            0%,100% { height: 6px; }
            50% { height: 14px; }
        }
        .spectrum-icon span {
            display: inline-block;
            width: 3px;
            background: var(--accent-color, #f43f5e);
            border-radius: 2px;
            animation: spectrumBar 0.8s ease-in-out infinite;
            vertical-align: bottom;
        }
        .spectrum-icon span:nth-child(2) { animation-delay: 0.15s; }
        .spectrum-icon span:nth-child(3) { animation-delay: 0.3s; }
        .spectrum-icon span:nth-child(4) { animation-delay: 0.1s; }

        /* Neon tooltip glow */
        .neon-tooltip {
            position: relative;
        }
        .neon-tooltip:hover::before {
            content: attr(data-tip);
            position: absolute;
            bottom: calc(100% + 8px);
            left: 50%;
            transform: translateX(-50%);
            background: rgba(10,16,30,0.95);
            border: 1px solid rgba(244,63,94,0.4);
            box-shadow: 0 0 10px rgba(244,63,94,0.3);
            color: #f9fafb;
            font-size: 10px;
            padding: 4px 10px;
            border-radius: 8px;
            white-space: nowrap;
            z-index: 9000;
            pointer-events: none;
        }

        /* Extra theme: Holographic */
        @keyframes holoPrism {
            0%   { filter: hue-rotate(0deg) brightness(1.1); }
            50%  { filter: hue-rotate(180deg) brightness(1.3); }
            100% { filter: hue-rotate(360deg) brightness(1.1); }
        }
        body.theme-holo .lyric-line.active {
            animation: holoPrism 3s linear infinite;
            background: linear-gradient(135deg, rgba(244,63,94,0.1), rgba(168,85,247,0.1), rgba(6,182,212,0.1)) !important;
        }

        /* Extra theme: Matrix Green */
        body.theme-matrix {
            --accent-color: #22c55e;
            --active-glow: rgba(34,197,94,0.35);
        }
        body.theme-matrix .lyric-line.active {
            border-color: rgba(34,197,94,0.4) !important;
            text-shadow: 0 0 12px rgba(34,197,94,0.8);
        }

        /* Extra theme: Ice Blue */
        body.theme-ice {
            --accent-color: #38bdf8;
            --active-glow: rgba(56,189,248,0.35);
        }

        /* Glow pulse ring on now-playing dot */
        @keyframes outerRingPulse {
            0%   { box-shadow: 0 0 0 0 rgba(244,63,94,0.5); }
            70%  { box-shadow: 0 0 0 8px rgba(244,63,94,0); }
            100% { box-shadow: 0 0 0 0 rgba(244,63,94,0); }
        }
        .now-playing-ring {
            animation: outerRingPulse 1.6s ease-out infinite;
        }

        /* Lyrics panel neon glow border when active line plays */
        #lyrics-panel.beat-glow {
            box-shadow: inset 0 0 30px rgba(244,63,94,0.07);
            transition: box-shadow 0.1s;
        }

        /* Floating particles canvas */
        #neon-particles-canvas {
            position: fixed;
            inset: 0;
            pointer-events: none;
            z-index: 0;
            opacity: 0.45;
        }

        /* Header title neon shimmer */
        @keyframes headerShimmer {
            0%   { text-shadow: 0 0 8px rgba(244,63,94,0.0); }
            50%  { text-shadow: 0 0 16px rgba(244,63,94,0.5), 0 0 32px rgba(168,85,247,0.3); }
            100% { text-shadow: 0 0 8px rgba(244,63,94,0.0); }
        }
        h3.lyrics-header-glow {
            animation: headerShimmer 3s ease-in-out infinite;
        }

        /* DSP bar neon active */
        .eq-active-neon {
            background: linear-gradient(90deg, rgba(244,63,94,0.3), rgba(168,85,247,0.3)) !important;
            border: 1px solid rgba(244,63,94,0.4) !important;
            box-shadow: 0 0 8px rgba(244,63,94,0.3);
        }
    </style>
</head>
<body class="h-full flex items-center justify-center p-0 select-none">
    
    <!-- Scanline neon overlay -->
    <div class="scanline-overlay" id="scanline-overlay"></div>

    <!-- Neon floating particles canvas -->
    <canvas id="neon-particles-canvas"></canvas>

    <!-- Ambient Glowing Background Orbs -->
    <div class="fixed inset-0 overflow-hidden pointer-events-none -z-10 bg-[#060810]">
        <div id="orb-1" class="absolute -top-40 -left-40 w-96 h-96 rounded-full bg-rose-900/30 blur-[120px]"></div>
        <div id="orb-2" class="absolute -bottom-40 -right-40 w-96 h-96 rounded-full bg-blue-900/20 blur-[120px]"></div>
        <div id="orb-3" class="absolute top-1/2 left-1/3 w-80 h-80 rounded-full bg-purple-950/20 blur-[100px]"></div>
        <!-- Extra orbs for richer ambient feel -->
        <div id="orb-4" class="absolute top-1/4 right-1/4 w-72 h-72 rounded-full bg-cyan-900/15 blur-[100px]"></div>
        <div id="orb-5" class="absolute bottom-1/4 left-1/4 w-64 h-64 rounded-full bg-fuchsia-900/15 blur-[90px]"></div>
        <!-- ⚡ NEON ADDITION: Two new intense neon orbs -->
        <div id="orb-6"></div>
        <div id="orb-7"></div>
    </div>
    
    <!-- Main Player UI Card Container with Ambilight back-glow -->
    <div id="player-fullscreen-wrapper" class="relative w-full max-w-5xl h-[610px] card-enter">
        <!-- Dynamic behind-the-scenes Ambient Ambilight Backglow -->
        <div id="player-ambilight-glow" class="absolute -inset-10 rounded-[40px] opacity-60 blur-[60px] pointer-events-none -z-10 transition-all duration-300"></div>
        
        <!-- Main Player UI Card -->
        <div class="glass-panel w-full h-full rounded-3xl overflow-hidden flex flex-col md:flex-row shadow-2xl relative">

            <!-- ⚡ NEON ADDITION: Top & Bottom edge glow lines -->
            <div class="neon-top-edge"></div>
            <div class="neon-bottom-edge"></div>

            <!-- ⚡ NEON ADDITION: Corner arc lightning decorators -->
            <div class="neon-corner-arc tl" aria-hidden="true"></div>
            <div class="neon-corner-arc tr" aria-hidden="true"></div>
            <div class="neon-corner-arc bl" aria-hidden="true"></div>
            <div class="neon-corner-arc br" aria-hidden="true"></div>

            <!-- NEW: Beat flash overlay -->
        <div id="beat-flash" class="absolute inset-0 rounded-3xl pointer-events-none z-50 opacity-0 transition-opacity duration-75" style="background: radial-gradient(ellipse at center, rgba(244,63,94,0.18) 0%, transparent 70%);"></div>

            <!-- ⚡ NEON ADDITION: Corner beat flash sparks -->
            <div id="beat-flash-corner-tl" aria-hidden="true"></div>
            <div id="beat-flash-corner-tr" aria-hidden="true"></div>
            <div id="beat-flash-corner-bl" aria-hidden="true"></div>
            <div id="beat-flash-corner-br" aria-hidden="true"></div>

        <!-- Interactive Parallax Cursor Glow Spot -->
            <div id="interactive-cursor-glow" class="absolute w-[350px] h-[350px] rounded-full pointer-events-none -z-5 opacity-0 blur-[80px] transition-opacity duration-500" style="background: radial-gradient(circle, rgba(255,255,255,0.08) 0%, transparent 70%);"></div>

            <!-- ⚡ NEON ADDITION: Inner ambient neon aura overlay -->
            <div id="neon-inner-aura"></div>

            <!-- ⚡ NEON ADDITION: Grain texture neon tint overlay -->
            <div id="neon-grain-overlay" aria-hidden="true"></div>
        
        <!-- Left Side: Music Panel (Controls & Visualizers) -->
        <div id="music-panel" class="w-full md:w-[45%] px-5 py-3 flex flex-col justify-between border-r border-white/5 relative z-10 transition-all duration-500 ease-in-out">
            
            <!-- Header (Title & Mode Toggle) -->
            <div class="flex items-center justify-between">
                <div class="flex items-center gap-2">
                    <span class="flex h-2 w-2 relative">
                        <span class="animate-ping absolute inline-flex h-full w-full rounded-full bg-rose-400 opacity-75"></span>
                        <span class="relative inline-flex rounded-full h-2 w-2 bg-rose-500"></span>
                    </span>
                    <p class="text-xs uppercase tracking-wider text-white/50 font-medium">Now Playing</p>
                </div>
                
                <!-- Audio/Video Mode Switcher -->
                <button id="mode-toggle-btn" onclick="togglePlayMode()" class="px-3 py-1 text-xs rounded-full border border-white/10 hover:border-white/30 bg-white/5 hover:bg-white/10 flex items-center gap-1.5 transition-all text-white/80 neon-cta">
                    <i data-lucide="video" class="w-3.5 h-3.5"></i>
                    <span>Switch to Video</span>
                </button>
            </div>
            
            <!-- Display Section (Rotating Album Art OR 3D Visualizer Canvas OR YouTube Video) -->
            <div class="flex-grow flex items-center justify-center py-2 relative" style="min-height: 180px; max-height: 220px;">
                
                <!-- Three.js 3D Visualizer Canvas Container (Hidden by default, shown when 3D style is chosen) -->
                <div id="three-visualizer-container" class="absolute inset-0 w-full h-full pointer-events-none z-0 overflow-hidden rounded-2xl"></div>

                <!-- 2D Visualizer Canvas -->
                <canvas id="visualizer-canvas" class="absolute w-full h-full opacity-40 pointer-events-none z-0"></canvas>
                
                <!-- Audio Mode View (Rotating Vinyl Record) -->
                <div id="audio-view" class="flex flex-col items-center justify-center transition-all duration-500 w-full z-10">
                    <div class="relative group vinyl-enter-active" style="transform:scale(0.85);">
                        <!-- ⚡ NEON ADDITION: Vinyl neon halo rings -->
                        <div class="vinyl-neon-halo-wrapper" aria-hidden="true">
                            <div class="vinyl-neon-ring-1"></div>
                            <div class="vinyl-neon-ring-2"></div>
                            <div class="vinyl-neon-ring-3"></div>
                        </div>

                        <!-- Vinyl Record Background Frame -->
                        <div id="vinyl-record" class="w-48 h-48 rounded-full bg-black border-4 border-zinc-800 flex items-center justify-center shadow-2xl relative transition-transform duration-75">
                            <div class="absolute inset-2 rounded-full border border-zinc-900/30 opacity-60"></div>
                            <div class="absolute inset-6 rounded-full border border-zinc-900/30 opacity-60"></div>
                            <div class="absolute inset-10 rounded-full border border-zinc-900/30 opacity-60"></div>
                            <div class="absolute inset-14 rounded-full border border-zinc-900/30 opacity-60"></div>
                            <div class="absolute inset-18 rounded-full border border-zinc-900/30 opacity-60"></div>
                            
                            <!-- Album Cover in the center -->
                            <img id="album-art-img" src="{thumbnail_url}" alt="Album Art" class="w-20 h-20 rounded-full object-cover border-4 border-zinc-900 z-10 shadow-lg">
                            
                            <!-- Center Hole -->
                            <div class="w-4 h-4 rounded-full bg-[#060810] border border-zinc-700 z-20 shadow-inner"></div>
                        </div>
                        
                        <!-- Ambient glowing ring behind vinyl -->
                        <div class="absolute inset-0 rounded-full bg-rose-500/10 blur-xl opacity-0 group-hover:opacity-100 transition-opacity pointer-events-none"></div>
                    </div>
                </div>
                
                <!-- Video Mode View (Embedded YouTube Iframe) -->
                <div id="video-view" class="hidden absolute inset-0 rounded-2xl overflow-hidden bg-black/60 flex items-center justify-center transition-all duration-500 p-2 z-20">
                    <div id="yt-player-container" class="w-full h-full rounded-xl overflow-hidden aspect-video border border-white/10">
                        <div id="yt-player"></div>
                    </div>
                </div>
            </div>
            
            <!-- Track Details -->
            <div class="text-center md:text-left mb-2 z-10">
                <h2 id="song-title-label" class="text-lg font-bold text-white tracking-wide truncate max-w-full" title="{song_title}">{song_title}</h2>
                <p id="artist-label" class="text-xs text-white/60 font-medium truncate mt-0.5" title="{artist}">{artist}</p>
            </div>
            
            <!-- Playback Controls -->
            <div class="flex flex-col gap-2 z-10">
                
                <!-- NEW: Waveform Scrubber Canvas (sits behind the range input) -->
                <div class="relative w-full mt-1 mb-0" style="height:36px;">
                    <canvas id="waveform-canvas" class="absolute inset-0 w-full h-full rounded-lg opacity-70 pointer-events-none"></canvas>
                    <input id="progress-bar" type="range" min="0" max="{duration_seconds}" value="0" oninput="onProgressSeek(this.value)" class="w-full h-1 relative z-10" style="margin-top:17px;background:transparent;">
                    <!-- ⚡ NEON ADDITION: Neon laser trail overlay for progress bar -->
                    <div id="neon-progress-layer" aria-hidden="true">
                        <div id="neon-progress-fill" style="width: 0%;"></div>
                        <div id="neon-progress-sweep"></div>
                    </div>
                </div>
                <div class="flex justify-between text-[10px] text-white/40 mt-0.5 font-mono">
                    <span id="time-current">00:00</span>
                    <span id="beat-bpm" class="text-rose-400/60 font-bold tracking-widest text-[9px]"></span>
                    <span id="time-total">{duration_str}</span>
                </div>
                
                <!-- Dynamic Button Controls with Prev/Next and Shuffle/Repeat -->
                <div class="flex items-center justify-center gap-4">
                    <!-- Shuffle Button -->
                    <button id="shuffle-btn" onclick="toggleShuffle()" class="text-white/40 hover:text-white transition-colors" title="Shuffle Off">
                        <i data-lucide="shuffle" class="w-4 h-4"></i>
                    </button>

                    <!-- Previous Track -->
                    <button onclick="playPrevTrack()" class="text-white/60 hover:text-white transition-colors hover:scale-105 active:scale-95" title="Previous Song">
                        <i data-lucide="skip-back" class="w-5 h-5"></i>
                    </button>

                    <!-- Rewind 10s -->
                    <button onclick="skipTime(-10)" class="text-white/40 hover:text-white transition-colors" title="Rewind 10s">
                        <i data-lucide="rotate-ccw" class="w-4 h-4"></i>
                    </button>
                    
                    <!-- Play/Pause -->
                    <!-- ⚡ NEON ADDITION: Lightning crown wrapper for play button -->
                    <div class="relative flex items-center justify-center">
                        <div id="play-pause-neon-crown" aria-hidden="true"></div>
                        <button id="play-pause-btn" onclick="togglePlayState()" class="w-12 h-12 rounded-full bg-rose-600 hover:bg-rose-500 text-white flex items-center justify-center shadow-lg shadow-rose-600/20 hover:scale-105 active:scale-95 transition-all">
                            <i id="play-icon" data-lucide="play" class="w-5 h-5 fill-white"></i>
                        </button>
                    </div>
                    
                    <!-- Fast Forward 10s -->
                    <button onclick="skipTime(10)" class="text-white/40 hover:text-white transition-colors" title="Forward 10s">
                        <i data-lucide="rotate-cw" class="w-4 h-4"></i>
                    </button>

                    <!-- Next Track -->
                    <button onclick="playNextTrack()" class="text-white/60 hover:text-white transition-colors hover:scale-105 active:scale-95" title="Next Song">
                        <i data-lucide="skip-forward" class="w-5 h-5"></i>
                    </button>

                    <!-- Repeat Button -->
                    <button id="repeat-btn" onclick="toggleRepeat()" class="text-white/40 hover:text-white transition-colors" title="Repeat Off">
                        <i data-lucide="repeat" class="w-4 h-4"></i>
                    </button>
                </div>
                
                <!-- Volume & Audio Details -->
                <div class="flex items-center gap-3 px-2">
                    <button onclick="toggleMute()" class="text-white/50 hover:text-white transition-colors">
                        <i id="volume-icon" data-lucide="volume-2" class="w-4 h-4"></i>
                    </button>
                    <input id="volume-slider" type="range" min="0" max="100" value="70" oninput="onVolumeChange(this.value)" class="w-20 h-1">
                    
                    <div class="flex-grow"></div>
                    
                    <!-- Lyrics Sync Offset Adjustment Slider -->
                    <div class="flex items-center gap-1.5 text-[10px] text-white/40 bg-white/5 px-2 py-0.5 rounded-full" title="Adjust lyrics synchronization offset">
                        <span>Sync offset:</span>
                        <input id="offset-slider" type="range" min="-50" max="50" value="0" class="w-12 h-1" oninput="onOffsetChange(this.value)">
                        <span id="offset-label" class="font-mono">0.0s</span>
                    </div>
                </div>
                
                <!-- Visualizer Selector Pill Bar (Includes 3D visualizers!) -->
                <div class="flex items-center justify-between text-[10px] border-t border-white/5 pt-2 px-1">
                    <span class="text-white/40 flex items-center gap-1">
                        <i data-lucide="activity" class="w-3.5 h-3.5 text-rose-500"></i>
                        <span>Visualizer Style:</span>
                    </span>
                    <div class="flex flex-wrap gap-1 bg-white/5 p-0.5 rounded-lg border border-white/5 max-w-[80%] justify-end">
                        <button onclick="setVisualizerStyle('wave')" id="viz-btn-wave" class="px-1 py-0.5 rounded text-[8px] bg-white/10 text-white font-medium transition-all">2D Wave</button>
                        <button onclick="setVisualizerStyle('radial')" id="viz-btn-radial" class="px-1 py-0.5 rounded text-[8px] text-white/60 hover:text-white font-medium transition-all">2D Sun</button>
                        <button onclick="setVisualizerStyle('orb')" id="viz-btn-orb" class="px-1 py-0.5 rounded text-[8px] text-white/60 hover:text-white font-medium transition-all">3D Orb</button>
                        <button onclick="setVisualizerStyle('grid')" id="viz-btn-grid" class="px-1 py-0.5 rounded text-[8px] text-white/60 hover:text-white font-medium transition-all">3D Grid</button>
                        <button onclick="setVisualizerStyle('tunnel')" id="viz-btn-tunnel" class="px-1 py-0.5 rounded text-[8px] text-white/60 hover:text-white font-medium transition-all">3D Tunnel</button>
                        <button onclick="setVisualizerStyle('spectrum')" id="viz-btn-spectrum" class="px-1 py-0.5 rounded text-[8px] text-white/60 hover:text-white font-medium transition-all">3D Ring</button>
                        <button onclick="setVisualizerStyle('galaxy')" id="viz-btn-galaxy" class="px-1 py-0.5 rounded text-[8px] text-white/60 hover:text-white font-medium transition-all">3D Vortex</button>
                        <button onclick="setVisualizerStyle('stars')" id="viz-btn-stars" class="px-1 py-0.5 rounded text-[8px] text-white/60 hover:text-white font-medium transition-all">⭐ Stars</button>
                        <button onclick="setVisualizerStyle('city')" id="viz-btn-city" class="px-1 py-0.5 rounded text-[8px] text-white/60 hover:text-white font-medium transition-all">🏙 City</button>
                        <!-- ✨ NEW visualizer presets -->
                        <button onclick="setVisualizerStyle('dna')" id="viz-btn-dna" class="px-1 py-0.5 rounded text-[8px] text-white/60 hover:text-white font-medium transition-all">🧬 DNA</button>
                        <button onclick="setVisualizerStyle('fire')" id="viz-btn-fire" class="px-1 py-0.5 rounded text-[8px] text-white/60 hover:text-white font-medium transition-all">🔥 Fire</button>
                        <button onclick="setVisualizerStyle('aurora')" id="viz-btn-aurora" class="px-1 py-0.5 rounded text-[8px] text-white/60 hover:text-white font-medium transition-all">🌌 Aurora</button>
                    </div>
                </div>
                
                <!-- Theme Selector Pill Bar -->
                <div class="flex items-center justify-between text-[10px] border-t border-white/5 pt-2 px-1">
                    <span class="text-white/40 flex items-center gap-1">
                        <i data-lucide="palette" class="w-3.5 h-3.5 text-purple-400"></i>
                        <span>Theme Accent:</span>
                    </span>
                    <div class="flex gap-2 items-center bg-white/5 px-2 py-1 rounded-lg border border-white/5">
                        <button onclick="setTheme('rose')" id="theme-btn-rose" class="w-3 h-3 rounded-full bg-rose-500 border border-white/40 ring-2 ring-white/10 transition-all scale-110" title="Sunset Rose"></button>
                        <button onclick="setTheme('aurora')" id="theme-btn-aurora" class="w-3 h-3 rounded-full bg-emerald-500 opacity-60 hover:opacity-100 transition-all hover:scale-105" title="Emerald Aurora"></button>
                        <button onclick="setTheme('cyberpunk')" id="theme-btn-cyberpunk" class="w-3 h-3 rounded-full bg-fuchsia-500 opacity-60 hover:opacity-100 transition-all hover:scale-105" title="Cyberpunk Neon"></button>
                        <button onclick="setTheme('ocean')" id="theme-btn-ocean" class="w-3 h-3 rounded-full bg-indigo-500 opacity-60 hover:opacity-100 transition-all hover:scale-105" title="Deep Ocean"></button>
                        <button onclick="setTheme('amber')" id="theme-btn-amber" class="w-3 h-3 rounded-full bg-amber-500 opacity-60 hover:opacity-100 transition-all hover:scale-105" title="Gold Amber"></button>
                        <!-- ✨ NEW themes -->
                        <button onclick="setTheme('matrix')" id="theme-btn-matrix" class="w-3 h-3 rounded-full bg-green-400 opacity-60 hover:opacity-100 transition-all hover:scale-105" title="Matrix Green"></button>
                        <button onclick="setTheme('ice')" id="theme-btn-ice" class="w-3 h-3 rounded-full bg-sky-300 opacity-60 hover:opacity-100 transition-all hover:scale-105" title="Ice Blue"></button>
                        <button onclick="setTheme('holo')" id="theme-btn-holo" class="w-3 h-3 rounded-full opacity-60 hover:opacity-100 transition-all hover:scale-105" style="background: linear-gradient(135deg,#f43f5e,#a855f7,#06b6d4);" title="Holographic"></button>
                        <button onclick="setTheme('lava')" id="theme-btn-lava" class="w-3 h-3 rounded-full bg-orange-500 opacity-60 hover:opacity-100 transition-all hover:scale-105" title="Lava Orange"></button>
                    </div>
                </div>
                
                <!-- Equalizer / DSP Preset Selector Pill Bar -->
                <div class="flex items-center justify-between text-[10px] border-t border-white/5 pt-2 px-1">
                    <span class="text-white/40 flex items-center gap-1">
                        <i data-lucide="sliders" class="w-3.5 h-3.5 text-emerald-400"></i>
                        <span>DSP Equalizer:</span>
                    </span>
                    <div class="flex flex-wrap gap-1 bg-white/5 p-0.5 rounded-lg border border-white/5 max-w-[80%] justify-end">
                        <button onclick="setEqualizerPreset('flat')" id="eq-btn-flat" class="px-1 py-0.5 rounded text-[8px] bg-white/10 text-white font-medium transition-all">Flat</button>
                        <button onclick="setEqualizerPreset('bass')" id="eq-btn-bass" class="px-1 py-0.5 rounded text-[8px] text-white/60 hover:text-white font-medium transition-all">Bass Boost</button>
                        <button onclick="setEqualizerPreset('vocals')" id="eq-btn-vocals" class="px-1 py-0.5 rounded text-[8px] text-white/60 hover:text-white font-medium transition-all">Vocals</button>
                        <button onclick="setEqualizerPreset('concert')" id="eq-btn-concert" class="px-1 py-0.5 rounded text-[8px] text-white/60 hover:text-white font-medium transition-all">3D Hall</button>
                        <button onclick="setEqualizerPreset('cyber')" id="eq-btn-cyber" class="px-1 py-0.5 rounded text-[8px] text-white/60 hover:text-white font-medium transition-all">Electronic</button>
                        <!-- ✨ NEW DSP presets -->
                        <button onclick="setEqualizerPreset('lofi')" id="eq-btn-lofi" class="px-1 py-0.5 rounded text-[8px] text-white/60 hover:text-white font-medium transition-all">Lo-Fi</button>
                        <button onclick="setEqualizerPreset('hifi')" id="eq-btn-hifi" class="px-1 py-0.5 rounded text-[8px] text-white/60 hover:text-white font-medium transition-all">Hi-Fi</button>
                        <button onclick="setEqualizerPreset('night')" id="eq-btn-night" class="px-1 py-0.5 rounded text-[8px] text-white/60 hover:text-white font-medium transition-all">🌙 Night</button>
                    </div>
                </div>
            </div>
        </div>

            <!-- ⚡ NEON ADDITION: BPM Ticker Widget -->
            <div id="neon-bpm-widget" aria-hidden="true">
                <div id="neon-bpm-dot"></div>
                <span id="neon-bpm-label">BPM</span>
                <span id="neon-bpm-value">—</span>
            </div>
        
        <!-- Right Side: Lyrics Panel -->
        <div id="lyrics-panel" class="w-full md:w-[55%] h-full flex flex-col justify-between px-5 py-3 relative z-10 bg-black/25 transition-all duration-500 ease-in-out">
            
            <!-- Panel Header -->
            <div class="flex items-center justify-between border-b border-white/5 pb-3">
                <div class="flex items-center gap-2">
                    <i data-lucide="music-2" class="w-4 h-4 text-rose-500"></i>
                    <h3 class="text-sm font-semibold tracking-wider uppercase text-white/70 lyrics-header-glow">Lyrics Reader</h3>
                    <!-- Spectrum bars decoration -->
                    <span class="spectrum-icon flex items-end gap-[2px] h-4 ml-1">
                        <span style="height:5px;animation-delay:0s;"></span>
                        <span style="height:9px;animation-delay:0.15s;"></span>
                        <span style="height:6px;animation-delay:0.3s;"></span>
                        <span style="height:11px;animation-delay:0.1s;"></span>
                    </span>
                </div>
                
                <div class="flex items-center gap-2">
                    <!-- NEW: Lyrics Search Toggle -->
                    <button id="lyrics-search-btn" onclick="toggleLyricsSearch()" class="px-2.5 py-1 text-xs rounded-full border border-white/10 hover:border-white/30 bg-white/5 hover:bg-white/10 flex items-center gap-1 transition-all text-white/80 neon-tooltip" data-tip="Search lyrics" title="Search Lyrics">
                        <i data-lucide="search" class="w-3 h-3 text-yellow-400"></i>
                        <span>Find</span>
                    </button>
                    <!-- Up Next Queue Drawer Toggle -->
                    <button id="queue-drawer-btn" onclick="toggleQueueDrawer()" class="px-2.5 py-1 text-xs rounded-full border border-white/10 hover:border-white/30 bg-white/5 hover:bg-white/10 flex items-center gap-1 transition-all text-white/80 neon-tooltip" data-tip="Up next queue" title="Show Up Next Queue">
                        <i data-lucide="list-music" class="w-3 h-3 text-cyan-400"></i>
                        <span>Queue</span>
                    </button>
                    <!-- Spotify Focus Mode Switcher -->
                    <button id="focus-toggle-btn" onclick="toggleFocusMode()" class="px-2.5 py-1 text-xs rounded-full border border-white/10 hover:border-white/30 bg-white/5 hover:bg-white/10 flex items-center gap-1 transition-all text-white/80 neon-tooltip" data-tip="Spotify focus mode" title="Toggle Spotify Focus Mode">
                        <i data-lucide="maximize-2" class="w-3 h-3 text-rose-400"></i>
                        <span>Spotify Mode</span>
                    </button>
                    <!-- ✨ NEW: Fullscreen Button -->
                    <button id="fullscreen-btn" onclick="toggleFullscreen()" class="px-2.5 py-1 text-xs rounded-full border border-white/15 hover:border-rose-500/50 bg-white/5 hover:bg-rose-500/10 flex items-center gap-1 transition-all text-white/80 neon-tooltip" data-tip="Fullscreen player" title="Toggle Fullscreen">
                        <i data-lucide="expand" class="w-3 h-3 text-fuchsia-400"></i>
                        <span>Full Screen</span>
                    </button>
                    <span id="lyrics-type-badge" class="px-2 py-0.5 text-[9px] font-bold uppercase rounded-full bg-rose-500/20 text-rose-300 border border-rose-500/20">Synced</span>
                </div>
            </div>

            <!-- NEW: Collapsible Lyrics Search Bar -->
            <div id="lyrics-search-bar" class="hidden flex items-center gap-2 py-2 border-b border-white/5">
                <input id="lyrics-search-input" type="text" placeholder="Search lyrics..." oninput="onLyricsSearch(this.value)" class="flex-grow bg-white/5 border border-white/10 rounded-lg px-3 py-1.5 text-xs text-white placeholder-white/30 outline-none focus:border-rose-500/50">
                <button onclick="lyricsSearchNav(-1)" class="text-white/50 hover:text-white p-1 rounded transition-colors"><i data-lucide="chevron-up" class="w-4 h-4"></i></button>
                <button onclick="lyricsSearchNav(1)" class="text-white/50 hover:text-white p-1 rounded transition-colors"><i data-lucide="chevron-down" class="w-4 h-4"></i></button>
                <span id="lyrics-search-count" class="text-[10px] text-white/40 font-mono min-w-[40px]"></span>
                <button onclick="copyAllLyrics()" class="text-white/40 hover:text-cyan-400 p-1 rounded transition-colors" title="Copy all lyrics"><i data-lucide="copy" class="w-3.5 h-3.5"></i></button>
            </div>
            
            <!-- Lyrics Scrolling Container -->
            <div id="lyrics-scroll-pane" class="lyrics-container flex-grow overflow-y-auto py-4 px-4 space-y-1 scroll-smooth text-center md:text-left flex flex-col">
            </div>
            
            <!-- Floating Spotify Lyric Effects selector (Hidden by default, shown in focus mode) -->
            <div id="effects-bar" class="hidden flex items-center justify-center gap-2.5 p-1.5 rounded-2xl bg-white/5 border border-white/5 text-[10px] mb-3 select-none z-10">
                <span class="text-white/40 font-medium px-2">Lyrics Effect:</span>
                <button onclick="setLyricEffect('blur')" id="effect-btn-blur" class="px-2.5 py-1 rounded-lg bg-white/10 text-white font-medium transition-all">Blur Focus</button>
                <button onclick="setLyricEffect('scale')" id="effect-btn-scale" class="px-2.5 py-1 rounded-lg text-white/60 hover:text-white/80 transition-all">Pop Scale</button>
                <button onclick="setLyricEffect('neon')" id="effect-btn-neon" class="px-2.5 py-1 rounded-lg text-white/60 hover:text-white/80 transition-all">Disco Neon</button>
                <button onclick="setLyricEffect('karaoke')" id="effect-btn-karaoke" class="px-2.5 py-1 rounded-lg text-white/60 hover:text-white/80 transition-all">Retro Karaoke</button>
                <button onclick="setLyricEffect('glitch')" id="effect-btn-glitch" class="px-2.5 py-1 rounded-lg text-white/60 hover:text-white/80 transition-all">⚡ Glitch</button>
                <button onclick="setLyricEffect('wave')" id="effect-btn-wave" class="px-2.5 py-1 rounded-lg text-white/60 hover:text-white/80 transition-all">🌊 Wave</button>
                <button onclick="setLyricEffect('gold')" id="effect-btn-gold" class="px-2.5 py-1 rounded-lg text-white/60 hover:text-white/80 transition-all">✨ Gold</button>
            </div>

            <!-- Click to seek instruction -->
            <div class="text-center text-[10px] text-white/30 pt-3 border-t border-white/5 flex justify-between items-center z-10">
                <span>💡 Click line to seek · <kbd class="px-1 py-0.5 bg-white/10 rounded text-[9px]">Space</kbd> play · <kbd class="px-1 py-0.5 bg-white/10 rounded text-[9px]">←→</kbd> skip · <kbd class="px-1 py-0.5 bg-white/10 rounded text-[9px]">M</kbd> mute</span>
                <span id="sync-status" class="font-mono text-emerald-400 opacity-80">Synced Ready</span>
            </div>
            
            <!-- Glassmorphic Up Next Playlist Queue Sidebar Drawer (Sliding animation) -->
            <div id="queue-drawer" class="absolute top-0 right-0 bottom-0 w-[85%] sm:w-[60%] glass-panel-sidebar z-50 p-6 flex flex-col justify-between transform translate-x-full transition-transform duration-500 ease-in-out shadow-2xl rounded-l-3xl">
                <div>
                    <div class="flex items-center justify-between border-b border-white/10 pb-4 mb-4">
                        <div class="flex items-center gap-2">
                            <i data-lucide="list-music" class="w-4 h-4 text-cyan-400"></i>
                            <h3 class="text-sm font-bold uppercase tracking-wider text-white">Up Next Play Queue</h3>
                        </div>
                        <button onclick="toggleQueueDrawer()" class="p-1 rounded-full hover:bg-white/10 text-white/60 hover:text-white transition-all">
                            <i data-lucide="x" class="w-4 h-4"></i>
                        </button>
                    </div>
                    <!-- Scrolling List of Songs in Queue -->
                    <div id="queue-song-list" class="flex-grow overflow-y-auto max-h-[420px] space-y-2 pr-1 lyrics-container">
                        <!-- Queue items injected here -->
                    </div>
                </div>
                <div class="text-center text-[10px] text-white/30 pt-4 border-t border-white/10">
                    <span>Active Playlist Length: <span id="queue-len-badge" class="font-mono text-cyan-400">0</span> songs</span>
                </div>
            </div>

        </div>
    </div>
</div>

    <!-- ⚡ NEON ADDITION: Fullscreen exit hint label -->
    <div id="fullscreen-exit-hint" aria-hidden="true">⚡ Press Esc to exit fullscreen</div>

    <!-- YouTube API and Player scripts -->
    <script>
        // 1. Data Injection (Replaced dynamically via Python)
        let activeVideoId = "{video_id}";
        let currentSongTitle = "{song_title}";
        let currentSongArtist = "{artist}";
        let currentSongThumbnail = "{thumbnail_url}";
        let currentSongDuration = parseInt("{duration_seconds}");
        
        let lyricsData = {synced_lyrics_json};
        let plainLyrics = `{plain_lyrics}`;
        
        let playlistQueue = [];
        try {
            playlistQueue = {queue_json};
        } catch(e) {
            console.warn('Queue parse error:', e);
            playlistQueue = [];
        }
        
        let currentQueueIndex = parseInt("{current_index}");
        
        // UI Globals
        let player;
        let lyricsInterval;
        let currentLyricIndex = -1;
        let isMuted = false;
        let lastVolume = 70;
        let isVideoMode = false;
        let lyricsSyncOffset = 0.0;
        let isFocusMode = false;
        let lyricEffect = 'blur';
        let isShuffleActive = false;
        let shuffleOrder = [];
        let repeatMode = 0; // 0 = Off, 1 = Repeat Song, 2 = Repeat Queue
        let isQueueDrawerOpen = false;
        let eqPreset = 'flat';
        
        // Dynamic Lighting & Cursor globals [PURE ADDITION]
        let activePointLight, activePointLight2, activeAmbientLight;
        let cursorX = 0, cursorY = 0, targetCursorX = 0, targetCursorY = 0;

        // ── NEW: Web Audio API context for real spectrum + beat detection ──────
        let audioCtxReal = null;
        let analyserNode = null;
        let sourceNode = null;
        let freqDataArray = null;
        let beatThreshold = 220;
        let beatCooldown = 0;
        let beatFlash = 0;
        let realSpectrumActive = false;

        // ── NEW: Waveform scrubber canvas ─────────────────────────────────────
        let waveformCanvas = null, waveformCtx = null;
        let waveformData = []; // pre-generated fake waveform for visual

        // ── NEW: Lyrics search state ──────────────────────────────────────────
        let lyricsSearchActive = false;
        let lyricsSearchTerm = '';
        let lyricsSearchMatches = [];
        let lyricsSearchIdx = 0;

        // ── NEW: Crossfade state ──────────────────────────────────────────────
        let crossfadeActive = false;
        let crossfadeTimer = null;

        // ── STREAMLIT IFRAME FIX: Manual time tracker ────────────────────────
        // Streamlit's nested iframe breaks YT postMessage bridge, so
        // getCurrentTime() always returns 0. We track time ourselves.
        let manualTimeStart = null;   // Date.now() when play started
        let manualTimeOffset = 0;     // seeked-to position in seconds
        let manualTimePaused = true;
        
        function getPlayerTime() {
            // Try YT API first - if it returns >0, it's working fine
            if (player && typeof player.getCurrentTime === 'function') {
                try {
                    const ytTime = player.getCurrentTime();
                    if (ytTime > 0) {
                        // YT API working - sync our manual tracker
                        manualTimeOffset = ytTime;
                        if (!manualTimePaused) manualTimeStart = Date.now();
                        return ytTime;
                    }
                } catch(e) {}
            }
            // Fallback: use manual timer
            if (manualTimePaused || manualTimeStart === null) return manualTimeOffset;
            const elapsed = (Date.now() - manualTimeStart) / 1000;
            return Math.min(manualTimeOffset + elapsed, currentSongDuration || 9999);
        }

        function manualPlay(seekPos) {
            if (seekPos !== undefined) manualTimeOffset = seekPos;
            manualTimeStart = Date.now();
            manualTimePaused = false;
        }

        function manualPause() {
            if (!manualTimePaused) {
                manualTimeOffset = getPlayerTime();
                manualTimePaused = true;
            }
        }

        function manualSeek(pos) {
            manualTimeOffset = pos;
            if (!manualTimePaused) manualTimeStart = Date.now();
        }
        
        // 2D Visualizer variables
        let canvas, ctx;
        let isPlaying = false;
        let waveOffset = 0;
        let visualizerAmp = 3;
        let visualizerSpeed = 0.015;
        let visualizerStyle = 'wave'; 
        let ambientParticles = [];
        let vinylRotation = 0;
        
        // Three.js 3D Visualizer variables
        let scene3d, camera3d, renderer3d;
        let active3dMesh, active3dGrid, active3dTunnel, active3dSun;
        let active3dSpectrum, active3dSpectrumBars = [], active3dSpectrumSphere;
        let active3dGalaxy;
        let active3dStars, active3dCity, active3dCityBars = [];
        let threeParticles = [];
        let animationFrameId3d;
        
        // Interactivity globals (Parallax & Beat)
        let mouseX = 0, mouseY = 0;
        let targetMouseX = 0, targetMouseY = 0;
        
        // Themes configuration
        const themes = {
            rose: {
                name: "Sunset Rose",
                orbs: ["rgba(244, 63, 94, 0.35)", "rgba(147, 51, 234, 0.25)", "rgba(59, 130, 246, 0.25)"],
                accent: "#f43f5e",
                glow: "rgba(244, 63, 94, 0.5)",
                vizColors: ['rgba(244, 63, 94, 0.45)', 'rgba(168, 85, 247, 0.35)', 'rgba(59, 130, 246, 0.25)'],
                threeHex: 0xf43f5e,
                complementaryHex: 0x6366f1
            },
            aurora: {
                name: "Emerald Aurora",
                orbs: ["rgba(16, 185, 129, 0.35)", "rgba(20, 184, 166, 0.25)", "rgba(6, 182, 212, 0.25)"],
                accent: "#10b981",
                glow: "rgba(16, 185, 129, 0.5)",
                vizColors: ['rgba(16, 185, 129, 0.45)', 'rgba(20, 184, 166, 0.35)', 'rgba(6, 182, 212, 0.25)'],
                threeHex: 0x10b981,
                complementaryHex: 0x06b6d4
            },
            cyberpunk: {
                name: "Cyberpunk Neon",
                orbs: ["rgba(217, 70, 239, 0.35)", "rgba(79, 70, 229, 0.25)", "rgba(245, 158, 11, 0.2)"],
                accent: "#d946ef",
                glow: "rgba(217, 70, 239, 0.5)",
                vizColors: ['rgba(217, 70, 239, 0.45)', 'rgba(79, 70, 229, 0.35)', 'rgba(245, 158, 11, 0.25)'],
                threeHex: 0xd946ef,
                complementaryHex: 0xf59e0b
            },
            ocean: {
                name: "Deep Ocean",
                orbs: ["rgba(99, 102, 241, 0.35)", "rgba(59, 130, 246, 0.25)", "rgba(6, 182, 212, 0.25)"],
                accent: "#6366f1",
                glow: "rgba(99, 102, 241, 0.5)",
                vizColors: ['rgba(99, 102, 241, 0.45)', 'rgba(59, 130, 246, 0.35)', 'rgba(6, 182, 212, 0.25)'],
                threeHex: 0x6366f1,
                complementaryHex: 0xf43f5e
            },
            amber: {
                name: "Gold Amber",
                orbs: ["rgba(245, 158, 11, 0.35)", "rgba(239, 68, 68, 0.25)", "rgba(251, 191, 36, 0.25)"],
                accent: "#fbbf24",
                glow: "rgba(245, 158, 11, 0.5)",
                vizColors: ['rgba(245, 158, 11, 0.45)', 'rgba(239, 68, 68, 0.35)', 'rgba(251, 191, 36, 0.25)'],
                threeHex: 0xfbbf24,
                complementaryHex: 0xd946ef
            },
            // ✨ NEW THEMES
            matrix: {
                name: "Matrix Green",
                orbs: ["rgba(34, 197, 94, 0.35)", "rgba(16, 185, 129, 0.25)", "rgba(4, 120, 87, 0.25)"],
                accent: "#22c55e",
                glow: "rgba(34, 197, 94, 0.5)",
                vizColors: ['rgba(34, 197, 94, 0.45)', 'rgba(16, 185, 129, 0.35)', 'rgba(6, 182, 212, 0.20)'],
                threeHex: 0x22c55e,
                complementaryHex: 0x06b6d4
            },
            ice: {
                name: "Ice Blue",
                orbs: ["rgba(56, 189, 248, 0.35)", "rgba(14, 165, 233, 0.25)", "rgba(99, 102, 241, 0.20)"],
                accent: "#38bdf8",
                glow: "rgba(56, 189, 248, 0.5)",
                vizColors: ['rgba(56, 189, 248, 0.45)', 'rgba(14, 165, 233, 0.35)', 'rgba(99, 102, 241, 0.20)'],
                threeHex: 0x38bdf8,
                complementaryHex: 0xf43f5e
            },
            holo: {
                name: "Holographic",
                orbs: ["rgba(244, 63, 94, 0.25)", "rgba(168, 85, 247, 0.25)", "rgba(6, 182, 212, 0.25)"],
                accent: "#a855f7",
                glow: "rgba(168, 85, 247, 0.5)",
                vizColors: ['rgba(244, 63, 94, 0.4)', 'rgba(168, 85, 247, 0.4)', 'rgba(6, 182, 212, 0.4)'],
                threeHex: 0xa855f7,
                complementaryHex: 0x06b6d4
            },
            lava: {
                name: "Lava Orange",
                orbs: ["rgba(249, 115, 22, 0.35)", "rgba(239, 68, 68, 0.25)", "rgba(234, 88, 12, 0.20)"],
                accent: "#f97316",
                glow: "rgba(249, 115, 22, 0.5)",
                vizColors: ['rgba(249, 115, 22, 0.45)', 'rgba(239, 68, 68, 0.35)', 'rgba(245, 158, 11, 0.25)'],
                threeHex: 0xf97316,
                complementaryHex: 0xfbbf24
            }
        };
        let currentTheme = 'rose';
        
        // 2. Initialize App
        // CRITICAL FIX: In Streamlit's srcdoc iframe, DOMContentLoaded fires BEFORE
        // the inline <script> tag executes, so addEventListener('DOMContentLoaded')
        // callback NEVER runs. We use a direct initApp() call instead.
        function initApp() {
            if (initApp._done) return;
            initApp._done = true;

            lucide.createIcons();


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

            initWaveformCanvas();
            // Inject crossfade button next to repeat
            const repeatBtnInit = document.getElementById('repeat-btn');
            if (repeatBtnInit && repeatBtnInit.parentNode) {
                const xBtn = document.createElement('button');
                xBtn.id = 'crossfade-btn';
                xBtn.onclick = toggleCrossfade;
                xBtn.title = 'Crossfade OFF';
                xBtn.className = 'text-white/40 hover:text-white transition-colors';
                xBtn.innerHTML = '<i data-lucide="arrow-right-left" class="w-4 h-4"></i>';
                repeatBtnInit.parentNode.insertBefore(xBtn, repeatBtnInit.nextSibling);
                lucide.createIcons();
            }
            // If Python already has lyrics, show them immediately
            // Otherwise kick off client-side fetch right away
            if (lyricsData && lyricsData.length > 0) {
                buildLyricsUI();
            } else {
                // Show loading spinner and fetch from browser
                const pane = document.getElementById('lyrics-scroll-pane');
                if (pane) pane.innerHTML = `
                    <div class="text-white/40 text-sm py-12 flex flex-col items-center justify-center">
                        <div class="animate-spin w-6 h-6 border-2 border-t-rose-500 border-white/20 rounded-full mb-2"></div>
                        Loading lyrics...
                    </div>
                `;
                fetchLyricsFromAPI(currentSongTitle, currentSongArtist, currentSongDuration);
            }
            initVisualizer();
            initThreeJS();
            setTheme('rose');
            buildQueueDrawerUI();
            
            // Add mouse interactivity parallax listener
            const musicPanel = document.getElementById('music-panel');
            if (musicPanel) {
                musicPanel.addEventListener('mousemove', (e) => {
                    const rect = musicPanel.getBoundingClientRect();
                    targetMouseX = ((e.clientX - rect.left) / rect.width) * 2 - 1;
                    targetMouseY = -(((e.clientY - rect.top) / rect.height) * 2 - 1);
                });
                musicPanel.addEventListener('mouseleave', () => {
                    targetMouseX = 0;
                    targetMouseY = 0;
                });
            }

            // Interactive cursor spotlight
            const glassPanel = document.querySelector('.glass-panel');
            const cursorGlow = document.getElementById('interactive-cursor-glow');
            if (glassPanel && cursorGlow) {
                glassPanel.addEventListener('mousemove', (e) => {
                    const rect = glassPanel.getBoundingClientRect();
                    targetCursorX = e.clientX - rect.left;
                    targetCursorY = e.clientY - rect.top;
                    cursorGlow.style.opacity = '1';
                });
                glassPanel.addEventListener('mouseleave', () => {
                    cursorGlow.style.opacity = '0';
                });
            }
            
            try {
                localStorage.setItem('melodify_active_song', JSON.stringify({
                    id: activeVideoId, title: currentSongTitle,
                    uploader: currentSongArtist, duration: currentSongDuration,
                    thumbnail: currentSongThumbnail
                }));
            } catch(e) {}
        }
        // Also register as fallback in case DOM isn't ready yet
        document.addEventListener("DOMContentLoaded", initApp);
        window.addEventListener("load", initApp);
        
        // 3. Load YouTube IFrame API
        const tag = document.createElement('script');
        tag.src = "https://www.youtube.com/iframe_api";
        const firstScriptTag = document.getElementsByTagName('script')[0];
        firstScriptTag.parentNode.insertBefore(tag, firstScriptTag);
        
        function onYouTubeIframeAPIReady() {
            player = new YT.Player('yt-player', {
                height: '100%',
                width: '100%',
                videoId: activeVideoId,
                playerVars: {
                    'controls': 0,
                    'disablekb': 1,
                    'fs': 0,
                    'rel': 0,
                    'modestbranding': 1,
                    'showinfo': 0,
                    'iv_load_policy': 3
                },
                events: {
                    'onReady': onPlayerReady,
                    'onStateChange': onPlayerStateChange
                }
            });
        }
        
        function onPlayerReady(event) {
            player.setVolume(lastVolume);
            document.getElementById('volume-slider').value = lastVolume;
            
            // NOTE: Browsers block autoplay inside iframes without a direct user gesture.
            // We do NOT call player.playVideo() here — user must click play.
            
            setTimeout(() => {
                const duration = player.getDuration();
                if(duration) {
                    currentSongDuration = duration;
                    document.getElementById('progress-bar').max = duration;
                    document.getElementById('time-total').innerText = formatTime(duration);
                }
                // Pulse the play button to signal the player is ready
                const playBtn = document.getElementById('play-pause-btn');
                if (playBtn) {
                    playBtn.classList.add('animate-pulse');
                    setTimeout(() => playBtn.classList.remove('animate-pulse'), 2000);
                }
            }, 800);

            // ── Streamlit iframe postMessage bridge fallback ─────────────────────
            // When Streamlit nests this component, YT.PlayerState events may fire
            // but getCurrentTime() returns 0 because the postMessage pipe is throttled.
            // This watchdog polls every 250ms: if the player says it's playing but
            // our manual timer isn't running, kick it off. Also syncs play/pause icon.
            setInterval(() => {
                if (!player) return;
                let ytState = -1;
                try { ytState = player.getPlayerState(); } catch(e) {}
                const ytPlaying = (typeof YT !== 'undefined' && ytState === YT.PlayerState.PLAYING);

                if (ytPlaying && !isPlaying) {
                    // YT is playing but we didn't catch the state change
                    isPlaying = true;
                    manualPlay();
                    const pi = document.getElementById('play-icon');
                    if (pi) { pi.setAttribute('data-lucide', 'pause'); lucide.createIcons(); }
                    startLyricsSync();
                } else if (!ytPlaying && ytState === 2 && isPlaying) {
                    // Paused (state 2) but we think we're playing
                    isPlaying = false;
                    manualPause();
                    const pi = document.getElementById('play-icon');
                    if (pi) { pi.setAttribute('data-lucide', 'play'); lucide.createIcons(); }
                    stopLyricsSync();
                }
            }, 250);
        }
        
        function onPlayerStateChange(event) {
            const playIcon = document.getElementById('play-icon');
            
            if (event.data === YT.PlayerState.PLAYING) {
                isPlaying = true;
                manualPlay();
                playIcon.setAttribute('data-lucide', 'pause');
                lucide.createIcons();
                startLyricsSync();
            } else if (event.data === YT.PlayerState.ENDED) {
                isPlaying = false;
                manualPause();
                playIcon.setAttribute('data-lucide', 'play');
                lucide.createIcons();
                stopLyricsSync();
                handleSongEnded();
            } else {
                isPlaying = false;
                manualPause();
                playIcon.setAttribute('data-lucide', 'play');
                lucide.createIcons();
                stopLyricsSync();
            }
        }
        
        // 4. Standalone STANDALONE Playlist Queue Navigation!
        function handleSongEnded() {
            if (repeatMode === 1) {
                // Repeat Song
                player.seekTo(0);
                player.playVideo();
            } else {
                // Next song
                playNextTrack();
            }
        }
        
        function playNextTrack() {
            if (!playlistQueue || playlistQueue.length === 0) {
                // Reset to beginning or stop
                if (repeatMode === 2) {
                    player.seekTo(0);
                    player.playVideo();
                }
                return;
            }
            
            let nextIndex = currentQueueIndex + 1;
            if (isShuffleActive) {
                // Get a random index
                nextIndex = Math.floor(Math.random() * playlistQueue.length);
            }
            
            if (nextIndex >= playlistQueue.length) {
                if (repeatMode === 2) {
                    nextIndex = 0; // Loop back
                } else {
                    // Queue ended
                    stStatusToast('Queue ended!');
                    return;
                }
            }
            
            playQueueSongAtIndex(nextIndex);
        }
        
        function playPrevTrack() {
            if (!playlistQueue || playlistQueue.length === 0) return;
            
            let prevIndex = currentQueueIndex - 1;
            if (prevIndex < 0) {
                if (repeatMode === 2) {
                    prevIndex = playlistQueue.length - 1;
                } else {
                    prevIndex = 0;
                }
            }
            
            playQueueSongAtIndex(prevIndex);
        }
        
        function playQueueSongAtIndex(index) {
            if (index < 0 || index >= playlistQueue.length) return;
            
            currentQueueIndex = index;
            const song = playlistQueue[index];
            
            activeVideoId = song.id || song.youtube_id;
            currentSongTitle = song.title;
            currentSongArtist = song.uploader;
            currentSongThumbnail = song.thumbnail;
            currentSongDuration = song.duration || 180;
            
            // Update labels
            document.getElementById('song-title-label').innerText = currentSongTitle;
            document.getElementById('song-title-label').title = currentSongTitle;
            document.getElementById('artist-label').innerText = currentSongArtist;
            document.getElementById('artist-label').title = currentSongArtist;
            document.getElementById('album-art-img').src = currentSongThumbnail;
            
            document.getElementById('progress-bar').value = 0;
            document.getElementById('progress-bar').max = currentSongDuration;
            document.getElementById('time-total').innerText = formatTime(currentSongDuration);
            document.getElementById('time-current').innerText = "00:00";
            
            // Reset lyrics states
            lyricsData = [];
            plainLyrics = "";
            currentLyricIndex = -1;
            document.getElementById('lyrics-scroll-pane').innerHTML = `
                <div class="text-white/40 text-sm py-12 flex flex-col items-center justify-center">
                    <div class="animate-spin w-6 h-6 border-2 border-t-rose-500 border-white/20 rounded-full mb-2"></div>
                    Searching lyrics database...
                </div>
            `;
            
            // Play song in Player
            if (player) {
                player.loadVideoById(activeVideoId);
                player.playVideo();
            }
            
            // Notify parent context (local storage update)
            localStorage.setItem('melodify_active_song', JSON.stringify(song));
            
            // Query public API in background from Javascript! (Mind-blowing client independence)
            fetchLyricsFromAPI(currentSongTitle, currentSongArtist, currentSongDuration);
            buildQueueDrawerUI();
            
            // Safety: if fetch hangs for 10s, clear spinner and show not-found state
            setTimeout(() => {
                const pane = document.getElementById('lyrics-scroll-pane');
                if (pane && pane.querySelector('.animate-spin')) {
                    lyricsData = [];
                    plainLyrics = '';
                    buildLyricsUI();
                }
            }, 10000);
        }
        
        // Multi-provider JS lyrics fetcher for queue-navigation (client-side)
        // Chain: LrcLib (search + get-by-params) → Lyrics.ovh → empty
        function fetchLyricsFromAPI(rawTitle, rawArtist, duration) {
            // ─── Step 1: Smart title cleaning (strips YouTube suffixes) ───────
            function cleanYtTitle(t) {
                return t
                    .replace(/(Official\s*(Music|Lyric|Dance|Audio|HD)?\s*Video)/gi, '')
                    .replace(/\[Official\s*(Music|Lyric|Dance|Audio|HD)?\s*Video\]/gi, '')
                    .replace(/\(Audio\)/gi, '').replace(/\[Audio\]/gi, '')
                    .replace(/\(Full\s*(Song|Audio|Video)\)/gi, '')
                    .replace(/\[Full\s*(Song|Audio|Video)\]/gi, '')
                    .replace(/\(Lyric\s*(Video)?\)/gi, '').replace(/\[Lyric\s*(Video)?\]/gi, '')
                    .replace(/\(Official\)/gi, '').replace(/\[Official\]/gi, '')
                    .replace(/\(HD\)/gi, '').replace(/\[HD\]/gi, '')
                    .replace(/\(4K\)/gi, '').replace(/\[4K\]/gi, '')
                    .replace(/feat\.?\s+[^|(\[]+/gi, '')
                    .replace(/ft\.?\s+[^|(\[]+/gi, '')
                    .replace(/\s+/g, ' ').trim();
            }
            const title = cleanYtTitle(rawTitle);
            const artist = cleanYtTitle(rawArtist);
            
            // ─── Step 2: Build query variants ────────────────────────────────
            const queries = [];
            // Variant A: artist + title
            if (artist && title) queries.push(encodeURIComponent(artist + ' ' + title));
            // Variant B: title only (good when artist name is a channel name)
            if (title) queries.push(encodeURIComponent(title));
            // Variant C: split on " - " (e.g. "Arijit Singh - Kesariya")
            const combined = artist + ' ' + title;
            if (combined.includes(' - ')) {
                const parts = combined.split(' - ');
                const p0 = parts[0].trim(), p1 = parts[1] ? parts[1].trim() : '';
                if (p0 && p1) queries.push(encodeURIComponent(p0 + ' ' + p1));
                if (p1) queries.push(encodeURIComponent(p1)); // just song name after dash
            }
            // Variant D: raw original title (unstripped)
            if (rawTitle !== title) queries.push(encodeURIComponent(rawTitle));
            
            // Remove duplicate queries
            const seen = new Set();
            const uniqueQueries = queries.filter(q => { if (seen.has(q)) return false; seen.add(q); return true; });
            
            // ─── Step 3: Try LrcLib /api/search (full-text) ─────────────────
            function tryLrcLibSearch(qIdx) {
                if (qIdx >= uniqueQueries.length) {
                    // Exhausted search queries → try structured GET by track+artist
                    tryLrcLibGet();
                    return;
                }
                const url = 'https://lrclib.net/api/search?q=' + uniqueQueries[qIdx];
                const ctrl = new AbortController();
                const tid = setTimeout(() => ctrl.abort(), 6000);
                fetch(url, { signal: ctrl.signal })
                    .then(res => { clearTimeout(tid); if (res.ok) return res.json(); throw new Error(); })
                    .then(data => {
                        if (data && data.length > 0) {
                            const match = data[0];
                            const synced = match.syncedLyrics || '';
                            const plain  = match.plainLyrics  || '';
                            if (synced || plain) {
                                applyLyrics(synced, plain, duration, '\u2705 LrcLib Synced');
                                return;
                            }
                        }
                        tryLrcLibSearch(qIdx + 1);
                    })
                    .catch(() => { clearTimeout(tid); tryLrcLibSearch(qIdx + 1); });
            }
            
            // ─── Step 4: Try LrcLib /api/search with explicit track_name+artist_name ─
            function tryLrcLibGet() {
                // Build structured param variants
                const structuredVariants = [];
                if (artist && title) {
                    structuredVariants.push(
                        'https://lrclib.net/api/search?track_name=' + encodeURIComponent(title) + '&artist_name=' + encodeURIComponent(artist)
                    );
                }
                // Try with just track name from dash-split
                if (combined.includes(' - ')) {
                    const dashParts = combined.split(' - ');
                    const songPart = dashParts[1] ? dashParts[1].trim() : '';
                    const artistPart = dashParts[0].trim();
                    if (songPart && artistPart) {
                        structuredVariants.push(
                            'https://lrclib.net/api/search?track_name=' + encodeURIComponent(songPart) + '&artist_name=' + encodeURIComponent(artistPart)
                        );
                    }
                }
                
                function tryStructured(idx) {
                    if (idx >= structuredVariants.length) {
                        fetchPlainLyricsFallback(title, artist, rawTitle, duration);
                        return;
                    }
                    const ctrl2 = new AbortController();
                    const tid2 = setTimeout(() => ctrl2.abort(), 6000);
                    fetch(structuredVariants[idx], { signal: ctrl2.signal })
                        .then(res => { clearTimeout(tid2); if (res.ok) return res.json(); throw new Error(); })
                        .then(data => {
                            if (data && data.length > 0) {
                                const match = data[0];
                                const synced = match.syncedLyrics || '';
                                const plain  = match.plainLyrics  || '';
                                if (synced || plain) {
                                    applyLyrics(synced, plain, duration, '\u2705 LrcLib Synced');
                                    return;
                                }
                            }
                            tryStructured(idx + 1);
                        })
                        .catch(() => { clearTimeout(tid2); tryStructured(idx + 1); });
                }
                tryStructured(0);
            }
            
            // ─── Apply result ──────────────────────────────────────────────
            function applyLyrics(synced, plain, dur, toastMsg) {
                plainLyrics = plain;
                lyricsData  = synced ? parseLrcInJS(synced) : generateLinearLrcInJS(plain, dur);
                buildLyricsUI();
                stStatusToast(toastMsg);
            }
            
            tryLrcLibSearch(0);
            
            // ─── Global safety timeout: if ALL fetches hang (e.g. CSP/network block),
            // fall back to whatever Python already injected into lyricsData/plainLyrics ─
            setTimeout(() => {
                const pane = document.getElementById('lyrics-scroll-pane');
                if (pane && (pane.innerHTML.trim() === '' || pane.querySelector('.animate-spin'))) {
                    // Still showing spinner after 8s — use Python-injected data or show not-found
                    buildLyricsUI();
                }
            }, 8000);
        }  // end fetchLyricsFromAPI
        
        function fetchPlainLyricsFallback(title, artist, rawTitle, duration) {
            // Lyrics.ovh — try multiple title/artist combos
            const attempts = [];
            if (artist && title) {
                attempts.push(`https://api.lyrics.ovh/v1/${encodeURIComponent(artist)}/${encodeURIComponent(title)}`);
                attempts.push(`https://api.lyrics.ovh/v1/${encodeURIComponent(title)}/${encodeURIComponent(artist)}`);
            }
            // Also try with raw title if different
            if (rawTitle && rawTitle !== title && artist) {
                attempts.push(`https://api.lyrics.ovh/v1/${encodeURIComponent(artist)}/${encodeURIComponent(rawTitle)}`);
            }
            
            function tryOvh(idx) {
                if (idx >= attempts.length) {
                    // Nothing found — show empty state
                    plainLyrics = ''; lyricsData = [];
                    buildLyricsUI();
                    return;
                }
                const ctrl3 = new AbortController();
                const tid3 = setTimeout(() => ctrl3.abort(), 6000);
                fetch(attempts[idx], { signal: ctrl3.signal })
                    .then(res => { clearTimeout(tid3); if (res.ok) return res.json(); throw new Error(); })
                    .then(data => {
                        if (data && data.lyrics && data.lyrics.trim().length > 20) {
                            plainLyrics = data.lyrics;
                            lyricsData  = generateLinearLrcInJS(plainLyrics, duration);
                            buildLyricsUI();
                            stStatusToast('\uD83D\uDCDD Lyrics.ovh Auto-Synced');
                        } else {
                            tryOvh(idx + 1);
                        }
                    })
                    .catch(() => { clearTimeout(tid3); tryOvh(idx + 1); });
            }
            tryOvh(0);
        }
        
        function parseLrcInJS(lrc) {
            // Split on real newlines (LRC data uses actual \n characters)
            const lines = lrc.split('\n');
            const result = [];
            // Correct JS regex for LRC timestamp: [mm:ss.xx]
            const tagRegex = /\[(\d+):(\d+(?:\.\d+)?)\]/g;
            
            lines.forEach(line => {
                const cleanLine = line.trim();
                if (!cleanLine) return;
                
                let matches = [];
                let match;
                // Reset lastIndex before exec loop
                tagRegex.lastIndex = 0;
                while ((match = tagRegex.exec(cleanLine)) !== null) {
                    matches.push([match[0], match[1], match[2]]);
                }
                
                if (matches.length === 0) return;
                
                // Strip all LRC timestamp tags to get clean lyric text
                const text = cleanLine.replace(/\[\d+:\d+(?:\.\d+)?\]/g, '').trim();
                // Skip metadata lines and blank lines
                if (!text || /^(ar|ti|al|by|offset|length):/i.test(text)) return;
                
                matches.forEach(m => {
                    const min = parseInt(m[1]);
                    const sec = parseFloat(m[2]);
                    result.push({
                        time: min * 60 + sec,
                        text: text
                    });
                });
            });
            result.sort((a,b) => a.time - b.time);
            return result;
        }
        
        function generateLinearLrcInJS(plain, duration) {
            // Split on real newlines
            const lines = plain.split('\n').map(l => l.trim()).filter(l => l.length > 0);
            if(lines.length === 0) return [];
            
            const start = Math.min(10, duration * 0.08);
            const end = Math.max(duration - 12, duration * 0.9);
            const result = [];
            const n = lines.length;
            
            lines.forEach((line, i) => {
                const t = n > 1 ? start + i * (end - start) / (n - 1) : start;
                result.push({
                    time: t,
                    text: line
                });
            });
            return result;
        }
        
        // Queue UI builders
        function buildQueueDrawerUI() {
            const list = document.getElementById('queue-song-list');
            const badge = document.getElementById('queue-len-badge');
            list.innerHTML = '';
            
            if (!playlistQueue || playlistQueue.length === 0) {
                list.innerHTML = `<div class="text-white/30 text-xs py-10 text-center">Your playback queue is empty.</div>`;
                badge.innerText = "0";
                return;
            }
            
            badge.innerText = playlistQueue.length;
            
            playlistQueue.forEach((song, index) => {
                const isActive = index === currentQueueIndex;
                const div = document.createElement('div');
                div.className = `p-2.5 rounded-xl border flex items-center gap-3 transition-all cursor-pointer ${
                    isActive 
                        ? 'bg-rose-500/10 border-rose-500/30' 
                        : 'bg-white/5 border-white/5 hover:bg-white/10 hover:border-white/10'
                }`;
                
                div.onclick = () => {
                    playQueueSongAtIndex(index);
                    toggleQueueDrawer();
                };
                
                const durationM = Math.floor((song.duration || 180) / 60);
                const durationS = Math.floor((song.duration || 180) % 60);
                const durStr = `${durationM}:${durationS < 10 ? '0' + durationS : durationS}`;
                
                div.innerHTML = `
                    <img src="${song.thumbnail}" class="w-10 h-10 rounded-lg object-cover">
                    <div class="flex-grow overflow-hidden text-left">
                        <p class="text-xs font-semibold text-white truncate ${isActive ? 'text-rose-400' : ''}">${song.title}</p>
                        <p class="text-[10px] text-white/50 truncate">${song.uploader}</p>
                    </div>
                    <span class="text-[10px] font-mono text-white/30">${durStr}</span>
                `;
                list.appendChild(div);
            });
        }
        
        function toggleQueueDrawer() {
            isQueueDrawerOpen = !isQueueDrawerOpen;
            const drawer = document.getElementById('queue-drawer');
            if (isQueueDrawerOpen) {
                drawer.classList.remove('translate-x-full');
            } else {
                drawer.classList.add('translate-x-full');
            }
        }
        
        function toggleShuffle() {
            isShuffleActive = !isShuffleActive;
            const btn = document.getElementById('shuffle-btn');
            if (isShuffleActive) {
                btn.className = "text-rose-500 transition-colors scale-105";
                btn.title = "Shuffle Active";
                stStatusToast("Shuffle ON");
            } else {
                btn.className = "text-white/40 hover:text-white transition-colors";
                btn.title = "Shuffle Off";
                stStatusToast("Shuffle OFF");
            }
        }
        
        function toggleRepeat() {
            repeatMode = (repeatMode + 1) % 3;
            const btn = document.getElementById('repeat-btn');
            
            if (repeatMode === 0) {
                btn.className = "text-white/40 hover:text-white transition-colors";
                btn.innerHTML = `<i data-lucide="repeat" class="w-4 h-4"></i>`;
                btn.title = "Repeat Off";
                stStatusToast("Repeat OFF");
            } else if (repeatMode === 1) {
                btn.className = "text-rose-500 transition-colors scale-105 relative";
                btn.innerHTML = `<i data-lucide="repeat-1" class="w-4 h-4"></i>`;
                btn.title = "Repeat One";
                stStatusToast("Repeat Current Track");
            } else if (repeatMode === 2) {
                btn.className = "text-cyan-400 transition-colors scale-105";
                btn.innerHTML = `<i data-lucide="repeat" class="w-4 h-4"></i>`;
                btn.title = "Repeat Queue";
                stStatusToast("Repeat Entire Queue");
            }
            lucide.createIcons();
        }
        
        function stStatusToast(msg) {
            const statusEl = document.getElementById('sync-status');
            statusEl.innerText = msg;
            statusEl.className = "font-mono text-cyan-400 opacity-90 transition-all scale-105";
            setTimeout(() => {
                statusEl.innerText = lyricsData.length > 0 ? "Synced Ready" : (plainLyrics ? "Static Lyrics" : "Synced Ready");
                statusEl.className = lyricsData.length > 0 ? "font-mono text-emerald-400 opacity-80" : "font-mono text-zinc-400 opacity-60";
            }, 2500);
        }
        
        // 5. Playback Helpers
        function togglePlayState() {
            if (!player) return;
            // Use our isPlaying flag as fallback since YT.getPlayerState()
            // may return -1/-2 when postMessage bridge is broken in Streamlit iframe
            let state = -1;
            try { state = player.getPlayerState(); } catch(e) {}
            const ytSaysPlaying = (typeof YT !== 'undefined' && state === YT.PlayerState.PLAYING);
            
            if (ytSaysPlaying || isPlaying) {
                player.pauseVideo();
                isPlaying = false;
                manualPause();
                const playIcon = document.getElementById('play-icon');
                if (playIcon) { playIcon.setAttribute('data-lucide', 'pause'); lucide.createIcons(); }
                stopLyricsSync();
            } else {
                player.playVideo();
                isPlaying = true;
                manualPlay();
                const playIcon = document.getElementById('play-icon');
                if (playIcon) { playIcon.setAttribute('data-lucide', 'pause'); lucide.createIcons(); }
                startLyricsSync();
            }

            // ⚡ NEON ADDITION: Sync body class with play state for neon halo intensity
            document.body.classList.toggle('is-playing', isPlaying);
        }
        
        function skipTime(seconds) {
            if (!player) return;
            const curTime = getPlayerTime();
            const duration = player.getDuration() || currentSongDuration;
            let targetTime = curTime + seconds;
            if (targetTime < 0) targetTime = 0;
            if (targetTime > duration) targetTime = duration;
            
            player.seekTo(targetTime, true);
            manualSeek(targetTime);
            updateProgressBar(targetTime);
        }
        
        function onProgressSeek(value) {
            if (!player) return;
            const t = parseFloat(value);
            player.seekTo(t, true);
            manualSeek(t);
            updateProgressBar(t);
        }
        
        function onVolumeChange(value) {
            if (!player) return;
            lastVolume = parseInt(value);
            player.setVolume(lastVolume);
            
            const volIcon = document.getElementById('volume-icon');
            if (lastVolume === 0) {
                volIcon.setAttribute('data-lucide', 'volume-x');
            } else if (lastVolume < 40) {
                volIcon.setAttribute('data-lucide', 'volume-1');
            } else {
                volIcon.setAttribute('data-lucide', 'volume-2');
            }
            lucide.createIcons();
        }
        
        function toggleMute() {
            if (!player) return;
            const volSlider = document.getElementById('volume-slider');
            if (isMuted) {
                player.unMute();
                player.setVolume(lastVolume);
                volSlider.value = lastVolume;
                isMuted = false;
                onVolumeChange(lastVolume);
            } else {
                player.mute();
                volSlider.value = 0;
                isMuted = true;
                document.getElementById('volume-icon').setAttribute('data-lucide', 'volume-x');
                lucide.createIcons();
            }
        }
        
        function onOffsetChange(value) {
            lyricsSyncOffset = parseFloat(value) / 10.0;
            document.getElementById('offset-label').innerText = (lyricsSyncOffset >= 0 ? "+" : "") + lyricsSyncOffset.toFixed(1) + "s";
            syncLyricsNow();
        }
        
        // 6. Lyrics UI rendering
        function buildLyricsUI() {
            const scrollPane = document.getElementById('lyrics-scroll-pane');
            scrollPane.innerHTML = '';
            
            if (lyricsData && lyricsData.length > 0) {
                document.getElementById('lyrics-type-badge').innerText = "Synced";
                document.getElementById('lyrics-type-badge').className = "px-2 py-0.5 text-[9px] font-bold uppercase rounded-full bg-rose-500/20 text-rose-300 border border-rose-500/20";
                document.getElementById('sync-status').innerText = "Synced Ready";
                document.getElementById('sync-status').className = "font-mono text-emerald-400 opacity-80";
                
                lyricsData.forEach((line, index) => {
                    const p = document.createElement('p');
                    p.id = `lyric-line-${index}`;
                    p.className = 'lyric-line';
                    p.innerText = line.text || "•••";
                    p.setAttribute('data-time', line.time);
                    p.onclick = () => seekToLyricTime(line.time);
                    scrollPane.appendChild(p);
                    applyEffectStyle(p, 9999, false);
                });
            } else {
                document.getElementById('lyrics-type-badge').innerText = "Plain Text";
                document.getElementById('lyrics-type-badge').className = "px-2 py-0.5 text-[9px] font-bold uppercase rounded-full bg-zinc-500/20 text-zinc-300 border border-zinc-500/20";
                document.getElementById('sync-status').innerText = "Static Lyrics";
                document.getElementById('sync-status').className = "font-mono text-zinc-400 opacity-60";
                
                if (plainLyrics && plainLyrics.trim().length > 0) {
                    const formattedPlain = plainLyrics.split('\n');
                    formattedPlain.forEach(line => {
                        const p = document.createElement('p');
                        p.className = 'text-sm font-medium text-white/60 py-2.5 transition-all text-center';
                        p.innerText = line.trim() || "";
                        scrollPane.appendChild(p);
                    });
                } else {
                    scrollPane.innerHTML = `
                        <div class="flex flex-col items-center justify-center text-center py-20">
                            <i data-lucide="frown" class="w-10 h-10 text-white/20 mb-3 animate-pulse"></i>
                            <p class="text-white/40 text-xs">Lyrics not found in LRCLIB database.</p>
                            <p class="text-white/20 text-[10px] mt-1">Plain or auto-sync lyrics not loaded.</p>
                        </div>
                    `;
                    lucide.createIcons();
                }
            }
        }
        
        function seekToLyricTime(time) {
            if (!player) return;
            player.seekTo(time + 0.05, true);
            manualSeek(time + 0.05);
            updateProgressBar(time);
            syncLyricsNow();
        }
        
        function startLyricsSync() {
            stopLyricsSync();
            lyricsInterval = setInterval(() => {
                if (!player) return;
                const curTime = getPlayerTime();
                updateProgressBar(curTime);
                syncLyrics(curTime);
                // Write current playback time so Karaoke Studio iframe can sync
                try { localStorage.setItem('melodify_playback_time', curTime.toString()); } catch(e) {}
                checkCrossfade();
            }, 100);
        }
        
        function stopLyricsSync() {
            if (lyricsInterval) {
                clearInterval(lyricsInterval);
            }
        }
        
        function syncLyrics(time) {
            if (!lyricsData || lyricsData.length === 0) return;
            
            const adjustedTime = time + lyricsSyncOffset;
            let activeIndex = -1;
            
            for (let i = 0; i < lyricsData.length; i++) {
                if (adjustedTime >= lyricsData[i].time) {
                    activeIndex = i;
                } else {
                    break;
                }
            }
            
            if (activeIndex !== currentLyricIndex && activeIndex !== -1) {
                if (currentLyricIndex !== -1) {
                    const prevEl = document.getElementById(`lyric-line-${currentLyricIndex}`);
                    if (prevEl) prevEl.classList.remove('active');
                }
                
                const activeEl = document.getElementById(`lyric-line-${activeIndex}`);
                if (activeEl) {
                    activeEl.classList.add('active');
                    
                    const scrollPane = document.getElementById('lyrics-scroll-pane');
                    const scrollOffset = activeEl.offsetTop - (scrollPane.clientHeight / 2) + (activeEl.clientHeight / 2);
                    scrollPane.scrollTo({
                        top: scrollOffset,
                        behavior: 'smooth'
                    });
                }
                
                for (let i = 0; i < lyricsData.length; i++) {
                    const el = document.getElementById(`lyric-line-${i}`);
                    if (el) {
                        const distance = Math.abs(i - activeIndex);
                        applyEffectStyle(el, distance, i === activeIndex);
                    }
                }
                currentLyricIndex = activeIndex;
            }
        }
        
        function toggleFocusMode() {
            isFocusMode = !isFocusMode;
            
            const musicPanel = document.getElementById('music-panel');
            const lyricsPanel = document.getElementById('lyrics-panel');
            const scrollPane = document.getElementById('lyrics-scroll-pane');
            const focusToggleBtn = document.getElementById('focus-toggle-btn');
            const effectsBar = document.getElementById('effects-bar');
            
            if (isFocusMode) {
                musicPanel.classList.add('md:w-0', 'p-0', 'border-r-0', 'opacity-0', 'overflow-hidden');
                musicPanel.classList.remove('md:w-[45%]', 'px-5', 'py-3');
                lyricsPanel.classList.add('md:w-full');
                lyricsPanel.classList.remove('md:w-[55%]');
                scrollPane.classList.add('text-center');
                scrollPane.classList.remove('md:text-left');
                
                focusToggleBtn.innerHTML = `
                    <i data-lucide="minimize-2" class="w-3 h-3 text-rose-400"></i>
                    <span>Normal Mode</span>
                `;
                effectsBar.classList.remove('hidden');
            } else {
                musicPanel.classList.remove('md:w-0', 'p-0', 'border-r-0', 'opacity-0', 'overflow-hidden');
                musicPanel.classList.add('md:w-[45%]', 'px-5', 'py-3');
                lyricsPanel.classList.remove('md:w-full');
                lyricsPanel.classList.add('md:w-[55%]');
                scrollPane.classList.remove('text-center');
                scrollPane.classList.add('md:text-left');
                
                focusToggleBtn.innerHTML = `
                    <i data-lucide="maximize-2" class="w-3 h-3 text-rose-400"></i>
                    <span>Spotify Mode</span>
                `;
                effectsBar.classList.add('hidden');
            }
            lucide.createIcons();
            
            setTimeout(() => {
                resizeCanvas();
                onThreeResize();
            }, 350);
            
            if (player) {
                currentLyricIndex = -1;
                syncLyrics(getPlayerTime());
            }
        }
        
        function setLyricEffect(effect) {
            lyricEffect = effect;
            
            const effects = ['blur', 'scale', 'neon', 'karaoke', 'glitch', 'wave', 'gold'];
            effects.forEach(eff => {
                const btn = document.getElementById(`effect-btn-${eff}`);
                if (btn) {
                    if (eff === effect) {
                        btn.className = "px-2.5 py-1 rounded-lg bg-white/10 text-white font-medium transition-all";
                    } else {
                        btn.className = "px-2.5 py-1 rounded-lg text-white/60 hover:text-white/80 transition-all";
                    }
                }
            });
            
            if (player) {
                currentLyricIndex = -1;
                syncLyrics(getPlayerTime());
            }
        }
        
        function applyEffectStyle(el, distance, isActive) {
            el.removeAttribute('style');
            el.className = 'lyric-line py-2 transition-all duration-300 cursor-pointer hover:scale-[1.03] active:scale-95';
            
            const themeObj = themes[currentTheme];
            
            if (lyricEffect === 'blur') {
                el.classList.add('text-base', 'font-medium');
                if (isActive) {
                    el.classList.add('active');
                    el.style.opacity = "1";
                    el.style.filter = "blur(0px)";
                    el.style.transform = "scale(1.05)";
                    el.style.fontWeight = "700";
                    el.style.color = themeObj.accent;
                    el.style.textShadow = `0 0 15px ${themeObj.glow}`;
                } else {
                    if (distance === 1) {
                        el.style.opacity = "0.45";
                        el.style.filter = "blur(1px)";
                        el.style.transform = "scale(0.97)";
                        el.style.color = "rgba(255, 255, 255, 0.8)";
                    } else if (distance === 2) {
                        el.style.opacity = "0.25";
                        el.style.filter = "blur(2px)";
                        el.style.transform = "scale(0.93)";
                        el.style.color = "rgba(255, 255, 255, 0.7)";
                    } else {
                        el.style.opacity = "0.12";
                        el.style.filter = "blur(3.5px)";
                        el.style.transform = "scale(0.9)";
                        el.style.color = "rgba(255, 255, 255, 0.5)";
                    }
                }
            } 
            else if (lyricEffect === 'scale') {
                el.classList.add('text-base');
                if (isActive) {
                    el.classList.add('active');
                    el.style.opacity = "1";
                    el.style.transform = "scale(1.20)";
                    el.style.fontWeight = "800";
                    el.style.color = themeObj.accent;
                    el.style.textShadow = `0 0 20px ${themeObj.glow}`;
                    el.style.transition = "all 0.15s ease-out";
                } else {
                    if (distance === 1) {
                        el.style.opacity = "0.6";
                        el.style.transform = "scale(0.96)";
                        el.style.color = "rgba(255, 255, 255, 0.7)";
                    } else {
                        el.style.opacity = "0.35";
                        el.style.transform = "scale(0.88)";
                        el.style.color = "rgba(255, 255, 255, 0.5)";
                    }
                }
            }
            else if (lyricEffect === 'neon') {
                el.classList.add('text-base', 'font-medium');
                if (isActive) {
                    el.classList.add('active');
                    el.style.opacity = "1";
                    el.style.transform = "scale(1.05)";
                    el.style.fontWeight = "700";
                    el.style.color = themeObj.accent;
                    el.style.textShadow = `0 0 20px ${themeObj.accent}, 0 0 10px ${themeObj.accent}`;
                    el.style.animation = "neonPulse 2.5s linear infinite";
                } else {
                    if (distance === 1) {
                        el.style.opacity = "0.55";
                        el.style.transform = "scale(0.97)";
                        el.style.color = "rgba(255, 255, 255, 0.7)";
                    } else {
                        el.style.opacity = "0.3";
                        el.style.transform = "scale(0.93)";
                        el.style.color = "rgba(255, 255, 255, 0.5)";
                    }
                }
            }
            else if (lyricEffect === 'karaoke') {
                el.classList.add('font-mono', 'text-sm');
                if (isActive) {
                    el.classList.add('active');
                    el.style.opacity = "1";
                    el.style.fontWeight = "800";
                    el.style.background = `linear-gradient(to right, ${themeObj.accent} 0%, ${themeObj.accent} var(--progress, 0%), rgba(255, 255, 255, 0.35) var(--progress, 0%))`;
                    el.style.webkitBackgroundClip = "text";
                    el.style.webkitTextFillColor = "transparent";
                    el.style.backgroundClip = "text";
                } else {
                    el.style.color = "rgba(255, 255, 255, 0.35)";
                    if (distance === 1) {
                        el.style.opacity = "0.5";
                        el.style.transform = "scale(0.97)";
                    } else {
                        el.style.opacity = "0.3";
                        el.style.transform = "scale(0.94)";
                    }
                }
            }
            // ── Glitch Cyber effect ────────────────────────────────────────────────
            else if (lyricEffect === 'glitch') {
                el.classList.add('text-base', 'font-bold');
                if (isActive) {
                    el.classList.add('active', 'lyric-glitch-active');
                    el.setAttribute('data-text', el.innerText);
                    el.style.opacity = '1';
                    el.style.color = themeObj.accent;
                    el.style.transform = 'scale(1.06)';
                    el.style.letterSpacing = '0.02em';
                } else {
                    el.classList.remove('lyric-glitch-active');
                    el.removeAttribute('data-text');
                    if (distance === 1) {
                        el.style.opacity = '0.45'; el.style.color = 'rgba(255,255,255,0.7)';
                    } else {
                        el.style.opacity = '0.15'; el.style.color = 'rgba(255,255,255,0.35)';
                    }
                }
            }
            // ── Wave Pulse effect ─────────────────────────────────────────────────
            else if (lyricEffect === 'wave') {
                el.classList.add('text-base', 'font-semibold');
                if (isActive) {
                    el.classList.add('active');
                    el.style.opacity = '1';
                    el.style.color = themeObj.accent;
                    el.style.transform = 'scale(1.08) translateY(-3px)';
                    el.style.textShadow = `0 6px 20px ${themeObj.glow}, 0 0 8px ${themeObj.glow}`;
                    el.style.animation = 'wavePulse 0.8s ease-in-out infinite';
                    el.style.fontWeight = '700';
                } else {
                    el.style.animation = 'none';
                    if (distance === 1) {
                        el.style.opacity = '0.5';
                        el.style.transform = 'scale(0.97) translateY(1px)';
                        el.style.color = 'rgba(255,255,255,0.75)';
                    } else if (distance === 2) {
                        el.style.opacity = '0.25';
                        el.style.transform = 'scale(0.92)';
                        el.style.color = 'rgba(255,255,255,0.5)';
                    } else {
                        el.style.opacity = '0.10';
                        el.style.transform = 'scale(0.88)';
                        el.style.color = 'rgba(255,255,255,0.3)';
                    }
                }
            }
            // ── Gold Slide effect ─────────────────────────────────────────────────
            else if (lyricEffect === 'gold') {
                el.classList.add('text-base');
                if (isActive) {
                    el.classList.add('active', 'lyric-gold-active');
                    el.style.fontWeight = '800';
                    el.style.transform = 'scale(1.08)';
                    el.style.fontSize = '1.05rem';
                    el.style.letterSpacing = '0.03em';
                } else {
                    el.classList.remove('lyric-gold-active');
                    if (distance === 1) {
                        el.style.opacity = '0.5';
                        el.style.color = 'rgba(251,191,36,0.45)';
                        el.style.transform = 'scale(0.96)';
                    } else {
                        el.style.opacity = '0.2';
                        el.style.color = 'rgba(255,255,255,0.4)';
                        el.style.transform = 'scale(0.91)';
                    }
                }
            }
        }
        
        function syncLyricsNow() {
            if (player) {
                syncLyrics(getPlayerTime());
            }
        }
        
        
        // 7. View Mode Toggling
        function togglePlayMode() {
            const audioView = document.getElementById('audio-view');
            const videoView = document.getElementById('video-view');
            const modeBtn = document.getElementById('mode-toggle-btn');
            
            isVideoMode = !isVideoMode;
            if (isVideoMode) {
                audioView.classList.add('opacity-0');
                document.getElementById('three-visualizer-container').classList.add('opacity-0');
                document.getElementById('visualizer-canvas').classList.add('opacity-0');
                
                setTimeout(() => {
                    audioView.classList.add('hidden');
                    videoView.classList.remove('hidden');
                    videoView.classList.add('opacity-100');
                }, 300);
                
                modeBtn.innerHTML = `
                    <i data-lucide="music" class="w-3.5 h-3.5"></i>
                    <span>Switch to Audio</span>
                `;
                // User pressed it — remove the neon highlight
                modeBtn.classList.remove('neon-cta');
            } else {
                videoView.classList.remove('opacity-100');
                videoView.classList.add('opacity-0');
                setTimeout(() => {
                    videoView.classList.add('hidden');
                    videoView.classList.remove('opacity-0');
                    audioView.classList.remove('hidden');
                    document.getElementById('three-visualizer-container').classList.remove('opacity-0');
                    document.getElementById('visualizer-canvas').classList.remove('opacity-0');
                    setTimeout(() => {
                        audioView.classList.remove('opacity-0');
                    }, 30);
                }, 280);
                
                modeBtn.innerHTML = `
                    <i data-lucide="video" class="w-3.5 h-3.5"></i>
                    <span>Switch to Video</span>
                `;
                // Back to audio — re-add neon highlight to prompt again
                modeBtn.classList.add('neon-cta');
            }
            lucide.createIcons();
        }
        
        function formatTime(seconds) {
            if (isNaN(seconds) || seconds === undefined) return "00:00";
            const m = Math.floor(seconds / 60);
            const s = Math.floor(seconds % 60);
            return (m < 10 ? "0" + m : m) + ":" + (s < 10 ? "0" + s : s);
        }
        
        // 8. 2D Visualizers Implementation
        function initVisualizer() {
            canvas = document.getElementById('visualizer-canvas');
            ctx = canvas.getContext('2d');
            resizeCanvas();
            window.addEventListener('resize', resizeCanvas);
            drawVisualizer();
        }
        
        function resizeCanvas() {
            if (canvas) {
                canvas.width = canvas.parentElement.clientWidth;
                canvas.height = canvas.parentElement.clientHeight;
            }
        }
        
        function setVisualizerStyle(style) {
            visualizerStyle = style;
            const styles = ['wave', 'radial', 'orb', 'grid', 'tunnel', 'spectrum', 'galaxy', 'stars', 'city'];
            
            styles.forEach(s => {
                const btn = document.getElementById(`viz-btn-${s}`);
                if (btn) {
                    if (s === style) {
                        btn.className = "px-1 py-0.5 rounded text-[8px] bg-white/10 text-white font-medium transition-all";
                    } else {
                        btn.className = "px-1 py-0.5 rounded text-[8px] text-white/60 hover:text-white font-medium transition-all";
                    }
                }
            });
            
            const canvas2d = document.getElementById('visualizer-canvas');
            const container3d = document.getElementById('three-visualizer-container');
            const vinyl = document.getElementById('vinyl-record');
            
            const is3d = ['orb','grid','tunnel','spectrum','galaxy','stars','city'].includes(style);
            if (is3d) {
                canvas2d.style.display = 'none';
                container3d.style.display = 'block';
                if(vinyl) vinyl.style.opacity = '0.25';
                
                if(active3dMesh)     active3dMesh.visible     = (style === 'orb');
                if(active3dGrid)     active3dGrid.visible     = (style === 'grid');
                if(active3dSun)      active3dSun.visible      = (style === 'grid');
                if(active3dTunnel)   active3dTunnel.visible   = (style === 'tunnel');
                if(active3dSpectrum) active3dSpectrum.visible = (style === 'spectrum');
                if(active3dGalaxy)   active3dGalaxy.visible   = (style === 'galaxy');
                if(active3dStars)    active3dStars.visible    = (style === 'stars');
                if(active3dCity)     active3dCity.visible     = (style === 'city');
                onThreeResize();
            } else {
                canvas2d.style.display = 'block';
                container3d.style.display = 'none';
                if(vinyl) vinyl.style.opacity = '1.0';
            }
            
            if (ctx && canvas) {
                ctx.clearRect(0, 0, canvas.width, canvas.height);
            }
        }
        
        // Recursive helper to update color across nesting [PURE ADDITION]
        function updateColor(obj, colorHex) {
            if (obj.material) {
                if (obj.material.color) {
                    obj.material.color.setHex(colorHex);
                }
            }
            if (obj.children) {
                obj.children.forEach(child => updateColor(child, colorHex));
            }
        }

        function setTheme(themeName) {
            if (!themes[themeName]) return;
            currentTheme = themeName;
            const t = themes[themeName];
            
            const themeKeys = Object.keys(themes);
            themeKeys.forEach(k => {
                const btn = document.getElementById(`theme-btn-${k}`);
                if (btn) {
                    if (k === themeName) {
                        btn.className = "w-3 h-3 rounded-full border border-white/40 ring-2 ring-white/20 transition-all scale-110";
                    } else {
                        btn.className = "w-3 h-3 rounded-full opacity-60 hover:opacity-100 transition-all hover:scale-105";
                    }
                }
            });
            
            const orb1 = document.getElementById('orb-1');
            const orb2 = document.getElementById('orb-2');
            const orb3 = document.getElementById('orb-3');
            
            if (orb1) orb1.style.background = `radial-gradient(circle, ${t.orbs[0]} 0%, transparent 70%)`;
            if (orb2) orb2.style.background = `radial-gradient(circle, ${t.orbs[1]} 0%, transparent 70%)`;
            if (orb3) orb3.style.background = `radial-gradient(circle, ${t.orbs[2]} 0%, transparent 70%)`;
            
            const playBtn = document.getElementById('play-pause-btn');
            if (playBtn) {
                playBtn.style.backgroundColor = t.accent;
                playBtn.style.boxShadow = `0 10px 25px -5px ${t.glow}`;
            }

            // Update Ambient Ambilight Backglow [PURE ADDITION]
            const ambilight = document.getElementById('player-ambilight-glow');
            if (ambilight) {
                ambilight.style.background = t.accent;
            }

            // Update interactive cursor spotlight [PURE ADDITION]
            const cursorGlow = document.getElementById('interactive-cursor-glow');
            if (cursorGlow) {
                cursorGlow.style.background = `radial-gradient(circle, ${t.accent}1c 0%, transparent 70%)`;
            }
            
            // Apply theme colors recursively to all Three.js elements
            if (active3dMesh)     updateColor(active3dMesh, t.threeHex);
            if (active3dGrid)     updateColor(active3dGrid, t.threeHex);
            if (active3dSun)      updateColor(active3dSun, t.threeHex);
            if (active3dTunnel)   updateColor(active3dTunnel, t.threeHex);
            if (active3dSpectrum) updateColor(active3dSpectrum, t.threeHex);
            if (active3dGalaxy)   updateColor(active3dGalaxy, t.threeHex);
            if (active3dStars)    updateColor(active3dStars, t.threeHex);
            if (active3dCity)     updateColor(active3dCity, t.threeHex);

            // Update 3D Light colors dynamically [PURE ADDITION]
            if (activeAmbientLight) {
                activeAmbientLight.color.setHex(t.threeHex);
            }
            if (activePointLight) {
                activePointLight.color.setHex(t.threeHex);
            }
            if (activePointLight2) {
                activePointLight2.color.setHex(t.complementaryHex || 0xffffff);
            }
            
            syncLyricsNow();
            // Repaint waveform scrubber with new theme colour
            if (player) drawWaveformScrubber((getPlayerTime()||0) / (currentSongDuration||1));
            // Apply body theme class for CSS-driven theme overrides
            document.body.classList.remove('theme-holo','theme-matrix','theme-ice');
            if (themeName === 'holo') document.body.classList.add('theme-holo');
            if (themeName === 'matrix') document.body.classList.add('theme-matrix');
            if (themeName === 'ice') document.body.classList.add('theme-ice');

            // ⚡ NEON ADDITION: Update Three.js particle field colors on theme change
            if (window.updateNeonParticleTheme) {
                const themeAccents = {
                    rose: '#f43f5e', aurora: '#10b981', cyberpunk: '#d946ef',
                    ocean: '#6366f1', amber: '#f59e0b', matrix: '#00ff50',
                    ice: '#67e8f9', holo: '#a855f7', lava: '#f97316'
                };
                window.updateNeonParticleTheme(themeAccents[themeName] || '#f43f5e');
            }
        }
        
        function setEqualizerPreset(preset) {
            eqPreset = preset;
            const presets = ['flat', 'bass', 'vocals', 'concert', 'cyber', 'lofi', 'hifi', 'night'];
            
            presets.forEach(p => {
                const btn = document.getElementById(`eq-btn-${p}`);
                if (btn) {
                    if (p === preset) {
                        btn.className = "px-1 py-0.5 rounded text-[8px] bg-white/10 text-white font-medium transition-all";
                    } else {
                        btn.className = "px-1 py-0.5 rounded text-[8px] text-white/60 hover:text-white font-medium transition-all";
                    }
                }
            });
            
            const labels = {
                flat: "DSP: Studio Flat",
                bass: "DSP: Bass Booster 🔥",
                vocals: "DSP: Vocal Enhancer ✨",
                concert: "DSP: 3D Concert Hall 🪐",
                cyber: "DSP: Electronic Space ⚡",
                lofi: "DSP: Lo-Fi Chill 🎧",
                hifi: "DSP: Hi-Fi Audiophile 🎵",
                night: "DSP: Night Mode 🌙"
            };
            
            stStatusToast(labels[preset] || "DSP Equalizer Updated");
            
            if (ctx && canvas) {
                ctx.clearRect(0, 0, canvas.width, canvas.height);
            }
        }

        // ════════════════════════════════════════════════════
        //  ✨ FULLSCREEN TOGGLE  (Added feature)
        // ════════════════════════════════════════════════════
        let isFullscreen = false;
        function toggleFullscreen() {
            isFullscreen = !isFullscreen;
            const body = document.body;
            const wrapper = document.getElementById('player-fullscreen-wrapper');
            const btn = document.getElementById('fullscreen-btn');
            const btnIcon = btn ? btn.querySelector('i[data-lucide]') : null;
            const btnSpan = btn ? btn.querySelector('span') : null;

            if (isFullscreen) {
                body.classList.add('fullscreen-active');
                if (btnIcon) { btnIcon.setAttribute('data-lucide', 'shrink'); lucide.createIcons(); }
                if (btnSpan) btnSpan.textContent = 'Exit Full';
                if (btn) {
                    btn.title = 'Exit Fullscreen';
                    btn.classList.add('border-rose-500/50');
                }
                stStatusToast('🖥 Fullscreen Mode ON — Press Esc to exit');
            } else {
                body.classList.remove('fullscreen-active');
                if (btnIcon) { btnIcon.setAttribute('data-lucide', 'expand'); lucide.createIcons(); }
                if (btnSpan) btnSpan.textContent = 'Full Screen';
                if (btn) {
                    btn.title = 'Toggle Fullscreen';
                    btn.classList.remove('border-rose-500/50');
                }
                stStatusToast('⬛ Exited Fullscreen');
            }
            // Resize 3D renderer if active
            setTimeout(() => {
                if (renderer3d) {
                    const c = document.getElementById('three-visualizer-container');
                    if (c) renderer3d.setSize(c.clientWidth, c.clientHeight);
                }
            }, 500);
        }
        // Allow Esc to exit fullscreen
        document.addEventListener('keydown', (e) => {
            if (e.key === 'Escape' && isFullscreen) toggleFullscreen();
        });

        // ════════════════════════════════════════════════════
        //  ✨ NEON FLOATING PARTICLES  (Added visual effect)
        // ════════════════════════════════════════════════════
        (function initNeonParticles() {
            const canvas = document.getElementById('neon-particles-canvas');
            if (!canvas) return;
            const ctx2 = canvas.getContext('2d');
            let W = canvas.width = window.innerWidth;
            let H = canvas.height = window.innerHeight;
            window.addEventListener('resize', () => {
                W = canvas.width = window.innerWidth;
                H = canvas.height = window.innerHeight;
            });
            const COLORS = ['#f43f5e','#a855f7','#06b6d4','#fbbf24','#22c55e'];
            const particles = Array.from({length: 55}, () => ({
                x: Math.random() * W,
                y: Math.random() * H,
                r: Math.random() * 1.8 + 0.4,
                vx: (Math.random() - 0.5) * 0.35,
                vy: (Math.random() - 0.5) * 0.35,
                color: COLORS[Math.floor(Math.random() * COLORS.length)],
                alpha: Math.random() * 0.5 + 0.15,
                pulse: Math.random() * Math.PI * 2
            }));
            function drawParticles() {
                ctx2.clearRect(0, 0, W, H);
                const t = Date.now() * 0.0008;
                particles.forEach(p => {
                    p.x += p.vx; p.y += p.vy;
                    p.pulse += 0.015;
                    if (p.x < 0) p.x = W; if (p.x > W) p.x = 0;
                    if (p.y < 0) p.y = H; if (p.y > H) p.y = 0;
                    const a = p.alpha * (0.6 + 0.4 * Math.sin(p.pulse));
                    ctx2.beginPath();
                    const grd = ctx2.createRadialGradient(p.x, p.y, 0, p.x, p.y, p.r * 4);
                    grd.addColorStop(0, p.color + Math.round(a * 255).toString(16).padStart(2,'0'));
                    grd.addColorStop(1, 'transparent');
                    ctx2.arc(p.x, p.y, p.r * 4, 0, Math.PI * 2);
                    ctx2.fillStyle = grd;
                    ctx2.fill();
                });
                requestAnimationFrame(drawParticles);
            }
            drawParticles();
        })();
        
        // 9. Three.js 3D Visualizer Core Engine (Mind-blowing visual premium logic)
        function initThreeJS() {
            const container = document.getElementById('three-visualizer-container');
            if (!container) return;
            
            scene3d = new THREE.Scene();
            
            // Perspective Camera
            camera3d = new THREE.PerspectiveCamera(50, container.clientWidth / container.clientHeight, 0.1, 100);
            camera3d.position.z = 6;
            
            // WebGL Renderer
            renderer3d = new THREE.WebGLRenderer({ alpha: true, antialias: true });
            renderer3d.setSize(container.clientWidth, container.clientHeight);
            renderer3d.setPixelRatio(Math.min(window.devicePixelRatio, 2));
            container.appendChild(renderer3d.domElement);

            // [PURE ADDITION]: Instantiate Ambient and Point lights
            activeAmbientLight = new THREE.AmbientLight(0xffffff, 0.55);
            scene3d.add(activeAmbientLight);

            activePointLight = new THREE.PointLight(0xffffff, 2.0, 15);
            activePointLight.position.set(3, 3, 4);
            scene3d.add(activePointLight);

            activePointLight2 = new THREE.PointLight(0xffffff, 1.5, 15);
            activePointLight2.position.set(-3, -3, 4);
            scene3d.add(activePointLight2);
            
            // Create the 3D meshes
            createThreeOrb();
            createThreeGrid();
            createThreeTunnel();
            createThreeSpectrum();
            createThreeGalaxy();
            createThreeStarfield();
            createThreeCity();
            createThreeParticles();
            
            // Trigger theme color update
            setTheme(currentTheme);
            
            // Hide 3D meshes initially since 2D Wave is default
            active3dMesh.visible    = false;
            active3dGrid.visible    = false;
            active3dSun.visible     = false;
            active3dTunnel.visible  = false;
            if (active3dSpectrum) active3dSpectrum.visible = false;
            if (active3dGalaxy)   active3dGalaxy.visible   = false;
            if (active3dStars)    active3dStars.visible    = false;
            if (active3dCity)     active3dCity.visible     = false;
            
            // Start rendering loop
            animateThreeJS();
        }
        
        function onThreeResize() {
            const container = document.getElementById('three-visualizer-container');
            if (!container || !renderer3d || !camera3d) return;
            
            camera3d.aspect = container.clientWidth / container.clientHeight;
            camera3d.updateProjectionMatrix();
            renderer3d.setSize(container.clientWidth, container.clientHeight);
        }
        
        function createThreeOrb() {
            // High fidelity 3D Icosahedron wireframe
            const geom = new THREE.IcosahedronGeometry(1.6, 3);
            
            // Save original positions to deform dynamically
            geom.userData = {
                originalPositions: geom.attributes.position.clone()
            };
            
            const mat = new THREE.MeshBasicMaterial({
                color: 0xf43f5e,
                wireframe: true,
                transparent: true,
                opacity: 0.15
            });
            active3dMesh = new THREE.Mesh(geom, mat);

            // [PURE ADDITION]: Nested solid shiny glossy Phong core
            const innerGeom = new THREE.IcosahedronGeometry(1.3, 3);
            innerGeom.userData = {
                originalPositions: innerGeom.attributes.position.clone()
            };
            const innerMat = new THREE.MeshPhongMaterial({
                color: 0xf43f5e,
                shininess: 90,
                specular: 0xffffff,
                transparent: true,
                opacity: 0.75,
                flatShading: true
            });
            const innerMesh = new THREE.Mesh(innerGeom, innerMat);
            innerMesh.name = "innerCore";
            active3dMesh.add(innerMesh);
            
            // Add particles on vertices for premium cyber glow
            const pointsMat = new THREE.PointsMaterial({
                size: 0.045,
                color: 0xf43f5e,
                transparent: true,
                opacity: 0.75
            });
            const points = new THREE.Points(geom, pointsMat);
            active3dMesh.add(points);
            
            scene3d.add(active3dMesh);
        }
        
        function createThreeGrid() {
            // Retro synthwave neon plane
            const gridGeom = new THREE.PlaneGeometry(16, 16, 20, 20);
            const gridMat = new THREE.MeshBasicMaterial({
                color: 0xa855f7,
                wireframe: true,
                transparent: true,
                opacity: 0.3
            });
            active3dGrid = new THREE.Mesh(gridGeom, gridMat);
            active3dGrid.rotation.x = -Math.PI / 2.2;
            active3dGrid.position.y = -1.2;
            active3dGrid.position.z = -1;
            
            // Retro neon wireframe sun
            const sunGeom = new THREE.CircleGeometry(1.8, 24);
            const sunMat = new THREE.MeshBasicMaterial({
                color: 0xf43f5e,
                wireframe: true,
                transparent: true,
                opacity: 0.45
            });
            active3dSun = new THREE.Mesh(sunGeom, sunMat);
            active3dSun.position.set(0, 0.8, -6);
            
            scene3d.add(active3dGrid);
            scene3d.add(active3dSun);
        }
        
        function createThreeTunnel() {
            // Cyberpunk particle wormhole
            const count = 360;
            const geom = new THREE.BufferGeometry();
            const posArray = new Float32Array(count * 3);
            
            for (let i = 0; i < count; i++) {
                const angle = (i / 18) * Math.PI * 2;
                const r = 2.0 + Math.random() * 0.3;
                const x = Math.cos(angle) * r;
                const y = Math.sin(angle) * r;
                const z = - (i * 0.06); 
                
                posArray[i*3] = x;
                posArray[i*3+1] = y;
                posArray[i*3+2] = z;
            }
            geom.setAttribute('position', new THREE.BufferAttribute(posArray, 3));
            
            const mat = new THREE.PointsMaterial({
                size: 0.06,
                color: 0x06b6d4,
                transparent: true,
                opacity: 0.75
            });
            
            active3dTunnel = new THREE.Points(geom, mat);
            scene3d.add(active3dTunnel);
        }
        
        function createThreeSpectrum() {
            // 3D Neon Pillar Equalizer Circle Group
            const group = new THREE.Group();
            const numBars = 36;
            const radius = 2.1;
            const barWidth = 0.12;
            const barDepth = 0.12;
            
            active3dSpectrumBars = [];
            
            for (let i = 0; i < numBars; i++) {
                const angle = (i / numBars) * Math.PI * 2;
                const geom = new THREE.BoxGeometry(barWidth, 1.2, barDepth);
                geom.translate(0, 0.6, 0); // Move origin to base for vertical scaling
                
                const mat = new THREE.MeshBasicMaterial({
                    color: 0xf43f5e,
                    wireframe: true,
                    transparent: true,
                    opacity: 0.35
                });
                const bar = new THREE.Mesh(geom, mat);

                // [PURE ADDITION]: Nested solid Phong core inside each bar wireframe
                const innerBarGeom = new THREE.BoxGeometry(barWidth * 0.7, 1.2, barDepth * 0.7);
                innerBarGeom.translate(0, 0.6, 0);
                const innerBarMat = new THREE.MeshPhongMaterial({
                    color: 0xf43f5e,
                    shininess: 80,
                    specular: 0xffffff,
                    transparent: true,
                    opacity: 0.65
                });
                const innerBar = new THREE.Mesh(innerBarGeom, innerBarMat);
                innerBar.name = "innerBar";
                bar.add(innerBar);
                
                bar.position.x = Math.cos(angle) * radius;
                bar.position.z = Math.sin(angle) * radius;
                bar.position.y = -1.0;
                
                // Align bar facing the center
                bar.rotation.y = -angle;
                
                group.add(bar);
                active3dSpectrumBars.push(bar);
            }
            
            // Central beat-responsive wireframe sphere
            const sphereGeom = new THREE.SphereGeometry(0.55, 12, 12);
            const sphereMat = new THREE.MeshBasicMaterial({
                color: 0xf43f5e,
                wireframe: true,
                transparent: true,
                opacity: 0.2
            });
            active3dSpectrumSphere = new THREE.Mesh(sphereGeom, sphereMat);
            active3dSpectrumSphere.position.y = -0.4;

            // [PURE ADDITION]: Nested solid Phong sphere inside the central sphere
            const innerSphereGeom = new THREE.SphereGeometry(0.43, 16, 16);
            const innerSphereMat = new THREE.MeshPhongMaterial({
                color: 0xf43f5e,
                shininess: 100,
                specular: 0xffffff,
                transparent: true,
                opacity: 0.8
            });
            const innerSphere = new THREE.Mesh(innerSphereGeom, innerSphereMat);
            innerSphere.name = "innerSphere";
            active3dSpectrumSphere.add(innerSphere);
            
            group.add(active3dSpectrumSphere);
            
            active3dSpectrum = group;
            scene3d.add(active3dSpectrum);
        }
        
        function createThreeGalaxy() {
            // 3D Organic Gravity Vortex
            const count = 1200;
            const geom = new THREE.BufferGeometry();
            const positions = new Float32Array(count * 3);
            const originalPositions = new Float32Array(count * 3);
            const velocities = new Float32Array(count);
            const angles = new Float32Array(count);
            const distances = new Float32Array(count);
            
            for (let i = 0; i < count; i++) {
                const dist = 0.4 + Math.random() * 2.8;
                const angle = Math.random() * Math.PI * 2;
                const speed = 0.01 + Math.random() * 0.03;
                
                distances[i] = dist;
                angles[i] = angle;
                velocities[i] = speed;
                
                const x = Math.cos(angle) * dist;
                const z = Math.sin(angle) * dist;
                const y = (Math.random() - 0.5) * 0.3 * (3.0 - dist); // Swarm thickness fades toward edges
                
                positions[i * 3] = x;
                positions[i * 3 + 1] = y;
                positions[i * 3 + 2] = z;
                
                originalPositions[i * 3] = x;
                originalPositions[i * 3 + 1] = y;
                originalPositions[i * 3 + 2] = z;
            }
            
            geom.setAttribute('position', new THREE.BufferAttribute(positions, 3));
            
            const mat = new THREE.PointsMaterial({
                size: 0.05,
                color: 0xf43f5e,
                transparent: true,
                opacity: 0.8
            });
            
            active3dGalaxy = new THREE.Points(geom, mat);
            active3dGalaxy.userData = {
                distances: distances,
                angles: angles,
                velocities: velocities,
                originalPositions: originalPositions
            };
            
            scene3d.add(active3dGalaxy);
        }
        
        // ── NEW: Starfield warp speed ──────────────────────────────────────────
        function createThreeStarfield() {
            const count = 2000;
            const geom = new THREE.BufferGeometry();
            const positions = new Float32Array(count * 3);
            const speeds    = new Float32Array(count);
            
            for (let i = 0; i < count; i++) {
                positions[i*3]   = (Math.random() - 0.5) * 20;
                positions[i*3+1] = (Math.random() - 0.5) * 20;
                positions[i*3+2] = (Math.random() - 0.5) * 30 - 5;
                speeds[i] = 0.04 + Math.random() * 0.18;
            }
            geom.setAttribute('position', new THREE.BufferAttribute(positions, 3));
            const mat = new THREE.PointsMaterial({
                size: 0.06, color: 0xffffff,
                transparent: true, opacity: 0.85
            });
            active3dStars = new THREE.Points(geom, mat);
            active3dStars.userData = { speeds };
            scene3d.add(active3dStars);
        }
        
        // ── NEW: City skyline equalizer ────────────────────────────────────────
        function createThreeCity() {
            const group = new THREE.Group();
            const cols   = 18;
            const spacing = 0.65;
            active3dCityBars = [];
            
            for (let i = 0; i < cols; i++) {
                const h = 0.4 + Math.random() * 2.2;
                const geom = new THREE.BoxGeometry(0.38, h, 0.38);
                geom.translate(0, h / 2, 0);
                const mat = new THREE.MeshBasicMaterial({
                    color: 0xa855f7, wireframe: true,
                    transparent: true, opacity: 0.5
                });
                const bar = new THREE.Mesh(geom, mat);

                // [PURE ADDITION]: Nested solid Phong core inside each city skyscraper building
                const innerCityGeom = new THREE.BoxGeometry(0.38 * 0.7, h, 0.38 * 0.7);
                innerCityGeom.translate(0, h / 2, 0);
                const innerCityMat = new THREE.MeshPhongMaterial({
                    color: 0xa855f7,
                    shininess: 75,
                    specular: 0xffffff,
                    transparent: true,
                    opacity: 0.6
                });
                const innerCity = new THREE.Mesh(innerCityGeom, innerCityMat);
                innerCity.name = "innerCityBlock";
                bar.add(innerCity);
                
                bar.position.x = (i - cols / 2) * spacing;
                bar.position.y = -1.6;
                bar.position.z = -1.5 + (Math.random() - 0.5) * 2.0;
                bar.userData = { baseH: h, phase: Math.random() * Math.PI * 2 };
                group.add(bar);
                active3dCityBars.push(bar);
            }
            
            // Ground plane
            const groundGeom = new THREE.PlaneGeometry(14, 6, 10, 4);
            const groundMat  = new THREE.MeshBasicMaterial({
                color: 0x6366f1, wireframe: true, transparent: true, opacity: 0.15
            });
            const ground = new THREE.Mesh(groundGeom, groundMat);
            ground.rotation.x = -Math.PI / 2;
            ground.position.y = -1.6;
            group.add(ground);
            
            active3dCity = group;
            scene3d.add(active3dCity);
        }

        function createThreeParticles() {
            const count = 120;
            const geom = new THREE.BufferGeometry();
            const posArray = new Float32Array(count * 3);
            
            for (let i = 0; i < count; i++) {
                posArray[i * 3] = (Math.random() - 0.5) * 8;
                posArray[i * 3 + 1] = (Math.random() - 0.5) * 8;
                posArray[i * 3 + 2] = (Math.random() - 0.5) * 6 - 2;
            }
            
            geom.setAttribute('position', new THREE.BufferAttribute(posArray, 3));
            const mat = new THREE.PointsMaterial({
                size: 0.05,
                color: 0xffffff,
                transparent: true,
                opacity: 0.4
            });
            
            threeParticles = new THREE.Points(geom, mat);
            scene3d.add(threeParticles);
        }
        
        function animateThreeJS() {
            requestAnimationFrame(animateThreeJS);
            if (!renderer3d || !scene3d || !camera3d) return;
            
            const time = Date.now() * 0.001;

            // [PURE ADDITION]: Orbit dynamic point lights around the 3D visualizers to sweep highlights across Phong cores
            if (activePointLight) {
                activePointLight.position.x = Math.cos(time * 1.5) * 4;
                activePointLight.position.y = Math.sin(time * 1.0) * 2;
                activePointLight.position.z = 3 + Math.sin(time * 1.5) * 2;
                activePointLight.intensity = 1.2 + (visualizerAmp / 45) * 2.8;
            }
            if (activePointLight2) {
                activePointLight2.position.x = -Math.cos(time * 1.2) * 4;
                activePointLight2.position.y = -Math.sin(time * 0.8) * 2;
                activePointLight2.position.z = 3 + Math.cos(time * 1.2) * 2;
                activePointLight2.intensity = 0.8 + (visualizerAmp / 45) * 2.2;
            }
            
            // Interpolate mouse coordinates smoothly for parallax effect
            mouseX += (targetMouseX - mouseX) * 0.05;
            mouseY += (targetMouseY - mouseY) * 0.05;
            
            // Animate threeParticles (Premium star falling particle field attracted to mouse)
            if (threeParticles && threeParticles.geometry) {
                const pos = threeParticles.geometry.attributes.position;
                let speed = 0.006 + (visualizerAmp / 45) * 0.012;
                if (eqPreset === 'bass') speed *= 1.6;
                if (eqPreset === 'cyber') speed *= 2.2;
                if (eqPreset === 'concert') speed *= 0.5;
                
                for (let i = 0; i < pos.count; i++) {
                    let y = pos.getY(i);
                    y -= speed;
                    if (y < -4) {
                        y = 4;
                        pos.setX(i, (Math.random() - 0.5) * 8);
                    }
                    pos.setY(i, y);
                    
                    let x = pos.getX(i);
                    x += (mouseX * 2.5 - x) * 0.003;
                    pos.setX(i, x);
                }
                pos.needsUpdate = true;
                
                const t = themes[currentTheme];
                threeParticles.material.color.setHex(t.threeHex);
            }
            
            // Rotate camera slightly to make grid/mesh look organic & alive
            if (visualizerStyle === 'orb') {
                active3dMesh.rotation.y = time * (eqPreset === 'cyber' ? 0.35 : 0.15);
                active3dMesh.rotation.x = time * 0.08;
                
                // Deform Orb based on simulated beat frequencies and EQ presets
                const geom = active3dMesh.geometry;
                const pos = geom.attributes.position;
                const orig = geom.userData.originalPositions;
                let displacement = visualizerAmp * 0.012;
                if (eqPreset === 'bass') displacement *= 2.2;
                if (eqPreset === 'vocals') displacement *= 0.55;
                
                for (let i = 0; i < pos.count; i++) {
                    const x = orig.getX(i);
                    const y = orig.getY(i);
                    const z = orig.getZ(i);
                    
                    // Procedural sine noise displacement
                    const factor = 1.0 + Math.sin(x*1.5 + time*5.0) * Math.cos(y*1.5 + time*4.0) * Math.sin(z*1.5 + time*3.0) * displacement;
                    pos.setXYZ(i, x * factor, y * factor, z * factor);
                }
                pos.needsUpdate = true;

                // [PURE ADDITION]: Deform nested inner solid core in sync
                const innerCore = active3dMesh.getObjectByName("innerCore");
                if (innerCore) {
                    const innerGeom = innerCore.geometry;
                    const innerPos = innerGeom.attributes.position;
                    const innerOrig = innerGeom.userData.originalPositions;
                    for (let i = 0; i < innerPos.count; i++) {
                        const x = innerOrig.getX(i);
                        const y = innerOrig.getY(i);
                        const z = innerOrig.getZ(i);
                        const factor = 1.0 + Math.sin(x*1.5 + time*5.0) * Math.cos(y*1.5 + time*4.0) * Math.sin(z*1.5 + time*3.0) * displacement;
                        innerPos.setXYZ(i, x * factor, y * factor, z * factor);
                    }
                    innerPos.needsUpdate = true;
                }
                
                // Camera orbit hover + mouse parallax
                camera3d.position.x = Math.sin(time * 0.3) * 0.5 + mouseX * 0.4;
                camera3d.position.y = Math.cos(time * 0.3) * 0.3 + mouseY * 0.4;
                camera3d.position.z = 4.8;
                camera3d.lookAt(0, 0, 0);
            }
            else if (visualizerStyle === 'grid') {
                // Animate retro mountains landscape
                const geom = active3dGrid.geometry;
                const pos = geom.attributes.position;
                const speed = time * (eqPreset === 'cyber' ? 5.5 : 2.0);
                
                for (let i = 0; i < pos.count; i++) {
                    const x = pos.getX(i);
                    const y = pos.getY(i);
                    
                    // scrolling wave height calculations
                    let zWave = Math.sin(x * 0.3 + speed) * Math.cos(y * 0.3 - speed) * 0.35 * (1.0 + visualizerAmp * 0.1);
                    if (eqPreset === 'bass') zWave *= 1.5;
                    pos.setZ(i, zWave);
                }
                pos.needsUpdate = true;
                
                // Pulsate sun scale to the beat
                const sunScale = 1.0 + Math.sin(time * 3) * 0.04 + visualizerAmp * 0.005;
                active3dSun.scale.setScalar(sunScale);
                
                camera3d.position.set(mouseX * 0.5, 0.4 + mouseY * 0.3, 4.2);
                camera3d.lookAt(0, 0.1, -1);
            }
            else if (visualizerStyle === 'tunnel') {
                // Fly-through scrolling tunnel
                const geom = active3dTunnel.geometry;
                const pos = geom.attributes.position;
                const count = pos.count;
                let speed = 0.05 + visualizerAmp * 0.005;
                if (eqPreset === 'bass') speed *= 1.8;
                if (eqPreset === 'vocals') speed *= 0.6;
                if (eqPreset === 'concert') speed *= 0.55;
                
                for (let i = 0; i < count; i++) {
                    let z = pos.getZ(i);
                    z += speed;
                    if (z > 2) {
                        z = -18; // recycle tunnel end
                    }
                    pos.setZ(i, z);
                }
                pos.needsUpdate = true;
                
                active3dTunnel.rotation.z = time * (eqPreset === 'cyber' ? 0.20 : 0.08);
                
                camera3d.position.set(Math.sin(time*0.5)*0.2 + mouseX * 0.2, Math.cos(time*0.5)*0.15 + mouseY * 0.2, 2.5);
                camera3d.lookAt(0, 0, -2);
            }
            else if (visualizerStyle === 'spectrum') {
                // Rotates spectrum equalizer circular layout
                active3dSpectrum.rotation.y = time * 0.12;
                
                // Pulsate core beat wireframe sphere
                const sphereScale = 1.0 + (visualizerAmp / 45) * 0.18 + Math.sin(time * 5.0) * 0.05;
                active3dSpectrumSphere.scale.setScalar(sphereScale);
                
                // Animate bars
                for (let i = 0; i < active3dSpectrumBars.length; i++) {
                    const bar = active3dSpectrumBars[i];
                    // Simulated waveform peaks using sine/cosine harmonies
                    const wave1 = Math.sin(i * 0.45 + time * (eqPreset === 'cyber' ? 16.0 : 7.5));
                    const wave2 = Math.cos(i * 0.25 - time * 4.5) * 0.5;
                    let peak = Math.max(0.1, 0.35 + Math.abs(wave1 + wave2) * (visualizerAmp / 35) * 1.2);
                    if (eqPreset === 'bass') peak *= 1.7;
                    bar.scale.y = peak;
                }
                
                camera3d.position.set(mouseX * 0.6, 1.2 + mouseY * 0.5, 4.2);
                camera3d.lookAt(0, -0.4, 0);
            }
            else if (visualizerStyle === 'galaxy') {
                const geom = active3dGalaxy.geometry;
                const pos = geom.attributes.position;
                const count = pos.count;
                
                const angles = active3dGalaxy.userData.angles;
                const distances = active3dGalaxy.userData.distances;
                const velocities = active3dGalaxy.userData.velocities;
                
                const expansion = 1.0 + (visualizerAmp / 45) * 0.28;
                
                for (let i = 0; i < count; i++) {
                    angles[i] += velocities[i] * (1.0 + (visualizerAmp / 45) * 0.5) * (eqPreset === 'cyber' ? 2.0 : 1.0);
                    if (angles[i] >= Math.PI * 2) angles[i] -= Math.PI * 2;
                    const radius = distances[i] * expansion;
                    pos.setX(i, Math.cos(angles[i]) * radius);
                    pos.setZ(i, Math.sin(angles[i]) * radius);
                }
                pos.needsUpdate = true;
                active3dGalaxy.rotation.y = time * (eqPreset === 'cyber' ? 0.20 : 0.08);
                camera3d.position.set(Math.sin(time * 0.2) * 1.5 + mouseX * 0.8, 2.5 + mouseY * 0.6, Math.cos(time * 0.2) * 4.0);
                camera3d.lookAt(0, 0, 0);
            }
            // ── Starfield warp ──────────────────────────────────────────────────
            else if (visualizerStyle === 'stars' && active3dStars) {
                const pos    = active3dStars.geometry.attributes.position;
                const speeds = active3dStars.userData.speeds;
                let warpMult = 1.0 + (visualizerAmp / 45) * 1.5;
                if (eqPreset === 'bass')  warpMult *= 2.2;
                if (eqPreset === 'cyber') warpMult *= 3.0;
                
                for (let i = 0; i < pos.count; i++) {
                    let z = pos.getZ(i) + speeds[i] * warpMult;
                    if (z > 10) {
                        z = -20;
                        pos.setX(i, (Math.random() - 0.5) * 20);
                        pos.setY(i, (Math.random() - 0.5) * 20);
                    }
                    pos.setZ(i, z);
                }
                pos.needsUpdate = true;
                
                const t2 = themes[currentTheme];
                active3dStars.material.color.setHex(t2.threeHex);
                active3dStars.material.size = 0.05 + (visualizerAmp / 45) * 0.08;
                camera3d.position.set(mouseX * 0.3, mouseY * 0.3, 2);
                camera3d.lookAt(0, 0, -10);
            }
            // ── City skyline EQ ─────────────────────────────────────────────────
            else if (visualizerStyle === 'city' && active3dCity) {
                active3dCityBars.forEach((bar, i) => {
                    const wave = Math.sin(i * 0.6 + time * (eqPreset === 'cyber' ? 9.0 : 4.5));
                    const wave2 = Math.cos(i * 0.35 - time * 3.0) * 0.4;
                    let peak = Math.max(0.05, 0.3 + Math.abs(wave + wave2) * (visualizerAmp / 35));
                    if (eqPreset === 'bass') peak *= 1.8;
                    
                    bar.scale.y = peak;
                    const t2 = themes[currentTheme];
                    bar.material.color.setHex(t2.threeHex);
                });
                
                active3dCity.rotation.y = Math.sin(time * 0.15) * 0.25 + mouseX * 0.2;
                camera3d.position.set(mouseX * 0.6, 1.0 + mouseY * 0.4, 5.5);
                camera3d.lookAt(0, 0.2, 0);
            }
            
            renderer3d.render(scene3d, camera3d);
        }
        
        // 10. 2D Canvas Visualizer loop
        function drawVisualizer() {
            requestAnimationFrame(drawVisualizer);
            if (!ctx || !canvas) return;
            
            ctx.clearRect(0, 0, canvas.width, canvas.height);
            
            const width = canvas.width;
            const height = canvas.height;
            const centerY = height / 2;
            
            const themeObj = themes[currentTheme];
            
            // Physics calculations for bounce decay
            let targetAmp = isPlaying ? (lastVolume / 100) * 35 + 10 : 3;
            visualizerAmp += (targetAmp - visualizerAmp) * 0.08;
            
            let targetSpeed = isPlaying ? 0.07 : 0.015;
            visualizerSpeed += (targetSpeed - visualizerSpeed) * 0.08;
            waveOffset += visualizerSpeed;
            
            // Simulated active lyric beating
            if (currentLyricIndex !== -1) {
                const activeEl = document.getElementById(`lyric-line-${currentLyricIndex}`);
                if (activeEl) {
                    if (lyricEffect === 'scale') {
                        const wobble = Math.sin(Date.now() / 200) * 1.5;
                        const activeScale = 1.15 + (visualizerAmp / 45) * 0.1; 
                        activeEl.style.transform = `scale(${activeScale}) rotate(${wobble}deg) translateY(-2px)`;
                        activeEl.style.textShadow = `0 0 25px ${themeObj.glow}`;
                    } else if (lyricEffect === 'neon') {
                        const neonScale = 1.03 + (visualizerAmp / 45) * 0.05;
                        activeEl.style.transform = `scale(${neonScale}) translateY(-2px)`;
                        const glowRadius = 15 + (visualizerAmp / 45) * 15;
                        activeEl.style.animation = "neonPulse 2.5s linear infinite";
                        activeEl.style.textShadow = `0 0 ${glowRadius}px ${themeObj.accent}`;
                    } else if (lyricEffect === 'blur') {
                        const blurScale = 1.04 + (visualizerAmp / 45) * 0.04;
                        activeEl.style.transform = `scale(${blurScale}) translateY(-2px)`;
                        activeEl.style.textShadow = `0 0 ${15 + (visualizerAmp / 45) * 12}px ${themeObj.glow}`;
                    } else if (lyricEffect === 'karaoke') {
                        const karaokeScale = 1.05 + (visualizerAmp / 45) * 0.04;
                        activeEl.style.transform = `scale(${karaokeScale}) translateY(-1px)`;
                        activeEl.style.textShadow = `0 0 ${10 + (visualizerAmp / 45) * 8}px ${themeObj.glow}`;
                    }
                }
            }
            
            // Continuous rotating vinyl inertia
            const vinyl = document.getElementById('vinyl-record');
            if (vinyl) {
                let targetRotationSpeed = isPlaying ? 0.45 : 0.0;
                vinylRotation += (isPlaying ? 0.35 : 0);
                if (vinylRotation >= 360) vinylRotation -= 360;
                vinyl.style.transform = `rotate(${vinylRotation}deg)`;
                
                const glowVal = isPlaying ? 12 + (visualizerAmp / 45) * 15 : 4;
                vinyl.style.boxShadow = `0 15px 35px -5px rgba(0, 0, 0, 0.6), 0 0 ${glowVal}px ${themeObj.accent}55`;
            }
            
            // Dynamic glowing background orb pulsing! Tying entire interface to music beats!
            const orb1 = document.getElementById('orb-1');
            const orb2 = document.getElementById('orb-2');
            const orb3 = document.getElementById('orb-3');
            
            if (orb1 && orb2 && orb3) {
                const beatPercent = visualizerAmp / 45; // simulated volume beat fraction
                const scale1 = 1.0 + beatPercent * 0.16;
                const scale2 = 1.0 + beatPercent * 0.12;
                const scale3 = 1.0 + beatPercent * 0.20;
                
                const opacity1 = 0.35 + beatPercent * 0.25;
                const opacity2 = 0.25 + beatPercent * 0.20;
                const opacity3 = 0.25 + beatPercent * 0.22;
                
                orb1.style.transform = `scale(${scale1})`;
                orb1.style.opacity = `${opacity1}`;
                
                orb2.style.transform = `scale(${scale2})`;
                orb2.style.opacity = `${opacity2}`;
                
                orb3.style.transform = `scale(${scale3})`;
                orb3.style.opacity = `${opacity3}`;
            }

            // [PURE ADDITION]: Drive behind-the-scenes Ambilight glow scale & opacity response
            const ambilight = document.getElementById('player-ambilight-glow');
            if (ambilight) {
                const beatPercent = visualizerAmp / 45;
                const ambilightScale = 1.0 + beatPercent * 0.08;
                const ambilightOpacity = 0.4 + beatPercent * 0.4;
                ambilight.style.transform = `scale(${ambilightScale})`;
                ambilight.style.opacity = `${ambilightOpacity}`;
            }

            // [PURE ADDITION]: Spring physics for mouse spotlight tracking cursor
            cursorX += (targetCursorX - cursorX) * 0.08;
            cursorY += (targetCursorY - cursorY) * 0.08;
            const cursorGlow = document.getElementById('interactive-cursor-glow');
            if (cursorGlow) {
                cursorGlow.style.left = `${cursorX - 175}px`;
                cursorGlow.style.top = `${cursorY - 175}px`;
            }
            
            // Render Karaoke scrolling progress bar tags in real-time
            if (currentLyricIndex !== -1 && lyricEffect === 'karaoke' && player) {
                const activeEl = document.getElementById(`lyric-line-${currentLyricIndex}`);
                if (activeEl) {
                    const curTime = getPlayerTime();
                    const adjustedTime = curTime + lyricsSyncOffset;
                    
                    let duration = 4.0;
                    if (currentLyricIndex < lyricsData.length - 1) {
                        duration = lyricsData[currentLyricIndex + 1].time - lyricsData[currentLyricIndex].time;
                    }
                    
                    let elapsed = adjustedTime - lyricsData[currentLyricIndex].time;
                    let pct = Math.min(100, Math.max(0, (elapsed / duration) * 100));
                    activeEl.style.setProperty('--progress', `${pct}%`);
                }
            }
            
            // Draw 2D visualizer wave lines
            if (visualizerStyle === 'wave') {
                drawWave(width, centerY, visualizerAmp, waveOffset, themeObj.vizColors[0], 1.2, 0.007);
                drawWave(width, centerY, visualizerAmp * 0.7, waveOffset * 0.8 + 2, themeObj.vizColors[1], 1.6, 0.005);
                drawWave(width, centerY, visualizerAmp * 0.5, waveOffset * 1.2 - 4, themeObj.vizColors[2], 0.8, 0.009);
            } else if (visualizerStyle === 'radial') {
                drawRadialVisualizer(width, height, visualizerAmp, themeObj);
            }
        }
        
        function drawWave(width, centerY, amp, offset, color, frequencyMultiplier, wavelength) {
            ctx.beginPath();
            ctx.strokeStyle = color;
            ctx.lineWidth = 3.0;
            ctx.shadowBlur = 10;
            ctx.shadowColor = color;
            
            for (let x = 0; x < width; x++) {
                let y = centerY + 
                        Math.sin(x * wavelength * frequencyMultiplier + offset) * amp * 
                        Math.cos(x * wavelength * 0.5 - offset * 0.3) * 
                        Math.sin(x * 0.002) * 1.2;
                
                if (x === 0) {
                    ctx.moveTo(x, y);
                } else {
                    ctx.lineTo(x, y);
                }
            }
            ctx.stroke();
            ctx.shadowBlur = 0;
        }
        
        function drawRadialVisualizer(width, height, baseAmp, themeObj) {
            const centerX = width / 2;
            const centerY = height / 2;
            const baseRadius = 88;
            const numBars = 60;
            
            for (let i = 0; i < numBars; i++) {
                const angle = (i / numBars) * Math.PI * 2 + waveOffset * 0.2;
                const noise = Math.sin(angle * 5 + waveOffset) * Math.cos(angle * 2.5 - waveOffset * 0.5);
                const barHeight = Math.max(2, baseAmp * 0.7 * (0.8 + noise * 0.35));
                
                const startX = centerX + Math.cos(angle) * baseRadius;
                const startY = centerY + Math.sin(angle) * baseRadius;
                const endX = centerX + Math.cos(angle) * (baseRadius + barHeight);
                const endY = centerY + Math.sin(angle) * (baseRadius + barHeight);
                
                ctx.beginPath();
                ctx.moveTo(startX, startY);
                ctx.lineTo(endX, endY);
                
                const gradient = ctx.createLinearGradient(startX, startY, endX, endY);
                gradient.addColorStop(0, themeObj.accent);
                gradient.addColorStop(0.5, themeObj.vizColors[1]);
                gradient.addColorStop(1, 'rgba(255, 255, 255, 0.01)');
                
                ctx.strokeStyle = gradient;
                ctx.lineWidth = 2.5;
                ctx.lineCap = 'round';
                ctx.shadowBlur = 5;
                ctx.shadowColor = themeObj.glow;
                ctx.stroke();
            }
        }
        // ══════════════════════════════════════════════════════════════════════
        // NEW ADDITIONS: Keyboard shortcuts, Waveform, Beat detection,
        //                Lyrics search, Crossfade, Real spectrum analyzer
        // ══════════════════════════════════════════════════════════════════════

        // ── Keyboard shortcuts ────────────────────────────────────────────────
        document.addEventListener('keydown', (e) => {
            const tag = document.activeElement.tagName.toLowerCase();
            if (tag === 'input' || tag === 'textarea') return; // don't hijack text fields
            switch(e.code) {
                case 'Space':
                    e.preventDefault();
                    togglePlayState();
                    break;
                case 'ArrowRight':
                    e.preventDefault();
                    skipTime(e.shiftKey ? 30 : 10);
                    break;
                case 'ArrowLeft':
                    e.preventDefault();
                    skipTime(e.shiftKey ? -30 : -10);
                    break;
                case 'ArrowUp':
                    e.preventDefault();
                    { const vs = document.getElementById('volume-slider'); const nv = Math.min(100, parseInt(vs.value||70)+5); vs.value=nv; onVolumeChange(nv); }
                    break;
                case 'ArrowDown':
                    e.preventDefault();
                    { const vs = document.getElementById('volume-slider'); const nv = Math.max(0, parseInt(vs.value||70)-5); vs.value=nv; onVolumeChange(nv); }
                    break;
                case 'KeyM':
                    toggleMute();
                    break;
                case 'KeyN':
                    playNextTrack();
                    break;
                case 'KeyP':
                    playPrevTrack();
                    break;
                case 'KeyF':
                    toggleFocusMode();
                    break;
                case 'Slash':
                    e.preventDefault();
                    toggleLyricsSearch();
                    break;
            }
        });

        // ── Waveform scrubber ─────────────────────────────────────────────────
        function initWaveformCanvas() {
            waveformCanvas = document.getElementById('waveform-canvas');
            if (!waveformCanvas) return;
            waveformCtx = waveformCanvas.getContext('2d');
            // Generate a fake but realistic-looking waveform
            const n = 300;
            waveformData = [];
            let envelope = 0;
            for (let i = 0; i < n; i++) {
                envelope += (Math.random() - 0.45) * 0.15;
                envelope = Math.max(0.05, Math.min(0.95, envelope));
                waveformData.push(envelope + Math.random() * 0.12);
            }
            drawWaveformScrubber(0);
        }

        function drawWaveformScrubber(progress) {
            if (!waveformCanvas || !waveformCtx || waveformData.length === 0) return;
            const W = waveformCanvas.offsetWidth;
            const H = waveformCanvas.offsetHeight;
            waveformCanvas.width = W;
            waveformCanvas.height = H;
            waveformCtx.clearRect(0, 0, W, H);
            const barW = W / waveformData.length;
            const mid = H / 2;
            const progressPx = progress * W;
            const t = themes[currentTheme];
            waveformData.forEach((v, i) => {
                const x = i * barW;
                const h = v * (H * 0.85);
                const isPast = x < progressPx;
                waveformCtx.fillStyle = isPast ? t.accent + 'cc' : 'rgba(255,255,255,0.12)';
                waveformCtx.beginPath();
                waveformCtx.roundRect(x + 0.5, mid - h/2, Math.max(1, barW - 1), h, 1);
                waveformCtx.fill();
            });
        }

        // Hook into existing progress bar update to repaint waveform
        function updateProgressBar(time) {
            const progress = document.getElementById('progress-bar');
            progress.value = time;
            document.getElementById('time-current').innerText = formatTime(time);
            const dur = currentSongDuration || 1;
            drawWaveformScrubber(Math.min(1, time / dur));

            // ⚡ NEON ADDITION: Update neon laser trail fill width
            (function updateNeonProgressFill() {
                const neonFill = document.getElementById('neon-progress-fill');
                const sb = document.getElementById('progress-bar');
                if (neonFill && sb) {
                    const pct = (parseFloat(sb.value) / parseFloat(sb.max || 100)) * 100;
                    neonFill.style.width = pct + '%';
                }
            })();
        }

        // Also update when theme changes - handled inside setTheme directly

        // ── Beat detection via simulated amplitude peaks ───────────────────────
        function tickBeatDetection() {
            if (!isPlaying) { beatFlash = Math.max(0, beatFlash - 0.08); applyBeatFlash(); return; }
            // Drive off visualizerAmp which tracks volume already
            if (beatCooldown > 0) { beatCooldown--; beatFlash = Math.max(0, beatFlash - 0.06); applyBeatFlash(); return; }
            const level = visualizerAmp; // 3–45 range
            if (level > 28 && Math.random() > 0.55) {
                beatFlash = 0.6 + (level / 45) * 0.4;
                beatCooldown = Math.floor(8 + Math.random() * 10);
                // Update BPM display (rough estimate: beats per minute from cooldown spacing)
                const bpm = Math.round(60 / ((beatCooldown + 8) / 60));
                const bpmEl = document.getElementById('beat-bpm');
                if (bpmEl) bpmEl.innerText = bpm + ' BPM ♪';
            }
            beatFlash = Math.max(0, beatFlash - 0.05);
            applyBeatFlash();
        }

        function applyBeatFlash() {
            const el = document.getElementById('beat-flash');

            // ⚡ NEON ADDITION: Corner beat flash sparks
            (function triggerCornerBeatFlash() {
                const corners = ['tl','tr','bl','br'];
                corners.forEach((c, i) => {
                    const elc = document.getElementById('beat-flash-corner-' + c);
                    if (elc) {
                        elc.style.opacity = (0.4 + Math.random() * 0.4).toString();
                        setTimeout(() => { elc.style.opacity = '0'; }, 80 + i * 15);
                    }
                });
            })();

            // ⚡ NEON ADDITION: Fire lightning on strong beats
            if (Math.random() > 0.7 && window.fireNeonLightning) {
                window.fireNeonLightning();
            }

            // ⚡ NEON ADDITION: Notify BPM tracker on beat
            if (window.neonBpmOnBeat) window.neonBpmOnBeat();
            if (!el) return;
            const t = themes[currentTheme];
            el.style.opacity = beatFlash.toFixed(3);
            el.style.background = `radial-gradient(ellipse at center, ${t.accent}30 0%, transparent 70%)`;
        }

        // Inject tickBeatDetection into the existing drawVisualizer RAF loop
        const _origDrawViz = drawVisualizer;
        // We patch by adding a side-effect call in the visualizerAmp block —
        // simpler: use a separate 60fps RAF loop
        (function beatLoop() {
            tickBeatDetection();
            requestAnimationFrame(beatLoop);
        })();

        // ── Lyrics search ─────────────────────────────────────────────────────
        function toggleLyricsSearch() {
            lyricsSearchActive = !lyricsSearchActive;
            const bar = document.getElementById('lyrics-search-bar');
            const btn = document.getElementById('lyrics-search-btn');
            if (lyricsSearchActive) {
                bar.classList.remove('hidden');
                bar.classList.add('flex');
                setTimeout(() => document.getElementById('lyrics-search-input').focus(), 50);
                btn.classList.add('border-yellow-500/50', 'text-yellow-300');
            } else {
                bar.classList.add('hidden');
                bar.classList.remove('flex');
                btn.classList.remove('border-yellow-500/50', 'text-yellow-300');
                clearLyricsSearch();
            }
            lucide.createIcons();
        }

        function onLyricsSearch(term) {
            lyricsSearchTerm = term.trim().toLowerCase();
            clearLyricsHighlights();
            lyricsSearchMatches = [];
            lyricsSearchIdx = 0;
            if (!lyricsSearchTerm) {
                document.getElementById('lyrics-search-count').innerText = '';
                return;
            }
            const lines = document.querySelectorAll('.lyric-line');
            lines.forEach((el, i) => {
                if (el.innerText.toLowerCase().includes(lyricsSearchTerm)) {
                    lyricsSearchMatches.push(i);
                    highlightLyricLine(el, lyricsSearchTerm);
                }
            });
            document.getElementById('lyrics-search-count').innerText =
                lyricsSearchMatches.length ? `1/${lyricsSearchMatches.length}` : '0 found';
            if (lyricsSearchMatches.length) scrollToLyricLine(lyricsSearchMatches[0]);
        }

        function lyricsSearchNav(dir) {
            if (!lyricsSearchMatches.length) return;
            lyricsSearchIdx = (lyricsSearchIdx + dir + lyricsSearchMatches.length) % lyricsSearchMatches.length;
            document.getElementById('lyrics-search-count').innerText =
                `${lyricsSearchIdx + 1}/${lyricsSearchMatches.length}`;
            scrollToLyricLine(lyricsSearchMatches[lyricsSearchIdx]);
        }

        function highlightLyricLine(el, term) {
            const raw = el.innerText;
            const idx = raw.toLowerCase().indexOf(term);
            if (idx === -1) return;
            el.innerHTML =
                escH(raw.slice(0, idx)) +
                `<mark style="background:rgba(250,204,21,0.35);color:#fde68a;border-radius:3px;padding:0 2px;">${escH(raw.slice(idx, idx + term.length))}</mark>` +
                escH(raw.slice(idx + term.length));
        }

        function escH(s) { return s.replace(/&/g,'&amp;').replace(/</g,'&lt;').replace(/>/g,'&gt;'); }

        function clearLyricsHighlights() {
            document.querySelectorAll('.lyric-line mark').forEach(m => {
                const p = m.parentNode;
                p.replaceChild(document.createTextNode(m.textContent), m);
                p.normalize();
            });
        }

        function clearLyricsSearch() {
            clearLyricsHighlights();
            lyricsSearchMatches = [];
            lyricsSearchTerm = '';
            const inp = document.getElementById('lyrics-search-input');
            if (inp) inp.value = '';
            const cnt = document.getElementById('lyrics-search-count');
            if (cnt) cnt.innerText = '';
        }

        function scrollToLyricLine(lineIndex) {
            const el = document.getElementById(`lyric-line-${lineIndex}`);
            const pane = document.getElementById('lyrics-scroll-pane');
            if (!el || !pane) return;
            pane.scrollTo({ top: el.offsetTop - pane.clientHeight / 2 + el.clientHeight / 2, behavior: 'smooth' });
        }

        function copyAllLyrics() {
            const lines = [...document.querySelectorAll('.lyric-line')].map(el => el.innerText).join('\n');
            if (!lines.trim()) { stStatusToast('No lyrics to copy'); return; }
            navigator.clipboard.writeText(lines).then(() => stStatusToast('📋 Lyrics copied!')).catch(() => {
                const ta = document.createElement('textarea');
                ta.value = lines; document.body.appendChild(ta); ta.select(); document.execCommand('copy'); document.body.removeChild(ta);
                stStatusToast('📋 Lyrics copied!');
            });
        }

        // ── Crossfade between queue tracks ────────────────────────────────────
        // Detects when < 8s remain and fades out then loads next
        function checkCrossfade() {
            if (!player || !crossfadeActive || !isPlaying) return;
            const remaining = (player.getDuration() || currentSongDuration) - getPlayerTime();
            if (remaining < 8 && remaining > 0 && !crossfadeTimer) {
                crossfadeTimer = setTimeout(() => {
                    crossfadeTimer = null;
                    playNextTrack();
                }, remaining * 1000 - 200);
                stStatusToast('⟶ Crossfading…');
            }
        }

        // Add crossfade toggle button logic
        function toggleCrossfade() {
            crossfadeActive = !crossfadeActive;
            const btn = document.getElementById('crossfade-btn');
            if (btn) {
                btn.style.color = crossfadeActive ? '#06b6d4' : '';
                btn.title = crossfadeActive ? 'Crossfade ON' : 'Crossfade OFF';
            }
            if (!crossfadeActive && crossfadeTimer) { clearTimeout(crossfadeTimer); crossfadeTimer = null; }
            stStatusToast(crossfadeActive ? '⟶ Crossfade ON' : 'Crossfade OFF');
        }

        // ── Init new features on DOMContentLoaded ─────────────────────────────
        // (merged into the main DOMContentLoaded listener above)

        // GUARANTEED INIT: Call directly at script end - works in Streamlit srcdoc iframes
        // where DOMContentLoaded has already fired before this script executes.
        // The _done flag inside initApp() prevents double-initialization.
        initApp();
    </script>
</body>
</html>"""
    
    # Safe casting and fallback for string inputs
    song_title = str(song_title or "")
    artist = str(artist or "")
    plain_lyrics = str(plain_lyrics or "")

    # Replace normal Python string keys with data injected values!
    # This completely eliminates f-string curly-brace escaping syntax bugs.
    html_content = html_template \
        .replace("{video_id}", video_id) \
        .replace("{song_title}", song_title.replace("'", "\\'").replace('"', '\\"')) \
        .replace("{artist}", artist.replace("'", "\\'").replace('"', '\\"')) \
        .replace("{thumbnail_url}", thumbnail_url) \
        .replace("{duration_seconds}", str(duration_seconds)) \
        .replace("{synced_lyrics_json}", synced_lyrics_json) \
        .replace("{plain_lyrics}", plain_lyrics.replace("`", "\\`").replace("\n", "\\n").replace("\r", "")) \
        .replace("{duration_str}", duration_str) \
        .replace("{queue_json}", queue_json) \
        .replace("{current_index}", str(current_index))
        
    # [PURE ADDITION]: Clean any invalid lone surrogates (U+D800 to U+DFFF) to avoid Streamlit / Protobuf marshalling crashes
    html_content = "".join(c for c in html_content if not (0xD800 <= ord(c) <= 0xDFFF))
        
    return html_content