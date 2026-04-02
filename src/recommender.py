"""
recommender.py — Core logic for GrooveMatch 1.0.

Provides functions to load songs from CSV, score each song against
a user preference dictionary, and return ranked recommendations.
"""

import csv
from typing import List, Dict, Tuple


def load_songs(csv_path: str) -> List[Dict]:
    """Load songs from a CSV file and return a list of dicts with numeric fields cast."""
    songs = []
    with open(csv_path, newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            row["id"] = int(row["id"])
            row["energy"] = float(row["energy"])
            row["tempo_bpm"] = float(row["tempo_bpm"])
            row["valence"] = float(row["valence"])
            row["danceability"] = float(row["danceability"])
            row["acousticness"] = float(row["acousticness"])
            songs.append(row)
    return songs


def score_song(user_prefs: Dict, song: Dict) -> Tuple[float, str]:
    """
    Score a single song against user preferences.

    Returns (score, reasons_string) where score is a float and
    reasons_string is a semicolon-separated list of what contributed.

    Scoring rules:
      +2.0  for a genre match
      +1.0  for a mood match
      +0.0-1.0  for energy proximity (1.0 - |song_energy - target_energy|)
      +0.0-0.5  acousticness bonus when user likes_acoustic=True
      +0.0-0.5  valence bonus when user specifies a target_valence
    """
    score = 0.0
    reasons = []

    # Genre match
    if song["genre"] == user_prefs.get("genre", ""):
        score += 2.0
        reasons.append("genre match (+2.0)")

    # Mood match
    if song["mood"] == user_prefs.get("mood", ""):
        score += 1.0
        reasons.append("mood match (+1.0)")

    # Energy proximity
    target_energy = user_prefs.get("energy", 0.5)
    energy_similarity = 1.0 - abs(song["energy"] - target_energy)
    score += energy_similarity
    reasons.append(f"energy similarity +{energy_similarity:.2f}")

    # Acousticness bonus
    if user_prefs.get("likes_acoustic", False):
        acoustic_bonus = song["acousticness"] * 0.5
        score += acoustic_bonus
        reasons.append(f"acousticness bonus +{acoustic_bonus:.2f}")

    # Valence bonus - reward songs with a similar emotional positivity level
    if "target_valence" in user_prefs:
        valence_similarity = 1.0 - abs(song["valence"] - user_prefs["target_valence"])
        valence_bonus = valence_similarity * 0.5
        score += valence_bonus
        reasons.append(f"valence match +{valence_bonus:.2f}")

    return score, "; ".join(reasons)


def recommend_songs(
    user_prefs: Dict, songs: List[Dict], k: int = 5
) -> List[Tuple[Dict, float, str]]:
    """
    Score all songs and return the top-k ranked by score (highest first).

    Uses sorted() rather than .sort() to leave the original song list unmodified,
    allowing the same catalog to be reused across multiple user profiles.
    """
    scored = []
    for song in songs:
        score, explanation = score_song(user_prefs, song)
        scored.append((song, score, explanation))
    return sorted(scored, key=lambda x: x[1], reverse=True)[:k]
