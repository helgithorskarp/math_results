"""Complete exact avoidance-polytope enumeration and stability constants.

Python >=3.11, standard library. This is not a proof-assistant formalization.
The optional --replay-prerequisites replays the previous near-contact source.
"""
import argparse,hashlib,importlib.util,itertools,json,sys
from pathlib import Path
from fractions import Fraction as Q
import field as f

HERE=Path(__file__).resolve().parent
ROOT=HERE.parents[2]
FIXED=tuple(range(14))
CYCLIC_PERM=(1,0,11,7,5,4,10,3,9,8,6,2,14,13,12)
G26=((0,5),(0,6),(0,7),(0,11),(1,2),(1,3),(1,4),(1,10),(1,12),
     (2,4),(2,8),(2,10),(2,13),(3,4),(4,8),(5,7),(5,9),(5,11),
     (6,8),(6,11),(7,12),(8,13),(9,10),(9,11),(9,13),(10,12))

def digest(value):
    return hashlib.sha256(json.dumps(value,sort_keys=True,separators=(',',':')).encode()).hexdigest()
def require(ok,message):f.require(ok,message)
def norm2(V,H):return f.dot(V,f.matvec(H,V))
def gram(V,H):return [[f.dot(x,f.matvec(H,y)) for y in V] for x in V]

def geometry(c):
    require(c['format']==1 and c['fixed_labels']==list(FIXED),'exact fourteen fixed labels')
    require(c['edges']==[list(e) for e in G26],'exact twenty-six near contacts')
    require(c['short_squared_norm_upper']=='3/4' and c['unit_squared_distance_lower']=='1/25',
            'fixed certified geometric gaps')
    require(c['relaxation_max']=='1/1000' and c['relaxed_distance_constant']==1000,
            'fixed relaxed-avoidance constants')
    require(c['near_contact_max']=='1/10000000000000' and
            c['asymmetric_exclusion_max']=='1/10000000000000000' and
            c['whole_configuration_constant']==2100000000,'fixed near-contact constants')
    require(c['cyclic_permutation']==list(CYCLIC_PERM),'known cyclic Gram relabeling')
    V=[tuple(f.readpoly(p) for p in row) for row in c['incumbent_vectors']]
    require(len(V)==15 and all(len(v)==3 for v in V),'fifteen coefficient vectors')
    H=tuple(tuple(f.ONE if i==j else f.T for j in range(3)) for i in range(3))
    require(f.evaluate(f.F,f.LO)<0<f.evaluate(f.F,f.HI),'root existence in bracket')
    require(f.interval(tuple(i*f.F[i] for i in range(1,6)))[0]>0,'root uniqueness in bracket')
    require(Q(1,2)<f.LO<f.HI<Q(3,5),'metric/root range')
    for k,i in enumerate((0,5,11)):
        require(V[i]==tuple(f.ONE if j==k else f.ZERO for j in range(3)),'anchor basis')
    require(all(norm2(v,H)==f.ONE for v in V),'all incumbent unit norms')
    G=gram(V,H);contacts=[]
    for i,j in itertools.combinations(range(15),2):
        if G[i][j]==f.T:contacts.append((i,j))
        else:require(f.interval(G[i][j])[1]<Q(17,40),'strict incumbent noncontacts')
    require(contacts==sorted(G26+((0,14),(6,14),(3,7),(3,14))),
            'exact prior asymmetric thirty-contact pattern')
    return V,H

def enumerate_polytope(V,H):
    N=[f.matvec(H,V[i]) for i in FIXED]
    # Full dimension follows from strict feasibility at zero. Positive origin
    # dependence of four spanning normals gives boundedness (PROOF section 1).
    labels=(0,1,2,5)
    A=[[V[labels[j]][i] for j in range(3)] for i in range(3)]
    D=f.det(A);sd=f.sign(D)
    require(sd!=0,'three independent origin-tetrahedron vectors')
    U=[f.det([[f.scale(V[labels[3]][i],-1) if j==k else A[i][j]
               for j in range(3)] for i in range(3)]) for k in range(3)]
    require(all(f.sign(x)*sd>0 for x in U),'strictly positive origin dependence')
    require(all(f.add(f.sum_field(f.mul(A[i][j],U[j]) for j in range(3)),
                      f.mul(D,V[labels[3]][i]))==f.ZERO for i in range(3)),
            'origin dependence identity')
    records=[];vertices=[];units=[];unit_triples=[]
    for triple in itertools.combinations(FIXED,3):
        M=[N[i] for i in triple];D=f.det(M);sd=f.sign(D)
        if not sd:
            records.append([list(triple),'singular']);continue
        U=tuple(f.det([[f.T if j==k else M[i][j] for j in range(3)]
                       for i in range(3)]) for k in range(3))
        require(all(f.dot(M[i],U)==f.mul(f.T,D) for i in range(3)),
                'homogeneous Cramer equations')
        witness=next((i for i in FIXED if f.sign(f.sub(f.dot(N[i],U),f.mul(f.T,D)))*sd>0),None)
        if witness is not None:
            records.append([list(triple),'infeasible',witness]);continue
        norm_n=norm2(U,H);square=f.mul(D,D)
        di=f.inverse(D);point=tuple(f.mul(p,di) for p in U)
        require(point not in vertices,'every feasible triple is a distinct vertex')
        vertices.append(point)
        if norm_n==square:
            require(point not in units,'distinct unit vertices')
            units.append(point);unit_triples.append(list(triple))
            records.append([list(triple),'unit'])
        else:
            require(f.sign(f.sub(norm_n,f.scale(square,Q(3,4))))<0,
                    'every other vertex strictly below squared norm three quarters')
            records.append([list(triple),'short'])
    require(len(records)==364 and len(vertices)==24 and len(units)==2,'complete enumeration counts')
    require(units[0]==V[14] and unit_triples==[[0,3,6],[3,4,6]],'first exact completion')
    gap=f.sub(f.scale(f.ONE,2),f.scale(f.dot(units[0],f.matvec(H,units[1])),2))
    require(f.sign(f.sub(gap,f.scalar(Q(1,25))))>0,
            'unit vertices separated by squared distance above one twenty-fifth')
    return vertices,units,records

def identify_cyclic(V,H,other):
    # Both prior incumbent constructions have the same two anchor triples.
    r=f.mul(f.scale(f.T,2),f.inverse(f.add(f.ONE,f.T)))
    C={i:V[i] for i in (0,5,11,1,2,4)}
    steps=((6,0,11,5),(7,0,5,11),(9,5,11,0),(14,0,6,11),
           (12,5,7,0),(13,11,9,5),(3,1,4,2),(8,2,4,1),(10,1,2,4))
    for n,i,j,o in steps:
        C[n]=tuple(f.sub(f.mul(r,f.add(x,y)),z) for x,y,z in zip(C[i],C[j],C[o]))
    alternate=list(V);alternate[14]=other
    G,J=gram([C[i] for i in range(15)],H),gram(alternate,H)
    require(all(J[i][j]==G[CYCLIC_PERM[i]][CYCLIC_PERM[j]] for i in range(15) for j in range(15)),
            'alternate completion exactly the known cyclic incumbent')
    return alternate

def scalar_bridges(c):
    delta=Q(c['relaxation_max']);e=Q(c['near_contact_max']);ea=Q(c['asymmetric_exclusion_max'])
    require(16*delta<=Q(1,2),'short vertex mass at most one half')
    require(4+100==104 and 2*104*4+2<=1000,'relaxed point distance at most one thousand delta')
    require(2000000+30000==2030000,'relaxed plane error from fourteen-point model')
    require(2030000*e<=delta,'entry into relaxed polytope')
    require(1000*2030000<=2100000000,'whole-configuration error at most 2.1 billion e')
    require(ea<=e and 10*2100000000*ea<=Q(1,400000),'asymmetric local-stress entry')
    return {'relaxed_distance_constant':1000,'plane_error_constant':2030000,
            'whole_configuration_constant':2100000000,'asymmetric_gauge_constant':21000000000}

def verify(c):
    V,H=geometry(c)
    vertices,units,records=enumerate_polytope(V,H)
    require(units[1]==tuple(f.readpoly(p) for p in c['alternate_vector']),
            'second exact completion matches the compact fixture')
    identify_cyclic(V,H,units[1]);constants=scalar_bridges(c)
    return {'status':'VERIFIED','active_plane_triples':364,'vertices':24,
            'short_vertices':22,'unit_vertices':2,'unit_triples':[[0,3,6],[3,4,6]],
            'short_squared_norm_upper':'3/4','unit_squared_distance_lower':'1/25',
            'enumeration_sha256':digest(records),'known_cyclic_gram_identified':True,**constants}

def replay(root,near,c):
    require(set(c['near_source_files_sha256'])=={'check.py','models.py','certificate.json','model-functions.json','PROOF.md'},
            'exact previous-source pin set')
    for name,sha in c['near_source_files_sha256'].items():
        require(hashlib.sha256((near/name).read_bytes()).hexdigest()==sha,'pinned previous near-contact file '+name)
    p=root/'tammes15_exact_local_certificate/certificate.json'
    require(hashlib.sha256(p.read_bytes()).hexdigest()==c['incumbent_source_certificate_sha256'],
            'pinned incumbent source certificate')
    require(json.loads(p.read_text())['vectors']==c['incumbent_vectors'],
            'incumbent coefficient data copied exactly from the pinned source')
    spec=importlib.util.spec_from_file_location('completion_near_prerequisite',near/'check.py')
    sys.path.insert(0,str(near))
    old=importlib.util.module_from_spec(spec);spec.loader.exec_module(old)
    # Each prerequisite hash, exact old derivation, and old scalar bridge is
    # checked by the published verifier; no unchanged theorem is claimed new.
    prior=old.verify(root)
    require(prior['status']=='VERIFIED','prior exact derivation replay')

if __name__=='__main__':
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--certificate',type=Path,default=HERE/'certificate.json')
    parser.add_argument('--replay-prerequisites',action='store_true')
    parser.add_argument('--prerequisite-root',type=Path,default=ROOT)
    parser.add_argument('--near-pattern-root',type=Path,default=ROOT/'round-two/six-tammes-2/robust-incumbent-pattern')
    args=parser.parse_args()
    c=json.loads(args.certificate.read_text())
    result=verify(c)
    if args.replay_prerequisites:
        replay(args.prerequisite_root,args.near_pattern_root,c)
        result['prior_exact_bounds_replayed']=True
    print(json.dumps(result,sort_keys=True))
