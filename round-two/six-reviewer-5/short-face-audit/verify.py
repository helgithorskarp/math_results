"""Offline complete independent evidence verification; no target code or network."""
import independent as I
import controls
from pathlib import Path
import hashlib,json

def main():
    p=Path(__file__).resolve().parent
    seal=json.loads((p/'INDEPENDENCE.json').read_text())
    for row in seal['files']:
        raw=(p/row['path']).read_bytes()
        I.need(len(raw)==row['bytes'] and hashlib.sha256(raw).hexdigest()==row['sha256'],'complete sealed file:'+row['path'])
    actual=I.build();expected=json.loads((p/'INDEPENDENT.json').read_text())
    I.need(actual==expected,'entire independent evidence, every coefficient and Gram entry')
    controls.main()
    print(json.dumps(dict(complete_independent_evidence=True,words=56,excluded=55,exceptional_core_points=12,gram_positions=144,
        core_capacity=14,actual_face_capacity=13,seal_files=len(seal['files']),evidence_sha256=hashlib.sha256((p/'INDEPENDENT.json').read_bytes()).hexdigest()),sort_keys=True))
if __name__=='__main__':main()
