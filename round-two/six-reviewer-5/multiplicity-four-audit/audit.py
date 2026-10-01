"""six-reviewer-5: independent multiplicity-four audit (standard library).

Previously reviewed 46 nineteen-star representatives and generic 23 twenty-star
fixtures are explicit mathematical premises. No author program executes.
Decode the former by literal cells; inspect all raw marks and signed LP rows.
Aggregate each dual by subset, then evaluate every column on its 25 subsets.
"""
import argparse
from collections import Counter
import copy
import hashlib
from itertools import combinations, permutations
import json
from pathlib import Path
import resource
import time
import iso_pairs
from local_pair import require, two_charge_control

HERE=Path(__file__).resolve().parent
NINETEEN_SHA='83adc2817c988fa4450ede02c7da09b4da857e3f1850a0b0d0dee4cfd4a24bca'

def encoded(x):
    return (json.dumps(x,sort_keys=True,separators=(',',':'))+'\n').encode()

def digest(x):
    return hashlib.sha256(encoded(x)).hexdigest()

def carriers(data):
    """Literal decoder extends this reviewer's earlier sharp-67 decoder."""
    records=[]; representatives=[]
    for mi,model in enumerate(data['models']):
        lengths=model['cycle_half_lengths'];require(lengths in ([5],[2,3]),'anchor form')
        absent=set();offset=0
        for n in lengths:
            for i in range(n):
                absent.update(((offset+i,offset+i),(offset+i,offset+(i+1)%n)))
            offset+=n
        cells=[(r,c) for r in range(5) for c in range(5) if (r,c) not in absent]
        label={p:i for i,p in enumerate(cells)}
        require(len(cells)==15,'fifteen cells')
        anchors=[frozenset([15]+[i for i,(r,c) in enumerate(cells) if r==x]) for x in range(5)]
        anchors += [frozenset([16]+[i for i,(r,c) in enumerate(cells) if c==x]) for x in range(5)]
        literal=[q for q in combinations(range(15),4) if len({cells[i][0] for i in q})==len({cells[i][1] for i in q})==4]
        injections=set()
        for rr in combinations(range(5),4):
            for cc in permutations(range(5),4):
                if all(p in label for p in zip(rr,cc)):
                    injections.add(tuple(sorted(label[p] for p in zip(rr,cc))))
        require(literal==sorted(injections) and len(literal)==model['candidate_count'],'two independent candidate decoders')
        for ci,entry in enumerate(model['marked_classes']):
            ids=entry['clique'];require(len(ids)==len(set(ids))==9,'nine private blocks')
            require(all(type(i) is int and 0<=i<len(literal) for i in ids),'private index domain')
            blocks=tuple(sorted(anchors+[frozenset(literal[i]) for i in ids],key=lambda s:tuple(sorted(s))))
            require(len(blocks)==len(set(blocks))==19 and all(len(w)==4 for w in blocks),'nineteen blocks')
            require(all(len(w&z)<=1 for w,z in combinations(blocks,2)),'nineteen pair packing')
            rho=[sum(x in w for w in blocks) for x in range(17)]
            require(sum(rho)==76 and max(rho)<=5,'replication')
            low={x for x in range(17) if rho[x]==5};high=set(range(17))-low
            leave={frozenset(p) for p in combinations(range(17),2) if not any(set(p)<=w for w in blocks)}
            ll=sorted(sorted(e) for e in leave if e<=low)
            require(len(leave)==22 and len(ll) in (1,2) and len(ll)==entry['low_low_pairs'],'marked low-low census')
            require(len({x for e in ll for x in e})==2*len(ll),'disjoint low-low edges')
            representatives.append([mi,ci])
            for u in range(17):
                if rho[u]!=4:continue
                C=set().union(*(w-{u} for w in blocks if u in w)); W=high-{u}
                require(len(C)==12,'covered hub neighborhood')
                friends={y:sorted(x for x in C&low if frozenset((x,y)) in leave) for y in W}
                friends={y:xs for y,xs in friends.items() if xs}
                require(all(x in C for e in ll for x in e),'all low-low endpoints covered')
                records.append(dict(id=(mi,ci,u),blocks=blocks,rho=rho,low=low,leave=leave,ll=ll,
                    C=C,W=W,WC=C&W,q={y:len(xs) for y,xs in friends.items()},friends=friends,
                    heavy={y for y in W if rho[y]<4},mu=len(ll),p=len(W),k=len(C&W)))
    require(len(representatives)==46 and len(records)==388,'all representatives and raw replication-four marks')
    return records

def screen(records):
    tested=0;coarse=[];author_local=[];strong=[];positive_excess=0
    for r in records:
        wc=sorted(r['WC'])
        for size in range(len(wc)+1):
            for tc in combinations(wc,size):
                c=len(tc)
                for z in range(5):
                    for X in range(3):
                        if 2*X+z+c>4:continue
                        tested+=1;R=4-z+c-2*X
                        Q=sum(max(r['q'].get(y,0),2 if y in tc else 0) for y in r['W'])
                        if Q>R:continue
                        if X>0:positive_excess+=1
                        if X==0 and Q+max(0,r['mu']-z)>R:continue
                        row=[*r['id'],X,list(tc),z,Q,R];coarse.append(row)
                        if not any(r['q'].get(y,0)>=2 and y not in r['heavy'] for y in tc):author_local.append(row)
                        # The standalone earlier local theorem gives e_u>=2 at
                        # each unit-v covered T center with a good forced friend.
                        # After the coarse exhaustion all these friends are good.
                        improved=sum((r['q'].get(y,0)+2) if y in tc and r['q'].get(y,0)>0 and y not in r['heavy']
                                     else max(r['q'].get(y,0),2 if y in tc else 0) for y in r['W'])
                        if improved+max(0,r['mu']-z)<=R:strong.append(row)
    for rows in (coarse,author_local,strong):rows.sort(key=encoded)
    require(positive_excess==0,'all positive-excess positive-mu cases excluded')
    require(len(coarse)==62 and len(author_local)==40 and len(strong)==6,'inventory stream counts')
    require(all(s[3]==0 and s[5] in (0,1) and s[7]-s[6]==1-s[5] for s in coarse),'exact one-exception budget')
    require(all(s[4]==[] for s in strong),'strong screen forces covered T empty')
    ids={tuple(s[:3]) for s in strong}
    require(ids=={(0,17,14),(0,19,1),(1,11,7)},'all surviving raw carrier marks')
    lookup={r['id']:r for r in records}
    for s in coarse:
        r=lookup[tuple(s[:3])]
        require(r['mu']==1,'coarse scope for local strengthening')
        endpoints=set().union(*(set(e) for e in r['ll']))
        require(all(not endpoints&set(xs) for xs in r['friends'].values()),'every forced friend avoids exceptions')
    for key in ids:
        r=lookup[key]
        require(r['ll']==[[15,16]] and sorted(r['q'].values())==[1,1,1],'residual structural data')
    return dict(tested_inventories=tested,coarse=coarse,author_after_shared_hub=author_local,strong=strong,positive_excess=positive_excess)

def candidates(r):
    # Inspect the whole 18-point domain before removing v; no row-filtering.
    words=[];tested=0
    for w in combinations(range(18),5):
        tested+=1
        if 17 in w:continue
        block=frozenset(w)
        if all(len(block&q)<=2 for q in r['blocks']):words.append(block)
    require(tested==8568 and len(words)==1219,'complete extra-word universe')
    return words

def row(descriptor,r,e):
    """Reconstruct one necessary A x <= b row from literal fixed blocks."""
    require(type(descriptor) is list and descriptor,'descriptor')
    tag=descriptor[0]
    arities={'point':1,'triple':3,'pair':3,'good-coverage':2,'forced-leave-upper':2,
        'u-good-upper':2,'u-good-lower':2,'u-good-b-lower':2,'u-exception-lower':2,
        'u-covered-t-lower':2,'u-outside-t-lower':2}
    require(tag in arities and len(descriptor)==arities[tag]+1,'tag and arity')
    points=descriptor[1:3] if tag=='pair' else descriptor[1:]
    require(all(type(x) is int and 0<=x<17 for x in points) and points==sorted(set(points)),'literal row points')
    s=frozenset(points);fixed=sum(s<=w for w in r['blocks']);u=r['id'][2]
    L=r['low']-{e};K=r['WC']-set(r['q'])
    if tag=='point':return (16 if points[0]==u else 20)-r['rho'][points[0]],[(s,1)]
    if tag=='triple':
        require(fixed==0,'triple already fixed');return 1,[(s,1)]
    if tag in ('pair','forced-leave-upper','good-coverage'):
        require(u not in s,'internal pair includes hub')
        if tag=='pair':
            lo=5 if s<=L or s<=K else 4
            require(type(descriptor[3]) is int and descriptor[3]==lo,'pair lower')
            return fixed-lo,[(s,-1)]
        if tag=='forced-leave-upper':
            require(fixed==0 and bool(s&r['low']),'unforced leave row');return 4,[(s,1)]
        require(bool(s&L),'coverage endpoint not good')
        t=s|{u};return fixed+sum(t<=w for w in r['blocks'])-5,[(s,-1),(t,-1)]
    require(u in s and len(s)==2,'hub pair')
    x=next(iter(s-{u}))
    if tag=='u-good-upper':
        require(x in L,'upper point not good A');return 4-fixed,[(s,1)]
    domains={'u-good-lower':L,'u-good-b-lower':K,'u-exception-lower':{e},
             'u-covered-t-lower':r['WC']-K,'u-outside-t-lower':r['W']-r['C']}
    require(x in domains[tag],'incorrect lower-row domain')
    lower={'u-good-lower':3,'u-good-b-lower':5,'u-exception-lower':2,
           'u-covered-t-lower':3,'u-outside-t-lower':2 if r['q'].get(x,0) else 4}[tag]
    return fixed-lower,[(s,-1)]

def duals(data,records,inventories):
    require(type(data) is dict and set(data)=={'format','cases'} and data['format']=='M4_INTEGER_DUAL_V1','dual format')
    require(type(data['cases']) is list,'dual list')
    ids={tuple(s[:3]) for s in inventories['strong']};lookup={r['id']:r for r in records}
    expected={(*key,e) for key in ids for pair in lookup[key]['ll'] for e in pair}
    require(len(expected)==6,'both choices of exception covered')
    seen=set();out=[]
    for cert in data['cases']:
        require(type(cert) is dict and set(cert)=={'model','class','u','exception','scale','weights'},'dual fields')
        key=tuple(cert[k] for k in ('model','class','u','exception'))
        require(all(type(x) is int for x in key) and key in expected and key not in seen,'dual case coverage')
        seen.add(key);r=lookup[key[:3]];D=cert['scale']
        require(type(D) is int and D>0,'positive exact scale')
        require(type(cert['weights']) is list and bool(cert['weights']),'weights')
        coefficients=Counter();rhs=0;seen_rows=set()
        for entry in cert['weights']:
            require(type(entry) is list and len(entry)==2,'weighted row')
            label,weight=entry;require(type(weight) is int and weight>0,'positive integer weight')
            key_label=encoded(label);require(key_label not in seen_rows,'repeated weighted row');seen_rows.add(key_label)
            b,terms=row(label,r,key[3]);rhs+=weight*b
            for subset,sign in terms:coefficients[subset]+=weight*sign
        columns=[];words=candidates(r)
        for w in words:
            columns.append(sum(coefficients[frozenset(s)] for n in (1,2,3) for s in combinations(sorted(w),n)))
        require(min(columns)>=D,'dual misses an actual candidate column')
        require(rhs<52*D,'no strict exclusion of 52 extra words')
        out.append(dict(case=list(key),candidate_count=len(words),weighted_rows=len(seen_rows),min_column=min(columns),
             integer_bound=rhs,scale=D,column_sha256=digest(columns),candidate_sha256=digest([sorted(w) for w in words])))
    require(seen==expected,'missing exception/carrier')
    return sorted(out,key=lambda x:x['case'])

def arithmetic():
    excess=[]
    for p in range(9):
        for k in range(p+1):
            if 6+k>p*(p-1)//2 or 5*p+k>21+p*(p-1)//2:continue
            for X in (1,2):
                for c in range(k+1):
                    for z in range(5):
                        if 2*X+c+z>4:continue
                        R=4-z+c-2*X
                        if max(12-k,2*c)<=R:excess.append([p,k,X,c,z])
    require(excess==[[8,8,1,2,0]],'all positive-excess inventories')
    unaffected=0
    for edge in combinations(range(16),2):
        if edge==(0,1):continue
        require(any(t not in edge and any(a not in edge for a in friends) for t,friends in [(0,(2,3)),(1,(4,5))]),'missing unaffected pair')
        unaffected+=1
    require(unaffected==119,'all 120 heavy-edge positions')
    equality=[]
    for p in range(9):
        for k in range(p+1):
            for c in range(k+1):
                for z in range(5):
                    R=4-z+c
                    if c+z>4 or 12-k>R or k<2*p+c-8:continue
                    require(z==0 and k==p and p+c==8,'two inequalities force equality')
                    equality.append([p,k,c,z])
    require(equality==[[4,4,4,0],[5,5,3,0],[6,6,2,0],[7,7,1,0],[8,8,0,0]],'large-domain equality family')
    require(1+1+2+1+1==6 and 6>5,'heavy T/T placement exceeds saturated row sum')
    return dict(positive_excess=excess,unaffected_heavy_positions=unaffected,row_sum_contradiction_positions=1,equality_family=equality)

def damage_controls(data,records,inv):
    names=[]
    def reject(name,bad):
        try:duals(bad,records,inv)
        except (ValueError,KeyError,TypeError,IndexError):names.append(name)
        else:raise ValueError('damaged dual accepted: '+name)
    mutations=[('negative weight',lambda c:c['weights'][0].__setitem__(1,-1)),
       ('zero scale',lambda c:c.__setitem__('scale',0)),
       ('unknown descriptor',lambda c:c['weights'][0][0].__setitem__(0,'invalid')),
       ('wrong exception',lambda c:c.__setitem__('exception',0)),
       ('empty weights',lambda c:c.__setitem__('weights',[])),
       ('uncovered columns',lambda c:c.__setitem__('scale',10**12)),
       ('noninteger weight',lambda c:c['weights'][0].__setitem__(1,0.5)),
       ('outside coordinate',lambda c:c['weights'][0][0].__setitem__(1,18)),
       ('duplicate row',lambda c:c['weights'].append(copy.deepcopy(c['weights'][0])))]
    for name,change in mutations:
        bad=copy.deepcopy(data);change(bad['cases'][0]);reject(name,bad)
    bad=copy.deepcopy(data);bad['cases'].pop();reject('missing carrier',bad)
    bad=copy.deepcopy(data);bad['cases'].append(copy.deepcopy(bad['cases'][0]));reject('duplicate carrier',bad)
    bad=copy.deepcopy(data)
    bad['cases'][0]['scale']=5
    bad['cases'][0]['weights']=[[['point',x],1] for x in range(17)]
    reject('column-covering bound exactly 52',bad)
    bad=copy.deepcopy(data)
    pair=next(x for x in bad['cases'][0]['weights'] if x[0][0]=='pair')
    pair[0][3]+=1;reject('incorrect pair lower',bad)
    # Weak duality deliberately allows negative row coefficients/RHS; only
    # nonnegative multipliers and strictly complete column domination prove it.
    return names

def main():
    parser=argparse.ArgumentParser();parser.add_argument('--write-expected',action='store_true');parser.add_argument('--out',type=Path)
    args=parser.parse_args();start=time.monotonic()
    raw=(HERE/'NINETEEN_STARS.json').read_bytes();require(hashlib.sha256(raw).hexdigest()==NINETEEN_SHA,'census hash')
    records=carriers(json.loads(raw));inv=screen(records);cert=json.loads((HERE/'INTEGER_DUALS.json').read_text())
    results=duals(cert,records,inv);controls=damage_controls(cert,records,inv)
    pairs=iso_pairs.audit();buckets=Counter((r['mu'],r['p'],r['k'],sum(r['q'].values())) for r in records)
    exact=dict(agent='six-reviewer-5',role='independent mathematical reviewer',nineteen_sha256=NINETEEN_SHA,
        marked_readout_sha256=digest([dict(id=list(r['id']),C=sorted(r['C']),W=sorted(r['W']),low=sorted(r['low']),
        q=sorted(r['q'].items()),ll=r['ll']) for r in records]),
        representatives=46,raw_marks=len(records),buckets=[[list(key),n] for key,n in sorted(buckets.items())],
        inventory=inv,duals=results,malformed_duals=controls,isolated_pairs=pairs,
        covered_two_hub_costs=two_charge_control(),arithmetic=arithmetic())
    expected=HERE/'EXPECTED.json'
    if args.write_expected:expected.write_bytes(encoded(exact))
    else:require(exact==json.loads(expected.read_text()),'exact audit stream changed')
    require(time.monotonic()-start<60,'INCOMPLETE whole audit exceeded fixed 60-second guard')
    result=dict(status='COMPLETE',exact_sha256=digest(exact),raw_marks=len(records),duals=len(results),isolated_cases=len(pairs['cases']),
        full_isolated_maps=sum(r['full_maps'] for r in pairs['cases']),isolated_nodes=sum(r['nodes'] for r in pairs['cases']),
        max_isolated_case_nodes=max(r['nodes'] for r in pairs['cases']),seconds=time.monotonic()-start,
        peak_RSS_KiB=resource.getrusage(resource.RUSAGE_SELF).ru_maxrss)
    if args.out:args.out.write_bytes(encoded(result))
    print(json.dumps(result,sort_keys=True))

if __name__=='__main__':main()
