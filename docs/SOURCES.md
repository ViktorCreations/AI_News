# Source access map

Which sources are reachable from the daily session, and how. Verified
2026-09-14 by fetching every entry.

## The two failure classes

A 403 while researching is almost never the egress proxy. Tell them apart
before doing anything else:

| Symptom | Meaning | What to do |
|---|---|---|
| curl reports a failed `CONNECT`, or `recentRelayFailures` in `curl -sS "$HTTPS_PROXY/__agentproxy/status"` names the host | Organization egress policy refuses the host | **Report it. Do not route around it.** |
| `HTTP/1.1 200 Connection Established` followed by an origin `403` (`cf-mitigated: challenge`, `AkamaiGHost`, `x-px-blocked: 1`) | The tunnel worked; the site's bot edge refused us | Use the route below |

Every domain on this page is the second kind. None of them is blocked by
policy — the proxy tunnels to all of them.

There are also two *clients*, and they are blocked differently. `WebFetch`
is refused by several origins that answer plain curl with 200, and it
independently refuses a few hosts of its own (`feeds.bbci.co.uk`). So
"WebFetch returned 403" does not mean the page is unreachable — try
`scripts/fetch.py` before giving up on a source.

## Usage

```
python3 scripts/fetch.py <url>            # readable text; feeds render as dated items
python3 scripts/fetch.py <url> --raw      # unmodified body
python3 scripts/fetch.py <url> --check    # status line only
python3 scripts/fetch.py --route <url>    # what works for this host, without fetching
```

On a 403 it prints the known route for that host rather than failing blind.
It never silently substitutes one URL for another: which page we cite and
which page we verified against has to be a deliberate choice.

**No user-agent spoofing.** The script sends curl's own identity. Where a
site turns curl away we go to a feed that site publishes, rather than
impersonating a browser to defeat its bot protection. OpenAI is the clean
example: `robots.txt` is `Allow: /` with a published sitemap, so the
challenge is a blanket edge rule and the feed is the front door.

## Routes

| Source | Direct | Route that works |
|---|---|---|
| **openai.com** | 403 (Cloudflare challenge) | `https://openai.com/news/rss.xml` — the whole archive, 1,190+ items, title + link + one-line description + pubDate |
| **cnbc.com** | 403 (Akamai) | `https://search.cnbc.com/rs/search/combinedcms/view.xml?partnerId=wrss01&id=19854910` (Technology). Other ids: 10000664 Business, 15839069 Markets, 10001147 Finance |
| **zillow.com/research** | 403 (PerimeterX) | `https://zillow.mediaroom.com/` — same monthly market and rent reports, dated |
| **forbes.com** | 403 on article paths | `https://www.forbes.com/innovation/feed2/`, `https://www.forbes.com/business/feed/` |
| **bbc.com** | 302 | `https://www.bbc.co.uk/...` for articles; `https://feeds.bbci.co.uk/news/technology/rss.xml` for the feed — **the feed host is refused by WebFetch specifically**, so use `scripts/fetch.py` |
| **housingwire.com** | 200 to curl, **403 to WebFetch** | Fetch article URLs with `scripts/fetch.py`; scan the beat via `https://www.housingwire.com/feed/` |
| multifamilydive.com | 200 | `https://www.multifamilydive.com/feeds/news/` |
| nationalmortgagenews.com | 200 | `https://www.nationalmortgagenews.com/feed` |
| techcrunch.com / the-decoder.com / theverge.com | 200 | `/feed/`, `/feed/`, `/rss/index.xml` |
| **arstechnica.com** | **403 on article pages as of 2026-09-19** (was 200) | `https://arstechnica.com/feed/` still answers and carries full headlines, links and summaries — enough to find a story, not to write one. Source the article elsewhere |

## Unreachable — no route found

Do not treat a story as verified because one of these is "the source". Either
corroborate it somewhere reachable or drop it under "when uncertain, drop".

| Source | Status | Note |
|---|---|---|
| **inman.com** | 403 everywhere, both clients, including `/feed/` | On the approved trade-press list in CLAUDE.md but **not actually readable**. An Inman-only real-estate story cannot be verified here |
| **ssrn.com** | Cloudflare challenge on `papers.ssrn.com` and `ssrn.com/abstract=` | Metadata via `api.crossref.org` or `api.openalex.org` (title, authors, date, DOI). For the text, find the author's own copy. Never characterise a preprint's findings from an abstract page you could not read |
| **x.com** | 200, but an empty SPA shell — post text never arrives | A post is not verifiable here. A story sourced only to a tweet is unsourced. This is why the Andreas Thom allegation stayed out |
| apnews.com | 403 | — |
| reuters.com | 401 | Cite the outlet carrying the wire |
| wsj.com / bloomberg.com | 403 + paywall | Cite whoever reports on it |

## Maintenance

Bot rules change. When a source starts or stops working, update both this
table and `ROUTES` in `scripts/fetch.py` — the script's suggestions are only
as good as that dict. Re-verify the whole table if a run hits several
unexpected blocks at once.
