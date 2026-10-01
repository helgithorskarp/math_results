"""Independent exact wider-domain row-gap and operator certificates.

Variables are affine dense polynomial arrays before any expression is formed.
The author's sparse arithmetic, substitutions and CAS are not imported.
"""
from fractions import Fraction as F
from exact import need
from symbols import Rat, coefficients
from formulas import formulas

DOMAINS={'q0':(12,0,0,0),'q1':(12,0,1,0),'q2':(12,0,2,0),
         'q4':(15,0,4,0),'odd3plus':(13,5,3,2),'even6plus':(20,5,6,2)}

def variables(config):
    v0,vy,q0,qy=config
    return Rat(((v0,vy),(1,))),Rat(((q0,qy),))

def expressions(v,q):
    l=v-q-2;f=formulas(v,l)
    m,r,s,N,c,d,t,w,h,D=(f[x] for x in ('m','r','s','N','c','d','t','w','h','D'))
    k=(v-2)*(v-3)/2;uq=q*(q-1)/2;rq=q*(v-1)/2;ul=l*(l-1)/2
    a12=v/3+q*v/2;a13=(F(3,2)+2*q)*v
    row1=s+l/3+t*uq*v+a12+a13
    row2=s+F(4,3)+a12+v*(v-4)/2
    row3=s+v*v/2+(2*q+F(3,2))*v-10
    A=12*v+6*v*v*(v-1)+2*v*l*(v-1)*(v-3)
    product=(v-1)*(v-2)*(v-3)
    G1=D*(A-4*v*l-(22+30*q)*v*v-3*product)-6*q*(q-1)*v*v*(v-1)*(l*(v-3)-6)
    G2=A-16*v-(4+6*q)*v*v-6*v*v*(v-4)-3*product
    G3=A-6*v*v*v-(24*q+18)*v*v+120*v-3*product
    rows=[row1,row2,row3];Gs=[G1,G2,G3]
    new23=(v-4)*(v+6)/4
    newrow2=s+F(4,3)+a12+new23
    newrow3=s+2*(v-5)+a13+new23
    ids={**{'row'+str(i)+'_repair_margin':N-row-m*k/(v*v)-G/(12*v*(D if i==1 else 1))
                 for i,(row,G) in enumerate(zip(rows,Gs),1)},
         'constant_below_s':s-(l*(v+7)/6+1)-(v-1+l*(v-5)/3),
         'complement_variance':(r-ul)-(rq-uq)-(l-q),
         'completion_Z_bound':q*rq-(rq-uq)-uq*v,
         'old_root_difference':(v-2)**2-8*(v-3)-(v*(v-12)+28),
         'new_root_difference':(v+6)**2/16-(2*v-6)-((v-10)**2+32)/16,
         'cross_entry_decrease':v*(v-4)/2-new23-(v-4)*(v-6)/4,
         'row3_dominates_row2':newrow3-newrow2-((F(3,2)*q+F(19,6))*v-F(34,3))}
    signs={'D_positive':D,'c_positive':c,'c_lt_4_over_3':Rat(F(4,3))-c,
        'd_positive':d,'d_lt_2':2-d,'t_gt_1':t-1,'t_lt_2':2-t,
        'd_minus_w_gt_minus1':1+d-w,'d_minus_w_lt1':1-d+w,
        'three_t_minus_h_gt_minus2':2+3*t-h,'three_t_minus_h_lt2':2-3*t+h,
        'old_root_comparison':(v-2)**2-8*(v-3),
        'constant_below_s':s-(l*(v+7)/6+1),
        **{'row'+str(i)+'_gap_above_twice_loss':N-row-m*k/(v*v) for i,row in enumerate(rows,1)},
        'new_root_comparison':(v+6)**2/16-(2*v-6),
        'cross_entry_decrease':v*(v-4)/2-new23,
        'row3_dominates_row2':newrow3-newrow2,
        'lambda_positive':l,'new23_positive':new23,'a12_positive':a12,'a13_positive':a13}
    return ids,signs,Gs

def run():
    records={};tables={};names=None
    for name,config in DOMAINS.items():
        v,q=variables(config);ids,signs,Gs=expressions(v,q)
        for label,z in ids.items():need(z.equals(0),'identity:'+name+':'+label)
        records[name]={label:z.strict_record(name+':'+label) for label,z in signs.items()}
        tables[name]={}
        for i,G in enumerate(Gs,1):
            need(G.d==((F(1),),),'nonpolynomial gap numerator')
            terms=coefficients(G.n)
            need(G.n[0][0]>0 and all(F(z)>0 for _,_,z in terms),'negative gap-polynomial coefficient')
            tables[name]['G'+str(i)]=terms
        names=list(ids)
    # The tempting single even-q quadrant is inconclusive, not a counterexample.
    _,_,Gs=expressions(*variables((15,5,4,2)))
    negative=[z for z in coefficients(Gs[0].n) if F(z[2])<0]
    need(bool(negative),'missing q4 continuous-quadrant diagnostic')
    return {'agent':'six-reviewer-5','role':'independent mathematical reviewer',
      'arithmetic':'Dense nested Fraction Q(x,y), no author/CAS/GCD/interpolation',
      'affine_domains':{n:{'v0':a,'vy':b,'q0':c,'qy':d} for n,(a,b,c,d) in DOMAINS.items()},
      'identity_names':names,'identities_per_domain':len(names),'identity_domain_checks':6*len(names),
      'strict_certificate_count':sum(len(a) for a in records.values()),'strict_certificates':records,
      'repair_margin_shifted_polynomials':tables,
      'inconclusive_unsplit_even_q4_G1_negative_terms':negative,
      'parameter_coverage':'Written exact integer q partition; not a design-existence test',
      'margin_normalization':'N-max(rows)-mk/v^2 is twice the actual half-gap repair margin'}
