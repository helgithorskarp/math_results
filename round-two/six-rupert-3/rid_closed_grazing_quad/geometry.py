"""Exact actual RID geometry, classical quotient and literal cut inventory.

All named proper-group/lift correspondences and Hamilton coefficients
are freshly checked. No floating arithmetic or private input is used.
Classical quaternion/polytope implications are proved in PROOF.md.
"""
from pathlib import Path
from fractions import Fraction as Q
from itertools import combinations, permutations, product
import hashlib, json, sys

HERE = Path(__file__).resolve().parent
FIELD_SHA256 = "7801bce4e611b05c8d3d982a862d3f281db7585ef5219ea8fb901c6417c129b0"
if hashlib.sha256((HERE/'field.py').read_bytes()).hexdigest()!=FIELD_SHA256:
    raise ValueError('named ordered-field source changed before import')
from field import F,ZERO as Z,ONE as O,PHI as phi,dot,cross,sub,neg,vertices,encode,determinant,proper_group,act,matmul
pins={'field.py':FIELD_SHA256}
OUT=HERE
RING=[48, 36, 54, 56, 38, 53, 46, 18, 11, 23, 5, 3, 21, 6, 13, 41]
DUAL_CONTACTS=[[0, -1, [[0, 36], [4, 53], [5, 53]]], [0, 1, [[6, 18], [4, 38], [7, 18]]], [1, -1, [[1, 36], [3, 38], [4, 38]]], [1, 1, [[4, 53], [5, 53], [7, 18]]], [2, -1, [[1, 54], [4, 53], [6, 18]]], [2, 1, [[1, 36], [5, 53], [0, 48]]]]

def need(ok,msg):
    if not ok:raise ValueError(msg)


def dec(v):
    return tuple(F(Q(a),Q(b)) for a,b in v)


def midpoint(a,b):
    return tuple((x+y)/2 for x,y in zip(a,b))


def binary(swap=False):
    result=set()
    for i in range(4):
        for sign in [-1,1]:
            a=[Z]*4;a[i]=F(sign);result.add(tuple(a))
    result.update(tuple(F(s)/2 for s in signs) for signs in product([-1,1],repeat=4))
    seed=(Z,O/2,phi/2,(phi-1)/2)
    if swap:seed=(Z,O/2,(phi-1)/2,phi/2)
    for perm in permutations(range(4)):
        if sum(perm[i]>perm[j] for i in range(4) for j in range(i+1,4))%2:continue
        raw=tuple(seed[i] for i in perm);indices=[i for i,x in enumerate(raw) if x!=Z]
        for signs in product([-1,1],repeat=3):
            a=list(raw)
            for i,s in zip(indices,signs):a[i]*=s
            result.add(tuple(a))
    need(len(result)==120 and all(dot(q,q)==O for q in result),'binary units differ')
    return sorted(result)


def qmatrix(q):
    h=q[0];v=q[1:];v2=dot(v,v)
    need(h*h+v2==O,'literal lift is not unit')
    skew=((Z,-v[2],v[1]),(v[2],Z,-v[0]),(-v[1],v[0],Z))
    return tuple(tuple((h*h-v2 if i==j else Z)+2*v[i]*v[j]+2*h*skew[i][j]
                       for j in range(3)) for i in range(3))


def qmul(a,b):
    h,v,k,w=a[0],a[1:],b[0],b[1:];x=cross(v,w)
    return (h*k-dot(v,w),*(h*w[j]+k*v[j]+x[j] for j in range(3)))


def hamilton_coefficients():
    e3=[tuple(O if i==j else Z for i in range(3)) for j in range(3)]
    e4=[tuple(O if i==j else Z for i in range(4)) for j in range(4)];count=0
    for r in e3:
        for q in e4:
            for k in e4:
                actual=qmul(qmul((Z,*r),q),k)[0]
                expected=-(q[0]*dot(r,k[1:])+k[0]*dot(r,q[1:])+dot(cross(k[1:],r),q[1:]))
                need(actual==expected,'universal Hamilton coefficient differs');count+=1
    need(count==48,'Hamilton coefficient coverage incomplete');return count


def build():
    V=vertices();G=set(proper_group(V));B=binary()
    matrices={qmatrix(q) for q in B}
    need(len(G)==len(matrices)==60 and matrices==G,'literal quaternion/body group correspondence fails')
    need({qmatrix(q) for q in binary(True)}!=G,'wrong named parity negative control fails')
    need(set(B)=={tuple(-x for x in q) for q in B},'signed lifted group is incomplete')
    coefficient_checks=hamilton_coefficients()
    normals=[q[1:] for q in B if q[0]==phi/2];height=1-phi/2
    need(len(normals)==12 and height>Z and set(normals)=={neg(n) for n in normals},'nearest opposite normals differ')
    need(any(dot(a,cross(b,c))!=Z for a,b,c in combinations(normals,3)),'quotient boundedness has no spanning opposite normals')
    D=set()
    for a,b,c in combinations(normals,3):
        det=dot(a,cross(b,c))
        if det==Z:continue
        v=tuple(height*(cross(b,c)[i]+cross(c,a)[i]+cross(a,b)[i])/det for i in range(3))
        if all(dot(n,v)<=height for n in normals):D.add(v)
    D=sorted(D)
    expected_D=set(tuple(F(s)*x for s in signs) for signs in product([-1,1],repeat=3) for x in [2*phi-3])
    for seed in [(2-phi,Z,5-3*phi)]:
        for shift in range(3):
            a=seed[shift:]+seed[:shift]
            for signs in product([-1,1],repeat=3):expected_D.add(tuple(s*x for s,x in zip(signs,a)))
    need(len(D)==20 and set(D)==expected_D,'complete literal quotient vertex enumeration differs')
    need(all(abs(q[0]+dot(q[1:],v))<=O for q in B for v in D),'full body comparison fails')
    need(all(dot(v,v)==39-24*phi for v in D),'whole quotient vertex radius differs')
    faces=[];triangles=[];roots=[];alpha=Q(1,9);root_metadata=[]
    volume=Z
    for ni,n in enumerate(normals):
        ids=[i for i,v in enumerate(D) if dot(n,v)==height]
        need(len(ids)==5,'quotient facet is not a complete pentagon')
        candidates=[]
        first=min(ids)
        for rest in permutations([i for i in ids if i!=first]):
            order=[first,*rest]
            if all(dot(n,cross(sub(D[b],D[a]),sub(D[c],D[a])))>Z
                   for a,b in zip(order,order[1:]+order[:1]) for c in order if c not in [a,b]):
                candidates.append(order)
        need(len(candidates)==1,'literal facet cycle orientation is ambiguous')
        face=candidates[0];faces.append(face)
        for j in [1,2,3]:
            indices=[face[0],face[j],face[j+1]];A,C,E=[D[i] for i in indices]
            det=abs(dot(A,cross(C,E)));need(det>Z,'source face triangle is degenerate')
            triangles.append(indices)
            aA,aC,aE=[tuple(alpha*x for x in v) for v in [A,C,E]]
            tet=[(aA,aC,aE,E),(aA,aC,C,E),(aA,A,C,E)]
            total=Z
            for slot,T in enumerate(tet):
                dv=abs(dot(sub(T[1],T[0]),cross(sub(T[2],T[0]),sub(T[3],T[0]))))
                need(dv>Z and all(dot(n0,v)<=height for n0 in normals for v in T),
                     'source root tetrahedron is degenerate or outside D')
                total+=dv;roots.append(T);root_metadata.append([ni,j-1,slot])
            need(total==(1-F(alpha)**3)*det,'independent exact frustum volume identity fails')
            volume+=total
    need(len(faces)==12 and len(triangles)==36 and len(roots)==108,'whole shell root count differs')
    need((39-24*phi)/81<F(Q(1,400)),'whole omitted core is outside local collar')
    V=vertices();radius2=7+8*phi;r=(O/10,(2+phi)/50,O);r2=dot(r,r)
    data={'actual_supports':[],'six_actual_signed_coordinate_duals':[]}
    for i,j in zip(RING,RING[1:]+RING[:1]):
        raw=cross(sub(V[j],V[i]),r);h=dot(raw,V[i])
        need(h>Z,'actual point support height nonpositive')
        data['actual_supports'].append({'endpoints':[i,j],'polar':encode(tuple(x/h for x in raw))})
    for axis,sign,contacts in DUAL_CONTACTS:
        f=[cross(V[vi],dec(data['actual_supports'][si]['polar'])) for si,vi in contacts]
        det=dot(f[0],cross(f[1],f[2]));need(det!=Z,'actual point coordinate basis singular')
        weights=[sign*x[axis]/det for x in [cross(f[1],f[2]),cross(f[2],f[0]),cross(f[0],f[1])]]
        data['six_actual_signed_coordinate_duals'].append({'axis':axis,'sign':sign,
              'contacts':[{'support':si,'source':vi} for si,vi in contacts],'weights':encode(weights)})
    need(len(V)==60 and set(V)=={neg(v) for v in V} and all(dot(v,v)==radius2 for v in V),
         'actual central sphere inventory differs')
    Ns=[];heights=[];offgaps=[]
    for row in data['actual_supports']:
        i,j=row['endpoints'];edge=sub(V[j],V[i]);raw=cross(edge,r);h=dot(raw,V[i])
        need(h>Z and dot(edge,edge)==F(4),'actual literal edge or support height differs')
        N=tuple(x/h for x in raw)
        need(encode(N)==row['polar'] and dot(N,r)==Z,'actual physical polar differs')
        actual=[k for k,v in enumerate(V) if dot(N,v)==O]
        need(actual==sorted([i,j]) and all(dot(N,v)<=O for v in V),'full original support inventory differs')
        need(radius2*dot(N,N)<F(Q(81,64)),'fresh quadratic support norm bound fails')
        Ns.append(N);heights.append(h)
        offgaps.extend(dot(raw,sub(V[i],v)) for k,v in enumerate(V) if k not in [i,j])
    need(len(Ns)==16 and set(Ns)=={neg(n) for n in Ns},'actual support antipodes missing')
    coord=[9,14,5];duals=[]
    for row in data['six_actual_signed_coordinate_duals']:
        weights=dec(row['weights']);targets=[]
        torques=[cross(V[c['source']],Ns[c['support']]) for c in row['contacts']]
        target=tuple(F(row['sign']) if j==row['axis'] else Z for j in range(3))
        actual=tuple(sum((w*f[j] for w,f in zip(weights,torques)),Z) for j in range(3))
        need(actual==target and all(w>Z for w in weights) and sum(weights,Z)<F(coord[row['axis']]),
             'actual positive signed coordinate dual or mass fails')
        duals.append(row)
    need(len(duals)==6 and {(x['sign'],x['axis']) for x in duals}=={(s,j) for s in [-1,1] for j in range(3)},
         'signed local coordinate coverage missing')
    cuts=[];seen=set()
    for si,N in enumerate(Ns):
        for vi,v in enumerate(V):
            a=dot(N,v);f=cross(v,N)
            M=tuple(tuple((a-1 if i==j==0 else f[j-1] if i==0 else f[i-1] if j==0 else
                           N[i-1]*v[j-1]+v[i-1]*N[j-1]-(a+1 if i==j else Z))
                          for j in range(4)) for i in range(4))
            if M in seen:continue
            seen.add(M);cuts.append({'kind':'support','support':si,'source':vi,'M':M,'N':N,'v':v})
    nsupport=len(cuts);need(nsupport==480,'unexpected literal antipodal cut count')
    for k in B:
        if next(x for x in k if x!=Z)<Z:continue
        u=cross(k[1:],r);linear=(dot(r,k[1:]),*(k[0]*r[j]+u[j] for j in range(3)))
        M=tuple(tuple(linear[i]*linear[j]-(r2 if i==j==0 else Z) for j in range(4)) for i in range(4))
        cuts.append({'kind':'gauge','k':k,'linear':linear,'M':M})
    need(len(cuts)==540,'complete sign-paired central gauge count differs')
    matrices=[[[x.encode() for x in row] for row in cut['M']] for cut in cuts]
    record={'agent':'six-rupert-3','role':'researcher','status':'exact named RID and classical closest-body geometry; joint source cover checked separately',
            'original_input_sha256':pins,'receiver_raw':encode(r),'source_body_vertices':60,'source_quotient_vertices':20,
            'literal_faces':faces,'face_triangles':triangles,'root_metadata':root_metadata,'complete_closed_shell_roots':108,
            'alpha':'1/9','whole_inner_core_local_entry':True,'source_root_abs_determinant_sum':volume.encode(),
            'actual_receiver_supports':16,'actual_source_comparisons':960,'minimum_raw_support_height':min(heights).encode(),
            'minimum_raw_offendpoint_support_gap':min(offgaps).encode(),
            'unique_literal_support_cut_matrices':nsupport,'all_sign_paired_central_gauge_matrices':60,
            'cut_matrices_sha256':hashlib.sha256(json.dumps(matrices,separators=(',',':')).encode()).hexdigest(),
            'root_geometry_sha256':hashlib.sha256(json.dumps([[encode(v) for v in T] for T in roots],separators=(',',':')).encode()).hexdigest(),
            'frustum_coverage_reference':'public pentagonal9363 ordinary closed frustum partition, rebuilt in the actual RID quotient',
            'local_conditional_squared_closure':'43639/51200','no_all_source_theorem':True}
    return {'D':D,'normals':normals,'height':height,'roots':roots,'cuts':cuts,'V':V,'Ns':Ns,'r':r,'r2':r2,'duals':duals,'record':record,'ring':RING,'actual_supports':data['actual_supports'],'B':B,'G':G}
