"""Independent original-image/cap/complete-clause audits and positive model.

Pinned scalar code changes only its two fixed-prefix capacity constants to
len(prefix). Provenance binds each residual leaf to the independently checked
finite reduction. Clause/Horn auditor reused verbatim; no encoder or solver.
"""
import argparse
import importlib.util
import inspect
import json
from pathlib import Path
import resource
import time
from shared import HERE,inputs,read,residual_tails,tail_path


def load(path,name):
    spec=importlib.util.spec_from_file_location(name,path)
    value=importlib.util.module_from_spec(spec);spec.loader.exec_module(value)
    return value


def prepare(repo,output):
    f,_,_,_=inputs(repo);tails=residual_tails(output)
    scalar=load(repo/'sorting13_B11_additional_ten_event_exclusions/audit_data.py','credited_scalar_auditor')
    def provenance(meta):
        r=meta['record'];index,image=r['parent_index'],r['local_image']
        tail=next(t for t in tails if (t['parent_index'],t['image'])==(index,image))
        assert r['prefix_case']==tail['case']
        assert r['code']==tail['class_code'] and r['prefix_B11']==tail['prefix_B11']
        assert r['image9']==tail['rows9'] and r['image9_rows']==len(tail['rows9'])
        assert meta['prefix']==f['prefix22']+[[a+1,b+1] for a,b in tail['prefix_B11']]
        assert len(meta['prefix'])==33 and meta['budget'] in (11,36)
        assert not meta['activity'] and not meta['domains'] and 'boundary' not in meta
    scalar.provenance=provenance
    source=inspect.getsource(scalar.audit_data)
    assert source.count("32 + meta['budget']")==2
    source=source.replace("32 + meta['budget']","len(prefix) + meta['budget']")
    exec(compile(source,'<pinned scalar audit with actual-prefix capacities>','exec'),scalar.__dict__)
    clauses=load(repo/'sorting13_B11_additional_ten_event_exclusions/audit_encoding.py','credited_complete_clause_auditor')
    return scalar,clauses


def main():
    assert __debug__
    parser=argparse.ArgumentParser()
    parser.add_argument('--repository',type=Path,default=HERE.parent)
    parser.add_argument('--output',type=Path,default=HERE/'generated')
    args=parser.parse_args();began=time.monotonic()
    scalar,clauses=prepare(args.repository,args.output);results=[]
    for tail in residual_tails(args.output):
        path=tail_path(args.output,tail);meta=read(path.with_suffix('.metadata.json'))
        assert meta['budget']==11
        data=scalar.audit_data(meta);audited=clauses.Audit(meta,path).run()
        result=dict(parent_index=tail['parent_index'],image=tail['image'],
                    status='ORIGINAL_PREFIX_CAPS_AND_EVERY_CLAUSE_VERIFIED',data=data,clauses=audited)
        results.append(result);print(json.dumps(result),flush=True)
    positive_path=args.output/'positive36.cnf';meta=read(positive_path.with_suffix('.metadata.json'))
    control=read(positive_path.with_suffix('.model.json'))
    data=scalar.audit_data(meta)
    positive=scalar.check_model(meta,control['word'],control['model'],positive_path)
    result=dict(agent='six-sorting-2',role='researcher',status='FIFTEEN_TAIL_ENCODINGS_AND_POSITIVE_CONTROL_CHECKED',
                records=results,positive_data=data,positive_model=positive,
                cardinality_shapes=list(clauses.SHAPES.values()),
                exhaustive_cardinality_assignments=sum(s['tests'] for s in clauses.SHAPES.values()),
                seconds=time.monotonic()-began,peak_rss_kib=resource.getrusage(resource.RUSAGE_SELF).ru_maxrss)
    (args.output/'tail-audit-summary.json').write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps({k:v for k,v in result.items() if k!='records'},indent=2),flush=True)


if __name__=='__main__':main()
