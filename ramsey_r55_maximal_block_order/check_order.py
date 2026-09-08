"""Independent count recurrence and literal order-suffix reconstruction.
Parent physical and triangle layers use their pinned independent auditors.
"""
from pathlib import Path
from itertools import combinations,product,combinations_with_replacement
from math import prod
import hashlib,json
import dependencies
HERE=Path(__file__).resolve().parent

def multiset_table(m,k):
 values=[1]+[0]*k
 for _ in range(m):
  for length in range(1,k+1):values[length]+=values[length-1]
 return values

def count_audit():
 d=dependencies.load();family=d['family'];reg=json.loads((HERE/'TASKS.json').read_text());red=multiset_table(1998,9);blue=multiset_table(1931,5);total=0;rows=[]
 for q in range(7,11):
  for r in range(5,q+1):
   n=43-4*q;a=r-1;b=q-r;value=red[a]*blue[b]
   for i,j in combinations(range(1,q),2):value*=37823 if (i<r)==(j<r) else 35714
   for _ in range(q*n):value*=15
   old=next(x for x in family.registry()['classes'] if (x['q'],x['r'])==(q,r));cores=old['core_stop'];row=reg['classes'][len(rows)]
   expected=dict(q=q,r=r,n=n,core_start=0,core_stop=cores,first_task=old['first_task'].replace('mp1','bo1'),last_task=old['last_task'].replace('mp1','bo1'),per_task=value,code_start=total,code_stop=total+cores*value,physical_variables=old['physical_variables'],input_sha256=old['input_sha256'])
   if row!=expected:raise ValueError('joint registry/count')
   total+=cores*value;rows.append((q,r))
 N=family.registry()['carrier_count']
 if reg['P']!=total or reg['parent_N']!=N or reg['tasks']!=2189178 or reg['macro_classes']!=18:raise ValueError('complete global registry')
 if not 1024*total<N or not 1939*total<N<1940*total or not total<2**759:raise ValueError('global gate')
 return dict(status='EXACT_JOINT_CARRIER_GATE_VERIFIED',P=total,N=N,ratio_lower=1939,ratio_upper=1940,strict_power_two_upper=759,tasks=2189178,macro_classes=18)

def independent_suffix(q,r,variables,base):
 new=base+1
 # Adjacent child positions, with the red/blue boundary removed.
 for block in range(1,q-1):
  if block==r-1:continue
  preceding=1
  for bit in range(15,-1,-1):
   row,col=divmod(bit,4);left=variables[row,4*block+col];right=variables[row,4*(block+1)+col]
   yield (-preceding,left,-right)
   if bit:
    yield (-new,preceding);yield (-new,-left,right);yield (-new,left,-right)
    yield (new,-preceding,left,right);yield (new,-preceding,-left,-right)
    preceding=new;new+=1

def audit_file(name,cache,path,triangles=False):
 modules=dependencies.load();old='mp1'+name[3:]
 if triangles:
  a=modules['triangle_audit'];data=a.physical(old,cache);plan=a.independent_plan(data);base=max(plan['variables'].values());q,r=data['q'],data['r'];variables=data['variables'];stream=(c for _,c in a.independent_clauses(data,plan))
 else:
  a=modules['physical_audit'];q,r,n,fixed,variables=a.physical(old,cache);base=len(variables)+1;stream=a.clauses(q,r,fixed,variables)
 count_pairs=sum(1 for i in range(1,q-1) if i!=r-1);h=hashlib.sha256();size=0;count=0;width=0
 with Path(path).open('rb') as f:
  line=f.readline();h.update(line);size+=len(line);parts=line.decode().split()
  if parts[:2]!=['p','cnf'] or len(parts)!=4 or int(parts[2])!=base+15*count_pairs:raise ValueError('header')
  def consume(stream):
   nonlocal size,count,width
   for clause in stream:
    line=f.readline();h.update(line);size+=len(line);count+=1;width=max(width,len(clause))
    if tuple(map(int,line.split()))!=clause+(0,):raise ValueError(('literal mismatch',name,count))
  consume(stream);base_clauses=count;consume(independent_suffix(q,r,variables,base))
  if count!=int(parts[3]) or count-base_clauses!=91*count_pairs or f.read(1):raise ValueError('length')
 return dict(task=name,triangles=triangles,variables=base+15*count_pairs,physical_variables=len(variables),clauses=count,ordering_comparisons=count_pairs,ordering_variables=15*count_pairs,ordering_clauses=91*count_pairs,base_variables=base,base_clauses=base_clauses,bytes=size,sha256=h.hexdigest(),max_width=width)

if __name__=='__main__':
 import argparse
 p=argparse.ArgumentParser();p.add_argument('--cache');p.add_argument('--task');p.add_argument('--cnf');p.add_argument('--triangles',action='store_true');a=p.parse_args()
 if a.cnf:
  if not a.task or not a.task.startswith('bo1-'):p.error('canonical bo1 task required')
  result=audit_file(a.task,a.cache,a.cnf,a.triangles)
 else:result=count_audit()
 print(json.dumps(result,indent=2,sort_keys=True))
