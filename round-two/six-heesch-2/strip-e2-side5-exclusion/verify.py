"""Literal proof, source/dependency binding, and normal/optimized replay."""
import hashlib
import json
from pathlib import Path
import deps
from run import run_all
H=Path(__file__).resolve().parent
def main():
    expected=json.loads((H/'expected.json').read_text())
    for name,digest in expected['source_hashes'].items():
        if hashlib.sha256((H/name).read_bytes()).hexdigest()!=digest:
            raise ValueError('Changed contribution source: '+name)
    out=run_all()
    if out['mathematics_sha256']!=expected['mathematics_sha256']:
        raise ValueError('Literal mathematical evidence does not match expected.json')
    if out['DAG_nodes']!=20 or out['collar_suppliers']!=99 or out['serial_jobs']!=6:
        raise ValueError('Unexpected certificate dimensions')
    print(json.dumps(out,sort_keys=True),flush=True)
if __name__=='__main__':main()
