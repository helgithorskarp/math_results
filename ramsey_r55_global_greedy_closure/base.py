"""Pinned access to the independently reviewed h3835 source; never mutate it."""
from pathlib import Path
import hashlib,importlib,sys
SOURCE_COMMIT='3f06352ae0735101a04afa1ba7b055736e7300f7'
MANIFEST_SHA256='1e3cafb437e30478f3961200529cb0a7bb4d5065495f8bf47f0da7589457172e'
DEFAULT=Path(__file__).resolve().parent.parent/'ramsey_r55_global_clique_packing'

def load(path=None):
 path=(DEFAULT if path is None else Path(path)).resolve();manifest=path/'SHA256SUMS'
 if hashlib.sha256(manifest.read_bytes()).hexdigest()!=MANIFEST_SHA256:raise ValueError('Reviewed parent manifest identity')
 count=0
 for line in manifest.read_text().splitlines():
  h,name=line.split('  ',1)
  if hashlib.sha256((path/name).read_bytes()).hexdigest()!=h:raise ValueError('Parent source changed: '+name)
  count+=1
 if count!=29:raise ValueError('Parent manifest cardinality')
 sys.path.insert(0,str(path))
 modules={name:importlib.import_module(name) for name in ('model','census','domains','normalize','verify_target','decode')}
 for name,module in modules.items():
  if Path(module.__file__).resolve().parent!=path:raise ValueError('Imported wrong parent module: '+name)
 return modules
