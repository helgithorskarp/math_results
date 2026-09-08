"""Acquire hash-pinned author inputs and prepare residues, without a SAT query."""
from pathlib import Path
from urllib.request import urlopen
import json,hashlib,zipfile,sys
import os
P=Path(os.environ.get("VND_WORKDIR",str(Path(__file__).resolve().parent/"work"))).resolve()

def require(x,msg):
 if not x:raise ValueError(msg)
def main():
 mode=sys.argv[1] if len(sys.argv)==2 else ''
 if mode=='fetch':
  data=json.loads((P/'UPSTREAM_INPUTS.json').read_text())
  for entry in data['files']:
   out=P/entry['local_file']
   if out.exists():raw=out.read_bytes()
   else:
    with urlopen(entry['url'],timeout=120) as r:raw=r.read()
   require(len(raw)==entry['bytes'] and hashlib.sha256(raw).hexdigest()==entry['sha256'],'upstream byte identity '+entry['local_file'])
   if not out.exists():out.write_bytes(raw)
  with zipfile.ZipFile(P/'source_graph.zip') as z:
   require(z.namelist()==['s2_graph10.vtx'],'only expected archive member')
   raw=z.read('s2_graph10.vtx');require(len(raw)==8514579,'coordinate byte count')
  out=P/'source_graph.vtx'
  if out.exists():require(out.read_bytes()==raw,'existing coordinates')
  else:out.write_bytes(raw)
  print('INPUTS_VERIFIED')
 elif mode=='residues':
  c=json.loads((P/'SIEVE_CONSTANTS.json').read_text());p=c['prime'];s2,s3,s5=(c[k] for k in ['sqrt2','sqrt3','sqrt5'])
  for n,s in [(2,s2),(3,s3),(5,s5)]:require(s*s%p==n,'square root')
  basis=[1,s2,s3,s2*s3%p,s5,s2*s5%p,s3*s5%p,s2*s3*s5%p]
  source=json.loads((P/'exact_points.json').read_text());pts=source['points'];den=source['denominator'];require(len(pts)==64513 and den==96,'exact source dimensions')
  rows=[f'{len(pts)} {p} {den}']
  for q in pts:
   x=sum(q[k]*basis[k] for k in range(8))%p;y=sum(q[k+8]*basis[k] for k in range(8))%p
   rows.append(f'{x} {y}')
  raw=('\n'.join(rows)+'\n').encode();require(hashlib.sha256(raw).hexdigest()==c['residue_file_sha256'],'residue identity')
  (P/'residues.tsv').write_bytes(raw);print('RESIDUES_VERIFIED')
 else:raise SystemExit('usage: reproduce_inputs.py fetch|residues')
if __name__=='__main__':main()
