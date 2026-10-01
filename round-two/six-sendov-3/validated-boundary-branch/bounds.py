"""One fixed covered box; all proof inputs and margins are exact rationals."""
from fractions import Fraction as F
from math import comb

from arithmetic import K
import interval as iv
from interval import I,J,C,require
import system as sy

def embedding():
    lo,hi=F(3,4),F(1)
    f=lambda x:8*x*x*x-6*x-1
    require(f(lo)<0<f(hi),'initial embedding bracket')
    for _ in range(160):
        mid=(lo+hi)/2
        if f(mid)<0:
            lo=mid
        else:
            hi=mid
    require(f(lo)<0<f(hi) and 24*lo*lo>6,'unique cubic embedding')
    return I.bounds(lo,hi)


def enclose(k,c):
    return I(k.a[0])+I(k.a[1])*c+I(k.a[2])*c.square()


def matvec(matrix,vector):
    return [sum((a*b for a,b in zip(row,vector)),I(0)) for row in matrix]


def norm(matrix):
    return F(max(sum(v.absmax() for v in row) for row in matrix),iv.DEN)


def certify(values,jac,Yexact,invBexact,damage=None):
    c=embedding()
    Y=[[enclose(v,c) for v in row] for row in Yexact]
    eta_max=F(1,65536);radius=F(1,1024);root_radius=F(1,16384)
    center=[enclose(v,c) for v in values]
    box=[v+I.bounds(-radius,radius) for v in center]
    eta=J.eta(I.bounds(0,eta_max))
    variables=[J.parameter(v,i) for i,v in enumerate(box)]
    equations,aux=sy.system(eta,variables,c)
    Dbar=[list(f.g[1]) for f in equations]
    contraction=[]
    for i in range(6):
        contraction.append([I(int(i==j))-sum((Y[i][k]*Dbar[k][j] for k in range(6)),I(0)) for j in range(6)])
    q=norm(contraction)
    central,_=sy.system(eta,[J(v) for v in center],c)
    residual=matvec(Y,[f.f[2] for f in central])
    b=eta_max*F(max(v.absmax() for v in residual),iv.DEN)
    record={'complete':False,
        'precision_bits':iv.BITS,'eta_interval':['0',str(eta_max)],
        'parameter_radius':str(radius),'root_disk_radius':str(root_radius),
        'c_interval':c.record(),'center':[v.record() for v in center],
        'parameter_box':[v.record() for v in box],
        'preconditioner':[[v.record() for v in row] for row in Y],
        'mixed_eta_parameter_enclosure':[[v.record() for v in row] for row in Dbar],
        'contraction_matrix':[[v.record() for v in row] for row in contraction],
        'contraction_q':str(q),'center_residual_b':str(b),
        'radii_margin':str(radius-b-q*radius)}
    require(q<1 and b+q*radius<radius,'uniform fixed-point radii inequality')

    # Uniform local phase, normal, opening and denominator margins.
    A,D,W=[aux[n].f[0] for n in ('A','D','W')]
    opening=box[2]
    phase_values=[v.f[0] for v in aux['phases']]
    phase_derivatives=[v.f[0] for v in aux['phase_derivatives']]
    normals=[[v.f[0] for v in row] for row in aux['normals']]
    normal_minor=normals[0][1]*normals[1][2]-normals[0][2]*normals[1][1]
    require(A.lo>0 and D.lo>0 and W.lo>0 and opening.lo>0,'positive physical distances and opening')
    require(all(-iv.DEN<t.lo<=t.hi<iv.DEN for t in phase_values),'unit phases remain inside(-1,1)')
    require(all(v.hi<0 for v in phase_derivatives),'nonzero negative phase Jacobians')
    require(normal_minor.lo>0,'positive active normal minor')

    # The scalar Schur complement of the actual divided equations is
    # bounded through an independently preconditioned five-variable block.
    invB=[[enclose(v,c) for v in row] for row in invBexact]
    Binterval=[row[1:] for row in Dbar[:5]]
    defect=[[I(int(i==j))-sum((invB[i][k]*Binterval[k][j] for k in range(5)),I(0)) for j in range(5)] for i in range(5)]
    beta=norm(defect)
    require(beta<1,'five-constraint block uniformly regular')
    tail=[I(-3),I(0),I(0),I(0),I(3)]
    tail_residual=[row[0]+sum((a*b for a,b in zip(row[1:],tail)),I(0)) for row in Dbar[:5]]
    pre_tail=matvec(invB,tail_residual)
    tail_error=F(max(v.absmax() for v in pre_tail),iv.DEN)/(1-beta)
    raw_schur=Dbar[5][0]+sum((a*b for a,b in zip(Dbar[5][1:],tail)),I(0))
    loss=tail_error*F(sum(v.absmax() for v in Dbar[5][1:]),iv.DEN)
    schur_lower=F(raw_schur.lo,iv.DEN)-loss
    curvature_factor=normal_minor*A.square()*W**3
    require(schur_lower>0 and curvature_factor.lo>0,'positive scalar constrained curvature')
    curvature_lower=schur_lower/F(curvature_factor.hi,iv.DEN)

    # Rouché disks, each with exactly one simple original root.
    require((c.square()).hi<I(F(8,9)).lo,'minimum ninth-root separation exceeds2/3')
    p=[v.f[0] for v in aux['poly']];peta=[v.f[1] for v in aux['poly']]
    perturbation=eta_max*sum((F(v.absmax(),iv.DEN)*(1+root_radius)**j for j,v in enumerate(peta)),F(0))
    require(2*root_radius<F(2,3),'nine Rouche disks are disjoint')
    rouche_lower=(0 if damage=='rouche' else 9)*root_radius-sum((comb(9,j)*root_radius**j for j in range(2,10)),F(0))
    rouche_margin=rouche_lower-perturbation
    require(rouche_margin>0,'uniform nine-disjoint-disk Rouche bound')
    require(eta_max<root_radius,'marked root remains in the ninth-root disk about1')
    require(all(t.square().hi<I(F(15,16)).lo for t in phase_values),
            'unit-root abscissa-to-root derivative is uniformly at most4')
    require(4*eta_max*max(F(box[3].absmax(),iv.DEN),F(box[4].absmax(),iv.DEN))<root_radius,
            'active unit roots remain in their identified ninth-root disks')
    d=2*c.square()-1
    inactive=[]
    derivative=[(j+1)*p[j+1] for j in range(9)]
    for index,cosine in ((1,d),(2,2*d.square()-1)):
        sine=(1-cosine.square()).sqrt()
        z=C(cosine+I.bounds(-root_radius,root_radius),sine+I.bounds(-root_radius,root_radius))
        numerator=iv.evaluate(peta,z);denominator=iv.evaluate(derivative,z)
        motion=(-numerator/denominator)*z.conj()
        if damage=='inward-sign':
            motion=-motion
        require(motion.re.hi<0,'strict original-root inward motion k'+str(index))
        inactive.append({'index':index,'half_radial_eta_derivative':motion.re.record(),
                         'root_derivative_denominator_norm2':(denominator.re.square()+denominator.im.square()).record()})

    objective_slope=6*(1+box[0])/A-2*box[5]/W
    require(objective_slope.lo>I(2).hi and objective_slope.hi<I(3).lo,
            'explicit branch first-power window8+2eta<F<8+3eta')
    lipschitz=b/(eta_max*(1-q))
    require(q<F(3,5) and b<F(1,5000),'clean contraction and residual bounds')
    require(lipschitz<25 and curvature_lower>22,'clean displacement and curvature bounds')
    record.update(complete=True,branch_displacement_coefficient=str(lipschitz),
        phase_values=[v.record() for v in phase_values],phase_derivatives=[v.record() for v in phase_derivatives],
        normal_minor=normal_minor.record(),physical_distances=[v.record() for v in (A,D,W)],opening=opening.record(),
        five_block_beta=str(beta),constraint_tangent_error=str(tail_error),scalar_schur_lower=str(schur_lower),
        symmetric_curvature_lower=str(curvature_lower),rouche_lower=str(rouche_lower),rouche_perturbation=str(perturbation),rouche_margin=str(rouche_margin),
        inactive_original_root_motion=inactive,objective_slope=objective_slope.record())
    return record
