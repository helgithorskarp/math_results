"""Independent original-set reconstruction for unrestricted triangle counts.

Own literal framework credited to REVIEW10237; arbitrary counts and the
complete spread line/inverse are new, current author native/certificate unread.
"""
from fractions import Fraction as R
import hashlib,json,pathlib,sys,time
P=pathlib.Path(__file__).resolve().parent;sys.path.insert(0,str(P));from forms import build,need
DAMAGE=''
def plus(*vs):
 out={}
 for v in vs:
  for i,c in v.items():out[i]=out.get(i,R(0))+c
 return {i:c for i,c in out.items() if c}
def mul(v,c):return {i:c*x for i,x in v.items() if c*x}
def unit(i):return {i:R(1)}
def ldl(a):
 a=[r[:] for r in a];out=[]
 for i in range(len(a)):
  p=a[i][i];need(p>0,'literal positive LDL');out.append(p)
  for j in range(i+1,len(a)):
   for k in range(j,len(a)):
    a[j][k]-=a[j][i]*a[i][k]/p;a[k][j]=a[j][k]
 return out
def literal(n,h,l):
 need(3<=n<=5 and 3<=h<=6 and 2<=l<h and 2**n+6*(h+l)<=62,'fixed literal resource bounds')
 q=2**(n-1);g=h+l;b=build(R(h),R(l),R(q));s=int(b['s']);N=int(b['N']);m=3*g;D=3*h;ell=m+1
 metric={};count=0
 def space(mat):
  nonlocal count
  ids=list(range(count,count+len(mat)));count+=len(mat)
  for i in range(len(mat)):
   for j in range(len(mat)):
    if mat[i][j]:metric[ids[i],ids[j]]=mat[i][j]
  return ids
 old=space([[R(s*(i==j)+(q-D)*(i+1+j+1==2*q-1)-1) for j in range(2*q-1)] for i in range(2*q-1)])
 # Full-set row has no proper complement, so the indicator above is zero there.
 Bs=[space([[R(s,3)*(R(i==j)-R(1,h)) for j in range(h)] for i in range(h)]) for _ in range(2)]
 Ts=[[space([[R(s)*(R(a==bb)-R(1,3)) for bb in range(3)] for a in range(3)]) for _ in range(k)] for k in (h,l)]
 Mg=[]
 for i in range(g):
  gi=0 if i<h else 1;ki=h if gi==0 else l;z=b['groups'][gi]
  Mg.append([z['mu'] if i==j else (z['mu']-z['nu'] if ((j<h)==(i<h)) else -b['tau']) for j in range(g)])
 Ms=space(Mg);WA=space([[b['groups'][0 if i<h else 1]['alpha'] if i==j else R(0) for j in range(g)] for i in range(g)])
 WF=space([[b['groups'][0 if i<h else 1]['beta'] if i==j else R(0) for j in range(g)] for i in range(g)])
 def image(v):
  out={}
  for (i,j),c in metric.items():
   if j in v:out[i]=out.get(i,R(0))+c*v[j]
  return out
 def dot_image(v,im):return sum((c*im.get(i,R(0)) for i,c in v.items()),R(0))
 def dot(v,w):return dot_image(v,image(w))
 G=plus(*(unit(i) for i in old));gF=unit(old[-1]);Hx=mul(plus(*(unit(old[a-1]) for a in range(1,2*q) if a&1)),-1);Hy=mul(plus(*(unit(old[a-1]) for a in range(1,2*q) if a&2)),-1)
 Bbar=mul(plus(*(unit(Bs[1][i]) for i in range(l))),R(1,l))
 Bt=[[unit(i) for i in Bs[0]], [plus(unit(Bs[1][i]),mul(Bbar,-1)) for i in range(l)]]
 K=plus(G,Hx,mul(Hy,R(l,h)),mul(Bbar,3*l));z=mul(K,-R(1,ell));need(dot(z,z)==b['c0'],'actual empty norm')
 rows=[unit(i) for i in old];sets=list(range(1,2*q));labels=[('old',a) for a in sets]
 private=[];marked=[];offset=n
 for gi,k in enumerate((h,l)):
  par=b['groups'][gi];hh=Hx if gi==0 else Hy;mark=1 if gi==0 else 2
  for i in range(k):
   facet=i+(h if gi else 0);pa=1<<offset;pb=1<<(offset+1);offset+=2
   for a,mem in enumerate((mark|pa,mark|pb,mark|pa|pb)):
    marked.append((plus(mul(hh,R(1,D)),unit(Bs[gi][i]),unit(Ts[gi][i][a])),mem,('marked',gi,i,a)))
   pro=[plus(z,mul(Bt[gi][i],par['a']),mul(unit(Ts[gi][i][1]),par['c'])),plus(z,mul(Bt[gi][i],par['a']),mul(unit(Ts[gi][i][0]),par['c'])),plus(z,mul(Bt[gi][i],par['b']),mul(plus(*(unit(Ts[gi][j][2]) for j in range(k) if j!=i)),par['c']/(k-1)))]
   wr=[plus(unit(Ms[facet]),mul(unit(WA[facet]),R(1,2)),mul(unit(WF[facet]),-R(1,2))),plus(unit(Ms[facet]),mul(unit(WA[facet]),-R(1,2)),mul(unit(WF[facet]),-R(1,2))),plus(unit(Ms[facet]),unit(WF[facet]))]
   for a,mem in enumerate((pa,pb,pa|pb)):private.append((plus(pro[a],wr[a]),mem,('private',gi,i,a)))
 for v,mem,label in marked+private:rows.append(v);sets.append(mem);labels.append(label)
 if DAMAGE=='missing-private-row':rows.pop();sets.pop();labels.pop()
 need(len(rows)==N-1 and len(set(sets))==N-1,'entire original carrier')
 whole_sum=plus(*rows,z);need(dot(whole_sum,whole_sum)==0,'whole row completion in singular ambient representation')
 ims=[image(r) for r in rows];C=[[dot_image(r,im) for im in ims] for r in rows]
 for i,A in enumerate(sets):
  need(C[i][i]==s-1,'nonempty diagonal')
  for j,B in enumerate(sets):
   if i!=j and A&B:need(C[i][j]==-1,'intersection support')
 stars=[sum(bool(A&bit) for A in sets) for bit in (1,2,4,1<<n)];need(stars[:2]==[s,q+3*l] and stars[2]==q and stars[3]==4,'actual stars')
 heavy=[R(bool(A&1)) for A in sets];completion=[R(m,ell) if label[0]!='private' else R(1) for label in labels]
 for ker in (heavy,completion):need(all(sum(C[i][j]*ker[j] for j in range(N-1))==0 for i in range(N-1)),'seed exact kernel')
 # Entire physical basis, including ALL unchanged old directions.
 basis=[];expect=[];names=[]
 def add(vs,mat,frame,name):
  start=len(basis);basis.extend(vs);names.extend([name]*len(vs));expect.append((start,mat,frame))
 for gi,k in enumerate((h,l)):
  par=b['groups'][gi]
  for i in range(k):add([plus(unit(Ts[gi][i][0]),mul(unit(Ts[gi][i][1]),-1)),unit(WA[i+(h if gi else 0)])],[[2*R(s),0],[0,par['alpha']]],b['physical'][f'{gi}-odd'][1],f'{gi}-odd')
  for j in range(1,k):
   profile=[R(1) if i<j else -R(j) if i==j else R(0) for i in range(k)];scale=R(j*(j+1),2)
   vs=[plus(*(mul(Bt[gi][i],profile[i]) for i in range(k))),plus(*(mul(plus(unit(Ts[gi][i][0]),unit(Ts[gi][i][1]),mul(unit(Ts[gi][i][2]),-2)),profile[i]) for i in range(k))),plus(*(mul(unit(WF[i+(h if gi else 0)]),profile[i]) for i in range(k))),plus(*(mul(unit(Ms[i+(h if gi else 0)]),profile[i]) for i in range(k)))]
   gam,frm=b['physical'][f'{gi}-standard'];add(vs,[[scale*gam[ii] if ii==jj else 0 for jj in range(4)] for ii in range(4)],[[scale*x for x in row] for row in frm],f'{gi}-standard')
 E=plus(G,mul(gF,-1));U=plus(G,gF);Rv=plus(Hx,Hy,G,gF);Ao=plus(Hx,mul(Hy,-1))
 gam,frm=b['physical']['five'];add([E,U,Rv,Ao,Bbar],[[gam[i] if i==j else 0 for j in range(5)] for i in range(5)],frm,'aggregate-five')
 for gi,k in enumerate((h,l)):
  gam,frm=b['physical'][f'{gi}-trace'];add([plus(*(plus(unit(Ts[gi][i][0]),unit(Ts[gi][i][1]),mul(unit(Ts[gi][i][2]),-2)) for i in range(k))),plus(*(unit(WF[i+(h if gi else 0)]) for i in range(k)))],[[gam[i] if i==j else 0 for j in range(2)] for i in range(2)],frm,f'{gi}-trace')
 add([plus(*(unit(Ms[i]) for i in range(h)))],[[h*l*b['tau']]],[[3*g*h*l*b['tau']**2]],'mean')
 pairs=[(a,2*q-1-a) for a in range(1,2*q-1) if a<2*q-1-a]
 for j in range(1,len(pairs)):
  prof=[R(1) if i<j else -R(j) if i==j else R(0) for i in range(len(pairs))];v=plus(*(mul(plus(unit(old[a-1]),unit(old[aa-1])),prof[i]) for i,(a,aa) in enumerate(pairs)));norm=4*q*j*(j+1);add([v],[[R(norm)]],[[R(2*q*norm)]],'old-sum')
 rr=[R(1-bool(a&1)-bool(a&2)) for a,aa in pairs];av=[R(bool(a&2)-bool(a&1)) for a,aa in pairs];null=[]
 for j in range(len(pairs)):
  v=[R(i==j) for i in range(len(pairs))]
  for w in [rr,av]+null:
   c=sum(x*y for x,y in zip(v,w))/sum(x*x for x in w);v=[x-c*y for x,y in zip(v,w)]
  if any(v):null.append(v)
 need(len(null)==q-3,'whole old difference complement')
 for v in null:
  vv=plus(*(mul(plus(unit(old[a-1]),mul(unit(old[aa-1]),-1)),v[i]) for i,(a,aa) in enumerate(pairs)));norm=4*D*sum(x*x for x in v);add([vv],[[norm]],[[2*D*norm]],'old-difference')
 need(len(basis)==N-3,'entire physical dimension')
 allrows=[({} if DAMAGE=='wrong-empty' else z)]+rows;allims=[image(v) for v in allrows];bims=[image(v) for v in basis];scores=[[dot_image(v,im) for im in allims] for v in basis]
 Gamma=[[dot_image(v,im) for im in bims] for v in basis];S=[[sum(x*y for x,y in zip(a,bb)) for bb in scores] for a in scores]
 eg=[[R(0) for _ in basis] for _ in basis];es=[[R(0) for _ in basis] for _ in basis]
 for st,gm,sm in expect:
  for i in range(len(gm)):
   for j in range(len(gm)):eg[st+i][st+j]=gm[i][j];es[st+i][st+j]=sm[i][j]
 need(Gamma==eg and S==es,'every full physical metric/frame/cross entry')
 ldl(Gamma);ldl([[(N-1)*Gamma[i][j]-S[i][j] for j in range(N-3)] for i in range(N-3)])
 heavy_private=[i for i,label in enumerate(labels) if label[:2]==('private',0)]
 light_full=[i for i,label in enumerate(labels) if label[:2]==('private',1) and label[3]==2]
 last=light_full[-1];ix=sets.index(1);keep=[i for i in range(N-1) if i not in (ix,last)]
 A0=[[C[i][j] for j in keep] for i in keep];ldl(A0)
 dual=plus(mul(plus(*(unit(Ms[i]) for i in (range(1) if DAMAGE=='omitted-heavy-mean' else range(h)))),1/(h*l*b['tau'])),mul(plus(*(unit(WF[h+i]) for i in range(l))),(-3 if DAMAGE=='wrong-light-full-score' else -2)/(l*b['groups'][1]['beta'])))
 if DAMAGE=='wrong-dual-energy':b['kappa']+=1
 pvec=[R(1,h) if i in heavy_private else -R(3,l) if i in light_full else R(0) for i in range(N-1)]
 score=[dot_image(dual,im) for im in allims]
 need(score==[R(0)]+pvec,'every original spread dual score including empty')
 need(dot(dual,dual)==b['kappa'] and 0<b['kappa']<R(49,78),'original harmonic dual norm and bound')
 # A completely literal original-principal inverse, not quotient inversion.
 inv=solve(A0,[pvec[i] for i in keep]);whole=[R(0) for _ in C]
 for i,v in zip(keep,inv):whole[i]=v
 need(all(sum(x*y for x,y in zip(row,whole))==t for row,t in zip(C,pvec)),'every original inverse row equation')
 need(sum(x*y for x,y in zip(whole,pvec))==b['kappa'],'literal original inverse energy')
 Q=[[dot_image(v,im) for im in allims] for v in allrows]
 need(all(sum(row)==0 for row in Q),'actual original zero row sums')
 repairs=[];endpoint=(5 if DAMAGE=='false-endpoint' else 6)/b['kappa']
 for delta in (R(1,32),R(1,8),R(1,7),endpoint):
  cc=[row[:] for row in C]
  for i in heavy_private:
   for j in light_full:cc[i][j]+=delta/(h*l);cc[j][i]+=delta/(h*l)
  if DAMAGE=='missing-spread-pair':cc[heavy_private[-1]][light_full[-1]]-=delta/(h*l);cc[light_full[-1]][heavy_private[-1]]-=delta/(h*l)
  kr=[i for i in range(N-1) if i!=ix]
  rank=psd_rank([[cc[i][j] for j in kr] for i in kr])
  need(rank==(N-3 if delta==endpoint else N-2),'whole lower endpoint/interior rank')
  qq=[[R(0) for _ in range(N)] for _ in range(N)]
  for i in range(N-1):
   for j in range(N-1):qq[i+1][j+1]=cc[i][j]
   qq[0][i+1]=qq[i+1][0]=-sum(cc[i])
  qq[0][0]=sum(sum(row) for row in cc)
  aa=[R(-2 if DAMAGE=='wrong-update-empty' else -3)]+[R(1,h) if i in heavy_private else R(0) for i in range(N-1)]
  bb=[R(-1)]+[R(1,l) if i in light_full else R(0) for i in range(N-1)]
  need(sum(aa)==sum(bb)==0 and sum(x*y for x,y in zip(aa,bb))==3,'actual original update factors')
  need(sum(x*x for x in aa)==9+R(3,h) and sum(x*x for x in bb)==1+R(1,l),'complete original update squared norms')
  need(all(qq[i][j]-Q[i][j]==delta*(aa[i]*bb[j]+bb[i]*aa[j]) for i in range(N) for j in range(N)),'whole original empty spread update')
  need(qq[0][0]-Q[0][0]==6*delta,'actual empty loop change')
  for i,A in enumerate([0]+sets):
   need(sum(qq[i])==0,'repaired zero row sums')
   for j,B in enumerate([0]+sets):
    if A&B:need(1+qq[i][j]-s*(i==j)==0,'repaired original M support')
  if delta!=endpoint:
   # Fresh strengthened original cap, paid without omitting the empty.
   floor=1-R(55,8)*delta
   ldl([[(N-floor)*(R(i==j)-R(1,N))-qq[i][j] for j in range(1,N)] for i in range(1,N)])
  repairs.append(dict(delta=str(delta),core_rank=rank,lower_rank=rank+1,actual_empty_change=str(6*delta),cap_floor=str(1-R(55,8)*delta) if delta!=endpoint else 'not asserted'))
 # Actual outside-line negative forms are described by the full core Schur.
 rho=[R(m,ell) if label[0] in ('old','marked') else R(1) for label in labels]
 heavy=[R(bool(A&1)) for A in sets]
 need(all(sum(row[j]*rho[j] for j in range(N-1))==0 for row in C),'whole second core kernel')
 need(all(sum(row[j]*heavy[j] for j in range(N-1))==0 for row in C),'whole heavy core kernel')
 return dict(n=n,h=h,l=l,q=q,N=N,s=s,span=N-3,original_positions=N*N,metric_and_frame_positions=2*(N-3)**2,kappa=str(b['kappa']),repairs=repairs,all_inverse_rows=N-1)

def solve(A,v):
 A=[row[:]+[t] for row,t in zip(A,v)];n=len(A)
 for i in range(n):
  pivot=A[i][i];need(pivot!=0,'literal inverse pivot')
  for j in range(i+1,n):
   c=A[j][i]/pivot
   for k in range(i+1,n+1):A[j][k]-=c*A[i][k]
 x=[R(0) for _ in range(n)]
 for i in range(n-1,-1,-1):x[i]=(A[i][-1]-sum(A[i][j]*x[j] for j in range(i+1,n)))/A[i][i]
 return x

def psd_rank(A):
 A=[row[:] for row in A];rank=0
 for i in range(len(A)):
  p=A[i][i];need(p>=0,'literal PSD pivot')
  if not p:
   need(all(A[i][j]==0 for j in range(i+1,len(A))),'zero pivot must have zero entire column');continue
  rank+=1
  for j in range(i+1,len(A)):
   for k in range(j,len(A)):A[j][k]-=A[j][i]*A[i][k]/p;A[k][j]=A[j][k]
 return rank

if __name__=='__main__':
 import argparse
 a=argparse.ArgumentParser();a.add_argument('--n',type=int,required=True);a.add_argument('--h',type=int,required=True);a.add_argument('--l',type=int,required=True);a.add_argument('--out',required=True);a.add_argument('--damage',default='');arg=a.parse_args();DAMAGE=arg.damage
 r=literal(arg.n,arg.h,arg.l);data=(json.dumps(r,sort_keys=True,separators=(',',':'))+'\n').encode();pathlib.Path(arg.out).write_bytes(data);print(json.dumps(dict(N=r['N'],span=r['span'],record_bytes=len(data),record_sha256=hashlib.sha256(data).hexdigest())))
