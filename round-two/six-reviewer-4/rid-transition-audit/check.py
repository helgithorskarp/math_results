"""Independent exact hypotheses for the RID Cauchy-transition receiving cones.

six-reviewer-4, independent mathematical reviewer. Only hash-pinned OWN
original-coordinate arithmetic/geometry is reused; no author code or expected
fixture is imported. REVIEW.md supplies all continuum/closed-fit bridges.
"""
import argparse
from importlib.util import module_from_spec, spec_from_file_location
import hashlib
import json
from pathlib import Path
import sys

HERE = Path(__file__).resolve().parent

def require(ok, message):
    if not ok:
        raise ValueError(message)

def load_geometry():
    pin=json.loads((HERE/'DEPENDENCIES.json').read_text())
    directory=(HERE/pin['directory']).resolve()
    require(set(pin['sha256'])=={'check.py','field.py','expected.json','REVIEW.md'}, 'own dependency inventory')
    for name, digest in pin['sha256'].items():
        require(hashlib.sha256((directory/name).read_bytes()).hexdigest()==digest, 'own dependency changed:'+name)
    require('field' not in sys.modules, 'field loaded before dependency check')
    sys.path.insert(0,str(directory))
    spec=spec_from_file_location('own_reviewed_rid_geometry',directory/'check.py')
    b=module_from_spec(spec);spec.loader.exec_module(b)
    require(Path(sys.modules['field'].__file__).resolve()==directory/'field.py', 'arithmetic module location')
    return b,pin

def digest(record):
    return hashlib.sha256((json.dumps(record,sort_keys=True,separators=(',',':'))+'\n').encode()).hexdigest()

def tangent(b,C,drop=False):
    P,Z,S=b.P,b.Z,b.S
    D={v for v in C if v[2]==0}
    if drop:D.remove((S(4),Z,Z))
    expected={(P-1,P,Z),(P-1,-P,Z),(1+3*P,2+P,Z),(1+3*P,-2-P,Z),(S(4),Z,Z),(Z,S(4),Z)}
    require(len(C)==31 and D==expected,'six actual tangent vectors')
    non=(Z,Z,Z)
    for v in C:
        if v[2]!=0:non=b.add(non,b.scale(S(1) if v[2]>0 else S(-1),v))
    require(non==(Z,Z,12+28*P),'global signed non-tangent axis')
    first=(P-1)/P;second=(1+3*P)/(2+P)
    require(first==2-P and second==P and 0<first<b.q(1,2)<second,'actual x kinks')
    require(b.q(1,2)<P-1,'entire y-major chamber')
    pieces=[(0,4+8*P,S(4)),(0,6+6*P,4+2*P),(1,8+4*P,S(4))]
    require(pieces[0][1]+first*pieces[0][2]==pieces[1][1]+first*pieces[1][2],'continuous physical x kink')
    signs=[]
    for j in (0,1):
        margins=[]
        for s,t in ((Z,Z),(b.q(1,20),b.q(1,40)),(b.q(1,20),-b.q(1,40))):
            r=[Z,Z,S(1)];r[j]=s;r[1-j]=t
            margins.extend(b.fdot(v,r)*(S(1) if v[2]>0 else S(-1)) for v in C if v[2]!=0)
        require(len(margins)==75 and min(margins)>0,'entire triangle affine facet signs')
        signs.append({'major_axis':j,'all75_margins':[str(x) for x in margins]})
    return pieces,{'vectors':[[str(x) for x in v] for v in sorted(D)],'x_transitions':[str(first),str(second)],'pieces':[[j,str(h),str(k)] for j,h,k in pieces],'affine_signs':signs}

def width(b,V,j,offset=None):
    P,Z=b.P,b.Z;offset=Z if offset is None else offset
    margins=[]
    for m in (Z,P/12):
        d=(P,b.S(1),-m);h=3*P**2+P*m+offset
        gaps=[h-b.fdot(d,v) for v in V]
        require(min(gaps)>=0 and b.fdot(d,(2*P,P**2,-P))==h,'every original support and attaining witness')
        margins.append([str(x) for x in gaps])
    require(P*(P+2)-3*P**2*(P/12)>0,'entire width support interval derivative')
    require(P>b.q(1,2) and 1-P/2>0,'both signed perpendicular direction branches')
    m=P/20 if j==0 else b.q(1,20)
    value=4*(3*P**2+P*m)**2/(P+2+m*m)
    limit=(20+32*P)*(1-b.q(10,11664))
    require(value<limit,'all-source filter actual receiving width')
    return {'maximum_parameter':str(m),'squared_width':str(value),'filter_margin':str(limit-value),'all120_original_support_gaps':margins}

def matching(b,V,eps=None):
    P,q,S,Z=b.P,b.q,b.S,b.Z;eps=q(11,20) if eps is None else eps
    a,c,B=P**2,2+P,P**3;R2=7+8*P
    E={v for v in V if v[2]==0}
    require(E=={(sx*a,sy*c,Z) for sx in (-1,1) for sy in (-1,1)},'actual equatorial labels')
    require(min(b.absolute(v[2]) for v in V if v not in E)==1 and max(b.absolute(x) for v in V for x in v)==B,'all original height/coordinate layers')
    require(1+q(1,20)**2+q(1,40)**2==q(321,320),'receiver raw norm')
    require(q(99,100)**2*q(321,320)<1 and q(1,20)**2+q(1,40)**2<q(1,11)**2,'entire receiver z/chord bounds')
    height=q(99,100)*(1-q(9,2)*q(3,40))
    require(B<q(9,2) and R2<20 and height>q(3,5),'new actual nonequatorial separation')
    require(q(36,125)<eps*eps and q(36,125)<q(9,25),'radial original matching error')
    sing=q(24,25)
    require(1-q(3,25)**2>sing**2 and q(99,100)>sing,'equatorial singular values')
    require(2*a*sing>2*eps and 2*c*sing-2*a>2*eps,'unequal rectangle side separation')
    require(4*eps*(a+c)+4*eps**2<4*a*c*sing,'all proper orientation matching determinants')
    roll=(eps+q(9,256)+q(9,484))/q(22,5)
    require(R2>q(22,5)**2 and q(1,8)+roll<q(4,15),'full arbitrary roll/frame bound')
    require(1-q(4,15)**2/2>q(9,10),'positive actual source row diagonal')
    require(1-q(1,40)**2/(1+q(99,100))>q(99,100) and 1+q(1,20)/(1+q(99,100))<q(21,20),'entire actual target minor row')
    faces=[]
    for k in (0,1):
        face={v for v in V if v[k]==B};other=[i for i in range(3) if i!=k]
        require(len(face)==4 and max(v[k] for v in V if v not in face)==c,'actual four-point next support layer')
        require({(v[other[0]],v[other[1]]) for v in face}=={(S(x),S(y)) for x in (-1,1) for y in (-1,1)},'actual independent original signs')
        faces.append([[str(x) for x in v] for v in sorted(face)])
    gap=(B-c)*q(99,100)-(B-1)*q(21,800)
    require(gap>0,'expanded receiver actual exposed face persists')
    return {'raw_norm_squared':'321/320','nonequatorial_height_lower':str(height),'roll_upper':str(roll),'actual_face_margin':str(gap),'actual_four_point_faces':faces,'all24_label_maps':b.label_maps()}

def bootstrap(b,factor=None,slope=None):
    q,P=b.q,b.P;factor=q(6,5) if factor is None else factor;slope=q(1,2) if slope is None else slope
    initial=q(21,20)/(1-q(9,2)*q(4,15)/q(19,10))
    require(initial==q(399,140)<3,'initial row bootstrap')
    require(1-q(3,40)**2>q(99,100)**2,'improved positive source row diagonal')
    first=q(21,20)/(1-q(9,2)*q(3,40)/q(199,100))
    second=q(21,20)/(1-q(9,2)*q(13,400)/q(199,100))
    require(first==q(4179,3305)<q(13,10) and second==q(8358,7375)<factor,'both exact new row refinements')
    require(factor*q(1,40)<=q(3,100),'full minor comparison rectangle')
    gamma=[P**2,2+P];gaps=[]
    for j in (0,1):
        gap=gamma[j]-factor*slope*gamma[1-j]
        require(gap>0 and gamma[j]>slope*gamma[1-j],'UNSQUARED wrong-radius-branch contradiction')
        gaps.append(str(gap))
    return {'initial':str(initial),'first':str(first),'second':str(second),'minor_factor_upper':str(factor),'source_minor_upper':'3/100','both_wrong_branch_margins':gaps,'zero_rule':'Y=0 gives q=y=0; X=0 then requires no division'}

def areas(b,C,pieces,premature=False,excessive=False):
    q,P,S,Z=b.q,b.P,b.S,b.Z;A0=12+28*P;U=q(1,20);M=q(3,100)
    root=q(124,125)
    require(1-q(3,25)**2-M*M>root*root,'sharper whole rectangle positive root')
    widths=[q(3,25),q(3,25),q(1,12)]
    Ds=[S(10),q(35,4),q(19,2)];Ls=[q(23,4),S(9),q(23,4)]
    if premature:widths[2]=q(3,25)
    if excessive:Ds[1]=S(10)
    records=[]
    for ix,(j,H,K) in enumerate(pieces):
        require(H-U*(A0+K*U/2)>0 and K-U/2*(A0+H*U)>0,'whole receiving raw-box monotonicity')
        r=[Z,Z,S(1)];r[j]=U;r[1-j]=U/2
        receiving=b.brightness(C,r)**2/b.fdot(r,r)
        corner=(A0+H*U+K*U/2)**2/(1+U*U*5/4)
        if ix!=0:require(corner==receiving,'actual physical upper-corner area')
        cap=q(1171,20) if j==0 else q(581,10)
        require(receiving<cap**2 and cap<=q(583,10)+q(1,4) and 940+1520*P>q(583,10)**2,'full receiving area source-filter budget')
        if j==1:
            require(H-A0*q(3,25)/q(24,25)>7 and K-A0*M/q(24,25)>0,'initial y-major source lower-bound monotonicity')
            right=cap-H/12;cut=A0*A0*q(143,144)-right*right
            require(right>0 and cut>0,'positive unsquared source y-major cutoff')
        else:cut=None
        dm=H-A0*widths[ix]/root-Ds[ix]
        lm=Ls[ix]-K-A0*M/root
        rho=(2+P)/P**2 if j==0 else P**2/(2+P)
        require(dm>0 and lm>0 and Ds[ix]*rho>Ls[ix],'sharper same-piece whole-domain area domination')
        records.append({'major_axis':j,'H':str(H),'K':str(K),'physical_receiver_corner_squared_area':str(receiving),'source_major_upper':str(widths[ix]),'source_minor_upper':str(M),'rectangle_root_lower':str(root),'major_derivative_lower':str(Ds[ix]),'minor_Lipschitz_upper':str(Ls[ix]),'positive_major_gate':str(dm),'positive_minor_gate':str(lm),'rho':str(rho),'area_domination_margin':str(Ds[ix]*rho-Ls[ix]),'positive_y_source_cutoff_gate':str(cut) if cut is not None else None})
    return records

def example(b,V,C,G,freeze=False,chord=None):
    q,P,S,Z=b.q,b.P,b.S,b.Z;chord=q(1,50) if chord is None else chord
    r=(q(1,20),q(1,40),S(1));N=b.fdot(r,r);physical=b.brightness(C,r)
    direct,corners=b.shadow(V,r)
    require(direct==physical**2/N and corners==16,'independent physical seed hull/Jacobian')
    raw_formula=12+28*P+(6+6*P)*r[0]+(4+2*P)*r[1]
    old=12+28*P+(4+8*P)*r[0]+4*r[1]
    require(physical==(old if freeze else raw_formula),'actual receiving kink cannot use old area formula')
    require(physical-old==(2-P)/20>0,'exact old area shortfall')
    maxima=[];members=[];best=Z
    for ix,g in enumerate(G):
        v=b.act(b.transpose(g),r)
        for j in (0,1):
            if v[2]>0 and 0<=v[j]<=v[2]/12 and 20*b.absolute(v[1-j])<=v[j]:members.append([ix,j])
            ts=[Z,q(1,12)]
            if v[2]!=0 and 0<v[j]/v[2]<q(1,12):ts.append(v[j]/v[2])
            scores=[]
            for t in ts:
                numerator=v[2]+t*v[j]
                if numerator>0:scores.append(numerator*numerator/(N*(1+t*t)))
            local=max(scores,default=Z);best=max(best,local)
            maxima.append({'group_index':ix,'family':j,'max_positive_cosine_squared':str(local)})
    require(not members and best==q(1604,1605),'all proper old-W membership and whole-mirror maximum')
    require(best<(1-chord*chord/2)**2,'entire mirror family distance bound')
    caps={}
    for name,refs,radius in [('twofold',[(Z,Z,S(1))],q(1,270)),('fivefold',[(Z,P,S(1))],q(1,1500)),('endpoint',[(S(1),Z,S(12)),(Z,S(1),S(12))],q(1,15000))]:
        score=Z
        for g in G:
            for ref in refs:
                v=b.act(g,ref);d=b.fdot(v,r)
                if d>0:score=max(score,d*d/(b.fdot(v,v)*N))
        require(score<(1-radius*radius/2)**2,'specified older '+name+' caps')
        caps[name]={'max_positive_cosine_squared':str(score),'radius':str(radius)}
    height=min(b.fdot(v,r)**2/N for v in V);require(height<q(83,200)**2,'specified height threshold')
    return {'physical_squared_area':str(direct),'corners':corners,'old_formula_raw_shortfall':str(physical-old),'old_W_members':members,'mirror_cosine_squared':str(best),'all120_signed_curve_maxima':maxima,'specified_caps':caps,'minimum_original_height_squared':str(height)}

def controls(b,V,C,G,pieces):
    functions=[('missing_actual_tangent',lambda:tangent(b,C,True)),('frozen_old_area_across_kink',lambda:example(b,V,C,G,freeze=True)),('altered_actual_width_witness',lambda:width(b,V,0,b.q(1,1000))),('excessive_matching_budget',lambda:matching(b,V,b.q(3,4))),('understated_minor_bootstrap',lambda:bootstrap(b,b.q(11,10))),('automatic_wider_slope',lambda:bootstrap(b,slope=b.q(2,3))),('premature_y_source_derivative',lambda:areas(b,C,pieces,premature=True)),('first_chamber_derivative_in_second',lambda:areas(b,C,pieces,excessive=True)),('false_whole_mirror_distance',lambda:example(b,V,C,G,chord=b.q(1,40)))]
    rejected=[]
    for name,fn in functions:
        try:fn()
        except ValueError:rejected.append(name)
        else:raise ValueError('damaged control accepted:'+name)
    physical=0
    for j in (0,1):
        for s in (b.Z,b.q(1,40),b.q(1,20)):
            for ratio in (-b.q(1,2),b.P-2,b.Z,2-b.P,b.q(1,2)):
                u=b.absolute(ratio*s);r=[b.Z,b.Z,b.S(1)];r[j]=s;r[1-j]=ratio*s
                if j==1:H,K=pieces[2][1:]
                elif b.absolute(ratio)<=2-b.P:H,K=pieces[0][1:]
                else:H,K=pieces[1][1:]
                sq=(12+28*b.P+H*s+K*u)**2/b.fdot(r,r)
                require(sq==b.brightness(C,r)**2/b.fdot(r,r)==b.shadow(V,r)[0],'signed/zero/boundary/kink physical control')
                physical+=1
    return {'damaged_hypotheses_rejected':rejected,'physical_signed_zero_boundary_kink_controls':physical,'continuum_status':'Controls are not enumeration of real parameters; affine/derivative proof is in REVIEW.md.'}

def build():
    b,pin=load_geometry()
    raw=b.originals();V=[b.as_fields(v,2) for v in raw];C,hull=b.facets(raw);G=b.proper_group(V)
    polar,rho0,rho5=b.polar_data(C,V,G)
    old_filter=b.width_filter(C,V,rho0,rho5)
    pieces,tan=tangent(b,C)
    return {'actual_reviewer':'six-reviewer-4','role':'independent mathematical reviewer','own_geometry_dependency_commit':pin['source_commit'],'own_W_review_reference':pin['review_reference'],'hull_sha256':digest(hull),'hull_census':{k:hull[k] for k in ['triples','supporting_triples','faces','edges']},'proper_group_size':len(G),'complete_polar_sha256':digest(polar),'all121_physical_polar_areas_rechecked':polar['direct_hull_comparisons'],'all_source_filter_sha256':digest(old_filter),'tangent':tan,'actual_widths':[width(b,V,j) for j in (0,1)],'actual_matching':matching(b,V),'minor_bootstrap_and_unsquared_branch':bootstrap(b),'sharper_area_pieces':areas(b,C,pieces),'expanded_domain_example':example(b,V,C,G),'controls':controls(b,V,C,G,pieces)}

def main():
    p=argparse.ArgumentParser();p.add_argument('--emit',action='store_true');a=p.parse_args()
    out=(json.dumps(build(),sort_keys=True,indent=2)+'\n').encode()
    if a.emit:sys.stdout.buffer.write(out)
    else:require(out==(HERE/'expected.json').read_bytes(),'entire frozen independent record differs');print('PASS')

if __name__=='__main__':main()
