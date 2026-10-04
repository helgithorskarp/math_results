"""New all-q closed forms against all three complete ORIGINAL inputs.

No producer, field-engine or sector imports. Independent reader formulas
are evaluated only for literal binding; universal signs use the whole
coefficient certificate and the ordinary proof, not these evaluations.
"""
from pathlib import Path
from fractions import Fraction as F
import json,time,resource,signal
from check_three_five import original_forms
from exact import require,vecadd,scale,dot,matvec,fingerprint


def bind(raw):
    n,h,l=raw['n'],raw['h'],raw['l']
    q,N=2**(n-1),len(raw['family'])
    rows=[[F(x) for x in row] for row in raw['all_physical_rows']]
    metric=[[F(x) for x in row] for row in raw['physical_metric']]
    oldsize=2*q-1
    old=rows[1:1+oldsize]
    G,gF=vecadd(*old),old[-1]
    H=[scale(-1,vecadd(*(old[i] for i in range(oldsize) if (i+1)&mark)))
       for mark in (1,2,4)]
    E,U=vecadd(G,scale(-1,gF)),vecadd(G,gF)
    R=vecadd(*H,scale(F(3,2),U))
    Hc=vecadd(scale(2,H[0]),scale(-1,H[1]),scale(-1,H[2]))
    bmeans=[]
    for group,start in ((1,h),(2,h+l)):
        marked=rows[1+oldsize+3*start:1+oldsize+3*(start+l)]
        bmeans.append(vecadd(scale(F(1,3*l),vecadd(*marked)),scale(F(-1,3*h),H[group])))
    basis=[E,U,R,Hc,vecadd(*bmeans)]
    images=[matvec(metric,v) for v in basis]
    GG=[[dot(v,im) for im in images] for v in basis]
    require(all(GG[i][j]==0 for i in range(5) for j in range(5) if i!=j)
            and min(GG[i][i] for i in range(5))>0, 'every original even metric position')
    scores=[[dot(row,im) for row in rows] for im in images]
    SS=[[dot(a,b) for b in scores] for a in scores]
    actual=[[F(N-1 if i==j else 0)-SS[i][j]/GG[i][i] for j in range(5)] for i in range(5)]
    point=(h-l-1,l-2,q-4)
    require(min(point)>=0, 'literal point belongs to complete all-q orthant')
    forms=original_forms()
    expected=[[F(num.evaluate(point,{}),den.evaluate(point,{})) for num,den in row]
              for row in forms]
    require(actual==expected,'ALL25 original even-cap positions against separate reader closed forms')
    return dict(n=n,counts=[h,l,l],N=N,s=q+3*h,point=point,
                complete_form_positions=25,actual_empty_row_in_frame=True,
                metric_sha256=fingerprint(GG),frame_sha256=fingerprint(SS),normalized_cap_sha256=fingerprint(actual))


if __name__=='__main__':
    def alarm(a,b):raise TimeoutError('unchanged60s original-form binding guard')
    signal.signal(signal.SIGALRM,alarm);signal.alarm(60);start=time.monotonic()
    folder=Path(__file__).resolve().parent
    controls=[bind(json.loads((folder/f'THREE-MARK-{name}-MATRIX.json').read_text()))
              for name in ('FIRST','SECOND','THIRD')]
    result=dict(agent='six-downset-1',role='researcher',private=True,complete=True,
        actual_original_form_positions=75,controls=controls,
        imports='separate whole reader plus credited rational vector primitives; no producer, sector or field engine',
        universal_identity_proof='complete certificate reader and ordinary PROOF.md, NOT interpolation',
        independently_reviewed=False,formalized=False)
    (folder/'THREE-ORIGINAL-FORM-BINDINGS.json').write_text(json.dumps(result,indent=2)+'\n')
    result['execution']=dict(seconds=time.monotonic()-start,
        peak_KiB=resource.getrusage(resource.RUSAGE_SELF).ru_maxrss,optimized=not __debug__)
    signal.alarm(0);print(json.dumps(result),flush=True)
