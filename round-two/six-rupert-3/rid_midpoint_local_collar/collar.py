"""Fresh uniform midpoint torque duals and an explicit physical local collar.

Exact power convolution is checked by full literal Gaussian/unisolvent grids.
No old source forest, collar constants or endpoint inventory is a premise.
"""
from pathlib import Path
from itertools import product
from fractions import Fraction as Q
from math import comb


from primitives import F,Z,O,phi,vertices,rotate,dot,cross,sub,encode,need,digest

def det(a,b,c):return dot(a,cross(b,c))
def plus(a,b):
    out=dict(a)
    for k,v in b.items():out[k]=out.get(k,Z)+v
    return out
def scale(a,b):return {k:b*v for k,v in a.items()}
def times(a,b):
    out={}
    for (i,j),v in a.items():
        for (k,l),w in b.items():
            key=(i+k,j+l);out[key]=out.get(key,Z)+v*w
    return out
def determinant(a,b,c):
    positive=plus(plus(times(times(a[0],b[1]),c[2]),times(times(a[1],b[2]),c[0])),times(times(a[2],b[0]),c[1]))
    negative=plus(plus(times(times(a[0],b[2]),c[1]),times(times(a[1],b[0]),c[2])),times(times(a[2],b[1]),c[0]))
    return plus(positive,scale(negative,-O))
def evaluate(p,u,v):return sum((a*u**i*v**j for (i,j),a in p.items()),Z)
def controls(p):
    need(all(i<=3 and j<=3 for i,j in p),'bidegree3 tensor exceeded')
    return [sum((a*F(Q(comb(i,k)*comb(j,l),comb(3,k)*comb(3,l)))
                 for (k,l),a in p.items() if k<=i and l<=j),Z)
            for i,j in product(range(4),repeat=2)]

def inverse(a):
    n=len(a);rows=[list(row)+[O if i==j else Z for j in range(n)] for i,row in enumerate(a)]
    for i in range(n):
        pivot=next((j for j in range(i,n) if rows[j][i]!=Z),None)
        need(pivot is not None,'literal Gaussian matrix singular')
        rows[i],rows[pivot]=rows[pivot],rows[i]
        q=rows[i][i];rows[i]=[v/q for v in rows[i]]
        for j in range(n):
            if j==i:continue
            q=rows[j][i];rows[j]=[v-q*w for v,w in zip(rows[j],rows[i])]
    need(all(rows[i][j]==(O if i==j else Z) for i in range(n) for j in range(n)), 'Gaussian inverse failed')
    return [row[n:] for row in rows]

def literal_determinant(a):
    rows=[list(row) for row in a];d=O
    for i in range(len(rows)):
        pivot=next((j for j in range(i,len(rows)) if rows[j][i]!=Z),None)
        if pivot is None:return Z
        if pivot!=i:rows[i],rows[pivot]=rows[pivot],rows[i];d=-d
        q=rows[i][i];d*=q
        for j in range(i+1,len(rows)):
            mult=rows[j][i]/q
            for k in range(i+1,len(rows)):rows[j][k]-=mult*rows[i][k]
    return d

def interpolate(samples):
    ts=[F(Q(i,3)) for i in range(4)]
    basis=[[F(comb(3,j))*t**j*(O-t)**(3-j) for j in range(4)] for t in ts]
    inv=inverse(basis)
    a=[[sum((inv[i][k]*samples[k][j] for k in range(4)),Z) for j in range(4)] for i in range(4)]
    b=[[sum((inv[j][k]*a[i][k] for k in range(4)),Z) for j in range(4)] for i in range(4)]
    return [b[i][j] for i,j in product(range(4),repeat=2)]

def verify(certificate):
    V=vertices()
    need(len(V)==60 and len(set(V))==60,'literal original60 vertices differ')
    need(set(V)=={tuple(-q for q in v) for v in V},'original RID centrality fails')
    c=tuple(F(*a) for a in certificate['source_cayley'])
    need(c==(F(Q(4,5),Q(-3,5)),Z,F(Q(3,5),Q(-1,5))),'claimed original source differs')
    receiver={'exact_fixed_receiver_duals':certificate['duals']}
    targets=[tuple(F(*a) for a in row['target']) for row in certificate['duals']]
    need(targets==[tuple(F(sign if j==i else 0) for j in range(3))
                   for i in range(3) for sign in (-1,1)],'complete signed-coordinate targets differ')
    source_to_original=dict(certificate['preimages']);need(len(source_to_original)==4,'four original preimages required')
    need(all(rotate(c,V[i])==V[j] for i,j in source_to_original.items()),'actual original spatial contact identities differ')
    ring=certificate['ring'];need(len(ring)==18 and len(set(ring))==18 and all(0<=i<60 for i in ring),'literal original ring malformed')
    x0,x1=[F(*a) for a in certificate['x_interval']]
    theta1=F(Q(certificate['theta_upper']));dx=x1-x0
    need(Z<2*phi-3<x0<x1<2-phi and theta1>Z,'closed receiver rectangle malformed')
    powers={(0,0):(x0,Z,O),(1,0):(dx,Z,Z),(0,1):(Z,x0*theta1,Z),(1,1):(Z,dx*theta1,Z)}
    def direction(u,v):return tuple(sum((q[j]*u**k*v**l for (k,l),q in powers.items()),Z) for j in range(3))
    corners=[direction(F(u),F(v)) for u,v in product((0,1),repeat=2)]
    norm2=dot(V[0],V[0]);need(all(dot(q,q)==norm2 for q in V),'original circumsphere differs')
    selected_supports=sorted({si for row in receiver['exact_fixed_receiver_duals'] for si,source in row['selected_labels']})
    support_records=[]
    for si in selected_supports:
        E=sub(V[ring[(si+1)%18]],V[ring[si]]);anchor=V[ring[si]]
        gaps=[];normal_bounds=[];heights=[]
        for r in corners:
            m=cross(E,r);h=dot(m,anchor)
            need(h>Z and dot(m,r)==Z,'actual support height/receiving plane failed')
            g=[h-dot(m,q) for q in V];need(all(v>=Z for v in g),'not an actual original support')
            bound=4*h*h-norm2*dot(m,m);need(bound>Z,'R times normalized-normal bound fails')
            gaps.extend(g);normal_bounds.append(bound);heights.append(h)
        support_records.append({'support':si,'all240_original_gap_controls':encode(gaps),
                                'all4_positive_support_heights':encode(heights),
                                'all4_positive_R_normal_bound_controls':encode(normal_bounds)})
    records=[];gaussian_checks=0;literal_coefficient_checks=0
    for row in receiver['exact_fixed_receiver_duals']:
        target=tuple(F(*a) for a in row['target']);labels=row['selected_labels']
        A=[];H=[];configs=[]
        for si,source in labels:
            E=sub(V[ring[(si+1)%18]],V[ring[si]]);anchor=V[ring[si]];v=V[source_to_original[source]]
            mp={k:cross(E,q) for k,q in powers.items()}
            ap={k:cross(v,m) for k,m in mp.items()};hp={k:dot(m,anchor) for k,m in mp.items()}
            need(all(dot(m,v)==hp[k] for k,m in mp.items()),'whole literal spatial contact polynomial fails')
            A.append([{k:q[j] for k,q in ap.items()} for j in range(3)])
            H.append(hp);configs.append((E,anchor,v))
        B=[{(0,0):v} for v in target]
        D=determinant(*A)
        sigma=evaluate(D,O/2,O/2).sign();need(sigma!=0,'center torque determinant zero')
        D=scale(D,F(sigma))
        N=[scale(determinant(B,A[1],A[2]),F(sigma)),
           scale(determinant(A[0],B,A[2]),F(sigma)),
           scale(determinant(A[0],A[1],B),F(sigma))]
        mass={}
        for n,h in zip(N,H):mass=plus(mass,times(n,h))
        torque_identity_controls=0
        for axis in range(3):
            lhs={}
            for n,a in zip(N,A):lhs=plus(lhs,times(n,a[axis]))
            difference=plus(lhs,scale(D,-target[axis]))
            need(all(a==Z for a in difference.values()),'complete spatial torque polynomial identity differs')
            torque_identity_controls+=len(difference)
        dc=controls(D);nc=[controls(n) for n in N];mc=controls(mass)
        need(all(v>Z for v in dc),'some full determinant controls not positive')
        need(all(v>=Z for a in nc for v in a),'some full cofactor controls negative')
        M=row['mass_bound'];need(isinstance(M,int) and M>0,'mass bound malformed')
        slack=[F(M)*a-b for a,b in zip(dc,mc)]
        need(all(v>Z for v in slack),'full mass-bound controls not positive')
        samples=[[[] for j in range(4)] for i in range(4)]
        for ui,vi in product(range(4),repeat=2):
            u,v=F(Q(ui,3)),F(Q(vi,3));r=direction(u,v)
            columns=[];hs=[]
            for E,anchor,q in configs:
                m=cross(E,r);hs.append(dot(m,anchor));columns.append(cross(q,m))
            matrix=[[columns[j][i] for j in range(3)] for i in range(3)]
            actualD=F(sigma)*literal_determinant(matrix);inv=inverse(matrix)
            w=[dot(a,target) for a in inv]
            need(all(dot(matrix[i],w)==target[i] for i in range(3)), 'independent literal Gaussian torque equation differs')
            vals=[actualD,*[actualD*a for a in w],actualD*dot(w,hs)]
            need(vals==[evaluate(p,u,v) for p in [D,*N,mass]],'whole literal Gaussian Cramer/mass values differ')
            samples[ui][vi]=vals;gaussian_checks+=1
        for pos,expected in enumerate([dc,*nc,mc]):
            observed=interpolate([[samples[i][j][pos] for j in range(4)] for i in range(4)])
            need(observed==expected,'full independent literal tensor interpolation differs')
            literal_coefficient_checks+=len(expected)
        records.append({'target':row['target'],'three_actual_spatial_contacts':labels,
                        'signed_determinant_controls':encode(dc),'all3_signed_cofactor_controls':[encode(a) for a in nc],
                        'signed_mass_controls':encode(mc),'integer_mass_bound':M,
                        'all16_strict_mass_bound_controls':encode(slack),
                        'all3_complete_spatial_torque_polynomial_identities_verified':True,
                        'complete_zero_torque_coefficient_count':torque_identity_controls})
    bounds=[a['integer_mass_bound'] for a in records]
    axis_bounds=[max(bounds[2*i:2*i+2]) for i in range(3)]
    C=F(Q(certificate['quadratic_error_bound']));rho=F(Q(certificate['left_Cayley_radius']))
    need(C>=F(Q(3,2)) and Z<rho<O,'physical error constant or radius invalid')
    closure=C*C*sum((F(a*a) for a in axis_bounds),Z)*rho*rho
    need(closure<O,'proposed physical closed radius does not absorb nonlinear contact error')
    result={'agent':'six-rupert-3','role':'researcher','source_cayley':encode(c),
            'whole_closed_receiving_x_interval':encode((x0,x1)),
            'whole_closed_receiving_theta_interval':['0',certificate['theta_upper']],
            'receiving_chart':'r=(x,x*theta,1)',
            'all4_original_parent_spatial_preimages':source_to_original,
            'all5_full_original_support_checks':support_records,
            'all6_exact_uniform_torque_duals':records,
            'independent_literal_Gaussian_grid_checks':gaussian_checks,
            'independent_complete_literal_tensor_coefficient_checks':literal_coefficient_checks,
            'positive_controls':sum(sum(v.sign()>0 for v in dc) for dc in [[F(*q) for q in a['signed_determinant_controls']] for a in records]),
            'six_signed_mass_bounds':bounds,'three_axis_mass_bounds':axis_bounds,
            'R_times_normal_norm_strictly_less_than':2,'quadratic_error_constant':certificate['quadratic_error_bound'],
            'closed_physical_left_Cayley_radius':certificate['left_Cayley_radius'],'nonlinear_absorption':closure.encode(),
            'unit_centered_necessary_local_result':'Q=R*; all original translation/enlargement removed by original RID centrality',
            'fit_receiving_subset_and_scale_translation_dependency':'9896/0: theta0, lambda1, original t0',
            'global_RID':'OPEN','proof_status':'author checked, unformalized, independently unreviewed',
            'threads':1}
    return result
