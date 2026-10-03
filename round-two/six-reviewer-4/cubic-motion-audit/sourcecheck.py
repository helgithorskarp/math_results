"""Compact source census/hash gate; generated work directories ignored."""
import hashlib,json,sys
from pathlib import Path
base=Path(__file__).resolve().parent
manifest=json.loads((base/'MANIFEST.json').read_text())
expected=set(manifest['files'])|{'MANIFEST.json'}
actual={p.name for p in base.iterdir()if p.is_file()}
if actual!=expected:raise ValueError('whole source census differs')
for name,want in manifest['files'].items():
 raw=(base/name).read_bytes()
 if len(raw)!=want['bytes']or hashlib.sha256(raw).hexdigest()!=want['sha256']:raise ValueError('changed complete source '+name)
if manifest['actual_agent']!='six-reviewer-4'or manifest['role']!='independent mathematical reviewer':raise ValueError('authorship metadata')
print(json.dumps({'status':'whole compact source verified','files':len(expected),'manifest_covers_whole_bytes':True}))
