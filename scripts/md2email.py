#!/usr/bin/env python3
"""Convert a newsletter markdown file to inline-styled email HTML.

Usage: python3 scripts/md2email.py newsletters/YYYY-MM-DD.md > /tmp/email.html
Handles the exact markdown subset used by CLAUDE.md's issue format:
h1/h2/h3, blockquote, bullets, links, bold, italic, hr.
"""
import re, sys, html

def inline(s):
    s = html.escape(s, quote=False)
    s = re.sub(r'\[([^\]]+)\]\((https?://[^\)]+)\)',
               r'<a href="\2" style="color:#1a5dab;text-decoration:none">\1</a>', s)
    s = re.sub(r'\*\*([^*]+)\*\*', r'<strong>\1</strong>', s)
    s = re.sub(r'(?<!\*)\*([^*]+)\*(?!\*)', r'<em>\1</em>', s)
    return s

def convert(md):
    out, in_list = [], False
    def close_list():
        nonlocal in_list
        if in_list:
            out.append('</ul>'); in_list = False
    for line in md.splitlines():
        l = line.rstrip()
        if l.startswith('# '):
            close_list(); out.append(f'<h1 style="font-size:22px;margin:0 0 12px">{inline(l[2:])}</h1>')
        elif l.startswith('### '):
            close_list(); out.append(f'<h3 style="font-size:16px;margin:18px 0 4px">{inline(l[4:])}</h3>')
        elif l.startswith('## '):
            close_list(); out.append(f'<h2 style="font-size:18px;margin:22px 0 6px;border-bottom:1px solid #ddd;padding-bottom:4px">{inline(l[3:])}</h2>')
        elif l.startswith('> '):
            close_list(); out.append(f'<blockquote style="margin:0 0 12px;padding:8px 14px;border-left:3px solid #1a5dab;color:#444;font-style:italic">{inline(l[2:])}</blockquote>')
        elif l.startswith('- '):
            if not in_list:
                out.append('<ul style="margin:6px 0 12px;padding-left:22px">'); in_list = True
            out.append(f'<li style="margin:6px 0">{inline(l[2:])}</li>')
        elif l == '---':
            close_list(); out.append('<hr style="border:none;border-top:1px solid #ddd;margin:18px 0">')
        elif l:
            close_list(); out.append(f'<p style="margin:6px 0 12px">{inline(l)}</p>')
    close_list()
    return ('<div style="font-family:Georgia,serif;max-width:640px;margin:0 auto;'
            'color:#222;line-height:1.55;font-size:15px">' + '\n'.join(out) +
            '<p style="color:#999;font-size:12px;margin-top:24px">Published at '
            '<a href="https://github.com/ViktorCreations/AI_News" style="color:#999">'
            'ViktorCreations/AI_News</a></p></div>')

if __name__ == '__main__':
    print(convert(open(sys.argv[1]).read()))
