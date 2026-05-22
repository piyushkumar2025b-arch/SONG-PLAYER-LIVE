import yt_dlp
from typing import List, Dict, Any

class YouTubeProvider:
    def __init__(self):
        self.ydl_opts = {
            'format': 'bestaudio/best',
            'noplaylist': True,
            'extract_flat': True,
            'quiet': True,
            'no_warnings': True,
            'skip_download': True,
            'playlist_items': '1-10', # Limit playlist extraction if it gets resolved as one
            'source_address': '0.0.0.0', # Force IPv4 to avoid IPv6 DNS timeouts
            'check_formats': False,      # Don't contact YouTube to check formats during search
        }

    def search_songs(self, query: str, max_results: int = 5) -> List[Dict[str, Any]]:
        """Search YouTube for songs and return a list of formatted results."""
        if not query.strip():
            return []
            
        with yt_dlp.YoutubeDL(self.ydl_opts) as ydl:
            try:
                # Use ytsearch prefix to search YouTube
                search_query = f"ytsearch{max_results}:{query}"
                results = ydl.extract_info(search_query, download=False)
                entries = results.get('entries', [])
                
                songs = []
                for entry in entries:
                    if not entry:
                        continue
                    video_id = entry.get('id')
                    if not video_id:
                        continue
                        
                    songs.append({
                        'id': video_id,
                        'title': entry.get('title', 'Unknown Title'),
                        'duration': entry.get('duration', 0),
                        'uploader': entry.get('uploader', 'Unknown Artist'),
                        'url': f"https://www.youtube.com/watch?v={video_id}",
                        'thumbnail': f"https://img.youtube.com/vi/{video_id}/hqdefault.jpg"
                    })
                return songs
            except Exception as e:
                print(f"Error searching YouTube: {e}")
                return []
