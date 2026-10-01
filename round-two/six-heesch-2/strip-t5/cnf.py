"""Reconstruct one necessary three-disc CNF, check its cuts, and replay RUP.

No SAT solver is used. The original producer's bitset conflict matrices,
candidate indices and CNF are not inputs. This reader rebuilds candidate
footprints, set-based incompatibilities, coverage and all auxiliary clauses.
"""
import argparse
from collections import defaultdict
from copy import deepcopy
import hashlib
import json
import math
from pathlib import Path
import resource
import signal
import subprocess
import time

from exact import (Instance, affine, component, compose, coronas, frame, halo,
                   inverse, pool, raw_contacts, require, sha, touching)
from verify import EXPECTED_UPPER, strip, must_reject

HERE = Path(__file__).absolute().parent


def validate_cut(cut,occupied,footprints,nsecond,incidence):
    require(cut['phase'] in ('second','third'), 'Unknown topological prefix')
    limit = nsecond if cut['phase']=='second' else len(footprints)
    wall = cut['boundary']
    require(wall and len(wall)==len(set(wall)) and
            all(type(v) is int and 1<=v<=limit for v in wall), 'Invalid wall indices')
    hole = {tuple(q) for q in cut['hole']}
    point = tuple(cut['point'])
    require(len(hole)==len(cut['hole']) and point in hole and
            component(hole,point)==hole, 'Invalid finite hole component')
    region = occupied.union(*(set(footprints[v-1]) for v in wall))
    require(hole.isdisjoint(region), 'Wall meets the certified empty component')
    require(halo(hole)<=region, 'Wall fails to seal the component')
    boundary = halo(hole)
    require(all(not boundary.isdisjoint(footprints[v-1]) for v in wall), 'Irrelevant wall copy')
    fillers = [v for v in incidence.get(point,[]) if v<=limit]
    expected = [-v for v in wall]+fillers
    require(cut['clause']==expected, 'Cut does not include exactly all permitted fillers')
    return expected


def reconstruct(case,destination):
    upper = json.loads((HERE/'upper.json').read_text())
    require(sha(upper)==EXPECTED_UPPER, 'Changed completed contact certificate')
    tile = strip(5)
    raw = raw_contacts(tile)
    require(sha(raw)==upper['raw_sha256'] and len(raw)==664, 'Wrong raw contact universe')
    domain = {raw[i] for i in upper['domains']['1']}
    f1 = {raw[i] for i in upper['F1_support']}
    f0 = {raw[i] for i in upper['root_support']}
    record = json.loads((HERE/f'case-{case}.json').read_text())
    require(record['case']==case, 'Wrong SAT case')
    star = upper['lifted_stars']['2'][case]
    require(star['case']==case and 'rejection' not in star, 'Case is not a remaining first star')
    fixed = (tile,)+tuple(raw[i] for i in star['contacts'])
    expected_first = [{'level':0,'pose':[1,0,0,1,0,0]}]+[
        {'level':1,'pose':list(frame(tile,t))} for t in fixed[1:]]
    require(record['fixed_first']==expected_first, 'CNF first prefix differs from the complete inventory')
    coronas(tile,expected_first,False)
    occupied = set().union(*(set(t) for t in fixed))
    old_halo = halo(occupied)
    needed,second_before = pool(tile,fixed,domain)
    require(set(needed)==old_halo, 'Wrong protected halo')
    _,second = pool(tile,fixed,f1)
    # Equivalent to filtering the full D1 pool, but built directly from outgoing F1.
    transported = {t:{affine(u,frame(tile,t)) for u in f1} for t in fixed}
    filtered = tuple(u for u in second_before
                     if all(not touching(u,t) or u in transported[t] for t in fixed))
    require(second==filtered, 'Directed support pool lost or added a second candidate')
    second_poses = [frame(tile,t) for t in second]
    raw_poses = [frame(tile,t) for t in f0]
    parent_sets = defaultdict(set)
    for i,g in enumerate(second_poses):
        for h in raw_poses:
            parent_sets[compose(g,h)].add(i)
    thirds,parents = [],[]
    for g,indices in sorted(parent_sets.items()):
        t = affine(tile,g)
        if occupied.isdisjoint(t) and old_halo.isdisjoint(t):
            thirds.append(t)
            parents.append(sorted(indices))
    footprints = list(second)+thirds
    nsecond = len(second)
    require(nsecond==record['second_candidates'] and len(thirds)==record['third_candidates'],
            'Wrong complete candidate inventory')
    incidence = defaultdict(list)
    for i,t in enumerate(footprints,1):
        for q in t:
            incidence[q].append(i)
    cuts = [validate_cut(c,occupied,footprints,nsecond,incidence) for c in record['cuts']]
    require(len(cuts)==(2 if case==6 else 0) and
            all(c['phase']=='third' for c in record['cuts']), 'Unexpected topology cuts')
    # Audit the topological trust boundary independently of RUP or the CNF hash.
    cut_controls = 0
    if cuts:
        for mutate in ('unsealed','wrong_filler','outside_point'):
            bad = deepcopy(record['cuts'][0])
            if mutate=='unsealed': bad['boundary']=[]
            if mutate=='wrong_filler': bad['clause']=bad['clause'][:-1]
            if mutate=='outside_point': bad['point']=[10000,10000]
            must_reject(lambda:validate_cut(bad,occupied,footprints,nsecond,incidence))
            cut_controls += 1

    variables = len(footprints)
    clauses = 0
    digest = hashlib.sha256()
    destination.parent.mkdir(parents=True,exist_ok=True)
    with destination.open('wb') as stream:
        def write(data):
            stream.write(data)
            digest.update(data)
        write(f"p cnf {record['variables']} {record['clauses']}\n".encode())
        def clause(literals):
            nonlocal clauses
            require(all(type(v) is int and v!=0 for v in literals), 'Invalid CNF literal')
            clauses += 1
            require(clauses<=900000 and variables<=300000, 'Instance-size guard')
            write((' '.join(map(str,literals))+' 0\n').encode())
        def sequential_amo(row):
            nonlocal variables
            if len(row)<2:
                return
            if len(row)==2:
                clause([-row[0],-row[1]])
                return
            chain = list(range(variables+1,variables+len(row)))
            variables += len(chain)
            for k,x in enumerate(row[:-1]):
                clause([-x,chain[k]])
                if k:
                    clause([-chain[k-1],chain[k]])
                    clause([-x,-chain[k-1]])
            clause([-row[-1],-chain[-1]])
        def product_amo(row):
            nonlocal variables
            if len(row)<36:
                sequential_amo(row)
                return
            columns = math.isqrt(len(row)-1)+1
            rows = (len(row)+columns-1)//columns
            row_vars = list(range(variables+1,variables+rows+1))
            variables += rows
            col_vars = list(range(variables+1,variables+columns+1))
            variables += columns
            for rank,x in enumerate(row):
                clause([-x,row_vars[rank//columns]])
                clause([-x,col_vars[rank%columns]])
            sequential_amo(row_vars)
            sequential_amo(col_vars)
        for q in sorted(incidence):
            product_amo(incidence[q])
        packing = Instance(tile,needed,second,domain)
        for i in range(nsecond):
            for j in range(i):
                if packing.incompatible(i,j):
                    clause([-(i+1),-(j+1)])
        for q in sorted(old_halo):
            clause([v for v in incidence[q] if v<=nsecond])
        for i,t in enumerate(second):
            for q in sorted(halo(t)-occupied):
                clause([-(i+1)]+incidence[q])
        for j,indices in enumerate(parents):
            clause([-(nsecond+j+1)]+[i+1 for i in indices])
        for cut in cuts:
            clause(cut)
    require(variables==record['variables'] and clauses==record['clauses'], 'Wrong complete CNF dimensions')
    require(digest.hexdigest()==record['cnf_sha256'], 'Reconstructed CNF differs from the checked frozen CNF')
    core = HERE/f'case-{case}.rup'
    require(hashlib.sha256(core.read_bytes()).hexdigest()==record['core_sha256'] and
            len(core.read_bytes().splitlines())==record['core_additions'], 'Changed compact RUP core')
    return record,{'case':case,'second':nsecond,'third':len(thirds),'variables':variables,
                   'clauses':clauses,'cnf_sha256':digest.hexdigest(),'core_sha256':record['core_sha256'],
                   'core_additions':record['core_additions'],'topology_cuts':len(cuts),
                   'malformed_cut_controls':cut_controls}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('case',type=int,choices=(4,5,6))
    parser.add_argument('--output',type=Path,required=True,help='Generated CNF path outside published source')
    parser.add_argument('--rup-audit',type=Path,required=True,help='Compiled solver-free rup_audit.cpp executable')
    args = parser.parse_args()
    start = time.monotonic()
    def timeout(signum,frame):
        raise RuntimeError('45-second reconstruction guard; no completed contradiction output')
    signal.signal(signal.SIGALRM,timeout)
    signal.alarm(45)
    try:
        record,evidence = reconstruct(args.case,args.output)
        replayed = args.output.with_suffix('.replayed.rup')
        run = subprocess.run([str(args.rup_audit.absolute()),str(args.output.absolute()),
                              str(HERE/f'case-{args.case}.rup'),str(replayed.absolute())],
                             text=True,capture_output=True,timeout=max(1,43-(time.monotonic()-start)))
        require(run.returncode==0, 'RUP checker failed: '+run.stdout+run.stderr)
        result = json.loads(run.stdout)
        require(result['complete'] and result['checked_additions']==record['core_additions'] and
                result['input_variables']==record['variables'] and result['input_clauses']==record['clauses'],
                'RUP replay did not certify the expected contradiction')
        evidence.update(complete_CNF_RUP_stage=True,rup={k:v for k,v in result.items()
                                                       if k not in ('seconds','max_rss_kib')})
        print(json.dumps({'evidence':evidence,'evidence_sha256':sha(evidence),
                          'rup_seconds':result['seconds'],'rup_max_rss_kib':result['max_rss_kib'],
                          'seconds':round(time.monotonic()-start,3),
                          'max_rss_kib':resource.getrusage(resource.RUSAGE_SELF).ru_maxrss},sort_keys=True),flush=True)
    finally:
        signal.alarm(0)


if __name__=='__main__':
    main()
