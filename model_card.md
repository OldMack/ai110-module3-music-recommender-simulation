# Model Card: Music Recommender Simulation

## 1. Model Name
**GrooveMatch 1.0**

---

## 2. Intended Use

GrooveMatch suggests songs from a local catalog based on a user's taste profile (genre, mood, energy level). It is built as a classroom project to make the logic of content-based recommendation systems visible and understandable — not for deployment in any real music platform.

**What it is for:** Learning how scoring and ranking turn user preferences into suggestions. Exploring how small dataset choices and weight decisions shape results.

**What it is NOT for:** Real-time streaming, replacing actual recommendation engines, serving production users, or making any decisions that affect real people's music access.

---

## 3. How the Model Works

The system uses a weighted point system — think of it as a checklist that scores each song against four questions:

1. **Does the genre match?** A match earns 2.0 points — the biggest single reward, because genre is the broadest filter separating music taste.
2. **Does the mood match?** A match earns 1.0 point — mood narrows within a genre (upbeat pop vs. melancholy pop are very different listening experiences).
3. **How close is the energy?** The system calculates `1.0 - |song_energy - target_energy|` — so a song with energy=0.80 when the user wants 0.85 earns 0.95 points. A perfect match earns a full point; a huge mismatch earns close to zero.
4. **Acoustic bonus (optional):** If the user prefers acoustic sounds, songs with high acousticness scores earn up to 0.5 additional points.
5. **Valence match (optional):** If the user specifies a target emotional positivity, songs whose valence is close earn up to 0.5 additional points.

All songs are scored, then sorted highest to lowest, and the top-K are returned with plain-English reasons.

---

## 4. Data

- **Catalog size:** 24 songs
- **Origin:** 10 from the course starter file; 14 added to increase genre and mood diversity
- **Genres:** pop, lofi, rock, ambient, jazz, synthwave, indie pop, metal, country, r&b, classical, electronic, hip-hop, folk, reggae
- **Moods:** happy, chill, intense, relaxed, focused, moody, sad
- **Artist data:** All artist names are fictional — no real labels, no real listener counts
- **Limitations:** The catalog is tiny. There is no listening history, no audio analysis, no user feedback, and no demographic data. Song attributes were assigned manually, which introduces the creator's subjective judgment about what "high energy" or "moody" means.

---

## 5. Strengths

- **Fully explainable:** Every recommendation comes with a plain-English reason string — users can see exactly which attributes drove the result.
- **Fast and deterministic:** The same profile always produces the same result, making it easy to test and debug.
- **Good for clear profiles:** Users with consistent, well-defined tastes (e.g., Chill Lofi Study or Deep Intense Rock) get intuitively correct results.
- **Valence scoring adds nuance:** Including emotional positivity as an optional signal helps separate "energetic but melancholy" songs from "energetic and euphoric" ones.

---

## 6. Limitations and Bias

**Filter bubble — genre dominance:** Genre weight of 2.0 means that genre match is almost always the deciding factor. A jazz fan who would genuinely enjoy a folk song with the same tempo and mood will rarely see folk songs because they never score the genre points. This is a simplified version of the filter bubbles that real streaming platforms create.

**Dataset imbalance:** The catalog has more "high-energy" songs than "low-energy" ones, and more pop-adjacent genres (pop, indie pop, r&b) than niche ones (classical, reggae, metal have 1-2 songs each). Users who prefer underrepresented genres exhaust their top matches faster.

**Semantic contradictions ignored:** The system has no understanding of meaning. A user who wants `mood=chill` and `energy=0.9` will get high-energy results because the math doesn't know that "high-energy" and "chill" are contradictory.

**No diversity control:** Two songs by the same artist can appear back-to-back if they both score high — no penalty for repetition.

**Tempo and danceability unused:** `danceability` and `tempo_bpm` are loaded from the CSV but never used in scoring. They represent wasted signal.

---

## 7. Evaluation

Five user profiles were tested, covering a broad range of genre, mood, and energy combinations:

| Profile | #1 Result | Intuitive? |
|---|---|---|
| High-Energy Pop (pop/happy/0.85) | Sunrise City (pop/happy/0.82) | Yes — triple match + high valence |
| Chill Lofi Study (lofi/chill/0.38) | Library Rain (lofi/chill/0.35) | Yes — genre + mood + acoustic + valence |
| Deep Intense Rock (rock/intense/0.92) | Storm Runner (rock/intense/0.91) | Yes |
| Late-Night Jazz (jazz/moody/0.32) | Jazz in the Rain (jazz/moody/0.31) | Yes |
| Hip-Hop Workout (hip-hop/focused/0.80) | Pulse Check (hip-hop/focused/0.77) | Yes |

**Most interesting edge case:** The Late-Night Jazz profile surfaced "Mountain Trail Song" (folk/chill) at #5 — no genre or mood match, just near-perfect energy proximity (0.33 vs target 0.32) and high acousticness. It makes acoustic sense even though the genre label is completely different. This shows that energy and acousticness can cross genre boundaries in ways a pure genre filter would miss.

**Weight-shift experiment:** Cutting genre weight to 1.0 and doubling energy weight caused "Acoustic Confession" (folk/sad) to enter the Chill Lofi top 5, even though it's neither lofi nor chill. This confirmed that the 2.0 genre weight is essential for keeping recommendations genre-coherent.

---

## 8. Ideas for Improvement

1. **Add a diversity penalty** — limit each artist to one appearance in any top-5 result to avoid surfacing two songs from the same artist back-to-back.
2. **Use danceability and tempo in scoring** — currently loaded but never used. A tempo-range preference (e.g., 80-120 BPM) would let users express the physical feel they want, not just the emotional one.
3. **Semantic mood grouping** — instead of exact mood string matches, group moods into clusters (e.g., {happy, energetic, euphoric} vs. {sad, melancholy, bittersweet}) and award partial points for near-matches.
4. **Implicit feedback loop** — let users rate results (thumbs up/down) and adjust weights per session, turning the static scorer into something that actually learns.

---

## 9. Personal Reflection

The biggest "aha" moment in this project was realizing how much a single weight controls the entire experience. When genre weight is 2.0, the system feels like a music expert — genre-first, then fine-tuned by mood and energy. When I cut it to 1.0, the system suddenly felt random, surfacing folk songs for jazz profiles. One number changed everything.

Adding the valence signal was the most interesting design choice I made. Valence captures whether a song feels "positive" or "negative" emotionally, independent of its energy. Without it, two songs with the same genre, mood, and energy score identically — but one might be triumphant while the other is bittersweet. The valence bonus (up to 0.5 points) is small enough that it doesn't override genre or mood, but it consistently pushes the "right feeling" song to the top when two songs are otherwise tied.

What surprised me most about this project: simple arithmetic can feel surprisingly intelligent. When the Chill Lofi profile pulled Library Rain to #1, it genuinely seemed like the system understood my preferences. But it was just four additions. That feeling comes from pattern-matching on genre labels — we see our favorite genre at the top and infer that the system "gets" us. Real understanding would require the system to hear the actual music. GrooveMatch never hears anything. That gap — between pattern-matching and understanding — is exactly where the interesting AI research is happening right now.
