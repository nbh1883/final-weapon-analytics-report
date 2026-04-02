---
name: final-weapon-analytics-report
description: "Generate a comprehensive monthly analytics report for Final Weapon, the Japanese gaming publication. Use this skill whenever Noah or a Final Weapon admin uploads analytics exports and asks for a report, summary, breakdown, or insights — even if they just say 'run the report', 'analyze this month', 'what did we do this month', or 'share with the team'. Accepts Google Analytics CSV exports, Mediavine CSV exports, and YouTube Studio ZIP or CSV exports in any combination. Produces a clean, shareable markdown report with an executive summary, per-platform deep dives, editorial recommendations, and a content opportunity matrix. Always use this skill when Final Weapon analytics data is present."
---

# Final Weapon Monthly Analytics Report

Generates a thorough but digestible monthly report from raw analytics exports. The output is a markdown file suitable for sharing with Final Weapon admins.

---

## Step 0 — Identify what was uploaded

Check `/mnt/user-data/uploads/` for the following file types and note which are present:

| Source | Expected format | Key signals |
|---|---|---|
| Google Analytics | `.csv` with comment header rows (`# ---`) | Columns: `Page title and screen class`, `Views`, `Active users`, `Average engagement time per active user` |
| Mediavine | `.csv` without comment headers | Columns: `slug`, `views`, `revenue`, `rpm`, `cpm`, `viewability`, `fillRate`, `impressionsPerPageview` |
| YouTube Studio | `.zip` containing `Table data.csv`, `Chart data.csv`, `Totals.csv` | OR a standalone `Table data.csv` with `Video title`, `Views`, `Watch time (hours)`, `Estimated revenue (USD)` |

Not all sources are required — generate the report with whatever is present, and note any missing sources at the top.

---

## Step 1 — Parse each data source

### Google Analytics
The GA export has ~9 comment rows before the real header. Skip them:

```python
import pandas as pd

def load_ga(path):
    with open(path, encoding='utf-8-sig') as f:
        for i, line in enumerate(f):
            if not line.startswith('#'):
                header_row = i
                break
    ga = pd.read_csv(path, skiprows=header_row, encoding='utf-8-sig')
    ga.columns = ga.columns.str.strip()
    return ga
```

Key columns to extract:
- `Page title and screen class` → page name
- `Views` → total pageviews
- `Active users` → unique users
- `Average engagement time per active user` → engagement (seconds)

Pull date range from the comment block (lines starting with `# Start date:` and `# End date:`).

### Mediavine
Standard CSV, no skip rows needed. Load directly with pandas.

**Important — Release guide analysis:** Release/schedule guide pages are the dominant traffic and revenue driver on the site. They are updated weekly and generate the majority of Mediavine views. Identify release guides by matching slugs that contain patterns like `release-date`, `schedule`, `episode`, or `when-does` (see `scripts/parse_slug.py` for the `is_release_guide()` helper). Always compute release guide metrics separately from non-guide content.

Key derived metrics:
- **Total revenue**: `df['revenue'].sum()`
- **Weighted RPM** (always use this, never simple average): `(df['revenue'].sum() / df['views'].sum()) * 1000`
- **Release guide vs. non-guide split**: separate `df` into guide and non-guide subsets; compute views, revenue, and weighted RPM for each
- **Top earners by revenue**: `df.nlargest(15, 'revenue')`
- **High-efficiency pages (RPM)**: filter `views > 100`, then `nlargest(10, 'rpm')`
- **Series grouping**: extract series name from slug using the helper in `scripts/parse_slug.py`

**Using parse_slug.py:** Copy the script to your working directory and import it directly:
```python
import sys, shutil
shutil.copy('<skill_path>/scripts/parse_slug.py', '/home/claude/parse_slug.py')
sys.path.insert(0, '/home/claude')
from parse_slug import extract_series, group_by_series, top_series_table, is_release_guide
```

### YouTube Studio ZIP
```python
import zipfile, io

def load_youtube_zip(path):
    with zipfile.ZipFile(path) as z:
        with z.open('Table data.csv') as f:
            table = pd.read_csv(f, encoding='utf-8-sig')
        with z.open('Chart data.csv') as f:
            chart = pd.read_csv(f, encoding='utf-8-sig')  # Daily time series
        with z.open('Totals.csv') as f:
            totals_csv = pd.read_csv(f, encoding='utf-8-sig')  # Channel-level totals
    videos = table[table['Content'] != 'Total'].copy()
    totals = table[table['Content'] == 'Total'].iloc[0]
    return videos, chart, totals
```

**Important:** `Chart data.csv` contains the daily time series (use for daily spike analysis in Signal 6). `Totals.csv` contains channel-level aggregate totals. Do not confuse them.

### YouTube content classification

Every video must be classified into one of the types below before analysis. Read `references/youtube-content-taxonomy.md` for full rules and examples. Summary:

**Shorts (Duration < 60s):**
- `short_review` — title contains "Review" or references a specific game title in a clearly evaluative way
- `short_evergreen` — news reaction, guide tip, opinion, or trend-based short (everything else)

**Long-form (Duration ≥ 60s):**
- `podcast` — *Switch Point* episodes (Nintendo podcast)
- `podcast_weaponized` — *Weaponized* episodes (general gaming podcast)
- `series_utp` — *Under The Plate* (Final Fantasy VII deep-dives and lore)
- `series_seed` — *SeeD Archives* (Final Fantasy VIII)
- `series_lost_pages` — *The Lost Pages* (Kingdom Hearts)
- `series_moonlight` — *In The Moonlight* (Type-Moon / Fate)
- `series_roe` — *Recollection of Evil* (Resident Evil)
- `series_btc` — *Beyond The Conduit* (Xeno series — Xenoblade, Xenogears, Xenosaga)
- `series_memory_card` — *memory//card* (gaming retrospectives — currently one episode: "Why Jak 2 Is A Cyberpunk Masterpiece")
- `review` — formal game or product review (title contains "Review" or "REVIEW")
- `preview` — preview or hands-on (title contains "Preview" or "Impressions")
- `oneoff_guide` — standalone guide, explainer, or how-to
- `oneoff_opinion` — standalone opinion, ranking, news analysis, or editorial video (default)

**Classification Python helper:**

> **Classification priority order (highest wins):**
> 1. Podcasts (`podcast`, `podcast_weaponized`) — series name in title is definitive
> 2. Named series (`series_utp`, `series_btc`, `series_seed`, etc.) — franchise keyword match
> 3. Short subtypes (`short_review`, `short_evergreen`) — only for duration < 60s
> 4. Review — explicit "Review" / "REVIEW" in title
> 5. Preview — explicit "Preview" / "Impressions" in title
> 6. Guide — guide keywords in title
> 7. Opinion (default) — everything else

```python
import re

# Podcasts checked first — highest priority
PODCAST_PATTERNS = {
    'podcast':           re.compile(r'switch point', re.IGNORECASE),
    'podcast_weaponized':re.compile(r'weaponized', re.IGNORECASE),
}

# Named series checked second — order within this dict matters (more specific first)
SERIES_PATTERNS = {
    'series_utp':        re.compile(r'(under the plate|city of the ancients|icicle inn|bone village|lifestream|highwind|fort condor|ff7 remake part 3|ff7 remake trilogy|cloud strife|tifa lockhart|aerith|sephiroth|zack fair|cid highwind|barret wallace|yuffie|wutai|vincent valentine|cait sith|first soldier|ever crisis)', re.IGNORECASE),
    'series_btc':        re.compile(r'(beyond the conduit|xenoblade|xenogears|xenosaga|xeno\s?series)', re.IGNORECASE),
    'series_seed':       re.compile(r'(seed archives|final fantasy viii remake|ff8)', re.IGNORECASE),
    'series_lost_pages': re.compile(r'(lost pages|kingdom hearts)', re.IGNORECASE),
    'series_moonlight':  re.compile(r'(in the moonlight|type.?moon|fate[/\s]|tsukihime|mahoyo|witch on the holy night|ufotable|fate.?stay.?night)', re.IGNORECASE),
    'series_roe':        re.compile(r'(recollection of evil|resident evil)', re.IGNORECASE),
    'series_memory_card':re.compile(r'(memory.{0,2}card)', re.IGNORECASE),
}

REVIEW_RE   = re.compile(r'\breevi?ew\b', re.IGNORECASE)
PREVIEW_RE  = re.compile(r'\bpreview\b|\bimpressions\b|\bhands.?on\b', re.IGNORECASE)
GUIDE_RE    = re.compile(r'\bguide\b|\bhow to\b|\btips?\b|\bgrinding\b|\bmethod\b|\bsecret\b|\bitem\b|\btutorial\b', re.IGNORECASE)

def classify_video(title: str, duration_seconds: float = None) -> str:
    """
    Classify a Final Weapon YouTube video into a content type.

    Args:
        title: Video title string
        duration_seconds: Video duration in seconds. If None, classification
            proceeds without the short/long distinction — the video will be
            classified by title patterns only and assumed to be long-form.
    """
    t = title or ''

    # Determine short vs long-form
    if duration_seconds is not None:
        is_short = duration_seconds < 60
    else:
        # Fallback: if no duration data, assume long-form unless title has
        # obvious Short signals (e.g., hashtag at the end is common for Shorts)
        is_short = bool(re.search(r'#\w+\s*$', t))

    # If it's a Short, classify into short subtypes only
    if is_short:
        return 'short_review' if REVIEW_RE.search(t) else 'short_evergreen'

    # --- Long-form classification (priority order) ---

    # 1. Podcasts (highest priority for long-form)
    for label, pattern in PODCAST_PATTERNS.items():
        if pattern.search(t):
            return label

    # 2. Named series
    for label, pattern in SERIES_PATTERNS.items():
        if pattern.search(t):
            return label

    # 3. Review / Preview / Guide / Opinion
    if REVIEW_RE.search(t):   return 'review'
    if PREVIEW_RE.search(t):  return 'preview'
    if GUIDE_RE.search(t):    return 'oneoff_guide'
    return 'oneoff_opinion'   # default for standalone longform
```

After classifying, add a `content_type` column. Handle the case where `Duration` may not exist:
```python
if 'Duration' in videos.columns:
    videos['content_type'] = videos.apply(
        lambda r: classify_video(str(r['Video title']), float(r['Duration'] or 0)), axis=1
    )
elif 'Average view duration' in videos.columns:
    # Some exports have this instead; it's in HH:MM:SS format
    def parse_duration(d):
        try:
            parts = str(d).split(':')
            return sum(float(p) * (60 ** (len(parts) - 1 - i)) for i, p in enumerate(parts))
        except:
            return None
    videos['content_type'] = videos.apply(
        lambda r: classify_video(str(r['Video title']), parse_duration(r.get('Average view duration'))), axis=1
    )
else:
    # No duration data — classify by title only
    videos['content_type'] = videos['Video title'].apply(
        lambda t: classify_video(str(t), duration_seconds=None)
    )
```

Then compute per-type aggregates:
```python
agg_cols = {
    'video_count': ('Views', 'count'),
    'total_views': ('Views', 'sum'),
    'avg_views': ('Views', 'mean'),
}
# Only include columns that exist in the data
if 'Estimated revenue (USD)' in videos.columns:
    agg_cols['total_revenue'] = ('Estimated revenue (USD)', 'sum')
if 'Watch time (hours)' in videos.columns:
    agg_cols['avg_watch_hours'] = ('Watch time (hours)', 'mean')
if 'Impressions click-through rate (%)' in videos.columns:
    agg_cols['avg_ctr'] = ('Impressions click-through rate (%)', 'mean')

type_summary = videos.groupby('content_type').agg(**agg_cols).round(2).sort_values('total_views', ascending=False)
```

Key YouTube metrics to compute:
- Channel totals: total views, watch hours, revenue, subscribers, impressions, avg CTR
- Top 10 by views; top 5 by revenue (show separately if lists differ)
- Per content-type summary table (see above)
- Best and worst performers within each type (top 3 / bottom 3 by views)
- Shorts breakdown: `short_review` vs `short_evergreen` performance comparison
- Series health: views and watch time per series episode (are series growing or declining?)
- CTR leaders (top 10 by CTR, min 1,000 impressions) — signals best-performing hooks
- Revenue efficiency: revenue per 1,000 views by content type

**Note on series with very few episodes:** For any series with fewer than 3 total episodes (e.g., memory//card currently has only 1), report raw numbers only. Do not use trend language like "growing", "stalling", or "declining" — there isn't enough data. Instead, note the episode count and its performance relative to benchmark.

---

## Step 2 — Compute cross-platform KPIs

Calculate these summary numbers to lead the report:

```python
# Mediavine release guide split
if mv is not None:
    mv['is_guide'] = mv['slug'].apply(is_release_guide)
    mv_guide = mv[mv['is_guide']]
    mv_non_guide = mv[~mv['is_guide']]
    guide_revenue = mv_guide['revenue'].sum().round(2)
    guide_views = int(mv_guide['views'].sum())
    non_guide_revenue = mv_non_guide['revenue'].sum().round(2)
    non_guide_views = int(mv_non_guide['views'].sum())
    guide_pct_revenue = round(guide_revenue / mv['revenue'].sum() * 100, 1) if mv['revenue'].sum() > 0 else 0
    guide_pct_views = round(guide_views / mv['views'].sum() * 100, 1) if mv['views'].sum() > 0 else 0

summary = {
    'period': '<Month Year>',
    'ga_total_views': ga['Views'].sum(),
    'ga_active_users': ga['Active users'].sum(),
    'mv_total_revenue': mv['revenue'].sum().round(2),
    'mv_weighted_rpm': round((mv['revenue'].sum() / mv['views'].sum()) * 1000, 2),
    'mv_guide_revenue': guide_revenue,
    'mv_guide_views': guide_views,
    'mv_guide_pct_revenue': guide_pct_revenue,
    'mv_guide_pct_views': guide_pct_views,
    'mv_non_guide_revenue': non_guide_revenue,
    'yt_total_views': int(yt_totals['Views']),
    'yt_watch_hours': round(float(yt_totals['Watch time (hours)']), 1),
    'yt_revenue': round(float(yt_totals['Estimated revenue (USD)']), 2),
    'yt_subscribers_gained': int(yt_totals.get('Subscribers', 0)),
    'combined_revenue': round(mv['revenue'].sum() + float(yt_totals['Estimated revenue (USD)']), 2),
}
```

Use `.get()` with defaults for columns that may not exist in every YouTube export (Subscribers, Impressions, etc.).

---

## Step 3 — Identify editorial signals

Run these analyses to generate the "Insights & Opportunities" section. See `references/editorial-signals.md` for how to interpret each signal.

1. **Traffic/Revenue mismatch**: pages with high views but low RPM vs. pages with low views but high RPM
2. **Engagement outliers**: pages with avg engagement time >60s (deep readers) vs. <10s (bounces)
3. **Series momentum**: which series gained the most total revenue across all weekly updates
4. **YouTube–Site alignment gap**: top YT franchise topics vs. top GA franchise topics — extract franchise/game names from both title sets and compare overlap
5. **Evergreen performers**: pages published before the current month that still rank in top 50 by views
6. **Daily traffic spikes**: days in `Chart data.csv` (the daily time series) that are >30% above daily average — note what likely caused them
7. **CTR vs. views mismatch on YouTube**: high CTR but low views = thumbnail/title works but reach is limited; low CTR but high views = algorithm is pushing it despite weak hook
8. **YouTube content type performance**: which types are generating the most views, watch time, and revenue? Which are underperforming relative to effort?
9. **Short_review vs. short_evergreen split**: are repurposed review Shorts outperforming or underperforming evergreen Shorts? What does that suggest about which Shorts to prioritize?
10. **Series health check**: for each named series, what is the avg views per episode vs. its benchmark? For series with fewer than 3 total episodes, report raw numbers only — no trend language.
11. **Release guide health**: which release guides are the top traffic and revenue drivers? Are any declining (could signal a series ending or losing search rank)? Are there trending anime/game series without a guide that should get one?

---

## Step 4 — Write the report

Output a `.md` file to `/mnt/user-data/outputs/FinalWeapon_[Month]_[Year]_Report.md`.

Follow the report template in `references/report-template.md` exactly. Do not invent new sections or reorder them.

---

## Step 5 — Present the file

Use the `present_files` tool to share the output markdown with the user.

Summarize in 2–3 sentences: total combined revenue, biggest traffic driver, and one key recommendation.

---

## Edge Cases

- **Missing Mediavine data**: skip the ad revenue and release guide sections; note it at the top of the report.
- **Missing YouTube data**: skip YouTube sections; note it.
- **Missing Google Analytics**: use Mediavine `views` column as the traffic proxy; note the difference.
- **GA file has no comment header** (different export format): try loading normally first; if columns don't match, try `skiprows=0`.
- **YouTube export is a flat CSV** (not a ZIP): look for `Video title` and `Views` columns directly; skip daily chart and totals sections.
- **No Duration column in YouTube export**: classify videos by title patterns only (the classifier handles `duration_seconds=None`).
- **Very small Mediavine dataset** (<20 rows): skip series grouping; just show all rows ranked by revenue.
- **Date range mismatch between sources**: note it in the report header. Do not normalize — report each source's own date range.
- **Series with fewer than 3 total episodes** (e.g., memory//card): report raw numbers; skip "growing/stalling/declining" language.
- **Columns that may be absent**: use `.get()` or `if col in df.columns` checks for Subscribers, Impressions, Duration, CTR, and Revenue columns — not all YouTube exports include all columns.

---

## Reference files

- `references/report-template.md` — Full markdown report template with all sections and placeholder text. **Read this before writing the report.**
- `references/editorial-signals.md` — How to interpret each of the 11 editorial signals and translate them into plain-English recommendations.
- `references/youtube-content-taxonomy.md` — Full rules, examples, and edge cases for classifying every Final Weapon YouTube video into a content type. **Read this before classifying videos.**
- `scripts/parse_slug.py` — Extracts a clean series name from a Mediavine URL slug. Also provides `is_release_guide()` for identifying release/schedule guide pages.
