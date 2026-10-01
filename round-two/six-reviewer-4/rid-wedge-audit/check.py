"""Independent original-vertex RID wedge audit by six-reviewer-4.

Only this reviewer's integer-pair Q(sqrt5) arithmetic is reused. No author
module or expected record is read. Complete hull/group/polar enumeration;
analytic continuum implications are proved in REVIEW.md.
"""
import argparse
from collections import Counter
from fractions import Fraction
from itertools import combinations, permutations, product
import json
from pathlib import Path
from field import S, need, plus, minus, times, sign, cross, dot, vsub, vscale, zero, axis, as_fields, fdot, fcross

HERE = Path(__file__).resolve().parent
P = S(1, 1, 2)
Z = S()

def q(a, b=1):
    return S(a, 0, b)

def absolute(x):
    return x if x >= 0 else -x

def add(a, b):
    return tuple(x+y for x,y in zip(a,b))

def sub(a, b):
    return tuple(x-y for x,y in zip(a,b))

def scale(t, a):
    return tuple(t*x for x in a)

def act(a, v):
    return tuple(fdot(row,v) for row in a)

def transpose(a):
    return tuple(zip(*a))

def mmul(a,b):
    return tuple(tuple(fdot(row,col) for col in zip(*b)) for row in a)

def inverse(a):
    rows=[list(row)+[S(i==j) for j in range(3)] for i,row in enumerate(a)]
    for j in range(3):
        k=next(i for i in range(j,3) if rows[i][j]!=0)
        rows[j],rows[k]=rows[k],rows[j]
        t=rows[j][j];rows[j]=[x/t for x in rows[j]]
        for i in range(3):
            if i!=j:
                t=rows[i][j];rows[i]=[x-t*y for x,y in zip(rows[i],rows[j])]
    return tuple(tuple(row[3:]) for row in rows)

def originals():
    v=set()
    for base in [((2,0),(2,0),(4,2)),((3,1),(1,1),(2,2)),((5,1),(0,0),(3,1))]:
        for ss in product((-1,1),repeat=3):
            r=tuple((s*a,s*b) for s,(a,b) in zip(ss,base))
            for k in range(3):v.add(r[k:]+r[:k])
    out=sorted(v)
    need(len(out)==60 and all(vscale(-1,r) in v for r in v),'60 antipodal originals')
    need(all(dot(r,r)==(44,16) for r in out),'edge-two squared radius')
    return out

def facets(v):
    # All triples; rejection needs two strict sides, independent of origin height.
    faces=set();accepted=0
    for i,j,k in combinations(range(len(v)),3):
        d=cross(vsub(v[j],v[i]),vsub(v[k],v[i]));need(not zero(d),'sphere triples noncollinear')
        h=dot(d,v[i]);orientation=0;face=[]
        for r,w in enumerate(v):
            s=sign(minus(dot(d,w),h))
            if s==0:face.append(r)
            elif orientation==0:orientation=s
            elif s!=orientation:break
        else:
            need(orientation!=0,'full dimension');faces.add(tuple(face));accepted+=1
    cycles=[];vectors=[];edges=Counter()
    for face in sorted(faces):
        adj={i:[j for j in face if i!=j and dot(vsub(v[j],v[i]),vsub(v[j],v[i]))==(16,0)] for i in face}
        need(all(len(x)==2 for x in adj.values()),'regular face boundary')
        cyc=[face[0],adj[face[0]][0]]
        while len(cyc)<len(face):
            nxt,=[i for i in adj[cyc[-1]] if i!=cyc[-2]]
            need(nxt not in cyc,'simple face boundary');cyc.append(nxt)
        need(cyc[0] in adj[cyc[-1]],'closed face')
        r=((0,0),)*3
        for i,j in zip(cyc,cyc[1:]+cyc[:1]):r=tuple(plus(a,b) for a,b in zip(r,cross(v[i],v[j])))
        if sign(dot(r,v[cyc[0]]))<0:cyc.reverse();r=vscale(-1,r)
        need(sign(dot(r,v[cyc[0]]))>0,'positive physical face height')
        for i,j in zip(cyc,cyc[1:]+cyc[:1]):
            for k in face:
                if k not in (i,j):need(sign(dot(r,cross(vsub(v[j],v[i]),vsub(v[k],v[i]))))>0,'all convex turns')
            edges[tuple(sorted((i,j)))]+=1
        need(all(sign(minus(dot(r,w),dot(r,v[cyc[0]])))<=0 for w in v),'all actual support sides')
        cycles.append(cyc);vectors.append(r) # physical vector r/8, originals v/2
    need(Counter(map(len,faces))=={3:20,4:30,5:12} and accepted==260,'complete hull census')
    need(len(edges)==120 and set(edges.values())=={2},'closed polyhedral boundary')
    need(len(set(vectors))==62 and all(vscale(-1,r) in vectors for r in vectors),'opposite physical facets')
    C=[as_fields(r,8) for r in vectors if sign(next(x for x in r if x!=(0,0)))>0]
    need(len(C)==31,'paired Cauchy vectors')
    return C,{'triples':34220,'supporting_triples':accepted,'faces':len(faces),'edges':len(edges),
              'facet_indices':sorted([sorted(x) for x in cycles]),'physical_paired_area_vectors':[[str(x) for x in c] for c in sorted(C)]}

def brightness(C,r):
    return sum((absolute(fdot(c,r)) for c in C),Z)

def projective(r):
    t=next(x for x in r if x!=0)
    return tuple(x/t for x in r)

def shadow(V,r):
    i=next(i for i in range(3) if r[i]!=0)
    e=tuple(S(k==(i+1)%3) for k in range(3))
    u=fcross(r,e);w=fcross(r,u)
    pts=sorted({(fdot(u,v),fdot(w,v)) for v in V})
    def turn(a,b,c):return (b[0]-a[0])*(c[1]-a[1])-(b[1]-a[1])*(c[0]-a[0])
    lo=[];hi=[]
    for chain,seq in [(lo,pts),(hi,reversed(pts))]:
        for p in seq:
            while len(chain)>1 and turn(chain[-2],chain[-1],p)<=0:chain.pop()
            chain.append(p)
    h=lo[:-1]+hi[:-1]
    shoelace=sum((a[0]*b[1]-a[1]*b[0] for a,b in zip(h,h[1:]+h[:1])),Z)
    return shoelace**2/(4*fdot(u,u)*fdot(w,w)),len(h)

def proper_group(V):
    # Every proper symmetry maps this labelled edge to one of 240 oriented edges.
    a=V[0];b=next(w for w in V if fdot(sub(w,a),sub(w,a))==4)
    ref=transpose((a,b,fcross(a,b)));inv=inverse(ref)
    G=[];candidates=0;I=tuple(tuple(S(i==j) for j in range(3)) for i in range(3));points=set(V)
    for x in V:
        for y in V:
            if fdot(x,y)!=fdot(a,b):continue
            candidates+=1;g=mmul(transpose((x,y,fcross(x,y))),inv)
            need(mmul(g,transpose(g))==I and fdot(g[0],fcross(g[1],g[2]))==1,'proper edge-frame map')
            if {act(g,v) for v in V}==points:G.append(g)
    need(candidates==240 and len(set(G))==60,'complete proper body group')
    need(all(mmul(a,b) in G for a in G for b in G),'proper group closure')
    need(tuple(((-S(1),Z,Z),(Z,-S(1),Z),(Z,Z,S(1)))) in G,'label-preserving half-turn')
    return G

def tangent_inradius(C,r):
    D=[c for c in C if fdot(c,r)==0]
    values=[]
    for c in D:
        t=fcross(r,c);need(fdot(t,t)>0,'tangent facet ray')
        values.append(sum((absolute(fdot(d,t)) for d in D),Z)**2/fdot(t,t))
    return min(values),D

def polar_data(C,V,G):
    rays=sorted({projective(fcross(c,d)) for c,d in combinations(C,2) if fcross(c,d)!=(Z,Z,Z)})
    need(len(rays)==121,'complete area-polar axes')
    records=[];spectrum=Counter();checks=0
    for r in rays:
        value=brightness(C,r)**2/fdot(r,r);spectrum[value]+=1
        physical,n=shadow(V,r);need(value==physical,'whole-original area at each polar axis');checks+=1
        records.append({'raw_ray':[str(x) for x in r],'squared_area':str(value),'shadow_corners':n})
    A0=12+28*P;A1sq=940+1520*P
    need(sorted(spectrum.values())==[6,10,15,30,30,30] and min(spectrum)==A0**2,'full polar spectrum')
    low={r for r in rays if brightness(C,r)**2/fdot(r,r)==A0**2}
    second={r for r in rays if brightness(C,r)**2/fdot(r,r)==A1sq}
    ez=(Z,Z,S(1));w=(Z,P,S(1))
    need(low=={projective(act(g,ez)) for g in G} and second=={projective(act(g,w)) for g in G},'two complete low-area proper orbits')
    rho0,D0=tangent_inradius(C,ez);rho5,D5=tangent_inradius(C,w)
    need(rho0==(288+464*P)/5 and rho5==48+64*P,'actual tangent inradii')
    for r,D,expected in [(ez,D0,A0),(w,D5,brightness(C,w))]:
        non=(Z,Z,Z)
        for c in C:
            if c not in D:non=add(non,scale(S(1) if fdot(c,r)>0 else S(-1),c))
        need(non==scale(expected/fdot(r,r),r),'global signed area lower-bound axis')
    return {'all_axes':records,'spectrum':[[str(k),v] for k,v in sorted(spectrum.items())],
            'direct_hull_comparisons':checks,'twofold_tangent_inradius_squared':str(rho0),
            'fivefold_tangent_inradius_squared':str(rho5)},rho0,rho5

def width_filter(C,V,rho0,rho5):
    w=(Z,P,S(1));W2=fdot(w,w)
    heights=[fdot(v,w)**2/W2 for v in V];p2=min(heights)
    contacts=[v for v,h in zip(V,heights) if h==p2]
    need(len(contacts)==10 and p2==(7-4*P)/5,'all fivefold contacts')
    # Complete edge loop, definition-level positive sides of all contact points.
    edges=[];gates=[]
    for a,b in permutations(contacts,2):
        if all(fdot(w,fcross(sub(b,a),sub(c,a)))>0 for c in contacts if c not in (a,b)):
            edges.append((a,b))
    need(len(edges)==10 and all(sum(a==v for a,b in edges)==1 for v in contacts),'complete directed contact boundary')
    for a,b in edges:
        M=scale(q(1,2),add(a,b));H=scale(q(1,2),sub(b,a))
        need(fdot(w,M)==0 and fdot(M,M)==P**6 and fdot(M,H)==0 and fdot(H,H)==2,'equatorial edge-midpoint identities')
        need(fdot(w,H)**2/W2==p2 and 2-p2==(3+4*P)/5,'axial/tangent halfedge identities')
        for c in contacts:
            if c not in (a,b):
                L=fcross(sub(b,a),sub(c,a));gate=fdot(w,L)**2/(W2*fdot(L,L));gates.append(gate)
    need(len(gates)==80 and min(gates)>q(1,900),'entire fivefold 1/30 cap determinants')
    need(p2<q(1,9) and 2-p2<q(49,25),'positive root halfedge bounds')
    need(2-(q(1,3)+q(7,5)/30)**2>q(9,5),'positive projected-edge denominator')
    # Global polar source elimination, eta=1/4 is all the wedge theorem needs.
    T=q(703,12);A0=12+28*P;A1sq=940+1520*P;A2sq=960+1536*P
    need(A1sq>58**2 and A1sq<q(175,3)**2 and T*T<A2sq,'global polar low-level cutoff')
    need(q(1,2)/58<q(1,100),'fivefold initial chord <1/10')
    need(rho5>144 and A1sq<59**2 and q(399,400)**2<1-q(1,10)**2/4,'fivefold tangent growth hypotheses')
    need(12*q(399,400)-q(59,20)>9 and q(1,36)<q(1,30),'fivefold chord <eta/9 enables width')
    r=q(3,25);rmax=1-A0**2/T**2
    need(r*r<rmax<rho0/(A0**2+rho0),'whole twofold monotone source interval')
    Q=T*T-A0**2*(1-r*r)-rho0*r*r
    need(Q>0 and 4*A0**2*rho0*r*r*(1-r*r)>Q*Q,'positive-branch area cutoff at 3/25')
    need(r*r<q(1,8)**2*(1-q(1,8)**2/4),'source chord <1/8')
    return {'fivefold_contacts':[[str(x) for x in v] for v in sorted(contacts)],
            'oriented_contact_edges':[[contacts.index(a),contacts.index(b)] for a,b in edges],
            'boundary_determinants':80,'minimum_squared_normalized_determinant':str(min(gates)),
            'source_tangent_upper':'3/25','source_chord_upper':'1/8','proof':'REVIEW.md: full-source filter, eta=1/4 only'}

def wedge_gates(C,V,slope=q(1,20)):
    a=P**2;b=P**3;c=2+P;R2=7+8*P;A0=12+28*P;U=q(1,12)
    E={v for v in V if v[2]==0};need(E=={(sx*a,sy*c,Z) for sx,sy in product((-1,1),repeat=2)},'original equatorial labels')
    need(min(absolute(v[2]) for v in V if v not in E)==1 and max(absolute(x) for v in V for x in v)==b,'actual nonequatorial coordinate bounds')
    records=[]
    for j,H in enumerate((4+8*P,8+4*P)):
        k=1-j;D=[v for v in C if v[2]==0];mix=[v for v in D if v[j]!=0];pure=[v for v in D if v[j]==0]
        signed=(Z,Z,Z)
        for v in mix:signed=add(signed,scale(S(1) if v[j]>0 else S(-1),v))
        need(signed[j]==H and signed[k]==signed[2]==0 and sum((absolute(v[k]) for v in pure),Z)==4,'global lower bound uses actual tangent vectors')
        need(all(absolute(v[j])>slope*absolute(v[k]) for v in mix),'whole wedge mixed signs')
        nonzero=[]
        for s,t in [(Z,Z),(U,U*slope),(U,-U*slope)]:
            r=[Z,Z,S(1)];r[j]=s;r[k]=t
            for v in C:
                if v[2]!=0:nonzero.append(fdot(v,r)*(S(1) if v[2]>0 else S(-1)))
        need(len(nonzero)==75 and min(nonzero)>0,'whole triangle nonzero area signs')
        norm2=1+U*U*(1+slope*slope)
        need(q(99,100)**2*norm2<1 and U*U*(1+slope*slope)<q(1,11)**2,'receiver z and chord')
        area2=(A0+H*U+4*U*slope)**2/norm2
        need(area2<q(1171,20)**2 and 940+1520*P>q(583,10)**2,'entire receiver area below A1+1/4')
        need(H-U*(A0+4*U*slope)>0 and 4-U*slope*(A0+H*U)>0,'whole raw rectangle area monotonicity')
        mmax=P*U if j==0 else U
        for m in [Z,P*U]:
            d=(P,S(1),-m);sup=3*P**2+P*m
            need(max(fdot(v,d) for v in V)==sup and fdot((2*P,P**2,-P),d)==sup,'whole affine width supports and witness')
        need(P+2-3*P*(P*U)>0 and P-slope>0 and 1-P*slope>0,'all directional width branches')
        width2=4*(3*P**2+P*mmax)**2/(P+2+mmax*mmax);limit=(20+32*P)*(1-q(10,11664))
        need(width2<limit,'minimum receiving width upper bound for full source filter')
        # New bounds are checked independently of the author output, including kink.
        eps=q(11,20);sing=q(24,25);frame=q(4,15);source=q(3,25)
        height=q(99,100)*(1-q(9,2)*U*(1+slope))
        need(height>q(3,5) and R2<20 and q(36,125)<eps*eps<q(9,25),'matching radial separation')
        need(1-source*source>sing*sing and q(99,100)>sing,'both equatorial singular values')
        need(2*a*sing>2*eps and 2*c*sing-2*a>2*eps,'short-side separation')
        need(4*eps*(a+c)+4*eps*eps<4*a*c*sing,'all triple orientation determinants')
        roll=(eps+q(9,256)+q(9,484))/q(22,5)
        need(R2>q(22,5)**2 and R2<q(9,2)**2 and q(1,8)+roll<frame,'arbitrary proper roll localized')
        need(1-frame*frame/2>q(9,10) and 1+U/(1+q(99,100))<q(21,20),'actual minor row budgets')
        face={v for v in V if v[k]==b};others=[i for i in range(3) if i!=k]
        need(len(face)==4 and max(v[k] for v in V if v not in face)==c,'four exposed originals and next layer')
        need({(v[others[0]],v[others[1]]) for v in face}==set(product((-S(1),S(1)),repeat=2)),'independent support signs')
        l1=q(21,20)*U*slope
        facegap=(b-c)*q(99,100)-(b-1)*l1;need(facegap>0,'whole actual target support face persists')
        kappa=q(21,20)/(1-q(9,2)*frame/q(19,10));need(kappa==q(399,140)<3,'strict minor-source factor')
        minor=3*U*slope
        need(1-source*source-minor*minor>sing*sing,'whole mixed comparison rectangle')
        major=[q(39,4),q(29,4)][j];lip=q(19,4)
        need(H-A0*source/sing>major and 4+A0*minor/sing<lip,'sharper whole major derivative and minor Lipschitz')
        gamma=[a,c];rho=gamma[k]/gamma[j]
        need(gamma[j]>4*gamma[k]*slope and 7*rho>5 and major*rho>lip,'both wrong-branch exclusions and area domination')
        records.append({'major_axis':j,'slope':str(slope),'H':str(H),'squared_corner_area':str(area2),
                        'minimum_nonzero_area_sign_margin':str(min(nonzero)),'max_squared_directional_width':str(width2),
                        'width_filter_margin':str(limit-width2),'target_support_face_margin':str(facegap),
                        'rho':str(rho),'strict_area_domination_margin':str(7*rho-5),'source_minor_upper':str(minor),
                        'sharper_major_derivative_lower':str(major),'sharper_minor_Lipschitz_upper':str(lip),
                        'sharper_area_domination_margin':str(major*rho-lip)})
    return records

def label_maps():
    pts=[(-1,-1),(-1,1),(1,-1),(1,1)];survive=[];blockers=[]
    def det(a,b,c):return (b[0]-a[0])*(c[1]-a[1])-(b[1]-a[1])*(c[0]-a[0])
    for perm in permutations(range(4)):
        short=all(pts[perm[i]][1]==pts[perm[j]][1] for i,j in [(0,2),(1,3)])
        orient=all(det(pts[i],pts[j],pts[k])*det(pts[perm[i]],pts[perm[j]],pts[perm[k]])>0 for i,j,k in combinations(range(4),3))
        if short and orient:survive.append(list(perm))
        else:blockers.append({'map':list(perm),'short_type':short,'orientation':orient})
    need(survive==[[0,1,2,3],[3,2,1,0]],'all24 label maps reduce to identity and antipode')
    return {'survivors':survive,'blocked':blockers}

def off_mirror(C,V,G):
    r=(q(1,20),q(1,1000),S(1));N=fdot(r,r);sq,n=shadow(V,r)
    need(sq==brightness(C,r)**2/N and n==18,'physical18-corner original example')
    records=[];cos2=Z
    for ix,g in enumerate(G):
        v=act(transpose(g),r)
        for j in (0,1):
            ts=[Z,q(1,12)]
            if v[2]!=0 and 0<v[j]/v[2]<q(1,12):ts.append(v[j]/v[2])
            candidates=[]
            for t in ts:
                num=v[2]+t*v[j]
                if num>0:candidates.append(num*num/(N*(1+t*t)))
            m=max(candidates,default=Z);cos2=max(cos2,m)
            records.append({'group_index':ix,'family':j,'maximum_positive_squared_cosine':str(m)})
    need(cos2==q(1002500,1002501) and cos2<(1-q(1,2000)**2/2)**2,'complete signed mirror distance')
    caps={}
    for name,refs,radius in [('twofold',[(Z,Z,S(1))],q(1,270)),
                             ('fivefold',[(Z,P,S(1))],q(1,1500)),
                             ('endpoint',[(S(1),Z,S(12)),(Z,S(1),S(12))],q(1,15000))]:
        values=[]
        for g in G:
            for v in refs:
                t=act(g,v);d=fdot(t,r)
                if d>0:values.append(d*d/(fdot(t,t)*N))
        m=max(values);need(m<(1-radius*radius/2)**2,'specified prior '+name+' cover')
        caps[name]={'radius':str(radius),'max_positive_cosine_squared':str(m)}
    height=min(fdot(v,r)**2/N for v in V);need(height<q(83,200)**2,'specified height band')
    return {'squared_area':str(sq),'corners':n,'mirror_cosine_squared':str(cos2),'all120_group_family_maxima':records,
            'specified_prior_caps':caps,'minimum_original_height_squared':str(height)}

def controls(V,C):
    rejected=[]
    for name,fn in [('missing_original',lambda:need(len(V[:-1])==60,'missing original')),
                    ('false_wide_wedge',lambda:wedge_gates(C,V,q(1,2))),
                    ('false_mirror_cosine',lambda:need(q(1002500,1002501)<(1-q(1,1000)**2/2)**2,'too-large mirror chord')),
                    ('wrong_minor_domination',lambda:need(6*(P**2)/(2+P)>5,'major6 fails y domination'))]:
        try:fn()
        except ValueError:rejected.append(name)
        else:raise ValueError('damaged control accepted:'+name)
    need(sign((9,-4))>0 and sign((-9,4))<0 and sign((2,-1))<0,'cancelling surd signs')
    return rejected

def physical_controls(C,V):
    cube=[tuple(S(x) for x in r) for r in product((-1,1),repeat=3)]
    cube_axes={projective(tuple(S(x) for x in r)) for r in product((-1,0,1),repeat=3) if any(r)}
    for r in cube_axes:
        sq,n=shadow(cube,r)
        need(sq==16*sum((absolute(x) for x in r),Z)**2/fdot(r,r),'physical cube area and Jacobian')
    checks=0
    for j in [0,1]:
        H=[4+8*P,8+4*P][j]
        for s in [Z,q(1,24),q(1,12)]:
            for factor in [q(-1,20),Z,q(1,20)]:
                r=[Z,Z,S(1)];r[j]=s;r[1-j]=factor*s
                a=(12+28*P+H*s+4*absolute(factor*s))**2/fdot(r,r)
                need(a==shadow(V,r)[0]==brightness(C,r)**2/fdot(r,r),'both signs and zero raw tilt physical regressions');checks+=1
    return {'cube_exact_axes':len(cube_axes),'wedge_physical_regressions':checks,
            'interpretation':'regression controls only; affine/derivative bounds prove continua'}

def build():
    raw=originals();V=[as_fields(v,2) for v in raw]
    C,hull=facets(raw);G=proper_group(V);polar,rho0,rho5=polar_data(C,V,G)
    return {'actual_reviewer':'six-reviewer-4','role':'independent mathematical reviewer',
            'hull':hull,'proper_group_size':len(G),'polar':polar,'full_source_filter':width_filter(C,V,rho0,rho5),
            'wedge_gates':wedge_gates(C,V),'all_label_maps':label_maps(),'off_mirror_example':off_mirror(C,V,G),
            'rejected_controls':controls(V,C),'physical_controls':physical_controls(C,V)}

def main():
    p=argparse.ArgumentParser();p.add_argument('--emit',action='store_true');a=p.parse_args()
    out=(json.dumps(build(),indent=2,sort_keys=True)+'\n').encode()
    if a.emit:print(out.decode(),end='')
    else:need(out==(HERE/'expected.json').read_bytes(),'whole expected record differs');print('PASS')

if __name__=='__main__':main()
