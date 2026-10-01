"""Complete degree-marked C3 root/outside incidence enumeration, bounded per root."""
import argparse
import itertools
import json
from pathlib import Path
import resource
import time

PAIR_A = tuple(itertools.combinations(range(9),2))


def require(value,message):
    if not value:
        raise RuntimeError(message)


def root_rows(code):
    rows = [0]*9
    for u,v in PAIR_A:
        i,j = u//3,v//3
        bit = i if i==j else 3+3*((0,1),(0,2),(1,2)).index((i,j))+(v-u)%3
        if code>>bit&1:
            rows[u] |= 1<<v
            rows[v] |= 1<<u
    return rows


def rotate(mask,shift):
    return sum(((mask>>t)&1)<<((t+shift)%3) for t in range(3))


def domains(rows,full,outside_degree):
    demands = [full[u]-1-rows[u].bit_count() for u in range(9)]
    caps = [(2 if rows[u]>>v&1 else full[u]+full[v]-15)-(rows[u]&rows[v]).bit_count()
            for u,v in PAIR_A]
    result = []
    for masks in itertools.product(range(8),repeat=3):
        if masks != min(tuple(rotate(m,s) for m in masks) for s in range(3)):
            continue
        counts = tuple(m.bit_count() for m in masks)
        q = sum(counts)
        beta = outside_degree-q
        if beta<5:
            continue
        columns = tuple(sum(((masks[a//3]>>((b-a)%3))&1)<<a for a in range(9)) for b in range(3))
        good = True
        for column in columns:
            for a in range(9):
                known = (rows[a]&column).bit_count()
                red = bool(column>>a&1)
                lower = max(0,demands[a]+beta-(12 if red else 11))
                bound = 3 if red else full[a]+outside_degree-14
                if known+lower>bound:
                    good = False
                    break
            if not good:
                break
        if not good:
            continue
        contributions = tuple(sum((column>>u&1) and (column>>v&1) for column in columns) for u,v in PAIR_A)
        if any(x>cap for x,cap in zip(contributions,caps)):
            continue
        result.append(dict(masks=list(masks),counts=counts,pairs=contributions))
    return result,tuple(demands[3*i] for i in range(3)),tuple(caps)


def enumerate_incidences(root_case,code,deadline):
    degree_cycles = root_case['degree_cycles']
    rows = root_rows(code)
    full = [degree_cycles[u//3] for u in range(9)]
    outside_degrees = degree_cycles[3:]
    domain_sets = {degree:domains(rows,full,degree) for degree in sorted(set(outside_degrees))}
    pools = [domain_sets[d][0] for d in outside_degrees]
    demands,caps = domain_sets[outside_degrees[0]][1:]
    final_by_counts = {}
    for key,pattern in enumerate(pools[3]):
        final_by_counts.setdefault(pattern['counts'],[]).append(key)
    visits,records,complete = 0,[],True

    def visit(position,lower_index,counts,pairs,chosen):
        nonlocal visits,complete
        visits += 1
        if visits%1024==0 and time.monotonic()>deadline:
            complete = False
            return
        if position==4:
            if counts==demands:
                records.append([pools[j][key]['masks'] for j,key in enumerate(chosen)])
            return
        remaining = 3-position
        if position==3:
            residual = tuple(target-x for target,x in zip(demands,counts))
            keys = (key for key in final_by_counts.get(residual,()) if key>=lower_index)
        else:
            keys = range(lower_index,len(pools[position]))
        for key in keys:
            pattern = pools[position][key]
            next_counts = tuple(x+y for x,y in zip(counts,pattern['counts']))
            if any(x>target or x+3*remaining<target for x,target in zip(next_counts,demands)):
                continue
            next_pairs = []
            for x,y,cap in zip(pairs,pattern['pairs'],caps):
                value = x+y
                if value>cap:
                    break
                next_pairs.append(value)
            if len(next_pairs)!=len(caps):
                continue
            next_lower = key if position<3 and outside_degrees[position]==outside_degrees[position+1] else 0
            visit(position+1,next_lower,next_counts,tuple(next_pairs),chosen+[key])
            if not complete:
                return

    visit(0,0,(0,0,0),(0,)*len(PAIR_A),[])
    return dict(name=root_case['name'],code=code,degree_cycles=degree_cycles,
                deficits=root_case['deficits'],status='COMPLETE' if complete else 'INCOMPLETE',
                domains={str(d):len(data[0]) for d,data in domain_sets.items()},
                nodes=visits,row_demands=list(demands),incidence_representatives=records,
                representatives=len(records),outside_completion_claim=False)


if __name__=='__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--roots',type=Path,required=True)
    parser.add_argument('--output',type=Path,required=True)
    parser.add_argument('--seconds',type=int,default=30)
    parser.add_argument('--resume-incomplete',action='store_true',
                        help='retain completed roots, archive and redo only an interrupted root')
    args = parser.parse_args()
    require(args.seconds>0,'positive phase budget required')
    roots = json.loads(args.roots.read_text())
    finished = json.loads(args.output.read_text()) if args.output.exists() else []
    interrupted = [item for item in finished if item['status']!='COMPLETE']
    if interrupted:
        require(args.resume_incomplete,'cannot resume an incomplete root without explicit intervention')
        require(len(interrupted)==1,'multiple incomplete roots in checkpoint')
        archive = args.output.with_name(args.output.stem+'.interrupted.json')
        require(not archive.exists(),'interrupted-root archive already exists; inspect before another retry')
        archive.write_text(json.dumps(interrupted,indent=2)+'\n')
        finished = [item for item in finished if item['status']=='COMPLETE']
    done = {(item['name'],item['code']) for item in finished}
    start = time.monotonic()
    for case in roots:
        for code in sorted(map(int,case['all_subsets_groups'])):
            if (case['name'],code) in done:
                continue
            record = enumerate_incidences(case,code,time.monotonic()+args.seconds)
            if interrupted and (record['name'],record['code'])==(interrupted[0]['name'],interrupted[0]['code']):
                prefix = interrupted[0]['incidence_representatives']
                require(record['incidence_representatives'][:len(prefix)]==prefix,'interrupted template prefix differs')
            finished.append(record)
            args.output.parent.mkdir(parents=True,exist_ok=True)
            temporary = args.output.with_suffix('.tmp')
            temporary.write_text(json.dumps(finished,indent=2)+'\n')
            temporary.replace(args.output)
            print(json.dumps({k:v for k,v in record.items() if k!='incidence_representatives'}),flush=True)
            if record['status']!='COMPLETE':
                print('Operational budget reached; no exclusion for the incomplete root.',flush=True)
                raise SystemExit(75)
    print('seconds',time.monotonic()-start,'RSS KiB',resource.getrusage(resource.RUSAGE_SELF).ru_maxrss,flush=True)
