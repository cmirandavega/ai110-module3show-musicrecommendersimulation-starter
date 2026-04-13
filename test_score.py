from src.recommender import load_songs, score_song

# Load songs
songs = load_songs('data/songs.csv')

# Test user profile
user_prefs = {
    'favorite_genre': 'pop',
    'favorite_mood': 'happy',
    'target_energy': 0.80,
    'likes_acoustic': False
}

# Score the first song (Sunrise City - should be a strong match)
song = songs[0]
score, reasons = score_song(user_prefs, song)

print(f"Song: {song['title']} by {song['artist']}")
print(f"Genre: {song['genre']}, Mood: {song['mood']}, Energy: {song['energy']}")
print(f"\nScore: {score}")
print("\nReasons:")
for reason in reasons:
    print(f"  {reason}")
