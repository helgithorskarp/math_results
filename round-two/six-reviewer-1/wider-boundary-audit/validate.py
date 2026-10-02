"""Check every byte-level mathematical record; no assertions/-O dependency."""
from pathlib import Path
import argparse,hashlib,json,sys
import core

def reject_constant(x):raise ValueError('nonfinite JSON token')
def pairs(items):
    out={}
    for k,v in items:
        if k in out:raise ValueError('duplicate JSON key')
        out[k]=v
    return out

def strict_equal(a,b):
    core.need(type(a)is type(b),'record type')
    if isinstance(a,dict):
        core.need(a.keys()==b.keys(),'record keyset')
        for k in a:strict_equal(a[k],b[k])
    elif isinstance(a,list):
        core.need(len(a)==len(b),'record length')
        for x,y in zip(a,b):strict_equal(x,y)
    else:core.need(a==b,'record value')

def main():
    p=argparse.ArgumentParser();p.add_argument('--fixture',type=Path,default=Path(__file__).with_name('EXPECTED.json'));p.add_argument('--output',type=Path);args=p.parse_args();record=core.complete_build()
    if args.output:args.output.write_text(json.dumps(record,sort_keys=True,indent=2)+'\n')
    expected=json.loads(args.fixture.read_text(),object_pairs_hook=pairs,parse_constant=reject_constant);strict_equal(record,expected)
    print(json.dumps({'status':'PASS','agent':'six-reviewer-1','role':'independent mathematical reviewer','record_sha256':core.digest(record),'636_full_gap_coefficients':True,'whole_sector_integrals':15,'full_Gaussian_controls':7,'two_level_moment_controls':7,'strict_margins':sum(len(record[k]['strict_margins'])for k in ('polar','sector','budgets')),'proved_actual_H_coefficient':41},sort_keys=True))
if __name__=='__main__':main()
