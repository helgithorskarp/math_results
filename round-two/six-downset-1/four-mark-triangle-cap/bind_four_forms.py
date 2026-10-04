"""Fresh all-q closed forms against both complete FOUR-mark original inputs.

Algorithm credited to source4dd74e66/bind_three_forms.py. New four-mark
original basis and point. No producer, sector or field-engine imports.
Literal bindings validate identities; generic signs use the complete reader.
"""
from pathlib import Path
from fractions import Fraction as F
import json, time, resource, signal
from check_four_five import original_forms
from exact import require, vecadd, scale, dot, matvec, fingerprint

def bind(raw):
    n, h, l = raw['n'], raw['h'], raw['l']
    q, N = 2**(n-1), len(raw['family'])
    require(type(n) is int and 4 <= n <= 6 and type(h) is int and 3 <= h <= 10
            and type(l) is int and 2 <= l < h and N == 2*q+6*(h+3*l) <= 80,
            'unchanged full original form binding guard')
    rows = [[F(x) for x in row] for row in raw['all_physical_rows']]
    metric = [[F(x) for x in row] for row in raw['physical_metric']]
    oldsize = 2*q-1
    old = rows[1:1+oldsize]
    G, gF = vecadd(*old), old[-1]
    H = [scale(-1, vecadd(*(old[i] for i in range(oldsize) if (i+1)&mark)))
         for mark in (1,2,4,8)]
    E, U = vecadd(G, scale(-1,gF)), vecadd(G,gF)
    R = vecadd(*H, scale(2,U))
    Hc = vecadd(scale(3,H[0]), *(scale(-1,v) for v in H[1:]))
    bmeans = []
    for group, start in ((1,h),(2,h+l),(3,h+2*l)):
        marked = rows[1+oldsize+3*start:1+oldsize+3*(start+l)]
        bmeans.append(vecadd(scale(F(1,3*l),vecadd(*marked)),
                            scale(F(-1,3*h),H[group])))
    basis = [E,U,R,Hc,vecadd(*bmeans)]
    images = [matvec(metric,v) for v in basis]
    GG = [[dot(v,im) for im in images] for v in basis]
    require(all(GG[i][j] == 0 for i in range(5) for j in range(5) if i != j)
            and min(GG[i][i] for i in range(5)) > 0, 'every original even metric position')
    scores = [[dot(row,im) for row in rows] for im in images]
    SS = [[dot(a,b) for b in scores] for a in scores]
    actual = [[F(N-1 if i == j else 0)-SS[i][j]/GG[i][i]
               for j in range(5)] for i in range(5)]
    point = (h-l-1,l-2,q-8)
    require(min(point) >= 0, 'literal point belongs to all-q shifted orthant')
    expected = [[F(num.evaluate(point,{}),den.evaluate(point,{})) for num,den in row]
                for row in original_forms()]
    require(actual == expected, 'ALL25 original even-cap positions against separate reader')
    return dict(n=n,counts=[h,l,l,l],N=N,s=q+3*h,point=point,
        complete_form_positions=25,actual_empty_row_in_frame=True,
        metric_sha256=fingerprint(GG),frame_sha256=fingerprint(SS),
        normalized_cap_sha256=fingerprint(actual))

if __name__ == '__main__':
    def alarm(a,b): raise TimeoutError('unchanged60s original-form binding guard')
    signal.signal(signal.SIGALRM,alarm); signal.alarm(60)
    start = time.monotonic(); folder = Path(__file__).resolve().parent
    controls = [bind(json.loads((folder/f'FOUR-MARK-{name}-MATRIX.json').read_text()))
                for name in ('FIRST','SECOND')]
    result = dict(agent='six-downset-1',role='researcher',private=True,complete=True,
        actual_original_form_positions=50,controls=controls,
        imports='separate reader plus credited rational primitives; no producer, sector or field engine',
        universal_identity_proof='complete certificate and ordinary PROOF.md, NOT interpolation',
        independently_reviewed=False,formalized=False)
    (folder/'FOUR-ORIGINAL-FORM-BINDINGS.json').write_text(json.dumps(result,indent=2)+'\n')
    result['execution'] = dict(seconds=time.monotonic()-start,
        peak_KiB=resource.getrusage(resource.RUSAGE_SELF).ru_maxrss,optimized=not __debug__)
    signal.alarm(0); print(json.dumps(result),flush=True)
