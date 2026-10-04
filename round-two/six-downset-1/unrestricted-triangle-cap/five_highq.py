"""bounded whole five-direction high-q coefficient producer.

Fresh d=1+u,l=2+v,h=l+d,q=3h+w domain, all u,v,w>=0.
The complete original row/sector bridge is supplied by PROOF.md.
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
    d=h-l;s=q+3*h;ell=3*(h+l)+1;N=2*q+6*(h+l)
    G=[4*(q-1),12*h,6*h*(q-2),6*h*q,s*d/(3*h*l)]
    S=[[R(0) for j in range(5)] for i in range(5)]
    S[0][0]=4*(q*q-1);S[0][1]=S[1][0]=-12*h*(q-1)
    S[1][1]=36*h*h;S[2][2]=36*h*h*(q-2);S[3][3]=36*h*h*q
    jx=[0,-2,q-2,q,0];jy=[0,-2,q-2,-q,s*d/(3*h*l)]
    z=[-2*(q-1),6*l,-3*(q-2)*(h+l),-3*q*d,-s*d/h]
    for image,mult in ((jx,3*h),(jy,3*l),(z,1/ell)):
        for i in range(5):
            for j in range(5):S[i][j]+=mult*image[i]*image[j]
    A=[[(N-1 if i==j else 0)-S[i][j]/G[i] for j in range(5)] for i in range(5)]
    return A

def main():
    def alarm(a,b):raise TimeoutError('unchanged60s five-block guard')
    signal.signal(signal.SIGALRM,alarm);signal.alarm(60);started=time.monotonic()
    ATOMS.clear();PROBES.clear();DEN_CACHE.clear()
    u=R(P({(1,0,0):1}));v=R(P({(0,1,0):1}));w=R(P({(0,0,1):1}))
    d=1+u;l=2+v;h=l+d;q=3*h+w;s=q+3*h;ell=3*(h+l)+1
    rows=[];updates=[];forms={};stage='initialize';status='INCOMPLETE';trace=None
    try:
        for z in (d,l,h,q,q-1,q-2,s,ell):atom(R(z).num)
        stage='construct complete five-direction cap'
        a=five(q,h,l);forms['five-highq']=[[coded(z) for z in row] for row in a]
        for k in range(5):
            stage='pivot '+str(k+1);pivot=a[k][k]
            positive=pivot.num.positive()
            denpositive=all(ATOMS[z].positive() for z in pivot.den)
            rows.append(dict(group='five-highq',order=k+1,pivot=coded(pivot),
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
                    updates.append(dict(group='five-highq',k=k,i=i,j=j,
                        before=coded(before),left=coded(left),right=coded(right),
                        pivot=coded(pivot),after=coded(after)))
                    a[i][j]=after
        require(len(rows)==5 and len(updates)==30,'whole five pivots and ordered local updates')
        status='ALL5 PIVOTS COEFFICIENT POSITIVE; validate with check_five.py; physical bridge in PROOF.md'
    except (ValueError,TimeoutError) as e:
        status='INCOMPLETE: '+str(e);trace=traceback.format_exc()
    finally:
        signal.alarm(0)
        data=dict(agent='six-downset-1',role='researcher',domain='u,v,w>=0; d=1+u,l=2+v,h=l+d,q=3h+w',
            guards=dict(child_seconds=60,polynomial_terms=512,packing_bytes=33554432,native_threads=1),
            forms=forms,rows=rows,updates=updates)
        compact=pack(data);back=unpack(compact)
        for key in ('domain','guards','forms','rows','updates'):
            require(data[key]==back[key],'whole lossless field/identity packing')
        folder=Path(__file__).resolve().parent
        raw=json.dumps(compact,separators=(',',':'))+'\n'
        require(len(raw.encode())<=32*1024*1024,'unchanged32MiB certificate guard')
        (folder/'FIVE-HIGHQ-CERTIFICATE.json').write_text(raw)
        result=dict(agent='six-downset-1',role='researcher',status=status,stage=stage,traceback=trace,
            certificate_bytes=len(raw.encode()),pivots=len(rows),local_updates=len(updates),
            complete_form_fields=sum(len(row) for a in forms.values() for row in a),
            seconds=time.monotonic()-started,peak_KiB=resource.getrusage(resource.RUSAGE_SELF).ru_maxrss)
        (folder/'FIVE-HIGHQ-RESULT.json').write_text(json.dumps(result,indent=2)+'\n')
        print(json.dumps(result),flush=True)

if __name__=='__main__':main()
