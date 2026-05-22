import re
import requests
from typing import List, Dict, Any, Optional

class LyricsProvider:
    def __init__(self):
        self.headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36"
        }
        self.lrclib_url = "https://lrclib.net/api/search"
        self.lyrics_ovh_url = "https://api.lyrics.ovh/v1"
        self.netease_search_url = "https://music.163.com/api/search/get/web"
        self.netease_lyric_url = "https://music.163.com/api/song/lyric"
        self.chartlyrics_url = "http://api.chartlyrics.com/apiv1.asmx/SearchLyricDirect"
        self.happi_url = "https://api.happi.dev/v1/music"

    # ─── LrcLib (Best: real synced LRC) ──────────────────────────────────────
    def search_lyrics(self, query: str) -> List[Dict[str, Any]]:
        """Search LRCLIB for lyrics based on the query."""
        if not query.strip():
            return []
        try:
            params = {"q": query}
            res = requests.get(self.lrclib_url, params=params, headers=self.headers, timeout=8)
            if res.status_code == 200:
                return res.json()
            return []
        except Exception as e:
            print(f"[LrcLib] Error: {e}")
            return []

    # ─── Lyrics.ovh (Plain text fallback) ────────────────────────────────────
    def get_lyrics_ovh(self, artist: str, title: str) -> Optional[str]:
        """Fetch plain text lyrics from lyrics.ovh."""
        if not artist or not title:
            return None
        try:
            url = f"{self.lyrics_ovh_url}/{requests.utils.quote(artist)}/{requests.utils.quote(title)}"
            res = requests.get(url, headers=self.headers, timeout=6)
            if res.status_code == 200:
                data = res.json()
                lyrics = data.get("lyrics", "")
                return lyrics if lyrics and len(lyrics) > 20 else None
            return None
        except Exception as e:
            print(f"[Lyrics.ovh] Error: {e}")
            return None

    # ─── NetEase Cloud Music (Best for Hindi / Asian / multi-language synced) ─
    def get_lyrics_netease(self, artist: str, title: str) -> Optional[Dict[str, str]]:
        """
        Fetch synced LRC + plain lyrics from NetEase Cloud Music.
        Extremely strong for Hindi, Korean, Japanese, Chinese, and Tamil songs.
        Returns dict with 'synced' (LRC string) and 'plain' (plain text).
        """
        query = f"{artist} {title}".strip()
        if not query:
            return None

        netease_headers = {
            **self.headers,
            "Referer": "https://music.163.com",
            "Origin": "https://music.163.com"
        }

        try:
            # Step 1: Search for song ID
            params = {"s": query, "type": 1, "limit": 3}
            res = requests.get(
                self.netease_search_url, params=params,
                headers=netease_headers, timeout=5
            )
            if res.status_code != 200:
                return None

            data = res.json()
            songs = data.get("result", {}).get("songs", [])
            if not songs:
                return None

            song_id = songs[0].get("id")
            if not song_id:
                return None

            # Step 2: Fetch LRC lyrics
            lyric_params = {"id": song_id, "lv": 1, "kv": 1, "tv": -1}
            lyric_res = requests.get(
                self.netease_lyric_url, params=lyric_params,
                headers=netease_headers, timeout=5
            )
            if lyric_res.status_code != 200:
                return None

            lyric_data = lyric_res.json()
            synced_lrc = lyric_data.get("lrc", {}).get("lyric", "")
            
            if not synced_lrc or len(synced_lrc.strip()) < 20:
                return None

            # Strip LRC timestamps to get plain text
            plain = re.sub(r'\[\d+:\d+\.\d+\]', '', synced_lrc)
            plain = "\n".join(
                line.strip() for line in plain.split("\n")
                if line.strip() and not line.strip().startswith("[")
            )

            return {"synced": synced_lrc, "plain": plain}

        except Exception as e:
            print(f"[NetEase] Error: {e}")
            return None

    # ─── Chartlyrics (Free open XML API, plain text) ─────────────────────────
    def get_lyrics_chartlyrics(self, artist: str, title: str) -> Optional[str]:
        """
        Fetch plain text lyrics from Chartlyrics SOAP/XML API.
        Good for English pop/rock songs not in other databases.
        """
        if not artist or not title:
            return None
        try:
            params = {
                "artist": artist,
                "song": title
            }
            res = requests.get(
                self.chartlyrics_url, params=params,
                headers=self.headers, timeout=7
            )
            if res.status_code != 200:
                return None

            xml = res.text
            # Parse <Lyric> tag from SOAP XML response
            match = re.search(r'<Lyric>(.*?)</Lyric>', xml, re.DOTALL)
            if match:
                lyrics = match.group(1).strip()
                # Unescape XML entities
                lyrics = lyrics.replace("&amp;", "&").replace("&lt;", "<").replace("&gt;", ">").replace("&apos;", "'").replace("&quot;", '"')
                return lyrics if len(lyrics) > 30 else None
            return None
        except Exception as e:
            print(f"[Chartlyrics] Error: {e}")
            return None

    # ─── Happi.dev Music API (Hindi / Bollywood strong, many languages) ───────
    def get_lyrics_happi(self, artist: str, title: str, api_key: str = "") -> Optional[str]:
        """
        Fetch lyrics from Happi.dev music API.
        Very good for Bollywood/Hindi songs. Requires free API key from happi.dev.
        Falls back gracefully if no key provided.
        """
        if not api_key or not artist or not title:
            return None
        try:
            search_url = f"{self.happi_url}?q={requests.utils.quote(title + ' ' + artist)}&limit=3&type=1&apikey={api_key}"
            res = requests.get(search_url, headers=self.headers, timeout=6)
            if res.status_code != 200:
                return None
            
            data = res.json()
            results = data.get("result", [])
            if not results:
                return None
            
            # Get first result's lyrics endpoint
            first = results[0]
            lyrics_url = first.get("api_lyrics")
            if not lyrics_url:
                return None
            
            lyric_res = requests.get(f"{lyrics_url}?apikey={api_key}", headers=self.headers, timeout=6)
            if lyric_res.status_code != 200:
                return None
            
            lyric_data = lyric_res.json()
            lyrics_text = lyric_data.get("result", {}).get("lyrics", "")
            return lyrics_text if len(lyrics_text) > 30 else None
        except Exception as e:
            print(f"[Happi.dev] Error: {e}")
            return None

    # ─── Megalobiz Synced LRC Scraper ────────────────────────────────────────
    def get_lyrics_megalobiz(self, artist: str, title: str) -> Optional[str]:
        """Fetch synced LRC lyrics from Megalobiz."""
        query = f"{artist} {title}".strip()
        if not query:
            return None
        search_url = f"https://www.megalobiz.com/search/all?qry={requests.utils.quote(query)}"
        try:
            res = requests.get(search_url, headers=self.headers, timeout=10)
            if res.status_code != 200:
                return None
                
            html = res.text
            link_pattern = re.compile(r'href="(/lrc/playlist/[^"]+)"')
            links = link_pattern.findall(html)
            if not links:
                return None
                
            song_url = f"https://www.megalobiz.com{links[0]}"
            song_res = requests.get(song_url, headers=self.headers, timeout=10)
            if song_res.status_code != 200:
                return None
                
            song_html = song_res.text
            lrc_pattern = re.compile(r'id="lrc_content"[^>]*>(.*?)</span>', re.DOTALL)
            match = lrc_pattern.search(song_html)
            if not match:
                lrc_pattern = re.compile(r'id="lrc_content"[^>]*>(.*?)</div>', re.DOTALL)
                match = lrc_pattern.search(song_html)
                
            if not match:
                return None
                
            lrc_text = match.group(1).strip()
            lrc_text = lrc_text.replace("&quot;", '"').replace("&amp;", "&").replace("&lt;", "<").replace("&gt;", ">").replace("<br />", "\n").replace("<br>", "\n")
            return lrc_text if len(lrc_text) > 30 else None
        except Exception as e:
            print(f"[Megalobiz] Error: {e}")
            return None

    # ─── Syncedlyrics Integration ───────────────────────────────────────────
    def get_lyrics_syncedlyrics(self, artist: str, title: str, allow_plain: bool = False) -> Optional[str]:
        """Fetch synced lyrics using the syncedlyrics python package.
        
        Searches Musixmatch, NetEase, LrcLib, and Deezer backends.
        Set allow_plain=True to also accept plain (non-synced) results.
        """
        query = f"{artist} {title}".strip()
        if not query:
            return None
        try:
            import syncedlyrics
            # First try to get synced (timestamped) lyrics
            lrc = syncedlyrics.search(query, allow_plain_format=allow_plain)
            if lrc and len(lrc.strip()) > 30:
                return lrc
            # If allow_plain, the library may have returned plain text; that's fine
            return None
        except TypeError:
            # Older syncedlyrics versions don't have allow_plain_format
            try:
                import syncedlyrics
                lrc = syncedlyrics.search(query)
                return lrc if lrc and len(lrc.strip()) > 30 else None
            except Exception as e2:
                print(f"[syncedlyrics] Error: {e2}")
                return None
        except Exception as e:
            print(f"[syncedlyrics] Error: {e}")
            return None

    # ─── YouTube Subtitles/Captions Provider ─────────────────────────────────
    def get_lyrics_youtube_captions(self, video_id: str) -> Optional[Dict[str, str]]:
        """Fetch and parse subtitles/captions directly from the YouTube video."""
        if not video_id:
            return None
        import yt_dlp
        
        ydl_opts = {
            'skip_download': True,
            'writesubtitles': True,
            'writeautomaticsub': True,
            'subtitlesformat': 'json3/vtt/srt',
            'quiet': True,
            'no_warnings': True,
        }
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            try:
                info = ydl.extract_info(f"https://www.youtube.com/watch?v={video_id}", download=False)
                subtitles = info.get('subtitles', {})
                auto = info.get('automatic_captions', {})
                
                # Check languages in order of preference: English, Hindi, Spanish, Japanese, others
                pref_langs = ['en', 'hi', 'en-US', 'es', 'ja']
                sub_list = None
                
                # Search manuals
                for plang in pref_langs:
                    for k in subtitles.keys():
                        if k == plang or k.startswith(plang + '-'):
                            sub_list = subtitles[k]
                            break
                    if sub_list:
                        break
                
                # Search autos
                if not sub_list:
                    for plang in pref_langs:
                        for k in auto.keys():
                            if k == plang or k.startswith(plang + '-'):
                                sub_list = auto[k]
                                break
                        if sub_list:
                            break
                
                # Default fallbacks
                if not sub_list and subtitles:
                    sub_list = subtitles[list(subtitles.keys())[0]]
                if not sub_list and auto:
                    sub_list = auto[list(auto.keys())[0]]
                    
                if not sub_list:
                    return None
                    
                # Find json3 format URL, then vtt, then srt
                target_format = None
                for fmt in ['json3', 'vtt', 'srt']:
                    for f in sub_list:
                        if f.get('ext') == fmt:
                            target_format = f
                            break
                    if target_format:
                        break
                        
                if not target_format:
                    target_format = sub_list[0]
                    
                sub_url = target_format.get('url')
                if not sub_url:
                    return None
                    
                res = requests.get(sub_url, timeout=10)
                if res.status_code != 200:
                    return None
                    
                # Parse json3
                if target_format.get('ext') == 'json3':
                    data = res.json()
                    events = data.get("events", [])
                    lrc_lines = []
                    plain_lines = []
                    
                    for ev in events:
                        if "tStartMs" not in ev:
                            continue
                        start_ms = ev["tStartMs"]
                        segs = ev.get("segs", [])
                        text = "".join(seg.get("utf8", "") for seg in segs).strip()
                        
                        if not text or text == "\n":
                            continue
                        text = re.sub(r'<[^>]*>', '', text)
                        text = text.replace('\n', ' ')
                        
                        # format timestamp [mm:ss.xx]
                        m, s = divmod(start_ms / 1000.0, 60)
                        sec_part = int(s)
                        centi_part = int((s - sec_part) * 100)
                        timestamp = f"[{int(m):02d}:{sec_part:02d}.{centi_part:02d}]"
                        
                        lrc_lines.append(f"{timestamp} {text}")
                        plain_lines.append(text)
                        
                    synced_lrc = "\n".join(lrc_lines)
                    plain = "\n".join(plain_lines)
                    return {"synced": synced_lrc, "plain": plain}
                    
                # Fallback parser for VTT / SRT formats if json3 is missing
                else:
                    text = res.text
                    # Simple WebVTT/SRT timestamp cleaner
                    lines = text.split('\n')
                    lrc_lines = []
                    plain_lines = []
                    
                    time_regex = re.compile(r'(\d{2}):(\d{2}):(\d{2})[.,](\d{3})')
                    
                    current_time_str = ""
                    for line in lines:
                        line = line.strip()
                        if not line:
                            continue
                        
                        match = time_regex.search(line)
                        if match:
                            hours = int(match.group(1))
                            mins = int(match.group(2)) + hours * 60
                            secs = int(match.group(3))
                            millis = int(match.group(4))
                            centi = millis // 10
                            current_time_str = f"[{mins:02d}:{secs:02d}.{centi:02d}]"
                        elif current_time_str and not line.isdigit() and '-->' not in line:
                            clean_text = re.sub(r'<[^>]*>', '', line).strip()
                            if clean_text:
                                lrc_lines.append(f"{current_time_str} {clean_text}")
                                plain_lines.append(clean_text)
                                current_time_str = ""
                                
                    synced_lrc = "\n".join(lrc_lines)
                    plain = "\n".join(plain_lines)
                    return {"synced": synced_lrc, "plain": plain}
                    
            except Exception as e:
                print(f"[YouTube Captions] Error: {e}")
                return None

    # ─── LRC Parser ──────────────────────────────────────────────────────────
    def parse_lrc(self, lrc_content: str) -> List[Dict[str, Any]]:
        """
        Parses LRC content (synchronized lyrics file text) into a sorted list of dicts.
        Each dict has 'time' (float, in seconds) and 'text' (str).
        Supports lines with multiple time tags, e.g., '[00:12.30][01:15.00] repeated lyrics'
        """
        if not lrc_content or not lrc_content.strip():
            return []

        parsed_lines = []
        tag_regex = re.compile(r'\[(\d+):(\d+(?:\.\d+)?)\]')

        lines = lrc_content.split('\n')
        for line in lines:
            line = line.strip()
            if not line:
                continue

            matches = list(tag_regex.finditer(line))
            if not matches:
                continue

            text = tag_regex.sub('', line).strip()

            if any(text.startswith(meta) for meta in ['ar:', 'ti:', 'al:', 'by:', 'offset:', 'length:']):
                continue

            # Skip lines with no actual text (pure metadata)
            if not text:
                continue

            for match in matches:
                try:
                    minutes = int(match.group(1))
                    seconds = float(match.group(2))
                    total_seconds = minutes * 60 + seconds
                    parsed_lines.append({
                        "time": round(total_seconds, 2),
                        "text": text
                    })
                except (ValueError, IndexError):
                    continue

        parsed_lines.sort(key=lambda x: x['time'])
        return parsed_lines

    # ─── Linear LRC Generator (fallback for plain text) ──────────────────────
    def generate_linear_lrc(self, plain_lyrics: str, duration_seconds: int) -> str:
        """
        Generates linear LRC content by distributing plain text lines evenly across the song's duration.
        Useful when synced lyrics are missing but plain text lyrics are found.
        """
        if not plain_lyrics or not plain_lyrics.strip():
            return ""

        lines = [line.strip() for line in plain_lyrics.split('\n') if line.strip()]
        if not lines:
            return ""

        n = len(lines)

        start_time = min(10.0, duration_seconds * 0.08)
        end_time = max(duration_seconds - 12.0, duration_seconds * 0.90)

        if end_time <= start_time:
            end_time = duration_seconds - 2.0
            start_time = 1.0

        lrc_lines = []
        for i, line in enumerate(lines):
            if n > 1:
                t = start_time + i * (end_time - start_time) / (n - 1)
            else:
                t = start_time

            m, s = divmod(t, 60)
            sec_part = int(s)
            centi_part = int((s - sec_part) * 100)

            timestamp_str = f"[{int(m):02d}:{sec_part:02d}.{centi_part:02d}]"
            lrc_lines.append(f"{timestamp_str} {line}")

        return "\n".join(lrc_lines)
