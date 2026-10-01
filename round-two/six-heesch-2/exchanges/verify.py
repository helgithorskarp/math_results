"""Replay all 4,990 shapes; regenerate and DAG-audit every negative."""
import argparse
from collections import Counter
import hashlib
import json
from pathlib import Path
import resource
import sys
import time

HERE=Path(__file__).resolve().parent
sys.path.insert(0,str(HERE.parent))
from geometry import affine,halo,pose
from family import earlier_family_overlap,grafts
from check_geometry import check_group,edge_contacts,check_coronas
from cover import Cover
from pair_peeling import PairPeeling
from audit import Audit
from periodic import verify as periodic_verify
from exchange_family import generate,independent_generate
from closure import eligible,first_peel
from parity import verify as parity_verify


def digest(value):
    return hashlib.sha256(json.dumps(value,sort_keys=True,separators=(',',':')).encode()).hexdigest()


def classify(i,tile,route,certs):
    if route=='periodic':
        r=certs['periodic'][str(i)]
        witness={'periods':r['periods'],'tiles':[affine(tile,tuple(g)) for g in r['poses']]}
        assert periodic_verify(tile,witness)
        return {'index':i,'status':'periodic','copies':len(witness['tiles'])}
    p=PairPeeling(tile,node_limit=300000,audit=True)
    assert p.raw==edge_contacts(tile)
    root=Cover(halo(tile),p.raw,node_limit=300000,audit=True)
    answer=root.find()
    if route=='root_negative':
        assert answer is None
        return {'index':i,'status':'Hh0'}
    assert answer is not None
    placements=[{'level':0,'pose':[1,0,0,1,0,0]}]
    placements += [{'level':1,'pose':list(pose(tile,root.tiles[j]))} for j in answer]
    check_coronas(tile,placements)
    d=eligible(p,root)
    if route=='eligibility_negative':
        assert p.cover((tile,),d).find() is None
        return {'index':i,'status':'Hh1'}
    e1=first_peel(p,d)
    if route=='pair_one_negative':
        assert p.cover((tile,),e1).find() is None
        return {'index':i,'status':'Hh1'}
    if route=='pair_two_negative':
        assert p.cover((tile,),e1).find() is not None
        e2,_=p.peel(e1);p.check_domain(e2)
        assert p.cover((tile,),e2).find() is None
    elif route=='star_triangle':
        assert i==3598
        assert parity_verify(p,e1)['Hh_upper']==2
        # Verify the claimed limitation of pair closure as well as the bound.
        e2,_=p.peel(e1);p.check_domain(e2)
        e3,_=p.peel(e2);p.check_domain(e3)
        assert len(e1)==11 and len(e2)==10 and e3==e2
        assert p.cover((tile,),e2).find() is not None
    else:raise AssertionError('Unknown verification route')
    if str(i) in certs['two_coronas']:
        stats,_,_=check_coronas(tile,certs['two_coronas'][str(i)])
        assert len(stats)==3
        return {'index':i,'status':'Hh2'}
    return {'index':i,'status':'one_to_two','upper':2}


def run(args):
    if not __debug__:raise RuntimeError('Assertions are required; do not use -O')
    if args.focus and args.checkpoint is not None:
        raise RuntimeError('Use --focus without an operational checkpoint')
    check_group()
    expected=json.loads((HERE/'expected.json').read_text())
    certs=json.loads((HERE/'certificates.json').read_text())
    seed_fixture=json.loads((HERE.parent/'seed.json').read_text())
    seed=tuple(map(tuple,seed_fixture['tile']))
    stats,_,_=check_coronas(seed,seed_fixture['placements'],allow_final_holes=False)
    assert len(stats)==5
    family,raw_count=generate(seed)
    independent,pair_count=independent_generate(seed)
    assert family==independent
    assert (len(family),raw_count,pair_count)==(4990,6080,26236)
    assert digest(family)==expected['family_sha256']
    assert not earlier_family_overlap(family)
    assert len(set(family)&set(grafts(seed)))==26
    routes={}
    for route,indices in expected['routes'].items():
        for i in indices:
            assert i not in routes;routes[i]=route
    assert set(routes)==set(range(len(family)))
    assert set(certs['periodic'])=={str(i) for i in expected['routes']['periodic']}
    assert len(certs['two_coronas'])==2 and '3598' in certs['two_coronas']
    dependencies=['geometry.py','family.py','check_geometry.py','cover.py',
                  'pair_peeling.py','audit.py','periodic.py','seed.json']
    source_files=list(HERE.glob('*.py'))+[HERE.parent/name for name in dependencies]
    source_files += [HERE/'expected.json',HERE/'certificates.json']
    source_digest=digest({str(p.relative_to(HERE.parent)):hashlib.sha256(p.read_bytes()).hexdigest()
                          for p in sorted(source_files)})
    result_rows={};checkpoint=args.checkpoint
    if checkpoint is not None and checkpoint.exists():
        content=checkpoint.read_text();lines=content.splitlines()
        if content and not content.endswith('\n'):
            lines=lines[:-1]
            checkpoint.write_text(''.join(line+'\n' for line in lines))
        for line in lines:
            row=json.loads(line)
            assert row['source_digest']==source_digest
            assert row['expected_digest']==digest(expected)
            r=row['result'];i=r['index']
            assert i not in result_rows and row['tile_sha256']==digest(family[i])
            result_rows[i]=r
    todo=[i for i in range(len(family)) if i not in result_rows]
    if args.focus:todo=[3598]
    if args.stop_after is not None:todo=todo[:args.stop_after]
    start=time.perf_counter()
    for i in todo:
        if args.pause_file is not None and args.pause_file.exists():
            raise RuntimeError('PAUSED barrier: saved completed cases; no full verdict')
        r=classify(i,family[i],routes[i],certs);result_rows[i]=r
        if checkpoint is not None:
            checkpoint.parent.mkdir(parents=True,exist_ok=True)
            with checkpoint.open('a') as f:
                f.write(json.dumps({'source_digest':source_digest,'expected_digest':digest(expected),
                                    'tile_sha256':digest(family[i]),'result':r},separators=(',',':'))+'\n')
        if len(result_rows)%50==0 or args.focus:
            print(json.dumps({'checked':len(result_rows),'last_index':i,
                              'seconds':round(time.perf_counter()-start,3)}),flush=True)
    if args.focus:
        assert result_rows[3598]['status']=='Hh2'
        return {'focus':result_rows[3598],'complete_family':False,'audit':Audit.totals}
    if len(result_rows)!=len(family):
        return {'checked':len(result_rows),'complete_family':False}
    ordered=[result_rows[i] for i in range(len(family))]
    counts=dict(sorted(Counter(r['status'] for r in ordered).items()))
    assert counts==expected['counts']
    assert digest(ordered)==expected['result_sha256']
    return {'agent':'six-heesch-2','role':'researcher','family_size':len(family),
            'family_sha256':digest(family),'result_sha256':digest(ordered),
            'counts':counts,'complete_family':True,'audit_this_process':Audit.totals,
            'checkpoint_loaded_cases':len(family)-len(todo)}


if __name__=='__main__':
    parser=argparse.ArgumentParser()
    parser.add_argument('--focus',action='store_true',help='Only stable-domain Hh2 example; no whole-family claim')
    parser.add_argument('--checkpoint',type=Path,help='Private operational resume file; cached rows are not standalone proof certificates')
    parser.add_argument('--pause-file',type=Path)
    parser.add_argument('--stop-after',type=int)
    args=parser.parse_args();started=time.perf_counter()
    result=run(args)
    result.update(seconds=round(time.perf_counter()-started,3),max_rss_kib=resource.getrusage(resource.RUSAGE_SELF).ru_maxrss)
    print(json.dumps(result,sort_keys=True),flush=True)
