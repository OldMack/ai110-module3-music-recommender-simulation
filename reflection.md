# Reflection: Profile Comparison Notes

## High-Energy Pop vs. Chill Lofi Study

These two profiles sit at opposite ends of the energy axis — pop/happy/0.85 vs. lofi/chill/0.38 — and their results barely overlap at all.

High-Energy Pop put Sunrise City at #1 (score 4.39) because all signals fired: genre, mood, energy, and valence were all near-perfect matches. The valence bonus (+0.50) pushed it just above where the old scoring would have placed it, which makes sense — Sunrise City has a valence of 0.84, almost identical to the target of 0.85. That emotional positivity match is real.

Chill Lofi Study put Library Rain at #1 (score 4.90) — actually higher than any Pop result — because the acousticness bonus and valence bonus stacked on top of the genre/mood/energy triple match. The acoustic bonus only helped lofi because lofi songs in the catalog have high acousticness scores; pop songs don't, so the bonus system naturally separated the two profiles without needing any extra logic.

The key takeaway: **energy was the primary divider, but valence reinforced it**. Songs that scored near the top for Pop (high energy, high valence) were near the bottom for Lofi, and vice versa. The two profiles were essentially using opposite ends of every scoring dimension.

## Deep Intense Rock vs. Late-Night Jazz

Rock (energy=0.92) and Jazz (energy=0.32) are not just genre opposites — they're energy opposites too. Their top-5 results share zero songs.

The Rock profile surfaced the same artist (Voltline) at both #1 and #2 because "rock" and "intense" only appear together for two songs in the catalog. After those two, the profile had to fall back on mood-only matches (intense songs from other genres). This exposed a real weakness: **a genre with only 2 catalog entries exhausts its genre-match pool almost immediately**, leaving spots 3–5 to be filled by songs that don't really fit the vibe.

The Jazz profile had a more interesting result: "Mountain Trail Song" (folk/chill) appeared at #5 despite having no genre or mood match. Its energy (0.33) was a near-perfect match to the target (0.32), and it scored an acousticness bonus because folk music is inherently acoustic. The valence score also helped — folk/chill songs tend to have mid-range valence similar to jazz. This makes some intuitive sense: a late-night jazz mood and a quiet folk song share texture even if the genre label differs. The system found this cross-genre connection purely through math, not musical understanding.

## Hip-Hop Workout vs. High-Energy Pop

Both profiles want fairly high energy (hip-hop at 0.80, pop at 0.85) but in different genres and moods (focused vs. happy). This makes them an interesting comparison: similar energy target, different emotional intent.

Hip-Hop Workout had Pulse Check at #1 (score 4.31, genre + mood + near-perfect energy + decent valence). But after the two hip-hop songs in the catalog, the profile completely lost genre traction. Spots #3–#5 were filled by lofi and indie pop tracks with zero genre match — chosen only because their energy happened to be near 0.80. For a real user, these would feel like wrong recommendations even if the math is "correct."

High-Energy Pop had the same energy-exhaustion problem, but mood=happy kept non-pop results feeling more coherent — happy songs from r&b and indie pop at least had the right emotional flavor even without the genre match.

The lesson: **when a genre is underrepresented in the catalog, mood becomes the next best filter**. Pop benefits from more "happy" songs across genres than hip-hop has "focused" songs. That's a dataset bias, not a scoring flaw — and it shows how much catalog composition shapes user experience.

## Adversarial Profile — High-Energy Chill

Tested: `genre="ambient", mood="chill", energy=0.9, likes_acoustic=True`

This profile is a deliberate contradiction: the user claims to want calm, acoustic, ambient music but also wants energy=0.9, which is near the top of the scale. I expected the system to struggle — and it did exactly as predicted.

Results: The top 3 included "Iron Sky" (metal/intense, energy=0.96) and "Drop It Low" (electronic/intense, energy=0.89). Neither ambient, neither chill. Energy proximity dominated because a 0.9 energy target pulls toward the high end of the catalog regardless of genre or mood. The acoustic preference (`likes_acoustic=True`) didn't help at all, because the high-energy songs that won on energy proximity all have near-zero acousticness. The acoustic bonus applied to low-energy acoustic songs, but those songs lost on the energy dimension first.

Crucially, the valence scores of "Iron Sky" and "Drop It Low" are low (0.32 and 0.61) — not the calm, positive valence you'd expect from ambient music. If the user had specified `target_valence=0.70`, those songs would have been penalized slightly. But they still would have won on energy, because the energy dimension alone can move a song by nearly 1.0 points while valence only contributes up to 0.5. This hierarchy — energy > valence > acoustic bonus — is baked into the weights, and it's the right order for most users. The adversarial profile just exposes that the system can't detect when a user is asking for something internally inconsistent.
