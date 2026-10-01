#!/usr/bin/env python3
"""Exact finite hypotheses for all-source closed RID receiving wedges.

PROOF.md supplies the continuum argument. The complete pinned source
filter is replayed; all new comparisons are ordered Q(phi), without floats.
Python 3.11+ standard library only. No sampling certifies a continuum.
"""
from pathlib import Path
from fractions import Fraction as Q
from importlib.util import module_from_spec, spec_from_file_location
from itertools import product
import argparse, hashlib, json, sys

HERE=Path(__file__).resolve().parent
U=Q(1,12)
SLOPE=Q(1,20)


def require(condition,message):
    if not condition:raise ValueError(message)


def replay():
    pin=json.loads((HERE/'DEPENDENCIES.json').read_text())
    directory=(HERE/pin['directory']).resolve()
    require(set(pin['sha256'])=={'check.py','PROOF.md','DEPENDENCIES.json','expected.json'},'filter inventory differs')
    for name,digest in pin['sha256'].items():
        require(hashlib.sha256((directory/name).read_bytes()).hexdigest()==digest,'published filter changed:'+name)
    require('field' not in sys.modules,'arithmetic loaded before verification')
    spec=spec_from_file_location('wedge_filter_dependency',directory/'check.py')
    f=module_from_spec(spec);spec.loader.exec_module(f)
    result=f.verify();output=(json.dumps(result,indent=2,sort_keys=True)+'\n').encode()
    require(output==(directory/'expected.json').read_bytes(),'whole filter expected record differs')
    five=json.loads((directory/'DEPENDENCIES.json').read_text())
    fold=(directory/five['directory']).resolve()
    original=json.loads((fold/'DEPENDENCIES.json').read_text())
    base=(fold/original['directory']).resolve()
    require(Path(sys.modules['field'].__file__).resolve()==base/'field.py','verified original arithmetic location differs')
    for name,digest in original['sha256'].items():
        require(hashlib.sha256((base/name).read_bytes()).hexdigest()==digest,'original source changed after replay:'+name)
    spec=spec_from_file_location('wedge_original_geometry',base/'verify.py')
    b=module_from_spec(spec);spec.loader.exec_module(b)
    return b,{'filter_whole_expected_bytes':len(output),'filter_whole_expected_sha256':hashlib.sha256(output).hexdigest(),
              'source_commit':pin['source_commit'],'graph':pin['graph_ref'],
              'transitive_replay':'complete filter, fivefold and original brightness records'}


def tangent_data(b,C,j,slope=SLOPE):
    Z=b.ZERO;k=1-j;D=[v for v in C if v[2]==Z]
    require(len(C)==31 and len(D)==6,'physical Cauchy generator inventory differs')
    signed=tuple(sum((v[i]*v[2].sign() for v in C if v[2]!=Z),Z) for i in range(3))
    require(signed==(Z,Z,12+28*b.PHI),'nonzero-height signed sum differs')
    mixed=[v for v in D if v[j]!=Z];pure=[v for v in D if v[j]==Z]
    H=sum((abs(v[j]) for v in mixed),Z)
    S=tuple(sum((v[i]*v[j].sign() for v in mixed),Z) for i in range(3))
    require(S[j]==H and S[k]==S[2]==Z,'mixed tangent sum is not axial')
    require(sum((abs(v[k]) for v in pure),Z)==b.F(4),'pure minor coefficient differs')
    require(all(abs(v[j])-slope*abs(v[k])>Z for v in mixed),'tangent signs fail on whole wedge')
    require(H==[4+8*b.PHI,8+4*b.PHI][j],'major coefficient differs')
    gaps=[]
    for s,t in [(Q(0),Q(0)),(U,U*slope),(U,-U*slope)]:
        raw=[Z,Z,b.ONE];raw[j]=b.F(s);raw[k]=b.F(t)
        gaps.extend(v[2].sign()*b.dot(v,raw) for v in C if v[2]!=Z)
    require(len(gaps)==75 and min(gaps)>Z,'nonzero facet signs fail on whole triangular wedge')
    return H,{'major_coefficient':H.encode(),'minor_coefficient':'4',
              'mixed_sign_margins':[ (abs(v[j])-slope*abs(v[k])).encode() for v in mixed],
              'nonzero_facet_sign_corner_comparisons':len(gaps),'minimum_nonzero_facet_sign_corner_margin':min(gaps).encode(),
              'global_tangent_lower':'H*abs(major)+4*abs(minor)',
              'receiving_exact_area':'(A0+H*s+4*abs(t))/sqrt(1+s^2+t^2)'}


def originals(b,V,E=None):
    F,p,Z=b.F,b.PHI,b.ZERO;a=p**2;c=2+p;R2=b.vertex_guard(V)
    expected={ (sx*a,sy*c,Z) for sx,sy in product((-1,1),repeat=2)}
    actual={v for v in V if v[2]==Z} if E is None else set(E)
    require(actual==expected,'four original equatorial contacts differ')
    require(all(abs(v[2])>=b.ONE for v in V if v not in actual),'nonequatorial original height below1')
    require(max(abs(x) for v in V for x in v)==p**3,'maximum original coordinate differs')
    faces=[]
    for k in [0,1]:
        other=[i for i in range(3) if i!=k]
        face={v for v in V if v[k]==p**3}
        wanted=set()
        for s1,s2 in product((-1,1),repeat=2):
            v=[Z,Z,Z];v[k]=p**3;v[other[0]]=F(s1);v[other[1]]=F(s2);wanted.add(tuple(v))
        require(face==wanted,'four independent minor-row originals differ')
        require(max(v[k] for v in V if v not in face)==c,'next original coordinate differs')
        faces.append({'axis':k,'actual_originals':[b.encode(v) for v in sorted(face,key=b.key)]})
    require(R2<F(20) and F(Q(22,5)**2)<R2<F(Q(9,2)**2),'original radius root brackets fail')
    return {'equatorial_originals':[b.encode(v) for v in sorted(actual,key=b.key)],'minor_row_faces':faces,
            'common_squared_radius':R2.encode(),'nonequatorial_original_count':len(V)-len(actual)}


def width_data(b,V,j,offset=Q(0)):
    # All sixty inequalities are affine in m, on the entire interval.
    F,p,Z=b.F,b.PHI,b.ZERO;B=3*p**2;S=p+2
    mmax=p*U if j==0 else F(U)
    comparisons=0
    for m in [Z,p*U]:
        z=(p,b.ONE,-m);h=B+p*m+F(offset)
        require(all(b.dot(z,v)<=h for v in V),'affine physical width support failed')
        require(b.dot(z,(2*p,p**2,-p))==h,'original width witness not attaining support')
        comparisons+=len(V)
    require(p*S-B*(p*U)>Z,'width derivative not positive on full m interval')
    w2=4*(B+p*mmax)**2/(S+mmax*mmax)
    limit=(20+32*p)*(1-Q(10,11664))
    require(w2<limit,'entire wedge width fails source filter')
    require(p-SLOPE>Z and 1-p*SLOPE>Z,'reduced receiving width parameter can be negative')
    return {'original_support_endpoint_comparisons':comparisons,'maximum_m':mmax.encode(),
            'maximum_squared_directional_width':w2.encode(),'filter_squared_width_margin':(limit-w2).encode(),
            'width_formula':'4*(3phi^2+phi*m)^2/(phi+2+m^2)',
            'receiving_m':['phi*s-abs(t)','s-phi*abs(t)'][j]}


def scalar_data(b,H,j,epsilon=Q(11,20),minor_bound=Q(1,80),major_derivative=Q(7)):
    F,p=b.F,b.PHI;A0=12+28*p;a=p**2;c=2+p;gamma=[a,c];rho=gamma[1-j]/gamma[j]
    bmax=Q(9,2);zmin=Q(99,100);sing=Q(24,25);source=Q(3,25);frame=Q(4,15)
    norm2=1+(1+SLOPE*SLOPE)*U*U
    require(F(50)<A0<F(58),'physical area bracket fails')
    require(zmin*zmin*norm2<1 and (1+SLOPE*SLOPE)*U*U<Q(1,11)**2,'receiving positive z/chord brackets fail')
    require((zmin*(1-bmax*U*(1+SLOPE)))**2>Q(9,25)>Q(36,125),'nonequatorial height separation fails')
    require(Q(36,125)<epsilon*epsilon,'actual equatorial matching error fails')
    require(1-source*source>sing*sing and zmin>sing,'equatorial singular bounds fail')
    require(2*a*sing>F(2*epsilon) and 2*c*sing-2*a>F(2*epsilon),'rectangle separation/side gates fail')
    require(F(4*epsilon)*(a+c)+F(4*epsilon*epsilon)<4*a*c*sing,'proper determinant gate fails')
    roll=(epsilon+Q(9,256)+Q(9,484))/Q(22,5)
    require(Q(1,8)+roll<frame,'full arbitrary-roll frame bound fails')
    require(1-frame*frame/2>Q(9,10),'initial positive source row fails')
    require(1+U/(1+zmin)<Q(21,20),'actual target row transverse budget fails')
    l1max=Q(21,20)*U*SLOPE
    require((p**3-c)*zmin-(p**3-1)*l1max>b.ZERO,'actual target row exposed face can change')
    coefficient=bmax*frame/Q(19,10)
    require(coefficient==Q(12,19) and Q(21,20)/(1-coefficient)<3,'minor-source localization factor3 fails')
    require(3*U*SLOPE<=minor_bound,'source minor outside declared derivative domain')
    require(1-source*source-minor_bound*minor_bound>sing*sing,'mixed comparison path square root fails')
    require(H-A0*source/sing>F(major_derivative),'major area derivative bound fails')
    require(4+A0*minor_bound/sing<F(5),'minor area Lipschitz bound5 fails')
    require(gamma[j]>4*gamma[1-j]*SLOPE,'wrong equatorial absolute-value branch can survive')
    require(major_derivative*rho>F(5),'paired radial order does not dominate minor area change')
    corner=(A0+H*U+4*U*SLOPE)**2/F(norm2)
    require(corner<F(Q(1171,20)**2) and 940+1520*p>F(Q(583,10)**2),'physical corner area fails source filter')
    require(H-U*(A0+4*U*SLOPE)>b.ZERO and 4-U*SLOPE*(A0+H*U)>b.ZERO,'whole-domain raw area monotonicity fails')
    return {'wedge_corner_squared_area':corner.encode(),'target_chord_upper':'1/11','target_z_lower':'99/100',
            'nonequatorial_height_lower':'3/5','source_tangent_upper':'3/25','equatorial_match_error':str(epsilon),
            'full_row_frame_error_upper':str(frame),'initial_roll_error_upper':str(roll),
            'target_minor_row_l1_factor_upper':'21/20','source_minor_factor_upper':'3',
            'source_minor_upper':str(minor_bound),'source_minor_face_strict_margin':((p**3-c)*zmin-(p**3-1)*l1max).encode(),
            'area_major_derivative_lower':str(major_derivative),'area_minor_Lipschitz_upper':'5',
            'paired_radius_ratio':rho.encode(),'strict_area_domination_margin':(major_derivative*rho-5).encode()}


def example(b,V,C,G):
    F,Z,O=b.F,b.ZERO,b.ONE;r=(F(Q(1,20)),F(Q(1,1000)),O);N=b.dot(r,r)
    raw=b.brightness_raw(C,r);direct,corners=b.direct_shadow_raw(V,r)
    require(raw==direct and corners==18,'independent physical example hull area differs')
    require(r[0]<=F(U) and abs(r[1])<=r[0]*SLOPE,'example not in new wedge')
    candidates=[]
    for g in G:
        q=b.act(tuple(zip(*g)),r)
        for j in [0,1]:
            ss=[Z,F(U)]
            if q[2]!=Z:
                t=q[j]/q[2]
                if Z<t<F(U):ss.append(t)
            for t in ss:
                numerator=q[2]+t*q[j]
                if numerator>Z:candidates.append((numerator**2/(N*(O+t*t)),j,t))
    cos2,j,t=max(candidates,key=lambda item:item[0])
    require(cos2==F(Q(1002500,1002501)) and j==0 and t==F(Q(1,20)),'complete mirror maximum differs')
    for radius in [Q(1,2000000),Q(1,2000)]:
        require(cos2<F((1-radius*radius/2)**2),'example covered by complete mirror tube')
    caps={}
    for label,refs,radius in [('twofold',[(Z,Z,O)],Q(1,270)),
                              ('endpoint',[(O,Z,F(12)),(Z,O,F(12))],Q(1,15000)),
                              ('fivefold',[(Z,b.PHI,O)],Q(1,1500))]:
        scores=[]
        for g in G:
            for ref in refs:
                q=b.act(g,ref);d=b.dot(q,r)
                if d>Z:scores.append(d*d/(b.dot(q,q)*N))
        maximum=max(scores)
        require(maximum<F((1-radius*radius/2)**2),'example covered by specified '+label+' caps')
        caps[label]={'chord_radius':str(radius),'maximum_positive_squared_cosine':maximum.encode()}
    f2=min(b.dot(v,r)**2/N for v in V)
    require(f2<F(Q(83,200)**2),'example covered by specified height band')
    return {'raw_receiving_normal':b.encode(r),'physical_squared_area':(raw*raw/N).encode(),
            'original_shadow_hull_size':corners,'complete_mirror_maximum_squared_cosine':cos2.encode(),
            'nearest_mirror_parameter':t.encode(),'complete_mirror_chord_distance_lower':'1/2000',
            'outside_specified_old_caps':caps,'minimum_original_height_squared':f2.encode(),
            'prior_cover_scope':'these specified caps, complete mirror tube and height band only; no exhaustive older-cover claim'}


def negative_controls(b,V,C,H):
    E=[v for v in V if v[2]==b.ZERO]
    cases=[lambda:originals(b,V,E[:-1]),lambda:tangent_data(b,C,0,Q(1,2)),
           lambda:width_data(b,V,0,Q(-1,100)),lambda:scalar_data(b,H[0],0,epsilon=Q(1)),
           lambda:scalar_data(b,H[0],0,minor_bound=Q(1,4)),
           lambda:scalar_data(b,H[1],1,major_derivative=Q(6))]
    for case in cases:
        try:case()
        except ValueError:continue
        raise ValueError('damaged certificate or domain control accepted')
    return len(cases)


def verify():
    b,pin=replay();V=b.vertices();planes,pc=b.complete_facets(V);C,records,cc=b.area_generators(V,planes)
    G=b.proper_group(V);F,Z,O=b.F,b.ZERO,b.ONE
    Rz=(( -O,Z,Z),(Z,-O,Z),(Z,Z,O))
    require(Rz in G,'proper tangent half-turn missing')
    data=originals(b,V);families=[];H=[]
    for j in [0,1]:
        h,tangent=tangent_data(b,C,j);H.append(h)
        families.append({'major_axis':['x','y'][j],**tangent,**width_data(b,V,j),**scalar_data(b,h,j)})
    return {'agent':'six-rupert-3','role':'researcher','arithmetic':'exact ordered Q(phi); no floating comparison',
            'proof_status':'complete written continuum proof with exact finite hypotheses; author-checked, unformalized, unreviewed',
            'global_RID_Rupert_status':'unresolved','receiving_raw_domain':'g*(s,t,1) or g*(t,s,1), normalized; 0<=s<=1/12, abs(t)<=s/20',
            'closed_fit_classification':'every lambda>=1 and arbitrary source/proper roll/physical translation: lambda=1,t=0,B1=sigma*B2*g',
            'direct_prerequisite':pin,'original_vertices':len(V),'proper_group_order':len(G),
            'physical_facet_record_sha256':b.digest(records),'physical_area_generators':len(C),
            'families':families,'original_geometry':data,'example':example(b,V,C,G),
            'damaged_controls_rejected':negative_controls(b,V,C,H),**pc,**cc}


def main():
    parser=argparse.ArgumentParser();parser.add_argument('--emit',action='store_true');args=parser.parse_args()
    output=(json.dumps(verify(),indent=2,sort_keys=True)+'\n').encode()
    if not args.emit:require(output==(HERE/'expected.json').read_bytes(),'new complete expected record differs')
    sys.stdout.buffer.write(output)


if __name__=='__main__':main()
