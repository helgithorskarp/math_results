#!/usr/bin/env python3
"""Exact finite hypotheses for all-source closed RID rigidity on a sector.

PROOF.md supplies the continuum geometry. All signs are in ordered
Q(phi); scalar root gates use rational squared comparisons. No floats,
solver, sampled motion search, or inferred nonexistence occurs.
"""
from pathlib import Path
from fractions import Fraction as Q
from importlib.util import module_from_spec,spec_from_file_location
from itertools import product
import argparse,hashlib,json,sys
from poly import P,dot,cross,determinant

HERE=Path(__file__).resolve().parent
U=Q(1,16);DELTA=Q(3,10);SCALED=Q(3,2);ROLL=Q(4);QUAD=Q(17,16)

def require(condition,message):
    if not condition:raise ValueError(message)

def replay():
    pin=json.loads((HERE/'DEPENDENCIES.json').read_text())
    directory=(HERE/pin['directory']).resolve()
    require(set(pin['sha256'])=={'check.py','PROOF.md','DEPENDENCIES.json','expected.json'},'filter inventory differs')
    for name,digest in pin['sha256'].items():
        require(hashlib.sha256((directory/name).read_bytes()).hexdigest()==digest,'published filter changed:'+name)
    require('field' not in sys.modules,'arithmetic loaded before verification')
    spec=spec_from_file_location('wider_filter_dependency',directory/'check.py')
    f=module_from_spec(spec);spec.loader.exec_module(f)
    result=f.verify();output=(json.dumps(result,indent=2,sort_keys=True)+'\n').encode()
    require(output==(directory/'expected.json').read_bytes(),'whole filter expected record differs')
    five=json.loads((directory/'DEPENDENCIES.json').read_text());fold=(directory/five['directory']).resolve()
    original=json.loads((fold/'DEPENDENCIES.json').read_text());base=(fold/original['directory']).resolve()
    require(Path(sys.modules['field'].__file__).resolve()==base/'field.py','verified arithmetic location differs')
    for name,digest in original['sha256'].items():
        require(hashlib.sha256((base/name).read_bytes()).hexdigest()==digest,'original source changed after replay:'+name)
    spec=spec_from_file_location('wider_original_geometry',base/'verify.py')
    b=module_from_spec(spec);spec.loader.exec_module(b)
    return b,{'filter_whole_expected_bytes':len(output),'filter_whole_expected_sha256':hashlib.sha256(output).hexdigest(),
              'source_commit':pin['source_commit'],'graph':pin['graph_ref'],
              'transitive_replay':'complete filter, fivefold and original brightness records'}

def original_geometry(b):
    F,Z,O,p=b.F,b.ZERO,b.ONE,b.PHI;V=b.vertices()
    require(len(V)==60 and set(V)=={b.neg(v) for v in V},'named central original inventory differs')
    require(all(b.dot(v,v)==7+8*p for v in V),'common original sphere differs')
    E={(sx*p**2,sy*(2+p),Z) for sx,sy in product([-1,1],repeat=2)}
    require(E=={v for v in V if v[2]==Z},'equatorial original inventory differs')
    require(all(abs(v[2])>=O for v in V if v not in E),'nonequatorial original axial gap differs')
    for j in [0,1]:
        face={v for v in V if v[j]==p**3};wanted=set()
        for s,t in product([-1,1],repeat=2):
            v=[Z,Z,F(t)];v[j]=p**3;v[1-j]=F(s);wanted.add(tuple(v))
        require(face==wanted and max(v[j] for v in V if v not in face)==2+p,'actual coordinate face differs')
    planes,counts=b.complete_facets(V);C,_,_=b.area_generators(V,planes)
    require(len(planes)==62 and len(C)==31,'complete physical facet/Cauchy inventory differs')
    facetmax=max(b.dot(n,n) for n in planes)
    require(facetmax<F(Q(1,16)),'global closed Ball4 is not inside the solid')
    r=(F(U),(2+p)*F(U)/5,O);u=(-r[1],r[0],Z);v=b.cross(r,u);points={}
    for i,x in enumerate(V):points.setdefault((b.dot(u,x),b.dot(v,x)),[]).append(i)
    keys=sorted(points)
    def turn(a,b,c):return (b[0]-a[0])*(c[1]-a[1])-(b[1]-a[1])*(c[0]-a[0])
    def half(seq):
        h=[]
        for x in seq:
            while len(h)>=2 and turn(h[-2],h[-1],x)<=Z:h.pop()
            h.append(x)
        return h
    hull=half(keys)[:-1]+half(reversed(keys))[:-1]
    require(all(len(points[x])==1 for x in hull),'center hull original not unique')
    cycle=[points[x][0] for x in hull]
    require(cycle==[48,36,54,56,38,53,46,18,11,23,5,3,21,6,13,41],'complete receiving cycle differs')
    return V,C,cycle,{'originals':len(V),'physical_facets':len(planes),'physical_Cauchy_generators':len(C),
                     'complete_facet_enumeration':counts,'maximum_normalized_facet_normal_squared':facetmax.encode(),
                     'global_inscribed_closed_ball_radius':'4','center_complete_receiving_cycle':cycle}

def receiving_triangle(b,V,C,cycle):
    F,Z,O,p=b.F,b.ZERO,b.ONE,b.PHI;a=p**2;c=2+p;k=c/5
    corners=[(Z,Z,O),(F(U),(k-F(DELTA))*F(U),O),(F(U),(k+F(DELTA))*F(U),O)]
    A0=12+28*p;D0=8+8*p;D1=4+2*p;alpha=D0-D1*k
    E={v for v in V if v[2]==Z};records=[]
    for number,r in enumerate(corners):
        heights=[];gaps=[]
        for i,j in zip(cycle,cycle[1:]+cycle[:1]):
            m=b.cross(b.sub(V[j],V[i]),r);h=b.dot(m,V[i]);heights.append(h)
            require(h>Z,'actual edge support height not positive')
            require(b.dot(m,V[j])==h,'literal incident endpoint equality differs')
            off=[h-b.dot(m,v) for index,v in enumerate(V) if index not in [i,j]];gaps.extend(off)
            require(min(off)>=Z and (number==0 or min(off)>Z),'actual full-original edge support fails')
        raw=b.brightness_raw(C,r)
        envelope=A0+alpha*r[0]+D1*r[1]
        require(raw==envelope,'raw Cauchy area does not equal the affine envelope at a corner')
        signed=[b.dot(r,v) if v[2]>Z else -b.dot(r,v) for v in V if v not in E]
        require(min(signed)>F(Q(13,20)),'actual nonequatorial raw height separation fails')
        records.append({'raw_corner':b.encode(r),'raw_Cauchy_area':raw.encode(),
                        'affine_raw_area_envelope':envelope.encode(),
                        'minimum_support_height':min(heights).encode(),'minimum_offendpoint_support_margin':min(gaps).encode(),
                        'minimum_signed_nonequatorial_raw_height':min(signed).encode()})
    lo=k-F(DELTA);hi=k+F(DELTA)
    require(Z<lo and alpha>Z and D1>Z and A0>Z,'physical-area monotonicity signs fail')
    derivative_u=D0-D1*DELTA-A0*(1+hi**2)*U
    derivative_slope=D1*(1+U**2)-(A0*U+alpha*U**2)*hi
    require(derivative_u>Z,'normalized area envelope is not increasing in raw major coordinate')
    require(derivative_slope>Z,'outer normalized area envelope is not increasing in slope')
    rawmax=A0+(D0+D1*DELTA)*U;normmax2=1+(1+hi**2)*U**2
    area_square_margin=F(Q(1171,20)**2)*normmax2-rawmax**2
    require(rawmax>Z and area_square_margin>Z,'receiving physical-area positive-root bound fails')
    N=Q(36,25);coord=Q(319,5000);rzmin=Q(199,200)
    require(1+hi**2<F(N*N),'whole-sector receiving tilt bound fails')
    require(F(rzmin*rzmin)*(1+F((N*U)**2))<O,'receiving axial root199/200 fails')
    require(1+(N*U)**2<Q(242,241)**2,'receiving chord1/11 fails')
    require(U<coord and (hi*U)**2<F(coord**2)*normmax2,'both physical coordinate maxima fail')
    require(1+(N*U)**2<Q(101,100)**2,'receiver normalization root101/100 fails')
    require(Q(13,20)/Q(101,100)>Q(3,5),'nonequatorial physical height separation fails')
    ratio=Q(7,4)
    require(F(1/ratio)<c*lo/a and c*hi/a<F(ratio),'weighted diagonal ratio interval fails')
    require(c*F(DELTA)<F(Q(9,8)),'equatorial receiving minus height coefficient fails')
    norm_difference_gate=F(Q(7,4)**2)-(1+c*DELTA/a)**2*(1+k*k)
    require(norm_difference_gate>Z,'weighted coordinate maximum vector norm fails')
    radius2=7+8*p
    require(radius2-F((Q(9,8)*U)**2)>F(Q(22,5)**2),'receiving minus original projected radius fails')
    B=3*p**2;S=p+2;endpointrecords=[]
    for m in [Z,p/12]:
        d=(p,-O,-m);h=B+p*m
        require(max(b.dot(d,v) for v in V)==h,'complete original width support fails')
        endpointrecords.append({'m':m.encode(),'support':h.encode(),'minimum_original_gap':min(h-b.dot(d,v) for v in V).encode()})
    attainer=(2*p,-a,-p)
    require(attainer in V and all(b.dot((p,-O,-m),attainer)==B+p*m for m in [Z,p/12]),'one actual original does not attain the whole affine width interval')
    require(Z<p-k-F(DELTA) and (p-k+F(DELTA))*F(U)<p/12,'whole-sector width parameter interval fails')
    require(p*S-B*(p/12)>Z,'width derivative positive gate fails')
    width_max=4*(B+p*(p/12))**2/(S+(p/12)**2);limit=(20+32*p)*(1-Q(10,11664))
    require(width_max<limit,'receiving width all-source filter fails')
    require(940+1520*p>F(Q(583,10)**2),'receiving/source area comparison fails')
    return {'raw_major_interval':['0',str(U)],'slope_offset_interval':[str(-DELTA),str(DELTA)],'raw_triangle_corners':records,
            'all_original_support_corner_comparisons':3*16*60,'literal_endpoint_equalities':3*16*2,
            'strict_offendpoint_tip_comparisons':2*16*58,'axis_offendpoint_comparisons':16*58,
            'nonequatorial_signed_raw_corner_comparisons':3*(len(V)-len(E)),
            'affine_raw_area_envelope_coefficients':{'constant':A0.encode(),'raw_x':alpha.encode(),'raw_y':D1.encode()},
            'area_envelope_u_derivative_numerator_lower':derivative_u.encode(),
            'outer_area_envelope_slope_derivative_numerator_lower':derivative_slope.encode(),
            'upper_tip_raw_area':rawmax.encode(),'upper_tip_raw_normal_squared':normmax2.encode(),
            'physical_area_upper':'1171/20','physical_area_positive_root_margin':area_square_margin.encode(),
            'receiving_tangent_coefficient':str(N),'receiving_positive_axial_lower':str(rzmin),
            'physical_coordinate_upper':str(coord),'nonequatorial_raw_height_lower':'13/20',
            'normalization_upper':'101/100','weighted_diagonal_ratio_factor':str(ratio),
            'weighted_coordinate_maximum_vector_norm_coefficient':'7/4',
            'weighted_coordinate_maximum_vector_squared_margin':norm_difference_gate.encode(),
            'receiving_width_endpoint_records':endpointrecords,'receiving_width_shared_attaining_original':b.encode(attainer),
            'all_source_width_margin':(limit-width_max).encode()},corners

def bernstein_record(polynomial,box):
    lower,upper,coeffs=polynomial.bounds(box)
    return {'polynomial':polynomial.encode(),'minimum':lower.encode(),'maximum':upper.encode(),
            'Bernstein_coefficients':[a.encode() for a in coeffs]}

def contact_duals(b,V,cycle):
    F,Z,O,p=b.F,b.ZERO,b.ONE,b.PHI;P.F=F
    u=P({(1,0):O});rho=P({(0,1):O});r=(u,(P((2+p)/5)+rho)*u,P(1));raw=[]
    for i,j in zip(cycle,cycle[1:]+cycle[:1]):
        m=cross(b.sub(V[j],V[i]),r);h=dot(m,V[i])
        for source in [i,j]:raw.append({'edge':[i,j],'source':source,'F':cross(V[source],m),'h':h})
    require(len(raw)==32,'complete endpoint contact inventory differs')
    selectors=[(0,-1,[1,9,10]),(0,1,[8,12,13]),(1,-1,[2,7,8]),
               (1,1,[9,10,14]),(2,-1,[3,9,13]),(2,1,[0,1,10])]
    box=(Q(0),U,-DELTA,DELTA);records=[];internal=[]
    for axis,sign,indices in selectors:
        rows=[raw[i]['F'] for i in indices];heights=[raw[i]['h'] for i in indices]
        D=determinant(*rows);target=tuple(sign*u if j==axis else P(0) for j in range(3))
        beta=[dot(target,cross(rows[1],rows[2])),dot(target,cross(rows[2],rows[0])),dot(target,cross(rows[0],rows[1]))]
        require(all(sum((beta[i]*rows[i][j] for i in range(3)),P(0))==D*target[j] for j in range(3)),'raw Cramer vector identities fail')
        numerators=[beta[i]*heights[i] for i in range(3)];order=D.order_u()
        require(order<999 and all(a.order_u()>=order for a in numerators),'uncancelled denominator pole')
        D=D.cancel_u(order);numerators=[a.cancel_u(order) for a in numerators]
        orientation=1
        if D.evaluate(U,Q(0))<Z:orientation=-1;D=-D;numerators=[-a for a in numerators]
        d=bernstein_record(D,box);ns=[bernstein_record(a,box) for a in numerators]
        gap=bernstein_record(D*SCALED-sum(numerators,P(0)),box)
        require(D.bounds(box)[0]>Z,'dual denominator not uniformly positive')
        require(all(a.bounds(box)[0]>=Z for a in numerators),'dual weight numerator not uniformly nonnegative')
        require((D*SCALED-sum(numerators,P(0))).bounds(box)[0]>=Z,'scaled dual total weight budget fails')
        record={'axis':axis,'sign':sign,'original_contacts':[{'index':i,'edge':raw[i]['edge'],'source':raw[i]['source']} for i in indices],
                'cancelled_common_u_order':order,'common_orientation':orientation,'denominator':d,
                'weight_numerators':ns,'scaled_mass_gap':gap,'scaled_total_weight_upper':str(SCALED)}
        rollnums=None
        if axis==2:
            require(all(a.order_u()>=1 for a in numerators),'unscaled roll numerator lacks a u factor')
            rollnums=[a.cancel_u(1) for a in numerators]
            require(all(a.bounds(box)[0]>=Z for a in rollnums),'unscaled roll weight numerator sign fails')
            require((D*ROLL-sum(rollnums,P(0))).bounds(box)[0]>=Z,'unscaled roll total weight budget fails')
            record['unscaled_roll_weight_numerators']=[bernstein_record(a,box) for a in rollnums]
            record['unscaled_roll_mass_gap']=bernstein_record(D*ROLL-sum(rollnums,P(0)),box)
            record['unscaled_roll_total_weight_upper']=str(ROLL)
        records.append(record);internal.append({'axis':axis,'sign':sign,'D':D,'N':numerators,'rollN':rollnums})
    return {'polynomial_variables':['raw_major_u','slope_offset_rho'],'closed_Bernstein_rectangle':[str(x) for x in box],
            'actual_endpoint_constraints':len(raw),'coordinate_dual_families':len(records),'unscaled_roll_dual_families':2,
            'Bernstein_basis_reexpanded_exactly':True,'certificates':records},internal,box

def all_source_frame_gates(b):
    F,Z,O,p=b.F,b.ZERO,b.ONE,b.PHI;a=p**2;c=2+p;radius2=7+8*p
    N=Q(36,25);ratio=Q(7,4);factor=Q(249,200);eps=factor-1;du=eps*Q(7,4)
    coord=Q(319,5000);ell=Q(129,125);rzmin=Q(199,200);zmin=Q(99,100)
    require(Q(36,125)<Q(11,20)**2 and 1-Q(3,25)**2>Q(24,25)**2,'matching radius/singular gates fail')
    match=Q(11,20);sigma=Q(24,25)
    require(2*a*sigma>F(2*match) and 2*c*sigma-2*a>F(2*match),'unequal-side matching fails')
    require(F(4*match)*(a+c)+F(4*match**2)<4*a*c*sigma,'proper matching determinant fails')
    require(Q(1,8)+(match+Q(9,256)+Q(9,484))/Q(22,5)<Q(4,15),'initial full frame4/15 fails')
    require(F(Q(106,25))>p**3 and p**3<F(Q(9,2)) and F(Q(22,5)**2)<radius2<F(20),'original radius constants fail')
    require(1+coord/(1+rzmin)<ell,'both actual row transverse factor fails')
    require((p**3-c)*rzmin-(p**3-1)*ell*coord>Z,'both actual exposed coordinate faces fail')
    require(1-Q(4,15)**2>Q(9,10)**2,'initial actual source row diagonal fails')
    require(ell/(1-Q(9,2)*Q(4,15)/(1+Q(9,10)))<3,'first actual row factor3 fails')
    sequence=[Q(3),Q(7,4),Q(11,8),Q(51,40),Q(5,4),factor]
    diagonals=[Q(49,50),Q(99,100),Q(199,200),Q(249,250),Q(249,250)]
    rows=[]
    for previous,nextfactor,diagonal in zip(sequence,sequence[1:],diagonals):
        tau=previous*coord
        require(1-tau*tau>diagonal*diagonal,'actual row positive-root bootstrap fails')
        denominator=1-Q(106,25)*tau/(1+diagonal)
        require(denominator>0,'actual row rearrangement denominator fails')
        bound=ell/denominator
        require(bound<nextfactor,'refined actual row factor fails')
        rows.append({'previous_factor':str(previous),'positive_diagonal_lower':str(diagonal),
                     'refined_factor':str(bound),'next_upper_factor':str(nextfactor)})
    require(factor<1+1/ratio,'positive source-coordinate branch fails')
    T=Q(23,200);source_tilt=factor*N*U
    require(source_tilt<T and 1-T*T>zmin*zmin,'shortest-transport root domain fails')
    dz=T/zmin;A=2*T/(1+zmin)+T*T*dz/(1+zmin)**2;block=Q(3,25)
    require(A<block and dz<block,'shortest proper transport block derivative fails')
    require(1+block**2<Q(101,100)**2,'proper transport two-singular-values bound fails')
    height=c*DELTA+2*eps*(a+c*DELTA)
    require(height<F(3),'matched minus-original source height fails')
    roll=(Q(3)+Q(9,2)*du*block)/Q(22,5);L=Q(3,4)
    require(roll<L,'actual arbitrary planar roll bound fails')
    beta=Q(47,125);require(4-(L*U)**2>0 and beta**2*(4-(L*U)**2)>L**2,'roll Cayley positive-root comparison fails')
    H=Q(101,100)*du;h=Q(109,500)
    require(4-(H*U)**2>0 and h**2*(4-(H*U)**2)>H**2,'normal transport Cayley positive-root comparison fails')
    sden=Q(249,250);require(1-(T/(1+zmin))**2>sden,'normal transport Cayley denominator fails')
    sdiff=1/(1+zmin)+T*dz/(1+zmin)**2
    hz=N/(1+zmin)*sdiff*du/sden;require(hz<Q(17,100),'normal transport axial Cayley coefficient fails')
    D=Q(999,1000);require(1-beta*h*U**2>D,'full relative Cayley composition denominator fails')
    qxy=(h+(beta*N+beta*h)*U)/D;qz=(beta+(Q(17,100)+beta*h)*U)/D
    bxy=Q(13,50);bz=Q(2,5);require(qxy<bxy and qz<bz,'derived initial anisotropic relative-motion enclosure fails')
    square=bxy*bxy+bz*bz;improved_z=ROLL*QUAD*square*U
    root2=Q(71,50);require(root2*root2>2,'vector ell1 positive-root upper fails')
    closure=SCALED*QUAD*(root2*bxy+improved_z)
    require(closure==Q(701199,1024000)<1,'complete vector nonlinear contact closure fails')
    return {'actual_source_coordinate_upper_factor':str(factor),'row_bootstrap':rows,
            'source_receiver_tangent_difference_coefficient':str(du),'source_tangent_upper':str(source_tilt),
            'positive_axial_lower':str(zmin),'proper_transport_equatorial_block_Lipschitz':str(A),
            'matched_minus_original_source_height_coefficient':height.encode(),'matched_minus_height_upper':'3',
            'arbitrary_roll_operator_coefficient':str(roll),'roll_Cayley_scalar_coefficient':str(beta),
            'normal_transport_Cayley_norm_coefficient':str(h),'normal_transport_Cayley_axial_coefficient':str(hz),
            'relative_Cayley_composition_denominator_lower':str(D),'initial_relative_Cayley_xy_VECTOR_coefficient':str(qxy),
            'initial_relative_Cayley_z_coefficient':str(qz),'relative_Cayley_xy_VECTOR_upper':str(bxy),
            'initial_relative_Cayley_z_upper':str(bz),'initial_relative_Cayley_squared_norm_coefficient':str(square),
            'unscaled_roll_dual_total_weight_upper':str(ROLL),'improved_relative_Cayley_z_coefficient':str(improved_z),
            'sqrt2_rational_upper':str(root2),'scaled_dual_total_weight_upper':str(SCALED),'quadratic_constant':str(QUAD),
            'vector_ell1_nonzero_fit_absorption_factor':str(closure),
            'axis_handling':'actual row supports force both transverse row norms to zero before division by u'}

def new_receiver_witness(b,V):
    F,Z,O,p=b.F,b.ZERO,b.ONE,b.PHI;group=b.proper_group(V);records=[];oldsector=[];oldbox=[];k=(2+p)/5
    r=(F(Q(3,50)),k*F(Q(3,50)),O)
    lo=(F(Q(99,2500)),(39+20*p)/2500);hi=(F(Q(101,2500)),(41+20*p)/2500)
    for g in sorted(group,key=lambda g:b.key(tuple(x for row in g for x in row))):
        for sign in [1,-1]:
            x=b.act(tuple(zip(*g)),tuple(sign*a for a in r))
            for family,major,minor in [('W',12,20),('P',20,2)]:
                for j in [0,1]:
                    t=1-j
                    tests=[('nonpositive_z',-x[2]),('negative_major',-x[j]),('major_above_limit',major*x[j]-x[2]),
                           ('positive_minor_above_slope',minor*x[t]-x[j]),('negative_minor_above_slope',-minor*x[t]-x[j])]
                    valid=[(name,gap) for name,gap in tests if gap>Z or (name=='nonpositive_z' and gap==Z)]
                    require(valid,'new witness may lie in a prior proper W/P image')
                    name,gap=valid[0];records.append({'sign':sign,'family':family,'coordinate':j,'violated_affine_requirement':name,'margin':gap.encode()})
            tests=[('nonpositive_z',-x[2]),('negative_major',-x[0]),('major_above_limit',25*x[0]-x[2]),
                   ('below_slope',(k-F(DELTA))*x[0]-x[1]),('above_slope',x[1]-(k+F(DELTA))*x[0])]
            valid=[(name,gap) for name,gap in tests if gap>Z or (name=='nonpositive_z' and gap==Z)]
            require(valid,'new witness may lie in a prior proper u<=1/25 sector image')
            name,gap=valid[0];oldsector.append({'sign':sign,'violated_affine_requirement':name,'margin':gap.encode()})
            tests=[('nonpositive_z',-x[2]),('x_below',lo[0]*x[2]-x[0]),('x_above',x[0]-hi[0]*x[2]),
                   ('y_below',lo[1]*x[2]-x[1]),('y_above',x[1]-hi[1]*x[2])]
            valid=[(name,gap) for name,gap in tests if gap>Z or (name=='nonpositive_z' and gap==Z)]
            require(valid,'new witness may lie in a prior proper small diagonal patch image')
            name,gap=valid[0];oldbox.append({'sign':sign,'violated_affine_requirement':name,'margin':gap.encode()})
    contained=[]
    for x,y in product([lo[0],hi[0]],[lo[1],hi[1]]):
        require(Z<x<F(U) and (k-F(DELTA))*x<y<(k+F(DELTA))*x,'full old raw box is not in new raw triangle')
        contained.append({'raw_corner':b.encode((x,y,O)),'upper_major_margin':(F(U)-x).encode(),
                          'lower_slope_margin':(y-(k-F(DELTA))*x).encode(),'upper_slope_margin':((k+F(DELTA))*x-y).encode()})
    require(Q(1,25)<U and len(group)==60 and len(records)==480 and len(oldsector)==120 and len(oldbox)==120,'complete coverage comparison inventory differs')
    digest=lambda a:hashlib.sha256((json.dumps(a,sort_keys=True)+'\n').encode()).hexdigest()
    return {'raw_receiver':b.encode(r),'proper_maps':len(group),'W_P_affine_nonmembership_cases':len(records),
            'previous_sector_affine_nonmembership_cases':len(oldsector),'diagonal_patch_affine_nonmembership_cases':len(oldbox),
            'W_P_certificate_sha256':digest(records),'previous_sector_certificate_sha256':digest(oldsector),
            'diagonal_patch_certificate_sha256':digest(oldbox),'previous_u1_25_sector_wholly_contained':True,
            'previous_small_box_wholly_contained_by_affine_corner_gates':contained,
            'all_older_receiving_covers_wholly_contained_claimed':False}

def proof_controls(b,internal,box,frame,geometry,triangle):
    Z=b.ZERO;rejected=[]
    def reject(name,f):
        try:f()
        except ValueError:rejected.append(name);return
        raise ValueError('damaged mathematical control accepted:'+name)
    # These alter mathematical sufficient gates, never runtime/resource controls.
    reject('scaled_mass6/5',lambda:require(all((c['D']*Q(6,5)-sum(c['N'],P(0))).bounds(box)[0]>=Z for c in internal),'scaled mass is unjustified'))
    rollcerts=[c for c in internal if c['axis']==2]
    reject('unscaled_roll_mass1',lambda:require(all((c['D']-sum(c['rollN'],P(0))).bounds(box)[0]>=Z for c in rollcerts),'roll mass is unjustified'))
    c=internal[0]
    reject('negative_dual_denominator',lambda:require((-c['D']).bounds(box)[0]>Z,'dual denominator not positive'))
    facetmax=b.F(*map(Q,geometry['maximum_normalized_facet_normal_squared']))
    reject('unjustified_Ball5',lambda:require(facetmax<b.F(Q(1,25)),'facet norms do not certify Ball5'))
    reject('source_coordinate_factor11/10',lambda:require(Q(frame['row_bootstrap'][-1]['refined_factor'])<Q(11,10),'actual rows do not prove11/10'))
    reject('tilt_VECTOR_coefficient1/2',lambda:require(SCALED*QUAD*(Q(71,50)*Q(1,2)+ROLL*QUAD*(Q(1,2)**2+Q(2,5)**2)*U)<1,'vector nonlinear closure fails'))
    raw=b.F(*map(Q,triangle['upper_tip_raw_area']))
    reject('discarding_physical_area_normalization',lambda:require(raw<b.F(Q(1171,20)),'raw area does not satisfy physical-area bound'))
    p=b.PHI;a=p**2;c=2+p;k=c/5
    reject('weighted_maximum_vector_coefficient6/5',lambda:require((1+c*DELTA/a)**2*(1+k*k)<b.F(Q(6,5)**2),'weighted coordinate norm coefficient unjustified'))
    return {'damaged_mathematical_controls_rejected':rejected}

def verify():
    b,dependency=replay();V,C,cycle,geometry=original_geometry(b)
    triangle,_=receiving_triangle(b,V,C,cycle)
    duals,internal,box=contact_duals(b,V,cycle);frame=all_source_frame_gates(b)
    witness=new_receiver_witness(b,V);controls=proof_controls(b,internal,box,frame,geometry,triangle)
    return {'agent':'six-rupert-3','role':'researcher',
            'claim':'all closed RID fits on signed proper images of the larger u<=1/16 diagonal sector are congruent; global problem unresolved',
            'dependency_replay':dependency,'named_original_geometry':geometry,'whole_receiving_triangle':triangle,
            'actual_contact_duals':duals,'all_source_motion_and_nonlinear_closure':frame,
            'strictly_new_receiver_witness':witness,'controls':controls}

if __name__=='__main__':
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--emit',action='store_true',help='derive a fresh record without comparing expected.json')
    args=parser.parse_args();data=(json.dumps(verify(),sort_keys=True,separators=(',',':'))+'\n').encode()
    if not args.emit:require(data==(HERE/'expected.json').read_bytes(),'whole expected record differs')
    sys.stdout.buffer.write(data)
