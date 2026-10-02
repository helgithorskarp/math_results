#!/usr/bin/env python3
"""Serial whole audit; optional post-seal pinned author replay/comparison."""
from pathlib import Path
from hashlib import sha256
import argparse, json, sys
from reproduce import child
ROOT=Path(__file__).resolve().parent

def need(ok,msg):
    if not ok:raise RuntimeError(msg)

def main():
    p=argparse.ArgumentParser();p.add_argument('--work',type=Path,required=True);p.add_argument('--author-packet',type=Path);a=p.parse_args()
    for sealfile,key in [('first-seal.json','source_sha256'),('controls-seal.json',None)]:
        seal=json.loads((ROOT/sealfile).read_bytes())
        pins=seal[key] if key else {'controls.py':seal['controls_source_sha256']}
        for name,digest in pins.items():need(sha256((ROOT/name).read_bytes()).hexdigest()==digest,'sealed source changed: '+name)
    if (ROOT/'SOURCE_PINS.json').exists():
        for name,digest in json.loads((ROOT/'SOURCE_PINS.json').read_bytes())['files'].items():need(sha256((ROOT/name).read_bytes()).hexdigest()==digest,'published source changed: '+name)
    flags=['-O','-B']if sys.flags.optimize else ['-B'];runs={}
    raw,runs['reproduce']=child([sys.executable,*flags,ROOT/'reproduce.py','--work',a.work.resolve()])
    records={'independent':json.loads((a.work/'MATHEMATICS.json').read_bytes())}
    raw,runs['controls']=child([sys.executable,*flags,ROOT/'controls.py','--work',a.work.resolve()]);need(raw==(ROOT/'CONTROLS.json').read_bytes(),'whole sealed controls changed');records['controls']=json.loads(raw)
    if a.author_packet:
        raw,runs['compare']=child([sys.executable,*flags,ROOT/'compare.py','--work',a.work.resolve(),'--author-packet',a.author_packet.resolve()]);need(raw==(ROOT/'COMPARISON.json').read_bytes(),'whole pinned comparison changed');records['comparison']=json.loads(raw)
        # The unchanged original driver itself runs both modes, always serially.
        raw,runs['author_both_modes']=child([sys.executable,'-B',a.author_packet.resolve()/'reproduce.py','--work',a.work.resolve()/'author-replay'])
        native=json.loads(raw);need(native['checkers_completed']==2 and native['damaged_certificates_rejected_per_mode']==10,'complete original replay')
        records['native']={'complete':True,'checkers_completed':2,'semantic_damages_rejected_per_mode':10}
    raw=(json.dumps(records,sort_keys=True,separators=(',',':'))+'\n').encode();(a.work/'FINAL.json').write_bytes(raw)
    expected=ROOT/('FINAL.json'if a.author_packet else 'CORE.json')
    if expected.exists():need(raw==expected.read_bytes(),'whole final record changed')
    report={'actual_agent':'six-reviewer-4','role':'independent mathematical reviewer','complete':True,'python':sys.version.split()[0],'optimized':bool(sys.flags.optimize),'native_threads':1,'one_mathematical_job_at_a_time':True,'fixed_child_guard_seconds':20,'author_packet_replayed':bool(a.author_packet),'whole_final_bytes':len(raw),'whole_final_sha256':sha256(raw).hexdigest(),'runs':runs};(a.work/'FINAL_RUN.json').write_text(json.dumps(report,indent=2)+'\n');print(json.dumps(report,sort_keys=True))

if __name__=='__main__':main()
