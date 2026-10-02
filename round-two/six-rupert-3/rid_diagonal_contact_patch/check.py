#!/usr/bin/env python3
"""Exact all-source RID closed-fit classification on a diagonal receiving box.

PROOF.md supplies the continuum arguments. Ordered Q(phi), rational
positive-root comparisons, and Python standard library only. No float,
solver, sampled-angle exclusion, or inferred nonexistence is used.
"""
from pathlib import Path
from fractions import Fraction as Q
from importlib.util import module_from_spec, spec_from_file_location
from itertools import product, combinations
import argparse, hashlib, json, sys

HERE=Path(__file__).resolve().parent


def require(condition,message):
    if not condition:raise ValueError(message)


def replay():
    # Credit: the complete published width-filter replay in the W checker.
    pin=json.loads((HERE/'DEPENDENCIES.json').read_text())
    directory=(HERE/pin['directory']).resolve()
    require(set(pin['sha256'])=={'check.py','PROOF.md','DEPENDENCIES.json','expected.json'},'filter inventory differs')
    for name,digest in pin['sha256'].items():
        require(hashlib.sha256((directory/name).read_bytes()).hexdigest()==digest,'published filter changed:'+name)
    require('field' not in sys.modules,'arithmetic loaded before verification')
    spec=spec_from_file_location('contact_filter_dependency',directory/'check.py')
    f=module_from_spec(spec);spec.loader.exec_module(f)
    result=f.verify();output=(json.dumps(result,indent=2,sort_keys=True)+'\n').encode()
    require(output==(directory/'expected.json').read_bytes(),'whole filter expected record differs')
    five=json.loads((directory/'DEPENDENCIES.json').read_text())
    fold=(directory/five['directory']).resolve()
    original=json.loads((fold/'DEPENDENCIES.json').read_text())
    base=(fold/original['directory']).resolve()
    require(Path(sys.modules['field'].__file__).resolve()==base/'field.py','verified arithmetic location differs')
    for name,digest in original['sha256'].items():
        require(hashlib.sha256((base/name).read_bytes()).hexdigest()==digest,'original source changed after replay:'+name)
    spec=spec_from_file_location('contact_original_geometry',base/'verify.py')
    b=module_from_spec(spec);spec.loader.exec_module(b)
    return b,{'filter_whole_expected_bytes':len(output),'filter_whole_expected_sha256':hashlib.sha256(output).hexdigest(),
              'source_commit':pin['source_commit'],'graph':pin['graph_ref'],
              'transitive_replay':'complete filter, fivefold and original brightness records'}


def center_data(b):
    F,Z,O,p=b.F,b.ZERO,b.ONE,b.PHI
    V=b.vertices();r=(F(Q(1,25)),(2+p)/125,O);N=b.dot(r,r)
    u=(-r[1],r[0],Z);v=b.cross(r,u)
    points={}
    for i,x in enumerate(V):points.setdefault((b.dot(u,x),b.dot(v,x)),[]).append(i)
    keys=sorted(points)
    def turn(a,b,c):return (b[0]-a[0])*(c[1]-a[1])-(b[1]-a[1])*(c[0]-a[0])
    def half(seq):
        h=[]
        for x in seq:
            while len(h)>=2 and turn(h[-2],h[-1],x)<=Z:h.pop()
            h.append(x)
        return h
    hull=half(keys)[:-1]+half(reversed(keys))[:-1];cycle=[points[x][0] for x in hull]
    b.require(len(cycle)==16,'complete receiving cycle count differs')
    rows=[];contacts=[];norms=[]
    for i,j in zip(cycle,cycle[1:]+cycle[:1]):
        m=b.cross(b.sub(V[j],V[i]),r);h=b.dot(m,V[i])
        if h<Z:m=b.neg(m);h=-h
        b.require(h>Z and all(b.dot(m,x)<=h for x in V),'original edge support invalid')
        m=tuple(x/h for x in m);b.require(b.dot(m,m)<F(Q(1,16)),'normalized support normal norm not below1/4')
        norms.append(b.dot(m,m))
        for k in [i,j]:
            f=b.cross(V[k],m)
            rows.append(f);contacts.append({'edge':[i,j],'source':k,'normal':m,'torque':f})
    unique=[];indices=[]
    for i,f in enumerate(rows):
        if f not in unique:unique.append(f);indices.append(i)
    rollplus=next(i for i,f in enumerate(unique) if b.cross(f,r)==(Z,Z,Z) and b.dot(f,r)>Z)
    rollminus=next(i for i,f in enumerate(unique) if b.cross(f,r)==(Z,Z,Z) and b.dot(f,r)<Z)
    tilt=[i for i in range(len(unique)) if i not in [rollplus,rollminus]]
    xy={i:(b.dot(unique[i],u),b.dot(unique[i],v)) for i in tilt}
    def det2(a,b):return a[0]*b[1]-a[1]*b[0]
    triple=None
    for ids in combinations(tilt,3):
        i,j,k=ids;weights=[det2(xy[j],xy[k]),det2(xy[k],xy[i]),det2(xy[i],xy[j])]
        if all(w<Z for w in weights):weights=[-w for w in weights]
        if all(w>Z for w in weights):triple=(ids,weights);break
    b.require(triple is not None,'no strict planar positive dependence found')
    ids,weights=triple
    combined=tuple(sum((w*unique[i][j] for i,w in zip(ids,weights)),Z) for j in range(3))
    b.require(b.cross(combined,r)==(Z,Z,Z),'tilt positive combination not purely axial')
    tau=b.dot(combined,r)/N;ap=b.dot(unique[rollplus],r)/N;am=b.dot(unique[rollminus],r)/N
    plus=(abs(tau)-tau+O)/ap;minus=(abs(tau)+O)/(-am)
    selected=list(ids)+[rollplus,rollminus];weights=weights+[plus,minus];total=sum(weights,Z);weights=[w/total for w in weights]
    b.require(all(w>Z for w in weights) and tuple(sum((w*unique[i][j] for i,w in zip(selected,weights)),Z) for j in range(3))==(Z,Z,Z),'positive spanning balance failed')
    rankdet=b.dot(unique[ids[0]],b.cross(unique[ids[1]],unique[rollplus]));b.require(rankdet!=Z,'spanning rank below3')
    vertices={};attempted=0;singular=0
    for ids in combinations(range(len(unique)),3):
        attempted+=1;i,j,k=ids;crossjk=b.cross(unique[j],unique[k]);det=b.dot(unique[i],crossjk)
        if det==Z:singular+=1;continue
        crosski=b.cross(unique[k],unique[i]);crossij=b.cross(unique[i],unique[j])
        x=tuple((crossjk[z]+crosski[z]+crossij[z])/det for z in range(3))
        if all(b.dot(f,x)<=O for f in unique):vertices.setdefault(x,[]).append(list(ids))
    b.require(vertices,'no polytope vertices found')
    M=max(abs(x) for vertex in vertices for x in vertex)
    # P={x:f_i.x<=1}. Boundedness follows from the positive balance/rank.
    # Hence ||q||inf<=M*(17/16)||q||2^2 for every centered closed fit.
    # A nonzero q therefore has ||q||inf>=16/(51*M).
    radius=F(16)/(F(51)*M)
    records=[{'x':b.encode(x),'active_triples':triples} for x,triples in sorted(vertices.items(),key=lambda item:b.key(item[0]))]
    return {'complete_receiving_cycle':cycle,'endpoint_constraints':len(rows),'unique_torque_rows':len(unique),
            'maximum_normalized_support_normal_squared':max(norms).encode(),
            'positive_spanning_original_contact_indices':[indices[i] for i in selected],
            'positive_spanning_weights':[w.encode() for w in weights],'positive_spanning_rank_determinant':rankdet.encode(),
            'attempted_constraint_triples':attempted,'singular_constraint_triples':singular,'polytope_vertices':records,
            'maximum_polytope_coordinate_M':M.encode(),'pointwise_local_infinity_radius':radius.encode()}, \
           {'V':V,'r':r,'cycle':cycle,'contacts':contacts,'M':M,'unique':unique,'selected':selected,'weights':weights,'vertices':vertices}


def patch_data(b,internal,C):
    F,Z,O,p=b.F,b.ZERO,b.ONE,b.PHI
    V=internal['V'];r0=internal['r'];cycle=internal['cycle'];delta=Q(1,2500);geom=b
    corners=[(r0[0]+F(s)*delta,r0[1]+F(t)*delta,O) for s,t in product([-1,1],repeat=2)]
    a=p**2;c=2+p;radius2=7+8*p
    eps=Q(3,20);zmin=Q(99,100);ell=Q(41,40)
    global_records=[]
    for r in corners:
        N=b.dot(r,r)
        b.require(r[0]>Z and r[1]>Z and N-O<F(Q(1,400)) and F(zmin*zmin)*N<O,'entire-box target tilt/z gate fails')
        b.require(r[0]+r[1]<F(Q(7,100)),'nonequatorial raw sum gate fails')
        ratio=c*r[1]/(a*r[0])
        b.require(F(Q(40,41))<ratio<F(Q(41,40)),'near weighted-diagonal ratio fails')
        b.require(abs(a*r[0]-c*r[1])<F(Q(1,400)),'receiver minus height bound fails')
        b.require(a*r[0]+c*r[1]<F(Q(53,250)),'receiver plus height bound fails')
        raw=geom.brightness_raw(C,r)
        b.require(raw<F(Q(1171,20)),'physical receiving area gate fails even with norm denominator removed')
        m=p*r[0]-r[1]
        b.require(Z<m<p/12,'receiving width parameter leaves affine interval')
        # Preserve all genuine edges, including endpoints, over the whole box.
        gaps=[];normal_bounds=[]
        for i,j in zip(cycle,cycle[1:]+cycle[:1]):
            mvec=b.cross(b.sub(V[j],V[i]),r);h=b.dot(mvec,V[i])
            b.require(h>Z,'outward raw edge orientation changed')
            b.require(h-b.dot(mvec,V[i])==Z and h-b.dot(mvec,V[j])==Z,'actual incident endpoint support equality fails')
            gaps.extend(h-b.dot(mvec,v) for k,v in enumerate(V) if k not in [i,j])
            b.require(b.dot(mvec,mvec)<h*h/16,'box normalized edge normal norm not below1/4')
            normal_bounds.append((b.dot(mvec,mvec)/(h*h)).encode())
        b.require(min(gaps)>Z,'full sixteen-edge original supports fail strictly at corner')
        global_records.append({'raw_corner':b.encode(r),'minimum_nonendpoint_edge_support_margin':min(gaps).encode(),
                               'raw_Cauchy_area':raw.encode(),'weighted_diagonal_ratio':ratio.encode()})
    eta=Z;row_errors=[]
    for contact in internal['contacts']:
        i,j=contact['edge'];vertex=V[contact['source']];edge=b.sub(V[j],V[i]);m0=b.cross(edge,r0);h0=b.dot(m0,V[i])
        # All center orientations above are positive; no sign changes.
        b.require(h0>Z,'raw center edge orientation unexpected')
        f0=contact['torque'];mx=b.cross(edge,(O,Z,Z));my=b.cross(edge,(Z,O,Z))
        hx=b.dot(mx,V[i]);hy=b.dot(my,V[i]);hmin=h0-F(delta)*(abs(hx)+abs(hy))
        b.require(hmin>Z,'entire-box support height lower bound fails')
        fx=b.cross(vertex,mx);fy=b.cross(vertex,my)
        numerator=sum((abs(fx[k]-f0[k]*hx)+abs(fy[k]-f0[k]*hy) for k in range(3)),Z)
        error=F(delta)*numerator/hmin;eta=max(eta,error);row_errors.append(error.encode())
    b.require(eta<F(Q(1,500)),'center torque-row perturbation exceeds selected budget')
    b.require(internal['M']<F(28),'center positive-span coordinate bound not below28')
    b.require(1-Q(28,500)>Q(3*28*17,16*100),'local1/100 Cayley absorption gate fails')
    # The width lemma is affine on all originals, independently rechecked.
    B=3*p**2;S=p+2;support_gaps=[]
    for m in [Z,p/12]:
        d=(p,-O,-m);h=B+p*m
        b.require(max(b.dot(d,v) for v in V)==h,'whole affine original width support failed')
        support_gaps.extend(h-b.dot(d,v) for v in V)
    b.require(p*S-B*(p/12)>Z,'whole receiving width derivative fails')
    width_max=4*(B+p*(p/12))**2/(S+(p/12)**2)
    width_limit=(20+32*p)*(1-Q(10,11664))
    b.require(width_max<width_limit,'entire affine width interval fails all-source filter')
    b.require(940+1520*p>F(Q(583,10)**2),'source-filter positive-root area comparison fails')
    # Fresh matching/exposed row gates; source positive frame is derived, not assumed.
    b.require(F(Q(99,100))*(1-F(Q(9,2))*F(Q(7,100)))>F(Q(3,5)),'nonequatorial receiver height separation fails')
    b.require(Q(36,125)<Q(11,20)**2 and 1-Q(3,25)**2>Q(24,25)**2,'source matching error/singular gates fail')
    match_eps=Q(11,20);sing=Q(24,25)
    b.require(2*a*sing>F(2*match_eps) and 2*c*sing-2*a>F(2*match_eps),'unequal-side matching gates fail')
    b.require(F(4*match_eps)*(a+c)+F(4*match_eps**2)<4*a*c*sing,'proper matching determinant gate fails')
    roll0=(match_eps+Q(9,256)+Q(9,484))/Q(22,5)
    b.require(Q(1,8)+roll0<Q(4,15),'full initial frame4/15 gate fails')
    b.require(F(Q(17,4))>p**3 and p**3<F(Q(9,2)) and F(Q(22,5)**2)<radius2<F(20),'original radius bounds fail')
    coord_max=Q(81,2000)
    b.require(max(r[k] for r in corners for k in [0,1])<F(coord_max),'receiver coordinate bound fails')
    b.require(1+coord_max/(1+zmin)<ell,'both-row actual transverse factor fails')
    b.require((p**3-c)*zmin-(p**3-1)*ell*coord_max>Z,'both actual target coordinate faces fail')
    # Use slightly sharper raw X max for the uniform bootstrap: r_x<=101/2500;
    # in particular BOTH normalized coordinates are below81/2000.
    # Step bounds below account for that common bound, not a hidden1/25 gate.
    q1=3*coord_max
    b.require(1-q1*q1>Q(99,100)**2,'first row diagonal99/100 fails')
    factor1=ell/(1-Q(17,4)*q1/(1+Q(99,100)))
    b.require(factor1<Q(7,5),'first refined actual-row factor7/5 fails')
    q2=Q(7,5)*coord_max
    b.require(1-q2*q2>Q(499,500)**2,'second row diagonal499/500 fails')
    factor2=ell/(1-Q(17,4)*q2/(1+Q(499,500)))
    b.require(factor2<Q(7,6),'second refined actual-row factor7/6 fails')
    q3=Q(7,6)*coord_max
    factor3=ell/(1-Q(17,4)*q3/(1+Q(499,500)))
    b.require(factor3<Q(23,20),'final actual-row factor23/20 fails')
    # Coordinate-radius branches: even the larger near-diagonal ratio leaves both source coordinates positive.
    b.require(Q(23,20)<1+Q(40,41),'source coordinate positivity branch fails')
    # Source |u|<3/50, entire interpolation z>99/100.
    b.require(Q(23,400)<Q(3,50) and 1-Q(3,50)**2>zmin*zmin,'interpolation root bound fails')
    dz=Q(3,50)/zmin
    A=Q(3,25)/(1+zmin)+Q(3,50)**2*dz/(1+zmin)**2
    b.require(A<Q(1,16) and dz<Q(1,16),'shortest-transport block derivative bounds fail')
    b.require(1+Q(1,256)<Q(101,100)**2,'full proper transport op/Frobenius bound fails')
    du=Q(123,16000)
    height=Q(1,400)+Q(123,800)*Q(53,250)
    b.require(height<Q(9,250) and radius2-F(Q(1,400)**2)>F(Q(22,5)**2),'actual equatorial minus radius/drift bound fails')
    roll_bound=(Q(9,250)+Q(9,2)*du/16)/Q(22,5)
    b.require(roll_bound<Q(9,1000) and Q(101,100)*du<Q(1,125),'final full proper roll or normal transport gate fails')
    b.require(Q(1,117)**2*(4-Q(17,1000)**2)>Q(17,1000)**2 and Q(1,117)<Q(1,100),'final derived Cayley chart lies outside selected local domain')
    return {'raw_center':b.encode(r0),'raw_half_width':str(delta),'corner_records':global_records,
            'all_original_edge_support_corner_comparisons':4*16*60,
            'incident_endpoint_equalities_at_corners':4*16*2,
            'strict_original_edge_support_corner_comparisons':4*16*58,'all_original_width_endpoint_comparisons':120,
            'maximum_normalized_torque_row_l1_perturbation':eta.encode(),'torque_row_perturbation_budget':'1/500',
            'local_center_polytope_M_upper':'28','local_Cayley_infinity_exclusion_radius':'1/100',
            'both_source_coordinate_upper_factor':'23/20','bootstrap_factors':[str(x) for x in [factor1,factor2,factor3]],
            'source_receiver_tangent_distance_upper':str(du),'shortest_transport_equatorial_block_derivative_upper':str(A),
            'proper_roll_operator_error_upper':str(roll_bound),'derived_relative_Cayley_Euclidean_upper':'1/117',
            'all_source_width_margin':(width_limit-width_max).encode()},corners


def nonmembership(b,V,corners):
    Z=b.ZERO;group=b.proper_group(V);records=[]
    for g in sorted(group,key=lambda g:b.key(tuple(x for row in g for x in row))):
        for sign in [1,-1]:
            raw=[b.act(tuple(zip(*g)),tuple(sign*x for x in r)) for r in corners]
            for family,major,minor in [('W',12,20),('P',20,2)]:
                for j in [0,1]:
                    k=1-j
                    tests=[('nonpositive_z',-max(x[2] for x in raw)),
                           ('negative_major',-max(x[j] for x in raw)),
                           ('major_above_limit',min(major*x[j]-x[2] for x in raw)),
                           ('positive_minor_above_slope',min(minor*x[k]-x[j] for x in raw)),
                           ('negative_minor_above_slope',min(-minor*x[k]-x[j] for x in raw))]
                    valid=[(name,gap) for name,gap in tests if gap>Z or (name=='nonpositive_z' and gap==Z)]
                    require(valid,'box may meet a proper prior W/P image')
                    name,gap=valid[0];records.append({'sign':sign,'family':family,'coordinate':j,'violated_affine_requirement':name,'margin':gap.encode()})
    require(len(group)==60 and len(records)==480,'complete proper/sign/family nonmembership inventory differs')
    return {'proper_maps':len(group),'signed_group_family_affine_nonmembership_certificates':len(records),
            'all_normalized_box_images_disjoint_from_W_union_P':True,
            'certificate_sha256':hashlib.sha256((json.dumps(records,sort_keys=True)+'\n').encode()).hexdigest()}


def proof_controls(b,internal):
    F,Z,O,p=b.F,b.ZERO,b.ONE,b.PHI;rejected=[]
    def reject(name,f):
        try:f()
        except ValueError:rejected.append(name);return
        raise ValueError('damaged proof control accepted:'+name)
    selected=internal['selected'];weights=internal['weights'];rows=internal['unique']
    def balance(ws):
        require(len(ws)==len(selected),'positive-balance inventory incomplete')
        require(all(w>Z for w in ws),'positive-balance weight not positive')
        require(tuple(sum((w*rows[i][j] for i,w in zip(selected,ws)),Z) for j in range(3))==(Z,Z,Z),'positive-balance identities fail')
    reject('omitted_positive_spanning_row',lambda:balance(weights[:-1]))
    reject('altered_positive_spanning_weight',lambda:balance([weights[0]+F(Q(1,1000)),*weights[1:]]))
    reject('negative_equilibrium_weight',lambda:balance([-weights[0],*weights[1:]]))
    reject('oversized_torque_perturbation',lambda:require(1-28*Q(1,100)>Q(3*28*17,16*100),'nonlinear absorption fails'))
    reject('uncovered_global_Cayley_chart',lambda:require(Q(1,90)<Q(1,100),'source-motion chart outside certified local domain'))
    reject('unjustified_source_coordinate_factor',lambda:require(Q(6068,5325)<Q(11,10),'both-row bootstrap does not prove claimed factor'))
    q=tuple(F(Q(x,200000)) for x in [12,14,11]);contact=internal['contacts'][0]
    v=internal['V'][contact['source']];m=contact['normal'];torque=contact['torque']
    violation=b.dot(torque,q)+b.dot(m,q)*b.dot(v,q)-b.dot(q,q)
    require(violation>Z and max(abs(x) for x in q)<F(Q(1,100)),'prior Gram-gap pose not excluded by actual contact')
    return {'damaged_controls_rejected':rejected,'explicit_prior_gap_endpoint_polynomial_excess':violation.encode(),
            'positive_spanning_balance_checked':True}


def verify():
    b,dependency=replay();F,Z,O,p=b.F,b.ZERO,b.ONE,b.PHI
    center,internal=center_data(b);V=internal['V']
    require(len(V)==60 and set(V)=={b.neg(v) for v in V},'named central original inventory differs')
    E={(sx*p**2,sy*(2+p),Z) for sx,sy in product([-1,1],repeat=2)}
    require(E=={v for v in V if v[2]==Z},'equatorial original inventory differs')
    require(all(b.dot(v,v)==7+8*p for v in V),'common original sphere differs')
    for j in [0,1]:
        face={v for v in V if v[j]==p**3};wanted=set()
        for s,t in product([-1,1],repeat=2):
            v=[Z,Z,F(t)];v[j]=p**3;v[1-j]=F(s);wanted.add(tuple(v))
        require(face==wanted and max(v[j] for v in V if v not in face)==2+p,'actual exposed four-original coordinate face differs')
    planes,facet_counts=b.complete_facets(V);C,_,cauchy_counts=b.area_generators(V,planes)
    require(len(planes)==62 and len(C)==31,'physical Cauchy geometry differs')
    patch,corners=patch_data(b,internal,C)
    membership=nonmembership(b,V,corners);controls=proof_controls(b,internal)
    return {'agent':'six-rupert-3','role':'researcher',
            'claim':'all closed RID fits on the signed proper images of the full diagonal receiving box are congruent; global problem unresolved',
            'dependency_replay':dependency,'original_count':len(V),'physical_facets':len(planes),'physical_Cauchy_generators':len(C),
            'complete_facet_enumeration':facet_counts,'center_certificate':center,'whole_receiving_box':patch,
            'strict_prior_cover_nonmembership':membership,'controls':controls}


if __name__=='__main__':
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--emit',action='store_true',help='derive fresh record without comparing expected.json')
    args=parser.parse_args();data=(json.dumps(verify(),indent=2,sort_keys=True)+'\n').encode()
    if not args.emit:require(data==(HERE/'expected.json').read_bytes(),'whole expected record differs')
    sys.stdout.buffer.write(data)
