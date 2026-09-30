"""Meaningful malformed-certificate, load and exact-coverage controls."""
import copy
import json
from pathlib import Path
import tempfile
import check_all
import verify


def run():
    root = Path(__file__).resolve().parent
    original = json.loads((root/'certificates/phase-184.json').read_text())
    mutations = []
    def mutate(name,fn):
        c=copy.deepcopy(original);fn(c);mutations.append((name,c))
    mutate('zero denominator',lambda c:c.update(denominator=0))
    mutate('negative mu',lambda c:c.update(mu_numerator=-1))
    mutate('false mu type',lambda c:c.update(mu_numerator=True))
    mutate('noninvariant bridge',lambda c:c.update(inner=[1287,2416]))
    mutate('empty bridge',lambda c:c.update(inner=[1852,1852]))
    mutate('wrong right phase',lambda c:c.update(t=(c['t']+1)%617))
    mutate('compatible sign',lambda c:c.update(g=0))
    mutate('wrong modulus',lambda c:c.update(P=619))
    mutate('unknown field',lambda c:c.update(unknown=0))
    mutate('negative AP weight',lambda c:c['color0_APs'][0].__setitem__(2,-1))
    mutate('bool AP weight',lambda c:c['color0_APs'][0].__setitem__(2,True))
    mutate('constant AP',lambda c:c['color0_APs'][0].__setitem__(1,0))
    mutate('AP outside window',lambda c:c['color0_APs'][0].__setitem__(0,-1))
    mutate('duplicate AP',lambda c:c['color0_APs'].append(c['color0_APs'][0][:]))
    mutate('capacity overload',lambda c:c['color0_APs'][0].__setitem__(2,1000000000))
    mutate('insufficient spatial mu',lambda c:c.update(mu_numerator=0))
    a,d,w=original['color0_APs'][0]
    mutate('opposite reference color',lambda c:c['color0_APs'][0].__setitem__(0,3703-a-6*d))
    # A positive-step crossing AP at an actual free pole, with all bounds valid.
    mutate('free-pole AP',lambda c:c['color0_APs'][0].__setitem__(slice(None),[1668,31,1]))
    rejected=[]
    for name,c in mutations:
        try:verify.check(c)
        except ValueError:rejected.append(name)
        else:raise RuntimeError('Control accepted: '+name)
    with tempfile.TemporaryDirectory() as tmp:
        p=Path(tmp)
        for f in (root/'certificates').glob('phase-*.json'):
            (p/f.name).write_bytes(f.read_bytes())
        (p/'phase-269.json').unlink()
        try:check_all.check_directory(p)
        except ValueError:rejected.append('incomplete four-phase coverage')
        else:raise RuntimeError('Partial coverage accepted')
        (p/'phase-269.json').write_bytes((root/'certificates/phase-205.json').read_bytes())
        try:check_all.check_directory(p)
        except ValueError:rejected.append('phase filename mismatch')
        else:raise RuntimeError('Wrong phase coverage accepted')
    print(json.dumps({'status':'CONTROLS_PASSED','rejected':rejected,'count':len(rejected)}))


if __name__ == '__main__':
    run()
