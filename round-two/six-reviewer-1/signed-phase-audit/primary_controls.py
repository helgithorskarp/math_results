"""Fresh literal Gaussian controls and full balanced endpoint controls."""
from independent import Q, canon, stringify, need, coeffs_gaussian, mul


def reconstruct():
    one = (Q(1),Q(0))
    w = (Q(249999,250001),Q(1000,250001))
    u = (Q(39999,40001),Q(400,40001))
    v = (Q(9999,10001),Q(200,10001))
    for z in (w,u,v):
        need(z[0]**2+z[1]**2==1, 'literal unit modulus')
    cases = [
        ('zero', [one]*8, [Q(1)]*8),
        ('broad-closed-rho', [(Q(17,16),Q(0))]+[one]*7, [Q(17,16)]+[Q(1)]*7),
        ('fine-closed-rho', [(Q(41,40),Q(0))]+[one]*7, [Q(41,40)]+[Q(1)]*7),
        ('coherent', [w]*8, [Q(1)]*8),
        ('balanced-enlarged-only', [v]*4+[(v[0],-v[1])]*4, [Q(1)]*8),
        ('nonconjugate', [u]*5+[(v[0],-v[1])]*2+[one], [Q(1)]*8),
    ]
    out = {}
    for name,z,R in cases:
        need(all(x*x+y*y==r*r for (x,y),r in zip(z,R)), 'all literal radii')
        p,O = coeffs_gaussian(z)
        pr,Or = coeffs_gaussian([(r,Q(0)) for r in R])
        delta = sum(R[j]-z[j][0] for j in range(8))
        Y = sum(y for x,y in z)
        rho2 = sum((r-1)**2 for r in R)
        loss = Or[0]-O[0]
        accepted = []
        for r,d,lam,label in [(Q(1,16),Q(1,1000),Q(1,8),'broad-original'),
                              (Q(1,40),Q(1,1000),Q(7,48),'fine-original'),
                              (Q(1,16),Q(1,200),Q(1,8),'broad-enlarged'),
                              (Q(1,40),Q(1,200),Q(7,48),'fine-enlarged')]:
            if rho2<=r*r and delta<=d:
                need(loss<=-lam*delta+Y*Y/Q(56), 'literal full theorem comparison')
                if delta>0:
                    need(loss<-lam*delta+Y*Y/Q(56), 'positive-phase strict comparison')
                accepted.append(label)
        need(accepted, 'literal control in at least one proved class')
        if name=='coherent':
            need(loss>0 and delta>0, 'negative-only claim refuted')
        if name=='balanced-enlarged-only':
            need(delta>Q(1,1000) and accepted==['broad-enlarged','fine-enlarged'],
                 'genuine class widening control')
        out[name] = {'z':z,'radii':R,'whole_complex_coefficients':p,
                     'whole_radial_coefficients':pr,'origin':O,'radial_origin':Or,
                     'Delta':delta,'Y':Y,'rho_squared':rho2,'loss':loss,'classes':accepted}
    # Algebraic endpoints d=Delta/8 do not require irrational root evaluation.
    for cap in (Q(1,1000),Q(1,200)):
        d=cap/8
        p=[Q(1)]
        for _ in range(4):
            p=mul(p,[Q(1),-2+2*d,Q(1)])
        origin=9*sum((v/Q(j+1) for j,v in enumerate(p)),Q(0))
        formula=1+Q(9,7)*d+Q(72,35)*d*d+Q(24,5)*d**3+Q(144,5)*d**4
        need(origin==formula and 1-origin<-Q(7,48)*cap,'full balanced closed phase endpoint')
        out['balanced-exact-cap-'+str(cap)]={'Delta':cap,'Y':Q(0),'rho_squared':Q(0),
                                            'all_coefficients':p,'origin':origin}
    return out


if __name__=='__main__':
    print(canon(stringify(reconstruct())))
