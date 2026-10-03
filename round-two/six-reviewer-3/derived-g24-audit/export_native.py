#!/usr/bin/env python3
"""POST-SEAL target-code execution to export all polynomial coordinate data."""
import argparse,json,sys
from pathlib import Path
ap=argparse.ArgumentParser();ap.add_argument('--native-dir',required=True);ap.add_argument('--output',required=True);args=ap.parse_args()
sys.path.insert(0,str(Path(args.native_dir).resolve()))
from model import make
from polynomials import P
Y,O,_=make(P.var(0))
def coefficients(p):
    if any(k[1:]!=(0,0) for k in p.c):raise ValueError('nonunivariate native polynomial')
    n=max((k[0] for k in p.c),default=-1)
    return [p.c.get((i,0,0),0) for i in range(n+1)]
Path(args.output).write_text(json.dumps({'coordinates':{str(i):[coefficients(p) for p in v] for i,v in Y.items()},'Omega':coefficients(O)},sort_keys=True)+'\n')
