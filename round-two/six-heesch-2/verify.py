"""Replay the complete 26-shape classification and check all finite decisions."""
import argparse,json,hashlib,time,resource
from pathlib import Path
from collections import Counter
from geometry import halo
from family import grafts,earlier_family_overlap
from check_geometry import check_group,edge_contacts,check_coronas
from periodic import verify as verify_periodic
from pair_peeling import PairPeeling
from audit import Audit
from cover import Cover

HERE=Path(__file__).resolve().parent

def digest(value):
    return hashlib.sha256(json.dumps(value,sort_keys=True,separators=(',',':')).encode()).hexdigest()

def run():
    if not __debug__:raise RuntimeError('Verification requires Python assertions; do not use -O')
    check_group()
    seed_input=json.loads((HERE/'seed.json').read_text())
    seed=tuple(map(tuple,seed_input['tile']))
    seed_stats,_,_=check_coronas(seed,seed_input['placements'],allow_final_holes=False)
    assert [r['copies'] for r in seed_stats]==[1,5,11,17,24]
    family=grafts(seed)
    assert len(family)==26 and not earlier_family_overlap(family)
    fixture=json.loads((HERE/'certificates.json').read_text())
    first={r['index']:r for r in fixture['first']}
    two=fixture['two'];assert two['index']==18
    periodic={r['index']:r for r in fixture['periodic']}
    assert len(first)==11 and len(periodic)==9
    lower={}
    for i,r in first.items():
        stats,_,_=check_coronas(family[i],r['placements'])
        assert len(stats)==2
        lower[i]={'depth':1,'holefree':stats[-1]['hole_cells']==0}
    two_stats,two_copies,two_levels=check_coronas(family[18],two['placements'])
    assert len(two_stats)==3 and two_stats[1]['hole_cells']==0
    lower[18]={'depth':2,'holefree':two_stats[-1]['hole_cells']==0}
    for i,r in periodic.items():
        from geometry import affine
        cert={'periods':r['periods'],'tiles':[affine(family[i],tuple(g)) for g in r['poses']]}
        verify_periodic(family[i],cert)
    controls=PairPeeling(((0,0),),audit=True).run(max_rounds=2)
    assert controls['upper'] is None and controls.get('stable') and controls['rows'][-1]['pairs']==6
    # The DAG auditor must reject a fabricated rejected root of a SAT instance.
    c=Cover({(0,0)},[((0,0),)],audit=True)
    c.failed.add((c.all,c.full))
    try:c.audit.certify((c.all,c.full))
    except AssertionError:pass
    else:raise AssertionError('Auditor accepted a fabricated SAT rejection')
    cases=[]
    for i,tile in enumerate(family):
        p=PairPeeling(tile,node_limit=300000,audit=True)
        assert p.raw==edge_contacts(tile),'Two independent contact inventories differ'
        if i in periodic:
            row={'index':i,'status':'periodic','tile_sha256':digest(tile),'period_copies':len(periodic[i]['poses'])}
        else:
            def progress(r):print(json.dumps({'index':i,**r}),flush=True)
            answer=p.run(max_rounds=3,progress=progress)
            upper=answer['upper']
            if upper is None:raise RuntimeError('Incomplete classification: local peeling did not establish a bound')
            assert upper in (0,1,2)
            if upper:
                assert lower[i]['depth']==upper
            row={'index':i,'status':f'Hh{upper}','tile_sha256':digest(tile),'rounds':answer['rows'],
                 'Hc_upper':upper,'Hc_lower':(1 if i==18 else int(lower.get(i,{}).get('holefree',False)))}
        cases.append(row)
    counts=dict(sorted(Counter(c['status'] for c in cases).items()))
    assert counts=={'Hh0':6,'Hh1':10,'Hh2':1,'periodic':9}
    return {'agent':'six-heesch-2','role':'researcher','family_size':len(family),'family_sha256':digest(family),
            'seed_witness':seed_stats,'two_corona_witness':two_stats,'earlier_family_overlap':[],
            'counts':counts,'cases':cases,'audit':Audit.totals,'all_upper_bounds_audited':True,
            'certificate_sha256':hashlib.sha256((HERE/'certificates.json').read_bytes()).hexdigest(),
            'seed_sha256':hashlib.sha256((HERE/'seed.json').read_bytes()).hexdigest()}

if __name__=='__main__':
    parser=argparse.ArgumentParser()
    parser.add_argument('--write-expected',type=Path)
    args=parser.parse_args()
    start=time.perf_counter();result=run()
    if args.write_expected:
        args.write_expected.write_text(json.dumps(result,indent=2)+'\n')
    else:
        expected=json.loads((HERE/'expected.json').read_text())
        assert result==expected,'Replay differs from compact expected evidence'
    print(json.dumps({'counts':result['counts'],'family_sha256':result['family_sha256'],'audit':result['audit'],
                      'all_upper_bounds_audited':True,'seconds':round(time.perf_counter()-start,3),
                      'max_rss_kib':resource.getrusage(resource.RUSAGE_SELF).ru_maxrss},sort_keys=True))
