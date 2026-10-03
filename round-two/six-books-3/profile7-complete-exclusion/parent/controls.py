"""Scope/deletion boundary controls, budget-three multiplicities and primary21."""
import collections
import copy
import hashlib
import itertools
import json
import argparse
from pathlib import Path

ROOT=Path(__file__).resolve().parent
SOURCE=ROOT
import check
import physical
from witness_kernel import accumulate

require=physical.require


def digest(value):
    return hashlib.sha256(json.dumps(value,sort_keys=True,separators=(',',':')).encode()).hexdigest()


def primary_baseline():
    raw=(SOURCE/'primary21.txt').read_bytes()
    require(hashlib.sha256(raw).hexdigest()==
        '3b648b66a5990d0b6ed945ce80d3f546e90f2b233f924775bb02ac2418558a55',
        'Primary21 fixture differs')
    A,_=json.JSONDecoder().raw_decode(raw.decode());n=len(A)
    require(n==21 and all(len(r)==n for r in A),'Primary order differs')
    require(all(type(A[i][j]) is int and A[i][j] in (0,1)
        and A[i][j]==A[j][i] and (i!=j or A[i][j]==0)
        for i in range(n) for j in range(n)),'Primary encoding differs')
    red=[{j for j in range(n) if j!=i and A[i][j]==0} for i in range(n)]
    blue=[{j for j in range(n) if j!=i and A[i][j]==1} for i in range(n)]
    pages=[[],[]];literal=[]
    for i in range(n):
        for j in range(i+1,n):
            cr=len(red[i]&red[j]);cb=len(blue[i]&blue[j]);edge=j in red[i]
            require(cb==n-2-len(red[i])-len(red[j])+cr+2*int(edge),
                    'Physical complement identity differs')
            value=cr if edge else cb
            require(value<=(3 if edge else 6),'Primary violates ordinary page cap')
            pages[0 if edge else 1].append(value);literal.append([i,j,int(edge),cr,cb])
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
        require(actual==expected,'Binary planes differ from scalar membership counts')
        complete.append(expected)
    for plane in (0,3):
        damaged=list(planes);damaged[plane]^=1
        actual=[sum(((p>>j)&1)*(1<<k) for k,p in enumerate(damaged)) for j in range(1<<9)]
        require(actual!=complete[-1],'Damaged count plane escaped')
    return dict(complete_membership_patterns=sum(map(len,complete)),maximum_inputs=9,
                whole_scalar_sha256=digest(complete),plane_damages_detected=2)


def semantic(packet):
    prefix=copy.deepcopy(packet);prefix['removals']=[];prefix['pending']=None
    prefix['current_sizes']=list(prefix['initial_sizes'])
    positive=check.verify(prefix)
    require(not positive['claim_template_excluded'] and positive['checked_stars']==0,
            'Valid no-action prefix differs')
    first=copy.deepcopy(prefix);first['removals']=[packet['removals'][0]]
    first['current_sizes'][first['removals'][0]['x']]-=1
    one=check.verify(first)
    require(one['checked_stars']==1 and not one['claim_template_excluded'],
            'Valid single-action prefix differs')
    damages=[];boundaries=[]

    expected_boundaries={
        'wrong-counts':'Wrong physical scope/matrix',
        'wrong-type':'Wrong physical scope/matrix',
        'wrong-column':'Wrong physical scope/matrix',
        'wrong-initial-size':'Wrong original domains',
        'fake-final-empty':'Final domains differ',
        'negative-case':'Certificate scope/claims differ',
        'case-outside-full-inventory':'Matrix number outside complete physical inventory',
        'boolean-case-number':'Certificate scope/claims differ',
        'unverified-exclusion-claim':'Certificate scope/claims differ',
        'wrong-color-rule':'Certificate scope/claims differ',
        'diagonal-star':'Malformed/repeated physical removal',
        'same-pair-endpoint':'Malformed/repeated physical removal',
        'repeated-removal':'Malformed/repeated physical removal',
        'action-after-empty':'Actions after final empty',
    }

    def rejected(name,mutate,base=prefix,expected=None):
        bad=copy.deepcopy(base);mutate(bad)
        try:check.verify(bad)
        except (ValueError,KeyError,TypeError,IndexError) as error:
            want=expected or expected_boundaries[name]
            require(want in str(error), 'Wrong semantic rejection boundary; operational failures are not damages')
            damages.append(name);boundaries.append(dict(case=name,actual_failure=str(error)))
        else:raise ValueError('Semantic damage accepted: '+name)

    rejected('wrong-counts',lambda p:p['profile_counts'].__setitem__(0,1))
    rejected('wrong-type',lambda p:p['types'].__setitem__(0,3))
    rejected('wrong-column',lambda p:p['columns'].__setitem__(0,1))
    rejected('wrong-initial-size',lambda p:p['initial_sizes'].__setitem__(0,0))
    rejected('fake-final-empty',lambda p:p['current_sizes'].__setitem__(0,0))
    rejected('negative-case',lambda p:p.__setitem__('template',-1))
    rejected('case-outside-full-inventory',lambda p:p.__setitem__('template',32))
    rejected('boolean-case-number',lambda p:p.__setitem__('template',True))
    rejected('unverified-exclusion-claim',lambda p:p.__setitem__('claim_template_excluded',True))
    rejected('wrong-color-rule',lambda p:p.__setitem__('rule','UNCOLORED'))
    rejected('diagonal-star',lambda p:p['removals'][0].__setitem__('star',
        p['removals'][0]['star'] | (1<<p['removals'][0]['x'])),base=first)
    rejected('same-pair-endpoint',lambda p:p['removals'][0].__setitem__('y',
        p['removals'][0]['x']),base=first)
    rejected('repeated-removal',lambda p:p['removals'].append(copy.deepcopy(p['removals'][0])),base=first)
    rejected('action-after-empty',lambda p:p['removals'].append(copy.deepcopy(p['removals'][-1])),base=packet)

    counts,types,low_rows,budget,matrices,census,domains,raw=physical.build()
    universe=frozenset(range(22));lows=frozenset(range(4))
    low_red=[frozenset(4+x for x in r) for r in low_rows]

    def endpoint(x,sx):
        red=frozenset(i for i in range(4) if types[x] & (1<<i)) | frozenset(
            4+y for y in range(18) if sx & (1<<y))
        blue=universe-red-{4+x}
        sigma=[3-len(red&low_red[i]) if i in red else
               6-len(blue&(universe-low_red[i]-{i})) for i in range(4)]
        B=2+2*len(red&lows)-sum(sigma);p=sum(sigma[i] for i in red&lows)%2
        scalar=[v for v in range(B+1) if v%2==p]
        return red,blue,(max(scalar,default=-1),max((B-v for v in scalar),default=-1))

    found=None
    for x in range(18):
        for sx in domains.get((x,matrices[packet['template']][x]),[]):
            rx,bx,cx=endpoint(x,sx)
            for y in range(18):
                if y==x:continue
                for sy in domains.get((y,matrices[packet['template']][y]),[]):
                    ry,by,cy=endpoint(y,sy);edge=4+y in rx
                    if edge!=(4+x in ry):continue
                    common=rx&ry
                    if edge and any(common&low_red[i] for i in common&lows):continue
                    delta=(3-len(common)) if edge else (6-len(bx&by))
                    color=0 if edge else 1
                    if 0<=delta<=min(cx[color],cy[color]):found=(x,sx,y,sy);break
                if found:break
            if found:break
        if found:break
    require(found is not None,'No positive physical pair')
    x,sx,y,sy=found
    false=copy.deepcopy(prefix);false['removals']=[dict(x=x,star=sx,y=y)]
    false['current_sizes'][x]-=1
    rejected('false-unsupported-pair',lambda p:None,base=false,expected='has a literal support')
    return dict(damages_detected=damages,actual_semantic_boundaries=boundaries,positive_nonempty_prefixes=2,
                positive_physical_pair=list(found),producer_status_is_not_a_verdict=True)


def budget_three():
    counts,types,red,budget,matrices,census,domains,raw=physical.build()
    red_three=list(itertools.combinations_with_replacement(red[0],3))
    repeated=collections.Counter(tuple(sorted(collections.Counter(v).values())) for v in red_three)
    require(len(red_three)==165 and repeated=={(1,1,1):84,(1,2):72,(3,):9},
            'Budget-three red multiplicities differ')
    blue=[x for x in range(18) if x not in red[0]]
    blue_two=list(itertools.combinations_with_replacement(blue,2))
    require(len(blue_two)==45 and sum(a==b for a,b in blue_two)==9,
            'Budget-three coincident blue units missing')
    red_subtotals=collections.Counter(sum((c&3) for t,c in zip(types,m) if t&1) for m in matrices)
    require(red_subtotals=={1:18,3:14},'Complete canonical red1/red3 branches differ')
    return dict(red3_multisets=165,red3_all_distinct=84,red3_two_equal=72,
        red3_all_equal=9,red1_blue2=405,red1_blue2_coincident=81,
        physical_row0_options=570,canonical_red_subtotal_counts=dict(red_subtotals),
        initial_empty_cases=[t for t,m in enumerate(matrices)
            if any(not domains.get((x,m[x]),[]) for x in range(18))])


if __name__=='__main__':
    parser=argparse.ArgumentParser();parser.add_argument('--packet',type=Path,required=True)
    args=parser.parse_args();packet=json.loads(args.packet.read_text())
    result=dict(agent='six-books-3',role='researcher',status='PROFILE7_CONTROLS_COMPLETED',
        certificate_controls=semantic(packet),budget_three_controls=budget_three(),
        count_planes=count_planes(),primary_baseline=primary_baseline())
    print(json.dumps(result,sort_keys=True,separators=(',',':')))
