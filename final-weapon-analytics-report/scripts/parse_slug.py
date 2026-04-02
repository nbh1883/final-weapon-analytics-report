"""
parse_slug.py
-------------
Extracts a clean series name from a Mediavine URL slug.
Also provides is_release_guide() to identify release/schedule guide pages.

Usage:
    from parse_slug import extract_series, group_by_series, is_release_guide

    series_name = extract_series("/2026/03/19/jujutsu-kaisen-season-3-release-dates-schedule-episodes-crunchyroll/")
    # → "Jujutsu Kaisen"

    is_guide = is_release_guide("/2026/03/19/jujutsu-kaisen-season-3-release-dates-schedule-episodes-crunchyroll/")
    # → True

    series_revenue = group_by_series(mediavine_df)
    # → pd.Series indexed by series name, values = total revenue
"""

import re
import pandas as pd

# Suffixes to strip from slugs before extracting the series name.
# Order matters — more specific patterns first.
_STRIP_PATTERNS = [
    r'-release-dates?-schedule-and-episodes?.*',
    r'-release-dates?-schedule-episodes?.*',
    r'-release-dates?-and-episodes?.*',
    r'-release-dates?.*',
    r'-schedule-and-episodes?.*',
    r'-schedule-episodes?.*',
    r'-season-\d+.*',
    r'-part-\d+.*',
    r'-episode-\d+.*',
    r'-anime.*',
    r'-crunchyroll.*',
    r'-hidive.*',
    r'-netflix.*',
    r'-review.*',
    r'-interview.*',
    r'-guide.*',
    r'-explained.*',
    r'-how-to.*',
    r'-update.*',
    r'-announced.*',
    r'-confirmed.*',
    r'-trailer.*',
]

# Compiled combined pattern
_STRIP_RE = re.compile('(' + '|'.join(_STRIP_PATTERNS) + ')', re.IGNORECASE)

# Date segment at start of path: /YYYY/MM/DD/
_DATE_RE = re.compile(r'^/?\d{4}/\d{2}/\d{2}/')

# Release guide detection patterns
_RELEASE_GUIDE_RE = re.compile(
    r'(release-dates?|'
    r'schedule-and-episodes?|'
    r'schedule-episodes?|'
    r'when-does.*-come-out|'
    r'when-is.*-release|'
    r'episode-guide|'
    r'airing-schedule|'
    r'release-schedule)',
    re.IGNORECASE
)


def is_release_guide(slug: str) -> bool:
    """
    Returns True if the slug looks like a release/schedule guide page.

    These are the weekly-updated anime/game release date pages that drive
    the majority of Final Weapon's site traffic and Mediavine revenue.

    Examples:
        "/2026/03/19/jujutsu-kaisen-season-3-release-dates-schedule-episodes-crunchyroll/"
        → True

        "/2026/03/16/pokemon-pokopia-review/"
        → False

        "/2026/03/27/fire-force-season-3-release-dates-schedule-episodes-time-crunchyroll/"
        → True
    """
    return bool(_RELEASE_GUIDE_RE.search(slug))


def extract_series(slug: str) -> str:
    """
    Given a Mediavine slug string, return a clean series/topic name.

    Examples:
        "/2026/03/19/jujutsu-kaisen-season-3-release-dates-schedule-episodes-crunchyroll/"
        → "Jujutsu Kaisen"

        "/2026/03/16/pokemon-pokopia-review/"
        → "Pokémon Pokopia"  (note: raw slug won't have accent; that's fine)

        "/2023/04/29/final-fantasy-iii-summon-locations-guide/"
        → "Final Fantasy III"

        "/"  (homepage)
        → "Homepage"
    """
    slug = slug.strip()

    # Homepage
    if slug in ('/', ''):
        return 'Homepage'

    # Strip leading date
    slug_clean = _DATE_RE.sub('', slug).strip('/')

    # Strip trailing slash
    slug_clean = slug_clean.rstrip('/')

    # Strip known suffixes
    slug_clean = _STRIP_RE.sub('', slug_clean)

    # Strip known page-type prefixes (interview, review standalone pages, etc.)
    slug_clean = re.sub(r'^interview-[^-]+-[^-]+-', '', slug_clean, flags=re.IGNORECASE)
    slug_clean = re.sub(r'^(review|preview|feature|opinion|interview)-', '', slug_clean, flags=re.IGNORECASE)

    # Convert hyphens to spaces and title-case
    name = slug_clean.replace('-', ' ').strip().title()

    return name if name else slug


def group_by_series(df: pd.DataFrame, slug_col: str = 'slug', value_col: str = 'revenue') -> pd.Series:
    """
    Groups a Mediavine dataframe by extracted series name and sums the value column.

    Returns a pd.Series sorted descending by total value.

    Args:
        df: Mediavine dataframe
        slug_col: Column containing URL slugs
        value_col: Column to aggregate (default: 'revenue')
    """
    df = df.copy()
    df['_series'] = df[slug_col].apply(extract_series)
    grouped = df.groupby('_series')[value_col].sum().sort_values(ascending=False)
    grouped.index.name = 'series'
    return grouped


def top_series_table(df: pd.DataFrame, n: int = 15, slug_col: str = 'slug') -> pd.DataFrame:
    """
    Returns a formatted DataFrame with series, total_revenue, total_views, weighted_rpm.

    Args:
        df: Mediavine dataframe (must have slug, revenue, views columns)
        n: Number of top series to return
        slug_col: Column containing URL slugs
    """
    df = df.copy()
    df['_series'] = df[slug_col].apply(extract_series)

    agg = df.groupby('_series').agg(
        total_revenue=('revenue', 'sum'),
        total_views=('views', 'sum'),
        page_count=(slug_col, 'count'),
    ).reset_index()

    agg['weighted_rpm'] = (agg['total_revenue'] / agg['total_views'] * 1000).round(2)
    agg['total_revenue'] = agg['total_revenue'].round(2)
    agg = agg.sort_values('total_revenue', ascending=False).head(n)
    agg.columns = ['Series', 'Revenue ($)', 'Total Views', 'Pages', 'Weighted RPM ($)']
    return agg.reset_index(drop=True)


def release_guide_table(df: pd.DataFrame, slug_col: str = 'slug', n: int = 15) -> pd.DataFrame:
    """
    Returns a table of release guide pages ranked by revenue.

    Args:
        df: Mediavine dataframe (must have slug, revenue, views, rpm columns)
        slug_col: Column containing URL slugs
        n: Number of top guides to return
    """
    df = df.copy()
    guides = df[df[slug_col].apply(is_release_guide)].copy()
    if guides.empty:
        return pd.DataFrame(columns=['Series', 'Views', 'Revenue ($)', 'RPM ($)'])

    guides['_series'] = guides[slug_col].apply(extract_series)
    agg = guides.groupby('_series').agg(
        total_revenue=('revenue', 'sum'),
        total_views=('views', 'sum'),
    ).reset_index()

    agg['weighted_rpm'] = (agg['total_revenue'] / agg['total_views'] * 1000).round(2)
    agg['total_revenue'] = agg['total_revenue'].round(2)
    agg = agg.sort_values('total_revenue', ascending=False).head(n)
    agg.columns = ['Series', 'Total Views', 'Revenue ($)', 'Weighted RPM ($)']
    return agg.reset_index(drop=True)


if __name__ == '__main__':
    # Quick smoke test
    test_slugs = [
        "/2026/03/19/jujutsu-kaisen-season-3-release-dates-schedule-episodes-crunchyroll/",
        "/2026/03/08/you-and-i-are-polar-opposites-release-dates-schedule-episodes-crunchyroll/",
        "/2026/03/13/dark-moon-the-blood-altar-release-dates-schedule-episodes-crunchyroll/",
        "/2023/04/29/final-fantasy-iii-summon-locations-guide/",
        "/2026/03/16/pokemon-pokopia-review/",
        "/2026/03/17/interview-christoffer-bodegard-esoteric-ebb/",
        "/2026/03/27/fire-force-season-3-release-dates-schedule-episodes-time-crunchyroll/",
        "/",
    ]
    print("=== Series extraction ===")
    for s in test_slugs:
        print(f"{s!r:80s} → {extract_series(s)!r}")

    print("\n=== Release guide detection ===")
    for s in test_slugs:
        print(f"{s!r:80s} → guide={is_release_guide(s)}")
