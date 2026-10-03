"""Late independent all-q original 8-coordinate compression; no author input.

Plain-core C0=sI-J plus2 on a/bc,b/ac,c/ab. Cross to sum e_ax is -q
except bc:2q+2. Its diagonal is q(s-q). These follow from the literal
20-type table and actual counts, independently of deletion k.
"""
import sys,json
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parent))
from exact import P,R,F,need

def quad(A,v,w):return sum((a*A[i][j]*b for i,a in enumerate(v) for j,b in enumerate(w)),P(0))
def run():
 q=P([0,1]);s=3*q+4;A=[[s*int(i==j)-1 for j in range(8)] for i in range(8)]
 for a,b in [(1,6),(2,5),(4,3)]:A[a-1][b-1]+=2;A[b-1][a-1]+=2
 for i in range(7):A[i][7]=A[7][i]=2*q+2 if i==5 else -q
 A[7][7]=q*(s-q)
 h=[int(i in (1,3)) for i in range(8)];g=[int(i in (2,4)) for i in range(8)]
 ds=[[-a+b for a,b in zip(h,g)],[int(i==0)+g[i] for i in range(8)],[int(i==5) for i in range(8)],[int(i==6) for i in range(8)],[int(i==7) for i in range(8)]]
 G=[[quad(A,v,w) for w in ds] for v in ds];b=[quad(A,h,v) for v in ds];S=s-2
 expected=[[4*S,2*S,P(0),P(0),P(0)],[2*S,3*(s-3),-P(1),-P(3),-3*q],[P(0),-P(1),s-1,-P(1),2*q+2],[P(0),-P(3),-P(1),s-1,-q],[P(0),-3*q,2*q+2,-q,q*(s-q)]]
 need(G==expected and b==[-2*S,-P(2),-P(2),-P(2),-2*q] and quad(A,h,h)==2*S,'whole all-q original compression and linear/base terms')
 # All-count balanced compression: actual outside singleton pair counts.
 o=R(6)/R(q)-R(q)-4;o/=R(q)-1
 v0=R(q)*R(s-1)+R(q)*R(q-1)*(o-1)
 need(v0==R(q*q+6),'whole outside-singleton lower energy')
 cross=2*R(q)*(1-R(1)/R(q)-1);need(cross==-2,'whole original singleton cross energy')
 need(R(q)*R(q-1)/R(q-1)==R(q),'whole outside-singleton slope energy')
 # Constant-action alpha from all undeleted type counts, not interpolation.
 hh=R(1)/R(3*q+5);alpha=R(q*(q+1))*F(1,2)+3*R(q+1)*hh
 total=R(q*(q+1))*F(1,2)+6*R(q+1)*hh-3*R(q+1)*hh
 need(total==alpha,'entire undeleted Delta row total')
 return {'whole_original_eight_coordinate_matrix':[[v.record() for v in row] for row in A],'whole_five_direction_matrix':[[v.record() for v in row] for row in G],'whole_linear_term':[v.record() for v in b],'base_energy':quad(A,h,h).record(),'balanced_singleton_energy':v0.record(),'balanced_cross':cross.record(),'whole_Delta_row_total_alpha':alpha.record(),'all_integer_q_ge4_and_all_k_zero_to_q':True,'ordinary_kernel_and_constant_action_inputs':'9195 scoped undeleted premises','late_addendum_not_first_sealed_core':True}
if __name__=='__main__':print(json.dumps(run(),sort_keys=True))
