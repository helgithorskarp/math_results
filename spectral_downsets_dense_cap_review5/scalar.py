"""Independent dense-complement audit with a sharper rational cap.

Dense nested polynomial rows, separate from the author's sparse backend.
The three affine domains exactly cover the integer-q hypotheses.
"""
from fractions import Fraction as F
from hashlib import sha256
import json
from exact import need
from symbols import Rat,coefficients
from formulas import formulas

def record(z):
    need(z.n[0][0]>0 and z.d[0][0]>0,'strict constant')
    need(all(c>=0 for p in (z.n,z.d) for row in p for c in row),'strict coefficient')
    vals=[coefficients(z.n),coefficients(z.d)]
    return {'numerator_terms':len(vals[0]),'denominator_terms':len(vals[1]),
      'numerator_constant':str(z.n[0][0]),'denominator_constant':str(z.d[0][0]),
      'coefficient_sha256':sha256(json.dumps(vals,separators=(',',':')).encode()).hexdigest()}

def domain(name):
    v=Rat(((12,),(1,)))
    if name=='q0':q=Rat(0)
    elif name=='q1':q=Rat(1)
    elif name=='q2plus':q=Rat(((2,1),));v=Rat(((12,4),(1,)))
    else:raise ValueError('unknown domain')
    return v,q

def run():
    out={};tables={};identity_names=None
    for label in ('q0','q1','q2plus'):
        v,q=domain(label);l=v-q-2;f=formulas(v,l)
        m,b,r,s,N,c,d,t,w,h,D=(f[x] for x in ('m','b','r','s','N','c','d','t','w','h','D'))
        k=(v-2)*(v-3)/2;u=l*(l-1)/2;rq=q*(v-1)/2;uq=q*(q-1)/2
        B=s+v*v/2+(q*q+2*q+F(3,2))*v-10;delta=N-B
        G=132*v-12*v*v*(q*q+2*q+2)+2*v*(v-q-2)*(v-1)*(v-3)-3*(v-1)*(v-2)*(v-3)
        row1=s+(q*q+F(3,2)*q+F(13,6))*v
        row2=s+F(4,3)+v/3+q*v/2+v*(v-4)/2
        row3=s+v*v/2+(2*q+F(3,2))*v-10
        Bnew=s+v*v/4+(q*q+2*q+4)*v-16;newdelta=N-Bnew
        new23=(v-4)*(v+6)/4
        newrow2=s+F(4,3)+v/3+q*v/2+new23
        newrow3=s+2*(v-5)+(F(3,2)+2*q)*v+new23
        constant=l*(v+7)/6+1;loss=m*k/(2*v*v)
        ids={'delta_polynomial':delta-(66-6*v*(q*q+2*q+2)+(v-q-2)*(v-1)*(v-3))/6,
         'repair_margin':delta/2-loss-G/(24*v),
         'row1_difference':B-row1-(v*v/2+(q/2-F(2,3))*v-10),
         'row2_difference':B-row2-(q*q*v+(F(3,2)*q+F(19,6))*v-F(34,3)),
         'row3_difference':B-row3-q*q*v,
         'constant_difference':s-constant-(v-1+l*(v-5)/3),
         'complement_variance':(r-u)-(rq-uq)-(l-q),
         'completion_Z_bound':q*rq-(rq-uq)-uq*v,
         'old_root_margin':(v-2)**2-8*(v-3)-(v*(v-12)+28),
         'new_cap_improvement':B-Bnew-(v-4)*(v-6)/4,
         'new_row1_margin':Bnew-row1-(v*v/4+(q/2+F(11,6))*v-16),
         'new_row2_margin':Bnew-newrow2-((q*q+F(3,2)*q+F(19,6))*v-F(34,3)),
         'new_row3_margin':Bnew-newrow3-q*q*v,
         'new_root_margin':(v+6)**2/16-(2*v-6)-((v-10)**2+32)/16,
         'row3_dominates_row2':newrow3-newrow2-((F(3,2)*q+F(19,6))*v-F(34,3))}
        for name,z in ids.items():need(z.equals(0),'identity:'+label+':'+name)
        expressions={'D_positive':D,'c_positive':c,'c_lt_4_over_3':Rat(F(4,3))-c,
         'd_positive':d,'d_lt_2':2-d,'t_gt_1':t-1,'t_lt_2':2-t,
         'd_minus_w_gt_minus1':1+d-w,'d_minus_w_lt1':1-d+w,
         'three_t_minus_h_gt_minus2':2+3*t-h,'three_t_minus_h_lt2':2-3*t+h,
         'gap_positive':delta,'repair_gap_gt_half_delta':G/(24*v),
         'constant_cap':B-constant,'row1_comparison':B-row1,'row2_comparison':B-row2,
         'old_root_comparison':(v-2)**2-8*(v-3),
         'new_cap_improvement':B-Bnew,'new_gap_positive':newdelta,
         'new_repair_gap_gt_half_delta':newdelta/2-loss,
         'new_constant_cap':Bnew-constant,'new_row1_comparison':Bnew-row1,
         'new_row2_comparison':Bnew-newrow2,'new_root_comparison':(v+6)**2/16-(2*v-6),
         'row3_dominates_row2':newrow3-newrow2,'row1_above_constant':row1-constant}
        out[label]={name:record(z) for name,z in expressions.items()}
        tables[label]=coefficients(G.n);identity_names=list(ids)
    need(len(tables['q2plus'])==15 and tables['q2plus'][0]==[0,0,'342'],'original repaired polynomial table')
    return {'agent':'six-reviewer-5','role':'independent mathematical reviewer','identity_names':identity_names,
      'identity_count':len(identity_names),'identity_domain_checks':3*len(identity_names),
      'strict_certificates':out,'strict_certificate_count':sum(len(z) for z in out.values()),
      'original_repaired_H_shifted_coefficients':tables,
      'quadrants':{'q0':'q=0,v=12+x','q1':'q=1,v=12+x','q2plus':'q=2+y,v=12+4y+x; x,y>=0'},
      'improved_cap':'s+v^2/4+(q^2+2q+4)v-16','improvement':'(v-4)(v-6)/4',
      'row_maximum_cap':'s+max((q^2+3q/2+13/6)v, v^2/4+(2q+4)v-16)'}
