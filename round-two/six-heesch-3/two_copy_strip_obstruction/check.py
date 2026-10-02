#!/usr/bin/env python3
"""Exact finite checks for the written uniform two-copy T_m obstruction.
Actual author six-heesch-3, researcher. Shared exact polygon primitives;
not a formalization, independent review or universal theorem by sampling.
Only the60-degree supplier matching forces the rotations used here.
"""
from dataclasses import dataclass
from fractions import Fraction as F
from pathlib import Path
import argparse,copy,json,resource,time
from hashlib import sha256
import geometry as b
HERE=Path(__file__).resolve().parent


def digest(value):
    return sha256(json.dumps(value,sort_keys=True,separators=(',',':')).encode()).hexdigest()


def direction_step(dx,dy):
    b.require(dx or dy,'zero boundary edge')
    if dy==0:return 0 if dx>0 else 6
    if dx==0:return 3 if dy>0 else 9
    if dx==3*dy:return 1 if dx>0 else 7
    if dx==dy:return 2 if dx>0 else 8
    if dx==-dy:return 4 if dy>0 else 10
    if dx==-3*dy:return 5 if dy>0 else 11
    raise ValueError('prototype edge outside thirty-degree directions')


def vertex_data(m):
    cycle,_=b.boundary(b.atoms(m))
    directions=[direction_step(*b.sub(cycle[(i+1)%len(cycle)],p)) for i,p in enumerate(cycle)]
    return [{'p':p,'start':directions[i],'end':(directions[i-1]+6)%12,
             'angle':6-((directions[i]-directions[i-1]+6)%12-6)} for i,p in enumerate(cycle)]


def compose(g,p):
    a,f,x,y=g;c,h,u,v=p
    tx,ty=b.point(g,(u,v))
    return (a+(-1 if f else 1)*c)%12,f^h,tx,ty


def hex_vertices(center):
    x,y=center
    return {(x+u,y+v) for u,v in ((-4,0),(-2,-2),(2,-2),(4,0),(2,2),(-2,2))}


@dataclass(frozen=True)
class Lin:
    """Exact affine form in independent real symbols m,r,j."""
    c:tuple
    def __post_init__(self):
        b.require(len(self.c)==4,'four affine coefficients required')
        object.__setattr__(self,'c',tuple(F(x) for x in self.c))
    @staticmethod
    def of(x):return x if isinstance(x,Lin) else Lin((x,0,0,0))
    def __add__(self,x):
        x=Lin.of(x);return Lin(tuple(a+z for a,z in zip(self.c,x.c)))
    __radd__=__add__
    def __neg__(self):return Lin(tuple(-x for x in self.c))
    def __sub__(self,x):return self+-Lin.of(x)
    def __rsub__(self,x):return Lin.of(x)+-self
    def __mul__(self,x):
        b.require(not isinstance(x,Lin),'nonlinear product outside affine identity checker')
        return Lin(tuple(a*F(x) for a in self.c))
    __rmul__=__mul__
    def __truediv__(self,x):return self*F(1,x)
    def serial(self):return [str(x) for x in self.c]

M=Lin((0,1,0,0));R=Lin((0,0,1,0));J=Lin((0,0,0,1))

def affine_point(pose,p):
    a,f,tx,ty=pose;x,y=map(Lin.of,p)
    if f:y=-y
    b.require(a in range(0,12,2),'affine identities use even rotations only')
    for unused in range(a//2):x,y=(x-3*y)/2,(x+y)/2
    return x+tx,y+ty

def universal_identities():
    B=(0,0,8*R+4,-4)
    U=(0,0,8*R-4-8*J,-4);V=(6,1,8*R+4+8*J,-4)
    L=(10,0,8*R-2-4*J,-2+4*J)
    Q=(4,1,8*R+2+4*J,-6-4*J)
    old_A=(8*R-4,Lin.of(0));old_B=(8*R+8,Lin.of(-4));H=(8*R,Lin.of(-4))
    rows=[('B flat host at v',affine_point(B,(2,2)),(8*R+6,Lin.of(-2))),
          ('A hex r-1',(8*R-4,Lin.of(0)),old_A),
          ('B hex0',affine_point(B,(4,0)),old_B),
          ('U_j hex j+1',affine_point(U,(8*J+12,0)),old_B),
          ('V_j hex j-1',affine_point(V,(8*J-4,0)),old_B),
          ('Ulast hex last',affine_point((0,0,8*R-8*M+4,-4),(8*M-4,0)),H),
          ('V0 hex0',affine_point((6,1,8*R+4,-4),(4,0)),H),
          ('L_j hex j-1',affine_point(L,(8*J-4,0)),old_A),
          ('R_j hex j+1',affine_point(Q,(8*J+12,0)),old_A),
          ('L0 hex0',affine_point((10,0,8*R-2,-2),(4,0)),H),
          ('Rlast hex last',affine_point((4,1,8*R+4*M-2,-4*M-2),(8*M-4,0)),H)]
    for name,actual,expected in rows:b.require(actual==expected,'universal identity failed: '+name)
    return [{'name':name,'x_coefficients':actual[0].serial(),'y_coefficients':actual[1].serial()}
            for name,actual,expected in rows]


def core_poses(m,r):
    b.require(type(m) is int and type(r) is int and m>=2 and 1<=r<m,
              'outside integer two-copy theorem range')
    return {'A':(0,0,0,0),'B':(0,0,8*r+4,-4)}


def fan(m,point,start,metadata):
    out=set()
    for vertex in metadata:
        if vertex['angle']!=2:continue
        for f in (0,1):
            a=(start-vertex['start'] if not f else start+vertex['end'])%12
            b.require(a%2==0,'pinned60 corner unexpectedly requires odd rotation')
            x,y=b.point((a,f,0,0),vertex['p'])
            out.add((a,f,point[0]-x,point[1]-y))
    return out


def instance_control(m,r):
    fixed=core_poses(m,r);meta=vertex_data(m);by={v['p']:v for v in meta}
    u=(8*r,0);v=(8*r+6,-2)
    b.require(min(z['angle'] for z in meta)==2 and
              {z['p'] for z in meta if z['angle']==2}=={(4+8*j,4) for j in range(m)},
              'complete minimum/60 corner boundary enumeration differs')
    b.require(all((z['start'],z['end'])==(8,10) for z in meta if z['angle']==2),
              'prototype60 rays differ')
    for point,expected in ((u,(10,10,8)),(v,(4,2,6)),((2,2),(6,8,2))):
        b.require(tuple(by[point][k] for k in ('angle','start','end'))==expected,
                  'required host local sector differs')
    U=[(0,0,8*r-4-8*j,-4) for j in range(m)]
    V=[(6,1,8*r+4+8*j,-4) for j in range(m)]
    L=[(10,0,8*r-2-4*j,-2+4*j) for j in range(m)]
    Q=[(4,1,8*r+2+4*j,-6-4*j) for j in range(m)]
    b.require(fan(m,u,8,meta)=={p for p in U+V} and
              fan(m,v,6,meta)=={p for p in L+Q},
              'complete arbitrary-motion pinned domains differ')
    Ahex=hex_vertices((8*r-4,0));Bhex=hex_vertices((8*r+8,-4));H=hex_vertices((8*r,-4))
    b.require(set(b.shape(m,fixed['A'])[0][3*(r-1)])==Ahex and
              set(b.shape(m,fixed['B'])[0][0])==Bhex,'old whole hexagons differ')
    for j in range(m-1):b.require(set(b.shape(m,U[j])[0][3*(j+1)])==Bhex,'U blocked by B differs')
    for j in range(1,m):b.require(set(b.shape(m,V[j])[0][3*(j-1)])==Bhex,'V blocked by B differs')
    for j in range(1,m):b.require(set(b.shape(m,L[j])[0][3*(j-1)])==Ahex,'L blocked by A differs')
    for j in range(m-1):b.require(set(b.shape(m,Q[j])[0][3*(j+1)])==Ahex,'R blocked by A differs')
    remaining=((U[-1],m-1),(V[0],0),(L[0],0),(Q[-1],m-1))
    for p,j in remaining:b.require(set(b.shape(m,p)[0][3*j])==H,'remaining supplier common whole hex differs')
    b.require(set(U+V).isdisjoint(set(L+Q)),'supplier motion sets are not disjoint')
    b.require(all(b.pair(m,p,c)[0] for p,j in remaining[:2] for c,k in remaining[2:]),
              'one of four cross-corner supplier pairs does not overlap')
    b.require(not b.pair(m,fixed['A'],fixed['B'])[0],'selected old pair is vacuous')
    b.require((u[0]-v[0])**2+3*(u[1]-v[1])**2==48 and 48%64!=0,
              'one-copy distance obstruction differs')
    return {'m':m,'r':r,'old_pair_packs':True,'raw_supplier_count_per_gap':2*m,
            'whole_hex_exclusions_per_gap':2*m-2,'remaining_suppliers_per_gap':2,
            'cross_corner_overlap_pairs':4,'same_copy_distance_obstruction_checked':True}


def images(data):
    m=data['tile_hexagons'];b.require(type(m) is int and m>=2,'invalid literal strip length')
    poses={tuple(row['pose']) for row in data['copies']};out=[]
    for common in sorted(poses):
        for r in range(1,m):
            expected=compose(common,(0,0,8*r+4,-4))
            if expected in poses:
                out.append({'m':m,'r':r,'common_isometry':common,
                            'members':{'A':common,'B':expected}})
    return out


def decode_fixture(value):
    b.require(type(value['tile_hexagons']) is int,'invalid fixture m')
    b.require(all(type(v) is int for row in value['rows'] for v in row),'noninteger literal fixture')
    b.require(all(len(row)==5 for row in value['rows']),'invalid fixture row')
    return {'tile_hexagons':value['tile_hexagons'],'level_counts':value['level_counts'],
            'copies':[{'pose':row[:4],'level':row[4]} for row in value['rows']]}


def check_example(value,fixtures):
    m,r=value['m'],value['r'];core_poses(m,r)
    common=tuple(value['A']);other=tuple(value['B'])
    b.require(other==compose(common,(0,0,8*r+4,-4)),'example is not the specified pair')
    data=decode_fixture(fixtures[value['fixture']])
    b.require(data['tile_hexagons']==m,'example strip length differs')
    poses={tuple(row['pose']) for row in data['copies']}
    b.require({common,other}<=poses,'example pair missing from actual fixture')
    b.require(not b.pair(m,common,other)[0],'example pair overlaps')
    return {'fixture':value['fixture'],'m':m,'r':r,'A':list(common),'B':list(other),
            'u':list(b.point(common,(8*r,0))),'v':list(b.point(common,(8*r+6,-2))),
            'no_next_surround_under_arbitrary_motions':True}


def check_certificate(cert,fixtures):
    actual=universal_identities()
    b.require(actual==cert['universal_affine_identities'],'affine certificate differs coefficient by coefficient')
    cases=[instance_control(m,r) for m,r in cert['finite_instances']]
    example=check_example(cert['example'],fixtures)
    return actual,cases,example


def damaged_controls(cert,fixtures):
    rejected=[]
    def reject(name,work):
        try:work()
        except ValueError:rejected.append(name)
        else:raise ValueError('damaged certificate accepted: '+name)
    for m,r in ((1,1),(2,0),(2,2),(6,6)):
        reject('range-m%d-r%d'%(m,r),lambda m=m,r=r:core_poses(m,r))
    bad=copy.deepcopy(cert);bad['universal_affine_identities'][3]['x_coefficients'][0]='9'
    reject('changed-affine-coefficient',lambda:check_certificate(bad,fixtures))
    bad=copy.deepcopy(cert['example']);bad['B'][2]+=8
    reject('wrong-geometric-example-pair',lambda:check_example(bad,fixtures))
    bad=copy.deepcopy(fixtures['basic_T6']);bad['rows'][1][:4]=bad['rows'][0][:4]
    reject('duplicate-positive-copy',lambda:b.check(decode_fixture(bad)))
    bad=copy.deepcopy(fixtures['pending_T7_five']);idx=next(i for i,row in enumerate(bad['rows']) if row[4]==1)
    bad['rows'][idx][4]=2;bad['level_counts'][1]-=1;bad['level_counts'][2]+=1
    reject('uncovered-inner-prefix-with-consistent-counts',lambda:b.check(decode_fixture(bad)))
    return rejected


def run():
    cert=json.loads((HERE/'certificate.json').read_text())
    fixtures=json.loads((HERE/'fixtures.json').read_text())
    actual,cases,example=check_certificate(cert,fixtures)
    positive=[]
    for name,depth in (('basic_T6',5),('pending_T7_five',4)):
        data=decode_fixture(fixtures[name]);checked=b.check(data)
        b.require(checked['verified_coronas']>depth,'positive lacks a genuine later corona')
        prefix={'tile_hexagons':data['tile_hexagons'],'copies':[row for row in data['copies'] if row['level']<=depth]}
        b.require(not images(prefix),'obstruction rejected an actually covered prefix')
        for key in ('elapsed_seconds','peak_rss_kib'):checked.pop(key)
        positive.append({'fixture':name,'exact_polygon_check':checked,'covered_prefix_depth':depth,
                         'forbidden_pair_absent_in_covered_prefix':True})
    damaged=damaged_controls(cert,fixtures)
    return {'agent':'six-heesch-3','role':'researcher','status':'author-checked uniform local obstruction',
            'integer_parameter_range':'m>=2, 1<=r<=m-1',
            'universal_affine_identities':actual,'finite_nonvacuous_controls':cases,
            'actual_positive_controls':positive,'literal_fifth_no_sixth_example':example,
            'damaged_certificates_rejected':damaged,
            'unbounded_range_proved_by_written_argument':True,'formalized':False,
            'independently_reviewed':False,'shared_polygon_primitives':True,
            'mate_premise_used':False,'global_grid_premise_used':False,
            'arbitrary_new_motions_allowed':True,'holes_elsewhere_allowed':True,
            'shape_Heesch_upper_claimed':False,'historical_priority_claimed':False}


if __name__=='__main__':
    parser=argparse.ArgumentParser(description=__doc__);parser.add_argument('--out');args=parser.parse_args()
    if args.out:b.require(not Path(args.out).exists(),'refuse overwrite of run output')
    start=time.monotonic();result=run()
    b.require(result==json.loads((HERE/'expected.json').read_text()),'expected evidence differs entry by entry')
    out={'stable_evidence_sha256':digest(result),'evidence':result,
         'elapsed_seconds':time.monotonic()-start,
         'peak_rss_kib':resource.getrusage(resource.RUSAGE_SELF).ru_maxrss}
    if args.out:Path(args.out).write_text(json.dumps(out,indent=2)+chr(10))
    print(json.dumps({'status':result['status'],'universal_affine_identities':len(result['universal_affine_identities']),
          'finite_controls':len(result['finite_nonvacuous_controls']),
          'verified_positive_coronas':[r['exact_polygon_check']['verified_coronas'] for r in result['actual_positive_controls']],
          'damaged_certificates_rejected':len(result['damaged_certificates_rejected']),
          'stable_evidence_sha256':out['stable_evidence_sha256'],
          'elapsed_seconds':out['elapsed_seconds'],'peak_rss_kib':out['peak_rss_kib']},indent=2))
