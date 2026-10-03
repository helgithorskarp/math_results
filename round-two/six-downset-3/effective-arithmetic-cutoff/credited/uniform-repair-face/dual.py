"""Original affine dual controls and semantic damage rejection.

The finite controls validate the full source mechanism. Uniform slope comes
from the whole coefficient certificates, not from these sampled parameters.
"""
from pathlib import Path
from fractions import Fraction as F
import argparse,copy,hashlib,json
import cap_slope as cs
import zero_generator
lower,inputs,z,r,require=cs.lower,cs.inputs,cs.z,cs.r,cs.require
BASE=Path(__file__).resolve().parent
def source_gate():
    """The full current packet and the pinned credited9980 bytes precede imports."""
    require(inputs.NEW_SOURCE['entire_sources_checked_before_mathematical_import'],
            'complete current source gate before mathematics')
    return {'entire_current_sources_checked_before_mathematics':True}


def aprime(q,k,fields):
    nu,tau=fields
    n0=inputs.coefficient.standard(q,F(0))[0];t0=inputs.coefficient.trivial(q,F(0))[0]
    np=F(z.evaluate(nu['numerator'],q,0),z.evaluate(nu['denominator'],q,0))
    tp=F(z.evaluate(tau['numerator'],q,0),z.evaluate(tau['denominator'],q,0))
    a=inputs.recovery.zero_coefficients(q,k)[0]
    return a*a/F(q)*(F(q-k,k)*np/(n0*n0)+tp/(t0*t0))


def minimize(G,support,anchors,excluded=()):
    O=[i for i in range(len(G)) if i not in support and i not in excluded]
    Y=r.solve(r.submatrix(G,O),r.multiply(r.submatrix(G,O,support),[[F(v)] for v in anchors]))
    x=[F(0)]*len(G)
    for i,v in zip(support,anchors):x[i]=F(v)
    for i,row in zip(O,Y):x[i]=-row[0]
    require(all(r.action(G,x)[i]==0 for i in O), 'ALL original stationary vector equations')
    return x


def check_plane(row):
    q,k=row['q'],row['k'];D=r.forms(q,k);C,U=r.evaluate(D,F(0),F(0),F(0))
    T=[D['keys'].index(key) for key in r.T_KEYS]
    h=[F(value) for value in row['optimizer']];ell=h[1]-h[0]
    low,cap=([F(v) for v in row[name]] for name in ('original_lower_vector','original_cap_vector'))
    require(len(low)==len(cap)==len(C) and len(h)==2, 'whole original dual vector dimensions')
    require([low[i] for i in T]==[0,1,1,ell,ell] and
            [cap[i] for i in T]==[h[0],1,1,h[1],h[1]], 'ALL original prescribed plane anchors')
    O=[i for i in range(len(C)) if i not in T]
    require(all(r.action(C,low)[i]==0 and r.action(U,cap)[i]==0 for i in O),
            'ALL original lower and cap stationarity equations')
    zz=[F(1-int(bool(core&1))-int(bool(core&2))-int(bool(core&4))+int(core.bit_count()>=2))
        for core,z0,w0 in D['keys']]
    require(not any(r.action(C,zz)) and all(not any(r.action(D[name],zz)) for name in ('Rb','Rc','B')),
            'FULL original lower kernel and all repair annihilations')
    alpha=r.pair(D['Delta'],zz)
    expected=F(q*(q+1),2)+F(3*(q+1),3*q+5)
    require(alpha==expected==F(row['kernel_orientation']) and alpha>0,
            'ENTIRE original kernel orientation and kappa nonnegative necessity')
    require(r.pair(D['Delta'],zz,low)==0, 'original best derivative gauge')
    lp=[r.pair(C,low),r.pair(D['Delta'],low),r.pair(D['Rb'],low),r.pair(D['Rc'],low),r.pair(D['B'],low)]
    cp=[r.pair(U,cap),-r.pair(D['Delta'],cap),-r.pair(D['Rb'],cap),-r.pair(D['Rc'],cap),-r.pair(D['B'],cap)]
    combined=[a+b for a,b in zip(lp,cp)]
    require(lp==[F(v) for v in row['original_lower_plane']] and cp==[F(v) for v in row['original_cap_plane']]
            and combined==[F(v) for v in row['combined_original_coefficients']],
            'ALL five original affine energies for both complete vectors')
    require(combined[2:]==[F(0)]*3, 'SEPARATE original tb,tc,sigma coefficients cancel exactly')
    M=inputs.cap.direct(q,k);H=r.submatrix(M,[0,2]);u=[M[0][1],M[2][1]];w=[F(-1),F(1)]
    a=inputs.recovery.zero_coefficients(q,k)[0]
    K=[[H[i][j]+a*w[i]*w[j] for j in range(2)] for i in range(2)]
    y=[u[i]+a*w[i] for i in range(2)]
    require([rr[0] for rr in r.solve(K,[[-v] for v in y])]==h, 'BOTH original optimized joint equations')
    R=M[1][1]+a+sum(y[i]*h[i] for i in range(2))
    require(R==F(row['residual'])==combined[0], 'ENTIRE original dual residual normalization')
    derivative=F(row['a0_derivative'])
    require(lp[1]==derivative*(1+ell)**2, 'full original best-gauge derivative normalization')
    require(combined[1]<0 and combined[1]==F(row['kappa_slope']), 'original strictly negative joint slope')
    return {'all_original_anchors_stationarity_energies_and_cancellations_checked':True}


def control(q,k,fields,old):
    D=r.forms(q,k);C,U=r.evaluate(D,F(0),F(0),F(0))
    T=[D['keys'].index(key) for key in r.T_KEYS]
    M=inputs.cap.direct(q,k);a=inputs.recovery.zero_coefficients(q,k)[0]
    H=r.submatrix(M,[0,2]);u=[M[0][1],M[2][1]];w=[F(-1),F(1)]
    K=[[H[i][j]+a*w[i]*w[j] for j in range(2)] for i in range(2)]
    y=[u[i]+a*w[i] for i in range(2)]
    h=[rr[0] for rr in r.solve(K,[[-value] for value in y])]
    R=M[1][1]+a+sum(y[i]*h[i] for i in range(2));ell=h[1]-h[0]
    n,d=(cs.decode(old[name]) for name in ('joint_residual_numerator','joint_residual_denominator'))
    require(R==F(z.evaluate(n,q,k),z.evaluate(d,q,k)), 'ENTIRE sealed prior scalar residual control')
    gauge=next(i for i,(core,z0,w0) in enumerate(D['keys']) if core==0 and z0+w0==1)
    low=minimize(C,T,[0,1,1,ell,ell],[gauge])
    zz=[F(1-int(bool(core&1))-int(bool(core&2))-int(bool(core&4))+int(core.bit_count()>=2))
        for core,z0,w0 in D['keys']]
    alpha=r.pair(D['Delta'],zz);shift=-r.pair(D['Delta'],zz,low)/alpha
    low=[v+shift*zz0 for v,zz0 in zip(low,zz)]
    cap=minimize(U,T,[h[0],1,1,h[1],h[1]])
    lp=[r.pair(C,low),r.pair(D['Delta'],low),r.pair(D['Rb'],low),r.pair(D['Rc'],low),r.pair(D['B'],low)]
    cp=[r.pair(U,cap),-r.pair(D['Delta'],cap),-r.pair(D['Rb'],cap),-r.pair(D['Rc'],cap),-r.pair(D['B'],cap)]
    total=[v+w0 for v,w0 in zip(lp,cp)]
    row={'q':q,'k':k,'optimizer':h,'residual':R,'a0_derivative':aprime(q,k,fields),
         'kernel_orientation':alpha,'original_lower_vector':low,'original_cap_vector':cap,
         'original_lower_plane':lp,'original_cap_plane':cp,'combined_original_coefficients':total,
         'kappa_slope':total[1],'all_real_face_excluded_at_this_control':R<0 and total[1]<0,
         'uniform_signs_require_separate_whole_certificates':True}
    check_plane(row)
    return row


def damage_probes(row):
    output=[]
    def reject(label,mutate):
        damaged=copy.deepcopy(row);mutate(damaged)
        try:check_plane(damaged)
        except ValueError:output.append({'damage':label,'rejected':True})
        else:raise ValueError('semantic damage accepted: '+label)
    reject('changed original constant',lambda d:d.__setitem__('residual',d['residual']+1))
    reject('invented kappa slope',lambda d:d.__setitem__('kappa_slope',d['kappa_slope']-1))
    reject('wrong physical orientation',lambda d:d.__setitem__('kernel_orientation',d['kernel_orientation']+1))
    reject('changed complete lower vector',lambda d:d['original_lower_vector'].__setitem__(0,d['original_lower_vector'][0]+1))
    reject('changed complete cap vector',lambda d:d['original_cap_vector'].__setitem__(0,d['original_cap_vector'][0]+1))
    reject('omitted independent tc coefficient',lambda d:d['combined_original_coefficients'].__setitem__(3,F(1)))
    reject('incorrect lower derivative metric',lambda d:d.__setitem__('a0_derivative',d['a0_derivative']+1))
    reject('changed original lower affine plane',lambda d:d['original_lower_plane'].__setitem__(4,d['original_lower_plane'][4]+1))
    return output


def verify():
    sealed=source_gate();old=zero_generator.generated()
    fields=(lower.generated('nu'),lower.generated('tau'))
    rows=[control(q,k,fields,old) for q,k in ((21,7),(26,7),(27,7),(32,8),(100,20))]
    probes=damage_probes(rows[3])
    return {'actual_agent':'six-downset-3','role':'researcher','complete_original_controls':rows,
            'all_eight_semantic_damage_probes':probes,'current_complete_source_gate':sealed,
            'CAS_imported':False,'independent_review':False,
            'uniform_slope_requires_the_separate_whole_polynomial_and_ordinary_bridges':True}


if __name__=='__main__':
    ap=argparse.ArgumentParser();ap.add_argument('--out',type=Path,required=True);args=ap.parse_args()
    result=verify();args.out.write_text(json.dumps(r.encode(result),indent=2,sort_keys=True)+'\n')
    print(json.dumps({'full_original_controls':len(result['complete_original_controls']),
                      'rejected_damages':len(result['all_eight_semantic_damage_probes']),
                      'all_kappa_slopes_strict_negative':all(row['kappa_slope']<0 for row in result['complete_original_controls']),
                      'complete_current_source_gate':result['current_complete_source_gate']['entire_current_sources_checked_before_mathematics']}))
