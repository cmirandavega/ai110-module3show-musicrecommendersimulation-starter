# 🎧 Model Card: Music Recommender Simulation

## 1. Model Name  

**VibeMatch 1.0**

---

## 2. Intended Use  

This system suggests songs from a small catalog based on a user's taste preferences.

- It returns up to 5 ranked song recommendations.
- It is built for classroom exploration, not for real users.
- It assumes each user has one favorite genre, one favorite mood, a target energy level, and an acoustic preference.
- It does not learn from listening history or change over time.

---

## 3. How the Model Works  

Think of it like a points system. Every song in the catalog gets a score out of 5.

- **+2.0** if the song's genre matches what the user likes most.
- **+1.0** if the mood matches too.
- **+1.0** based on how close the song's energy is to the user's target. Songs far from the target earn less.
- **+0.5** if the song's acoustic level fits the user's preference (electronic vs. acoustic).
- **+0.5** small bonus for songs that sound upbeat and positive.

Songs are ranked from highest score to lowest. The top 5 are returned.

---

## 4. Data  

The catalog has **18 songs** stored in `data/songs.csv`.

- The original starter dataset had 10 songs. 8 more were added to improve variety.
- Genres include: pop, lofi, rock, ambient, jazz, synthwave, indie pop, hip-hop, folk, electronic, soul, metal, latin, blues, and classical.
- Moods include: happy, chill, intense, relaxed, moody, focused, energetic, melancholic, romantic, playful, nostalgic, and introspective.
- Most genres have only one song, so users with niche tastes get weaker results.
- The catalog skews toward Western music. There is no K-pop, Afrobeats, or other globally popular styles.
- Lyrics, language, and cultural context are not included at all.

---

## 5. Strengths  

The system works well when the user's taste matches a well-represented genre.

- The Chill Lofi and Deep Intense Rock profiles both returned strong, intuitive top picks ("Library Rain" and "Storm Runner") with scores above 4.7 / 5.0.
- Energy scoring adds useful nuance within a genre. For the High-Energy Pop profile, "Sunrise City" correctly ranked above "Gym Hero" because its energy (0.82) was closer to the target (0.80) than Gym Hero's (0.93).
- Every recommendation has a clear reason. You can always point to exactly which features helped or hurt a song's score.

---

## 6. Limitations and Bias 

The system's most significant structural bias is its **genre lock-in**: 40% of the maximum score (2.0 out of 5.0 points) is awarded for a single exact string match between the song's genre label and the user's favorite genre. This means no combination of perfect energy, mood, acousticness, and valence scores can compensate for a genre miss — a song that is sonically identical to a user's favorite but labeled differently will always rank below a poor-quality genre match. This was directly observable during testing: the Latin Playful profile's ranks 2 through 5 all scored below 2.0, not because those songs were a bad fit, but because the catalog only contained one song with the genre label "latin." Users who prefer niche or underrepresented genres are therefore served meaningfully worse than users who prefer genres with broader catalog coverage, creating an unequal experience that has nothing to do with actual musical taste.

---

## 7. Evaluation  

Four user profiles were tested: High-Energy Pop, Chill Lofi, Deep Intense Rock, and Latin Playful.

- For each profile, the top 5 results were checked to see if they made intuitive sense.
- The top-ranked song for every profile matched expectations — the scores and reasons confirmed why each song ranked where it did.
- The most surprising result was the Latin Playful profile. The #1 song ("Calor de Noche") scored 4.82, but #2 dropped all the way to 1.82. That cliff revealed how badly the system struggles when a genre has only one song in the catalog.
- A sensitivity experiment was also run: genre weight was halved and energy weight was doubled. "Rooftop Lights" jumped above "Gym Hero" for the Pop profile, showing that small weight changes can meaningfully shift rankings.

---

## 8. Future Work  

- **Soften genre matching.** Allow partial credit for related genres (e.g., rock and metal, lofi and ambient). Right now a genre miss costs the full 2.0 points with no middle ground.
- **Make acousticness a spectrum.** The current `likes_acoustic` field is True or False. Replacing it with a float (0–1) would let users express a preference like "slightly acoustic" instead of forcing a hard choice.
- **Add a diversity rule.** Right now the top 5 can all be from the same artist or genre cluster. A simple rule like "no more than 2 songs per artist" would improve variety.
- **Score valence against the user.** Currently all users get a bonus for high-valence songs. A user who prefers dark or melancholic music should not be penalized for it.
- **Expand the catalog.** With 18 songs, niche genre users almost always hit a wall after rank 1. A larger, more balanced catalog would make the scoring differences matter more.

---

## 9. Personal Reflection  

Building this made it clear how much a recommender's behavior is shaped by decisions that happen before any code runs — like which genres to include in the dataset and how many songs each gets. The Latin Playful result was a good example of that: the scoring formula was working correctly, but the catalog made a fair result impossible. It was also surprising how much a single weight change could shift rankings. Doubling the energy weight during the sensitivity experiment caused a song with the wrong genre to jump above one with the right genre. That kind of instability is easy to miss if you only look at the top result and not the full list. Real music apps like Spotify are doing something far more complex, but the core tension — balancing user preferences, catalog coverage, and fairness — is the same problem at every scale.
