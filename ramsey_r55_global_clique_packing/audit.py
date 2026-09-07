"""Independent graph-level interface checks and exact full-formula audits."""
from collections import Counter
from itertools import combinations
from pathlib import Path
from math import comb
import argparse,hashlib,json,random,time
import census,domains,model,index_family,normalize,decode,verify_target,check_domains

FULL_BRANCHES=[[5,0,0],[5,4,3],[6,2,1],[6,2,2],[7,0,1],[7,4,2]]

def layout(branch):
 r,s,t=branch;types=['R4']*r+['B4']*(7-r)+['R3']*s+['B3']*(4-s)+[('B3','E3','P3','R3')[t]]
 blocks=[list(range(4*i,4*i+4)) for i in range(7)]+[list(range(28+3*i,31+3*i)) for i in range(5)]
 fixed={};owner={v:i for i,b in enumerate(blocks) for v in b}
 for kind,b in zip(types,blocks):
  bits=check_domains.ATOMS[kind][1]
  for k,pair in enumerate(combinations(b,2)):fixed[pair]=(bits>>k)&1
 return types,blocks,owner,fixed

def direct(data):
 types,blocks,owner,fixed=layout(data['branch']);matrix=[[0]*43 for _ in range(43)]
 for (u,v),x in fixed.items():matrix[u][v]=matrix[v][u]=x
 for x,(i,j) in zip(data['matrices'],combinations(range(12),2)):
  k=0
  for u in blocks[i]:
   for v in blocks[j]:matrix[u][v]=matrix[v][u]=(x>>k)&1;k+=1
 return matrix

def graph(matrix):
 n=len(matrix);bits=sum(matrix[u][v]<<k for k,(u,v) in enumerate(combinations(range(n),2)))
 return {'n':n,'red_hex':format(bits,f'0{(comb(n,2)+3)//4}x')}

def clique_count(matrix):
 n=len(matrix);universe=(1<<n)-1;redrows=[sum(x<<v for v,x in enumerate(row)) for row in matrix]
 def count(rows,vertices,k):
  if k==0:return 1
  answer=0
  while vertices.bit_count()>=k:
   bit=vertices&-vertices;vertices^=bit;v=bit.bit_length()-1
   answer+=count(rows,vertices&rows[v],k-1)
  return answer
 red=count(redrows,universe,5);blue=count([universe^(1<<v)^row for v,row in enumerate(redrows)],universe,5)
 return {'red_fives':red,'blue_fives':blue}

def fixture(branch):
 packing=model.Packing(branch);rng=random.Random(12000+100*branch[0]+10*branch[1]+branch[2])
 return {'branch':branch,'matrices':[rng.choice(packing.matrix_domain(i,j)) for i,j in packing.matrix_pairs]}

def stencil_counts(counts):
 _,blocks,owner,fixed=layout([5,0,0]);inside=sorted(fixed);positions={p:k for k,p in enumerate(inside)};stencils=Counter();two=0
 for q in combinations(range(43),5):
  mask=sum(1<<positions[p] for p in combinations(q,2) if p in positions);stencils[mask]+=1
  two+=len({owner[v] for v in q})<=2
 if two!=1971 or sum(stencils.values())!=comb(43,5):raise ValueError('physical subset census')
 for row in counts['branches']:
  _,_,_,fixed=layout(row['branch']);ones=sum(c<<positions[p] for p,c in fixed.items());red=blue=0
  for mask,multiplicity in stencils.items():
   if mask&ones==mask:red+=multiplicity
   if mask&ones==0:blue+=multiplicity
  ordering=3360 if row['branch'][2] in (0,3) else 3240
  if row['root_order_clauses']!=ordering or (red,blue)!=(row['red_clauses'],row['blue_clauses']) or row['cnf_variables']!=847 or row['cnf_clauses']!=red+blue+ordering+1:raise ValueError('all-branch clause census')
 return {'physical_five_sets':sum(stencils.values()),'internal_stencils':len(stencils),'two_atom_five_sets':two,'branches_checked':60}

def independent_comparisons(types):
 for j,kind in enumerate(types[1:],1):
  pairs=[(0,1)] if kind=='E3' else [(1,2)] if kind=='P3' else list(zip(range(check_domains.ATOMS[kind][0]-1),range(1,check_domains.ATOMS[kind][0])))
  for a,b in pairs:yield j,a,b

def root_semantics():
 seen=set();cases=0
 for t in range(4):
  p=model.Packing([5,2,t]);clauses=iter(p.root_clauses())
  for j,a,b in independent_comparisons(p.types):
   group=[next(clauses) for _ in range(120)];key=(p.types[j],a,b)
   if key in seen:continue
   seen.add(key)
   for x in range(16):
    for y in range(16):
     values={p.variables[p.blocks[0][i],p.blocks[j][c]]:bool(v>>i&1) for c,v in [(a,x),(b,y)] for i in range(4)}
     result=all(any(values[abs(l)]==(l>0) for l in clause) for clause in group)
     if result!=(x>=y):raise ValueError('root comparator truth table')
     cases+=1
  if list(clauses):raise ValueError('unexpected ordering clauses')
 return {'atom_comparators':len(seen),'signature_assignments':cases}

def controls(counts):
 rng=random.Random(52019);boundary=0;offset=0;transports=0;physical=0;clause_cases=0;fixtures=[]
 for row in counts['branches']:
  for k in [offset,offset+row['count']//2,offset+row['count']-1]:
   data=index_family.unrank(k)
   if index_family.rank(data)!=k or data['branch']!=row['branch']:raise ValueError('global index bijection')
   boundary+=1
  offset+=row['count'];data=fixture(row['branch']);p=model.Packing(row['branch']);expected=direct(data);actual=verify_target.adjacency(p.graph(data['matrices']))
  if actual!=expected:raise ValueError('physical graph assembly')
  types,blocks,owner,fixed=layout(row['branch'])
  for i,j in combinations(range(12),2):
   union=blocks[i]+blocks[j];a=[[actual[u][v] for v in union] for u in union]
   if any(clique_count(a).values()):raise ValueError('pair domain did not survive physical realization')
  violations=clique_count(actual)
  if not sum(violations.values()):raise ValueError('Unexpected good43: independently certify before continuation')
  fixtures.append({'branch':row['branch'],**violations,'graph_sha256':hashlib.sha256((json.dumps(p.graph(data['matrices']),sort_keys=True)+'\n').encode()).hexdigest()})
  # Transport every physical edge under arbitrary vertex names and a supplied
  # verified packing; no assumption that the input graph is already a target.
  order=list(range(43));rng.shuffle(order);inverse={v:i for i,v in enumerate(order)}
  raw=[[actual[order[u]][order[v]] for v in range(43)] for u in range(43)]
  supplied=[[inverse[v] for v in block] for block in blocks]
  for b in supplied:rng.shuffle(b)
  a=supplied[:7];b=supplied[7:11];rng.shuffle(a);rng.shuffle(b);supplied=a+b+supplied[11:]
  norm=normalize.normalize(graph(raw),supplied);restored=verify_target.adjacency(norm['graph'])
  if norm['parameters']['branch']!=row['branch'] or not norm['pair_domains_hold']:raise ValueError('normal form branch/domain')
  for u,v in combinations(range(43),2):
   if restored[u][v]!=raw[norm['new_to_old'][u]][norm['new_to_old'][v]]:raise ValueError('normalization transport')
   physical+=1
  transports+=1
  # Exhaust all free assignments on representative five-set placements, including
  # triples in the mixed last atom and five distinct atoms.
  for q in [(0,1,2,3,4),(0,1,4,5,8),(0,4,8,12,16),(28,29,30,40,41),(28,31,40,41,42)]:
   qs=list(combinations(q,2));vs=[pair for pair in qs if pair not in fixed];clauses=list(p.five_clauses(q))
   for mask in range(1<<len(vs)):
    colors=dict(fixed);colors.update({pair:(mask>>k)&1 for k,pair in enumerate(vs)})
    values={p.variables[pair]:bool(colors[pair]) for pair in vs}
    got=all(any(values[abs(x)]==(x>0) for x in c) for c in clauses)
    cs=[colors[pair] for pair in qs];wanted=any(cs) and not all(cs)
    if got!=wanted:raise ValueError('small physical clause semantics')
    clause_cases+=1
 if offset!=counts['retained_rooted_family']:raise ValueError('index interval endpoints')
 p=model.Packing([5,0,0]);zero=[0]*66;base=int(p.graph(zero,False)['red_hex'],16);coordinate=0
 for slot,(i,j) in enumerate(p.matrix_pairs):
  for a,u in enumerate(p.blocks[i]):
   for b,v in enumerate(p.blocks[j]):
    xs=zero.copy();xs[slot]=1<<(a*len(p.blocks[j])+b)
    changed=int(p.graph(xs,False)['red_hex'],16)^base
    wanted=1<<list(combinations(range(43),2)).index((u,v))
    if changed!=wanted:raise ValueError('matrix/physical coordinate')
    coordinate+=1
 negatives=0
 def rejects(function,*args):
  nonlocal negatives
  try:function(*args)
  except ValueError:negatives+=1
  else:raise ValueError('invalid input accepted')
 for k in [-1,counts['retained_rooted_family'],True]:rejects(index_family.unrank,k)
 for branch in [[4,0,0],[5,5,0],[5,0,4],[True,0,0]]:rejects(model.Packing,branch)
 sample=fixture([5,0,0])
 for d in [{**sample,'extra':0},{'branch':sample['branch'],'matrices':sample['matrices'][:-1]},{'branch':sample['branch'],'matrices':[65535]+sample['matrices'][1:]}]:rejects(model.parse,d)
 rejects(verify_target.adjacency,{'n':42,'red_hex':'0'*216});rejects(verify_target.adjacency,{'n':43,'red_hex':'f'*226})
 actual=direct(sample);mask=int(graph(actual)['red_hex'],16);vals={1:True}
 for k,pair in enumerate(combinations(range(43),2)):
  if pair in p.variables:vals[p.variables[pair]]=bool(mask>>k&1)
 fake='s SATISFIABLE\nv '+' '.join(str(v if c else -v) for v,c in sorted(vals.items()))+' 0\n'
 for text in ['s UNKNOWN\n','s SATISFIABLE\nv 1 0\n',fake.replace('v 1 ','v -1 ',1),fake]:rejects(decode.decode,[5,0,0],text)
 allred=[[int(i!=j) for j in range(43)] for i in range(43)];g=normalize.normalize(graph(allred))
 if g['parameters']['branch']!=[7,4,3] or g['pair_domains_hold']:raise ValueError('greedy packing control')
 allblue=[[0]*43 for _ in range(43)];rejects(normalize.normalize,graph(allblue))
 positive=verify_target.count(json.loads(Path(__file__).with_name('control42.json').read_text()),False)
 if positive['red_fives'] or positive['blue_fives']:raise ValueError('positive42')
 return {'status':'VERIFIED_GLOBAL_PACKING_INTERFACE','root_comparator_controls':root_semantics(),'boundary_indices':boundary,'physical_clause_assignments':clause_cases,'normalization_transports':transports,'transported_edges':physical,'matrix_coordinate_checks':coordinate,'negative_controls':negatives,'greedy_packing_controls':2,'positive42':positive,'fixtures':fixtures}

def full_cnf(branch,path):
 p=model.Packing(branch);record=p.write(path);data=fixture(branch);matrix=direct(data);types,blocks,owner,fixed=layout(branch)
 variables={pair:k+2 for k,pair in enumerate(pair for pair in combinations(range(43),2) if pair not in fixed)}
 # Closed physical pair ordering differs from the source's matrix-state order.
 checked=0;root_checked=0;red=blue=0
 with Path(path).open() as f:
  if f.readline().strip()!=f"p cnf 847 {record['clauses']}" or f.readline().strip()!='1 0':raise ValueError('CNF header/constant')
  for j,a,b in independent_comparisons(types):
   for x,y in combinations(range(16),2):
    expected=[]
    for column,value in [(a,x),(b,y)]:
     for row in range(4):expected.append((-1 if value>>row&1 else 1)*variables[blocks[0][row],blocks[j][column]])
    if list(map(int,f.readline().split()))!=expected+[0]:raise ValueError('root order clause content')
    root_checked+=1
  for q in combinations(range(43),5):
   pairs=list(combinations(q,2));values=[matrix[u][v] for u,v in pairs];red+=all(values);blue+=not any(values)
   for color in (1,0):
    required=[];skip=False
    for pair in pairs:
     if pair in fixed:
      if fixed[pair]!=color:skip=True;break
     else:required.append((-1 if color else 1)*variables[pair])
    if skip:continue
    line=list(map(int,f.readline().split()))
    if line!=required+[0]:raise ValueError(('physical clause content',branch,q,color))
    checked+=1
  if f.read():raise ValueError('extra CNF clauses')
 if root_checked!=record['root_order_clauses'] or checked+root_checked+1!=record['clauses'] or {'red_fives':red,'blue_fives':blue}!=clique_count(matrix):raise ValueError('full physical clause/graph census')
 return {**record,'physical_clauses_checked':checked,'root_order_clauses_checked':root_checked,'fixture_red_fives':red,'fixture_blue_fives':blue}

if __name__=='__main__':
 p=argparse.ArgumentParser();p.add_argument('--work',required=True);p.add_argument('--output',required=True);p.add_argument('--controls-only',action='store_true');p.add_argument('--existing-controls');a=p.parse_args();work=Path(a.work);work.mkdir(exist_ok=True)
 counts=json.loads(Path(__file__).with_name('COUNTS.json').read_text());t=time.monotonic()
 controls_result=json.loads(Path(a.existing_controls).read_text())['controls'] if a.existing_controls else {'stencils':stencil_counts(counts),'interfaces':controls(counts)}
 result={'status':'VERIFIED_PACKING_CONTROLS_ONLY' if a.controls_only else 'VERIFIED_UNCONDITIONAL_GLOBAL_PACKING_HANDOFF','controls':controls_result}
 if not a.controls_only:
  result['cnfs']=[]
  for branch in FULL_BRANCHES:
   print('Checking full43 branch',branch,flush=True);result['cnfs'].append(full_cnf(branch,work/('branch-'+'-'.join(map(str,branch))+'.cnf')))
 Path(a.output).write_text(json.dumps(result,indent=2,sort_keys=True)+'\n');print(json.dumps({'seconds':time.monotonic()-t,'status':result['status']}))
