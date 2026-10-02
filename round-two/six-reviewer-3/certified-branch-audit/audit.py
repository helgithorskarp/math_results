#!/usr/bin/env python3
"""Independent full-box audit of the certified original-root continuation."""
import argparse
from fractions import Fraction as F
from hashlib import sha256
from itertools import permutations
import json
from math import comb
from pathlib import Path
import sys
sys.path.insert(0,str(Path(__file__).resolve().parent))
from exact_numbers import K,I,D,Z,need,up,down,embedding,enclose,evaluate,derivative,equations
from controls import run as controls

BASE=Path(__file__).resolve().parent


def canonical(x):return json.dumps(x,sort_keys=True,separators=(',',':')).encode()


def inverse(matrix):
    n=len(matrix);rows=[list(r)+[K(int(i==j)) for j in range(n)] for i,r in enumerate(matrix)]
    for j in range(n):
        k=next((i for i in range(j,n) if rows[i][j]!=0),None);need(k is not None,'exact preconditioner pivot');rows[j],rows[k]=rows[k],rows[j];p=rows[j][j];rows[j]=[x/p for x in rows[j]]
        for i in range(n):
            if i!=j:
                factor=rows[i][j];rows[i]=[x-factor*y for x,y in zip(rows[i],rows[j])]
    out=[r[n:] for r in rows]
    for a,b in ((matrix,out),(out,matrix)):
        need(all(sum((a[i][k]*b[k][j] for k in range(n)),K(0))==int(i==j) for i in range(n) for j in range(n)),'both exact inverse products')
    return out


def constants():
    c=K((0,1,0));d=2*c*c-1;q=1/(3*(1+c));H=14*q;U=-8*(F(2,3)-q);h=(c-5)/3;x=(U+h*H)/8;y=x-h*H/2
    return c,d,[x,y,H/2,K((-F(1,6),-F(4,3),F(4,3))),(c-1)/3,H/4-1-y]


def exact_initial():
    c,d,v=constants();G,aux=equations(D.variable(K(0),0),[D.variable(x,i+1) for i,x in enumerate(v)],c)
    need(all(g.v==0 and g.g.get(0,0)==0 for g in G),'G and divided G vanish at true initial point')
    J=[[K(g.h.get((0,i+1),0)) for i in range(6)] for g in G];Y=inverse(J);B=[r[1:] for r in J[:5]];B_inv=inverse(B);tail=[-sum((B_inv[i][j]*J[j][0] for j in range(5)),K(0)) for i in range(5)]
    need(tail==list(map(K,(-3,0,0,0,3))),'literal full constrained initial tangent')
    determinant=K(0);terms=0
    for perm in permutations(range(6)):
        term=K(1)
        for i,j in enumerate(perm):term*=J[i][j]
        if term!=0:terms+=1
        parity=sum(perm[i]>perm[j] for i in range(6) for j in range(i+1,6))%2;determinant+=(-term if parity else term)
    need(determinant==-F(8264970432,49)*(1+F(13,2)*c+7*c*c),'definition-level exact full determinant')
    schur=J[5][0]+sum((a*b for a,b in zip(J[5][1:],tail)),K(0));factor=81*(3*(c+d)/56)*108/(1-c*c)
    need(schur==24*factor==F(629856,7)*(c+c*c),'exact initial constrained scalar curvature24')
    record={'variables':['x','y','T','xi3','xi4','omega'],'values':[x.record() for x in v],'jacobian':[[x.record() for x in r] for r in J],'inverse':[[x.record() for x in r] for r in Y],'five_block_inverse':[[x.record() for x in r] for r in B_inv],'determinant':determinant.record(),'nonzero_permutation_terms':terms,'constraint_tangent_tail':[x.record() for x in tail],'scalar_schur':schur.record(),'initial_curvature_factor':factor.record()}
    return v,Y,B_inv,record


def norm(m):return max(sum(x.absmax() for x in r) for r in m)


def matvec(m,v):return [sum((x*y for x,y in zip(r,v)),I(0)) for r in m]


def certify(values,Yfield,Bfield,radius):
    c=embedding();center=[enclose(x,c) for x in values];box=[x+I(-radius,radius) for x in center];epsilon=F(1,65536);delta=F(1,16384);Y=[[enclose(x,c) for x in r] for r in Yfield];Bi=[[enclose(x,c) for x in r] for r in Bfield]
    G,aux=equations(D.variable(I(0,epsilon),0),[D.variable(x,i+1) for i,x in enumerate(box)],c)
    Hv=[[I(g.h.get((0,i+1),0)) for i in range(6)] for g in G]
    defect=[[I(int(i==j))-sum((Y[i][k]*Hv[k][j] for k in range(6)),I(0)) for j in range(6)] for i in range(6)];q=up(norm(defect))
    central,_=equations(D.variable(I(0,epsilon),0),[D(x) for x in center],c);forcing=matvec(Y,[I(g.h.get((0,0),0))/2 for g in central]);R=up(max(x.absmax() for x in forcing));b=up(epsilon*R);margin=down(radius-b-q*radius)
    need(q<1 and margin>0,'independent full closed-cube contraction');lipschitz=up(R/(1-q));need(lipschitz<25,'independent pointwise displacement bound')
    A,dist,W=[I(aux[name].v) for name in ('A','D','W')];opening=box[2];phases=[I(x.v) for x in aux['phases']];its=[I(x.v) for x in aux['Its']];N=[[I(x.v) for x in r] for r in aux['normals']];minor=N[0][1]*N[1][2]-N[0][2]*N[1][1]
    need(all(x.lo>0 for x in (A,dist,W,opening,minor)),'positive physical branch denominators and active minor');need(all(-1<x.lo<=x.hi<1 and x.square().hi<F(15,16) for x in phases),'four active unit-root phases');need(all(x.hi<0 for x in its),'nonzero original phase Jacobians')
    B=[r[1:] for r in Hv[:5]];five_defect=[[I(int(i==j))-sum((Bi[i][k]*B[k][j] for k in range(5)),I(0)) for j in range(5)] for i in range(5)];beta=up(norm(five_defect));need(beta<1,'independent five-constraint block regularity');t0=(-3,0,0,0,3);residual=[r[0]+sum((x*y for x,y in zip(r[1:],t0)),I(0)) for r in Hv[:5]];pre=matvec(Bi,residual);tail_error=up(max(x.absmax() for x in pre)/(1-beta));raw=Hv[5][0]+sum((x*y for x,y in zip(Hv[5][1:],t0)),I(0));schur=down(raw.lo-tail_error*sum(x.absmax() for x in Hv[5][1:]));factor=minor*A.square()*W**3;curvature=down(schur/factor.hi);need(factor.lo>0 and curvature>22,'independent actual constrained scalar curvature')
    poly=[I(x.v) for x in aux['poly']];peta=[I(x.g.get(0,0)) for x in aux['poly']];rouche_lower=9*delta-sum(comb(9,j)*delta**j for j in range(2,10));perturb=epsilon*sum(x.absmax()*(1+delta)**j for j,x in enumerate(peta));rouche_margin=down(rouche_lower-perturb);need(rouche_margin>0 and epsilon<delta and c.square().hi<F(8,9),'nine original Rouche disks including the marked root');need(4*epsilon*max(box[3].absmax(),box[4].absmax())<delta,'active roots in their distinct original disks')
    d=2*c.square()-1;motions=[]
    for k,cosine in ((1,d),(2,2*d.square()-1)):
        sine=(1-cosine.square()).sqrt();z=Z(cosine+I(-delta,delta),sine+I(-delta,delta));num=evaluate([Z(x) for x in peta],z);den=evaluate([Z(x) for x in derivative(poly)],z);radial=(-num/den*z.conjugate()).re;need(radial.hi<0,'all fixed-parameter original-root inward derivatives k'+str(k));motions.append({'reference_index':k,'half_squared_modulus_eta_derivative':radial.record(),'positive_squared_modulus_loss_rate':str(down(-2*radial.hi)),'original_root_derivative_norm2':(den.re.square()+den.im.square()).record()})
    slope=6*(1+box[0])/A-2*box[5]/W;need(slope.lo>2 and slope.hi<3,'independent full effective branch first-power bounds')
    return {'parameter_radius':str(radius),'c_interval':c.record(),'center':[x.record() for x in center],'whole_box':[x.record() for x in box],'mixed_eta_parameter_enclosures':[[x.record() for x in r] for r in Hv],'contraction_matrix':[[x.record() for x in r] for r in defect],'q_upper':str(q),'R_upper':str(R),'b_upper':str(b),'positive_radii_margin_lower':str(margin),'displacement_coefficient_upper':str(lipschitz),'physical_distances':[x.record() for x in (A,dist,W)],'opening':opening.record(),'active_phases':[x.record() for x in phases],'phase_derivatives':[x.record() for x in its],'normal_minor':minor.record(),'five_block_beta_upper':str(beta),'constraint_tangent_error_upper':str(tail_error),'scalar_schur_lower':str(schur),'symmetric_curvature_lower':str(curvature),'rouche_lower':str(rouche_lower),'rouche_perturbation_upper':str(up(perturb)),'rouche_margin_lower':str(rouche_margin),'inactive_original_root_motion':motions,'objective_slope':slope.record()}


def main():
    parser=argparse.ArgumentParser();parser.add_argument('--emit-fixture',type=Path);parser.add_argument('--fixture',type=Path,default=BASE/'EXPECTED.json');parser.add_argument('--author-fixture',type=Path);args=parser.parse_args()
    control_record=controls();values,Y,Bi,initial=exact_initial();full=certify(values,Y,Bi,F(1,1024));need(F(full['displacement_coefficient_upper'])<19,'full certificate enters19eta tube');need(F(full['q_upper'])<F(3,8),'stronger full contraction');tight=certify(values,Y,Bi,F(19,65536))
    need(F(tight['symmetric_curvature_lower'])>F(45,2),'stronger constrained scalar curvature')
    slope=tight['objective_slope'];need(F(slope[0])>F(181,64) and F(slope[1])<F(91,32),'stronger actual first-power branch interval')
    motions=tight['inactive_original_root_motion'];need(F(motions[0]['positive_squared_modulus_loss_rate'])>F(7,5) and F(motions[1]['positive_squared_modulus_loss_rate'])>F(1,2),'quantitative original-root disk slack')
    epsilon=F(1,65536);kappa=(2-epsilon)*(F(3,8)-epsilon)
    strengthened={'full_contraction_strict_upper':'3/8','pointwise_displacement_strict_coefficient':'19','scalar_x_curvature_strict_coefficient':'45/2','objective_eta_slope_strict_interval':['181/64','91/32'],'inactive_squared_modulus_loss_strict_rates':['7/5','1/2'],'collapsed_kappa_uniform_lower':str(kappa),'collapsed_uniform_original_root_radius':str(kappa/5000),'collapsed_energy_uniform_coefficient':str(kappa/2),'collapsed_M_gap_eta_strict_coefficient':'37/32'}
    out={'actual_agent':'six-reviewer-3','role':'independent mathematical reviewer','method':'full seven-variable Hessian tensors, polynomial convolutions and coefficient Chebyshev evaluation, exact Fraction interval endpoints; fixed112 cubic bisections,128 square-root/record grids; no runtime source calculation inputs','eta_max':'1/65536','controls':control_record,'exact_initial':initial,'full_cube_certificate':full,'certified19eta_tube':tight,'strengthened_consequences':strengthened}
    if args.author_fixture:
        author=json.loads(args.author_fixture.read_text());need(canonical(initial)==canonical(author['exact_initial']),'entire original initial field/Jacobian/inverse/determinant/tangent record')
    if args.emit_fixture:args.emit_fixture.write_text(json.dumps(out,indent=2)+'\n')
    else:need(canonical(out)==canonical(json.loads(args.fixture.read_text())),'complete independent frozen record')
    print('PASS independent original-root certificate; full-record SHA256',sha256(canonical(out)).hexdigest())
    print(json.dumps({k:tight[k] for k in ('q_upper','displacement_coefficient_upper','symmetric_curvature_lower','objective_slope','inactive_original_root_motion')},indent=2))


if __name__=='__main__':main()
