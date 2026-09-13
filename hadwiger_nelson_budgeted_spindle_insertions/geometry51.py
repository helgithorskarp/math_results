from attachments import *
import ctypes as ct
from math import lcm

class Geometry51:
 def __init__(self,path):
  self.lib=ct.CDLL(str(Path(path).resolve()))
  for name in('contacts','real_contacts'):
   f=getattr(self.lib,name);f.argtypes=[ct.c_int]*3+[ct.c_int64]*4+[ct.POINTER(ct.c_int64),ct.POINTER(ct.c_int)];f.restype=ct.c_int
 def graph(self,P,s,first_end=None,audit=False):
  n=len(P);first_end=n if first_end is None else first_end;require(n>0 and n<=200000 and len(set(P))==n,'point census');require(sign(s)>0 and K.sqrt_real(s)is None,'extension basis')
  den=lcm(*(x.denominator for p in P for z in p for x in z));nums=[int(x*den)for p in P for z in p for x in z];sd=lcm(s[0].denominator,s[1].denominator);s0=int(s[0]*sd);s1=int(s[1]*sd)
  mx=max(map(abs,nums+[den,sd,s0,s1]));require(mx<=10**9,'guard: '+str(mx));data=(ct.c_int64*len(nums))(*nums);cap=max(10000,n*100);out=(ct.c_int*(2*cap))();found=[]
  for name in (('contacts','real_contacts')if audit else('contacts',)):
   m=getattr(self.lib,name)(n,first_end,cap,den,sd,s0,s1,data,out);require(m>=0,'native failed: '+str(m));found.append([(out[2*i],out[2*i+1])for i in range(m)])
  if audit:require(found[0]==found[1],'metric disagreement')
  return found[0]

def boundary(tag):
 st=time.time();x=json.loads((W/f'placements_{tag}.json').read_text());P=[(tuple(map(F,p[:4])),tuple(map(F,p[4:])))for p in x['seed_points']+x['new_points']];s=tuple(map(F,x['radicand']));G=Geometry51(W/'sparse_geometry.so');es=G.graph(P,s,490,True);ne=[[]for _ in x['new_points']];base=[]
 for i,j in es:
  if j<490:base.append((i,j))
  else:ne[j-490].append(i)
 require(len(base)==x['seed_edges'],'seed edges changed');require(all(x['seed_word'][a]!=x['seed_word'][b]for a,b in base),'seed colour')
 z={'tag':tag,'neighbours':ne,'seed_edges':base,'old_new_edges':len(es)-len(base),'new_degree_counts':dict(Counter(map(len,ne))),'seconds':time.time()-st};(W/f'boundary_{tag}.json').write_text(json.dumps(z,separators=(',',':'))+'\n');print('BOUNDARY',tag,'new',len(ne),'contacts',z['old_new_edges'],'degrees',z['new_degree_counts'],'seconds',z['seconds'],flush=True)
if __name__=='__main__':boundary(sys.argv[1])
