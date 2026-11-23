"""Keeps the review numbers on the three deodorant sites in step with Yotpo.

Usage (from the repo root):
    python3 tools/reviews.py ORIG_COUNT ORIG_AVG ORIG_FIVE BSF_COUNT BSF_AVG BSF_FIVE
e.g. python3 tools/reviews.py 86 5.0 86 7 5.0 7

ORIG = "Aluminum-Free Natural Deodorant That Works" (handle natural-deodorant)
BSF  = "Baking Soda-Free Natural Deodorant for Sensitive Skin" (handle natural-deodorant-baking-soda-free)
Read them from the Shopify product metafields reviews.rating_count, reviews.rating (value)
and yotpo.preloaded_star_distribution (the "5" entry), which Yotpo keeps in sync.

It rewrites every review number and review phrase in the three index.html files,
saves reviews.json, and prints what changed. Never type numbers by hand.
"""
import json, os, re, sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SITES = {'simplebodydeodorant.com': 'orig', 'allnaturaldeodorant.com': 'bsf', 'monthlydeodorant.com': None}

def phrases(rv):
    o, b = rv['orig'], rv['bsf']
    total = o['count'] + b['count']
    avg = (o['avg'] * o['count'] + b['avg'] * b['count']) / total if total else 0
    allfive = (o['five_star'] + b['five_star']) == total
    f1 = lambda x: '%.1f' % x
    return {
        'total': str(total), 'avg': f1(avg), 'orig': str(o['count']), 'bsf': str(b['count']),
        'avg_orig': f1(o['avg']), 'avg_bsf': f1(b['avg']),
        'band': ('All %d reviews are five stars' % total) if allfive else ('Average of %d reviews' % total),
        'every': 'every review five stars' if allfive else 'across both formulas',
        'og': ('%d five-star reviews' % total) if allfive else ('%d reviews, rated %s' % (total, f1(avg))),
    }

def apply(html, rv, which):
    p = phrases(rv)
    html = re.sub(r'(<span data-rv="(\w+)">)[^<]*(</span>)', lambda m: m.group(1) + p[m.group(2)] + m.group(3), html)
    html = re.sub(r'data-to="[^"]*"( data-rv="(\w+)")', lambda m: 'data-to="%s"%s' % (p[m.group(2)], m.group(1)), html)
    html = re.sub(r'Rated [\d.]+ across \d+ reviews\.', 'Rated %s across %s reviews.' % (p['avg'], p['total']), html)
    html = re.sub(r'(content="Two formulas, five scents, ).*?(\. Made in Colorado Springs\.")', lambda m: m.group(1) + p['og'] + m.group(2), html)
    if which:
        html = re.sub(r'"ratingValue":"[\d.]+","reviewCount":"\d+"',
                      '"ratingValue":"%s","reviewCount":"%s"' % (p['avg_' + which], p[which]), html)
    return html

def main(args):
    if len(args) != 6:
        sys.exit(__doc__)
    oc, oa, of, bc, ba, bf = args
    new = {'orig': {'count': int(oc), 'avg': float(oa), 'five_star': int(of)},
           'bsf': {'count': int(bc), 'avg': float(ba), 'five_star': int(bf)}}
    path = os.path.join(ROOT, 'reviews.json')
    old = json.load(open(path))
    if old == new:
        print('No change: reviews already up to date.'); return
    for dom, which in SITES.items():
        f = os.path.join(ROOT, dom, 'index.html')
        s = open(f).read(); t = apply(s, new, which)
        open(f, 'w').write(t)
        print(dom, 'updated' if s != t else 'no visible change')
    json.dump(new, open(path, 'w'))
    print('Old:', old); print('New:', new)

if __name__ == '__main__':
    main(sys.argv[1:])
