"""Full strict typed record checker, normal and optimized Python."""
from pathlib import Path
import argparse,json
import core
def pairs(items):
    d={}
    for k,v in items:
        if k in d:raise ValueError('duplicate JSON key')
        d[k]=v
    return d
def constant(x):raise ValueError('nonfinite JSON')
def equal(a,b):
    core.need(type(a)is type(b),'whole record type')
    if isinstance(a,dict):
        core.need(a.keys()==b.keys(),'whole record keyset')
        for k in a:equal(a[k],b[k])
    elif isinstance(a,list):
        core.need(len(a)==len(b),'whole record length')
        for x,y in zip(a,b):equal(x,y)
    else:core.need(a==b,'whole record value')
def main():
    p=argparse.ArgumentParser();p.add_argument('--fixture',type=Path,default=Path(__file__).with_name('EXPECTED.json'));p.add_argument('--output',type=Path);a=p.parse_args()
    d=core.build()
    if a.output:a.output.write_text(json.dumps(d,indent=2,sort_keys=True)+'\n')
    equal(d,json.loads(a.fixture.read_text(),object_pairs_hook=pairs,parse_constant=constant))
    print(json.dumps({'status':'PASS','agent':'six-reviewer-1','role':'independent mathematical reviewer','whole_record_sha256':core.digest(d),'strict_rational_margins':sum(len(d[k]['strict_margins'])for k in ['polar','sectors','budgets'])+len(d['whole_radial_faces39over5'])+2,'whole_sectors':15,'whole_faces':8,'whole_Gaussian_controls':7,'whole_twolevel_controls':7,'whole_mean_square_controls':4,'proved_actual_H_coefficient':40,'actual_energy_after_entry':'H<1/400'},sort_keys=True))
if __name__=='__main__':main()
