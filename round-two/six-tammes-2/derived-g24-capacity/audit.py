"""Exact sign replay with centered rational Taylor enclosures.

This arithmetic route is separate from both Bernstein implementations.
It shares the explicitly stated coordinate, Cramer and coverage reduction;
same-author arithmetic corroboration, not independent geometric review.
"""
from pathlib import Path
import argparse,json,signal
from check import HERE,run

def main():
    signal.signal(signal.SIGALRM,lambda *_:(_ for _ in ()).throw(TimeoutError('50-second Taylor audit guard')));signal.alarm(50)
    p=argparse.ArgumentParser();p.add_argument('--certificate',type=Path,default=HERE/'CERTIFICATE.json');p.add_argument('--output',type=Path);args=p.parse_args()
    out=run(json.loads(args.certificate.read_text()),method='taylor');raw=json.dumps(out,sort_keys=True,indent=2)+'\n'
    if args.output:args.output.write_text(raw)
    print(raw,end='')
if __name__=='__main__':main()
