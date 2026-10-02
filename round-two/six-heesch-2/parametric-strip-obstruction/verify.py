"""Serial regeneration and search-free verification of the compact evidence."""
import argparse
import hashlib
import json
from pathlib import Path
import subprocess
import sys

H=Path(__file__).absolute().parent
def require(value,message):
    if not value:raise ValueError(message)
def main():
    parser=argparse.ArgumentParser();parser.add_argument('--record-expected',action='store_true')
    args=parser.parse_args()
    for script in ('strip_parametric_certificate.py','strip_parametric_pair.py',
                   'strip_parametric_reader.py','strip_parametric_pair_reader.py'):
        for mode in ('normal','optimized'):
            command=[sys.executable]+(['-O'] if mode=='optimized' else [])+[str(H/script)]
            result=subprocess.run(command,text=True,capture_output=True,timeout=47)
            require(result.returncode==0,f'{script}/{mode} did not complete: {result.stderr[-1000:]}')
    summaries={}
    for label,prefix in (('root','reader'),('pair','pair-reader')):
        n=json.loads((H/f'strip-parametric/{prefix}-normal.json').read_text())
        o=json.loads((H/f'strip-parametric/{prefix}-optimized.json').read_text())
        require(n['evidence']==o['evidence'],'Reader modes disagree')
        e=n['evidence'];require(e['complete'] and e['damaged_controls']==3,'Reader incomplete')
        summaries[label]={'evidence_sha256':n['evidence_sha256'],'matrix_sha256':e['matrix_sha256'],
            'atlas_sha256':e['atlas_sha256'],'DAG_nodes':e['DAG_nodes'],'breakpoints':e['breakpoints'],
            'period':e['period'],'atomic_predicates':e['atomic_predicates'],'damaged_controls':e['damaged_controls']}
    package={'agent':'six-heesch-2','role':'researcher','complete':True,'root':summaries['root'],'pair':summaries['pair'],
        'source_hashes':{p.name:hashlib.sha256(p.read_bytes()).hexdigest() for p in H.glob('*.py')},
        'external_kernel_sha256':hashlib.sha256((H.parent/'strip-t5/exact.py').read_bytes()).hexdigest(),
        'scope':'For each k>=6, E2(T_k) contained in the explicit affine32 atlas implies Hc<=Hh<=3. The inclusion is unproved for all k.'}
    expected=H/'expected.json'
    if args.record_expected:expected.write_text(json.dumps(package,indent=2)+'\n')
    else:require(json.loads(expected.read_text())==package,'Expected evidence/source binding changed')
    print(json.dumps(package,sort_keys=True))

if __name__=='__main__':main()
