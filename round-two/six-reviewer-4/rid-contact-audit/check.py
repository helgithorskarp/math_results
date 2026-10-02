"""Independent physical-contact/dual/clipping audit of RID9156 by six-reviewer-4.
Only own previously published exact geometry is imported after byte checks.
No researcher executable, certificate or expected record is used here.
"""
import argparse,hashlib,importlib.util,itertools,json,sys
from fractions import Fraction as F
from pathlib import Path
HERE=Path(__file__).resolve().parent

def need(ok,msg):
    if not ok:raise ValueError(msg)

def absolute(x):return x if x>=0 else -x

def load():
    pin=json.loads((HERE/'DEPENDENCIES.json').read_text());d=(HERE/pin['directory']).resolve()
    for n,h in pin['sha256'].items():need(hashlib.sha256((d/n).read_bytes()).hexdigest()==h,'own source pin:'+n)
    need('field' not in sys.modules,'unexpected arithmetic module');sys.path.insert(0,str(d))
    sp=importlib.util.spec_from_file_location('independent_rid_geometry',d/'check.py');b=importlib.util.module_from_spec(sp);sp.loader.exec_module(b)
    need(Path(sys.modules['field'].__file__).resolve()==d/'field.py','own field origin');return b

def encode(x):
    if isinstance(x,(list,tuple)):return [encode(t) for t in x]
    if hasattr(x,'a'):return [str(F(x.a,x.d)),str(F(x.b,x.d))]
    if isinstance(x,F):return str(x)
    return x

def digest(x):return hashlib.sha256((json.dumps(x,sort_keys=True)+'\n').encode()).hexdigest()

def giftwrap(b,V,r):
    # Definition-level directed hull edges against ALL originals, no projected sorting.
    E=[]
    for i,j in itertools.permutations(range(60),2):
        m=b.fcross(b.sub(V[j],V[i]),r);h=b.fdot(m,V[i])
        if h>0 and all(b.fdot(m,v)<h for k,v in enumerate(V) if k not in (i,j)):E.append((i,j))
    need(len(E)==16,'literal all-original shadow boundary')
    nxt=dict(E);need(len(nxt)==16 and set(nxt)==set(nxt.values()),'simple directed boundary')
    cyc=[min(nxt)]
    while nxt[cyc[-1]]!=cyc[0]:need(nxt[cyc[-1]] not in cyc,'boundary loop');cyc.append(nxt[cyc[-1]])
    need(len(cyc)==16,'one complete shadow cycle');return cyc

def duals(b,rows):
    S,Z=b.S,b.Z;records=[];bases=[]
    for ids in itertools.combinations(range(16),3):
        A=tuple(rows[i] for i in ids);det=b.fdot(A[0],b.fcross(A[1],A[2]))
        if det!=0:bases.append((ids,b.inverse(b.transpose(A))))
    need(len(bases)==534,'independent torque bases')
    for j,sgn in itertools.product(range(3),(-1,1)):
        e=tuple(S(sgn if k==j else 0) for k in range(3));cand=[]
        for ids,inv in bases:
            w=b.act(inv,e)
            if min(w)>=0:cand.append((sum(w,Z),ids,w))
        need(cand,'coordinate has a nonnegative dual certificate');m,ids,w=min(cand)
        need(b.add(b.add(b.scale(w[0],rows[ids[0]]),b.scale(w[1],rows[ids[1]])),b.scale(w[2],rows[ids[2]]))==e,'dual exact equality')
        witness=None
        for m0,ids0,w0 in sorted(cand):
            if m0!=m:break
            p0=b.act(b.inverse(tuple(rows[i] for i in ids0)),(S(1),)*3)
            if all(b.fdot(f,p0)<=1 for f in rows):witness=(ids0,w0,p0);break
        need(witness is not None,'matching feasible primal extremizer')
        ids,w,p=witness
        need(sgn*p[j]==m and m>0 and m<28,'dual/primal optimum and bound')
        records.append({'coordinate':j,'sign':sgn,'row_indices':list(ids),'weights':encode(w),'optimum':encode(m),'attaining_point':encode(p)})
    return records,max(decode(b,x['optimum']) for x in records)

def decode(b,x):
    a,c=map(F,x);return b.q(a.numerator,a.denominator)+b.q(c.numerator,c.denominator)*b.S(0,1)

def clip(b,rows):
    # Start in the cube PROVED to contain P by the six duals; clip one halfspace.
    S=b.S;planes=[]
    for j,sgn in itertools.product(range(3),(-1,1)):planes.append((tuple(S(sgn if k==j else 0) for k in range(3)),S(28)))
    verts=set(itertools.product((S(-28),S(28)),repeat=3));counts=[len(verts)]
    for f in rows:
        active={v:{i for i,(a,h) in enumerate(planes) if b.fdot(a,v)==h} for v in verts}
        pair_edges={}
        for v,ids in active.items():
            for ij in itertools.combinations(sorted(ids),2):
                if b.fcross(planes[ij[0]][0],planes[ij[1]][0])!=(b.Z,)*3:pair_edges.setdefault(ij,[]).append(v)
        new={v for v in verts if b.fdot(f,v)<=1};edges=set()
        for ends in pair_edges.values():
            if len(ends)==1:continue
            need(len(ends)==2,'two endpoints for true polytope edge');edges.add(tuple(sorted(ends)))
        for a,c in edges:
            x,y=b.fdot(f,a)-1,b.fdot(f,c)-1
            if (x<0<y) or (y<0<x):new.add(b.add(a,b.scale(x/(x-y),b.sub(c,a))))
        verts=new;planes.append((f,S(1)));need(verts,'nonempty clipped polytope');counts.append(len(verts))
    need(len(verts)==20,'full clipped vertex count');need(all(all(b.fdot(f,v)<=1 for f in rows) for v in verts),'all final vertices feasible')
    return sorted(verts),counts

def gates(b,V,C,r0,corners):
    q,p,Z=b.q,b.P,b.Z;a=p**2;c=2+p;R2=7+8*p;Fmax=F(23,20);cmax=F(81,2000);ell=F(41,40)
    E={(sx*a,sy*c,Z) for sx,sy in itertools.product((-1,1),repeat=2)}
    need(E=={v for v in V if v[2]==0},'exact equatorial originals')
    need(all(b.fdot(v,v)==R2 for v in V),'equal radius')
    need(all(absolute(v[2])>=1 for v in V if v not in E),'nonequatorial axial heights')
    face_records=[]
    for j in range(2):
        face={v for v in V if v[j]==p**3};wanted=set()
        for ss,tt in itertools.product((-1,1),repeat=2):
            v=[Z,Z,b.S(tt)];v[j]=p**3;v[1-j]=b.S(ss);wanted.add(tuple(v))
        need(face==wanted and max(v[j] for v in V if v not in face)==c,'physical coordinate exposed face');face_records.append(encode(sorted(face)))
    raw=[]
    for r in corners:
        N=b.fdot(r,r);need(r[0]>0 and r[1]>0 and N-1<q(1,400),'convex box tilt')
        need(q(99,100)**2*N<1 and r[0]+r[1]<q(7,100),'box axial lower height')
        need(max(r[:2])<q(81,2000),'both coordinate bound')
        ratio=c*r[1]/(a*r[0]);need(q(40,41)<ratio<q(41,40),'weighted diagonal ratio')
        need(absolute(a*r[0]-c*r[1])<q(1,400) and a*r[0]+c*r[1]<q(53,250),'equatorial axial bounds')
        area=b.brightness(C,r);need(area<q(1171,20),'convex brightness bound')
        mm=p*r[0]-r[1];need(0<mm<p/12,'width parameter')
        raw.append({'raw':encode(r),'area':encode(area),'ratio':encode(ratio)})
    B=3*p**2;W=p+2
    widthends=[]
    for m in (Z,p/12):
        d=(p,-b.S(1),-m);need(max(b.fdot(d,v) for v in V)==B+p*m,'literal width support and attainability');widthends.append(encode(sorted(B+p*m-b.fdot(d,v) for v in V)))
    need(p*W-B*p/12>0,'monotone width');wm=4*(B+p*p/12)**2/(W+(p/12)**2);wl=(20+32*p)*(1-q(10,11664))
    need(wm<wl and 940+1520*p>q(583,10)**2,'filter area/width gates')
    need(q(99,100)*(1-q(9,2)*q(7,100))>q(3,5),'nonequatorial height gap')
    need(R2<20 and R2>q(22,5)**2 and p**3<q(17,4),'radius/coefficient gates')
    eps=q(11,20);sig=q(24,25)
    need(q(36,125)<eps**2 and 1-q(3,25)**2>sig**2,'matching distance and singular gates')
    need(2*a*sig>2*eps and 2*c*sig-2*a>2*eps,'unequal sides')
    need(4*eps*(a+c)+4*eps**2<4*a*c*sig,'label determinant')
    initial=F(1,8)+(F(11,20)+F(9,256)+F(9,484))/F(22,5)
    need(initial<F(4,15),'full initial frame bound')
    need((p**3-c)*q(99,100)-(p**3-1)*q(41,40)*q(81,2000)>0,'actual receiver support faces')
    need(1+cmax/F(199,100)<ell,'actual target transverse l1')
    first=ell/(1-F(9,2)*F(4,15)/F(19,10));need(first<3,'initial row confinement')
    steps=[(3,F(99,100),F(7,5)),(F(7,5),F(499,500),F(7,6)),(F(7,6),F(499,500),F(23,20))];factors=[]
    for prev,dmin,out in steps:
        tau=prev*cmax;need(1-tau*tau>dmin*dmin,'actual source positive diagonal');fac=ell/(1-F(17,4)*tau/(1+dmin));need(fac<out,'row bootstrap');factors.append(str(fac))
    need(Fmax<1+F(40,41),'source sign branch')
    du=F(3,20)*F(41,40)*F(1,20);need(du==F(123,16000),'tangent difference')
    U=F(3,50);zmin=F(99,100);dz=2*U/(2*zmin);A=2*U/(1+zmin)+U*U*dz/(1+zmin)**2
    need(Fmax/20<U and 1-U*U>zmin*zmin and A<F(1,16) and dz<F(1,16),'proper transport derivative')
    fullF=1+(A*A+dz*dz)/2;need(fullF<F(101,100)**2,'proper equal-singular-value bound')
    axial=F(1,400)+F(123,800)*F(53,250);need(axial<F(9,250) and R2-q(1,400)**2>q(22,5)**2,'matched minus endpoint')
    roll=(F(9,250)+F(9,2)*du/16)/F(22,5);need(roll<F(9,1000) and F(101,100)*du<F(1,125),'full roll and transport')
    need(F(17,1000)**2/(4-F(17,1000)**2)<F(1,117)**2,'derived Cayley Euclidean enclosure')
    cgap=F(1,28)-F(1,500)-F(17,624)
    normgap=2*cgap/(1+3*F(1,117)**2)
    need(cgap>F(1,160) and normgap>F(1,80),'uniform quantitative relative support violation')
    return {'corners':raw,'coordinate_faces':face_records,'all_width_endpoint_values':widthends,'width_margin':encode(wl-wm),'initial_frame_bound':str(initial),'initial_row_factor':str(first),'row_bootstrap_factors':factors,'tangent_distance_bound':str(du),'transport_A_coefficient':str(A),'roll_bound':str(roll),'cayley_euclidean_upper':'1/117','local_infinity_closed_radius':str(F(472,44625)),'polynomial_linear_margin':str(cgap),'normalized_relative_support_margin':str(normgap),'physical_support_violation_per_infinity_norm':'1/20'}

def nonmembership(b,V,G,corners):
    rec=[]
    for gi,g in enumerate(sorted(G)):
        for sg in (-1,1):
            R=[b.act(b.transpose(g),b.scale(b.S(sg),r)) for r in corners]
            for fam,up,slope in [('W',12,20),('P',20,2)]:
                for j in range(2):
                    k=1-j;tests=[min(-r[2] for r in R),min(-r[j] for r in R),min(up*r[j]-r[2] for r in R),min(slope*r[k]-r[j] for r in R),min(-slope*r[k]-r[j] for r in R)]
                    need(max(tests)>0,'whole box excluded by a single strict affine inequality');idx=max(range(5),key=lambda i:tests[i]);rec.append({'proper_map':gi,'sign':sg,'family':fam,'major':j,'false_requirement':idx,'margin':encode(tests[idx])})
    need(len(rec)==480,'complete signed family inventory');return rec

def verify():
    b=load();V=list(map(b.as_fields,b.originals()));V=[b.scale(b.q(1,2),v) for v in V];r=(b.q(1,25),(2+b.P)/125,b.S(1));delta=b.q(1,2500)
    corners=[b.add(r,(sx*delta,sy*delta,b.Z)) for sx,sy in itertools.product((-1,1),repeat=2)]
    C,hull=b.facets(b.originals());G=b.proper_group(V);cyc=giftwrap(b,V,r);contacts=[]
    for i,j in zip(cyc,cyc[1:]+cyc[:1]):
        m=b.fcross(b.sub(V[j],V[i]),r);h=b.fdot(m,V[i]);mn=b.scale(1/h,m)
        for k in (i,j):contacts.append((i,j,k,mn,b.fcross(V[k],mn)))
    rows=sorted({x[4] for x in contacts});need(len(rows)==16 and len(contacts)==32,'all endpoint torque rows');dual,M=duals(b,rows);vertices,clipcounts=clip(b,rows)
    need(max(absolute(t) for v in vertices for t in v)==M,'independent clipping/dual maximum')
    need(M==b.q(61689,3124)+b.q(60741,12496)*b.P,'original exact coercivity constant')
    errs=[];norms=[];cornergaps=[]
    for i,j,k,mn,f in contacts:
        e=b.sub(V[j],V[i]);m0=b.fcross(e,r);h0=b.fdot(m0,V[k]);mx=b.fcross(e,(b.S(1),b.Z,b.Z));my=b.fcross(e,(b.Z,b.S(1),b.Z));hx=b.fdot(mx,V[k]);hy=b.fdot(my,V[k]);hmin=h0-delta*(absolute(hx)+absolute(hy))
        need(hmin>0,'whole-box support denominator');fx=b.fcross(V[k],mx);fy=b.fcross(V[k],my)
        err=delta*sum((absolute(fx[t]-f[t]*hx)+absolute(fy[t]-f[t]*hy) for t in range(3)),b.Z)/hmin
        need(err<b.q(1,500),'whole-box torque l1 bound');errs.append(err)
    for cr in corners:
        for i,j in zip(cyc,cyc[1:]+cyc[:1]):
            m=b.fcross(b.sub(V[j],V[i]),cr);h=b.fdot(m,V[i]);need(h>0 and b.fdot(m,V[j])==h,'actual endpoint support')
            g=[h-b.fdot(m,v) for t,v in enumerate(V) if t not in (i,j)];need(min(g)>0,'strict whole-box horizon');cornergaps.append(min(g));n2=b.fdot(m,m)/(h*h);need(n2<b.q(1,16),'whole-box normal norm');norms.append(n2)
    prerequisites=gates(b,V,C,r,corners);membership=nonmembership(b,V,G,corners)
    # Independent Cayley polynomial identity on rational nonzero controls and zero.
    identitychecks=0;positive=0;gappose=tuple(b.q(x,200000) for x in (12,14,11));maxgap=b.Z
    for qq in [(b.Z,)*3,gappose]+[tuple(b.q(s,200) if j==k else b.Z for j in range(3)) for k,s in itertools.product(range(3),(-1,1))]:
        u2=b.fdot(qq,qq)
        for i,j,k,m,f in contacts:
            v=V[k];rv=b.add(v,b.scale(2/(1+u2),b.add(b.fcross(qq,v),b.fcross(qq,b.fcross(qq,v)))))
            polynomial=b.fdot(f,qq)+b.fdot(m,qq)*b.fdot(v,qq)-u2
            need(b.fdot(m,rv)-1==2*polynomial/(1+u2),'literal physical Cayley support identity');identitychecks+=1
            if qq==gappose:maxgap=max(maxgap,polynomial)
        if qq!=(b.Z,)*3:
            U=max(absolute(x) for x in qq);polys=[b.fdot(f,qq)+b.fdot(m,qq)*b.fdot(V[k],qq)-u2 for i,j,k,m,f in contacts];need(max(polys)>b.q(3533,546000)*U,'positive margin control');positive+=1
    need(maxgap>0,'original relaxation gap fails full shadow')
    return {'actual_agent':'six-reviewer-4','role':'independent mathematical reviewer','claim':'RID9156 whole receiving box all-source proof audit; quantitative physical support gap on local proper-motion chart','originals':encode(V),'physical_facets':hull['faces'],'facet_inventory_sha256':digest(hull),'proper_group_count':len(G),'center_raw':encode(r),'corner_raw':encode(corners),'cycle_original_indices':cyc,'contacts':[{'edge':[i,j],'original':k,'normal':encode(m),'torque':encode(f)} for i,j,k,m,f in contacts],'sorted_torque_rows':encode(rows),'dual_coordinate_certificates':dual,'exact_M':encode(M),'clipping_vertex_counts':clipcounts,'complete_polytope_vertices':encode(vertices),'whole_box_l1_errors':encode(errs),'maximum_l1_error':encode(max(errs)),'whole_box_maximum_normal_squared':encode(max(norms)),'whole_box_minimum_nonendpoint_margin':encode(min(cornergaps)),'continuum_gates':prerequisites,'signed_prior_cover_nonmembership':{'count':len(membership),'sha256':digest(membership),'minimum_strict_affine_margin':encode(min(decode(b,z['margin']) for z in membership))},'literal_cayley_identity_checks':identitychecks,'nonzero_margin_controls':positive,'prior_relaxation_pose_maximum_polynomial_violation':encode(maxgap)}

if __name__=='__main__':
    a=argparse.ArgumentParser();a.add_argument('--emit',action='store_true');args=a.parse_args();data=(json.dumps(verify(),indent=2,sort_keys=True)+'\n').encode()
    if not args.emit:need(data==(HERE/'expected.json').read_bytes(),'whole independent record differs')
    sys.stdout.buffer.write(data)
