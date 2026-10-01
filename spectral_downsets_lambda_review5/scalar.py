"""Independent exact scalar audit and complement-STS upper-cap certificates."""
import argparse
from fractions import Fraction as F
from hashlib import sha256
import json
from pathlib import Path
from exact import need, determinant3, psd_rank
from symbols import Rat, coefficients


def formulas(v, lam):
    v, lam = Rat.cast(v), Rat.cast(lam)
    m, b, r, u = v*(v-1)/2, lam*v*(v-1)/6, lam*(v-1)/2, lam*(lam-1)/2
    s, N = v+r, 1+v+m+b
    D = lam*(v*v-10*v+27)-6
    E = 3*lam*v*v-3*lam*v-16*lam+6*v
    a = -lam/3
    c = (v*v-(lam+3)*v+11*lam/3)/((v-2)*(v-3))
    d = (v*v-v-4)/((v-4)*(v-3))
    t = (v-1)*(lam*(v-3)-6)/D
    w = s-(v-3)*c-(r-2*lam)*d
    h = s-(v-4)*d-(r-3*lam)*t
    alpha1 = E/(6*(v-2))
    alpha2 = s+c
    beta = t-d*d/alpha2
    gamma = t-4*d*d/(alpha2*(v-2))+d*d*(v-4)**2/((v-2)*alpha1)
    red = t*(v-6)/(v-2)+d*d*(v-4)**2/((v-2)*alpha1)
    mu = s-t-(r-lam)*red
    A = (r-lam)*d*d*(v-4)**2/(v-2)
    P = (lam**4*(3*v**5-15*v**4+5*v**3+55*v*v-48*v)
         +lam**3*(-19*v**5+127*v**4-203*v**3-235*v*v+618*v)
         +lam**2*(3*v**6-12*v**5-68*v**4+438*v**3-223*v*v-2034*v+2592)
         +lam*(-6*v**5+108*v**4-642*v**3+1452*v*v-816*v-576)
         +36*v**3-180*v*v+216*v)
    return locals()


def run():
    v = Rat(((13,), (1,)))
    lam = Rat(((2, 1),))
    f = formulas(v, lam)
    a,c,d,t,w,h = (f[x] for x in ('a','c','d','t','w','h'))
    m,b,r,u,s,N,D,E = (f[x] for x in ('m','b','r','u','s','N','D','E'))
    alpha1,alpha2,beta,gamma,red,mu,A,P = (f[x] for x in ('alpha1','alpha2','beta','gamma','red','mu','A','P'))
    eta = 1/(8*v*v)
    ap = alpha1-eta*(v-3)
    rp = t*(v-6)/(v-2)+d*d*(v-4)**2/((v-2)*ap)
    identities = {
        'triple_star': h+(v-4)*d+(r-3*lam)*t-s,
        'triple_row': 1+s+(v-3)*h-3*(lam-1)*t+(v-3)*(v-4)*d/2+(b-3*r+3*lam-1)*t-N,
        'pair_star': w+(v-3)*c+(r-2*lam)*d-s,
        'pair_row': 1+s+(v-2)*w-lam*d+(v-2)*(v-3)*c/2+(b-2*r+lam)*d-N,
        'point_star': a+(v-2)*w-lam*d+(r-lam)*h-3*u*t-s,
        'point_row': 1+s+(v-1)*a+(v-1)*(v-2)*w/2-r*d+(b-r)*h-(lam-1)*r*t-N,
        # Independently select c,d,t by the three constant-block equations.
        'solve_c_constant': c-(m-s+4*lam/3)/(m-2*v+3),
        'solve_d_constant': d-(b-2*lam/3)/(lam-2*r+b),
        'solve_t_constant': t-(b-s+1)/(3*lam-1-3*r+b),
        'constant_trace': s-a+(a-1)*v+4*lam/3+1-(lam*(v+7)/6+1),
        'expanded_w': w-(lam*v*v+11*lam*v-36*lam+3*v**3-21*v*v+36*v)/(3*(v-4)*(v-3)*(v-2)),
        'expanded_h': h-(3*lam*lam*(v-1)*(v-3)+lam*(v**3-12*v*v+11*v+36)+12*v-24)/((v-3)*D),
        'point_standard': s-c*(v-3)-alpha1,
        'Schur_reduction': gamma-4*beta/(v-2)-red,
        'Schur_margin': mu-1/lam-P/(lam*(v-3)*(v-2)*D*E),
        'perturbed_Schur_loss': s-t-(r-lam)*rp-(mu-A*eta*(v-3)/(alpha1*ap)),
        'density': N-2*s-(v-1)*((v-2)/2+lam*(v-6)/6),
    }
    for ll in (2,3):
        old = {'a': Rat(-F(ll,3)), 'd': d,
               't': (v-1)/(v-ll-2)}
        if ll == 2:
            old.update(w=1+4*v*(2*v-5)/(3*(v-2)*(v-3)*(v-4)),
                       c=1+4/(3*(v-2)*(v-3)), h=(v*v-7)/((v-3)*(v-4)))
        else:
            old.update(w=(v**3-6*v*v+23*v-36)/((v-4)*(v-3)*(v-2)),
                       c=(v*v-6*v+11)/((v-2)*(v-3)), h=(v*v+2*v-11)/((v-5)*(v-3)))
        specialized = formulas(v, ll)
        for key,value in old.items():
            identities['specialize_'+str(ll)+'_'+key] = specialized[key]-value
    for name,value in identities.items():
        need(value.equals(0), 'independent symbolic identity: '+name)
    base = {'D':D,'E':E,'P':P,'alpha1_gt_lv_over_2':alpha1-lam*v/2,
            'alpha2_gt_v':alpha2-v,'t_gt_1':t-1,'t_lt_2':2-t,
            'd_positive':d,'d_lt_2':2-d,'w_positive':w,'h_positive':h,
            'A_lt_2lv2':2*lam*v*v-A,'c_lt_4_over_3':Rat(F(4,3))-c,
            'v_gt_4':v-4,'v_gt_2':v-2,
            'c_simplicity_lower':(8*v-22)/(3*(v-2)*(v-3))}
    records = {'base_'+name:value.strict_record(name) for name,value in base.items()}
    fc = formulas(24*lam+Rat(((0,), (1,))),lam)
    cv,cl,cs,cN,cu = (fc[x] for x in ('v','lam','s','N','u'))
    cap = {'w_lt_3_over_2':Rat(F(3,2))-fc['w'], 'd_lt_3_over_2':Rat(F(3,2))-fc['d'],
           'h_lt_2':2-fc['h'],'t_lt_4_over_3':Rat(F(4,3))-fc['t'],
           'diag1_lt_l2v':cl*cl*cv-(cs+cl/3+F(4,3)*cu*cv),
           'diag2_lt_l2v':cl*cl*cv-(cs+F(4,3)),
           'diag3_lt_l2v':cl*cl*cv-(cs+F(4,3)*(3*cl-1)),
           'constant_lt_2l2v':2*cl*cl*cv-(cl*(cv+7)/6+1),
           'gap_gt_v2_over_4':cN-2*cl*cl*cv-cv*cv/4,
           'pair_cross':cl*cl-cl-1,'point_triple_cross':3*cl-5,
           'pair_triple_cross':2*cl-3,'sqrtv_comparison':cv-36,'sqrtlv_comparison':cv-16*cl,
           'constant_lt_27_over_16_l2v':F(27,16)*cl*cl*cv-(cl*(cv+7)/6+1)}
    records.update({'cap_'+name:value.strict_record(name) for name,value in cap.items()})
    # Independently audit the inherited centered lambda3 cap (not its old
    # perturbation interval). The present all-lambda repair proof is separate.
    three = formulas(v,3)
    three_caps = {'w_lt_3_over_2':Rat(F(3,2))-three['w'],
                  'c_lt_1':1-three['c'],'c_positive':three['c'],
                  'h_lt_5_over_2':Rat(F(5,2))-three['h'],
                  'centered_gap':three['N']-F(25,2)*v,
                  'row1_margin':v/3,'row2_margin':(11*v-12)/2,
                  'row3_margin':(26*v-99)/6}
    records.update({'lambda3_'+name:value.strict_record(name) for name,value in three_caps.items()})
    need((Rat(F(3,2))-three['t']).equals((v-13)/(2*(v-5))),
         'inherited weak t upper-bound identity')
    # Complementing the triple layer preserves its point completion defect.
    complement = v-2-lam
    rc,uc = complement*(v-1)/2,complement*(complement-1)/2
    need((r-u).equals((v-2)-2*complement+rc-uc), 'complement Z invariant scalar')
    fd = formulas(v,v-3)
    dl,ds,dN = (fd[x] for x in ('lam','s','N'))
    dense_bound = dl*v+5*v+6*dl
    dense = {'one_minus_d_minus_w':1-fd['d']+fd['w'],
             'one_plus_d_minus_w':1+fd['d']-fd['w'],
             'two_minus_h_minus_3t':2-fd['h']+3*fd['t'],
             'two_plus_h_minus_3t':2+fd['h']-3*fd['t'],
             'c_positive':fd['c'],
             'sqrtv_at_most_v_over_3':v*v/9-v,
             'sqrt2lambda_lt_lambda_over_2':dl*dl/4-2*dl,
             'lambda_below_v':v-dl,
             'row1':dense_bound-(ds+dl/3+29*v/6),
             'row2':dense_bound-(ds+F(4,3)+5*v/6+dl*v/2),
             'row3':dense_bound-(ds+6*dl-2+4*v+dl*v/2),
             'constant':dense_bound-(dl*(v+7)/6+1),
             'gap_gt_v2_over_4':dN-dense_bound-v*v/4}
    nxt=formulas(v+1,v-2)
    dense['density_strictly_decreasing']=ds/dN-nxt['s']/nxt['N']
    records.update({'complement_STS_'+name:value.strict_record(name) for name,value in dense.items()})
    need(dense_bound.equals(v*v+8*v-18), 'dense bound simplification')
    need((dN-dense_bound).equals((v**3-7*v*v-42*v+114)/6), 'dense gap simplification')
    need(F(3,2)**2>2 and F(5,2)**2>6 and F(3,4)**2>F(1,2) and F(5,4)**2>F(3,2)
         and F(9,4)**2>F(9,2) and F(17,4)**2>18,
         'rational radical comparison')
    comparison = [[F(1),F(1,4),F(1,4)],[F(1,4),F(1),F(1,2)],[F(1,4),F(1,2),F(1)]]
    margin = [[F(27,16)*(i==j)-comparison[i][j] for j in range(3)] for i in range(3)]
    minors = [margin[0][0],margin[0][0]*margin[1][1]-margin[0][1]**2,determinant3(margin)]
    need(minors == [F(11,16),F(105,256),F(19,4096)] and psd_rank(margin)==3,
         'fixed generic cap comparison')
    return {'identity_names':list(identities),'identity_count':len(identities),
            'positive_certificates':records,'positive_certificate_count':len(records),
            'Schur_P_shifted_coefficients':coefficients(P.n),
            'base_domain':'v=13+x,lambda=2+y; x,y>=0',
            'cap_domain':'v=24lambda+x,lambda=2+y; x,y>=0',
            'dense_domain':'v=13+x,lambda=v-3; x>=0',
            'generic_improved_cap':'27lambda^2 v/16',
            'comparison_Sylvester_minors':list(map(str,minors)),
            'dense_centered_cap':'v^2+8v-18',
            'dense_gap':'(v^3-7v^2-42v+114)/6'}


if __name__ == '__main__':
    parser=argparse.ArgumentParser()
    parser.add_argument('--write',type=Path)
    parser.add_argument('--check',type=Path)
    args=parser.parse_args()
    result=run()
    if args.write:
        args.write.write_text(json.dumps(result,indent=2)+'\n')
    if args.check:
        need(result==json.loads(args.check.read_text()),'independent scalar summary mismatch')
    print(json.dumps({'status':'passed','identities':result['identity_count'],
                      'positive_certificates':result['positive_certificate_count'],
                      'canonical_sha256':sha256(json.dumps(result,sort_keys=True,separators=(',',':')).encode()).hexdigest()}))
