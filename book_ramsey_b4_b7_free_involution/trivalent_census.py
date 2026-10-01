"""Regular free Book quotients need a trivalent red vertex.
Actual author six-books-2, researcher. Exact standard-library census.
Degree-star residual helper adapted from own source05653f3/twenty_census.py.
TRIVALENT.md gives finite coverage and the separate analytic cases.
"""
import argparse
from collections import Counter
from hashlib import sha256
from itertools import combinations, product
import json
from pathlib import Path

PAIRS = tuple(combinations(range(11), 2))
INDEX = {e: i for i, e in enumerate(PAIRS)}

def require(condition, message):
    if not condition: raise RuntimeError(message)

def neighbors(edges):
    rows = [set() for _ in range(11)]
    for i, j in edges:
        rows[i].add(j); rows[j].add(i)
    return rows

def mask(edges):
    return sum(1 << INDEX[e] for e in edges)

def failure(red, blue):
    nr, nd = neighbors(red), neighbors(blue)
    def square(i,j):
        return len(nr[i]&nr[j])+len(nd[i]&nd[j])-len(nr[i]&nd[j])-len(nd[i]&nr[j])
    for edges,label,base,cap in [(sorted(red),'R',7,6),(sorted(blue),'D',11,12),
        ([e for e in PAIRS if e not in red|blue],'M',9,9)]:
        for i,j in edges:
            pages=base+square(i,j)
            if pages>cap:return [label,i,j,pages]
    return None

def completions(fixed, forbidden):
    degree=[2-sum(i in e for e in fixed) for i in range(11)]
    if any(v<0 for v in degree):return
    free=set(PAIRS)-forbidden-fixed
    def visit(i,remaining,edges):
        while i<11 and remaining[i]==0:i+=1
        if i==11:
            yield frozenset(fixed|edges);return
        choices=[j for j in range(i+1,11) if remaining[j]>0 and (i,j) in free]
        for selected in combinations(choices,remaining[i]):
            after=remaining[:];after[i]=0
            for j in selected:after[j]-=1
            if all(after[j]<=sum(after[k]>0 and (min(j,k),max(j,k)) in free
                for k in range(i+1,11) if k!=j) for j in range(i+1,11)):
                yield from visit(i+1,after,edges|{(i,j) for j in selected})
    yield from visit(0,degree,set())

def cycle_graph(sizes):
    red,first=set(),0
    for size in sizes:
        red.update(tuple(sorted((first+i,first+(i+1)%size))) for i in range(size))
        first+=size
    return red

def controls():
    R={(i,i+1) for i in range(10)}
    A={(0,2),(1,3),(1,4),(2,4),(3,5),(5,7),(6,8),(6,9),(7,9),(8,10)}
    B={(0,2),(1,3),(1,6),(2,6),(3,5),(4,8),(4,9),(5,7),(7,9),(8,10)}
    require(failure(R,A)==['M',3,7,10] and failure(R,B)==['M',2,4,10], 'P11 analytic table decoding')
    R6={(i,i+1) for i in range(5)}|{tuple(sorted((6+i,6+(i+1)%5))) for i in range(5)}
    D6={(0,2),(1,3),(1,4),(2,4),(3,5)}|{e for e in combinations(range(6,11),2) if e not in R6}
    require(failure(R6,D6) is None, 'P6+C5 must survive summed unsigned caps; known sign parity is needed')
    signs=tuple(product([-1,1],repeat=6));pairs=0
    for x in signs:
        for y in signs:
            if sum(a*b for a,b in zip(x,y))==0:
                require(__import__('math').prod(x)==-__import__('math').prod(y),'six-sign orthogonality parity')
                pairs+=1
    require(not any(all(word[i]!=word[(i+1)%5] for i in range(5)) for word in product([0,1],repeat=5)), 'odd cycle parity')
    return {'P11_control_quotients':2,'P6_C5_unsigned_positive_control':True,'six_sign_orthogonal_ordered_pairs':pairs,'odd_cycle_binary_words':32,'controls_are_validation_not_census_premises':True}

def run(records_path=None):
    rows=[];profiles=[]
    R8=cycle_graph([8])|{(8,9),(9,10)}
    core=tuple(e for e in combinations(range(8),2) if e not in R8)
    incident=[sum(1<<k for k,e in enumerate(core) if i in e) for i in range(8)]
    groups={k:[] for k in range(1,5)};raw=0
    for subset in combinations(range(len(core)),7):
        raw+=1;word=sum(1<<i for i in subset)
        degrees=[(word&v).bit_count() for v in incident]
        leaves=[i for i in range(8) if degrees[i]==1]
        if degrees[0]==1 and len(leaves)==2 and all(v in [1,2] for v in degrees) and leaves[1] in groups:
            groups[leaves[1]].append(word)
    require(raw==77520,'C8 raw subset coverage')
    for k,words in groups.items():
        counts=Counter();seen=set()
        for word in words:
            D={e for i,e in enumerate(core) if (word>>i)&1}|{(8,10),(0,9),(k,9)}
            code=mask(D);fail=failure(R8,D)
            require(code not in seen and len(D)==10 and [len(r) for r in neighbors(D)]==[len(r) for r in neighbors(R8)],'C8 degree/duplicate guard')
            require(fail is not None,'C8 necessary survivor; theorem incomplete')
            seen.add(code);counts[fail[0]]+=1;rows.append(['C8:'+str(k),code,fail])
        profiles.append({'case':'C8:'+str(k),'D_completions':len(seen),'first_failure_counts':dict(counts)})
    for sizes,label in [([11],'C11'),([5,6],'C5+C6')]:
        red=cycle_graph(sizes);nr=neighbors(red)
        chords=tuple(sorted(tuple(sorted(v)) for v in nr))
        require(len(set(chords))==11 and not set(chords)&red,'distance-two indexing')
        chord_index={e:i for i,e in enumerate(chords)};covers=[]
        for i,j in sorted(red):
            a=next(iter(nr[i]-{j}));b=next(iter(nr[j]-{i}))
            covers.append((chord_index[tuple(sorted((a,j)))],chord_index[tuple(sorted((i,b)))]))
        patterns=0;seen=set();counts=Counter()
        for word in range(2048):
            if not all((word>>a)&1 or (word>>b)&1 for a,b in covers):continue
            patterns+=1
            fixed={e for i,e in enumerate(chords) if (word>>i)&1}
            forbidden=red|{e for i,e in enumerate(chords) if not (word>>i)&1}
            for D in completions(fixed,forbidden):
                code=mask(D);fail=failure(red,D)
                require(code not in seen and len(D)==11 and all(len(r)==2 for r in neighbors(D)),'cycle degree/duplicate guard')
                require(fail is not None,'cycle necessary survivor; theorem incomplete')
                seen.add(code);counts[fail[0]]+=1;rows.append([label,code,fail])
        profiles.append({'case':label,'raw_chord_words':2048,'edge_cover_words':patterns,'D_completions':len(seen),'first_failure_counts':dict(counts)})
    rows.sort(key=lambda r:(r[0],r[1]));encoded=''.join(json.dumps(r,separators=(',',':'))+'\n' for r in rows)
    if records_path:records_path.write_text(encoded)
    return {'agent':'six-books-2','role':'researcher','complete':True,'raw_C8_core_subsets':raw,'profiles':profiles,'total_D_completions':len(rows),'survivors':0,'canonical_records_sha256':sha256(encoded.encode()).hexdigest(),'analytic_controls':controls(),'threads':1,'local_jobs':1,'new_finite_census_is_a_theorem_premise':True}

def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--records',type=Path);parser.add_argument('--emit',action='store_true')
    parser.add_argument('--expected',type=Path,default=Path(__file__).with_name('trivalent_expected.json'))
    args=parser.parse_args();result=run(args.records)
    if not args.emit:require(result==json.loads(args.expected.read_text())['census'],'census fixture mismatch')
    print(json.dumps(result,indent=2,sort_keys=True))
if __name__=='__main__':main()
