"""Exact adverse/positive controls for physical dual and support bridges.
No author executable/input. These finite controls supplement REVIEW.md's continuum proof.
"""
import itertools,json
from fractions import Fraction as F
from pathlib import Path
from check import load,decode,need,absolute,encode
HERE=Path(__file__).resolve().parent

def verify():
    b=load();d=json.loads((HERE/'expected.json').read_text());V=[tuple(decode(b,t) for t in v) for v in d['originals']];rows=[tuple(decode(b,t) for t in v) for v in d['sorted_torque_rows']];rejected=[]
    def reject(name,f):
        try:f()
        except ValueError:rejected.append(name);return
        raise ValueError('damaged mathematical input accepted:'+name)
    def dual(ids,weights,j,sgn):
        need(len(ids)==len(weights),'dual inventory');need(min(weights)>=0,'nonnegative cone weights');actual=tuple(sum((w*rows[i][k] for w,i in zip(weights,ids)),b.Z) for k in range(3));need(actual==tuple(b.S(sgn if k==j else 0) for k in range(3)),'physical dual coordinate identity');need(sum(weights,b.Z)<28,'dual coordinate bound')
    for n,z in enumerate(d['dual_coordinate_certificates']):
        ids=z['row_indices'];w=[decode(b,t) for t in z['weights']];dual(ids,w,z['coordinate'],z['sign'])
        reject('dual_weight_'+str(n),lambda ids=ids,w=w,z=z:dual(ids,[w[0]+b.q(1,1000),*w[1:]],z['coordinate'],z['sign']))
    z=d['dual_coordinate_certificates'][0];ids=z['row_indices'];w=[decode(b,t) for t in z['weights']]
    reject('omitted_dual_row',lambda:dual(ids[:-1],w,z['coordinate'],z['sign']))
    reject('negative_dual_coefficient',lambda:dual(ids,[-absolute(w[0])-1,*w[1:]],z['coordinate'],z['sign']))
    reject('wrong_coordinate_sign',lambda:dual(ids,w,z['coordinate'],-z['sign']))
    reject('overstated_local_radius',lambda:need(F(1,28)-F(1,500)-3*F(17,16)*F(1,90)>0,'nonlinear margin lost'))
    reject('overstated_receiver_x_max',lambda:need(b.q(101,2500)<b.q(1,25),'raw target corner not covered'))
    reject('unproved_bootstrap_factor',lambda:need(F(6068,5325)<F(11,10),'row bootstrap does not reach11/10'))
    ident=0;positive=0;shifted=0;cyc=d['cycle_original_indices']
    for cr in d['corner_raw']:
        r=tuple(decode(b,t) for t in cr);contact=[]
        for i,j in zip(cyc,cyc[1:]+cyc[:1]):
            m=b.fcross(b.sub(V[j],V[i]),r);h=b.fdot(m,V[i]);m=b.scale(1/h,m)
            for k in (i,j):contact.append((V[k],m,b.fcross(V[k],m)))
        for signs in itertools.product((-1,0,1),repeat=3):
            qq=tuple(b.q(s,117) for s in signs);u2=b.fdot(qq,qq);U=max(absolute(t) for t in qq);violations=[]
            for v,m,f in contact:
                rv=b.add(v,b.scale(2/(1+u2),b.add(b.fcross(qq,v),b.fcross(qq,b.fcross(qq,v)))));gap=b.fdot(m,rv)-1;poly=b.fdot(f,qq)+b.fdot(m,qq)*b.fdot(v,qq)-u2
                need(gap==2*poly/(1+u2),'literal actual Cayley identity');ident+=1;violations.append((gap,m,rv))
            if U==0:need(all(gap==0 for gap,m,rv in violations),'known congruent fit');continue
            gap,m,rv=max(violations,key=lambda z:z[0]);need(gap>U*b.q(1,80) and gap*gap>U*U*b.fdot(m,m)/400,'actual physical support violation');positive+=1
            for lam,tx in itertools.product((b.S(1),b.q(11,10)),(-1,0,1)):
                T=(b.q(tx,17),b.Z,-r[0]*b.q(tx,17));need(b.fdot(T,r)==0,'physical receiving-plane translation');res=lam*b.fdot(m,rv)-1+absolute(b.fdot(m,T));need(res>=gap and res*res>U*U*b.fdot(m,m)/400,'antipodal support with actual scale/translation');shifted+=1
    return {'actual_agent':'six-reviewer-4','role':'independent mathematical reviewer','all_six_exact_coordinate_duals_accept':True,'semantic_damaged_controls_rejected':rejected,'all_boundary_corner_motion_control_vectors':108,'literal_cayley_polynomial_identities':ident,'nonzero_boundary_corner_support_margin_controls':positive,'actual_scale_translation_antipodal_controls':shifted,'zero_motion_known_congruent_corner_controls':4,'finite_controls_not_a_continuum_sampling_proof':True}

if __name__=='__main__':print(json.dumps(verify(),indent=2,sort_keys=True))
