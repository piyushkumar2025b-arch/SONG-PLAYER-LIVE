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
    </style>
</head>
<body class="h-full flex items-center justify-center p-0 select-none">
    
    <!-- Ambient Glowing Background Orbs -->
    <div class="fixed inset-0 overflow-hidden pointer-events-none -z-10 bg-[#060810]">
        <div id="orb-1" class="absolute -top-40 -left-40 w-96 h-96 rounded-full bg-rose-900/30 blur-[120px]"></div>
        <div id="orb-2" class="absolute -bottom-40 -right-40 w-96 h-96 rounded-full bg-blue-900/20 blur-[120px]"></div>
        <div id="orb-3" class="absolute top-1/2 left-1/3 w-80 h-80 rounded-full bg-purple-950/20 blur-[100px]"></div>
    </div>
    
    <!-- Main Player UI Card Container with Ambilight back-glow -->
    <div class="relative w-full max-w-5xl h-[610px] card-enter">
        <!-- Dynamic behind-the-scenes Ambient Ambilight Backglow -->
        <div id="player-ambilight-glow" class="absolute -inset-10 rounded-[40px] opacity-60 blur-[60px] pointer-events-none -z-10 transition-all duration-300"></div>
        
        <!-- Main Player UI Card -->
        <div class="glass-panel w-full h-full rounded-3xl overflow-hidden flex flex-col md:flex-row shadow-2xl relative">
            
            <!-- Interactive Parallax Cursor Glow Spot -->
            <div id="interactive-cursor-glow" class="absolute w-[350px] h-[350px] rounded-full pointer-events-none -z-5 opacity-0 blur-[80px] transition-opacity duration-500" style="background: radial-gradient(circle, rgba(255,255,255,0.08) 0%, transparent 70%);"></div>
        
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
                <button id="mode-toggle-btn" onclick="togglePlayMode()" class="px-3 py-1 text-xs rounded-full border border-white/10 hover:border-white/30 bg-white/5 hover:bg-white/10 flex items-center gap-1.5 transition-all text-white/80">
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
                
                <!-- Progress Bar & Time -->
                <div>
                    <input id="progress-bar" type="range" min="0" max="{duration_seconds}" value="0" oninput="onProgressSeek(this.value)" class="w-full h-1">
                    <div class="flex justify-between text-[10px] text-white/40 mt-1 font-mono">
                        <span id="time-current">00:00</span>
                        <span id="time-total">{duration_str}</span>
                    </div>
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
                    <button id="play-pause-btn" onclick="togglePlayState()" class="w-12 h-12 rounded-full bg-rose-600 hover:bg-rose-500 text-white flex items-center justify-center shadow-lg shadow-rose-600/20 hover:scale-105 active:scale-95 transition-all">
                        <i id="play-icon" data-lucide="play" class="w-5 h-5 fill-white"></i>
                    </button>
                    
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
                    </div>
                </div>
            </div>
        </div>
        
        <!-- Right Side: Lyrics Panel -->
        <div id="lyrics-panel" class="w-full md:w-[55%] h-full flex flex-col justify-between px-5 py-3 relative z-10 bg-black/25 transition-all duration-500 ease-in-out">
            
            <!-- Panel Header -->
            <div class="flex items-center justify-between border-b border-white/5 pb-3">
                <div class="flex items-center gap-2">
                    <i data-lucide="music-2" class="w-4 h-4 text-rose-500"></i>
                    <h3 class="text-sm font-semibold tracking-wider uppercase text-white/70">Lyrics Reader</h3>
                </div>
                
                <div class="flex items-center gap-2">
                    <!-- Up Next Queue Drawer Toggle -->
                    <button id="queue-drawer-btn" onclick="toggleQueueDrawer()" class="px-2.5 py-1 text-xs rounded-full border border-white/10 hover:border-white/30 bg-white/5 hover:bg-white/10 flex items-center gap-1 transition-all text-white/80" title="Show Up Next Queue">
                        <i data-lucide="list-music" class="w-3 h-3 text-cyan-400"></i>
                        <span>Queue</span>
                    </button>
                    <!-- Spotify Focus Mode Switcher -->
                    <button id="focus-toggle-btn" onclick="toggleFocusMode()" class="px-2.5 py-1 text-xs rounded-full border border-white/10 hover:border-white/30 bg-white/5 hover:bg-white/10 flex items-center gap-1 transition-all text-white/80" title="Toggle Spotify Focus Mode">
                        <i data-lucide="maximize-2" class="w-3 h-3 text-rose-400"></i>
                        <span>Spotify Mode</span>
                    </button>
                    <span id="lyrics-type-badge" class="px-2 py-0.5 text-[9px] font-bold uppercase rounded-full bg-rose-500/20 text-rose-300 border border-rose-500/20">Synced</span>
                </div>
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
                <span>💡 Click on any line to seek player</span>
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
            }
        };
        let currentTheme = 'rose';
        
        // 2. Initialize App
        document.addEventListener("DOMContentLoaded", () => {
            lucide.createIcons();
            // If Python already has lyrics, show them immediately
            // Otherwise kick off client-side fetch right away (Python API calls are blocked server-side)
            if (lyricsData && lyricsData.length > 0) {
                buildLyricsUI();
            } else {
                // Show loading spinner and immediately fetch from browser (lrclib.net works client-side)
                document.getElementById('lyrics-scroll-pane').innerHTML = `
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

            // Interactive cursor spotlight with smooth spring physics [PURE ADDITION]
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
            
            // Write active song info to local storage so Streamlit knows what's playing
            localStorage.setItem('melodify_active_song', JSON.stringify({
                id: activeVideoId,
                title: currentSongTitle,
                uploader: currentSongArtist,
                duration: currentSongDuration,
                thumbnail: currentSongThumbnail
            }));
        });
        
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
            // Removing the silent-fail autoplay is what makes the player actually work.
            
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
        }
        
        function onPlayerStateChange(event) {
            const playIcon = document.getElementById('play-icon');
            
            if (event.data === YT.PlayerState.PLAYING) {
                isPlaying = true;
                playIcon.setAttribute('data-lucide', 'pause');
                lucide.createIcons();
                startLyricsSync();
            } else if (event.data === YT.PlayerState.ENDED) {
                isPlaying = false;
                playIcon.setAttribute('data-lucide', 'play');
                lucide.createIcons();
                stopLyricsSync();
                handleSongEnded();
            } else {
                isPlaying = false;
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
            const state = player.getPlayerState();
            if (state === YT.PlayerState.PLAYING) {
                player.pauseVideo();
            } else {
                player.playVideo();
            }
        }
        
        function skipTime(seconds) {
            if (!player) return;
            const curTime = player.getCurrentTime();
            const duration = player.getDuration() || currentSongDuration;
            let targetTime = curTime + seconds;
            if (targetTime < 0) targetTime = 0;
            if (targetTime > duration) targetTime = duration;
            
            player.seekTo(targetTime, true);
            updateProgressBar(targetTime);
        }
        
        function onProgressSeek(value) {
            if (!player) return;
            player.seekTo(parseFloat(value), true);
            updateProgressBar(parseFloat(value));
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
            updateProgressBar(time);
            syncLyricsNow();
        }
        
        function startLyricsSync() {
            stopLyricsSync();
            lyricsInterval = setInterval(() => {
                if (!player) return;
                const curTime = player.getCurrentTime();
                updateProgressBar(curTime);
                syncLyrics(curTime);
                // Write current playback time so Karaoke Studio iframe can sync
                try { localStorage.setItem('melodify_playback_time', curTime.toString()); } catch(e) {}
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
                syncLyrics(player.getCurrentTime());
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
                syncLyrics(player.getCurrentTime());
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
                syncLyrics(player.getCurrentTime());
            }
        }
        
        function updateProgressBar(time) {
            const progress = document.getElementById('progress-bar');
            progress.value = time;
            document.getElementById('time-current').innerText = formatTime(time);
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
        }
        
        function setEqualizerPreset(preset) {
            eqPreset = preset;
            const presets = ['flat', 'bass', 'vocals', 'concert', 'cyber'];
            
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
                cyber: "DSP: Electronic Space ⚡"
            };
            
            stStatusToast(labels[preset] || "DSP Equalizer Updated");
            
            if (ctx && canvas) {
                ctx.clearRect(0, 0, canvas.width, canvas.height);
            }
        }
        
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
                    const curTime = player.getCurrentTime();
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
