#!/usr/bin/env python3
"""Positive radical geometry, negative radius, singular fallback and exact lookup controls."""
from pathlib import Path
from fractions import Fraction as Q
from itertools import combinations
from tempfile import TemporaryDirectory
import argparse,json,subprocess,sys
HERE=Path(__file__).resolve().parent

def norm(a):return a[0]*a[0]+3*a[1]*a[1]
def dot(a,b):return a[0]*b[0]+3*a[1]*b[1]
def sub(a,b):return tuple(x-y for x,y in zip(a,b))
def main():
 p=argparse.ArgumentParser(description=__doc__);p.add_argument('--binary-dir',type=Path,required=True);a=p.parse_args()
 H=[(-51,-17),(51,17),(57,-17),(-45,17),(3,37),(3,-31)]
 H=[tuple(Q(x,72) for x in h) for h in H]
 mids=[(Q(0),Q(0)),(Q(1,12),Q(0)),(Q(1,24),Q(1,24))];o=(Q(1,24),Q(1,72));q=Q(143,3)
 coefficients=[(-3*(m[1]-o[1]),m[0]-o[0]) for m in mids]
 incidences=0
 for i,(m,v) in enumerate(zip(mids,coefficients)):
  for h in H[2*i:2*i+2]:
   u=sub(m,h);assert norm(u)+q*norm(v)==1 and dot(u,v)==0;incidences+=1
 for i,j in combinations(range(3),2):
  u=sub(mids[i],mids[j]);v=sub(coefficients[i],coefficients[j]);assert norm(u)+q*norm(v)==1 and dot(u,v)==0
 assert all(norm(sub(x,y))!=1 for x,y in combinations(H,2))
 prime=10007;radius_scale=144**2%prime
 ms=[(0,0),(6,6),(12,0)]
 pairs=[(0,1,204,68),(4,5,0,-136),(2,3,-204,68)]
 runs=0
 with TemporaryDirectory(prefix='hn-nonfield-controls-') as tmp:
  w=Path(tmp);tri=w/'triangles.txt';tri.write_text('0 0 1 2 -1\n')
  rows=[([m[0],0,0,0,m[1],0,0,0],[[r[0],r[1]]]) for m,r in zip(ms,pairs)]
  (w/'groups.json').write_text(json.dumps([[[0,1],rows]])+'\n')
  (w/'midpoints.txt').write_text('1\n3\n'+''.join(' '.join(map(str,m))+'\n' for m,_ in rows))
  out=w/'enumerated.txt'
  subprocess.run([str(a.binary_dir/'enumerate'),str(w/'midpoints.txt'),str(out),'0'],check=True,capture_output=True)
  assert out.read_bytes()==tri.read_bytes();runs+=1
  packed=json.loads(subprocess.check_output([sys.executable,str(HERE/'packed_audit.py'),'--work',str(w)],text=True))
  assert packed['triangles']==1 and packed['all_rows_match']
  for fixture in ['positive','negative','singular']:
   ps=list(pairs)
   if fixture=='negative':ps[0]=ps[0][:2]+tuple(2*x for x in ps[0][2:])
   if fixture=='singular':ps=[r[:2]+(1,0) for r in ps]
   data=f'{prime} {radius_scale} 1\n3\n'
   for m,r in zip(ms,ps):data+=f'{m[0]} {m[1]} 1\n{r[0]} {r[1]} {r[2]%prime} {r[3]%prime}\n'
   inp=w/(fixture+'.txt');inp.write_text(data)
   for binary in ['screen','audit_screen']:
    subprocess.run([str(a.binary_dir/binary),str(inp),str(tri),str(out),'0'],check=True,capture_output=True);runs+=1
    assert len(out.read_text().splitlines())==(0 if fixture=='negative' else 1)
  (w/'bad.txt').write_text('1\n2\n'+'0 '*7+'0\n'+'0 '*7+'0\n')
  bad=subprocess.run([str(a.binary_dir/'enumerate'),str(w/'bad.txt'),str(out),'0'],capture_output=True)
  assert bad.returncode!=0
  (w/'truncated.txt').write_text('0 0 1 2')
  for binary in ['screen','audit_screen']:
   bad=subprocess.run([str(a.binary_dir/binary),str(w/'positive.txt'),str(w/'truncated.txt'),str(out),'0'],capture_output=True)
   assert bad.returncode!=0
 print(json.dumps({'radical_fixture_host_points':6,'exact_host_incidences':incidences,
  'exact_triangle_edges':3,'fixture_host_unit_edges':0,'native_positive_negative_singular_checks':6,
  'native_midpoint_fixture':True,'packed_midpoint_fixture':True,'duplicate_midpoints_rejected':True,
  'truncated_triangle_streams_rejected':2,'native_successful_runs':runs},indent=2))
if __name__=='__main__':main()
