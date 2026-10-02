"""Independent quantitative consequences and literal original matrix control."""
from fractions import Fraction as Q
from itertools import combinations
from independent import data,require
import hashlib,json

def consequences(n):
 d=data(n);norm=sum(d['counts'][a]*d['u'][a]**2 for a in d['counts']);den=d['mu']-d['f'][3]**2
 require(norm>0 and den>0 and d['eta']<0,'consequence signs')
 return {'n':n,'upper_test_squared_norm':str(norm),'positive_mass_floor':str(-d['eta']/(2*d['h']*den)),'S2_lambda_max_M_minus1_floor':str(-d['eta']/(d['h']*norm)),'S2_lambda_max_L_minusN_floor':str(-d['eta']/norm)}

def literal(n):
 """Partition core control: actual matrix, no PSD or coefficient quotient assumptions.
 Singleton layer is one group; every other group is a complementary middle pair.
 There are s groups. C=s sum g_j g_j^T-J is PSD by Cauchy--Schwarz.
 Point-star indicators meet each group once. This is a known ordinary H,
 credited to the partition/near-cube results, not a new capped construction.
 """
 d=data(n);s,h,N=d['s'],d['h'],d['N'];full=(1<<n)-1
 masks=[a for a in range(1,full) if a.bit_count()<=n-2];position={a:i for i,a in enumerate(masks)}
 group={a:0 for a in masks if a.bit_count()==1};gid=1
 for a in masks:
  if a not in group:group[a]=group[full^a]=gid;gid+=1
 require(gid==s,'s partition groups')
 C=[[s*(a==b or (a&b==0 and (a.bit_count()==b.bit_count()==1 or a^b==full)))-1 for b in masks] for a in masks]
 require(all(C[i][j]==s*(group[a]==group[b])-1 for i,a in enumerate(masks) for j,b in enumerate(masks)),'literal partition Gram')
 row=[sum(v) for v in C];L0=[1-x for x in row];loop=1+sum(row)
 L=[[loop]+L0]+[[L0[i]]+[C[i][j]+1 for j in range(len(masks))] for i in range(len(masks))]
 actual=[0]+masks
 require(all(sum(row)==N for row in L),'actual full regularity')
 require(all(L[i][j]==(s if i==j else 0) for i,a in enumerate(actual) for j,b in enumerate(actual) if a&b),'actual support including nonempty diagonal')
 require(all(L[i][j]==L[j][i] for i in range(N) for j in range(N)),'actual symmetry')
 stars=0
 for k in range(n):
  chosen=[i for i,a in enumerate(actual) if a&(1<<k)]
  require(len(chosen)==s,'actual star size')
  for i in range(N):require(sum(L[i][j] for j in chosen)==s,'actual forced point-star equation');stars+=1
 # Evaluate the two quadratic forms directly, and separately every original coefficient.
 u=[d['u'][a.bit_count()] for a in masks];ell=[d['ell'][a.bit_count()] for a in masks];card=[a.bit_count() for a in masks]
 def quad(x):return sum(x[i]*x[j]*C[i][j] for i in range(len(masks)) for j in range(len(masks)))
 lower=quad(ell);upper=N*sum(x*x for x in u)-sum(u)**2-quad(u)
 Phi=upper+d['mu']*lower;defect=sum((2*u[i]-card[i])*sum(C[i][j]*card[j] for j in range(len(masks))) for i in range(len(masks)))
 Z=sum((d['mu']-d['w'][a.bit_count()])*(s-L[position[a]+1][position[full^a]+1]) for a in masks if 3<=a.bit_count()<=n-3)
 weighted=Q(0);proper=0
 for i,a in enumerate(masks):
  for j,b in enumerate(masks[i+1:],i+1):
   if not a&b and a.bit_count()>=3 and b.bit_count()>=3 and a|b!=full:
    weighted+=(d['mu']-d['f'][a.bit_count()]*d['f'][b.bit_count()])*L[i+1][j+1];proper+=1
 require(defect==0 and Phi==d['eta']-Z+2*weighted,'literal original identity')
 require(weighted==0,'literal S2 support')
 # Deliberately break a physical disjoint edge: support/row completion survives,
 # cardinality kernel does not. Full defect must account for the exact difference.
 a=7;b=full^a
 i,j=position[a],position[b];change=Q(1,7)
 direct_change=2*change*(d['mu']*ell[i]*ell[j]-u[i]*u[j])
 rhs_change=2*change*(d['mu']-d['w'][a.bit_count()])
 defect_change=change*((2*u[i]-card[i])*card[j]+(2*u[j]-card[j])*card[i])
 require(defect_change!=0 and direct_change==rhs_change-defect_change,'physical kernel damage catches missing defect')
 fingerprints=hashlib.sha256(json.dumps(L,separators=(',',':')).encode()).hexdigest()
 return {'n':n,'vertices':N,'groups':s,'full_original_entries':N*N,'point_star_equations':stars,'actual_empty_L_loop':loop,'actual_empty_L_singleton':L0[0],'actual_empty_L_middle':n-1,'lower_energy':str(lower),'upper_energy':str(upper),'Phi':str(Phi),'kernel_defect':str(defect),'proper_pairs':proper,'physical_damaged_kernel_defect':str(defect_change),'full_original_matrix_sha256':fingerprints,'ordinary_PSD_proof':'partition Cauchy--Schwarz plus actual empty lift; cap not claimed'}

def run():return {'literal_original_controls':[literal(n) for n in (6,8)],'quantitative_consequences':[consequences(n) for n in (11,12,16,20,32,64)]}
if __name__=='__main__':print(json.dumps(run(),indent=2))
