"""Discover integer LP duals; six-code-1, researcher, 2026-10-01.

The optional solver is not part of the certificate check. Model reconstruction
adapts the credited literal decoder in our multiplicity-three artifact.
"""
import argparse
from collections import Counter
import hashlib
from itertools import combinations, product
import json
from pathlib import Path

HERE = Path(__file__).resolve().parent
MANIFEST_SHA = '83adc2817c988fa4450ede02c7da09b4da857e3f1850a0b0d0dee4cfd4a24bca'


def require(ok, message):
    if not ok:
        raise ValueError(message)


def encode(x):
    return (json.dumps(x, sort_keys=True, separators=(',', ':'))+'\n').encode()


def literal_carriers():
    raw=(HERE/'NINETEEN_STARS.json').read_bytes()
    require(hashlib.sha256(raw).hexdigest()==MANIFEST_SHA,'manifest hash')
    record=json.loads(raw)
    rows=[]
    for mi,model in enumerate(record['models']):
        holes=set(); start=0
        for size in model['cycle_half_lengths']:
            for i in range(size):
                holes.add((start+i,start+i))
                holes.add((start+i,start+(i+1)%size))
            start+=size
        cells=sorted(set(product(range(5),repeat=2))-holes)
        anchors=[frozenset([15]+[i for i,rc in enumerate(cells) if rc[0]==r])
                 for r in range(5)]
        anchors += [frozenset([16]+[i for i,rc in enumerate(cells) if rc[1]==c])
                    for c in range(5)]
        covered={p for w in anchors for p in combinations(sorted(w),2)}
        candidates=[frozenset(w) for w in combinations(range(15),4)
                    if not any(p in covered for p in combinations(w,2))]
        for ci,entry in enumerate(model['marked_classes']):
            words=anchors+[candidates[i] for i in entry['clique']]
            require(len(words)==len(set(words))==19,'block count')
            pairs=[p for w in words for p in combinations(sorted(w),2)]
            require(len(pairs)==len(set(pairs))==114,'pair repetition')
            rho=[sum(i in w for w in words) for i in range(17)]
            low={i for i,t in enumerate(rho) if t==5}
            high=set(range(17))-low
            leave=set(combinations(range(17),2))-set(pairs)
            ll=sorted(p for p in leave if set(p)<=low)
            for u in range(17):
                if rho[u]!=4:continue
                C={i for w in words if u in w for i in w if i!=u}
                W=high-{u}; q=Counter(); friends={}
                for a,b in sorted(leave):
                    if a in C&low and b in W:
                        q[b]+=1;friends.setdefault(b,[]).append(a)
                    if b in C&low and a in W:
                        q[a]+=1;friends.setdefault(a,[]).append(b)
                rows.append({'model':mi,'class':ci,'u':u,
                             'blocks':sorted(sum(1<<i for i in w) for w in words),
                             'rho':rho,'C':sorted(C),'W':sorted(W),'low':sorted(low),
                             'W_C':sorted(W&C),'q':[[i,q[i]] for i in sorted(q)],
                             'friends':[[i,sorted(friends[i])] for i in sorted(friends)],
                             'heavy_v':sorted(i for i in W if rho[i]==3),
                             'low_low_pairs':[list(p) for p in ll],
                             'mu':len(ll),'p':len(W),'k':len(W&C),
                             'LL_C_endpoints':sum(i in C for p in ll for i in p)})
    return rows


def screen(rows):
    coarse=[]; final=[]
    for r in rows:
        q=dict(r['q'])
        for X in range(3):
            for c in range(5):
                for z in range(5):
                    if 2*X+z+c>4:continue
                    for TC in combinations(r['W_C'],c):
                        R=4-z+c-2*X
                        Q=sum(max(q.get(y,0),2*(y in TC)) for y in r['W'])
                        if Q>R:continue
                        # X0: each disjoint LL edge avoiding Z needs a charged A endpoint.
                        if X==0 and Q+max(0,r['mu']-z)>R:continue
                        case=[r['model'],r['class'],r['u'],X,list(TC),z,Q,R]
                        coarse.append(case)
                        if any(q.get(y,0)>=2 and y not in r['heavy_v'] for y in TC):
                            continue  # Written shared-isolated-hub bridge.
                        final.append(case)
    return coarse,final


def lp_rows(r,e):
    """All rows are A x <= b for nonnegative candidate-word variables."""
    u=r['u']; words=[frozenset(i for i in range(17) if w>>i&1) for w in r['blocks']]
    forbidden={t for w in words for t in combinations(sorted(w),3)}
    candidates=[frozenset(w) for w in combinations(range(17),5)
                if not any(t in forbidden for t in combinations(w,3))]
    low=set(r['low']);good=low-{e};q=dict(r['q'])
    good_b=set(r['W_C'])-set(q)
    pmap={p:[j for j,w in enumerate(candidates) if set(p)<=w]
          for p in combinations(range(17),2)}
    tmap={t:[] for t in combinations(range(17),3) if t not in forbidden}
    for j,w in enumerate(candidates):
        for t in combinations(sorted(w),3):tmap[t].append(j)
    rows=[]
    def add(label,coeff,bound):rows.append((label,coeff,bound))
    for i in range(17):
        add(['point',i],{j:1 for j,w in enumerate(candidates) if i in w},
            (16 if i==u else 20)-r['rho'][i])
    for t,js in tmap.items():
        if js:add(['triple',*t],dict.fromkeys(js,1),1)
    for p,js in pmap.items():
        inc=sum(set(p)<=w for w in words)
        if u in p:
            other=next(x for x in p if x!=u)
            if other in good:
                add(['u-good-upper',*p],dict.fromkeys(js,1),4-inc)
                add(['u-good-lower',*p],dict.fromkeys(js,-1),inc-3)
            elif other in good_b:
                add(['u-good-b-lower',*p],dict.fromkeys(js,-1),inc-5)
            elif other==e:
                add(['u-exception-lower',*p],dict.fromkeys(js,-1),inc-2)
            elif other in r['W_C']:
                add(['u-covered-t-lower',*p],dict.fromkeys(js,-1),inc-3)
            else:
                lower=2 if q.get(other,0) else 4
                add(['u-outside-t-lower',*p],dict.fromkeys(js,-1),inc-lower)
            continue
        lower=5 if set(p)<=good or set(p)<=good_b else 4
        add(['pair',*p,lower],dict.fromkeys(js,-1),inc-lower)
        if inc==0 and set(p)&low:
            add(['forced-leave-upper',*p],dict.fromkeys(js,1),4)
        if set(p)&good:
            t=tuple(sorted((u,*p)));it=sum(set(t)<=w for w in words)
            coeff=dict.fromkeys(js,-1)
            for j in tmap.get(t,[]):coeff[j]=coeff.get(j,0)-1
            add(['good-coverage',*p],coeff,inc+it-5)
    return candidates,rows


def make_certificates(rows,scale=100000):
    # Import only for discovery. The checker needs no numerical libraries.
    import numpy as np
    from scipy.optimize import linprog
    from scipy.sparse import csr_matrix
    coarse,final=screen(rows)
    ids=sorted({tuple(c[:3]) for c in final})
    require(ids==[(0,17,14),(0,19,1),(1,11,7)],'unexpected residual carrier')
    require(all(c[3]==0 and c[5] in (0,1) and c[7]-c[6]==1-c[5]
                for c in coarse),'charge-exhaustion bridge changed')
    output=[]
    for cid in ids:
        r=next(r for r in rows if tuple(r[k] for k in ('model','class','u'))==cid)
        for e in r['low_low_pairs'][0]:
            cs,rs=lp_rows(r,e)
            rr=[];cc=[];vv=[]
            for i,(_,coeff,_) in enumerate(rs):
                for j,v in coeff.items():rr.append(i);cc.append(j);vv.append(v)
            A=csr_matrix((vv,(rr,cc)),shape=(len(rs),len(cs)))
            result=linprog(-np.ones(len(cs)),A_ub=A,
                           b_ub=np.array([b for _,_,b in rs]),bounds=(0,None),
                           method='highs-ds',options={'threads':1,'time_limit':40.0})
            require(result.success,'INCOMPLETE LP; no certificate')
            weights=[max(0,round(scale*(-float(x)))) for x in result.ineqlin.marginals]
            cover=[0]*len(cs)
            for w,(_,coeff,_) in zip(weights,rs):
                for j,v in coeff.items():cover[j]+=w*v
            repair=max(0,(scale-min(cover)+4)//5)
            for i,(label,_,_) in enumerate(rs):
                if label[0]=='point':weights[i]+=repair
            numerator=sum(w*b for w,(_,_,b) in zip(weights,rs))
            require(min(cover)+5*repair>=scale and numerator<52*scale,
                    'no strict exact integer bound; not an exclusion')
            output.append({'model':cid[0],'class':cid[1],'u':cid[2],'exception':e,
                           'scale':scale,'weights':[[label,w] for w,(label,_,_) in zip(weights,rs) if w]})
            print({'case':[*cid,e],'candidates':len(cs),'rows':len(rs),
                   'integer_bound':numerator,'scale':scale},flush=True)
    return {'format':'M4_INTEGER_DUAL_V1','cases':output}


def main():
    p=argparse.ArgumentParser();p.add_argument('--out',type=Path,required=True)
    args=p.parse_args()
    args.out.parent.mkdir(parents=True,exist_ok=True)
    args.out.write_bytes(encode(make_certificates(literal_carriers())))


if __name__=='__main__':main()
