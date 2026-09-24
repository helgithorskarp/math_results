#!/usr/bin/env python3
"""Generate expanded witnesses privately and verify them by an independent method."""
from __future__ import annotations
import json
import subprocess
import sys
import tempfile
from pathlib import Path
from verify import verify

ROOT=Path(__file__).resolve().parent
CASES=[('S',1,'S',1,0),('H',1,'S',1,1),('S',2,'H',1,0),
       ('S',2,'S',2,1),('F',1,'S',1,0),('S',1,'F',1,1),
       ('H',1,'F',1,1),('S',2,'F',1,0),('F',1,'S',2,1),
       ('H',2,'S',2,0),('S',4,'S',1,0),('F',1,'F',1,0)]


def main() -> None:
    rows=[]
    with tempfile.TemporaryDirectory(prefix='square-saturation-') as tmp:
        witness=Path(tmp)/'witness.json'
        for case in CASES:
            result=subprocess.run([sys.executable,str(ROOT/'construct.py'),'--blocks',
                                   *map(str,case),'--output',str(witness)],
                                  check=True,capture_output=True,text=True)
            row=json.loads(result.stdout)
            checked=verify(json.loads(witness.read_text()))
            if (checked['edge_sha256']!=row['edge_sha256'] or
                    checked['selected_edges_checked']!=row['edge_count']):
                raise RuntimeError('constructor/checker disagreement')
            row['independent_check']=checked
            rows.append(row)
    negative=[]
    for name,data in [('empty',{'dimension':2,'adjacency_masks':[0]*4}),
                      ('full',{'dimension':2,'adjacency_masks':[3]*4}),
                      ('asymmetric',{'dimension':2,'adjacency_masks':[1,0,0,0]})]:
        try:verify(data)
        except ValueError:negative.append(name)
        else:raise RuntimeError('invalid witness accepted')
    print(json.dumps({'instances':rows,'negative_controls_rejected':negative},indent=2,sort_keys=True))


if __name__=='__main__':main()
