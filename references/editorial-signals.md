# Editorial Signals — Interpretation Guide

How to translate raw analytics numbers into plain-English editorial recommendations for Final Weapon.

---

## Signal 1: Traffic / Revenue Mismatch

**What it is:** Pages where traffic rank and revenue rank are far apart.

**High traffic, low RPM (< $4):**  
Usually indicates a broad audience that doesn't match advertiser targeting. Common on homepage, news roundups, or viral content from social. Not worth chasing for revenue — but good for brand awareness and new user acquisition.

**Low traffic, high RPM (> $10):**  
The hidden gems. These pages attract a commercially valuable audience — often review pages, buying guides, or niche guides. More content in this category = more efficient revenue. Flag any page with RPM > $10 and views < 500 as a "scale opportunity" — the RPM proves the audience exists, it just needs more search surface area.

**Language to use in report:**  
> "[Series X] pages are delivering a $[rpm] RPM despite modest traffic — this signals a commercially engaged audience that rewards more coverage."

---

## Signal 2: Engagement Outliers

**What it is:** Pages where `Average engagement time per active user` is unusually high or low.

**High engagement (> 60 seconds):**  
Readers are genuinely reading, not just scanning. Strong signal for SEO (Google favors engaged pages) and for ad revenue (more time on page = more ad impressions). Pages like this should be updated regularly to maintain rankings.

**Very high engagement (> 90 seconds):**  
Exceptional. Call these out specifically — they are likely review pages, deep guides, or interview features. Worth noting as evidence of editorial quality.

**Low engagement (< 12 seconds):**  
Likely a search query answered by the title/snippet before the reader scrolled. Not necessarily bad — quick-answer pages can still rank well and generate RPM — but don't invest in making them longer.

**Anomaly to watch:** If a schedule/release guide page has engagement > 100 seconds, it may be because readers are using it as a reference (checking dates repeatedly). This is a good sign and worth updating weekly — which Final Weapon already does for its release guides.

---

## Signal 3: Series Momentum

**What it is:** Total Mediavine revenue summed across all weekly schedule/date update pages for each anime series.

**How to compute it:** Group slugs by series name (use `parse_slug.py`), sum `revenue`.

**Interpretation tiers:**

| Monthly series revenue | Signal |
|---|---|
| > $30 | Core franchise — high priority coverage |
| $15 – $30 | Solid performer — maintain weekly updates |
| $8 – $15 | Emerging — worth tracking; consider expanding |
| < $8 | Low ROI or limited audience — evaluate continuation |

**What to look for:**  
New series entering the top tier for the first time. Old series dropping out. Any series where revenue is disproportionate to its traffic (suggests high advertiser intent around that topic).

---

## Signal 4: YouTube–Site Alignment Gap

**What it is:** Whether the top YT video topics match the top site traffic topics.

**Why it matters:** Final Weapon's YT audience and web audience may have different interests. If FF7 Remake content dominates YT but barely appears in the GA top 20, there's a missed cross-pollination opportunity.

**How to compare:** Extract the franchise or game name from both GA page titles and YouTube video titles. Look for franchises that appear in one platform's top 15 but not the other's.

**Categories of gap:**

- **YT leads, site lags:** Strong YouTube franchise with weak site coverage. Opportunity to write companion articles — guides, timelines, analysis pieces — to capture search traffic from the same audience.
- **Site leads, YT lags:** Strong search traffic topic with no YouTube presence. Opportunity to convert top-performing articles into video content (Shorts recaps work well for schedule pages).
- **Both aligned:** Healthy. Note which franchises have full-stack presence (site + YT).

**Language to use:**  
> "FF7 Remake content drove [X] YouTube views this month but doesn't appear in the top 20 site pages. A dedicated hub or written guide series could capture the search traffic this audience is also generating."

---

## Signal 5: Evergreen Performers

**What it is:** Articles published before the current month that still rank in the top 50 GA pages.

**How to identify:** If the page title doesn't contain the current month's airing dates, or if the Mediavine slug has a publish date from a prior year/month, it's evergreen.

**Why it matters:** These pages represent compounding search equity. They require minimal effort to maintain (an annual update, a few added paragraphs) but continue driving traffic and revenue indefinitely.

**Types at Final Weapon:**
- Game guides (e.g., "FF III Summon Locations") — very high RPM, very durable
- Review pages — durable if the game remains popular
- Character/lore explainers — extremely durable for long-running franchises

**Recommendation language:**  
> "The [page title] guide from [year] is still delivering $[rpm] RPM — a light refresh with updated information and internal links could extend its rankings for another cycle."

---

## Signal 6: Daily Traffic Spikes

**What it is:** Days in the YouTube `Chart data.csv` (or GA daily data if available) that exceed the monthly daily average by 30% or more.

**How to calculate:**
```python
avg = chart['Views'].mean()
spikes = chart[chart['Views'] > avg * 1.3]
```

**Common causes at Final Weapon:**
- Weekly anime episode air dates (especially JJK, which airs Thursdays on Crunchyroll)
- Nintendo Directs or major gaming events
- A viral YouTube Short that drove site referrals
- A news scoop picked up by a larger outlet
- Reddit or social media post going viral

**What to note in the report:** The date, the view count, and a one-line hypothesis for the cause. If two spikes occur on the same weekday throughout the month, it's almost certainly tied to an airing schedule.

---

## Signal 7: YouTube CTR vs. Views Mismatch

**What it is:** Videos where CTR and views tell different stories.

**High CTR (> 8%), low views:**  
The thumbnail and title are compelling, but the video isn't getting surfaced. Algorithm reach issue, not a creative issue. Strategy: publish more in this format to teach the algorithm, or promote externally.

**Low CTR (< 3%), high views:**  
The algorithm is pushing it despite a weak hook — usually because it taps into a trending topic the algorithm is boosting. The video succeeded despite the creative. Worth making a stronger-hook version of the same topic.

**High CTR + High views:**  
The ideal. Note these as the template to replicate: what topic, what title format, what thumbnail approach?

**Low CTR + Low views:**  
The video failed on both dimensions. What was the topic? Was it too niche, too late, or does it just need a better title? Worth a brief note in the report but not worth dwelling on.

**Threshold reference:**
- CTR < 2%: Poor
- CTR 2–4%: Below average
- CTR 4–7%: Good
- CTR > 7%: Excellent

---

## Signal 8: YouTube Content Type Performance

**What it is:** The per-type breakdown showing which content formats (Shorts, series, reviews, podcasts, etc.) are pulling their weight.

**How to compute it:** Use the `content_type` column added by the `classify_video()` function in SKILL.md to group and aggregate by type.

**What to look for:**

**Shorts (evergreen vs. review):**
Evergreen Shorts are algorithm-dependent discovery content; review Shorts are conversion content designed to drive views to the full review. Compare avg views per type. If evergreen Shorts are pulling 3,000+ avg and review Shorts are averaging 300, the news-hook format is significantly outperforming repurposed review content — signal to make more original Shorts rather than purely repurposing reviews.

**Series (Under The Plate, Beyond The Conduit, etc.):**
Named series build loyal sub-audiences but typically have lower avg views than viral Shorts. Evaluate series by watch time and revenue, not views alone — a 500-view episode with 7 minutes of avg watch time is healthier than a 2,000-view Short. Series that are publishing consistently and maintaining 200+ avg views are healthy; series with zero episodes in a month may indicate a production gap.

**Reviews:**
Reviews are the editorial core of Final Weapon and have the highest RPM on YouTube. A review under 300 views typically means it needs better title/thumbnail work or a companion Short. If a review doesn't have a companion Short, flag it explicitly in the report — this is a coverage gap.

**Podcasts:**
Switch Point and Weaponized are audience-building investments, not view-drivers. Low views are expected and normal. What matters: consistency (are they publishing regularly?) and whether any episode broke out (500+ views = notable). Don't interpret low podcast views as failure.

**Revenue efficiency:**
Include revenue per 1,000 views by content type in the Performance by Content Type table. This reveals which formats are the most monetization-efficient, independent of total volume.

**Language to use:**
> "Evergreen Shorts averaged [X] views vs. [Y] for review Shorts this month — original news-hook content is [outperforming/underperforming] repurposed reviews. The top Short ([title]) worked because [reason from title/topic]."

---

## Signal 9: Short_review vs. Short_evergreen Split

**What it is:** A comparison of the two Short subtypes to inform which to prioritize production time on.

**Key questions:**
- What % of Shorts are review-repurposed vs. original evergreen?
- Which type has a higher avg views per video?
- Are there any review-repurposed Shorts that outperformed their evergreen counterparts? (If so, why — was it the franchise?)

**Interpretation framework:**

| Scenario | Interpretation | Recommendation |
|---|---|---|
| Evergreen >> Review Shorts on avg views | Algorithm rewards original hooks over repurposed content | Invest more effort in original evergreen Shorts; keep review Shorts but don't over-invest |
| Review Shorts >> Evergreen on avg views | The specific franchises reviewed are very popular; repurposing works | Prioritize review Shorts for every major title; they're driving discovery |
| Both similar | Neither type is dominant | Maintain current mix; focus on title/thumbnail quality over type |
| Very few review Shorts published | Coverage gap | Ensure every review gets a companion Short |

**Language to use:**
> "Of [X] Shorts published this month, [Y] were review-repurposed and [Z] were original evergreen. Evergreen Shorts averaged [A] views vs. [B] for review Shorts. [Interpretation sentence.]"

---

## Signal 10: Series Health Check

**What it is:** A per-series view of whether each named Final Weapon series is healthy, growing, or stalling.

**Series to check:** Under The Plate (FF7), Beyond The Conduit (Xeno), SeeD Archives (FF8), The Lost Pages (Kingdom Hearts), In The Moonlight (Type-Moon), Recollection of Evil (Resident Evil), memory//card (retrospectives).

**Healthy benchmarks (per episode, monthly):**
- Under The Plate: 300–5,000 views (high variance based on FF7 news cycle)
- Beyond The Conduit: 200–2,000 views (Xenoblade has strong niche appeal; spikes around new game announcements)
- The Lost Pages: 100–400 views
- SeeD Archives: 100–300 views
- In The Moonlight: 150–400 views
- Recollection of Evil: 200–3,500 views (RE has broader appeal)
- memory//card: 50–300 views

**Important — low-episode series:** For any series with fewer than 3 total episodes (currently memory//card has only 1: "Why Jak 2 Is A Cyberpunk Masterpiece"), report raw performance numbers only. Do not characterize the series as "growing," "stalling," or "declining" — there isn't enough data for trend analysis. Instead, note the episode count and how it performed relative to the benchmark range.

**What to flag:**
- Any series with 0 episodes published: note as absent; may be intentional or a production gap
- Any series averaging below its low benchmark: may need a topic refresh or is in a between-game lull
- Any series episode significantly outperforming benchmark: what was the topic? Replicate.
- Under The Plate specifically: views spike on FF7 Part 3 news days — track whether spike episodes are news-reactive or purely analytical
- Beyond The Conduit: Xeno content tends to spike around Nintendo Direct announcements and new game reveals

**Language to use:**
> "Under The Plate published [X] episodes this month averaging [Y] views — above its typical benchmark, likely driven by FF7 Part 3 speculation content. The Lifestream deep-dive ([views] views, [watch hours] hrs) was the standout. The Lost Pages published [X] episode(s) at [Y] avg views — within normal range for a quiet KH news month."
>
> "memory//card has 1 episode to date ('Why Jak 2 Is A Cyberpunk Masterpiece') with [X] views — [above/within/below] the 50–300 benchmark. Too early for trend analysis."

**Note on trend language throughout the report:** All "growing/stalling/declining" assessments are relative to per-type benchmarks documented here, not compared to a prior month's actual data. Month-over-month comparison would require the previous month's report as an input, which is not currently part of this skill's workflow.

---

## Signal 11: Release Guide Health

**What it is:** A dedicated analysis of Final Weapon's release/schedule guide pages, which are the site's dominant traffic and revenue driver on the Mediavine side.

**Why it's separate from other signals:** Release guides account for the majority of site views and Mediavine revenue. Treating them as just another content type in the top-10 tables obscures their structural importance to the business. This signal isolates their performance so editorial decisions about guides are data-driven.

**Key questions:**
- What % of total Mediavine revenue came from release guides this month?
- Which individual guide was the top earner?
- Are any existing guides declining in views? (Possible cause: series ended, went on hiatus, lost search ranking, or a competitor guide is outranking)
- Are any guides growing unexpectedly? (Possible cause: new anime season started, or the series is gaining popularity)
- Are there trending anime/game series visible in GA or YouTube data that don't yet have a release guide? These are new guide opportunities.

**How to identify release guides:** Use the `is_release_guide()` function in `parse_slug.py`, which checks for slug patterns like `release-date`, `schedule`, `episode`, and `when-does`.

**Interpretation tiers (monthly per-guide):**

| Monthly guide revenue | Signal |
|---|---|
| > $10 | Anchor guide — highest priority to keep updated weekly |
| $4 – $10 | Solid guide — maintain weekly updates |
| $1 – $4 | Moderate — update if effort is low; consider biweekly |
| < $1 | Low performer — series may have ended or audience moved on; evaluate whether to continue updating |

**What to flag in the report:**
- Any guide dropping >30% in views (vs. what you'd expect for an active series) — investigate cause
- Any non-guide anime/game page in the GA top 50 that doesn't have a release guide yet — this is the strongest "create a new guide" signal
- The ratio of guide revenue to total revenue — if this exceeds ~75%, note the concentration risk and suggest investing in diversifying (more reviews, more guides for games, more evergreen content)

**Language to use:**
> "Release guides accounted for [X]% of Mediavine revenue this month ($[Y] of $[Z]). The top earner was [series name] at $[rev]. [One sentence on notable guide movement — new entrant, declining guide, or opportunity.]"
