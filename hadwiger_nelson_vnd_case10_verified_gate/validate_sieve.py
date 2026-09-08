"""Cross-language sieve controls; only an existing support is audited."""
from pathlib import Path
import json,struct,sys,hashlib,time,subprocess
import os
P=Path(os.environ.get("VND_WORKDIR",str(Path(__file__).resolve().parent/"work"))).resolve()
sys.path.insert(0,str(P))
from audit_source import norm,require
start=time.monotonic();c=json.loads((P/'SIEVE_CONSTANTS.json').read_text());p=c['prime'];s2,s3,s5=(c[k] for k in ['sqrt2','sqrt3','sqrt5'])
for n,s in [(2,s2),(3,s3),(5,s5)]:require(s*s%p==n,'square roots')
# Primality is unnecessary for a sound ring-evaluation filter, but is checked.
from math import isqrt
require(p>2 and all(p%d for d in range(2,isqrt(p)+1)),'prime')
basis=[1,s2,s3,s2*s3%p,s5,s2*s5%p,s3*s5%p,s2*s3*s5%p]
source=json.loads((P/'exact_points.json').read_text());pts=source['points'];den=source['denominator'];require(den==96,'denominator')
rows=(P/'residues.tsv').read_text().splitlines();require(list(map(int,rows[0].split()))==[64513,p,den],'header')
res=[tuple(map(int,r.split())) for r in rows[1:]]
require(len(res)==len(pts)==64513,'residue count')
require(res==[(sum(q[k]*basis[k] for k in range(8))%p,sum(q[8+k]*basis[k] for k in range(8))%p) for q in pts],'all residues')
require(2*(p-1)**2<2**63,'integer overflow bound')
reports={}
for binary,label in [('strict_sieve','release'),('strict_sieve_sanitized','sanitized')]:
 run=subprocess.run([str(P/binary),str(P/'residues.tsv'),'2000',str(P/(label+'_pilot.bin'))],capture_output=True,text=True,check=True)
 require(not run.stderr,'clean sanitizer/stderr');reports[label]=json.loads(run.stdout)
 require((P/(label+'_pilot.bin')).read_bytes()==(P/'sieve_pilot.bin').read_bytes(),'pilot stable')
actual=list(struct.iter_unpack('<II',(P/'release_pilot.bin').read_bytes()))
expected=[]
for i,(x,y) in enumerate(res[:2000]):
 for j in range(i+1,2000):
  X,Y=res[j]
  if ((x-X)**2+(y-Y)**2-den**2)%p==0:expected.append((i,j))
require(actual==expected,'all 1999000 pilot pairs modular agreement')
want=(den*den,)+(0,)*7
char0=[]
for i,a in enumerate(pts[:256]):
 for j in range(i+1,256):
  d=tuple(x-y for x,y in zip(a,pts[j]))
  if norm(d)==want:char0.append((i,j))
filtered=[]
for i,j in actual:
 if j<256 and norm(tuple(x-y for x,y in zip(pts[i],pts[j])))==want:filtered.append((i,j))
require(filtered==char0,'all 32640 pairs exact agreement')
out={'verified':True,'residues_checked':64513,'modular_pilot_pairs_checked':1999000,'exact_pilot_pairs_checked':32640,'exact_pilot_edges':len(char0),'cpp_runs':reports,'compiler':subprocess.check_output(['g++','--version'],text=True).splitlines()[0],'sanitizer':'ASan+UBSan clean on 2000 vertices','input_residue_sha256':hashlib.sha256((P/'residues.tsv').read_bytes()).hexdigest(),'elapsed_seconds':time.monotonic()-start}
(P/'sieve_controls.json').write_text(json.dumps(out,indent=2)+'\n');print(json.dumps(out,indent=2))
