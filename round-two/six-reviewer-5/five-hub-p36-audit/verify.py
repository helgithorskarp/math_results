"""Offline independent replay; full finite records are regenerated, not shipped."""
import argparse,hashlib,json,pathlib,time
import audit as a
import propagation,graph_checks,controls

P=pathlib.Path(__file__).resolve().parent

def run():
    start=time.monotonic()
    for name in ('first-seal.json','strengthening-seal.json'):
        seal=json.loads((P/name).read_text())
        for source,h in seal['files'].items():
            if source.endswith('-record.json'):continue
            a.need(hashlib.sha256((P/source).read_bytes()).hexdigest()==h,'unchanged pre-author sealed source '+source)
    core=a.compute();place=propagation.run();graph=graph_checks.run()
    expected=json.loads((P/'EXPECTED.json').read_text())
    hashes={'independent_entire_record_sha256':a.digest(core),
            'propagation_entire_record_sha256':a.digest(place),
            'graph_entire_record_sha256':a.digest(graph)}
    for k,h in hashes.items():a.need(h==expected[k],'whole regenerated pre-author record '+k)
    direct=[r for c in core['all_scalar_cases'] for r in c['vectors']]
    active=[r['stronger_graph_cut'] for r in direct if r['stronger_graph_cut']['active']]
    extra={'controls':controls.run(core,place),'transports':controls.transports(place)}
    a.need(time.monotonic()-start<45,'INCOMPLETE fixed45s final guard')
    result={'agent':'six-reviewer-5','role':'independent mathematical reviewer',**hashes,
            'all27branch_counts':expected['all27branch_counts'],
            'core_vectors':len(direct),'original_ordered_failures':core['ordered_original_failures'],
            'DAG_states':sum(c['count_DAG_states'] for c in core['all_scalar_cases']),
            'local5Hplacements':place['whole_physical_five_H_placements'],
            'positive_local5Hplacements':place['whole_positive_five_H_placements'],
            'refined_marks':place['propagation_feasible_high_marks'],
            'refined_types':len(place['propagation_feasible_types']),
            'refined_vectors':place['refined_total_vectors'],
            'refined_ordered_failures':place['refined_ordered_failures'],
            'all_root_B_joint_cases':len(active),
            'joint_endpoint_excluded':sum(r['violates_joint_endpoint'] for r in active),
            'root_pair_cover_excluded':sum(r['violates_root_pair_cover'] for r in active),
            'graph_calibration':graph,**extra,
            'scope':'Conditional P>=36 with explicit expository correction. Positive local placements/types/abstract graphs are necessary carriers, not packings. Complete generic classification8933 and prior9367 imported.'}
    return result,(core,place,graph)

if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('--output',required=True);p.add_argument('--check');p.add_argument('--records')
    args=p.parse_args();result,records=run();raw=a.encode(result)
    if args.check:a.need(raw==pathlib.Path(args.check).read_bytes(),'every final mathematical output byte equal')
    output=pathlib.Path(args.output);output.parent.mkdir(parents=True,exist_ok=True);output.write_bytes(raw)
    if args.records:
        d=pathlib.Path(args.records);d.mkdir(parents=True,exist_ok=True)
        for name,r in zip(('first-record.json','propagation-record.json','graph-record.json'),records):(d/name).write_bytes(a.encode(r))
    print(json.dumps({'complete':True,'whole_sha256':hashlib.sha256(raw).hexdigest(),'core_vectors':result['core_vectors'],
                      'refined_marks':result['refined_marks'],'all_root_B_joint_cases':result['all_root_B_joint_cases']}))
