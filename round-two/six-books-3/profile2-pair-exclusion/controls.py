"""Semantic damages, positive prefixes, physical spines and exact count planes."""
import contextlib
import copy
import hashlib
import io
import json
from pathlib import Path

import check
import physical
from witness_kernel import accumulate

ROOT=Path(__file__).resolve().parent


def digest(value):
    return hashlib.sha256(json.dumps(value,sort_keys=True,separators=(',',':')).encode()).hexdigest()


def primary_baseline():
    raw=(ROOT/'primary21.txt').read_bytes()
    physical.require(hashlib.sha256(raw).hexdigest()==
        '3b648b66a5990d0b6ed945ce80d3f546e90f2b233f924775bb02ac2418558a55',
        'Primary21 fixture differs')
    A,_=json.JSONDecoder().raw_decode(raw.decode())
    n=len(A)
    physical.require(n==21 and all(len(r)==n for r in A), 'Primary order differs')
    physical.require(all(type(A[i][j]) is int and A[i][j] in (0,1)
        and A[i][j]==A[j][i] and (i!=j or A[i][j]==0)
        for i in range(n) for j in range(n)), 'Primary encoding differs')
    red=[{j for j in range(n) if j!=i and A[i][j]==0} for i in range(n)]
    blue=[{j for j in range(n) if j!=i and A[i][j]==1} for i in range(n)]
    pages=[[],[]];literal=[]
    for i in range(n):
        for j in range(i+1,n):
            cr=len(red[i]&red[j]);cb=len(blue[i]&blue[j]);edge=j in red[i]
            physical.require(cb==n-2-len(red[i])-len(red[j])+cr+2*int(edge),
                             'Physical complement endpoint identity differs')
            c=cr if edge else cb
            physical.require(c<=(3 if edge else 6), 'Primary violates ordinary page cap')
            pages[0 if edge else 1].append(c);literal.append([i,j,int(edge),cr,cb])
    return dict(order=n,red_edges=len(pages[0]),blue_edges=len(pages[1]),
        whole_spines=len(literal),page_maxima=list(map(max,pages)),
        all_endpoint_identities_checked=len(literal),whole_physical_sha256=digest(literal),
        upper23_flag_certificate_replayed=False,baseline_validation_only=True)


def count_planes():
    complete=[]
    for m in range(10):
        words=[sum(1<<j for j in range(1<<m) if j & (1<<z)) for z in range(m)]
        planes=accumulate(words,(1<<m)-1,lambda a,b:a&b,lambda a,b:a^b)
        actual=[sum(((p>>j)&1)*(1<<k) for k,p in enumerate(planes)) for j in range(1<<m)]
        expected=[sum((j>>z)&1 for z in range(m)) for j in range(1<<m)]
        physical.require(actual==expected,'Binary planes differ from scalar membership count')
        complete.append(expected)
    for plane in (0,3):
        damaged=list(planes);damaged[plane]^=1
        actual=[sum(((p>>j)&1)*(1<<k) for k,p in enumerate(damaged)) for j in range(1<<9)]
        physical.require(actual!=complete[-1],'Damaged count plane escaped detection')
    return dict(complete_membership_patterns=sum(map(len,complete)),maximum_inputs=9,
                whole_scalar_sha256=digest(complete),plane_damages_detected=2)


def semantic(packet,initial_packet):
    require=physical.require
    prefix=copy.deepcopy(packet);prefix['removals']=[]
    prefix['current_sizes']=list(prefix['initial_sizes']);prefix['pending']=None
    positive=check.verify(prefix)
    require(not positive['claim_template_excluded'] and positive['checked_stars']==0,
            'No-action positive prefix differs')
    first=copy.deepcopy(prefix);first['removals']=[packet['removals'][0]]
    first['current_sizes'][first['removals'][0]['x']]-=1
    one=check.verify(first)
    require(one['checked_stars']==1 and not one['claim_template_excluded'],
            'Valid single-removal prefix differs')
    initial=check.verify(initial_packet)
    require(initial['initial_empty']==[5] and initial['checked_stars']==0
            and initial['claim_template_excluded'],'Initial-empty positive differs')
    damages=[]

    def rejected(name,mutate,base=prefix,expected=None):
        bad=copy.deepcopy(base);mutate(bad)
        try:
            check.verify(bad)
        except (ValueError,KeyError,TypeError,IndexError) as error:
            if expected is not None:
                require(expected in str(error),'Damage rejected at wrong mathematical boundary')
            damages.append(name)
        else:
            raise ValueError('Semantic damage accepted: '+name)

    rejected('wrong-counts',lambda p:p['profile_counts'].__setitem__(2,2))
    rejected('wrong-degree-type',lambda p:p['types'].__setitem__(0,1))
    rejected('wrong-column',lambda p:p['columns'].__setitem__(0,1))
    rejected('wrong-initial-margin',lambda p:p['initial_sizes'].__setitem__(0,0))
    rejected('fake-final-empty',lambda p:p['current_sizes'].__setitem__(0,0))
    rejected('claimed-unverified-exclusion',lambda p:p.__setitem__('claim_template_excluded',True))
    rejected('wrong-color-rule',lambda p:p.__setitem__('rule','UNCOLORED'))
    rejected('diagonal-star',lambda p:p['removals'][0].__setitem__('star',
        p['removals'][0]['star'] | (1<<p['removals'][0]['x'])),base=first)
    rejected('bad-pair-endpoint',lambda p:p['removals'][0].__setitem__('y',
        p['removals'][0]['x']),base=first)
    rejected('duplicate-removal',lambda p:p['removals'].append(copy.deepcopy(p['removals'][0])),base=first)
    rejected('actions-after-final-empty',lambda p:p['removals'].append(copy.deepcopy(p['removals'][-1])),base=packet)
    rejected('initial-empty-extra-action',lambda p:p.__setitem__('removals',[dict(x=0,star=0,y=1)]),base=initial_packet)
    # A claim that a genuinely supported first-domain star is unsupported.
    # Derive the support from actual colored neighborhoods independently here.
    counts,types,low_rows,budget,matrices,census,domains,raw=physical.build()
    universe=frozenset(range(22));lows=frozenset(range(4))
    low_red=[frozenset(4+x for x in r) for r in low_rows]
    def endpoints(x,sx):
        r=frozenset(i for i in range(4) if types[x] & (1<<i)) | frozenset(
            4+y for y in range(18) if sx & (1<<y))
        b=universe-r-{4+x}
        sigma=[3-len(r&low_red[i]) if i in r else
               6-len(b&(universe-low_red[i]-{i})) for i in range(4)]
        B=2+2*len(r&lows)-sum(sigma);parity=sum(sigma[i] for i in r&lows)%2
        values=[v for v in range(B+1) if v%2==parity]
        return r,b,(max(values,default=-1),max((B-v for v in values),default=-1))
    found=None
    for x in range(18):
        for sx in domains.get((x,matrices[packet['template']][x]),[]):
            rx,bx,cx=endpoints(x,sx)
            for y in range(18):
                if y==x:continue
                for sy in domains.get((y,matrices[packet['template']][y]),[]):
                    ry,by,cy=endpoints(y,sy);edge=4+y in rx
                    if edge!=(4+x in ry):continue
                    common=rx&ry
                    if edge and any(common&low_red[i] for i in common&lows):continue
                    delta=(3-len(common)) if edge else (6-len(bx&by))
                    c=0 if edge else 1
                    if 0<=delta<=min(cx[c],cy[c]):
                        found=(x,sx,y,sy);break
                if found:break
            if found:break
        if found:break
    require(found is not None,'No positive physical pair support control')
    x,sx,y,sy=found
    false=copy.deepcopy(prefix);false['removals']=[dict(x=x,star=sx,y=y)]
    false['current_sizes'][x]-=1
    rejected('false-unsupported-pair',lambda p:None,base=false,
             expected='has a literal support')
    return dict(damages_detected=damages,positive_prefixes=2,positive_initial_empty=1,
                positive_physical_pair=list(found))


def run(packet,initial_packet):
    return dict(agent='six-books-3',role='researcher',status='COMPLETE_SEMANTIC_CONTROLS',
        certificate_controls=semantic(packet,initial_packet),
        count_planes=count_planes(),primary_baseline=primary_baseline())


if __name__=='__main__':
    import argparse
    p=argparse.ArgumentParser();p.add_argument('--packet',type=Path,required=True)
    p.add_argument('--initial-packet',type=Path,required=True);a=p.parse_args()
    print(json.dumps(run(json.loads(a.packet.read_text()),
                         json.loads(a.initial_packet.read_text())),sort_keys=True,separators=(',',':')))
