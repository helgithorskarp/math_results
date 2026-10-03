"""Whole original frame chart, full closed rectangle and every derivative."""
import json,pathlib
from fractions import Fraction as F
from algebra import A,T,solve,dot,determinant,sign
from enclosure import Box,BITS,SCALE
from normals import references
from jets import Jet,frame

LABELS=(0,1,2,4,5,6,7,8,9,10,11,12)
def upper_absolute(b):return F(max(abs(b.lo),abs(b.hi)),SCALE)
def audit():
    d,root,p,alt,q=references();M=[[p[j][i] for j in (1,2,4)] for i in range(3)]
    if determinant(M)!=-1:raise ValueError('old-to-new anchor determinant')
    for i in range(3):
        for j in range(3):
            if dot([M[k][i] for k in range(3)],[M[k][j] for k in range(3)])!=(1 if i==j else T):raise ValueError('complete anchor isometry')
    B=[solve(M,v) for v in p];z0=determinant([[B[7][i],B[12][i],B[1][i]] for i in range(3)])/(1-dot(B[7],B[1]))
    advertised=A([F(-115,16),-4,F(215,8),F(-37,2),F(637,16)])
    if z0!=advertised:raise ValueError('entire chart inverse identity')
    Dt=(1-T)**2*(1+2*T);rad=-Dt*determinant([[B[9][i],B[7][i],B[10][i]] for i in range(3)])
    if sign(rad,root)!=1:raise ValueError('original positive branch radical')
    exact,scalars=frame(Jet(T,1,0),Jet(z0,0,1),rad)
    for label in LABELS:
        if [x.v for x in exact[label]]!=B[label]:raise ValueError('ALL original specialization coordinates')
    Zlo=F(9400279416352442033499962019,10**28);Zhi=F(470013970817622101674998101,5*10**26)
    if sign(z0-Zlo,root)!=1 or sign(Zhi-z0,root)!=1:raise ValueError('whole exact incumbent z enclosure')
    lo,hi=map(F,d['root_bracket']);rectangle=[lo-F(1,10**6),hi+F(1,10**6),Zlo-F(1,10**6),Zhi+F(1,10**6)]
    whole,domain=frame(Jet(Box(*rectangle[:2]),1,0),Jet(Box(*rectangle[2:]),0,1))
    for key in ('metric_determinant','chart_denominator','g','one_minus_s_squared','chart_domain_gap','original_radical'):
        if domain[key].v.lo<=0:raise ValueError('whole rectangle positive domain:'+key)
    point,point_domain=frame(Jet(root,1,0),Jet(z0.enclosure(root),0,1))
    bounds=[];exact_jets=[];compared=0
    for label in LABELS:
        norms=[sum(upper_absolute(x.d[j]) for x in whole[label]) for j in range(2)]
        if not norms[0]<15 or not norms[1]<2:raise ValueError('whole rectangle derivative sum')
        bounds.append(dict(label=label,sum_dt_upper=str(norms[0]),sum_dz_upper=str(norms[1]),whole_coordinate_jets=[dict(value=x.v.endpoints(),dt=x.d[0].endpoints(),dz=x.d[1].endpoints()) for x in whole[label]]))
        for i,x in enumerate(exact[label]):
            for y,b in zip((x.v,)+x.d,(point[label][i].v,)+point[label][i].d):
                # Compare the exact algebraic number to each interval endpoint.
                # Independently rounded enclosures need not contain each other.
                if sign(y-A(F(b.lo,SCALE)),root)<0 or sign(A(F(b.hi,SCALE))-y,root)<0:
                    raise ValueError('exact specialized jet outside interval')
                compared+=1
            exact_jets.append(dict(label=label,coordinate=i,value=x.v.encode(),dt=x.d[0].encode(),dz=x.d[1].encode()))
    # The Q_t eigenvalue bounds require no numerical square roots.
    if not 1+2*F(593,1000)<F(3,2)**2 or not 1-F(593,1000)>F(25,64) or not 1+2*F(14,25)>F(25,16):raise ValueError('physical Q_t and derivative eigenvalue bounds')
    if not F(5,2)<F(8,5)**2 or not F(3,2)*15+F(4,5)*F(8,5)<24:raise ValueError('whole physical mean-value constants')
    if not rectangle[0]>F(14,25) or not rectangle[1]<F(593,1000):raise ValueError('whole closed original t domain')
    return dict(original_labels=list(LABELS),anchor_determinant='-1',complete_original_anchor_Gram_positions=9,original_anchor_solve_coordinates=45,all_original_frame_specializations=36,chart_inverse_z0=z0.encode(),positive_radical=rad.encode(),rectangle=list(map(str,rectangle)),bits=BITS,clipping=False,whole_positive_domains={k:v.v.endpoints() for k,v in domain.items() if k not in ('s','k')},complete_coordinate_partials=72,complete_exact_value_and_partial_enclosures=compared,whole_derivative_bounds=bounds,exact_jet_values=exact_jets,physical_displacement='24|t-tau|+3|z-z0|')
if __name__=='__main__':print(json.dumps(audit(),sort_keys=True))
