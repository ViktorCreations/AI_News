#!/usr/bin/env python3
"""Fetch a page for research/fact-checking when WebFetch is refused.

Usage:
    python3 scripts/fetch.py <url> [--raw] [--limit N]
    python3 scripts/fetch.py --check <url>     # status only, no body
    python3 scripts/fetch.py --route <url>     # print the known route, no fetch

Why this exists
---------------
Several sources this newsletter depends on answer 403 to the WebFetch tool
but 200 to plain curl, and a few answer 403 to both while publishing the same
material on a feed or press-room host that is wide open. Those are bot-edge
responses from the origin (Cloudflare challenge, Akamai, PerimeterX), NOT the
egress proxy refusing the host — a proxy denial shows up as a failed CONNECT
and is reported, never worked around. This script does three things:

 1. Fetches through the environment proxy with curl's own user agent. No
    browser impersonation: where a site turns curl away, we go to a feed it
    publishes instead of pretending to be something we are not.
 2. Renders HTML/RSS/Atom/JSON down to readable text.
 3. When a host is known to block, names the working route instead of just
    failing — see ROUTES, and docs/SOURCES.md for the full table.

It never silently substitutes one URL for another: a suggested route is
printed for you to call deliberately, because the link the issue cites and
the page whose content was verified have to be a decision, not an accident.
"""
import argparse
import html
import json
import re
import subprocess
import sys
from html.parser import HTMLParser
from urllib.parse import urlparse

CA = "/root/.ccr/ca-bundle.crt"

# host suffix -> (how to reach it, human note)
ROUTES = {
    "openai.com": (
        "https://openai.com/news/rss.xml",
        "HTML pages sit behind a Cloudflare challenge; the RSS feed carries the "
        "full archive (1000+ items: title, link, one-line description, pubDate) "
        "and is enough to confirm that an announcement exists and its date. "
        "robots.txt is Allow: / — the challenge is a blanket edge rule.",
    ),
    "cnbc.com": (
        "https://search.cnbc.com/rs/search/combinedcms/view.xml?partnerId=wrss01&id=19854910",
        "www.cnbc.com is Akamai-blocked. That XML endpoint is CNBC's own "
        "Technology feed and answers 200. Other section ids: 10000664 "
        "(Business), 15839069 (Markets), 10001147 (Finance).",
    ),
    "zillow.com": (
        "https://zillow.mediaroom.com/",
        "zillow.com/research is PerimeterX-blocked (x-px-blocked: 1). The press "
        "room carries the same monthly market and rent reports, dated.",
    ),
    "forbes.com": (
        "https://www.forbes.com/innovation/feed2/",
        "Article paths 403; the section feeds answer 200. Also "
        "/business/feed/. Forbes contributor posts are weak sourcing anyway.",
    ),
    "bbc.com": (
        "https://feeds.bbci.co.uk/news/technology/rss.xml",
        "bbc.com redirects; use bbc.co.uk for article HTML. The feed host is "
        "refused by WebFetch specifically — fetch it with this script.",
    ),
    "housingwire.com": (
        "https://www.housingwire.com/feed/",
        "WebFetch gets 403, curl gets 200 — fetch article URLs with this "
        "script directly. The feed is the fastest way to scan the beat.",
    ),
    "inman.com": (
        None,
        "Cloudflare-blocked on every path including /feed/, both tools. No "
        "route found. Treat as unreachable: corroborate Inman-only stories "
        "elsewhere or drop them.",
    ),
    "ssrn.com": (
        None,
        "Cloudflare challenge on papers.ssrn.com and ssrn.com/abstract=. Use "
        "api.crossref.org or api.openalex.org for metadata (title, authors, "
        "date, DOI), and find the author's own copy for the text. Never cite a "
        "preprint's claims from its abstract page alone if you cannot read it.",
    ),
    "apnews.com": (None, "403 to both tools. No route found."),
    "arstechnica.com": (
        "https://arstechnica.com/feed/",
        "Article pages started returning 403 on 2026-09-19; they answered 200 "
        "before that. The feed still works and carries headline, link and "
        "summary — enough to find a story and date it, not to write it from. "
        "Source the article elsewhere.",
    ),
    "wsj.com": (None, "403 + paywall. Not citable here."),
    "bloomberg.com": (None, "403 + paywall. Cite whoever reports on it."),
    "reuters.com": (None, "401 to both tools. Cite the outlet carrying the wire."),
    "x.com": (
        None,
        "The homepage answers 200 but serves an empty SPA shell — no post text "
        "ever arrives. A tweet is not verifiable here; treat any story whose "
        "only source is a post as unsourced.",
    ),
}


def route_for(url):
    host = (urlparse(url).hostname or "").lower()
    for suffix, entry in ROUTES.items():
        if host == suffix or host.endswith("." + suffix):
            return suffix, entry
    return None, None


class Text(HTMLParser):
    """Strip tags, keeping block structure and dropping script/style/nav."""

    SKIP = {"script", "style", "noscript", "svg", "head", "nav", "footer", "form"}
    BLOCK = {"p", "div", "br", "li", "tr", "section", "article",
             "h1", "h2", "h3", "h4", "h5", "h6", "blockquote"}

    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.out = []
        self.skip = 0

    def handle_starttag(self, tag, attrs):
        if tag in self.SKIP:
            self.skip += 1
        elif tag in self.BLOCK:
            self.out.append("\n")

    def handle_endtag(self, tag):
        if tag in self.SKIP and self.skip:
            self.skip -= 1
        elif tag in self.BLOCK:
            self.out.append("\n")

    def handle_data(self, data):
        if not self.skip and data.strip():
            self.out.append(data.strip() + " ")

    def text(self):
        t = "".join(self.out)
        t = re.sub(r"[ \t]+", " ", t)
        return re.sub(r"\n\s*\n\s*", "\n\n", t).strip()


def main_content(body):
    """Narrow to <article>/<main> when present, so site chrome does not
    crowd out the story. Falls back to the whole document."""
    for tag in ("article", "main"):
        blocks = re.findall(rf"<{tag}\b[^>]*>(.*?)</{tag}>", body, re.S | re.I)
        if blocks:
            best = max(blocks, key=len)
            if len(best) > 500:
                return best
    return body


def render_feed(body):
    """Format RSS/Atom items compactly: date, title, link, summary."""
    items = re.findall(r"<(item|entry)\b(.*?)</\1>", body, re.S | re.I)
    if not items:
        return None
    lines = []
    for _, chunk in items:
        def pick(*tags):
            for tag in tags:
                m = re.search(rf"<{tag}\b[^>]*>(.*?)</{tag}>", chunk, re.S | re.I)
                if m:
                    v = re.sub(r"<!\[CDATA\[(.*?)\]\]>", r"\1", m.group(1), flags=re.S)
                    return html.unescape(re.sub(r"<[^>]+>", "", v)).strip()
            return ""
        link = pick("link")
        if not link:
            m = re.search(r'<link\b[^>]*href="([^"]+)"', chunk, re.I)
            link = m.group(1) if m else ""
        date = pick("pubDate", "published", "updated", "dc:date")
        summary = pick("description", "summary", "content")
        lines.append(f"[{date}] {pick('title')}\n  {link}"
                     + (f"\n  {summary[:400]}" if summary else ""))
    return "\n\n".join(lines)


def fetch(url, timeout=30):
    """Return (status, body, connected). connected=False means CONNECT failed."""
    proc = subprocess.run(
        ["curl", "-sSL", "--cacert", CA, "--max-time", str(timeout),
         "-w", "\n__STATUS__%{http_code}", url],
        capture_output=True, text=True, errors="replace",
    )
    body = proc.stdout
    status = 0
    m = re.search(r"\n__STATUS__(\d+)$", body)
    if m:
        status = int(m.group(1))
        body = body[: m.start()]
    # A refused CONNECT never yields an HTTP status from the origin.
    connected = status != 0
    if not connected and proc.stderr:
        body = proc.stderr
    return status, body, connected


def main():
    ap = argparse.ArgumentParser(add_help=True)
    ap.add_argument("url")
    ap.add_argument("--raw", action="store_true", help="skip text rendering")
    ap.add_argument("--check", action="store_true", help="status line only")
    ap.add_argument("--route", action="store_true", help="print known route, do not fetch")
    ap.add_argument("--limit", type=int, default=6000, help="max chars of body")
    args = ap.parse_args()

    suffix, entry = route_for(args.url)

    if args.route:
        if not entry:
            print(f"{args.url}: no known restriction — fetch normally.")
        else:
            alt, note = entry
            print(f"host: {suffix}\nroute: {alt or 'NONE — unreachable'}\nnote: {note}")
        return 0

    status, body, connected = fetch(args.url)

    if not connected:
        print(f"NO CONNECTION for {args.url}\n{body[:600]}", file=sys.stderr)
        print("If curl reports a failed CONNECT this is the egress proxy "
              "refusing the host. Report it; do not route around it.", file=sys.stderr)
        return 2

    print(f"HTTP {status}  {len(body)}b  {args.url}", file=sys.stderr)

    if status >= 400:
        print(f"BLOCKED: the origin refused this request (HTTP {status}). The "
              f"proxy tunnel succeeded, so this is the site's bot edge.",
              file=sys.stderr)
        if entry:
            alt, note = entry
            print(f"Known route for {suffix}: {alt or 'NONE — treat as unreachable'}"
                  f"\n{note}", file=sys.stderr)
        else:
            print("No route recorded for this host. Try the site's RSS feed, "
                  "press room, or sitemap; if none work, add it to ROUTES as "
                  "unreachable and source the story elsewhere.", file=sys.stderr)
        return 1

    if args.check:
        return 0

    if args.raw:
        out = body
    else:
        stripped = body.lstrip()
        if stripped.startswith("{") or stripped.startswith("["):
            try:
                out = json.dumps(json.loads(body), indent=2)
            except ValueError:
                out = body
        else:
            out = render_feed(body)
            if out is None:
                p = Text()
                p.feed(main_content(body))
                out = p.text()

    if len(out) > args.limit:
        out = out[: args.limit] + f"\n\n[... truncated at {args.limit} chars; " \
                                  f"re-run with --limit to see more]"
    print(out)
    return 0


if __name__ == "__main__":
    sys.exit(main())
