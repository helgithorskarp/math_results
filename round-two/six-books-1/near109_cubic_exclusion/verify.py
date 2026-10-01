"""Separate direct-star incidence generation and literal neighbor-mask replay."""
from itertools import combinations, combinations_with_replacement, product
from collections import defaultdict, Counter
from pathlib import Path
import json
import time
import hashlib

start=time.monotonic()
HERE=Path(__file__).resolve().parent
fixture=json.loads((HERE/'model.json').read_text())
# Build the rooted-six-cycle model, then check its supplied isomorphism.
model=[set() for _ in range(10)]
def edge(a,b):model[a].add(b);model[b].add(a)
for t in range(1,4):
    edge(0,t);edge(t,t+3);edge(t,t+6)
for t in range(4,10):edge(t,4+(t-3)%6)
mapping=fixture['leaf_full_isomorphism']
need=lambda ok,msg: None if ok else (_ for _ in ()).throw(ValueError(msg))
P=[set() for _ in range(10)]
for i in range(10):P[mapping[i]]={mapping[j] for j in model[i]}
need(P==[{j for j in range(10) if w>>j&1} for w in fixture['petersen']], 'Petersen model')
ground=list(combinations(range(5),2))
fourstars=[sum(1<<i for i,e in enumerate(ground) if a in e) for a in range(5)]
pairlist=list(combinations(range(10),2))
rp=[(i,j) for i,j in pairlist if j in P[i]]
psets={z:{i for i in range(10) if z>>i&1} for z in range(1024)}
redmask={z:sum(1<<t for t,(i,j) in enumerate(rp) if {i,j}<=psets[z]) for z in range(1024)}
isomask={z:sum(1<<i for i in range(10) if i not in psets[z] and P[i]<=psets[z]) for z in range(1024)}
vec={z:tuple(int(i in psets[z]) for i in range(10)) for z in range(1024)}
domains={}
for deficit in range(3):
    words=[]
    for csize in range(2,7-deficit):
        for chosen in combinations(range(10),csize):
            c=set(chosen);z=set(range(10))-c;k=len(z);d=k-deficit
            if k<4+deficit or k>8:continue
            if any(len(P[i]&c)>(1 if deficit==0 else 2) for i in c):continue
            # Literal A-pages plus smallest possible B-pages of a red A--b spine.
            if any(len(P[i]&c)+max(0,d-5)>3 for i in c):continue
            # Known A-pages of each blue A--b spine alone.
            if any(len(z-{i}-P[i])>6 for i in z):continue
            words.append(sum(1<<i for i in z))
    domains[deficit]=sorted(words)
# Generate all high-row multisets by deciding each next word, retaining
# exact ten-column sums. No quotient projection or solved mu equation.
large=sorted(z for z in domains[0] if z.bit_count()>=5)
high=defaultdict(list)
high_counts=Counter()
def high_visit(begin,words,columns,used,excess):
    high[(excess,len(words),columns)].append((tuple(words),used))
    high_counts[excess]+=1
    for pos in range(begin,len(large)):
        z=large[pos];next_excess=excess+z.bit_count()-4
        if next_excess>4 or used&redmask[z]:continue
        high_visit(pos,words+[z],tuple(columns[i]+vec[z][i] for i in range(10)),
                   used|redmask[z],next_excess)
high_visit(0,[],(0,)*10,0,0)
need([high_counts[i] for i in range(5)]==[1,30,425,3360,14980],'high recursion coverage')
mus=defaultdict(list)
for mu in product(range(3),repeat=5):
    cols=tuple(mu[i]+mu[j] for i,j in ground)
    mus[sum(mu)].append((mu,cols))

all_records={}
for mode,d,nlow in [('one8',2,1),('two9',1,2)]:
    records=set();low_count=0
    choices=((z,) for z in domains[d]) if nlow==1 else combinations_with_replacement(domains[d],2)
    for lows in choices:
        excess=6-sum(z.bit_count()-4 for z in lows)
        if not 0<=excess<=4:continue
        low_count+=1
        used=0
        for z in lows:
            if used&redmask[z]:break
            used|=redmask[z]
        else:
            lc=tuple(sum(vec[z][i] for z in lows) for i in range(10))
            clean=1023
            for z in lows:clean&=z
            for nhigh in range(5):
                for mu,mc in mus[11-nlow-nhigh]:
                    remaining=tuple(5-lc[i]-mc[i] for i in range(10))
                    if min(remaining)<0 or max(remaining)>nhigh:continue
                    for hi,hred in high.get((excess,nhigh,remaining),[]):
                        if used&hred or any(isomask[z]&clean for z in hi):continue
                        words=lows+hi+tuple(z for z,m in zip(fourstars,mu) for _ in range(m))
                        if any(sum(i in psets[z] and j in psets[z] for z in words)>
                               (1 if j in P[i] else 3) for i,j in pairlist):continue
                        key=(tuple(lows),tuple(sorted(hi)),tuple(mu))
                        need(key not in records,'duplicate normalized incidence')
                        records.add(key)
        if low_count%20000==0:
            print(json.dumps({'phase':'incidence','mode':mode,'low_count':low_count,
                              'records':len(records),'elapsed':time.monotonic()-start}),flush=True)
    all_records[mode]=records
    print(json.dumps({'phase':'incidence-complete','mode':mode,'records':len(records),
                      'elapsed':time.monotonic()-start}),flush=True)

def make_host(words,local=None):
    local=P if local is None else local
    g=[set() for _ in range(11+len(words))]
    for i in range(10):
        g[0].add(i+1);g[i+1].add(0)
        g[i+1].update(j+1 for j in local[i])
        for b,z in enumerate(words):
            if i not in psets[z]:g[i+1].add(b+11);g[b+11].add(i+1)
    known=[sum(1<<j for j in row) for row in g]
    return known


def domain(words,d,b,known):
    degree=words[b].bit_count()-d[b]
    bpoints=[j for j in range(len(words)) if j!=b]
    red_a=known[b+11]
    out=[]
    for blue_neighbors in combinations(bpoints,len(words)-1-degree):
        blue=set(blue_neighbors)
        neighbors=red_a+sum(1<<(j+11) for j in bpoints if j not in blue)
        blue_full=(2**len(known)-1)^neighbors^(1<<(b+11))
        for i in range(10):
            if i in psets[words[b]]:
                ai_blue=(2**len(known)-1)^known[i+1]^(1<<(i+1))
                if (ai_blue&blue_full).bit_count()>6:break
            elif (known[i+1]&neighbors).bit_count()>3:break
        else:out.append(neighbors)
    return out


def compatible(b,c,x,y,order=22):
    red=bool(x&(1<<(c+11)))
    if red!=bool(y&(1<<(b+11))):return False
    if red:return (x&y).bit_count()<=3
    bx=(2**order-1)^x^(1<<(b+11));by=(2**order-1)^y^(1<<(c+11))
    return (bx&by).bit_count()<=6


def visit(domains,unassigned,order=22):
    if not unassigned:return True,1
    b=max(unassigned,key=lambda i:(-len(domains[i]),i))
    nodes=1
    for x in domains[b]:
        next_domain={}
        for c in unassigned:
            if c==b:continue
            keep=[y for y in domains[c] if compatible(b,c,x,y,order)]
            if not keep:break
            next_domain[c]=keep
        else:
            valid,count=visit(next_domain,[c for c in unassigned if c!=b],order);nodes+=count
            if valid:return True,nodes
    return False,nodes




def digest(records):
    return hashlib.sha256(''.join(json.dumps(x,separators=(',',':'))+'\n' for x in sorted(records)).encode()).hexdigest()


def controls():
    from control_data import primary_problem,weighted_controls
    local,words,delta,actual,masks=primary_problem(HERE)
    local_sets=[{j for j in range(10) if x>>j&1} for x in local]
    known=make_host(words,local_sets)
    ds={b:domain(words,delta,b,known) for b in range(10)}
    need(all(masks[b+11] in ds[b] for b in range(10)), 'literal positive star acceptance')
    valid,_=visit({b:[masks[b+11]] for b in range(10)},list(range(10)),21)
    need(valid,'literal positive completion acceptance')
    damaged=0
    for b in range(10):
        for c in range(10):
            for d in range(10):
                if c==b or d==b or c==d or not actual[b]>>c&1 or actual[b]>>d&1:continue
                trial={i:[masks[i+11]] for i in range(10)}
                trial[b]=[masks[b+11]^((1<<(c+11))|(1<<(d+11)))]
                valid,_=visit(trial,list(range(10)),21)
                need(not valid,'damaged literal completion accepted');damaged+=1
    literal=0
    for record in weighted_controls():
        red=[{j for j in range(22) if x>>j&1} for x in record['neighbor_masks']]
        blue=[set(range(22))-{i}-red[i] for i in range(22)]
        local=[{j for j in range(10) if x>>j&1} for x in record['local']]
        miss=[{b for b,z in enumerate(record['miss_rows']) if z>>i&1} for i in range(10)]
        degree=[len(x) for x in red]
        need(all(len(miss[i])==len(local[i])+12-degree[i+1] for i in range(10)),'literal weighted column')
        for i,j in combinations(range(10),2):
            overlap=len(miss[i]&miss[j]);common_local=len(local[i]&local[j]);hs=len(local[i])+len(local[j])
            if j in local[i]:
                bound=3-(8-hs-(10-degree[i+1])-(10-degree[j+1])+common_local)
                capacity=3-len(red[i+1]&red[j+1])
            else:
                bound=6-(8-hs+common_local)
                capacity=6-len(blue[i+1]&blue[j+1])
            need(capacity==bound-overlap,'literal weighted capacity');literal+=1
    need(all(sum(range(t))>=t-1 for t in range(5)),'four packing')
    need(all(sum(range(t))>=2*t-3 for t in range(6)),'five packing')
    return {'positive21_star_domains':10,'positive21_completion':1,
            'damaged21_completions_rejected':damaged,'signed109_controls':4,
            'weighted_column_entries':40,'weighted_literal_pair_entries':literal}


def compute():
    result={'schema':1,'row_domains':{str(d):{'count':len(domains[d]),
        'by_size':dict(sorted(Counter(z.bit_count() for z in domains[d]).items()))} for d in range(3)},
        'red_capped_high_multisets':[high_counts[x] for x in range(5)],
        'controls':controls(),'cases':{}}
    for mode in ['one8','two9']:
        records=all_records[mode];nonempty=[];empty=nodes=solutions=0
        for key in sorted(records):
            words=list(key[0])+list(key[1])+[z for z,m in zip(fourstars,key[2]) for _ in range(m)]
            deficit=([2] if mode=='one8' else [1,1])+[0]*(11-len(key[0]))
            known=make_host(words);ds={};sizes=[]
            for b in range(11):
                ds[b]=domain(words,deficit,b,known)
                if not ds[b]:empty+=1;break
                sizes.append(len(ds[b]))
            else:
                nonempty.append((key,tuple(sizes)))
                valid,count=visit(ds,list(range(11)));nodes+=count;solutions+=valid
                need(not valid,'literal counterexample found; theorem fails')
        result['cases'][mode]={'incidence_records':len(records),'incidence_sha256':digest(records),
            'empty_star_cases':empty,'all_stars_nonempty':len(nonempty),
            'nonempty_domain_sizes_sha256':digest(nonempty),'completions':solutions}
        print(json.dumps({'phase':'literal-case-complete','mode':mode,'records':len(records),
                          'nonempty':len(nonempty),'search_nodes':nodes,
                          'elapsed':time.monotonic()-start}),flush=True)
    return json.loads(json.dumps(result))


def check_report(actual,cached):
    need(actual==cached,'expected record mismatch')
    need(all(x['completions']==0 for x in actual['cases'].values()),'nonzero completions')

if __name__=='__main__':
    import copy
    result=compute();expected=json.loads((HERE/'expected.json').read_text());check_report(result,expected)
    corruptions=[]
    for case,field in [('one8','incidence_records'),('two9','incidence_records'),
                       ('one8','completions'),('two9','all_stars_nonempty')]:
        bad=copy.deepcopy(expected);bad['cases'][case][field]+=1;corruptions.append(bad)
    bad=copy.deepcopy(expected);bad['cases']['two9']['incidence_sha256']='0'*64;corruptions.append(bad)
    bad=copy.deepcopy(expected);bad['cases']['two9']['nonempty_domain_sizes_sha256']='0'*64;corruptions.append(bad)
    rejected=0
    for bad in corruptions:
        try:check_report(result,bad)
        except ValueError:rejected+=1
        else:raise ValueError('damaged certificate accepted')
    need(rejected==6,'six damaged summaries')
    print(json.dumps({'status':'PASS','rejected_damaged_summaries':rejected,
                      'elapsed':time.monotonic()-start,'cases':result['cases']}),flush=True)
