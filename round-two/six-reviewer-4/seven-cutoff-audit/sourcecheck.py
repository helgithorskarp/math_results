"""Whole independent publication-source gate; no math imports."""
import hashlib,json,sys,tempfile
from pathlib import Path
def need(ok,why):
 if not ok:raise ValueError(why)
def check(root):
 m=json.loads((root/'MANIFEST.json').read_text());actual={p.name for p in root.iterdir()if p.is_file()and not p.name.endswith('.pyc')}
 need(actual==set(m['files'])|{'MANIFEST.json'},'exact compact source census')
 for name,w in m['files'].items():
  raw=(root/name).read_bytes();need(len(raw)==w['bytes']and hashlib.sha256(raw).hexdigest()==w['sha256'],'whole source '+name)
 p=json.loads((root/'PROVENANCE.json').read_text())
 for name,w in p['primary_files'].items():need(m['files'][name]==w,'primary seal '+name)
 return dict(files=len(actual),bytes=sum((root/n).stat().st_size for n in actual),whole_source=True,primary_files=len(p['primary_files']),primary_seal_unchanged=True)
def controls(root):
 import shutil
 rejected=[]
 with tempfile.TemporaryDirectory()as t:
  base=Path(t)/'base';shutil.copytree(root,base,ignore=shutil.ignore_patterns('work','__pycache__'))
  for name,damage in [('changed-one-source-byte',lambda d:(d/'model.py').write_bytes((d/'model.py').read_bytes()+b'\n')),('missing-whole-input',lambda d:(d/'INPUT.json').unlink()),('unrelated-added-source',lambda d:(d/'unrelated.txt').write_text('extra'))]:
   dest=Path(t)/name;shutil.copytree(base,dest);damage(dest)
   try:check(dest)
   except(ValueError,FileNotFoundError):rejected.append(name)
   else:raise ValueError('accepted damage '+name)
 need(len(rejected)==3,'all source damages')
 return dict(whole_source=check(root),source_damages=rejected)
if __name__=='__main__':
 root=Path(__file__).resolve().parent
 print(json.dumps(controls(root)if '--controls'in sys.argv else check(root),sort_keys=True))
