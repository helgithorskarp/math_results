"""Compare the ENTIRE exact record, preserving JSON types and every entry."""
from pathlib import Path
import argparse,json
import core

def pairs(items):
    out={}
    for k,v in items:
        core.require(k not in out,'duplicate JSON key')
        out[k]=v
    return out

def finite(s):raise ValueError('nonfinite JSON constant')

def equal(a,b):
    core.require(type(a)is type(b),'whole exact record type')
    if isinstance(a,dict):
        core.require(a.keys()==b.keys(),'whole exact record keyset')
        for k in a:equal(a[k],b[k])
    elif isinstance(a,list):
        core.require(len(a)==len(b),'whole exact record length')
        for x,y in zip(a,b):equal(x,y)
    else:core.require(a==b,'whole exact record value')

def load(p):return json.loads(Path(p).read_text(),object_pairs_hook=pairs,parse_constant=finite)

def main():
    p=argparse.ArgumentParser();p.add_argument('--fixture',type=Path,default=Path(__file__).with_name('EXPECTED.json'));p.add_argument('--output',type=Path)
    a=p.parse_args();record=core.build();equal(record,load(a.fixture))
    if a.output:a.output.write_text(json.dumps(record,sort_keys=True,separators=(',',':'))+'\n')
    print(json.dumps({'status':'PASS','agent':'six-reviewer-1','role':'independent mathematical reviewer','whole_record_sha256':core.digest(record),'strict_margins':len(record['strict_margins']),'whole_identities':len(record['whole_identities']),'whole_nine_phases':len(record['whole_phase_table']),'fresh_Gaussian_controls':len(record['fresh_Gaussian_controls']),'Legendre_degrees':len(record['whole_Legendre_through_degree12']),'objective_remainder':record['proved_objective_remainder'],'separate_physical_remainder':record['proved_physical_remainder']},sort_keys=True))

if __name__=='__main__':main()
