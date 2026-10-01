"""Exact cap certificate, complete vertex enumeration, and scalar bridges."""
import argparse,hashlib,itertools,json
from pathlib import Path
from fractions import Fraction as Q
import field as f

HERE=Path(__file__).resolve().parent
CORE=tuple(i for i in range(15) if i not in (3,14))
STEPS=((6,0,11,5),(7,0,5,11),(9,5,11,0),
       (8,2,4,1),(10,1,2,4),(12,1,10,2),(13,2,8,4))

def require(ok,message):f.require(ok,message)
def norm(v,H):return f.dot(v,f.matvec(H,v))
def digest(value):
    return hashlib.sha256(json.dumps(value,sort_keys=True,separators=(',',':')).encode()).hexdigest()
def graph():
    edges=set()
    for anchors in ((0,5,11),(1,2,4)):
        edges.update(tuple(sorted(e)) for e in itertools.combinations(anchors,2))
    K={0:0,5:2,11:17,1:0,2:2,4:17}
    for n,i,j,o in STEPS:
        require(all(tuple(sorted(e)) in edges for e in ((i,j),(i,o),(j,o))),
                'old triangle present for every core reflection')
        edges.update((tuple(sorted((n,i))),tuple(sorted((n,j)))))
        K[n]=20+K[i]+K[j]+K[o]
    edges.update(((6,8),(7,12),(9,10),(9,13)))
    require(set(K)==set(CORE) and max(K.values())<80,'thirteen core reflection error constants')
    require(len(edges)==24 and {x for e in edges for x in e}==set(CORE),'exact twenty-four-edge core')
    # Every label used by the orientation, determinant and recovery proof is
    # in CORE. The two omitted reflections supply no antecedent for that proof.
    require({2,6,7,8,9,10,12,13}<=set(CORE),'core-only orientation data')
    return sorted(edges),K

def geometry(c):
    require(c['format']==1 and c['core_labels']==list(CORE),'thirteen fixed core labels')
    edges,K=graph();require(c['core_edges']==[list(e) for e in edges],'derived core graph')
    require(f.evaluate(f.F,f.LO)<0<f.evaluate(f.F,f.HI),'root bracket')
    require(f.interval(tuple(i*f.F[i] for i in range(1,6)))[0]>0,'unique bracketed root')
    require(Q(1,2)<f.LO<f.HI<Q(3,5),'positive definite metric and scale domain')
    V=[tuple(f.readpoly(p) for p in v) for v in c['incumbent_vectors']]
    require(len(V)==15 and all(len(v)==3 for v in V),'fifteen reference coefficient vectors')
    H=tuple(tuple(f.ONE if i==j else f.T for j in range(3)) for i in range(3))
    N=[f.matvec(H,v) for v in V]
    require(all(norm(v,H)==f.ONE for v in V),'exact reference unit norms')
    for k,i in enumerate((0,5,11)):
        require(V[i]==tuple(f.ONE if j==k else f.ZERO for j in range(3)),'anchor basis')
    for n,i,j,o in STEPS+((3,1,4,2),(14,0,6,11)):
        require(all(f.mul(f.add(f.ONE,f.T),f.add(V[n][k],V[o][k]))==
                    f.scale(f.mul(f.T,f.add(V[i][k],V[j][k])),2) for k in range(3)),
                'reference triangle-reflection identity')
    a=tuple(map(Q,('-27/2','-3','35','-24','117/2')))
    b=tuple(map(Q,('-31/4','-19/2','34','-53/2','195/4')))
    d=tuple(map(Q,('81/4','21/2','-69','101/2','-429/4')))
    M=((a,b,d),(d,a,b),(b,d,a))
    require(all(f.dot(V[i],N[j])==M[ii][jj] for ii,i in enumerate((0,5,11))
                for jj,j in enumerate((1,2,4))),'known anchor cross Gram matrix')
    contacts=[]
    for i,j in itertools.combinations(range(15),2):
        g=f.dot(V[i],N[j])
        if g==f.T:contacts.append((i,j))
        else:require(f.interval(g)[1]<Q(17,40),'reference strict noncontacts')
    require(contacts==sorted(edges+[(1,3),(3,4),(0,14),(6,14),(3,7),(3,14)]),
            'reference exact thirty-contact pattern')
    longs=[]
    require([x['active_labels'] for x in c['exterior_vertices']]==[[0,4,6],[0,4,7]],
            'two specified exterior intersections')
    for item in c['exterior_vertices']:
        p=tuple(f.readpoly(q) for q in item['vector']);labels=item['active_labels']
        require(f.sign(f.det([N[i] for i in labels]))!=0,'independent exterior active normals')
        require(all(f.dot(N[i],p)==f.T for i in labels),'exact exterior intersection')
        require(all(f.sign(f.sub(f.dot(N[i],p),f.T))<=0 for i in CORE),'exterior point feasible')
        require(f.sign(f.sub(norm(p,H),f.ONE))>0,'exterior point squared norm above one')
        longs.append(p)
    blend=Q(c['center_blend']);C=tuple(f.readpoly(q) for q in c['center'])
    require(blend==Q(4,5) and C==tuple(f.add(f.add(a,b),f.scale(z,blend))
                                    for a,b,z in zip(longs[0],longs[1],V[3])),
            'exact selected cap center')
    cut=Q(c['cap_bound']);center_norm=norm(C,H);upper=Q(c['cap_code_parameter_upper'])
    require(cut>0 and upper==Q(593,1000),'cap bound and code parameter domain')
    gap=f.sub(f.scalar(2*cut**2),f.mul(f.scalar(1+upper),center_norm))
    require(f.sign(f.sub(gap,f.scalar(Q(c['cap_capacity_gap_lower']))))>0,
            'strict cap-capacity gap')
    require(f.sign(f.sub(center_norm,f.scalar(cut**2)))>0,'nonempty proper cap')
    require(f.sign(f.sub(f.scalar(cut),f.dot(V[3],f.matvec(H,C))))>0,
            'isolated completion strictly inside the cut polytope')
    return V,H,C,cut

def enumerate_cut(V,H,C,cut,c):
    constraints=[(i,f.matvec(H,V[i]),f.T) for i in CORE]+[('cap',f.matvec(H,C),f.scalar(cut))]
    tet=(0,1,2,5)
    A=[[V[tet[j]][i] for j in range(3)] for i in range(3)]
    D=f.det(A);sd=f.sign(D)
    U=[f.det([[f.scale(V[5][i],-1) if j==k else A[i][j] for j in range(3)] for i in range(3)]) for k in range(3)]
    require(sd!=0 and all(f.sign(x)*sd>0 for x in U),'positive spanning origin tetrahedron')
    require(all(f.add(f.dot(A[i],U),f.mul(D,V[5][i]))==f.ZERO for i in range(3)),
            'positive origin dependence identity')
    r=Q(c['short_squared_norm_upper'])
    require(0<r<1,'strict short-vertex bound')
    records=[];vertices=[];unit_labels=[]
    for inds in itertools.combinations(range(len(constraints)),3):
        labels=[constraints[i][0] for i in inds]
        rows=[constraints[i][1] for i in inds];rhs=[constraints[i][2] for i in inds]
        D=f.det(rows);sd=f.sign(D)
        if not sd:records.append([labels,'singular']);continue
        U=tuple(f.det([[rhs[i] if j==k else rows[i][j] for j in range(3)] for i in range(3)]) for k in range(3))
        require(all(f.dot(rows[i],U)==f.mul(rhs[i],D) for i in range(3)),'homogeneous Cramer equations')
        witness=next((label for label,n,b in constraints if f.sign(f.sub(f.dot(n,U),f.mul(b,D)))*sd>0),None)
        if witness is not None:records.append([labels,'infeasible',witness]);continue
        square=f.mul(D,D);nn=norm(U,H)
        if nn==square:
            require(all(U[k]==f.mul(D,V[3][k]) for k in range(3)),'unique advertised unit vertex')
            unit_labels.append(labels);records.append([labels,'unit'])
        else:
            require(f.sign(f.sub(nn,f.scale(square,r)))<0,'all other vertices strictly short')
            records.append([labels,'short'])
        inv=f.inverse(D);point=tuple(f.mul(x,inv) for x in U)
        require(point not in vertices,'no duplicated feasible active triple')
        vertices.append(point)
    require(len(records)==364 and len(vertices)==24 and unit_labels==[[1,4,7]],
            'complete cut enumeration counts')
    return records,vertices

def scalar_bridges(c):
    r=Q(c['short_squared_norm_upper']);d=Q(c['relaxation_max'])
    distance=c['relaxed_isolated_distance_constant']
    require(0<d<=Q(1,1000),'relaxed cap domain')
    require(distance>=2+8/(1-r),'convex-mass isolated-point distance')
    e=Q(c['near_contact_max']);ee=Q(c['exclusion_max']);K=c['whole_configuration_constant']
    require(0<=ee<=e<=Q(1,10**13),'old quantitative core domain')
    require(2030000*e<=d,'core-to-avoidance relaxation')
    fourteen=max(2000000,distance*2030000)
    last_relax=fourteen+30000
    require(last_relax*e<=Q(1,1000),'entry into the old fourteen-plane relaxation')
    require(K>=max(fourteen,1000*last_relax),'whole-code distance coefficient')
    require(K*ee<=Q(1,100) and 10*K*ee<=Q(1,400000),'both local exclusion radii reached')
    return {'relaxed_isolated_distance_constant':distance,'fourteen_point_error_constant':fourteen,
            'last_point_relaxation_constant':last_relax,'whole_configuration_constant':K,
            'near_contact_max':str(e),'exclusion_max':str(ee)}

def verify(c):
    V,H,C,cut=geometry(c);records,vertices=enumerate_cut(V,H,C,cut,c)
    return {'status':'VERIFIED','core_points':13,'prescribed_edges':24,
            'active_plane_triples':364,'cut_vertices':24,'short_vertices':23,'unit_vertices':1,
            'unit_triple':[1,4,7],'short_squared_norm_upper':c['short_squared_norm_upper'],
            'cap_code_parameter_upper':c['cap_code_parameter_upper'],
            'cap_capacity_gap_lower':c['cap_capacity_gap_lower'],
            'enumeration_sha256':digest(records),**scalar_bridges(c)}

if __name__=='__main__':
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--certificate',type=Path,default=HERE/'certificate.json')
    args=parser.parse_args()
    print(json.dumps(verify(json.loads(args.certificate.read_text())),sort_keys=True))
