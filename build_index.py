#!/usr/bin/env python3
"""Build index.json from packs/*.json. Run in the repo root. Stdlib only.
Bump "v" in the old index by one when a pack's sha256 changes."""
import json, glob, hashlib, os, datetime
old = {}
if os.path.exists('index.json'):
    for p in json.load(open('index.json', encoding='utf8')).get('packs', []):
        old[p['file']] = p
packs = []
for f in sorted(glob.glob('packs/*.json')):
    raw = open(f, 'rb').read(); j = json.loads(raw.decode('utf8'))
    L = j['lessons'][0]; sha = hashlib.sha256(raw).hexdigest(); o = old.get(f, {})
    v = o.get('v', 0) + (0 if o.get('sha256') == sha else 1)
    packs.append({'subject': L['subject'], 'grade': L['grade'], 'semester': L['semester'], 'file': f,
                  'count': len(j['lessons']), 'v': v, 'bytes': len(raw), 'sha256': sha, 'reviewed': True,
                  'images': 'separate' if j.get('images') == 'separate' else 'none'})
json.dump({'schema': 2, 'updatedAt': datetime.datetime.utcnow().strftime('%Y-%m-%dT%H:%M:%SZ'), 'packs': packs},
          open('index.json', 'w', encoding='utf8'), ensure_ascii=False, indent=1)
print(len(packs), 'packs')
