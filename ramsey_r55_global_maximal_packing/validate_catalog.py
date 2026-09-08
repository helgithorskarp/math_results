"""Reproduce all-record comparison with a separate literal C++ checker."""
from pathlib import Path
import argparse,hashlib,json,subprocess,time,sys
import catalog
HERE=Path(__file__).resolve().parent
FLAGS=['-std=c++17','-O3','-Wall','-Wextra','-Wconversion','-Wsign-conversion','-Werror']

def run(cache,scratch,sanitizers=False):
 p=Path(scratch).resolve();p.mkdir(parents=True,exist_ok=True);t=time.monotonic()
 summary=catalog.census(cache,p/'python.rows')
 if summary!=json.loads((HERE/'CATALOG_CENSUS.json').read_text()):raise ValueError('frozen census')
 py_seconds=time.monotonic()-t;compiler=subprocess.check_output(['g++','--version'],text=True).splitlines()[0]
 def cpp(flags,name):
  binary=p/name;subprocess.run(['g++',*flags,str(HERE/'check_catalog.cpp'),'-o',str(binary)],check=True)
  t=time.monotonic()
  with (p/(name+'.rows')).open('wb') as f:subprocess.run([str(binary),str(Path(cache).resolve())],stdout=f,check=True)
  raw=(p/(name+'.rows')).read_bytes()
  if raw!=(p/'python.rows').read_bytes():raise ValueError('independent catalog disagreement')
  return time.monotonic()-t
 seconds=cpp(FLAGS,'literal_checker');san_seconds=None
 if sanitizers:san_seconds=cpp([x for x in FLAGS if x!='-O3']+['-O1','-g','-fsanitize=address,undefined','-fno-omit-frame-pointer'],'sanitized_checker')
 raw=(p/'python.rows').read_bytes()
 return dict(status='EVERY_RECORD_PHYSICALLY_VERIFIED_AND_CROSS_CHECKED',records=len(raw.splitlines()),row_sha256=hashlib.sha256(raw).hexdigest(),row_bytes=len(raw),python=sys.version.split()[0],compiler=compiler,flags=FLAGS,python_seconds=py_seconds,cpp_seconds=seconds,sanitized_cpp_seconds=san_seconds)

if __name__=='__main__':
 p=argparse.ArgumentParser();p.add_argument('cache');p.add_argument('scratch');p.add_argument('--sanitizers',action='store_true');a=p.parse_args()
 print(json.dumps(run(a.cache,a.scratch,a.sanitizers),sort_keys=True))
