"""Independent formal-T scalar, rational circle, moment and shift certificates."""
from exact import P,R,A,F,need


def derive():
    n=R(P([0,1]));T=A(0,1);s=T-n;h=T-1
    b11=(T*(n*n-9*n+16)-n**3+9*n*n-8*n-16)/(n*(n-1))
    b12=2*(T*(-n+4)+2*n*n-4*n-4)/(n*(n-1))
    b22=-4*(T*(-n+2)+2*n*n-2*n-2)/(n*(n-3)*(n-1))
    middle_count=2*T-n*n-n-2
    first_middle=2*(n-2)*middle_count/n
    second_middle=-2*(n-2)*middle_count/(n*(n-1))
    # These reconstruct the complete low row and star equations from literal
    # binomial sums; T remains formal, not 2^(n-1) in these identities.
    low_constraints=[(n-1)*b11+(n-1)*(n-2)*b12/2+first_middle+(n-1)*(n-2)-(T-2),
        (n-1)*b11+(n-1)*(n-2)*b12+first_middle*n/2+(n-1)*(n-2)**2-(n-1)*s,
        (n-2)*b12+(n-2)*(n-3)*b22/2+second_middle+s-(n-2)-(T-2),
        (n-2)*b12+(n-2)*(n-3)*b22+second_middle*n/2+(n-2)*(s-(n-2))-(n-2)*s]
    need(all(x==0 for x in low_constraints),'all four symbolic low affine rows')
    c=2/n;d=-(2*n+5)/(n*n);q1=c+d;q2=c+2*d
    phi=(n*h-n*(n-1)*b11)*q1**2
    phi+=(n*(n-1)*(2*n-3)-n*(n-1)*(n-2)*(n-3)*b22/4)*q2**2
    phi-=(n*(n-1)*(n-2)*b12+2*n*(n-1)*(n-2))*q1*q2
    # With an odd p and p1=p2=1, only low/two-boundary terms survive.
    # Reconstruct these terms before simplifying to the credited scalar.
    lower_low=(n+n*(n-1)/2)*s
    lower_low+=n*(n-1)*b11+n*(n-1)*(n-2)*b12+n*(n-1)*(n-2)*(n-3)*b22/4
    boundary_lower=n*(n-1)/2*s
    boundary_cross=-2*n*(n-1)*(n-2)-n*(n-1)*(s-(n-2))
    # F has no layer n-1, so the unmatched singleton layer has total n:
    # the -J term is -n^2, not zero despite middle-pair oddness.
    lower=lower_low+boundary_lower+boundary_cross-n*n
    need(lower==4*(T-n-1),'entire odd lower energy identity')
    qstar=c*(n-2)/(n-1);b=-1/(2*n)-qstar;v=(2*n+5)**2/(16*n**4)
    bound=lower+phi-(n-1)*qstar**2*middle_count+2*T*(n-1)*(b*b+4*b*v*n+4*(1-b)*v*v*(3*n*n-2*n))
    Apoly=P([-11250,2625,19075,8170,-7608,-7952,592,192]);Rpoly=P([-75,236,-70,-119,28,16])
    claimed=-T*R(Apoly)/(64*n**8)+R(Rpoly)/(n**3*(n-1))
    need(bound==claimed,'whole scalar identity in Q(n)[formal T]')
    rho=P([0,1]);need(4*rho**6+(1+3*rho**2)**2==(1+4*rho**2)*(1+rho**2)**2,'whole normalized rational-circle polynomial')
    # The moment majorant is linear in b; verify both coefficients as exact
    # polynomial identities in the nonnegative parameter t.
    t=P([0,1]);constant=4*t*t*(1+t)**2-4*t*t
    bcoefficient=(4*t-4*t*t)*(1+t)**2-4*t*(1+t)
    need(constant==4*t**3*(2+t) and bcoefficient==-4*t**3*(1+t),'entire moment-majorant remainder including b coefficient')
    shifts={
        'A_minus_128n7':(Apoly-128*P([0,1])**7).shifted(64),
        '20n4_nminus1_minus_R':(20*P([0,1])**4*(P([0,1])-1)-Rpoly).shifted(64),
        'tail_3n_margin':P([25,-5,-16,2]).shifted(64),
        'exponential_induction_margin':P([-1,-2,1]).shifted(64)}
    for name,p in shifts.items():need(all(x>0 for x in p.c),'all coefficients positive at n64 '+name)
    need(2**63>80*64**2,'stronger exponential induction base T>80n^2')
    # Symbolic rational-function and affine equality records are complete;
    # positivity is proved for real n>=64, the exponential bridge for integers.
    return {'four_low_constraints_zero':[x.record() for x in low_constraints],
        'reconstructed_lower_energy':lower.record(),'reconstructed_low_upper_energy':phi.record(),
        'whole_moment_upper_bound':bound.record(),'A_coefficients':Apoly.record(),'R_coefficients':Rpoly.record(),
        'positive_shift_coefficients':{k:p.record() for k,p in shifts.items()},
        'circle_cleared_degree':6,'moment_remainder_coefficients':{'constant':constant.record(),'b':bcoefficient.record()},
        'credited_original_tail_factor':6,'proved_improved_tail_factor':2,
        'uniform_improved_negative_pairing':'W_(n,k)<-T/(4n) when2n^2 B_(n,k)<=T, integer n>=64',
        'uniform_scalar_bound':'W_(n,2)<-2T/n+20n; T>80n^2'}
