#!/usr/bin/env python3
"""Exact hypotheses for all-source RID endpoint closed-rigidity caps.

PROOF.md supplies the support-torque, quadratic row-correction, averaged
radial order, local area, proper-branch and all-source continuum arguments.
No exploratory hull search, floating-point decision or solver is needed.
"""
from fractions import Fraction as Q
from importlib.util import module_from_spec,spec_from_file_location
from itertools import combinations
from pathlib import Path
import argparse
import copy
import hashlib
import json
import sys

HERE=Path(__file__).resolve().parent
DELTA=Q(1,15000)


def require(condition,message):
    if not condition:
        raise ValueError(message)


def replay():
    pin=json.loads((HERE/'DEPENDENCIES.json').read_text())
    parent=(HERE/pin['directory']).resolve()
    require(set(pin['sha256'])=={'check.py','expected.json','PROOF.md','DEPENDENCIES.json'},'prerequisite list differs')
    for name,sha in pin['sha256'].items():
        require(hashlib.sha256((parent/name).read_bytes()).hexdigest()==sha,'tube prerequisite changed:'+name)
    require('field' not in sys.modules,'unverified arithmetic already imported')
    spec=spec_from_file_location('endpoint_tube_dependency',parent/'check.py')
    tube=module_from_spec(spec);spec.loader.exec_module(tube)
    result=tube.verify();output=(json.dumps(result,indent=2,sort_keys=True)+'\n').encode()
    require(output==(parent/'expected.json').read_bytes(),'complete tube expected record differs')
    # The tube has verified this field path and all transitive geometry hashes.
    base_path=Path(sys.modules['field'].__file__).resolve().parent
    arc=json.loads((parent/'DEPENDENCIES.json').read_text())['arcs']
    current=(parent/arc['directory']).resolve()
    for _ in range(3):
        pin2=json.loads((current/'DEPENDENCIES.json').read_text())
        current=(current/pin2['directory']).resolve()
    require(current==base_path and hashlib.sha256((base_path/'verify.py').read_bytes()).hexdigest()==pin2['sha256']['verify.py'],'replayed brightness source differs')
    spec=spec_from_file_location('endpoint_brightness_geometry',base_path/'verify.py')
    b=module_from_spec(spec);spec.loader.exec_module(b)
    return b,result,hashlib.sha256(output).hexdigest()


def read_vector(b,encoded):
    require(len(encoded)==3 and all(len(q)==2 for q in encoded),'malformed field vector')
    return tuple(b.F(*q) for q in encoded)


def tetrahedron(b,record,radius=Q(3,20),norm_upper=Q(4),gap_lower=Q(1,10)):
    require(record['axis'] in ['x','y'] and len(record['probes'])==4 and len(record['positive_stress_weights'])==4,'four actual probes required')
    r=tuple(b.F(x) for x in record['raw_reference']);require(b.dot(r,r)==b.F(145),'reference normalization differs')
    required=(b.ONE,b.ZERO,b.F(12)) if record['axis']=='x' else (b.ZERO,b.ONE,b.F(12))
    require(r==required,'wrong named endpoint reference')
    V=b.vertices();T=[];gaps=[];probe_data=[]
    for p in record['probes']:
        v,m=read_vector(b,p['vertex']),read_vector(b,p['probe'])
        require(v in V and b.dot(m,r)==b.ZERO,'probe original or actual row plane differs')
        require(b.dot(m,m)<b.F(norm_upper**2),'probe norm bound fails')
        gap=min(b.dot(m,b.sub(v,w)) for w in V if w!=v)
        require(gap>b.F(gap_lower),'unique actual-original support gap fails')
        t=b.cross(v,m);T.append(t);gaps.append(gap)
        probe_data.append({'vertex':b.encode(v),'probe':b.encode(m),'torque':b.encode(t),'squared_probe_norm':b.dot(m,m).encode(),'minimum_actual_support_gap':gap.encode()})
    weights=[b.F(*w) for w in record['positive_stress_weights']]
    require(all(w>b.ZERO for w in weights),'stress is not strictly positive')
    require(all(sum((w*t[k] for w,t in zip(weights,T)),b.ZERO)==b.ZERO for k in range(3)),'actual torque balance fails')
    determinant=b.dot(b.sub(T[1],T[0]),b.cross(b.sub(T[2],T[0]),b.sub(T[3],T[0])))
    require(determinant!=b.ZERO,'torque tetrahedron is degenerate')
    distances=[]
    for indices in combinations(range(4),3):
        a,c,d=[T[i] for i in indices];normal=b.cross(b.sub(c,a),b.sub(d,a));h=b.dot(normal,a)
        require(b.dot(normal,normal)>b.ZERO and h*h>b.F(radius**2)*b.dot(normal,normal),'origin-facet distance does not contain torque ball')
        distances.append((h*h/b.dot(normal,normal)).encode())
    return {'axis':record['axis'],'raw_reference':record['raw_reference'],'actual_support_comparisons':4*59,'probes':probe_data,'positive_stress_weights':[w.encode() for w in weights],'affine_torque_determinant':determinant.encode(),'four_origin_facet_squared_distances':distances,'torque_ball_radius_lower':str(radius)}


def geometry_gates(b,C,delta=DELTA):
    F,Z,phi=b.F,b.ZERO,b.PHI;V=b.vertices()
    require(len(C)==31 and len(set(C))==31,'complete physical area inventory differs')
    require(0<delta<=Q(1,1000),'unsupported endpoint domain')
    require(7+8*phi<F(20) and phi**3<F(Q(9,2)),'physical body bound differs')
    require(Q(1473,5632)+Q(25,22)*delta<Q(4,15),'initial full-roll bound lost')
    require(Q(144,145)>Q(99,100)**2 and Q(99,100)-delta>Q(24,25),'actual oriented normal determinant bound lost')
    require(Q(45,116)>Q(3,5)**2 and (Q(3,5)-5*delta)**2>Q(1,3)>Q(36,125),'all-original radial match separation lost')
    require(250*delta<Q(1,50) and 180*delta+100*delta**2<Q(1,50),'all-source filter margins lost')
    A1sq=940+1520*phi;width_limit=(20+32*phi)*(1-Q(10,11664))
    require(A1sq>F(Q(583,10)**2),'endpoint area budget comparison fails')
    endpoint_values=[((F(28048)+44032*phi)/29,(F(2371108)+3159652*phi)/104401),
                     (F(Q(138704,145))+Q(43792,29)*phi,(F(2292772)+3127108*phi)/104401)]
    D=[c for c in C if c[2]==Z];require(len(D)==6,'six equatorial Cauchy generators required')
    require(all((c[2]*c[2])/b.dot(c,c)>F(Q(1,16)) for c in C if c[2]!=Z),'strong nonzero-z sign radius lost')
    records=[]
    for j in [0,1]:
        k=1-j;H=sum((abs(c[j]) for c in D),Z)
        require(H==(4+8*phi if j==0 else 8+4*phi) and F(14)<H<F(17),'mirror area coefficient differs')
        pure=sum((abs(c[k]) for c in D if c[j]==Z),Z);require(pure==F(4),'off-mirror pure coefficient is not four')
        signed=tuple(sum((c[i]*c[j].sign() for c in D if c[j]!=Z),Z) for i in range(3))
        require(signed==tuple(H if i==j else Z for i in range(3)),'nonzero equatorial sign sum differs')
        require(all(abs(c[j])*F(Q(1,13)-delta)>abs(c[k])*F(delta) for c in D if c[j]!=Z),'actual receiving signs do not persist')
        for c in D:
            reflected=tuple(-x if i==k else x for i,x in enumerate(c))
            require(reflected in D or b.neg(reflected) in D,'equatorial area is not reflection-even')
        area2,width2=endpoint_values[j]
        require(area2<F((Q(1171,20)-Q(1,50))**2) and width_limit-width2>F(Q(1,50)) and width2<F(81),'strengthened actual endpoint margins fail')
        gamma=phi**2 if j==0 else 2+phi;other=2+phi if j==0 else phi**2
        require(gamma**2>F(6) and other**2<F(20),'averaged radial coefficients differ')
        records.append({'axis':'x' if j==0 else 'y','H':H.encode(),'pure_other_coefficient':pure.encode(),'squared_area_gate_margin':(F((Q(1171,20)-Q(1,50))**2)-area2).encode(),'squared_width_margin':(width_limit-width2).encode(),'signed_equatorial_sum':b.encode(signed)})
    require(145<13**2 and Q(1,13)-delta>Q(1,14),'positive endpoint tilt lower bound lost')
    require(Q(3,25)+16*delta<Q(123,1000) and Q(1,8)+16*delta<Q(1,4),'corrected source leaves sign/derivative domain')
    require(1-Q(123,1000)**2>Q(24,25)**2 and 14-58*Q(123,1000)/Q(24,25)>6,'mirror area derivative lower bound six fails')
    require(Q(10,9)*14<16 and Q(16*14,1)/Q(19,10)<120,'quadratic retained-coordinate correction coefficient fails')
    require((58+17)*120==9000 and (21+9000*delta)/6<4,'quadratic area correction loses4delta upper tilt bound')
    require(Q(20,6)*16**2+2*120<1100 and 1+15400*delta<3,'averaged radial lower tilt bound loses3delta')
    require((2*Q(123,1000)/(2*Q(24,25)))**2+1<4 and 2*4+16+1==25,'proper locked-frame coefficient25 fails')
    require(6*25*delta<=Q(1,100) and delta<Q(1,1000),'all-source pose does not enter local torque box')
    require(2*20*Q(1,1000)<Q(1,10) and 20*(Q(1,1000)+Q(1,200))<Q(3,20),'local support-torque perturbation budget fails')
    return {'all_source_closed_receiving_chord_radius':str(delta),'local_box_receiving_chord_radius':'1/1000','local_box_relative_full_angle_radians':'1/100','original_support_gap_lower':'1/10','R_times_probe_norm_upper':'20','torque_ball_radius_lower':'3/20','nearly_fixed_row_chord_upper':'16delta','original_source_other_normal_coordinate_upper':'16delta','retained_mirror_normal_coordinate_error_upper':'120delta^2','source_area_correction_upper':'9000delta^2','actual_receiver_area_excess_upper':'21delta','averaged_equatorial_radius_squared_error_upper':'1100delta^2','source_tilt_magnitude_error_upper':'4delta','proper_frame_proximity_upper':'25delta','corrected_relative_full_angle_radians_upper':'150delta','mirror_area_derivative_lower':'6','endpoint_physical_margins':records}


def negative_controls(b,C,records):
    damaged=copy.deepcopy(records[0]);damaged['probes'][0]['probe']=[[-Q(x),-Q(y)] for x,y in damaged['probes'][0]['probe']]
    wrong=copy.deepcopy(records[0]);wrong['positive_stress_weights'][0]=['0','0']
    short=copy.deepcopy(records[0]);short['probes']=short['probes'][:-1]
    bad_normal=copy.deepcopy(records[0]);bad_normal['raw_reference']=[0,0,12]
    cases=[lambda:tetrahedron(b,damaged),lambda:tetrahedron(b,wrong),lambda:tetrahedron(b,short),lambda:tetrahedron(b,bad_normal),lambda:tetrahedron(b,records[0],radius=Q(1,5)),lambda:geometry_gates(b,C,delta=Q(1,1000)),lambda:geometry_gates(b,C[:-1])]
    for case in cases:
        try:case()
        except ValueError:continue
        raise ValueError('damaged contact/pose premise accepted')
    return len(cases)


def verify():
    b,parent,parent_sha=replay();V=b.vertices();planes,_=b.complete_facets(V);C,_,_=b.area_generators(V,planes)
    records=json.loads((HERE/'PROBES.json').read_text());require([r['axis'] for r in records]==['x','y'],'both endpoint certificates required')
    tetrahedra=[tetrahedron(b,r) for r in records];gates=geometry_gates(b,C)
    G=b.proper_group(V);orbits=[{b.act(g,tuple(b.F(x) for x in record['raw_reference'])) for g in G} for record in records]
    require(all(len(a)==60 and all(b.neg(n) in a for n in a) for a in orbits) and not orbits[0]&orbits[1],'proper endpoint orbits differ from two disjoint signed60sets')
    return {'agent':'six-rupert-3','role':'researcher','arithmetic':'ordered exact Q(phi) and rational budgets','proof_status':'written all-source closed endpoint-cap rigidity with exact support and linear-pose hypotheses','global_RID_Rupert_status':'unresolved','parent_whole_expected_bytes':3452,'parent_whole_expected_sha256':parent_sha,'inherited_local_expected_sha256':parent['complete_uniform_local_expected_sha256'],'actual_named_vertices':60,'proper_body_group_order':60,'directed_endpoint_centers':120,'unoriented_endpoint_axes':60,'total_new_actual_support_comparisons':sum(r['actual_support_comparisons'] for r in tetrahedra),'exact_tetrahedra':tetrahedra,'damaged_controls_rejected':negative_controls(b,C,records),**gates}


def main():
    parser=argparse.ArgumentParser();parser.add_argument('--emit',action='store_true');args=parser.parse_args()
    output=json.dumps(verify(),indent=2,sort_keys=True)+'\n'
    if not args.emit:require(output==(HERE/'expected.json').read_text(),'new whole expected output differs')
    print(output,end='')


if __name__=='__main__':main()
