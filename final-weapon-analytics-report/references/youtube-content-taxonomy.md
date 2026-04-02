# Final Weapon YouTube Content Taxonomy

This file defines every content type published on the Final Weapon YouTube channel, how to classify videos into those types programmatically, and how to interpret performance benchmarks for each type.

---

## Content Type Definitions

### Shorts (Duration < 60 seconds)

#### `short_review`
A Short that repurposes or summarizes a full written/video review. Usually obvious from the title — it will reference a specific game title alongside evaluative language.

**Examples:**
- "UNBEATABLE Is Very Disappointing #rhythmgame #gaming"
- "Legacy of Kain: Ascendance Is a Disappointing Return for the Series"
- "A NINTENDO DS REMASTER DONE RIGHT? Capcom's GENIUS Fix For The Mega Man Starforce Collection"

**Key signal:** Title names a specific game AND carries a verdict (adjective, opinion word, or evaluative framing). These are derived from longer review content and serve as top-of-funnel for the full review.

#### `short_evergreen`
All other Shorts — news reactions, guide tips, opinion takes, trending topic hooks. These are original short-form content, not derived from a longer piece.

**Examples:**
- "NEW Final Fantasy VII Remake Update Just BROKE the Game! #ff7remake"
- "Pokémon Pokopia Is The Switch 2 System Seller NOBODY Saw Coming"
- "The SECRET METHOD to Grinding Vocation Experience in DQVII Reimagined!"
- "Fox McCloud CONFIRMED in the Super Mario Galaxy Movie!"
- "KINGDOM HEARTS 25TH ANNIVERSARY JUST GOT TEASED?!"

**Key signal:** News hook, trending reaction, guide tip, or hype/speculation. Most Shorts that aren't named reviews fall here.

---

### Long-Form — Named Series

These are Final Weapon's flagship original series. They are recurring, franchise-focused deep dives with consistent branding.

#### `series_utp` — *Under The Plate*
Final Fantasy VII universe deep dives — lore analysis, location breakdowns, character studies, and FF7 Remake trilogy coverage. These are the most prolific long-form series and the channel's core identity pillar for FF7 content.

**Title signals:** "Under The Plate", "Remake Part 3", "City of the Ancients", "Icicle Inn", "Bone Village", "Lifestream", "Highwind", "Fort Condor", "Cloud Strife", "Tifa Lockhart", "Aerith", "Sephiroth", "Zack Fair", "Cid Highwind", "Barret Wallace", "Yuffie", "Wutai", "Vincent Valentine", "Cait Sith", "First Soldier", "Ever Crisis", "FF7 Rebirth" (non-review context)

**Examples:**
- "FF7 Remake Part 3 Will Finally Open the City of the Ancients"
- "Why Bone Village in FF7 Remake Part 3 Could Be Bigger Than You Think"
- "The Crucial Role of Tifa Lockhart in Final Fantasy VII Remake Part 3"
- "What is Negative Lifestream? Breaking Down Sephiroth's Final Plan"
- "The Final Fantasy VII: The First Soldier Episode 1 Full Story Recap"

#### `series_btc` — *Beyond The Conduit*
Xeno series coverage — Xenoblade Chronicles, Xenogears, and Xenosaga analysis, lore deep dives, retrospectives, and new game speculation. Covers all entries in the Xeno metaseries.

**Title signals:** "Beyond The Conduit", "Xenoblade", "Xenogears", "Xenosaga", "Xeno series"

**Examples:**
- "Xenoblade Chronicles X on Switch 2 — Everything We Know"
- "Why Xenogears Deserves a Full Remake"
- "The Xeno Series Timeline Explained"
- "Xenoblade Chronicles 4: What Could Come Next?"

**Note:** Any video with "Xenoblade" in the title is classified here even if it also contains "review" — series cohesion takes priority over the standalone review type.

#### `series_seed` — *SeeD Archives*
Final Fantasy VIII focused coverage — analysis, remake speculation, lore. Less prolific than UTP but a dedicated series.

**Title signals:** "SeeD Archives", "Final Fantasy VIII", "FF8"

#### `series_lost_pages` — *The Lost Pages*
Kingdom Hearts series coverage — lore, analysis, sequel speculation, franchise retrospectives.

**Title signals:** "Lost Pages", "Kingdom Hearts", "KH"

**Examples:**
- "Kingdom Hearts in 2026: Is the DROUGHT Finally OVER?"
- "Yozora - The Greatest Boss Fight Of All Time"
- "It's Time to Bring the Kingdom Hearts Series to Nintendo Switch 2"
- "Kingdom Hearts Missing-Link is Officially Canceled"

#### `series_moonlight` — *In The Moonlight*
Type-Moon universe coverage — Fate series, Tsukihime, Mahoyo/Witch on the Holy Night, ufotable anime adaptations.

**Title signals:** "In The Moonlight", "Type-Moon", "Fate/", "Fate Stay Night" (with or without slash), "Tsukihime", "Mahoyo", "Witch on the Holy Night", "ufotable", "Fate/EXTRA Record", "Fate/stay night"

**Examples:**
- "Fate/EXTRA Record DELAYED Again… And It's Worse Than You Think"
- "Witch on the Holy Night Anime Film CONFIRMS 2026 Release Date!"
- "Where Is ufotable's Witch on the Holy Night (Mahoyo) Anime Film?"
- "Fate/stay night Remastered REVIEW"
- "Fate Stay Night Remastered REVIEW"

**Note:** Fate/stay night reviews are classified here rather than as `review` because they are part of the In The Moonlight series. This applies regardless of whether the title uses "Fate/" or "Fate Stay Night" (no slash).

#### `series_roe` — *Recollection of Evil*
Resident Evil series coverage — analysis, retrospectives, new game coverage.

**Title signals:** "Recollection of Evil", "Resident Evil"

**Examples:**
- "Resident Evil Is Entering a New Era on Switch 2"
- "Did Resident Evil Requiem Live Up to the Hype?"
- "Should You Play Resident Evil Requiem as a Newcomer?"

#### `series_memory_card` — *memory//card*
Gaming retrospectives covering any franchise. Currently has one episode: "Why Jak 2 Is A Cyberpunk Masterpiece". Identified by explicit "memory//card" branding in the title.

**Title signals:** "memory//card" (explicit branding only)

**Important:** The classifier for this series uses a narrow pattern matching only the "memory//card" brand name. Generic retrospective videos (e.g., "A 2019 Retrospective") are NOT automatically classified here — they need the explicit branding. This avoids misclassifying standalone retrospective videos from other series (like a "Resident Evil Retrospective" which belongs in `series_roe`).

**Examples:**
- "Why Jak 2 Is A Cyberpunk Masterpiece"

---

### Long-Form — Podcasts

#### `podcast` — *Switch Point*
Final Weapon's Nintendo-focused podcast. Identified by "Switch Point" in the title.

**Examples:**
- "Nintendo Switch 2 Reveal Reactions Are CRAZY | Switch Point Episode 1"
- "3DS Games That Deserve A Second Life on Nintendo Switch 2 | Switch Point Episode 4"
- "Is Donkey Kong Bananza The Best Game of 2025? | Switch Point Episode 16"

#### `podcast_weaponized` — *Weaponized*
Final Weapon's general gaming podcast covering broader industry topics.

**Examples:**
- "Is Square Enix's Silence in 2025 Concerning? | Weaponized Episode 7"
- "The Hilarious Solo Leveling Aura Farming Obsession | Weaponized Episode 9"
- "Death Stranding 2 Looks Absolutely Insane, And We're Here For It | Weaponized Episode 10"

---

### Long-Form — Standalone

#### `review`
A formal game or product review. Title contains "Review" or "REVIEW" and is not part of a named series (see series rules above for exceptions).

**Examples:**
- "Esoteric Ebb Review - Existential Democracy"
- "Legacy of Kain: Ascendance Review – An Identity Crisis"
- "Mega Man Star Force Legacy Collection Review – Tune Into the Stars"
- "Marathon Review - An Extremely Promising Start"
- "Monster Hunter Stories 3: Twisted Reflection Review - Third Time's the Charm"

#### `preview`
A hands-on preview, first impressions, or beta impressions piece. Title contains "Preview", "Impressions", or "Hands-On".

**Examples:**
- "Mega Man Star Force Legacy Collection Preview – A Dream Come True"
- "STARBITES Preview - An Intriguing Mecha Turn-Based RPG Emerges"
- "MOUSE: P.I. For Hire Final Preview - Simply Un-brie-lievable"

#### `oneoff_guide`
A standalone guide, explainer, tips video, or how-to that doesn't fit a series. Identified by guide language in the title.

**Title signals:** "guide", "how to", "tips", "grinding", "method", "secret item", "tutorial", "where to find", "best way", "play order"

**Examples:**
- "The SECRET METHOD to Grinding Vocation Experience in DQVII Reimagined!" *(if long-form)*
- "Xenoblade Chronicles: Where To Start & The Best Play Order"
- "5 Must Know Tips for Mai Shiranui Players in Street Fighter 6"
- "Should You Play Resident Evil Requiem as a Newcomer?"

#### `oneoff_opinion`
The default for standalone long-form that doesn't match any above category. Covers: news analysis, franchise speculation, rankings, opinion editorials, industry commentary, announcements, and standalone news reaction or analysis videos.

**Examples:**
- "Where Is Devil May Cry 6?"
- "Pokémon Winds & Waves Looks AMAZING! The UPGRADE We Deserve?"
- "Dragon Quest 8 Remake: Is It FINALLY Time?"
- "Handheld Mode Boost FIXED Xenoblade on Switch 2"
- "Why the Next Nintendo Direct Likely Isn't Until April 2026"
- "The History of the Mana Series - A Comprehensive Timeline"
- "Did Square Enix Just Confirm A NieR: Automata Sequel?"

---

## Classification Priority Rules

When a video could match multiple types, apply this priority order (highest wins):

1. **Podcast** (`podcast`, `podcast_weaponized`) — series name in title is definitive
2. **Named series** (`series_utp`, `series_btc`, `series_seed`, `series_lost_pages`, `series_moonlight`, `series_roe`, `series_memory_card`) — franchise/series keyword match
3. **Short subtypes** (`short_review`, `short_evergreen`) — only for duration < 60s
4. **Review** — explicit "Review" or "REVIEW" in title
5. **Preview** — explicit "Preview" / "Impressions" in title
6. **Guide** — guide keywords in title
7. **Opinion** (default) — everything else

**Important: The Python classifier in SKILL.md enforces this exact priority order.** Podcasts are checked first, then named series, then the short/long split, then review/preview/guide/opinion. This ensures the documented priority and the code are always in sync.

**Important edge cases:**
- Under The Plate (series_utp) covers almost all FF7 Remake content, including "review" videos about FF7 games. If a title has both "Review" and an FF7 UTP keyword, classify as `series_utp`.
- Beyond The Conduit (series_btc) covers all Xeno content. A "Xenoblade Chronicles Review" would be classified as `series_btc`, not `review`.
- In The Moonlight (series_moonlight) covers all Fate/Type-Moon content. "Fate/stay night Remastered REVIEW" is `series_moonlight`.
- memory//card uses a narrow match on the brand name only. A generic "retrospective" video is NOT memory//card unless the title explicitly says "memory//card" or "memory card".

---

## Performance Benchmarks by Type

Use these as context when writing the report. Final Weapon's channel is in a growth phase — benchmarks reflect realistic expectations for a niche JRPG/anime gaming outlet, not a mainstream channel.

| Content Type | Typical view range | What "good" looks like | Revenue profile |
|---|---|---|---|
| `short_evergreen` | 500–35,000+ | Viral potential; 5,000+ = strong | Low RPM but high volume driver |
| `short_review` | 200–3,000 | 1,000+ = solid; drives review page traffic | Very low revenue |
| `series_utp` | 100–5,000 | 500+ per episode = healthy; spikes on Part 3 news | Medium-high revenue for watch time |
| `series_btc` | 200–2,000 | 500+ = strong; spikes around new game announcements and Nintendo Directs | Medium revenue; Xenoblade has dedicated niche appeal |
| `series_lost_pages` | 100–400 | 200+ = solid | Medium |
| `series_seed` | 100–300 | 150+ = solid | Medium |
| `series_moonlight` | 100–400 | 200+ = solid | Medium |
| `series_roe` | 200–3,500 | 500+ = strong; RE has broad appeal | Medium-high |
| `series_memory_card` | 50–300 | 100+ = solid for retrospective content (only 1 episode to date) | Low-medium |
| `podcast` | 1–100 | Podcasts build slowly; focus on consistent output | Very low |
| `podcast_weaponized` | 1–100 | Same as Switch Point | Very low |
| `review` | 50–2,000 | 300+ = strong; flagship reviews 500+ | Medium-high RPM |
| `preview` | 100–700 | 300+ = solid | Medium |
| `oneoff_guide` | 500–15,000 | Search-driven; 1,000+ = strong | High RPM for search traffic |
| `oneoff_opinion` | 100–5,000 | 500+ = strong; FF7/KH opinions spike higher | Medium |

---

## What to Analyze in the Report

### Per-type summary table
Show all content types with: video count, total views, avg views/video, total revenue, avg watch hours, revenue per 1,000 views, avg CTR. Sort by total views descending.

### Shorts deep dive
- How many were `short_review` vs `short_evergreen`?
- Which Shorts crossed 5,000 views? What topics/franchises?
- Are review Shorts driving traffic to the full reviews on site? (Cross-reference GA top pages)
- What hook formats worked best (question, "BROKE", "CONFIRMED", "NOBODY SAW", etc.)?

### Series health
For each named series with at least one video this month, report:
- Episodes published this month
- Total and avg views
- Is this growth, flat, or decline vs. typical benchmark?
- Standout episode if any
- **Exception:** For series with fewer than 3 total episodes (e.g., memory//card), report raw numbers vs. benchmark only — no trend language.

### Review pipeline
- How many reviews published as long-form this month?
- Which got the most views? Which underperformed?
- Are review Shorts being made for every review? (If not, flag it)
- To check for companion Shorts: look for Short titles that reference the same game name as a review. If the match is uncertain, note "Unclear" rather than asserting Yes or No.

### Content recommendation output
Based on the type analysis, the recommendations section should address:
1. Which Shorts topics/formats should be doubled down on next month
2. Which series is strongest and deserves more episodes
3. Whether reviews are being properly promoted through Shorts
4. Any content type that is underperforming and may not be worth the effort investment
5. New topic opportunities based on what the algorithm is responding to this month
