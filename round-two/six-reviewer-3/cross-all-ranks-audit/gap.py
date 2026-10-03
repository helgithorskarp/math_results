"""Literal-shell local-spine countermodel; NOT a Ramsey counterexample."""
import itertools,json,hashlib,argparse
from pathlib import Path
V=('u','v','a')+tuple('X'+str(i) for i in range(6))+('SX0','SX1','SY0','SY1','T0','T1','T2')+tuple('q'+str(i) for i in range(6))
def build():
 n={x:set() for x in V}
 def e(a,b):n[a].add(b);n[b].add(a)
 for b in V[1:11]:e('u',b)
 for b in ('v','SX0','SX1','SY0','SY1','T0','T1','T2'):e('a',b)
 for b in ('SY0','SY1')+V[16:]:e('v',b)
 for i,j in ((0,4),(4,3),(3,1),(1,2),(2,5),(5,0)):e('X'+str(i),'X'+str(j))
 for a,row in {'SX0':(3,5),'SX1':(2,4),'SY0':(1,4,5),'SY1':(0,2,3),'T0':(1,3,4,5),'T1':(1,2,4,5),'T2':(0,2,3)}.items():
  for i in row:e(a,'X'+str(i))
 for a,bs in {'SX0':('T1','T2'),'SX1':('T0','T2'),'SY0':('T1','T2'),'SY1':('T0','T1')}.items():
  for b in bs:e(a,b)
 # Fill exact root-neighbor degrees. Chosen freely; other caps may fail.
 for a in tuple('X'+str(i) for i in range(6))+('SX0','SX1'):
  need=10-len(n[a])
  for q in V[16:16+need]:e(a,q)
 for a,qs in {'SY0':(1,2),'SY1':(0,3),'T0':(0,1,3),'T1':(4,5),'T2':(0,1,2)}.items():
  for i in qs:e(a,'q'+str(i))
 violations=[];spines=[]
 for a,b in itertools.combinations(V,2):
  red=b in n[a];pages=sorted((n[a]&n[b]) if red else (set(V)-{a,b}-n[a]-n[b]));cap=3 if red else 6
  row={'pair':[a,b],'color':'red' if red else 'blue','pages':pages,'cap':cap};spines.append(row)
  if len(pages)>cap:violations.append(row)
 if n['u']!=set(V[1:11]) or len(n['a'])!=9 or any(len(n[x])!=10 for x in V[1:11] if x!='a'):raise ValueError('literal marked degree mismatch')
 # Complete fixed-pair contract directly against a separately listed set.
 free=set()
 for a in ('SY0','SY1','T0','T1','T2'):
  for b in V[3:9]:free.add(frozenset((a,b)))
 for a in V[3:16]:
  for b in V[16:]:free.add(frozenset((a,b)))
 for a,b in itertools.combinations(V[16:],2):free.add(frozenset((a,b)))
 literal=[('u',b) for b in V[1:11]]+[('a',b) for b in ('v','SX0','SX1','SY0','SY1','T0','T1','T2')]+[('v',b) for b in ('SY0','SY1')+V[16:]]+[(f'X{i}',f'X{j}') for i,j in ((0,4),(4,3),(3,1),(1,2),(2,5),(5,0))]+[('SX0','X3'),('SX0','X5'),('SX1','X2'),('SX1','X4'),('SX0','T1'),('SX0','T2'),('SX1','T0'),('SX1','T2'),('SY0','T1'),('SY0','T2'),('SY1','T0'),('SY1','T1')]
 fixedred={frozenset(z) for z in literal}
 for a,b in itertools.combinations(V,2):
  if frozenset((a,b)) not in free and (b in n[a])!=(frozenset((a,b)) in fixedred):raise ValueError('fixed-pair mismatch')
 p=next(z for z in spines if z['pair']==['SY1','T2'])
 if p['color']!='blue' or len(p['pages'])!=6 or 'X0' not in n['SY1'] or not(n['SY1']&n['T2']&set(V[16:])) or not violations:raise ValueError('local countermodel semantics')
 return {'scope':'local-spine implication only; NOT a Ramsey counterexample','rows':{a:sorted(n[a]) for a in V},'degrees':{a:len(n[a]) for a in V},'all231_spines':spines,'disputed_pair':p,'disputed_common_red':sorted(n['SY1']&n['T2']),'other_global_violations':violations,'SY1_X0_red':True,'SY1_T2_Q_overlap':sorted(n['SY1']&n['T2']&set(V[16:]))}
def main():
 ap=argparse.ArgumentParser();ap.add_argument('--output',type=Path,required=True);args=ap.parse_args();x=build();data=(json.dumps(x,sort_keys=True,separators=(',',':'))+'\n').encode();args.output.parent.mkdir(parents=True,exist_ok=True);args.output.write_bytes(data);print(json.dumps({'bytes':len(data),'sha256':hashlib.sha256(data).hexdigest(),'disputed_pair':x['disputed_pair'],'global_violations':len(x['other_global_violations'])}))
if __name__=='__main__':main()
