"""Separate injection/owner decoder and inventory checker; no solver.

This verifies the finite reductions. PROOF.md supplies the ordinary
good-friend bridge and states every imported theorem and review boundary.
"""
import argparse
from collections import Counter
import copy
import hashlib
from itertools import combinations, permutations
import json
from pathlib import Path

HERE=Path(__file__).resolve().parent
MANIFEST_SHA='83adc2817c988fa4450ede02c7da09b4da857e3f1850a0b0d0dee4cfd4a24bca'
BASELINE_SHA='cf71ac44391d86eeb244cbf75de3fee5cfbedb36081175a830e7571acf370c7d'

def check(ok,message):
    if not ok:raise ValueError(message)
def encode(obj):return (json.dumps(obj,sort_keys=True,separators=(',',':'))+'\n').encode()
def digest(obj):return hashlib.sha256(encode(obj)).hexdigest()

def decode_row(mi,ci,u,masks):
    check(type(u) is int and 0<=u<17,'mark domain')
    check(len(masks)==len(set(masks))==19,'nineteen distinct masks')
    rho=[0]*17;owner=[[-1]*17 for _ in range(17)]
    for wi,w in enumerate(masks):
        check(type(w) is int and 0<w<1<<17 and w.bit_count()==4,'four-subset mask domain')
        for a in range(17):
            if not w>>a&1:continue
            rho[a]+=1
            for b in range(a+1,17):
                if w>>b&1:
                    check(owner[a][b]==-1,'a pair is repeated')
                    owner[a][b]=wi
    check(sum(rho)==76 and max(rho)<=5 and rho[u]==5,'replication and mark')
    low=[i for i in range(17) if rho[i]==5];high=[i for i in range(17) if rho[i]<5]
    leave=[(a,b) for a in range(17) for b in range(a+1,17) if owner[a][b]==-1]
    check(len(leave)==22,'leave cardinality')
    ll=[list(p) for p in leave if p[0] in low and p[1] in low]
    check(len(ll) in (1,2) and len({a for p in ll for a in p})==2*len(ll),'positive low-low matching')
    check(sorted(rho) in ([4]*9+[5]*8,[3]+[4]*7+[5]*9),'classified replication profile')
    cm=0
    for w in masks:
        if w>>u&1:cm|=w
    C=[i for i in range(17) if i!=u and cm>>i&1]
    outside=[i for i in range(17) if i!=u and not cm>>i&1]
    check(len(C)==15 and len(outside)==1,'common tail domain')
    x=outside[0];check(tuple(sorted((u,x))) in leave,'uvx absent')
    friends=[]
    for y in high:
        xs=[a for a in low if a!=u and owner[min(a,y)][max(a,y)]==-1]
        if xs:friends.append([y,xs])
    check(all(a in C for y,xs in friends for a in xs),'all friends are covered')
    check(len({a for y,xs in friends for a in xs})==sum(len(xs) for y,xs in friends),
          'friends counted at distinct centers')
    return {'model':mi,'class':ci,'u':u,'x':x,'blocks':sorted(masks),'rho':rho,'low':low,'W':high,'C':C,
            'W_C':[i for i in high if i in C],'q':[[y,len(xs)] for y,xs in friends],'friends':friends,
            'low_low_pairs':ll,'sat_low_low':[p for p in ll if u not in p],
            'mu':len(ll),'j':int(x in low),'p':len(high),'k':sum(i in C for i in high),
            'heavy_v':[i for i in high if rho[i]==3]}

def carriers():
    raw=(HERE/'NINETEEN_STARS.json').read_bytes()
    check(hashlib.sha256(raw).hexdigest()==MANIFEST_SHA,'manifest integrity')
    data=json.loads(raw);rows=[];classes=0
    for mi,model in enumerate(data['models']):
        missing={};offset=0
        for n in model['cycle_half_lengths']:
            for r in range(offset,offset+n):missing[r]={r,offset+(r-offset+1)%n}
            offset+=n
        cells=[(r,c) for r in range(5) for c in range(5) if c not in missing[r]]
        labels={rc:i for i,rc in enumerate(cells)}
        anchors=[(1<<15)+sum(1<<labels[r,c] for c in range(5) if (r,c) in labels) for r in range(5)]
        anchors +=[(1<<16)+sum(1<<labels[r,c] for r in range(5) if (r,c) in labels) for c in range(5)]
        injections=set()
        for rs in combinations(range(5),4):
            for cs in permutations(range(5),4):
                if all((r,c) in labels for r,c in zip(rs,cs)):
                    injections.add(tuple(sorted(labels[r,c] for r,c in zip(rs,cs))))
        candidates=[sum(1<<i for i in w) for w in sorted(injections)]
        check(len(candidates) in (95,96),'anchor-compatible quadruple domain')
        for ci,e in enumerate(model['marked_classes']):
            classes+=1;masks=sorted(anchors+[candidates[i] for i in e['clique']])
            for u in range(17):
                if sum(w>>u&1 for w in masks)==5:rows.append(decode_row(mi,ci,u,masks))
    check(classes==46 and len(rows)==381,'complete classified mark domain')
    return rows

def screen(rows,sharp67):
    cases=[]
    for r in rows:
        costs={y:len(xs) for y,xs in r['friends']}
        for z in range(6):
            if z>sum(a in r['C'] and a!=r['u'] for a in r['low']):continue
            for c in range(min(5,len(r['W_C']))+1):
                for tc in combinations(r['W_C'],c):
                    for X in range(3):
                        if 2*X+z+c>5:continue
                        if sharp67 and X<len(r['sat_low_low']):continue
                        R=5+c-z-2*X
                        Q=sum(max(costs.get(y,0),2 if y in tc else 0) for y in r['W'])
                        if R>=Q:cases.append([r['model'],r['class'],r['u'],X,list(tc),z,Q,R])
    return sorted(cases,key=encode)

def checked_discharge(rows,cases):
    lookup={tuple(r[k] for k in ('model','class','u')):r for r in rows}
    check(len(lookup)==len(rows),'duplicate mark')
    exceptions=[];regular=0
    for s in cases:
        r=lookup[tuple(s[:3])];X,tc,z,Q,R=s[3:]
        check(r['mu']==1,'no mu2 inventory')
        if r['j']:
            check(X==0,'regular branch has no excess')
            q=sum(len(xs) for y,xs in r['friends'])
            check(q==15-r['p'],'all other low points are covered friends')
            # R >= p+2c-z-3 follows from the written transfer.
            check(R<r['p']+2*len(tc)-z-3,'strict regular-branch contradiction')
            regular+=1
        else:
            check(X==1 and z==0 and R==Q and len(r['sat_low_low'])==1,'exhausted exceptional branch')
            heavy=r['sat_low_low'][0];q=dict(r['q']);friends=dict(r['friends'])
            check(all(not set(xs)&set(heavy) for xs in friends.values()),'heavy endpoints are not friends')
            check(all(y not in heavy for y in tc),'covered T avoids heavy endpoints')
            qualifying=sorted(y for y in tc if r['rho'][y]==4 and len(friends.get(y,[]))>=2)
            check(qualifying,'local-lemma center exists')
            y=qualifying[0]
            check(q[y]+2>max(q[y],2),'additional u incidences exceed the budget')
            exceptions.append({'inventory':s,'center':y,'friends':friends[y],
                               'heavy_edge':heavy,'allocated':max(q[y],2),'required':q[y]+2})
    check(regular==700 and len(exceptions)==5,'complete discharge count')
    return {'regular_discharge_count':regular,'exceptional_discharge':exceptions}

def zero_mu_audit():
    necessary=[];final=[]
    for z in range(6):
        for c in range(6):
            for X in range(3):
                for p in range(10):
                    if 2*X+z+c>5:continue
                    q=16-p;R=5-z+c-2*X
                    if R<q or R<2*c:continue
                    check(X==0,'zero-mu excess contradiction')
                    row=[p,X,c,z,q,R];necessary.append(row)
                    if R>=p+2*c-z-2:final.append(row)
    check(necessary and not final,'zero-mu bound excludes every scalar case')
    return {'necessary_inventories':sorted(necessary),'after_good_friend_bound':final}

def grouped(rows,cases):
    lookup={tuple(r[k] for k in ('model','class','u')):r for r in rows};bins=Counter()
    for s in cases:
        r=lookup[tuple(s[:3])];bins[(r['mu'],r['j'],r['p'],s[3])]+=1
    return [[list(k),v] for k,v in sorted(bins.items())]

def readout(rows,raw,cut):
    return {'agent':'six-code-1','role':'researcher','status':'COMPLETE_NECESSARY_INVENTORY_READOUT',
            'manifest_sha256':MANIFEST_SHA,'low_hub_marks':len(rows),'carrier_sha256':digest(rows),
            'carrier_types':[[list(k),v] for k,v in sorted(Counter((r['mu'],r['j'],r['p']) for r in rows).items())],
            'before_sharp67':{'count':len(raw),'sha256':digest(raw),'groups':grouped(rows,raw)},
            'after_sharp67':{'count':len(cut),'sha256':digest(cut),'groups':grouped(rows,cut)},
            'discharge':checked_discharge(rows,cut),'zero_mu_audit':zero_mu_audit()}

def baseline():
    raw=(HERE/'acl69.txt').read_bytes();check(hashlib.sha256(raw).hexdigest()==BASELINE_SHA,'known69 fixture integrity')
    words=[line.strip() for line in raw.decode().splitlines() if line.strip()]
    check(len(words)==len(set(words))==69,'known69 cardinality')
    check(all(len(w)==18 and set(w)<=set('01') and w.count('1')==5 for w in words),'known69 weight')
    ds=Counter(sum(a!=b for a,b in zip(x,y)) for x,y in combinations(words,2))
    check(min(ds)==6 and sum(ds.values())==2346,'known69 distances')
    return {'words':69,'distances':dict(sorted(ds.items()))}

def controls(rows,cut,expected):
    failures=[]
    def reject(name,f):
        try:f()
        except (ValueError,KeyError,IndexError,TypeError):failures.append(name);return
        raise ValueError('control erroneously accepted: '+name)
    r=rows[0]
    reject('missing star block',lambda:decode_row(r['model'],r['class'],r['u'],r['blocks'][:-1]))
    reject('duplicate star block',lambda:decode_row(r['model'],r['class'],r['u'],r['blocks'][:-1]+r['blocks'][:1]))
    reject('point outside mask domain',lambda:decode_row(r['model'],r['class'],r['u'],r['blocks'][:-1]+[1<<17]))
    high=r['W'][0]
    reject('incorrect low hub marking',lambda:decode_row(r['model'],r['class'],high,r['blocks']))
    reject('mark outside domain',lambda:decode_row(r['model'],r['class'],17,r['blocks']))
    reject('missing inventory',lambda:check(readout(rows,screen(rows,False),cut[:-1])==expected,'inventory evidence differs'))
    reject('duplicate inventory',lambda:check(readout(rows,screen(rows,False),cut+cut[:1])==expected,'inventory evidence differs'))
    damaged=copy.deepcopy(cut);damaged[0][7]+=1
    reject('incorrect incidence budget',lambda:check(readout(rows,screen(rows,False),damaged)==expected,'budget evidence differs'))
    damaged=copy.deepcopy(expected);damaged['discharge']['exceptional_discharge'][0]['required']=0
    reject('false local charge bound',lambda:check(readout(rows,screen(rows,False),cut)==damaged,'false local conclusion'))
    damaged=copy.deepcopy(expected);damaged['after_sharp67']['count']-=1
    reject('incomplete coverage count',lambda:check(readout(rows,screen(rows,False),cut)==damaged,'coverage differs'))
    return failures

def main():
    p=argparse.ArgumentParser();p.add_argument('--compare-primary',action='store_true');p.add_argument('--out',type=Path);args=p.parse_args()
    rows=carriers();raw=screen(rows,False);cut=screen(rows,True);record=readout(rows,raw,cut)
    expected=json.loads((HERE/'expected.json').read_text())
    check(record==expected,'complete finite readout differs')
    if args.compare_primary:
        import produce
        check(rows==produce.carriers(),'all381 decoded marks compared entrywise')
        check(raw==produce.screen(rows),'raw inventory entrywise comparison')
        check(cut==produce.screen(rows,True),'restricted inventory entrywise comparison')
    result={'agent':'six-code-1','role':'researcher','status':'COMPLETE_SEPARATE_CHECK',
            'finite_record_sha256':digest(record),'baseline':baseline(),
            'controls':controls(rows,cut,expected),'entrywise_comparison':args.compare_primary,
            'low_hub_marks':len(rows),'raw_inventories':len(raw),'restricted_inventories':len(cut),
            'discharged_inventories':record['discharge']['regular_discharge_count']+len(record['discharge']['exceptional_discharge'])}
    if args.out:args.out.write_bytes(encode(result))
    print(json.dumps(result,sort_keys=True))

if __name__=='__main__':main()
