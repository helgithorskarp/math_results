"""Exact necessary-inventory readout, six-code-1, researcher, 2026-10-01.

The unchanged nineteen-star classification is an imported theorem. This
program adds no enumeration of stars and asserts no realized global code.
"""
import argparse
from collections import Counter
import hashlib
from itertools import combinations, product
import json
from pathlib import Path

HERE=Path(__file__).resolve().parent
MANIFEST_SHA='83adc2817c988fa4450ede02c7da09b4da857e3f1850a0b0d0dee4cfd4a24bca'

def require(ok,message):
    if not ok:raise ValueError(message)

def encode(obj):return (json.dumps(obj,sort_keys=True,separators=(',',':'))+'\n').encode()
def digest(obj):return hashlib.sha256(encode(obj)).hexdigest()

def literal_row(mi,ci,u,words):
    pairs=[p for w in words for p in combinations(sorted(w),2)]
    require(len(words)==len(set(words))==19 and len(pairs)==len(set(pairs))==114,'nineteen pair packing')
    rho=[sum(i in w for w in words) for i in range(17)]
    require(rho[u]==5,'marked replication five')
    low={i for i in range(17) if rho[i]==5};W=set(range(17))-low
    leave=set(combinations(range(17),2))-set(pairs)
    ll=sorted(p for p in leave if set(p)<=low)
    C={i for w in words if u in w for i in w if i!=u}
    require(len(C)==15,'common tail union')
    x=next(i for i in range(17) if i!=u and i not in C)
    require(tuple(sorted((u,x))) in leave,'unique uvx absence')
    j=int(x in low);q=Counter();friends={}
    for a in sorted(low-{u}):
        ps=[b for b in range(17) if b!=a and tuple(sorted((a,b))) in leave]
        require(len(ps)==1,'unique low leave partner')
        b=ps[0]
        if b in W:
            require(a in C,'covered low friend')
            q[b]+=1;friends.setdefault(b,[]).append(a)
    satll=[list(p) for p in ll if u not in p]
    require(sum(q.values())==len(low)-1-2*len(ll)+j,'friend count')
    require(len(satll)==len(ll)-j,'saturated low-low count')
    return {'model':mi,'class':ci,'u':u,'x':x,'blocks':sorted(sum(1<<i for i in w) for w in words),
            'rho':rho,'low':sorted(low),'W':sorted(W),'C':sorted(C),'W_C':sorted(W&C),
            'q':[[a,q[a]] for a in sorted(q)],'friends':[[a,friends[a]] for a in sorted(friends)],
            'low_low_pairs':[list(p) for p in ll],'sat_low_low':satll,'mu':len(ll),'j':j,
            'p':len(W),'k':len(W&C),'heavy_v':sorted(i for i in W if rho[i]==3)}

def carriers():
    raw=(HERE/'NINETEEN_STARS.json').read_bytes()
    require(hashlib.sha256(raw).hexdigest()==MANIFEST_SHA,'pinned nineteen-star manifest')
    data=json.loads(raw);rows=[]
    for mi,model in enumerate(data['models']):
        holes=set();start=0
        for n in model['cycle_half_lengths']:
            for i in range(n):holes.update([(start+i,start+i),(start+i,start+(i+1)%n)])
            start+=n
        cells=sorted(set(product(range(5),repeat=2))-holes)
        anchors=[frozenset([15]+[i for i,rc in enumerate(cells) if rc[0]==r]) for r in range(5)]
        anchors +=[frozenset([16]+[i for i,rc in enumerate(cells) if rc[1]==c]) for c in range(5)]
        covered={p for w in anchors for p in combinations(sorted(w),2)}
        candidates=[frozenset(w) for w in combinations(range(15),4)
                    if not any(p in covered for p in combinations(w,2))]
        for ci,e in enumerate(model['marked_classes']):
            words=anchors+[candidates[i] for i in e['clique']]
            for u in range(17):
                if sum(u in w for w in words)==5:rows.append(literal_row(mi,ci,u,words))
    return rows

def screen(rows,sharp67=False):
    out=[]
    for r in rows:
        q=dict(r['q']);wc=r['W_C']
        for bits in range(1<<len(wc)):
            tc=[y for i,y in enumerate(wc) if bits>>i&1];c=len(tc)
            for X in range(3):
                if sharp67 and X<r['mu']-r['j']:continue
                for z in range(6):
                    if 2*X+z+c>5:continue
                    if z>sum(a!=r['u'] and a in r['C'] for a in r['low']):continue
                    R=5-z+c-2*X
                    Q=sum(max(q.get(y,0),2*int(y in tc)) for y in r['W'])
                    if Q<=R:out.append([r['model'],r['class'],r['u'],X,tc,z,Q,R])
    return sorted(out,key=encode)

def grouped(rows,cases):
    lookup={tuple(r[k] for k in ('model','class','u')):r for r in rows}
    bins=Counter()
    for c in cases:
        r=lookup[tuple(c[:3])];bins[(r['mu'],r['j'],r['p'],c[3])]+=1
    return [[list(k),v] for k,v in sorted(bins.items())]

def discharge(rows,cases):
    lookup={tuple(r[k] for k in ('model','class','u')):r for r in rows}
    exceptions=[];regular=0
    for s in cases:
        r=lookup[tuple(s[:3])];X=s[3];tc=s[4];z=s[5];Q=s[6];R=s[7]
        require(r['mu']==1,'no multiplicity-two leave survives')
        if r['j']==1:
            require(X==0 and sum(dict(r['q']).values())==15-r['p'],'regular branch premises')
            # Written good-friend transfer: c <= 8-p.
            require(len(tc)>8-r['p'],'regular branch contradiction')
            regular+=1
        else:
            require(X==1 and z==0 and R==Q,'exception exhausts the incidence budget')
            require(len(r['sat_low_low'])==1,'unique heavy saturated edge')
            heavy=set(r['sat_low_low'][0]);friends=dict(r['friends']);q=dict(r['q'])
            require(not heavy.intersection(a for xs in friends.values() for a in xs),
                    'forced friends avoid heavy endpoints')
            require(all(y not in heavy for y in tc),'covered T centers avoid heavy endpoints')
            ys=[y for y in tc if q.get(y,0)>=2 and r['rho'][y]==4]
            require(ys,'unit-v covered T center with at least two good friends')
            y=min(ys)
            require(q[y]+2>max(q[y],2),'local pair lemma strictly exceeds allocated cost')
            exceptions.append({'inventory':s,'center':y,'friends':friends[y],
                               'heavy_edge':sorted(heavy),'allocated':max(q[y],2),'required':q[y]+2})
    return {'regular_discharge_count':regular,'exceptional_discharge':exceptions}

def zero_mu_audit():
    before=[];after=[]
    for p in range(10):
        q=16-p
        for X in range(3):
            for c in range(6):
                for z in range(6):
                    if 2*X+z+c>5:continue
                    R=5-z+c-2*X
                    if R<max(q,2*c):continue
                    before.append([p,X,c,z,q,R])
                    require(X==0,'no internal excess when mu zero')
                    if c<=7-p:after.append([p,X,c,z,q,R])
    require(before and not after,'zero-mu contradiction')
    return {'necessary_inventories':before,'after_good_friend_bound':after}

def summary(rows):
    raw=screen(rows);cut=screen(rows,True)
    return {'agent':'six-code-1','role':'researcher','status':'COMPLETE_NECESSARY_INVENTORY_READOUT',
            'manifest_sha256':MANIFEST_SHA,'low_hub_marks':len(rows),'carrier_sha256':digest(rows),
            'carrier_types':[[list(k),v] for k,v in sorted(Counter((r['mu'],r['j'],r['p']) for r in rows).items())],
            'before_sharp67':{'count':len(raw),'sha256':digest(raw),'groups':grouped(rows,raw)},
            'after_sharp67':{'count':len(cut),'sha256':digest(cut),'groups':grouped(rows,cut)},
            'discharge':discharge(rows,cut),'zero_mu_audit':zero_mu_audit()}

def main():
    p=argparse.ArgumentParser();p.add_argument('--out',type=Path);args=p.parse_args()
    rows=carriers();require(len(rows)==381,'all381 low-hub marks')
    record=summary(rows)
    if args.out:args.out.write_bytes(encode(record))
    print(json.dumps(record,sort_keys=True))

if __name__=='__main__':main()
