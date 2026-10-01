"""Solver-free reader of T4's exact all-motion Hc=Hh=3 certificate."""
from copy import deepcopy
import json
from pathlib import Path
import resource
import signal
import sys
import time

from lazy import Instance, enumerate_stars, pool, sha
from geometry import affine, canonical, contacts, halo, inverse, pose, matrices
from check_geometry import check_coronas, check_group, edge_contacts
from pair_peeling import PairPeeling
from cover import Cover, Incomplete

HERE=Path(__file__).resolve().parent


def strip(k):
    cells={(0,0),(-2*k,k-1),(-2*k-1,k)}
    for r in range(k):cells.update((x,y) for x in (-2*r-1,-2*r-2) for y in (r+1,r+2))
    return tuple(sorted(cells))


def must_reject(action):
    try:action()
    except (ValueError,AssertionError):return
    raise AssertionError('A false or malformed control was accepted')


def main():
    if not __debug__:raise RuntimeError('The proof reader requires Python assertions')
    start=time.monotonic();nodes=0
    def timeout(signum,frame):raise Incomplete('Reader45-second guard; no completed theorem output')
    signal.signal(signal.SIGALRM,timeout);signal.alarm(45)
    try:
        upper=json.loads((HERE/'upper.json').read_text());lower=json.loads((HERE/'lower.json').read_text())
        control=json.loads((HERE/'control15.json').read_text());tile=strip(4)
        check_group();assert len(tile)==19 and tuple(map(tuple,lower['tile']))==tile
        lower_stats,_,_=check_coronas(tile,lower['placements'],False)
        assert [r['copies'] for r in lower_stats]==[1,5,12,21]
        assert lower_stats==lower['coronas']
        control_tile=tuple(map(tuple,control['tile']))
        assert canonical(strip(3))==canonical(control_tile)
        control_stats,_,_=check_coronas(control_tile,control['placements'],False)
        assert [r['copies'] for r in control_stats]==[1,6,13,21,35]
        p=PairPeeling(tile,node_limit=100000,audit=True);raw=tuple(sorted(p.raw))
        assert set(raw)==edge_contacts(tile) and len(raw)==568 and sha(raw)==upper['raw_sha256']
        raw_index={t:i for i,t in enumerate(raw)}
        first_exclusions=upper['first_exclusions']
        assert len(first_exclusions)==len(set(first_exclusions))==243
        first=Cover(halo(tile),raw,node_limit=100000,audit=True)
        for i in first_exclusions:assert first.find(i) is None
        nodes+=first.nodes
        reciprocal={i for i in range(len(raw)) if i not in first_exclusions and
                    raw_index[affine(tile,inverse(pose(tile,raw[i])))] not in first_exclusions}
        assert len(reciprocal)==upper['first_reciprocal_contacts']==240
        p.check_domain({raw[i] for i in reciprocal})
        r1=upper['round1_exclusions'];assert len(r1)==len(set(r1))==50 and set(r1)<=reciprocal
        for i in r1:
            p.node_limit=max(1,100000-nodes);case=p.cover((tile,raw[i]),p.raw)
            assert case.find() is None;nodes+=case.nodes
            if nodes>100000:raise Incomplete('Reader node guard')
        current=reciprocal-set(r1)
        assert sorted(current)==upper['domains']['1'] and len(current)==190
        counts=[len(raw),len(current)];dag_nodes=0;negative_late=0
        for r in (2,3):
            domain={raw[i] for i in current};p.check_domain(domain)
            rows=upper['later_exclusions'][str(r)];excluded=set(map(int,rows))
            assert excluded<=current
            for key,certificate in rows.items():
                required,tiles=pool(tile,(tile,raw[int(key)]),domain)
                dag_nodes+=Instance(tile,required,tiles,domain).reject(certificate);negative_late+=1
            current-=excluded
            assert sorted(current)==upper['domains'][str(r)]
            p.check_domain({raw[i] for i in current});counts.append(len(current))
        assert counts==[568,190,43,29]
        domain3={raw[i] for i in current};domain2={raw[i] for i in upper['domains']['2']}
        inventory,inventory_nodes=enumerate_stars(tile,domain3)
        expected={tuple(sorted(raw[i] for i in row['contacts'])) for row in upper['root_stars']}
        assert inventory==expected and len(expected)==17 and len(upper['root_stars'])==17
        stable=json.loads((HERE/'stable.json').read_text())
        assert {row['contact'] for row in stable}==current and len(stable)==29
        for row in stable:
            fixed=(tile,raw[row['contact']]);local=list(fixed)
            for record in row['neighbors']:
                g=tuple(record)
                assert len(g)==6 and all(type(v) is int for v in g) and g[:4] in matrices()
                local.append(affine(tile,g))
            occupied=set()
            for t in local:assert occupied.isdisjoint(t);occupied.update(t)
            assert halo(set().union(*(set(t) for t in fixed)))<=occupied
            for i,t in enumerate(local):
                g=inverse(pose(tile,t));boundary=halo(t)
                for u in local[:i]:
                    if set(u)&boundary:assert affine(u,g) in domain3
        for row in upper['root_stars']:
            fixed=(tile,)+tuple(raw[i] for i in row['contacts'])
            required,tiles=pool(tile,fixed,domain2)
            dag_nodes+=Instance(tile,required,tiles,domain2).reject(row['second_rejection']);negative_late+=1
        example=upper['later_exclusions']['2'][next(iter(upper['later_exclusions']['2']))]
        i=int(next(iter(upper['later_exclusions']['2'])));d={raw[j] for j in upper['domains']['1']}
        required,tiles=pool(tile,(tile,raw[i]),d);instance=Instance(tile,required,tiles,d)
        bad=deepcopy(example);bad['pool_sha256']='0'*64;must_reject(lambda:instance.reject(bad))
        bad=deepcopy(example);bad['nodes']=[];must_reject(lambda:instance.reject(bad))
        bad=deepcopy(example);bad['nodes'][0][2]=len(required);must_reject(lambda:instance.reject(bad))
        tiny=Instance(((0,0),),((0,0),),(((0,0),),),set())
        false={'pool_sha256':sha({'required':tiny.required,'tiles':tiny.tiles}),'root':['0x1','0x1'],'nodes':[['0x1','0x1',0]]}
        must_reject(lambda:tiny.reject(false))
        result={'agent':'six-heesch-2','role':'researcher','claim':'Hc(T4)=Hh(T4)=3, with all Euclidean motions and reflections.',
                'domain_sizes':counts,'root_stars':len(inventory),'lifted_rejections':17,'fixed_point_pair_witnesses':29,
                'regenerated_first_exclusions':243,'regenerated_pair_exclusions':50,
                'lazy_negative_certificates':negative_late,'lazy_DAG_nodes':dag_nodes,
                'independent_inventory_nodes':inventory_nodes,'search_nodes':nodes,'false_malformed_controls':4,
                'lower_coronas':lower_stats,'known_T3_four_coronas':control_stats,
                'upper_sha256':sha(upper),'seconds':round(time.monotonic()-start,3),
                'max_rss_kib':resource.getrusage(resource.RUSAGE_SELF).ru_maxrss,'complete':True}
        print(json.dumps(result,sort_keys=True),flush=True)
    finally:signal.alarm(0)


if __name__=='__main__':main()
