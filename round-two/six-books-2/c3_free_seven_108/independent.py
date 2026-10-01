"""Independent column-word, pair-join and weight-phase completion checker.

Imports no producer, solver, or third-party package. The input incidence
table is untrusted: its complete set is independently regenerated.
"""
import argparse
import hashlib
import itertools
import json
from pathlib import Path
import resource
import time

PAIRS_A = tuple(itertools.combinations(range(9),2))
PAIRS_B = tuple(itertools.combinations(range(4),2))
WEIGHT_MASKS = ((0,),(1,2,4),(3,5,6),(7,))


def require(condition,message):
    if not condition:
        raise ValueError(message)


def local_graph(code):
    rows = [0]*9
    for u,v in PAIRS_A:
        i,j = u//3,v//3
        bit = i if i==j else 3+3*((0,1),(0,2),(1,2)).index((i,j))+(v%3-u%3)%3
        if code>>bit&1:
            rows[u] |= 1<<v
            rows[v] |= 1<<u
    return rows


def row_data(rows,full):
    demands = tuple(full[u]-1-rows[u].bit_count() for u in range(9))
    caps = []
    for u,v in PAIRS_A:
        if rows[u]>>v&1:
            cap = 3-1-(rows[u]&rows[v]).bit_count()
        else:
            known_blue = (511^(rows[u]|rows[v]|(1<<u)|(1<<v))).bit_count()
            cap = 6-known_blue-12+demands[u]+demands[v]
        caps.append(cap)
    return demands,tuple(caps)


def local_coverage():
    result = {}
    for inside in (True,False):
        full = [9]*3+[10]*6 if inside else [10]*9
        inverse_maps = []
        for permutation in itertools.permutations(range(3)):
            if inside and permutation[0]!=0:
                continue
            for shifts in itertools.product(range(3),repeat=3):
                for sign in (-1,1):
                    inverse = [0]*9
                    for i in range(3):
                        for t in range(3):
                            inverse[3*permutation[i]+(sign*t+shifts[i])%3] = 3*i+t
                    inverse_maps.append(inverse)
        groups = {}
        initial = set()
        for code in range(4096):
            rows = local_graph(code)
            degrees = [row.bit_count() for row in rows]
            edges = sum(degrees)//2
            if max(degrees)>3 or not (9 if inside else 12)<=edges<=12:
                continue
            demands,caps = row_data(rows,full)
            if any(cap<max(0,demands[u]+demands[v]-12) for (u,v),cap in zip(PAIRS_A,caps)):
                continue
            initial.add(code)
            obstructed = False
            for triple in itertools.combinations(range(9),3):
                s = sum(demands[u] for u in triple)
                q,r = divmod(s,12)
                minimum = 12*sum(range(q))+r*q
                capacity = sum(caps[PAIRS_A.index((u,v))] for u,v in itertools.combinations(triple,2))
                if minimum>capacity:
                    obstructed = True
                    break
            if obstructed:
                continue
            variants = []
            for inverse in inverse_maps:
                bits = [rows[inverse[3*i]]>>inverse[3*i+1]&1 for i in range(3)]
                bits += [rows[inverse[3*i]]>>inverse[3*j+t]&1
                         for i,j in ((0,1),(0,2),(1,2)) for t in range(3)]
                variants.append(sum(bit<<k for k,bit in enumerate(bits)))
            groups.setdefault(min(variants),[]).append(code)
        result['inside' if inside else 'outside'] = dict(initial=len(initial),groups=groups)
    return result


def shift_word(word):
    return sum((((word>>(3*i)&7)<<1 & 7) | ((word>>(3*i)&7)>>2))<<(3*i) for i in range(3))


def masks_of_column(word):
    return tuple(sum((word>>(3*i+(-k)%3)&1)<<k for k in range(3)) for i in range(3))


def column_domains(rows,full,outside_degree):
    demands,caps = row_data(rows,full)
    candidates = {}
    for seed in range(512):
        columns = (seed,shift_word(seed),shift_word(shift_word(seed)))
        key = min(masks_of_column(column) for column in columns)
        if key in candidates:
            continue
        aligned = next(i for i,column in enumerate(columns) if masks_of_column(column)==key)
        columns = columns[aligned:]+columns[:aligned]
        q = seed.bit_count()
        beta = outside_degree-q
        if beta<5:
            continue
        good = True
        for column in columns:
            for a in range(9):
                if column>>a&1:
                    known = (rows[a]&column).bit_count()
                    lower = max(0,demands[a]-1+beta-11)
                    cap = 3
                else:
                    known = (511^(rows[a]|column|(1<<a))).bit_count()
                    lower = max(0,11-demands[a]-beta)
                    cap = 6
                if known+lower>cap:
                    good = False
                    break
            if not good:
                break
        if not good:
            continue
        intersections = tuple(sum((col>>u&1)&(col>>v&1) for col in columns) for u,v in PAIRS_A)
        if any(x>cap for x,cap in zip(intersections,caps)):
            continue
        counts = tuple(sum(col>>(3*i)&1 for col in columns) for i in range(3))
        candidates[key] = dict(columns=columns,counts=counts,pairs=intersections)
    return candidates


def join_templates(rows,full,inside):
    high = column_domains(rows,full,10)
    low = high if inside else column_domains(rows,full,9)
    hkeys,lkeys = sorted(high),sorted(low)
    demands,caps = row_data(rows,full)
    target = tuple(demands[3*i] for i in range(3))
    second_pairs = {}
    for j,key in enumerate(hkeys):
        for k in range(j,len(hkeys)):
            other = hkeys[k]
            counts = tuple(x+y for x,y in zip(high[key]['counts'],high[other]['counts']))
            pairs = tuple(x+y for x,y in zip(high[key]['pairs'],high[other]['pairs']))
            if any(x>t for x,t in zip(counts,target)) or any(x>cap for x,cap in zip(pairs,caps)):
                continue
            second_pairs.setdefault(counts,[]).append((j,k,pairs))
    results = set()
    for i,key in enumerate(lkeys):
        for j in range(i if inside else 0,len(hkeys)):
            other = hkeys[j]
            counts = tuple(x+y for x,y in zip(low[key]['counts'],high[other]['counts']))
            residual = tuple(t-x for t,x in zip(target,counts))
            if min(residual)<0:
                continue
            pairs = tuple(x+y for x,y in zip(low[key]['pairs'],high[other]['pairs']))
            for k,l,other_pairs in second_pairs.get(residual,[]):
                if j>k or any(x+y>cap for x,y,cap in zip(pairs,other_pairs,caps)):
                    continue
                results.add((key,other,hkeys[k],hkeys[l]))
    return results,high,low


def check_incidence_input(cases):
    coverage = local_coverage()
    required = {(placement,code) for placement,data in coverage.items() for code in data['groups']}
    require(len(cases)==len(required),'incorrect number of root cases')
    require({(case['placement'],case['code']) for case in cases}==required,'missing or extra root case')
    data = {}
    for case in cases:
        inside = case['placement']=='inside'
        rows = local_graph(case['code'])
        full = [9]*3+[10]*6 if inside else [10]*9
        generated,high,low = join_templates(rows,full,inside)
        recorded = [tuple(tuple(mask) for mask in template) for template in case['incidence_representatives']]
        require(len(recorded)==len(set(recorded)),'duplicate incidence template')
        require(set(recorded)==generated,'incidence table omits or alters a template')
        require(case['status']=='COMPLETE' and case['representatives']==len(generated),'incomplete incidence declaration')
        require(case['high_domains']==len(high) and case['low_domains']==len(low),'domain count differs')
        data[case['placement'],case['code']] = (rows,full,high,low,recorded)
    return coverage,data


def b_rows(internal,masks):
    rows = [0]*12
    for u,v in itertools.combinations(range(12),2):
        i,j = u//3,v//3
        red = internal>>i&1 if i==j else masks[PAIRS_B.index((i,j))]>>((v-u)%3)&1
        if red:
            rows[u] |= 1<<v
            rows[v] |= 1<<u
    return tuple(rows)


def independent_b_graphs(profile):
    accepted = {}
    matched = 0
    for internal in range(16):
        target = [profile[i]-2*(internal>>i&1) for i in range(4)]
        if min(target)<0:
            continue
        def visit(position,remaining,weights):
            nonlocal matched
            if position==6:
                if any(remaining):
                    return
                for masks in itertools.product(*(WEIGHT_MASKS[w] for w in weights)):
                    matched += 1
                    rows = b_rows(internal,masks)
                    good = True
                    for u,v in itertools.combinations(range(12),2):
                        if rows[u]>>v&1:
                            count = (rows[u]&rows[v]).bit_count()
                            cap = 3
                        else:
                            count = (4095^(rows[u]|rows[v]|(1<<u)|(1<<v))).bit_count()
                            cap = 5
                        if count>cap:
                            good = False
                            break
                    if good:
                        code = internal+sum(mask<<(4+3*p) for p,mask in enumerate(masks))
                        require(code not in accepted,'duplicate outside graph')
                        accepted[code] = rows
                return
            u,v = PAIRS_B[position]
            for weight in range(min(3,remaining[u],remaining[v])+1):
                next_remaining = remaining.copy()
                next_remaining[u] -= weight
                next_remaining[v] -= weight
                if any(next_remaining[i]>3*sum(i in pair for pair in PAIRS_B[position+1:]) for i in range(4)):
                    continue
                visit(position+1,next_remaining,weights+[weight])
        visit(0,target,[])
    digest = hashlib.sha256(''.join(str(code)+'\n' for code in sorted(accepted)).encode()).hexdigest()
    return accepted,dict(degrees=list(profile),degree_matches=matched,
                         necessary_page_survivors=len(accepted),candidate_sha256=digest)


def accepts_completion(local,full,columns,bgraph):
    # Inspect all physical B-B spines first, separately in A and B.
    for u,v in itertools.combinations(range(12),2):
        if bgraph[u]>>v&1:
            pages = (bgraph[u]&bgraph[v]).bit_count()+(columns[u]&columns[v]).bit_count()
            cap = 3
        else:
            pages = (4095^(bgraph[u]|bgraph[v]|(1<<u)|(1<<v))).bit_count()
            pages += (511^(columns[u]|columns[v])).bit_count()+1
            cap = 6
        if pages>cap:
            return False
    stars = tuple(sum((columns[b]>>a&1)<<b for b in range(12)) for a in range(9))
    demands,caps = row_data(local,full)
    require(tuple(star.bit_count() for star in stars)==demands,'completion has wrong A degrees')
    for (u,v),cap in zip(PAIRS_A,caps):
        require((stars[u]&stars[v]).bit_count()<=cap,'invalid A pair in incidence template')
    for a in range(9):
        for b in range(12):
            if columns[b]>>a&1:
                pages = (local[a]&columns[b]).bit_count()+(stars[a]&bgraph[b]).bit_count()
                cap = 3
            else:
                pages = (511^(local[a]|columns[b]|(1<<a))).bit_count()
                pages += (4095^(stars[a]|bgraph[b]|(1<<b))).bit_count()
                cap = 6
            if pages>cap:
                return False
    return True


def run(cases,expected):
    coverage,data = check_incidence_input(cases)
    profiles = set()
    for case in cases:
        full_b = (10,10,10,10) if case['placement']=='inside' else (9,10,10,10)
        for template in case['incidence_representatives']:
            profiles.add(tuple(d-sum(mask.bit_count() for mask in pattern) for d,pattern in zip(full_b,template)))
    all_b = {}
    manifests = []
    for profile in sorted(profiles):
        all_b[profile],manifest = independent_b_graphs(profile)
        manifests.append(manifest)
        print('independent outside profile',profile,manifest['degree_matches'],manifest['necessary_page_survivors'],flush=True)
    if expected is not None:
        require(manifests==expected['outside_profiles'],'outside enumeration manifests differ')
    results = []
    valid = 0
    for case in cases:
        tag = case['placement'],case['code']
        local,full,high,low,recorded = data[tag]
        full_b = (10,10,10,10) if tag[0]=='inside' else (9,10,10,10)
        counts = []
        for template in recorded:
            columns = tuple(column for j,key in enumerate(template)
                            for column in (low if j==0 else high)[key]['columns'])
            profile = tuple(d-columns[3*j].bit_count() for j,d in enumerate(full_b))
            failures = 0
            for bgraph in all_b[profile].values():
                if accepts_completion(local,full,columns,bgraph):
                    valid += 1
                else:
                    failures += 1
            counts.append(dict(profile=list(profile),tested=len(all_b[profile]),rejected=failures))
        record = dict(placement=tag[0],code=tag[1],incidence_representatives=len(recorded),
                      completions_tested=sum(x['tested'] for x in counts),
                      completions_rejected=sum(x['rejected'] for x in counts),per_incidence=counts)
        if expected is not None:
            matching = [x for x in expected['cases'] if (x['placement'],x['code'])==tag]
            require(len(matching)==1,'missing expected completion case')
            require(all(matching[0].get(k)==v for k,v in record.items()),'completion records differ')
        results.append(record)
        print('independent completion',tag,record['completions_tested'],record['completions_rejected'],flush=True)
    require(valid==0,'valid completion found: exclusion is false')
    return dict(status='EXACT_INDEPENDENT_EXCLUSION',mathematical_exclusion=True,
                initial_roots={k:v['initial'] for k,v in coverage.items()},
                reduced_roots={k:{str(c):len(words) for c,words in v['groups'].items()} for k,v in coverage.items()},
                outside_profiles=manifests,cases=results,valid_completions=valid)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--incidences',type=Path,required=True)
    parser.add_argument('--expected',type=Path)
    parser.add_argument('--output',type=Path,required=True)
    args = parser.parse_args()
    started = time.monotonic()
    result = run(json.loads(args.incidences.read_text()),
                 json.loads(args.expected.read_text()) if args.expected else None)
    result['seconds'] = time.monotonic()-started
    result['rss_kib'] = resource.getrusage(resource.RUSAGE_SELF).ru_maxrss
    args.output.write_text(json.dumps(result,indent=2)+'\n')
    print('EXACT_INDEPENDENT_EXCLUSION',result['seconds'],'seconds',result['rss_kib'],'RSS KiB',flush=True)


if __name__ == '__main__':
    main()
