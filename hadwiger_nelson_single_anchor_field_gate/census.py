"""Complete contact-polynomial gate; all raw streams remain in --work."""
from common import *
import argparse,subprocess,time
p=1000000021
def sqrtmod(n):
 n%=p;require(pow(n,(p-1)//2,p)==1,'not split')
 q=p-1;s=0
 while q%2==0:q//=2;s+=1
 z=2
 while pow(z,(p-1)//2,p)!=p-1:z+=1
 c=pow(z,q,p);x=pow(n,(q+1)//2,p);t=pow(n,q,p);m=s
 while t!=1:
  i=1;tt=t*t%p
  while tt!=1:tt=tt*tt%p;i+=1
  b=pow(c,1<<(m-i-1),p);x=x*b%p;t=t*b*b%p;c=b*b%p;m=i
 return x

require(all(p%d for d in range(2,isqrt(p)+1)),'prime')
a,b,c=map(sqrtmod,[-3,-11,5])
require(a*a%p==p-3 and b*b%p==p-11 and c*c%p==5,'split roots')
def rat(x):require(x.denominator%p!=0,'singular denominator');return x.numerator*pow(x.denominator,-1,p)%p
def e(z,con=False):
 aa,bb=(-a,-b)if con else(a,b)
 return sum(rat(x)*v for x,v in zip(z,[1,-a*b,aa,bb]))%p
def emb(z,con=False):return(e(z[0],con)+c*e(z[1],con))%p
@lru_cache(None)
def data(a):return en(a),ei(ec(a))
@lru_cache(None)
def bd(b):return(norm(b),ZERO),mul(conj(b),inverse_real(norm(b))),conj(b)
@lru_cache(None)
def key(a,b):
 na,ia=data(a);nb,ib,cb=bd(b);h=es(ea(na,nb),EO);ci=sc(ia,ib)
 return sc(em(h,ci),scale(ONE,-1)),em(sc(a,cb),ci)
@lru_cache(None)
def shape(na,nb):
 h=es(ea(na,nb),EO);d=es(sc(em(na,nb),scale(ONE,4)),em(h,h))
 if sgn(d)<=0:return 'no_outside_root',d
 return ('outside'if sq(sc(d,scale(ONE,F(1,3))))is None else'inside'),d

def native_reference(A,B):
 # Different language/dictionary path, same modular reduction; execution audit.
 for pp in range(len(A)):
  D=[((A[pp][0]-r[0])%p,(A[pp][1]-r[1])%p)for r in A]
  iv=[pow(z[1],-1,p)if r!=pp else 0 for r,z in enumerate(D)]
  ns=[z[0]*z[1]%p for z in D]
  for kk,C in enumerate(B):
   groups=defaultdict(list)
   for jj,(b,cb)in enumerate(C[1:],1):
    bi=pow(b,-1,p);nb=b*cb%p
    for rr,(d,cd)in enumerate(D):
     if rr==pp:continue
     ci=iv[rr]*bi%p;t=-(ns[rr]+nb-1)*ci%p;j=d*cb*ci%p;groups[t,j].append((rr,jj))
   records=[]
   for ev in groups.values():
    if len({r for r,j in ev})<3:continue
    ev.sort();records.append([pp,kk,len(ev)]+[v for z in ev for v in z])
   yield from sorted(records)

def run(name,work,native,reference=False):
 st=time.time();work.mkdir(parents=True,exist_ok=True);P,word=seed();AA=patterns(name);m=len(AA[0]);A=[(emb(z),emb(z,True))for z in P];B=[[(e(z),e(z,True))for z in C]for C in AA]
 require(all(A[i][1]!=A[j][1]for i,j in combinations(range(490),2)),'singular seed difference')
 require(all(z[0]for C in B for z in C[1:]),'singular motif offset')
 inp=work/(name+'_input.txt');groups=work/(name+'_groups.txt');stats=work/(name+'_native.txt')
 with inp.open('w')as f:
  f.write(f'{len(P)} {len(AA)} {m}\n')
  for z in A+[z for C in B for z in C]:f.write(f'{z[0]} {z[1]}\n')
 with groups.open('w')as f,stats.open('w')as err:subprocess.run([str(native.resolve()),str(inp.resolve())],stdout=f,stderr=err,check=True)
 if reference:
  # Compare entries, not just aggregate counts.
  with groups.open()as f:
   for rr in native_reference(A,B):require(list(map(int,next(f).split()))==rr,'native/reference mismatch')
   require(f.read()=='','extra native entries')
 counts=Counter();kept=[]
 for line in groups.open():
  row=list(map(int,line.split()));pp,kk,n=row[:3];ev=list(zip(row[3::2],row[4::2]));require(len(ev)==n,'native row size');C=AA[kk];gg=defaultdict(list)
  for rr,jj in ev:gg[key(es(P[pp],P[rr]),C[jj])].append((rr,jj))
  counts['modular_groups']+=1;counts['exact_groups']+=len(gg)
  for (T,J),events in sorted(gg.items()):
   old={rr for rr,jj in events}|{pp}
   if len(old)<4:counts['false_modular_group']+=1;continue
   rr,jj=events[0];typ,disc=shape(data(es(P[pp],P[rr]))[0],bd(C[jj])[0]);counts[typ]+=1
   if typ!='outside':continue
   cross=sorted(events+[(pp,jj)for jj in range(1,m)if norm(C[jj])==ONE]);inside=[(i,j)for i,j in combinations(range(1,m),2)if norm(sub(C[i],C[j]))==ONE]
   kept.append({'p':pp,'pattern':kk,'T':ser(T),'J':ser(J),'disc':ser(disc),'events':events,'cross':cross,'inside':inside,'old_vertices':len(old)})
 out={'name':name,'counts':dict(counts),'outside_groups':kept,'native_stats':stats.read_text().strip(),'seed_sha256':digest([ser(z)for z in P]),'outside_sha256':digest(kept),'reference_checked':reference,'seconds':time.time()-st}
 (work/(name+'_census.json')).write_text(json.dumps(out,separators=(',',':'))+'\n');print(name,dict(counts),'seconds',out['seconds'],flush=True)
 return out
if __name__=='__main__':
 ap=argparse.ArgumentParser();ap.add_argument('--work',required=True,type=Path);ap.add_argument('--native',required=True,type=Path);ap.add_argument('--reference',action='store_true');args=ap.parse_args()
 for name in ['M','G']:run(name,args.work,args.native,args.reference)
