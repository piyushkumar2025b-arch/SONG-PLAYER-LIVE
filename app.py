import streamlit as st
import streamlit.components.v1 as components

import json
import re
import time
from datetime import datetime, timedelta
from streamlit_option_menu import option_menu
import requests
from typing import List, Dict, Any, Optional

# Import custom modules
from database import DatabaseManager
from youtube_provider import YouTubeProvider
from lyrics_provider import LyricsProvider
from player_component import render_player_html

# Page Configuration
st.set_page_config(
    page_title="Melodify AI - Synced Lyrics Player",
    page_icon="✨",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Initialize Providers
@st.cache_resource
def get_db():
    return DatabaseManager()

@st.cache_resource
def get_youtube():
    return YouTubeProvider()

@st.cache_resource
def get_lyrics_provider():
    return LyricsProvider()

db = get_db()
yt = get_youtube()
lp = get_lyrics_provider()

# Session State Initialization
if "current_song" not in st.session_state:
    st.session_state.current_song = None
if "search_results" not in st.session_state:
    st.session_state.search_results = []
if "lyrics_status" not in st.session_state:
    st.session_state.lyrics_status = None
if "synced_lyrics" not in st.session_state:
    st.session_state.synced_lyrics = []
if "plain_lyrics" not in st.session_state:
    st.session_state.plain_lyrics = ""
if "lyrics_manual_search" not in st.session_state:
    st.session_state.lyrics_manual_search = []
if "selected_playlist_id" not in st.session_state:
    st.session_state.selected_playlist_id = None
if "gemini_key" not in st.session_state:
    st.session_state.gemini_key = ""
if "queue" not in st.session_state:
    st.session_state.queue = []
if "queue_index" not in st.session_state:
    st.session_state.queue_index = 0
if "ai_recs" not in st.session_state:
    st.session_state.ai_recs = []
if "sleep_timer_end" not in st.session_state:
    st.session_state.sleep_timer_end = None
if "sleep_timer_minutes" not in st.session_state:
    st.session_state.sleep_timer_minutes = 30
if "rating_cache" not in st.session_state:
    st.session_state.rating_cache = {}
if "note_editing" not in st.session_state:
    st.session_state.note_editing = None
if "mood_recs" not in st.session_state:
    st.session_state.mood_recs = []
if "search_duration_filter" not in st.session_state:
    st.session_state.search_duration_filter = "All"
if "search_sort" not in st.session_state:
    st.session_state.search_sort = "Relevance"
if "journal_entries" not in st.session_state:
    st.session_state.journal_entries = []
if "trivia_questions" not in st.session_state:
    st.session_state.trivia_questions = []
if "trivia_score" not in st.session_state:
    st.session_state.trivia_score = 0
if "trivia_current" not in st.session_state:
    st.session_state.trivia_current = 0
if "trivia_answered" not in st.session_state:
    st.session_state.trivia_answered = False
if "radio_stations" not in st.session_state:
    st.session_state.radio_stations = []
if "mood_board_result" not in st.session_state:
    st.session_state.mood_board_result = None
if "song_analysis_result" not in st.session_state:
    st.session_state.song_analysis_result = None
if "world_music_data" not in st.session_state:
    st.session_state.world_music_data = None
if "weather_recs" not in st.session_state:
    st.session_state.weather_recs = None
if "active_mood" not in st.session_state:
    st.session_state.active_mood = None
if "music_dna" not in st.session_state:
    st.session_state.music_dna = None
if "trending_chart" not in st.session_state:
    st.session_state.trending_chart = []
if "trending_chart_name" not in st.session_state:
    st.session_state.trending_chart_name = ""
if "collab_messages" not in st.session_state:
    st.session_state.collab_messages = []
if "setlist_result" not in st.session_state:
    st.session_state.setlist_result = None
if "artist_battle_result" not in st.session_state:
    st.session_state.artist_battle_result = None
if "music_timeline" not in st.session_state:
    st.session_state.music_timeline = None
if "cover_art_result" not in st.session_state:
    st.session_state.cover_art_result = None

# Inject Custom CSS for Premium Design & Modern Typography
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Outfit:wght@300;400;500;600;700&display=swap');
    
    /* Global Styles */
    html, body, [class*="css"], .stApp {
        font-family: 'Outfit', sans-serif !important;
        background-color: #060810 !important;
        color: #f3f4f6 !important;
    }
    
    /* Subtle animated gradient bg */
    .stApp::before {
        content: '';
        position: fixed;
        inset: 0;
        background:
            radial-gradient(ellipse 80% 50% at 20% 10%, rgba(244,63,94,0.07) 0%, transparent 60%),
            radial-gradient(ellipse 60% 60% at 80% 90%, rgba(99,102,241,0.06) 0%, transparent 60%);
        pointer-events: none;
        z-index: 0;
    }
    
    /* Sidebar styling */
    [data-testid="stSidebar"] {
        background-color: #080c18 !important;
        border-right: 1px solid rgba(255, 255, 255, 0.05) !important;
    }
    
    /* Song cards — elevated glass */
    .song-item-card {
        background: rgba(12, 18, 38, 0.55);
        backdrop-filter: blur(16px);
        -webkit-backdrop-filter: blur(16px);
        border: 1px solid rgba(255, 255, 255, 0.07);
        border-radius: 18px;
        padding: 14px;
        transition: all 0.25s cubic-bezier(0.4,0,0.2,1);
        margin-bottom: 12px;
    }
    .song-item-card:hover {
        background: rgba(244, 63, 94, 0.06);
        border-color: rgba(244, 63, 94, 0.28);
        transform: translateY(-3px);
        box-shadow: 0 12px 32px -8px rgba(244, 63, 94, 0.22), 0 0 0 1px rgba(244,63,94,0.08);
    }
    
    /* Streamlit buttons — pill style */
    .stButton > button {
        background: rgba(255,255,255,0.05) !important;
        border: 1px solid rgba(255,255,255,0.10) !important;
        border-radius: 12px !important;
        color: rgba(255,255,255,0.85) !important;
        font-family: 'Outfit', sans-serif !important;
        font-weight: 500 !important;
        transition: all 0.2s ease !important;
        letter-spacing: 0.01em !important;
    }
    .stButton > button:hover {
        background: rgba(244,63,94,0.12) !important;
        border-color: rgba(244,63,94,0.35) !important;
        color: #fff !important;
        transform: translateY(-1px) !important;
        box-shadow: 0 4px 16px -4px rgba(244,63,94,0.25) !important;
    }
    .stButton > button:active {
        transform: translateY(0) !important;
    }

    /* Primary action buttons (full width) */
    .stButton > button[kind="primary"] {
        background: linear-gradient(135deg, rgba(244,63,94,0.2), rgba(168,85,247,0.15)) !important;
        border-color: rgba(244,63,94,0.4) !important;
        color: #fff !important;
    }
    
    /* Styled Input Boxes */
    .stTextInput>div>div>input {
        background-color: rgba(255, 255, 255, 0.04) !important;
        border: 1px solid rgba(255, 255, 255, 0.10) !important;
        color: #fff !important;
        border-radius: 12px !important;
        padding: 10px 14px !important;
        transition: border-color 0.2s, box-shadow 0.2s !important;
    }
    .stTextInput>div>div>input:focus {
        border-color: #f43f5e !important;
        box-shadow: 0 0 0 2px rgba(244,63,94,0.15) !important;
    }
    
    /* Selectbox */
    .stSelectbox > div > div {
        background-color: rgba(255,255,255,0.04) !important;
        border: 1px solid rgba(255,255,255,0.10) !important;
        border-radius: 12px !important;
        color: #fff !important;
    }

    /* Tabs */
    .stTabs [data-baseweb="tab-list"] {
        background: rgba(255,255,255,0.03) !important;
        border-radius: 12px !important;
        padding: 4px !important;
        gap: 2px !important;
        border: 1px solid rgba(255,255,255,0.06) !important;
    }
    .stTabs [data-baseweb="tab"] {
        border-radius: 9px !important;
        color: rgba(255,255,255,0.55) !important;
        font-weight: 500 !important;
        transition: all 0.2s !important;
    }
    .stTabs [aria-selected="true"] {
        background: rgba(244,63,94,0.15) !important;
        color: #f43f5e !important;
        border: 1px solid rgba(244,63,94,0.25) !important;
    }
    
    /* Headings Styling */
    h1, h2, h3 {
        color: #ffffff !important;
        font-weight: 700 !important;
        letter-spacing: -0.025em !important;
    }
    
    /* Animated Waveform bars */
    .wave-bar {
        display: inline-block;
        width: 3px;
        border-radius: 2px;
        background: linear-gradient(180deg, #f43f5e, #a855f7);
        animation: wavePulse 1.2s ease-in-out infinite;
        margin: 0 1px;
    }
    .wave-bar:nth-child(1) { animation-delay: 0s;    height: 8px; }
    .wave-bar:nth-child(2) { animation-delay: 0.15s; height: 14px; }
    .wave-bar:nth-child(3) { animation-delay: 0.3s;  height: 10px; }
    .wave-bar:nth-child(4) { animation-delay: 0.45s; height: 16px; }
    .wave-bar:nth-child(5) { animation-delay: 0.6s;  height: 6px; }
    @keyframes wavePulse {
        0%, 100% { transform: scaleY(1);   opacity: 0.8; }
        50%       { transform: scaleY(2.2); opacity: 1; }
    }
    
    /* Sleep timer badge */
    .sleep-badge {
        display: inline-flex;
        align-items: center;
        gap: 5px;
        background: rgba(245, 158, 11, 0.15);
        border: 1px solid rgba(245, 158, 11, 0.3);
        color: #fbbf24;
        font-size: 0.72rem;
        font-weight: 600;
        padding: 4px 10px;
        border-radius: 20px;
        animation: sleepPulse 2s ease-in-out infinite;
    }
    @keyframes sleepPulse {
        0%, 100% { opacity: 1; }
        50% { opacity: 0.6; }
    }

    /* Expanders */
    .stExpander {
        background: rgba(255,255,255,0.02) !important;
        border: 1px solid rgba(255,255,255,0.07) !important;
        border-radius: 14px !important;
    }
    .stExpander summary {
        font-weight: 500 !important;
        color: rgba(255,255,255,0.75) !important;
    }

    /* Scrollbar */
    ::-webkit-scrollbar { width: 5px; height: 5px; }
    ::-webkit-scrollbar-track { background: transparent; }
    ::-webkit-scrollbar-thumb { background: rgba(255,255,255,0.12); border-radius: 99px; }
    ::-webkit-scrollbar-thumb:hover { background: rgba(244,63,94,0.4); }

    /* Stat pill */
    .stat-pill {
        background: rgba(255,255,255,0.04);
        border: 1px solid rgba(255,255,255,0.08);
        border-radius: 12px;
        padding: 14px 18px;
        text-align: center;
    }

    /* Toast / info boxes */
    .stAlert {
        border-radius: 14px !important;
        border: 1px solid rgba(255,255,255,0.07) !important;
        background: rgba(255,255,255,0.03) !important;
    }

    /* Progress / spinner */
    .stSpinner > div { border-color: #f43f5e transparent transparent !important; }

    /* HR dividers */
    hr { border-color: rgba(255,255,255,0.05) !important; }

    /* ── NEW UI ADDITIONS ────────────────────────────────── */

    /* Floating now-playing bottom bar */
    .mini-now-playing {
        position: fixed;
        bottom: 0; left: 0; right: 0;
        background: rgba(6,6,16,0.92);
        backdrop-filter: blur(20px);
        -webkit-backdrop-filter: blur(20px);
        border-top: 1px solid rgba(244,63,94,0.18);
        padding: 8px 24px;
        display: flex;
        align-items: center;
        gap: 14px;
        z-index: 9999;
        box-shadow: 0 -8px 32px rgba(0,0,0,0.4);
    }
    .mini-now-playing .mnp-thumb {
        width: 36px; height: 36px;
        border-radius: 6px;
        object-fit: cover;
        border: 1px solid rgba(244,63,94,0.3);
    }
    .mini-now-playing .mnp-title {
        font-size: 0.8rem; font-weight: 700; color: #fff;
        white-space: nowrap; overflow: hidden; text-overflow: ellipsis; max-width: 220px;
    }
    .mini-now-playing .mnp-artist {
        font-size: 0.68rem; color: rgba(255,255,255,0.45);
    }
    .mnp-bars {
        display: flex; align-items: flex-end; gap: 2px; height: 16px; margin-left: 4px;
    }
    .mnp-bar {
        width: 3px; border-radius: 2px;
        background: linear-gradient(180deg,#f43f5e,#a855f7);
        animation: wavePulse 1.2s ease-in-out infinite;
    }
    .mnp-bar:nth-child(1){height:6px;animation-delay:0s;}
    .mnp-bar:nth-child(2){height:10px;animation-delay:0.15s;}
    .mnp-bar:nth-child(3){height:8px;animation-delay:0.3s;}
    .mnp-bar:nth-child(4){height:13px;animation-delay:0.45s;}

    /* Genre / tag pills */
    .genre-pill {
        display: inline-block;
        background: linear-gradient(135deg, rgba(168,85,247,0.12), rgba(244,63,94,0.08));
        border: 1px solid rgba(168,85,247,0.22);
        border-radius: 20px;
        padding: 3px 11px;
        font-size: 0.68rem;
        font-weight: 600;
        color: #c084fc;
        margin: 2px 3px 2px 0;
        letter-spacing: 0.02em;
    }

    /* Song result card with shimmer on hover */
    .search-result-card {
        background: rgba(12,18,38,0.55);
        border: 1px solid rgba(255,255,255,0.06);
        border-radius: 18px;
        padding: 14px;
        margin-bottom: 10px;
        transition: all 0.25s cubic-bezier(0.4,0,0.2,1);
        position: relative;
        overflow: hidden;
    }
    .search-result-card::after {
        content: '';
        position: absolute;
        inset: 0;
        background: linear-gradient(120deg, transparent 30%, rgba(244,63,94,0.07) 50%, transparent 70%);
        transform: translateX(-100%);
        transition: transform 0.5s ease;
    }
    .search-result-card:hover::after {
        transform: translateX(100%);
    }
    .search-result-card:hover {
        border-color: rgba(244,63,94,0.28);
        transform: translateY(-2px);
        box-shadow: 0 12px 32px -8px rgba(244,63,94,0.18);
    }

    /* Keyboard shortcuts badge */
    .kbd-badge {
        display: inline-flex;
        align-items: center;
        justify-content: center;
        background: rgba(255,255,255,0.06);
        border: 1px solid rgba(255,255,255,0.12);
        border-bottom: 2px solid rgba(255,255,255,0.18);
        border-radius: 5px;
        padding: 1px 6px;
        font-size: 0.62rem;
        font-weight: 700;
        color: rgba(255,255,255,0.55);
        font-family: monospace;
        margin: 0 2px;
    }

    /* Inline star rating row */
    .inline-stars {
        display: flex;
        gap: 2px;
        align-items: center;
    }
    .inline-stars span {
        font-size: 1.1rem;
        cursor: pointer;
        transition: transform 0.15s, filter 0.15s;
    }
    .inline-stars span:hover {
        transform: scale(1.25);
        filter: drop-shadow(0 0 4px rgba(251,191,36,0.6));
    }

    /* Queue track number badge */
    .q-num-badge {
        width: 22px; height: 22px;
        border-radius: 50%;
        background: rgba(255,255,255,0.05);
        border: 1px solid rgba(255,255,255,0.1);
        display: flex; align-items: center; justify-content: center;
        font-size: 0.6rem; font-weight: 700;
        color: rgba(255,255,255,0.4);
        flex-shrink: 0;
    }
    .q-num-badge.active-q {
        background: rgba(244,63,94,0.2);
        border-color: rgba(244,63,94,0.5);
        color: #f43f5e;
    }

    /* Stats chart bar */
    .stat-bar-wrap { margin-bottom: 6px; }
    .stat-bar-track {
        background: rgba(255,255,255,0.04);
        border-radius: 100px;
        height: 8px;
        overflow: hidden;
        margin-top: 4px;
    }
    .stat-bar-fill {
        height: 100%;
        border-radius: 100px;
        background: linear-gradient(90deg, #f43f5e, #a855f7);
        transition: width 0.6s cubic-bezier(0.4,0,0.2,1);
    }

    /* Tooltip-style info tag */
    .info-tag {
        display: inline-flex;
        align-items: center;
        gap: 4px;
        font-size: 0.68rem;
        color: rgba(255,255,255,0.38);
        background: rgba(255,255,255,0.03);
        border: 1px solid rgba(255,255,255,0.07);
        border-radius: 6px;
        padding: 2px 7px;
    }

    /* Page section header pill */
    .section-header-pill {
        display: inline-flex;
        align-items: center;
        gap: 7px;
        background: linear-gradient(135deg, rgba(244,63,94,0.1), rgba(168,85,247,0.08));
        border: 1px solid rgba(244,63,94,0.2);
        border-radius: 12px;
        padding: 6px 14px;
        margin-bottom: 18px;
    }
    .section-header-pill span.pill-label {
        font-size: 0.75rem;
        font-weight: 700;
        color: rgba(255,255,255,0.5);
        text-transform: uppercase;
        letter-spacing: 0.08em;
    }
    .section-header-pill span.pill-icon {
        font-size: 1rem;
    }

    /* Pulse dot (live indicator) */
    .live-dot {
        width: 7px; height: 7px;
        border-radius: 50%;
        background: #22c55e;
        display: inline-block;
        box-shadow: 0 0 0 0 rgba(34,197,94,0.6);
        animation: livePulse 1.5s ease-out infinite;
    }
    @keyframes livePulse {
        0% { box-shadow: 0 0 0 0 rgba(34,197,94,0.55); }
        70% { box-shadow: 0 0 0 7px rgba(34,197,94,0); }
        100% { box-shadow: 0 0 0 0 rgba(34,197,94,0); }
    }

    /* Gradient text utility */
    .grad-text {
        background: linear-gradient(135deg, #f43f5e 0%, #a855f7 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
    }

    /* Duration chip */
    .dur-chip {
        background: rgba(255,255,255,0.04);
        border: 1px solid rgba(255,255,255,0.07);
        border-radius: 6px;
        padding: 2px 8px;
        font-size: 0.68rem;
        font-family: monospace;
        color: rgba(255,255,255,0.45);
    }
</style>
""", unsafe_allow_html=True)

# ── NEON UI ADDITIONS ─────────────────────────────────────────────────────────
st.markdown("""
<style>
    /* ═══════════════════════════════════════════════════
       NEON GLOW SYSTEM
    ═══════════════════════════════════════════════════ */

    /* Neon pink glow card */
    .neon-card-pink {
        background: rgba(8, 4, 18, 0.75);
        border: 1px solid #f43f5e;
        border-radius: 16px;
        padding: 16px;
        box-shadow: 0 0 12px rgba(244,63,94,0.35), inset 0 0 20px rgba(244,63,94,0.04);
        transition: box-shadow 0.3s ease;
    }
    .neon-card-pink:hover {
        box-shadow: 0 0 24px rgba(244,63,94,0.6), 0 0 48px rgba(244,63,94,0.2), inset 0 0 20px rgba(244,63,94,0.07);
    }

    /* Neon purple glow card */
    .neon-card-purple {
        background: rgba(8, 4, 18, 0.75);
        border: 1px solid #a855f7;
        border-radius: 16px;
        padding: 16px;
        box-shadow: 0 0 12px rgba(168,85,247,0.35), inset 0 0 20px rgba(168,85,247,0.04);
        transition: box-shadow 0.3s ease;
    }
    .neon-card-purple:hover {
        box-shadow: 0 0 24px rgba(168,85,247,0.6), 0 0 48px rgba(168,85,247,0.2), inset 0 0 20px rgba(168,85,247,0.07);
    }

    /* Neon cyan glow card */
    .neon-card-cyan {
        background: rgba(4, 12, 18, 0.75);
        border: 1px solid #06b6d4;
        border-radius: 16px;
        padding: 16px;
        box-shadow: 0 0 12px rgba(6,182,212,0.35), inset 0 0 20px rgba(6,182,212,0.04);
        transition: box-shadow 0.3s ease;
    }
    .neon-card-cyan:hover {
        box-shadow: 0 0 24px rgba(6,182,212,0.6), 0 0 48px rgba(6,182,212,0.2), inset 0 0 20px rgba(6,182,212,0.07);
    }

    /* Neon green glow card */
    .neon-card-green {
        background: rgba(4, 14, 8, 0.75);
        border: 1px solid #22c55e;
        border-radius: 16px;
        padding: 16px;
        box-shadow: 0 0 12px rgba(34,197,94,0.3), inset 0 0 20px rgba(34,197,94,0.03);
        transition: box-shadow 0.3s ease;
    }
    .neon-card-green:hover {
        box-shadow: 0 0 24px rgba(34,197,94,0.55), 0 0 48px rgba(34,197,94,0.18), inset 0 0 20px rgba(34,197,94,0.06);
    }

    /* Neon orange glow card */
    .neon-card-orange {
        background: rgba(14, 8, 4, 0.75);
        border: 1px solid #f97316;
        border-radius: 16px;
        padding: 16px;
        box-shadow: 0 0 12px rgba(249,115,22,0.3), inset 0 0 20px rgba(249,115,22,0.03);
        transition: box-shadow 0.3s ease;
    }
    .neon-card-orange:hover {
        box-shadow: 0 0 24px rgba(249,115,22,0.55), 0 0 48px rgba(249,115,22,0.18), inset 0 0 20px rgba(249,115,22,0.06);
    }

    /* Neon text styles */
    .neon-text-pink {
        color: #ff2d6b;
        text-shadow: 0 0 8px rgba(255,45,107,0.8), 0 0 20px rgba(255,45,107,0.4);
    }
    .neon-text-purple {
        color: #c084fc;
        text-shadow: 0 0 8px rgba(192,132,252,0.8), 0 0 20px rgba(192,132,252,0.4);
    }
    .neon-text-cyan {
        color: #22d3ee;
        text-shadow: 0 0 8px rgba(34,211,238,0.8), 0 0 20px rgba(34,211,238,0.4);
    }
    .neon-text-green {
        color: #4ade80;
        text-shadow: 0 0 8px rgba(74,222,128,0.8), 0 0 20px rgba(74,222,128,0.4);
    }

    /* Neon heading with animated flicker */
    .neon-heading {
        font-size: 2rem;
        font-weight: 800;
        letter-spacing: -0.02em;
        background: linear-gradient(135deg, #ff2d6b 0%, #c084fc 50%, #22d3ee 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        filter: drop-shadow(0 0 8px rgba(244,63,94,0.5));
        animation: neonFlicker 4s ease-in-out infinite;
    }
    @keyframes neonFlicker {
        0%, 95%, 100% { filter: drop-shadow(0 0 8px rgba(244,63,94,0.5)); }
        96% { filter: drop-shadow(0 0 2px rgba(244,63,94,0.1)); }
        97% { filter: drop-shadow(0 0 10px rgba(244,63,94,0.7)); }
        98% { filter: drop-shadow(0 0 3px rgba(244,63,94,0.2)); }
    }

    /* Neon divider line */
    .neon-divider {
        height: 1px;
        background: linear-gradient(90deg, transparent, #f43f5e, #a855f7, #06b6d4, transparent);
        border: none;
        margin: 1.5rem 0;
        box-shadow: 0 0 8px rgba(168,85,247,0.4);
    }

    /* Neon badge / tag */
    .neon-badge {
        display: inline-flex;
        align-items: center;
        gap: 5px;
        border-radius: 20px;
        padding: 4px 12px;
        font-size: 0.7rem;
        font-weight: 700;
        letter-spacing: 0.05em;
        text-transform: uppercase;
    }
    .neon-badge-pink {
        background: rgba(244,63,94,0.1);
        border: 1px solid #f43f5e;
        color: #f43f5e;
        box-shadow: 0 0 8px rgba(244,63,94,0.3);
    }
    .neon-badge-purple {
        background: rgba(168,85,247,0.1);
        border: 1px solid #a855f7;
        color: #c084fc;
        box-shadow: 0 0 8px rgba(168,85,247,0.3);
    }
    .neon-badge-cyan {
        background: rgba(6,182,212,0.1);
        border: 1px solid #06b6d4;
        color: #22d3ee;
        box-shadow: 0 0 8px rgba(6,182,212,0.3);
    }
    .neon-badge-green {
        background: rgba(34,197,94,0.1);
        border: 1px solid #22c55e;
        color: #4ade80;
        box-shadow: 0 0 8px rgba(34,197,94,0.3);
    }

    /* Neon pulsing ring avatar */
    .neon-avatar {
        border-radius: 50%;
        box-shadow: 0 0 0 3px #f43f5e, 0 0 16px rgba(244,63,94,0.5);
        animation: neonRingPulse 2s ease-in-out infinite;
    }
    @keyframes neonRingPulse {
        0%, 100% { box-shadow: 0 0 0 3px #f43f5e, 0 0 16px rgba(244,63,94,0.5); }
        50% { box-shadow: 0 0 0 5px #a855f7, 0 0 28px rgba(168,85,247,0.6); }
    }

    /* Neon progress bar */
    .neon-progress-track {
        background: rgba(255,255,255,0.04);
        border-radius: 100px;
        height: 6px;
        overflow: visible;
        position: relative;
    }
    .neon-progress-fill {
        height: 100%;
        border-radius: 100px;
        background: linear-gradient(90deg, #f43f5e, #a855f7, #06b6d4);
        box-shadow: 0 0 10px rgba(168,85,247,0.6), 0 0 20px rgba(244,63,94,0.3);
        position: relative;
    }
    .neon-progress-fill::after {
        content: '';
        position: absolute;
        right: -1px;
        top: 50%;
        transform: translateY(-50%);
        width: 10px;
        height: 10px;
        border-radius: 50%;
        background: #fff;
        box-shadow: 0 0 8px #a855f7, 0 0 16px #f43f5e;
    }

    /* Neon stat number */
    .neon-stat-num {
        font-size: 2.4rem;
        font-weight: 900;
        line-height: 1;
    }

    /* Neon scanline overlay (subtle CRT effect on cards) */
    .neon-scanlines {
        position: relative;
        overflow: hidden;
    }
    .neon-scanlines::before {
        content: '';
        position: absolute;
        inset: 0;
        background: repeating-linear-gradient(
            0deg,
            transparent,
            transparent 2px,
            rgba(0,0,0,0.03) 2px,
            rgba(0,0,0,0.03) 4px
        );
        pointer-events: none;
        z-index: 1;
    }

    /* Neon grid background pattern for section headers */
    .neon-grid-header {
        background:
            linear-gradient(rgba(244,63,94,0.04) 1px, transparent 1px),
            linear-gradient(90deg, rgba(244,63,94,0.04) 1px, transparent 1px),
            linear-gradient(135deg, rgba(168,85,247,0.06) 0%, rgba(244,63,94,0.06) 100%);
        background-size: 40px 40px, 40px 40px, 100% 100%;
        border: 1px solid rgba(244,63,94,0.15);
        border-radius: 18px;
        padding: 18px 22px;
        margin-bottom: 22px;
        position: relative;
    }
    .neon-grid-header::before {
        content: '';
        position: absolute;
        top: -1px; left: 20px; right: 20px; height: 1px;
        background: linear-gradient(90deg, transparent, #f43f5e, #a855f7, transparent);
        box-shadow: 0 0 8px rgba(168,85,247,0.5);
    }

    /* Neon song card enhancement */
    .song-item-card:hover {
        box-shadow: 0 0 16px rgba(244,63,94,0.25), 0 12px 32px -8px rgba(244,63,94,0.22) !important;
    }

    /* Neon sidebar now-playing glow */
    [data-testid="stSidebar"] .stButton > button:hover {
        box-shadow: 0 0 12px rgba(244,63,94,0.4) !important;
    }

    /* Neon active tab indicator */
    .stTabs [aria-selected="true"] {
        box-shadow: 0 0 10px rgba(244,63,94,0.3) !important;
    }

    /* Neon input focus glow */
    .stTextInput>div>div>input:focus {
        box-shadow: 0 0 0 2px rgba(244,63,94,0.15), 0 0 12px rgba(244,63,94,0.2) !important;
    }

    /* Neon button primary glow on hover */
    .stButton > button:hover {
        box-shadow: 0 0 14px rgba(244,63,94,0.3), 0 4px 16px -4px rgba(244,63,94,0.25) !important;
    }

    /* Neon colour sweep animation for section dividers */
    .neon-sweep {
        height: 2px;
        background: linear-gradient(90deg, transparent 0%, #f43f5e 25%, #a855f7 50%, #06b6d4 75%, transparent 100%);
        background-size: 200% 100%;
        animation: neonSweep 3s linear infinite;
        border-radius: 2px;
        margin: 1rem 0;
    }
    @keyframes neonSweep {
        0% { background-position: 100% 0; }
        100% { background-position: -100% 0; }
    }

    /* Neon glow on thumbnails */
    .neon-thumb {
        border-radius: 10px;
        border: 1px solid rgba(168,85,247,0.4);
        box-shadow: 0 0 10px rgba(168,85,247,0.25);
    }

    /* Equalizer bars — larger, neon version */
    .eq-bar {
        display: inline-block;
        width: 4px;
        border-radius: 3px;
        background: linear-gradient(180deg, #22d3ee, #a855f7, #f43f5e);
        box-shadow: 0 0 6px rgba(168,85,247,0.6);
        animation: eqPulse 1s ease-in-out infinite;
        margin: 0 1.5px;
    }
    .eq-bar:nth-child(1){height:10px;animation-delay:0s;}
    .eq-bar:nth-child(2){height:18px;animation-delay:0.1s;}
    .eq-bar:nth-child(3){height:14px;animation-delay:0.2s;}
    .eq-bar:nth-child(4){height:22px;animation-delay:0.3s;}
    .eq-bar:nth-child(5){height:10px;animation-delay:0.4s;}
    .eq-bar:nth-child(6){height:16px;animation-delay:0.5s;}
    .eq-bar:nth-child(7){height:20px;animation-delay:0.15s;}
    @keyframes eqPulse {
        0%,100%{transform:scaleY(0.4);opacity:0.7;}
        50%{transform:scaleY(1);opacity:1;}
    }

    /* Neon floating particles bg (purely decorative CSS) */
    .neon-particle-bg {
        position: relative;
    }
    .neon-particle-bg::after {
        content: '';
        position: absolute;
        inset: 0;
        background:
            radial-gradient(circle 2px at 15% 25%, rgba(244,63,94,0.5) 0%, transparent 100%),
            radial-gradient(circle 2px at 85% 70%, rgba(168,85,247,0.5) 0%, transparent 100%),
            radial-gradient(circle 2px at 50% 90%, rgba(6,182,212,0.5) 0%, transparent 100%),
            radial-gradient(circle 1px at 30% 60%, rgba(34,197,94,0.4) 0%, transparent 100%),
            radial-gradient(circle 1px at 70% 20%, rgba(249,115,22,0.4) 0%, transparent 100%);
        pointer-events: none;
        border-radius: inherit;
        animation: particleDrift 6s ease-in-out infinite alternate;
    }
    @keyframes particleDrift {
        0% { opacity: 0.4; transform: translateY(0); }
        100% { opacity: 0.9; transform: translateY(-4px); }
    }
</style>
""", unsafe_allow_html=True)

# ── LAVENDER THEME & EXTRAORDINARY UI ADDITIONS ──────────────────────────────
st.markdown("""
<style>
    /* ═══════════════════════════════════════════════════
       LAVENDER THEME — complete palette injection
    ═══════════════════════════════════════════════════ */

    :root {
        --lavender-50:  #f5f3ff;
        --lavender-100: #ede9fe;
        --lavender-200: #ddd6fe;
        --lavender-300: #c4b5fd;
        --lavender-400: #a78bfa;
        --lavender-500: #8b5cf6;
        --lavender-600: #7c3aed;
        --lavender-700: #6d28d9;
        --lavender-800: #5b21b6;
        --lavender-900: #4c1d95;
        --rose-neon:    #ff2d6b;
        --cyan-neon:    #00f5ff;
        --gold-neon:    #ffd700;
        --mint-neon:    #00ffb3;
        --coral-neon:   #ff6b6b;
        --electric-blue:#4361ee;
    }

    /* ── Lavender Glow Card ── */
    .lavender-card {
        background: linear-gradient(135deg,
            rgba(139,92,246,0.10) 0%,
            rgba(196,181,253,0.06) 50%,
            rgba(109,40,217,0.10) 100%);
        border: 1px solid rgba(167,139,250,0.35);
        border-radius: 18px;
        padding: 18px;
        box-shadow:
            0 0 16px rgba(139,92,246,0.22),
            0 0 40px rgba(139,92,246,0.08),
            inset 0 0 24px rgba(139,92,246,0.04);
        transition: box-shadow 0.3s ease, transform 0.25s ease;
        position: relative;
        overflow: hidden;
    }
    .lavender-card::before {
        content: '';
        position: absolute;
        top: -1px; left: 20%; right: 20%; height: 1px;
        background: linear-gradient(90deg, transparent, #a78bfa, #c4b5fd, #a78bfa, transparent);
        box-shadow: 0 0 8px rgba(167,139,250,0.8);
    }
    .lavender-card:hover {
        box-shadow:
            0 0 28px rgba(139,92,246,0.45),
            0 0 60px rgba(139,92,246,0.15),
            inset 0 0 28px rgba(139,92,246,0.06);
        transform: translateY(-3px);
    }

    /* ── Lavender Neon Text ── */
    .lavender-neon-text {
        color: #c4b5fd;
        text-shadow:
            0 0 6px rgba(196,181,253,0.9),
            0 0 14px rgba(167,139,250,0.7),
            0 0 28px rgba(139,92,246,0.5);
    }
    .lavender-gradient-text {
        background: linear-gradient(135deg, #e9d5ff 0%, #a78bfa 40%, #7c3aed 80%, #4c1d95 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        filter: drop-shadow(0 0 8px rgba(167,139,250,0.6));
    }

    /* ── Lavender Badge / Tag ── */
    .lavender-badge {
        display: inline-flex;
        align-items: center;
        gap: 5px;
        background: rgba(139,92,246,0.12);
        border: 1px solid rgba(167,139,250,0.45);
        border-radius: 20px;
        padding: 4px 13px;
        font-size: 0.7rem;
        font-weight: 700;
        letter-spacing: 0.05em;
        text-transform: uppercase;
        color: #c4b5fd;
        box-shadow: 0 0 8px rgba(139,92,246,0.28);
    }

    /* ── Lavender Progress Bar ── */
    .lavender-progress-track {
        background: rgba(139,92,246,0.08);
        border: 1px solid rgba(167,139,250,0.15);
        border-radius: 100px;
        height: 8px;
        overflow: hidden;
    }
    .lavender-progress-fill {
        height: 100%;
        border-radius: 100px;
        background: linear-gradient(90deg, #7c3aed, #a78bfa, #c4b5fd);
        box-shadow: 0 0 10px rgba(167,139,250,0.6), 0 0 20px rgba(139,92,246,0.3);
        position: relative;
    }
    .lavender-progress-fill::after {
        content: '';
        position: absolute;
        right: -2px; top: 50%; transform: translateY(-50%);
        width: 12px; height: 12px; border-radius: 50%;
        background: #e9d5ff;
        box-shadow: 0 0 8px #a78bfa, 0 0 16px #7c3aed;
    }

    /* ── Lavender Divider ── */
    .lavender-divider {
        height: 1px;
        background: linear-gradient(90deg, transparent, #7c3aed, #a78bfa, #c4b5fd, #a78bfa, #7c3aed, transparent);
        border: none;
        margin: 1.5rem 0;
        box-shadow: 0 0 10px rgba(167,139,250,0.5);
    }

    /* ── Lavender Glow Button ── */
    .lavender-btn {
        background: linear-gradient(135deg, rgba(124,58,237,0.18), rgba(167,139,250,0.12));
        border: 1px solid rgba(167,139,250,0.45);
        border-radius: 12px;
        padding: 10px 22px;
        color: #c4b5fd;
        font-weight: 700;
        font-size: 0.85rem;
        cursor: pointer;
        transition: all 0.22s ease;
        box-shadow: 0 0 10px rgba(139,92,246,0.2);
        font-family: 'Outfit', sans-serif;
        letter-spacing: 0.02em;
    }
    .lavender-btn:hover {
        background: linear-gradient(135deg, rgba(124,58,237,0.38), rgba(167,139,250,0.28));
        box-shadow: 0 0 20px rgba(167,139,250,0.5), 0 0 40px rgba(139,92,246,0.2);
        transform: translateY(-2px);
        color: #e9d5ff;
    }

    /* ── Lavender Grid Section Header ── */
    .lavender-section-header {
        background:
            linear-gradient(rgba(139,92,246,0.05) 1px, transparent 1px),
            linear-gradient(90deg, rgba(139,92,246,0.05) 1px, transparent 1px),
            linear-gradient(135deg, rgba(124,58,237,0.08) 0%, rgba(167,139,250,0.06) 100%);
        background-size: 36px 36px, 36px 36px, 100% 100%;
        border: 1px solid rgba(167,139,250,0.18);
        border-radius: 18px;
        padding: 18px 22px;
        margin-bottom: 22px;
        position: relative;
    }
    .lavender-section-header::before {
        content: '';
        position: absolute;
        top: -1px; left: 18px; right: 18px; height: 1px;
        background: linear-gradient(90deg, transparent, #a78bfa, #c4b5fd, #a78bfa, transparent);
        box-shadow: 0 0 8px rgba(167,139,250,0.6);
    }
    .lavender-section-header::after {
        content: '';
        position: absolute;
        bottom: -1px; left: 18px; right: 18px; height: 1px;
        background: linear-gradient(90deg, transparent, #7c3aed, #a78bfa, #7c3aed, transparent);
        box-shadow: 0 0 6px rgba(124,58,237,0.4);
    }

    /* ── Lavender Floating Orb ── */
    .lavender-orb {
        width: 80px; height: 80px;
        border-radius: 50%;
        background: radial-gradient(circle, rgba(196,181,253,0.3) 0%, rgba(139,92,246,0.15) 50%, transparent 70%);
        box-shadow:
            0 0 20px rgba(167,139,250,0.4),
            0 0 40px rgba(139,92,246,0.2),
            inset 0 0 20px rgba(196,181,253,0.1);
        animation: lavenderOrb 4s ease-in-out infinite alternate;
        display: flex; align-items: center; justify-content: center;
        font-size: 2rem;
    }
    @keyframes lavenderOrb {
        0%  { box-shadow: 0 0 20px rgba(167,139,250,0.4), 0 0 40px rgba(139,92,246,0.2); transform: scale(1); }
        100%{ box-shadow: 0 0 36px rgba(167,139,250,0.7), 0 0 70px rgba(139,92,246,0.35); transform: scale(1.08); }
    }

    /* ── Lavender Animated Border Card ── */
    .lavender-border-card {
        position: relative;
        background: rgba(8, 5, 20, 0.82);
        border-radius: 18px;
        padding: 18px;
        overflow: hidden;
    }
    .lavender-border-card::before {
        content: '';
        position: absolute;
        inset: -1px;
        border-radius: 18px;
        background: linear-gradient(135deg, #7c3aed, #a78bfa, #c4b5fd, #7c3aed);
        background-size: 300% 300%;
        animation: lavenderBorderSpin 4s linear infinite;
        z-index: 0;
    }
    .lavender-border-card::after {
        content: '';
        position: absolute;
        inset: 1px;
        border-radius: 17px;
        background: rgba(8,5,20,0.92);
        z-index: 1;
    }
    .lavender-border-card > * { position: relative; z-index: 2; }
    @keyframes lavenderBorderSpin {
        0%   { background-position: 0% 50%; }
        50%  { background-position: 100% 50%; }
        100% { background-position: 0% 50%; }
    }

    /* ── MULTI-COLOUR NEON ADDITIONS ── */

    /* Gold neon card */
    .neon-card-gold {
        background: rgba(14, 10, 4, 0.75);
        border: 1px solid #ffd700;
        border-radius: 16px;
        padding: 16px;
        box-shadow: 0 0 12px rgba(255,215,0,0.35), inset 0 0 20px rgba(255,215,0,0.03);
        transition: box-shadow 0.3s ease;
    }
    .neon-card-gold:hover {
        box-shadow: 0 0 28px rgba(255,215,0,0.65), 0 0 56px rgba(255,215,0,0.2), inset 0 0 28px rgba(255,215,0,0.06);
    }

    /* Electric blue neon card */
    .neon-card-blue {
        background: rgba(4, 6, 18, 0.75);
        border: 1px solid #4361ee;
        border-radius: 16px;
        padding: 16px;
        box-shadow: 0 0 12px rgba(67,97,238,0.35), inset 0 0 20px rgba(67,97,238,0.04);
        transition: box-shadow 0.3s ease;
    }
    .neon-card-blue:hover {
        box-shadow: 0 0 28px rgba(67,97,238,0.6), 0 0 56px rgba(67,97,238,0.18), inset 0 0 28px rgba(67,97,238,0.06);
    }

    /* Coral / mint neon text */
    .neon-text-coral  { color: #ff6b6b; text-shadow: 0 0 8px rgba(255,107,107,0.8), 0 0 20px rgba(255,107,107,0.4); }
    .neon-text-gold   { color: #ffd700; text-shadow: 0 0 8px rgba(255,215,0,0.9),   0 0 20px rgba(255,215,0,0.5); }
    .neon-text-mint   { color: #00ffb3; text-shadow: 0 0 8px rgba(0,255,179,0.9),   0 0 20px rgba(0,255,179,0.5); }
    .neon-text-blue   { color: #4361ee; text-shadow: 0 0 8px rgba(67,97,238,0.9),   0 0 20px rgba(67,97,238,0.5); }

    /* Gold / mint / coral neon badges */
    .neon-badge-gold {
        background: rgba(255,215,0,0.1); border: 1px solid #ffd700;
        color: #ffd700; box-shadow: 0 0 8px rgba(255,215,0,0.4);
    }
    .neon-badge-mint {
        background: rgba(0,255,179,0.08); border: 1px solid #00ffb3;
        color: #00ffb3; box-shadow: 0 0 8px rgba(0,255,179,0.35);
    }
    .neon-badge-coral {
        background: rgba(255,107,107,0.08); border: 1px solid #ff6b6b;
        color: #ff6b6b; box-shadow: 0 0 8px rgba(255,107,107,0.35);
    }

    /* ── EXTRAORDINARY UI COMPONENTS ── */

    /* Aurora background card */
    .aurora-card {
        background:
            radial-gradient(ellipse 70% 55% at 20% 30%, rgba(139,92,246,0.14) 0%, transparent 55%),
            radial-gradient(ellipse 50% 50% at 80% 70%, rgba(244,63,94,0.10) 0%, transparent 55%),
            radial-gradient(ellipse 60% 60% at 55% 10%, rgba(6,182,212,0.08) 0%, transparent 55%),
            rgba(8,6,22,0.88);
        border: 1px solid rgba(167,139,250,0.18);
        border-radius: 20px;
        padding: 20px;
        backdrop-filter: blur(14px);
        -webkit-backdrop-filter: blur(14px);
        animation: auroraShift 8s ease-in-out infinite alternate;
        position: relative;
        overflow: hidden;
    }
    @keyframes auroraShift {
        0%  { background-position: 0% 0%; }
        100%{ background-position: 100% 100%; }
    }

    /* Holographic shimmer */
    .holographic-card {
        background: rgba(8, 6, 22, 0.88);
        border: 1px solid transparent;
        border-radius: 18px;
        padding: 18px;
        position: relative;
        overflow: hidden;
    }
    .holographic-card::before {
        content: '';
        position: absolute;
        inset: 0;
        background: linear-gradient(
            135deg,
            rgba(255,0,128,0.06) 0%,
            rgba(139,92,246,0.10) 25%,
            rgba(0,255,255,0.06) 50%,
            rgba(255,215,0,0.06) 75%,
            rgba(255,0,128,0.06) 100%
        );
        background-size: 400% 400%;
        animation: holoShift 6s linear infinite;
        border-radius: inherit;
        pointer-events: none;
    }
    .holographic-card::after {
        content: '';
        position: absolute;
        inset: -1px;
        border-radius: 18px;
        background: linear-gradient(135deg, #ff007f44, #8b5cf655, #00ffff44, #ffd70044, #ff007f44);
        background-size: 400% 400%;
        animation: holoShift 6s linear infinite;
        z-index: -1;
    }
    @keyframes holoShift {
        0%   { background-position: 0% 50%; }
        50%  { background-position: 100% 50%; }
        100% { background-position: 0% 50%; }
    }

    /* Morphing gradient button */
    .morph-btn {
        position: relative;
        background: linear-gradient(135deg, #7c3aed, #a855f7, #f43f5e, #06b6d4, #7c3aed);
        background-size: 300% 300%;
        animation: morphBtnGrad 5s ease infinite;
        border: none;
        border-radius: 14px;
        padding: 12px 26px;
        color: #fff;
        font-weight: 800;
        font-size: 0.88rem;
        cursor: pointer;
        box-shadow: 0 0 24px rgba(139,92,246,0.4), 0 0 48px rgba(244,63,94,0.2);
        font-family: 'Outfit', sans-serif;
        letter-spacing: 0.03em;
        transition: transform 0.2s, box-shadow 0.2s;
    }
    .morph-btn:hover {
        transform: translateY(-3px) scale(1.02);
        box-shadow: 0 0 40px rgba(139,92,246,0.6), 0 0 80px rgba(244,63,94,0.3);
    }
    @keyframes morphBtnGrad {
        0%   { background-position: 0% 50%; }
        50%  { background-position: 100% 50%; }
        100% { background-position: 0% 50%; }
    }

    /* Floating emoji / icon with glow */
    .float-icon {
        display: inline-flex;
        align-items: center;
        justify-content: center;
        width: 48px; height: 48px;
        border-radius: 14px;
        background: rgba(139,92,246,0.1);
        border: 1px solid rgba(167,139,250,0.3);
        box-shadow: 0 0 12px rgba(139,92,246,0.25);
        font-size: 1.4rem;
        animation: iconFloat 3s ease-in-out infinite alternate;
        flex-shrink: 0;
    }
    @keyframes iconFloat {
        0%  { transform: translateY(0px);   box-shadow: 0 0 12px rgba(139,92,246,0.25); }
        100%{ transform: translateY(-5px);  box-shadow: 0 0 22px rgba(139,92,246,0.5); }
    }

    /* Glass pill stats row */
    .glass-pill-row {
        display: flex;
        gap: 10px;
        flex-wrap: wrap;
    }
    .glass-pill {
        display: inline-flex;
        align-items: center;
        gap: 6px;
        background: rgba(255,255,255,0.03);
        border: 1px solid rgba(255,255,255,0.08);
        border-radius: 50px;
        padding: 6px 14px;
        font-size: 0.74rem;
        font-weight: 600;
        color: rgba(255,255,255,0.55);
        backdrop-filter: blur(8px);
        transition: all 0.2s;
    }
    .glass-pill:hover {
        background: rgba(139,92,246,0.1);
        border-color: rgba(167,139,250,0.3);
        color: #c4b5fd;
        box-shadow: 0 0 8px rgba(139,92,246,0.2);
    }
    .glass-pill .pip { width: 6px; height: 6px; border-radius: 50%; flex-shrink: 0; }

    /* Prismatic number display */
    .prism-number {
        font-size: 3.2rem;
        font-weight: 900;
        line-height: 1;
        background: linear-gradient(135deg,
            #ff2d6b 0%, #f43f5e 15%,
            #c4b5fd 35%, #a78bfa 50%,
            #06b6d4 70%, #22d3ee 85%,
            #00ffb3 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-size: 200% 200%;
        animation: prismShift 4s ease infinite alternate;
        filter: drop-shadow(0 0 10px rgba(167,139,250,0.5));
    }
    @keyframes prismShift {
        0%  { background-position: 0% 50%; }
        100%{ background-position: 100% 50%; }
    }

    /* Neon outline text */
    .neon-outline-text {
        font-size: 2.2rem;
        font-weight: 900;
        color: transparent;
        -webkit-text-stroke: 2px #a78bfa;
        text-stroke: 2px #a78bfa;
        text-shadow:
            0 0 12px rgba(167,139,250,0.7),
            0 0 24px rgba(139,92,246,0.4);
        letter-spacing: -0.02em;
    }

    /* Translucent rainbow separator */
    .rainbow-sep {
        height: 2px;
        background: linear-gradient(90deg,
            #ff2d6b, #ff6b6b, #ffd700, #00ffb3,
            #06b6d4, #a78bfa, #7c3aed, #ff2d6b);
        background-size: 200% 100%;
        animation: rainbowFlow 4s linear infinite;
        border: none;
        border-radius: 2px;
        margin: 1.2rem 0;
        box-shadow: 0 0 8px rgba(167,139,250,0.3);
    }
    @keyframes rainbowFlow {
        0%  { background-position: 0% 0; }
        100%{ background-position: 200% 0; }
    }

    /* Constellation dot pattern overlay */
    .constellation-bg {
        position: relative;
        overflow: hidden;
    }
    .constellation-bg::before {
        content: '';
        position: absolute;
        inset: 0;
        background-image:
            radial-gradient(circle 1px at 10% 20%, rgba(196,181,253,0.5) 0%, transparent 100%),
            radial-gradient(circle 1px at 30% 80%, rgba(167,139,250,0.4) 0%, transparent 100%),
            radial-gradient(circle 1px at 60% 40%, rgba(244,63,94,0.35) 0%, transparent 100%),
            radial-gradient(circle 1px at 80% 15%, rgba(6,182,212,0.4) 0%, transparent 100%),
            radial-gradient(circle 1px at 90% 65%, rgba(196,181,253,0.45) 0%, transparent 100%),
            radial-gradient(circle 1px at 45% 90%, rgba(255,215,0,0.35) 0%, transparent 100%),
            radial-gradient(circle 1px at 20% 55%, rgba(0,255,179,0.3) 0%, transparent 100%);
        pointer-events: none;
        border-radius: inherit;
        animation: constellationTwinkle 5s ease-in-out infinite alternate;
    }
    @keyframes constellationTwinkle {
        0%  { opacity: 0.5; }
        100%{ opacity: 1; }
    }

    /* Layered depth card (3D effect) */
    .depth-card {
        background: rgba(10,7,30,0.9);
        border: 1px solid rgba(167,139,250,0.2);
        border-radius: 18px;
        padding: 18px;
        box-shadow:
            0 1px 0 rgba(255,255,255,0.04) inset,
            0 -1px 0 rgba(0,0,0,0.5) inset,
            0 4px 6px rgba(0,0,0,0.4),
            0 12px 24px rgba(0,0,0,0.3),
            0 0 0 1px rgba(139,92,246,0.1),
            0 0 30px rgba(139,92,246,0.08);
        transform: perspective(800px) rotateX(0deg);
        transition: transform 0.3s ease, box-shadow 0.3s ease;
    }
    .depth-card:hover {
        transform: perspective(800px) rotateX(-2deg) translateY(-4px);
        box-shadow:
            0 1px 0 rgba(255,255,255,0.06) inset,
            0 -1px 0 rgba(0,0,0,0.6) inset,
            0 8px 16px rgba(0,0,0,0.5),
            0 24px 48px rgba(0,0,0,0.4),
            0 0 0 1px rgba(167,139,250,0.25),
            0 0 50px rgba(139,92,246,0.15);
    }

    /* Retro CRT scanline card with neon border */
    .crt-card {
        position: relative;
        background: rgba(4, 2, 12, 0.92);
        border: 1px solid rgba(167,139,250,0.35);
        border-radius: 14px;
        padding: 18px;
        overflow: hidden;
        box-shadow:
            0 0 0 2px rgba(139,92,246,0.08),
            0 0 20px rgba(139,92,246,0.2);
    }
    .crt-card::after {
        content: '';
        position: absolute;
        inset: 0;
        background: repeating-linear-gradient(
            0deg,
            transparent,
            transparent 2px,
            rgba(139,92,246,0.018) 2px,
            rgba(139,92,246,0.018) 4px
        );
        pointer-events: none;
        z-index: 2;
        border-radius: inherit;
    }

    /* Pulsing ring indicator */
    .ring-pulse {
        position: relative;
        display: inline-flex;
        align-items: center;
        justify-content: center;
    }
    .ring-pulse::before,
    .ring-pulse::after {
        content: '';
        position: absolute;
        inset: -6px;
        border-radius: 50%;
        border: 2px solid rgba(167,139,250,0.5);
        animation: ringPulseExpand 2s ease-out infinite;
    }
    .ring-pulse::after {
        animation-delay: 1s;
    }
    @keyframes ringPulseExpand {
        0%   { transform: scale(0.9); opacity: 0.7; }
        100% { transform: scale(1.6); opacity: 0; }
    }

    /* Lavender sidebar accent line */
    [data-testid="stSidebar"] {
        border-right: 1px solid rgba(139,92,246,0.12) !important;
    }
    [data-testid="stSidebar"]::before {
        content: '';
        position: absolute;
        top: 0; bottom: 0; right: -1px; width: 1px;
        background: linear-gradient(180deg, transparent, rgba(167,139,250,0.5), rgba(244,63,94,0.3), rgba(167,139,250,0.5), transparent);
        animation: sidebarGlow 4s ease-in-out infinite alternate;
    }
    @keyframes sidebarGlow {
        0%  { opacity: 0.4; }
        100%{ opacity: 1; }
    }

    /* Search result card lavender hover enhancement */
    .search-result-card:hover {
        background: rgba(139,92,246,0.07) !important;
        border-color: rgba(167,139,250,0.3) !important;
        box-shadow:
            0 0 16px rgba(139,92,246,0.2),
            0 12px 32px -8px rgba(244,63,94,0.15) !important;
    }

    /* Active queue item lavender flash */
    .active-q-lavender {
        background: rgba(139,92,246,0.15) !important;
        border-color: rgba(167,139,250,0.5) !important;
        box-shadow: 0 0 12px rgba(139,92,246,0.3);
    }

    /* Lavender tooltip style */
    .lav-tooltip {
        position: relative;
        cursor: help;
    }
    .lav-tooltip::after {
        content: attr(data-tip);
        position: absolute;
        bottom: 125%;
        left: 50%;
        transform: translateX(-50%);
        background: rgba(20,12,40,0.95);
        border: 1px solid rgba(167,139,250,0.3);
        border-radius: 8px;
        padding: 5px 10px;
        font-size: 0.68rem;
        color: #c4b5fd;
        white-space: nowrap;
        opacity: 0;
        pointer-events: none;
        transition: opacity 0.2s;
        box-shadow: 0 0 10px rgba(139,92,246,0.3);
        z-index: 9999;
    }
    .lav-tooltip:hover::after { opacity: 1; }

    /* Neon number counter badge */
    .neon-counter {
        display: inline-flex;
        align-items: center;
        justify-content: center;
        min-width: 24px;
        height: 24px;
        border-radius: 50%;
        background: linear-gradient(135deg, rgba(244,63,94,0.2), rgba(139,92,246,0.2));
        border: 1px solid rgba(167,139,250,0.4);
        font-size: 0.65rem;
        font-weight: 800;
        color: #c4b5fd;
        box-shadow: 0 0 6px rgba(139,92,246,0.35);
        padding: 0 5px;
        letter-spacing: 0.02em;
    }

    /* Crystalline input focus */
    .stTextInput>div>div>input:focus {
        border-color: rgba(167,139,250,0.7) !important;
        box-shadow:
            0 0 0 2px rgba(139,92,246,0.15),
            0 0 14px rgba(167,139,250,0.25),
            0 0 28px rgba(139,92,246,0.12) !important;
    }

    /* Lavender sidebar nav selected state enhancement */
    .nav-link-selected {
        box-shadow: 0 0 12px rgba(139,92,246,0.25) !important;
    }

    /* Animated background gradient for main area */
    .stApp::after {
        content: '';
        position: fixed;
        inset: 0;
        background:
            radial-gradient(ellipse 50% 40% at 50% 50%, rgba(139,92,246,0.025) 0%, transparent 60%),
            radial-gradient(ellipse 40% 30% at 10% 80%, rgba(244,63,94,0.03) 0%, transparent 55%),
            radial-gradient(ellipse 40% 30% at 90% 20%, rgba(6,182,212,0.025) 0%, transparent 55%);
        pointer-events: none;
        z-index: 0;
    }

    /* Enhanced song card: lavender shimmer */
    .song-item-card::before {
        content: '';
        position: absolute;
        top: 0; left: -100%; width: 60%; height: 100%;
        background: linear-gradient(120deg, transparent, rgba(167,139,250,0.06), transparent);
        transition: left 0.6s ease;
    }
    .song-item-card {
        position: relative;
        overflow: hidden;
    }
    .song-item-card:hover::before {
        left: 140%;
    }

    /* Neon glow tabs enhancement */
    .stTabs [aria-selected="true"] {
        text-shadow: 0 0 10px rgba(244,63,94,0.5) !important;
    }

    /* Soft lavender card for recommendations */
    .rec-card-lavender {
        background: linear-gradient(135deg, rgba(124,58,237,0.06), rgba(167,139,250,0.04));
        border: 1px solid rgba(167,139,250,0.18);
        border-radius: 14px;
        padding: 12px 14px;
        transition: all 0.22s ease;
        position: relative;
        overflow: hidden;
    }
    .rec-card-lavender:hover {
        background: linear-gradient(135deg, rgba(124,58,237,0.12), rgba(167,139,250,0.08));
        border-color: rgba(167,139,250,0.35);
        box-shadow: 0 0 14px rgba(139,92,246,0.2);
        transform: translateX(3px);
    }
    .rec-card-lavender::after {
        content: '';
        position: absolute;
        left: 0; top: 0; bottom: 0; width: 3px;
        background: linear-gradient(180deg, #7c3aed, #a78bfa, #c4b5fd);
        border-radius: 14px 0 0 14px;
    }

    /* Top-of-page lavender glow header bar */
    .stApp > header {
        background: linear-gradient(90deg,
            rgba(124,58,237,0.08),
            rgba(167,139,250,0.05),
            rgba(244,63,94,0.06)) !important;
        border-bottom: 1px solid rgba(167,139,250,0.1) !important;
    }

    /* Enhanced scrollbar — lavender */
    ::-webkit-scrollbar-thumb {
        background: rgba(139,92,246,0.25) !important;
    }
    ::-webkit-scrollbar-thumb:hover {
        background: rgba(167,139,250,0.5) !important;
    }

    /* Tooltip chip inside cards */
    .lav-chip {
        display: inline-flex;
        align-items: center;
        gap: 4px;
        background: rgba(139,92,246,0.08);
        border: 1px solid rgba(167,139,250,0.2);
        border-radius: 8px;
        padding: 2px 8px;
        font-size: 0.65rem;
        font-weight: 600;
        color: rgba(196,181,253,0.8);
        letter-spacing: 0.02em;
    }

    /* Neon sweep — lavender variant */
    .neon-sweep-lavender {
        height: 2px;
        background: linear-gradient(90deg,
            transparent 0%,
            #7c3aed 20%,
            #a78bfa 40%,
            #c4b5fd 50%,
            #a78bfa 60%,
            #7c3aed 80%,
            transparent 100%);
        background-size: 200% 100%;
        animation: neonSweep 3s linear infinite;
        border-radius: 2px;
        margin: 1rem 0;
        box-shadow: 0 0 10px rgba(167,139,250,0.5);
    }

    /* Hover card — lifting with lavender shadow */
    .lift-card {
        transition: transform 0.28s cubic-bezier(0.34,1.56,0.64,1), box-shadow 0.28s ease;
        cursor: pointer;
    }
    .lift-card:hover {
        transform: translateY(-6px) scale(1.015);
        box-shadow:
            0 12px 40px rgba(139,92,246,0.3),
            0 4px 12px rgba(0,0,0,0.4),
            0 0 0 1px rgba(167,139,250,0.2);
    }

    /* Rainbow neon heading animation */
    .rainbow-neon-heading {
        font-weight: 900;
        letter-spacing: -0.02em;
        background: linear-gradient(135deg,
            #ff2d6b, #f43f5e, #f97316,
            #ffd700, #00ffb3, #06b6d4,
            #4361ee, #a78bfa, #ff2d6b);
        background-size: 300% 300%;
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        animation: rainbowNeonMove 6s ease infinite;
        filter: drop-shadow(0 0 8px rgba(167,139,250,0.5));
    }
    @keyframes rainbowNeonMove {
        0%   { background-position: 0%   50%; }
        50%  { background-position: 100% 50%; }
        100% { background-position: 0%   50%; }
    }

    /* Multi-colour glow divider */
    .multi-glow-divider {
        height: 1px;
        background: linear-gradient(90deg,
            transparent,
            #ff2d6b 10%, #f43f5e 18%,
            #ffd700 30%,
            #00ffb3 45%, #06b6d4 55%,
            #4361ee 68%, #a78bfa 80%,
            transparent);
        border: none;
        margin: 1.5rem 0;
        box-shadow:
            0 0 6px rgba(244,63,94,0.3),
            0 0 12px rgba(167,139,250,0.3),
            0 0 18px rgba(6,182,212,0.2);
    }

    /* Now-playing pulse ring enhancement */
    .live-dot {
        box-shadow: 0 0 0 0 rgba(34,197,94,0.6) !important;
        animation: livePulse 1.5s ease-out infinite, livePulseExtra 3s ease-in-out infinite alternate !important;
    }
    @keyframes livePulseExtra {
        0%  { filter: none; }
        100%{ filter: drop-shadow(0 0 4px rgba(34,197,94,0.8)); }
    }
</style>
""", unsafe_allow_html=True)

# ── EXCESSIVE NEON UI MEGA-BLOCK ─────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Orbitron:wght@400;700;900&family=Rajdhani:wght@400;600;700&family=Share+Tech+Mono&display=swap');

/* ═══════════════════════════════════════════════════════════
   LEVEL 1 — ELECTRIC NEON CARDS (12 colour variants)
═══════════════════════════════════════════════════════════ */
.neon-card-electric {
    background: rgba(4,2,14,0.85);
    border: 1px solid #00f5ff;
    border-radius: 16px; padding: 16px;
    box-shadow: 0 0 8px #00f5ff, 0 0 20px rgba(0,245,255,0.3), 0 0 40px rgba(0,245,255,0.1), inset 0 0 16px rgba(0,245,255,0.03);
    transition: box-shadow .3s ease;
}
.neon-card-electric:hover {
    box-shadow: 0 0 20px #00f5ff, 0 0 50px rgba(0,245,255,0.6), 0 0 90px rgba(0,245,255,0.25), inset 0 0 28px rgba(0,245,255,0.06);
}
.neon-card-magenta {
    background: rgba(14,2,14,0.85);
    border: 1px solid #ff00ff;
    border-radius: 16px; padding: 16px;
    box-shadow: 0 0 8px #ff00ff, 0 0 20px rgba(255,0,255,0.35), 0 0 40px rgba(255,0,255,0.12), inset 0 0 16px rgba(255,0,255,0.03);
    transition: box-shadow .3s;
}
.neon-card-magenta:hover {
    box-shadow: 0 0 22px #ff00ff, 0 0 55px rgba(255,0,255,0.6), 0 0 100px rgba(255,0,255,0.25);
}
.neon-card-lime {
    background: rgba(2,14,2,0.85);
    border: 1px solid #39ff14;
    border-radius: 16px; padding: 16px;
    box-shadow: 0 0 8px #39ff14, 0 0 20px rgba(57,255,20,0.35), 0 0 40px rgba(57,255,20,0.1);
    transition: box-shadow .3s;
}
.neon-card-lime:hover {
    box-shadow: 0 0 22px #39ff14, 0 0 55px rgba(57,255,20,0.6), 0 0 100px rgba(57,255,20,0.25);
}
.neon-card-amber {
    background: rgba(14,8,2,0.85);
    border: 1px solid #ffbf00;
    border-radius: 16px; padding: 16px;
    box-shadow: 0 0 8px #ffbf00, 0 0 20px rgba(255,191,0,0.35), 0 0 40px rgba(255,191,0,0.1);
    transition: box-shadow .3s;
}
.neon-card-amber:hover {
    box-shadow: 0 0 22px #ffbf00, 0 0 55px rgba(255,191,0,0.6), 0 0 100px rgba(255,191,0,0.25);
}
.neon-card-hot-pink {
    background: rgba(14,2,8,0.85);
    border: 1px solid #ff69b4;
    border-radius: 16px; padding: 16px;
    box-shadow: 0 0 8px #ff69b4, 0 0 20px rgba(255,105,180,0.35), 0 0 40px rgba(255,105,180,0.12);
    transition: box-shadow .3s;
}
.neon-card-hot-pink:hover {
    box-shadow: 0 0 22px #ff69b4, 0 0 55px rgba(255,105,180,0.65), 0 0 100px rgba(255,105,180,0.28);
}
.neon-card-ice {
    background: rgba(2,8,14,0.85);
    border: 1px solid #a8edea;
    border-radius: 16px; padding: 16px;
    box-shadow: 0 0 8px #a8edea, 0 0 20px rgba(168,237,234,0.3), 0 0 40px rgba(168,237,234,0.1);
    transition: box-shadow .3s;
}
.neon-card-ice:hover {
    box-shadow: 0 0 22px #a8edea, 0 0 55px rgba(168,237,234,0.6), 0 0 100px rgba(168,237,234,0.22);
}
.neon-card-blood {
    background: rgba(14,2,2,0.85);
    border: 1px solid #ff0040;
    border-radius: 16px; padding: 16px;
    box-shadow: 0 0 8px #ff0040, 0 0 20px rgba(255,0,64,0.4), 0 0 40px rgba(255,0,64,0.15);
    transition: box-shadow .3s;
}
.neon-card-blood:hover {
    box-shadow: 0 0 24px #ff0040, 0 0 60px rgba(255,0,64,0.65), 0 0 110px rgba(255,0,64,0.3);
}
.neon-card-ultraviolet {
    background: rgba(6,2,14,0.85);
    border: 1px solid #9400d3;
    border-radius: 16px; padding: 16px;
    box-shadow: 0 0 8px #9400d3, 0 0 20px rgba(148,0,211,0.4), 0 0 40px rgba(148,0,211,0.15);
    transition: box-shadow .3s;
}
.neon-card-ultraviolet:hover {
    box-shadow: 0 0 24px #9400d3, 0 0 60px rgba(148,0,211,0.65), 0 0 110px rgba(148,0,211,0.3);
}
.neon-card-plasma {
    background: rgba(6,2,12,0.85);
    border: 1px solid transparent;
    border-radius: 16px; padding: 16px;
    background-clip: padding-box;
    position: relative;
    box-shadow: 0 0 20px rgba(139,92,246,0.3), 0 0 40px rgba(244,63,94,0.2), 0 0 60px rgba(6,182,212,0.15);
    transition: box-shadow .3s;
}
.neon-card-plasma::before {
    content: '';
    position: absolute; inset: -1px; border-radius: 16px; z-index: -1;
    background: linear-gradient(135deg, #ff2d6b, #a855f7, #06b6d4, #39ff14, #ff2d6b);
    background-size: 300% 300%;
    animation: plasmaBorder 4s linear infinite;
    box-shadow: 0 0 16px rgba(168,85,247,0.5), 0 0 32px rgba(244,63,94,0.3);
}
@keyframes plasmaBorder {
    0%  { background-position: 0% 50%; }
    50% { background-position: 100% 50%; }
    100%{ background-position: 0% 50%; }
}
.neon-card-plasma:hover {
    box-shadow: 0 0 36px rgba(139,92,246,0.6), 0 0 72px rgba(244,63,94,0.4), 0 0 108px rgba(6,182,212,0.3);
}
.neon-card-void {
    background: radial-gradient(ellipse at 50% 50%, rgba(30,0,60,0.7) 0%, rgba(4,2,14,0.95) 70%);
    border: 1px solid rgba(148,0,211,0.6);
    border-radius: 16px; padding: 16px;
    box-shadow:
        0 0 0 1px rgba(148,0,211,0.2),
        0 0 15px rgba(148,0,211,0.4),
        0 0 40px rgba(148,0,211,0.2),
        inset 0 0 40px rgba(148,0,211,0.06);
    transition: all .3s;
}
.neon-card-void:hover {
    box-shadow:
        0 0 0 2px rgba(255,0,255,0.4),
        0 0 30px rgba(255,0,255,0.6),
        0 0 70px rgba(148,0,211,0.4),
        inset 0 0 50px rgba(148,0,211,0.1);
}
.neon-card-matrix {
    background: rgba(0,10,0,0.92);
    border: 1px solid #00ff41;
    border-radius: 16px; padding: 16px;
    box-shadow: 0 0 8px #00ff41, 0 0 20px rgba(0,255,65,0.3), 0 0 40px rgba(0,255,65,0.1);
    position: relative; overflow: hidden;
    transition: box-shadow .3s;
}
.neon-card-matrix::after {
    content: '';
    position: absolute; inset: 0;
    background: repeating-linear-gradient(0deg, transparent, transparent 2px, rgba(0,255,65,0.025) 2px, rgba(0,255,65,0.025) 4px);
    pointer-events: none; border-radius: inherit;
}
.neon-card-matrix:hover {
    box-shadow: 0 0 22px #00ff41, 0 0 55px rgba(0,255,65,0.55), 0 0 100px rgba(0,255,65,0.22);
}

/* ═══════════════════════════════════════════════════════════
   LEVEL 2 — NEON TEXT SYSTEM (20+ variants)
═══════════════════════════════════════════════════════════ */
.nt-electric  { color:#00f5ff; text-shadow:0 0 6px #00f5ff,0 0 14px rgba(0,245,255,.8),0 0 28px rgba(0,245,255,.5); }
.nt-magenta   { color:#ff00ff; text-shadow:0 0 6px #ff00ff,0 0 14px rgba(255,0,255,.8),0 0 28px rgba(255,0,255,.5); }
.nt-lime      { color:#39ff14; text-shadow:0 0 6px #39ff14,0 0 14px rgba(57,255,20,.8),0 0 28px rgba(57,255,20,.5); }
.nt-amber     { color:#ffbf00; text-shadow:0 0 6px #ffbf00,0 0 14px rgba(255,191,0,.8),0 0 28px rgba(255,191,0,.5); }
.nt-hot-pink  { color:#ff69b4; text-shadow:0 0 6px #ff69b4,0 0 14px rgba(255,105,180,.8),0 0 28px rgba(255,105,180,.5); }
.nt-ice       { color:#a8edea; text-shadow:0 0 6px #a8edea,0 0 14px rgba(168,237,234,.8),0 0 28px rgba(168,237,234,.5); }
.nt-blood     { color:#ff0040; text-shadow:0 0 6px #ff0040,0 0 14px rgba(255,0,64,.9),0 0 28px rgba(255,0,64,.6); }
.nt-uv        { color:#df80ff; text-shadow:0 0 6px #df80ff,0 0 14px rgba(223,128,255,.8),0 0 28px rgba(223,128,255,.5); }
.nt-matrix    { color:#00ff41; text-shadow:0 0 6px #00ff41,0 0 14px rgba(0,255,65,.8),0 0 28px rgba(0,255,65,.5); }
.nt-solar     { color:#ffdd00; text-shadow:0 0 6px #ffdd00,0 0 14px rgba(255,221,0,.8),0 0 28px rgba(255,221,0,.4); }
.nt-arctic    { color:#bfefff; text-shadow:0 0 6px #bfefff,0 0 14px rgba(191,239,255,.8),0 0 30px rgba(191,239,255,.5),0 0 50px rgba(191,239,255,.2); }
.nt-volcano   { color:#ff4500; text-shadow:0 0 6px #ff4500,0 0 14px rgba(255,69,0,.9),0 0 28px rgba(255,69,0,.5); }
.nt-radioactive{ color:#ccff00; text-shadow:0 0 6px #ccff00,0 0 14px rgba(204,255,0,.9),0 0 28px rgba(204,255,0,.5),0 0 50px rgba(204,255,0,.2); }
.nt-ghost     { color:rgba(255,255,255,0.92); text-shadow:0 0 8px rgba(255,255,255,.7),0 0 16px rgba(255,255,255,.4),0 0 32px rgba(255,255,255,.2); }
.nt-plasma    {
    background: linear-gradient(135deg, #ff2d6b, #ff00ff, #00f5ff, #39ff14, #ffbf00, #ff2d6b);
    background-size: 400% 400%;
    -webkit-background-clip: text; -webkit-text-fill-color: transparent;
    animation: ntPlasmaFlow 3s linear infinite;
    filter: drop-shadow(0 0 8px rgba(255,0,255,0.6));
}
@keyframes ntPlasmaFlow {
    0%  { background-position: 0% 50%; }
    50% { background-position: 100% 50%; }
    100%{ background-position: 0% 50%; }
}
.nt-hologram {
    background: linear-gradient(90deg, #00f5ff, #ff00ff, #00f5ff);
    background-size: 200% 100%;
    -webkit-background-clip: text; -webkit-text-fill-color: transparent;
    animation: ntHologram 2s linear infinite;
    filter: drop-shadow(0 0 6px rgba(0,245,255,0.7));
}
@keyframes ntHologram {
    0%  { background-position: 0% 0; }
    100%{ background-position: 200% 0; }
}
.nt-flicker {
    color: #ff2d6b;
    text-shadow: 0 0 8px rgba(255,45,107,.8), 0 0 20px rgba(255,45,107,.5);
    animation: ntFlicker 2.5s ease-in-out infinite;
}
@keyframes ntFlicker {
    0%,92%,100%{ opacity:1; text-shadow:0 0 8px rgba(255,45,107,.8),0 0 20px rgba(255,45,107,.5); }
    93%{ opacity:.3; text-shadow:none; }
    94%{ opacity:1; text-shadow:0 0 12px rgba(255,45,107,1),0 0 28px rgba(255,45,107,.7); }
    96%{ opacity:.5; text-shadow:none; }
    97%{ opacity:1; text-shadow:0 0 8px rgba(255,45,107,.8); }
}
.nt-glitch {
    color:#a855f7;
    text-shadow: 0 0 8px rgba(168,85,247,.8);
    animation: ntGlitch 4s ease-in-out infinite;
    position: relative;
}
@keyframes ntGlitch {
    0%,88%,100%{ transform:none; text-shadow:0 0 8px rgba(168,85,247,.8); }
    89%{ transform:translate(-2px,0); text-shadow:-2px 0 #00f5ff,2px 0 #ff2d6b; }
    90%{ transform:translate(2px,0); text-shadow:2px 0 #00f5ff,-2px 0 #ff2d6b; }
    91%{ transform:none; text-shadow:0 0 8px rgba(168,85,247,.8); }
    92%{ transform:translate(0,-2px); text-shadow:0 -2px #ff00ff,0 2px #39ff14; }
    93%{ transform:none; text-shadow:0 0 8px rgba(168,85,247,.8); }
}
.nt-orbitron { font-family:'Orbitron',monospace; letter-spacing:.08em; }
.nt-rajdhani { font-family:'Rajdhani',sans-serif; font-weight:700; }
.nt-mono     { font-family:'Share Tech Mono',monospace; }

/* ═══════════════════════════════════════════════════════════
   LEVEL 3 — NEON BADGES (30 variants)
═══════════════════════════════════════════════════════════ */
.nb { display:inline-flex;align-items:center;gap:5px;border-radius:20px;padding:4px 13px;font-size:.7rem;font-weight:700;letter-spacing:.05em;text-transform:uppercase; }
.nb-electric  { background:rgba(0,245,255,.08); border:1px solid #00f5ff; color:#00f5ff; box-shadow:0 0 8px rgba(0,245,255,.4); }
.nb-magenta   { background:rgba(255,0,255,.08); border:1px solid #ff00ff; color:#ff00ff; box-shadow:0 0 8px rgba(255,0,255,.4); }
.nb-lime      { background:rgba(57,255,20,.07); border:1px solid #39ff14; color:#39ff14; box-shadow:0 0 8px rgba(57,255,20,.4); }
.nb-amber     { background:rgba(255,191,0,.08); border:1px solid #ffbf00; color:#ffbf00; box-shadow:0 0 8px rgba(255,191,0,.4); }
.nb-hot-pink  { background:rgba(255,105,180,.08); border:1px solid #ff69b4; color:#ff69b4; box-shadow:0 0 8px rgba(255,105,180,.4); }
.nb-ice       { background:rgba(168,237,234,.07); border:1px solid #a8edea; color:#a8edea; box-shadow:0 0 8px rgba(168,237,234,.4); }
.nb-blood     { background:rgba(255,0,64,.08); border:1px solid #ff0040; color:#ff0040; box-shadow:0 0 8px rgba(255,0,64,.45); }
.nb-uv        { background:rgba(148,0,211,.1); border:1px solid #9400d3; color:#df80ff; box-shadow:0 0 8px rgba(148,0,211,.45); }
.nb-matrix    { background:rgba(0,255,65,.06); border:1px solid #00ff41; color:#00ff41; box-shadow:0 0 8px rgba(0,255,65,.4); }
.nb-solar     { background:rgba(255,221,0,.08); border:1px solid #ffdd00; color:#ffdd00; box-shadow:0 0 8px rgba(255,221,0,.4); }
.nb-radioactive{ background:rgba(204,255,0,.07); border:1px solid #ccff00; color:#ccff00; box-shadow:0 0 8px rgba(204,255,0,.4); }
.nb-volcano   { background:rgba(255,69,0,.08); border:1px solid #ff4500; color:#ff6030; box-shadow:0 0 8px rgba(255,69,0,.4); }
.nb-ghost     { background:rgba(255,255,255,.04); border:1px solid rgba(255,255,255,.4); color:rgba(255,255,255,.85); box-shadow:0 0 8px rgba(255,255,255,.2); }
.nb-plasma    { background:rgba(168,85,247,.1); border:1px solid transparent; color:#fff; position:relative; overflow:hidden; z-index:0; }
.nb-plasma::before { content:''; position:absolute; inset:-1px; background:linear-gradient(135deg,#ff2d6b,#a855f7,#06b6d4,#ff2d6b); background-size:300% 300%; animation:plasmaBorder 3s linear infinite; border-radius:inherit; z-index:-1; }
.nb-hologram  { background:rgba(0,245,255,.06); border:1px solid rgba(0,245,255,.4); color:#00f5ff; box-shadow:0 0 8px rgba(0,245,255,.3),0 0 20px rgba(255,0,255,.2); animation:nbHoloPulse 2s ease-in-out infinite; }
@keyframes nbHoloPulse { 0%,100%{box-shadow:0 0 8px rgba(0,245,255,.3),0 0 20px rgba(255,0,255,.2);} 50%{box-shadow:0 0 16px rgba(0,245,255,.7),0 0 36px rgba(255,0,255,.5);} }
.nb-fire      { background:rgba(255,69,0,.1); border:1px solid #ff4500; color:#ff8c00; box-shadow:0 0 8px rgba(255,69,0,.4),0 0 16px rgba(255,140,0,.2); animation:nbFireGlow 1.5s ease-in-out infinite alternate; }
@keyframes nbFireGlow { 0%{box-shadow:0 0 8px rgba(255,69,0,.4),0 0 16px rgba(255,140,0,.2);} 100%{box-shadow:0 0 16px rgba(255,140,0,.7),0 0 32px rgba(255,69,0,.4);} }
.nb-ice-cold  { background:rgba(191,239,255,.06); border:1px solid #bfefff; color:#bfefff; box-shadow:0 0 8px rgba(191,239,255,.35),0 0 20px rgba(0,245,255,.2); }
.nb-toxic     { background:rgba(57,255,20,.07); border:1px solid #39ff14; color:#39ff14; box-shadow:0 0 8px rgba(57,255,20,.4),0 0 20px rgba(0,255,65,.2); animation:nbToxicPulse 2s ease-in-out infinite; }
@keyframes nbToxicPulse { 0%,100%{box-shadow:0 0 8px rgba(57,255,20,.4);} 50%{box-shadow:0 0 18px rgba(57,255,20,.8),0 0 36px rgba(57,255,20,.3);} }

/* ═══════════════════════════════════════════════════════════
   LEVEL 4 — NEON DIVIDERS (10 types)
═══════════════════════════════════════════════════════════ */
.nd-electric  { height:1px; background:linear-gradient(90deg,transparent,#00f5ff,transparent); box-shadow:0 0 8px rgba(0,245,255,.6); border:none; margin:1.2rem 0; }
.nd-magenta   { height:1px; background:linear-gradient(90deg,transparent,#ff00ff,transparent); box-shadow:0 0 8px rgba(255,0,255,.6); border:none; margin:1.2rem 0; }
.nd-tricolor  { height:2px; background:linear-gradient(90deg,transparent,#ff2d6b 20%,#a855f7 50%,#00f5ff 80%,transparent); box-shadow:0 0 10px rgba(168,85,247,.5); border:none; margin:1.2rem 0; }
.nd-rainbow   { height:2px; background:linear-gradient(90deg,#ff0040,#ff4500,#ffdd00,#39ff14,#00f5ff,#4361ee,#9400d3,#ff0040); background-size:200% 100%; animation:neonSweep 3s linear infinite; border:none; margin:1.2rem 0; box-shadow:0 0 10px rgba(168,85,247,.4); }
.nd-double    { height:3px; background:linear-gradient(90deg,transparent,#ff2d6b,transparent); border:none; margin:1.5rem 0; position:relative; box-shadow:0 0 8px rgba(244,63,94,.5); }
.nd-double::after { content:''; position:absolute; top:5px; left:10%; right:10%; height:1px; background:linear-gradient(90deg,transparent,rgba(168,85,247,.6),transparent); box-shadow:0 0 6px rgba(168,85,247,.4); }
.nd-dotted    { height:0; border:none; border-top:2px dotted rgba(167,139,250,.5); margin:1.2rem 0; box-shadow:none; filter:drop-shadow(0 0 3px rgba(167,139,250,.6)); }
.nd-dashed    { height:0; border:none; border-top:2px dashed rgba(0,245,255,.4); margin:1.2rem 0; filter:drop-shadow(0 0 3px rgba(0,245,255,.5)); }
.nd-zigzag    { height:8px; border:none; margin:1.2rem 0;
    background: linear-gradient(135deg, rgba(168,85,247,.6) 25%, transparent 25%) -10px 0,
                linear-gradient(225deg, rgba(168,85,247,.6) 25%, transparent 25%) -10px 0,
                linear-gradient(315deg, rgba(168,85,247,.6) 25%, transparent 25%),
                linear-gradient(45deg,  rgba(168,85,247,.6) 25%, transparent 25%);
    background-size:20px 8px; background-color:transparent;
    filter: drop-shadow(0 0 4px rgba(168,85,247,.7));
}
.nd-glow-pulse { height:2px; background:linear-gradient(90deg,transparent,#a855f7,transparent); border:none; margin:1.5rem 0; animation:ndGlowPulse 2s ease-in-out infinite; }
@keyframes ndGlowPulse { 0%,100%{box-shadow:0 0 6px rgba(168,85,247,.4);} 50%{box-shadow:0 0 18px rgba(168,85,247,.9),0 0 36px rgba(168,85,247,.4);} }
.nd-fire      { height:2px; background:linear-gradient(90deg,transparent,#ff4500,#ffdd00,#ff4500,transparent); border:none; margin:1.2rem 0; box-shadow:0 0 8px rgba(255,69,0,.5),0 0 16px rgba(255,221,0,.3); animation:ndFireShift 2s ease-in-out infinite alternate; }
@keyframes ndFireShift { 0%{box-shadow:0 0 8px rgba(255,69,0,.5);} 100%{box-shadow:0 0 18px rgba(255,140,0,.8),0 0 36px rgba(255,221,0,.3);} }

/* ═══════════════════════════════════════════════════════════
   LEVEL 5 — NEON PROGRESS BARS (8 types)
═══════════════════════════════════════════════════════════ */
.np-track { background:rgba(255,255,255,.04); border-radius:100px; height:8px; overflow:visible; position:relative; margin:6px 0; }
.np-fill-electric { height:100%; border-radius:100px; background:linear-gradient(90deg,#0040ff,#00f5ff); box-shadow:0 0 10px #00f5ff,0 0 20px rgba(0,245,255,.4); position:relative; }
.np-fill-fire     { height:100%; border-radius:100px; background:linear-gradient(90deg,#ff0040,#ff4500,#ffbf00); box-shadow:0 0 10px rgba(255,69,0,.7),0 0 20px rgba(255,191,0,.3); }
.np-fill-matrix   { height:100%; border-radius:100px; background:linear-gradient(90deg,#004d00,#00ff41); box-shadow:0 0 10px #00ff41,0 0 20px rgba(0,255,65,.4); }
.np-fill-plasma   { height:100%; border-radius:100px; background:linear-gradient(90deg,#7c3aed,#ff2d6b,#00f5ff); background-size:200% 100%; animation:npPlasmaSlide 2s linear infinite; box-shadow:0 0 10px rgba(168,85,247,.6); }
@keyframes npPlasmaSlide { 0%{background-position:0% 0;} 100%{background-position:200% 0;} }
.np-fill-magenta  { height:100%; border-radius:100px; background:linear-gradient(90deg,#440044,#ff00ff); box-shadow:0 0 10px #ff00ff,0 0 22px rgba(255,0,255,.4); }
.np-fill-uv       { height:100%; border-radius:100px; background:linear-gradient(90deg,#2d0055,#9400d3,#df80ff); box-shadow:0 0 10px rgba(148,0,211,.7),0 0 22px rgba(223,128,255,.3); }
.np-fill-ice      { height:100%; border-radius:100px; background:linear-gradient(90deg,#004466,#a8edea); box-shadow:0 0 10px #a8edea,0 0 20px rgba(168,237,234,.4); }
.np-fill-rainbow  { height:100%; border-radius:100px; background:linear-gradient(90deg,#ff0040,#ff4500,#ffdd00,#39ff14,#00f5ff,#9400d3); background-size:200% 100%; animation:npRainbowSlide 3s linear infinite; box-shadow:0 0 12px rgba(168,85,247,.5); }
@keyframes npRainbowSlide { 0%{background-position:0% 0;} 100%{background-position:200% 0;} }
/* Glow dot cursor for progress */
.np-fill-electric::after,.np-fill-fire::after,.np-fill-matrix::after,.np-fill-plasma::after,.np-fill-magenta::after,.np-fill-uv::after,.np-fill-ice::after,.np-fill-rainbow::after {
    content:''; position:absolute; right:-2px; top:50%; transform:translateY(-50%);
    width:12px; height:12px; border-radius:50%; background:#fff;
}
.np-fill-electric::after { box-shadow:0 0 8px #00f5ff,0 0 16px #00f5ff; }
.np-fill-fire::after     { box-shadow:0 0 8px #ffbf00,0 0 16px #ff4500; }
.np-fill-matrix::after   { box-shadow:0 0 8px #00ff41,0 0 16px #39ff14; }
.np-fill-plasma::after   { box-shadow:0 0 8px #a855f7,0 0 16px #ff2d6b; }
.np-fill-magenta::after  { box-shadow:0 0 8px #ff00ff,0 0 16px #ff00ff; }
.np-fill-uv::after       { box-shadow:0 0 8px #9400d3,0 0 16px #df80ff; }
.np-fill-ice::after      { box-shadow:0 0 8px #a8edea,0 0 16px #a8edea; }
.np-fill-rainbow::after  { box-shadow:0 0 8px #fff,0 0 16px rgba(168,85,247,.8); }

/* ═══════════════════════════════════════════════════════════
   LEVEL 6 — NEON SECTION HEADERS (10 styles)
═══════════════════════════════════════════════════════════ */
.nsh { border-radius:18px; padding:20px 24px; margin-bottom:22px; position:relative; overflow:hidden; }
.nsh::before { content:''; position:absolute; top:-1px; left:15%; right:15%; height:1px; }
.nsh-electric  { background:linear-gradient(135deg,rgba(0,245,255,.06),rgba(0,64,255,.04)); border:1px solid rgba(0,245,255,.25); }
.nsh-electric::before { background:linear-gradient(90deg,transparent,#00f5ff,transparent); box-shadow:0 0 8px rgba(0,245,255,.7); }
.nsh-magenta   { background:linear-gradient(135deg,rgba(255,0,255,.06),rgba(148,0,211,.04)); border:1px solid rgba(255,0,255,.25); }
.nsh-magenta::before { background:linear-gradient(90deg,transparent,#ff00ff,transparent); box-shadow:0 0 8px rgba(255,0,255,.7); }
.nsh-matrix    { background:linear-gradient(135deg,rgba(0,255,65,.05),rgba(0,180,40,.03)); border:1px solid rgba(0,255,65,.2); }
.nsh-matrix::before { background:linear-gradient(90deg,transparent,#00ff41,transparent); box-shadow:0 0 8px rgba(0,255,65,.7); }
.nsh-fire      { background:linear-gradient(135deg,rgba(255,69,0,.08),rgba(255,191,0,.04)); border:1px solid rgba(255,69,0,.3); }
.nsh-fire::before { background:linear-gradient(90deg,transparent,#ff4500,#ffdd00,transparent); box-shadow:0 0 8px rgba(255,69,0,.6); }
.nsh-plasma    { background:linear-gradient(135deg,rgba(168,85,247,.07),rgba(244,63,94,.05),rgba(6,182,212,.04)); border:1px solid rgba(168,85,247,.22); }
.nsh-plasma::before { background:linear-gradient(90deg,transparent,#f43f5e,#a855f7,#06b6d4,transparent); box-shadow:0 0 10px rgba(168,85,247,.6); }
.nsh-ultraviolet { background:radial-gradient(ellipse at 50% 0%, rgba(148,0,211,.12) 0%,transparent 60%), rgba(6,2,14,.88); border:1px solid rgba(148,0,211,.3); }
.nsh-ultraviolet::before { background:linear-gradient(90deg,transparent,#9400d3,#df80ff,transparent); box-shadow:0 0 8px rgba(148,0,211,.8); }
.nsh-ice       { background:linear-gradient(135deg,rgba(168,237,234,.06),rgba(0,245,255,.03)); border:1px solid rgba(168,237,234,.22); }
.nsh-ice::before { background:linear-gradient(90deg,transparent,#a8edea,transparent); box-shadow:0 0 8px rgba(168,237,234,.7); }
.nsh-void      { background:radial-gradient(ellipse at 50% 0%, rgba(60,0,120,.2) 0%,rgba(6,2,14,.92) 60%); border:1px solid rgba(255,0,255,.2); }
.nsh-void::before { background:linear-gradient(90deg,transparent,#ff00ff,#9400d3,transparent); box-shadow:0 0 10px rgba(255,0,255,.6); }
.nsh-rainbow   { background:rgba(6,8,16,.88); border:1px solid transparent; position:relative; }
.nsh-rainbow::after { content:''; position:absolute; inset:-1px; border-radius:18px; background:linear-gradient(135deg,#ff0040,#ffbf00,#39ff14,#00f5ff,#9400d3,#ff0040); background-size:300% 300%; animation:plasmaBorder 4s linear infinite; z-index:-1; }

/* ═══════════════════════════════════════════════════════════
   LEVEL 7 — NEON ICON FRAMES / AVATARS
═══════════════════════════════════════════════════════════ */
.nif { display:inline-flex; align-items:center; justify-content:center; border-radius:14px; flex-shrink:0; transition:all .25s; }
.nif-sm { width:40px; height:40px; font-size:1.2rem; }
.nif-md { width:56px; height:56px; font-size:1.6rem; }
.nif-lg { width:72px; height:72px; font-size:2rem; }
.nif-electric { background:rgba(0,245,255,.08); border:1px solid rgba(0,245,255,.5); box-shadow:0 0 12px rgba(0,245,255,.3); }
.nif-electric:hover { box-shadow:0 0 24px rgba(0,245,255,.7),0 0 48px rgba(0,245,255,.3); transform:scale(1.1) rotate(5deg); }
.nif-magenta  { background:rgba(255,0,255,.08); border:1px solid rgba(255,0,255,.5); box-shadow:0 0 12px rgba(255,0,255,.3); }
.nif-magenta:hover { box-shadow:0 0 24px rgba(255,0,255,.7); transform:scale(1.1) rotate(-5deg); }
.nif-lime     { background:rgba(57,255,20,.07); border:1px solid rgba(57,255,20,.5); box-shadow:0 0 12px rgba(57,255,20,.3); }
.nif-fire     { background:rgba(255,69,0,.08); border:1px solid rgba(255,69,0,.5); box-shadow:0 0 12px rgba(255,69,0,.35); animation:nifFireBlink 2s ease-in-out infinite; }
@keyframes nifFireBlink { 0%,100%{box-shadow:0 0 12px rgba(255,69,0,.35);} 50%{box-shadow:0 0 22px rgba(255,140,0,.7),0 0 40px rgba(255,69,0,.3);} }
.nif-plasma   { background:rgba(8,4,18,.9); border:2px solid transparent; position:relative; overflow:hidden; }
.nif-plasma::before { content:''; position:absolute; inset:-2px; background:linear-gradient(135deg,#ff2d6b,#a855f7,#00f5ff,#ff2d6b); background-size:300% 300%; animation:plasmaBorder 3s linear infinite; border-radius:inherit; z-index:0; }
.nif-plasma > * { position:relative; z-index:1; }
.nif-circle  { border-radius:50%; }
.nif-hex     { clip-path:polygon(50% 0%,93% 25%,93% 75%,50% 100%,7% 75%,7% 25%); border-radius:0; border:none !important; }
.nif-pulse { animation:nifPulse 2s ease-in-out infinite; }
@keyframes nifPulse { 0%,100%{transform:scale(1);} 50%{transform:scale(1.06);} }

/* ═══════════════════════════════════════════════════════════
   LEVEL 8 — NEON BUTTONS (12 variants)
═══════════════════════════════════════════════════════════ */
.nbtn { display:inline-flex; align-items:center; justify-content:center; gap:7px; border-radius:12px; padding:10px 22px; font-weight:700; font-size:.85rem; cursor:pointer; font-family:'Outfit',sans-serif; letter-spacing:.02em; transition:all .22s ease; border:none; text-decoration:none; }
.nbtn-electric { background:rgba(0,245,255,.1); border:1px solid #00f5ff; color:#00f5ff; box-shadow:0 0 10px rgba(0,245,255,.25); }
.nbtn-electric:hover { background:rgba(0,245,255,.2); box-shadow:0 0 22px rgba(0,245,255,.6),0 0 44px rgba(0,245,255,.25); transform:translateY(-2px); }
.nbtn-magenta { background:rgba(255,0,255,.08); border:1px solid #ff00ff; color:#ff00ff; box-shadow:0 0 10px rgba(255,0,255,.25); }
.nbtn-magenta:hover { background:rgba(255,0,255,.2); box-shadow:0 0 22px rgba(255,0,255,.65),0 0 44px rgba(255,0,255,.28); transform:translateY(-2px); }
.nbtn-lime    { background:rgba(57,255,20,.07); border:1px solid #39ff14; color:#39ff14; box-shadow:0 0 10px rgba(57,255,20,.25); }
.nbtn-lime:hover { background:rgba(57,255,20,.18); box-shadow:0 0 22px rgba(57,255,20,.65); transform:translateY(-2px); }
.nbtn-fire    { background:rgba(255,69,0,.1); border:1px solid #ff4500; color:#ff8c00; box-shadow:0 0 10px rgba(255,69,0,.3); }
.nbtn-fire:hover { background:rgba(255,140,0,.2); box-shadow:0 0 22px rgba(255,140,0,.65),0 0 44px rgba(255,69,0,.28); transform:translateY(-2px); }
.nbtn-plasma  { background:linear-gradient(135deg,rgba(124,58,237,.2),rgba(244,63,94,.15),rgba(6,182,212,.12)); border:1px solid rgba(168,85,247,.5); color:#fff; box-shadow:0 0 12px rgba(168,85,247,.3); }
.nbtn-plasma:hover { box-shadow:0 0 24px rgba(168,85,247,.6),0 0 48px rgba(244,63,94,.3); transform:translateY(-3px) scale(1.02); }
.nbtn-ghost   { background:rgba(255,255,255,.03); border:1px solid rgba(255,255,255,.2); color:rgba(255,255,255,.8); }
.nbtn-ghost:hover { background:rgba(255,255,255,.08); border-color:rgba(255,255,255,.4); box-shadow:0 0 16px rgba(255,255,255,.15); transform:translateY(-2px); }
.nbtn-matrix  { background:rgba(0,255,65,.06); border:1px solid #00ff41; color:#00ff41; font-family:'Share Tech Mono',monospace; box-shadow:0 0 10px rgba(0,255,65,.25); }
.nbtn-matrix:hover { background:rgba(0,255,65,.16); box-shadow:0 0 22px rgba(0,255,65,.6); transform:translateY(-2px); }
.nbtn-morph   { border:none; color:#fff; background:linear-gradient(135deg,#ff2d6b,#a855f7,#06b6d4,#39ff14,#ffbf00,#ff2d6b); background-size:400% 400%; animation:morphBtnGrad 5s ease infinite; box-shadow:0 0 20px rgba(168,85,247,.4); }
.nbtn-morph:hover { box-shadow:0 0 36px rgba(244,63,94,.65),0 0 72px rgba(168,85,247,.35); transform:translateY(-3px) scale(1.03); }
.nbtn-outline-glow { background:transparent; border:2px solid #a855f7; color:#c4b5fd; box-shadow:0 0 0 0 rgba(168,85,247,.4),inset 0 0 0 0 rgba(168,85,247,.1); transition:all .3s; }
.nbtn-outline-glow:hover { box-shadow:0 0 16px rgba(168,85,247,.7),inset 0 0 20px rgba(168,85,247,.1); border-color:#c4b5fd; color:#e9d5ff; transform:translateY(-2px); }
.nbtn-pill    { border-radius:50px; }
.nbtn-square  { border-radius:6px; }
.nbtn-icon    { padding:10px; width:44px; height:44px; border-radius:12px; }

/* ═══════════════════════════════════════════════════════════
   LEVEL 9 — NEON STAT COUNTERS / DISPLAY NUMBERS
═══════════════════════════════════════════════════════════ */
.neon-stat-card { border-radius:18px; padding:22px; text-align:center; position:relative; overflow:hidden; }
.neon-stat-card::before { content:''; position:absolute; inset:0; opacity:.06; pointer-events:none;
    background: radial-gradient(ellipse 80% 60% at 50% -10%, white 0%, transparent 70%);
}
.nsc-electric  { background:rgba(0,10,20,.88); border:1px solid rgba(0,245,255,.3); box-shadow:0 0 20px rgba(0,245,255,.12),inset 0 0 30px rgba(0,245,255,.04); }
.nsc-magenta   { background:rgba(14,0,14,.88); border:1px solid rgba(255,0,255,.3); box-shadow:0 0 20px rgba(255,0,255,.12),inset 0 0 30px rgba(255,0,255,.04); }
.nsc-fire      { background:rgba(14,4,0,.88); border:1px solid rgba(255,69,0,.3); box-shadow:0 0 20px rgba(255,69,0,.12),inset 0 0 30px rgba(255,69,0,.04); }
.nsc-matrix    { background:rgba(0,8,0,.92); border:1px solid rgba(0,255,65,.25); box-shadow:0 0 20px rgba(0,255,65,.10),inset 0 0 30px rgba(0,255,65,.03); }
.nsc-plasma    { background:rgba(8,4,18,.88); border:1px solid rgba(168,85,247,.3); box-shadow:0 0 20px rgba(168,85,247,.12),inset 0 0 30px rgba(168,85,247,.04); }
.neon-stat-num-xl { font-family:'Orbitron',monospace; font-size:3.6rem; font-weight:900; line-height:1; letter-spacing:.02em; }
.neon-stat-label { font-size:.65rem; text-transform:uppercase; letter-spacing:.15em; color:rgba(255,255,255,.35); margin-top:8px; font-weight:700; }
.neon-stat-sub   { font-size:.78rem; color:rgba(255,255,255,.5); margin-top:4px; }

/* ═══════════════════════════════════════════════════════════
   LEVEL 10 — ANIMATED BACKGROUND EFFECTS
═══════════════════════════════════════════════════════════ */
/* Cyberpunk grid floor */
.cyber-grid-bg {
    position: relative; overflow: hidden;
}
.cyber-grid-bg::before {
    content: '';
    position: absolute; inset: 0; z-index: 0; pointer-events: none;
    background:
        linear-gradient(rgba(0,245,255,.04) 1px, transparent 1px),
        linear-gradient(90deg, rgba(0,245,255,.04) 1px, transparent 1px),
        linear-gradient(rgba(168,85,247,.02) 1px, transparent 1px),
        linear-gradient(90deg, rgba(168,85,247,.02) 1px, transparent 1px);
    background-size: 60px 60px, 60px 60px, 20px 20px, 20px 20px;
    animation: cyberGridScroll 10s linear infinite;
}
@keyframes cyberGridScroll {
    0%   { background-position: 0 0, 0 0, 0 0, 0 0; }
    100% { background-position: 0 60px, 60px 0, 0 20px, 20px 0; }
}
.cyber-grid-bg > * { position: relative; z-index: 1; }

/* Neon hexagon tiling */
.hex-bg {
    position: relative; overflow: hidden;
}
.hex-bg::before {
    content: '';
    position: absolute; inset: 0; z-index: 0; pointer-events: none;
    background-image: url("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' width='56' height='100'%3E%3Cpath d='M28 66L0 50V16L28 0l28 16v34z' fill='none' stroke='rgba(168,85,247,0.07)' stroke-width='1'/%3E%3C/svg%3E");
    background-size: 56px 100px;
    animation: hexDrift 12s linear infinite;
}
@keyframes hexDrift {
    0%   { background-position: 0 0; }
    100% { background-position: 56px 100px; }
}
.hex-bg > * { position: relative; z-index: 1; }

/* Neon spotlight overlay */
.spotlight-card {
    position: relative; overflow: hidden;
    background: rgba(6,4,18,.9); border-radius: 18px; padding: 20px;
    border: 1px solid rgba(168,85,247,.2);
}
.spotlight-card::after {
    content: '';
    position: absolute;
    width: 200px; height: 200px;
    border-radius: 50%;
    background: radial-gradient(circle, rgba(168,85,247,.18) 0%, transparent 70%);
    top: -60px; right: -40px;
    animation: spotlightMove 8s ease-in-out infinite alternate;
    pointer-events: none;
}
@keyframes spotlightMove {
    0%   { transform: translate(0,0); }
    33%  { transform: translate(-80px,60px); background:radial-gradient(circle,rgba(0,245,255,.15) 0%,transparent 70%); }
    66%  { transform: translate(-120px,-20px); background:radial-gradient(circle,rgba(244,63,94,.15) 0%,transparent 70%); }
    100% { transform: translate(-40px,80px); background:radial-gradient(circle,rgba(168,85,247,.18) 0%,transparent 70%); }
}

/* Neon lightning flashes on cards */
.lightning-card {
    position: relative; overflow: hidden;
    background: rgba(4,2,14,.88); border-radius: 16px; padding: 18px;
    border: 1px solid rgba(0,245,255,.2);
}
.lightning-card::before {
    content: '';
    position: absolute; top: 0; left: -100%; width: 3px; height: 100%;
    background: linear-gradient(180deg, transparent, #00f5ff, rgba(0,245,255,.3), transparent);
    animation: lightningSlide 5s ease-in-out infinite;
    filter: blur(1px);
}
@keyframes lightningSlide {
    0%  { left: -5%; opacity: 0; }
    5%  { opacity: 1; }
    25% { left: 105%; opacity: 0; }
    100%{ left: 105%; opacity: 0; }
}

/* Neon rain / matrix rain effect */
.matrix-rain-card {
    position: relative; overflow: hidden;
    background: rgba(0,8,0,.92); border-radius: 16px; padding: 18px;
    border: 1px solid rgba(0,255,65,.2);
}
.matrix-rain-card::before {
    content: '01 10 11 10 01 0 1 0 1 11 0';
    position: absolute; top: 0; left: 0; right: 0; bottom: 0;
    font-family: 'Share Tech Mono', monospace;
    font-size: .55rem; line-height: 1.8;
    color: rgba(0,255,65,.08);
    word-break: break-all;
    overflow: hidden;
    pointer-events: none;
    animation: matrixRainText 4s linear infinite alternate;
    letter-spacing: .2em;
    padding: 8px;
}
@keyframes matrixRainText {
    0%   { opacity: .4; letter-spacing: .2em; }
    100% { opacity: .7; letter-spacing: .3em; }
}

/* ═══════════════════════════════════════════════════════════
   LEVEL 11 — SPECIAL EFFECTS & ANIMATIONS
═══════════════════════════════════════════════════════════ */
/* Neon warp speed lines */
.warp-lines {
    position: relative; overflow: hidden;
}
.warp-lines::after {
    content: '';
    position: absolute; inset: 0; z-index: 0; pointer-events: none;
    background:
        linear-gradient(92deg, transparent 45%, rgba(0,245,255,.04) 50%, transparent 55%),
        linear-gradient(89deg, transparent 42%, rgba(168,85,247,.04) 48%, transparent 54%),
        linear-gradient(91deg, transparent 48%, rgba(244,63,94,.04) 52%, transparent 56%),
        linear-gradient(90deg, transparent 38%, rgba(57,255,20,.03) 44%, transparent 50%);
    animation: warpFlow 6s linear infinite;
}
@keyframes warpFlow {
    0%   { transform: translateX(-100%); }
    100% { transform: translateX(100%); }
}
.warp-lines > * { position: relative; z-index: 1; }

/* Neon ticker / scrolling label */
.neon-ticker-wrap { overflow: hidden; white-space: nowrap; border-radius: 8px; padding: 6px 0; background: rgba(0,245,255,.04); border: 1px solid rgba(0,245,255,.12); }
.neon-ticker { display: inline-block; animation: tickerScroll 18s linear infinite; color: #00f5ff; font-size: .72rem; font-weight: 700; text-transform: uppercase; letter-spacing: .12em; font-family: 'Orbitron', monospace; text-shadow: 0 0 6px rgba(0,245,255,.7); }
@keyframes tickerScroll { 0%{ transform:translateX(100vw); } 100%{ transform:translateX(-100%); } }

/* Neon typewriter cursor */
.typewriter-cursor::after {
    content: '|';
    color: #a855f7;
    animation: twBlink .7s ease-in-out infinite;
    text-shadow: 0 0 6px rgba(168,85,247,.8);
    margin-left: 2px;
}
@keyframes twBlink { 0%,100%{opacity:1;} 50%{opacity:0;} }

/* Neon shake on hover */
.neon-shake:hover { animation: neonShake .4s ease-in-out; }
@keyframes neonShake {
    0%  { transform:translateX(0); }
    20% { transform:translateX(-4px) rotate(-1deg); }
    40% { transform:translateX(4px)  rotate(1deg); }
    60% { transform:translateX(-3px); }
    80% { transform:translateX(3px); }
    100%{ transform:translateX(0); }
}

/* Neon bounce on hover */
.neon-bounce:hover { animation: neonBounce .5s cubic-bezier(0.36,0.07,0.19,0.97); }
@keyframes neonBounce {
    0%,100%{ transform:translateY(0); }
    30%    { transform:translateY(-8px); }
    60%    { transform:translateY(-3px); }
    80%    { transform:translateY(-6px); }
}

/* Neon spin icon */
.neon-spin { animation: neonSpin 3s linear infinite; }
.neon-spin-slow { animation: neonSpin 8s linear infinite; }
@keyframes neonSpin { 0%{transform:rotate(0deg);} 100%{transform:rotate(360deg);} }

/* Neon pulse ring (standalone element) */
.pulse-ring {
    position: relative; display: inline-flex; align-items: center; justify-content: center;
    width: 60px; height: 60px;
}
.pulse-ring::before,.pulse-ring::after {
    content: '';
    position: absolute; inset: 0; border-radius: 50%;
    border: 2px solid rgba(168,85,247,.6);
    animation: pulseRingExpand 2.4s ease-out infinite;
}
.pulse-ring::after { animation-delay: 1.2s; border-color: rgba(244,63,94,.4); }
@keyframes pulseRingExpand {
    0%  { transform:scale(1);   opacity:.8; }
    100%{ transform:scale(2.2); opacity:0; }
}
.pulse-ring-electric::before { border-color:rgba(0,245,255,.6); }
.pulse-ring-electric::after  { border-color:rgba(0,245,255,.3); }
.pulse-ring-lime::before { border-color:rgba(57,255,20,.6); }
.pulse-ring-lime::after  { border-color:rgba(57,255,20,.3); }

/* ═══════════════════════════════════════════════════════════
   LEVEL 12 — NEON TABLE / DATA GRID ROWS
═══════════════════════════════════════════════════════════ */
.neon-table { width:100%; border-collapse:separate; border-spacing:0 6px; }
.neon-table th { font-size:.62rem; text-transform:uppercase; letter-spacing:.12em; color:rgba(255,255,255,.3); padding:6px 14px; font-weight:700; }
.neon-table td { padding:10px 14px; }
.neon-table tr.ntr { background:rgba(8,6,20,.8); transition:all .2s; }
.neon-table tr.ntr td:first-child { border-radius:10px 0 0 10px; }
.neon-table tr.ntr td:last-child  { border-radius:0 10px 10px 0; }
.neon-table tr.ntr:hover { background:rgba(139,92,246,.08); box-shadow:inset 0 0 0 1px rgba(167,139,250,.2); }
.ntr-electric:hover { background:rgba(0,245,255,.06) !important; box-shadow:inset 0 0 0 1px rgba(0,245,255,.2) !important; }
.ntr-fire:hover     { background:rgba(255,69,0,.06) !important; box-shadow:inset 0 0 0 1px rgba(255,69,0,.25) !important; }
.ntr-matrix:hover   { background:rgba(0,255,65,.05) !important; box-shadow:inset 0 0 0 1px rgba(0,255,65,.2) !important; }

/* ═══════════════════════════════════════════════════════════
   LEVEL 13 — NEON TAG CLOUD
═══════════════════════════════════════════════════════════ */
.neon-tag-cloud { display:flex; flex-wrap:wrap; gap:8px; }
.ntag { display:inline-block; border-radius:20px; padding:5px 14px; font-size:.74rem; font-weight:700; letter-spacing:.03em; cursor:pointer; transition:all .2s; }
.ntag-e  { background:rgba(0,245,255,.07); border:1px solid rgba(0,245,255,.3); color:#00f5ff; }
.ntag-e:hover  { background:rgba(0,245,255,.18); box-shadow:0 0 12px rgba(0,245,255,.5); transform:scale(1.05); }
.ntag-m  { background:rgba(255,0,255,.06); border:1px solid rgba(255,0,255,.3); color:#ff00ff; }
.ntag-m:hover  { background:rgba(255,0,255,.18); box-shadow:0 0 12px rgba(255,0,255,.5); transform:scale(1.05); }
.ntag-l  { background:rgba(57,255,20,.06); border:1px solid rgba(57,255,20,.3); color:#39ff14; }
.ntag-l:hover  { background:rgba(57,255,20,.16); box-shadow:0 0 12px rgba(57,255,20,.5); transform:scale(1.05); }
.ntag-f  { background:rgba(255,69,0,.07); border:1px solid rgba(255,69,0,.3); color:#ff8c00; }
.ntag-f:hover  { background:rgba(255,140,0,.18); box-shadow:0 0 12px rgba(255,140,0,.5); transform:scale(1.05); }
.ntag-p  { background:rgba(139,92,246,.08); border:1px solid rgba(167,139,250,.3); color:#c4b5fd; }
.ntag-p:hover  { background:rgba(139,92,246,.2); box-shadow:0 0 12px rgba(167,139,250,.5); transform:scale(1.05); }
.ntag-r  { background:rgba(244,63,94,.07); border:1px solid rgba(244,63,94,.3); color:#f43f5e; }
.ntag-r:hover  { background:rgba(244,63,94,.18); box-shadow:0 0 12px rgba(244,63,94,.5); transform:scale(1.05); }
.ntag-c  { background:rgba(6,182,212,.07); border:1px solid rgba(6,182,212,.3); color:#22d3ee; }
.ntag-c:hover  { background:rgba(6,182,212,.18); box-shadow:0 0 12px rgba(6,182,212,.5); transform:scale(1.05); }

/* ═══════════════════════════════════════════════════════════
   LEVEL 14 — MEGA GLOWING HEADERS (Orbitron font)
═══════════════════════════════════════════════════════════ */
.mega-header-electric {
    font-family: 'Orbitron', monospace; font-weight: 900; letter-spacing: .08em;
    color: #00f5ff;
    text-shadow: 0 0 10px #00f5ff, 0 0 24px rgba(0,245,255,.7), 0 0 48px rgba(0,245,255,.4), 0 0 80px rgba(0,245,255,.2);
    animation: megaHeaderPulse 3s ease-in-out infinite;
}
.mega-header-magenta {
    font-family: 'Orbitron', monospace; font-weight: 900; letter-spacing: .08em;
    color: #ff00ff;
    text-shadow: 0 0 10px #ff00ff, 0 0 24px rgba(255,0,255,.7), 0 0 48px rgba(255,0,255,.4), 0 0 80px rgba(255,0,255,.2);
    animation: megaHeaderPulse 3s ease-in-out infinite;
}
.mega-header-lime {
    font-family: 'Orbitron', monospace; font-weight: 900; letter-spacing: .08em;
    color: #39ff14;
    text-shadow: 0 0 10px #39ff14, 0 0 24px rgba(57,255,20,.7), 0 0 48px rgba(57,255,20,.4), 0 0 80px rgba(57,255,20,.2);
    animation: megaHeaderPulse 3s ease-in-out infinite;
}
.mega-header-plasma {
    font-family: 'Orbitron', monospace; font-weight: 900; letter-spacing: .08em;
    background: linear-gradient(135deg, #ff2d6b, #ff00ff, #00f5ff, #39ff14, #ffbf00, #ff2d6b);
    background-size: 400% 400%;
    -webkit-background-clip: text; -webkit-text-fill-color: transparent;
    animation: ntPlasmaFlow 3s linear infinite;
    filter: drop-shadow(0 0 12px rgba(168,85,247,.8)) drop-shadow(0 0 24px rgba(244,63,94,.5));
}
@keyframes megaHeaderPulse {
    0%,100%{ filter:brightness(1); }
    50%    { filter:brightness(1.3); }
}

/* ═══════════════════════════════════════════════════════════
   LEVEL 15 — NEON TOOLTIP SYSTEM
═══════════════════════════════════════════════════════════ */
.ntt { position:relative; cursor:help; }
.ntt::after {
    content: attr(data-ntt);
    position: absolute; bottom: calc(100% + 8px); left: 50%; transform: translateX(-50%);
    background: rgba(8,4,22,.96); border-radius: 8px; padding: 6px 12px;
    font-size: .68rem; font-weight: 600; white-space: nowrap;
    opacity: 0; pointer-events: none; transition: opacity .2s;
    z-index: 9999;
}
.ntt::before {
    content: '';
    position: absolute; bottom: calc(100% + 3px); left: 50%; transform: translateX(-50%);
    border: 5px solid transparent;
    opacity: 0; pointer-events: none; transition: opacity .2s;
    z-index: 9999;
}
.ntt:hover::after,.ntt:hover::before { opacity: 1; }
.ntt-electric::after { border:1px solid rgba(0,245,255,.4); color:#00f5ff; box-shadow:0 0 10px rgba(0,245,255,.3); }
.ntt-electric::before { border-top-color:rgba(0,245,255,.4); }
.ntt-magenta::after { border:1px solid rgba(255,0,255,.4); color:#ff00ff; box-shadow:0 0 10px rgba(255,0,255,.3); }
.ntt-magenta::before { border-top-color:rgba(255,0,255,.4); }
.ntt-purple::after { border:1px solid rgba(167,139,250,.4); color:#c4b5fd; box-shadow:0 0 10px rgba(139,92,246,.3); }
.ntt-purple::before { border-top-color:rgba(167,139,250,.4); }
.ntt-fire::after { border:1px solid rgba(255,69,0,.4); color:#ff8c00; box-shadow:0 0 10px rgba(255,69,0,.3); }
.ntt-fire::before { border-top-color:rgba(255,69,0,.4); }

/* ═══════════════════════════════════════════════════════════
   LEVEL 16 — NEON LOADING INDICATORS
═══════════════════════════════════════════════════════════ */
.neon-spinner { width:40px; height:40px; border-radius:50%; border:3px solid rgba(255,255,255,.06); border-top:3px solid #a855f7; animation:neonSpin .8s linear infinite; box-shadow:0 0 12px rgba(168,85,247,.5); }
.neon-spinner-electric { border-top-color:#00f5ff; box-shadow:0 0 12px rgba(0,245,255,.5); }
.neon-spinner-magenta  { border-top-color:#ff00ff; box-shadow:0 0 12px rgba(255,0,255,.5); }
.neon-spinner-fire     { border-top-color:#ff4500; box-shadow:0 0 12px rgba(255,69,0,.5); }
.neon-spinner-matrix   { border-top-color:#00ff41; box-shadow:0 0 12px rgba(0,255,65,.5); }
.neon-spinner-dual {
    width:40px; height:40px; border-radius:50%;
    border:3px solid transparent;
    border-top:3px solid #a855f7;
    border-bottom:3px solid #00f5ff;
    animation:neonSpin .8s linear infinite;
    box-shadow:0 0 12px rgba(168,85,247,.4),0 0 20px rgba(0,245,255,.2);
}
.neon-dots { display:flex; gap:6px; align-items:center; }
.neon-dot  { width:8px; height:8px; border-radius:50%; animation:neonDotBounce 1.2s ease-in-out infinite; }
.neon-dot:nth-child(1){ background:#f43f5e; box-shadow:0 0 6px rgba(244,63,94,.7); animation-delay:0s; }
.neon-dot:nth-child(2){ background:#a855f7; box-shadow:0 0 6px rgba(168,85,247,.7); animation-delay:.15s; }
.neon-dot:nth-child(3){ background:#06b6d4; box-shadow:0 0 6px rgba(6,182,212,.7); animation-delay:.3s; }
.neon-dot:nth-child(4){ background:#00ff41; box-shadow:0 0 6px rgba(0,255,65,.7); animation-delay:.45s; }
.neon-dot:nth-child(5){ background:#ff00ff; box-shadow:0 0 6px rgba(255,0,255,.7); animation-delay:.6s; }
@keyframes neonDotBounce {
    0%,100%{ transform:translateY(0); opacity:.5; }
    50%    { transform:translateY(-10px); opacity:1; }
}
/* Neon bar loading */
.neon-bar-loader { height:4px; border-radius:2px; background:rgba(255,255,255,.04); overflow:hidden; }
.neon-bar-loader::after {
    content:''; display:block; height:100%;
    background:linear-gradient(90deg,transparent,#a855f7,#f43f5e,#00f5ff,transparent);
    background-size:60% 100%;
    animation:neonBarSlide 1.6s ease-in-out infinite;
}
@keyframes neonBarSlide { 0%{background-position:-60% 0;} 100%{background-position:160% 0;} }

/* ═══════════════════════════════════════════════════════════
   LEVEL 17 — NEON TOOLTIP LABELS (floating)
═══════════════════════════════════════════════════════════ */
.neon-label {
    display:inline-block; font-size:.58rem; font-weight:800; text-transform:uppercase;
    letter-spacing:.12em; padding:2px 8px; border-radius:4px;
    font-family:'Orbitron',monospace;
}
.nl-new     { background:rgba(57,255,20,.12); border:1px solid #39ff14; color:#39ff14; box-shadow:0 0 6px rgba(57,255,20,.4); }
.nl-hot     { background:rgba(255,69,0,.12); border:1px solid #ff4500; color:#ff8c00; box-shadow:0 0 6px rgba(255,69,0,.45); animation:nbFireGlow 1.5s ease-in-out infinite alternate; }
.nl-live    { background:rgba(244,63,94,.12); border:1px solid #f43f5e; color:#f43f5e; box-shadow:0 0 6px rgba(244,63,94,.45); animation:nbFireGlow 1.5s ease-in-out infinite alternate; }
.nl-top     { background:rgba(255,191,0,.1); border:1px solid #ffbf00; color:#ffbf00; box-shadow:0 0 6px rgba(255,191,0,.4); }
.nl-beta    { background:rgba(0,245,255,.08); border:1px solid #00f5ff; color:#00f5ff; box-shadow:0 0 6px rgba(0,245,255,.35); }
.nl-ai      { background:rgba(168,85,247,.12); border:1px solid #a855f7; color:#c4b5fd; box-shadow:0 0 6px rgba(168,85,247,.45); }
.nl-excl    { background:rgba(255,0,64,.12); border:1px solid #ff0040; color:#ff0040; box-shadow:0 0 6px rgba(255,0,64,.5); animation:ntFlicker 2s infinite; }

/* ═══════════════════════════════════════════════════════════
   LEVEL 18 — GLOBAL STREAMLIT ELEMENT GLOW POLISH
═══════════════════════════════════════════════════════════ */
/* Sidebar nav link neon selected */
[data-testid="stSidebar"] .nav-link-selected {
    background: linear-gradient(90deg, rgba(139,92,246,.18), rgba(244,63,94,.08)) !important;
    border-left: 3px solid #a855f7 !important;
    box-shadow: inset 0 0 16px rgba(139,92,246,.12), 0 0 10px rgba(139,92,246,.2) !important;
}

/* Selectbox neon glow */
.stSelectbox > div > div:focus-within {
    border-color: rgba(167,139,250,.6) !important;
    box-shadow: 0 0 0 2px rgba(139,92,246,.15), 0 0 12px rgba(167,139,250,.25) !important;
}

/* Slider track glow */
.stSlider [data-baseweb="slider"] [data-testid="stThumbValue"] {
    color: #c4b5fd !important;
}
.stSlider [role="slider"] {
    box-shadow: 0 0 8px rgba(139,92,246,.6) !important;
}

/* Toast / success / warning glow polish */
.stToast { box-shadow: 0 0 20px rgba(139,92,246,.2), 0 4px 16px rgba(0,0,0,.4) !important; }
.stSuccess { border-color: rgba(57,255,20,.3) !important; box-shadow: 0 0 12px rgba(57,255,20,.1) !important; }
.stWarning { border-color: rgba(255,191,0,.3) !important; box-shadow: 0 0 12px rgba(255,191,0,.1) !important; }
.stInfo    { border-color: rgba(0,245,255,.25) !important; box-shadow: 0 0 12px rgba(0,245,255,.08) !important; }

/* Checkbox neon glow */
.stCheckbox [data-testid="stCheckbox"] > label > div[data-testid="stMarkdownContainer"] {
    color: rgba(255,255,255,.75) !important;
}

/* Radio selection glow */
.stRadio [role="radio"][aria-checked="true"] + div {
    color: #c4b5fd !important;
    text-shadow: 0 0 6px rgba(167,139,250,.5);
}

/* Neon glow on number_input */
.stNumberInput [data-testid="stNumberInputField"]:focus {
    border-color: rgba(167,139,250,.6) !important;
    box-shadow: 0 0 0 2px rgba(139,92,246,.15), 0 0 12px rgba(167,139,250,.22) !important;
}

/* Expander header neon hover */
.stExpander > details > summary:hover {
    color: #c4b5fd !important;
    text-shadow: 0 0 6px rgba(167,139,250,.5);
}

/* Metric delta neon glow */
[data-testid="stMetricDelta"] {
    text-shadow: 0 0 6px rgba(34,197,94,.5);
}

/* Data frame header glow */
.stDataFrame thead th {
    background: rgba(139,92,246,.06) !important;
    color: #c4b5fd !important;
    text-shadow: 0 0 4px rgba(167,139,250,.4);
    border-bottom: 1px solid rgba(167,139,250,.2) !important;
}

/* ═══════════════════════════════════════════════════════════
   LEVEL 19 — NEON CORNER ACCENTS
═══════════════════════════════════════════════════════════ */
.corner-accent { position:relative; }
.corner-accent::before,.corner-accent::after {
    content:''; position:absolute; width:16px; height:16px; z-index:10;
}
.corner-accent::before { top:-1px; left:-1px; border-top:2px solid #a855f7; border-left:2px solid #a855f7; border-radius:4px 0 0 0; box-shadow:-2px -2px 8px rgba(168,85,247,.5); }
.corner-accent::after  { bottom:-1px; right:-1px; border-bottom:2px solid #f43f5e; border-right:2px solid #f43f5e; border-radius:0 0 4px 0; box-shadow:2px 2px 8px rgba(244,63,94,.5); }
.corner-accent-electric::before { border-color:#00f5ff; box-shadow:-2px -2px 8px rgba(0,245,255,.5); }
.corner-accent-electric::after  { border-color:#00f5ff; box-shadow:2px 2px 8px rgba(0,245,255,.5); }
.corner-accent-full::before { width:24px; height:24px; }
.corner-accent-full::after  { width:24px; height:24px; }

/* ═══════════════════════════════════════════════════════════
   LEVEL 20 — NEON GLOW SCROLLBAR UPGRADE
═══════════════════════════════════════════════════════════ */
::-webkit-scrollbar       { width:6px; height:6px; }
::-webkit-scrollbar-track { background:rgba(8,6,20,.6); border-radius:3px; }
::-webkit-scrollbar-thumb { background:linear-gradient(180deg,#7c3aed,#a855f7,#f43f5e); border-radius:3px; box-shadow:0 0 6px rgba(168,85,247,.5); }
::-webkit-scrollbar-thumb:hover { background:linear-gradient(180deg,#a855f7,#f43f5e,#06b6d4); box-shadow:0 0 12px rgba(168,85,247,.8); }
::-webkit-scrollbar-corner { background:rgba(6,8,16,.8); }

/* ═══════════════════════════════════════════════════════════
   LEVEL 21 — NEON MARQUEE BANNER
═══════════════════════════════════════════════════════════ */
.neon-marquee-wrap {
    overflow:hidden; border-radius:10px; padding:8px 0;
    background:rgba(139,92,246,.04); border:1px solid rgba(139,92,246,.14);
    box-shadow:inset 0 0 16px rgba(139,92,246,.04);
}
.neon-marquee {
    display:inline-flex; gap:60px; white-space:nowrap;
    animation:marqueeScroll 24s linear infinite;
    font-family:'Orbitron',monospace; font-size:.68rem; font-weight:700;
    text-transform:uppercase; letter-spacing:.12em;
}
.neon-marquee span.m-pink   { color:#f43f5e; text-shadow:0 0 6px rgba(244,63,94,.7); }
.neon-marquee span.m-purple { color:#a855f7; text-shadow:0 0 6px rgba(168,85,247,.7); }
.neon-marquee span.m-cyan   { color:#22d3ee; text-shadow:0 0 6px rgba(34,211,238,.7); }
.neon-marquee span.m-lime   { color:#39ff14; text-shadow:0 0 6px rgba(57,255,20,.7); }
.neon-marquee span.m-gold   { color:#ffbf00; text-shadow:0 0 6px rgba(255,191,0,.7); }
.neon-marquee span.m-white  { color:rgba(255,255,255,.6); }
@keyframes marqueeScroll { 0%{transform:translateX(0);} 100%{transform:translateX(-50%);} }

/* ═══════════════════════════════════════════════════════════
   LEVEL 22 — NEON ALERT / NOTIFICATION BOXES
═══════════════════════════════════════════════════════════ */
.neon-alert { border-radius:14px; padding:14px 18px; display:flex; align-items:center; gap:12px; margin-bottom:12px; font-size:.85rem; }
.neon-alert-icon { font-size:1.3rem; flex-shrink:0; }
.na-electric{ background:rgba(0,245,255,.05); border:1px solid rgba(0,245,255,.3); color:rgba(255,255,255,.8); box-shadow:0 0 12px rgba(0,245,255,.1); }
.na-electric .neon-alert-icon { filter:drop-shadow(0 0 6px #00f5ff); }
.na-magenta { background:rgba(255,0,255,.05); border:1px solid rgba(255,0,255,.3); color:rgba(255,255,255,.8); box-shadow:0 0 12px rgba(255,0,255,.1); }
.na-fire    { background:rgba(255,69,0,.06); border:1px solid rgba(255,69,0,.3); color:rgba(255,255,255,.8); box-shadow:0 0 12px rgba(255,69,0,.1); }
.na-success { background:rgba(57,255,20,.05); border:1px solid rgba(57,255,20,.3); color:rgba(255,255,255,.8); box-shadow:0 0 12px rgba(57,255,20,.1); }
.na-plasma  { background:rgba(139,92,246,.06); border:1px solid rgba(168,85,247,.3); color:rgba(255,255,255,.8); box-shadow:0 0 12px rgba(139,92,246,.12); }

/* ═══════════════════════════════════════════════════════════
   LEVEL 23 — NEON GLASSMORPHISM MEGA CARD
═══════════════════════════════════════════════════════════ */
.glass-mega {
    background: linear-gradient(135deg,
        rgba(139,92,246,.08) 0%,
        rgba(6,182,212,.05) 35%,
        rgba(244,63,94,.06) 70%,
        rgba(139,92,246,.08) 100%);
    backdrop-filter: blur(28px);
    -webkit-backdrop-filter: blur(28px);
    border: 1px solid rgba(255,255,255,.08);
    border-radius: 24px;
    padding: 24px;
    box-shadow:
        0 0 0 1px rgba(167,139,250,.08),
        0 8px 32px rgba(0,0,0,.4),
        0 0 60px rgba(139,92,246,.06),
        inset 0 1px 0 rgba(255,255,255,.06),
        inset 0 -1px 0 rgba(0,0,0,.2);
    position: relative; overflow: hidden;
    transition: all .3s ease;
}
.glass-mega::before {
    content: '';
    position: absolute; top: 0; left: 0; right: 0; height: 1px;
    background: linear-gradient(90deg, transparent, rgba(167,139,250,.5), rgba(244,63,94,.3), rgba(6,182,212,.4), transparent);
    box-shadow: 0 0 8px rgba(167,139,250,.4);
}
.glass-mega:hover {
    border-color: rgba(167,139,250,.2);
    box-shadow:
        0 0 0 1px rgba(167,139,250,.2),
        0 16px 48px rgba(0,0,0,.5),
        0 0 80px rgba(139,92,246,.1),
        inset 0 1px 0 rgba(255,255,255,.08);
    transform: translateY(-2px);
}

/* ═══════════════════════════════════════════════════════════
   LEVEL 24 — NEON SONG CARD MEGA ENHANCEMENT
═══════════════════════════════════════════════════════════ */
.song-item-card.neon-enhanced {
    border-color: rgba(139,92,246,.25) !important;
    box-shadow: 0 0 8px rgba(139,92,246,.15), 0 4px 16px rgba(0,0,0,.3) !important;
}
.song-item-card.neon-enhanced:hover {
    border-color: rgba(167,139,250,.5) !important;
    box-shadow: 0 0 20px rgba(139,92,246,.35), 0 0 40px rgba(244,63,94,.15), 0 12px 32px rgba(0,0,0,.4) !important;
}

/* ═══════════════════════════════════════════════════════════
   LEVEL 25 — FINAL POLISH: AMBIENT GLOBAL GLOW
═══════════════════════════════════════════════════════════ */
/* Extra ambient layers on top of existing ::before */
.stApp {
    background:
        radial-gradient(ellipse 90% 50% at 20% 5%, rgba(139,92,246,.04) 0%, transparent 55%),
        radial-gradient(ellipse 70% 50% at 80% 95%, rgba(244,63,94,.04) 0%, transparent 55%),
        radial-gradient(ellipse 60% 40% at 50% 50%, rgba(0,245,255,.02) 0%, transparent 60%),
        #060810 !important;
}
/* Pulsing ambient glow on body edges */
body::before {
    content:''; position:fixed; inset:0; z-index:0; pointer-events:none;
    background:
        radial-gradient(ellipse 40% 40% at 0% 0%,   rgba(139,92,246,.06) 0%, transparent 60%),
        radial-gradient(ellipse 40% 40% at 100% 100%,rgba(244,63,94,.05) 0%, transparent 60%),
        radial-gradient(ellipse 30% 30% at 100% 0%,  rgba(0,245,255,.04) 0%, transparent 55%),
        radial-gradient(ellipse 30% 30% at 0% 100%,  rgba(57,255,20,.03) 0%, transparent 55%);
    animation: ambientGlowPulse 8s ease-in-out infinite alternate;
}
@keyframes ambientGlowPulse {
    0%  { opacity:.5; }
    100%{ opacity:1; }
}

/* Orbitron headings utility */
.font-orbitron { font-family:'Orbitron',monospace !important; }
.font-rajdhani { font-family:'Rajdhani',sans-serif !important; font-weight:700 !important; }
.font-mono-neon { font-family:'Share Tech Mono',monospace !important; }

</style>
""", unsafe_allow_html=True)

# Helper Function: Clean Song Titles for Lyrics Query
def clean_song_title(title: str) -> str:
    """Strip YouTube-style noise from song/artist names for better API matching."""
    # Remove parenthesised and bracketed suffixes first
    title = re.sub(r'\([^)]*\)', '', title)   # (Official Video), (Full Song) …
    title = re.sub(r'\[[^\]]*\]', '', title)   # [Official], [4K] …
    # Common YouTube noise phrases
    _noise = [
        'official music video', 'official video', 'official audio',
        'lyric video', 'lyrics video', 'full video', 'full song', 'full audio',
        'audio song', 'video song', 'new song', 'latest song',
        'hd video', 'hq video', 'lyrics', 'hq', 'hd', '4k',
        'ft.', 'feat.', ' ft ', ' feat '
    ]
    for phrase in _noise:
        title = re.compile(re.escape(phrase), re.IGNORECASE).sub('', title)
    # Collapse whitespace
    title = re.sub(r'\s{2,}', ' ', title).strip(' |-_,')
    return title

# Helper Function: Fetch & Process Lyrics via Gemini
def load_lyrics_via_gemini(title: str, artist: str, duration_sec: int, api_key: str) -> Optional[dict]:
    url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-2.5-flash:generateContent?key={api_key}"
    prompt = f"""
    Search for the lyrics of the song "{title}" by "{artist}". 
    Create a highly accurate synced lyric LRC file with [mm:ss.xx] timestamps that fit inside a song of {duration_sec} seconds.
    If the song is in Hindi, Telugu, or another language, keep the lyrics in its transliterated (romanized/English script) or native script so it is readable.
    The first lyric line should start around [00:10.00] or later, and the last line should end before the total duration.
    
    Return ONLY the parsed .lrc formatted text block. Do not return any introduction, explanation, markdown fences, or notes.
    """
    
    headers = {"Content-Type": "application/json"}
    data = {
        "contents": [{
            "parts": [{"text": prompt}]
        }]
    }
    try:
        res = requests.post(url, json=data, headers=headers, timeout=15)
        if res.status_code == 200:
            content = res.json()
            generated_text = content['candidates'][0]['content']['parts'][0]['text'].strip()
            generated_text = re.sub(r'^```[a-zA-Z]*\n', '', generated_text)
            generated_text = re.sub(r'\n```$', '', generated_text)
            plain_text = re.sub(r'^\[\d+:\d+\.\d+\]\s*', '', generated_text, flags=re.MULTILINE)
            return {
                "synced": generated_text,
                "plain": plain_text
            }
        return None
    except Exception as e:
        print(f"Error calling Gemini for auto-lyrics: {e}")
        return None

# Helper Function: Translate Lyrics
def translate_lyrics_via_gemini(lrc_text: str, api_key: str) -> Optional[str]:
    url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-2.5-flash:generateContent?key={api_key}"
    prompt = f"""
    You are a professional music translator. Given the following LRC synced lyrics, translate them line-by-line into English.
    Keep the exact [mm:ss.xx] timestamps unchanged. Place the translated text next to the timestamp, replacing the original text.
    Do not add notes, explanations, or wrappers. Return only the translated LRC lines.
    
    LRC Synced Lyrics:
    {lrc_text}
    """
    headers = {"Content-Type": "application/json"}
    data = {"contents": [{"parts": [{"text": prompt}]}]}
    try:
        res = requests.post(url, json=data, headers=headers, timeout=20)
        if res.status_code == 200:
            content = res.json()
            generated_text = content['candidates'][0]['content']['parts'][0]['text'].strip()
            generated_text = re.sub(r'^```[a-zA-Z]*\n', '', generated_text)
            generated_text = re.sub(r'\n```$', '', generated_text)
            return generated_text
        return None
    except Exception as e:
        print(f"Error translating lyrics: {e}")
        return None

# Helper Function: Fetch & Process Lyrics
def load_lyrics_for_song(song: dict):
    youtube_id = song['id']
    
    # Check cache first
    cached = db.get_cached_lyrics(youtube_id)
    if cached:
        if cached.get('synced_lyrics') or cached.get('plain_lyrics'):
            st.session_state.synced_lyrics = lp.parse_lrc(cached['synced_lyrics']) if cached['synced_lyrics'] else []
            st.session_state.plain_lyrics = cached['plain_lyrics'] or ""
            st.session_state.lyrics_status = "synced" if st.session_state.synced_lyrics else "plain"
            return

    cleaned_title = clean_song_title(song['title'])
    artist = clean_song_title(song['uploader'])
    duration_sec = int(song.get('duration', 180))

    def _alt_parts():
        """Split 'Artist - Song' YouTube titles to derive real artist & track name."""
        raw = song['title']
        if " - " in raw:
            parts = raw.split(" - ", 1)
            return clean_song_title(parts[0].strip()), clean_song_title(parts[1].strip())
        if "-" in raw:
            parts = raw.split("-", 1)
            return clean_song_title(parts[0].strip()), clean_song_title(parts[1].strip())
        return None, None

    def _title_only_parts():
        """Return just the song title (no artist), useful when uploader is a music label."""
        raw = song['title']
        if " - " in raw:
            return None, clean_song_title(raw.split(" - ", 1)[1].strip())
        return None, cleaned_title

    synced = ""
    plain = ""
    source = ""

    # ── Provider 1: LrcLib (synced LRC, global) ───────────────────────────────
    results = lp.search_lyrics(f"{artist} {cleaned_title}")
    if not results:
        a2, t2 = _alt_parts()
        if a2:
            results = lp.search_lyrics(f"{a2} {t2}")
    if not results:
        _, t_only = _title_only_parts()
        if t_only:
            results = lp.search_lyrics(t_only)
    if results:
        best = results[0]
        synced = best.get('syncedLyrics') or ""
        plain  = best.get('plainLyrics') or ""
        if synced or plain:
            source = "LrcLib"

    # ── Provider 2: NetEase Cloud Music (Hindi/Korean/Japanese/any-language synced) ─
    if not synced and not plain:
        ne = lp.get_lyrics_netease(artist, cleaned_title)
        if not ne:
            a2, t2 = _alt_parts()
            if a2:
                ne = lp.get_lyrics_netease(a2, t2)
        if not ne:
            _, t_only = _title_only_parts()
            if t_only:
                ne = lp.get_lyrics_netease("", t_only)
        if ne:
            synced = ne.get("synced", "")
            plain  = ne.get("plain", "")
            if synced or plain:
                source = "NetEase"

    # ── Provider 3: Megalobiz (synced LRC, Hindi/Bollywood strong) ────────────
    if not synced and not plain:
        mb = lp.get_lyrics_megalobiz(artist, cleaned_title)
        if not mb:
            a2, t2 = _alt_parts()
            if a2:
                mb = lp.get_lyrics_megalobiz(a2, t2)
        if not mb:
            _, t_only = _title_only_parts()
            if t_only:
                mb = lp.get_lyrics_megalobiz("", t_only)
        if mb:
            synced = mb
            plain = re.sub(r'\[\d+:\d+\.\d+\]', '', synced)
            plain = "\n".join(
                line.strip() for line in plain.split("\n")
                if line.strip() and not line.strip().startswith("[")
            )
            source = "Megalobiz"

    # ── Provider 4: Syncedlyrics Package (Musixmatch/NetEase/LrcLib search) ───
    if not synced and not plain:
        sl = lp.get_lyrics_syncedlyrics(artist, cleaned_title, allow_plain=True)
        if not sl:
            a2, t2 = _alt_parts()
            if a2:
                sl = lp.get_lyrics_syncedlyrics(a2, t2, allow_plain=True)
        if not sl:
            _, t_only = _title_only_parts()
            if t_only:
                sl = lp.get_lyrics_syncedlyrics("", t_only, allow_plain=True)
        if sl:
            synced = sl
            plain = re.sub(r'\[\d+:\d+\.\d+\]', '', synced)
            plain = "\n".join(
                line.strip() for line in plain.split("\n")
                if line.strip() and not line.strip().startswith("[")
            )
            source = "Syncedlyrics"

    # ── Provider 5: YouTube Captions/Subtitles (extracted from video) ─────────
    if not synced and not plain:
        yt_caps = lp.get_lyrics_youtube_captions(youtube_id)
        if yt_caps:
            synced = yt_caps.get("synced", "")
            plain = yt_caps.get("plain", "")
            if synced or plain:
                source = "YouTube Captions"

    # ── Provider 6: Gemini AI auto-sync (requires key) ────────────────────────
    if not synced and not plain and st.session_state.get("gemini_key"):
        with st.spinner("🤖 Querying Gemini AI for auto-sync lyrics…"):
            g = load_lyrics_via_gemini(cleaned_title, artist, duration_sec, st.session_state.gemini_key)
            if g:
                synced = g["synced"]
                plain  = g["plain"]
                source = "Gemini AI"

    # ── Provider 7: Lyrics.ovh (plain → linear sync) ──────────────────────────
    if not synced and not plain:
        p = lp.get_lyrics_ovh(artist, cleaned_title)
        if not p:
            a2, t2 = _alt_parts()
            if a2:
                p = lp.get_lyrics_ovh(a2, t2)
        if not p:
            _, t_only = _title_only_parts()
            if t_only:
                p = lp.get_lyrics_ovh("", t_only)
        if p:
            plain  = p
            synced = lp.generate_linear_lrc(plain, duration_sec)
            source = "Lyrics.ovh"

    # ── Provider 8: Chartlyrics XML API (plain → linear sync) ────────────────
    if not synced and not plain:
        c = lp.get_lyrics_chartlyrics(artist, cleaned_title)
        if not c:
            a2, t2 = _alt_parts()
            if a2:
                c = lp.get_lyrics_chartlyrics(a2, t2)
        if not c:
            _, t_only = _title_only_parts()
            if t_only:
                c = lp.get_lyrics_chartlyrics("", t_only)
        if c:
            plain  = c
            synced = lp.generate_linear_lrc(plain, duration_sec)
            source = "Chartlyrics"

    # Toast which provider won
    toast_map = {
        "LrcLib":     ("✅ Synced lyrics from LrcLib!", "🎵"),
        "NetEase":    ("🌏 Synced lyrics via NetEase Cloud Music!", "🎶"),
        "Megalobiz":  ("✨ Synced lyrics via Megalobiz!", "🎼"),
        "Syncedlyrics":("🔥 Synced lyrics via Musixmatch!", "⚡"),
        "YouTube Captions": ("📺 Timed captions extracted from YouTube video!", "🎤"),
        "Gemini AI":  ("🤖 Lyrics auto-generated by Gemini AI!", "✨"),
        "Lyrics.ovh": ("📝 Plain lyrics via Lyrics.ovh — auto-synced!", "🎤"),
        "Chartlyrics":("📋 Lyrics via Chartlyrics — auto-synced!", "🎼"),
    }
    if source in toast_map:
        msg, icon = toast_map[source]
        st.toast(msg, icon=icon)

    # Cache into SQLite
    db.cache_lyrics(
        youtube_id=youtube_id,
        track_name=cleaned_title,
        artist_name=artist,
        synced_lyrics=synced,
        plain_lyrics=plain
    )

    st.session_state.synced_lyrics = lp.parse_lrc(synced) if synced else []
    st.session_state.plain_lyrics  = plain
    st.session_state.lyrics_status = (
        "synced" if st.session_state.synced_lyrics else
        ("plain" if plain else "not_found")
    )

# Helper Function: Run Play Song Actions
def play_song(song: dict):
    st.session_state.current_song = song
    db.add_recent_play(song)
    
    # Manage session playback queue
    queue = st.session_state.get("queue", [])
    song_ids = [s.get('id') or s.get('youtube_id') for s in queue]
    target_id = song.get('id') or song.get('youtube_id')
    
    if target_id in song_ids:
        st.session_state.queue_index = song_ids.index(target_id)
    else:
        curr_idx = st.session_state.get("queue_index", 0)
        if queue:
            queue.insert(curr_idx + 1, song)
            st.session_state.queue_index = curr_idx + 1
        else:
            queue.append(song)
            st.session_state.queue_index = 0
        st.session_state.queue = queue
        
    load_lyrics_for_song(song)
    st.session_state.lyrics_manual_search = []
    st.rerun()

# Helper Function: Gemini Recommendations
def generate_ai_recommendations(api_key: str, favorites: List[dict], recents: List[dict]) -> List[dict]:
    url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-2.5-flash:generateContent?key={api_key}"
    
    fav_list = [f"{f.get('uploader', 'Unknown')} - {f.get('title', 'Unknown')}" for f in favorites[:8]]
    rec_list = [f"{r.get('uploader', 'Unknown')} - {r.get('title', 'Unknown')}" for r in recents[:8]]
    
    prompt = f"""
    You are an expert personal music DJ. Analyze the user's music preferences:
    - Favorites: {json.dumps(fav_list)}
    - Recent plays: {json.dumps(rec_list)}
    
    Recommend exactly 5 new songs matching their taste (varying genres/moods).
    Return ONLY a valid JSON array of objects. Do not include markdown code block formats or notes.
    Each object MUST have these EXACT keys:
    - "title": Song title.
    - "artist": Artist name.
    - "mood": Mood description.
    - "reason": A single sentence explanation of why they will love it.
    """
    
    headers = {"Content-Type": "application/json"}
    data = {"contents": [{"parts": [{"text": prompt}]}]}
    try:
        res = requests.post(url, json=data, headers=headers, timeout=20)
        if res.status_code == 200:
            content = res.json()
            generated_text = content['candidates'][0]['content']['parts'][0]['text'].strip()
            generated_text = re.sub(r'^```[a-zA-Z]*\n', '', generated_text)
            generated_text = re.sub(r'\n```$', '', generated_text)
            return json.loads(generated_text)
        return []
    except Exception as e:
        print(f"Error fetching AI recs: {e}")
        return []

# Helper Function: Generate Mood-Based Radio Playlist
def generate_mood_radio(api_key: str, mood: str) -> List[dict]:
    url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-2.5-flash:generateContent?key={api_key}"
    prompt = f"""
    You are an expert music DJ. Generate a playlist of exactly 6 songs that perfectly match the mood: "{mood}".
    Choose well-known songs from various genres that capture that mood beautifully.
    Return ONLY a valid JSON array. No markdown fences, no extra text.
    Each object MUST have these EXACT keys:
    - "title": Song title.
    - "artist": Artist name.
    - "mood": The mood tag.
    - "reason": One sentence on why it fits the mood.
    """
    headers = {"Content-Type": "application/json"}
    data = {"contents": [{"parts": [{"text": prompt}]}]}
    try:
        res = requests.post(url, json=data, headers=headers, timeout=20)
        if res.status_code == 200:
            content = res.json()
            generated_text = content['candidates'][0]['content']['parts'][0]['text'].strip()
            generated_text = re.sub(r'^```[a-zA-Z]*\n', '', generated_text)
            generated_text = re.sub(r'\n```$', '', generated_text)
            return json.loads(generated_text)
        return []
    except Exception as e:
        print(f"Error in mood radio: {e}")
        return []

# Helper Function: Check Sleep Timer
def check_sleep_timer():
    if st.session_state.sleep_timer_end:
        remaining = st.session_state.sleep_timer_end - datetime.now()
        if remaining.total_seconds() <= 0:
            st.session_state.sleep_timer_end = None
            st.toast("😴 Sleep timer ended — playback paused!", icon="🌙")
            st.session_state.current_song = None
            st.rerun()
        return remaining
    return None

# Helper: Render Star Rating Widget
def render_star_rating(song_id: str, song: dict, key_prefix: str = ""):
    current = st.session_state.rating_cache.get(song_id) or db.get_rating(song_id)
    st.session_state.rating_cache[song_id] = current
    stars_html = ""
    for i in range(1, 6):
        color = "#fbbf24" if i <= current else "rgba(255,255,255,0.2)"
        stars_html += f'<span style="color:{color}; font-size:1.1rem; cursor:pointer;">★</span>'
    cols = st.columns(5)
    for i, col in enumerate(cols, 1):
        with col:
            star = "★" if i <= current else "☆"
            color = "#fbbf24" if i <= current else "rgba(255,255,255,0.3)"
            if st.button(star, key=f"{key_prefix}star_{song_id}_{i}", help=f"{i} star{'s' if i>1 else ''}"):
                db.rate_song(song, i)
                st.session_state.rating_cache[song_id] = i
                st.toast(f"Rated {'⭐' * i}")
                st.rerun()

# Side Navigation Menu using streamlit-option-menu
with st.sidebar:
    st.markdown("""
    <div style="padding: 1.5rem 0 2rem 0; text-align: center;">
        <h1 style="font-size: 2.2rem; background: linear-gradient(135deg, #f43f5e 0%, #a855f7 100%); -webkit-background-clip: text; -webkit-text-fill-color: transparent; margin-bottom: 0;">MELODIFY AI</h1>
        <p style="font-size: 0.8rem; color: rgba(255,255,255,0.4); letter-spacing: 0.1em; text-transform: uppercase;">Realtime Synced Player</p>
    </div>
    """, unsafe_allow_html=True)
    
    choice = option_menu(
        menu_title=None,
        options=["Search Songs", "Play Queue & AI Recommendations", "My Favorites", "Playlists", "Recent Plays", "AI Lyrics Syncer", "📊 Stats", "🌦️ Weather Radio", "💬 Sound Therapist", "🎸 Chord Finder", "🍃 Ambient Mixer", "🧘 Focus Zone", "✨ Sonic Persona", "🎤 Vocal Coach", "🎹 Virtual Piano", "📻 Live Radio", "🏆 Music Trivia", "🌍 World Music", "📝 Song Journal", "🎭 Mood Board", "🎯 Karaoke Studio", "🔬 Song Analyzer", "⚡ BPM Tap Tempo", "🎨 Neon Visualizer", "🧬 Music DNA", "🔥 Trending Now", "🤝 Collab Studio", "📋 Setlist Builder", "⚔️ Artist Battle", "🕰️ Music Timeline", "🎬 Cover Art Lab", "🌀 Crossfade Mixer"],
        icons=["search", "list-music", "heart-fill", "music-note-list", "clock-history", "robot", "bar-chart-fill", "cloud-sun-fill", "chat-left-heart-fill", "music-note-beamed", "wind", "hourglass-split", "stars", "mic-fill", "music-note", "broadcast", "trophy-fill", "globe2", "journal-text", "palette2", "camera-reels", "activity", "lightning-charge-fill", "brush-fill", "dna", "fire"],
        menu_icon="cast",
        default_index=0,
        styles={
            "container": {"padding": "0!important", "background-color": "transparent"},
            "icon": {"color": "#a855f7", "font-size": "15px"},
            "nav-link": {
                "font-size": "14px",
                "text-align": "left",
                "margin": "0px",
                "padding": "10px 15px",
                "color": "rgba(255, 255, 255, 0.65)",
                "font-weight": "500",
                "border-radius": "10px",
                "transition": "all 0.2s"
            },
            "nav-link-selected": {"background-color": "rgba(244, 63, 94, 0.15)", "color": "#f43f5e", "border-left": "3px solid #f43f5e"},
        }
    )
    

    st.markdown("<hr style='border-color: rgba(255,255,255,0.05); margin: 1.5rem 0 1rem 0;'>", unsafe_allow_html=True)

    # --- Sleep Timer UI ---
    st.markdown("<p style='font-size:0.7rem; color:rgba(255,255,255,0.4); text-transform:uppercase; letter-spacing:0.08em; margin-bottom:6px;'>🌙 Sleep Timer</p>", unsafe_allow_html=True)
    remaining = check_sleep_timer()
    if remaining and remaining.total_seconds() > 0:
        mins_left = int(remaining.total_seconds() // 60)
        secs_left = int(remaining.total_seconds() % 60)
        st.markdown(f"<div class='sleep-badge'>🌙 Sleeping in {mins_left}m {secs_left:02d}s</div>", unsafe_allow_html=True)
        if st.button("❌ Cancel Timer", key="cancel_sleep_timer", use_container_width=True):
            st.session_state.sleep_timer_end = None
            st.toast("Sleep timer cancelled")
            st.rerun()
    else:
        timer_col1, timer_col2 = st.columns([3, 2])
        with timer_col1:
            mins = st.selectbox("Minutes", [15, 30, 45, 60, 90], index=1, key="sleep_timer_select", label_visibility="collapsed")
        with timer_col2:
            if st.button("Set ⏱️", key="set_sleep_timer", use_container_width=True):
                st.session_state.sleep_timer_end = datetime.now() + timedelta(minutes=mins)
                st.toast(f"😴 Sleep timer set for {mins} minutes!")
                st.rerun()

    st.markdown("<hr style='border-color: rgba(255,255,255,0.05); margin: 1rem 0;'>", unsafe_allow_html=True)

    # --- Keyboard Shortcuts Quick Reference ---
    with st.expander("⌨️ Keyboard Shortcuts", expanded=False):
        st.markdown("""
        <div style="font-size:0.72rem; line-height:2.2; color:rgba(255,255,255,0.55);">
            <div style="display:flex;justify-content:space-between;padding:2px 0;border-bottom:1px solid rgba(255,255,255,0.04);">
                <span>Play / Pause</span><span class="kbd-badge">Space</span>
            </div>
            <div style="display:flex;justify-content:space-between;padding:2px 0;border-bottom:1px solid rgba(255,255,255,0.04);">
                <span>Skip 10s forward</span><span class="kbd-badge">→</span>
            </div>
            <div style="display:flex;justify-content:space-between;padding:2px 0;border-bottom:1px solid rgba(255,255,255,0.04);">
                <span>Skip 10s back</span><span class="kbd-badge">←</span>
            </div>
            <div style="display:flex;justify-content:space-between;padding:2px 0;border-bottom:1px solid rgba(255,255,255,0.04);">
                <span>Volume up</span><span class="kbd-badge">↑</span>
            </div>
            <div style="display:flex;justify-content:space-between;padding:2px 0;border-bottom:1px solid rgba(255,255,255,0.04);">
                <span>Volume down</span><span class="kbd-badge">↓</span>
            </div>
            <div style="display:flex;justify-content:space-between;padding:2px 0;">
                <span>Mute</span><span class="kbd-badge">M</span>
            </div>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("<div style='height:6px;'></div>", unsafe_allow_html=True)

    # --- Animated Now Playing Widget ---
    if st.session_state.current_song:
        curr = st.session_state.current_song
        st.markdown(f"""
        <div style="background: linear-gradient(135deg, rgba(244,63,94,0.08), rgba(168,85,247,0.06));
                    border: 1px solid rgba(244,63,94,0.2); border-radius: 14px; padding: 10px 12px;">
            <div style="display:flex; align-items:center; gap:10px; margin-bottom:8px;">
                <img src="{curr['thumbnail']}" style="width:42px; height:42px; border-radius:8px; object-fit:cover; border:1px solid rgba(255,255,255,0.1);">
                <div style="overflow:hidden; flex:1;">
                    <p style="font-size:0.78rem; font-weight:700; margin:0; color:#fff;
                              text-overflow:ellipsis; white-space:nowrap; overflow:hidden;">{curr['title'][:28]}{'…' if len(curr['title'])>28 else ''}</p>
                    <p style="font-size:0.68rem; color:rgba(255,255,255,0.5); margin:0;
                              text-overflow:ellipsis; white-space:nowrap; overflow:hidden;">{curr['uploader']}</p>
                </div>
            </div>
            <div style="display:flex; align-items:flex-end; gap:3px; height:18px; padding:0 2px;">
                <div class="wave-bar"></div>
                <div class="wave-bar"></div>
                <div class="wave-bar"></div>
                <div class="wave-bar"></div>
                <div class="wave-bar"></div>
                <span style="font-size:0.6rem; color:rgba(255,255,255,0.3); margin-left:6px; align-self:center;">NOW PLAYING</span>
            </div>
        </div>
        """, unsafe_allow_html=True)


# ----------------- MAIN PLAYER VIEW (Top of Main Screen) -----------------
if st.session_state.current_song:
    song = st.session_state.current_song
    
    # Sync Python active index with JS updates
    queue_songs = st.session_state.get("queue", [])
    if not queue_songs:
        queue_songs = [song]
        st.session_state.queue = queue_songs
        st.session_state.queue_index = 0
        
    queue_json = json.dumps(queue_songs)
    current_index = st.session_state.get("queue_index", 0)
    
    # 1. Render HTML5 Three.js component
    player_html = render_player_html(
        video_id=song['id'],
        song_title=song['title'],
        artist=song['uploader'],
        thumbnail_url=song['thumbnail'],
        duration_seconds=song['duration'],
        synced_lyrics=st.session_state.synced_lyrics,
        plain_lyrics=st.session_state.plain_lyrics,
        queue_json=queue_json,
        current_index=current_index
    )
    
    components.html(player_html, height=620)
    
    # 2. Sub-controls (Favorites, Playlists, Manual Search, Close player)
    ctrl_col1, ctrl_col2, ctrl_col3, ctrl_col4 = st.columns([1.5, 2.5, 3.5, 1])
    
    with ctrl_col1:
        is_fav = db.is_favorite(song['id'])
        if is_fav:
            if st.button("❤️ Remove Favorite", key="fav_remove_btn", use_container_width=True):
                db.remove_favorite(song['id'])
                st.toast("Removed from Favorites!")
                st.rerun()
        else:
            if st.button("🤍 Add to Favorites", key="fav_add_btn", use_container_width=True):
                db.add_favorite(song)
                st.toast("Added to Favorites!")
                st.rerun()
                
    with ctrl_col2:
        playlists = db.get_playlists()
        if playlists:
            playlist_options = {p['name']: p['id'] for p in playlists}
            selected_pl_name = st.selectbox(
                "Select Playlist",
                options=list(playlist_options.keys()),
                label_visibility="collapsed",
                key="playlist_select_box"
            )
            if st.button("➕ Add to Playlist", use_container_width=True):
                target_pl_id = playlist_options[selected_pl_name]
                db.add_to_playlist(target_pl_id, song)
                st.toast(f"Added to {selected_pl_name}!")
        else:
            st.write("No playlists created yet.")
            
    with ctrl_col3:
        with st.expander("🔍 Lyrics Not Matching? Search Manually"):
            man_query = st.text_input("Song / Artist lyrics search", placeholder="e.g. Coldplay Yellow", key="manual_lyrics_search_input")
            
            # Check translation toggle if Gemini is loaded
            translate_checked = False
            if st.session_state.gemini_key:
                translate_checked = st.checkbox("AI Translate Lyrics to English", value=False)
                
            if st.button("Search Lyrics DB", key="manual_lyrics_search_btn"):
                if man_query.strip():
                    results = lp.search_lyrics(man_query)
                    st.session_state.lyrics_manual_search = results
                    st.toast(f"Found {len(results)} matches!")
            
            if st.session_state.lyrics_manual_search:
                st.markdown("<p class='text-xs text-white/50'>Select the correct lyrics match below:</p>", unsafe_allow_html=True)
                for l_match in st.session_state.lyrics_manual_search[:6]:
                    match_label = f"🎵 {l_match.get('trackName')} — {l_match.get('artistName')} ({l_match.get('albumName')})"
                    if st.button(match_label, key=f"manual_l_id_{l_match.get('id')}", use_container_width=True):
                        synced = l_match.get('syncedLyrics') or ""
                        plain = l_match.get('plainLyrics') or ""
                        
                        # AI Translate on the fly
                        if translate_checked and st.session_state.gemini_key:
                            with st.spinner("AI is translating lyrics..."):
                                translated_lrc = translate_lyrics_via_gemini(synced or plain, st.session_state.gemini_key)
                                if translated_lrc:
                                    synced = translated_lrc
                                    st.toast("Lyrics translated successfully!")
                        
                        db.cache_lyrics(
                            youtube_id=song['id'],
                            track_name=l_match.get('trackName', ''),
                            artist_name=l_match.get('artistName', ''),
                            synced_lyrics=synced,
                            plain_lyrics=plain
                        )
                        st.session_state.synced_lyrics = lp.parse_lrc(synced) if synced else []
                        st.session_state.plain_lyrics = plain
                        st.session_state.lyrics_status = "synced" if st.session_state.synced_lyrics else "plain"
                        st.session_state.lyrics_manual_search = []
                        st.toast("Lyrics successfully updated!")
                        st.rerun()
                        
        with st.expander("🎨 Artist Spotlight Bio"):
            artist_name = song['uploader']
            if st.button("✨ Load Artist Spotlight Bio", key=f"artist_spotlight_{song['id']}", use_container_width=True):
                if not st.session_state.gemini_key:
                    st.warning("Please provide a Gemini API Key to enable Artist Spotlight.")
                else:
                    with st.spinner(f"Curating story for {artist_name}..."):
                        url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-2.5-flash:generateContent?key={st.session_state.gemini_key}"
                        prompt = f"""
                        You are a music historian and curator. 
                        Generate an engaging and professional spotlight bio for the artist '{artist_name}' (who uploaded the song '{song['title']}').
                        Format it beautifully with the following sections in clean markdown:
                        - **Background & Style**: A paragraph about who they are and their musical genre/style.
                        - **Signature Releases**: List 3 of their most famous albums or top hits.
                        - **Did You Know?**: An intriguing trivia fact or story about the artist.
                        Keep it concise, premium, and visually engaging. Do not include markdown fences or wrap the response.
                        """
                        headers = {"Content-Type": "application/json"}
                        data = {"contents": [{"parts": [{"text": prompt}]}]}
                        try:
                            res = requests.post(url, json=data, headers=headers, timeout=15)
                            if res.status_code == 200:
                                content = res.json()
                                bio = content['candidates'][0]['content']['parts'][0]['text'].strip()
                                st.session_state[f"bio_{song['id']}"] = bio
                            else:
                                st.error("Failed to fetch artist bio.")
                        except Exception as e:
                            st.error(f"Error: {e}")
            
            stored_bio = st.session_state.get(f"bio_{song['id']}")
            if stored_bio:
                st.markdown(f"""
                <div style="background: rgba(168, 85, 247, 0.03); border-left: 3px solid #a855f7; padding: 12px; border-radius: 8px; margin-top: 10px; font-size: 0.85rem; line-height: 1.5; color: #e2e8f0;">
                    {stored_bio}
                </div>
                """, unsafe_allow_html=True)
                        
    with ctrl_col4:
        if st.button("✖️ Close Player", key="close_player_btn", use_container_width=True):
            st.session_state.current_song = None
            st.rerun()

    st.markdown("<hr style='border-color: rgba(255,255,255,0.05); margin: 2rem 0;'>", unsafe_allow_html=True)

# ── Floating mini now-playing bar (rendered on all pages when a song is active) ──
if st.session_state.current_song:
    _c = st.session_state.current_song
    _m, _s = divmod(int(_c.get('duration', 0)), 60)
    st.markdown(f"""
    <div class="mini-now-playing">
        <img class="mnp-thumb" src="{_c['thumbnail']}" alt="thumb">
        <div style="flex:1;overflow:hidden;">
            <div class="mnp-title">{_c['title']}</div>
            <div class="mnp-artist">{_c['uploader']}</div>
        </div>
        <div class="mnp-bars">
            <div class="mnp-bar"></div>
            <div class="mnp-bar"></div>
            <div class="mnp-bar"></div>
            <div class="mnp-bar"></div>
        </div>
        <div style="display:flex;align-items:center;gap:6px;">
            <span class="live-dot"></span>
            <span style="font-size:0.65rem;color:rgba(255,255,255,0.3);font-weight:600;text-transform:uppercase;letter-spacing:0.08em;">Live</span>
        </div>
        <span class="dur-chip">{_m:02d}:{_s:02d}</span>
    </div>
    <div style="height:52px;"></div>
    """, unsafe_allow_html=True)

# ----------------- VIEW 1: SEARCH SONGS -----------------
if choice == "Search Songs":
    st.markdown("""
    <div class="section-header-pill">
        <span class="pill-icon">🔍</span>
        <span class="pill-label">Discover Songs</span>
    </div>
    """, unsafe_allow_html=True)
    st.markdown("<h2 style='font-size:2rem;font-weight:700;margin-bottom:4px;'>Find Your Next Track</h2>", unsafe_allow_html=True)
    st.markdown("<p style='color:rgba(255,255,255,0.45);font-size:0.88rem;margin-bottom:20px;'>Search YouTube by song title, artist, album, mood, or paste a URL.</p>", unsafe_allow_html=True)
    
    search_col1, search_col2 = st.columns([8, 2])
    with search_col1:
        query_input = st.text_input(
            "Search",
            placeholder="Search by title, artist, album, or url...",
            label_visibility="collapsed",
            key="song_search_input"
        )
    with search_col2:
        search_clicked = st.button("🔍 Find Tracks", use_container_width=True, key="song_search_btn")

    if search_clicked or (query_input and query_input != st.session_state.get("prev_query", "")):
        if query_input.strip():
            with st.spinner("Searching YouTube database..."):
                st.session_state.search_results = yt.search_songs(query_input, max_results=6)
                st.session_state.prev_query = query_input
                if not st.session_state.search_results:
                    st.toast("No results found on YouTube. Try a different query.")
    
    if st.session_state.search_results:
        total_r = len(st.session_state.search_results)
        st.markdown(f"""
        <div style="display:flex;align-items:center;gap:10px;margin-bottom:16px;">
            <span style="font-size:0.75rem;color:rgba(255,255,255,0.4);">Showing <strong style="color:rgba(255,255,255,0.7);">{total_r}</strong> result{'s' if total_r!=1 else ''}</span>
            <span class="info-tag">🎵 YouTube</span>
        </div>
        """, unsafe_allow_html=True)
        
        for index, item in enumerate(st.session_state.search_results):
            duration_m, duration_s = divmod(int(item['duration']), 60)
            duration_str = f"{duration_m:02d}:{duration_s:02d}"
            
            st.markdown(f"<div class='search-result-card'>", unsafe_allow_html=True)
            card_col1, card_col2, card_col3 = st.columns([1.5, 6, 2.5])
            
            with card_col1:
                st.image(item['thumbnail'], width='stretch')
                
            with card_col2:
                st.markdown(f"""
                <div style="padding-top: 4px;">
                    <h4 style="font-size: 1.1rem; font-weight: 600; margin: 0 0 6px 0; color: #fff; line-height:1.3;">{item['title']}</h4>
                    <div style="display:flex;align-items:center;gap:7px;flex-wrap:wrap;">
                        <span class="genre-pill">🎤 {item['uploader']}</span>
                        <span class="dur-chip">⏱ {duration_str}</span>
                        <span class="info-tag">#{index+1}</span>
                    </div>
                </div>
                """, unsafe_allow_html=True)
                
            with card_col3:
                st.markdown("<div style='height: 8px;'></div>", unsafe_allow_html=True)
                play_col, queue_col = st.columns(2)
                with play_col:
                    if st.button("▶️ Play", key=f"play_search_{item['id']}", use_container_width=True):
                        play_song(item)
                with queue_col:
                    if st.button("➕ Queue", key=f"q_search_{item['id']}", use_container_width=True):
                        q = st.session_state.get("queue", [])
                        q.append(item)
                        st.session_state.queue = q
                        st.toast("Added to playback queue!")
            
            st.markdown("</div>", unsafe_allow_html=True)

# ----------------- VIEW 2: PLAY QUEUE & AI RECOMMENDATIONS -----------------
elif choice == "Play Queue & AI Recommendations":
    st.markdown("<h2 class='text-3xl font-bold mb-4'>🎵 Active Play Queue & AI Recommendations</h2>", unsafe_allow_html=True)
    
    col_q_left, col_q_right = st.columns([5, 5])
    
    with col_q_left:
        st.markdown("### 📋 Active Playback Queue")
        
        q_tracks = st.session_state.get("queue", [])
        if q_tracks:
            clear_col, shuffle_col = st.columns(2)
            with clear_col:
                if st.button("🗑️ Clear Play Queue", use_container_width=True):
                    st.session_state.queue = []
                    st.session_state.queue_index = 0
                    st.toast("Play queue cleared!")
                    st.rerun()
            with shuffle_col:
                if st.button("🔀 Shuffle Play Queue", use_container_width=True):
                    import random
                    random.shuffle(st.session_state.queue)
                    st.session_state.queue_index = 0
                    st.toast("Play queue shuffled!")
                    st.rerun()
                    
            st.markdown("<div style='height: 10px;'></div>", unsafe_allow_html=True)
            for idx, q_song in enumerate(q_tracks):
                is_playing_item = idx == st.session_state.queue_index
                bg_border_style = "border: 1px solid #f43f5e; background: rgba(244,63,94,0.06);" if is_playing_item else "border: 1px solid rgba(255,255,255,0.05); background: rgba(255,255,255,0.02);"
                
                # Format duration
                m, s = divmod(int(q_song.get('duration', 180)), 60)
                dur_str = f"{m}:{s:02d}"
                
                st.markdown(f"""
                <div style="{bg_border_style} border-radius: 12px; padding: 8px 12px; display: flex; align-items: center; gap: 12px; margin-bottom: 8px;">
                    <img src="{q_song['thumbnail']}" style="width: 40px; height: 40px; border-radius: 6px; object-fit: cover;">
                    <div style="flex-grow: 1; overflow: hidden; text-align: left;">
                        <p style="font-size: 0.85rem; font-weight: 600; margin: 0; color: { '#f43f5e' if is_playing_item else '#fff' }; text-overflow: ellipsis; white-space: nowrap; overflow: hidden;">{q_song['title']}</p>
                        <p style="font-size: 0.75rem; color: rgba(255,255,255,0.5); margin: 0; text-overflow: ellipsis; white-space: nowrap; overflow: hidden;">{q_song['uploader']}</p>
                    </div>
                    <span style="font-size: 0.75rem; font-family: monospace; color: rgba(255,255,255,0.3);">{dur_str}</span>
                </div>
                """, unsafe_allow_html=True)
        else:
            st.info("The playback queue is currently empty. Go to 'Search Songs' to add items!")
            
    with col_q_right:
        st.markdown("### 🤖 AI Recommendations & Radio")
        
        gemini_key = st.text_input(
            "Gemini API Key", 
            type="password", 
            value=st.session_state.gemini_key, 
            placeholder="AIzaSy...", 
            key="queue_gemini_key_input"
        )
        if gemini_key:
            st.session_state.gemini_key = gemini_key
            
        rec_tabs = st.tabs(["🎯 Taste Profiler", "📻 AI Mood Radio"])
        
        with rec_tabs[0]:
            st.markdown("<p style='font-size: 0.85rem; color: rgba(255,255,255,0.6); margin-bottom: 12px;'>Unlock highly personalized music recommendations based on your favorite and recently played tracks!</p>", unsafe_allow_html=True)
            if st.session_state.gemini_key:
                favs = db.get_favorites()
                recs = db.get_recent_plays()
                
                if not favs and not recs:
                    st.info("💡 Tip: Add some songs to Favorites first so the AI can analyze your taste and recommend matching tracks!")
                else:
                    if st.button("⚡ Generate AI Recommended Playlist", use_container_width=True):
                        with st.spinner("Analyzing music taste and generating recommendations..."):
                            st.session_state.ai_recs = generate_ai_recommendations(st.session_state.gemini_key, favs, recs)
                            st.toast("New AI playlist generated!")
                    
                    if st.session_state.ai_recs:
                        st.markdown("<p class='text-xs text-white/50 mb-3'>AI Recommended Tracks:</p>", unsafe_allow_html=True)
                        for idx, rec in enumerate(st.session_state.ai_recs):
                            r_col1, r_col2 = st.columns([7, 3])
                            with r_col1:
                                st.markdown(f"""
                                <div style="background: rgba(168, 85, 247, 0.04); border: 1px solid rgba(168, 85, 247, 0.15); border-radius: 12px; padding: 10px; text-align: left; margin-bottom: 8px;">
                                    <span style="font-size: 0.65rem; text-transform: uppercase; font-weight: bold; background: rgba(168,85,247,0.2); color: #c084fc; padding: 2px 6px; border-radius: 4px;">{rec.get('mood', 'Cohesive')}</span>
                                    <h5 style="margin: 6px 0 2px 0; font-size: 0.9rem; font-weight: 600; color: #fff;">{rec['title']}</h5>
                                    <p style="margin: 0; font-size: 0.75rem; color: rgba(255,255,255,0.6);">{rec['artist']}</p>
                                    <p style="margin: 4px 0 0 0; font-size: 0.7rem; font-style: italic; color: rgba(255,255,255,0.45);">{rec['reason']}</p>
                                </div>
                                """, unsafe_allow_html=True)
                            with r_col2:
                                st.markdown("<div style='height: 12px;'></div>", unsafe_allow_html=True)
                                
                                # Quick Play Recommendation
                                if st.button("▶️ Play", key=f"rec_play_{idx}", use_container_width=True):
                                    with st.spinner("Searching track on YouTube..."):
                                        search_res = yt.search_songs(f"{rec['artist']} {rec['title']}", max_results=1)
                                        if search_res:
                                            play_song(search_res[0])
                                        else:
                                            st.error("Track could not be resolved on YouTube.")
                                            
                                # Queue Recommendation
                                if st.button("➕ Queue", key=f"rec_q_{idx}", use_container_width=True):
                                    with st.spinner("Resolving track..."):
                                        search_res = yt.search_songs(f"{rec['artist']} {rec['title']}", max_results=1)
                                        if search_res:
                                            q = st.session_state.get("queue", [])
                                            q.append(search_res[0])
                                            st.session_state.queue = q
                                            st.toast(f"Added {rec['title']} to play queue!")
                                        else:
                                            st.error("Could not find song.")
            else:
                st.warning("Please provide a Gemini API Key to enable AI music suggestions.")
                
        with rec_tabs[1]:
            st.markdown("<p style='font-size: 0.85rem; color: rgba(255,255,255,0.6); margin-bottom: 15px;'>Select a vibe and let the Gemini AI DJ curate a bespoke 6-song thematic radio station for you!</p>", unsafe_allow_html=True)
            
            if not st.session_state.gemini_key:
                st.warning("Please provide a Gemini API Key to unlock AI Mood Radio.")
            else:
                # 6 Mood cards grid (3 columns x 2 rows)
                mood_data = [
                    {"name": "Energetic / Workout", "emoji": "🔥", "bg": "linear-gradient(135deg, rgba(244,63,94,0.15), rgba(249,115,22,0.15))", "border": "rgba(244,63,94,0.3)"},
                    {"name": "Chill / Relaxed", "emoji": "🌈", "bg": "linear-gradient(135deg, rgba(6,182,212,0.15), rgba(59,130,246,0.15))", "border": "rgba(6,182,212,0.3)"},
                    {"name": "Melancholic / Rainy Day", "emoji": "🌧️", "bg": "linear-gradient(135deg, rgba(99,102,241,0.15), rgba(168,85,247,0.15))", "border": "rgba(99,102,241,0.3)"},
                    {"name": "Focus / Lofi", "emoji": "⚡", "bg": "linear-gradient(135deg, rgba(16,185,129,0.15), rgba(20,184,166,0.15))", "border": "rgba(16,185,129,0.3)"},
                    {"name": "Dance / Party", "emoji": "💃", "bg": "linear-gradient(135deg, rgba(236,72,153,0.15), rgba(217,70,239,0.15))", "border": "rgba(236,72,153,0.3)"},
                    {"name": "Zen / Meditative", "emoji": "🧘", "bg": "linear-gradient(135deg, rgba(245,158,11,0.15), rgba(234,179,8,0.15))", "border": "rgba(245,158,11,0.3)"}
                ]
                
                selected_mood_click = None
                
                r1_cols = st.columns(3)
                for i in range(3):
                    m = mood_data[i]
                    with r1_cols[i]:
                        st.markdown(f"""
                        <div style="background: {m['bg']}; border: 1px solid {m['border']}; padding: 14px; border-radius: 12px; text-align: center; margin-bottom: 6px;">
                            <span style="font-size: 1.5rem;">{m['emoji']}</span>
                            <p style="margin: 4px 0 0 0; font-size: 0.82rem; color: #fff; font-weight: 600; line-height: 1.2; height: 32px; display: flex; align-items: center; justify-content: center;">{m['name'].split(' / ')[0]}</p>
                        </div>
                        """, unsafe_allow_html=True)
                        if st.button("Tune In", key=f"btn_mood_{i}", use_container_width=True):
                            selected_mood_click = m['name']
                            
                r2_cols = st.columns(3)
                for i in range(3, 6):
                    m = mood_data[i]
                    with r2_cols[i-3]:
                        st.markdown(f"""
                        <div style="background: {m['bg']}; border: 1px solid {m['border']}; padding: 14px; border-radius: 12px; text-align: center; margin-bottom: 6px;">
                            <span style="font-size: 1.5rem;">{m['emoji']}</span>
                            <p style="margin: 4px 0 0 0; font-size: 0.82rem; color: #fff; font-weight: 600; line-height: 1.2; height: 32px; display: flex; align-items: center; justify-content: center;">{m['name'].split(' / ')[0]}</p>
                        </div>
                        """, unsafe_allow_html=True)
                        if st.button("Tune In", key=f"btn_mood_{i}", use_container_width=True):
                            selected_mood_click = m['name']
                            
                if selected_mood_click:
                    st.session_state.active_mood = selected_mood_click
                    with st.spinner(f"Curating a beautiful {selected_mood_click} setlist..."):
                        st.session_state.mood_recs = generate_mood_radio(st.session_state.gemini_key, selected_mood_click)
                        st.toast(f"📻 Tuned in to {selected_mood_click} radio!")
                        st.rerun()
                
                # Render results if present
                if st.session_state.mood_recs:
                    active_m = st.session_state.get("active_mood", "AI Mood")
                    st.markdown(f"""
                    <div style="margin-top: 15px; border-left: 3px solid #f43f5e; padding-left: 10px; margin-bottom: 12px;">
                        <h4 style="margin: 0; font-size: 1rem; color: #fff;">📻 Active Station: {active_m}</h4>
                        <p style="margin: 2px 0 0 0; font-size: 0.75rem; color: rgba(255,255,255,0.45);">Handcrafted by Gemini AI Studio</p>
                    </div>
                    """, unsafe_allow_html=True)
                    
                    # Queue/Play all button
                    if st.button("🔀 Play & Queue All Mood Tracks", key="queue_all_mood_tracks", use_container_width=True):
                        with st.spinner("Resolving setlist and lining up tracks..."):
                            resolved_songs = []
                            progress_text = st.empty()
                            for idx, track in enumerate(st.session_state.mood_recs):
                                progress_text.text(f"Resolving ({idx+1}/6): {track['title']}...")
                                search_res = yt.search_songs(f"{track['artist']} {track['title']}", max_results=1)
                                if search_res:
                                    resolved_songs.append(search_res[0])
                            
                            progress_text.empty()
                            if resolved_songs:
                                q = st.session_state.get("queue", [])
                                # Append all to queue
                                q.extend(resolved_songs)
                                st.session_state.queue = q
                                st.toast(f"Added {len(resolved_songs)} tracks to queue!")
                                # Play first resolved song
                                play_song(resolved_songs[0])
                            else:
                                st.error("Could not resolve any tracks on YouTube.")
                                
                    st.markdown("<div style='height: 10px;'></div>", unsafe_allow_html=True)
                    
                    for idx, rec in enumerate(st.session_state.mood_recs):
                        r_col1, r_col2 = st.columns([7, 3])
                        with r_col1:
                            st.markdown(f"""
                            <div style="background: rgba(244, 63, 94, 0.04); border: 1px solid rgba(244, 63, 94, 0.15); border-radius: 12px; padding: 10px; text-align: left; margin-bottom: 8px;">
                                <h5 style="margin: 0 0 2px 0; font-size: 0.9rem; font-weight: 600; color: #fff;">{rec['title']}</h5>
                                <p style="margin: 0; font-size: 0.75rem; color: rgba(255,255,255,0.6);">{rec['artist']}</p>
                                <p style="margin: 4px 0 0 0; font-size: 0.7rem; font-style: italic; color: rgba(255,255,255,0.45);">{rec['reason']}</p>
                            </div>
                            """, unsafe_allow_html=True)
                        with r_col2:
                            st.markdown("<div style='height: 12px;'></div>", unsafe_allow_html=True)
                            
                            # Quick Play Recommendation
                            if st.button("▶️ Play", key=f"mood_rec_play_{idx}", use_container_width=True):
                                with st.spinner("Searching track on YouTube..."):
                                    search_res = yt.search_songs(f"{rec['artist']} {rec['title']}", max_results=1)
                                    if search_res:
                                        play_song(search_res[0])
                                    else:
                                        st.error("Track could not be resolved on YouTube.")
                                        
                            # Queue Recommendation
                            if st.button("➕ Queue", key=f"mood_rec_q_{idx}", use_container_width=True):
                                with st.spinner("Resolving track..."):
                                    search_res = yt.search_songs(f"{rec['artist']} {rec['title']}", max_results=1)
                                    if search_res:
                                        q = st.session_state.get("queue", [])
                                        q.append(search_res[0])
                                        st.session_state.queue = q
                                        st.toast(f"Added {rec['title']} to play queue!")
                                    else:
                                        st.error("Could not find song.")

# ----------------- VIEW 3: FAVORITES -----------------
elif choice == "My Favorites":
    st.markdown("<h2 class='text-3xl font-bold mb-4'>❤️ My Favorites</h2>", unsafe_allow_html=True)
    favorites = db.get_favorites()
    
    if favorites:
        if st.button("⚡ Queue All Favorites", use_container_width=True):
            queue = st.session_state.get("queue", [])
            for fav in favorites:
                song_item = {
                    'id': fav['youtube_id'],
                    'title': fav['title'],
                    'uploader': fav['uploader'],
                    'duration': fav['duration'],
                    'thumbnail': fav['thumbnail'],
                    'url': f"https://www.youtube.com/watch?v={fav['youtube_id']}"
                }
                queue.append(song_item)
            st.session_state.queue = queue
            st.toast("All favorites added to play queue!")
            
        st.markdown("<div style='height: 10px;'></div>", unsafe_allow_html=True)
        for fav in favorites:
            card_col1, card_col2, card_col3 = st.columns([1.5, 6.5, 2])
            
            duration_m, duration_s = divmod(int(fav['duration']), 60)
            duration_str = f"{duration_m:02d}:{duration_s:02d}"
            
            with card_col1:
                st.image(fav['thumbnail'], use_container_width=True)
                
            with card_col2:
                st.markdown(f"""
                <div style="padding-top: 4px;">
                    <h4 style="font-size: 1.15rem; font-weight: 600; margin: 0; color: #fff;">{fav['title']}</h4>
                    <p style="font-size: 0.85rem; color: rgba(255,255,255,0.6); margin: 2px 0 0 0;">Artist: {fav['uploader']} &nbsp;|&nbsp; Duration: {duration_str}</p>
                </div>
                """, unsafe_allow_html=True)
                
            with card_col3:
                st.markdown("<div style='height: 8px;'></div>", unsafe_allow_html=True)
                col_play, col_q, col_del = st.columns(3)
                
                song_item = {
                    'id': fav['youtube_id'],
                    'title': fav['title'],
                    'uploader': fav['uploader'],
                    'duration': fav['duration'],
                    'thumbnail': fav['thumbnail'],
                    'url': f"https://www.youtube.com/watch?v={fav['youtube_id']}"
                }
                
                with col_play:
                    if st.button("▶️", key=f"play_fav_{fav['youtube_id']}", use_container_width=True):
                        play_song(song_item)
                with col_q:
                    if st.button("➕", key=f"q_fav_{fav['youtube_id']}", use_container_width=True, help="Queue"):
                        q = st.session_state.get("queue", [])
                        q.append(song_item)
                        st.session_state.queue = q
                        st.toast("Added to Queue!")
                with col_del:
                    if st.button("🗑️", key=f"del_fav_{fav['youtube_id']}", use_container_width=True):
                        db.remove_favorite(fav['youtube_id'])
                        st.toast("Removed from favorites")
                        st.rerun()
                        
            st.markdown("<hr style='border-color: rgba(255,255,255,0.03); margin: 8px 0;'>", unsafe_allow_html=True)
    else:
        st.info("No favorites added yet! Search for songs and click '🤍 Add to Favorites' to build your collection.")

# ----------------- VIEW 4: PLAYLISTS -----------------
elif choice == "Playlists":
    st.markdown("<h2 class='text-3xl font-bold mb-4'>📂 My Playlists</h2>", unsafe_allow_html=True)
    
    col_pl_list, col_pl_content = st.columns([3, 7])
    
    with col_pl_list:
        st.markdown("<h3 class='text-lg font-semibold mb-2'>Create Playlist</h3>", unsafe_allow_html=True)
        pl_name_input = st.text_input("Playlist Name", label_visibility="collapsed", placeholder="Enter playlist name...", key="new_playlist_name_input")
        if st.button("Create Playlist", use_container_width=True):
            if pl_name_input.strip():
                if db.create_playlist(pl_name_input.strip()):
                    st.toast(f"Playlist '{pl_name_input}' created!")
                    st.rerun()
                else:
                    st.error("A playlist with that name already exists.")
                    
        st.markdown("<hr style='border-color: rgba(255,255,255,0.05); margin: 1.5rem 0;'>", unsafe_allow_html=True)
        st.markdown("<h3 class='text-lg font-semibold mb-2'>All Playlists</h3>", unsafe_allow_html=True)
        
        playlists = db.get_playlists()
        if playlists:
            for p in playlists:
                pl_btn_col1, pl_btn_col2 = st.columns([7, 3])
                with pl_btn_col1:
                    if st.button(f"📁 {p['name']}", key=f"sel_pl_{p['id']}", use_container_width=True):
                        st.session_state.selected_playlist_id = p['id']
                        st.rerun()
                with pl_btn_col2:
                    if st.button("🗑️", key=f"del_pl_{p['id']}", use_container_width=True):
                        db.delete_playlist(p['id'])
                        if st.session_state.selected_playlist_id == p['id']:
                            st.session_state.selected_playlist_id = None
                        st.toast("Playlist deleted")
                        st.rerun()
        else:
            st.info("No playlists created yet.")
            
    with col_pl_content:
        if st.session_state.selected_playlist_id:
            pl_details = [p for p in playlists if p['id'] == st.session_state.selected_playlist_id]
            if pl_details:
                pl_name = pl_details[0]['name']
                st.markdown(f"<h3 class='text-xl font-bold mb-3'>🎵 {pl_name}</h3>", unsafe_allow_html=True)
                
                songs = db.get_playlist_songs(st.session_state.selected_playlist_id)
                if songs:
                    # Queue entire playlist action
                    if st.button("⚡ Queue Entire Playlist", use_container_width=True):
                        q = st.session_state.get("queue", [])
                        for s in songs:
                            song_item = {
                                'id': s['youtube_id'],
                                'title': s['title'],
                                'uploader': s['uploader'],
                                'duration': s['duration'],
                                'thumbnail': s['thumbnail'],
                                'url': f"https://www.youtube.com/watch?v={s['youtube_id']}"
                            }
                            q.append(song_item)
                        st.session_state.queue = q
                        st.toast(f"All tracks queued!")
                        
                    st.markdown("<div style='height: 10px;'></div>", unsafe_allow_html=True)
                    for s in songs:
                        card_col1, card_col2, card_col3 = st.columns([1.5, 6.5, 2])
                        duration_m, duration_s = divmod(int(s['duration']), 60)
                        duration_str = f"{duration_m:02d}:{duration_s:02d}"
                        
                        with card_col1:
                            st.image(s['thumbnail'], use_container_width=True)
                        with card_col2:
                            st.markdown(f"""
                            <div style="padding-top: 4px;">
                                <h4 style="font-size: 1.15rem; font-weight: 600; margin: 0; color: #fff;">{s['title']}</h4>
                                <p style="font-size: 0.85rem; color: rgba(255,255,255,0.6); margin: 2px 0 0 0;">Artist: {s['uploader']} &nbsp;|&nbsp; Duration: {duration_str}</p>
                            </div>
                            """, unsafe_allow_html=True)
                        with card_col3:
                            st.markdown("<div style='height: 8px;'></div>", unsafe_allow_html=True)
                            col_play, col_q, col_del = st.columns(3)
                            
                            song_item = {
                                'id': s['youtube_id'],
                                'title': s['title'],
                                'uploader': s['uploader'],
                                'duration': s['duration'],
                                'thumbnail': s['thumbnail'],
                                'url': f"https://www.youtube.com/watch?v={s['youtube_id']}"
                            }
                            
                            with col_play:
                                if st.button("▶️", key=f"play_pl_song_{s['youtube_id']}", use_container_width=True):
                                    play_song(song_item)
                            with col_q:
                                if st.button("➕", key=f"q_pl_song_{s['youtube_id']}", use_container_width=True, help="Queue"):
                                    q = st.session_state.get("queue", [])
                                    q.append(song_item)
                                    st.session_state.queue = q
                                    st.toast("Added to Queue!")
                            with col_del:
                                if st.button("🗑️", key=f"del_pl_song_{s['youtube_id']}", use_container_width=True):
                                    db.remove_from_playlist(st.session_state.selected_playlist_id, s['youtube_id'])
                                    st.toast("Removed from playlist")
                                    st.rerun()
                        st.markdown("<hr style='border-color: rgba(255,255,255,0.03); margin: 8px 0;'>", unsafe_allow_html=True)
                else:
                    st.info("This playlist is empty. Search for songs and add them here!")
            else:
                st.session_state.selected_playlist_id = None
                st.rerun()
        else:
            st.info("Select a playlist from the sidebar to view its tracks.")

# ----------------- VIEW 5: RECENT PLAYS -----------------
elif choice == "Recent Plays":
    st.markdown("<h2 class='text-3xl font-bold mb-4'>🕒 Recent Plays</h2>", unsafe_allow_html=True)
    recents = db.get_recent_plays()
    
    if recents:
        for r in recents:
            card_col1, card_col2, card_col3 = st.columns([1.5, 6.5, 2])
            
            duration_m, duration_s = divmod(int(r['duration']), 60)
            duration_str = f"{duration_m:02d}:{duration_s:02d}"
            
            with card_col1:
                st.image(r['thumbnail'], use_container_width=True)
                
            with card_col2:
                st.markdown(f"""
                <div style="padding-top: 4px;">
                    <h4 style="font-size: 1.15rem; font-weight: 600; margin: 0; color: #fff;">{r['title']}</h4>
                    <p style="font-size: 0.85rem; color: rgba(255,255,255,0.6); margin: 2px 0 0 0;">Artist: {r['uploader']} &nbsp;|&nbsp; Duration: {duration_str}</p>
                </div>
                """, unsafe_allow_html=True)
                
            with card_col3:
                st.markdown("<div style='height: 8px;'></div>", unsafe_allow_html=True)
                play_col, queue_col = st.columns(2)
                
                song_item = {
                    'id': r['youtube_id'],
                    'title': r['title'],
                    'uploader': r['uploader'],
                    'duration': r['duration'],
                    'thumbnail': r['thumbnail'],
                    'url': f"https://www.youtube.com/watch?v={r['youtube_id']}"
                }
                
                with play_col:
                    if st.button("▶️ Play Again", key=f"play_recent_{r['youtube_id']}", use_container_width=True):
                        play_song(song_item)
                with queue_col:
                    if st.button("➕ Queue", key=f"q_recent_{r['youtube_id']}", use_container_width=True):
                        q = st.session_state.get("queue", [])
                        q.append(song_item)
                        st.session_state.queue = q
                        st.toast("Added to playback queue!")
                        
            st.markdown("<hr style='border-color: rgba(255,255,255,0.03); margin: 8px 0;'>", unsafe_allow_html=True)
    else:
        st.info("No play history yet. Play some tracks to build your history!")

# ----------------- VIEW 6: AI LYRICS SYNCER -----------------
elif choice == "AI Lyrics Syncer":
    st.markdown("<h2 class='text-3xl font-bold mb-4'>🤖 AI Synced Lyrics Generator & Sync Tagging</h2>", unsafe_allow_html=True)
    
    st.markdown(
        """
        Sometimes lyrics on LRCLIB are **plain text only** (without timestamps). 
        You can use Gemini AI to automatically generate timestamps (`[mm:ss.xx]`) for plain lyrics, 
        or use the manual syncer tool inside the active HTML5 player to sync in real time!
        """,
        unsafe_allow_html=True
    )
    
    # API key setup
    st.session_state.gemini_key = st.text_input(
        "Enter your Google Gemini API Key",
        type="password",
        value=st.session_state.gemini_key,
        placeholder="AIzaSy...",
        help="Get a free Gemini API Key from Google AI Studio"
    )
    
    st.markdown("<hr style='border-color: rgba(255,255,255,0.05); margin: 1.5rem 0;'>", unsafe_allow_html=True)
    
    if not st.session_state.current_song:
        st.info("💡 Tip: Load/Play a song first, and if it only has plain lyrics, come back here to sync it!")
        
    c_song = st.session_state.current_song
    
    col_ai_left, col_ai_right = st.columns(2)
    
    with col_ai_left:
        st.markdown("### 1. Plain Lyrics (Unsynced)")
        lyrics_to_sync = st.text_area(
            "Paste unsynced lyrics here",
            value=st.session_state.plain_lyrics if c_song else "",
            height=300,
            placeholder="Line 1 of song\nLine 2 of song..."
        )
        
        song_duration_sec = st.number_input(
            "Song duration in seconds",
            min_value=10,
            max_value=1200,
            value=int(c_song['duration']) if c_song else 180
        )
        
    with col_ai_right:
        st.markdown("### 2. Timestamps Output")
        
        generate_btn = st.button("⚡ Generate AI Synced Lyrics (.lrc)", use_container_width=True)
        
        output_lrc_lyrics = st.text_area(
            "Output LRC Timestamps (LRC format)",
            height=300,
            placeholder="[00:15.20] Line 1 of song\n[00:20.45] Line 2 of song..."
        )
        
        if generate_btn:
            if not st.session_state.gemini_key:
                st.error("Please enter a Google Gemini API Key first!")
            elif not lyrics_to_sync.strip():
                st.error("Please provide some lyrics to synchronize!")
            else:
                with st.spinner("AI is estimating and generating synced timestamps..."):
                    # Call Gemini API
                    api_key = st.session_state.gemini_key
                    url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-2.5-flash:generateContent?key={api_key}"
                    
                    prompt = f"""
                    You are an expert music visualizer assistant. 
                    Given the following song's plain lyrics and total duration in seconds, estimate timestamps [mm:ss.xx] (minutes:seconds.centiseconds) for each line.
                    The timestamps should be evenly spaced and proportional, estimating where they would naturally occur in a {song_duration_sec}-second song.
                    The first line should start around [00:10.00] or later, and the last line should end before the total duration.
                    
                    Return ONLY the parsed .lrc formatted text block. Do not return any introduction, explanation, markdown fences, or notes.
                    
                    Song Duration: {song_duration_sec} seconds.
                    Plain Lyrics:
                    {lyrics_to_sync}
                    """
                    
                    headers = {"Content-Type": "application/json"}
                    data = {
                        "contents": [{
                            "parts": [{"text": prompt}]
                        }]
                    }
                    
                    try:
                        res = requests.post(url, headers=headers, json=data, timeout=30)
                        if res.status_code == 200:
                            content = res.json()
                            generated_text = content['candidates'][0]['content']['parts'][0]['text'].strip()
                            generated_text = re.sub(r'^```[a-zA-Z]*\n', '', generated_text)
                            generated_text = re.sub(r'\n```$', '', generated_text)
                            
                            st.toast("AI Timestamps generated successfully!")
                            
                            if c_song:
                                db.cache_lyrics(
                                    youtube_id=c_song['id'],
                                    track_name=c_song['title'],
                                    artist_name=c_song['uploader'],
                                    synced_lyrics=generated_text,
                                    plain_lyrics=lyrics_to_sync
                                )
                                st.session_state.synced_lyrics = lp.parse_lrc(generated_text)
                                st.session_state.plain_lyrics = lyrics_to_sync
                                st.session_state.lyrics_status = "synced"
                                st.toast("Saved & Synced automatically!")
                                st.rerun()
                        else:
                            st.error(f"Gemini API Error: {res.status_code} - {res.text}")
                    except Exception as ex:
                        st.error(f"Failed to connect to Gemini API: {ex}")

# ----------------- VIEW 7: STATS & ANALYTICS -----------------
elif choice == "📊 Stats":
    st.markdown("<h2 class='text-3xl font-bold mb-1'>📊 Listening Analytics & Insights</h2>", unsafe_allow_html=True)
    st.markdown("<p style='font-size: 0.9rem; color: rgba(255,255,255,0.5); margin-bottom: 25px;'>Your personal sonic journey, decoded in real time</p>", unsafe_allow_html=True)
    
    total_seconds = db.get_total_listening_seconds()
    hours = total_seconds // 3600
    minutes = (total_seconds % 3600) // 60
    seconds = total_seconds % 60
    time_str = f"{hours}h {minutes}m {seconds}s" if hours > 0 else f"{minutes}m {seconds}s"
    
    total_plays = db.get_total_songs_played()
    favorites = db.get_favorites()
    favs_count = len(favorites)
    
    # 3-column Grid
    st.markdown(f"""
    <div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(280px, 1fr)); gap: 20px; margin-bottom: 25px;">
        <div style="background: linear-gradient(135deg, rgba(244, 63, 94, 0.08) 0%, rgba(168, 85, 247, 0.08) 100%);
                    border: 1px solid rgba(244, 63, 94, 0.2); border-radius: 16px; padding: 20px; text-align: center;
                    box-shadow: 0 8px 32px 0 rgba(0, 0, 0, 0.25);">
            <span style="font-size: 2.2rem; filter: drop-shadow(0 0 10px rgba(244,63,94,0.4));">🎧</span>
            <h4 style="margin: 10px 0 5px 0; font-size: 0.9rem; text-transform: uppercase; letter-spacing: 0.1em; color: rgba(255,255,255,0.5);">Listening Time</h4>
            <h2 style="margin: 0; font-size: 1.8rem; font-weight: 700; color: #fff; background: linear-gradient(135deg, #f43f5e, #a855f7); -webkit-background-clip: text; -webkit-text-fill-color: transparent;">{time_str}</h2>
        </div>
        <div style="background: linear-gradient(135deg, rgba(6, 182, 212, 0.08) 0%, rgba(59, 130, 246, 0.08) 100%);
                    border: 1px solid rgba(6, 182, 212, 0.2); border-radius: 16px; padding: 20px; text-align: center;
                    box-shadow: 0 8px 32px 0 rgba(0, 0, 0, 0.25);">
            <span style="font-size: 2.2rem; filter: drop-shadow(0 0 10px rgba(6,182,212,0.4));">💿</span>
            <h4 style="margin: 10px 0 5px 0; font-size: 0.9rem; text-transform: uppercase; letter-spacing: 0.1em; color: rgba(255,255,255,0.5);">Total Streams</h4>
            <h2 style="margin: 0; font-size: 1.8rem; font-weight: 700; color: #fff; background: linear-gradient(135deg, #06b6d4, #3b82f6); -webkit-background-clip: text; -webkit-text-fill-color: transparent;">{total_plays} Plays</h2>
        </div>
        <div style="background: linear-gradient(135deg, rgba(16, 185, 129, 0.08) 0%, rgba(20, 184, 166, 0.08) 100%);
                    border: 1px solid rgba(16, 185, 129, 0.2); border-radius: 16px; padding: 20px; text-align: center;
                    box-shadow: 0 8px 32px 0 rgba(0, 0, 0, 0.25);">
            <span style="font-size: 2.2rem; filter: drop-shadow(0 0 10px rgba(16,185,129,0.4));">❤️</span>
            <h4 style="margin: 10px 0 5px 0; font-size: 0.9rem; text-transform: uppercase; letter-spacing: 0.1em; color: rgba(255,255,255,0.5);">Total Favorites</h4>
            <h2 style="margin: 0; font-size: 1.8rem; font-weight: 700; color: #fff; background: linear-gradient(135deg, #10b981, #14b8a6); -webkit-background-clip: text; -webkit-text-fill-color: transparent;">{favs_count} Songs</h2>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    col_stats_left, col_stats_right = st.columns([5, 5])
    
    with col_stats_left:
        st.markdown("### 🔥 Top 10 Most Played Tracks")
        top_tracks = db.get_top_tracks(10)
        
        if top_tracks:
            for idx, r in enumerate(top_tracks):
                if idx == 0:
                    rank_badge = "👑 <span style='color: #fbbf24; font-weight: bold;'>#1</span>"
                elif idx == 1:
                    rank_badge = "🥈 <span style='color: #9ca3af; font-weight: bold;'>#2</span>"
                elif idx == 2:
                    rank_badge = "🥉 <span style='color: #b45309; font-weight: bold;'>#3</span>"
                else:
                    rank_badge = f"<span style='color: rgba(255,255,255,0.4); font-weight: 600;'>#{idx+1}</span>"
                    
                card_col1, card_col2, card_col3 = st.columns([2, 5.5, 2.5])
                
                with card_col1:
                    st.markdown(f"<div style='padding-top: 14px; text-align: center;'>{rank_badge}</div>", unsafe_allow_html=True)
                    st.image(r['thumbnail'], use_container_width=True)
                    
                with card_col2:
                    st.markdown(f"""
                    <div style="padding-top: 6px;">
                        <p style="font-size: 0.88rem; font-weight: 600; margin: 0; color: #fff; text-overflow: ellipsis; white-space: nowrap; overflow: hidden;">{r['title']}</p>
                        <p style="font-size: 0.76rem; color: rgba(255,255,255,0.5); margin: 0; text-overflow: ellipsis; white-space: nowrap; overflow: hidden;">{r['uploader']}</p>
                        <p style="font-size: 0.72rem; margin-top: 2px; margin-bottom: 0;"><span style="background: rgba(244,63,94,0.15); color: #f43f5e; padding: 2px 8px; border-radius: 12px; font-weight: 600;">🔥 {r['play_count']} plays</span></p>
                    </div>
                    """, unsafe_allow_html=True)
                    
                with card_col3:
                    st.markdown("<div style='height: 12px;'></div>", unsafe_allow_html=True)
                    col_play, col_q = st.columns(2)
                    
                    song_item = {
                        'id': r['youtube_id'],
                        'title': r['title'],
                        'uploader': r['uploader'],
                        'duration': r['duration'],
                        'thumbnail': r['thumbnail'],
                        'url': f"https://www.youtube.com/watch?v={r['youtube_id']}"
                    }
                    
                    with col_play:
                        if st.button("▶️", key=f"play_top_{r['youtube_id']}", use_container_width=True, help="Play"):
                            play_song(song_item)
                    with col_q:
                        if st.button("➕", key=f"q_top_{r['youtube_id']}", use_container_width=True, help="Queue"):
                            q = st.session_state.get("queue", [])
                            q.append(song_item)
                            st.session_state.queue = q
                            st.toast("Added to Queue!")
                            
                st.markdown("<hr style='border-color: rgba(255,255,255,0.03); margin: 8px 0;'>", unsafe_allow_html=True)
        else:
            st.info("No listening history recorded yet. Listen to some tracks and come back!")
            
    with col_stats_right:
        st.markdown("### ⭐ Highest Rated Tracks")
        rated_tracks = db.get_all_ratings()
        
        if rated_tracks:
            for idx, r in enumerate(rated_tracks):
                card_col1, card_col2, card_col3 = st.columns([1.5, 6, 2.5])
                
                with card_col1:
                    thumb = "https://images.unsplash.com/photo-1614149162883-504ce4d13909?w=100&q=80"
                    for rec in top_tracks:
                        if rec['youtube_id'] == r['youtube_id']:
                            thumb = rec['thumbnail']
                            break
                    else:
                        for fav in favorites:
                            if fav['youtube_id'] == r['youtube_id']:
                                thumb = fav['thumbnail']
                                break
                    st.image(thumb, use_container_width=True)
                    
                with card_col2:
                    stars_str = "⭐" * r['rating']
                    st.markdown(f"""
                    <div style="padding-top: 6px;">
                        <p style="font-size: 0.88rem; font-weight: 600; margin: 0; color: #fff; text-overflow: ellipsis; white-space: nowrap; overflow: hidden;">{r['title']}</p>
                        <p style="font-size: 0.76rem; color: rgba(255,255,255,0.5); margin: 0; text-overflow: ellipsis; white-space: nowrap; overflow: hidden;">{r['uploader']}</p>
                        <p style="font-size: 0.85rem; margin: 2px 0 0 0; color: #fbbf24; font-weight: bold;">{stars_str}</p>
                    </div>
                    """, unsafe_allow_html=True)
                    
                with card_col3:
                    st.markdown("<div style='height: 12px;'></div>", unsafe_allow_html=True)
                    col_play, col_q = st.columns(2)
                    
                    song_item = {
                        'id': r['youtube_id'],
                        'title': r['title'],
                        'uploader': r['uploader'],
                        'duration': 180,
                        'thumbnail': thumb,
                        'url': f"https://www.youtube.com/watch?v={r['youtube_id']}"
                    }
                    
                    with col_play:
                        if st.button("▶️", key=f"play_rated_{r['youtube_id']}", use_container_width=True, help="Play"):
                            play_song(song_item)
                    with col_q:
                        if st.button("➕", key=f"q_rated_{r['youtube_id']}", use_container_width=True, help="Queue"):
                            q = st.session_state.get("queue", [])
                            q.append(song_item)
                            st.session_state.queue = q
                            st.toast("Added to Queue!")
                            
                st.markdown("<hr style='border-color: rgba(255,255,255,0.03); margin: 8px 0;'>", unsafe_allow_html=True)
        else:
            st.info("No rated tracks yet. Rate songs on the main player screen to see them here!")
            
    st.markdown("<hr style='border-color: rgba(255,255,255,0.05); margin: 2rem 0;'>", unsafe_allow_html=True)
    
    # Bottom full width section: Listening Diary
    st.markdown("### 📔 Personal Listening Diary & Private Notes")
    st.markdown("<p style='font-size: 0.85rem; color: rgba(255,255,255,0.5); margin-bottom: 15px;'>Capture memories, chords, tabs, or listening journals for your favorite songs.</p>", unsafe_allow_html=True)
    
    if favorites:
        diary_col_select, diary_col_editor = st.columns([4, 6])
        
        with diary_col_select:
            fav_dict = {f['title']: f for f in favorites}
            selected_fav_title = st.selectbox(
                "Choose a Favorited Song to write or edit a note for:",
                options=list(fav_dict.keys()),
                key="diary_song_select"
            )
            
            selected_fav = fav_dict[selected_fav_title]
            
            st.markdown(f"""
            <div style="background: rgba(255,255,255,0.02); border: 1px solid rgba(255,255,255,0.05); border-radius: 12px; padding: 15px; text-align: center; margin-top: 15px;">
                <img src="{selected_fav['thumbnail']}" style="width: 100px; height: 100px; border-radius: 8px; object-fit: cover; margin-bottom: 10px; border: 1px solid rgba(255,255,255,0.1);">
                <h5 style="margin: 0 0 4px 0; font-size: 1rem; font-weight: 600; color: #fff;">{selected_fav['title']}</h5>
                <p style="margin: 0; font-size: 0.8rem; color: rgba(255,255,255,0.5);">{selected_fav['uploader']}</p>
            </div>
            """, unsafe_allow_html=True)
            
        with diary_col_editor:
            current_note = db.get_song_note(selected_fav['youtube_id'])
            note_input = st.text_area(
                "Write your thoughts/memories for this song...",
                value=current_note,
                height=180,
                key=f"diary_note_input_{selected_fav['youtube_id']}"
            )
            
            if st.button("💾 Save to Listening Diary", key="save_diary_note_btn", use_container_width=True):
                if db.update_song_note(selected_fav['youtube_id'], note_input):
                    st.toast("Note saved to Listening Diary!")
                    st.rerun()
                else:
                    st.error("Failed to save note.")
                    
        st.markdown("<div style='height: 20px;'></div>", unsafe_allow_html=True)
        st.markdown("#### 📖 My Diary Entries")
        
        diary_songs = [f for f in db.get_favorites() if f.get('notes') and f.get('notes').strip()]
        
        if diary_songs:
            for idx, d_song in enumerate(diary_songs):
                st.markdown(f"""
                <div style="background: rgba(255,255,255,0.02); border: 1px solid rgba(255,255,255,0.06); border-radius: 12px; padding: 15px; margin-bottom: 12px; display: flex; gap: 15px; align-items: flex-start;">
                    <img src="{d_song['thumbnail']}" style="width: 50px; height: 50px; border-radius: 6px; object-fit: cover; border: 1px solid rgba(255,255,255,0.1);">
                    <div style="flex-grow: 1;">
                        <h5 style="margin: 0; font-size: 0.95rem; font-weight: 600; color: #fff;">{d_song['title']}</h5>
                        <p style="margin: 2px 0 6px 0; font-size: 0.75rem; color: rgba(255,255,255,0.45);">{d_song['uploader']}</p>
                        <p style="margin: 0; font-size: 0.85rem; color: #e2e8f0; font-style: italic; line-height: 1.4; background: rgba(0,0,0,0.2); padding: 10px; border-radius: 8px; border-left: 2px solid #10b981;">{d_song['notes']}</p>
                    </div>
                </div>
                """, unsafe_allow_html=True)
        else:
            st.info("No diary entries yet. Write a note above to record your first entry!")
            
    else:
        st.info("You haven't favorited any songs yet! Go add some songs to your favorites to unlock the Personal Listening Diary.")

# ----------------- VIEW 8: WEATHER DJ RADIO -----------------
elif choice == "🌦️ Weather Radio":
    st.markdown("<h2 class='text-3xl font-bold mb-1'>🌦️ Smart Weather Radio</h2>", unsafe_allow_html=True)
    st.markdown("<p style='font-size: 0.9rem; color: rgba(255,255,255,0.5); margin-bottom: 25px;'>Decodes your local weather conditions to curate the perfect atmospheric soundscape.</p>", unsafe_allow_html=True)
    
    # Geolocate & Fetch Weather
    if st.button("📡 Geolocation & Sync Weather DJ", use_container_width=True):
        with st.spinner("Geolocating your IP address..."):
            try:
                ip_res = requests.get("http://ip-api.com/json/", timeout=5).json()
                if ip_res.get("status") == "success":
                    st.session_state.weather_city = ip_res.get("city", "Delhi")
                    st.session_state.weather_country = ip_res.get("country", "India")
                    st.session_state.weather_lat = ip_res.get("lat")
                    st.session_state.weather_lon = ip_res.get("lon")
                    st.toast("Located successfully!")
                else:
                    st.error("Failed to geolocate.")
            except Exception as e:
                st.error(f"Geolocation Error: {e}")
                
        if st.session_state.get("weather_lat"):
            with st.spinner("Querying meteorological data..."):
                try:
                    w_url = f"https://api.open-meteo.com/v1/forecast?latitude={st.session_state.weather_lat}&longitude={st.session_state.weather_lon}&current_weather=true"
                    w_res = requests.get(w_url, timeout=5).json()
                    current = w_res.get("current_weather", {})
                    st.session_state.weather_temp = current.get("temperature", 25)
                    st.session_state.weather_code = current.get("weathercode", 0)
                    st.toast("Weather synced!")
                except Exception as e:
                    st.error(f"Weather Fetch Error: {e}")
                    
    # Display Visual Card if weather exists
    if st.session_state.get("weather_city"):
        city = st.session_state.weather_city
        country = st.session_state.weather_country
        temp_c = st.session_state.weather_temp
        temp_f = (temp_c * 9/5) + 32
        code = st.session_state.weather_code
        
        # Weather Mapping
        mapping = {
            0: {"desc": "Clear Skies", "emoji": "☀️", "vibe": "sunny, bright, high-energy, warm"},
            1: {"desc": "Mainly Clear", "emoji": "🌤️", "vibe": "bright, upbeat, cheerful"},
            2: {"desc": "Partly Cloudy", "emoji": "⛅", "vibe": "mid-tempo, relaxing, warm"},
            3: {"desc": "Overcast", "emoji": "☁️", "vibe": "chill, indie, lofi, atmospheric"},
            45: {"desc": "Foggy", "emoji": "🌫️", "vibe": "dreamy, ambient, mysterious, slow"},
            48: {"desc": "Foggy", "emoji": "🌫️", "vibe": "dreamy, ambient, mysterious, slow"},
            51: {"desc": "Light Drizzle", "emoji": "🌦️", "vibe": "melancholic, cozy lofi, peaceful"},
            53: {"desc": "Drizzle", "emoji": "🌦️", "vibe": "melancholic, cozy lofi, peaceful"},
            55: {"desc": "Heavy Drizzle", "emoji": "🌦️", "vibe": "melancholic, cozy lofi, peaceful"},
            61: {"desc": "Light Rain", "emoji": "🌧️", "vibe": "rainy day, melancholic, acoustic, acoustic indie"},
            63: {"desc": "Moderate Rain", "emoji": "🌧️", "vibe": "rainy day, melancholic, acoustic, lofi rain"},
            65: {"desc": "Heavy Rain", "emoji": "🌧️", "vibe": "melancholic, moody, powerful, dramatic"},
            71: {"desc": "Light Snow", "emoji": "🌨️", "vibe": "cozy, warm, acoustic, winter lounge, soft jazz"},
            73: {"desc": "Snowfall", "emoji": "🌨️", "vibe": "cozy, warm, winter lounge, chillout"},
            75: {"desc": "Heavy Snowfall", "emoji": "🌨️", "vibe": "cozy, warm, cinematic, soft piano"},
            80: {"desc": "Passing Showers", "emoji": "🌧️", "vibe": "melancholic, refreshing, chill wave"},
            81: {"desc": "Showers", "emoji": "🌧️", "vibe": "melancholic, refreshing, acoustic"},
            82: {"desc": "Violent Showers", "emoji": "🌧️", "vibe": "powerful, dramatic, high energy, electronic"},
            95: {"desc": "Thunderstorms", "emoji": "⚡", "vibe": "dark, intense, energetic, rock, powerful synth"},
            96: {"desc": "Thunderstorms with Hail", "emoji": "⚡", "vibe": "dark, intense, energetic, rock"},
            99: {"desc": "Heavy Thunderstorms", "emoji": "⚡", "vibe": "dark, intense, energetic, metal, orchestral"}
        }
        w_info = mapping.get(code, {"desc": "Clear Skies", "emoji": "☀️", "vibe": "relaxing, pleasant"})
        
        st.markdown(f"""
        <div style="background: linear-gradient(135deg, rgba(6,182,212,0.08) 0%, rgba(59,130,246,0.08) 100%);
                    border: 1px solid rgba(6,182,212,0.2); border-radius: 16px; padding: 25px; text-align: center;
                    box-shadow: 0 8px 32px 0 rgba(0,0,0,0.25); margin-bottom: 25px;">
            <span style="font-size: 3.5rem; filter: drop-shadow(0 0 15px rgba(6,182,212,0.5));">{w_info['emoji']}</span>
            <h3 style="margin: 10px 0 5px 0; font-size: 1.5rem; font-weight: 700; color: #fff;">{city}, {country}</h3>
            <h2 style="margin: 0; font-size: 2.8rem; font-weight: 800; background: linear-gradient(135deg, #06b6d4, #3b82f6); -webkit-background-clip: text; -webkit-text-fill-color: transparent;">{temp_c}°C / {temp_f:.1f}°F</h2>
            <p style="margin: 5px 0 0 0; font-size: 0.95rem; color: rgba(255,255,255,0.6); font-weight: 600; text-transform: uppercase; letter-spacing: 0.05em;">{w_info['desc']}</p>
        </div>
        """, unsafe_allow_html=True)
        
        # Trigger Gemini Prompt
        if not st.session_state.gemini_key:
            st.warning("Please provide a Gemini API Key to enable Weather DJ playlist generation.")
        else:
            if st.button("🌦️ Curate Weather DJ Setlist", use_container_width=True):
                with st.spinner("Consulting the Weather DJ..."):
                    url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-2.5-flash:generateContent?key={st.session_state.gemini_key}"
                    prompt = f"""
                    You are an expert music DJ. Generate a playlist of exactly 6 songs that perfectly match the current environment:
                    - City: {city}, {country}
                    - Temperature: {temp_c}°C
                    - Weather Condition: {w_info['desc']} (Vibe: {w_info['vibe']})
                    Choose well-known songs from various genres that capture this exact atmosphere.
                    Return ONLY a valid JSON array. No markdown fences, no extra text.
                    Each object MUST have these EXACT keys:
                    - "title": Song title.
                    - "artist": Artist name.
                    - "mood": The specific weather mood tag.
                    - "reason": One sentence on why it matches this weather.
                    """
                    headers = {"Content-Type": "application/json"}
                    data = {"contents": [{"parts": [{"text": prompt}]}]}
                    try:
                        res = requests.post(url, json=data, headers=headers, timeout=20)
                        if res.status_code == 200:
                            content = res.json()
                            generated_text = content['candidates'][0]['content']['parts'][0]['text'].strip()
                            generated_text = re.sub(r'^```[a-zA-Z]*\n', '', generated_text)
                            generated_text = re.sub(r'\n```$', '', generated_text)
                            st.session_state.weather_recs = json.loads(generated_text)
                            st.toast("Weather playlist curated!")
                        else:
                            st.error("Failed to curate weather playlist.")
                    except Exception as e:
                        st.error(f"Error: {e}")
                        
            # Render Weather Recs if available
            w_recs = st.session_state.get("weather_recs")
            if w_recs:
                st.markdown("### 📻 Curated Meteorological Playlist")
                
                if st.button("🔀 Play & Queue All Weather Tracks", key="weather_play_all", use_container_width=True):
                    with st.spinner("Resolving setlist and lining up tracks..."):
                        resolved_songs = []
                        progress_text = st.empty()
                        for idx, track in enumerate(w_recs):
                            progress_text.text(f"Resolving ({idx+1}/6): {track['title']}...")
                            search_res = yt.search_songs(f"{track['artist']} {track['title']}", max_results=1)
                            if search_res:
                                resolved_songs.append(search_res[0])
                        progress_text.empty()
                        if resolved_songs:
                            q = st.session_state.get("queue", [])
                            q.extend(resolved_songs)
                            st.session_state.queue = q
                            st.toast(f"Added {len(resolved_songs)} tracks to queue!")
                            play_song(resolved_songs[0])
                        else:
                            st.error("Could not resolve any tracks.")
                            
                st.markdown("<div style='height: 10px;'></div>", unsafe_allow_html=True)
                for idx, rec in enumerate(w_recs):
                    r_col1, r_col2 = st.columns([7, 3])
                    with r_col1:
                        st.markdown(f"""
                        <div style="background: rgba(6,182,212,0.04); border: 1px solid rgba(6,182,212,0.15); border-radius: 12px; padding: 10px; text-align: left; margin-bottom: 8px;">
                            <span style="font-size: 0.65rem; text-transform: uppercase; font-weight: bold; background: rgba(6,182,212,0.2); color: #06b6d4; padding: 2px 6px; border-radius: 4px;">{rec.get('mood', 'Weather Vibe')}</span>
                            <h5 style="margin: 6px 0 2px 0; font-size: 0.9rem; font-weight: 600; color: #fff;">{rec['title']}</h5>
                            <p style="margin: 0; font-size: 0.75rem; color: rgba(255,255,255,0.6);">{rec['artist']}</p>
                            <p style="margin: 4px 0 0 0; font-size: 0.7rem; font-style: italic; color: rgba(255,255,255,0.45);">{rec['reason']}</p>
                        </div>
                        """, unsafe_allow_html=True)
                    with r_col2:
                        st.markdown("<div style='height: 12px;'></div>", unsafe_allow_html=True)
                        if st.button("▶️ Play", key=f"w_play_{idx}", use_container_width=True):
                            with st.spinner("Searching YouTube..."):
                                search_res = yt.search_songs(f"{rec['artist']} {rec['title']}", max_results=1)
                                if search_res:
                                    play_song(search_res[0])
                        if st.button("➕ Queue", key=f"w_q_{idx}", use_container_width=True):
                            with st.spinner("Searching YouTube..."):
                                search_res = yt.search_songs(f"{rec['artist']} {rec['title']}", max_results=1)
                                if search_res:
                                    q = st.session_state.get("queue", [])
                                    q.append(search_res[0])
                                    st.session_state.queue = q
                                    st.toast("Added to queue!")
    else:
        st.info("Click '📡 Geolocation & Sync Weather DJ' above to fetch your meteorological environment and build weather-specific soundscapes.")

# ----------------- VIEW 9: SOUND THERAPIST -----------------
elif choice == "💬 Sound Therapist":
    st.markdown("<h2 class='text-3xl font-bold mb-1'>💬 AI Sound Therapist & Playlist Doctor</h2>", unsafe_allow_html=True)
    st.markdown("<p style='font-size: 0.9rem; color: rgba(255,255,255,0.5); margin-bottom: 25px;'>Share your thoughts, feelings, or day-to-day vibes, and let Dr. Melodify heal you with tailored playlists.</p>", unsafe_allow_html=True)
    
    if "therapist_messages" not in st.session_state:
        st.session_state.therapist_messages = [
            {"role": "assistant", "content": "Hello! I am Dr. Melodify, your personal AI Sound Therapist. Tell me how you are feeling, what's on your mind, or what kind of vibe you need, and I'll curate the perfect playlist to heal your soul or match your energy."}
        ]
        
    if not st.session_state.gemini_key:
        st.warning("Please provide a Gemini API Key to enable the AI Therapist Chatbot.")
    else:
        # Reset therapy button
        if st.button("🗑️ Reset Therapy Session", use_container_width=True):
            st.session_state.therapist_messages = [
                {"role": "assistant", "content": "Hello! I am Dr. Melodify, your personal AI Sound Therapist. Tell me how you are feeling, what's on your mind, or what kind of vibe you need, and I'll curate the perfect playlist to heal your soul or match your energy."}
            ]
            st.rerun()
            
        st.markdown("<div style='height: 15px;'></div>", unsafe_allow_html=True)
        
        # Render Chat history
        for msg in st.session_state.therapist_messages:
            align = "left" if msg["role"] == "assistant" else "right"
            bg = "rgba(255,255,255,0.02)" if msg["role"] == "assistant" else "rgba(244,63,94,0.08)"
            border = "rgba(255,255,255,0.05)" if msg["role"] == "assistant" else "rgba(244,63,94,0.2)"
            icon = "🩺" if msg["role"] == "assistant" else "👤"
            
            # Filter out JSON block from final user visible text
            visible_text = msg["content"]
            json_pattern = r"\[PLAYLIST_JSON\].*?\[/PLAYLIST_JSON\]"
            visible_text = re.sub(json_pattern, "", visible_text, flags=re.DOTALL).strip()
            
            st.markdown(f"""
            <div style="background: {bg}; border: 1px solid {border}; border-radius: 12px; padding: 12px 16px; margin-bottom: 12px; max-width: 85%; margin-left: {'0' if align=='left' else 'auto'}; margin-right: {'auto' if align=='left' else '0'};">
                <span style="font-size: 1.1rem; margin-right: 8px;">{icon}</span>
                <strong style="color: {'#a855f7' if align=='left' else '#f43f5e'}; font-size: 0.85rem;">{ 'Dr. Melodify' if align=='left' else 'You' }</strong>
                <p style="margin: 8px 0 0 0; font-size: 0.9rem; line-height: 1.5; color: #f3f4f6; white-space: pre-wrap;">{visible_text}</p>
            </div>
            """, unsafe_allow_html=True)
            
            # If assistant message contains a structural playlist, render the interactive widget
            if msg["role"] == "assistant" and "[PLAYLIST_JSON]" in msg["content"]:
                match = re.search(r"\[PLAYLIST_JSON\](.*?)\[/PLAYLIST_JSON\]", msg["content"], flags=re.DOTALL)
                if match:
                    try:
                        pl_data = json.loads(match.group(1).strip())
                        st.markdown("""
                        <div style="margin-left: 10px; border-left: 2px solid #a855f7; padding-left: 10px; margin-bottom: 15px; margin-top: -5px;">
                            <p style="font-size: 0.75rem; color: rgba(255,255,255,0.45); font-weight: bold; text-transform: uppercase;">🎵 Curated Healing Prescription:</p>
                        </div>
                        """, unsafe_allow_html=True)
                        for t_idx, track in enumerate(pl_data):
                            col_t1, col_t2 = st.columns([7, 3])
                            with col_t1:
                                st.markdown(f"""
                                <div style="background: rgba(168,85,247,0.03); border: 1px solid rgba(168,85,247,0.1); border-radius: 8px; padding: 8px; margin-bottom: 6px;">
                                    <span style="font-size: 0.72rem; font-weight: bold; background: rgba(168,85,247,0.15); color: #c084fc; padding: 1px 4px; border-radius: 4px;">Track {t_idx+1}</span>
                                    <h6 style="margin: 4px 0 1px 0; font-size: 0.82rem; color: #fff;">{track['title']}</h6>
                                    <p style="margin: 0; font-size: 0.72rem; color: rgba(255,255,255,0.5);">{track['artist']}</p>
                                    <p style="margin: 2px 0 0 0; font-size: 0.68rem; font-style: italic; color: rgba(255,255,255,0.35);">{track.get('reason', '')}</p>
                                </div>
                                """, unsafe_allow_html=True)
                            with col_t2:
                                st.markdown("<div style='height: 10px;'></div>", unsafe_allow_html=True)
                                if st.button("▶️ Play", key=f"th_play_{t_idx}_{hash(track['title'])}", use_container_width=True):
                                    with st.spinner("Resolving..."):
                                        res = yt.search_songs(f"{track['artist']} {track['title']}", max_results=1)
                                        if res:
                                            play_song(res[0])
                                if st.button("➕ Queue", key=f"th_q_{t_idx}_{hash(track['title'])}", use_container_width=True):
                                    with st.spinner("Resolving..."):
                                        res = yt.search_songs(f"{track['artist']} {track['title']}", max_results=1)
                                        if res:
                                            q = st.session_state.get("queue", [])
                                            q.append(res[0])
                                            st.session_state.queue = q
                                            st.toast("Queued!")
                    except Exception as e:
                        print(f"Error parsing therapist playlist: {e}")
                        
        # Chat input text box
        chat_user_input = st.text_input("Talk to Dr. Melodify...", placeholder="e.g. I am feeling a bit anxious and overwhelmed today...", key="therapist_chat_input")
        if st.button("Send Message 📤", use_container_width=True) and chat_user_input.strip():
            # Append user message
            st.session_state.therapist_messages.append({"role": "user", "content": chat_user_input})
            
            # Create full prompt with history
            history_prompt = "You are Dr. Melodify, a highly professional, empathetic, and knowledgeable music therapist. Talk to the patient, validate their feelings, offer warm encouragement, and suggest relevant musical styles or advice.\n"
            for msg in st.session_state.therapist_messages[-6:]: # last 6 messages for context
                history_prompt += f"{'Patient' if msg['role']=='user' else 'Doctor'}: {msg['content']}\n"
            
            history_prompt += """
            Doctor:
            
            If the conversation naturally leads to recommending songs, or if the user explicitly asks for a playlist, conclude your response with a 5-song playlist structured exactly inside [PLAYLIST_JSON] and [/PLAYLIST_JSON] tags like this:
            [PLAYLIST_JSON]
            [
              {"title": "Song Title", "artist": "Artist Name", "reason": "Short therapeutic justification"}
            ]
            [/PLAYLIST_JSON]
            Do not put any other markup or fences around the JSON array, keep it as raw valid JSON inside the tags.
            """
            
            with st.spinner("Dr. Melodify is listening..."):
                url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-2.5-flash:generateContent?key={st.session_state.gemini_key}"
                headers = {"Content-Type": "application/json"}
                data = {"contents": [{"parts": [{"text": history_prompt}]}]}
                try:
                    res = requests.post(url, json=data, headers=headers, timeout=25)
                    if res.status_code == 200:
                        ans = res.json()['candidates'][0]['content']['parts'][0]['text'].strip()
                        st.session_state.therapist_messages.append({"role": "assistant", "content": ans})
                    else:
                        st.session_state.therapist_messages.append({"role": "assistant", "content": "I apologize, my communication frequency seems to be interrupted. Please check your Gemini key or try again."})
                except Exception as e:
                    st.session_state.therapist_messages.append({"role": "assistant", "content": f"Connection error: {e}"})
            st.rerun()

# ----------------- VIEW 10: CHORD FINDER -----------------
elif choice == "🎸 Chord Finder":
    st.markdown("<h2 class='text-3xl font-bold mb-1'>🎸 Chord & Tab Finder</h2>", unsafe_allow_html=True)
    st.markdown("<p style='font-size: 0.9rem; color: rgba(255,255,255,0.5); margin-bottom: 25px;'>Get professional guitar chords, tab sheets, and strumming patterns for any track.</p>", unsafe_allow_html=True)
    
    # Auto-fill using currently playing song if present
    default_lookup = ""
    if st.session_state.current_song:
        c = st.session_state.current_song
        default_lookup = f"{clean_song_title(c['title'])} by {clean_song_title(c['uploader'])}"
        
    search_term = st.text_input("Enter Song Name & Artist", value=default_lookup, placeholder="e.g. Hotel California by Eagles", key="chord_finder_search_input")
    
    if not st.session_state.gemini_key:
        st.warning("Please provide a Gemini API Key to enable the AI Chord sheet generator.")
    else:
        instrument = st.radio("Select Instrument Chord Chart", ["🎸 Guitar Chords & Tabs", "🎹 Piano Keyboard Chords", "🪕 Ukulele Chords"], horizontal=True)
        
        if st.button("✨ Generate Professional Chord Sheet", use_container_width=True):
            if search_term.strip():
                with st.spinner(f"Transcribing {search_term} chords..."):
                    url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-2.5-flash:generateContent?key={st.session_state.gemini_key}"
                    prompt = f"""
                    You are a professional music transcriber and instrument instructor.
                    Generate a detailed, professional chord sheet and tab guide for the song '{search_term}' optimized for '{instrument}'.
                    Include:
                    1. Recommended Strumming/Picking Pattern.
                    2. Recommended Key & Chord Shapes charts (using plain text grid or standard syntax).
                    3. The full lyrics with Chord notation placed EXACTLY above the appropriate syllables and words.
                    Ensure the formatting is flawless and aligned. Do not return markdown fences or summaries. Just return the structured sheet.
                    """
                    headers = {"Content-Type": "application/json"}
                    data = {"contents": [{"parts": [{"text": prompt}]}]}
                    try:
                        res = requests.post(url, json=data, headers=headers, timeout=20)
                        if res.status_code == 200:
                            sheet = res.json()['candidates'][0]['content']['parts'][0]['text'].strip()
                            st.session_state[f"chord_{search_term}_{instrument}"] = sheet
                        else:
                            st.error("Failed to generate chords.")
                    except Exception as e:
                        st.error(f"Error: {e}")
                        
        stored_sheet = st.session_state.get(f"chord_{search_term}_{instrument}")
        if stored_sheet:
            st.markdown(f"""
            <div style="background: #0b0f19; border: 1px solid rgba(255,255,255,0.06); border-radius: 12px; padding: 20px; font-family: monospace; font-size: 0.9rem; line-height: 1.6; color: #fff; overflow-x: auto; white-space: pre;">
                {stored_sheet}
            </div>
            """, unsafe_allow_html=True)

# ----------------- VIEW 11: AMBIENT SOUND MIXER -----------------
elif choice == "🍃 Ambient Mixer":
    st.markdown("<h2 class='text-3xl font-bold mb-1'>🍃 Ambient Soundscape Mixer</h2>", unsafe_allow_html=True)
    st.markdown("<p style='font-size: 0.9rem; color: rgba(255,255,255,0.5); margin-bottom: 25px;'>Overlay high-fidelity environmental backdrops in the background, mixing seamlessly with Melodify AI audio tracks.</p>", unsafe_allow_html=True)

    mixer_html = """
    <!DOCTYPE html>
    <html>
    <head>
        <meta charset="UTF-8">
        <style>
            @import url('https://fonts.googleapis.com/css2?family=Outfit:wght@300;400;500;600;700&display=swap');
            body {
                font-family: 'Outfit', sans-serif;
                background-color: transparent;
                color: #f3f4f6;
                margin: 0;
                padding: 10px;
                overflow: hidden;
            }
            .mixer-grid {
                display: grid;
                grid-template-columns: repeat(auto-fit, minmax(180px, 1fr));
                gap: 20px;
                padding: 10px 0;
            }
            .sound-card {
                background: rgba(15, 23, 42, 0.45);
                backdrop-filter: blur(12px);
                border: 1px solid rgba(255, 255, 255, 0.06);
                border-radius: 16px;
                padding: 20px;
                text-align: center;
                transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
                position: relative;
            }
            .sound-card:hover {
                transform: translateY(-4px);
                border-color: rgba(6, 182, 212, 0.4);
                box-shadow: 0 10px 20px -10px rgba(6, 182, 212, 0.3);
            }
            .sound-card.active {
                background: rgba(6, 182, 212, 0.08);
                border-color: rgba(6, 182, 212, 0.5);
                box-shadow: 0 0 15px rgba(6, 182, 212, 0.15);
            }
            .emoji {
                font-size: 2.5rem;
                margin-bottom: 10px;
                display: inline-block;
                filter: drop-shadow(0 0 8px rgba(255,255,255,0.1));
                transition: transform 0.3s;
            }
            .sound-card.active .emoji {
                transform: scale(1.1) rotate(5deg);
                filter: drop-shadow(0 0 12px rgba(6, 182, 212, 0.6));
            }
            .sound-title {
                font-size: 1.05rem;
                font-weight: 600;
                margin: 4px 0 12px 0;
                color: #fff;
            }
            .slider-container {
                margin-bottom: 15px;
            }
            .volume-slider {
                -webkit-appearance: none;
                width: 100%;
                height: 6px;
                border-radius: 3px;
                background: rgba(255, 255, 255, 0.12);
                outline: none;
                transition: background 0.3s;
            }
            .volume-slider::-webkit-slider-thumb {
                -webkit-appearance: none;
                width: 14px;
                height: 14px;
                border-radius: 50%;
                background: #06b6d4;
                cursor: pointer;
                box-shadow: 0 0 8px rgba(6, 182, 212, 0.5);
                transition: transform 0.15s;
            }
            .volume-slider::-webkit-slider-thumb:hover {
                transform: scale(1.3);
            }
            .control-btn {
                background: rgba(255, 255, 255, 0.05);
                border: 1px solid rgba(255, 255, 255, 0.1);
                color: #fff;
                border-radius: 20px;
                padding: 8px 18px;
                font-size: 0.8rem;
                font-weight: 600;
                cursor: pointer;
                transition: all 0.2s;
                width: 100%;
            }
            .control-btn:hover {
                background: #06b6d4;
                border-color: #06b6d4;
                box-shadow: 0 4px 12px rgba(6, 182, 212, 0.3);
            }
            .sound-card.active .control-btn {
                background: rgba(6, 182, 212, 0.2);
                border-color: #06b6d4;
                color: #06b6d4;
            }
            .sound-card.active .control-btn:hover {
                background: #06b6d4;
                color: #fff;
            }
        </style>
    </head>
    <body>
        <div class="mixer-grid">
            <div class="sound-card" id="card-rain">
                <span class="emoji">🌧️</span>
                <div class="sound-title">Rain on Window</div>
                <div class="slider-container">
                    <input type="range" class="volume-slider" id="slider-rain" min="0" max="100" value="50" oninput="adjustVolume('rain', this.value)">
                </div>
                <button class="control-btn" id="btn-rain" onclick="toggleSound('rain')">Enable</button>
            </div>

            <div class="sound-card" id="card-campfire">
                <span class="emoji">🏕️</span>
                <div class="sound-title">Cozy Campfire</div>
                <div class="slider-container">
                    <input type="range" class="volume-slider" id="slider-campfire" min="0" max="100" value="50" oninput="adjustVolume('campfire', this.value)">
                </div>
                <button class="control-btn" id="btn-campfire" onclick="toggleSound('campfire')">Enable</button>
            </div>

            <div class="sound-card" id="card-ocean">
                <span class="emoji">🌊</span>
                <div class="sound-title">Ocean Waves</div>
                <div class="slider-container">
                    <input type="range" class="volume-slider" id="slider-ocean" min="0" max="100" value="50" oninput="adjustVolume('ocean', this.value)">
                </div>
                <button class="control-btn" id="btn-ocean" onclick="toggleSound('ocean')">Enable</button>
            </div>

            <div class="sound-card" id="card-cafe">
                <span class="emoji">☕</span>
                <div class="sound-title">Parisian Cafe</div>
                <div class="slider-container">
                    <input type="range" class="volume-slider" id="slider-cafe" min="0" max="100" value="50" oninput="adjustVolume('cafe', this.value)">
                </div>
                <button class="control-btn" id="btn-cafe" onclick="toggleSound('cafe')">Enable</button>
            </div>

            <div class="sound-card" id="card-wind">
                <span class="emoji">🌲</span>
                <div class="sound-title">Forest Whisper</div>
                <div class="slider-container">
                    <input type="range" class="volume-slider" id="slider-wind" min="0" max="100" value="50" oninput="adjustVolume('wind', this.value)">
                </div>
                <button class="control-btn" id="btn-wind" onclick="toggleSound('wind')">Enable</button>
            </div>

            <div class="sound-card" id="card-brook">
                <span class="emoji">🏞️</span>
                <div class="sound-title">Mountain Brook</div>
                <div class="slider-container">
                    <input type="range" class="volume-slider" id="slider-brook" min="0" max="100" value="50" oninput="adjustVolume('brook', this.value)">
                </div>
                <button class="control-btn" id="btn-brook" onclick="toggleSound('brook')">Enable</button>
            </div>
        </div>

        <script>
            const sounds = {
                rain: { audio: new Audio("https://www.soundjay.com/nature/sounds/rain-07.mp3"), active: false },
                campfire: { audio: new Audio("https://www.soundjay.com/nature/sounds/fire-1.mp3"), active: false },
                ocean: { audio: new Audio("https://www.soundjay.com/nature/sounds/ocean-wave-1.mp3"), active: false },
                cafe: { audio: new Audio("https://assets.mixkit.co/active_storage/sfx/91/91-84.wav"), active: false },
                wind: { audio: new Audio("https://www.soundjay.com/nature/sounds/wind-gust-1.mp3"), active: false },
                brook: { audio: new Audio("https://www.soundjay.com/nature/sounds/river-1.mp3"), active: false }
            };

            for (let key in sounds) {
                sounds[key].audio.loop = true;
                sounds[key].audio.volume = 0.5;
            }

            function toggleSound(key) {
                const s = sounds[key];
                const card = document.getElementById(`card-${key}`);
                const btn = document.getElementById(`btn-${key}`);
                
                if (s.active) {
                    s.audio.pause();
                    s.active = false;
                    card.classList.remove('active');
                    btn.innerText = "Enable";
                } else {
                    s.audio.play().catch(e => console.log("Audio Play Failed:", e));
                    s.active = true;
                    card.classList.add('active');
                    btn.innerText = "Mute";
                }
            }

            function adjustVolume(key, val) {
                sounds[key].audio.volume = val / 100;
            }
        </script>
    </body>
    </html>
    """
    components.html(mixer_html, height=540)

# ----------------- VIEW 12: FOCUS ZONE -----------------
elif choice == "🧘 Focus Zone":
    st.markdown("<h2 class='text-3xl font-bold mb-1'>🧘 Focus Zone & Binaural Beats</h2>", unsafe_allow_html=True)
    st.markdown("<p style='font-size: 0.9rem; color: rgba(255,255,255,0.5); margin-bottom: 25px;'>Procedurally synthesize custom brainwave entrainment frequencies and track focus sessions client-side.</p>", unsafe_allow_html=True)

    focus_html = """
    <!DOCTYPE html>
    <html>
    <head>
        <meta charset="UTF-8">
        <style>
            @import url('https://fonts.googleapis.com/css2?family=Outfit:wght@300;400;500;600;700&display=swap');
            body {
                font-family: 'Outfit', sans-serif;
                background-color: transparent;
                color: #f3f4f6;
                margin: 0;
                padding: 10px;
                overflow: hidden;
            }
            .focus-container {
                display: grid;
                grid-template-columns: 1fr 1fr;
                gap: 24px;
            }
            .card {
                background: rgba(15, 23, 42, 0.45);
                backdrop-filter: blur(12px);
                border: 1px solid rgba(255, 255, 255, 0.06);
                border-radius: 20px;
                padding: 24px;
                text-align: center;
                height: 420px;
                display: flex;
                flex-direction: column;
                justify-content: space-between;
                box-sizing: border-box;
            }
            .timer-display {
                font-size: 4rem;
                font-weight: 800;
                font-variant-numeric: tabular-nums;
                background: linear-gradient(135deg, #fbbf24, #f59e0b);
                -webkit-background-clip: text;
                -webkit-text-fill-color: transparent;
                margin: 15px 0;
                filter: drop-shadow(0 0 8px rgba(245,158,11,0.2));
            }
            .title-badge {
                font-size: 0.8rem;
                text-transform: uppercase;
                letter-spacing: 0.1em;
                font-weight: 700;
                color: rgba(255,255,255,0.4);
                margin-bottom: 5px;
            }
            .btn-group {
                display: flex;
                gap: 10px;
                justify-content: center;
                margin-top: 10px;
            }
            .timer-btn {
                background: rgba(255,255,255,0.05);
                border: 1px solid rgba(255,255,255,0.1);
                color: #fff;
                border-radius: 12px;
                padding: 10px 20px;
                font-size: 0.88rem;
                font-weight: 600;
                cursor: pointer;
                transition: all 0.2s;
            }
            .timer-btn.active {
                background: #f59e0b;
                border-color: #f59e0b;
                color: #fff;
                box-shadow: 0 4px 15px rgba(245,158,11,0.3);
            }
            .timer-btn:hover:not(.active) {
                background: rgba(255,255,255,0.1);
            }
            .action-btn {
                background: rgba(245, 158, 11, 0.15);
                border: 1px solid rgba(245, 158, 11, 0.3);
                color: #fbbf24;
                border-radius: 14px;
                padding: 12px 28px;
                font-size: 0.95rem;
                font-weight: 700;
                cursor: pointer;
                transition: all 0.2s;
                width: 100%;
            }
            .action-btn:hover {
                background: #f59e0b;
                color: #fff;
                box-shadow: 0 5px 15px rgba(245,158,11,0.3);
            }
            
            /* Binaural Beats Card Styles */
            .wave-selector {
                display: grid;
                grid-template-columns: repeat(2, 1fr);
                gap: 10px;
                margin: 15px 0;
            }
            .wave-btn {
                background: rgba(255,255,255,0.03);
                border: 1px solid rgba(255,255,255,0.06);
                color: rgba(255,255,255,0.7);
                border-radius: 12px;
                padding: 12px;
                font-size: 0.82rem;
                cursor: pointer;
                transition: all 0.2s;
                text-align: left;
            }
            .wave-btn:hover {
                background: rgba(255,255,255,0.06);
                color: #fff;
            }
            .wave-btn.active {
                background: rgba(168, 85, 247, 0.12);
                border-color: rgba(168, 85, 247, 0.4);
                color: #c084fc;
                box-shadow: 0 0 12px rgba(168,85,247,0.15);
            }
            .canvas-container {
                height: 70px;
                background: rgba(0,0,0,0.2);
                border-radius: 12px;
                border: 1px solid rgba(255,255,255,0.04);
                overflow: hidden;
                position: relative;
            }
            canvas {
                width: 100%;
                height: 100%;
                display: block;
            }
            .wave-action-btn {
                background: rgba(168, 85, 247, 0.15);
                border: 1px solid rgba(168, 85, 247, 0.3);
                color: #c084fc;
                border-radius: 14px;
                padding: 12px 28px;
                font-size: 0.95rem;
                font-weight: 700;
                cursor: pointer;
                transition: all 0.2s;
                width: 100%;
            }
            .wave-action-btn:hover {
                background: #a855f7;
                color: #fff;
                box-shadow: 0 5px 15px rgba(168,85,247,0.3);
            }
        </style>
    </head>
    <body>
        <div class="focus-container">
            <!-- Pomodoro Clock -->
            <div class="card">
                <div>
                    <div class="title-badge">⏱️ Focus Session Clock</div>
                    <div class="btn-group">
                        <button class="timer-btn active" id="btn-pomodoro" onclick="setTimerType('work')">Work</button>
                        <button class="timer-btn" id="btn-short" onclick="setTimerType('short')">Short Break</button>
                        <button class="timer-btn" id="btn-long" onclick="setTimerType('long')">Long Break</button>
                    </div>
                </div>
                
                <div class="timer-display" id="time-display">25:00</div>
                
                <div>
                    <button class="action-btn" id="action-btn" onclick="toggleTimer()">Start Focus Session</button>
                </div>
            </div>

            <!-- Procedural Binaural Synthesizer -->
            <div class="card">
                <div>
                    <div class="title-badge">🧠 Dynamic Binaural Beats (Stereo)</div>
                    <div class="wave-selector">
                        <button class="wave-btn active" id="wave-alpha" onclick="selectWave('alpha', 10)">
                            <strong>🧘 Alpha (10 Hz)</strong><br><span style="font-size:0.68rem; opacity:0.65;">Deep study & creativity</span>
                        </button>
                        <button class="wave-btn" id="wave-beta" onclick="selectWave('beta', 20)">
                            <strong>⚡ Beta (20 Hz)</strong><br><span style="font-size:0.68rem; opacity:0.65;">Focus & problem-solving</span>
                        </button>
                        <button class="wave-btn" id="wave-theta" onclick="selectWave('theta', 6)">
                            <strong>🎨 Theta (6 Hz)</strong><br><span style="font-size:0.68rem; opacity:0.65;">Meditation & memory</span>
                        </button>
                        <button class="wave-btn" id="wave-delta" onclick="selectWave('delta', 2.5)">
                            <strong>💤 Delta (2.5 Hz)</strong><br><span style="font-size:0.68rem; opacity:0.65;">Deep sleep & recovery</span>
                        </button>
                    </div>
                </div>

                <div class="canvas-container">
                    <canvas id="wave-canvas"></canvas>
                </div>

                <div>
                    <button class="wave-action-btn" id="wave-btn" onclick="toggleBinaural()">Generate Frequencies</button>
                </div>
            </div>
        </div>

        <script>
            // --- Pomodoro State & Timer Logic ---
            let timerInterval = null;
            let timeRemaining = 25 * 60; // 25 mins
            let isTimerRunning = false;
            let currentType = 'work'; // 'work', 'short', 'long'

            const times = {
                work: 25 * 60,
                short: 5 * 60,
                long: 15 * 60
            };

            function setTimerType(type) {
                currentType = type;
                timeRemaining = times[type];
                updateDisplay();
                
                document.querySelectorAll('.timer-btn').forEach(btn => btn.classList.remove('active'));
                document.getElementById(`btn-${type === 'work' ? 'pomodoro' : type}`).classList.add('active');
                
                if (isTimerRunning) {
                    toggleTimer();
                }
            }

            function updateDisplay() {
                const mins = Math.floor(timeRemaining / 60);
                const secs = timeRemaining % 60;
                document.getElementById('time-display').innerText = `${mins.toString().padStart(2, '0')}:${secs.toString().padStart(2, '0')}`;
            }

            function toggleTimer() {
                const btn = document.getElementById('action-btn');
                if (isTimerRunning) {
                    clearInterval(timerInterval);
                    isTimerRunning = false;
                    btn.innerText = "Start Focus Session";
                } else {
                    isTimerRunning = true;
                    btn.innerText = "Pause Session";
                    timerInterval = setInterval(() => {
                        timeRemaining--;
                        updateDisplay();
                        
                        if (timeRemaining <= 0) {
                            clearInterval(timerInterval);
                            isTimerRunning = false;
                            btn.innerText = "Start Focus Session";
                            const bell = new Audio("https://assets.mixkit.co/active_storage/sfx/911/911-84.wav");
                            bell.play();
                            alert("Focus Session Complete! Take a break.");
                            setTimerType(currentType === 'work' ? 'short' : 'work');
                        }
                    }, 1000);
                }
            }

            // --- Binaural Audio Synthesizer ---
            let audioCtx = null;
            let oscL = null;
            let oscR = null;
            let pannerL = null;
            let pannerR = null;
            let mainGain = null;
            let isBinauralPlaying = false;
            let selectedFreq = 10;
            let canvas = document.getElementById('wave-canvas');
            let ctx = canvas.getContext('2d');
            let animationFrameId = null;

            function selectWave(id, freq) {
                selectedFreq = freq;
                document.querySelectorAll('.wave-btn').forEach(btn => btn.classList.remove('active'));
                document.getElementById(`wave-${id}`).classList.add('active');
                
                if (isBinauralPlaying) {
                    oscR.frequency.value = 150 + selectedFreq;
                }
            }

            function toggleBinaural() {
                const btn = document.getElementById('wave-btn');
                if (isBinauralPlaying) {
                    if (oscL) { oscL.stop(); oscL.disconnect(); }
                    if (oscR) { oscR.stop(); oscR.disconnect(); }
                    if (mainGain) { mainGain.disconnect(); }
                    isBinauralPlaying = false;
                    btn.innerText = "Generate Frequencies";
                    btn.style.background = 'rgba(168, 85, 247, 0.15)';
                    btn.style.color = '#c084fc';
                    cancelAnimationFrame(animationFrameId);
                    ctx.clearRect(0, 0, canvas.width, canvas.height);
                } else {
                    if (!audioCtx) {
                        audioCtx = new (window.AudioContext || window.webkitAudioContext)();
                    }
                    
                    oscL = audioCtx.createOscillator();
                    oscR = audioCtx.createOscillator();
                    
                    oscL.frequency.value = 150;
                    oscR.frequency.value = 150 + selectedFreq;
                    
                    const filter = audioCtx.createBiquadFilter();
                    filter.type = 'lowpass';
                    filter.frequency.value = 200;
                    
                    pannerL = audioCtx.createStereoPanner();
                    pannerR = audioCtx.createStereoPanner();
                    
                    pannerL.pan.value = -1;
                    pannerR.pan.value = 1;
                    
                    mainGain = audioCtx.createGain();
                    mainGain.gain.value = 0.25;
                    
                    oscL.connect(pannerL);
                    pannerL.connect(filter);
                    
                    oscR.connect(pannerR);
                    pannerR.connect(filter);
                    
                    filter.connect(mainGain);
                    mainGain.connect(audioCtx.destination);
                    
                    oscL.start();
                    oscR.start();
                    
                    isBinauralPlaying = true;
                    btn.innerText = "Stop Frequencies";
                    btn.style.background = '#e11d48';
                    btn.style.color = '#fff';
                    btn.style.border = '1px solid #e11d48';
                    
                    drawWave();
                }
            }

            function drawWave() {
                canvas.width = canvas.offsetWidth;
                canvas.height = canvas.offsetHeight;
                
                ctx.clearRect(0, 0, canvas.width, canvas.height);
                ctx.lineWidth = 2;
                ctx.strokeStyle = '#c084fc';
                ctx.beginPath();
                
                const width = canvas.width;
                const height = canvas.height;
                const sliceWidth = width / 100;
                let x = 0;
                
                const time = Date.now() * 0.004;
                
                for (let i = 0; i < 100; i++) {
                    const y = height / 2 + Math.sin(i * 0.15 + time) * (height / 3) + Math.cos(i * 0.08 - time * 0.5) * 8;
                    if (i === 0) {
                        ctx.moveTo(x, y);
                    } else {
                        ctx.lineTo(x, y);
                    }
                    x += sliceWidth;
                }
                
                ctx.lineTo(width, height / 2);
                ctx.stroke();
                
                animationFrameId = requestAnimationFrame(drawWave);
            }
        </script>
    </body>
    </html>
    """
    components.html(focus_html, height=450)

# ----------------- VIEW 13: SONIC PERSONA ANALYST -----------------
elif choice == "✨ Sonic Persona":
    st.markdown("<h2 class='text-3xl font-bold mb-1'>✨ Sonic Persona Analyst</h2>", unsafe_allow_html=True)
    st.markdown("<p style='font-size: 0.9rem; color: rgba(255,255,255,0.5); margin-bottom: 25px;'>Analyze your musical preferences, Listening Diary sentiments, and star ratings to formulate your psychological sonic archetype.</p>", unsafe_allow_html=True)
    
    if not st.session_state.gemini_key:
        st.warning("Please provide a Gemini API Key to unlock your AI Sonic Persona Analysis.")
    else:
        total_seconds = db.get_total_listening_seconds()
        total_streams = db.get_total_songs_played()
        favs = db.get_favorites()
        rated_songs = db.get_all_ratings()
        recent_songs = db.get_recent_plays()
        
        if total_streams == 0 and not favs:
            st.info("💡 Tip: To generate a highly precise analysis, stream a few tracks, add items to favorites, and rate songs so the AI can capture your musical vibrations!")
        else:
            if st.button("🔮 Decode My Sonic Soul Archetype", use_container_width=True):
                with st.spinner("Decoding cosmic audio vibrations and reading diary entries..."):
                    fav_list = [f"{f.get('uploader')} - {f.get('title')}" for f in favs[:10]]
                    recents_list = [f"{r.get('uploader')} - {r.get('title')} (Plays: {r.get('play_count', 1)})" for r in recent_songs[:10]]
                    ratings_list = [f"{r.get('uploader')} - {r.get('title')} (Rating: {r.get('rating')}/5)" for r in rated_songs[:8]]
                    diaries_list = [f"Song: {d.get('title')} | Note: {d.get('notes')}" for d in favs if d.get('notes') and d['notes'].strip()][:6]
                    
                    analyst_prompt = f"""
                    You are a musical astrologer and psychoacoustic therapist. Analyze the user's comprehensive music listening diary and telemetry:
                    - Total Streams: {total_streams}
                    - Total Listening Duration: {total_seconds} seconds
                    - Favorites List: {json.dumps(fav_list)}
                    - Star-Rated Songs: {json.dumps(ratings_list)}
                    - Recently Played Tracks: {json.dumps(recents_list)}
                    - Personal Listening Diary Entries: {json.dumps(diaries_list)}
                    
                    Generate a highly immersive, beautiful sonic personality report containing:
                    1. **Your Sonic Archetype**: Assign them a poetic, premium musical archetype (e.g. "The Cyberpunk Synthesizer Rogue", "The Ethereal Dream Voyager", "The Cinematic Nostalgia Collector").
                    2. **Psychoacoustic Profile**: A beautiful, deep analysis of their subconscious mind based on the sentiments of their diary entries and ratings.
                    3. **Daily Cosmic Sonic Horoscope**: A poetic astrological prediction for their mood today.
                    
                    Conclude the report with a customized therapeutic prescription of exactly 4 songs structured in [PLAYLIST_JSON] and [/PLAYLIST_JSON] tags like this:
                    [PLAYLIST_JSON]
                    [
                      {{"title": "Song Title", "artist": "Artist Name", "reason": "Why this aligns with your cosmic frequency"}}
                    ]
                    [/PLAYLIST_JSON]
                    Make the response look stunningly formatted in clean markdown, with beautiful layout headings.
                    """
                    
                    url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-2.5-flash:generateContent?key={st.session_state.gemini_key}"
                    headers = {"Content-Type": "application/json"}
                    data = {"contents": [{"parts": [{"text": analyst_prompt}]}]}
                    try:
                        res = requests.post(url, json=data, headers=headers, timeout=30)
                        if res.status_code == 200:
                            ans = res.json()['candidates'][0]['content']['parts'][0]['text'].strip()
                            st.session_state.persona_report = ans
                            st.toast("Sonic Soul Archetype compiled!")
                        else:
                            st.error("Failed to query Gemini API.")
                    except Exception as e:
                        st.error(f"Error: {e}")
            
            stored_report = st.session_state.get("persona_report")
            if stored_report:
                visible_report = re.sub(r"\[PLAYLIST_JSON\].*?\[/PLAYLIST_JSON\]", "", stored_report, flags=re.DOTALL).strip()
                
                st.markdown(f"""
                <div style="background: rgba(15, 23, 42, 0.45); border: 1px solid rgba(168, 85, 247, 0.2); border-radius: 20px; padding: 25px; line-height: 1.6; color: #e2e8f0; box-shadow: 0 10px 30px rgba(0,0,0,0.3);">
                    {visible_report}
                </div>
                """, unsafe_allow_html=True)
                
                if "[PLAYLIST_JSON]" in stored_report:
                    match = re.search(r"\[PLAYLIST_JSON\](.*?)\[/PLAYLIST_JSON\]", stored_report, flags=re.DOTALL)
                    if match:
                        try:
                            pl_data = json.loads(match.group(1).strip())
                            st.markdown("<div style='height: 25px;'></div>", unsafe_allow_html=True)
                            st.markdown("### 🪐 Your Prescribed Cosmic Tracks")
                            
                            for t_idx, track in enumerate(pl_data):
                                col_t1, col_t2 = st.columns([7, 3])
                                with col_t1:
                                    st.markdown(f"""
                                    <div style="background: rgba(168,85,247,0.03); border: 1px solid rgba(168,85,247,0.15); border-radius: 12px; padding: 12px; margin-bottom: 8px;">
                                        <span style="font-size: 0.72rem; font-weight: bold; background: rgba(168,85,247,0.2); color: #c084fc; padding: 2px 6px; border-radius: 4px;">Alignment {t_idx+1}</span>
                                        <h5 style="margin: 6px 0 2px 0; font-size: 0.92rem; font-weight: 600; color: #fff;">{track['title']}</h5>
                                        <p style="margin: 0; font-size: 0.78rem; color: rgba(255,255,255,0.6);">{track['artist']}</p>
                                        <p style="margin: 4px 0 0 0; font-size: 0.72rem; font-style: italic; color: rgba(255,255,255,0.45);">{track.get('reason', '')}</p>
                                    </div>
                                    """, unsafe_allow_html=True)
                                with col_t2:
                                    st.markdown("<div style='height: 14px;'></div>", unsafe_allow_html=True)
                                    if st.button("▶️ Play", key=f"pe_play_{t_idx}_{hash(track['title'])}", use_container_width=True):
                                        with st.spinner("Resolving track..."):
                                            res = yt.search_songs(f"{track['artist']} {track['title']}", max_results=1)
                                            if res:
                                                play_song(res[0])
                                    if st.button("➕ Queue", key=f"pe_q_{t_idx}_{hash(track['title'])}", use_container_width=True):
                                        with st.spinner("Resolving track..."):
                                            res = yt.search_songs(f"{track['artist']} {track['title']}", max_results=1)
                                            if res:
                                                q = st.session_state.get("queue", [])
                                                q.append(res[0])
                                                st.session_state.queue = q
                                                st.toast("Queued!")
                        except Exception as e:
                            print(f"Error parsing archetype prescription: {e}")

# ----------------- VIEW 14: LYRIC GENIUS & VOCAL COACH -----------------
elif choice == "🎤 Vocal Coach":
    st.markdown("<h2 class='text-3xl font-bold mb-1'>🎤 Lyric Genius & Vocal Pitch Coach</h2>", unsafe_allow_html=True)
    st.markdown("<p style='font-size: 0.9rem; color: rgba(255,255,255,0.5); margin-bottom: 25px;'>Analyze deep metaphors behind track lyrics, and practice singing along with a real-time pitch feedback tuner in your browser.</p>", unsafe_allow_html=True)
    
    coach_tabs = st.tabs(["💡 Lyric Genius Explainer", "🎯 Interactive Vocal Pitch Coach"])
    
    with coach_tabs[0]:
        st.markdown("<h3 class='text-lg font-semibold mb-2'>Analyze Active Track Meanings</h3>", unsafe_allow_html=True)
        if not st.session_state.current_song:
            st.info("💡 Tip: Load and play a song first, then come back here to analyze its deep meanings!")
        elif not st.session_state.gemini_key:
            st.warning("Please provide a Gemini API Key to enable Lyric Genius Explainer.")
        else:
            c_song = st.session_state.current_song
            st.markdown(f"#### Active Track: **{c_song['title']}** by *{c_song['uploader']}*")
            
            if st.button("💡 Decode Song Lyrics Context & Meaning", use_container_width=True):
                with st.spinner("Analyzing text files, cultural history, and poetic metaphors..."):
                    plain_lyrics = st.session_state.plain_lyrics
                    if not plain_lyrics and st.session_state.synced_lyrics:
                        plain_lyrics = "\\n".join([line.get('text', '') for line in st.session_state.synced_lyrics])
                        
                    prompt = f"""
                    You are an expert music literary critic and musicologist. Analyze the song '{c_song['title']}' by '{c_song['uploader']}'.
                    Here are the lyrics:
                    {plain_lyrics if plain_lyrics else "Poetic lyrics are implicitly known for this track."}
                    
                    Provide a rich, visually stunning analysis outlining:
                    1. **Central Narrative Theme**: What is the song actually about?
                    2. **Hidden Metaphors & Literary Devices**: Explain 2-3 specific phrases or metaphors used in the song.
                    3. **Cultural Context**: What was the background, decade inspiration, or artist motivation behind this record?
                    Keep the response highly engaging, professional, and formatted in gorgeous markdown.
                    """
                    
                    url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-2.5-flash:generateContent?key={st.session_state.gemini_key}"
                    headers = {"Content-Type": "application/json"}
                    data = {"contents": [{"parts": [{"text": prompt}]}]}
                    try:
                        res = requests.post(url, json=data, headers=headers, timeout=25)
                        if res.status_code == 200:
                            ans = res.json()['candidates'][0]['content']['parts'][0]['text'].strip()
                            st.session_state[f"genius_{c_song['id']}"] = ans
                            st.toast("Lyric insights compiled!")
                        else:
                            st.error("Failed to consult Lyric Genius API.")
                    except Exception as e:
                        st.error(f"Error: {e}")
                        
            stored_genius = st.session_state.get(f"genius_{c_song['id']}")
            if stored_genius:
                st.markdown(f"""
                <div style="background: rgba(15,23,42,0.45); border: 1px solid rgba(244,63,94,0.15); border-radius: 16px; padding: 20px; color: #e2e8f0; line-height: 1.6; margin-top: 15px;">
                    {stored_genius}
                </div>
                """, unsafe_allow_html=True)
                
    with coach_tabs[1]:
        st.markdown("<p style='font-size: 0.85rem; color: rgba(255,255,255,0.6); margin-bottom: 15px;'>Allow browser microphone permissions, start singing, and watch your voice track across the live pitch timeline. Completely offline and client-side.</p>", unsafe_allow_html=True)
        
        pitch_html = """
        <!DOCTYPE html>
        <html>
        <head>
            <meta charset="UTF-8">
            <style>
                @import url('https://fonts.googleapis.com/css2?family=Outfit:wght@300;400;500;600;700&display=swap');
                body {
                    font-family: 'Outfit', sans-serif;
                    background-color: transparent;
                    color: #f3f4f6;
                    margin: 0;
                    padding: 10px;
                    overflow: hidden;
                }
                .coach-container {
                    text-align: center;
                }
                .tuner-card {
                    background: rgba(15, 23, 42, 0.45);
                    backdrop-filter: blur(12px);
                    border: 1px solid rgba(255, 255, 255, 0.06);
                    border-radius: 20px;
                    padding: 20px;
                    margin-bottom: 20px;
                }
                .note-display {
                    font-size: 3.5rem;
                    font-weight: 800;
                    color: #06b6d4;
                    margin: 10px 0;
                    text-shadow: 0 0 10px rgba(6,182,212,0.3);
                }
                .freq-display {
                    font-size: 0.95rem;
                    color: rgba(255,255,255,0.5);
                    font-family: monospace;
                    margin-bottom: 15px;
                }
                .graph-container {
                    background: rgba(0,0,0,0.3);
                    border: 1px solid rgba(255,255,255,0.05);
                    border-radius: 12px;
                    height: 200px;
                    position: relative;
                    margin-bottom: 15px;
                }
                canvas {
                    width: 100%;
                    height: 100%;
                    display: block;
                }
                .btn {
                    background: rgba(6, 182, 212, 0.15);
                    border: 1px solid rgba(6, 182, 212, 0.3);
                    color: #06b6d4;
                    border-radius: 14px;
                    padding: 12px 30px;
                    font-size: 0.95rem;
                    font-weight: 700;
                    cursor: pointer;
                    transition: all 0.2s;
                    width: 100%;
                }
                .btn:hover {
                    background: #06b6d4;
                    color: #fff;
                    box-shadow: 0 4px 15px rgba(6,182,212,0.3);
                }
                .btn.active {
                    background: #e11d48;
                    border-color: #e11d48;
                    color: #fff;
                }
            </style>
        </head>
        <body>
            <div class="coach-container">
                <div class="tuner-card">
                    <div style="font-size: 0.78rem; text-transform: uppercase; color: rgba(255,255,255,0.4); font-weight: bold; letter-spacing:0.05em;">🎤 Fundamental Vocal Note</div>
                    <div class="note-display" id="note-text">--</div>
                    <div class="freq-display" id="freq-text">Frequency: -- Hz</div>
                    
                    <div class="graph-container">
                        <canvas id="pitch-canvas"></canvas>
                    </div>
                    
                    <button class="btn" id="start-btn" onclick="togglePitchTracker()">Activate Vocal Coach Tuner</button>
                </div>
            </div>

            <script>
                let audioCtx = null;
                let analyser = null;
                let microphone = null;
                let isTracking = false;
                let animationId = null;
                let frequencies = [];
                let notes = [];
                let canvas = document.getElementById('pitch-canvas');
                let ctx = canvas.getContext('2d');

                const noteNames = ["C", "C#", "D", "D#", "E", "F", "F#", "G", "G#", "A", "A#", "B"];

                function noteFromFrequency(frequency) {
                    const noteNum = 12 * (Math.log(frequency / 440) / Math.log(2));
                    return Math.round(noteNum) + 69;
                }

                function togglePitchTracker() {
                    const btn = document.getElementById('start-btn');
                    if (isTracking) {
                        isTracking = false;
                        btn.innerText = "Activate Vocal Coach Tuner";
                        btn.classList.remove('active');
                        cancelAnimationFrame(animationId);
                        if (microphone) microphone.disconnect();
                        if (analyser) analyser.disconnect();
                        document.getElementById('note-text').innerText = "--";
                        document.getElementById('freq-text').innerText = "Frequency: -- Hz";
                        ctx.clearRect(0, 0, canvas.width, canvas.height);
                    } else {
                        navigator.mediaDevices.getUserMedia({ audio: true, video: false })
                            .then(stream => {
                                isTracking = true;
                                btn.innerText = "Deactivate Pitch Tracker";
                                btn.classList.add('active');
                                
                                audioCtx = new (window.AudioContext || window.webkitAudioContext)();
                                analyser = audioCtx.createAnalyser();
                                analyser.fftSize = 2048;
                                
                                microphone = audioCtx.createMediaStreamSource(stream);
                                microphone.connect(analyser);
                                
                                trackPitch();
                            })
                            .catch(err => {
                                alert("Microphone access is required for pitch estimation. Error: " + err);
                            });
                    }
                }

                function autoCorrelate(buffer, sampleRate) {
                    const SIZE = buffer.length;
                    let rms = 0;

                    for (let i = 0; i < SIZE; i++) {
                        let val = buffer[i];
                        rms += val * val;
                    }
                    rms = Math.sqrt(rms / SIZE);
                    if (rms < 0.01) return -1;

                    let r1 = 0, r2 = SIZE - 1, thres = 0.2;
                    for (let i = 0; i < SIZE / 2; i++) {
                        if (Math.abs(buffer[i]) < thres) { r1 = i; break; }
                    }
                    for (let i = SIZE - 1; i >= SIZE / 2; i--) {
                        if (Math.abs(buffer[i]) < thres) { r2 = i; break; }
                    }
                    
                    const slicedBuffer = buffer.slice(r1, r2);
                    const slicedSize = slicedBuffer.length;

                    const correlations = new Float32Array(slicedSize);
                    for (let i = 0; i < slicedSize; i++) {
                        for (let j = 0; j < slicedSize - i; j++) {
                            correlations[i] += slicedBuffer[j] * slicedBuffer[j + i];
                        }
                    }

                    let d = 0;
                    while (correlations[d] > correlations[d + 1]) d++;
                    let maxval = -1, maxpos = -1;
                    for (let i = d; i < slicedSize; i++) {
                        if (correlations[i] > maxval) {
                            maxval = correlations[i];
                            maxpos = i;
                        }
                    }
                    
                    let T0 = maxpos;
                    if (correlations[T0 - 1] && correlations[T0 + 1]) {
                        const x1 = correlations[T0 - 1], x2 = correlations[T0], x3 = correlations[T0 + 1];
                        const a = (x1 + x3 - 2 * x2) / 2;
                        const b = (x3 - x1) / 2;
                        if (a) T0 = T0 - b / (2 * a);
                    }

                    return sampleRate / T0;
                }

                function trackPitch() {
                    canvas.width = canvas.offsetWidth;
                    canvas.height = canvas.offsetHeight;
                    
                    const buffer = new Float32Array(analyser.fftSize);
                    analyser.getFloatTimeDomainData(buffer);
                    
                    const pitch = autoCorrelate(buffer, audioCtx.sampleRate);
                    
                    if (pitch !== -1 && pitch > 50 && pitch < 1200) {
                        const noteNum = noteFromFrequency(pitch);
                        const noteName = noteNames[noteNum % 12];
                        const octave = Math.floor(noteNum / 12) - 1;
                        
                        document.getElementById('note-text').innerText = noteName + octave;
                        document.getElementById('freq-text').innerText = "Frequency: " + pitch.toFixed(1) + " Hz";
                        
                        frequencies.push(pitch);
                    } else {
                        frequencies.push(null);
                    }

                    if (frequencies.length > 100) {
                        frequencies.shift();
                    }

                    ctx.clearRect(0, 0, canvas.width, canvas.height);
                    ctx.lineWidth = 3;
                    ctx.strokeStyle = '#06b6d4';
                    ctx.lineCap = 'round';
                    ctx.beginPath();

                    const width = canvas.width;
                    const height = canvas.height;
                    const step = width / 100;
                    let lastX = -1, lastY = -1;

                    for (let i = 0; i < frequencies.length; i++) {
                        const freq = frequencies[i];
                        const x = i * step;
                        if (freq !== null) {
                            const logMin = Math.log(80);
                            const logMax = Math.log(600);
                            const val = Math.log(freq);
                            const y = height - ((val - logMin) / (logMax - logMin)) * height;
                            
                            if (lastX === -1) {
                                ctx.moveTo(x, y);
                            } else if (frequencies[i-1] !== null) {
                                ctx.lineTo(x, y);
                            } else {
                                ctx.moveTo(x, y);
                            }
                            lastX = x;
                            lastY = y;
                        }
                    }
                    ctx.stroke();

                    animationId = requestAnimationFrame(trackPitch);
                }
            </script>
        </body>
        </html>
        """
        components.html(pitch_html, height=450)


# ═══════════════════════════ VIEW 15: VIRTUAL PIANO ═══════════════════════════
elif choice == "🎹 Virtual Piano":
    st.markdown("<h2 style='font-size:2rem;font-weight:700;margin-bottom:4px;'>🎹 Virtual Piano Studio</h2>", unsafe_allow_html=True)
    st.markdown("<p style='color:rgba(255,255,255,0.5);margin-bottom:20px;'>Play an interactive browser piano powered by the Web Audio API — click keys, use your keyboard, or strike instant chords.</p>", unsafe_allow_html=True)

    col_pw, col_pr = st.columns([3, 1])
    with col_pw:
        instrument_wave = st.radio("🎛️ Timbre", ["sine", "triangle", "square", "sawtooth"], horizontal=True, key="piano_wave")
    with col_pr:
        reverb_on = st.toggle("🌀 Reverb", value=False, key="piano_reverb")

    piano_html = f"""<!DOCTYPE html><html><head><meta charset="UTF-8">
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Outfit:wght@400;600;700&display=swap');
    *{{box-sizing:border-box;margin:0;padding:0;}}
    body{{background:transparent;font-family:'Outfit',sans-serif;color:#f3f4f6;overflow:hidden;}}
    .wrap{{display:flex;flex-direction:column;align-items:center;padding:16px;gap:16px;}}
    .note-badge{{background:linear-gradient(135deg,rgba(168,85,247,0.2),rgba(244,63,94,0.1));border:1px solid rgba(168,85,247,0.4);border-radius:12px;padding:10px 28px;font-size:1.8rem;font-weight:700;color:#a855f7;min-width:110px;text-align:center;}}
    .piano-row{{display:flex;position:relative;height:180px;touch-action:none;}}
    .wkey{{width:50px;height:180px;background:linear-gradient(180deg,#e8e0ff,#fff);border:1px solid rgba(0,0,0,0.25);border-radius:0 0 8px 8px;cursor:pointer;display:flex;align-items:flex-end;justify-content:center;padding-bottom:8px;font-size:0.58rem;font-weight:600;color:#555;transition:background 0.05s;box-shadow:2px 4px 8px rgba(0,0,0,0.3);user-select:none;}}
    .wkey:hover{{background:linear-gradient(180deg,#d8c0ff,#ece8ff);}}
    .wkey.on{{background:linear-gradient(180deg,#a855f7,#c084fc)!important;color:#fff;box-shadow:0 0 20px rgba(168,85,247,0.5)!important;}}
    .bkey{{width:32px;height:115px;background:linear-gradient(180deg,#1a1a2e,#0b0b1a);border:1px solid rgba(255,255,255,0.08);border-radius:0 0 6px 6px;cursor:pointer;position:absolute;top:0;z-index:2;display:flex;align-items:flex-end;justify-content:center;padding-bottom:5px;font-size:0.52rem;color:rgba(255,255,255,0.3);transition:background 0.05s;box-shadow:2px 6px 12px rgba(0,0,0,0.8);user-select:none;}}
    .bkey:hover{{background:linear-gradient(180deg,#2d1b69,#1a0f42);}}
    .bkey.on{{background:linear-gradient(180deg,#7c3aed,#a855f7)!important;box-shadow:0 0 16px rgba(168,85,247,0.6)!important;}}
    .chord-row{{display:flex;gap:7px;flex-wrap:wrap;justify-content:center;}}
    .cbtn{{background:rgba(244,63,94,0.08);border:1px solid rgba(244,63,94,0.25);border-radius:8px;padding:5px 11px;color:#f43f5e;cursor:pointer;font-family:'Outfit',sans-serif;font-size:0.78rem;transition:all 0.2s;}}
    .cbtn:hover{{background:rgba(244,63,94,0.2);transform:translateY(-2px);}}
    .hint{{font-size:0.62rem;color:rgba(255,255,255,0.22);text-align:center;}}
    </style></head><body>
    <div class="wrap">
      <div style="display:flex;align-items:center;gap:20px;">
        <div class="note-badge" id="nd">—</div>
        <div style="font-size:0.72rem;color:rgba(255,255,255,0.35);line-height:1.6;">Click or tap piano keys<br>Keyboard: A S D F G H J K<br>Black keys: W E T Y U</div>
      </div>
      <div class="piano-row" id="piano"></div>
      <div class="chord-row">
        <button class="cbtn" onclick="chord(['C4','E4','G4'])">C Maj</button>
        <button class="cbtn" onclick="chord(['A3','C4','E4'])">A Min</button>
        <button class="cbtn" onclick="chord(['F3','A3','C4'])">F Maj</button>
        <button class="cbtn" onclick="chord(['G3','B3','D4'])">G Maj</button>
        <button class="cbtn" onclick="chord(['D4','F4','A4'])">D Min</button>
        <button class="cbtn" onclick="chord(['E3','G3','B3'])">E Min</button>
        <button class="cbtn" onclick="chord(['C4','E4','G4','B4'])">Cmaj7</button>
        <button class="cbtn" onclick="chord(['A3','C4','E4','G4'])">Am7</button>
        <button class="cbtn" onclick="chord(['D4','F4','A4','C5'])">Dm7</button>
        <button class="cbtn" onclick="chord(['G3','B3','D4','F4'])">G7</button>
        <button class="cbtn" onclick="chord(['C4','E4','G4','A4'])">C6</button>
        <button class="cbtn" onclick="chord(['B3','D4','F4','A4'])">Bm7b5</button>
      </div>
      <div class="hint">⌨️ Keyboard: A=C · W=C# · S=D · E=D# · D=E · F=F · T=F# · G=G · Y=G# · H=A · U=A# · J=B · K=C5</div>
    </div>
    <script>
    const ctx=new(window.AudioContext||window.webkitAudioContext)();
    const wave='{instrument_wave}';
    const useReverb={'true' if reverb_on else 'false'};
    const active={{}};
    const freqs={{'C':261.63,'C#':277.18,'D':293.66,'D#':311.13,'E':329.63,'F':349.23,'F#':369.99,'G':392.00,'G#':415.30,'A':440.00,'A#':466.16,'B':493.88}};
    let convolver=null;
    if(useReverb){{
      convolver=ctx.createConvolver();
      const len=ctx.sampleRate*2,buf=ctx.createBuffer(2,len,ctx.sampleRate);
      for(let c=0;c<2;c++){{const d=buf.getChannelData(c);for(let i=0;i<len;i++)d[i]=(Math.random()*2-1)*Math.pow(1-i/len,3);}}
      convolver.buffer=buf;convolver.connect(ctx.destination);
    }}
    function getF(n,o){{return freqs[n]*Math.pow(2,o-4);}}
    function play(n,o,el){{
      if(ctx.state==='suspended')ctx.resume();
      const k=n+o;if(active[k])return;
      const osc=ctx.createOscillator(),g=ctx.createGain();
      osc.type=wave;osc.frequency.value=getF(n,o);
      g.gain.setValueAtTime(0,ctx.currentTime);
      g.gain.linearRampToValueAtTime(0.45,ctx.currentTime+0.01);
      osc.connect(g);
      if(useReverb&&convolver){{const d=ctx.createGain();d.gain.value=0.35;g.connect(d);d.connect(convolver);}}
      g.connect(ctx.destination);osc.start();
      active[k]={{osc,g}};
      document.getElementById('nd').innerText=n+o;
      if(el)el.classList.add('on');
    }}
    function stop(n,o,el){{
      const k=n+o;
      if(active[k]){{const {{osc,g}}=active[k];g.gain.linearRampToValueAtTime(0,ctx.currentTime+0.4);osc.stop(ctx.currentTime+0.4);delete active[k];}}
      if(el)el.classList.remove('on');
      if(!Object.keys(active).length)document.getElementById('nd').innerText='—';
    }}
    function chord(notes){{notes.forEach(nk=>{{const n=nk.slice(0,-1),o=parseInt(nk.slice(-1));play(n,o,null);setTimeout(()=>stop(n,o,null),950);}});}}
    const whites=['C','D','E','F','G','A','B'];
    const blacks={{'C':'C#','D':'D#','F':'F#','G':'G#','A':'A#'}};
    const piano=document.getElementById('piano');
    piano.style.cssText='display:flex;position:relative;height:180px;';
    for(let oct=3;oct<5;oct++){{
      const od=document.createElement('div');
      od.style.cssText='position:relative;display:flex;';
      whites.forEach((n,i)=>{{
        const wk=document.createElement('div');
        wk.className='wkey';wk.innerHTML=`<span>${{n}}${{oct}}</span>`;
        wk.addEventListener('mousedown',()=>play(n,oct,wk));
        wk.addEventListener('mouseup',()=>stop(n,oct,wk));
        wk.addEventListener('mouseleave',()=>stop(n,oct,wk));
        wk.addEventListener('touchstart',e=>{{e.preventDefault();play(n,oct,wk);}},{{passive:false}});
        wk.addEventListener('touchend',()=>stop(n,oct,wk));
        od.appendChild(wk);
        if(blacks[n]){{
          const bk=document.createElement('div');
          bk.className='bkey';const bn=blacks[n];
          bk.style.left=(i*50+33)+'px';bk.innerHTML=`<span>${{bn}}</span>`;
          bk.addEventListener('mousedown',e=>{{e.stopPropagation();play(bn,oct,bk);}});
          bk.addEventListener('mouseup',()=>stop(bn,oct,bk));
          bk.addEventListener('mouseleave',()=>stop(bn,oct,bk));
          bk.addEventListener('touchstart',e=>{{e.preventDefault();e.stopPropagation();play(bn,oct,bk);}},{{passive:false}});
          bk.addEventListener('touchend',()=>stop(bn,oct,bk));
          od.appendChild(bk);
        }}
      }});
      piano.appendChild(od);
    }}
    const km={{'a':'C4','w':'C#4','s':'D4','e':'D#4','d':'E4','f':'F4','t':'F#4','g':'G4','y':'G#4','h':'A4','u':'A#4','j':'B4','k':'C5'}};
    document.addEventListener('keydown',e=>{{const nk=km[e.key.toLowerCase()];if(nk&&!e.repeat){{const n=nk.slice(0,-1),o=parseInt(nk.slice(-1));play(n,o,null);}}}});
    document.addEventListener('keyup',e=>{{const nk=km[e.key.toLowerCase()];if(nk){{const n=nk.slice(0,-1),o=parseInt(nk.slice(-1));stop(n,o,null);}}}});
    </script></body></html>"""
    components.html(piano_html, height=430)


# ═══════════════════════════ VIEW 16: LIVE RADIO ═══════════════════════════
elif choice == "📻 Live Radio":
    st.markdown("<h2 style='font-size:2rem;font-weight:700;margin-bottom:4px;'>📻 Live Internet Radio</h2>", unsafe_allow_html=True)
    st.markdown("<p style='color:rgba(255,255,255,0.5);margin-bottom:20px;'>Tune into thousands of live radio stations worldwide via the free <strong>Radio Browser</strong> public API.</p>", unsafe_allow_html=True)

    col_rg, col_rc, col_rs = st.columns([2, 2, 3])
    with col_rg:
        genre_filter = st.selectbox("Genre", ["Top Clicked", "pop", "rock", "jazz", "classical", "electronic", "hiphop", "metal", "country", "reggae", "blues", "ambient", "indie", "rnb", "lofi", "news", "talk"], key="radio_genre")
    with col_rc:
        country_filter = st.selectbox("Country", ["All", "US", "GB", "DE", "FR", "IN", "JP", "BR", "AU", "CA", "IT", "ES", "KR", "MX", "RU", "ZA", "NG", "EG", "AR", "CL"], key="radio_country")
    with col_rs:
        station_search = st.text_input("Search Station Name", placeholder="e.g. BBC, NPR, Jazz FM, KEXP...", key="radio_station_search")

    radio_limit = st.slider("Stations to Load", 6, 48, 18, step=6, key="radio_limit")

    if st.button("📡 Find Live Stations", use_container_width=True, key="radio_find_btn"):
        with st.spinner("Scanning the airwaves..."):
            try:
                base = "https://de1.api.radio-browser.info/json/stations"
                hdr = {"User-Agent": "MelodifyAI/1.0"}
                if station_search.strip():
                    url_r = f"{base}/byname/{requests.utils.quote(station_search.strip())}?limit={radio_limit}&hidebroken=true&order=clickcount&reverse=true"
                elif genre_filter == "Top Clicked" and country_filter != "All":
                    url_r = f"{base}/bycountrycode/{country_filter}?limit={radio_limit}&hidebroken=true&order=clickcount&reverse=true"
                elif genre_filter == "Top Clicked":
                    url_r = f"{base}/topclick/{radio_limit}?hidebroken=true"
                else:
                    url_r = f"{base}/bytag/{genre_filter}?limit={radio_limit}&hidebroken=true&order=clickcount&reverse=true"
                resp = requests.get(url_r, timeout=12, headers=hdr)
                if resp.status_code == 200:
                    st.session_state.radio_stations = resp.json()
                    st.toast(f"✅ Found {len(st.session_state.radio_stations)} stations!")
                else:
                    st.error("Radio Browser API returned an error. Try again.")
            except Exception as ex:
                st.error(f"Network error: {ex}")

    stations = st.session_state.get("radio_stations", [])
    if stations:
        st.markdown(f"<p style='color:rgba(255,255,255,0.4);font-size:0.8rem;margin:4px 0 16px 0;'>🎙️ {len(stations)} stations — click ▶ to tune in live</p>", unsafe_allow_html=True)
        rcols = st.columns(3)
        for i, s in enumerate(stations):
            with rcols[i % 3]:
                name = (s.get("name") or "Unknown")[:30]
                cc = s.get("countrycode", "")
                tags = (s.get("tags") or "")[:35]
                bitrate = s.get("bitrate", 0)
                clicks = s.get("clickcount", 0)
                url_stream = s.get("url_resolved") or s.get("url", "")
                favicon = s.get("favicon", "")
                fav_tag = f'<img src="{favicon}" style="width:32px;height:32px;border-radius:6px;object-fit:cover;" onerror="this.style.display=\'none\'">' if favicon else "📻"
                st.markdown(f"""
                <div style="background:rgba(15,23,42,0.5);border:1px solid rgba(255,255,255,0.06);border-radius:14px;padding:12px;margin-bottom:4px;">
                    <div style="display:flex;align-items:center;gap:10px;margin-bottom:8px;">
                        <div style="flex-shrink:0;">{fav_tag}</div>
                        <div style="overflow:hidden;flex:1;">
                            <p style="font-weight:700;font-size:0.82rem;margin:0;color:#fff;white-space:nowrap;overflow:hidden;text-overflow:ellipsis;">{name}</p>
                            <p style="font-size:0.66rem;color:rgba(255,255,255,0.4);margin:0;">{cc} · {tags or 'Various'}</p>
                        </div>
                    </div>
                    <div style="display:flex;gap:6px;margin-bottom:8px;">
                        <span style="background:rgba(168,85,247,0.1);border:1px solid rgba(168,85,247,0.2);border-radius:5px;padding:2px 7px;font-size:0.6rem;color:#a855f7;">{bitrate}kbps</span>
                        <span style="background:rgba(6,182,212,0.1);border:1px solid rgba(6,182,212,0.2);border-radius:5px;padding:2px 7px;font-size:0.6rem;color:#06b6d4;">👂 {clicks}</span>
                    </div>
                </div>
                """, unsafe_allow_html=True)
                if url_stream:
                    components.html(f'<audio controls style="width:100%;height:38px;border-radius:8px;margin-bottom:10px;" preload="none"><source src="{url_stream}"></audio>', height=42)
    else:
        st.markdown("""
        <div style="text-align:center;padding:60px 20px;color:rgba(255,255,255,0.25);">
            <div style="font-size:4rem;margin-bottom:16px;">📡</div>
            <p style="font-size:1rem;">Click <strong>Find Live Stations</strong> to browse global radio.</p>
            <p style="font-size:0.85rem;">Powered by the free Radio Browser open API.</p>
        </div>
        """, unsafe_allow_html=True)


# ═══════════════════════════ VIEW 17: MUSIC TRIVIA ═══════════════════════════
elif choice == "🏆 Music Trivia":
    st.markdown("<h2 style='font-size:2rem;font-weight:700;margin-bottom:4px;'>🏆 AI Music Trivia Quiz</h2>", unsafe_allow_html=True)
    st.markdown("<p style='color:rgba(255,255,255,0.5);margin-bottom:20px;'>Test your music knowledge with AI-generated trivia. 10 rounds of multiple-choice challenges!</p>", unsafe_allow_html=True)

    if not st.session_state.gemini_key:
        st.warning("Please provide a Gemini API Key in the sidebar to play Music Trivia!")
    else:
        col_td, col_tt = st.columns(2)
        with col_td:
            difficulty = st.select_slider("Difficulty", ["Easy", "Medium", "Hard", "Expert"], value="Medium", key="trivia_diff")
        with col_tt:
            topic = st.selectbox("Topic", ["General Music", "Rock & Metal", "Pop Icons", "Hip-Hop & Rap", "Jazz & Blues", "Classical Composers", "Electronic & EDM", "90s & 2000s Nostalgia", "Music Theory", "Music History", "One-Hit Wonders", "Grammy Winners"], key="trivia_topic")

        if st.button("🎲 Generate New Quiz (10 Questions)", use_container_width=True, key="trivia_gen_btn"):
            with st.spinner("AI is crafting your trivia quiz..."):
                url_g = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-2.5-flash:generateContent?key={st.session_state.gemini_key}"
                prompt = f"""Generate exactly 10 music trivia questions about '{topic}' at '{difficulty}' difficulty.
Return ONLY a valid JSON array (no markdown fences, no extra text):
[{{"q":"Question text","options":["A) opt","B) opt","C) opt","D) opt"],"answer":"A) correct","fact":"Short fun fact"}}]
Make all questions unique and educational. Exactly one correct answer per question."""
                try:
                    res = requests.post(url_g, json={{"contents":[{{"parts":[{{"text":prompt}}]}}]}}, headers={{"Content-Type":"application/json"}}, timeout=25)
                    if res.status_code == 200:
                        raw = res.json()['candidates'][0]['content']['parts'][0]['text'].strip()
                        raw = re.sub(r'^```json\s*', '', raw)
                        raw = re.sub(r'\s*```$', '', raw)
                        qs = json.loads(raw)
                        st.session_state.trivia_questions = qs
                        st.session_state.trivia_score = 0
                        st.session_state.trivia_current = 0
                        st.session_state.trivia_answered = False
                        st.session_state.trivia_selected = None
                        st.toast("Quiz ready! Let's go! 🎵")
                        st.rerun()
                except Exception as ex:
                    st.error(f"Error generating quiz: {ex}")

        questions = st.session_state.get("trivia_questions", [])
        current = st.session_state.get("trivia_current", 0)
        score = st.session_state.get("trivia_score", 0)

        if questions:
            if current < len(questions):
                q = questions[current]
                pct_prog = int((current / len(questions)) * 100)
                st.markdown(f"""
                <div style="background:rgba(255,255,255,0.06);border-radius:100px;height:6px;margin-bottom:16px;overflow:hidden;">
                    <div style="background:linear-gradient(90deg,#a855f7,#f43f5e);height:100%;width:{pct_prog}%;border-radius:100px;"></div>
                </div>
                <div style="display:flex;justify-content:space-between;margin-bottom:16px;">
                    <span style="color:rgba(255,255,255,0.5);font-size:0.85rem;">Question {current+1} of {len(questions)}</span>
                    <span style="color:#a855f7;font-weight:700;font-size:0.85rem;">⭐ Score: {score}/{current}</span>
                </div>
                """, unsafe_allow_html=True)
                st.markdown(f"<div style='background:rgba(15,23,42,0.5);border:1px solid rgba(255,255,255,0.08);border-radius:16px;padding:20px;margin-bottom:16px;'><p style='font-size:1.05rem;font-weight:600;color:#fff;margin:0;'>{q['q']}</p></div>", unsafe_allow_html=True)
                answered = st.session_state.get("trivia_answered", False)
                selected = st.session_state.get("trivia_selected", None)
                for opt in q.get("options", []):
                    if st.button(opt, key=f"trivia_opt_{current}_{opt}", use_container_width=True, disabled=answered):
                        st.session_state.trivia_selected = opt
                        st.session_state.trivia_answered = True
                        if opt == q["answer"]:
                            st.session_state.trivia_score += 1
                            st.toast("✅ Correct!")
                        else:
                            st.toast(f"❌ Wrong! Answer: {q['answer']}")
                        st.rerun()
                    if answered and opt == q["answer"]:
                        st.markdown(f"<p style='color:#22c55e;font-size:0.8rem;margin-top:-8px;margin-bottom:4px;'>✅ Correct answer</p>", unsafe_allow_html=True)
                    elif answered and opt == selected and opt != q["answer"]:
                        st.markdown(f"<p style='color:#f43f5e;font-size:0.8rem;margin-top:-8px;margin-bottom:4px;'>❌ Your answer</p>", unsafe_allow_html=True)
                if answered:
                    st.info(f"💡 Fun Fact: {q.get('fact','')}")
                    if st.button("➡️ Next Question", use_container_width=True, key="trivia_next_btn"):
                        st.session_state.trivia_current += 1
                        st.session_state.trivia_answered = False
                        st.session_state.trivia_selected = None
                        st.rerun()
            else:
                final_score = st.session_state.trivia_score
                total = len(questions)
                pct = int((final_score / total) * 100)
                grade = "🏆 Music Genius!" if pct >= 90 else "⭐ Music Expert!" if pct >= 70 else "🎵 Getting There!" if pct >= 50 else "🎸 Keep Practicing!"
                st.markdown(f"""
                <div style="text-align:center;padding:40px;background:linear-gradient(135deg,rgba(168,85,247,0.1),rgba(244,63,94,0.08));border:1px solid rgba(168,85,247,0.2);border-radius:24px;margin:20px 0;">
                    <div style="font-size:4rem;margin-bottom:12px;">{grade.split()[0]}</div>
                    <h2 style="font-size:1.8rem;font-weight:700;margin:0 0 8px 0;color:#fff;">{grade}</h2>
                    <p style="font-size:1.1rem;color:rgba(255,255,255,0.6);margin-bottom:16px;">You scored {final_score} out of {total} ({pct}%)</p>
                    <div style="background:rgba(255,255,255,0.06);border-radius:100px;height:10px;width:80%;margin:0 auto;">
                        <div style="background:linear-gradient(90deg,#a855f7,#f43f5e);height:100%;width:{pct}%;border-radius:100px;"></div>
                    </div>
                </div>
                """, unsafe_allow_html=True)
                if st.button("🔄 Play Again", use_container_width=True, key="trivia_restart"):
                    st.session_state.trivia_questions = []
                    st.session_state.trivia_score = 0
                    st.session_state.trivia_current = 0
                    st.rerun()


# ═══════════════════════════ VIEW 18: WORLD MUSIC EXPLORER ═══════════════════════════
elif choice == "🌍 World Music":
    st.markdown("<h2 style='font-size:2rem;font-weight:700;margin-bottom:4px;'>🌍 World Music Explorer</h2>", unsafe_allow_html=True)
    st.markdown("<p style='color:rgba(255,255,255,0.5);margin-bottom:20px;'>Discover traditional instruments, legendary artists, iconic songs, and the soul of music from every corner of the globe.</p>", unsafe_allow_html=True)

    countries_list = [
        "🇺🇸 United States", "🇬🇧 United Kingdom", "🇯🇵 Japan", "🇧🇷 Brazil", "🇮🇳 India",
        "🇨🇴 Colombia", "🇨🇺 Cuba", "🇳🇬 Nigeria", "🇿🇦 South Africa", "🇸🇳 Senegal",
        "🇦🇺 Australia", "🇩🇪 Germany", "🇫🇷 France", "🇮🇹 Italy", "🇪🇸 Spain",
        "🇲🇽 Mexico", "🇦🇷 Argentina", "🇰🇷 South Korea", "🇵🇹 Portugal", "🇹🇷 Turkey",
        "🇬🇷 Greece", "🇮🇷 Iran", "🇪🇬 Egypt", "🇨🇳 China", "🇷🇺 Russia",
        "🇯🇲 Jamaica", "🇮🇪 Ireland", "🇳🇴 Norway", "🇸🇪 Sweden", "🇨🇱 Chile",
        "🇪🇹 Ethiopia", "🇬🇭 Ghana", "🇵🇰 Pakistan", "🇺🇦 Ukraine", "🇻🇳 Vietnam"
    ]

    col_wc, col_wf = st.columns(2)
    with col_wc:
        selected_country = st.selectbox("🌐 Select Country / Region", countries_list, key="world_music_country")
    with col_wf:
        focus_area = st.selectbox("Focus Area", ["Everything", "Traditional Music & Instruments", "Modern Pop Scene", "Underground & Indie", "Folk & Heritage", "Dance & Rhythms", "Music History"], key="world_music_focus")

    if st.button("🌍 Explore Music Culture", use_container_width=True, key="world_music_btn"):
        if not st.session_state.gemini_key:
            st.warning("Please provide a Gemini API Key in the sidebar.")
        else:
            with st.spinner(f"Researching music from {selected_country}..."):
                url_g = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-2.5-flash:generateContent?key={st.session_state.gemini_key}"
                prompt = f"""You are a world music ethnomusicologist and cultural expert.
Create a comprehensive music guide for: {selected_country} | Focus: {focus_area}
Return ONLY a valid JSON object (no markdown fences):
{{"country":"Name","tagline":"Evocative sentence","genres":["g1","g2","g3","g4","g5"],"instruments":[{{"name":"Instr","description":"desc"}},...3],"artists":[{{"name":"Artist","genre":"Genre","era":"Era","fact":"fact"}},...5],"songs":[{{"title":"Song","artist":"Artist","year":"Year","why":"Iconic reason"}},...4],"cultural_note":"Paragraph about music in daily life","fun_fact":"Surprising music fact"}}"""
                try:
                    res = requests.post(url_g, json={{"contents":[{{"parts":[{{"text":prompt}}]}}]}}, headers={{"Content-Type":"application/json"}}, timeout=25)
                    if res.status_code == 200:
                        raw = res.json()['candidates'][0]['content']['parts'][0]['text'].strip()
                        raw = re.sub(r'^```json\s*', '', raw)
                        raw = re.sub(r'\s*```$', '', raw)
                        st.session_state.world_music_data = json.loads(raw)
                        st.rerun()
                except Exception as ex:
                    st.error(f"Error: {ex}")

    wmd = st.session_state.get("world_music_data")
    if wmd:
        st.markdown(f"""
        <div style="background:linear-gradient(135deg,rgba(168,85,247,0.08),rgba(6,182,212,0.05));border:1px solid rgba(168,85,247,0.15);border-radius:20px;padding:22px;margin-bottom:22px;">
            <h3 style="font-size:1.5rem;font-weight:700;color:#fff;margin:0 0 4px 0;">{wmd.get('country','')}</h3>
            <p style="color:rgba(255,255,255,0.5);font-style:italic;margin:0 0 14px 0;">{wmd.get('tagline','')}</p>
            <div style="display:flex;flex-wrap:wrap;gap:8px;">{''.join(f"<span style='background:rgba(168,85,247,0.1);border:1px solid rgba(168,85,247,0.25);border-radius:20px;padding:4px 12px;font-size:0.78rem;color:#a855f7;'>{g}</span>" for g in wmd.get('genres',[]))}</div>
        </div>
        """, unsafe_allow_html=True)
        col_wi, col_wa = st.columns(2)
        with col_wi:
            st.markdown("#### 🎺 Iconic Instruments")
            for inst in wmd.get("instruments", []):
                st.markdown(f"<div style='background:rgba(15,23,42,0.4);border:1px solid rgba(255,255,255,0.06);border-radius:12px;padding:12px;margin-bottom:8px;'><p style='font-weight:700;color:#06b6d4;margin:0 0 4px 0;'>{inst.get('name','')}</p><p style='font-size:0.8rem;color:rgba(255,255,255,0.5);margin:0;'>{inst.get('description','')}</p></div>", unsafe_allow_html=True)
        with col_wa:
            st.markdown("#### 🎤 Legendary Artists")
            for art in wmd.get("artists", []):
                st.markdown(f"<div style='background:rgba(15,23,42,0.4);border:1px solid rgba(255,255,255,0.06);border-radius:12px;padding:12px;margin-bottom:8px;'><p style='font-weight:700;color:#f43f5e;margin:0 0 2px 0;'>{art.get('name','')} <span style='font-size:0.7rem;color:rgba(255,255,255,0.3);'>({art.get('era','')})</span></p><p style='font-size:0.72rem;color:#a855f7;margin:0 0 4px 0;'>{art.get('genre','')}</p><p style='font-size:0.78rem;color:rgba(255,255,255,0.5);margin:0;'>{art.get('fact','')}</p></div>", unsafe_allow_html=True)
        st.markdown("#### 🎵 Must-Listen Songs")
        scols = st.columns(2)
        for si, sg in enumerate(wmd.get("songs", [])):
            with scols[si % 2]:
                st.markdown(f"<div style='background:rgba(15,23,42,0.4);border:1px solid rgba(255,255,255,0.06);border-radius:12px;padding:14px;margin-bottom:8px;'><p style='font-weight:700;color:#fff;margin:0 0 2px 0;'>🎵 {sg.get('title','')}</p><p style='font-size:0.72rem;color:rgba(255,255,255,0.5);margin:0 0 6px 0;'>{sg.get('artist','')} · {sg.get('year','')}</p><p style='font-size:0.8rem;color:rgba(255,255,255,0.6);margin:0;'>{sg.get('why','')}</p></div>", unsafe_allow_html=True)
        st.markdown(f"<div style='background:rgba(6,182,212,0.05);border:1px solid rgba(6,182,212,0.15);border-radius:14px;padding:16px;margin-top:8px;'><p style='font-size:0.85rem;color:rgba(255,255,255,0.65);margin:0 0 8px 0;'>🎭 <strong>Cultural Note</strong></p><p style='font-size:0.88rem;color:rgba(255,255,255,0.7);margin:0;'>{wmd.get('cultural_note','')}</p></div>", unsafe_allow_html=True)
        st.markdown(f"<div style='background:rgba(244,63,94,0.05);border:1px solid rgba(244,63,94,0.15);border-radius:14px;padding:14px;margin-top:10px;'><p style='font-size:0.85rem;color:#f43f5e;margin:0;'>💡 <strong>Fun Fact:</strong> {wmd.get('fun_fact','')}</p></div>", unsafe_allow_html=True)
        if st.button("🔍 Search This Country's Music on Melodify", use_container_width=True, key="world_music_search"):
            country_name = wmd.get("country", selected_country)
            results = yt.search_songs(f"traditional music from {country_name}", max_results=5)
            if results:
                st.session_state.search_results = results
                st.toast(f"Found music from {country_name}!")
                st.rerun()
    else:
        st.markdown("""
        <div style="text-align:center;padding:60px 20px;color:rgba(255,255,255,0.25);">
            <div style="font-size:4rem;margin-bottom:16px;">🌏</div>
            <p style="font-size:1rem;">Select a country and click <strong>Explore Music Culture</strong></p>
        </div>
        """, unsafe_allow_html=True)


# ═══════════════════════════ VIEW 19: SONG JOURNAL ═══════════════════════════
elif choice == "📝 Song Journal":
    st.markdown("<h2 style='font-size:2rem;font-weight:700;margin-bottom:4px;'>📝 Music Journal</h2>", unsafe_allow_html=True)
    st.markdown("<p style='color:rgba(255,255,255,0.5);margin-bottom:20px;'>Write personal notes, memories, and feelings about songs. Your private music diary.</p>", unsafe_allow_html=True)

    with st.expander("✏️ Write New Journal Entry", expanded=not bool(st.session_state.get("journal_entries", []))):
        col_jt, col_jm = st.columns([3, 1])
        with col_jt:
            default_song_j = f"{st.session_state.current_song['title']} — {st.session_state.current_song['uploader']}" if st.session_state.current_song else ""
            journal_song = st.text_input("Song / Artist", value=default_song_j, placeholder="Which song is this about?", key="journal_song_input")
        with col_jm:
            journal_mood = st.selectbox("Mood 🎭", ["😊 Happy", "😢 Sad", "🔥 Energized", "😌 Peaceful", "😤 Angry", "🥺 Nostalgic", "😍 In Love", "🤔 Thoughtful", "💃 Dancey", "😴 Sleepy"], key="journal_mood_select")
        journal_text = st.text_area("Your Thoughts & Memories", placeholder="What does this song make you think or feel? A memory it reminds you of?", height=120, key="journal_text_input")
        journal_tags = st.text_input("Tags (comma separated)", placeholder="e.g. rainy day, childhood, road trip", key="journal_tags_input")
        if st.button("💾 Save Journal Entry", use_container_width=True, key="journal_save_btn"):
            if journal_song.strip() and journal_text.strip():
                entry = {
                    "id": int(time.time()),
                    "song": journal_song.strip(),
                    "mood": journal_mood,
                    "text": journal_text.strip(),
                    "tags": [t.strip() for t in journal_tags.split(",") if t.strip()],
                    "timestamp": datetime.now().strftime("%B %d, %Y at %I:%M %p"),
                    "youtube_id": st.session_state.current_song['id'] if st.session_state.current_song else None
                }
                if "journal_entries" not in st.session_state:
                    st.session_state.journal_entries = []
                st.session_state.journal_entries.insert(0, entry)
                st.toast("📝 Journal entry saved!")
                st.rerun()
            else:
                st.warning("Please fill in both the song name and your thoughts.")

    entries = st.session_state.get("journal_entries", [])
    if entries:
        moods_available = list(set(e["mood"] for e in entries))
        filter_mood = st.selectbox("Filter by Mood", ["All Moods"] + moods_available, key="journal_filter_mood")
        filtered = entries if filter_mood == "All Moods" else [e for e in entries if e["mood"] == filter_mood]
        st.markdown(f"<p style='color:rgba(255,255,255,0.4);font-size:0.8rem;margin:8px 0 16px 0;'>{len(filtered)} entr{'y' if len(filtered)==1 else 'ies'}</p>", unsafe_allow_html=True)
        for entry in filtered:
            tags_html = "".join(f"<span style='background:rgba(168,85,247,0.1);border:1px solid rgba(168,85,247,0.2);border-radius:20px;padding:2px 8px;font-size:0.63rem;color:#a855f7;margin-right:4px;'>#{t}</span>" for t in entry.get("tags", []))
            st.markdown(f"""
            <div style="background:rgba(15,23,42,0.5);border:1px solid rgba(255,255,255,0.06);border-radius:16px;padding:18px;margin-bottom:12px;">
                <div style="display:flex;justify-content:space-between;align-items:flex-start;margin-bottom:10px;">
                    <div><p style="font-weight:700;font-size:0.95rem;color:#fff;margin:0 0 2px 0;">🎵 {entry['song']}</p><p style="font-size:0.7rem;color:rgba(255,255,255,0.35);margin:0;">{entry['timestamp']}</p></div>
                    <span style="font-size:1.3rem;">{entry['mood'].split()[0]}</span>
                </div>
                <p style="font-size:0.88rem;color:rgba(255,255,255,0.7);line-height:1.6;margin:0 0 10px 0;">{entry['text']}</p>
                <div style="display:flex;flex-wrap:wrap;gap:4px;">{tags_html}</div>
            </div>
            """, unsafe_allow_html=True)
            if st.button("🗑️ Delete", key=f"journal_del_{entry['id']}"):
                st.session_state.journal_entries = [e for e in st.session_state.journal_entries if e["id"] != entry["id"]]
                st.rerun()
    else:
        st.markdown("""
        <div style="text-align:center;padding:60px 20px;color:rgba(255,255,255,0.25);">
            <div style="font-size:4rem;margin-bottom:16px;">📖</div>
            <p>Your music journal is empty. Write your first entry above!</p>
        </div>
        """, unsafe_allow_html=True)


# ═══════════════════════════ VIEW 20: MOOD BOARD ═══════════════════════════
elif choice == "🎭 Mood Board":
    st.markdown("<h2 style='font-size:2rem;font-weight:700;margin-bottom:4px;'>🎭 AI Mood Board Creator</h2>", unsafe_allow_html=True)
    st.markdown("<p style='color:rgba(255,255,255,0.5);margin-bottom:20px;'>Transform any song into a stunning visual mood board — colors, textures, aesthetic words, and cinematic imagery.</p>", unsafe_allow_html=True)

    col_mb1, col_mb2 = st.columns([3, 2])
    with col_mb1:
        default_mb = f"{st.session_state.current_song['title']} by {st.session_state.current_song['uploader']}" if st.session_state.current_song else ""
        mb_song = st.text_input("Song or Vibe", value=default_mb, placeholder="e.g. Bohemian Rhapsody by Queen", key="moodboard_song")
    with col_mb2:
        mb_style = st.selectbox("Visual Style", ["Cinematic", "Abstract", "Vintage", "Neon Cyberpunk", "Cottagecore", "Dark Academia", "Vaporwave", "Minimalist", "Impressionist", "Surrealist"], key="moodboard_style")

    if st.button("🎨 Generate Mood Board", use_container_width=True, key="moodboard_gen_btn"):
        if not st.session_state.gemini_key:
            st.warning("Please provide a Gemini API Key in the sidebar.")
        elif not mb_song.strip():
            st.warning("Please enter a song or vibe.")
        else:
            with st.spinner("AI is painting your mood board..."):
                url_g = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-2.5-flash:generateContent?key={st.session_state.gemini_key}"
                prompt = f"""You are a synesthesia artist and creative director. Create a mood board for: "{mb_song}" in "{mb_style}" style.
Return ONLY a valid JSON object (no markdown fences):
{{"title":"Board title","palette":[{{"hex":"#hex","name":"Color name","feeling":"What it evokes"}},...5],"textures":["desc1","desc2","desc3"],"words":["w1","w2","w3","w4","w5","w6","w7","w8","w9","w10"],"imagery":["scene1","scene2","scene3","scene4"],"time_of_day":"Best time","season":"Best season","setting":"Ideal environment","emotion_arc":"How emotion evolves","similar_vibes":["Artist/Song 1","Artist/Song 2","Artist/Song 3"]}}"""
                try:
                    res = requests.post(url_g, json={{"contents":[{{"parts":[{{"text":prompt}}]}}]}}, headers={{"Content-Type":"application/json"}}, timeout=22)
                    if res.status_code == 200:
                        raw = res.json()['candidates'][0]['content']['parts'][0]['text'].strip()
                        raw = re.sub(r'^```json\s*', '', raw)
                        raw = re.sub(r'\s*```$', '', raw)
                        st.session_state.mood_board_result = json.loads(raw)
                        st.rerun()
                except Exception as ex:
                    st.error(f"Error: {ex}")

    mb = st.session_state.get("mood_board_result")
    if mb:
        st.markdown(f"<h3 style='font-size:1.4rem;font-weight:700;color:#fff;margin-bottom:20px;'>{mb.get('title','')}</h3>", unsafe_allow_html=True)
        st.markdown("#### 🎨 Color Palette")
        pal_html = "<div style='display:flex;gap:14px;flex-wrap:wrap;margin-bottom:22px;'>"
        for c in mb.get("palette", []):
            hx = c.get('hex','#333')
            pal_html += f"<div style='text-align:center;'><div style='width:68px;height:68px;border-radius:14px;background:{hx};box-shadow:0 4px 16px {hx}55;margin-bottom:6px;'></div><p style='font-size:0.63rem;color:rgba(255,255,255,0.5);margin:0;'>{c.get('name','')}</p><p style='font-size:0.6rem;color:rgba(255,255,255,0.3);margin:0;'>{hx}</p><p style='font-size:0.6rem;color:rgba(255,255,255,0.4);margin:0;font-style:italic;'>{c.get('feeling','')}</p></div>"
        pal_html += "</div>"
        st.markdown(pal_html, unsafe_allow_html=True)
        st.markdown("#### 💬 Mood Words")
        sizes = ["0.8rem","0.95rem","1.1rem","0.85rem","1rem","0.9rem","1.05rem","0.82rem","0.98rem","1.02rem"]
        words_html = "<div style='display:flex;flex-wrap:wrap;gap:8px;margin-bottom:20px;'>"
        for i, w in enumerate(mb.get("words", [])):
            words_html += f"<span style='font-size:{sizes[i%len(sizes)]};font-weight:600;color:rgba(168,85,247,0.9);background:rgba(168,85,247,0.07);border:1px solid rgba(168,85,247,0.15);border-radius:20px;padding:5px 14px;'>{w}</span>"
        words_html += "</div>"
        st.markdown(words_html, unsafe_allow_html=True)
        col_img, col_meta = st.columns(2)
        with col_img:
            st.markdown("#### 🖼️ Visual Imagery")
            for img in mb.get("imagery", []):
                st.markdown(f"<div style='background:rgba(15,23,42,0.4);border:1px solid rgba(255,255,255,0.06);border-radius:10px;padding:10px;margin-bottom:8px;font-size:0.83rem;color:rgba(255,255,255,0.7);'>🎬 {img}</div>", unsafe_allow_html=True)
        with col_meta:
            st.markdown("#### 📍 Context")
            for icon, label, val in [("🕐","Time of Day",mb.get('time_of_day','')), ("🍂","Season",mb.get('season','')), ("🌍","Setting",mb.get('setting',''))]:
                st.markdown(f"<div style='background:rgba(15,23,42,0.4);border:1px solid rgba(255,255,255,0.06);border-radius:10px;padding:10px;margin-bottom:8px;'><p style='font-size:0.68rem;color:rgba(255,255,255,0.35);margin:0;'>{icon} {label}</p><p style='font-size:0.83rem;color:#fff;margin:0;font-weight:600;'>{val}</p></div>", unsafe_allow_html=True)
        st.markdown(f"<div style='background:rgba(244,63,94,0.05);border:1px solid rgba(244,63,94,0.15);border-radius:12px;padding:14px;margin-top:4px;'><p style='font-size:0.72rem;color:#f43f5e;margin:0 0 4px 0;'>🌊 Emotion Arc</p><p style='font-size:0.85rem;color:rgba(255,255,255,0.7);margin:0;'>{mb.get('emotion_arc','')}</p></div>", unsafe_allow_html=True)
        st.markdown("#### 🔗 Similar Vibes")
        sv_html = "<div style='display:flex;flex-wrap:wrap;gap:8px;margin-top:8px;'>"
        for sv in mb.get("similar_vibes", []):
            sv_html += f"<span style='background:rgba(6,182,212,0.08);border:1px solid rgba(6,182,212,0.2);border-radius:20px;padding:5px 14px;font-size:0.8rem;color:#06b6d4;'>🎵 {sv}</span>"
        sv_html += "</div>"
        st.markdown(sv_html, unsafe_allow_html=True)
    else:
        st.markdown("""
        <div style="text-align:center;padding:60px 20px;color:rgba(255,255,255,0.25);">
            <div style="font-size:4rem;margin-bottom:16px;">🎨</div>
            <p>Enter a song and click <strong>Generate Mood Board</strong> to visualize its vibe.</p>
        </div>
        """, unsafe_allow_html=True)


# ═══════════════════════════ VIEW 21: KARAOKE STUDIO ═══════════════════════════
elif choice == "🎯 Karaoke Studio":
    st.markdown("<h2 style='font-size:2rem;font-weight:700;margin-bottom:4px;'>🎯 Karaoke Studio</h2>", unsafe_allow_html=True)
    st.markdown("<p style='color:rgba(255,255,255,0.5);margin-bottom:20px;'>Sing along with large, auto-highlighted lyrics. Load a song with synced lyrics from AI Lyrics Syncer first.</p>", unsafe_allow_html=True)

    if not st.session_state.current_song:
        st.info("🎵 Play a song first to enter Karaoke Studio!")
    elif not st.session_state.synced_lyrics and not st.session_state.plain_lyrics:
        st.warning("⚠️ No lyrics loaded. Go to **AI Lyrics Syncer** to load lyrics for this song.")
    else:
        song = st.session_state.current_song
        col_kt, col_kf = st.columns([3, 1])
        with col_kt:
            theme = st.radio("Theme", ["🌌 Dark Galaxy", "🌸 Neon Pink", "🌊 Ocean Blue", "🔥 Fire", "💚 Matrix"], horizontal=True, key="karaoke_theme")
        with col_kf:
            font_size = st.slider("Font Size", 14, 38, 22, key="karaoke_font")
        themes_map = {
            "🌌 Dark Galaxy": {"bg": "#060810", "active": "#a855f7", "inactive": "rgba(255,255,255,0.22)", "glow": "rgba(168,85,247,0.45)"},
            "🌸 Neon Pink":   {"bg": "#0d0010", "active": "#f43f5e", "inactive": "rgba(255,255,255,0.25)", "glow": "rgba(244,63,94,0.45)"},
            "🌊 Ocean Blue":  {"bg": "#000d1a", "active": "#06b6d4", "inactive": "rgba(255,255,255,0.25)", "glow": "rgba(6,182,212,0.45)"},
            "🔥 Fire":        {"bg": "#0a0500", "active": "#f97316", "inactive": "rgba(255,255,255,0.25)", "glow": "rgba(249,115,22,0.45)"},
            "💚 Matrix":      {"bg": "#000a00", "active": "#22c55e", "inactive": "rgba(255,255,255,0.2)",  "glow": "rgba(34,197,94,0.45)"},
        }
        t = themes_map.get(theme, themes_map["🌌 Dark Galaxy"])
        # Use synced or plain lyrics
        if st.session_state.synced_lyrics:
            lyrics_data = st.session_state.synced_lyrics
            lyrics_json = json.dumps(lyrics_data)
            use_synced = True
        else:
            plain_lines = [l.strip() for l in st.session_state.plain_lyrics.split('\n') if l.strip()]
            lyrics_data = [{"time": i * 3.5, "text": l} for i, l in enumerate(plain_lines)]
            lyrics_json = json.dumps(lyrics_data)
            use_synced = False
        karaoke_html = f"""<!DOCTYPE html><html><head><meta charset="UTF-8">
        <style>
        @import url('https://fonts.googleapis.com/css2?family=Outfit:wght@400;700;900&display=swap');
        *{{box-sizing:border-box;margin:0;padding:0;}}
        body{{background:{t['bg']};font-family:'Outfit',sans-serif;overflow:hidden;height:480px;}}
        #stage{{height:480px;display:flex;flex-direction:column;align-items:center;justify-content:center;padding:20px;overflow:hidden;position:relative;}}
        .lyric-line{{font-size:{font_size}px;text-align:center;padding:10px 20px;transition:all 0.4s cubic-bezier(0.4,0,0.2,1);opacity:0.28;transform:scale(0.88);color:{t['inactive']};white-space:pre-wrap;max-width:90%;}}
        .lyric-line.active{{opacity:1;transform:scale(1.06);color:{t['active']};text-shadow:0 0 20px {t['glow']},0 0 40px {t['glow']};font-weight:900;}}
        .lyric-line.prev{{opacity:0.5;transform:scale(0.95);}}
        .lyric-line.next{{opacity:0.45;transform:scale(0.92);}}
        #time-bar{{position:absolute;bottom:0;left:0;height:3px;background:linear-gradient(90deg,{t['active']},{t['glow']});width:0%;transition:width 0.25s linear;border-radius:0 3px 3px 0;}}
        #song-info{{position:absolute;top:12px;left:0;right:0;text-align:center;font-size:0.68rem;color:rgba(255,255,255,0.28);letter-spacing:0.12em;text-transform:uppercase;}}
        #line-counter{{position:absolute;bottom:10px;right:16px;font-size:0.65rem;color:rgba(255,255,255,0.2);}}
        </style></head><body>
        <div id="stage">
          <div id="song-info">{song['title'][:40]} — {song['uploader']}</div>
          <div id="lc" style="display:flex;flex-direction:column;align-items:center;gap:2px;"></div>
          <div id="time-bar"></div>
          <div id="line-counter"></div>
        </div>
        <script>
        const lyrics={lyrics_json};
        const lc=document.getElementById('lc');
        const tb=document.getElementById('time-bar');
        const lineC=document.getElementById('line-counter');
        let curIdx=-1;
        
        function render(idx){{
          lc.innerHTML='';
          for(let i=idx-1;i<=idx+3;i++){{
            if(i<0||i>=lyrics.length)continue;
            const el=document.createElement('div');
            el.className='lyric-line'+(i===idx?' active':i===idx-1?' prev':i===idx+1?' next':'');
            el.innerText=lyrics[i].text||'';
            lc.appendChild(el);
          }}
          lineC.innerText=(idx+1)+'/'+lyrics.length;
        }}
        
        function getPlaybackTime(){{
          try {{
            const v = localStorage.getItem('melodify_playback_time');
            return v !== null ? parseFloat(v) : -1;
          }} catch(e) {{ return -1; }}
        }}
        
        function tick(){{
          const now = getPlaybackTime();
          if(now < 0) return;
          let idx=-1;
          for(let i=0;i<lyrics.length;i++){{
            if(lyrics[i].time<=now)idx=i;else break;
          }}
          if(idx!==curIdx){{curIdx=idx;if(idx>=0)render(idx);}}
          const total=lyrics[lyrics.length-1]?.time||1;
          tb.style.width=Math.min(100,(now/total)*100)+'%';
        }}
        
        render(0);
        setInterval(tick,150);
        </script></body></html>"""
        components.html(karaoke_html, height=490)
        if use_synced:
            st.success("🎤 Synced lyrics mode active — start the song above to see real-time karaoke!")
        else:
            st.info("ℹ️ Using plain lyrics with auto-scroll (no time sync). Load synced lyrics for best karaoke experience.")


# ═══════════════════════════ VIEW 22: SONG ANALYZER ═══════════════════════════
elif choice == "🔬 Song Analyzer":
    st.markdown("<h2 style='font-size:2rem;font-weight:700;margin-bottom:4px;'>🔬 Deep Song Analyzer</h2>", unsafe_allow_html=True)
    st.markdown("<p style='color:rgba(255,255,255,0.5);margin-bottom:20px;'>AI-powered deep musicology: key, tempo, mood spectrum, lyrical themes, production style, cultural impact, and more.</p>", unsafe_allow_html=True)

    col_an1, col_an2 = st.columns([3, 1])
    with col_an1:
        default_analyze = f"{st.session_state.current_song['title']} by {st.session_state.current_song['uploader']}" if st.session_state.current_song else ""
        analyze_song = st.text_input("Song to Analyze", value=default_analyze, placeholder="e.g. Stairway to Heaven by Led Zeppelin", key="analyzer_song_input")
    with col_an2:
        depth = st.selectbox("Depth", ["Quick", "Standard", "Deep Dive"], key="analyzer_depth", index=1)

    if st.button("🔬 Run Analysis", use_container_width=True, key="analyze_btn"):
        if not st.session_state.gemini_key:
            st.warning("Please provide a Gemini API Key in the sidebar.")
        elif not analyze_song.strip():
            st.warning("Please enter a song to analyze.")
        else:
            with st.spinner(f"Running {depth} analysis..."):
                url_g = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-2.5-flash:generateContent?key={st.session_state.gemini_key}"
                depth_note = "Be thorough and scholarly." if depth == "Deep Dive" else "Be concise." if depth == "Quick" else "Balance depth and clarity."
                prompt = f"""You are a professional musicologist and cultural analyst. Analyze: "{analyze_song}"
{depth_note} Return ONLY valid JSON (no markdown fences):
{{"song_title":"Title","artist":"Artist","release_year":"Year","genre":"Genre","subgenres":["s1","s2"],"musical_key":"Key","tempo_bpm":"BPM","time_signature":"e.g.4/4","energy_level":"1-10","danceability":"1-10","mood_spectrum":[{{"mood":"Mood","percentage":40}},{{"mood":"Mood2","percentage":35}},{{"mood":"Mood3","percentage":25}}],"lyrical_themes":["t1","t2","t3"],"production_style":"desc","instruments":["i1","i2","i3","i4"],"vocal_style":"desc","song_structure":"desc","cultural_impact":"desc","standout_moment":"desc","similar_songs":["s1","s2","s3"],"for_fans_of":["a1","a2","a3"]}}"""
                try:
                    res = requests.post(url_g, json={{"contents":[{{"parts":[{{"text":prompt}}]}}]}}, headers={{"Content-Type":"application/json"}}, timeout=25)
                    if res.status_code == 200:
                        raw = res.json()['candidates'][0]['content']['parts'][0]['text'].strip()
                        raw = re.sub(r'^```json\s*', '', raw)
                        raw = re.sub(r'\s*```$', '', raw)
                        st.session_state.song_analysis_result = json.loads(raw)
                        st.rerun()
                except Exception as ex:
                    st.error(f"Analysis error: {ex}")

    sa = st.session_state.get("song_analysis_result")
    if sa:
        st.markdown(f"""
        <div style="background:linear-gradient(135deg,rgba(6,182,212,0.08),rgba(168,85,247,0.05));border:1px solid rgba(6,182,212,0.15);border-radius:20px;padding:22px;margin-bottom:22px;">
            <h3 style="font-size:1.5rem;font-weight:700;color:#fff;margin:0 0 4px 0;">{sa.get('song_title','')} <span style="color:rgba(255,255,255,0.4);font-size:1rem;font-weight:400;">({sa.get('release_year','')})</span></h3>
            <p style="color:#06b6d4;font-size:0.95rem;font-weight:600;margin:0 0 14px 0;">by {sa.get('artist','')}</p>
            <div style="display:flex;flex-wrap:wrap;gap:8px;">
                <span style="background:rgba(168,85,247,0.1);border:1px solid rgba(168,85,247,0.25);border-radius:20px;padding:4px 12px;font-size:0.78rem;color:#a855f7;">🎵 {sa.get('genre','')}</span>
                <span style="background:rgba(6,182,212,0.1);border:1px solid rgba(6,182,212,0.25);border-radius:20px;padding:4px 12px;font-size:0.78rem;color:#06b6d4;">🎹 {sa.get('musical_key','')}</span>
                <span style="background:rgba(244,63,94,0.1);border:1px solid rgba(244,63,94,0.25);border-radius:20px;padding:4px 12px;font-size:0.78rem;color:#f43f5e;">⏱ {sa.get('tempo_bpm','')} BPM</span>
                <span style="background:rgba(34,197,94,0.1);border:1px solid rgba(34,197,94,0.25);border-radius:20px;padding:4px 12px;font-size:0.78rem;color:#22c55e;">📊 {sa.get('time_signature','')}</span>
            </div>
        </div>
        """, unsafe_allow_html=True)
        col_m1, col_m2, col_m3, col_m4 = st.columns(4)
        for col, label, val, suffix, color in [
            (col_m1, "⚡ Energy", sa.get('energy_level','?'), "/10", "#f43f5e"),
            (col_m2, "💃 Danceability", sa.get('danceability','?'), "/10", "#a855f7"),
            (col_m3, "🎼 Sub-genres", len(sa.get('subgenres',[])), "", "#06b6d4"),
            (col_m4, "🎸 Instruments", len(sa.get('instruments',[])), " found", "#22c55e"),
        ]:
            with col:
                st.markdown(f"<div style='background:rgba(15,23,42,0.5);border:1px solid rgba(255,255,255,0.06);border-radius:14px;padding:16px;text-align:center;'><p style='font-size:0.68rem;color:rgba(255,255,255,0.4);margin:0 0 4px 0;'>{label}</p><p style='font-size:1.7rem;font-weight:700;color:{color};margin:0;'>{val}<span style='font-size:0.78rem;color:rgba(255,255,255,0.4);'>{suffix}</span></p></div>", unsafe_allow_html=True)
        st.markdown("<br>", unsafe_allow_html=True)
        st.markdown("#### 🌈 Mood Spectrum")
        mood_colors = ["#a855f7","#f43f5e","#06b6d4","#22c55e","#f97316"]
        for mi, m in enumerate(sa.get("mood_spectrum", [])):
            pct = m.get('percentage', 0)
            col_mc = mood_colors[mi % len(mood_colors)]
            st.markdown(f"""<div style="margin-bottom:10px;"><div style="display:flex;justify-content:space-between;margin-bottom:4px;"><span style="font-size:0.85rem;color:rgba(255,255,255,0.7);">{m.get('mood','')}</span><span style="font-size:0.85rem;color:{col_mc};font-weight:700;">{pct}%</span></div><div style="background:rgba(255,255,255,0.06);border-radius:100px;height:8px;overflow:hidden;"><div style="background:{col_mc};height:100%;width:{pct}%;border-radius:100px;"></div></div></div>""", unsafe_allow_html=True)
        col_sa1, col_sa2 = st.columns(2)
        with col_sa1:
            st.markdown("#### 🎭 Lyrical Themes")
            themes_html = "".join(f"<span style='background:rgba(168,85,247,0.1);border:1px solid rgba(168,85,247,0.2);border-radius:20px;padding:5px 14px;font-size:0.78rem;color:#a855f7;display:inline-block;margin:3px;'>📌 {th}</span>" for th in sa.get('lyrical_themes', []))
            st.markdown(themes_html, unsafe_allow_html=True)
            st.markdown("#### 🎸 Instruments")
            inst_html = "".join(f"<span style='background:rgba(6,182,212,0.08);border:1px solid rgba(6,182,212,0.18);border-radius:20px;padding:5px 14px;font-size:0.78rem;color:#06b6d4;display:inline-block;margin:3px;'>🎸 {ins}</span>" for ins in sa.get('instruments', []))
            st.markdown(inst_html, unsafe_allow_html=True)
        with col_sa2:
            st.markdown("#### 🎤 Vocal Style")
            st.markdown(f"<div style='background:rgba(15,23,42,0.4);border:1px solid rgba(255,255,255,0.06);border-radius:12px;padding:12px;margin-bottom:12px;'><p style='font-size:0.83rem;color:rgba(255,255,255,0.7);margin:0;'>{sa.get('vocal_style','')}</p></div>", unsafe_allow_html=True)
            st.markdown("#### 🏗️ Song Structure")
            st.markdown(f"<div style='background:rgba(15,23,42,0.4);border:1px solid rgba(255,255,255,0.06);border-radius:12px;padding:12px;'><p style='font-size:0.83rem;color:rgba(255,255,255,0.7);margin:0;'>{sa.get('song_structure','')}</p></div>", unsafe_allow_html=True)
        st.markdown(f"<div style='background:rgba(244,63,94,0.05);border:1px solid rgba(244,63,94,0.15);border-radius:14px;padding:16px;margin-top:12px;'><p style='font-size:0.72rem;color:#f43f5e;font-weight:700;margin:0 0 6px 0;'>✨ STANDOUT MOMENT</p><p style='font-size:0.88rem;color:rgba(255,255,255,0.75);margin:0;'>{sa.get('standout_moment','')}</p></div>", unsafe_allow_html=True)
        st.markdown(f"<div style='background:rgba(168,85,247,0.05);border:1px solid rgba(168,85,247,0.15);border-radius:14px;padding:16px;margin-top:10px;'><p style='font-size:0.72rem;color:#a855f7;font-weight:700;margin:0 0 6px 0;'>🌍 CULTURAL IMPACT</p><p style='font-size:0.88rem;color:rgba(255,255,255,0.75);margin:0;'>{sa.get('cultural_impact','')}</p></div>", unsafe_allow_html=True)
        col_ss, col_fo = st.columns(2)
        with col_ss:
            st.markdown("#### 🔗 Similar Songs")
            for ss in sa.get("similar_songs", []):
                st.markdown(f"<p style='color:rgba(255,255,255,0.6);font-size:0.83rem;padding:4px 0;border-bottom:1px solid rgba(255,255,255,0.04);margin:0;'>🎵 {ss}</p>", unsafe_allow_html=True)
        with col_fo:
            st.markdown("#### 💜 For Fans Of")
            for fa in sa.get("for_fans_of", []):
                st.markdown(f"<p style='color:rgba(255,255,255,0.6);font-size:0.83rem;padding:4px 0;border-bottom:1px solid rgba(255,255,255,0.04);margin:0;'>🎤 {fa}</p>", unsafe_allow_html=True)
        if st.button("🔍 Search This Song on Melodify", use_container_width=True, key="analyzer_search_btn"):
            results = yt.search_songs(f"{sa.get('song_title','')} {sa.get('artist','')} official", max_results=5)
            if results:
                st.session_state.search_results = results
                st.toast("Search results loaded!")
                st.rerun()
    else:
        st.markdown("""
        <div style="text-align:center;padding:60px 20px;color:rgba(255,255,255,0.25);">
            <div style="font-size:4rem;margin-bottom:16px;">🔬</div>
            <p>Enter any song above and click <strong>Run Analysis</strong> to get a deep musicology report.</p>
        </div>
        """, unsafe_allow_html=True)

# ═══════════════════════════ VIEW 23: BPM TAP TEMPO ═══════════════════════════
elif choice == "⚡ BPM Tap Tempo":
    st.markdown("""
    <div class="neon-grid-header neon-particle-bg">
        <div class="neon-heading">⚡ BPM Tap Tempo & Key Calculator</div>
        <p style="color:rgba(255,255,255,0.45);font-size:0.88rem;margin:6px 0 0 0;">Tap the button to the beat to detect BPM. Transpose keys, calculate tempo divisions, and find matching metronome presets.</p>
    </div>
    """, unsafe_allow_html=True)

    bpm_html = """<!DOCTYPE html><html><head><meta charset="UTF-8">
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Outfit:wght@300;400;600;700;900&display=swap');
    *{box-sizing:border-box;margin:0;padding:0;}
    body{font-family:'Outfit',sans-serif;background:transparent;color:#f3f4f6;padding:16px;overflow:hidden;}
    .main{display:grid;grid-template-columns:1fr 1fr;gap:20px;}
    .card{background:rgba(8,4,18,0.85);border-radius:18px;padding:22px;text-align:center;}
    .card-pink{border:1px solid #f43f5e;box-shadow:0 0 16px rgba(244,63,94,0.3),inset 0 0 24px rgba(244,63,94,0.03);}
    .card-purple{border:1px solid #a855f7;box-shadow:0 0 16px rgba(168,85,247,0.3),inset 0 0 24px rgba(168,85,247,0.03);}
    .bpm-display{font-size:5rem;font-weight:900;line-height:1;
        background:linear-gradient(135deg,#ff2d6b,#a855f7);
        -webkit-background-clip:text;-webkit-text-fill-color:transparent;
        filter:drop-shadow(0 0 12px rgba(244,63,94,0.6));
        margin:16px 0 8px 0;}
    .bpm-label{font-size:0.7rem;text-transform:uppercase;letter-spacing:0.15em;color:rgba(255,255,255,0.3);margin-bottom:20px;}
    .tap-btn{
        width:140px;height:140px;border-radius:50%;cursor:pointer;
        background:radial-gradient(circle,rgba(244,63,94,0.15),rgba(168,85,247,0.08));
        border:2px solid #f43f5e;
        box-shadow:0 0 20px rgba(244,63,94,0.4),0 0 40px rgba(244,63,94,0.15);
        font-size:1rem;font-weight:700;color:#f43f5e;font-family:'Outfit',sans-serif;
        transition:all 0.1s;display:flex;align-items:center;justify-content:center;
        flex-direction:column;gap:4px;margin:0 auto 16px auto;
    }
    .tap-btn:active,.tap-btn.flash{
        background:radial-gradient(circle,rgba(244,63,94,0.4),rgba(168,85,247,0.2));
        box-shadow:0 0 40px rgba(244,63,94,0.8),0 0 80px rgba(244,63,94,0.3);
        transform:scale(0.94);
    }
    .sub-btn{background:rgba(255,255,255,0.04);border:1px solid rgba(255,255,255,0.1);
        color:rgba(255,255,255,0.6);border-radius:10px;padding:8px 18px;
        font-family:'Outfit',sans-serif;font-size:0.8rem;cursor:pointer;transition:all 0.2s;margin:4px;}
    .sub-btn:hover{background:rgba(168,85,247,0.15);border-color:#a855f7;color:#c084fc;box-shadow:0 0 10px rgba(168,85,247,0.3);}
    .divisions{display:grid;grid-template-columns:repeat(3,1fr);gap:10px;margin-top:16px;}
    .div-chip{background:rgba(168,85,247,0.06);border:1px solid rgba(168,85,247,0.2);
        border-radius:10px;padding:10px 6px;text-align:center;}
    .div-chip .val{font-size:1.1rem;font-weight:700;color:#c084fc;text-shadow:0 0 8px rgba(192,132,252,0.5);}
    .div-chip .lbl{font-size:0.6rem;color:rgba(255,255,255,0.35);margin-top:2px;}
    .key-grid{display:grid;grid-template-columns:repeat(4,1fr);gap:8px;margin-top:12px;}
    .key-btn{background:rgba(6,182,212,0.06);border:1px solid rgba(6,182,212,0.2);
        border-radius:10px;padding:10px 4px;text-align:center;cursor:pointer;transition:all 0.2s;font-family:'Outfit',sans-serif;}
    .key-btn:hover{background:rgba(6,182,212,0.18);box-shadow:0 0 10px rgba(6,182,212,0.3);border-color:#06b6d4;}
    .key-btn.active{background:rgba(6,182,212,0.25);border-color:#22d3ee;box-shadow:0 0 14px rgba(6,182,212,0.5);}
    .key-btn .kn{font-size:1.1rem;font-weight:700;color:#22d3ee;text-shadow:0 0 8px rgba(34,211,238,0.5);}
    .key-btn .km{font-size:0.6rem;color:rgba(255,255,255,0.3);}
    h3{font-size:0.8rem;text-transform:uppercase;letter-spacing:0.1em;color:rgba(255,255,255,0.35);margin-bottom:12px;}
    </style></head><body>
    <div class="main">
      <div class="card card-pink">
        <h3>🥁 Tap Beat Detector</h3>
        <div class="bpm-display" id="bpm">--</div>
        <div class="bpm-label">Beats Per Minute</div>
        <button class="tap-btn" id="tapBtn" onmousedown="tap()">
          <span style="font-size:2rem;">🥁</span>
          <span>TAP</span>
        </button>
        <div style="display:flex;justify-content:center;gap:8px;">
          <button class="sub-btn" onclick="resetTaps()">↺ Reset</button>
          <button class="sub-btn" id="metBtn" onclick="toggleMetronome()">🔔 Metronome</button>
        </div>
        <div class="divisions" id="divs" style="opacity:0.3;">
          <div class="div-chip"><div class="val" id="d-whole">--</div><div class="lbl">Whole</div></div>
          <div class="div-chip"><div class="val" id="d-half">--</div><div class="lbl">Half</div></div>
          <div class="div-chip"><div class="val" id="d-quarter">--</div><div class="lbl">Quarter</div></div>
          <div class="div-chip"><div class="val" id="d-8th">--</div><div class="lbl">8th</div></div>
          <div class="div-chip"><div class="val" id="d-16th">--</div><div class="lbl">16th</div></div>
          <div class="div-chip"><div class="val" id="d-triplet">--</div><div class="lbl">Triplet</div></div>
        </div>
      </div>
      <div class="card card-purple">
        <h3>🎵 Key & Scale Finder</h3>
        <div class="key-grid" id="keyGrid"></div>
        <div style="margin-top:16px;background:rgba(168,85,247,0.05);border:1px solid rgba(168,85,247,0.15);border-radius:12px;padding:14px;">
          <p style="font-size:0.72rem;color:rgba(255,255,255,0.35);margin:0 0 6px 0;text-transform:uppercase;letter-spacing:0.08em;">Relative & Parallel Keys</p>
          <div id="relKeys" style="font-size:0.85rem;color:rgba(255,255,255,0.65);line-height:1.8;"></div>
        </div>
        <div style="margin-top:12px;background:rgba(6,182,212,0.04);border:1px solid rgba(6,182,212,0.12);border-radius:12px;padding:12px;">
          <p style="font-size:0.72rem;color:rgba(255,255,255,0.35);margin:0 0 6px 0;text-transform:uppercase;letter-spacing:0.08em;">Common Chord Progression</p>
          <div id="progDisplay" style="font-size:0.92rem;color:#22d3ee;text-shadow:0 0 8px rgba(34,211,238,0.4);letter-spacing:0.04em;"></div>
        </div>
      </div>
    </div>
    <script>
    let taps=[],metInterval=null,metOn=false;
    const audioCtx=new(window.AudioContext||window.webkitAudioContext)();

    function tap(){
        const now=performance.now();
        taps.push(now);
        if(taps.length>8)taps.shift();
        const btn=document.getElementById('tapBtn');
        btn.classList.add('flash');
        setTimeout(()=>btn.classList.remove('flash'),120);
        if(taps.length>=2){
            const intervals=[];
            for(let i=1;i<taps.length;i++)intervals.push(taps[i]-taps[i-1]);
            const avg=intervals.reduce((a,b)=>a+b,0)/intervals.length;
            const bpm=Math.round(60000/avg);
            document.getElementById('bpm').innerText=bpm;
            const s=(60/bpm).toFixed(3);
            document.getElementById('d-whole').innerText=(parseFloat(s)*4).toFixed(2)+'s';
            document.getElementById('d-half').innerText=(parseFloat(s)*2).toFixed(2)+'s';
            document.getElementById('d-quarter').innerText=parseFloat(s).toFixed(3)+'s';
            document.getElementById('d-8th').innerText=(parseFloat(s)/2).toFixed(3)+'s';
            document.getElementById('d-16th').innerText=(parseFloat(s)/4).toFixed(3)+'s';
            document.getElementById('d-triplet').innerText=(parseFloat(s)*2/3).toFixed(3)+'s';
            document.getElementById('divs').style.opacity='1';
        }
    }

    function resetTaps(){taps=[];document.getElementById('bpm').innerText='--';document.getElementById('divs').style.opacity='0.3';}

    function toggleMetronome(){
        metOn=!metOn;
        const btn=document.getElementById('metBtn');
        if(metOn){
            btn.style.color='#f43f5e';btn.style.borderColor='#f43f5e';btn.style.boxShadow='0 0 10px rgba(244,63,94,0.4)';
            const bpmVal=parseInt(document.getElementById('bpm').innerText)||120;
            const interval=60000/bpmVal;
            function click(){
                const o=audioCtx.createOscillator(),g=audioCtx.createGain();
                o.frequency.value=880;o.type='sine';
                g.gain.setValueAtTime(0.3,audioCtx.currentTime);
                g.gain.exponentialRampToValueAtTime(0.001,audioCtx.currentTime+0.08);
                o.connect(g);g.connect(audioCtx.destination);
                o.start();o.stop(audioCtx.currentTime+0.08);
            }
            click();metInterval=setInterval(click,interval);
        } else {
            clearInterval(metInterval);
            btn.style.color='';btn.style.borderColor='';btn.style.boxShadow='';
        }
    }

    const keys=['C','C#','D','D#','E','F','F#','G','G#','A','A#','B'];
    const relMinor={'C':'Am','G':'Em','D':'Bm','A':'F#m','E':'C#m','B':'G#m','F#':'D#m','C#':'A#m','F':'Dm','Bb':'Gm','Eb':'Cm','Ab':'Fm'};
    const progs={'C':'C - Am - F - G','G':'G - Em - C - D','D':'D - Bm - G - A','A':'A - F#m - D - E','E':'E - C#m - A - B','F':'F - Dm - Bb - C','Bb':'Bb - Gm - Eb - F','Eb':'Eb - Cm - Ab - Bb','Ab':'Ab - Fm - Db - Eb'};
    let selKey='C';
    const kg=document.getElementById('keyGrid');
    keys.forEach(k=>{
        const b=document.createElement('div');b.className='key-btn'+(k===selKey?' active':'');
        b.innerHTML=`<div class="kn">${k}</div><div class="km">Major</div>`;
        b.onclick=()=>{selKey=k;document.querySelectorAll('.key-btn').forEach(x=>x.classList.remove('active'));b.classList.add('active');updateKey(k);};
        kg.appendChild(b);
    });
    function updateKey(k){
        const rel=relMinor[k]||'—';
        document.getElementById('relKeys').innerHTML=`🔗 Relative Minor: <strong style="color:#c084fc;">${rel}</strong><br>🎵 Parallel Minor: <strong style="color:#06b6d4;">${k}m</strong><br>🔄 Dominant: <strong style="color:#f43f5e;">${keys[(keys.indexOf(k)+7)%12]}</strong>`;
        document.getElementById('progDisplay').innerText=progs[k]||`${k} - ${k}m - IV - V`;
    }
    updateKey('C');
    document.addEventListener('keydown',e=>{if(e.code==='Space'){e.preventDefault();tap();}});
    </script></body></html>"""
    components.html(bpm_html, height=540)
    st.markdown("<div class='neon-sweep'></div>", unsafe_allow_html=True)
    st.markdown("<p style='color:rgba(255,255,255,0.3);font-size:0.75rem;text-align:center;'>Press <strong>Space</strong> to tap on the beat · Metronome uses Web Audio API</p>", unsafe_allow_html=True)


# ═══════════════════════════ VIEW 24: NEON VISUALIZER ═══════════════════════════
elif choice == "🎨 Neon Visualizer":
    st.markdown("""
    <div class="neon-grid-header neon-particle-bg">
        <div class="neon-heading">🎨 Neon Audio Visualizer</div>
        <p style="color:rgba(255,255,255,0.45);font-size:0.88rem;margin:6px 0 0 0;">Five reactive neon visualizer modes powered by the Web Audio API — mic or oscillator input.</p>
    </div>
    """, unsafe_allow_html=True)

    viz_html = """<!DOCTYPE html><html><head><meta charset="UTF-8">
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Outfit:wght@400;600;700&display=swap');
    *{box-sizing:border-box;margin:0;padding:0;}
    body{font-family:'Outfit',sans-serif;background:#060810;color:#f3f4f6;overflow:hidden;}
    canvas{display:block;border-radius:16px;border:1px solid rgba(168,85,247,0.2);box-shadow:0 0 20px rgba(168,85,247,0.15);}
    .controls{display:flex;gap:10px;flex-wrap:wrap;padding:12px 0 10px 0;align-items:center;}
    .vbtn{background:rgba(255,255,255,0.04);border:1px solid rgba(255,255,255,0.1);color:rgba(255,255,255,0.6);
        border-radius:10px;padding:8px 16px;font-family:'Outfit',sans-serif;font-size:0.8rem;cursor:pointer;transition:all 0.2s;}
    .vbtn.active{background:rgba(168,85,247,0.15);border-color:#a855f7;color:#c084fc;box-shadow:0 0 10px rgba(168,85,247,0.3);}
    .vbtn:hover:not(.active){background:rgba(255,255,255,0.08);}
    .start-btn{background:linear-gradient(135deg,rgba(244,63,94,0.2),rgba(168,85,247,0.15));
        border:1px solid #f43f5e;color:#fff;border-radius:12px;padding:10px 24px;
        font-size:0.88rem;font-weight:700;cursor:pointer;font-family:'Outfit',sans-serif;
        box-shadow:0 0 14px rgba(244,63,94,0.3);transition:all 0.2s;}
    .start-btn:hover{box-shadow:0 0 24px rgba(244,63,94,0.5);}
    .src-btn{background:rgba(6,182,212,0.08);border:1px solid rgba(6,182,212,0.25);color:#22d3ee;
        border-radius:10px;padding:8px 16px;font-family:'Outfit',sans-serif;font-size:0.8rem;cursor:pointer;transition:all 0.2s;}
    .src-btn.active{background:rgba(6,182,212,0.2);box-shadow:0 0 10px rgba(6,182,212,0.3);}
    </style></head><body>
    <div style="padding:12px;">
      <div class="controls">
        <button class="start-btn" id="startBtn" onclick="toggleViz()">▶ Start Visualizer</button>
        <button class="src-btn active" id="srcMic" onclick="setSource('mic')">🎤 Microphone</button>
        <button class="src-btn" id="srcOsc" onclick="setSource('osc')">〜 Oscillator</button>
      </div>
      <div class="controls" style="padding-top:0;">
        <span style="font-size:0.7rem;color:rgba(255,255,255,0.3);text-transform:uppercase;letter-spacing:0.08em;">Mode:</span>
        <button class="vbtn active" id="m-bars" onclick="setMode('bars')">▮ Bars</button>
        <button class="vbtn" id="m-wave" onclick="setMode('wave')">〜 Wave</button>
        <button class="vbtn" id="m-circle" onclick="setMode('circle')">◉ Circular</button>
        <button class="vbtn" id="m-stars" onclick="setMode('stars')">✦ Starfield</button>
        <button class="vbtn" id="m-mirror" onclick="setMode('mirror')">⬡ Mirror</button>
      </div>
      <canvas id="viz" width="720" height="320"></canvas>
    </div>
    <script>
    let audioCtx=null,analyser=null,source=null,osc=null,gainNode=null;
    let running=false,animId=null,mode='bars',srcType='mic',stream=null;
    const canvas=document.getElementById('viz');
    const ctx=canvas.getContext('2d');
    const W=720,H=320;

    const palettes={
        bars:['#ff2d6b','#f43f5e','#a855f7','#7c3aed','#06b6d4','#0891b2'],
        wave:['#22d3ee','#06b6d4'],circle:['#a855f7','#f43f5e','#06b6d4'],
        stars:['#fff','#c084fc','#f43f5e','#22d3ee'],mirror:['#f43f5e','#a855f7']
    };

    async function toggleViz(){
        const btn=document.getElementById('startBtn');
        if(running){running=false;cancelAnimationFrame(animId);ctx.clearRect(0,0,W,H);btn.innerText='▶ Start Visualizer';if(stream)stream.getTracks().forEach(t=>t.stop());if(osc)osc.stop();return;}
        if(!audioCtx)audioCtx=new(window.AudioContext||window.webkitAudioContext)();
        analyser=audioCtx.createAnalyser();analyser.fftSize=2048;
        if(srcType==='mic'){
            try{stream=await navigator.mediaDevices.getUserMedia({audio:true});source=audioCtx.createMediaStreamSource(stream);source.connect(analyser);}
            catch(e){alert('Mic access denied. Switching to oscillator.');setSource('osc');return;}
        } else {
            osc=audioCtx.createOscillator();gainNode=audioCtx.createGain();gainNode.gain.value=0.01;
            osc.type='sawtooth';osc.frequency.setValueAtTime(220,audioCtx.currentTime);
            osc.connect(gainNode);gainNode.connect(analyser);analyser.connect(audioCtx.destination);
            osc.start();
        }
        running=true;btn.innerText='⏹ Stop';draw();
    }

    function setMode(m){mode=m;document.querySelectorAll('.vbtn').forEach(b=>b.classList.remove('active'));document.getElementById('m-'+m).classList.add('active');}
    function setSource(s){srcType=s;document.getElementById('srcMic').classList.toggle('active',s==='mic');document.getElementById('srcOsc').classList.toggle('active',s==='osc');}

    function draw(){
        animId=requestAnimationFrame(draw);
        const buf=new Uint8Array(analyser.frequencyBinCount);
        analyser.getByteFrequencyData(buf);
        const tbuf=new Uint8Array(analyser.fftSize);
        analyser.getByteTimeDomainData(tbuf);
        ctx.fillStyle='rgba(6,8,16,0.25)';ctx.fillRect(0,0,W,H);

        if(mode==='bars'){
            const bw=W/128,gap=1;
            for(let i=0;i<128;i++){
                const v=buf[i*2]/255;
                const h=v*H;
                const grd=ctx.createLinearGradient(0,H-h,0,H);
                grd.addColorStop(0,'#22d3ee');grd.addColorStop(0.5,'#a855f7');grd.addColorStop(1,'#f43f5e');
                ctx.fillStyle=grd;
                ctx.shadowBlur=8+v*12;ctx.shadowColor='rgba(168,85,247,0.8)';
                ctx.fillRect(i*(bw+gap),H-h,bw,h);
            }
        } else if(mode==='wave'){
            ctx.lineWidth=2;ctx.strokeStyle='#22d3ee';ctx.shadowBlur=12;ctx.shadowColor='rgba(34,211,238,0.7)';
            ctx.beginPath();
            const sl=W/tbuf.length;
            for(let i=0;i<tbuf.length;i++){const y=(tbuf[i]/128)*H/2;i===0?ctx.moveTo(0,y):ctx.lineTo(i*sl,y);}
            ctx.stroke();
            ctx.strokeStyle='rgba(168,85,247,0.5)';ctx.shadowColor='rgba(168,85,247,0.5)';
            ctx.beginPath();
            for(let i=0;i<tbuf.length;i++){const y=H-(tbuf[i]/128)*H/2;i===0?ctx.moveTo(0,y):ctx.lineTo(i*sl,y);}
            ctx.stroke();
        } else if(mode==='circle'){
            const cx=W/2,cy=H/2,r=90;
            ctx.strokeStyle='rgba(168,85,247,0.1)';ctx.lineWidth=1;ctx.beginPath();ctx.arc(cx,cy,r,0,Math.PI*2);ctx.stroke();
            for(let i=0;i<360;i+=2){
                const angle=(i/360)*Math.PI*2;
                const v=buf[Math.floor(i/360*128)]/255;
                const len=v*70;
                ctx.strokeStyle=`hsl(${280+v*80},90%,${50+v*30}%)`;
                ctx.shadowBlur=v*16;ctx.shadowColor=`hsl(${280+v*80},90%,60%)`;
                ctx.lineWidth=1.5;ctx.beginPath();
                ctx.moveTo(cx+Math.cos(angle)*r,cy+Math.sin(angle)*r);
                ctx.lineTo(cx+Math.cos(angle)*(r+len),cy+Math.sin(angle)*(r+len));
                ctx.stroke();
            }
        } else if(mode==='stars'){
            if(!draw.stars){draw.stars=Array.from({length:80},()=>({x:Math.random()*W,y:Math.random()*H,s:Math.random()*2+0.5,spd:Math.random()*0.4+0.1}));}
            const avg=buf.slice(0,64).reduce((a,b)=>a+b,0)/64/255;
            draw.stars.forEach(s=>{
                s.x-=s.spd*(1+avg*4);if(s.x<0)s.x=W;
                const a=0.4+avg*0.6;
                ctx.fillStyle=`rgba(${168+avg*80},${85+avg*50},${247},${a})`;
                ctx.shadowBlur=4+avg*8;ctx.shadowColor='rgba(168,85,247,0.8)';
                ctx.beginPath();ctx.arc(s.x,s.y,s.s*(1+avg),0,Math.PI*2);ctx.fill();
            });
        } else if(mode==='mirror'){
            const cx=W/2;
            for(let i=0;i<64;i++){
                const v=buf[i*2]/255;const h=v*H/2;
                const x=(i/64)*cx;
                const grd=ctx.createLinearGradient(0,H/2-h,0,H/2);
                grd.addColorStop(0,'#f43f5e');grd.addColorStop(1,'rgba(168,85,247,0.3)');
                ctx.fillStyle=grd;ctx.shadowBlur=v*10;ctx.shadowColor='rgba(244,63,94,0.6)';
                ctx.fillRect(cx-x-4,H/2-h,4,h);ctx.fillRect(cx+x,H/2-h,4,h);
                ctx.fillRect(cx-x-4,H/2,4,h);ctx.fillRect(cx+x,H/2,4,h);
            }
        }
        ctx.shadowBlur=0;
    }
    </script></body></html>"""
    components.html(viz_html, height=510)


# ═══════════════════════════ VIEW 25: MUSIC DNA ═══════════════════════════
elif choice == "🧬 Music DNA":
    st.markdown("""
    <div class="neon-grid-header neon-particle-bg">
        <div class="neon-heading">🧬 My Music DNA Profile</div>
        <p style="color:rgba(255,255,255,0.45);font-size:0.88rem;margin:6px 0 0 0;">Your listening data decoded into a visual audio genome — genre helix, emotion spectrum, and sonic fingerprint.</p>
    </div>
    """, unsafe_allow_html=True)

    if not st.session_state.gemini_key:
        st.markdown("<div class='neon-card-pink' style='text-align:center;padding:24px;'>⚠️ Add your Gemini API Key in the sidebar to generate your Music DNA.</div>", unsafe_allow_html=True)
    else:
        favs = db.get_favorites()
        recents = db.get_recent_plays()
        rated = db.get_all_ratings()

        if not favs and not recents:
            st.markdown("<div class='neon-card-purple' style='text-align:center;padding:24px;'>💡 Play and favorite some songs first, then come back to decode your Music DNA!</div>", unsafe_allow_html=True)
        else:
            if st.button("🧬 Decode My Music DNA", use_container_width=True):
                fav_list = [f"{f['uploader']} - {f['title']}" for f in favs[:12]]
                rec_list = [f"{r['uploader']} - {r['title']}" for r in recents[:12]]
                rat_list = [f"{r['uploader']} - {r['title']} ({r['rating']}/5)" for r in rated[:8]]
                with st.spinner("Sequencing your audio genome..."):
                    url_g = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-2.5-flash:generateContent?key={st.session_state.gemini_key}"
                    prompt = f"""Analyze this music listener's DNA from their data:
Favorites: {json.dumps(fav_list)}
Recent plays: {json.dumps(rec_list)}
Ratings: {json.dumps(rat_list)}
Return ONLY valid JSON (no fences):
{{"dna_name":"Creative musical archetype name","genome":[{{"trait":"Trait name","value":75,"color":"#f43f5e","desc":"Short description"}},...8],"genre_helix":[{{"genre":"Genre","pct":30}},...5],"emotion_map":[{{"emotion":"Joy","pct":40}},...6],"sonic_signature":"2-sentence poetic description","era_affinity":"Decade","tempo_soul":"Slow/Mid/Fast/Mixed","listening_style":"Immersive/Social/Background","top_instruments":["inst1","inst2","inst3"]}}"""
                    try:
                        res = requests.post(url_g, json={"contents":[{"parts":[{"text":prompt}]}]}, headers={"Content-Type":"application/json"}, timeout=25)
                        if res.status_code == 200:
                            raw = res.json()['candidates'][0]['content']['parts'][0]['text'].strip()
                            raw = re.sub(r'^```json\s*','',raw); raw = re.sub(r'\s*```$','',raw)
                            st.session_state.music_dna = json.loads(raw)
                            st.rerun()
                    except Exception as ex:
                        st.error(f"Error: {ex}")

        dna = st.session_state.get("music_dna")
        if dna:
            st.markdown(f"""
            <div class="neon-card-purple neon-scanlines" style="text-align:center;margin-bottom:22px;">
                <div style="font-size:0.7rem;color:rgba(255,255,255,0.3);text-transform:uppercase;letter-spacing:0.15em;margin-bottom:6px;">Your Sonic Archetype</div>
                <div class="neon-text-purple" style="font-size:1.8rem;font-weight:800;">{dna.get('dna_name','')}</div>
                <p style="color:rgba(255,255,255,0.5);font-size:0.88rem;margin:10px 0 0 0;font-style:italic;">{dna.get('sonic_signature','')}</p>
                <div style="display:flex;justify-content:center;gap:16px;margin-top:14px;flex-wrap:wrap;">
                    <span class="neon-badge neon-badge-cyan">🕐 {dna.get('era_affinity','')}</span>
                    <span class="neon-badge neon-badge-pink">⏱ {dna.get('tempo_soul','')}</span>
                    <span class="neon-badge neon-badge-green">🎧 {dna.get('listening_style','')}</span>
                </div>
            </div>
            """, unsafe_allow_html=True)

            col_g, col_e = st.columns(2)
            with col_g:
                st.markdown("<p style='font-size:0.7rem;text-transform:uppercase;letter-spacing:0.1em;color:rgba(255,255,255,0.3);margin-bottom:10px;'>🎵 Genre Helix</p>", unsafe_allow_html=True)
                neon_cols = ["#f43f5e","#a855f7","#06b6d4","#22c55e","#f97316"]
                for i, g in enumerate(dna.get("genre_helix", [])):
                    col = neon_cols[i % len(neon_cols)]
                    pct = g.get('pct', 0)
                    st.markdown(f"""
                    <div style="margin-bottom:10px;">
                        <div style="display:flex;justify-content:space-between;margin-bottom:4px;">
                            <span style="font-size:0.82rem;color:rgba(255,255,255,0.7);">{g.get('genre','')}</span>
                            <span style="font-size:0.82rem;color:{col};font-weight:700;">{pct}%</span>
                        </div>
                        <div class="neon-progress-track">
                            <div class="neon-progress-fill" style="width:{pct}%;background:{col};box-shadow:0 0 8px {col}88;"></div>
                        </div>
                    </div>
                    """, unsafe_allow_html=True)

            with col_e:
                st.markdown("<p style='font-size:0.7rem;text-transform:uppercase;letter-spacing:0.1em;color:rgba(255,255,255,0.3);margin-bottom:10px;'>💠 Emotion Spectrum</p>", unsafe_allow_html=True)
                for i, em in enumerate(dna.get("emotion_map", [])):
                    col = neon_cols[i % len(neon_cols)]
                    pct = em.get('pct', 0)
                    st.markdown(f"""
                    <div style="margin-bottom:10px;">
                        <div style="display:flex;justify-content:space-between;margin-bottom:4px;">
                            <span style="font-size:0.82rem;color:rgba(255,255,255,0.7);">{em.get('emotion','')}</span>
                            <span style="font-size:0.82rem;color:{col};font-weight:700;">{pct}%</span>
                        </div>
                        <div class="neon-progress-track">
                            <div class="neon-progress-fill" style="width:{pct}%;background:{col};box-shadow:0 0 8px {col}88;"></div>
                        </div>
                    </div>
                    """, unsafe_allow_html=True)

            st.markdown("<div class='neon-sweep'></div>", unsafe_allow_html=True)
            st.markdown("<p style='font-size:0.7rem;text-transform:uppercase;letter-spacing:0.1em;color:rgba(255,255,255,0.3);margin-bottom:12px;'>🎸 Genome Traits</p>", unsafe_allow_html=True)
            genome = dna.get("genome", [])
            gcols = st.columns(4)
            for i, trait in enumerate(genome):
                with gcols[i % 4]:
                    val = trait.get('value', 50)
                    col = trait.get('color', '#a855f7')
                    st.markdown(f"""
                    <div style="background:rgba(8,4,18,0.8);border:1px solid {col};border-radius:14px;padding:14px;text-align:center;margin-bottom:10px;box-shadow:0 0 10px {col}44;">
                        <div style="font-size:1.6rem;font-weight:900;color:{col};text-shadow:0 0 12px {col};">{val}</div>
                        <div style="font-size:0.68rem;font-weight:700;color:rgba(255,255,255,0.5);text-transform:uppercase;letter-spacing:0.06em;margin:4px 0 2px 0;">{trait.get('trait','')}</div>
                        <div style="font-size:0.65rem;color:rgba(255,255,255,0.3);">{trait.get('desc','')}</div>
                    </div>
                    """, unsafe_allow_html=True)

            st.markdown("<p style='font-size:0.7rem;text-transform:uppercase;letter-spacing:0.1em;color:rgba(255,255,255,0.3);margin:12px 0 8px 0;'>🎹 Top Instruments in Your DNA</p>", unsafe_allow_html=True)
            inst_html = "".join(f"<span class='neon-badge neon-badge-purple' style='margin:3px;'>🎵 {ins}</span>" for ins in dna.get("top_instruments", []))
            st.markdown(f"<div style='display:flex;flex-wrap:wrap;gap:4px;'>{inst_html}</div>", unsafe_allow_html=True)


# ═══════════════════════════ VIEW 26: TRENDING NOW ═══════════════════════════
elif choice == "🔥 Trending Now":
    st.markdown("""
    <div class="neon-grid-header neon-particle-bg">
        <div class="neon-heading">🔥 Trending Now</div>
        <p style="color:rgba(255,255,255,0.45);font-size:0.88rem;margin:6px 0 0 0;">AI-curated real-time charts: hottest tracks, rising artists, and viral moments across genres.</p>
    </div>
    """, unsafe_allow_html=True)

    if not st.session_state.gemini_key:
        st.markdown("<div class='neon-card-pink' style='text-align:center;padding:24px;'>⚠️ Add your Gemini API Key to load trending charts.</div>", unsafe_allow_html=True)
    else:
        col_tc, col_tg = st.columns([2, 3])
        with col_tc:
            chart_type = st.selectbox("Chart", ["Global Hot 100", "Viral 50", "Rising Artists", "Throwback Hits", "Genre Spotlight"], key="trend_chart")
        with col_tg:
            trend_genre = st.selectbox("Genre Filter", ["All Genres", "Pop", "Hip-Hop", "Rock", "Electronic", "R&B", "K-Pop", "Latin", "Indie", "Metal", "Country", "Jazz"], key="trend_genre")

        if st.button("🔥 Load Trending Chart", use_container_width=True, key="trend_load_btn"):
            with st.spinner("Scanning the zeitgeist..."):
                url_g = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-2.5-flash:generateContent?key={st.session_state.gemini_key}"
                prompt = f"""You are a music industry data analyst. Generate a realistic '{chart_type}' chart for '{trend_genre}' as of 2025.
Return ONLY valid JSON array (no fences), 10 entries:
[{{"rank":1,"title":"Song","artist":"Artist","genre":"Genre","trend":"up/down/new/stable","trend_pct":15,"hot_reason":"Why it's trending in one sentence","weeks_on_chart":3}}]"""
                try:
                    res = requests.post(url_g, json={"contents":[{"parts":[{"text":prompt}]}]}, headers={"Content-Type":"application/json"}, timeout=20)
                    if res.status_code == 200:
                        raw = res.json()['candidates'][0]['content']['parts'][0]['text'].strip()
                        raw = re.sub(r'^```json\s*','',raw); raw = re.sub(r'\s*```$','',raw)
                        st.session_state.trending_chart = json.loads(raw)
                        st.session_state.trending_chart_name = f"{chart_type} — {trend_genre}"
                        st.rerun()
                except Exception as ex:
                    st.error(f"Error: {ex}")

        chart = st.session_state.get("trending_chart", [])
        chart_name = st.session_state.get("trending_chart_name", "")
        if chart:
            st.markdown(f"""
            <div style="display:flex;align-items:center;gap:12px;margin-bottom:18px;">
                <div style="display:flex;align-items:flex-end;gap:2px;">
                    <div class="eq-bar"></div><div class="eq-bar"></div><div class="eq-bar"></div>
                    <div class="eq-bar"></div><div class="eq-bar"></div><div class="eq-bar"></div>
                    <div class="eq-bar"></div>
                </div>
                <span style="font-size:0.75rem;font-weight:700;color:rgba(255,255,255,0.5);text-transform:uppercase;letter-spacing:0.08em;">{chart_name}</span>
            </div>
            """, unsafe_allow_html=True)

            for track in chart:
                rank = track.get('rank', 0)
                trend = track.get('trend', 'stable')
                trend_icon = {"up": "🟢 ▲", "down": "🔴 ▼", "new": "⚡ NEW", "stable": "⬜ —"}.get(trend, "—")
                trend_pct = track.get('trend_pct', 0)
                weeks = track.get('weeks_on_chart', 1)
                border_col = "#f43f5e" if rank <= 3 else ("rgba(168,85,247,0.4)" if rank <= 7 else "rgba(255,255,255,0.07)")
                rank_glow = f"box-shadow:0 0 16px rgba(244,63,94,0.4);" if rank <= 3 else ""

                card_cols = st.columns([0.6, 5, 2.5, 1.5])
                with card_cols[0]:
                    rank_color = "#fbbf24" if rank == 1 else ("#9ca3af" if rank == 2 else ("#b45309" if rank == 3 else "rgba(255,255,255,0.3)"))
                    st.markdown(f"<div style='text-align:center;padding-top:8px;font-size:1.2rem;font-weight:900;color:{rank_color};text-shadow:0 0 8px {rank_color};'>#{rank}</div>", unsafe_allow_html=True)
                with card_cols[1]:
                    st.markdown(f"""
                    <div style="background:rgba(8,4,18,0.7);border:1px solid {border_col};border-radius:12px;padding:10px 14px;{rank_glow}margin-bottom:4px;">
                        <p style="font-weight:700;font-size:0.92rem;color:#fff;margin:0 0 2px 0;">{track.get('title','')}</p>
                        <p style="font-size:0.75rem;color:rgba(255,255,255,0.5);margin:0 0 5px 0;">{track.get('artist','')} · <span style="color:rgba(168,85,247,0.7);">{track.get('genre','')}</span></p>
                        <p style="font-size:0.7rem;font-style:italic;color:rgba(255,255,255,0.4);margin:0;">{track.get('hot_reason','')}</p>
                    </div>
                    """, unsafe_allow_html=True)
                with card_cols[2]:
                    st.markdown(f"<div style='padding-top:6px;font-size:0.8rem;color:rgba(255,255,255,0.5);'>{trend_icon} <span style='font-size:0.72rem;'>{trend_pct}% · {weeks}w on chart</span></div>", unsafe_allow_html=True)
                with card_cols[3]:
                    st.markdown("<div style='height:6px;'></div>", unsafe_allow_html=True)
                    if st.button("▶️", key=f"trend_play_{rank}_{track.get('title','')[:8]}", help="Play", use_container_width=True):
                        with st.spinner("Searching..."):
                            res = yt.search_songs(f"{track.get('artist','')} {track.get('title','')}", max_results=1)
                            if res:
                                play_song(res[0])
                            else:
                                st.toast("Not found on YouTube")
        else:
            st.markdown("""
            <div style="text-align:center;padding:60px 20px;color:rgba(255,255,255,0.25);">
                <div style="display:flex;justify-content:center;align-items:flex-end;gap:4px;margin-bottom:20px;height:48px;">
                    <div class="eq-bar" style="height:20px;"></div><div class="eq-bar" style="height:36px;"></div>
                    <div class="eq-bar" style="height:28px;"></div><div class="eq-bar" style="height:44px;"></div>
                    <div class="eq-bar" style="height:22px;"></div><div class="eq-bar" style="height:38px;"></div>
                </div>
                <p style="font-size:1rem;">Select a chart type and click <strong>Load Trending Chart</strong></p>
            </div>
            """, unsafe_allow_html=True)


# ═══════════════════════════ VIEW 27: COLLAB STUDIO ═══════════════════════════
elif choice == "🤝 Collab Studio":
    st.markdown("""
    <div class="neon-grid-header neon-particle-bg">
        <div class="neon-heading">🤝 AI Collab Studio</div>
        <p style="color:rgba(255,255,255,0.45);font-size:0.88rem;margin:6px 0 0 0;">Co-write lyrics, melodies, and song concepts with an AI music producer. Brainstorm hooks, verses, and bridges in real time.</p>
    </div>
    """, unsafe_allow_html=True)

    if not st.session_state.gemini_key:
        st.markdown("<div class='neon-card-pink' style='padding:20px;text-align:center;'>⚠️ Add your Gemini API Key in the sidebar to start collaborating.</div>", unsafe_allow_html=True)
    else:
        col_cs1, col_cs2 = st.columns([2, 3])
        with col_cs1:
            st.markdown("<p style='font-size:0.72rem;text-transform:uppercase;letter-spacing:0.1em;color:rgba(255,255,255,0.35);margin-bottom:10px;'>⚙️ Session Settings</p>", unsafe_allow_html=True)
            collab_genre = st.selectbox("Genre", ["Pop", "Hip-Hop", "R&B", "Rock", "Electronic", "Indie", "Country", "Latin", "Jazz", "Cinematic"], key="collab_genre")
            collab_mood = st.selectbox("Mood / Vibe", ["Upbeat", "Melancholic", "Dark", "Romantic", "Angry", "Nostalgic", "Euphoric", "Mysterious", "Empowering"], key="collab_mood")
            collab_theme = st.text_input("Song Theme", placeholder="e.g. late night drives, lost love, winning", key="collab_theme")
            if st.button("🗑️ Clear Session", key="collab_clear", use_container_width=True):
                st.session_state.collab_messages = []
                st.rerun()
        with col_cs2:
            st.markdown("<p style='font-size:0.72rem;text-transform:uppercase;letter-spacing:0.1em;color:rgba(255,255,255,0.35);margin-bottom:10px;'>💬 Collab Chat</p>", unsafe_allow_html=True)
            if not st.session_state.collab_messages:
                st.markdown(f"""
                <div class="neon-card-purple" style="margin-bottom:12px;">
                    <span class="neon-badge neon-badge-purple" style="margin-bottom:8px;display:inline-block;">🎛️ AI Producer</span>
                    <p style="color:rgba(255,255,255,0.75);font-size:0.88rem;margin:0;line-height:1.6;">
                        Hey! I'm your AI music producer. Tell me what you're working on — a hook, a verse, a concept — and let's build something incredible together. Genre: <strong>{collab_genre}</strong>, Vibe: <strong>{collab_mood}</strong>.
                    </p>
                </div>
                """, unsafe_allow_html=True)
            for msg in st.session_state.collab_messages:
                is_ai = msg["role"] == "assistant"
                card_class = "neon-card-purple" if is_ai else "neon-card-pink"
                label = "🎛️ AI Producer" if is_ai else "✍️ You"
                badge_class = "neon-badge-purple" if is_ai else "neon-badge-pink"
                st.markdown(f"""
                <div class="{card_class}" style="margin-bottom:10px;">
                    <span class="neon-badge {badge_class}" style="margin-bottom:8px;display:inline-block;">{label}</span>
                    <p style="color:rgba(255,255,255,0.78);font-size:0.86rem;margin:0;line-height:1.7;white-space:pre-wrap;">{msg['content']}</p>
                </div>
                """, unsafe_allow_html=True)
            user_input = st.text_area("Your idea / request", placeholder="e.g. Write me a chorus about chasing dreams at midnight...", height=80, key="collab_input")
            if st.button("🚀 Send to Producer", use_container_width=True, key="collab_send"):
                if user_input.strip():
                    st.session_state.collab_messages.append({"role": "user", "content": user_input.strip()})
                    history = "\n".join([f"{'Producer' if m['role']=='assistant' else 'Artist'}: {m['content']}" for m in st.session_state.collab_messages[-8:]])
                    prompt = f"""You are a professional music producer and co-writer. Genre: {collab_genre}. Mood: {collab_mood}. Theme: {collab_theme or 'open'}.
Conversation so far:
{history}
Respond as the producer — write lyrics, suggest structure, offer hooks, provide verse/chorus/bridge. Keep it creative and actionable. Format lyrics clearly with section labels like [Verse 1], [Chorus], etc."""
                    url_g = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-2.5-flash:generateContent?key={st.session_state.gemini_key}"
                    with st.spinner("Producer is writing..."):
                        try:
                            res = requests.post(url_g, json={"contents":[{"parts":[{"text":prompt}]}]}, headers={"Content-Type":"application/json"}, timeout=20)
                            if res.status_code == 200:
                                ans = res.json()['candidates'][0]['content']['parts'][0]['text'].strip()
                                st.session_state.collab_messages.append({"role": "assistant", "content": ans})
                                st.rerun()
                        except Exception as ex:
                            st.error(f"Error: {ex}")


# ═══════════════════════════ VIEW 28: SETLIST BUILDER ═══════════════════════════
elif choice == "📋 Setlist Builder":
    st.markdown("""
    <div class="neon-grid-header neon-particle-bg">
        <div class="neon-heading">📋 AI Setlist Builder</div>
        <p style="color:rgba(255,255,255,0.45);font-size:0.88rem;margin:6px 0 0 0;">Generate a professionally paced concert setlist for any artist — with energy curves, encore planning, and crowd moment annotations.</p>
    </div>
    """, unsafe_allow_html=True)

    if not st.session_state.gemini_key:
        st.markdown("<div class='neon-card-pink' style='padding:20px;text-align:center;'>⚠️ Add your Gemini API Key to build setlists.</div>", unsafe_allow_html=True)
    else:
        col_sb1, col_sb2, col_sb3 = st.columns(3)
        with col_sb1:
            setlist_artist = st.text_input("Artist / Band", placeholder="e.g. Arctic Monkeys", key="setlist_artist")
        with col_sb2:
            setlist_duration = st.selectbox("Show Length", ["45 min", "60 min", "75 min", "90 min", "120 min", "150 min"], index=3, key="setlist_duration")
        with col_sb3:
            setlist_type = st.selectbox("Show Type", ["Club Night", "Festival Slot", "Arena Tour", "Intimate Acoustic", "Best-Of Retrospective", "New Album Promo"], key="setlist_type")

        if st.button("📋 Generate Setlist", use_container_width=True, key="setlist_gen"):
            if not setlist_artist.strip():
                st.warning("Enter an artist name first.")
            else:
                with st.spinner(f"Programming {setlist_artist}'s setlist..."):
                    url_g = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-2.5-flash:generateContent?key={st.session_state.gemini_key}"
                    prompt = f"""You are a professional concert tour manager. Build a setlist for {setlist_artist} — {setlist_type}, {setlist_duration}.
Return ONLY valid JSON (no fences):
{{"artist":"{setlist_artist}","show_type":"{setlist_type}","total_songs":12,"energy_arc":"description of energy flow","setlist":[{{"position":1,"title":"Song","year":"Year","energy":8,"note":"crowd moment annotation","segment":"opener/build/peak/cool-down/encore"}}],"encore":[{{"title":"Song","year":"Year","note":"why it closes the show"}}],"production_tip":"One sentence stage/lighting tip"}}"""
                    try:
                        res = requests.post(url_g, json={"contents":[{"parts":[{"text":prompt}]}]}, headers={"Content-Type":"application/json"}, timeout=22)
                        if res.status_code == 200:
                            raw = res.json()['candidates'][0]['content']['parts'][0]['text'].strip()
                            raw = re.sub(r'^```json\s*','',raw); raw = re.sub(r'\s*```$','',raw)
                            st.session_state.setlist_result = json.loads(raw)
                            st.rerun()
                    except Exception as ex:
                        st.error(f"Error: {ex}")

        sl = st.session_state.get("setlist_result")
        if sl:
            st.markdown(f"""
            <div class="neon-card-cyan neon-scanlines" style="margin-bottom:20px;">
                <div style="display:flex;justify-content:space-between;align-items:center;flex-wrap:wrap;gap:10px;">
                    <div>
                        <div class="neon-text-cyan" style="font-size:1.4rem;font-weight:800;">{sl.get('artist','')}</div>
                        <div style="color:rgba(255,255,255,0.4);font-size:0.8rem;margin-top:2px;">{sl.get('show_type','')} · {sl.get('total_songs',0)} songs</div>
                    </div>
                    <span class="neon-badge neon-badge-cyan">⚡ {sl.get('energy_arc','')[:40]}</span>
                </div>
            </div>
            """, unsafe_allow_html=True)
            seg_colors = {"opener":"#f43f5e","build":"#f97316","peak":"#a855f7","cool-down":"#06b6d4","encore":"#22c55e"}
            st.markdown("<p style='font-size:0.7rem;text-transform:uppercase;letter-spacing:0.1em;color:rgba(255,255,255,0.3);margin-bottom:10px;'>🎵 Main Set</p>", unsafe_allow_html=True)
            for track in sl.get("setlist", []):
                seg = track.get("segment","build")
                col = seg_colors.get(seg, "#a855f7")
                energy = track.get("energy", 5)
                energy_bar = "█" * energy + "░" * (10 - energy)
                tc1, tc2 = st.columns([6, 4])
                with tc1:
                    st.markdown(f"""
                    <div style="display:flex;align-items:center;gap:12px;background:rgba(8,4,18,0.7);border:1px solid {col}44;border-left:3px solid {col};border-radius:0 10px 10px 0;padding:10px 14px;margin-bottom:6px;box-shadow:0 0 8px {col}22;">
                        <span style="font-size:1rem;font-weight:800;color:{col};min-width:24px;text-shadow:0 0 8px {col};">{track.get('position','')}</span>
                        <div style="flex:1;overflow:hidden;">
                            <p style="font-weight:700;font-size:0.9rem;color:#fff;margin:0;">{track.get('title','')}</p>
                            <p style="font-size:0.7rem;color:rgba(255,255,255,0.4);margin:0;">{track.get('year','')} · <span style="color:{col};">{seg}</span></p>
                        </div>
                    </div>
                    """, unsafe_allow_html=True)
                with tc2:
                    st.markdown(f"""
                    <div style="padding-top:8px;">
                        <p style="font-size:0.62rem;color:rgba(255,255,255,0.3);font-family:monospace;margin:0 0 3px 0;">Energy <span style="color:{col};">{energy}/10</span></p>
                        <p style="font-size:0.62rem;font-family:monospace;color:{col};margin:0 0 4px 0;">{energy_bar}</p>
                        <p style="font-size:0.68rem;font-style:italic;color:rgba(255,255,255,0.4);margin:0;">{track.get('note','')}</p>
                    </div>
                    """, unsafe_allow_html=True)
            st.markdown("<div class='neon-sweep'></div>", unsafe_allow_html=True)
            st.markdown("<p style='font-size:0.7rem;text-transform:uppercase;letter-spacing:0.1em;color:rgba(255,255,255,0.3);margin-bottom:10px;'>🎤 Encore</p>", unsafe_allow_html=True)
            for et in sl.get("encore", []):
                st.markdown(f"""
                <div class="neon-card-green" style="margin-bottom:8px;">
                    <p style="font-weight:700;font-size:0.9rem;color:#4ade80;margin:0 0 3px 0;">🎤 {et.get('title','')} <span style="color:rgba(255,255,255,0.3);font-size:0.75rem;font-weight:400;">({et.get('year','')})</span></p>
                    <p style="font-size:0.76rem;color:rgba(255,255,255,0.5);margin:0;">{et.get('note','')}</p>
                </div>
                """, unsafe_allow_html=True)
            st.markdown(f"<div class='neon-card-orange' style='margin-top:8px;'><span class='neon-badge neon-badge-cyan' style='margin-bottom:6px;display:inline-block;'>💡 Production Tip</span><p style='color:rgba(255,255,255,0.7);font-size:0.85rem;margin:0;'>{sl.get('production_tip','')}</p></div>", unsafe_allow_html=True)
        else:
            st.markdown("""<div style="text-align:center;padding:50px 20px;color:rgba(255,255,255,0.25);">
                <div style="font-size:3.5rem;margin-bottom:14px;">📋</div>
                <p>Enter an artist and click <strong>Generate Setlist</strong></p>
            </div>""", unsafe_allow_html=True)


# ═══════════════════════════ VIEW 29: ARTIST BATTLE ═══════════════════════════
elif choice == "⚔️ Artist Battle":
    st.markdown("""
    <div class="neon-grid-header neon-particle-bg">
        <div class="neon-heading">⚔️ Artist Battle Arena</div>
        <p style="color:rgba(255,255,255,0.45);font-size:0.88rem;margin:6px 0 0 0;">Pit two artists head-to-head across 8 musical dimensions. AI judges every round.</p>
    </div>
    """, unsafe_allow_html=True)

    if not st.session_state.gemini_key:
        st.markdown("<div class='neon-card-pink' style='padding:20px;text-align:center;'>⚠️ Add your Gemini API Key to start battles.</div>", unsafe_allow_html=True)
    else:
        col_ab1, col_ab2, col_ab3 = st.columns([2, 0.3, 2])
        with col_ab1:
            artist1 = st.text_input("🔴 Artist 1", placeholder="e.g. Taylor Swift", key="battle_a1")
        with col_ab2:
            st.markdown("<div style='text-align:center;padding-top:32px;font-size:1.4rem;color:rgba(255,255,255,0.2);font-weight:900;'>VS</div>", unsafe_allow_html=True)
        with col_ab3:
            artist2 = st.text_input("🔵 Artist 2", placeholder="e.g. Beyoncé", key="battle_a2")

        if st.button("⚔️ Start Battle", use_container_width=True, key="battle_go"):
            if not artist1.strip() or not artist2.strip():
                st.warning("Enter both artist names.")
            else:
                with st.spinner(f"Judging {artist1} vs {artist2}..."):
                    url_g = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-2.5-flash:generateContent?key={st.session_state.gemini_key}"
                    prompt = f"""You are an expert music critic and judge. Compare {artist1} vs {artist2} across 8 musical dimensions.
Return ONLY valid JSON (no fences):
{{"artist1":"{artist1}","artist2":"{artist2}","rounds":[{{"dimension":"Vocal Range","a1_score":8,"a2_score":7,"a1_note":"brief","a2_note":"brief","winner":"artist1"}}],"final_winner":"artist name","final_verdict":"2 sentence verdict","a1_strengths":["s1","s2","s3"],"a2_strengths":["s1","s2","s3"]}}
Provide all 8 rounds for: Vocal Range, Lyricism, Stage Presence, Commercial Impact, Critical Acclaim, Discography Depth, Innovation, Cultural Impact."""
                    try:
                        res = requests.post(url_g, json={"contents":[{"parts":[{"text":prompt}]}]}, headers={"Content-Type":"application/json"}, timeout=25)
                        if res.status_code == 200:
                            raw = res.json()['candidates'][0]['content']['parts'][0]['text'].strip()
                            raw = re.sub(r'^```json\s*','',raw); raw = re.sub(r'\s*```$','',raw)
                            st.session_state.artist_battle_result = json.loads(raw)
                            st.rerun()
                    except Exception as ex:
                        st.error(f"Error: {ex}")

        br = st.session_state.get("artist_battle_result")
        if br:
            a1_wins = sum(1 for r in br.get("rounds",[]) if r.get("winner") == "artist1")
            a2_wins = sum(1 for r in br.get("rounds",[]) if r.get("winner") == "artist2")
            winner = br.get("final_winner","")
            st.markdown(f"""
            <div style="display:grid;grid-template-columns:1fr auto 1fr;gap:16px;margin-bottom:22px;align-items:center;">
                <div class="neon-card-pink" style="text-align:center;">
                    <div class="neon-text-pink" style="font-size:1.5rem;font-weight:800;">{br.get('artist1','')}</div>
                    <div style="font-size:3rem;font-weight:900;color:#f43f5e;text-shadow:0 0 20px rgba(244,63,94,0.7);">{a1_wins}</div>
                    <div style="font-size:0.7rem;color:rgba(255,255,255,0.35);">rounds won</div>
                </div>
                <div style="text-align:center;font-size:1.8rem;font-weight:900;color:rgba(255,255,255,0.15);">⚔️</div>
                <div class="neon-card-purple" style="text-align:center;">
                    <div class="neon-text-purple" style="font-size:1.5rem;font-weight:800;">{br.get('artist2','')}</div>
                    <div style="font-size:3rem;font-weight:900;color:#a855f7;text-shadow:0 0 20px rgba(168,85,247,0.7);">{a2_wins}</div>
                    <div style="font-size:0.7rem;color:rgba(255,255,255,0.35);">rounds won</div>
                </div>
            </div>
            <div class="neon-card-cyan neon-scanlines" style="text-align:center;margin-bottom:22px;">
                <div style="font-size:0.7rem;text-transform:uppercase;letter-spacing:0.15em;color:rgba(255,255,255,0.3);margin-bottom:6px;">🏆 WINNER</div>
                <div class="neon-text-cyan" style="font-size:2rem;font-weight:900;">{winner}</div>
                <p style="color:rgba(255,255,255,0.55);font-size:0.85rem;margin:10px 0 0 0;font-style:italic;">{br.get('final_verdict','')}</p>
            </div>
            """, unsafe_allow_html=True)
            st.markdown("<p style='font-size:0.7rem;text-transform:uppercase;letter-spacing:0.1em;color:rgba(255,255,255,0.3);margin-bottom:12px;'>📊 Round-by-Round Breakdown</p>", unsafe_allow_html=True)
            for rnd in br.get("rounds", []):
                w = rnd.get("winner","")
                s1, s2 = rnd.get("a1_score",5), rnd.get("a2_score",5)
                w_col = "#f43f5e" if w == "artist1" else "#a855f7"
                rc1, rc2, rc3 = st.columns([3, 1, 3])
                with rc1:
                    st.markdown(f"<div style='text-align:right;padding:8px 12px;background:rgba(244,63,94,0.05);border-right:2px solid rgba(244,63,94,0.2);border-radius:8px 0 0 8px;'><span style='font-size:1.1rem;font-weight:700;color:#f43f5e;'>{s1}</span><span style='font-size:0.72rem;color:rgba(255,255,255,0.4);display:block;'>{rnd.get('a1_note','')}</span></div>", unsafe_allow_html=True)
                with rc2:
                    st.markdown(f"<div style='text-align:center;padding:8px 0;'><span style='font-size:0.65rem;font-weight:700;color:{w_col};text-transform:uppercase;'>{rnd.get('dimension','')}</span></div>", unsafe_allow_html=True)
                with rc3:
                    st.markdown(f"<div style='padding:8px 12px;background:rgba(168,85,247,0.05);border-left:2px solid rgba(168,85,247,0.2);border-radius:0 8px 8px 0;'><span style='font-size:1.1rem;font-weight:700;color:#a855f7;'>{s2}</span><span style='font-size:0.72rem;color:rgba(255,255,255,0.4);display:block;'>{rnd.get('a2_note','')}</span></div>", unsafe_allow_html=True)
                st.markdown("<div style='height:4px;'></div>", unsafe_allow_html=True)
        else:
            st.markdown("""<div style="text-align:center;padding:50px 20px;color:rgba(255,255,255,0.25);">
                <div style="font-size:3.5rem;margin-bottom:14px;">⚔️</div>
                <p>Enter two artists and click <strong>Start Battle</strong></p>
            </div>""", unsafe_allow_html=True)


# ═══════════════════════════ VIEW 30: MUSIC TIMELINE ═══════════════════════════
elif choice == "🕰️ Music Timeline":
    st.markdown("""
    <div class="neon-grid-header neon-particle-bg">
        <div class="neon-heading">🕰️ Music History Timeline</div>
        <p style="color:rgba(255,255,255,0.45);font-size:0.88rem;margin:6px 0 0 0;">Explore any artist's or genre's full discography and cultural evolution as an interactive neon timeline.</p>
    </div>
    """, unsafe_allow_html=True)

    if not st.session_state.gemini_key:
        st.markdown("<div class='neon-card-pink' style='padding:20px;text-align:center;'>⚠️ Add your Gemini API Key to build timelines.</div>", unsafe_allow_html=True)
    else:
        col_tl1, col_tl2 = st.columns([3, 2])
        with col_tl1:
            tl_subject = st.text_input("Artist, Band, or Genre", placeholder="e.g. David Bowie / Hip-Hop / Punk Rock", key="timeline_subject")
        with col_tl2:
            tl_focus = st.selectbox("Focus", ["Albums & Singles", "Cultural Impact", "Genre Evolution", "Artist Career Arc", "Collaborations"], key="timeline_focus")

        if st.button("🕰️ Build Timeline", use_container_width=True, key="timeline_build"):
            if not tl_subject.strip():
                st.warning("Enter a subject.")
            else:
                with st.spinner(f"Assembling timeline for {tl_subject}..."):
                    url_g = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-2.5-flash:generateContent?key={st.session_state.gemini_key}"
                    prompt = f"""Build a music history timeline for: "{tl_subject}" focused on "{tl_focus}".
Return ONLY valid JSON (no fences):
{{"subject":"{tl_subject}","focus":"{tl_focus}","summary":"2-sentence overview","events":[{{"year":"1975","title":"Event/Album title","description":"2 sentences","impact":"High/Medium/Low","type":"album/single/event/milestone/collaboration","color":"#hex neon color"}}]}}
Include 10-14 events in chronological order."""
                    try:
                        res = requests.post(url_g, json={"contents":[{"parts":[{"text":prompt}]}]}, headers={"Content-Type":"application/json"}, timeout=25)
                        if res.status_code == 200:
                            raw = res.json()['candidates'][0]['content']['parts'][0]['text'].strip()
                            raw = re.sub(r'^```json\s*','',raw); raw = re.sub(r'\s*```$','',raw)
                            st.session_state.music_timeline = json.loads(raw)
                            st.rerun()
                    except Exception as ex:
                        st.error(f"Error: {ex}")

        tl = st.session_state.get("music_timeline")
        if tl:
            st.markdown(f"""
            <div class="neon-card-purple" style="margin-bottom:20px;">
                <div class="neon-text-purple" style="font-size:1.4rem;font-weight:800;margin-bottom:6px;">{tl.get('subject','')} — {tl.get('focus','')}</div>
                <p style="color:rgba(255,255,255,0.55);font-size:0.86rem;margin:0;">{tl.get('summary','')}</p>
            </div>
            """, unsafe_allow_html=True)
            type_icons = {"album":"💿","single":"🎵","event":"⚡","milestone":"🏆","collaboration":"🤝"}
            impact_size = {"High":"1rem","Medium":"0.88rem","Low":"0.78rem"}
            for i, ev in enumerate(tl.get("events", [])):
                ev_color = ev.get("color","#a855f7")
                icon = type_icons.get(ev.get("type","event"), "🎵")
                side = i % 2 == 0
                imp = ev.get("impact","Medium")
                imp_fs = impact_size.get(imp, "0.88rem")
                ev_col1, ev_col2, ev_col3 = st.columns([2, 0.2, 8] if side else [8, 0.2, 2])
                if side:
                    with ev_col1:
                        st.markdown(f"<div style='text-align:right;padding-top:8px;'><span style='font-size:1.1rem;font-weight:800;color:{ev_color};text-shadow:0 0 10px {ev_color};'>{ev.get('year','')}</span></div>", unsafe_allow_html=True)
                    with ev_col2:
                        st.markdown(f"<div style='display:flex;flex-direction:column;align-items:center;padding-top:2px;'><div style='width:12px;height:12px;border-radius:50%;background:{ev_color};box-shadow:0 0 10px {ev_color};margin-bottom:2px;'></div><div style='width:1px;background:linear-gradient({ev_color},transparent);flex:1;min-height:40px;'></div></div>", unsafe_allow_html=True)
                    with ev_col3:
                        st.markdown(f"<div style='background:rgba(8,4,18,0.8);border:1px solid {ev_color}55;border-left:3px solid {ev_color};border-radius:0 12px 12px 0;padding:12px 16px;margin-bottom:12px;box-shadow:0 0 10px {ev_color}22;'><p style='font-size:{imp_fs};font-weight:700;color:#fff;margin:0 0 4px 0;'>{icon} {ev.get('title','')}</p><p style='font-size:0.78rem;color:rgba(255,255,255,0.55);margin:0 0 4px 0;'>{ev.get('description','')}</p><span class='neon-badge' style='background:{ev_color}18;border:1px solid {ev_color}44;color:{ev_color};box-shadow:0 0 6px {ev_color}44;font-size:0.6rem;padding:2px 8px;border-radius:20px;'>{imp} Impact</span></div>", unsafe_allow_html=True)
                else:
                    with ev_col1:
                        st.markdown(f"<div style='background:rgba(8,4,18,0.8);border:1px solid {ev_color}55;border-right:3px solid {ev_color};border-radius:12px 0 0 12px;padding:12px 16px;margin-bottom:12px;box-shadow:0 0 10px {ev_color}22;'><p style='font-size:{imp_fs};font-weight:700;color:#fff;margin:0 0 4px 0;'>{icon} {ev.get('title','')}</p><p style='font-size:0.78rem;color:rgba(255,255,255,0.55);margin:0 0 4px 0;'>{ev.get('description','')}</p><span class='neon-badge' style='background:{ev_color}18;border:1px solid {ev_color}44;color:{ev_color};box-shadow:0 0 6px {ev_color}44;font-size:0.6rem;padding:2px 8px;border-radius:20px;'>{imp} Impact</span></div>", unsafe_allow_html=True)
                    with ev_col2:
                        st.markdown(f"<div style='display:flex;flex-direction:column;align-items:center;padding-top:2px;'><div style='width:12px;height:12px;border-radius:50%;background:{ev_color};box-shadow:0 0 10px {ev_color};margin-bottom:2px;'></div><div style='width:1px;background:linear-gradient({ev_color},transparent);flex:1;min-height:40px;'></div></div>", unsafe_allow_html=True)
                    with ev_col3:
                        st.markdown(f"<div style='text-align:left;padding-top:8px;'><span style='font-size:1.1rem;font-weight:800;color:{ev_color};text-shadow:0 0 10px {ev_color};'>{ev.get('year','')}</span></div>", unsafe_allow_html=True)
        else:
            st.markdown("""<div style="text-align:center;padding:50px 20px;color:rgba(255,255,255,0.25);">
                <div style="font-size:3.5rem;margin-bottom:14px;">🕰️</div>
                <p>Enter an artist or genre and click <strong>Build Timeline</strong></p>
            </div>""", unsafe_allow_html=True)


# ═══════════════════════════ VIEW 31: COVER ART LAB ═══════════════════════════
elif choice == "🎬 Cover Art Lab":
    st.markdown("""
    <div class="neon-grid-header neon-particle-bg">
        <div class="neon-heading">🎬 Cover Art Lab</div>
        <p style="color:rgba(255,255,255,0.45);font-size:0.88rem;margin:6px 0 0 0;">AI generates detailed visual prompts, colour palettes, and art direction briefs for album or single cover art.</p>
    </div>
    """, unsafe_allow_html=True)

    if not st.session_state.gemini_key:
        st.markdown("<div class='neon-card-pink' style='padding:20px;text-align:center;'>⚠️ Add your Gemini API Key to use Cover Art Lab.</div>", unsafe_allow_html=True)
    else:
        col_ca1, col_ca2 = st.columns(2)
        with col_ca1:
            ca_title = st.text_input("Album / Single Title", placeholder="e.g. Midnight Reverie", key="ca_title")
            ca_artist = st.text_input("Artist Name", placeholder="e.g. Luna Vex", key="ca_artist")
            ca_genre = st.selectbox("Genre", ["Pop", "Hip-Hop", "Electronic", "Rock", "R&B", "Indie", "Jazz", "Metal", "Classical", "Ambient"], key="ca_genre")
        with col_ca2:
            ca_style = st.selectbox("Visual Style", ["Cyberpunk Neon", "Minimalist", "Abstract Expressionist", "Vintage Analog", "Surrealist", "Dark Academia", "Vaporwave", "Psychedelic", "Photorealistic", "Brutalist"], key="ca_style")
            ca_mood = st.selectbox("Emotional Tone", ["Euphoric", "Melancholic", "Powerful", "Dreamy", "Dark", "Nostalgic", "Defiant", "Romantic", "Mysterious"], key="ca_mood")
            ca_format = st.radio("Format", ["Album Cover (Square)", "Single Cover", "EP Cover", "Tour Poster"], horizontal=True, key="ca_format")

        if st.button("🎨 Generate Art Direction", use_container_width=True, key="ca_gen"):
            if not ca_title.strip():
                st.warning("Enter a title.")
            else:
                with st.spinner("Art director is conceptualising..."):
                    url_g = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-2.5-flash:generateContent?key={st.session_state.gemini_key}"
                    prompt = f"""You are a world-class album art director. Create a complete cover art brief for:
Title: "{ca_title}" by {ca_artist or 'Unknown Artist'} | Genre: {ca_genre} | Style: {ca_style} | Mood: {ca_mood} | Format: {ca_format}
Return ONLY valid JSON (no fences):
{{"title":"{ca_title}","concept":"3-sentence visual concept","palette":[{{"hex":"#hex","name":"color name","role":"how it's used"}}],"composition":"detailed layout description","focal_element":"main visual subject","typography_style":"font/text treatment suggestion","texture_details":"surface/material textures","lighting":"lighting direction and quality","ai_image_prompt":"A detailed 100-word prompt ready to paste into Midjourney or DALL-E","dont_use":["element to avoid 1","element to avoid 2","element to avoid 3"],"inspiration_refs":["Reference artwork/artist 1","Ref 2","Ref 3"]}}
Include 5 palette colors."""
                    try:
                        res = requests.post(url_g, json={"contents":[{"parts":[{"text":prompt}]}]}, headers={"Content-Type":"application/json"}, timeout=22)
                        if res.status_code == 200:
                            raw = res.json()['candidates'][0]['content']['parts'][0]['text'].strip()
                            raw = re.sub(r'^```json\s*','',raw); raw = re.sub(r'\s*```$','',raw)
                            st.session_state.cover_art_result = json.loads(raw)
                            st.rerun()
                    except Exception as ex:
                        st.error(f"Error: {ex}")

        ca = st.session_state.get("cover_art_result")
        if ca:
            st.markdown(f"""
            <div class="neon-card-pink neon-scanlines" style="margin-bottom:20px;">
                <div class="neon-text-pink" style="font-size:1.3rem;font-weight:800;margin-bottom:6px;">🎨 {ca.get('title','')}</div>
                <p style="color:rgba(255,255,255,0.65);font-size:0.88rem;line-height:1.6;margin:0;">{ca.get('concept','')}</p>
            </div>
            """, unsafe_allow_html=True)
            col_pal, col_comp = st.columns(2)
            with col_pal:
                st.markdown("<p style='font-size:0.7rem;text-transform:uppercase;letter-spacing:0.1em;color:rgba(255,255,255,0.3);margin-bottom:10px;'>🎨 Colour Palette</p>", unsafe_allow_html=True)
                for c in ca.get("palette", []):
                    hx = c.get("hex","#333")
                    st.markdown(f"""
                    <div style="display:flex;align-items:center;gap:12px;background:rgba(8,4,18,0.6);border:1px solid {hx}44;border-radius:10px;padding:8px 12px;margin-bottom:6px;">
                        <div style="width:36px;height:36px;border-radius:8px;background:{hx};box-shadow:0 0 10px {hx}88;flex-shrink:0;"></div>
                        <div>
                            <p style="font-weight:700;font-size:0.82rem;color:#fff;margin:0;">{c.get('name','')}</p>
                            <p style="font-size:0.68rem;color:rgba(255,255,255,0.4);margin:0;font-family:monospace;">{hx} · {c.get('role','')}</p>
                        </div>
                    </div>
                    """, unsafe_allow_html=True)
            with col_comp:
                st.markdown("<p style='font-size:0.7rem;text-transform:uppercase;letter-spacing:0.1em;color:rgba(255,255,255,0.3);margin-bottom:10px;'>🖼️ Composition Details</p>", unsafe_allow_html=True)
                for label, val in [("📐 Layout", ca.get('composition','')), ("🎯 Focal Element", ca.get('focal_element','')), ("✍️ Typography", ca.get('typography_style','')), ("🔆 Lighting", ca.get('lighting','')), ("🪨 Textures", ca.get('texture_details',''))]:
                    st.markdown(f"<div style='background:rgba(8,4,18,0.6);border:1px solid rgba(255,255,255,0.06);border-radius:10px;padding:8px 12px;margin-bottom:6px;'><p style='font-size:0.65rem;color:rgba(255,255,255,0.3);margin:0 0 2px 0;'>{label}</p><p style='font-size:0.8rem;color:rgba(255,255,255,0.7);margin:0;'>{val}</p></div>", unsafe_allow_html=True)
            st.markdown("<div class='neon-sweep'></div>", unsafe_allow_html=True)
            st.markdown("<p style='font-size:0.7rem;text-transform:uppercase;letter-spacing:0.1em;color:rgba(255,255,255,0.3);margin-bottom:8px;'>🤖 AI Image Generation Prompt</p>", unsafe_allow_html=True)
            st.markdown(f"""
            <div class="neon-card-cyan" style="margin-bottom:14px;">
                <p style="font-size:0.85rem;color:rgba(255,255,255,0.75);line-height:1.7;margin:0;font-style:italic;">"{ca.get('ai_image_prompt','')}"</p>
            </div>
            """, unsafe_allow_html=True)
            col_ref, col_avoid = st.columns(2)
            with col_ref:
                st.markdown("<p style='font-size:0.7rem;text-transform:uppercase;letter-spacing:0.1em;color:rgba(255,255,255,0.3);margin-bottom:8px;'>💡 Inspiration References</p>", unsafe_allow_html=True)
                for ref in ca.get("inspiration_refs", []):
                    st.markdown(f"<p style='color:rgba(255,255,255,0.55);font-size:0.8rem;padding:3px 0;border-bottom:1px solid rgba(255,255,255,0.04);margin:0;'>🎨 {ref}</p>", unsafe_allow_html=True)
            with col_avoid:
                st.markdown("<p style='font-size:0.7rem;text-transform:uppercase;letter-spacing:0.1em;color:rgba(255,255,255,0.3);margin-bottom:8px;'>🚫 Avoid</p>", unsafe_allow_html=True)
                for av in ca.get("dont_use", []):
                    st.markdown(f"<p style='color:rgba(244,63,94,0.6);font-size:0.8rem;padding:3px 0;border-bottom:1px solid rgba(255,255,255,0.04);margin:0;'>✗ {av}</p>", unsafe_allow_html=True)
        else:
            st.markdown("""<div style="text-align:center;padding:50px 20px;color:rgba(255,255,255,0.25);">
                <div style="font-size:3.5rem;margin-bottom:14px;">🎨</div>
                <p>Fill in the details above and click <strong>Generate Art Direction</strong></p>
            </div>""", unsafe_allow_html=True)


# ═══════════════════════════ VIEW 32: CROSSFADE MIXER ═══════════════════════════
elif choice == "🌀 Crossfade Mixer":
    st.markdown("""
    <div class="neon-grid-header neon-particle-bg">
        <div class="neon-heading">🌀 Crossfade Mixer</div>
        <p style="color:rgba(255,255,255,0.45);font-size:0.88rem;margin:6px 0 0 0;">Visually arrange your queue into a DJ-style crossfade set. Drag tracks, set transition times, and export as an ordered playlist.</p>
    </div>
    """, unsafe_allow_html=True)

    cf_queue = st.session_state.get("queue", [])
    if not cf_queue:
        st.markdown("""
        <div class="neon-card-purple" style="text-align:center;padding:30px;">
            <div style="font-size:3rem;margin-bottom:12px;">🎵</div>
            <p style="color:rgba(255,255,255,0.5);">Your play queue is empty. Go to <strong>Search Songs</strong> and add tracks to the queue first.</p>
        </div>
        """, unsafe_allow_html=True)
    else:
        st.markdown(f"<p style='color:rgba(255,255,255,0.4);font-size:0.8rem;margin-bottom:16px;'>{len(cf_queue)} tracks in queue — set crossfade time for each transition below</p>", unsafe_allow_html=True)

        crossfade_html_tracks = ""
        for i, track in enumerate(cf_queue):
            m, s = divmod(int(track.get('duration', 180)), 60)
            crossfade_html_tracks += f"""
            <div class="cf-track" id="cf-{i}">
                <img src="{track.get('thumbnail','')}" class="cf-thumb" onerror="this.style.background='#1a0a2e'">
                <div class="cf-info">
                    <p class="cf-title">{track.get('title','')[:38]}{'…' if len(track.get('title',''))>38 else ''}</p>
                    <p class="cf-artist">{track.get('uploader','')}</p>
                </div>
                <span class="cf-dur">{m:02d}:{s:02d}</span>
                <div class="cf-num">{i+1}</div>
            </div>
            {"<div class='cf-arrow'>⬇ Crossfade <span class='cf-fade-val' id='fade-val-" + str(i) + "'>3s</span> <input type='range' class='cf-slider' min='1' max='10' value='3' oninput=\"document.getElementById('fade-val-" + str(i) + "').innerText=this.value+'s'\" title='Crossfade duration'></div>" if i < len(cf_queue)-1 else ""}
            """

        mixer_html = f"""<!DOCTYPE html><html><head><meta charset="UTF-8">
        <style>
        *{{box-sizing:border-box;margin:0;padding:0;}}
        body{{font-family:'Outfit',sans-serif;background:transparent;color:#f3f4f6;padding:8px;}}
        .cf-track{{display:flex;align-items:center;gap:12px;background:rgba(8,4,18,0.8);
            border:1px solid rgba(168,85,247,0.2);border-radius:12px;padding:10px 14px;margin-bottom:4px;transition:all 0.2s;}}
        .cf-track:hover{{border-color:rgba(168,85,247,0.5);box-shadow:0 0 12px rgba(168,85,247,0.2);transform:translateX(3px);}}
        .cf-thumb{{width:40px;height:40px;border-radius:7px;object-fit:cover;border:1px solid rgba(168,85,247,0.3);flex-shrink:0;background:#1a0a2e;}}
        .cf-info{{flex:1;overflow:hidden;}}
        .cf-title{{font-size:0.82rem;font-weight:700;color:#fff;white-space:nowrap;overflow:hidden;text-overflow:ellipsis;margin:0;}}
        .cf-artist{{font-size:0.68rem;color:rgba(255,255,255,0.4);margin:0;}}
        .cf-dur{{font-size:0.68rem;font-family:monospace;color:rgba(255,255,255,0.3);flex-shrink:0;}}
        .cf-num{{width:22px;height:22px;border-radius:50%;background:rgba(168,85,247,0.15);border:1px solid rgba(168,85,247,0.3);
            display:flex;align-items:center;justify-content:center;font-size:0.6rem;font-weight:700;color:#c084fc;flex-shrink:0;}}
        .cf-arrow{{text-align:center;font-size:0.7rem;color:rgba(255,255,255,0.3);padding:4px 0;display:flex;align-items:center;justify-content:center;gap:10px;}}
        .cf-fade-val{{color:#22d3ee;font-weight:700;}}
        .cf-slider{{-webkit-appearance:none;width:100px;height:4px;border-radius:2px;background:rgba(6,182,212,0.2);outline:none;}}
        .cf-slider::-webkit-slider-thumb{{-webkit-appearance:none;width:12px;height:12px;border-radius:50%;background:#06b6d4;box-shadow:0 0 6px rgba(6,182,212,0.5);cursor:pointer;}}
        </style></head><body>
        <div id="cf-container">{crossfade_html_tracks}</div>
        </body></html>"""

        components.html(mixer_html, height=min(64 * len(cf_queue) + 60, 600))

        col_cx1, col_cx2, col_cx3 = st.columns(3)
        with col_cx1:
            if st.button("🔀 Shuffle Order", use_container_width=True, key="cf_shuffle"):
                import random
                random.shuffle(st.session_state.queue)
                st.toast("Crossfade order shuffled!")
                st.rerun()
        with col_cx2:
            if st.button("⚡ Play First Track", use_container_width=True, key="cf_play_first"):
                if cf_queue:
                    play_song(cf_queue[0])
        with col_cx3:
            if st.button("🗑️ Clear Queue", use_container_width=True, key="cf_clear"):
                st.session_state.queue = []
                st.session_state.queue_index = 0
                st.toast("Queue cleared!")
                st.rerun()
