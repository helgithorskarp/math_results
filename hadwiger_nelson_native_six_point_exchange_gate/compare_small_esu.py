#!/usr/bin/env python3
"""Entry comparison after verify.py has regenerated the spanning-tree lists."""
from pathlib import Path
import argparse
import hashlib
import json
import subprocess
import time
from verify import HERE, require


def compare(work):
    start=time.monotonic()
    subprocess.run(['g++','-std=c++17','-O3',str(HERE/'enumerate_small_esu.cpp'),
                    '-o',str(work/'small_esu')],check=True)
    result=subprocess.run([str(work/'small_esu'),str(work/'graph-input.txt'),str(work/'small-esu')],
                          check=True,capture_output=True,text=True)
    (work/'small-esu.log').write_text(result.stdout+result.stderr)
    rows=[]
    for k in (3,4,5):
        a=sorted((work/f'groups-{k}.txt').read_text().splitlines())
        b=sorted((work/f'small-esu-{k}.txt').read_text().splitlines())
        require(a==b,'native entry mismatch at size '+str(k))
        rows.append({'size':k,'sets':len(a),'entry_equal':True,
                     'canonical_sha256':hashlib.sha256(('\n'.join(a)+'\n').encode()).hexdigest()})
    out={'status':'PASS','rows':rows,'seconds':time.monotonic()-start}
    (work/'entry-comparison.json').write_text(json.dumps(out,indent=2)+'\n')
    return out


if __name__=='__main__':
    p=argparse.ArgumentParser(description=__doc__);p.add_argument('--work',type=Path,required=True)
    print(json.dumps(compare(p.parse_args().work.resolve()),indent=2))
