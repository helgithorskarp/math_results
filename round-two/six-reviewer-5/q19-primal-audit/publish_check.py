"""Full publication integrity; optional restoration of the paid mathematical packet."""
import hashlib
import json
import os
from pathlib import Path
import subprocess
import sys
import tempfile

PRIMARY={'COEFFICIENTS.json','PROOF.md','README.md','RECORD.json','REVIEW.md','SOURCE.json','literal.py','primal.py','validate.py'}
EXPECTED=PRIMARY|{'SHA256SUMS','.gitignore','EDITORIAL.json','VALIDATION.json','publish_check.py'}
BASELINE='668f10ff3720c1d7f0e8d1414a82f02dce4bc3cbcc490448d1ba18458fd20c82'
RECORD='1ddf622a592e963a5f98a8b755a748c4fb3490f85671b5bf79d342411efc6aa7'

def need(ok,message):
    if not ok:raise ValueError(message)

def digest(raw):return hashlib.sha256(raw).hexdigest()

def check(root):
    manifest={}
    for line in (root/'MANIFEST.sha256').read_text().splitlines():
        sha,name=line.split('  ',1)
        need(len(sha)==64 and all(c in '0123456789abcdef' for c in sha),'digest syntax')
        need(name not in manifest and '/' not in name and name!='MANIFEST.sha256','unique sealed file names')
        p=root/name
        need(p.is_file() and not p.is_symlink(),'regular public source')
        need(digest(p.read_bytes())==sha,'whole public source seal: '+name)
        manifest[name]=sha
    need(set(manifest)==EXPECTED,'entire intended compact public source')
    need({p.name for p in root.iterdir()}==EXPECTED|{'MANIFEST.sha256'},'exact entire public census')
    edits=json.loads((root/'EDITORIAL.json').read_text())
    need({r['name'] for r in edits['baseline']}==PRIMARY,'full nine-file primary census')
    need(set(edits['changes'])=={'README.md','REVIEW.md'},'only disclosed publication words')
    need(set(edits['unchanged'])==PRIMARY-{'README.md','REVIEW.md'},'every unchanged mathematical input/proof/program/record')
    old_manifest='';restored={}
    for row in edits['baseline']:
        name=row['name'];actual=(root/name).read_bytes();raw=actual
        if name in edits['changes']:
            text=raw.decode()
            for change in reversed(edits['changes'][name]):
                need(text.count(change['after'])==1,'exact reverse publication occurrence')
                text=text.replace(change['after'],change['before'])
            raw=text.encode()
        need(len(raw)==row['bytes'] and digest(raw)==row['sha256'],'ENTIRE paid primary restoration: '+name)
        if name in edits['unchanged']:need(raw==actual,'entire unchanged mathematical source')
        restored[name]=raw
        old_manifest+=row['sha256']+'  '+name+'\n'
    need(digest(old_manifest.encode())==edits['baseline_manifest_sha256']==BASELINE,'fixed entire private source seal')
    need((root/'SHA256SUMS').read_bytes()==old_manifest.encode(),'whole historical primary seal')
    restored['SHA256SUMS']=old_manifest.encode()
    record=(root/'RECORD.json').read_bytes();validation=json.loads((root/'VALIDATION.json').read_text())
    need(len(record)==validation['whole_record_bytes']==11979,'entire mathematical record length')
    need(digest(record)==validation['whole_record_sha256']==RECORD,'entire mathematical record hash')
    need(validation['status']=='PASS' and validation['positive_replays']==4 and validation['actual_semantic_rejections']==44 and validation['actual_preimport_source_rejections']==10,'paid mathematical provenance')
    need(len(validation['positive_runs'])==4 and all(r['exit_code']==0 and r['whole_record_sha256']==RECORD and r['whole_record_bytes']==11979 for r in validation['positive_runs']),'four full mathematical records')
    need('## Strengthening and improvement opportunities' in (root/'REVIEW.md').read_text(),'required review section')
    result=dict(actual_agent='six-reviewer-5',role='independent mathematical reviewer',public_files=15,
        entire_private_math_and_record_unchanged=True,entire_editorial_reversal_exact=True,
        original_source_manifest_sha256=BASELINE,whole_record_bytes=11979,whole_record_sha256=RECORD,closed_math_replays=0)
    return result,restored

if __name__=='__main__':
    need(sys.argv[1:] in ([],['--math']),'declared integrity or exact mathematical reproduction')
    result,restored=check(Path(__file__).resolve().parent)
    print(json.dumps(result,sort_keys=True,indent=2),flush=True)
    if sys.argv[1:]:
        env={**os.environ,**{k:'1' for k in ('OMP_NUM_THREADS','OPENBLAS_NUM_THREADS','MKL_NUM_THREADS','NUMEXPR_NUM_THREADS','BLIS_NUM_THREADS','VECLIB_MAXIMUM_THREADS')}}
        with tempfile.TemporaryDirectory(prefix='q19-primary-reproduction-') as tmp:
            for name,raw in restored.items():(Path(tmp)/name).write_bytes(raw)
            try:r=subprocess.run([sys.executable,'-B','validate.py'],cwd=tmp,env=env,timeout=150)
            except subprocess.TimeoutExpired:raise RuntimeError('fixed150s driver guard; incomplete reproduction gives no mathematical conclusion')
            if r.returncode:raise SystemExit(r.returncode)
