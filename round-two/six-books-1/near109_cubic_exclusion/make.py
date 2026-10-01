"""Exact quotient enumeration, integer star tests and full outside completion search."""
from collections import defaultdict, Counter
from itertools import combinations, combinations_with_replacement, product
import json
from pathlib import Path
import time
import sys

START = time.monotonic()
HERE = Path(__file__).resolve().parent
base = json.loads((HERE/'model.json').read_text())
ground = list(combinations(range(5), 2))
P=[sum(1<<j for j,e in enumerate(ground) if set(f).isdisjoint(e)) for f in ground]
if P!=base['petersen']:raise ValueError('two-subset model mismatch')
index = {e: i for i, e in enumerate(ground)}
pairs = list(combinations(range(10), 2))
red_pairs = [(i, j) for i, j in pairs if P[i] >> j & 1]
neighbors = [{j for j in range(10) if P[i] >> j & 1} for i in range(10)]
stars = [sum(1 << i for i, e in enumerate(ground) if a in e) for a in range(5)]
domains={}
for deficit in range(3):
    words=[]
    for z in range(1024):
        C={i for i in range(10) if not z>>i&1};Z=set(range(10))-C;k=len(Z)
        if not 4+deficit<=k<=8:continue
        if any(len(neighbors[i]&C)>(1 if deficit==0 else 2) for i in C):continue
        if any(k-deficit>8-len(neighbors[i]&C) for i in C):continue
        if any(len(neighbors[i]&Z)<k-7 for i in Z):continue
        words.append(z)
    domains[str(deficit)]=words


def vector(z):
    return tuple(z >> i & 1 for i in range(10))


def quotient(v):
    def e(i, j):
        return v[index[tuple(sorted((i, j)))]]
    return tuple([e(0, j) - e(1, j) - e(0, 2) + e(1, 2) for j in [3, 4]] +
                 [e(0, i) + e(0, j) - e(i, j) - e(0, 1) - e(0, 2) + e(1, 2)
                  for i, j in [(2, 3), (2, 4), (3, 4)]])


vec = {z: vector(z) for z in range(1024)}
quo = {z: quotient(vec[z]) for z in range(1024)}
red = {z: sum(1 << t for t, (i, j) in enumerate(red_pairs) if z >> i & 1 and z >> j & 1)
       for z in range(1024)}
isolated = {z: sum(1 << i for i in range(10) if not (z >> i & 1)
                  and all(z >> j & 1 for j in neighbors[i])) for z in range(1024)}
high = {k: sorted(z for z in domains['0'] if z.bit_count() == k) for k in range(5, 9)}


def patterns(amount, min_size=5):
    if not amount:
        yield ()
        return
    for k in range(min_size, min(8, amount + 4) + 1):
        for tail in patterns(amount - (k - 4), k):
            yield (k,) + tail


def words_for_pattern(pattern):
    blocks = []
    for k, copies in sorted(Counter(pattern).items()):
        blocks.append(combinations_with_replacement(high[k], copies))
    for choice in product(*blocks):
        yield tuple(z for group in choice for z in group)


groups = {}
high_counts = []
for excess in range(5):
    by_key = defaultdict(list)
    raw = retained = 0
    for pattern in patterns(excess):
        for words in words_for_pattern(pattern):
            raw += 1
            used = 0
            for z in words:
                if red[z] & used:
                    break
                used |= red[z]
            else:
                key = tuple(sum(quo[z][i] for z in words) for i in range(5))
                by_key[key].append((words, used))
                retained += 1
    groups[excess] = by_key
    high_counts.append({'excess': excess, 'raw_high_multisets': raw,
                        'red_capped_high_multisets': retained, 'quotient_keys': len(by_key)})


def four_multiplicities(large):
    a = [5 - sum(vec[z][i] for z in large) for i in range(10)]
    twice0 = a[index[0, 1]] + a[index[0, 2]] - a[index[1, 2]]
    if twice0 % 2:
        return None
    mu = [twice0 // 2]
    mu.extend(a[index[0, j]] - mu[0] for j in range(1, 5))
    if any(m < 0 or m > 2 for m in mu):
        return None
    if any(mu[i] + mu[j] != a[index[i, j]] for i, j in ground):
        return None
    if sum(mu) + len(large) != 11:
        return None
    return mu


def pair_bounds(words):
    for i, j in pairs:
        count = sum(bool(z >> i & 1 and z >> j & 1) for z in words)
        if count > (1 if P[i] >> j & 1 else 3):
            return False
    return True


def row_pair_possible(z, w, dz, dw):
    common_red = 10 - (z | w).bit_count()
    blue_possible = (z & w).bit_count() <= 5 and common_red + dz + dw <= 6
    return common_red <= 3 or blue_possible


def scan(mode):
    stats = Counter()
    records = []
    pool = sorted(domains['2'] if mode == 'one8' else domains['1'])
    low_choices = ((z,) for z in pool) if mode == 'one8' else combinations_with_replacement(pool, 2)
    for lows in low_choices:
        excess = 6 - sum(z.bit_count() - 4 for z in lows)
        if not 0 <= excess <= 4:
            continue
        stats['low_choices'] += 1
        used = 0
        for z in lows:
            if used & red[z]:
                break
            used |= red[z]
        else:
            stats['low_red_capped'] += 1
            if mode == 'two9' and not row_pair_possible(lows[0], lows[1], 1, 1):
                continue
            key = tuple(-sum(quo[z][i] for z in lows) for i in range(5))
            for highs, high_red in groups[excess].get(key, []):
                stats['projection_joins'] += 1
                if high_red & used:
                    continue
                highs=tuple(sorted(highs))
                large = lows + highs
                mu = four_multiplicities(large)
                if mu is None:
                    continue
                stats['four_integer_recoveries'] += 1
                words = list(large) + [star for star, count in zip(stars, mu) for _ in range(count)]
                if not pair_bounds(words):
                    continue
                stats['pair_capped_incidence'] += 1
                deficit = ([2] if mode == 'one8' else [1, 1]) + [0] * (11 - len(lows))
                if not all(row_pair_possible(words[a], words[b], deficit[a], deficit[b])
                           for a, b in combinations(range(11), 2)):
                    continue
                stats['literal_B_pair_minima'] += 1
                # Optional conditional strengthening: if all full-degree roots
                # are cubic, an isolated C-point of a high row must be dirty.
                clean = 1023
                for z in lows:
                    clean &= z
                conditional = all(not (isolated[z] & clean) for z in words[len(lows):])
                stats['conditional_all_full_roots_cubic'] += conditional
                if not conditional:continue
                records.append({'low_rows': list(lows), 'high_large_rows': list(highs),
                                'four_star_multiplicities': mu,
                                'conditional_all_full_roots_cubic': conditional})
    return {'mode': mode, 'statistics': dict(stats), 'records': records}



weights={d:[z for z in range(2048) if z.bit_count()==d] for d in range(11)}
def domain(words,deficits,b,cols,local=None):
    local=P if local is None else local
    z=words[b];k=z.bit_count();degree=k-deficits[b];universe=((1<<len(words))-1)^(1<<b)
    lower=[]
    for i in range(10):
        if z>>i&1:lo=k+cols[i].bit_count()-8-(local[i]&z).bit_count()
        else:lo=degree+(local[i]&(1023^z)).bit_count()-3
        if lo>0:lower.append((cols[i]&universe,lo,i))
    # Exact two-column required-intersection bound; a necessary pruning cut.
    for (x,lx,i),(y,ly,j) in combinations(lower,2):
        twice=(x&y).bit_count();once=(x^y).bit_count()
        maximum=2*min(degree,twice)+min(max(0,degree-twice),once)
        if lx+ly>maximum:return [],{'type':'pair','points':[i,j],'required':lx+ly,'maximum':maximum}
    lower.sort(key=lambda item:(-item[1],item[0].bit_count(),item[2]))
    pool=weights[degree] if len(words)==11 else [w for w in range(1<<len(words)) if w.bit_count()==degree]
    out=[w for w in pool if not w>>b&1 and all((w&x).bit_count()>=lo for x,lo,_ in lower)]
    return out,None


def compatible(words,b,c,x,y):
    edge=x>>c&1
    if edge!=(y>>b&1):return False
    if edge:
        return 10-(words[b]|words[c]).bit_count()+(x&y).bit_count()<=3
    universe=(1<<len(words))-1
    bluex=(universe^(1<<b))^x;bluey=(universe^(1<<c))^y
    return 1+(words[b]&words[c]).bit_count()+(bluex&bluey).bit_count()<=6


def solve(words,domains):
    nodes=0;solutions=0
    def visit(current,assignment):
        nonlocal nodes,solutions
        nodes+=1
        if not current:
            solutions+=1
            return assignment
        b=min(current,key=lambda i:(len(current[i]),i))
        for x in current[b]:
            next_domains={}
            for c,ys in current.items():
                if c==b:continue
                kept=[y for y in ys if compatible(words,b,c,x,y)]
                if not kept:break
                next_domains[c]=kept
            else:
                found=visit(next_domains,assignment+[(b,x)])
                if found is not None:return found
        return None
    answer=visit({i:v for i,v in enumerate(domains)},[])
    return answer,nodes,solutions




def digest(records):
    import hashlib
    return hashlib.sha256(''.join(json.dumps(x,separators=(',',':'))+'\n' for x in sorted(records)).encode()).hexdigest()


def controls():
    from control_data import primary_problem,weighted_controls,require
    local,words,delta,actual,masks=primary_problem(HERE)
    cols=[sum(1<<b for b,z in enumerate(words) if z>>i&1) for i in range(10)]
    ds=[domain(words,delta,b,cols,local)[0] for b in range(10)]
    require(all(actual[b] in ds[b] for b in range(10)),'positive star acceptance')
    answer,_,_=solve(words,[[x] for x in actual])
    require(answer is not None,'positive completion acceptance')
    # Damage an actual degree-correct star by exchanging one red and one blue B-point.
    damaged=0
    for b in range(10):
        for c in range(10):
            for d in range(10):
                if c==b or d==b or c==d or not actual[b]>>c&1 or actual[b]>>d&1:continue
                trial=actual[:];trial[b]^=(1<<c)|(1<<d)
                result,_,_=solve(words,[[x] for x in trial])
                require(result is None,'asymmetric damaged completion accepted')
                damaged+=1
    literal=0
    for record in weighted_controls():
        g=record['neighbor_masks'];local=record['local'];rows=record['miss_rows']
        delta=[10-x.bit_count() for x in g]
        col=[sum(1<<b for b,z in enumerate(rows) if z>>i&1) for i in range(10)]
        require(all(col[i].bit_count()==local[i].bit_count()+2+delta[i+1] for i in range(10)), 'weighted columns')
        for i,j in combinations(range(10),2):
            h=local[i].bit_count()+local[j].bit_count();c=(local[i]&local[j]).bit_count();s=(col[i]&col[j]).bit_count()
            if local[i]>>j&1:
                pages=(g[i+1]&g[j+1]).bit_count();formula=8-h-delta[i+1]-delta[j+1]+c+s
            else:
                bluei=((1<<22)-1)^g[i+1]^(1<<(i+1));bluej=((1<<22)-1)^g[j+1]^(1<<(j+1))
                pages=(bluei&bluej).bit_count();formula=8-h+c+s
            require(pages==formula,'literal weighted pair identity');literal+=1
    # Integer packing inequalities, including endpoints, are checked literally.
    require(all(t*(t-1)//2>=t-1 for t in range(5)),'four column packing')
    require(all(t*(t-1)//2>=2*t-3 for t in range(6)),'five column packing')
    return {'positive21_star_domains':10,'positive21_completion':1,
            'damaged21_completions_rejected':damaged,'signed109_controls':4,
            'weighted_column_entries':40,'weighted_literal_pair_entries':literal}


def compute():
    result={'schema':1,'row_domains':{str(d):{'count':len(domains[str(d)]),
        'by_size':dict(sorted(Counter(z.bit_count() for z in domains[str(d)]).items()))} for d in range(3)},
        'red_capped_high_multisets':[x['red_capped_high_multisets'] for x in high_counts],
        'controls':controls(),'cases':{}}
    for mode in ['one8','two9']:
        data=scan(mode);keys=set();nonempty=[];empty=paircuts=nodes=solutions=0
        for record in data['records']:
            key=(tuple(record['low_rows']),tuple(record['high_large_rows']),tuple(record['four_star_multiplicities']))
            if key in keys:raise ValueError('duplicate incidence')
            keys.add(key)
            words=list(key[0])+list(key[1])+[z for z,m in zip(stars,key[2]) for _ in range(m)]
            ds=([2] if mode=='one8' else [1,1])+[0]*(11-len(key[0]))
            cols=[sum(1<<b for b,z in enumerate(words) if z>>i&1) for i in range(10)]
            sizes=[];all_domains=[]
            for b in range(11):
                values,cut=domain(words,ds,b,cols)
                if not values:
                    empty+=1;paircuts+=cut is not None;break
                all_domains.append(values);sizes.append(len(values))
            else:
                nonempty.append((key,tuple(sizes)))
                answer,n,sol=solve(words,all_domains);nodes+=n;solutions+=sol
                if answer is not None:raise ValueError('counterexample found; theorem fails')
        result['cases'][mode]={'incidence_records':len(keys),'incidence_sha256':digest(keys),
            'empty_star_cases':empty,'all_stars_nonempty':len(nonempty),
            'nonempty_domain_sizes_sha256':digest(nonempty),'completions':solutions}
        print(json.dumps({'phase':'case-complete','mode':mode,'records':len(keys),
                          'nonempty':len(nonempty),'search_nodes':nodes,'pair_cuts':paircuts,
                          'elapsed':time.monotonic()-START}),flush=True)
    return result

if __name__=='__main__':
    result=compute()
    canonical=json.loads(json.dumps(result))
    if sys.argv[1:]==['--write']:
        (HERE/'expected.json').write_text(json.dumps(canonical,sort_keys=True,indent=2)+'\n')
    elif sys.argv[1:]:raise ValueError('usage: make.py [--write]')
    elif canonical!=json.loads((HERE/'expected.json').read_text()):raise ValueError('expected record mismatch')
    print(json.dumps({'status':'PASS','elapsed':time.monotonic()-START,'cases':result['cases']}),flush=True)
