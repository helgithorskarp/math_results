"""Independent all-original optimizer geometry reader and stronger real interior line."""
import copy,hashlib,json
from collections import Counter
from fractions import Fraction as F
from math import lcm
from geometry import literal,typ,build,outerlift,repairs,integer,need,canon
OLD=16384;DEN=148635648;HD=162;TARGET_ETA=F(1,2**60);NEW_ETA=F(1,2**20)
ZZ=(0,2,0);WW=(0,0,2);BCW=(6,0,1);ZS=(0,1,0);WS=(0,0,1);ABC=(7,0,0)
def key(a,b):return tuple(sorted((a,b)))
def rat(x,label):need(type(x)is str,label+' rational string');return F(x)

def inputs(base,comparison):
 need(integer(base['free_original_entry_denominator'],'base denominator')==DEN,'parent midpoint denominator')
 keys=[tuple(tuple(integer(x,'orbit integer') for x in t) for t in k) for k in base['free_original_entry_orbit_keys']]
 need(keys==sorted(set(keys)) and len(keys)==143 and all(len(k)==2 and all(len(t)==3 for t in k) for k in keys),'whole orbit order')
 nums=base['free_original_entry_numerators'];need(type(nums)is list and len(nums)==143,'whole midpoint values');nums=[integer(x,'midpoint coefficient') for x in nums]
 old=comparison['comparison_free_numerators'];need(type(old)is list and len(old)==143 and integer(comparison['comparison_free_denominator'],'old denominator')==OLD,'whole comparison');old=[integer(x,'old coefficient') for x in old]
 need(base['parent_graph_ref']=='bafkreia6zoi2ypjf2xs2jsdzsoz43vbk6ujexvpagj6x32cryqbthrashq' and base['parent_source_commit']=='40c0527d02729a26498418bcbdf273ca9b2c1a95','exact samecarrier dependency identifiers')
 need(base['parent_real_tau_interval']==['0','1/128'] and rat(base['parent_proper_C_starperp_and_U_floor_for_ALL_real_tau'],'parent floor')==F(1,128),'precise target dependency floor/range')
 return keys,dict(zip(keys,old)),nums


def recipe(old,tau):
 # Open adaptation of own independently derived sparse recipe in REVIEW10312.
 dz=F(32877,OLD)+tau;dw=F(36259,OLD)+tau;db=F(999,OLD)+tau
 a=(dz-db/4)/36;b=db/36;w=(dw-dz+db/4)/21;p=(F(476335,32768)+41*tau)/81;t=(F(20819,OLD)+tau)/9
 change={key(ZZ,WW):-a,key(ZZ,BCW):-b,key(WW,WW):-w,key(ZS,WS):p,key(ZS,ABC):-t}
 values={k:F(v,OLD)+change.get(k,F(0)) for k,v in old.items()};need(all((v*DEN).denominator==1 for v in values.values()),'every primal coefficient decoder')
 return {k:int(v*DEN) for k,v in values.items()}


def rowspace(D,bad,edges,data,damage):
 proper=D[1:];badm=sorted(proper[i] for i in bad);lookup={A:i for i,A in enumerate(badm)};w=data['bad_incidence_rank_witness_edges'];need(type(w)is list and len(w)==81,'complete incidence witness length')
 w=[tuple(integer(x,'witness integer') for x in e) for e in w];need(all(len(e)==2 and e[0]<e[1] and e[0] in lookup and e[1] in lookup and not e[0]&e[1] for e in w) and len(set(w))==81,'all original witness columns')
 if damage=='incidence':w[-1]=(w[-1][0],w[-1][0])
 mat=[[int(A in e) for e in w] for A in badm];need(all(sum(row)==sum(A in e for e in w) for A,row in zip(badm,mat)),'all 6561 literal incidence entries')
 # Independent leaf Laplace elimination, not the author's Bareiss algorithm.
 M=[r[:] for r in mat];sign=1;steps=[]
 while len(M)>3:
  candidates=[i for i,row in enumerate(M) if sum(x!=0 for x in row)==1];need(candidates,'unicyclic witness has literal leaf')
  i=candidates[0];j=next(j for j,x in enumerate(M[i]) if x);v=M[i][j];sign*=(-1)**(i+j)*v;steps.append([i,j,v]);M=[[x for k,x in enumerate(row) if k!=j] for k,row in enumerate(M) if k!=i]
 det=M[0][0]*(M[1][1]*M[2][2]-M[1][2]*M[2][1])-M[0][1]*(M[1][0]*M[2][2]-M[1][2]*M[2][0])+M[0][2]*(M[1][0]*M[2][1]-M[1][1]*M[2][0]);det*=sign
 need(abs(det)==integer(data['bad_incidence_absolute_determinant'],'claimed determinant')==2,'independent full incidence determinant')
 adj={A:[] for A in badm}
 for A,B in w[:80]:adj[A].append(B);adj[B].append(A)
 colors={badm[0]:1};todo=[badm[0]]
 while todo:
  A=todo.pop()
  for B in adj[A]:
   if B not in colors:colors[B]=-colors[A];todo.append(B)
   else:need(colors[B]==-colors[A],'every selected tree parity')
 need(len(colors)==81 and len(w[:80])==80,'full original spanning tree')
 need(colors[w[-1][0]]==colors[w[-1][1]],'extra odd cycle edge closes rank')
 tri=[integer(x,'triangle mask') for x in data['odd_triangle_masks']];need(len(set(tri))==3 and all(x in lookup for x in tri) and all(not x&y for i,x in enumerate(tri) for y in tri[:i]),'entire odd triangle original support')
 dim=len(edges[2])-81+len(edges[0])-1+10280
 if damage=='dimension':dim+=1
 need(dim==integer(data['claimed_affine_dimension'],'claimed dimension')==20711,'complete independent affine dimension')
 return dict(original_bad_vertices=badm,witness_original_edges=[list(e) for e in w],incidence_sha256=hashlib.sha256(canon(mat)).hexdigest(),independent_algorithm='78 leaf Laplace expansions and a complete3x3 determinant, plus all81 tree colors and odd chord',leaf_expansions=steps,remaining_triangle_matrix=M,signed_determinant=det,bad_equation_rank=81,good_total_rank=1,mixed_equalities=9009,anchored_free=10280,affine_dimension=dim,not_a_feasible_set_face_assertion=True)


def perturbation(D,Co,Mo,keys,data,damage):
 proper=D[1:];a=proper.index(1);bad={i for i,A in enumerate(proper) if not A&1 and Mo[0][i+1]<0};need(len(bad)==81 and Counter(typ(proper[i]) for i in bad)==Counter({ZZ:36,WW:36,BCW:9}),'whole bad set')
 H=[[0]*277 for _ in proper];edges={0:[],1:[],2:[]};masses=Counter();counts=Counter();table={};trades=0
 badtypes={key(ZZ,ZZ):F(-1),key(WW,BCW):F(-1),key(ZZ,WW):F(7,18),key(ZZ,BCW):F(7,9),key(WW,WW):F(-1,3)}
 for i,A in enumerate(proper):
  for j,B in enumerate(proper[:i]):
   if A&B or a in (i,j):continue
   k=key(typ(A),typ(B));v=F(0)
   if not A&1 and not B&1:
    cat=int(i in bad)+int(j in bad);edges[cat].append((i,j));v=badtypes.get(k,F(0)) if cat==2 else F(-7804,81) if cat==0 and k==key(ZS,WS) else F(1) if cat==0 else F(0);masses[cat]+=abs(v)
    if v:counts[cat,str(v)]+=1
   else:
    trades+=1
    if k==key(ZS,ABC):v=F(-1);masses['trades']+=1;counts['trades',str(v)]+=1
   if k in table:need(table[k]==v,'orbit formula compatible with literal coordinates')
   table[k]=v;n=v*HD;need(n.denominator==1,'full H rational decoder');H[i][j]=H[j][i]=n.numerator
 need(set(table)==set(keys),'every H free orbit covered')
 if damage=='degree':i,j=edges[2][0];H[i][j]+=HD;H[j][i]+=HD
 for i,A in enumerate(proper):
  if not A&1:H[i][a]=H[a][i]=-sum(H[i][j] for j,B in enumerate(proper) if B&1 and j!=a)
 need(all(sum(row[j] for j,A in enumerate(proper) if A&1)==0 for row in H),'every H star row')
 need(all(sum(H[i][j] for j in bad)==0 for i in bad),'every individual bad degree preserved')
 need(sum(H[i][j] for i,j in edges[0])==0,'whole good total preserved')
 need([len(edges[k]) for k in (0,1,2)]==[7885,9009,2628] and trades==10280,'complete coordinate class census')
 need([masses[k] for k in (2,0,'trades')]==[1512,15608,9],'whole H independent coordinate masses')
 for name,k in [('claimed_bad_bad_free_l1',2),('claimed_good_good_free_l1',0),('claimed_anchored_free_l1','trades')]:need(rat(data[name],name)==masses[k],'supplied masses checked after whole calculation')
 need(integer(data['perturbation_denominator'],'Hden')==HD,'whole supplied H denominator');skeys=[tuple(tuple(integer(x,'Hkeyinteger') for x in t) for t in k) for k in data['free_original_entry_orbit_keys']];snums=data['free_original_perturbation_numerators'];need(skeys==keys and type(snums)is list and len(snums)==143,'complete supplied H order/values');snums=[integer(x,'Hcoefficient integer') for x in snums];need(snums==[int(table[k]*HD) for k in keys],'all143 supplied H coefficients independently bound')
 row=[sum(r) for r in H];LH=[[sum(row) if i==j==0 else -row[(i or j)-1] if not i or not j else H[i-1][j-1] for j in range(278)] for i in range(278)]
 need(all(sum(r)==0 for r in LH),'every original Hlift row');need(all(not A&B or LH[i][j]==0 for i,A in enumerate(D) for j,B in enumerate(D)),'all original Hlift support')
 forced={(0,0)}|{(0,i+1) for i in bad}|{(i+1,0) for i in bad};need(len(forced)==163 and all(LH[i][j]==0 for i,j in forced),'all forced entries unchanged')
 need(LH[0][D.index(7)]==LH[D.index(7)][0]==9*HD,'abc original empty slope')
 f2=F(sum(x*x for row in H for x in row),HD**2);formula=2*(378+252+1296*F(7,18)**2+324*F(7,9)**2+378*F(1,3)**2+81*F(7804,81)**2+7804+18)
 need(f2==formula==F(123244364,81) and f2<1280**2,'entire proper Frobenius H norm')
 need(rat(data['claimed_proper_operator_coefficient_bound'],'old norm')==17138 and rat(data['claimed_actual_entry_coefficient_bound'],'old entry')==34249,'written coarse budgets')
 need(rat(data['eta'],'old eta')==TARGET_ETA and rat(data['published_parent_C_starperp_and_U_uniform_floor'],'targetfloor')==F(1,128) and rat(data['derived_C_starperp_and_U_uniform_floor'],'targetpaidfloor')==F(1,256),'exact original eta and PSD transfer')
 if damage=='norm':need(f2<1024**2,'deliberately false smaller physical norm')
 return H,LH,bad,edges,forced,table,dict(coordinate_count=29802,NN_counts=[len(edges[k]) for k in (0,1,2)],anchored_count=trades,mass_bad=str(masses[2]),mass_good=str(masses[0]),mass_trades=str(masses['trades']),slope_type_counts=[[list(k) if type(k)is tuple else k,v] for k,v in sorted(counts.items(),key=lambda x:str(x[0]))],all81_bad_degrees_zero=True,whole_good_total_zero=True,proper_H_frobenius_squared=str(f2),new_operator_upper=1280,maximum_actual_H_entry=str(F(max(abs(x) for row in LH for x in row),HD)),proper_H_sha256=hashlib.sha256(canon(H)).hexdigest(),actual_Hlift_sha256=hashlib.sha256(canon(LH)).hexdigest(),forced_ordered_masks=[[D[i],D[j]] for i,j in sorted(forced)],all143_author_H_values_bound=True)


def point(D,parent,Co,H,LH,table,bad,edges,forced,tau,eta,damage):
 C,U,L,M=parent;den=lcm(DEN,eta.denominator*HD);hs=eta*den/HD;need(hs.denominator==1,'exact interior common denominator');hs=hs.numerator
 nt={k:int(F(n,DEN)*den+eta*table[k]*den) for k,n in recipe(OLD_TABLE,tau).items()};Ci,Ui,Li,Mi=build(D,nt,den)
 need(all(Ci[i][j]==C[i][j]*(den//DEN)+hs*H[i][j] and Ui[i][j]==U[i][j]*(den//DEN)-hs*H[i][j] for i in range(277) for j in range(277)),'all proper interior reconstruction')
 need(all(Mi[i][j]==M[i][j]*(den//DEN)+hs*LH[i][j] for i in range(278) for j in range(278)),'all actual interior reconstruction')
 if damage=='loop':Mi[0][0]+=1
 if damage=='empty':Mi[0][D.index(7)]-=20*eta.numerator*(den//eta.denominator)
 need(all(sum(row)==220*den for row in Mi),'every actual perturbed row')
 tauN=tau*den;need(tauN.denominator==1,'exact interior floor');slacks=[];floors=[];strict=[];basemin=[]
 for i,A in enumerate(D):
  for j,B in enumerate(D):
   if A&B:continue
   base=F(M[i][j],DEN)-tau;s=F(Mi[i][j],den)-tau;need(s>=0,'every original interior allowed entry floor');slacks.append(s)
   if base>0:basemin.append(base)
   if s==0:floors.append((i,j))
   else:strict.append(s)
 need(set(floors)==forced,'exact163 forced ordered entry floors');need(min(strict)>=9*eta and Mi[0][D.index(7)]*eta.denominator==9*eta.numerator*den+tauN.numerator*eta.denominator,'all unforced strict margins including abc')
 if damage=='margin':need(min(strict)>=10*eta,'deliberately unpaid stronger entry margin')
 d=F(2497887,OLD);P=T=F(0);marg=[]
 for k in (0,1,2):
  for i,j in edges[k]:
   r=F(Ci[i][j],den)-F(Co[i][j],OLD)
   if k==0:need(r>=eta,'every good repair strict');marg.append(r)
   elif k==2:need(r<=-eta,'every bad repair strict');marg.append(-r)
   else:need(r==0,'every mixed repair fixed')
   P+=max(r,F(0));T+=max(-r,F(0))
 need(P==F(476335,32768)+41*tau and T==d/2+F(81,2)*tau,'complete NN optimum and decreasing mass')
 proper=D[1:]
 for i in bad:
  deficit={ZZ:F(32877,OLD),WW:F(36259,OLD),BCW:F(999,OLD)}[typ(proper[i])];degree=sum(F(Ci[i][j],den)-F(Co[i][j],OLD) for j in bad if i!=j and not proper[i]&proper[j]);need(degree==-deficit-tau,'each original bad degree equation')
 return dict(tau=str(tau),eta=str(eta),common_denominator=den,all77284_original_entries_reconstructed=True,all60597_allowed_entries_checked=True,forced_ordered_entries=len(floors),minimum_unforced_C_unit_surplus=str(min(strict)),minimum_strict_NN_repair=str(min(marg)),minimum_parent_unforced_C_unit_surplus=str(min(basemin)),P=str(P),T=str(T),all81_bad_equations=True,whole_original_matrices_sha256={k:hashlib.sha256(canon(v)).hexdigest() for k,v in [('C',Ci),('U',Ui),('L',Li),('Mnum',Mi)]})


def make(base,comparison,data,damage='none'):
 global OLD_TABLE
 base=copy.deepcopy(base);comparison=copy.deepcopy(comparison);data=copy.deepcopy(data)
 if damage=='float':data['free_original_perturbation_numerators'][0]=float(data['free_original_perturbation_numerators'][0])
 if damage=='boolean':data['free_original_perturbation_numerators'][0]=True
 if damage=='key':data['free_original_entry_orbit_keys'].pop()
 if damage=='coefficient':data['free_original_perturbation_numerators'][0]+=1
 if damage=='parent-coefficient':base['free_original_entry_numerators'][0]+=1
 if damage=='dependency':base['parent_graph_ref']='wrong'
 keys,OLD_TABLE,values=inputs(base,comparison);D,stars=literal();Co,Uo,Lo,Mo=build(D,OLD_TABLE,OLD);H,LH,bad,edges,forced,htable,hrec=perturbation(D,Co,Mo,keys,data,damage);rank=rowspace(D,bad,edges,data,damage);budget,face=repairs(D);records=[]
 for tau in (F(0),F(1,128),F(1,64)):
  table=recipe(OLD_TABLE,tau)
  if tau==F(1,128):need([table[k] for k in keys]==values,'entire supplied parent midpoint recipe binding')
  parent=build(D,table,DEN);zero={(i,j) for i,A in enumerate(D) for j,B in enumerate(D) if not A&B and F(parent[3][i][j],DEN)==tau};need(zero==forced|{(0,D.index(7)),(D.index(7),0)},'entire parent165 floor positions')
  if tau!=F(1,64):records.append(point(D,parent,Co,H,LH,htable,bad,edges,forced,tau,TARGET_ETA,damage))
  records.append(point(D,parent,Co,H,LH,htable,bad,edges,forced,tau,NEW_ETA,damage))
 oldfloor=F(1,128)-17138*TARGET_ETA;need(oldfloor>=F(1,256),'original precise samecarrier PSD dependency paid')
 newfloor=F(11,1024)-1280*NEW_ETA;need(newfloor==F(39,4096)>F(1,128),'new whole-interval physical norm paid')
 if damage=='spectral':need(F(11,1024)-1280*F(1,65536)>0,'deliberately unpaid enlarged step spectral budget')
 return dict(actual_agent='six-reviewer-5',role='independent mathematical reviewer',carrier=dict(N=278,proper=277,s=58,stars=stars),affine_space=face,rank_and_dimension=rank,interior_perturbation=hrec,full_original_interior_endpoints=records,target_all_real_tau_interval=['0','1/128'],new_all_real_tau_interval=['0','1/64'],target_eta=str(TARGET_ETA),new_eta=str(NEW_ETA),proved_interior_eta_factor=2**40,target_proper_floor='1/256',new_uniform_proper_floor=str(newfloor),new_uniform_actual_gap=str(newfloor/220),new_uniform_unforced_M_surplus=str(9*NEW_ETA/220),new_uniform_strict_NN_repair=str(NEW_ETA),both_actual_endpoint_ranks=277,simple_extreme_M_eigenvalues=['-29/110','1'],exact_ri_iff='For M in O_tau: all E2 strictly negative/E0 strictly positive; every allowed unforced original entry above tau/220; C positive on hperp. No extra upperPSD test is required.',every_real_optimizer_continuation='(1-t)M+t*interior in ri for EVERY0<t<=1; both276 nonextreme eigenvalues have gap>=t*39/901120 on enlarged tau interval.',dependency='Explicit mathematical use of independently audited original sparse theorem10296 and REVIEW10312 on identical carrier/comparison; source bfa286572e2ef4cf6b301fb926eab339eed7a715; no current/old PSD factor rerun or imported.',trust_boundary='UNFORMALIZED original affine completeness, unsigned-incidence/tree determinant rank, relative interior supporting-functional/Slater neighborhoods, stochastic Laplacian, exact samecarrier PSD lemma, norm/congruence/ranks and all-real parameter convexity. Author written+coefficient/witness DATA exposed. Own published literal/sparse recipe openly reused; new H/rank/whole interior checks independent. No author code/EXPECTED/private corpus or chart/cube proof used.')
