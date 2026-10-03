"""Independent five physical positive-normal systems and all cube vertices."""
import itertools,json,pathlib
from fractions import Fraction as F
from algebra import A,T,solve,dot,sign,determinant
from enclosure import Box,SCALE

P=pathlib.Path(__file__).resolve().parent
def references():
    d=json.loads((P/'REFERENCE.json').read_text());lo,hi=map(F,d['root_bracket']);root=Box(lo,hi)
    def f(x):return 13*x**5-x**4+6*x**3+2*x*x-3*x-1
    if not f(lo)<0<f(hi):raise ValueError('exact root bracket signs')
    derivative=65*root.square().square()-4*root.square()*root+18*root.square()+4*root-3
    if derivative.lo<=0:raise ValueError('root uniqueness')
    if 13*T**5-T**4+6*T**3+2*T**2-3*T-1:raise ValueError('quintic quotient identity')
    points=[[A(v) for v in row] for row in d['vectors']];alt=[A(v) for v in d['alternate_last']]
    if len(points)!=15 or any(len(x)!=3 for x in points):raise ValueError('all fifteen originals')
    for v in points+[alt]:
        if dot(v,v)!=1:raise ValueError('original unit identity')
    for i,j in itertools.combinations(range(15),2):
        if sign(dot(points[i],points[j])-T,root)>0:raise ValueError('original packing support')
    q=solve([[(1-T)*v[j]+T*sum(v,A()) for j in range(3)] for v in [points[i] for i in (8,9,11)]],[T]*3)
    if dot(q,q)!=1:raise ValueError('third contact intersection unit')
    return d,root,points,alt,q

def audit():
    d,root,p,alt,q=references();rows=[]
    for name,v,labels in [('p3',p[3],(1,4,7)),('p13',p[13],(2,8,9)),('q',q,(8,9,11)),('p14',p[14],(0,3,6)),('c14',alt,(3,4,6))]:
        ns=[p[i] for i in labels]
        if any(dot(v,n)!=T for n in ns):raise ValueError('all normal contacts')
        lam=solve([[ns[j][i] for j in range(3)] for i in range(3)],v)
        if any(sign(x-F(2,15),root)!=1 for x in lam) or T*sum(lam,A())!=1:raise ValueError('whole positive stress')
        mat=[[(1-T)*n[j]+T*sum(n,A()) for j in range(3)] for n in ns]
        vertices=[]
        for signs in itertools.product((-1,1),repeat=3):
            u=solve(mat,signs);norm=dot(u,u)
            if sign(9-norm,root)!=1:raise ValueError('complete infinity cube norm')
            bound=norm.enclosure(root)
            vertices.append(dict(signs=list(signs),norm_squared=norm.encode(),norm_squared_interval=bound.endpoints()))
        rows.append(dict(name=name,normal_labels=list(labels),weights=[x.encode() for x in lam],weight_intervals=[x.enclosure(root).endpoints() for x in lam],cube_vertices=vertices))
    if sign(F(17,10)-1/T,root)!=1:raise ValueError('total positive weight bound')
    max_hi=max(F(v['norm_squared_interval'][1]) for row in rows for v in row['cube_vertices'])
    minimum_weight=min(F(x[0]) for row in rows for x in row['weight_intervals'])
    initial=F(21,1000);alpha=F(141,4);beta=F(45,4)
    if alpha/(1-beta*initial)!=F(600,13):raise ValueError('exact first bootstrap')
    if F(600,13)*(1+F(600,13))>=2200:raise ValueError('complete first stage')
    if alpha/(1-beta*F(22,10**6))>=36:raise ValueError('exact second bootstrap')
    if not max_hi<F(35,12)**2 or not minimum_weight>F(11,80) or sign(F(27,16)-1/T,root)!=1:raise ValueError('stronger exact positive-normal bounds')
    aa=F(1085,33);bb=F(350,33)
    if aa/(1-bb*initial)>=43 or 43*44!=1892:raise ValueError('stronger first bootstrap')
    if aa/(1-bb*F(22,10**6))>=33 or 33*34!=1122:raise ValueError('stronger final bootstrap')
    if 10*1122*F(2,10**10)>=F(1,400000):raise ValueError('doubled physical gate')
    return dict(root_bracket=d['root_bracket'],original_unit_vectors=16,original_pair_bounds=105,normal_systems=rows,all_cube_vertices=40,independent_max_norm_squared_upper=str(max_hi),independent_min_weight_lower=str(minimum_weight),scalar_bootstrap=dict(first='600/13',all_after_first='2200delta',second='36',last='1332delta',source='1400delta',delta_upper='1/100000000'),proved_refinement=dict(inverse_norm='35/12',individual_weight_lower='11/80',total_weight_upper='27/16',linear_coefficient='1085/33',quadratic_coefficient='350/33',first='43',all_after_first='1892delta',second='33',last='1122delta',gate_E_upper='2/10000000000'))

if __name__=='__main__':print(json.dumps(audit(),sort_keys=True))
