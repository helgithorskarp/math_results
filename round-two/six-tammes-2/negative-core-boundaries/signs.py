"""Exact dyadic witnesses fixing the signs between the isolated loci."""
from dependency import load
def verify():
    e=load();critical=[];lower=[]
    witnesses=(('critical',e.Q(29,50),1),('critical',e.Q(593,1000),-1),
               ('lower',e.Q(14,25),1),('lower',e.Q(29,50),-1))
    for family,t,desired in witnesses:
        rows=e.factor_bernstein(-1,0,t,t)
        a,b=e.root_bracket(rows,e.Q(29,5),e.Q(39,5))
        P,H=e.build(e.I(t),e.I(a,b),-1)
        if family=='critical':
            r=2*e.I(t)/(1+e.I(t))
            B3=[r*(x+y)-z for x,y,z in zip(P[1],P[4],P[2])]
            gap=e.dot(P[7],B3,H)-e.I(t)
            result=critical
        else:
            gap=e.dot(P[5],P[12],H)-e.I(t);result=lower
        e.require(gap.sign()==desired,'exact scalar sign witness: '+family)
        result.append({'t':str(t),'q_bracket':[str(a),str(b)],
                       'gap_enclosure':[str(x) for x in gap.fractions()], 'sign':desired})
    return {'rounding':'outward integer dyadics','precision_bits':80,
            'critical':critical,'lower':lower}
