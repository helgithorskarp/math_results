"""Six C11 Boolean/pruning proof generators and a genuine C36 control.

Credits six-sorting-2/8222 for the pinned depth-free Boolean encoding.
No activity or suffix clauses are added. UNKNOWN proves no exclusion.
"""
import argparse
import hashlib
import json
import os
from pathlib import Path
import sys
import time
from shared import HERE,inputs,read,residual_tails,tail_path

for name in ('OMP_NUM_THREADS','OPENBLAS_NUM_THREADS','MKL_NUM_THREADS','NUMEXPR_NUM_THREADS'):
    os.environ[name]='1'


def data_provider(f,SIZES):
    def data(record,budget):
        prefix=f['prefix22']+[[a+1,b+1] for a,b in record['prefix_B11']]
        assert len(prefix)==33 and budget in (11,36)
        caps={}
        for original in range(1,8191):
            row=original;charges=[0,0]
            for a,b in prefix:
                left,right=(row>>a)&1,(row>>b)&1
                charges[0]+=not (left and right);charges[1]+=bool(left or right)
                if left>right:row^=(1<<a)|(1<<b)
            middle=(row>>2)&511
            for mode,marks in ((0,13-original.bit_count()),(1,original.bit_count())):
                cap=len(prefix)+budget-SIZES[13-marks]-charges[mode]
                key=middle,mode
                caps[key]=min(cap,caps.get(key,len(prefix)+budget))
        return prefix,caps,[]
    return data


def main():
    assert __debug__
    parser=argparse.ArgumentParser()
    parser.add_argument('--repository',type=Path,default=HERE.parent)
    parser.add_argument('--output',type=Path,default=HERE/'generated')
    parser.add_argument('--skip-positive',action='store_true')
    parser.add_argument('--skip-search',action='store_true')
    args=parser.parse_args();f,_,_,_=inputs(args.repository)
    sys.path.insert(0,str(args.repository/'sorting13_B11_additional_ten_event_exclusions'))
    import build as core
    import pysat
    assert pysat.__version__=='1.8.dev24'
    core.data=data_provider(f,core.SIZES)
    args.output.mkdir(parents=True,exist_ok=True)
    cert=read(HERE/'certificate.json');records=[];began=time.monotonic()
    for ordinal,tail in enumerate(residual_tails(args.output)):
        index,image=tail['parent_index'],tail['image'];count=len(tail['rows9'])
        record=dict(code=tail['class_code'],image9=tail['rows9'],image9_rows=count,
                    prefix_B11=tail['prefix_B11'],parent_index=index,local_image=image,prefix_case=tail['case'])
        if ordinal==0 and not args.skip_positive:
            path=args.output/'positive36.cnf';enc=core.Encoding(record,36,path,activity=False)
            word=core.normalize([(j-1,j) for i in range(1,9) for j in range(i,0,-1)])
            answer,seconds=enc.limited(15,assumptions=enc.fixed(word))
            assert answer is True,'Positive control failed or incomplete'
            model=enc.solver.get_model();enc.solver.delete()
            path.with_suffix('.model.json').write_text(json.dumps(dict(word=word,model=model),separators=(',',':'))+'\n')
        path=tail_path(args.output,tail);enc=core.Encoding(record,11,path,activity=False)
        expected=next((t for t in cert.get('tail_certificates',[]) if (t['parent_index'],t['image'])==(index,image)),None)
        if expected is not None:assert enc.metadata['cnf_sha256']==expected['cnf_sha256']
        if args.skip_search:
            records.append(dict(parent_index=index,image=image,status='COMPLETE_CNF_REBUILT_WITHOUT_NEGATIVE_SEARCH',
                                cnf_sha256=enc.metadata['cnf_sha256'],variables=enc.top,clauses=enc.count))
            enc.solver.delete();continue
        answer,seconds=enc.limited(40,30000)
        result=dict(parent_index=index,image=image,budget=11,case=tail['case'],rows=count,
                    cnf_sha256=enc.metadata['cnf_sha256'],variables=enc.top,clauses=enc.count,
                    solve_seconds=seconds,statistics=enc.solver.accum_stats())
        if answer is not False:
            result.update(status='NO_EXCLUSION_ESTABLISHED',solver_answer=answer)
            if answer is True:
                model=enc.solver.get_model();positive=set(x for x in model if x>0)
                word=[]
                for choices in enc.choice:
                    chosen=[i for i,c in enumerate(choices) if c in positive]
                    assert len(chosen)==1
                    word.append(core.PAIRS[chosen[0]])
                full=enc.prefix+[[a+2,b+2] for a,b in word]
                assert len(full)==44
                assert all(core.scalar(row,full)==((1<<row.bit_count())-1)<<(13-row.bit_count()) for row in range(8192))
                path.with_suffix('.model.json').write_text(json.dumps(dict(word=word,full13=full,model=model),separators=(',',':'))+'\n')
                result.update(status='SAT_FULL44_BOOLEAN_WITNESS_PENDING_INDEPENDENT_CHECK',full13=full)
            enc.solver.delete();records.append(result);print(json.dumps(result),flush=True)
            break
        proof=path.with_suffix('.drat');proof.write_text('\n'.join(enc.solver.get_proof())+'\n')
        result.update(status='UNSAT_LOGGED_PENDING_AUDIT_AND_REPLAY',raw_drat_sha256=hashlib.sha256(proof.read_bytes()).hexdigest())
        if expected is not None:assert result['raw_drat_sha256']==expected['raw_drat_sha256']
        enc.solver.delete();records.append(result);print(json.dumps(result),flush=True)
    status='ALL_SIX_TAILS_UNSAT_LOGGED_PENDING_INDEPENDENT_CHECKS' if len(records)==6 and all(r['status']=='UNSAT_LOGGED_PENDING_AUDIT_AND_REPLAY' for r in records) else 'PARTIAL_OR_REBUILD_ONLY_NO_NEW_EXCLUSION'
    (args.output/'tail-generation-summary.json').write_text(json.dumps(dict(agent='six-sorting-2',role='researcher',
        status=status,records=records,seconds=time.monotonic()-began),indent=2)+'\n')


if __name__=='__main__':main()
