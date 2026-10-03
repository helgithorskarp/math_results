"""Universal exact decoder/action identities for the original source cover."""
from fractions import Fraction as F
from pathlib import Path
import importlib.util
import forms as j
c=j.c
path=Path(__file__).resolve().parent.parent/'three_cube_cover/poly.py'
# The invoking forms module has already verified this published file's hash.
spec=importlib.util.spec_from_file_location('published_cover_polynomials',path)
p=importlib.util.module_from_spec(spec);spec.loader.exec_module(p)

def record():
    x,y,U,V,w=[p.Poly.variable(i,n=5) for i in range(5)]
    zero=p.Poly(0,n=5);one=p.Poly(1,n=5);L=F(7,4);M=F(15,4)
    u=(x+y*w-M*V)*F(4,7)
    v=(y-x*w+M*U)*F(4,7)
    old=(one,L*v-y+x*w,x+y*w-L*u,w);new=(one,M*U,M*V,w)
    c.require(old==new and L*u==x+y*w-M*V and L*v==y-x*w+M*U,'universal original canonical inverse and all four decoder components')
    Sy=((1,0,0),(0,0,1),(0,-1,0));qw=p.qmul((1,-1,0,0),new)
    c.require(qw==(1+M*U,-1+M*U,M*V+w,w-M*V),'all four true original world source quaternion components')
    Rh=p.rotation_homogeneous(qw)
    c.require(Rh==p.scaled(p.mm(Sy,p.rotation_homogeneous(new)),2),'all nine original world/source rotation entries')
    norm=p.dot(qw,qw)
    c.require(norm==2*(1+M*M*U*U+M*M*V*V+w*w),'positive world quaternion norm and original half-turn coverage')
    c.require(L*L-3==F(1,16) and L+2==M and 2+2*M*M==F(241,8),'exact original global cube/rectangle margins')
    # Homogeneous quaternion properness and the actual D,C actions, with all
    # positive receiver denominators cleared. No finite source sampling.
    x,y,h,vx,vy,vz=[p.Poly.variable(i,n=6) for i in range(6)]
    one=p.Poly(1,n=6);zero=p.Poly(0,n=6);r=(x,y,one);r2=p.dot(r,r);q=(h,vx,vy,vz);N=p.dot(q,q)
    Rh=p.rotation_homogeneous(q);eye=p.identity()
    c.require(p.mm(p.transpose(Rh),Rh)==p.scaled(eye,N*N) and p.det(Rh)==N*N*N,'every quaternion properness polynomial coefficient')
    H=((-1,0,0),(0,-1,0),(0,0,1));Mx=((-1,0,0),(0,1,0),(0,0,1))
    D=p.qmul(q,(0,0,0,1));C=p.qmul(p.qmul((zero,*r),q),(0,1,0,0));CD=p.qmul(p.qmul((zero,*r),D),(0,1,0,0))
    Mraw=tuple(tuple(r2*int(i==k)-2*r[i]*r[k] for k in range(3)) for i in range(3))
    c.require(p.rotation_homogeneous(D)==p.mm(Rh,H),'all nine actual full-body H action entries')
    c.require(p.rotation_homogeneous(C)==p.mm(p.mm(Mraw,Rh),Mx),'all nine actual receiving reflection/body Mx action entries')
    c.require(p.dot(D,D)==N and p.dot(C,C)==r2*N,'actual homogeneous action norms')
    c.require(D[0]==-vz and C[0]==-x*h-y*vz+vy and CD[0]==-y*h+x*vz-vx,'all actual canonical scalar comparisons')
    c.require(p.qmul(p.qmul((zero,*r),C),(0,1,0,0))==tuple(r2*v for v in q),'actual C involution with positive norm factor')
    c.require(p.qmul(D,(0,0,0,1))==tuple(-v for v in q),'actual signed D involution')
    c.require(p.qmul(C,(0,0,0,1))==tuple(-v for v in CD),'closed eight signed quaternion lifts')
    Praw=tuple(tuple(r2*int(i==k)-r[i]*r[k] for k in range(3)) for i in range(3))
    c.require(p.mm(Praw,Mraw)==p.scaled(Praw,r2),'all nine actual projected-set preservation entries')
    return {'agent':'six-rupert-2','role':'researcher','scope':'universal original H/Mx canonical source decoder/actions and degree-preserving Sy realization; no prior full-source exclusion premise','universal_decoder_components':4,'universal_gauge_inverse_identities':2,'world_quaternion_lift_components':4,'world_rotation_matrix_entries':9,'world_norm_identity':1,'quaternion_orthogonality_entries':9,'quaternion_determinant_identity':1,'actual_H_action_entries':9,'actual_receiving_body_reflection_action_entries':9,'actual_action_norms':2,'actual_maximal_scalar_comparisons':3,'actual_C_involution_components':4,'actual_signed_D_involution_components':4,'closed_signed_action_orbit_components':4,'projected_set_preservation_entries':9,'source_M':'15/4','global_prior_L':'7/4','margin_L2_minus3':'1/16','sharp_ungated_relative_norm_squared':'241/8','original_translation_scale_and_absolute_halfturns_retained':True,'body_actions_only':'H,Mx; no A/B or parent-group right quotient'}
