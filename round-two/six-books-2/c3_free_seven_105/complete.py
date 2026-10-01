"""Exact, resumable 105-edge C3 outside completion exploration.

All decisions are integer predicates. COMPLETE is coverage of the supplied
incidence table; full root/incidence coverage needs a separate checker.
"""
import argparse
import hashlib
import itertools
import json
from pathlib import Path
import resource
import time

from incidence import root_rows,require

PAIRS = tuple(itertools.combinations(range(4),2))
SPINES_B = tuple([(3*i,3*i+1) for i in range(4)]+
                [(3*i,3*j+k) for i,j in PAIRS for k in range(3)])
POPCOUNT = tuple(x.bit_count() for x in range(8))
SPINES_ALL = tuple(itertools.combinations(range(9,21),2))+tuple(
    (a,b) for a in range(9) for b in range(9,21))+tuple(
    itertools.combinations(range(9),2))+tuple((a,21) for a in range(21))
require(len(SPINES_ALL)==231 and len(set(SPINES_ALL))==231,'all spine partition')


def pair_rows(i,j,mask):
    rows = [0]*12
    for t in range(3):
        for k in range(3):
            if mask>>k&1:
                u,v = 3*i+t,3*j+(t+k)%3
                rows[u] |= 1<<v
                rows[v] |= 1<<u
    return tuple(rows)


def outside_graphs(profiles,deadline):
    targets,result = {},{profile:[] for profile in profiles}
    for profile in profiles:
        for internal in range(16):
            sums = tuple(profile[i]-2*(internal>>i&1) for i in range(4))
            targets.setdefault(sums,[]).append((profile,internal))
    table = [[pair_rows(i,j,m) for m in range(8)] for i,j in PAIRS]
    triangles = [tuple(sum(1<<(3*i+s) for s in range(3) if s!=u%3) if u//3==i else 0
                       for u in range(12)) for i in range(4)]
    matched = {profile:0 for profile in profiles}
    cross_count = 0
    for masks in itertools.product(range(8),repeat=6):
        cross_count += 1
        if cross_count%4096==0 and time.monotonic()>deadline:
            return result,matched,cross_count,False
        a,b,c,d,e,f = map(POPCOUNT.__getitem__,masks)
        sums = (a+b+c,a+d+e,b+d+f,c+e+f)
        choices = targets.get(sums)
        if not choices:
            continue
        base = [0]*12
        for p,mask in enumerate(masks):
            for u,component in enumerate(table[p][mask]):
                base[u] |= component
        for profile,internal in choices:
            matched[profile] += 1
            rows = base.copy()
            for i in range(4):
                if internal>>i&1:
                    for u in range(3*i,3*i+3):
                        rows[u] |= triangles[i][u]
            require(tuple(rows[3*i].bit_count() for i in range(4))==profile,'outside degrees')
            good = True
            for u,v in SPINES_B:
                red = bool(rows[u]>>v&1)
                common = rows[u]&rows[v] if red else 4095^((1<<u)|(1<<v)|rows[u]|rows[v])
                if common.bit_count()>(3 if red else 5):
                    good = False
                    break
            if good:
                page_signature = []
                for u,v in SPINES_B:
                    red = bool(rows[u]>>v&1)
                    common = rows[u]&rows[v] if red else 4095^((1<<u)|(1<<v)|rows[u]|rows[v])
                    page_signature.append((red,common.bit_count()))
                result[profile].append(dict(internal=internal,masks=list(masks),rows=rows,
                    code=internal+sum(mask<<(4+3*p) for p,mask in enumerate(masks)),
                    page_signature=page_signature))
    return result,matched,cross_count,True


def base_rows(code,patterns):
    rows = root_rows(code)+[0]*13
    rows[21] = 511
    for a in range(9):
        rows[a] |= 1<<21
    for j,masks in enumerate(patterns):
        for a in range(9):
            for t in range(3):
                if masks[a//3]>>((t-a)%3)&1:
                    b = 9+3*j+t
                    rows[a] |= 1<<b
                    rows[b] |= 1<<a
    return rows


def forced_outside(base,profile,full_b):
    """Necessary red/blue choices from A intersections and B degree floors.

For a B-pair, common-B red neighbors are at least beta_u+beta_v-12
on a red edge and beta_u+beta_v-10 on a blue edge.  Blue spines in
the full graph require total common red neighbors <= d_u+d_v-14.
"""
    columns = [base[b]&511 for b in range(9,21)]
    required,forbidden = 0,0
    for u,v in SPINES_B:
        i,j = u//3,v//3
        bit = i if i==j else 4+3*PAIRS.index((i,j))+(v-u)%3
        common_A = (columns[u]&columns[v]).bit_count()
        red_ok = common_A+max(0,profile[i]+profile[j]-12)<=3
        blue_ok = common_A+max(0,profile[i]+profile[j]-10)<=full_b[i]+full_b[j]-14
        if not red_ok and not blue_ok:
            return None
        if not blue_ok:
            required |= 1<<bit
        if not red_ok:
            forbidden |= 1<<bit
    require(not required&forbidden,'incompatible edge filters')
    return required,forbidden


def bad_spine(rows):
    for u,v in SPINES_ALL:
        red = bool(rows[u]>>v&1)
        common = rows[u]&rows[v] if red else ((1<<22)-1)^((1<<u)|(1<<v)|rows[u]|rows[v])
        if common.bit_count()>(3 if red else 6):
            return u,v,red,common.bit_count()
    return None


def known_outside_pages(base):
    columns = [base[b]&511 for b in range(9,21)]
    return tuple(((columns[u]&columns[v]).bit_count(),
                  (511^(columns[u]|columns[v])).bit_count()+1) for u,v in SPINES_B)


def outside_spine_bad(candidate,known):
    # Each rejection names an actual B-B spine whose pages split as A+B+x.
    # The orbit representatives suffice for this early rejection screen;
    # a candidate surviving it still gets the full 231-spine predicate.
    for (red,pages),counts in zip(candidate['page_signature'],known):
        if pages+counts[0 if red else 1]>(3 if red else 6):
            return True
    return False


def atomic_write(path,report):
    path.parent.mkdir(parents=True,exist_ok=True)
    temporary = path.with_suffix('.tmp')
    temporary.write_text(json.dumps(report,indent=2)+'\n')
    temporary.replace(path)


def run(cases,output,seconds):
    start = time.monotonic()
    require(all(case['status']=='COMPLETE' for case in cases),'incomplete input incidence table')
    profiles = set()
    for case in cases:
        full_b = case['degree_cycles'][3:]
        for patterns in case['incidence_representatives']:
            profiles.add(tuple(d-sum(m.bit_count() for m in pattern) for d,pattern in zip(full_b,patterns)))
    graphs,matched,coverage,complete = outside_graphs(sorted(profiles),time.monotonic()+seconds)
    manifests = [dict(degrees=list(profile),degree_matches=matched[profile],
                     necessary_page_survivors=len(graphs[profile]),candidate_sha256=hashlib.sha256(
                     ''.join(str(candidate['code'])+'\n' for candidate in sorted(graphs[profile],key=lambda c:c['code'])).encode()).hexdigest())
                 for profile in sorted(profiles)]
    print(json.dumps(dict(outside_complete=complete,cross_assignments=coverage,
                         profiles=len(profiles),outside_candidates=sum(len(g) for g in graphs.values()))),flush=True)
    previous = json.loads(output.read_text()) if output.exists() else None
    if previous:
        require(previous['outside_profiles']==manifests and previous['cross_assignments']==coverage,
                'resumption outside graph coverage differs')
        require(sum(case['status']!='COMPLETE' for case in previous['cases'])<=1,
                'multiple incomplete roots in checkpoint')
        report = previous
    else:
        report = dict(status='INCOMPLETE',outside_complete=complete,cross_assignments=coverage,
                      expected_cross_assignments=8**6,outside_profiles=manifests,
                      cases=[],valid_completions=[],phase_seconds_budget=seconds)
    if not complete:
        atomic_write(output,report)
        return report
    done = {(item['name'],item['code']) for item in report['cases'] if item['status']=='COMPLETE'}
    for case in cases:
        tag = case['name'],case['code']
        if tag in done:
            continue
        full_b = case['degree_cycles'][3:]
        expected_A = [case['degree_cycles'][u//3] for u in range(9)]
        deadline = time.monotonic()+seconds
        counts,digest,case_complete = [],hashlib.sha256(),True
        partial = [item for item in report['cases'] if (item['name'],item['code'])==tag]
        require(len(partial)<=1,'duplicate checkpoint root')
        prefix = partial[0]['per_incidence'] if partial else []
        if partial:
            require(partial[0]['incidence_representatives']==len(case['incidence_representatives']) and
                    partial[0]['incidences_completed']==len(prefix),'partial incidence checkpoint shape')
            report['cases'].remove(partial[0])
        for position,patterns in enumerate(case['incidence_representatives']):
            if time.monotonic()>deadline:
                case_complete = False
                break
            profile = tuple(d-sum(m.bit_count() for m in pattern) for d,pattern in zip(full_b,patterns))
            base = base_rows(case['code'],patterns)
            require([r.bit_count() for r in base[:9]]==expected_A and base[21].bit_count()==9,
                    'root-side incidence degree')
            forcing = forced_outside(base,profile,full_b)
            if position<len(prefix):
                count = prefix[position]
                require(count['profile']==list(profile) and count['candidates']==len(graphs[profile]) and
                        count['forcing']==(list(forcing) if forcing is not None else None),
                        'checkpoint incidence parameters differ')
                require(count['forced_rejected']+count['tested']==count['candidates'] and
                        count['rejected']==count['tested'],'checkpoint lacks completed rejection coverage')
                counts.append(count)
                digest.update(json.dumps([patterns,count],separators=(',',':')).encode()+b'\n')
                continue
            known = known_outside_pages(base)
            tested,rejected,forced_rejected = 0,0,0
            for candidate in graphs[profile]:
                if forcing is None or candidate['code']&forcing[0]!=forcing[0] or candidate['code']&forcing[1]:
                    forced_rejected += 1
                    continue
                tested += 1
                if outside_spine_bad(candidate,known):
                    rejected += 1
                    continue
                rows = base.copy()
                for u in range(12):
                    rows[u+9] |= candidate['rows'][u]<<9
                require(sum(r.bit_count() for r in rows)==210,'completed edge count')
                require([rows[9+3*i].bit_count() for i in range(4)]==full_b,'outside full degrees')
                failure = bad_spine(rows)
                if failure is None:
                    report['valid_completions'].append(dict(name=case['name'],code=case['code'],
                        patterns=patterns,candidate=candidate,rows=rows))
                else:
                    rejected += 1
            count = dict(profile=list(profile),candidates=len(graphs[profile]),
                         forcing=list(forcing) if forcing is not None else None,
                         forced_rejected=forced_rejected,tested=tested,rejected=rejected)
            counts.append(count)
            digest.update(json.dumps([patterns,count],separators=(',',':')).encode()+b'\n')
        record = dict(name=case['name'],code=case['code'],status='COMPLETE' if case_complete else 'INCOMPLETE',
                      incidence_representatives=len(case['incidence_representatives']),
                      incidences_completed=len(counts),completions_considered=sum(x['candidates'] for x in counts),
                      forced_rejected=sum(x['forced_rejected'] for x in counts),
                      completions_tested=sum(x['tested'] for x in counts),
                      completions_rejected=sum(x['rejected'] for x in counts),
                      per_incidence=counts,completion_sha256=digest.hexdigest())
        report['cases'].append(record)
        report['seconds'] = time.monotonic()-start
        report['rss_kib'] = resource.getrusage(resource.RUSAGE_SELF).ru_maxrss
        atomic_write(output,report)
        print(json.dumps({k:v for k,v in record.items() if k!='per_incidence'}),flush=True)
        if not case_complete:
            return report
    require({(case['name'],case['code']) for case in report['cases']}=={(case['name'],case['code']) for case in cases},
            'completed root cases differ')
    report['status']='COMPLETE'
    atomic_write(output,report)
    return report


if __name__=='__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--incidences',type=Path,required=True)
    parser.add_argument('--output',type=Path,required=True)
    parser.add_argument('--seconds',type=int,default=30)
    args = parser.parse_args()
    require(args.seconds>0,'positive phase budget')
    result = run(json.loads(args.incidences.read_text()),args.output,args.seconds)
    print('status',result['status'],'valid_completions',len(result['valid_completions']),flush=True)
    if result['status']!='COMPLETE':
        raise SystemExit(75)
