import itertools,json,time,hashlib,argparse
from pathlib import Path
X=tuple('x'+str(i) for i in range(6));SX=('sx0','sx1');SY=('sy0','sy1');T=('t0','t1','t2');V=('u','v','a')+X+SX+SY+T
C={X[0],X[1]};P={X[0],X[2],X[3]};S=set(X)-P;H=C|{X[3],X[5]};K=C|{X[2],X[4]}
cycle=((0,4),(4,3),(3,1),(1,2),(2,5),(5,0))
def frame(r=0,swap=False):
 n={x:set() for x in V}
 def e(a,b):n[a].add(b);n[b].add(a)
 for x in ('v','a')+X+SX:e('u',x)
 for x in ('v',)+SX+SY+T:e('a',x)
 for x in SY:e('v',x)
 for i,j in cycle:e(X[i],X[j])
 for j,row in enumerate(((3,5),(2,4))):
  for i in row:e(SX[j],X[i])
 for a,row in zip(SY,((T[1],T[2]),(T[0],T[1]))):
  for b in row:e(a,b)
 for a,row in zip(SX,((T[1-r],T[2]),(T[r],T[2]))):
  for b in row:e(a,b)
 # r1 is transported by leaf and SX swapping
 rows=[P,S,H,K,C]
 if swap:rows[:2]=[S,P]
 if r:
  phi={X[2]:X[3],X[3]:X[2],X[4]:X[5],X[5]:X[4]}
  rows=[{phi.get(x,x) for x in row} for row in rows]
 for a,row in zip(SY+T,rows):
  for b in row:e(a,b)
 return n

def calculate(k,typ,r=0,swap=False,role_perm=None):
 n=frame(r,swap);roles=('A0','A1','B0','B1','C0','C1');Ar={'A0','A1'};Br={'B0','B1'};Cr={'C0','C1'}
 t2={'A1','B0','B1'}|({'C0'} if k==4 else set())
 t0={'A0'}|set((('C0','C1'),('A1','C0'),('A1','C1'))[typ])
 if role_perm is not None:
  t0={role_perm.get(x,x) for x in t0};t2={role_perm.get(x,x) for x in t2}
 qr={'u':set(),'a':set(),'v':set(roles),'sy0':Ar,'sy1':Br,'t0':t0,'t1':Cr,'t2':t2}
 deg={x:10 for x in ('u','v')+X+SX};deg['a']=9
 for x in SY+T:deg[x]=len(n[x])+len(qr[x])
 rank={x:(deg[x]-len(n[x])) for x in V}
 pairs=list(itertools.combinations(V,2));cn={(a,b):len(n[a]&n[b]) for a,b in pairs}
 cap={(a,b):(3 if b in n[a] else deg[a]+deg[b]-14) for a,b in pairs}
 domains=[]
 for q in roles:
  fixed={x for x in qr if q in qr[x]};s=len(fixed&set(SY));t=len(fixed&set(T));vals=[]
  for h in range(max(0,4-s-t),4-s):
   for word in itertools.product((0,1),repeat=8):
    neighbors=fixed|{x for x,b in zip(X+SX,word) if b};dq=len(neighbors)+h
    if any(cn[a,b]+int(a in neighbors and b in neighbors)+max(0,rank[a]-int(a in neighbors)+rank[b]-int(b in neighbors)-5)>cap[a,b] for a,b in pairs):continue
    if any(len(n[a]&neighbors)+max(0,rank[a]+h-5-int(a in neighbors))>(3 if a in neighbors else deg[a]+dq-14) for a in V):continue
    vals.append({'h':h,'word':list(word),'degree':dq})
  domains.append(vals)
 target=tuple(rank[x] for x in X+SX)
 balanced=[];cuts=[]
 for tup in itertools.product(*domains):
  totals=tuple(sum(d['word'][i] for d in tup) for i in range(8))
  if totals!=target:continue
  balanced.append(tup)
  # Full known-pair contributions, without a Q graph or density hypothesis.
  pages=[]
  for a,b in pairs:
   nr=cn[a,b]+sum(int(a in (fixed_role_neighbors(q,qr)|{x for x,bit in zip(X+SX,d['word']) if bit}) and b in (fixed_role_neighbors(q,qr)|{x for x,bit in zip(X+SX,d['word']) if bit})) for q,d in zip(roles,tup))
   if nr>cap[a,b]:pages.append({'spine':[a,b],'red_common':nr,'allowed':cap[a,b],'color':'red' if b in n[a] else 'blue'})
  if not pages:raise RuntimeError('unexcluded balanced columns')
  cuts.append(pages)
 return {'type':[k,typ,r,swap], 'role_permutation':role_perm,'T0Q':sorted(t0),'T2Q':sorted(t2),'target':list(target),'ranks':rank,'degrees':deg,'known_red_rows':{a:sorted(n[a]) for a in V},'known_allowances':[{'spine':[a,b],'pages':cn[a,b],'cap':cap[a,b]} for a,b in pairs],'domains':domains,'balanced':balanced,'cuts':cuts,'completions':[]}

def fixed_role_neighbors(q,qr):
 return {a for a in qr if q in qr[a]}

def transported_word(d, mapping):
 base=dict(zip(X+SX,d['word']));out=dict(base)
 for a,b in mapping.items():out[b]=base[a]
 return {'h':d['h'],'degree':d['degree'],'word':[out[x] for x in X+SX]}

def canonical_bytes(value):
 return (json.dumps(value,sort_keys=True,separators=(',',':'))+'\n').encode()

def terminal():
 canonical={};records=[];transport=[]
 for k in (3,4):
  for typ in range(3):canonical[k,typ]=calculate(k,typ)
 # Whole labeled role coverage, rather than treating a host as symmetric.
 for k in (3,4):
  for typ in range(3):
   for r in (0,1):
    for swap in (False,True):
     for swA in (False,True):
      for swC in ((False,True) if k==4 else (False,)):
       perm={}
       if swA:perm.update({'A0':'A1','A1':'A0'})
       if swC:perm.update({'C0':'C1','C1':'C0'})
       rec=calculate(k,typ,r,swap,perm)
       # phi exchanges SY X rows; psi exchanges SX and two leaf pairs.
       maps=[]
       if swap:maps.append({X[0]:X[1],X[1]:X[0],X[2]:X[4],X[4]:X[2],X[3]:X[5],X[5]:X[3]})
       if r:maps.append({X[2]:X[3],X[3]:X[2],X[4]:X[5],X[5]:X[4],SX[0]:SX[1],SX[1]:SX[0]})
       raw=canonical[k,typ]
       roles=('A0','A1','B0','B1','C0','C1')
       for i,q in enumerate(roles):
        src=raw['domains'][i];ds=[dict(z) for z in src]
        for mp in maps:ds=[transported_word(z,mp) for z in ds]
        j=roles.index(perm.get(q,q))
        if canonical_bytes(sorted(ds,key=canonical_bytes))!=canonical_bytes(sorted(rec['domains'][j],key=canonical_bytes)):raise RuntimeError('whole-domain transport failed')
       records.append(rec);transport.append({'type':rec['type'],'permutation':perm,'full_domain_transport':True})
 # 18 labeled T-role assignments times four literal X/SX cores.
 if len(records)!=72:raise RuntimeError('incomplete role cover')
 return {'canonical':[canonical[k,i] for k in (3,4) for i in range(3)],'labeled_cases':records,'transports':transport}

def main():
 parser=argparse.ArgumentParser();parser.add_argument('--output',type=Path,required=True);args=parser.parse_args()
 evidence={'schema':1,'actual_agent':'six-reviewer-3','role':'independent mathematical reviewer','terminal':terminal()}
 args.output.parent.mkdir(parents=True,exist_ok=True);data=canonical_bytes(evidence);args.output.write_bytes(data)
 print(json.dumps({'bytes':len(data),'sha256':hashlib.sha256(data).hexdigest(),'labeled_cases':len(evidence['terminal']['labeled_cases']),'canonical_summary':[{'case':z['type'],'domains':[len(v) for v in z['domains']],'balanced':len(z['balanced']),'completions':len(z['completions'])} for z in evidence['terminal']['canonical']]}))
if __name__=='__main__':main()
