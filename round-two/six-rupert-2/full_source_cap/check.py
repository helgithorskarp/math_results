#!/usr/bin/env python3
"""Exact replay of the full-SO3 J74 nonminimal receiving-cap certificate.

Standard library only. Numeric discovery and solver outputs are not imported.
Four complete closed quaternion cubes are checked, including h=0; every
terminal cube has a positive exact support cut or lies in a proved local
equality neighborhood. Geometry and continuum bridges are in PROOF.md.
"""
from pathlib import Path
from fractions import Fraction as F
from itertools import combinations, product
import argparse, copy, hashlib, importlib.util, json, sys

HERE=Path(__file__).resolve().parent
def require(ok,message):
    if not ok:raise ValueError(message)
def load_geometry():
    dep=json.loads((HERE/'DEPENDENCIES.json').read_text())
    base=(HERE/dep['relative_directory']).resolve()
    require(set(dep['sha256'])=={'q5.py','model.py'},'exact prerequisite source set')
    for name,digest in dep['sha256'].items():
        require(hashlib.sha256((base/name).read_bytes()).hexdigest()==digest,'pinned source fingerprint: '+name)
    require('q5' not in sys.modules,'unexpected preloaded field module')
    sys.path.insert(0,str(base))
    spec=importlib.util.spec_from_file_location('j74_original_model',base/'model.py')
    model=importlib.util.module_from_spec(spec);spec.loader.exec_module(model)
    import q5
    require(Path(q5.__file__).resolve()==base/'q5.py','verified arithmetic source imported')
    return model,q5
model,a=load_geometry()
Q=a.Q;V=model.VERTICES
ZERO=(Q(),Q(),Q())
IDENTITY=tuple(tuple(Q(int(i==j)) for j in range(3)) for i in range(3))
def field(x):
    require(isinstance(x,list) and len(x)==2 and all(isinstance(y,str) for y in x),'literal ordered-field scalar')
    return Q(F(x[0]),F(x[1]))
def enc(x):return [str(x.a),str(x.b)]
def vec(x):
    require(isinstance(x,list) and len(x)==3,'spatial literal vector')
    return tuple(field(y) for y in x)
def absolute(x):return x if x>=0 else -x
def matmul(A,B):return tuple(tuple(a.dot(row,col) for col in zip(*B)) for row in A)
def act(A,v):return tuple(a.dot(row,v) for row in A)
def matrix(x):
    require(isinstance(x,list) and len(x)==3,'three literal matrix rows')
    return tuple(vec(row) for row in x)
def smul(x,t):return Q(x.a*t,x.b*t)
def linear(xs,ts):
    return Q(sum((x.a*t for x,t in zip(xs,ts)),F()),sum((x.b*t for x,t in zip(xs,ts)),F()))
def canonical(x):return json.dumps(x,sort_keys=True,separators=(',',':')).encode()
def hull(vertices,u):
    basis=((Q(1),Q(),Q()),(Q(),Q(1),Q()),(Q(),Q(),Q(1)))
    e=next(a.cross(u,b) for b in basis if a.cross(u,b)!=ZERO);f=a.cross(u,e)
    points={}
    for i,v in enumerate(vertices):points.setdefault((a.dot(e,v),a.dot(f,v)),i)
    points=sorted(points.items())
    def side(items):
        chain=[]
        for p in items:
            while len(chain)>1:
                x,y=chain[-2][0],chain[-1][0];z=p[0]
                if (y[0]-x[0])*(z[1]-x[1])-(y[1]-x[1])*(z[0]-x[0])>0:break
                chain.pop()
            chain.append(p)
        return chain
    return [i for _,i in side(points)[:-1]+side(points[::-1])[:-1]]
def original_geometry():
    standard,caps,gyrated,built,axes=model.cupola_construction()
    require(len(V)==len(set(V))==60 and built==set(V),'all original cupola-constructed J74 vertices')
    require(len(standard)==60 and all(len(c)==5 for c in caps),'two five-original cap replacements')
    radius2=(11+4*Q(0,1))/4
    require(all(a.dot(v,v)==radius2 for v in V),'every original common radius')
    for i,j in ((0,7),(1,6),(2,5)):require(a.add(V[i],V[j])==ZERO,'actual antipodal originals')
    require(a.dot(V[0],a.cross(V[1],V[2]))!=0,'three independent antipodal pairs')
    s=Q(0,1);phi=(1+s)/2
    m=a.scale(1/(2*phi),(Q(1),-phi,-phi*phi))
    d=((-5+3*s)/8,(11-3*s)/8,Q(F(-1,4)))
    u=a.scale(Q(F(1,11)),a.add(m,a.scale(10,d)))
    require(u[2]<0 and a.dot(u,u)>0,'nonzero fixed raw receiver')
    cycle=hull(V,u)
    require(cycle==[16,0,36,28,10,11,47,55,27,7,43,31,13,12,48,56,20],
            'complete original receiving hull at t=10')
    N=[]
    for i,j in zip(cycle,cycle[1:]+cycle[:1]):
        n=a.cross(a.sub(V[j],V[i]),u);h=a.dot(n,V[i])
        require(h>0 and a.dot(n,u)==0,'positive original spatial support')
        require(a.dot(n,V[j])==h and all(a.dot(n,v)<=h for v in V),'all original receiving supports')
        N.append(a.scale(1/h,n))
    return u,cycle,N,radius2
def det2(n,m):return n[0]*m[1]-n[1]*m[0]
def force_circuits(N):
    circuits=[]
    for i,j in combinations(range(len(N)),2):
        if det2(N[i],N[j])!=0 or a.dot(N[i],N[j])>=0:continue
        k=next(k for k in range(2) if N[i][k]!=0)
        w=[absolute(N[j][k]),absolute(N[i][k])];total=sum(w,Q());w=[x/total for x in w]
        circuits.append(([i,j],w))
    for i,j,k in combinations(range(len(N)),3):
        w=[det2(N[j],N[k]),det2(N[k],N[i]),det2(N[i],N[j])]
        if all(x<0 for x in w):w=[-x for x in w]
        if not all(x>0 for x in w):continue
        total=sum(w,Q());circuits.append(([i,j,k],[x/total for x in w]))
    for indices,w in circuits:
        require(min(w)>0 and sum(w,Q())==1,'positive normalized force circuit')
        require(all(sum((weight*N[i][k] for i,weight in zip(indices,w)),Q())==0 for k in range(3)),
                'three literal force equilibrium components')
    require(len(circuits)==168,'deterministic circuit index inventory')
    return circuits
def rotation_form(n,p):
    z=a.dot(n,p);f=a.cross(p,n)
    A=[[Q() for j in range(4)] for i in range(4)];A[0][0]=z
    for j in range(3):A[0][j+1]=A[j+1][0]=f[j]
    for i in range(3):
        for j in range(3):A[i+1][j+1]=n[i]*p[j]+p[i]*n[j]-z*int(i==j)
    return A
def audit_rotation_form():
    """A second construction from the homogeneous three-dimensional matrix."""
    basis=((Q(1),Q(),Q()),(Q(),Q(1),Q()),(Q(),Q(),Q(1)))
    for n,p in ((V[0],V[1]),(V[16],V[20]),(basis[0],basis[2])):
        A=rotation_form(n,p);z=a.dot(n,p)
        require(A[0][0]==z,'homogeneous h-square coefficient')
        for i,e in enumerate(basis):
            image=a.sub(a.scale(2*p[i],e),p)
            require(A[i+1][i+1]==a.dot(n,image),'homogeneous vector-square coefficient')
            require(2*A[0][i+1]==2*a.dot(n,a.cross(e,p)),'homogeneous h-vector coefficient')
            for j in range(i+1,3):
                image=a.add(a.scale(p[j],e),a.scale(p[i],basis[j]))
                require(2*A[i+1][j+1]==2*a.dot(n,image),'homogeneous mixed-vector coefficient')
def proper(A):
    require(matmul(A,tuple(zip(*A)))==IDENTITY and a.dot(A[0],a.cross(A[1],A[2]))==1,'proper source motion')
def local_hypotheses(data,u,cycle,N,radius2):
    C=field(data['quadratic_constant']);gate=field(data['local_Cayley_Euclidean_gate']);hole=field(data['hole_Cayley_Euclidean_gate'])
    require(C==Q(F(5,4)) and gate==Q(F(1,15)) and hole==Q(F(4,75)),
            'fixed proved local and covering constants')
    require(C>Q(F(1,2)) and all(radius2*a.dot(n,n)<(2*C-1)*(2*C-1) for n in N),
            'global original-contact quadratic bound')
    Mn=tuple(tuple(IDENTITY[i][j]-2*u[i]*u[j]/a.dot(u,u) for j in range(3)) for i in range(3))
    Mx=((Q(-1),Q(),Q()),(Q(),Q(1),Q()),(Q(),Q(),Q(1)))
    require({act(Mx,v) for v in V}==set(V),'actual full-body x reflection')
    poses=[];locals_record=[]
    require(isinstance(data['poses'],list) and len(data['poses'])==6,'six proper base equality poses')
    for item in data['poses']:
        g=matrix(item['proper_matrix_rows']);proper(g);images=[act(g,v) for v in V]
        require(all(max(a.dot(n,p) for p in images)==1 for n in N),'full actual source support containment')
        matching=[]
        for j in cycle:
            ks=[k for k,p in enumerate(images) if a.cross(a.sub(p,V[j]),u)==ZERO]
            require(ks,'every original receiver corner has an actual source preimage');matching.append([j,ks])
        duals=item['coordinate_duals'];require(len(duals)==6,'six signed coordinate duals')
        seen=set();masses=[Q() for j in range(3)]
        for dual in duals:
            axis,sign=dual['axis'],dual['sign']
            require(type(axis) is int and axis in range(3) and type(sign) is int and sign in (-1,1),
                    'actual signed coordinate target')
            require((axis,sign) not in seen,'distinct signed coordinate dual');seen.add((axis,sign))
            contacts=dual['actual_contact_rows'];weights=[field(x) for x in dual['weights']]
            require(len(contacts)==len(weights)==5 and all(x>=0 for x in weights),'five nonnegative actual weights')
            torque=ZERO;force=ZERO
            for pair,w in zip(contacts,weights):
                require(isinstance(pair,list) and len(pair)==2 and all(type(x) is int for x in pair),'literal actual contact labels')
                i,k=pair;require(i in range(len(N)) and k in range(len(V)),'actual contact label range')
                n,p=N[i],images[k];require(a.dot(n,p)==1,'actual original source contact')
                torque=a.add(torque,a.scale(w,a.cross(p,n)));force=a.add(force,a.scale(w,n))
            require(force==ZERO and torque==tuple(Q(sign*int(j==axis)) for j in range(3)),
                    'all six exact torque and spatial force equations')
            mass=sum(weights,Q());masses[axis]=max(masses[axis],mass)
        factor2=C*C*sum((x*x for x in masses),Q())
        require(factor2*gate*gate<1,'strict Euclidean local rigidity absorption')
        companion=matmul(matmul(Mn,g),Mx);proper(companion)
        poses.extend((g,companion))
        locals_record.append({'proper_matrix_rows':item['proper_matrix_rows'],'corner_preimages':matching,
                    'coordinate_mass_maxima':[enc(x) for x in masses],
                    'squared_coercivity_factor':enc(factor2),'closed_radius_squared_absorption':enc(factor2*gate*gate)})
    require(len(set(poses))==12,'twelve distinct actual equal-shadow source poses')
    threshold=(3-hole*hole)/(1+hole*hole)
    holes=[]
    for g in poses:
        T=[[Q() for j in range(4)] for i in range(4)]
        for j in range(3):
            A=rotation_form(IDENTITY[j],g[j])
            for i in range(4):
                for k in range(4):T[i][k]+=A[i][k]
        for j in range(4):T[j][j]-=threshold
        holes.append(T)
    return holes,locals_record
def validate_partition(leaves):
    require(isinstance(leaves,list) and leaves,'nonempty full quaternion forest')
    roots=[[] for j in range(4)]
    for leaf in leaves:
        require(isinstance(leaf,list) and len(leaf)>=5,'literal terminal cube')
        chart,depth,code,kind=leaf[:4]
        require(all(type(x) is int for x in (chart,depth,code)) and chart in range(4)
                and 0<=depth<=60 and 0<=code<2**depth,'four full chart path ranges')
        require(kind in ('C','H'),'every leaf needs an actual cut or local pose')
        roots[chart].append((F(code,2**depth),F(code+1,2**depth)))
    for chart,intervals in enumerate(roots):
        end=F()
        for lo,hi in sorted(intervals):
            require(lo==end,'closed chart partition has a gap or overlap: '+str(chart));end=hi
        require(end==1,'complete closed cube for every quaternion component chart')
    return [len(x) for x in roots]
def box(depth,code):
    lo=[F(-1)]*3;hi=[F(1)]*3
    for level in range(depth):
        axis=level%3;mid=(lo[axis]+hi[axis])/2
        if (code>>(depth-level-1))&1:lo[axis]=mid
        else:hi[axis]=mid
    return lo,hi
PAIRS=((0,1),(0,2),(1,2))
CONTROL=list(product(range(3),repeat=3))
def coefficients(B,chart,lo,hi):
    other=[j for j in range(4) if j!=chart];width=[b-a for a,b in zip(lo,hi)]
    A=[[B[i][j] for j in other] for i in other];b=[2*B[chart][j] for j in other]
    constant=B[chart][chart]+linear(b,lo)
    constant+=linear([A[j][j] for j in range(3)],[x*x for x in lo])
    constant+=linear([2*A[j][k] for j,k in PAIRS],[lo[j]*lo[k] for j,k in PAIRS])
    first=[smul(b[j]+linear(A[j],[2*x for x in lo]),width[j]) for j in range(3)]
    diag=[smul(A[j][j],width[j]*width[j]) for j in range(3)]
    mixed=[smul(2*A[j][k],width[j]*width[k]) for j,k in PAIRS]
    result=[]
    for I in CONTROL:
        x=[F(i,2) for i in I]
        y=[F(i*(i-1),2) for i in I]
        z=[x[j]*x[k] for j,k in PAIRS]
        result.append(constant+linear(first,x)+linear(diag,y)+linear(mixed,z))
    return result
def verify(data,leaf_limit=None):
    require(set(data)=={'schema','agent','role','receiver_t','receiver_r','quadratic_constant','local_Cayley_Euclidean_gate',
                       'hole_Cayley_Euclidean_gate','receiving_projective_chord_radius','poses','leaves'},'complete certificate schema')
    require(data['schema']==1 and data['agent']=='six-rupert-2' and data['role']=='researcher','certificate author and schema')
    require(data['receiver_t']==10 and data['receiver_r']==0,'fixed receiving domain t=10,r=0')
    receiving_radius=field(data['receiving_projective_chord_radius'])
    require(receiving_radius>0,'positive stated receiving-cap radius')
    chart_counts=validate_partition(data['leaves'])
    u,cycle,N,radius2=original_geometry();circuits=force_circuits(N);audit_rotation_form()
    holes,local_record=local_hypotheses(data,u,cycle,N,radius2)
    cache={};hashes=hashlib.sha256();counts={'C':0,'H':0};minimum={};checked=0
    leaves=data['leaves'] if leaf_limit is None else data['leaves'][:leaf_limit]
    for index,leaf in enumerate(leaves):
        chart,depth,code,kind=leaf[:4];lo,hi=box(depth,code)
        if kind=='H':
            require(len(leaf)==5 and type(leaf[4]) is int and leaf[4] in range(12),'actual local-pose index')
            B=holes[leaf[4]]
        else:
            ci=leaf[4];require(type(ci) is int and ci in range(len(circuits)),'actual force circuit index')
            rows,w=circuits[ci];ks=leaf[5:]
            require(len(ks)==len(rows) and all(type(k) is int and k in range(60) for k in ks),'actual source original indices')
            key=(ci,*ks)
            if key not in cache:
                forms=[rotation_form(N[i],V[k]) for i,k in zip(rows,ks)]
                B=[[sum((weight*A[i][j] for weight,A in zip(w,forms)),Q())-int(i==j)
                    for j in range(4)] for i in range(4)]
                require(all(B[i][j]==B[j][i] for i in range(4) for j in range(4)),'literal symmetric cut matrix')
                cache[key]=B
            B=cache[key]
        values=coefficients(B,chart,lo,hi)
        require(len(values)==27 and min(values)>0,'strict whole-cube Bernstein sign at leaf '+str(index))
        minimum[kind]=min(minimum.get(kind,values[0]),min(values))
        hashes.update(canonical([leaf,[enc(x) for x in values]]));hashes.update(b'\n')
        counts[kind]+=1;checked+=1
    collar_record=None
    if checked==len(data['leaves']):
        collar_record=load_collar().finite_bounds(sys.modules[__name__],data,u,cycle,N,radius2,
                                                  minimum['C'],receiving_radius)
    return {'agent':'six-rupert-2','role':'researcher','arithmetic':'exact ordered Q(sqrt5), standard library only',
        'scope':('all-source closed fits on the stated closed nonminimal receiving cap; global J74 remains open'
                  if collar_record is not None else 'partial exact leaf replay; no full-source receiving cap certified'),
        'certificate_canonical_sha256':hashlib.sha256(canonical(data)).hexdigest(),
        'original_vertex_count':60,'original_radius_squared':enc(radius2),'raw_receiving_normal':[enc(x) for x in u],
        'complete_original_shadow_cycle':cycle,'original_support_comparisons':len(N)*60,
        'positive_force_circuit_count':len(circuits),'exact_local_dual_count':36,
        'exact_local_torque_and_spatial_force_equations':216,
        'local_pose_records':local_record,'distinct_actual_equal_shadow_poses':12,
        'closed_quaternion_chart_leaf_counts':chart_counts,'total_chart_leaves':len(data['leaves']),
        'verified_leaf_count':checked,'partial_leaf_replay':checked!=len(data['leaves']),
        'verified_leaf_kinds':counts,'strict_Bernstein_coefficient_checks':27*checked,
        'minimum_Bernstein_coefficients':{k:enc(v) for k,v in minimum.items()},
        'whole_verified_Bernstein_stream_sha256':hashes.hexdigest(),'unique_cut_matrices_used':len(cache),
        'maximum_closed_cube_depth':max(leaf[1] for leaf in data['leaves']),
        'receiving_collar_finite_bounds':collar_record}
def load_collar():
    name='j74_exact_cap_collar'
    if name not in sys.modules:
        spec=importlib.util.spec_from_file_location(name,HERE/'collar.py')
        module=importlib.util.module_from_spec(spec);sys.modules[name]=module;spec.loader.exec_module(module)
    return sys.modules[name]
def damaged_controls(data,record):
    variants=[]
    bad=copy.deepcopy(data);bad['leaves'].pop(0);variants.append(('missing closed cube',bad))
    bad=copy.deepcopy(data);bad['leaves']=[x for x in bad['leaves'] if x[0]!=3];variants.append(('omitted half-turn component chart',bad))
    bad=copy.deepcopy(data);bad['poses'][0]['coordinate_duals'][0]['weights'][0][0]=str(F(bad['poses'][0]['coordinate_duals'][0]['weights'][0][0])+F(1,10**6));variants.append(('positive weight with false equilibrium',bad))
    bad=copy.deepcopy(data);k=next(i for i,leaf in enumerate(bad['leaves']) if leaf[3]=='C');bad['leaves'][k][5:]=[0]*(len(bad['leaves'][k])-5);variants.append(('same original at every balanced support',bad))
    bad=copy.deepcopy(data);bad['poses'][0]['proper_matrix_rows'][0][0][0]=str(F(bad['poses'][0]['proper_matrix_rows'][0][0][0])+F(1,1000));variants.append(('improper source pose',bad))
    bad=copy.deepcopy(data);bad['hole_Cayley_Euclidean_gate']=['1/2','0'];variants.append(('unsupported source hole radius',bad))
    bad=copy.deepcopy(data);bad['receiver_t']=11;variants.append(('different receiving center',bad))
    passed=[]
    for label,bad in variants:
        try:verify(bad,k+1 if label=='same original at every balanced support' else 1)
        except (ValueError,StopIteration,ZeroDivisionError):passed.append(label)
        else:raise ValueError('damaged control was accepted: '+label)
    try:
        load_collar().finite_bounds(sys.modules[__name__],data,*original_geometry(),
                      field(record['minimum_Bernstein_coefficients']['C']),Q(F(1,100000)))
    except ValueError:passed.append('enlarged receiving cap without absorption')
    else:raise ValueError('unsupported enlarged receiving cap was accepted')
    return passed
def main():
    parser=argparse.ArgumentParser();parser.add_argument('--write-expected',action='store_true')
    parser.add_argument('--print-record',action='store_true');parser.add_argument('--profile-leaves',type=int)
    parser.add_argument('--self-test',action='store_true')
    args=parser.parse_args();data=json.loads((HERE/'certificate.json').read_text())
    result=verify(data,args.profile_leaves)
    if args.profile_leaves is not None:
        require(not args.write_expected,'partial proof replay cannot create an expected theorem record')
    elif args.write_expected:
        (HERE/'expected.json').write_text(json.dumps(result,indent=2,sort_keys=True)+'\n')
    else:
        require(result==json.loads((HERE/'expected.json').read_text()),'complete exact mathematical record mismatch')
    if args.self_test:
        require(not result['partial_leaf_replay'],'damage controls require a completed mathematical replay')
        result={**result,'damaged_controls_rejected':damaged_controls(data,result)}
    if args.print_record:print(json.dumps(result,indent=2,sort_keys=True))
    else:print(json.dumps({k:v for k,v in result.items() if k!='local_pose_records'},indent=2,sort_keys=True))
if __name__=='__main__':main()
