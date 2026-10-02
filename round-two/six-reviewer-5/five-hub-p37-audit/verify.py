"""Offline whole independent proof-record regeneration; no target/native code."""
import argparse,json,pathlib,hashlib
import audit as a,controls,column_quotas
P=pathlib.Path(__file__).resolve().parent

def compute():
    core=a.compute();cs=controls.run();qs=column_quotas.run(core,cs)
    for seal in ('first-seal.json','strengthening-seal.json'):
      ss=json.loads((P/seal).read_text())
      for f,sha in ss['files'].items():
        if f=='core-record.json':got=a.digest(core)
        elif f=='controls-record.json':got=a.digest(cs)
        else:got=hashlib.sha256((P/f).read_bytes()).hexdigest()
        a.need(got==sha,'unchanged independent first seal:'+f)
    return dict(agent='six-reviewer-5',role='independent mathematical reviewer',status='COMPLETE_CONDITIONAL_9594_P37_REVIEW_AND_ORDINARY_COLUMN_REFINEMENTS',
      core_sha256=a.digest(core),controls_sha256=a.digest(cs),column_quotas_sha256=a.digest(qs),
      scalar_counts=[[r[k] for k in ('N5','T','X','tau','Q','E','K','margin_budget')]+[len(r['vectors']),r['states']] for r in core['all_cases']],
      ordered_failures=core['ordered_failures'],total_vectors=core['total_vectors'],last6_scope_metrics=[x[1]['metrics'] for x in core['simple_endpoint_only_residuals']],
      controls=cs,column_quotas=qs)

def run():
    parser=argparse.ArgumentParser();parser.add_argument('--write',type=pathlib.Path);args=parser.parse_args()
    record=compute();data=a.encode(record)
    if args.write:args.write.write_bytes(data)
    else:a.need(data==(P/'EXPECTED.json').read_bytes(),'complete sealed final independent record')
    print(json.dumps(dict(agent=record['agent'],role=record['role'],status=record['status'],whole_sha256=hashlib.sha256(data).hexdigest(),
      cases=len(record['scalar_counts']),vectors=record['total_vectors'],core_sha256=record['core_sha256'],
      graph_cases=record['controls']['graph']['labelled_cases'],local_placement_domains=[{k:row[k] for k in ('scope','full_physical_placements','positive_abstract_local_placements','positive_marks','retained_P36_vectors')} for row in record['column_quotas']['placements']]),indent=2))
if __name__=='__main__':run()
