"""Complete one-trivalent regular free Book quotient census.
Actual author six-books-2, researcher. Standard-library exact integers.
Whole-star helper adapted from own source485cb22/trivalent_census.py.
TWO_TRIVALENT.md supplies the ordinary finite reduction and trust boundary.
"""
import argparse
from collections import Counter
from itertools import combinations
from hashlib import sha256
from pathlib import Path
import json

PAIRS=tuple(combinations(range(11),2))
INDEX={e:k for k,e in enumerate(PAIRS)}
def require(condition,message):
    if not condition:raise RuntimeError(message)

def edge(a, b): return tuple(sorted((a, b)))

def mask(edges): return sum(1 << INDEX[e] for e in edges)

def rows(edges):
    nr = [set() for _ in range(11)]
    for i, j in edges: nr[i].add(j); nr[j].add(i)
    return nr

def complete(wanted, allowed, clauses, fixed, stats):
    remaining = [wanted[i] - sum(i in e for e in fixed) for i in range(11)]
    if min(remaining) < 0 or any(not c for c in clauses): return
    free = allowed-fixed
    def visit(i, need, chosen):
        stats['nodes'] += 1
        while i < 11 and need[i] == 0: i += 1
        if i == 11:
            if all(c & chosen for c in clauses): yield chosen
            return
        candidates = [j for j in range(i+1, 11) if need[j] and (i,j) in free]
        for selected in combinations(candidates, need[i]):
            after = need[:]; after[i] = 0
            for j in selected: after[j] -= 1
            if any(after[j] < 0 for j in range(i+1, 11)): continue
            future = {e for e in free if e[0] > i and after[e[0]] and after[e[1]]}
            if any(after[j] > sum(j in e for e in future) for j in range(i+1, 11)): continue
            new = chosen | {(i,j) for j in selected}
            if any(not(c & new) and not(c & future) for c in clauses): continue
            yield from visit(i+1, after, new)
    yield from visit(0, remaining, fixed)

def failure(red,blue,inside):
    nr,nd=rows(red),rows(blue)
    def square(i,j):return len(nr[i]&nr[j])+len(nd[i]&nd[j])-len(nr[i]&nd[j])-len(nd[i]&nr[j])
    for edges,label,base,cap in [(sorted(red),'R',7,6),(sorted(blue),'D',11,12),([e for e in PAIRS if e not in red|blue],'M',9,9)]:
        for i,j in edges:
            flags=((inside>>i)&1)+((inside>>j)&1)
            pages=base+square(i,j)+(flags if label=='R' else -flags if label=='D' else 0)
            if pages>cap:return [label,i,j,pages]
    return None

def domain(red,inside):
    nr=rows(red);degree=[len(nr[i])+((inside>>i)&1) for i in range(11)]
    allowed=set(PAIRS)-red;fixed=set()
    for i in range(11):
        siblings=sorted(j for j in nr[i] if len(nr[j])==1)
        fixed.update(__import__('itertools').combinations(siblings,2))
        if len(nr[i])==1:
            parent=next(iter(nr[i]));targets=nr[parent]-{i}
            allowed-={e for e in allowed if i in e and next(v for v in e if v!=i) not in targets}
    for i in range(11):
        incident={e for e in allowed if i in e}
        if len(incident)==degree[i]:fixed|=incident
    if not fixed<=allowed:raise RuntimeError('forced incompatible')
    clauses=[({edge(k,j) for k in nr[i]-{j}}|{edge(i,k) for k in nr[j]-{i}})&allowed for i,j in sorted(red)]
    return degree,allowed,clauses,fixed

def cycle_parts(total,minimum=5):
    if total==0:yield ();return
    for size in range(minimum,total+1):
        for rest in cycle_parts(total-size,size):yield (size,)+rest

def ygraph(arms,cycles):
    red=set();v=1
    for length in arms:
        previous=0
        for _ in range(length):red.add(edge(previous,v));previous=v;v+=1
    for k in cycles:
        red.update(edge(v+j,v+(j+1)%k) for j in range(k));v+=k
    if v!=11:raise RuntimeError('Y order')
    return red

def lgraph(k,t,path,cycles):
    red={edge(j,(j+1)%k) for j in range(k)};v=k;previous=0
    for _ in range(t):red.add(edge(previous,v));previous=v;v+=1
    if path:
        red.update((v+j,v+j+1) for j in range(path-1));v+=path
    for s in cycles:red.update(edge(v+j,v+(j+1)%s) for j in range(s));v+=s
    if v!=11:raise RuntimeError('L order')
    return red

def red_forms():
    for a in range(1,11):
        for b in range(a,11):
            for c in range(b,11):
                rest=10-a-b-c
                if rest<0:continue
                for cycles in cycle_parts(rest):
                    yield f'Y:{a},{b},{c}'+('+'+','.join('C'+str(x) for x in cycles) if cycles else ''),ygraph((a,b,c),cycles)
    for k in range(5,11):
        for t in range(1,12-k):
            for p in range(3,12-k-t):
                if p==5:continue
                for cycles in cycle_parts(11-k-t-p):
                    yield f'L10:{k},{t},{p}',lgraph(k,t,p,cycles)
    for k in range(5,11):
        for t in range(1,12-k):
            for cycles in cycle_parts(11-k-t):
                yield f'L11:{k},{t}'+('+'+','.join('C'+str(x) for x in cycles) if cycles else ''),lgraph(k,t,0,cycles)

def cases():
    for label,red in red_forms():
        nr=rows(red);eligible=[i for i in range(11) if len(nr[i])==1 and len(nr[next(iter(nr[i]))])==3]
        for word in range(1<<len(eligible)):
            if word.bit_count()%2:continue
            inside=sum(1<<v for k,v in enumerate(eligible) if (word>>k)&1)
            yield label+':F'+str(inside),red,inside

def run(record_path=None):
    profiles,records=[],[];counts=Counter();densities=Counter()
    sibling_controls=Counter();geometries=list(red_forms())
    require(len(geometries)==24,'geometric red coverage count')
    for label,red,inside in cases():
        nr=rows(red);rd=[len(v) for v in nr]
        require(rd.count(3)==1 and min(rd)==1 and max(rd)==3 and len(red) in (10,11),'R profile')
        wanted,allowed,clauses,fixed=domain(red,inside);stats=Counter();local=Counter();seen=set()
        for blue in complete(wanted,allowed,clauses,fixed,stats):
            code=mask(blue);nd=rows(blue)
            require(code not in seen and not red&blue and [len(v) for v in nd]==wanted,'D degree/disjoint/duplicate')
            require(len(blue)==len(red)+inside.bit_count()//2,'D edge count')
            require(all(clauses[k]&blue for k in range(len(clauses))),'red cross-term cover')
            seen.add(code);fail=failure(red,blue,inside)
            require(fail is not None,'necessary quotient survivor; theorem incomplete')
            local[fail[0]]+=1;counts[fail[0]]+=1;densities['r'+str(len(red))]+=1
            records.append([label,code,fail])
            root=rd.index(3);leaves=sorted(v for v in nr[root] if rd[v]==1)
            if len(leaves)==2:
                l,m=leaves;x=next(iter(nr[root]-set(leaves)))
                if not ((inside>>l)&1):
                    sq=len(nr[l]&nr[x])+len(nd[l]&nd[x])-len(nr[l]&nd[x])-len(nd[l]&nr[x])
                    require(edge(l,x) not in red|blue and sq>=1,'blue sibling leaf matching obstruction')
                    sibling_controls['blue_inside_matching_obstruction']+=1
                else:
                    require((inside>>m)&1 and nd[l]=={m,x} and nd[m]=={l,x},'red inside sibling transfer')
                    sibling_controls['red_inside_forced_neighborhoods']+=1
        profiles.append({'case':label,'R':sorted(red),'inside':inside,'D_completions':len(seen),'first_failure_counts':dict(local)})
    require(len(profiles)==30,'R/inside coverage count')
    records.sort(key=lambda x:(x[0],x[1]))
    encoded=''.join(json.dumps(x,separators=(',',':'))+'\n' for x in records)
    if record_path:record_path.write_text(encoded)
    return {'agent':'six-books-2','role':'researcher','complete':True,
            'scope':'one red trivalent vertex, all regular densities and inside flags; arbitrary matching signs covered by written page identities',
            'profiles':profiles,'geometric_R_forms':len(geometries),'R_inside_cases':len(profiles),
            'total_D_completions':len(records),'density_counts':dict(densities),'first_failure_counts':dict(counts),
            'survivors':0,'canonical_records_sha256':sha256(encoded.encode()).hexdigest(),
            'analytic_sibling_controls':dict(sibling_controls),'controls_are_validation_not_coverage_prunes':True,
            'new_finite_census_is_a_theorem_premise':True,'threads':1,'local_jobs':1}

def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--records',type=Path);parser.add_argument('--emit',action='store_true')
    parser.add_argument('--expected',type=Path,default=Path(__file__).with_name('two_trivalent_expected.json'))
    args=parser.parse_args();result=run(args.records)
    if not args.emit:require(result==json.loads(args.expected.read_text())['census'],'census fixture mismatch')
    print(json.dumps(result,indent=2,sort_keys=True))

if __name__=='__main__':main()
