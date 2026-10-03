"""Bounded serial whole replay. Resource receipt excluded from mathematical bytes."""
from pathlib import Path
import argparse,json,subprocess,sys,os,hashlib,time
ROOT=Path(__file__).resolve().parent
ENV=os.environ.copy()
for k in ['OMP_NUM_THREADS','OPENBLAS_NUM_THREADS','MKL_NUM_THREADS','NUMEXPR_NUM_THREADS','VECLIB_MAXIMUM_THREADS','BLIS_NUM_THREADS']:ENV[k]='1'
def run(args):
 start=time.monotonic()
 r=subprocess.run([sys.executable,'-B',*(['-O']if sys.flags.optimize else []),*[str(a)for a in args]],cwd=ROOT,env=ENV,text=True,stdout=subprocess.PIPE,stderr=subprocess.PIPE,timeout=30)
 if r.returncode:raise ValueError('mathematical child failed: '+r.stderr)
 return json.loads(r.stdout),dict(argv=[str(a)for a in args],seconds=time.monotonic()-start,returncode=r.returncode)
def check_manifest():
 m=json.loads((ROOT/'MANIFEST.json').read_text())
 for name,expected in m.items():
  p=ROOT/name
  if not p.is_file()or p.stat().st_size!=expected['bytes']or hashlib.sha256(p.read_bytes()).hexdigest()!=expected['sha256']:raise ValueError('source integrity mismatch '+name)
def main():
 ap=argparse.ArgumentParser();ap.add_argument('--check',type=Path);ap.add_argument('--output',type=Path);ap.add_argument('--receipt',type=Path);ap.add_argument('--manifest',action='store_true');a=ap.parse_args()
 if a.manifest:check_manifest()
 symbolic,receipt=run([ROOT/'audit.py',ROOT/'CERTIFICATE.json']);receipts=[receipt];literal=[]
 for n,h in [(4,2),(4,3),(5,2)]:
  row,receipt=run([ROOT/'literal.py',n,h]);literal.append(row);receipts.append(receipt)
 record=dict(actual_agent='six-reviewer-4',role='independent mathematical reviewer',target='bafkreiailm2w3yvzhfqflc2nwzrnv3o2v3xuxygp5zzkk6if7aumqrylaq',symbolic=symbolic,literal=literal)
 raw=(json.dumps(record,sort_keys=True,separators=(',',':'))+'\n').encode()
 if a.check and raw!=a.check.read_bytes():raise ValueError('whole mathematical record mismatch')
 if a.output:a.output.write_bytes(raw)
 if a.receipt:a.receipt.write_text(json.dumps(dict(children=receipts,maximum_child_seconds=max(r['seconds']for r in receipts),serial=1,threads=1,child_guard_seconds=30,wrapper_guard_seconds=45,source_integrity_checked=a.manifest),indent=2)+'\n')
 sys.stdout.buffer.write(raw)
if __name__=='__main__':main()
