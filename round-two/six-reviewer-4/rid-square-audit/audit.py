"""Fresh physical RID reconstruction. No target executable/data imports."""
import argparse, hashlib, itertools, json
from pathlib import Path
from exact import E,F,PHI as p,ZERO as Z,ONE as O,dot,sub,cross,mv,mm,tr,det,ID,cayley,rodrigues,encode

def need(ok,why):
    if not ok: raise ValueError(why)
def polyadd(a,b): return [ (a[i]if i<len(a)else Z)+(b[i]if i<len(b)else Z)for i in range(max(len(a),len(b)))]
def polymul(a,b):
    v=[Z]*(len(a)+len(b)-1)
    for i,x in enumerate(a):
        for j,y in enumerate(b): v[i+j]=v[i+j]+x*y
    return v
def polyeval(a,z):
    out=Z
    for x in reversed(a):out=out*z+x
    return out
def vertices():
    seeds=((O,O,1+2*p),(1+p,p,2*p),(2+p,Z,1+p))
    vs=set()
    for seed in seeds:
        for signs in itertools.product((-1,1),repeat=3):
            v=tuple(t*k for t,k in zip(seed,signs))
            for c in range(3):vs.add(v[c:]+v[:c])
    return sorted(vs,key=lambda v:tuple(q.phi_key()for q in v))
def pi(v,x):return (v[0]-x*v[2],v[1])
def turn(a,b,c):return (b[0]-a[0])*(c[1]-a[1])-(b[1]-a[1])*(c[0]-a[0])
def hull(points):
    pts=sorted(set(points));chains=[]
    for seq in (pts,list(reversed(pts))):
        chain=[]
        for v in seq:
            while len(chain)>=2 and turn(chain[-2],chain[-1],v)<=0:chain.pop()
            chain.append(v)
        chains.append(chain[:-1])
    return chains[0]+chains[1]
def bernstein2(a,r):return [a[0],a[0]+a[1]*r/2,polyeval(a,r)]

def run(damage=None):
    vs=vertices();need(len(vs)==60,'60 distinct original vertices')
    need(all(tuple(-x for x in v)in vs for v in vs),'central symmetry')
    c=((4-3*p)/5,Z,(3-p)/5);R=cayley(c)
    if damage=='wrong_source':R=cayley(tuple(-x for x in c))
    need(mm(tr(R),R)==ID and det(R)==1,'proper physical Rstar')
    moved=[mv(R,v)for v in vs]
    for v,w in zip(vs,moved):need(w==rodrigues(c,v),'matrix / Rodrigues full point bridge')
    ell,s=2*p-3,2-p;mid=(ell+s)/2;h=1+2*p;U=(Z,O,Z);A=O+dot(c,c)
    need(A==(12-4*p)/5,'A factor')
    square={};squaregaps=[]
    for name,body,positive,negative in [('receiving',vs,[18,19,46,47],[12,13,40,41]),('moving',moved,[35,39,47,53],[6,12,20,24])]:
        if damage=='face_height':h=h+E(F(1,1000))
        for k,v in enumerate(body):
            for sign in (-1,1):
                gap=h-sign*v[1];need(gap>=0,'actual square support');squaregaps.append([name,k,sign,gap])
        need([i for i,v in enumerate(body)if v[1]==h]==positive,'positive face labels')
        need([i for i,v in enumerate(body)if v[1]==-h]==negative,'negative face labels')
        square[name]={'positive':positive,'negative':negative}
    u=((4*p-2)/5,Z,(1-2*p)/5);v=((1-2*p)/5,Z,(2-4*p)/5)
    need(dot(u,u)==1 and dot(v,v)==1 and dot(u,v)==0 and dot(U,u)==dot(U,v)==0,'orthonormal square frame')
    corners={tuple(h*U[i]+a*u[i]+b*v[i]for i in range(3))for a,b in itertools.product((-1,1),repeat=2)}
    need(corners=={moved[i]for i in square['moving']['positive']},'all literal moving square corners')
    for d in [(E(F(1,13)),E(F(-2,31)),E(F(1,19))),(Z,E(F(1,11)),Z)]:
        Rd=cayley(d);q=O+dot(d,d);off=d[0]*d[0]+d[2]*d[2]
        need(mv(Rd,U)[1]==O-2*off/q,'cos identity')
        need(sum((dot(U,mv(Rd,t))*dot(U,mv(Rd,t)) for t in (u,v)),Z)==4*off*(O+d[1]*d[1])/(q*q),'sin squared identity')
    cycle=[48,36,54,56,38,53,46,18,19,11,23,5,3,21,6,13,41,40]
    if damage=='missing_hull_edge':cycle.pop(2)
    if damage=='reversed_hull':cycle.reverse()
    endpoints=[ell,s];turns=[];gaps=[];normals=[];distinct=[];hulls=[]
    for x in [ell,mid,s]:
        need(hull([pi(v,x)for v in vs])==hull([pi(vs[i],x)for i in cycle]),'fresh 60-point hull completeness')
        hv=hull([pi(v,x)for v in vs]);hulls.append([x,hv])
        for w in moved:need(all(turn(hv[i],hv[(i+1)%len(hv)],pi(w,x))>=0 for i in range(len(hv))),'all moving points in independently reconstructed hull')
    for i,j,k in itertools.combinations(range(len(cycle)),3):
        vals=[turn(pi(vs[cycle[i]],x),pi(vs[cycle[j]],x),pi(vs[cycle[k]],x))for x in [ell,mid,s]]
        need(vals[0]>=0 and vals[2]>=0,'cyclic triple orientation')
        need(2*vals[1]==vals[0]+vals[2],'full affine turn bridge')
        turns.append([i,j,k,vals])
    for i,j in itertools.combinations(cycle,2):
        w=sub(vs[i],vs[j]);root=None
        if w[1]==0:
            if w[2]==0:need(w[0]!=0,'distinct throughout, constant')
            else:root=w[0]/w[2];need(root<ell or root>s,'distinct throughout, root outside')
        distinct.append([i,j,w,root])
    for a,b in zip(cycle,cycle[1:]+cycle[:1]):
        edge=sub(vs[b],vs[a]);ms=[cross(edge,(x,Z,O))for x in [ell,mid,s]]
        if damage=='wrong_normal':ms=[tuple(-v for v in m)for m in ms]
        # Entire affine normal cannot vanish: its third coordinate is -x*m_x.
        if ms[0][0]!=0:why='fixed nonzero first component'
        else:
            need(ms[0][2]==0 and ms[2][2]==0,'normal first-third relation')
            if ms[0][1]==ms[2][1]:need(ms[0][1]!=0,'fixed nonzero y');why='fixed nonzero second component'
            else:need(ms[0][1]*ms[2][1]>0,'no y zero across segment');why='same strict endpoint second signs'
        hs=[dot(m,vs[a])for m in ms];need(hs[0]>0 and hs[2]>0,'positive receiving heights')
        normals.append([a,b,edge,ms,hs,why])
        for name,body in [('receiving',vs),('moving',moved)]:
            for j,w in enumerate(body):
                vals=[hs[k]-dot(ms[k],w)for k in range(3)]
                need(vals[0]>=0 and vals[2]>=0,'all physical endpoint supports')
                need(2*vals[1]==vals[0]+vals[2],'full affine support bridge')
                gaps.append([a,b,name,j,vals])
    # Reconstruct every polynomial from the physical coordinate definitions.
    rows=[];grid=[];selected={}
    for edge_index,(a,b)in enumerate([(48,36),(36,54)]):
        edge=sub(vs[b],vs[a]);m0=cross(edge,(Z,Z,O));mx=cross(edge,(O,Z,Z))
        H0,Hx=dot(m0,vs[a]),dot(mx,vs[a])
        for j,w in enumerate(moved):
            # Numerator of R(zU) acting on w: w+2z(U cross w)+z²(-w+2U(U dot w)).
            wcoef=[w,tuple(2*q for q in cross(U,w)),tuple(-w[i]+2*U[i]*w[1]for i in range(3))]
            aa=[A*(dot(mx,wcoef[k])-(Hx if k in (0,2)else Z))for k in range(3)]
            bb=[A*(dot(m0,wcoef[k])-(H0 if k in (0,2)else Z))for k in range(3)]
            rows.append([edge_index,j,aa,bb])
            for x,z in itertools.product(endpoints,[E(F(-1,11)),Z,E(F(1,11))]):
                actual=A*(O+z*z)*(dot(cross(edge,(x,Z,O)),mv(cayley((Z,z,Z)),w))-dot(cross(edge,(x,Z,O)),vs[a]))
                symbolic=polyeval(aa,z)*x+polyeval(bb,z)
                need(actual==symbolic,'720 full physical polynomial comparisons');grid.append([edge_index,j,x,z,actual])
            if (edge_index,j)in [(0,32),(0,40),(1,36)]:selected[(edge_index,j)]=(aa,bb)
    a32,b32=selected[(0,32)];a40,b40=selected[(0,40)];a96,b96=selected[(1,36)]
    k=8*(2*p-1)/5
    need(a32==[Z,2*k,-k]and b32==[Z,-k,-2*k],'row32 full factor')
    need(a40==[(8-8*p)/5,(8+16*p)/5,(24-16*p)/5] and b40==[(40-24*p)/5,(16-8*p)/5,(32-40*p)/5],'all written row40 coefficients')
    need(a96==[Z,(24+32*p)/5,(8-16*p)/5] and b96==[Z,(8-16*p)/5,(-24-32*p)/5],'all written row96 coefficients')
    determinant=polyadd(polymul(b40,a96),[-v for v in polymul(b96,a40)])
    if damage=='wrong_determinant':determinant[2]=determinant[2]+O
    need(determinant==[Z,Z,64*(3-p)/5,Z,64*(3-p)/5],'full elimination determinant')
    need(cross(cross(sub(vs[36],vs[48]),(ell,Z,O)),U)==(ell,Z,O),'translation full rank identity')
    need(a32[0]*ell+b32[0]==0,'persistent moving support')
    rho=(2*p-3)/(4-p);need(E(F(1,11))<rho<E(F(1,10)),'critical radius exact bracket');radii={}
    for name,r in [('author',E(F(1,12))),('larger',E(F(1,11))),('critical',rho)]:
        if damage=='unsupported_radius'and name=='larger':r=E(F(1,8))
        bracket=[2*x-1-(x+2)*z for x,z in itertools.product(endpoints,[-r,r])]
        need(1-h*h*r*r>0,'square transverse cusp margin')
        if name!='critical':need(max(bracket)<0,'closed radius row32 strict bracket')
        else:need(max(bracket)==0 and 2*s-1+(s+2)*r==0,'critical corner zero')
        b40controls=bernstein2(a40,r);b96controls=[a96[1],a96[1]+a96[2]*r]
        need(all(v<0 for v in b40controls),'a40 whole sign')
        need(all(v>0 for v in b96controls),'a96 divided z whole sign')
        radii[name]=dict(radius=r,square_margin=1-h*h*r*r,bracket=bracket,a40_bernstein=b40controls,a96_over_z_bernstein=b96controls)
    # At the sole critical negative-axis corner, test ALL actual supports.
    z=-rho;x=s
    if damage=='wrong_boundary_pose':z=rho
    rot=cayley((Z,z,Z));critical=[]
    for a,b in zip(cycle,cycle[1:]+cycle[:1]):
        m=cross(sub(vs[b],vs[a]),(x,Z,O));H=dot(m,vs[a])
        for j,w in enumerate(moved):critical.append([a,b,j,H-dot(m,mv(rot,w))])
    critical_fits=all(g[-1]>=0 for g in critical)
    need(critical_fits,'all actual critical corner supports nonnegative')
    Q=mm(rot,R);rr=(s,Z,O);rn=dot(rr,rr)
    Hr=tuple(tuple(2*rr[i]*rr[j]/rn-ID[i][j]for j in range(3))for i in range(3))
    if damage=='improper_symmetry':Hr=tuple(tuple(-v for v in row)for row in Hr)
    need(mm(tr(Hr),Hr)==ID and det(Hr)==1,'proper receiver halfturn')
    vset=set(vs)
    right=mm(tr(R),Q);halfturn_right=mm(mm(tr(R),Hr),Q)
    in_right={mv(right,v)for v in vs}==vset
    in_halfturn_right={mv(halfturn_right,v)for v in vs}==vset
    gs=tuple(tuple(v/2 for v in row)for row in [(-p,1-p,O),(1-p,-O,-p),(O,-p,p-1)])
    need(halfturn_right==gs and mm(tr(gs),gs)==ID and det(gs)==1,'explicit actual proper body halfturn')
    permutation=[vs.index(mv(gs,v))for v in vs]
    need(sorted(permutation)==list(range(60)),'full literal 60 point body permutation')
    need(mm(mm(Hr,R),gs)==Q,'all nine companion identity entries')
    need(dot(cross(sub(vs[36],vs[48]),rr),mv(Q,vs[32]))==dot(cross(sub(vs[36],vs[48]),rr),vs[48]),'critical opposite support closes original translation')
    if damage=='translation_nonzero':
        t=(O,Z,-s);m=cross(sub(vs[36],vs[48]),rr)
        need(dot(m,tuple(mv(Q,vs[32])[i]+t[i]for i in range(3)))<=dot(m,vs[48]),'nonzero original planar translation violates support')
    if damage=='bad_scale':need(E(F(1001,1000))*h<=h,'original scale enlargement violates paired square')
    ch=hull([pi(mv(Q,v),s)for v in vs]);rh=hull([pi(v,s)for v in vs])
    need(all(turn(rh[i],rh[(i+1)%len(rh)],w)>=0 for i in range(len(rh))for w in ch),'independent critical hull containment')
    critical_trace=sum(rot[i][i]for i in range(3));need(critical_trace==(3-rho*rho)/(O+rho*rho),'critical physical gate trace')
    record=dict(vertices=vs,physical_Rstar=R,moving_vertices=moved,squares=square,square_gaps=squaregaps,square_frame=[U,u,v],continuum_turns=turns,distinct=distinct,continuum_supports=gaps,continuous_normals=normals,independent_hulls=hulls,width_polynomials=rows,full_width_grid=grid,determinant=determinant,radii=radii,critical_corner=dict(x=x,z=z,all1080_support_gaps=critical,fits=critical_fits,physical_Q=Q,original_t=[Z,Z,Z],original_lambda=1,trace=critical_trace,right_body_candidate=right,halfturn_right_body_candidate=halfturn_right,actual_body_permutation=permutation,in_RstarG=in_right,in_HrRstarG=in_halfturn_right,moving_hull=ch,receiving_hull=rh))
    return encode(record)

def digest(record):return hashlib.sha256(json.dumps(record,sort_keys=True,separators=(',',':')).encode()).hexdigest()
def summary(record):
    return dict(actual_agent='six-reviewer-4',role='independent mathematical reviewer',math_sha256=digest(record),vertices=len(record['vertices']),cyclic_triples=len(record['continuum_turns']),distinct_pairs=len(record['distinct']),support_rows=len(record['continuum_supports']),endpoint_support_values=2*len(record['continuum_supports']),width_polynomials=len(record['width_polynomials']),physical_grid_comparisons=len(record['full_width_grid']),radii=record['radii'],critical_corner_fits=record['critical_corner']['fits'])
if __name__=='__main__':
    ap=argparse.ArgumentParser();ap.add_argument('--record');ap.add_argument('--damage');args=ap.parse_args();record=run(args.damage)
    if args.record:Path(args.record).write_text(json.dumps(record,sort_keys=True,indent=2)+'\n')
    print(json.dumps(summary(record),sort_keys=True,indent=2))
