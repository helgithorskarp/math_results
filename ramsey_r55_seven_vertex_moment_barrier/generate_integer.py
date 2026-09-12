from generate_base import *

def poly_values(roots,sgn=1):
 vals=[]
 for t in range(len(roots)+1):
  v=sgn
  for r in roots:v*=t-r
  vals.append(v)
 out=[]
 while vals:
  out.append(vals[0]);vals=[b-a for a,b in zip(vals,vals[1:])]
 return out

def augment(graphs,n=43,k=7):
 full=(1<<comb(k,2))-1;roots=list(range(18,25));polys=[]
 for d in roots:
  rs=[e for e in roots if e!=d];sign=1
  for e in rs:sign*=1 if d>e else -1
  polys.append(('degree_indicator',d,poly_values(rs,sign)))
 books=[]
 for zeros in combinations(range(11),5):
  def ev(t):
   x=1
   for z in zeros:x*=t-z
   return x
  values=[ev(t) for t in range(11)]
  if all(x>=0 for x in values):books.append((zeros,1))
  elif all(x<=0 for x in values):books.append((zeros,-1))
 for zeros,sign in books:polys.append(('book_support',list(zeros),poly_values(zeros,sign)))
 we={s:10*comb(n-2,s)//comb(k-2,s) for s in range(6)}
 wv={s:60*comb(n-1,s)//comb(k-1,s) for s in range(7)}
 vf,vfs,_=canon_table(3,[(1,2)]);vi={f:i for i,f in enumerate(vfs)}
 Qd=[np.zeros((len(graphs),6,6),dtype=np.int64) for j in range(18,24)]
 Qb=[np.zeros((len(graphs),4,4),dtype=np.int64) for j in range(10)]
 rows=np.zeros((len(polys),len(graphs)),dtype=np.int64)
 for g,mask in enumerate(graphs):
  dm=[0]*7;bm=[0]*6
  for m in (mask,full^mask):
   a=adj(k,m)
   for u in range(k):
    d=a[u].bit_count()
    for s in range(7):dm[s]+=comb(d,s)*wv[s]
    pairs=list(combinations([v for v in range(k) if v!=u],2));pm=[sum(1<<t for t in A) for A in pairs];flags=[vi[int(vf[induced(a,[u]+list(A))])] for A in pairs]
    for x,A in enumerate(pm):
     for y,B in enumerate(pm):
      U=A|B;s=U.bit_count();inside=(a[u]&U).bit_count();extra=d-inside
      for j in range(18,24):
       aa=inside-j;coeff=aa*(aa-1)*wv[s]+2*aa*extra*wv[s+1]+extra*(extra-1)*wv[s+2]
       Qd[j-18][g,flags[x],flags[y]]+=coeff
   for u,v in combinations(range(k),2):
    if not a[u]>>v&1:continue
    common=a[u]&a[v];q=common.bit_count()
    for s in range(6):bm[s]+=comb(q,s)*we[s]
   for u in range(k):
    for v in range(k):
     if u==v or not a[u]>>v&1:continue
     outside=[w for w in range(k) if w not in (u,v)];common=a[u]&a[v];q=common.bit_count()
     flags={w:((a[u]>>w)&1)+2*((a[v]>>w)&1) for w in outside}
     for x in outside:
      for y in outside:
       U=(1<<x)|(1<<y);s=U.bit_count();inside=(common&U).bit_count();extra=q-inside
       for j in range(10):
        aa=inside-j;coeff=aa*(aa-1)*we[s]+2*aa*extra*we[s+1]+extra*(extra-1)*we[s+2]
        Qb[j][g,flags[x],flags[y]]+=coeff
  for i,(kind,label,cs) in enumerate(polys):rows[i,g]=sum(c*m for c,m in zip(cs,dm if kind=='degree_indicator' else bm))
 return rows,Qd+Qb,polys
if __name__=='__main__':
 z=np.load(P/'M10_sevendeck.npz');graphs=z['graphs'].tolist();start=time.monotonic();A,Q,polys=augment(graphs)
 np.savez(P/'M10_integer_moments.npz',A=A,**{f'Q{i}':q for i,q in enumerate(Q)})
 (P/'M10_integer_moments_meta.json').write_text(json.dumps({'polynomials':polys,'matrix_labels':[f'integer_degree_{j}' for j in range(18,24)]+[f'integer_codegree_{j}' for j in range(10)],'seconds':time.monotonic()-start},indent=2)+'\n')
 print('integer augment',A.shape,len(Q),time.monotonic()-start,flush=True)
