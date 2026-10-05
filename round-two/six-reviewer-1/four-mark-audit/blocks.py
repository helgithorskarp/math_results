"""Fresh whole prototype frames and exact all-count rational bounds.

No author executable is imported. Full polynomial identities in(a,c,t)
are read by direct Fraction coefficient comparison, not point sampling.
"""
from fractions import Fraction as Q
from polynomials import plus,times,scale,p

def outer(rows,size):
    matrix=[[{}for _ in range(size)]for _ in range(size)]
    for count,row in rows:
        for i in range(size):
            for j in range(size):matrix[i][j]=plus(matrix[i][j],scale(times(row[i],row[j]),count))
    return matrix

def evaluate(poly,a,c,t):
    return sum(value*a**e[0]*c**e[1]*t**e[2]for e,value in poly.items())

def templates(defect=None):
    a={(1,0,0):Q(1)};c={(0,1,0):Q(1)};t={(0,0,1):Q(1)}
    half=p(Q(1,2));minus_half=p(Q(-1,2));zero={}
    leaf=outer([(1,[half,zero]),(1,[minus_half,zero]),
                (1,[scale(c,Q(-1,2)),half]),(1,[scale(c,Q(1,2)),minus_half])],2)
    standard=outer([(3 if defect=='prototype-count' else 4,[half,p(Q(1,12)),zero,zero]),
                    (2,[half,p(Q(-1,6)),zero,zero]),
                    (4,[scale(a,Q(1,2)),scale(c,Q(1,12)),p(Q(-1,4)),half]),
                    (2,[scale(a,-1),scale(times(c,t),Q(1,6)),half,half])],4)
    # These coordinates are multiplied by k, and their counts divided by k:
    # the result is k times the group trace coordinate-frame matrix.
    trace=outer([(2,[p(Q(1,6)),zero]),(1,[p(Q(-1,3)),zero]),
                 (2,[scale(c,Q(1,6)),minus_half]),(1,[scale(c,Q(-1,3)),p(1)])],2)
    return leaf,standard,trace

def verify_symbolic(defect=None):
    leaf,standard,trace=templates(defect)
    a={(1,0,0):Q(1)};c={(0,1,0):Q(1)};t={(0,0,1):Q(1)}
    a2=times(a,a);c2=times(c,c);z=plus(p(1),scale(t,-2));zero={}
    expected_leaf=[[scale(plus(p(1),c2),Q(1,2)),scale(c,Q(-1,2))],
                   [scale(c,Q(-1,2)),p(Q(1,2))]]
    expected_standard=[
        [plus(p(Q(3,2)),scale(a2,3)),scale(times(times(a,c),z),Q(1,6)),scale(a,Q(-3,2)),zero],
        [scale(times(times(a,c),z),Q(1,6)),plus(p(Q(1,12)),plus(scale(c2,Q(1,36)),scale(times(c2,times(t,t)),Q(1,18)))),scale(times(c,z),Q(-1,12)),scale(times(c,plus(p(1),t)),Q(1,6))],
        [scale(a,Q(-3,2)),scale(times(c,z),Q(-1,12)),p(Q(3,4)),zero],
        [zero,scale(times(c,plus(p(1),t)),Q(1,6)),zero,p(Q(3,2))]]
    expected_trace=[[scale(plus(p(1),c2),Q(1,6)),scale(c,Q(-1,2))],
                    [scale(c,Q(-1,2)),p(Q(3,2))]]
    records=[]
    for label,actual,expected in [('leaf',leaf,expected_leaf),('standard',standard,expected_standard),('trace',trace,expected_trace)]:
        for i,row in enumerate(actual):
            for j,poly in enumerate(row):
                if poly!=expected[i][j]:raise ValueError('whole generic prototype coefficient identity')
                records.append({'block':label,'i':i,'j':j,'whole_coefficients':[{'e':list(e),'c':str(v)}for e,v in sorted(poly.items())]})
    A=Q(3,13);C=Q(9,26);sqrt2=Q(3,2);sqrt58over19=Q(7,4)
    if not 2<sqrt2**2 or not Q(58,19)<sqrt58over19**2:raise ValueError('exact square-root comparison')
    off01=A*C*sqrt2/3;off02=A*sqrt2;off12=C/3;off13=C*2*sqrt58over19/3
    rows=[1+2*A*A+off01+off02,1+C*C+off01+off12+off13,1+off02+off12,Q(29,19)+off13]
    if rows!=[Q(1009,676),Q(1135,676),Q(19,13),Q(1907,988)]or any(r>=2 for r in rows):raise ValueError('complete standard row bounds')
    leaf_trace=1+C*C+C
    if leaf_trace!=Q(991,676)or not leaf_trace<2:raise ValueError('complete leaf and trace row bounds')
    slope=Q(13,135)-Q(9,578);mu_floor=17*slope-Q(15,16)
    if slope<=0 or mu_floor!=Q(15967,36720)or mu_floor<=0:raise ValueError('whole uniform mu margin')
    if not 2-Q(54,289)>1 or not Q(2,3)-Q(15,289)>Q(1,2):raise ValueError('whole uniform alpha beta margins')
    if not Q(37,81)<Q(1,2)or not Q(37,81)<Q(29,57):raise ValueError('whole mean-contrast bounds')
    kappa_bound=Q(5,51)+Q(13,102)
    if kappa_bound!=Q(23,102)or not kappa_bound*Q(3,20)<6:raise ValueError('repair strictly inside uniform lower interval')
    if not Q(35,3)<Q(55,16)**2 or 1-Q(103,16)*Q(3,20)!=Q(11,320)or 1-Q(103,16)*Q(1,32)!=Q(409,512):raise ValueError('whole actual repair norm and refined floors')
    return {'all_generic_prototype_positions':24,'records':records,'standard_row_bounds':[str(v)for v in rows],
            'leaf_trace_row_bound':str(leaf_trace),'uniform_mu_over_s_fifth_margin':str(mu_floor),
            'uniform_kappa_upper_bound':str(kappa_bound),'repair_operator_norm_upper_bound':'103/16',
            'refined_three_twentieths_floor':'11/320','refined_one_thirty_second_floor':'409/512',
            'all_comparisons_exact':True}

def literal_prototype(label,s,scalars,groups,h,l,q):
    """Return a diagonal metric/frame prototype, or None for separately bound blocks."""
    import ast
    leaf,standard,trace=templates()
    if label.startswith('leaf '):
        facet=int(label[5:]);g=next(g for g,facets in enumerate(groups)if facet in facets)
        _,alpha,_=scalars[g];k=len(groups[g]);kind='leaf';metric=[2*s,alpha];poly=leaf;factor=1
    elif label.startswith('standard '):
        g,j=ast.literal_eval(label[len('standard '):]);k=len(groups[g]);mu,_,beta=scalars[g]
        S=sum(len(f)*scalars[g][0]for g,f in enumerate(groups));nu=mu+k*mu*mu/(S*(k-1))
        kind='standard';metric=[Q(2*s,3),12*s,2*beta,2*nu];poly=standard;factor=Q(j*(j+1),2)
    elif label.startswith('trace '):
        g=int(label[len('trace '):]);k=len(groups[g]);_,_,beta=scalars[g]
        kind='trace';metric=[6*s,beta];poly=trace;factor=k
    else:return None
    # Caller supplies its freshly derived r from the original row construction.
    return kind,g,k,metric,poly,factor
