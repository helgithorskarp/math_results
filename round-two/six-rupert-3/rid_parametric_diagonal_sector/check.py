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
U=Q(1,25);DELTA=Q(3,10);SCALED=Q(7,5);ROLL=Q(8);QUAD=Q(17,16)

def require(condition,message):
    if not condition:raise ValueError(message)

def replay():
    pin=json.loads((HERE/'DEPENDENCIES.json').read_text())
    directory=(HERE/pin['directory']).resolve()
    require(set(pin['sha256'])=={'check.py','PROOF.md','DEPENDENCIES.json','expected.json'},'filter inventory differs')
    for name,digest in pin['sha256'].items():
        require(hashlib.sha256((directory/name).read_bytes()).hexdigest()==digest,'published filter changed:'+name)
    require('field' not in sys.modules,'arithmetic loaded before verification')
    spec=spec_from_file_location('sector_filter_dependency',directory/'check.py')
    f=module_from_spec(spec);spec.loader.exec_module(f)
    result=f.verify();output=(json.dumps(result,indent=2,sort_keys=True)+'\n').encode()
    require(output==(directory/'expected.json').read_bytes(),'whole filter expected record differs')
    five=json.loads((directory/'DEPENDENCIES.json').read_text());fold=(directory/five['directory']).resolve()
    original=json.loads((fold/'DEPENDENCIES.json').read_text());base=(fold/original['directory']).resolve()
    require(Path(sys.modules['field'].__file__).resolve()==base/'field.py','verified arithmetic location differs')
    for name,digest in original['sha256'].items():
        require(hashlib.sha256((base/name).read_bytes()).hexdigest()==digest,'original source changed after replay:'+name)
    spec=spec_from_file_location('sector_original_geometry',base/'verify.py')
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
    records=[]
    for number,r in enumerate(corners):
        heights=[];gaps=[]
        for i,j in zip(cycle,cycle[1:]+cycle[:1]):
            m=b.cross(b.sub(V[j],V[i]),r);h=b.dot(m,V[i]);heights.append(h)
            require(h>Z,'actual edge support height not positive')
            require(b.dot(m,V[j])==h,'literal incident endpoint equality differs')
            off=[h-b.dot(m,v) for index,v in enumerate(V) if index not in [i,j]];gaps.extend(off)
            require(min(off)>=Z and (number==0 or min(off)>Z),'actual full-original edge support fails')
        raw=b.brightness_raw(C,r)
        require(raw<F(Q(1171,20)),'receiving raw-area bound fails')
        records.append({'raw_corner':b.encode(r),'raw_Cauchy_area':raw.encode(),
                        'minimum_support_height':min(heights).encode(),'minimum_offendpoint_support_margin':min(gaps).encode()})
    N=Q(36,25);coord=Q(41,1000);rawsum=Q(41,500);zmin=Q(99,100)
    require(Z<k-F(DELTA) and 1+(k+F(DELTA))**2<F(N*N),'whole-sector receiving tilt bound fails')
    require(F(zmin*zmin)*(1+F((N*U)**2))<O,'receiving axial root99/100 fails')
    require(1+(N*U)**2<Q(242,241)**2,'receiving chord1/11 fails')
    require(F(U)<F(coord) and (k+F(DELTA))*F(U)<F(coord),'both raw coordinate maxima fail')
    require((1+k+F(DELTA))*F(U)<F(rawsum),'nonequatorial receiver raw sum fails')
    require(F(zmin)*(1-F(Q(9,2)*rawsum))>F(Q(3,5)),'nonequatorial receiving height separation fails')
    ratio=Q(7,4)
    require(F(1/ratio)<c*(k-F(DELTA))/a and c*(k+F(DELTA))/a<F(ratio),'weighted diagonal ratio interval fails')
    require(c*F(DELTA)<F(Q(9,8)) and 2*a+c*F(DELTA)<F(Q(13,2)),'equatorial plus/minus height coefficients fail')
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
            'receiving_tangent_coefficient':str(N),'receiving_positive_axial_lower':str(zmin),
            'raw_coordinate_upper':str(coord),'raw_coordinate_sum_upper':str(rawsum),
            'weighted_diagonal_ratio_factor':str(ratio),'receiving_width_endpoint_records':endpointrecords,
            'receiving_width_shared_attaining_original':b.encode(attainer),
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
    N=Q(36,25);ratio=Q(7,4);eps=Q(3,20);du=eps*ratio*N
    coord=Q(41,1000);ell=Q(41,40);zmin=Q(99,100)
    require(Q(36,125)<Q(11,20)**2 and 1-Q(3,25)**2>Q(24,25)**2,'matching radius/singular gates fail')
    match=Q(11,20);sigma=Q(24,25)
    require(2*a*sigma>F(2*match) and 2*c*sigma-2*a>F(2*match),'unequal-side matching fails')
    require(F(4*match)*(a+c)+F(4*match**2)<4*a*c*sigma,'proper matching determinant fails')
    require(Q(1,8)+(match+Q(9,256)+Q(9,484))/Q(22,5)<Q(4,15),'initial full frame4/15 fails')
    require(F(Q(17,4))>p**3 and p**3<F(Q(9,2)) and F(Q(22,5)**2)<radius2<F(20),'original radius constants fail')
    require(1+coord/(1+zmin)<ell,'both actual row transverse factor fails')
    require((p**3-c)*zmin-(p**3-1)*ell*coord>Z,'both actual exposed coordinate faces fail')
    require(1-Q(4,15)**2>Q(9,10)**2,'initial actual source row diagonal fails')
    require(ell/(1-Q(9,2)*Q(4,15)/(1+Q(9,10)))<3,'first actual row factor3 fails')
    q1=3*coord;require(1-q1*q1>zmin*zmin,'row99/100 positive root fails')
    f1=ell/(1-Q(17,4)*q1/(1+zmin));require(f1<Q(7,5),'refined row7/5 factor fails')
    q2=Q(7,5)*coord;require(1-q2*q2>Q(499,500)**2,'row499/500 positive root fails')
    f2=ell/(1-Q(17,4)*q2/(1+Q(499,500)));require(f2<Q(117,100),'refined row117/100 factor fails')
    q3=Q(117,100)*coord;f3=ell/(1-Q(17,4)*q3/(1+Q(499,500)));require(f3<Q(23,20),'final actual row23/20 factor fails')
    require(Q(23,20)<1+1/ratio,'positive source-coordinate branch fails')
    T=Q(1,15);source_tilt=Q(23,20)*N*U
    require(source_tilt<T and 1-T*T>zmin*zmin,'shortest-transport root domain fails')
    dz=T/zmin;A=2*T/(1+zmin)+T*T*dz/(1+zmin)**2
    require(A<Q(7,100) and dz<Q(7,100),'shortest proper transport block derivative fails')
    require(1+Q(7,100)**2<Q(101,100)**2,'proper transport two-singular-values bound fails')
    height=Q(9,8)+eps*ratio*Q(13,2);require(height<Q(23,8),'matched minus-original source height fails')
    roll=(Q(23,8)+Q(9,2)*du*Q(7,100))/Q(22,5);L=Q(7,10)
    require(roll<L,'actual arbitrary planar roll bound fails')
    beta=Q(351,1000);require(4-(L*U)**2>0 and beta**2*(4-(L*U)**2)>L**2,'roll Cayley positive-root comparison fails')
    H=Q(101,100)*du;h=Q(39,200)
    require(4-(H*U)**2>0 and h**2*(4-(H*U)**2)>H**2,'normal transport Cayley positive-root comparison fails')
    sden=Q(499,500);require(1-(T/(1+zmin))**2>sden,'normal transport Cayley denominator fails')
    sdiff=1/(1+zmin)+T*dz/(1+zmin)**2;require(sdiff<Q(51,100),'shortest-transport Cayley derivative fails')
    hz=N/(1+zmin)*Q(51,100)*du/sden;require(hz<Q(3,20),'normal transport axial Cayley coefficient fails')
    D=Q(4999,5000);require(1-beta*h*U**2>D,'full relative Cayley composition denominator fails')
    qxy=(h+(beta*N+beta*h)*U)/D;qz=(beta+(Q(3,20)+beta*h)*U)/D
    bxy=Q(11,50);bz=Q(3,8);require(qxy<bxy and qz<bz,'derived initial anisotropic relative-motion enclosure fails')
    square=2*bxy*bxy+bz*bz;improved_z=ROLL*QUAD*square*U
    require(improved_z<bxy,'actual roll contacts do not bootstrap the full motion')
    closure=3*SCALED*QUAD*bxy;require(closure==Q(3927,4000)<1,'complete nonlinear contact closure fails')
    return {'actual_source_coordinate_upper_factor':'23/20','row_bootstrap_factors':[str(x) for x in [f1,f2,f3]],
            'source_receiver_tangent_difference_coefficient':str(du),'source_tangent_upper':str(source_tilt),
            'positive_axial_lower':str(zmin),'proper_transport_equatorial_block_Lipschitz':str(A),
            'matched_minus_original_source_height_coefficient':str(height),'arbitrary_roll_operator_coefficient':str(roll),
            'roll_Cayley_scalar_coefficient':str(beta),'normal_transport_Cayley_norm_coefficient':str(h),
            'normal_transport_Cayley_axial_coefficient':str(hz),'relative_Cayley_composition_denominator_lower':str(D),
            'initial_relative_Cayley_xy_coefficient':str(qxy),'initial_relative_Cayley_z_coefficient':str(qz),
            'initial_relative_Cayley_squared_norm_coefficient':str(square),'unscaled_roll_dual_total_weight_upper':str(ROLL),
            'improved_relative_Cayley_z_coefficient':str(improved_z),'derived_relative_Cayley_infinity_coefficient':str(bxy),
            'scaled_dual_total_weight_upper':str(SCALED),'quadratic_constant':str(QUAD),
            'nonzero_fit_absorption_factor':str(closure),'axis_handling':'actual row supports force both transverse row norms to zero'}

def new_receiver_witness(b,V):
    F,Z,O,p=b.F,b.ZERO,b.ONE,b.PHI;group=b.proper_group(V);records=[];oldbox=[]
    r=(F(Q(1,50)),(2+p)/250,O)
    lo=(F(Q(99,2500)),(39+20*p)/2500);hi=(F(Q(101,2500)),(41+20*p)/2500)
    for g in sorted(group,key=lambda g:b.key(tuple(x for row in g for x in row))):
        for sign in [1,-1]:
            x=b.act(tuple(zip(*g)),tuple(sign*a for a in r))
            for family,major,minor in [('W',12,20),('P',20,2)]:
                for j in [0,1]:
                    k=1-j
                    tests=[('nonpositive_z',-x[2]),('negative_major',-x[j]),('major_above_limit',major*x[j]-x[2]),
                           ('positive_minor_above_slope',minor*x[k]-x[j]),('negative_minor_above_slope',-minor*x[k]-x[j])]
                    valid=[(name,gap) for name,gap in tests if gap>Z or (name=='nonpositive_z' and gap==Z)]
                    require(valid,'new witness may lie in a prior proper W/P image')
                    name,gap=valid[0];records.append({'sign':sign,'family':family,'coordinate':j,'violated_affine_requirement':name,'margin':gap.encode()})
            tests=[('nonpositive_z',-x[2]),('x_below',lo[0]*x[2]-x[0]),('x_above',x[0]-hi[0]*x[2]),
                   ('y_below',lo[1]*x[2]-x[1]),('y_above',x[1]-hi[1]*x[2])]
            valid=[(name,gap) for name,gap in tests if gap>Z or (name=='nonpositive_z' and gap==Z)]
            require(valid,'new witness may lie in a prior proper diagonal patch image')
            name,gap=valid[0];oldbox.append({'sign':sign,'violated_affine_requirement':name,'margin':gap.encode()})
    require(len(group)==60 and len(records)==480 and len(oldbox)==120,'complete witness nonmembership inventory differs')
    digest=lambda a:hashlib.sha256((json.dumps(a,sort_keys=True)+'\n').encode()).hexdigest()
    return {'raw_receiver':b.encode(r),'proper_maps':len(group),'W_P_affine_nonmembership_cases':len(records),
            'diagonal_patch_affine_nonmembership_cases':len(oldbox),'W_P_certificate_sha256':digest(records),
            'diagonal_patch_certificate_sha256':digest(oldbox),'whole_sector_disjointness_from_prior_covers_claimed':False}

def proof_controls(b,internal,box,frame,geometry):
    Z=b.ZERO;rejected=[]
    def reject(name,f):
        try:f()
        except ValueError:rejected.append(name);return
        raise ValueError('damaged mathematical control accepted:'+name)
    # Alter sufficient mathematical budgets, not interpreter/resource settings.
    reject('scaled_mass6/5',lambda:require(all((c['D']*Q(6,5)-sum(c['N'],P(0))).bounds(box)[0]>=Z for c in internal),'scaled mass is unjustified'))
    rollcerts=[c for c in internal if c['axis']==2]
    reject('unscaled_roll_mass1',lambda:require(all((c['D']-sum(c['rollN'],P(0))).bounds(box)[0]>=Z for c in rollcerts),'roll mass is unjustified'))
    c=internal[0]
    reject('negative_dual_denominator',lambda:require((-c['D']).bounds(box)[0]>Z,'dual denominator not positive'))
    facetmax=b.F(*map(Q,geometry['maximum_normalized_facet_normal_squared']))
    reject('unjustified_Ball5',lambda:require(facetmax<b.F(Q(1,25)),'facet norms do not certify Ball5'))
    reject('source_coordinate_factor11/10',lambda:require(Q(frame['row_bootstrap_factors'][2])<Q(11,10),'actual rows do not prove11/10'))
    reject('motion_infinity_coefficient1/4',lambda:require(3*SCALED*QUAD*Q(1,4)<1,'nonlinear contact closure fails'))
    return {'damaged_mathematical_controls_rejected':rejected}

def verify():
    b,dependency=replay();V,C,cycle,geometry=original_geometry(b)
    triangle,_=receiving_triangle(b,V,C,cycle)
    duals,internal,box=contact_duals(b,V,cycle);frame=all_source_frame_gates(b)
    witness=new_receiver_witness(b,V);controls=proof_controls(b,internal,box,frame,geometry)
    return {'agent':'six-rupert-3','role':'researcher',
            'claim':'all closed RID fits on signed proper images of the full parametric diagonal sector are congruent; global problem unresolved',
            'dependency_replay':dependency,'named_original_geometry':geometry,'whole_receiving_triangle':triangle,
            'actual_contact_duals':duals,'all_source_motion_and_nonlinear_closure':frame,
            'strictly_new_receiver_witness':witness,'controls':controls}

if __name__=='__main__':
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--emit',action='store_true',help='derive a fresh record without comparing expected.json')
    args=parser.parse_args();data=(json.dumps(verify(),sort_keys=True,separators=(',',':'))+'\n').encode()
    if not args.emit:require(data==(HERE/'expected.json').read_bytes(),'whole expected record differs')
    sys.stdout.buffer.write(data)
