"""Append proved global cuts to a complete classical Schur-six CNF."""
import argparse
import hashlib
import itertools
from pathlib import Path
from pysat.card import CardEnc,EncType
from pysat.formula import CNF

p=argparse.ArgumentParser()
p.add_argument('--base-mode',choices=('plain','rgs'),default='rgs')
p.add_argument('--base',type=Path,required=True)
p.add_argument('--branch',type=int,choices=(0,1,2,3),default=0)
p.add_argument('--distance',action='store_true')
p.add_argument('--splitting',action='store_true')
p.add_argument('--first-use',action='store_true')
p.add_argument('--out',type=Path,required=True)
a=p.parse_args()

def x(v,c):return 6*(v-1)+c
BASE_SHA={'plain':'fd6503a79cfeb53c614fe436669f192e81416b6e7292069938cf607f41b070e2',
          'rgs':'332e4b211a672836c68320f9403b0454462a96df2071aefcc2a72f809820eb7c'}
assert hashlib.sha256(a.base.read_bytes()).hexdigest()==BASE_SHA[a.base_mode]
assert not (a.first_use and a.branch==0)
base=CNF(from_file=str(a.base))
assert (base.nv,len(base.clauses))==((3222,441145) if a.base_mode=='plain' else (5907,451879))
clauses=list(base.clauses)
top=base.nv
assert not (a.base_mode=='rgs' and (a.branch or a.first_use))
if a.branch:
 clauses.extend([[x(2,2)],[x(537,a.branch)]])
if a.distance:
 fs_file=Path(__file__).resolve().parent.parent/'schur_s6_fredricksen_sweet_distance/baseline.txt'
 assert hashlib.sha256(fs_file.read_bytes()).hexdigest()=='2fdf85110de782426dd5deccfa7244f182441fda9870db64ba8e4eea7e3d600d'
 fs=fs_file.read_text().strip()
 assert len(fs)==536
 mismatches=[-x(v,int(c)) for v,c in enumerate(fs,1)]
 card=CardEnc.atleast(lits=mismatches,bound=54,top_id=top,encoding=EncType.totalizer)
 clauses.extend(card.clauses)
 top=card.nv
 print('distance_cut','vars',top,'clauses',len(card.clauses),flush=True)
if a.splitting:
 w_file=Path(__file__).resolve().parent.parent/'schur_s6_external_class_trade/seed537.txt'
 assert hashlib.sha256(w_file.read_bytes()).hexdigest()=='58c26704225562a6cde8346f0febe1e09f5604c18f9ec0397e8bf16b3e3497b3'
 w=w_file.read_text().strip()
 assert len(w)==537
 groups=[[v for v,c in enumerate(w,1) if c==str(i)] for i in range(1,7)]
 assert [len(g) for g in groups]==[93,163,119,35,63,64]
 selector=[]
 for group in groups:
  top+=1;s=top;selector.append(s)
  r=group[0]
  for c in range(1,7):
   clauses.append([-s,-x(r,c)]+[-x(v,c) for v in group if v!=r])
 for subset in itertools.combinations(selector,3):clauses.append(list(subset))
 print('splitting_cut','vars',top,'groupsizes',[len(g) for g in groups],
       'extra_clauses',56,flush=True)
if a.first_use:
 # Within branch 3, the labels 4,5,6 can be permuted freely. In the
 # other branches, labels 3,4,5,6 can be permuted freely. Order their first
 # appearances; a colour may also be absent.
 first=4 if a.branch==3 else 3
 seen={}
 for c in range(first,6):
  for v in range(1,538):
   top+=1
   seen[c,v]=top
   old=seen.get((c,v-1))
   # seen[c,v] iff seen[c,v-1] or x(v,c).
   if old is None:
    clauses.extend([[-x(v,c),top],[-top,x(v,c)]])
   else:
    clauses.extend([[-old,top],[-x(v,c),top],[-top,old,x(v,c)]])
 for c in range(first+1,7):
  for v in range(1,538):
   old=seen.get((c-1,v-1))
   clauses.append([-x(v,c),old] if old is not None else [-x(v,c)])
 print('first_use','vars',top,'first',first,flush=True)
with a.out.open('w',encoding='ascii',newline='\n') as stream:
 stream.write(f'p cnf {top} {len(clauses)}\n')
 for clause in clauses:stream.write(' '.join(map(str,clause))+' 0\n')
print('out',a.out,'vars',top,'clauses',len(clauses),
      'sha256',hashlib.sha256(a.out.read_bytes()).hexdigest(),flush=True)
