import csv
import math
from typing import List, Dict, Tuple, Optional
from dataclasses import dataclass

@dataclass
class Song:
    """
    Represents a song and its attributes.
    Required by tests/test_recommender.py
    """
    id: int
    title: str
    artist: str
    genre: str
    mood: str
    energy: float
    tempo_bpm: float
    valence: float
    danceability: float
    acousticness: float

@dataclass
class UserProfile:
    """
    Represents a user's taste preferences.
    Required by tests/test_recommender.py
    """
    favorite_genre: str
    favorite_mood: str
    target_energy: float
    likes_acoustic: bool

class Recommender:
    """
    OOP implementation of the recommendation logic.
    Required by tests/test_recommender.py
    """
    def __init__(self, songs: List[Song]):
        self.songs = songs

    def recommend(self, user: UserProfile, k: int = 5) -> List[Song]:
        # TODO: Implement recommendation logic
        return self.songs[:k]

    def explain_recommendation(self, user: UserProfile, song: Song) -> str:
        # TODO: Implement explanation logic
        return "Explanation placeholder"

def load_songs(csv_path: str) -> List[Dict]:
    """
    Loads songs from a CSV file.
    Required by src/main.py
    """
    songs = []
    try:
        with open(csv_path, newline="", encoding="utf-8") as f:
            reader = csv.DictReader(f)
            for row in reader:
                songs.append({
                    "id":           int(row["id"]),
                    "title":        row["title"],
                    "artist":       row["artist"],
                    "genre":        row["genre"],
                    "mood":         row["mood"],
                    "energy":       float(row["energy"]),
                    "tempo_bpm":    float(row["tempo_bpm"]),
                    "valence":      float(row["valence"]),
                    "danceability": float(row["danceability"]),
                    "acousticness": float(row["acousticness"]),
                })
    except FileNotFoundError:
        print(f"Error: file not found at {csv_path}")
    return songs

def score_song(user_prefs: Dict, song: Dict) -> Tuple[float, List[str]]:
    """
    Scores a single song against a user profile using the finalized recipe.

    Scoring recipe (max 5.0 points):
        Genre match    +2.0  (exact match)
        Mood match     +1.0  (exact match)
        Energy sim     +1.0  (Gaussian: exp(−diff² / 0.045))
        Acousticness   +0.5  (linear preference match)
        Valence bonus  +0.5  (song.valence × 0.5)
        ─────────────────────
        MAX SCORE       5.0

    Returns:
        (score, reasons) where score is in [0.0, 5.0] and reasons is a list
        of strings explaining each component's contribution.
    """
    points = 0.0
    reasons = []

    # Genre match: +2.0
    if song["genre"] == user_prefs["favorite_genre"]:
        points += 2.0
        reasons.append(f"✓ Genre ({song['genre']}) +2.0")
    else:
        reasons.append(f"✗ Genre ({song['genre']} ≠ {user_prefs['favorite_genre']})")

    # Mood match: +1.0
    if song["mood"] == user_prefs["favorite_mood"]:
        points += 1.0
        reasons.append(f"✓ Mood ({song['mood']}) +1.0")
    else:
        reasons.append(f"✗ Mood ({song['mood']} ≠ {user_prefs['favorite_mood']})")

    # Energy similarity: Gaussian, max +1.0
    diff = song["energy"] - user_prefs["target_energy"]
    energy_points = math.exp(-(diff ** 2) / (2 * 0.15 ** 2))
    points += energy_points
    reasons.append(
        f"Energy +{energy_points:.2f} (target: {user_prefs['target_energy']}, song: {song['energy']})"
    )

    # Acousticness fit: linear preference match, max +0.5
    a = song["acousticness"]
    if user_prefs["likes_acoustic"]:
        raw = 1.0 if a >= 0.7 else a / 0.7
        label = "high, preferred" if a >= 0.7 else "low, preferred high"
    else:
        if a <= 0.3:
            raw = 1.0
        else:
            raw = max(0.0, (1.0 - a) / 0.7)
        label = "low, preferred" if a <= 0.3 else "high, preferred low"
    acoustic_points = raw * 0.5
    points += acoustic_points
    reasons.append(f"Acousticness +{acoustic_points:.2f} ({label})")

    # Valence bonus: song.valence * 0.5
    valence_points = song["valence"] * 0.5
    points += valence_points
    reasons.append(f"Valence +{valence_points:.2f}")

    score = round(points, 4)
    reasons.append(f"TOTAL: {score} / 5.0")
    return score, reasons


def recommend_songs(user_prefs: Dict, songs: List[Dict], k: int = 5) -> List[Tuple[Dict, float, str]]:
    """
    Scores all songs and returns top k recommendations sorted by score (descending).

    Args:
        user_prefs: Dict with keys: favorite_genre, favorite_mood, target_energy, likes_acoustic
        songs: List of song dictionaries from load_songs()
        k: Number of top recommendations to return

    Returns:
        List of (song_dict, score, explanation_string) tuples, sorted highest score first.

    sorted() vs .sort():
        sorted() returns a NEW list and leaves the original untouched, making it safe to
        call on any iterable without side effects — the right choice here since we never
        want to permanently reorder the catalog. .sort() sorts a list IN PLACE (returns
        None) and is marginally more memory-efficient when you own the list and don't
        need the original order preserved.
    """
    if not songs or k == 0:
        return []

    # Score every song in one pass; unpack the (score, reasons) tuple from score_song
    scored = [
        (song, score, " | ".join(reasons))
        for song in songs
        for score, reasons in [score_song(user_prefs, song)]
    ]

    # sorted() leaves the original catalog list untouched; [:k] handles k > len(songs)
    return sorted(scored, key=lambda x: x[1], reverse=True)[:k]
