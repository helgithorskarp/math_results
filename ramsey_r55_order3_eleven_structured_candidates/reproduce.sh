#!/usr/bin/env bash
set -eu
cd -- "$(dirname -- "$0")"
sha256sum -c SHA256SUMS
python3 -B - <<'PY'
import hashlib,json
from pathlib import Path
import verify

root=Path.cwd()
expected=json.loads((root/'verification.json').read_text())
for source,pin in json.loads((root/'inputs.json').read_text()).items():
    data=(root.parent/source).read_bytes()
    verify.need({'bytes':len(data),'sha256':hashlib.sha256(data).hexdigest()}==pin,'input identity')
for core,row in expected['cores'].items():
    path=root/'graphs'/f'core{core}.edges'
    verify.need(hashlib.sha256(path.read_bytes()).hexdigest()==row['edges_sha256'],'graph identity')
    a=verify.audit(path,row['core_word'],True)
    actual={k:a[k] for k in ('core_word','red_edges','red_k5','blue_k5','defects')}
    actual.update(minimum_neighbor_score=a['one_orbit_neighbors']['minimum'],
                  improving=a['one_orbit_neighbors']['improving'],
                  neutral=a['one_orbit_neighbors']['neutral'],edges_sha256=row['edges_sha256'])
    verify.need(actual==row,'candidate audit '+core)
    if int(core)==expected['best_core']:
        # JSON round trip normalizes tuple/list and integer/string dictionary keys.
        verify.need(json.loads(json.dumps(a))==json.loads((root/'best_verification.json').read_text()),'best full audit')
    print('PASS',core,a['defects'],'defects;',a['one_orbit_neighbors']['minimum'],'minimum neighbor',flush=True)
verify.need(len(expected['cores'])==17,'fixture count')
print('PASS all 17 literal colorings and 5134 physical one-orbit neighbors')
PY
