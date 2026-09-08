"""Identity-checked imports of immutable preceding source packages."""
from pathlib import Path
from functools import lru_cache
import hashlib,importlib,importlib.util,sys,json
HERE=Path(__file__).resolve().parent

@lru_cache(maxsize=None)
def load():
 records=json.loads((HERE/'DEPENDENCIES.json').read_text())
 for row in records:
  path=HERE.parent/row['directory'];raw=(path/'SHA256SUMS').read_bytes()
  if hashlib.sha256(raw).hexdigest()!=row['manifest_sha256']:raise ValueError('dependency manifest')
  entries=raw.decode().splitlines()
  if len(entries)!=row['manifest_entries']:raise ValueError('dependency count')
  for line in entries:
   sha,name=line.split('  ',1)
   if hashlib.sha256((path/name).read_bytes()).hexdigest()!=sha:raise ValueError('changed dependency '+name)
 out={}
 for name,dirname in [('family','ramsey_r55_global_maximal_packing'),('factor','ramsey_r55_triangle_interface')]:
  path=HERE.parent/dirname;sys.path.insert(0,str(path));module=importlib.import_module(name)
  if Path(module.__file__).resolve().parent!=path.resolve():raise ValueError('wrong module')
  out[name]=module
 for name,dirname in [('physical_audit','ramsey_r55_global_maximal_packing'),('triangle_audit','ramsey_r55_triangle_interface')]:
  path=HERE.parent/dirname/'audit.py';spec=importlib.util.spec_from_file_location('_block_order_'+name,path);module=importlib.util.module_from_spec(spec);spec.loader.exec_module(module);out[name]=module
 return out
