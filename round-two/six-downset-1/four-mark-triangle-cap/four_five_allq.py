"""Bounded FOUR-mark even-five coefficient producer.

Fresh d=1+u,l=2+v,h=l+d,q=8+w domain, all u,v,w>=0.
The complete original row/sector bridge is an ordinary UNFORMALIZED
argument in PROOF.md. This PRIVATE producer does not independently
prove that bridge or certify its own coefficient identities.
"""
import os
for name in ('OPENBLAS_NUM_THREADS','OMP_NUM_THREADS','MKL_NUM_THREADS',
             'BLIS_NUM_THREADS','NUMEXPR_NUM_THREADS','VECLIB_MAXIMUM_THREADS'):
    os.environ[name]='1'
from pathlib import Path
from fractions import Fraction as F
import json,signal,time,resource,traceback
from trivariate import P,R,ATOMS,PROBES,DEN_CACHE,atom
from pack_certificate import pack,unpack

def require(ok,msg):
    if not ok:raise ValueError(msg)

def encode(p):
    return dict(denominator=p.den,terms=[[list(e),str(c)] for e,c in sorted(p.a.items())])

def coded(z):
    z=R(z)
    return dict(numerator=encode(z.num),denominator_factors=[
        dict(factor=encode(ATOMS[k]),power=e) for k,e in sorted(z.den.items())])

def five(q,h,l):
    d=h-l;s=q+3*h;ell=3*(h+3*l)+1;N=2*q+6*(h+3*l)
    D=3*h
    G=[4*(q-1),4*D,4*D*(q-4),12*q*D,3*s*d/(3*h*l)]
    S=[[R(0) for j in range(5)] for i in range(5)]
    S[0][0]=4*(q*q-1);S[0][1]=S[1][0]=-4*D*(q-1)
    S[1][1]=4*D*D;S[2][2]=8*D*D*(q-4);S[3][3]=24*q*D*D
    jx=[0,-2,q-4,3*q,0];jl=[0,-2,q-4,-q,s*d/(3*h*l)]
    z=[-2*(q-1),18*l,-3*(q-4)*(h+3*l),-9*q*d,-3*s*d/h]
    for image,mult in ((jx,3*h),(jl,9*l),(z,1/ell)):
        for i in range(5):
            for j in range(5):S[i][j]+=mult*image[i]*image[j]
    A=[[(N-1 if i==j else 0)-S[i][j]/G[i] for j in range(5)] for i in range(5)]
    return A

def main():
    def alarm(a,b):raise TimeoutError('unchanged60s five-block guard')
    signal.signal(signal.SIGALRM,alarm);signal.alarm(60);started=time.monotonic()
    ATOMS.clear();PROBES.clear();DEN_CACHE.clear()
    u=R(P({(1,0,0):1}));v=R(P({(0,1,0):1}));w=R(P({(0,0,1):1}))
    d=1+u;l=2+v;h=l+d;q=8+w;s=q+3*h;ell=3*(h+3*l)+1
    rows=[];updates=[];forms={};stage='initialize';status='INCOMPLETE';trace=None
    try:
        for z in (d,l,h,q,q-1,q-4,s,ell):atom(R(z).num)
        stage='construct complete five-direction cap'
        a=five(q,h,l)
        from trivariate import rational_value
        original=json.loads((Path(__file__).resolve().parent/'FOUR-MARK-FIRST-SECTOR.json').read_text())
        GG=[[F(x) for x in row] for row in original['grams']['first-even-five']]
        SS=[[F(x) for x in row] for row in original['frames']['first-even-five']]
        require([[rational_value(z,(0,0,0)) for z in row] for row in a]
             ==[[F(69 if i==j else 0)-SS[i][j]/GG[i][i] for j in range(5)] for i in range(5)],
             'EVERY new even-five formula bound to actual original N70 block before coefficient trial')
        forms['four-even-five-allq']=[[coded(z) for z in row] for row in a]
        for k in range(5):
            stage='pivot '+str(k+1);pivot=a[k][k]
            positive=pivot.num.positive()
            denpositive=all(ATOMS[z].positive() for z in pivot.den)
            rows.append(dict(group='four-even-five-allq',order=k+1,pivot=coded(pivot),
                shifted_numerator=encode(pivot.num),positive=positive,
                denominator_positive=denpositive,degree=pivot.num.degree(),
                terms=len(pivot.num.a),shifted_terms=len(pivot.num.a)))
            print(json.dumps({key:rows[-1][key] for key in ('order','positive',
                'denominator_positive','degree','terms')}),flush=True)
            require(positive and denpositive,'five-block complete coefficient sign unproved')
            atom(pivot.num)
            for i in range(k+1,5):
                for j in range(k+1,5):
                    stage='Schur '+str((k,i,j))
                    before=a[i][j];left=a[i][k];right=a[k][j]
                    after=before-(left/pivot)*right
                    require(pivot*(before-after)==left*right,'exact five-block field identity')
                    updates.append(dict(group='four-even-five-allq',k=k,i=i,j=j,
                        before=coded(before),left=coded(left),right=coded(right),
                        pivot=coded(pivot),after=coded(after)))
                    a[i][j]=after
        require(len(rows)==5 and len(updates)==30,'whole five pivots and ordered local updates')
        status='ALL5 PIVOTS COEFFICIENT POSITIVE; separate whole reader and ordinary geometry bridges remain separate/unformalized'
    except (ValueError,TimeoutError) as e:
        status='INCOMPLETE: '+str(e);trace=traceback.format_exc()
    finally:
        signal.alarm(0)
        data=dict(agent='six-downset-1',role='researcher',domain='u,v,w>=0; d=1+u,l=2+v,h=l+d,q=8+w',
            guards=dict(child_seconds=60,polynomial_terms=512,packing_bytes=33554432,native_threads=1),
            forms=forms,rows=rows,updates=updates)
        compact=pack(data);back=unpack(compact)
        for key in ('domain','guards','forms','rows','updates'):
            require(data[key]==back[key],'whole lossless field/identity packing')
        folder=Path(__file__).resolve().parent
        raw=json.dumps(compact,separators=(',',':'))+'\n'
        require(len(raw.encode())<=32*1024*1024,'unchanged32MiB certificate guard')
        (folder/'FOUR-EVEN-FIVE-ALLQ-CERTIFICATE.json').write_text(raw)
        result=dict(agent='six-downset-1',role='researcher',status=status,stage=stage,traceback=trace,
            certificate_bytes=len(raw.encode()),pivots=len(rows),local_updates=len(updates),
            complete_form_fields=sum(len(row) for a in forms.values() for row in a),
            seconds=time.monotonic()-started,peak_KiB=resource.getrusage(resource.RUSAGE_SELF).ru_maxrss)
        (folder/'FOUR-EVEN-FIVE-ALLQ-RESULT.json').write_text(json.dumps(result,indent=2)+'\n')
        print(json.dumps(result),flush=True)

if __name__=='__main__':main()
