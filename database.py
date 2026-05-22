import sqlite3
import os
from datetime import datetime
from typing import List, Dict, Any, Optional

DB_FILE = "song_player.db"

class DatabaseManager:
    def __init__(self):
        self.db_path = DB_FILE
        self._init_db()
        self._run_migrations()

    def _get_connection(self):
        return sqlite3.connect(self.db_path)

    def _init_db(self):
        """Initializes the database tables if they do not exist."""
        with self._get_connection() as conn:
            cursor = conn.cursor()
            
            # 1. Favorites Table
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS favorites (
                    youtube_id TEXT PRIMARY KEY,
                    title TEXT NOT NULL,
                    uploader TEXT,
                    duration INTEGER,
                    thumbnail TEXT,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            """)
            
            # 2. Playlists Table
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS playlists (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    name TEXT UNIQUE NOT NULL,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            """)
            
            # 3. Playlist Songs Table
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS playlist_songs (
                    playlist_id INTEGER,
                    youtube_id TEXT,
                    title TEXT NOT NULL,
                    uploader TEXT,
                    duration INTEGER,
                    thumbnail TEXT,
                    added_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    PRIMARY KEY (playlist_id, youtube_id),
                    FOREIGN KEY (playlist_id) REFERENCES playlists (id) ON DELETE CASCADE
                )
            """)
            
            # 4. Lyrics Cache Table
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS lyrics_cache (
                    youtube_id TEXT PRIMARY KEY,
                    track_name TEXT,
                    artist_name TEXT,
                    synced_lyrics TEXT,
                    plain_lyrics TEXT,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            """)
            
            # 5. Recent Plays Table
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS recent_plays (
                    youtube_id TEXT PRIMARY KEY,
                    title TEXT NOT NULL,
                    uploader TEXT,
                    duration INTEGER,
                    thumbnail TEXT,
                    play_count INTEGER DEFAULT 1,
                    played_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            """)
            
            # 6. Ratings Table (NEW)
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS ratings (
                    youtube_id TEXT PRIMARY KEY,
                    title TEXT,
                    uploader TEXT,
                    rating INTEGER NOT NULL CHECK(rating >= 1 AND rating <= 5),
                    rated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            """)
            
            conn.commit()

    def _run_migrations(self):
        """Safe ALTER TABLE migrations for existing databases."""
        with self._get_connection() as conn:
            cursor = conn.cursor()
            
            # Add play_count to recent_plays if missing
            try:
                cursor.execute("ALTER TABLE recent_plays ADD COLUMN play_count INTEGER DEFAULT 1")
                conn.commit()
            except Exception:
                pass
            
            # Add notes column to favorites if missing
            try:
                cursor.execute("ALTER TABLE favorites ADD COLUMN notes TEXT DEFAULT ''")
                conn.commit()
            except Exception:
                pass

    # --- Favorites CRUD ---
    def add_favorite(self, song: Dict[str, Any]) -> bool:
        try:
            with self._get_connection() as conn:
                cursor = conn.cursor()
                cursor.execute("""
                    INSERT OR REPLACE INTO favorites (youtube_id, title, uploader, duration, thumbnail, created_at)
                    VALUES (?, ?, ?, ?, ?, CURRENT_TIMESTAMP)
                """, (song['id'], song['title'], song['uploader'], song['duration'], song['thumbnail']))
                conn.commit()
                return True
        except Exception as e:
            print(f"DB Error add_favorite: {e}")
            return False

    def remove_favorite(self, youtube_id: str) -> bool:
        try:
            with self._get_connection() as conn:
                cursor = conn.cursor()
                cursor.execute("DELETE FROM favorites WHERE youtube_id = ?", (youtube_id,))
                conn.commit()
                return True
        except Exception as e:
            print(f"DB Error remove_favorite: {e}")
            return False

    def get_favorites(self) -> List[Dict[str, Any]]:
        try:
            with self._get_connection() as conn:
                conn.row_factory = sqlite3.Row
                cursor = conn.cursor()
                cursor.execute("SELECT * FROM favorites ORDER BY created_at DESC")
                return [dict(row) for row in cursor.fetchall()]
        except Exception as e:
            print(f"DB Error get_favorites: {e}")
            return []

    def is_favorite(self, youtube_id: str) -> bool:
        try:
            with self._get_connection() as conn:
                cursor = conn.cursor()
                cursor.execute("SELECT 1 FROM favorites WHERE youtube_id = ?", (youtube_id,))
                return cursor.fetchone() is not None
        except Exception as e:
            print(f"DB Error is_favorite: {e}")
            return False

    def update_song_note(self, youtube_id: str, note: str) -> bool:
        """Save a personal note to a favorited song."""
        try:
            with self._get_connection() as conn:
                cursor = conn.cursor()
                cursor.execute("UPDATE favorites SET notes = ? WHERE youtube_id = ?", (note, youtube_id))
                conn.commit()
                return True
        except Exception as e:
            print(f"DB Error update_song_note: {e}")
            return False

    def get_song_note(self, youtube_id: str) -> str:
        """Get a personal note for a song."""
        try:
            with self._get_connection() as conn:
                cursor = conn.cursor()
                cursor.execute("SELECT notes FROM favorites WHERE youtube_id = ?", (youtube_id,))
                row = cursor.fetchone()
                return row[0] if row and row[0] else ""
        except Exception as e:
            print(f"DB Error get_song_note: {e}")
            return ""

    # --- Playlists CRUD ---
    def create_playlist(self, name: str) -> bool:
        try:
            with self._get_connection() as conn:
                cursor = conn.cursor()
                cursor.execute("INSERT INTO playlists (name) VALUES (?)", (name,))
                conn.commit()
                return True
        except Exception as e:
            print(f"DB Error create_playlist: {e}")
            return False

    def get_playlists(self) -> List[Dict[str, Any]]:
        try:
            with self._get_connection() as conn:
                conn.row_factory = sqlite3.Row
                cursor = conn.cursor()
                cursor.execute("SELECT * FROM playlists ORDER BY name ASC")
                return [dict(row) for row in cursor.fetchall()]
        except Exception as e:
            print(f"DB Error get_playlists: {e}")
            return []

    def delete_playlist(self, playlist_id: int) -> bool:
        try:
            with self._get_connection() as conn:
                cursor = conn.cursor()
                cursor.execute("DELETE FROM playlist_songs WHERE playlist_id = ?", (playlist_id,))
                cursor.execute("DELETE FROM playlists WHERE id = ?", (playlist_id,))
                conn.commit()
                return True
        except Exception as e:
            print(f"DB Error delete_playlist: {e}")
            return False

    def add_to_playlist(self, playlist_id: int, song: Dict[str, Any]) -> bool:
        try:
            with self._get_connection() as conn:
                cursor = conn.cursor()
                cursor.execute("""
                    INSERT OR REPLACE INTO playlist_songs (playlist_id, youtube_id, title, uploader, duration, thumbnail)
                    VALUES (?, ?, ?, ?, ?, ?)
                """, (playlist_id, song['id'], song['title'], song['uploader'], song['duration'], song['thumbnail']))
                conn.commit()
                return True
        except Exception as e:
            print(f"DB Error add_to_playlist: {e}")
            return False

    def remove_from_playlist(self, playlist_id: int, youtube_id: str) -> bool:
        try:
            with self._get_connection() as conn:
                cursor = conn.cursor()
                cursor.execute("DELETE FROM playlist_songs WHERE playlist_id = ? AND youtube_id = ?", (playlist_id, youtube_id))
                conn.commit()
                return True
        except Exception as e:
            print(f"DB Error remove_from_playlist: {e}")
            return False

    def get_playlist_songs(self, playlist_id: int) -> List[Dict[str, Any]]:
        try:
            with self._get_connection() as conn:
                conn.row_factory = sqlite3.Row
                cursor = conn.cursor()
                cursor.execute("SELECT * FROM playlist_songs WHERE playlist_id = ? ORDER BY added_at DESC", (playlist_id,))
                results = []
                for row in cursor.fetchall():
                    item = dict(row)
                    item['id'] = item['youtube_id']
                    results.append(item)
                return results
        except Exception as e:
            print(f"DB Error get_playlist_songs: {e}")
            return []

    # --- Recent Plays ---
    def add_recent_play(self, song: Dict[str, Any]) -> bool:
        try:
            with self._get_connection() as conn:
                cursor = conn.cursor()
                # Increment play_count if song already in table
                cursor.execute("SELECT play_count FROM recent_plays WHERE youtube_id = ?", (song['id'],))
                row = cursor.fetchone()
                play_count = (row[0] if row and row[0] else 0) + 1
                
                cursor.execute("""
                    INSERT OR REPLACE INTO recent_plays (youtube_id, title, uploader, duration, thumbnail, play_count, played_at)
                    VALUES (?, ?, ?, ?, ?, ?, CURRENT_TIMESTAMP)
                """, (song['id'], song['title'], song['uploader'], song['duration'], song['thumbnail'], play_count))
                
                # Keep only top 20 recent plays
                cursor.execute("""
                    DELETE FROM recent_plays WHERE youtube_id NOT IN (
                        SELECT youtube_id FROM recent_plays ORDER BY played_at DESC LIMIT 20
                    )
                """)
                conn.commit()
                return True
        except Exception as e:
            print(f"DB Error add_recent_play: {e}")
            return False

    def get_recent_plays(self) -> List[Dict[str, Any]]:
        try:
            with self._get_connection() as conn:
                conn.row_factory = sqlite3.Row
                cursor = conn.cursor()
                cursor.execute("SELECT * FROM recent_plays ORDER BY played_at DESC")
                results = []
                for row in cursor.fetchall():
                    item = dict(row)
                    item['id'] = item['youtube_id']
                    results.append(item)
                return results
        except Exception as e:
            print(f"DB Error get_recent_plays: {e}")
            return []

    def get_top_tracks(self, limit: int = 10) -> List[Dict[str, Any]]:
        """Return songs ordered by play count descending."""
        try:
            with self._get_connection() as conn:
                conn.row_factory = sqlite3.Row
                cursor = conn.cursor()
                cursor.execute("""
                    SELECT * FROM recent_plays
                    ORDER BY play_count DESC
                    LIMIT ?
                """, (limit,))
                results = []
                for row in cursor.fetchall():
                    item = dict(row)
                    item['id'] = item['youtube_id']
                    results.append(item)
                return results
        except Exception as e:
            print(f"DB Error get_top_tracks: {e}")
            return []

    def get_total_listening_seconds(self) -> int:
        """Return total listening time in seconds based on play counts × duration."""
        try:
            with self._get_connection() as conn:
                cursor = conn.cursor()
                cursor.execute("SELECT SUM(play_count * duration) FROM recent_plays")
                row = cursor.fetchone()
                return int(row[0]) if row and row[0] else 0
        except Exception as e:
            print(f"DB Error get_total_listening_seconds: {e}")
            return 0

    def get_total_songs_played(self) -> int:
        """Return total number of play events (sum of all play counts)."""
        try:
            with self._get_connection() as conn:
                cursor = conn.cursor()
                cursor.execute("SELECT SUM(play_count) FROM recent_plays")
                row = cursor.fetchone()
                return int(row[0]) if row and row[0] else 0
        except Exception as e:
            print(f"DB Error get_total_songs_played: {e}")
            return 0

    # --- Lyrics Cache ---
    def get_cached_lyrics(self, youtube_id: str) -> Optional[Dict[str, Any]]:
        try:
            with self._get_connection() as conn:
                conn.row_factory = sqlite3.Row
                cursor = conn.cursor()
                cursor.execute("SELECT * FROM lyrics_cache WHERE youtube_id = ?", (youtube_id,))
                row = cursor.fetchone()
                return dict(row) if row else None
        except Exception as e:
            print(f"DB Error get_cached_lyrics: {e}")
            return None

    def cache_lyrics(self, youtube_id: str, track_name: str, artist_name: str, synced_lyrics: str, plain_lyrics: str) -> bool:
        try:
            with self._get_connection() as conn:
                cursor = conn.cursor()
                cursor.execute("""
                    INSERT OR REPLACE INTO lyrics_cache (youtube_id, track_name, artist_name, synced_lyrics, plain_lyrics, created_at)
                    VALUES (?, ?, ?, ?, ?, CURRENT_TIMESTAMP)
                """, (youtube_id, track_name, artist_name, synced_lyrics, plain_lyrics))
                conn.commit()
                return True
        except Exception as e:
            print(f"DB Error cache_lyrics: {e}")
            return False

    # --- Ratings ---
    def rate_song(self, song: Dict[str, Any], rating: int) -> bool:
        """Save a 1-5 star rating for a song."""
        try:
            with self._get_connection() as conn:
                cursor = conn.cursor()
                cursor.execute("""
                    INSERT OR REPLACE INTO ratings (youtube_id, title, uploader, rating, rated_at)
                    VALUES (?, ?, ?, ?, CURRENT_TIMESTAMP)
                """, (song.get('id') or song.get('youtube_id'), song.get('title', ''), song.get('uploader', ''), rating))
                conn.commit()
                return True
        except Exception as e:
            print(f"DB Error rate_song: {e}")
            return False

    def get_rating(self, youtube_id: str) -> int:
        """Get the star rating (1-5) for a song, or 0 if not rated."""
        try:
            with self._get_connection() as conn:
                cursor = conn.cursor()
                cursor.execute("SELECT rating FROM ratings WHERE youtube_id = ?", (youtube_id,))
                row = cursor.fetchone()
                return int(row[0]) if row else 0
        except Exception as e:
            print(f"DB Error get_rating: {e}")
            return 0

    def get_all_ratings(self) -> List[Dict[str, Any]]:
        """Get all rated songs ordered by rating desc."""
        try:
            with self._get_connection() as conn:
                conn.row_factory = sqlite3.Row
                cursor = conn.cursor()
                cursor.execute("SELECT * FROM ratings ORDER BY rating DESC, rated_at DESC")
                return [dict(row) for row in cursor.fetchall()]
        except Exception as e:
            print(f"DB Error get_all_ratings: {e}")
            return []
