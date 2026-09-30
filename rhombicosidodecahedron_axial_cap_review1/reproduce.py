"""Run both independent exact audits; expected.json is output, not proof input."""
import argparse, json, resource, sys, time
from pathlib import Path
from fractions import Fraction as F
from check import Q, PHI, need, vertices, group, optimizers
from cap_checks import verify

def main():
    parser=argparse.ArgumentParser()
    parser.add_argument('--self-test',action='store_true')
    parser.add_argument('--output',type=Path)
    parser.add_argument('--records',type=Path,help='optional private full optimizer dump; do not publish')
    args=parser.parse_args();start=time.monotonic()
    need(PHI*PHI==PHI+1 and Q(0,1)>2 and Q(0,1)<3,'quadratic field calibration')
    need(Q(F(9,4),-1)>0 and Q(F(11,5),-1)<0,'opposite-sign ordering calibration')
    V=vertices();G,gs=group(V);regions,rs,records=optimizers(V,G)
    result={'agent':'six-reviewer-1','role':'independent mathematical reviewer','field':'a+b*sqrt(5)',
            'vertices':60,'group':gs,'axial':rs,'all_source_cap':verify(V,G)}
    result=json.loads(json.dumps(result))
    if args.self_test:
        expected=json.loads(Path(__file__).with_name('expected.json').read_text())
        need(result==expected,'independent expected summary mismatch')
    output=json.dumps(result,indent=2,sort_keys=True)+'\n'
    if args.output:args.output.write_text(output)
    if args.records:args.records.write_text(json.dumps(records,indent=2,sort_keys=True)+'\n')
    print(output,end='')
    print(json.dumps({'python':sys.version.split()[0],'seconds':time.monotonic()-start,
                     'peak_rss_kib':resource.getrusage(resource.RUSAGE_SELF).ru_maxrss}),file=sys.stderr)

if __name__=='__main__':main()
