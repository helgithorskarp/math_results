"""six-reviewer-5: group-free full raw interface audit; standard library.

Generic 23-star coverage is the explicit reviewed premise. No author code,
group quotient, positive-map population or expected readout drives enumeration.
Literal automorphisms are used only to transport surviving actual packings
to the two supplied coloring certificates, after the complete raw scan.
"""
import argparse
from collections import Counter
from hashlib import sha256
from itertools import combinations, permutations
import json
from math import factorial
from pathlib import Path
import resource
import time

HERE = Path(__file__).resolve().parent
PINS = {'TWENTY_STARS.json': 'c188200792c201bdb44ea1667a8a70255c4e40f04fee6c334c98ecfa650113e7',
        'SEED_CERTIFICATES.json': '521f0b322523a340c302fa5f4ea86fd3803a73e3665194e8cff556c0d0635ff6'}

def need(ok, why):
    if not ok:
        raise ValueError(why)

def encoded(x):
    return (json.dumps(x, sort_keys=True, separators=(',', ':'))+'\n').encode()

def mask(word):
    return sum(1 << p for p in word)

def star(raw):
    need(len(raw) == 20 and all(len(w) == len(set(w)) == 4 and all(type(p) is int and 0 <= p < 17 for p in w) for w in raw), 'star domain')
    Q = tuple(frozenset(w) for w in raw)
    need(len(set(Q)) == 20 and all(len(a & b) <= 1 for a,b in combinations(Q,2)), 'star pair packing')
    rho = tuple(sum(p in w for w in Q) for p in range(17))
    need(max(rho) <= 5 and sum(rho) == 80, 'star replication')
    high = frozenset(p for p in range(17) if rho[p] < 5)
    leave = frozenset(frozenset(e) for e in combinations(range(17),2) if not any(set(e) <= w for w in Q))
    core = frozenset(e for e in leave if e <= high)
    need(all(e & high for e in leave) and len(core) == len(high)-1, 'reviewed universal structure')
    return Q, rho, high, leave, core

def domains(data):
    need(len(data['stars']) == 23, 'complete generic fixture list')
    stars, first, second = [], [], []
    for i,raw in enumerate(data['stars']):
        Q,rho,high,leave,core = star(raw); stars.append(Q)
        for u in sorted(high):
            if rho[u] not in (3,4) or any(u in e for e in core) or any(rho[p] != 4 for p in high-{u}):
                continue
            for y in sorted(high-{u}):
                for v in range(17):
                    if rho[v] == 5 and frozenset((v,y)) in leave:
                        first.append((i,u,y,v))
        if any(rho[p] != 4 for p in high):
            continue
        for u,v in permutations(sorted(set(range(17))-high),2):
            for x in sorted(high):
                if frozenset((u,x)) not in leave and frozenset((v,x)) in leave:
                    # The u-leave friend is unique and is not a restriction.
                    friends = [p for p in range(17) if frozenset((u,p)) in leave]
                    need(len(friends) == 1, 'low friend uniqueness')
                    second.append((i,u,v,x,friends[0]))
    need(len(first) == 14 and len(second) == 878, 'full raw marking populations')
    return stars, sorted(first), sorted(second)

class Incomplete(RuntimeError):
    pass

def maps(Q,P,f,s,nodes=200000,seconds=10):
    """Disjoint common-tail recursion; every rejected prefix counts its suffix.

    Private second word images of size3/4 conflict precisely when containing
    an actual first private triple. The finite forbidden set contains exactly
    those triples and their four-point supersets. No partial upper bound is used.
    """
    need(type(nodes) is int and 0 <= nodes <= 200000 and 0 < seconds <= 10, 'fixed guard domain')
    _,u,y,v = f; _,su,sv,sx,*_ = s
    source = sorted(tuple(sorted(w-{sx})) for w in P if sx in w)
    target = sorted(tuple(sorted(w-{y})) for w in Q if y in w)
    m = len(source)
    need(m == len(target) and m in (4,5), 'common tails')
    need(len(set().union(*map(set,source))) == len(set().union(*map(set,target))) == 3*m, 'disjoint tails')
    si = next(i for i,w in enumerate(source) if su in w)
    ti = next(i for i,w in enumerate(target) if u in w)
    need(all(sv not in w for w in source) and all(v not in w for w in target), 'uncovered vxy')
    rs = sorted(set(range(17))-set().union(*map(set,source))-{sx,sv})
    rt = sorted(set(range(18))-set().union(*map(set,target))-{17,y,v})
    need(len(rs) == len(rt), 'residual universe')
    allowed = sorted(set(range(18))-{17,y})
    forbidden = set()
    for w in Q:
        if y in w:
            continue
        for triple in combinations(sorted(w),3):
            t = mask(triple); forbidden.add(t)
            forbidden.update(t | (1 << p) for p in allowed if p not in triple)
    private = tuple(tuple(sorted(w)) for w in P if sx not in w)
    phi = [-1]*17; bits = [0]*17
    for p,q in ((sx,17),(su,u),(sv,v)):
        need(phi[p] == -1 and q not in phi, 'three distinct fixed marks')
        phi[p] = q; bits[p] = 1 << q
    rest = [source[i] for i in range(m) if i != si]
    targets = [target[i] for i in range(m) if i != ti]
    total = 2*factorial(m-1)*6**(m-1)*factorial(len(rs))
    visited = rejected = 0; solutions = []; start = time.monotonic()
    def inspect(weight):
        nonlocal visited,rejected
        visited += 1
        if visited > nodes or time.monotonic()-start > seconds:
            raise Incomplete('unfinished relative-map carrier')
        for a,b,c,d in private:
            if bits[a] | bits[b] | bits[c] | bits[d] in forbidden:
                rejected += weight
                return False
        return True
    def put(src,dst):
        for p,q in zip(src,dst): phi[p]=q; bits[p]=1<<q
    def clear(src):
        for p in src: phi[p]=-1; bits[p]=0
    def visit(depth,available):
        left = len(rest)-depth
        if not inspect(factorial(left)*6**left*factorial(len(rs))): return
        if left:
            tail = rest[depth]
            for k in available:
                for image in permutations(targets[k]):
                    put(tail,image); visit(depth+1,tuple(j for j in available if j != k)); clear(tail)
        else:
            for image in permutations(rt):
                put(rs,image)
                if inspect(1):
                    need(set(phi) == set(range(18))-{y}, 'full point injection')
                    family = tuple(sorted(set(mask(w | {17}) for w in Q) | set((1<<y) | mask(phi[p] for p in w) for w in P)))
                    need(len(family) == 40-m and all((a&b).bit_count() <= 2 for a,b in combinations(family,2)), 'literal full packing')
                    solutions.append((tuple(phi),family))
                clear(rs)
    if inspect(total):
        unmapped = sorted(set(source[si])-{su})
        for image in permutations(sorted(set(target[ti])-{u})):
            put(unmapped,image); visit(0,tuple(range(m-1))); clear(unmapped)
    need(rejected+len(solutions) == total, 'exact map-cylinder coverage')
    return {'full_maps':total,'collision_maps':rejected,'nodes':visited,'solutions':solutions}

def triangles(f,family):
    _,u,y,v=f; result=[]
    for p in sorted(set(range(18))-{17,y,u,v}):
        triple=(1<<17)|(1<<y)|(1<<p)
        if not any(triple & w == triple for w in family) and all(sum(pair & w == pair for w in family) == 4 for pair in ((1<<17)|(1<<y),(1<<17)|(1<<p),(1<<y)|(1<<p))):
            result.append(p)
    return result

def seed_caps(seeds):
    result=[]
    for seed in seeds['seeds']:
        family=tuple(seed['core_masks']); centers=seed['saturated_centers']
        need(len(family) == len(set(family)) == 36 and all(type(w) is int and 0<w<(1<<18) and w.bit_count()==5 for w in family), 'seed domain')
        need(all((a&b).bit_count()<=2 for a,b in combinations(family,2)), 'seed packing')
        need(len(centers)==len(set(centers))==2 and all(sum(w>>p&1 for w in family)==20 for p in centers), 'complete seed centers')
        candidates=[]
        for q in combinations(sorted(set(range(18))-set(centers)),5):
            w=mask(q)
            if all((w&a).bit_count()<=2 for a in family): candidates.append(w)
        need(len(candidates)==seed['candidate_count'] and sha256(encoded(candidates)).hexdigest()==seed['candidate_sha256'], 'whole residual candidate universe')
        colors=seed['colors']; cap=seed['capacity']
        need(type(cap) is int and cap>0 and len(colors)==len(candidates) and all(type(c) is int and 0<=c<cap for c in colors), 'color certificate domain')
        edges=0
        for i,j in combinations(range(len(candidates)),2):
            if (candidates[i]&candidates[j]).bit_count()<=2:
                need(colors[i]!=colors[j], 'improper coloring'); edges+=1
        need(seed['upper_bound']==36+cap, 'total bound')
        result.append({'seed':seed['seed'],'candidates':len(candidates),'edges':edges,'colors':cap,'upper_bound':36+cap})
    need(sorted(r['upper_bound'] for r in result)==[61,64], 'two literal caps')
    return result

def transport(f,family,stars,data,seeds):
    i,u,y,v=f
    need(i==9, 'surviving first fixture')
    # Every returned map is a checked actual point bijection and block image.
    # Failure to find one raises, and cannot establish nonexistence.
    for g in data['groups'][i]:
        if (g[u],g[y],g[v]) != (13,11,2): continue
        need(len(g)==17 and set(g)==set(range(17)), 'transport permutation')
        need({frozenset(g[p] for p in w) for w in stars[i]}==set(stars[i]), 'actual star automorphism')
        gp=tuple(g)+(17,)
        images=tuple(sorted(mask(gp[p] for p in range(18) if w>>p&1) for w in family))
        for seed in seeds['seeds']:
            if images==tuple(seed['core_masks']): return {'seed':seed['seed'],'point_map':gp}
    raise ValueError('survivor has no literal seed transport')

def run(data,seeds,limit=None):
    stars,first,second=domains(data); caps=seed_caps(seeds)
    records=[]; positives=[]; survivors=[]; start=time.monotonic()
    for fi,f in enumerate(first):
        for si,s in enumerate(second):
            if time.monotonic()-start>180: raise Incomplete('whole raw carrier budget hit')
            r=maps(stars[f[0]],stars[s[0]],f,s)
            records.append([list(f),list(s),r['full_maps'],r['collision_maps'],r['nodes']])
            for phi,family in r['solutions']:
                ts=triangles(f,family); pos={'first':f,'second':s,'point_map':phi,'family':family,'triangles':ts}; positives.append(pos)
                if not ts:
                    t=transport(f,family,stars,data,seeds); survivors.append({**pos,'transport':t})
            if limit and len(records)>=limit: return {'sample_cases':len(records),'seconds':time.monotonic()-start,'nodes':sum(r[4] for r in records)}
    exact={'raw_first':len(first),'raw_second':len(second),'products':len(records),
           'represented_full_maps':sum(r[2] for r in records),'collision_full_maps':sum(r[3] for r in records),
           'nodes':sum(r[4] for r in records),'maximum_nodes':max(r[4] for r in records),
           'positive_maps':len(positives),'positive_products':len({(r['first'],r['second']) for r in positives}),
           'triangle_rejected':sum(bool(r['triangles']) for r in positives),'triangle_witnesses':sum(len(r['triangles']) for r in positives),
           'surviving_maps':len(survivors),'survivor_seed_counts':{str(k):v for k,v in sorted(Counter(r['transport']['seed'] for r in survivors).items())},
           'survivor_hub_multiplicities':sorted({sum(r['first'][1] in w for w in stars[r['first'][0]]) for r in survivors}),
           'caps':caps,'records_sha256':sha256(encoded(records)).hexdigest(),'positive_sha256':sha256(encoded(positives)).hexdigest(),
           'survivors_sha256':sha256(encoded(survivors)).hexdigest()}
    need(exact['survivor_hub_multiplicities']==[3], 'forced deficient pair count')
    return {'status':'PASS_COMPLETE_RAW_CARRIER','agent':'six-reviewer-5','role':'independent mathematical reviewer','exact':exact,
            'seconds':time.monotonic()-start,'peak_rss_kib':resource.getrusage(resource.RUSAGE_SELF).ru_maxrss,
            '_records':records,'_positives':positives,'_survivors':survivors}

def main():
    parser=argparse.ArgumentParser(); parser.add_argument('--output',required=True); parser.add_argument('--sample',type=int); parser.add_argument('--compare',action='store_true');args=parser.parse_args()
    inputs={}
    for name,pin in PINS.items():
        raw=(HERE/name).read_bytes();need(sha256(raw).hexdigest()==pin,'credited input pin '+name);inputs[name]=json.loads(raw)
    result=run(inputs['TWENTY_STARS.json'],inputs['SEED_CERTIFICATES.json'],args.sample)
    out=Path(args.output);out.parent.mkdir(parents=True,exist_ok=True)
    private={k:result.pop(k) for k in list(result) if k.startswith('_')}
    if private: out.with_suffix('.private.json').write_bytes(encoded(private))
    if args.compare: need(result['exact']==json.loads((HERE/'EXPECTED.json').read_text()),'frozen full readout')
    out.write_bytes(encoded(result));print(json.dumps(result,sort_keys=True))

if __name__=='__main__': main()
