"""
main.py — CLI runner for GrooveMatch 1.0.

Run with: python -m src.main
"""

try:
    from src.recommender import load_songs, recommend_songs
except ImportError:
    from recommender import load_songs, recommend_songs

# Five distinct taste profiles to demonstrate and evaluate the recommender
PROFILES = {
    "High-Energy Pop": {
        "genre": "pop",
        "mood": "happy",
        "energy": 0.85,
        "target_valence": 0.85,
        "likes_acoustic": False,
    },
    "Chill Lofi Study": {
        "genre": "lofi",
        "mood": "chill",
        "energy": 0.38,
        "target_valence": 0.58,
        "likes_acoustic": True,
    },
    "Deep Intense Rock": {
        "genre": "rock",
        "mood": "intense",
        "energy": 0.92,
        "target_valence": 0.45,
        "likes_acoustic": False,
    },
    "Late-Night Jazz": {
        "genre": "jazz",
        "mood": "moody",
        "energy": 0.32,
        "target_valence": 0.55,
        "likes_acoustic": True,
    },
    "Hip-Hop Workout": {
        "genre": "hip-hop",
        "mood": "focused",
        "energy": 0.80,
        "target_valence": 0.75,
        "likes_acoustic": False,
    },
}


def print_recommendations(
    profile_name: str, user_prefs: dict, songs: list, k: int = 5
) -> None:
    """Print a formatted block of top-k recommendations for one user profile."""
    recommendations = recommend_songs(user_prefs, songs, k=k)
    print(f"\n{'='*60}")
    print(f"  Profile : {profile_name}")
    print(
        f"  Prefs   : genre={user_prefs['genre']}, "
        f"mood={user_prefs['mood']}, energy={user_prefs['energy']}"
    )
    print(f"{'='*60}")
    for rank, (song, score, explanation) in enumerate(recommendations, start=1):
        print(f"  #{rank}  {song['title']}  —  {song['artist']}")
        print(f"       Score  : {score:.2f}")
        print(f"       Why    : {explanation}")
        print()


def main() -> None:
    """Load the catalog and run all profiles."""
    songs = load_songs("data/songs.csv")
    print(f"Loaded songs: {len(songs)}")

    for profile_name, user_prefs in PROFILES.items():
        print_recommendations(profile_name, user_prefs, songs, k=5)


if __name__ == "__main__":
    main()
