"""Fresh actual opposite-double companion/cofactor audit, all coefficients.
Standard library only. Old own reviewed polynomial maps are cross-multiplied
against the newly constructed actual-ring formula before sign inference."""
from pathlib import Path
import sys,json,argparse,signal
sys.path.insert(0,str(Path(__file__).resolve().parent))
from arithmetic import *
cli=argparse.ArgumentParser();cli.add_argument('--record',type=Path);cli.add_argument('--damage');args=cli.parse_args()
signal.alarm(45)
need(args.damage in [None,'mass-factor','last-numerator','denominator-factor','critical-slot','odd-coefficient'],'known semantic defect')
s=p;lam=t
d=[-one,s,one];B=[-one,-s,one];U=zmul(B,B);r=[s*s-1,-2*s,one]
Q=[U[i]+(lam*r[i]if i<3 else P())for i in range(5)]
f=zmul(zmul(d,d),Q)
if args.damage=='odd-coefficient':f[1]=f[1]+1
H=[lam*s**3/4,-lam*s*s/4-3*lam/4+s*s/2+1,-3*lam*s/4+s**3/2+s,3*lam/4-s*s/2-2,-s,one]
need([x/8 for x in zdiff(f)]==zmul(d,H),'entire actual derivative')
N=8+4*s*s-2*lam;X=8+16*s*s+4*s**4-4*lam+2*lam*lam;D=X-N*N/8
mu=newton(f,8)
need(mu[1]==mu[3]==mu[5]==P()and mu[2]==N and mu[4]==X,'entire original moment slots')
need(f[1]==-2*s**3*lam and f[3]==f[5]==f[7]==P(),'all remaining odd original coefficients')
need(D==F(3,2)*(lam+F(2,3)*s*s)**2+F(4,3)*s**4+8*s*s,'positive completed square')
M=matrix(5)
for i in range(1,5):M[i][i-1]=one
for i in range(5):M[i][4]=-H[i]
need(evalm(H,M)==matrix(5),'entire actual quotient')
der=evalm(zdiff(H),M);delta=det(der);inv=adj(der)
need(multiply(der,inv)==scale(eye(5),delta)==multiply(inv,der),'all two-sided inverse entries')
W=scale(multiply(evalm(zmul(d,Q),M),inv),-8)
if args.damage=='mass-factor':W=scale(W,F(1,8))
need(trace(W)==N*delta,'all five actual positive-mass normalization')
eta_num=trace(multiply(W,W));top=N*N*delta*delta-eta_num;bottom=D*delta*delta
inputs=json.loads((Path(__file__).resolve().parent/'INPUT.json').read_text())
need(set(inputs)=={'num_p_t','den_p_t','delta_p_t'},'whole own input schema')
def rotate(q):
    need(all(i%2==0 for i,j in q),'complete old even parity')
    return P({(i,j):v*(-1)**(i//2)for(i,j),v in q.items()})
num=rotate(decode(inputs['num_p_t']));den=rotate(decode(inputs['den_p_t']))
if args.damage=='last-numerator':num.pop(max(num))
need(delta==rotate(decode(inputs['delta_p_t'])),'every actual derivative norm coefficient')
if args.damage=='denominator-factor':den=den*2
need(den==8192*D*delta,'entire positive actual denominator factor')
need(top*den==bottom*num,'all500 angular trace coefficients')
need(len(top*den)==500 and len(num)==71 and len(den)==70,'complete identity census')
# Original two-double zero slots supplement the five strictly interlacing gaps.
masses=[P(),P()];slots=['zero-double-positive','zero-double-negative']+[f'gap-{j}'for j in range(5)]
if args.damage=='critical-slot':slots.pop(1)
need(len(slots)==7 and len(masses)==2 and slots[:2]==['zero-double-positive','zero-double-negative'],'all seven original critical slots')
stationary=[-s**3,3*s*s-1,-3*s,one]
diff=[a-b for a,b in zip(zmul(zdiff(U),r),zmul(U,zdiff(r)))]
need(diff==[2*x for x in zmul(B,stationary)],'whole negative stationary numerator')
# A separate singular coefficient specialization leaves the quartic constant free.
E=p;G=t
even=zmul(zmul([-one,P(),one],[-one,P(),one]),[G,P(),E,P(),one])
need(even[1]==even[3]==even[5]==even[7]==P(),'entire singular-even branch')
need(evalz([1,E,G][::-1],one)==1+E+G,'singular branch disjointness factor')
# All coefficient conditions at s>0 have nonzero divisor2s; s=0 is not divided.
normal_conditions={'z7':'q3+2s','z5':'q1+2s*q2-2s^3+2s','z3_after_first_two':'2s*(q0-1-(s^2-1)*lambda)','s0':'q3=q1=0; q0,q2 free'}
record=encode({'agent':'six-reviewer-1','role':'independent mathematical reviewer','actual_octic':f,'actual_Q4':Q,'all8_original_moments':mu[1:],'positive_Draw':D,'actual_H5':H,'entire_companion':M,'derivative_norm':delta,'whole_cofactor_inverse':inv,'whole_actual_mass_numerator':W,'whole_squared_mass_numerator':eta_num,'all500_cleared_identity_coefficients':top*den,'angular_numerator_s_lambda':num,'angular_denominator_s_lambda':den,'all_seven_slot_labels':slots,'negative_ratio_stationary':stationary,'singular_even_octic':even,'coefficient_case_equations':normal_conditions,'physical_inverse_license':'actual real interlacing and D>0; ordinary proof, not generic polynomial nonzero alone'})
data=json.dumps(record,sort_keys=True,separators=(',',':')).encode()
if args.record:args.record.write_bytes(data)
else:print(data.decode())
