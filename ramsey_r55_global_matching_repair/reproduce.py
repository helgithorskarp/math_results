"""Check the included complete proofs and reproduce them byte for byte."""
import hashlib
import json
from pathlib import Path
import subprocess
import sys
import tempfile

ROOT=Path(__file__).resolve().parent


def need(ok,message):
    if not ok:
        raise RuntimeError(message)


def run():
    entries=set()
    for line in (ROOT/'SHA256SUMS').read_text().splitlines():
        sha,name=line.split('  ',1)
        path=Path(name)
        need(not path.is_absolute() and '..' not in path.parts and name not in entries,'manifest path')
        entries.add(name)
        need(hashlib.sha256((ROOT/path).read_bytes()).hexdigest()==sha,'manifest mismatch: '+name)
    actual={p.relative_to(ROOT).as_posix() for p in ROOT.rglob('*') if p.is_file()
            and '__pycache__' not in p.parts and p.name!='SHA256SUMS'}
    need(entries==actual,'manifest coverage')
    modes=[]
    for flags in (['-B'],['-O','-B']):
        def call(*args):
            p=subprocess.run([sys.executable,*flags,*map(str,args)],cwd=ROOT,
                             stdout=subprocess.PIPE,stderr=subprocess.PIPE)
            if p.returncode:
                raise RuntimeError(p.stderr.decode()+p.stdout.decode())
            return p.stdout
        need(call('controls.py')==(ROOT/'expected_controls.json').read_bytes(),'small controls changed')
        need(call('audit_corpus.py','proofs')==(ROOT/'expected_audit.json').read_bytes(),'independent corpus audit changed')
        with tempfile.TemporaryDirectory(prefix='r55-matching-replay-') as tmp:
            out=Path(tmp)/'fresh-proof'
            call('run_gate.py',out)
            facts=json.loads((out/'gate.json').read_text())
            need(facts['status']=='COMPLETE_GLOBAL_MATCHING_FAMILY_EXCLUDED' and facts['completed_records']==21,'production gate incomplete')
            for i in range(21):
                name=f'parent_{i:02}.json'
                need((out/name).read_bytes()==(ROOT/'proofs'/name).read_bytes(),'cover proof changed: '+name)
        modes.append('optimized' if '-O' in flags else 'normal')
    return {'status':'REPRODUCED_COMPLETE_MATCHING_REPAIR_EXCLUSION','modes':modes,
            'source_manifest_entries':len(entries),'reference_records':21,
            'complete_global_family_excluded':True,'proof_nodes':2155,'proof_bytes':40749,
            'audit_sha256':hashlib.sha256((ROOT/'expected_audit.json').read_bytes()).hexdigest(),
            'ramsey_graph_found':False,'ramsey_bound_improved':False}


if __name__=='__main__':
    print(json.dumps(run(),indent=2,sort_keys=True))
