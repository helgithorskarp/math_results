#!/usr/bin/env python3
"""Known square/root cases, geometric positives and corrupted-certificate rejection."""
from pathlib import Path
from itertools import product
from fractions import Fraction as Q
import argparse,json,subprocess,sys,tempfile
sys.dont_write_bytecode=True
import common as C
import field as F
p=argparse.ArgumentParser();p.add_argument('--work',type=Path,required=True);a=p.parse_args()
count=0
for row in product(range(-2,3),repeat=4):
 for denominator in [1,7]:
  x=tuple(Q(v,denominator) for v in row);sq=F.mul(x,x);b=F.sqrt4(sq)
  assert b is not None and F.mul(b,b)==sq
  assert b==(x if F.sign4(x)>=0 else F.neg(x))
  assert F.sign4(x)==-F.sign4(F.neg(x)) and F.sign4(sq)==(x!=F.Z)
  count+=1
for n in [-1,2,3,5,11]:assert F.sqrt4((n,0,0,0)) is None
assert F.sqrt4((33,0,0,0))==(0,1,0,0)
assert F.sqrt4(F.L+(0,0))==(0,0,1,0)
assert F.sqrt4((0,0,1,0)) is None and F.sqrt4((0,1,0,0)) is None
assert F.sqrt4(F.Z)==F.Z
try:F.inv(F.Z)
except ZeroDivisionError:pass
else:raise AssertionError('zero inverse')
# Exact tangent, separated, non-field and field unit-circle intersections for rational chords.
for s,hasroot in [(4,True),(5,False),(2,False),(1,True)]:
 q=(Q(4-s,3*s),0,0,0);b=F.sqrt4(q)
 assert (b is not None)==hasroot
G=C.producer();R=C.reviewer()
points=[(1,0,0,0,0,0,0,0,0),(1,1,0,0,0,0,0,0,0),(2,1,0,0,0,1,0,0,0)]
assert all(G.unit(points[i],points[j]) for i in range(3) for j in range(i+1,3))
rp=[R.decode_candidate(x) for x in points]
assert all(R.unit_pair(rp[i],rp[j]) for i in range(3) for j in range(i+1,3))
alpha=(0,0,1,0,0,0,0,0);third=R.add(R.ONE,alpha)
assert R.rational_equal((third,2),rp[2])
assert not G.unit(points[0],(1,2,0,0,0,0,0,0,0))
# Each case changes only one external file; all other inputs are read-only symlinks.
# Require a specific verifier assertion to reject, so a missing file/import does not count.
base=a.work.resolve();rejections=[]
for case in ['bad_prime','false_nonsquare','bad_square','missing_pair','missing_point']:
 with tempfile.TemporaryDirectory(prefix='hn-c2-control-',dir=base.parent) as tmp:
  work=Path(tmp)
  for n in ['lengths.json','points.json','nonsquare_certificate.json','triangles.json']:(work/n).symlink_to(base/n)
  target='nonsquare_certificate.json' if case in ['bad_prime','false_nonsquare'] else 'points.json' if case=='missing_point' else 'lengths.json'
  value=json.loads((base/target).read_text())
  if case=='bad_prime':value['maps'][0][0]=11;needle='assert z*z%p'
  elif case=='false_nonsquare':
   # Set the image to a verified map under which this q is a nonzero square.
   rows=json.loads((base/'lengths.json').read_text());ix=value['rows'][0][0];q=list(map(Q,rows[ix]['q']))
   for m,(p,z,r) in enumerate(value['maps']):
    if any(v.denominator%p==0 for v in q):continue
    vv=[v.numerator*pow(v.denominator,-1,p)%p for v in q];v=(vv[0]+z*vv[1]+r*vv[2]+z*r*vv[3])%p
    if pow(v,(p-1)//2,p)==1:value['rows'][0][1]=m;break
   else:raise AssertionError('no positive-residue corruption fixture')
   needle='assert pow(value'
  elif case=='bad_square':
   row=next(x for x in value if x['root'] is not None);row['root'][0]=str(Q(row['root'][0])+1);needle='assert R.multiply(b,b)==q'
  elif case=='missing_pair':value[0]['pairs'].pop();needle='assert set(pairdict)==set(raw_norms)'
  else:value.pop();needle='assert len(pts)==len(rebuilt)'
  (work/target).unlink();C.write(work/target,value)
  result=subprocess.run([sys.executable,'-B',str(C.HERE/'audit.py'),'--work',str(work)],text=True,capture_output=True)
  if case=='bad_prime':needle='assert prime(p)'
  assert result.returncode and 'AssertionError' in result.stderr and needle in result.stderr,(case,result.stderr)
  rejections.append(case)
result={'known_squared_elements':count,'known_rational_nonsquares':5,'pure_r_and_zero_branches':True,'circle_boundary_cases':4,'positive_unit_triangle_edges':3,'corruptions_rejected':rejections}
print(json.dumps(result,indent=2))
C.write(base/'controls_result.json',result)
