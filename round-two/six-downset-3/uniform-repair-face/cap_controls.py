"""Bounded original cap-derivative compression probes, not a uniform claim."""
from pathlib import Path
from fractions import Fraction as F
import argparse,json
import input as inputs
import lower
r,require=inputs.r,inputs.require


def control(q,k,fields):
    D=r.forms(q,k);_,U0=r.evaluate(D,F(0),F(0),F(0))
    T=[D['keys'].index(key) for key in r.T_KEYS]
    O=[i for i in range(len(U0)) if i not in T]
    anchors=((1,0,0,0,0),(0,1,1,0,0),(0,0,0,1,1))
    V=[]
    for x in anchors:
        Y=r.solve(r.submatrix(U0,O),r.multiply(r.submatrix(U0,O,T),[[F(v)] for v in x]))
        vv=[F(0)]*len(U0)
        for i,v in zip(T,x):vv[i]=F(v)
        for i,row in zip(O,Y):vv[i]=-row[0]
        require(all(r.action(U0,vv)[i]==0 for i in O), 'ALL original cap stationary equations')
        V.append(vv)
    zero=[[r.pair(U0,x,y) for y in V] for x in V]
    require(zero==inputs.cap.direct(q,k), 'ALL9 complete original unrepaired cap values')
    slope=[[r.pair(D['Delta'],x,y) for y in V] for x in V]
    require(all(slope[i][1]==slope[i][2] for i in range(3)),
            'ALL original cap slope columns1 and2 equal at this control')
    negative_minor=slope[0][0]*slope[1][1]-slope[0][1]**2
    try:rank=r.schur_psd(slope);positive=True
    except ValueError:rank=None;positive=False
    nu,tau=fields
    n0=inputs.coefficient.standard(q,F(0))[0];t0=inputs.coefficient.trivial(q,F(0))[0]
    np=F(lower.z.evaluate(nu['numerator'],q,0),lower.z.evaluate(nu['denominator'],q,0))
    tp=F(lower.z.evaluate(tau['numerator'],q,0),lower.z.evaluate(tau['denominator'],q,0))
    a0=inputs.recovery.zero_coefficients(q,k)[0]
    aprime=a0**2/F(q)*(F(q-k,k)*np/n0**2+tp/t0**2)
    ss=(-1,1,1)
    joint=[[slope[i][j]-aprime*ss[i]*ss[j] for j in range(3)] for i in range(3)]
    joint_rank=r.schur_psd(joint)
    require(joint_rank==2 and r.polynomial_psd(joint)[0]==2,
            'TWO full exact algorithms confirm joint slope at this control')
    return {'q':q,'k':k,'whole_minimizing_vectors':V,'whole_zero_cap':zero,
            'whole_Delta_compression':slope,'PSD_at_this_control':positive,'rank_at_this_control':rank,
            'exact_negative_principal_minor':negative_minor,
            'a0_derivative':aprime,'whole_joint_slope_matrix':joint,'joint_rank_at_this_control':joint_rank,
            'uniform_sign_claim':False}


if __name__=='__main__':
    ap=argparse.ArgumentParser();ap.add_argument('--out',type=Path,required=True);args=ap.parse_args()
    fields=(lower.generated('nu'),lower.generated('tau'))
    data={'actual_agent':'six-downset-3','role':'researcher',
          'controls':[control(q,k,fields)
                      for q,k in ((9,3),(21,7),(26,7),(27,7),(32,8),(100,20))],
          'finite_controls_are_not_uniform_proof':True,'independent_review':False}
    args.out.write_text(json.dumps(r.encode(data),indent=2,sort_keys=True)+'\n')
    print(json.dumps({'controls':[[row['q'],row['k'],row['PSD_at_this_control'],row['rank_at_this_control']]
                                  for row in data['controls']]}))
