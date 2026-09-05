"""Explicit finite-ring coloring recipe and exact mixed-gadget calibration."""
from pathlib import Path
from collections import Counter,defaultdict
from hashlib import sha256
import importlib.util,json
HERE=Path(__file__).resolve().parent
ROOT=HERE.parent
def module(name,path,pin):
 assert sha256(path.read_bytes()).hexdigest()==pin,'dependency pin mismatch'
 s=importlib.util.spec_from_file_location(name,path);m=importlib.util.module_from_spec(s);s.loader.exec_module(m);return m
F=module('input',ROOT/'hadwiger_nelson_mixed505_all_gadget_anchors/verify.py','526b12cbd9d28217e59feb7191c93ace4e5a572ebeadd66cdf384393126aee38')
K=module('local_field',ROOT/'hadwiger_nelson_nonmono_field_obstruction/coloring.py','a612f6f145f511340d930cf093939cf102128e960ae12977e86dfb1d1e5b486e')
def realmul(x,y):return (x[0]*y[0]+33*x[1]*y[1],x[0]*y[1]+x[1]*y[0])
def pairs(P):
 out=defaultdict(list)
 for i in range(len(P)):
  for j in range(i+1,len(P)):
   d=F.subtract(P[j],P[i]);out[F.norm(d)].append((i,j,d))
 return out

def residue(x,den,bits):
 # Return coordinates in Z/2^bits[omega], omega^2+omega+1=0.
 e=(den&-den).bit_length()-1;M=1<<(bits+e);r=K.root33_mod_power2(bits+e)
 a,b,c,d=x;inv=pow(3*(den>>e),-1,M)
 A=((3*a+3*b*r+3*c+d*r)*inv)%M
 B=((6*c+2*d*r)*inv)%M
 assert A%(1<<e)==B%(1<<e)==0,'point is not locally integral'
 return (A>>e,B>>e)
def umul(x,y,m):
 a,b=x;c,d=y;return ((a*c-b*d)%m,(a*d+b*c-b*d)%m)
def uadd(x,y,m):return tuple((a+b)%m for a,b in zip(x,y))
def uinv(x,m):
 a,b=x;k=pow((a*a-a*b+b*b)%m,-1,m);return ((a-b)*k%m,-b*k%m)
def col(x):return x[0]+2*x[1]
def emul(x,y):
 a,b,c,d=x;A,B,C,D=y
 return (a*A+33*b*B-3*c*C-11*d*D,a*B+b*A-c*D-d*C,a*C+c*A+11*(b*D+d*B),a*D+d*A+3*(b*C+c*B))
def bar(x):return (x[0],x[1],-x[2],-x[3])
def connected(n,edges):
 adj=[[] for _ in range(n)]
 for i,j in edges:adj[i].append(j);adj[j].append(i)
 seen={0};todo=[0]
 for i in todo:
  for j in adj[i]:
   if j not in seen:seen.add(j);todo.append(j)
 return len(seen)==n

def case(B,V,EB,EV,seed,SB=72,SV=12):
 i,j,k,l=seed;db=F.subtract(B[j],B[i]);dv=F.subtract(V[l],V[k])
 nb,nv=F.norm(db),F.norm(dv);assert tuple(SV*SV*a+SB*SB*b for a,b in zip(nb,nv))==(4*SB*SB*SV*SV,0)
 assert not F.field_roots(*realmul(nb,nv))
 mb=tuple(a+b for a,b in zip(B[i],B[j]));mv=tuple(a+b for a,b in zip(V[k],V[l]))
 XB=[tuple(2*x-y for x,y in zip(b,mb)) for b in B];YV=[tuple(2*x-y for x,y in zip(v,mv)) for v in V]
 unit=residue(db,SB,1)!=(0,0);assert unit==(residue(dv,SV,1)!=(0,0))
 if unit:
  ratio=umul(residue(db,SB,1),uinv(residue(dv,SV,1),2),2)
  r={(1,0):(1,0),(0,1):(0,1),(1,1):(3,3)}[ratio]
  cb=[col(residue(F.subtract(b,B[i]),SB,1)) for b in B];cv=[]
  for y in YV:
   w=uadd(residue(db,SB,2),umul(r,residue(y,SV,2),4),4)
   assert w[0]%2==w[1]%2==0
   cv.append(col(tuple(t//2 for t in w)))
  branch='unit_diagonals'
 else:
  cb=[col(residue(x,2*SB,1)) for x in XB];cv=[col(residue(y,2*SV,1)) for y in YV];branch='even_diagonals'
 assert all(cb[a]!=cb[b] for a,b in EB);assert all(cv[a]!=cv[b] for a,b in EV)
 c0=emul(bar(db),dv);indices=defaultdict(list)
 for v,y in enumerate(YV):indices[F.norm(y)].append(v)
 cross=[]
 for b,x in enumerate(XB):
  n=F.norm(x);target=(4*SB*SB*SV*SV-SV*SV*n[0],-SV*SV*n[1])
  if any(t%(SB*SB) for t in target):continue
  for v in indices[tuple(t//(SB*SB) for t in target)]:
   c=emul(bar(x),YV[v]);z=emul(c,bar(c0))
   if z[2:]==(0,0):cross.append((b,v))
 assert all((a,b) in cross for a in (i,j) for b in (k,l))
 assert all(cb[b]!=cv[v] for b,v in cross)
 ib=next((b for b,x in enumerate(XB) if x==(0,0,0,0)),None)
 iv=next((v for v,x in enumerate(YV) if x==(0,0,0,0)),None)
 if ib is not None and iv is not None:assert cb[ib]==cv[iv]
 aliases=list(range(len(B)+len(V)))
 if ib is not None and iv is not None:aliases[len(B)+iv]=ib
 all_edges=EB+[(len(B)+a,len(B)+b) for a,b in EV]+[(b,len(B)+v) for b,v in cross]
 union_edges=sorted({tuple(sorted((aliases[a],aliases[b]))) for a,b in all_edges})
 assert all(a!=b and (cb+cv)[a]!=(cb+cv)[b] for a,b in union_edges)
 return {'seed':seed,'branch':branch,'overlaps':int(ib is not None and iv is not None),'B_midpoint_vertex':ib,'V_midpoint_vertex':iv,'vertices':len(set(aliases)),'strict_edges':len(union_edges),'cross_edges':len(cross),'colors_sha256':sha256((''.join(map(str,cb+cv))+'\n').encode()).hexdigest(),'cross_sha256':sha256(''.join(f'{b},{v}\n' for b,v in cross).encode()).hexdigest(),'union_edges_sha256':sha256(''.join(f'{a},{b}\n' for a,b in union_edges).encode()).hexdigest()},(cross,cb,cv)

def controls():
 B=[(0,0,0,0),(2,0,0,0),(-2,0,0,0)]
 V=[(0,0,0,0),(0,1,2,0),(0,-1,-2,0)]
 r,_=case(B,V,[],[],(1,2,1,2),3,9)
 assert r['overlaps']==1 and r['vertices']==5 and r['strict_edges']==4
 rejected=False
 try:residue((1,0,0,0),2,1)
 except AssertionError:rejected=True
 assert rejected,'nonintegral input was not rejected'
 return {'locally_integral_overlap_control':True,'nonintegral_residue_rejected':True}


def main():
 import argparse
 parser=argparse.ArgumentParser(description=__doc__)
 parser.add_argument('--cases-out',type=Path)
 args=parser.parse_args();cc=controls()
 B,V,D,inc,EB,EV=F.construction();assert connected(len(B),EB) and connected(len(V),EV)
 PB,PV=pairs(B),pairs(V);rows=[];counts=Counter();census=Counter()
 twiceB={tuple(2*x for x in b) for b in B};twiceV={tuple(2*x for x in v) for v in V}
 for n,vv in sorted(PV.items()):
  m=(20736-36*n[0],-36*n[1]);bb=PB.get(m,[])
  if not bb:continue
  typ='in_E' if F.field_roots(*realmul(n,m)) else 'outside_E'
  census[typ+'_norm_pairs']+=1;census[typ+'_segment_pairs']+=len(bb)*len(vv)
  if typ=='in_E':continue
  b_by={};v_by={}
  for i,j,d in bb:b_by.setdefault(tuple(a+b for a,b in zip(B[i],B[j])) in twiceB,(i,j))
  for k,l,d in vv:v_by.setdefault(tuple(a+b for a,b in zip(V[k],V[l])) in twiceV,(k,l))
  assert set(b_by)==set(v_by)=={False},'unexpected source midpoint inside component'
  r,_=case(B,V,EB,EV,(*b_by[False],*v_by[False]));rows.append(r);counts[r['branch']]+=1
 text=json.dumps(rows,separators=(',',':'))+'\n'
 if args.cases_out:args.cases_out.write_text(text)
 output={'connected_components_checked':True,'B_norm_types':len(PB),'V_norm_types':len(PV),'complementary_diagonal_census':dict(census),'selected_exact_cases':len(rows),'case_branches':dict(counts),'all_selected_cases_disjoint':all(r['overlaps']==0 for r in rows),'cross_edge_histogram':dict(sorted(Counter(r['cross_edges'] for r in rows).items())),'case_data_sha256':sha256(text.encode()).hexdigest(),'controls':cc,'uniform_claim_requires_PROOF_md':True}
 assert len(rows)==51 and counts=={'unit_diagonals':43,'even_diagonals':8}
 print(json.dumps(output,indent=2))

if __name__=='__main__':main()
