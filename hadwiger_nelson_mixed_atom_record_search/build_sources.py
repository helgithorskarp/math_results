from atoms import *
W=workdir();M=spindle();G=golomb();rho=M[2];rots=[ONE]
for j in range(5):rots.append(mul(rots[-1],rho))

def canon(P):
 out=[]
 for r in rots:
  Q=sorted(mul(r,p)for p in P);anchor=Q[0];Q=tuple(sub(p,anchor)for p in Q);out.append(Q)
 return min(out)

def source_pool():
 data=json.loads((W/'phase_inventory.json').read_text());groups={'GM':(G,M),'MM':(M,M),'GG':(G,G),'GGbar':(G,[K.conj(p)for p in G])};pool={}
 for name,(A,B)in groups.items():
  for rec in data[name]['records']:
   u=tuple(map(F,rec['u']));P=canon({add(a,mul(u,b))for a,b in product(A,B)})
   for cname,C in [('M',M),('G',G),('Gbar',[K.conj(g)for g in G])]:
    if len(P)*len(C)>508:continue
    if name=='MM' and cname=='M':continue # prioritize new mixed-atom supports
    original_c=cname
    Q=P
    if cname=='Gbar':Q=canon([K.conj(x)for x in P]);cname='G'
    if cname=='M':Q=min(Q,canon([K.conj(x)for x in Q]))
    key=(Q,cname);pool.setdefault(key,[]).append({'family':name,'u':rec['u'],'original_C':original_c})
 # Four-spindle architecture using its exact repeated three-factor coefficient set.
 P={ZERO}
 for _ in range(3):P={add(a,b)for a,b in product(P,M)}
 print('3M source size',len(P),flush=True)
 if len(P)*7<=508:pool.setdefault((min(canon(P),canon([K.conj(x)for x in P])),'M'),[]).append({'family':'3M','u':None})
 out=[]
 for (P,cname),orig in pool.items():
  C={'M':M,'G':G,'Gbar':[K.conj(g)for g in G]}[cname];eb=sum(norm(sub(a,b))==ONE for a,b in combinations(P,2));ec=11 if cname=='M' else 18
  out.append({'P':[[str(x)for x in p]for p in P],'C':cname,'origins':orig,'vertices':len(P)*len(C),'P_vertices':len(P),'P_edges':eb,'Cartesian_edges':eb*len(C)+ec*len(P)})
 out.sort(key=lambda z:(-z['Cartesian_edges']/z['vertices'],-z['Cartesian_edges'],json.dumps(z['P']),z['C']))
 return out
if __name__=='__main__':
 st=time.time();out=source_pool();(W/'sources.json').write_text(json.dumps(out,separators=(',',':'))+'\n');print('sources',len(out),'vertices',Counter(x['vertices']for x in out),'seconds',time.time()-st)
 print('ranking',[(i,x['C'],x['P_vertices'],x['P_edges'],x['Cartesian_edges'])for i,x in enumerate(out)][:20])
