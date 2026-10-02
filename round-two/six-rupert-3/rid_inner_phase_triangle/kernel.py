"""Exact joint receiver/source kernel for the first closed annular cell.

No numerical proposal enters the signs or domain. CPython/Fraction Q(phi).
Physical receiver degree (1,1); central-gauge receiver degree (2,2).
Every source polynomial is homogeneous quadratic on a closed tetrahedron.
"""
from pathlib import Path
from itertools import product
from functools import lru_cache
from math import comb
import hashlib,json,sys
ROOT=Path(__file__).resolve().parent
from geometry import build,F,Q,Z,O,phi,dot,cross,sub,midpoint,need,encode,qmul

RING=[48,36,54,56,38,53,46,18,19,11,23,5,3,21,6,13,41,40]
BITS=list(product(range(2),repeat=2))
PAIRS=[(i,j) for i in range(4) for j in range(i,4)]
EDGES=[(i,j) for i in range(4) for j in range(i+1,4)]

def digest(value):
    return hashlib.sha256(json.dumps(value,sort_keys=True,separators=(',',':')).encode()).hexdigest()

@lru_cache(maxsize=50000)
def scalar(a,b):return dot(a,b)

def raw(V,si,r):
    i,j=RING[si],RING[(si+1)%18];E=sub(V[j],V[i])
    if si in (7,16):
        need(E[:2]==(Z,Z) and r[0]>Z,'normalized pole edge or positive x differs')
        return (-E[2]*r[1]/r[0],E[2],Z)
    return cross(E,r)

def source_geometry():
    data=build();D=data['D'];alpha=F(Q(1,22));roots=[];volume=Z
    for face in data['record']['face_triangles']:
        A,B,C=[D[i] for i in face]
        aA,aB,aC=[tuple(alpha*x for x in p) for p in (A,B,C)]
        local=[(aA,aB,aC,C),(aA,aB,B,C),(aA,A,B,C)];total=Z
        for T in local:
            dv=abs(dot(sub(T[1],T[0]),cross(sub(T[2],T[0]),sub(T[3],T[0]))))
            need(dv>Z,'new closed source root degenerate')
            need(all(dot(n,v)<=data['height'] for n in data['normals'] for v in T),'new source root outside actual D')
            total+=dv;roots.append(T)
        need(total==(O-alpha**3)*abs(dot(A,cross(B,C))),'new alpha1/22 frustum partition volume differs')
        volume+=total
    need(len(roots)==108 and len(data['record']['face_triangles'])==36,'closed source root inventory differs')
    need((39-24*phi)/484<F(Q(1,53**2)),'whole omitted core outside proved annular collar')
    need(all(tuple(O if i==j else Z for i in range(4)) in data['B'] for j in range(4)),'true zero-scalar chart obstruction axes missing')
    return data,roots,volume

def make_domain(data,bounds=(Q(1,8),Q(3,16),Q(0),Q(1,2))):
    u0,u1,v0,v1=map(Q,bounds)
    need(Q(1,8)<=u0<u1<=1 and 0<=v0<v1<=1,'closed receiver rectangle outside proved annulus')
    s=2-phi;x0,x1,t0,t1=[F(a)*s for a in (u0,u1,v0,v1)]
    R=[(x,x*t,O) for x,t in product((x0,x1),(t0,t1))]
    V=data['V'];supports=[];gaps=[];heights=[]
    for si in range(18):
        ms=[raw(V,si,r) for r in R];hs=[dot(m,V[RING[si]]) for m in ms]
        row=[[dot(m,sub(V[RING[si]],v)) for v in V] for m in ms]
        need(all(h>Z for h in hs) and all(a>=Z for g in row for a in g),'actual all-original receiver support failed')
        need(all(dot(m,r)==Z for m,r in zip(ms,R)),'actual support not in receiving plane')
        supports.append({'m':ms,'h':hs});gaps.extend(a for g in row for a in g);heights.extend(hs)
    # Power basis in u,v on [0,1]^2: constant, u, v, uv.
    dx,dt=x1-x0,t1-t0
    powers=[R[0],(dx,dx*t0,Z),(Z,x0*dt,Z),(Z,dx*dt,Z)]
    pbits=[(0,0),(1,0),(0,1),(1,1)]
    norm={(u,v):Z for u,v in product(range(3),repeat=2)}
    for a,b in product(range(4),repeat=2):
        ex=tuple(pbits[a][j]+pbits[b][j] for j in range(2))
        norm[ex]+=dot(powers[a],powers[b])
    labels=[{'kind':'support','support':si,'source':vi,'v':v} for si in range(9) for vi,v in enumerate(V)]
    labels.extend({'kind':'gauge','k':k} for k in data['B'] if next(a for a in k if a!=Z)>Z)
    need(len(labels)==600 and sum(c['kind']=='gauge' for c in labels)==60,'fresh actual600 cut inventory differs')
    # Antipodal physical cuts are equal polynomials, including normalized rows.
    index={v:i for i,v in enumerate(V)}
    for si in range(9):
        need(RING[si+9]==index[tuple(-a for a in V[RING[si]])],'full18 ring lacks actual antipodal endpoint')
        need(all(a==tuple(-q for q in b) for a,b in zip(supports[si]['m'],supports[si+9]['m'])),'antipodal raw support differs')
    record={'receiving_rectangle_in_s_units':[str(a) for a in (u0,u1,v0,v1)],
            'receiver_raw_corners':[encode(r) for r in R],
            'actual_support_ring':RING,'all_original_receiver_gap_controls':len(gaps),
            'minimum_original_gap':min(gaps).encode(),'minimum_support_height':min(heights).encode(),
            'physical_receiver_controls_per_cut':4,'gauge_receiver_controls_per_cut':9,
            'source_controls_per_cut':10,'source_root_alpha':'1/22',
            'cut_inventory':{'actual_supports':18,'physical_antipodal_representatives':540,'sign_paired_actual_central_gauges':60},
            'whole_core_squared_radius':((39-24*phi)/484).encode(),'local_collar_radius':'1/53'}
    return {'R':R,'powers':powers,'norm_power':norm,'supports':supports,'cuts':labels,'record':record,'data':data}

def coefficients(cut,T,domain):
    if cut['kind']=='support':
        v=cut['v'];vs=[dot(v,c) for c in T];result=[]
        support=domain['supports'][cut['support']]
        for m,h in zip(support['m'],support['h']):
            a=dot(m,v);f=cross(v,m);ns=[dot(m,c) for c in T];fs=[dot(f,c) for c in T]
            result.extend(a-h-(a+h)*scalar(T[i],T[j])+ns[i]*vs[j]+ns[j]*vs[i]+fs[i]+fs[j] for i,j in PAIRS)
        return result
    k=cut['k'];L=[]
    for c in T:
        L.append([dot(r,k[1:])+k[0]*dot(r,c)+dot(cross(k[1:],r),c) for r in domain['powers']])
    norm=domain['norm_power'];tensors=[]
    for i,j in PAIRS:
        A,U,V,W=L[i];a,u,v,w=L[j]
        p={(0,0):A*a-norm[0,0],(1,0):A*u+U*a-norm[1,0],
           (0,1):A*v+V*a-norm[0,1],(2,0):U*u-norm[2,0],
           (0,2):V*v-norm[0,2],(1,1):A*w+W*a+U*v+V*u-norm[1,1],
           (2,1):U*w+W*u-norm[2,1],(1,2):V*w+W*v-norm[1,2],(2,2):W*w-norm[2,2]}
        tensors.append([sum((value*F(Q(comb(a,u)*comb(b,v),comb(2,u)*comb(2,v)))
                            for (u,v),value in p.items() if u<=a and v<=b),Z)
                        for a,b in product(range(3),repeat=2)])
    return [tensors[j][uv] for uv in range(9) for j in range(10)]

def literal(cut,c,r,domain):
    if cut['kind']=='gauge':
        actual=qmul(qmul((Z,*r),(O,*c)),cut['k'])[0]
        return actual*actual-dot(r,r)
    V=domain['data']['V'];m=raw(V,cut['support'],r);h=dot(m,V[RING[cut['support']]])
    c2=dot(c,c);cxv=cross(c,cut['v']);v=cut['v']
    rotated=tuple(((O-c2)*v[j]+2*c[j]*dot(c,v)+2*cxv[j])/(O+c2) for j in range(3))
    return (O+c2)*(dot(m,rotated)-h)

def independent_check(cut,T,values,domain):
    def source(r):
        at=[literal(cut,c,r,domain) for c in T]
        return [at[i] if i==j else 2*literal(cut,midpoint(T[i],T[j]),r,domain)-(at[i]+at[j])/2 for i,j in PAIRS]
    if cut['kind']=='support':exact=[a for r in domain['R'] for a in source(r)]
    else:
        r0,ru,rv,ruv=domain['powers']
        samples=[]
        for u,v in product((Z,O/2,O),repeat=2):
            r=tuple(r0[j]+u*ru[j]+v*rv[j]+u*v*ruv[j] for j in range(3))
            samples.append(source(r))
        def quad(a,b,c):return [a,2*b-(a+c)/2,c]
        exact=[None]*90
        for j in range(10):
            columns=[quad(*(samples[u*3+v][j] for u in range(3))) for v in range(3)]
            tensor=[quad(*(columns[v][u] for v in range(3))) for u in range(3)]
            for u,v in product(range(3),repeat=2):exact[(u*3+v)*10+j]=tensor[u][v]
    need(exact==values,'independent literal Hamilton/Cayley receiver/source polarization differs')
    return len(exact)

def structural(forest):
    need(not forest.get('pending'),'incomplete forest is not a certificate')
    rows=forest['internal_nodes']+forest['leaves'];entries={}
    for row in rows:
        ri,path=row['root'],row['path'];key=(ri,path)
        need(type(ri) is int and 0<=ri<108 and type(path) is str and set(path)<=set('01') and len(path)<=40,'malformed root or path')
        need(key not in entries,'duplicate source subdivision address');entries[key]=row
        if 'edge' in row:need(tuple(row['edge']) in EDGES,'not a literal source edge')
        else:need(type(row['cut']) is int and 0<=row['cut']<600 and row['kind']==('support' if row['cut']<540 else 'gauge'),'actual cut label interpretation differs')
    visited=set()
    def walk(ri,path):
        key=(ri,path);need(key in entries,'missing complete source root or closed child')
        need(key not in visited,'repeated source node');visited.add(key)
        if 'edge' in entries[key]:walk(ri,path+'0');walk(ri,path+'1')
    for ri in range(108):walk(ri,'')
    need(visited==set(entries),'orphan source node')
    need(len(forest['leaves'])==108+len(forest['internal_nodes']),'closed binary forest count differs')
    return entries

def semantic_controls(forest,domain):
    import copy
    tests=[]
    mutations=[('omit one entire closed source root',lambda f:[f.__setitem__(key,[x for x in f[key] if x['root']!=0]) for key in ['internal_nodes','leaves']]),
               ('omit a closed leaf child',lambda f:f['leaves'].pop()),
               ('duplicate subdivision address',lambda f:f['leaves'].append(copy.deepcopy(f['leaves'][0]))),
               ('misinterpret a physical cut as gauge',lambda f:f['leaves'][0].__setitem__('kind','gauge')),
               ('insert an orphan source node',lambda f:f['leaves'].append({'root':0,'path':'1'*40,'cut':0,'kind':'support'}))]
    for title,mutation in mutations:
        bad=copy.deepcopy(forest);mutation(bad)
        try:structural(bad)
        except ValueError as e:tests.append({'control':title,'rejected':str(e)});continue
        raise ValueError('damaged source forest accepted:'+title)
    r=tuple(sum((v[j] for v in domain['R']),Z)/4 for j in range(3));c=(-r[1],r[0],Z)
    c2=dot(c,c);V=domain['data']['V'];plane=c;other=cross(r,plane)
    projected={(dot(plane,v),dot(other,v)) for v in V};rotated=set()
    for v in V:
        w=tuple(((O-c2)*v[j]+2*c[j]*dot(c,v)+2*cross(c,v)[j])/(O+c2) for j in range(3))
        rotated.add((dot(plane,w),dot(other,w)))
    need(rotated==projected and c2>F(Q(1,53**2)),'true central equal shadow or outer-collar control differs')
    need(all(dot(n,c)<=domain['data']['height'] for n in domain['data']['normals']),'true central companion outside proper-body chart')
    need(all(literal(cut,c,r,domain)<=Z for cut in domain['cuts'][:540]),'real equal-shadow fit incorrectly rejected by a physical cut')
    kz=(Z,Z,Z,O);gauge={'kind':'gauge','k':kz}
    need(kz in domain['data']['B'] and literal(gauge,c,r,domain)>Z,'true central-body symmetry fails to remove nonzero equal-shadow representative')
    tests.append({'control':'drop all central gauges','rejected':'actual nonzero equal-shadow fit survives ALL physical rows in D but is outside the true closest-shadow fold'})
    tests.append({'control':'scalar-zero source in the closest proper-body chart','rejected':'actual four coordinate-unit binary lifts force all quaternion coordinates zero if q0=0'})
    return tests
