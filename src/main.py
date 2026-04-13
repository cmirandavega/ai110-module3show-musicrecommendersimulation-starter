"""
Command line runner for the Music Recommender Simulation.

This file helps you quickly run and test your recommender.

You will implement the functions in recommender.py:
- load_songs
- score_song
- recommend_songs
"""

from src.recommender import load_songs, recommend_songs


def display_recommendations(user_name: str, user_prefs: dict, recommendations: list) -> None:
    """Helper function to display recommendations for a user profile."""
    print("\n" + "="*80)
    print(f"🎵 {user_name.upper()} 🎵")
    print("="*80)
    print(f"\nUser Preferences:")
    print(f"  • Genre: {user_prefs['favorite_genre']}")
    print(f"  • Mood: {user_prefs['favorite_mood']}")
    print(f"  • Target Energy: {user_prefs['target_energy']}")
    print(f"  • Acoustic: {user_prefs['likes_acoustic']}")
    print(f"\nTop {len(recommendations)} Recommendations:\n")
    
    for rank, rec in enumerate(recommendations, 1):
        song, score, explanation = rec
        
        # Format score as a progress bar
        score_percent = (score / 5.0) * 100
        bar = "█" * int(score_percent / 5) + "░" * (20 - int(score_percent / 5))
        
        print(f"{rank}. {song['title']} by {song['artist']}")
        print(f"   Score: {score:.2f}/5.0 {bar} ({score_percent:.0f}%)")
        print(f"   Reasons:")
        
        # Parse and format the pipe-delimited reasons
        reasons = explanation.split(" | ")
        for reason in reasons:
            if reason.strip():
                print(f"     • {reason}")
        print()


def main() -> None:
    songs = load_songs("data/songs.csv")
    
    # Define three distinct user profiles
    profiles = {
        "High-Energy Pop": {
            "favorite_genre": "pop",
            "favorite_mood": "happy",
            "target_energy": 0.8,
            "likes_acoustic": False
        },
        "Chill Lofi": {
            "favorite_genre": "lofi",
            "favorite_mood": "chill",
            "target_energy": 0.35,
            "likes_acoustic": True
        },
        "Deep Intense Rock": {
            "favorite_genre": "rock",
            "favorite_mood": "intense",
            "target_energy": 0.91,
            "likes_acoustic": False
        },
        "Latin Playful": {
            "favorite_genre": "latin",
            "favorite_mood": "playful",
            "target_energy": 0.71,
            "likes_acoustic": False
        }
    }
    
    # Generate recommendations for each profile
    for profile_name, user_prefs in profiles.items():
        recommendations = recommend_songs(user_prefs, songs, k=5)
        display_recommendations(profile_name, user_prefs, recommendations)


if __name__ == "__main__":
    main()
