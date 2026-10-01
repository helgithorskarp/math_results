"""Independent degree-composition, column-word, pair-join and weight-phase audit.

Imports no producer, solver or third-party package. Input incidence templates
are untrusted and their entire set is regenerated. Completions are checked
without the producer's forced-edge cuts, on all physical pairs in A and B.
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
POINT_PAIRS_B = tuple(itertools.combinations(range(12),2))
WEIGHT_MASKS = ((0,),(1,2,4),(3,5,6),(7,))


def require(condition,message):
    if not condition:
        raise ValueError(message)


def degree_profiles():
    profiles = set()
    for deficits in itertools.product(range(4),repeat=7):
        if sum(deficits)==3 and sum(deficits[:3])>0:
            profiles.add(tuple(sorted(deficits[:3],reverse=True)+sorted(deficits[3:],reverse=True)))
    require(len(profiles)==7,'degree composition coverage')
    return sorted(profiles,reverse=True)


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


def incidence_minima():
    """Independent finite DP: 12 column loads, each in {0,...,t}."""
    tables = {}
    for points in range(3,10):
        values = {0:0}
        for _ in range(12):
            next_values = {}
            for total,cost in values.items():
                for load in range(points+1):
                    key = total+load
                    new_cost = cost+load*(load-1)//2
                    next_values[key] = min(next_values.get(key,10**9),new_cost)
            values = next_values
        tables[points] = values
    return tables


def local_coverage():
    result = {}
    minima = incidence_minima()
    subsets = [(subset,[PAIRS_A.index(pair) for pair in itertools.combinations(subset,2)])
               for size in range(3,10) for subset in itertools.combinations(range(9),size)]
    for deficits in degree_profiles():
        cycles = tuple(10-d for d in deficits)
        full = [cycles[u//3] for u in range(9)]
        lower_edges = sum(full)+30-105
        inverse_maps = []
        for permutation in itertools.permutations(range(3)):
            if any(cycles[i]!=cycles[permutation[i]] for i in range(3)):
                continue
            for shifts in itertools.product(range(3),repeat=3):
                for sign in (-1,1):
                    inverse = [0]*9
                    for i in range(3):
                        for t in range(3):
                            inverse[3*permutation[i]+(sign*t+shifts[i])%3] = 3*i+t
                    inverse_maps.append(inverse)
        groups,initial = {},set()
        for code in range(4096):
            rows = local_graph(code)
            degrees = [row.bit_count() for row in rows]
            if max(degrees)>3 or not lower_edges<=sum(degrees)//2<=12:
                continue
            demands,caps = row_data(rows,full)
            if any(cap<max(0,demands[u]+demands[v]-12) for (u,v),cap in zip(PAIRS_A,caps)):
                continue
            initial.add(code)
            obstructed = False
            for subset,indices in subsets:
                total = sum(demands[u] for u in subset)
                require(total in minima[len(subset)],'incidence total outside finite DP')
                if minima[len(subset)][total]>sum(caps[i] for i in indices):
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
        result[deficits] = dict(pair_raw=len(initial),groups=groups)
    return result


def shift_word(word):
    return sum((((word>>(3*i)&7)<<1&7)|((word>>(3*i)&7)>>2))<<(3*i) for i in range(3))


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
        beta = outside_degree-seed.bit_count()
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


def join_templates(rows,full,degrees_b):
    by_degree = {degree:column_domains(rows,full,degree) for degree in sorted(set(degrees_b))}
    pools = [by_degree[d] for d in degrees_b]
    keys = [sorted(pool) for pool in pools]
    demands,caps = row_data(rows,full)
    target = tuple(demands[3*i] for i in range(3))
    last_pairs = {}
    for i,key in enumerate(keys[2]):
        for j in range(i if degrees_b[2]==degrees_b[3] else 0,len(keys[3])):
            other = keys[3][j]
            left,right = pools[2][key],pools[3][other]
            counts = tuple(x+y for x,y in zip(left['counts'],right['counts']))
            pairs = tuple(x+y for x,y in zip(left['pairs'],right['pairs']))
            if any(x>t for x,t in zip(counts,target)) or any(x>cap for x,cap in zip(pairs,caps)):
                continue
            last_pairs.setdefault(counts,[]).append((key,other,pairs))
    results = set()
    for i,key in enumerate(keys[0]):
        for j in range(i if degrees_b[0]==degrees_b[1] else 0,len(keys[1])):
            other = keys[1][j]
            left,right = pools[0][key],pools[1][other]
            counts = tuple(x+y for x,y in zip(left['counts'],right['counts']))
            residual = tuple(t-x for t,x in zip(target,counts))
            if min(residual)<0:
                continue
            pairs = tuple(x+y for x,y in zip(left['pairs'],right['pairs']))
            for key2,key3,other_pairs in last_pairs.get(residual,[]):
                if degrees_b[1]==degrees_b[2] and other>key2:
                    continue
                if any(x+y>cap for x,y,cap in zip(pairs,other_pairs,caps)):
                    continue
                results.add((key,other,key2,key3))
    return results,by_degree


def preflight(cases,roots):
    """Reject malformed tables before any coverage computation; no proof here."""
    require(len(roots)==7,'wrong number of degree placements')
    root_by_profile = {tuple(item['deficits']):item for item in roots}
    require(set(root_by_profile)==set(degree_profiles()),'missing or extra degree placement')
    for profile,item in root_by_profile.items():
        require(all(type(d) is int for d in profile),'invalid deficit types')
        require(item['degree_cycles']==[10-d for d in profile],'root degrees differ')
    required = {(profile,int(code)) for profile,item in root_by_profile.items() for code in item['all_subsets_groups']}
    require(len(cases)==len(required),'incorrect number of incidence root cases')
    require({(tuple(case['deficits']),case['code']) for case in cases}==required,'missing or extra incidence root case')
    for case in cases:
        profile = tuple(case['deficits'])
        require(all(type(d) is int for d in profile) and type(case['code']) is int and 0<=case['code']<4096,
                'incidence identifier types or range')
        require(case['degree_cycles']==[10-d for d in profile],'incidence degree cycles differ')
        require(case['name']==root_by_profile[profile]['name'],'incidence placement name differs')
        recorded = case['incidence_representatives']
        require(all(len(template)==4 and all(len(mask)==3 and all(type(m) is int and 0<=m<8 for m in mask)
                    for mask in template) for template in recorded),'incidence template shape or alphabet')
        keys = [tuple(tuple(mask) for mask in template) for template in recorded]
        require(len(keys)==len(set(keys)),'duplicate incidence template')
        require(case['status']=='COMPLETE' and case['representatives']==len(keys),'incomplete incidence declaration')
    return root_by_profile


def check_incidence_input(cases,roots):
    root_by_profile = preflight(cases,roots)
    coverage = local_coverage()
    require(set(root_by_profile)==set(coverage),'degree composition coverage differs')
    for profile,data in coverage.items():
        recorded = root_by_profile[profile]
        require(recorded['degree_cycles']==[10-d for d in profile],'root degrees differ')
        require(recorded['pair_raw']==data['pair_raw'],'pair-filter local coverage differs')
        require(recorded['all_subsets_groups']=={str(k):v for k,v in data['groups'].items()},
                'local root-word groups differ')
    required = {(profile,code) for profile,data in coverage.items() for code in data['groups']}
    require(len(cases)==len(required),'incorrect number of incidence root cases')
    require({(tuple(case['deficits']),case['code']) for case in cases}==required,'missing or extra incidence root case')
    data = {}
    for case in cases:
        profile = tuple(case['deficits'])
        require(all(type(d) is int and 0<=d<=3 for d in profile),'invalid deficit values')
        full_cycles = tuple(10-d for d in profile)
        require(case['degree_cycles']==list(full_cycles),'incidence degree cycles differ')
        require(case['name']==root_by_profile[profile]['name'],'incidence placement name differs')
        rows = local_graph(case['code'])
        full = [full_cycles[u//3] for u in range(9)]
        generated,pools = join_templates(rows,full,full_cycles[3:])
        recorded = [tuple(tuple(mask) for mask in template) for template in case['incidence_representatives']]
        require(all(len(template)==4 and all(len(mask)==3 and all(type(m) is int and 0<=m<8 for m in mask)
                    for mask in template) for template in recorded),'incidence template shape or alphabet')
        require(len(recorded)==len(set(recorded)),'duplicate incidence template')
        require(set(recorded)==generated,'incidence template coverage differs')
        require(case['status']=='COMPLETE' and case['representatives']==len(generated),'incomplete incidence declaration')
        require(case['domains']=={str(d):len(pool) for d,pool in pools.items()},'incidence domain sizes differ')
        data[profile,case['code']] = (rows,full,pools,recorded)
        print('independent incidence',case['name'],case['code'],len(generated),flush=True)
    return coverage,data


def b_rows(internal,masks):
    rows = [0]*12
    for u,v in POINT_PAIRS_B:
        i,j = u//3,v//3
        red = internal>>i&1 if i==j else masks[PAIRS_B.index((i,j))]>>((v-u)%3)&1
        if red:
            rows[u] |= 1<<v
            rows[v] |= 1<<u
    return tuple(rows)


def outside_signature(rows):
    result = []
    for u,v in POINT_PAIRS_B:
        red = bool(rows[u]>>v&1)
        count = ((rows[u]&rows[v]) if red else (4095^(rows[u]|rows[v]|(1<<u)|(1<<v)))).bit_count()
        result.append((red,count))
    return tuple(result)


def independent_b_graphs(profile,deadline):
    accepted,matched,visits = {},0,0
    for internal in range(16):
        target = [profile[i]-2*(internal>>i&1) for i in range(4)]
        if min(target)<0:
            continue
        def visit(position,remaining,weights):
            nonlocal matched,visits
            visits += 1
            if visits%1024==0 and time.monotonic()>deadline:
                raise TimeoutError('independent B profile budget reached; no exclusion for incomplete profile')
            if position==6:
                if any(remaining):
                    return
                for masks in itertools.product(*(WEIGHT_MASKS[w] for w in weights)):
                    matched += 1
                    rows = b_rows(internal,masks)
                    require(all(row.bit_count()==profile[u//3] for u,row in enumerate(rows)),
                            'independent weighted graph has wrong physical degrees')
                    # Direct predicate on all 66 physical pairs, without producer masks.
                    good = True
                    for u,v in POINT_PAIRS_B:
                        red = bool(rows[u]>>v&1)
                        count = ((rows[u]&rows[v]) if red else (4095^(rows[u]|rows[v]|(1<<u)|(1<<v)))).bit_count()
                        if count>(3 if red else 5):
                            good = False
                            break
                    if good:
                        code = internal+sum(mask<<(4+3*p) for p,mask in enumerate(masks))
                        require(code not in accepted,'duplicate outside graph')
                        accepted[code] = (rows,outside_signature(rows))
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


def prepare_components(local,columns):
    require(len(local)==9 and len(columns)==12,'component dimensions')
    stars = tuple(sum((columns[b]>>a&1)<<b for b in range(12)) for a in range(9))
    a_valid = max(row.bit_count() for row in local)<=3
    for u,v in PAIRS_A:
        if local[u]>>v&1:
            pages = (local[u]&local[v]).bit_count()+(stars[u]&stars[v]).bit_count()+1
            cap = 3
        else:
            pages = (511^(local[u]|local[v]|(1<<u)|(1<<v))).bit_count()
            pages += (4095^(stars[u]|stars[v])).bit_count()
            cap = 6
        if pages>cap:
            a_valid = False
    known_b = tuple(((columns[u]&columns[v]).bit_count(),
                     (511^(columns[u]|columns[v])).bit_count()+1) for u,v in POINT_PAIRS_B)
    return local,columns,stars,a_valid,known_b


def accepts_completion(prepared,bgraph,signature=None):
    local,columns,stars,a_valid,known_b = prepared
    if not a_valid or any(row.bit_count()<5 for row in bgraph):
        return False
    if signature is None:
        signature = outside_signature(bgraph)
    for (red,pages),known in zip(signature,known_b):
        if pages+known[0 if red else 1]>(3 if red else 6):
            return False
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


def run(cases,roots,expected,output,seconds):
    start = time.monotonic()
    coverage,data = check_incidence_input(cases,roots)
    profiles = set()
    for case in cases:
        full_b = case['degree_cycles'][3:]
        for template in case['incidence_representatives']:
            profiles.add(tuple(d-sum(mask.bit_count() for mask in pattern) for d,pattern in zip(full_b,template)))
    all_b,manifests = {},[]
    for profile in sorted(profiles):
        all_b[profile],manifest = independent_b_graphs(profile,time.monotonic()+seconds)
        manifests.append(manifest)
        print('independent B',profile,manifest['degree_matches'],manifest['necessary_page_survivors'],flush=True)
    if expected is not None:
        require(expected['status']=='COMPLETE' and expected['outside_complete'],'producer completion is incomplete')
        require(manifests==expected['outside_profiles'],'outside candidate manifests differ')
    report = dict(status='INCOMPLETE',mathematical_exclusion=False,
                  degree_profiles=[list(p) for p in coverage],
                  local_groups={','.join(map(str,p)):{str(c):words for c,words in v['groups'].items()} for p,v in coverage.items()},
                  incidence_cases=len(cases),incidences=sum(case['representatives'] for case in cases),
                  outside_profiles=manifests,cases=[],valid_completions=0,phase_seconds_budget=seconds)
    for case in cases:
        tag = tuple(case['deficits']),case['code']
        local,full,pools,recorded = data[tag]
        full_b = case['degree_cycles'][3:]
        counts = []
        deadline = time.monotonic()+seconds
        for template in recorded:
            columns = tuple(col for j,key in enumerate(template) for col in pools[full_b[j]][key]['columns'])
            profile = tuple(d-columns[3*j].bit_count() for j,d in enumerate(full_b))
            prepared = prepare_components(local,columns)
            demands,_ = row_data(local,full)
            require(tuple(star.bit_count() for star in prepared[2])==demands and prepared[3],
                    'incidence fails physical A/root spine or degree checks')
            failures = 0
            for bgraph,signature in all_b[profile].values():
                if accepts_completion(prepared,bgraph,signature):
                    report['valid_completions'] += 1
                else:
                    failures += 1
            counts.append(dict(profile=list(profile),tested=len(all_b[profile]),rejected=failures))
            if time.monotonic()>deadline:
                report['reason']='independent root phase budget reached; incomplete root excluded from coverage'
                report['partial_root'] = dict(name=case['name'],code=case['code'],incidences_completed=len(counts))
                output.write_text(json.dumps(report,indent=2)+'\n')
                raise TimeoutError(report['reason'])
        record = dict(name=case['name'],code=case['code'],incidences=len(recorded),
                      completions_tested=sum(x['tested'] for x in counts),
                      completions_rejected=sum(x['rejected'] for x in counts),per_incidence=counts)
        if expected is not None:
            matches = [x for x in expected['cases'] if (x['name'],x['code'])==(case['name'],case['code'])]
            require(len(matches)==1,'missing producer root case')
            primary = matches[0]
            require(primary['status']=='COMPLETE' and primary['incidence_representatives']==len(recorded),
                    'producer root coverage differs')
            require(primary['completions_considered']==record['completions_tested'],
                    'total completion coverage differs')
            require([c['candidates'] for c in primary['per_incidence']]==[c['tested'] for c in counts],
                    'per-incidence completion coverage differs')
        report['cases'].append(record)
        output.write_text(json.dumps(report,indent=2)+'\n')
        print('independent completion',case['name'],case['code'],record['completions_tested'],record['completions_rejected'],flush=True)
    report['status']='EXACT_INDEPENDENT_EXCLUSION' if report['valid_completions']==0 else 'VALID_COMPLETION_FOUND'
    report['mathematical_exclusion']=report['valid_completions']==0
    report['seconds']=time.monotonic()-start
    report['rss_kib']=resource.getrusage(resource.RUSAGE_SELF).ru_maxrss
    output.write_text(json.dumps(report,indent=2)+'\n')
    return report


if __name__=='__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--roots',type=Path,required=True)
    parser.add_argument('--incidences',type=Path,required=True)
    parser.add_argument('--expected',type=Path)
    parser.add_argument('--output',type=Path,required=True)
    parser.add_argument('--seconds',type=int,default=30)
    args = parser.parse_args()
    require(args.seconds>0,'positive phase budget')
    out = run(json.loads(args.incidences.read_text()),json.loads(args.roots.read_text()),
              json.loads(args.expected.read_text()) if args.expected else None,args.output,args.seconds)
    print(out['status'],out['seconds'],'seconds',out['rss_kib'],'RSS KiB',flush=True)
