#!/usr/bin/env python3
"""Reproduce the compact certificates and finite controls without rewriting them."""
import hashlib,json,subprocess,sys
from pathlib import Path
ROOT=Path(__file__).resolve().parent

def main():
    for line in (ROOT/'SHA256SUMS').read_text().splitlines():
        digest,name=line.split('  ',1)
        if hashlib.sha256((ROOT/name).read_bytes()).hexdigest()!=digest:raise ValueError(('manifest mismatch',name))
    for flags in ([],['-O']):
        for source,expected in [('derive.py','certificate.json'),('check.py','expected_kernel.json'),('controls.py','expected_controls.json')]:
            out=subprocess.check_output([sys.executable,*flags,'-B',str(ROOT/source)])
            if out!=(ROOT/expected).read_bytes():raise ValueError(('reproduction mismatch',flags,source))
    print(json.dumps({'status':'VERIFIED_H24_WHOLE_GLOBAL_FAMILY_PACKAGE','variants':2,
                      'kernel_stars':14641,'physical43_controls':64,'new_solver_runs':0},indent=2))
if __name__=='__main__':main()
