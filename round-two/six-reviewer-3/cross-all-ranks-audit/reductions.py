"""Fresh finite checks of the ordinary reduction's small set descriptions.
No producer module or native record is loaded. Output regenerates all cells.
P-branch scalar projections check algebra CONDITIONED on extra assumptions;
they do not justify the original missing red/blue premise.
"""
import itertools,json,hashlib,argparse
from pathlib import Path
XS=frozenset(range(6));C=frozenset((0,1));P=frozenset((0,2,3));S=XS-P;H=C|{3,5};K=C|{2,4};L=XS-C
CYCLE=((0,4),(4,3),(3,1),(1,2),(2,5),(5,0));MIXED=((0,4),(0,5),(1,2),(1,3))
def powers(s):
 return [frozenset(x for x,b in zip(sorted(s),bits) if b) for bits in itertools.product((0,1),repeat=len(s))]
def covers(row,edges):return all(a in row or b in row for a,b in edges)
def require(condition,message):
 if not condition:raise ValueError(message)
def calculate():
 rows=powers(XS);cyclecovers=[r for r in rows if covers(r,CYCLE)]
 t2={k:[r for r in rows if covers(r,MIXED) and all(k+len(r&own)<=4 for own in ({3,5},{2,4}))] for k in (3,4)}
 require(set(t2[4])=={C},'rank4 T2 cover')
 proper=[r for r in t2[3] if C<r]
 require(len(proper)==8 and set(t2[3])=={C,P,S}|set(proper),'rank3 T2 cover')
 propercuts=[]
 for row in proper:
  for leaf in sorted(row-C):
   own=({3,5} if leaf in {3,5} else {2,4})
   # SX/T2: a plus at least one OWN leaf, Q ranks4,3.
   allowance=3-(1+len(row&own));require(allowance==1,'tight SX/T2 union')
   # SX/leaf: u,T2. T2/leaf: own SX and included adjacent center.
   propercuts.append({'T2':sorted(row),'leaf':leaf,'union_ranks':[4,3], 'union_allowance':allowance,'leaf_Q_rank_lower':3,'leaf_overlap_upper_sum':2})
 # Actual four-variable leaf cells from the union budget in the P branch.
 leafcells=[]
 for u,v,a,b in itertools.product((0,1),repeat=4):
  rank=5-u-v-a-b;sx_allow=1-a;t_allow=2-u
  # Blue a/X forces the endpoint total <=3, including T2.
  admissible=(u+v+a+b+1<=3 and rank<=sx_allow+t_allow)
  leafcells.append({'bits':[u,v,a,b],'Qrank':rank,'allowances':[sx_allow,t_allow],'admissible':admissible})
 require([z['bits'] for z in leafcells if z['admissible']]==[[0,1,0,1]],'forced leaf')
 scalars=[]
 for c,ell,s,t,h,beta,b1 in itertools.product(range(3),range(5),range(1,3),range(1,3),range(4),(0,1),(0,1)):
  if not (b1<=c<=b1+1):continue
  degree=3+c+ell+s+t+h
  if s+h<=3 and 1+t+ell+beta*b1<=3 and degree>=8+s+t:
   scalars.append([c,ell,s,t,h,beta,b1,degree])
 require(scalars==[[2,1,1,1,2,0,1,10]],'P/S scalar contradiction')
 A=[r for r in cyclecovers if all(not(a in r and b in r) for a,b in ((0,4),(4,3),(1,2),(2,5)))]
 D=[r for r in cyclecovers if all(not(a in r and b in r) for a,b in ((0,5),(5,2),(1,3),(3,4)))]
 require(set(A)=={P,S,H} and set(D)=={P,S,K},'T cover descriptions')
 joint=[(a,d) for a in A for d in D if a|d==XS]
 require(set(joint)=={(P,S),(S,P),(H,K)},'T joint rows')
 U=[r for r in cyclecovers if len(r&K)<=2];V=[r for r in cyclecovers if len(r&H)<=2 and len(r&K)<=2]
 require(set(U)=={P,H,P|{5},S,S|{3},L},'SY0 descriptions')
 require(set(V)=={P,S,L},'SY1 descriptions')
 require(all(len(r&K)==2 for r in U),'SY0/T1 saturation')
 uv=[(u,v) for u in U if u not in (H,L) for v in V if len(u|v)>=5]
 require(len(uv)==8,'SY pair union8')
 independent=[r for r in rows if all(not(a in r and b in r) for a,b in CYCLE)]
 require([r for r in independent if len(r)==3]==[S,P] or set(r for r in independent if len(r)==3)=={P,S},'independent triples')
 # Both-SY q: each T incidence is literal; no individual degree floor.
 bothsy=[]
 for missing in independent:
  for t in powers({0,1,2}):
   if not t:continue
   good=(len(missing&P)>=1+int(1 in t)+int(2 in t) and len(missing&S)>=1+int(0 in t)+int(1 in t))
   if good:bothsy.append([sorted(missing),sorted(t)])
 require(not bothsy,'SY Q rows disjoint')
 # Exact all-label T-role cover after final Q ranks are established.
 roles=frozenset(range(6));Aq={0,1};Bq={2,3};Cq={4,5};tcases={}
 for k in (3,4):
  out=[]
  for t0 in powers(roles):
   if len(t0)!=3 or t0&Bq:continue
   for t2row in powers(roles):
    if len(t2row)!=k:continue
    if not Bq<=t2row or len(t2row&Aq)>1 or len(t2row&Cq)>k-3:continue
    if t0|Cq|t2row!=roles:continue
    out.append([sorted(t0),sorted(t2row)])
  require(len(out)==(6 if k==3 else 12),'complete T role cover')
  tcases[k]=out
 return {'cycle_covers':[sorted(r) for r in cyclecovers],'T2_covers':{k:[sorted(r) for r in rs] for k,rs in t2.items()},'proper_C_cuts':propercuts,'leaf_cells':leafcells,'scalar_survivor_then_four_pages':scalars,'A_rows':[sorted(r) for r in A],'D_rows':[sorted(r) for r in D],'joint_T_rows':[[sorted(a),sorted(d)] for a,d in joint],'U_rows':[sorted(r) for r in U],'V_rows':[sorted(r) for r in V],'UV_union_cases':[[sorted(u),sorted(v)] for u,v in uv],'independent_missing_sets':[sorted(r) for r in independent],'both_SY_candidates':bothsy,'T_role_cover':tcases}
def main():
 ap=argparse.ArgumentParser();ap.add_argument('--output',type=Path,required=True);args=ap.parse_args();x=calculate();data=(json.dumps(x,sort_keys=True,separators=(',',':'))+'\n').encode();args.output.parent.mkdir(parents=True,exist_ok=True);args.output.write_bytes(data);print(json.dumps({'bytes':len(data),'sha256':hashlib.sha256(data).hexdigest(),'covers':len(x['cycle_covers']),'Trolecases':[len(x['T_role_cover'][k]) for k in (3,4)]}))
if __name__=='__main__':main()
