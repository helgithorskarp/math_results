#!/usr/bin/env python3
"""Replay pinned prerequisites and the exact common-to-cyclic Gram map."""
import argparse
import hashlib
import json
from pathlib import Path
import subprocess
import sys
import check as c

HERE=Path(__file__).resolve().parent
ROOT=HERE.parents[2]

def replay(prerequisite_root,completion_root,near_root):
    inputs=json.loads((HERE/'INPUTS.json').read_text())
    asym=prerequisite_root/inputs['asymmetric']['directory']
    for entry,folder in ((inputs['asymmetric'],asym),(inputs['completion'],completion_root)):
        for name,sha in entry['files_sha256'].items():
            c.require(hashlib.sha256((folder/name).read_bytes()).hexdigest()==sha,'pinned source '+str(folder/name))
    flags=['-O'] if sys.flags.optimize else []
    previous=subprocess.run([sys.executable,*flags,'-B',str(completion_root/'check.py'),
                             '--replay-prerequisites','--prerequisite-root',str(prerequisite_root),
                             '--near-pattern-root',str(near_root)],
                            check=True,capture_output=True,text=True,timeout=50)
    prior=json.loads(previous.stdout)
    c.require(prior['status']=='VERIFIED' and prior['prior_exact_bounds_replayed'],
              'full published completion prerequisites replayed')
    previous=subprocess.run([sys.executable,*flags,'-B',str(asym/'verify.py'),'--selftest'],
                            check=True,capture_output=True,text=True,timeout=10)
    local=json.loads(previous.stdout.splitlines()[0])
    c.require(local['status']=='VERIFIED' and local['coefficient_radius']=='1/250000',
              'old asymmetric local certificate replayed')
    prior_data=json.loads((completion_root/'certificate.json').read_text())
    data=json.loads((HERE/'certificate.json').read_text())
    cyclic=c.verify(data,False)
    V=[tuple(c.readpoly(p) for p in row) for row in prior_data['incumbent_vectors']]
    V[14]=tuple(c.readpoly(p) for p in prior_data['alternate_vector'])
    C=[tuple(c.readpoly(p) for p in row) for row in data['vectors']]
    H=tuple(tuple(c.ONE if i==j else c.T for j in range(3)) for i in range(3))
    HV=[c.matvec(H,v) for v in V];HC=[c.matvec(H,v) for v in C]
    permutation=prior_data['cyclic_permutation']
    c.require(permutation==[1,0,11,7,5,4,10,3,9,8,6,2,14,13,12],'fixed cyclic Gram relabeling')
    c.require(all(c.dot(V[i],HV[j])==c.dot(C[permutation[i]],HC[permutation[j]])
                  for i in range(15) for j in range(15)), 'all 225 common-to-cyclic Gram entries')
    return {'status':'VERIFIED','asymmetric_local_replayed':True,
            'full_completion_prerequisites_replayed':True,'cyclic_local_verified':True,
            'common_to_cyclic_gram_entries':225,'tolerance':cyclic['twenty_six_contact_tolerance']}

if __name__=='__main__':
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--prerequisite-root',type=Path,default=ROOT)
    parser.add_argument('--completion-root',type=Path,default=ROOT/'round-two/six-tammes-2/fourteen-point-completion')
    parser.add_argument('--near-pattern-root',type=Path,default=ROOT/'round-two/six-tammes-2/robust-incumbent-pattern')
    args=parser.parse_args()
    print(json.dumps(replay(args.prerequisite_root,args.completion_root,args.near_pattern_root),sort_keys=True))
