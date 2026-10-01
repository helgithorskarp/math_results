"""Produce the saturated two-minimum lift from the native P24 to P23.

Ordinary marked costs only; no conditional domains or suffix search are folded.
"""
import hashlib
import importlib.util
import json
from pathlib import Path
import resource
import time

ROOT = Path(__file__).resolve().parent
PINS = {
    'fixture.json': '93b7cda51cc14fa8f53c0ed89c7c1c2150b8ab6b58f823fc69b41ec7035022e6',
    'NESTED.md': '3c291c8796cc7586db522d515098debf769482dc5b2d6bf8467fd8aa03322433',
}
PROFILE_SHA256 = 'dca9c8d6331c3fc548c514ca8f5f1cd170f4a0bb39a3c05250876247d0362719'
P24_GRAPH = 'bafkreieelq5auvzgfgmbfzwzvam5canm3neqjv35ybhmnne76bs5ymswpy'


def checked(name, pin):
    raw = (ROOT / name).read_bytes()
    if hashlib.sha256(raw).hexdigest() != pin:
        raise ValueError('published dependency changed: ' + name)
    return raw


raw = (ROOT.parent / 'semantic-pruning/profile.py').read_bytes()
if hashlib.sha256(raw).hexdigest() != PROFILE_SHA256:
    raise ValueError('published column profiler changed')
spec = importlib.util.spec_from_file_location('p23_column', ROOT.parent / 'semantic-pruning/profile.py')
s = importlib.util.module_from_spec(spec); spec.loader.exec_module(s)


def digest(obj):
    return hashlib.sha256(json.dumps(obj, separators=(',', ':')).encode()).hexdigest()


def move(mask, gate):
    a, b = gate
    x, y = mask >> a & 1, mask >> b & 1
    # Marked minima move to the first endpoint; both minima stay marked.
    if not x and y:
        mask ^= (1 << a) | (1 << b)
    return mask, bool(x or y)


def transition(envelope, gate):
    result = {}
    for mask, d in envelope:
        new, hit = move(mask, gate)
        result[new] = max(result.get(new, -1), d + hit)
    return [[mask, result[mask]] for mask in sorted(result)]


def build():
    fixture = json.loads(checked('fixture.json', PINS['fixture.json']))
    checked('NESTED.md', PINS['NESTED.md'])
    prefix = fixture['gates'][:23]
    family = s.analyze_family(13, prefix, 2, 0)
    envelope = [[z[0], z[2]] for z in family['envelope']]
    if envelope != [[3,8],[5,7],[17,7]]:
        raise ValueError('required saturation profile differs')
    cases = []
    for a in range(13):
        for b in range(a + 1, 13):
            gate = [a,b]
            successor = transition(envelope, gate)
            mass = sum(2 ** d for _,d in successor)
            if mass > 512:
                category = 'forbidden_by_saturation'
            elif {a,b} & {1,2,4}:
                category = 'forced_live_merge'
            else:
                category = 'invisible_to_two_minima'
            cases.append({'gate': gate, 'ordinary_envelope': successor,
                          'ordinary_mass': mass, 'category': category})
    forced = [c['gate'] for c in cases if c['category'] == 'forced_live_merge']
    if forced != [[2,4]] or prefix + forced != fixture['gates'][:24]:
        raise ValueError('forced extension is not the excluded native P24')
    return {'schema':'native23-saturation-v1','agent':'six-sorting-2','role':'researcher',
            'parent_files_sha256':PINS,'n':13,'size_budget':44,'small_size_lower_bound':35,
            'prefix_length':23,'prefix_sha256':digest(prefix),
            'original_family_records_sha256':digest(family['records']),
            'ordinary_envelope':envelope,'ordinary_mass':512,'forced_gate':[2,4],
            'next_prefix_sha256':digest(fixture['gates'][:24]),'p24_theorem_graph':P24_GRAPH,
            'safe_gates': [c['gate'] for c in cases if c['category'] == 'invisible_to_two_minima'],
            'forbidden_gate_count':sum(c['category'] == 'forbidden_by_saturation' for c in cases),
            'cases':cases}


def main():
    start=time.monotonic()
    data=build()
    out=ROOT/'p23-certificate.json'
    out.write_text(json.dumps(data,sort_keys=True,indent=2)+'\n')
    print(json.dumps({'status':'NATIVE23_SATURATION_CERTIFICATE_REGENERATED','agent':'six-sorting-2',
                      'role':'researcher','standard_next_gates':len(data['cases']),
                      'safe_gates':len(data['safe_gates']),'forbidden_gates':data['forbidden_gate_count'],
                      'forced_gate':data['forced_gate'],'bytes':out.stat().st_size,
                      'certificate_sha256':hashlib.sha256(out.read_bytes()).hexdigest(),
                      'seconds':time.monotonic()-start,
                      'maximum_rss_kib':resource.getrusage(resource.RUSAGE_SELF).ru_maxrss},sort_keys=True))


if __name__ == '__main__':
    main()
