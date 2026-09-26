"""Find affine maps from the three named seeds to all normalized models.

Map discovery is not a proof premise: verify.py checks each map directly.
"""
from itertools import product
import json
from pathlib import Path

HERE=Path(__file__).resolve().parent
P=list(product(range(5),repeat=3))
N=[v for v in P if any(v) and next(x for x in v if x)==1]


def det(A):
    a,b,c=A
    return (a[0]*(b[1]*c[2]-b[2]*c[1])-a[1]*(b[0]*c[2]-b[2]*c[0])
            +a[2]*(b[0]*c[1]-b[1]*c[0]))%5


def main():
    models=json.loads((HERE/'models.json').read_text())
    targets={tuple(m['sections']) for m in models};maps={}
    small=3238
    affine2=[(a,b,c,d,e,f) for a,b,c,d in product(range(5),repeat=4)
             if (a*d-b*c)%5 for e,f in product(range(5),repeat=2)]
    basis=[(1,0,0),(0,1,0),(0,0,1)]
    for seed in json.loads((HERE/'seeds.json').read_text()):
        S=[P[i] for i in seed['points']]
        lows=[(v,t) for v in N for t in range(5)
              if sum(sum(a*b for a,b in zip(v,p))%5==t for p in S)==6]
        for v,t in lows:
            for scale in range(1,5):
                X=[scale*x%5 for x in v];tx=-scale*t%5
                Y,Z=next((y,z) for y in basis for z in basis if det([X,y,z]))
                initial=[((sum(a*b for a,b in zip(X,p))+tx)%5,
                          sum(a*b for a,b in zip(Y,p))%5,
                          sum(a*b for a,b in zip(Z,p))%5) for p in S]
                C=[(y,z) for x,y,z in initial if x==0]
                for a,b,c,d,e,f in affine2:
                    mask=sum(1<<(5*((a*y+b*z+e)%5)+(c*y+d*z+f)%5) for y,z in C)
                    if mask!=small:
                        continue
                    image=[(x,(a*y+b*z+e)%5,(c*y+d*z+f)%5) for x,y,z in initial]
                    my=sum(y for x,y,z in image if x==1)%5
                    mz=sum(z for x,y,z in image if x==1)%5
                    image=[(x,(y-x*my)%5,(z-x*mz)%5) for x,y,z in image]
                    sections=tuple(sum(1<<(5*y+z) for x,y,z in image if x==layer)
                                   for layer in range(5))
                    if sections not in targets:
                        raise RuntimeError('seed image absent from complete census')
                    A=[X,[(a*Y[j]+b*Z[j]-my*X[j])%5 for j in range(3)],
                       [(c*Y[j]+d*Z[j]-mz*X[j])%5 for j in range(3)]]
                    translation=[tx,(e-my*tx)%5,(f-mz*tx)%5]
                    maps.setdefault(sections,{'seed':seed['name'],'matrix':A,
                                              'translation':translation})
    if set(maps)!=targets:
        raise RuntimeError(('unidentified models',len(targets-set(maps))))
    for m in models:
        m['affine_map']=maps[tuple(m['sections'])]
    (HERE/'models.json').write_text('[\n'+',\n'.join(json.dumps(m,separators=(',',':'))
                                                   for m in models)+'\n]\n')
    print('Explicit affine maps found:',len(models))


if __name__=='__main__':
    main()
