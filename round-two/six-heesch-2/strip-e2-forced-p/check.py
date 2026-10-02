"""Search-free check of all exclusions, every supplier and its transport."""
from copy import deepcopy
from datetime import datetime,timezone
import json
from pathlib import Path
import resource
import signal
import time

import deps
import reader as V
import strip_contact_reader as R
import strip_parametric_geometry as G
from strip_columns import require
from strip_point_suppliers import IDENTITY
import supplier_trees as T

HERE=Path(__file__).absolute().parent
SHIFT=((1,0,0,1),(0,6),(-1,4))
HALFTURN=((-1,0,0,-1),(0,5),(0,3))
S=((-1,0,-1,1),(0,7),(0,5))
P=((2,-3,1,-2),(3,6),(2,5))
EXPECTED=((-1,3,0,1),(-3,2),(0,2)),((1,-3,0,-1),(0,0),(1,1)),((1,0,1,-1),(0,-4),(1,-2)),None
DEMANDS=(((0,3),(1,2)),((0,-2),(1,0)),((0,-3),(1,-2)),((0,1),(0,0)))


def bind(record,entry):
    require(record['case']==entry['name'] and record['method']==entry['method']
            and R.freeze(record['fixed'])==(IDENTITY,R.freeze(entry['pose']))
            and R.freeze(record['points'])==R.freeze(entry['points']),'Changed literal case binding')


def exclusion(record,entry,guard,material=True):
    bind(record,entry);fixed=R.freeze(record['fixed'])
    V.universal([G.neg(G.intersection(G.relative(*fixed))),G.touching(G.relative(*fixed))],guard)
    if entry['method']=='tree':return T.check(record,entry,guard,material)
    result=R.local_check(record,guard,material);result.update(case=entry['name'],record_sha256=R.sha(record))
    return result


def check_chain(record,entries,guard,material=True):
    require(record['complete'] and len(record['stages'])==4,'Missing complete forced-chain stage')
    names={e['name']:e for e in entries};models=tuple(R.freeze(e['pose']) for e in entries)
    fixed=(IDENTITY,SHIFT,HALFTURN,S);evidence=[]
    for number,saved in enumerate(record['stages']):
        point=DEMANDS[number];chosen=EXPECTED[number]
        require(R.freeze(saved['fixed'])==fixed and R.freeze(saved['point'])==point
                and R.freeze(saved['expected'])==chosen,'Changed literal forced chain')
        geometry=V.universal([V.in_halo(point,fixed[:2]),
                              *[G.neg(G.point_membership(f,point)) for f in fixed],
                              *[G.neg(G.intersection(G.relative(f,h))) for i,h in enumerate(fixed) for f in fixed[:i]]],guard)
        fresh=R.supplier_atlas(point,fixed,guard)
        require(R.freeze(fresh)==R.freeze(saved['supplier_record']),'Changed complete chain supplier reduction')
        if material:V.material(point,fixed,fresh,guard)
        atlas=R.freeze(fresh['atlas']);mappings=saved['mappings']
        candidates=[R.freeze(x['candidate']) for x in mappings]
        require(len(candidates)==len(set(candidates)) and set(candidates)==set(atlas)-{chosen},
                'Missing or repeated rejected supplier mapping')
        for mapping,candidate in zip(mappings,candidates):
            guard();index=mapping['anchor_index'];name=mapping['case'];inverse=mapping['inverse']
            require(type(index) is int and 0<=index<len(fixed) and name in names
                    and type(inverse) is bool,'Invalid transport binding')
            target=R.freeze(names[name]['pose'])
            if inverse:target=G.inverse(target)
            relative=G.relative(fixed[index],candidate)
            require(relative==target,'Contact is not the proved literal exclusion')
            V.universal([G.touching(relative),G.neg(G.intersection(relative))],guard)
        def blocked(relative):
            match=G.either(G.allowed(relative,models),G.allowed(G.inverse(relative),models))
            return G.both(G.touching(relative),match)
        rows=[G.both(G.point_membership(c,point),
                     *[G.neg(G.intersection(G.relative(f,c))) for f in fixed],
                     *[G.neg(blocked(G.relative(f,c))) for f in fixed]) for c in atlas]
        demanded=G.both(V.in_halo(point,fixed[:2]),G.neg(G.either(*(G.point_membership(f,point) for f in fixed))))
        partition=R.splitter(rows+[demanded])
        require(partition==G.partition(rows+[demanded]) and partition==saved['partition'],'Changed exact chain partition')
        samples=[]
        for k in partition['representatives']:
            guard();require(G.evaluate(demanded,k),'Demand is not an unfilled ORIGINAL pair-halo cell')
            allowed=[c for c,row in zip(atlas,rows) if G.evaluate(row,k)]
            require(set(allowed)==({chosen} if chosen is not None else set()),'Chain admits a different supplier')
            if chosen is not None and material:
                tile=R.literal(k);feet=[set(R.E.affine(tile,R.axial(f,k))) for f in fixed]
                new=set(R.E.affine(tile,R.axial(chosen,k)))
                u,v=G.value(point[0],k),G.value(point[1],k)
                require((u-2*v,v) in new and not new.intersection(set().union(*feet)),
                        'Material forced copy does not fill the demand disjointly')
            samples.append({'k':k,'eligible':allowed})
        require(R.freeze(samples)==R.freeze(saved['samples']),'Changed parameter representatives or eligibility')
        evidence.append({'stage':number,'suppliers':len(atlas),'rejected_suppliers':len(mappings),
                         'forced':chosen,'cuts':partition['cuts'],'geometry_cuts':geometry['cuts']})
        if chosen is not None:fixed=(*fixed,chosen)
    return {'stages':evidence,'rejected_supplier_mappings':sum(e['rejected_suppliers'] for e in evidence),
            'chain_sha256':R.sha(record),'remaining_point44_supplier':P,
            'corollary_dependency':'Published9474: forced R and the complete S-or-P alternative',
            'scope':'S branch impossible for every k>=6; P cover existence/global corona upper remain open'}


def main():
    start=time.monotonic();calls=0
    def guard():
        nonlocal calls
        calls+=1
        if deps.paused() or time.monotonic()-start>=43 or calls>100000:
            raise RuntimeError('Operational/43s/100000-operation guard; incomplete check inconclusive')
    def alarm(x,y):raise RuntimeError('45s signal guard; incomplete check inconclusive')
    signal.signal(signal.SIGALRM,alarm);signal.alarm(45)
    entries=json.loads((HERE/'inputs.json').read_text())['cases']
    require(len(entries)==29 and sum(e['prior_result'] is None for e in entries)==27,'Wrong declared case inventory')
    require(len({e['name'] for e in entries})==29,'Repeated case name')
    folder=HERE/'generated/normal';records={e['name']:json.loads((folder/f"{e['name']}.json").read_text()) for e in entries}
    evidence=[exclusion(records[e['name']],e,guard) for e in entries]
    chain=json.loads((folder/'chain.json').read_text());result=check_chain(chain,entries,guard)
    damages=[]
    def negative(label,operation):
        try:operation()
        except ValueError:damages.append(label)
        else:raise ValueError('Damaged certificate accepted: '+label)
    nonempty=next(e for e in entries if e['method']=='finite' and records[e['name']]['atlas'])
    tree=next(e for e in entries if e['method']=='tree')
    for label in ('changed_case_pose','missing_supplier','changed_partition','missing_DAG_node','changed_conflict'):
        damaged=deepcopy(records[nonempty['name']])
        if label=='changed_case_pose':damaged['fixed'][1][1][1]+=1
        elif label=='missing_supplier':damaged['supplier_records'][0]['atlas'].append(IDENTITY)
        elif label=='changed_partition':damaged['partition']['cuts'].append(999)
        elif label=='missing_DAG_node':damaged['proof']['nodes'].pop()
        else:damaged['universal']['conflicts'][0]^=1
        negative(label,lambda d=damaged:exclusion(d,nonempty,guard,False))
    for label in ('missing_cap_branch','new_halo_demand','false_empty_leaf'):
        damaged=deepcopy(records[tree['name']])
        if label=='missing_cap_branch':damaged['tree']['children'].pop()
        elif label=='new_halo_demand':damaged['tree']['children'][0]['node']['point']=((0,100),(0,100))
        else:damaged['tree']['children'][0]['node']['suppliers']['atlas'].append(IDENTITY)
        negative(label,lambda d=damaged:exclusion(d,tree,guard,False))
    for label in ('missing_chain_stage','changed_original_demand','missing_rejected_supplier','wrong_anchor',
                  'wrong_inverse','changed_forced_copy','false_final_choice'):
        damaged=deepcopy(chain)
        if label=='missing_chain_stage':damaged['stages'].pop()
        elif label=='changed_original_demand':damaged['stages'][0]['point']=((0,100),(0,100))
        elif label=='missing_rejected_supplier':damaged['stages'][0]['mappings'].pop()
        elif label=='wrong_anchor':damaged['stages'][0]['mappings'][0]['anchor_index']=999
        elif label=='wrong_inverse':damaged['stages'][0]['mappings'][0]['inverse']=not damaged['stages'][0]['mappings'][0]['inverse']
        elif label=='changed_forced_copy':damaged['stages'][0]['expected']=HALFTURN
        else:damaged['stages'][-1]['expected']=HALFTURN
        negative(label,lambda d=damaged:check_chain(d,entries,guard,False))
    signal.alarm(0)
    math={'exclusions':evidence,'chain':result,'damaged_controls':damages,
          'trust_boundary':'Shared affine/height kernels; separate interval sweeps, material geometry and search-free replay; ordinary proof unformalized and independently unreviewed'}
    mode='normal' if __debug__ else 'optimized'
    out={'agent':'six-heesch-2','role':'researcher','complete':True,'evidence':math,'mathematics_sha256':R.sha(math),
         'seconds':round(time.monotonic()-start,3),'max_rss_kib':resource.getrusage(resource.RUSAGE_SELF).ru_maxrss,
         'checked_utc':datetime.now(timezone.utc).isoformat()}
    (HERE/f'generated/reader-{mode}.json').write_text(json.dumps(out,indent=2)+'\n')
    print(json.dumps({k:v for k,v in out.items() if k!='evidence'}),flush=True)
    print(json.dumps({'cases':len(evidence),'additional':27,'stage_suppliers':[e['suppliers'] for e in result['stages']],
                      'forced':EXPECTED[:3],'final_suppliers':0,'mappings':result['rejected_supplier_mappings'],
                      'damaged_controls':len(damages)}),flush=True)


if __name__=='__main__':main()
