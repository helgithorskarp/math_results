"""Read all geometric/contact certificates. No solver or producer is imported."""
from copy import deepcopy
import json
from pathlib import Path
import resource
import signal
import time

from exact import (Instance, affine, compose, coronas, enumerate_stars, frame,
                   halo, inverse, matrices, pool, raw_contacts, require, sha, DIRS)

HERE = Path(__file__).absolute().parent
EXPECTED_UPPER = 'cd3d3fb6694022d3e158b126e71cdea0d3261d1a1dec42d26a73856e5ee060d0'


def strip(k):
    cells = {(0,0),(-2*k,k-1),(-2*k-1,k)}
    for r in range(k):
        cells.update((x,y) for x in (-2*r-1,-2*r-2) for y in (r+1,r+2))
    return tuple(sorted(cells))


def must_reject(action):
    try:
        action()
    except ValueError:
        return
    raise ValueError('False or malformed control was accepted')


def check_domain(tile,raw,indices):
    require(indices==sorted(set(indices)) and all(type(i) is int and 0<=i<len(raw) for i in indices),
            'Noncanonical domain indices')
    domain = {raw[i] for i in indices}
    require(all(affine(tile,inverse(frame(tile,t))) in domain for t in domain), 'Nonreciprocal domain')
    return domain


def main():
    start = time.monotonic()
    def timeout(signum,frame):
        raise RuntimeError('45-second reader guard; no completed theorem output')
    signal.signal(signal.SIGALRM,timeout)
    signal.alarm(45)
    try:
        upper = json.loads((HERE/'upper.json').read_text())
        require(sha(upper)==EXPECTED_UPPER, 'Changed completed certificate')
        tile = strip(5)
        require(len(tile)==23 and upper['parameter']==5, 'Wrong family member')
        group = matrices()
        require(len(set(group))==12, 'Wrong motion group')
        for m in group:
            require(set(affine(DIRS,m+(0,0)))==set(DIRS), 'Motion does not preserve grid edges')
            for n in group:
                require(compose(m+(0,0),n+(0,0))[:4] in group, 'Motion group is not closed')
        require(frame(tile,tile)==(1,0,0,1,0,0), 'Unexpected tile symmetry')
        lower = {}
        for filename,final_holes,counts,holes in [
                ('lower-Hc2.json',False,[1,8,19],[0,0,0]),
                ('lower-Hh3.json',True,[1,5,14,28],[0,0,0,27])]:
            d = json.loads((HERE/filename).read_text())
            require(tuple(map(tuple,d['tile']))==tile, 'Wrong witness tile')
            stats = coronas(tile,d['placements'],final_holes)
            require(stats==d['coronas'] and [r['copies'] for r in stats]==counts and
                    [r['hole_cells'] for r in stats]==holes, 'Wrong lower witness statistics')
            lower[filename] = stats
        raw = raw_contacts(tile)
        require(len(raw)==664 and sha(raw)==upper['raw_sha256'], 'Wrong complete contact inventory')
        raw_index = {t:i for i,t in enumerate(raw)}
        root = Instance(tile,tuple(sorted(halo(tile))),raw)
        dag_nodes = 0
        rejected = set(map(int,upper['root_exclusions']))
        require(len(rejected)==317 and rejected<=set(range(len(raw))), 'Wrong forced exclusions')
        for key,proof in upper['root_exclusions'].items():
            dag_nodes += root.reject(proof,int(key))
        support_indices = sorted(set(range(len(raw)))-rejected)
        require(support_indices==upper['root_support'] and len(support_indices)==347, 'Wrong retained root support')
        support = {raw[i] for i in support_indices}
        reciprocal = {i for i in support_indices
                      if raw_index[affine(tile,inverse(frame(tile,raw[i])))] in support_indices}
        require(len(reciprocal)==230, 'Wrong reciprocal initial domain')
        negative = set(map(int,upper['pair1_exclusions']))
        require(len(negative)==64 and negative<=reciprocal, 'Wrong first pair exclusions')
        for key,proof in upper['pair1_exclusions'].items():
            # Directed support at both FIXED centers, packing only among added copies.
            required,tiles = pool(tile,(tile,raw[int(key)]),support)
            dag_nodes += Instance(tile,required,tiles).reject(proof)
        current = sorted(reciprocal-negative)
        require(current==upper['domains']['1'] and len(current)==166, 'Wrong D1')
        domains = {'1':check_domain(tile,raw,current)}
        for r,size in [('2',39),('3',22)]:
            excluded = set(map(int,upper['later_exclusions'][r]))
            require(excluded<=set(current), 'Excluded a contact outside the input domain')
            domain = domains[str(int(r)-1)]
            for key,proof in upper['later_exclusions'][r].items():
                required,tiles = pool(tile,(tile,raw[int(key)]),domain)
                dag_nodes += Instance(tile,required,tiles,domain).reject(proof)
            current = sorted(set(current)-excluded)
            require(current==upper['domains'][r] and len(current)==size, 'Wrong later domain')
            domains[r] = check_domain(tile,raw,current)
        inventories = {}
        inventory_nodes = 0
        for r,expected_count in [('3',3),('2',8)]:
            stars,nodes = enumerate_stars(tile,domains[r])
            inventory_nodes += nodes
            rows = upper['lifted_stars'][r]
            expected = tuple(tuple(raw[i] for i in row['contacts']) for row in rows)
            require(stars==expected and len(stars)==expected_count and
                    [row['case'] for row in rows]==list(range(expected_count)), 'Incomplete root-star inventory')
            inventories[r] = stars
            for row,star in zip(rows,stars):
                placements = [{'level':0,'pose':[1,0,0,1,0,0]}]+[
                    {'level':1,'pose':list(frame(tile,t))} for t in star]
                coronas(tile,placements,False)
                if 'rejection' in row:
                    required,tiles = pool(tile,(tile,)+star,domains[str(int(r)-1)])
                    dag_nodes += Instance(tile,required,tiles,domains[str(int(r)-1)]).reject(row['rejection'])
            require([row['case'] for row in rows if 'rejection' not in row]==([] if r=='3' else [4,5,6]),
                    'Wrong unresolved first stars')
        candidates = tuple(sorted(domains['1']))
        candidate_index = {t:i for i,t in enumerate(candidates)}
        f1 = Instance(tile,tuple(sorted(halo(tile))),candidates,domains['1'])
        excluded_f1 = set(map(int,upper['F1_exclusions']))
        require(len(excluded_f1)==110 and excluded_f1<=set(upper['domains']['1']), 'Wrong F1 exclusions')
        for key,proof in upper['F1_exclusions'].items():
            dag_nodes += f1.reject(proof,candidate_index[raw[int(key)]])
        require(sorted(set(upper['domains']['1'])-excluded_f1)==upper['F1_support'] and
                len(upper['F1_support'])==56, 'Wrong retained F1 support')

        # Independent negative controls cover fingerprint, root, split, branches,
        # packing and the distinction between final-hole and disc witnesses.
        sample = deepcopy(next(iter(upper['root_exclusions'].values())))
        forced = int(next(iter(upper['root_exclusions'])))
        bad = deepcopy(sample);bad['pool_sha256']='0'*64
        must_reject(lambda:root.reject(bad,forced))
        bad = deepcopy(sample);bad['root']=['0x0','0x0']
        must_reject(lambda:root.reject(bad,forced))
        bad = deepcopy(sample);bad['nodes']=[]
        must_reject(lambda:root.reject(bad,forced))
        bad = deepcopy(sample);bad['nodes'][0][2]=len(root.required)
        must_reject(lambda:root.reject(bad,forced))
        tiny = Instance(((0,0),),((0,0),),(((0,0),),))
        false = {'pool_sha256':sha({'required':tiny.required,'tiles':tiny.tiles}),
                 'root':['0x1','0x1'],'nodes':[['0x1','0x1',0]]}
        must_reject(lambda:tiny.reject(false))
        d = json.loads((HERE/'lower-Hc2.json').read_text());bad=deepcopy(d['placements']);bad.append(bad[0])
        must_reject(lambda:coronas(tile,bad,False))
        d = json.loads((HERE/'lower-Hh3.json').read_text())
        must_reject(lambda:coronas(tile,d['placements'],False))
        evidence = {'agent':'six-heesch-2','role':'researcher','complete_contact_stage':True,
                    'scope':'Hh=3 and non-tiling; Hc>=2, remaining three cases need CNF/RUP checks.',
                    'domain_sizes':[664,166,39,22],'root_support':347,'reciprocal':230,'F1_support':56,
                    'root_exclusions':317,'pair_exclusions':[64,127,17],
                    'first_inventories':{'D3':3,'D2':8},'disc_three_remaining_cases':[4,5,6],
                    'rejection_DAG_nodes':dag_nodes,'inventory_nodes':inventory_nodes,
                    'false_malformed_controls':7,'lower':lower,'upper_sha256':sha(upper)}
        print(json.dumps({'evidence':evidence,'evidence_sha256':sha(evidence),
                          'seconds':round(time.monotonic()-start,3),
                          'max_rss_kib':resource.getrusage(resource.RUSAGE_SELF).ru_maxrss},sort_keys=True),flush=True)
    finally:
        signal.alarm(0)


if __name__=='__main__':
    main()
