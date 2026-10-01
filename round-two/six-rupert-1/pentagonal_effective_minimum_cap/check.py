#!/usr/bin/env python3
"""Exact global pose localization for a pentagonal minimum receiving cap.

All proof decisions use rational quotient-field coefficients and outward
rational bounds at the positive named root; no floating solver is used.
"""
from pathlib import Path
from fractions import Fraction as F
import argparse,copy,hashlib,importlib.util,json,sys

HERE=Path(__file__).resolve().parent
AREA=HERE.parent/'pentagonal_area_spectrum'
LOCAL=HERE.parent/'pentagonal_minimum_contact_cap'
HASHES={
    AREA:{'check.py':'64f847094441915167ce42601fe418d9332b39474bedf63f075c76cbfdccd534',
          'polygons.json':'9cf8972b021a148625d037adfe17c86d0ee45fd61811c0737d73ed71ceec79ec',
          'expected.json':'0368f8a13f76e5e3e745735dab9d0dd4df954c59c98a0f0e783359220c06cf9d'},
    LOCAL:{'check.py':'c63d858250b1044a8d098cc9dc8fa75d97d5e332844432a3f18b2bf35183adce',
           'certificate.json':'4c648190614ed61adb5d4f74572696f3b9c5bd18b1bfa3ba76204ae8fa5c26a6',
           'expected.json':'511dbcb6573cf3ca43bfa8aa08264129e5015d6de6c79c1fc6fdde175417bb69'},
}
for folder,files in HASHES.items():
    for name,digest in files.items():
        if hashlib.sha256((folder/name).read_bytes()).hexdigest()!=digest:
            raise ValueError('proof dependency changed: '+str(folder/name))
sys.path.insert(0,str(AREA))
import check as A
spec=importlib.util.spec_from_file_location('pentagonal_local_contact_parent',LOCAL/'check.py')
C=importlib.util.module_from_spec(spec);spec.loader.exec_module(C)
M,V,Z=A.M,A.V,A.ZERO
ONE=M.K.coerce(1)


def rational(text):
    V.require(type(text) is str,'rational scalar must be a string')
    value=F(text)
    V.require(str(value)==text,'rational scalar is not canonical')
    return value


def setup():
    geometry=A.build_geometry()
    root,scale,mats,points,areas=geometry
    charts=A.enumerate_charts(areas,root)
    parent=A.audit_extrema(root,scale,mats,areas,A.permutation_group(areas),charts)
    wanted=json.loads((AREA/'expected.json').read_text())
    V.require(all(wanted[k]==v for k,v in parent.items()),'global area parent record mismatch')
    local=C.audit(json.loads((LOCAL/'certificate.json').read_text()),geometry)
    V.require(local==json.loads((LOCAL/'expected.json').read_text()),'local contact parent record mismatch')
    raw=charts[57]['normal']
    N=tuple(c/raw[0] for c in raw)
    norm2=M.dot(N,N)
    cycle=json.loads((AREA/'polygons.json').read_text())['minimum']['ccw_literal_vertex_indices']
    probes=[M.cross(M.sub(points[j],points[i]),N)
            for i,j in zip(cycle,cycle[1:]+cycle[:1])]
    heights=[M.dot(m,points[i]) for m,i in zip(probes,cycle)]
    for m,h in zip(probes,heights):
        V.require(A.field_sign(h,root)>0,'receiver support height')
        V.require(A.field_sign(4*h.square()-M.dot(m,m),root)>0,
                  'minimum shadow does not contain the radius-one-half disk')
    minimum=charts[57]
    V.require(A.field_sign(minimum['support2']-9*minimum['norm2'],root)>0,
              'minimum area not above three')
    maximum=next(c for c in charts[37]['corners'] if c['choices']==(1,-1))
    V.require(A.field_sign(16-maximum['norm2'],root)>0,'maximum area not below four')
    return {'geometry':geometry,'charts':charts,'parent_area':parent,'local':local,
            'N':N,'norm2':norm2,'cycle':cycle,'probes':probes,'heights':heights}


def decoded_rows(data,state):
    root,_,_,points,_=state['geometry']
    expected={'format','duals','circle_left_shift','tangent_lower_bound',
              'source_normal_chord','receiver_normal_chord','roll_chord'}
    V.require(type(data) is dict and set(data)==expected,'certificate fields')
    V.require(type(data['format']) is int and data['format']==1,'format version')
    rows=data['duals']
    V.require(type(rows) is list and len(rows)>=3,'dual polygon rows')
    polygon=[];pair_count=0
    for row in rows:
        V.require(type(row) is dict and set(row)=={'receiving_edges','source_vertices'},'dual row fields')
        edges,vertices=row['receiving_edges'],row['source_vertices']
        V.require(type(edges) is list and len(edges) in (2,3) and
                  all(type(i) is int and 0<=i<26 for i in edges) and
                  len(set(edges))==len(edges),'receiving edge choices')
        V.require(type(vertices) is list and len(vertices)==len(edges) and
                  all(type(i) is int and 0<=i<92 for i in vertices),'source vertex choices')
        normals=[state['probes'][i] for i in edges]
        if len(edges)==2:
            pair_count+=1
            V.require(M.cross(normals[0],normals[1])==(Z,Z,Z) and
                      A.field_sign(M.dot(normals[0],normals[1]),root)<0,
                      'dual pair is not exactly opposite')
            at=next(i for i,c in enumerate(normals[0]) if c!=Z)
            sign=A.field_sign(normals[0][at],root)
            weights=[-normals[1][at]*sign,normals[0][at]*sign]
        else:
            weights=[M.dot(state['N'],M.cross(normals[j],normals[k]))
                     for j,k in ((1,2),(2,0),(0,1))]
            if A.field_sign(weights[0],root)<0:
                weights=[-w for w in weights]
        V.require(all(A.field_sign(w,root)>0 for w in weights),'dual weight not positive')
        for k in range(3):
            V.require(sum((w*n[k] for w,n in zip(weights,normals)),Z)==Z,
                      'actual translation does not cancel')
        D=sum((w*state['heights'][i] for w,i in zip(weights,edges)),Z)
        V.require(A.field_sign(D,root)>0,'dual height denominator')
        x=sum((w*M.dot(n,points[i]) for w,n,i in zip(weights,normals,vertices)),Z)/D
        y=sum((w*M.dot(n,M.cross(state['N'],points[i]))
               for w,n,i in zip(weights,normals,vertices)),Z)/D
        V.require(A.field_sign(ONE-x,root)>=0,'a self-shadow dual exceeds one at identity')
        polygon.append((x,y))
    V.require(len(set(polygon))==len(polygon),'repeated exact dual point')
    return polygon,pair_count


def audit(data,state):
    root,_,_,_,_=state['geometry']
    polygon,pairs=decoded_rows(data,state)
    a,s,delta,rho,zeta=[rational(data[k]) for k in
                      ('circle_left_shift','tangent_lower_bound','source_normal_chord',
                       'receiver_normal_chord','roll_chord')]
    V.require(a>0 and 0<s<=1 and 0<zeta<s/2,'disk/tangent/roll scalars')
    V.require(0<rho<delta and delta< F(1,4),'normal scalars')
    norm2=state['norm2'];supports=0;right=[]
    for i,(x,y) in enumerate(polygon):
        u,v=polygon[(i+1)%len(polygon)]
        for k,(p,q) in enumerate(polygon):
            if k in (i,(i+1)%len(polygon)):
                continue
            determinant=(u-x)*(q-y)-(v-y)*(p-x)
            V.require(A.field_sign(determinant,root)>0,'dual polygon is not strictly convex CCW')
            supports+=1
        shifted_det=(x+a)*v-(u+a)*y
        V.require(A.field_sign(shifted_det,root)>0,'disk center is outside a directed edge')
        difference=shifted_det.square()-(1+a)**2*(norm2*(u-x).square()+(v-y).square())
        if difference==Z:
            V.require(x==u==ONE,'unexpected non-right disk tangency')
            V.require(A.field_sign(y,root)<0 and A.field_sign(v,root)>0,
                      'right contact edge does not straddle zero')
            V.require(A.field_sign(y.square()-s*s*norm2,root)>0 and
                      A.field_sign(v.square()-s*s*norm2,root)>0,
                      'right contact span is below the claimed tangent bound')
            right.append(i)
        else:
            V.require(A.field_sign(difference,root)>0,'shifted disk leaves the dual polygon')
    V.require(len(right)==1,'exactly one right tangent edge required')
    kappa=1-delta*delta/2
    minimum=state['charts'][57]
    count=0
    for chart in state['charts']:
        if chart['index']==58:
            continue
        gap=kappa*kappa*chart['support2']*minimum['norm2']-minimum['support2']*chart['norm2']
        V.require(A.field_sign(gap,root)>0,'nonminimum facet does not clear m/kappa')
        count+=1
    area_margin=F(3,2)*delta*delta-4*rho
    gamma=min(s*zeta/4,a*s*s/8)
    roll_margin=gamma-16*delta
    pose_margin=F(1,10000)-(4*delta+2*zeta)
    V.require(area_margin>0,'global source-area localization margin')
    V.require(roll_margin>0,'full-circle roll localization margin')
    V.require(2*delta+zeta<1 and pose_margin>0,'localized proper motion exceeds parent angle box')
    V.require(rho<=F(1,1000000),'receiving cap exceeds parent local normal box')
    return {'agent':'six-rupert-1','role':'researcher',
            'status':'COMPLETE_EXACT_FINITE_PREMISES_UNFORMALIZED_BRIDGES',
            'dual_polygon_corners':len(polygon),'positive_balanced_pairs':pairs,
            'positive_balanced_triples':len(polygon)-pairs,
            'exact_three_coordinate_translation_balances':3*len(polygon),
            'strict_dual_polygon_supports':supports,
            'strict_shifted_disk_edges':len(polygon)-1,'exact_right_tangent_edges':1,
            'circle_center':[str(-a),'0'],'circle_radius':str(1+a),
            'right_tangent_span_lower_bound':str(s),
            'minimum_shadow_radius_one_half_supports':26,
            'source_normal_localizer_chord':str(delta),'source_area_kappa':str(kappa),
            'nonminimum_facet_localizers':count,
            'global_source_area_margin':str(area_margin),
            'roll_localizer_chord':str(zeta),'roll_circle_gain':str(gamma),
            'roll_perturbation_margin':str(roll_margin),'proper_pose_angle_margin':str(pose_margin),
            'all_source_closed_receiver_cap_chord':str(rho),
            'receiver_minimum_projective_axes':30,
            'allowed_fits':'scale1, proper body symmetry, zero physical projected translation',
            'full_rupert_status':'OPEN',
            'parent_global_area_record_fields_replayed':len(state['parent_area']),
            'parent_global_area_checks':state['parent_area'],
            'parent_local_contact_checks':state['local'],
            'parent_sha256':{p.name:hashes for p,hashes in HASHES.items()}}


def negative_controls(original,state):
    tests=[]
    a=copy.deepcopy(original);a['duals'][0]['source_vertices'][0]=True;tests.append(('boolean_source_vertex',a))
    a=copy.deepcopy(original);a['duals'][0]={'receiving_edges':[0,1],'source_vertices':[21,57]};tests.append(('nonopposite_pair',a))
    a=copy.deepcopy(original);a['duals']=[a['duals'][0]]+list(reversed(a['duals'][1:]));tests.append(('reversed_dual_boundary',a))
    a=copy.deepcopy(original);a['circle_left_shift']='1/10';tests.append(('excessive_disk_shift',a))
    a=copy.deepcopy(original);a['tangent_lower_bound']='1/2';tests.append(('overstated_tangent_span',a))
    rejected=[]
    for label,data in tests:
        try:
            audit(data,state)
        except (ValueError,ZeroDivisionError):
            rejected.append(label)
        else:
            raise ValueError('damaged certificate accepted: '+label)
    return rejected


def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--emit',action='store_true')
    parser.add_argument('--negative-controls',action='store_true')
    parser.add_argument('--discovery',action='store_true',help='author fixture generation; all mathematical gates remain active')
    args=parser.parse_args()
    data=json.loads((HERE/'certificate.json').read_text())
    state=setup();out=audit(data,state)
    if not args.discovery:
        V.require(out==json.loads((HERE/'expected.json').read_text()),'expected record changed')
    if args.negative_controls:
        out=dict(out,negative_controls_rejected=negative_controls(data,state))
    if args.emit:
        print(json.dumps(out,sort_keys=True,indent=2))
    else:
        print('PASS: effective minimum receiving cap with all source motions and translations.')


if __name__=='__main__':main()
