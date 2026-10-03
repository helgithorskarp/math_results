"""Exact fixed-source closed RID receiving family; standard library only.

No source cover, local collar, solver, numerical proposal or private input.
All checks are unconditional in normal and optimized CPython modes.
"""
from pathlib import Path
from fractions import Fraction as Q
import argparse, hashlib, json, resource, time

HERE = Path(__file__).resolve().parent
FIELD_SHA256 = '7801bce4e611b05c8d3d982a862d3f281db7585ef5219ea8fb901c6417c129b0'
if hashlib.sha256((HERE / 'field.py').read_bytes()).hexdigest() != FIELD_SHA256:
    raise ValueError('pinned exact named-body field primitive differs')
from field import F, ZERO as Z, ONE as O, PHI as phi, vertices, dot, cross, sub, encode, determinant

RING = [48,36,54,56,38,53,46,18,19,11,23,5,3,21,6,13,41,40]

def need(condition, message):
    if not condition: raise ValueError(message)

def digest(data):
    return hashlib.sha256(json.dumps(data, sort_keys=True, separators=(',', ':')).encode()).hexdigest()

def qmul(q, p):
    h, v, k, w = q[0], q[1:], p[0], p[1:]; vxw = cross(v, w)
    return (h*k-dot(v,w), *(h*w[j]+k*v[j]+vxw[j] for j in range(3)))

def rotate(c, v):
    c2 = dot(c,c); cv = dot(c,v); cxv = cross(c,v)
    return tuple(((O-c2)*v[j]+2*c[j]*cv+2*cxv[j])/(O+c2) for j in range(3))

def literal_line(c, v, anchor, edge):
    c2 = dot(c,c); cv = dot(c,v); cxv = cross(c,v)
    W = tuple((O-c2)*v[j]+2*c[j]*cv+2*cxv[j]-(O+c2)*anchor[j] for j in range(3))
    return cross(W,edge)

def projection(v, r):
    return (v[0]-r[0]*v[2], v[1]-r[1]*v[2])

def turn(a,b,c):
    return (b[0]-a[0])*(c[1]-a[1])-(b[1]-a[1])*(c[0]-a[0])

def hull(points):
    ordered = sorted(set(points)); low = []; high = []
    for p in ordered:
        while len(low)>1 and turn(low[-2],low[-1],p)<=Z: low.pop()
        low.append(p)
    for p in reversed(ordered):
        while len(high)>1 and turn(high[-2],high[-1],p)<=Z: high.pop()
        high.append(p)
    out = low[:-1]+high[:-1]
    need(len(out)>=3, 'actual full projected hull degenerate')
    need(all(turn(a,b,p)>=Z for a,b in zip(out,out[1:]+out[:1]) for p in ordered), 'full original hull membership differs')
    return out

def main():
    parser = argparse.ArgumentParser(); parser.add_argument('--output', type=Path)
    args = parser.parse_args(); start = time.monotonic()
    if args.output is not None: need(not args.output.exists(), 'fresh output required')
    V = vertices(); need(len(V)==60 and len(set(V))==60, 'actual named60 vertices differ')
    need(set(V)=={tuple(-x for x in v) for v in V}, 'actual RID centrality fails')
    c = (F(Q(4,5),Q(-3,5)),Z,F(Q(3,5),Q(-1,5)))
    c2 = dot(c,c); need(O+c2>Z, 'Cayley denominator fails')
    M = [rotate(c, v) for v in V]
    basis = [tuple(O if i==j else Z for i in range(3)) for j in range(3)]
    Rcolumns = [rotate(c,e) for e in basis]
    R = tuple(tuple(Rcolumns[j][i] for j in range(3)) for i in range(3))
    need(all(dot(a,b)==(O if i==j else Z) for i,a in enumerate(Rcolumns) for j,b in enumerate(Rcolumns)), 'literal Cayley matrix is not orthogonal')
    need(determinant(R)==O and sum((R[i][i] for i in range(3)),Z)==1+phi, 'source is not the claimed proper36-degree rotation')
    squared = tuple(a/(O+c2) for a in qmul((O,*c),(O,*c)))
    need(squared==(phi/2,-(phi-1)/2,Z,O/2) and dot(squared,squared)==O, 'actual midpoint square differs')
    need({rotate(c,rotate(c,v)) for v in V}==set(V), 'midpoint square is not an actual named-body symmetry')
    lo,hi = 2*phi-3,2-phi
    need(Z<lo<hi and lo>hi/2, 'receiving segment is not outside the proved inner triangle')
    endpoints = [(lo,Z,O),(hi,Z,O)]; phase = [(Z,Z,O),(hi,Z,O),(hi,hi*hi,O)]
    # Two ORIGINAL necessary physical rows yield the entire receiving set.
    E0=sub(V[36],V[48]); E6=sub(V[18],V[46])
    need(E0==(phi-1,O,-phi), 'written original edge0 vector differs')
    line40=literal_line(c,V[40],V[48],E0)
    line413=literal_line(c,V[53],V[46],E6)
    k=F(Q(8,5))*(phi-1)
    need(line40==(-k,k,k*lo) and line413==(Z,F(Q(16,5))*lo,Z), 'written original physical rows differ')
    need(line413[0]==line413[2]==Z and line413[1]>Z, 'original413 does not force receiving y0')
    need(line40[0]<Z and line40[2]==-lo*line40[0], 'original40 does not force x>=2phi-3 at y0')
    # These raw edges support K throughout the ENTIRE closed phase by affinity.
    necessary_support_gaps = []
    for anchor,E in ((V[48],E0),(V[46],E6)):
        for r in phase:
            m=cross(E,r); h=dot(m,anchor)
            need(dot(m,r)==Z, 'necessary original support is not projected')
            gaps=[h-dot(m,v) for v in V]
            need(all(g>=Z for g in gaps), 'necessary row is not an actual original support on full phase')
            necessary_support_gaps.extend(gaps)
    receiving_controls=[]; moving_controls=[]; normals=[]; heights=[]; hull_records=[]
    for r in endpoints:
        points=[projection(V[i],r) for i in RING]
        need(len(set(points))>=3, 'actual receiving ring degenerates')
        original=[turn(a,b,projection(v,r)) for a,b in zip(points,points[1:]+points[:1]) for v in V]
        nonzero=next(g for g in original if g!=Z); sigma=1 if nonzero>Z else -1
        need(sigma==1, 'receiving ring orientation must agree at both endpoints')
        original=[sigma*g for g in original]
        moved=[sigma*turn(a,b,projection(v,r)) for a,b in zip(points,points[1:]+points[:1]) for v in M]
        need(all(g>=Z for g in original) and all(g>=Z for g in moved), 'entire-ring endpoint containment failed')
        # Exact oriented turns are affine in x when y0; endpoint controls
        # establish BOTH receiving hull equality and all moving memberships.
        receiving_controls.extend(original); moving_controls.extend(moved)
        ns=[]; hs=[]
        for si in range(18):
            i,j=RING[si],RING[(si+1)%18]; E=sub(V[j],V[i])
            m=cross(E,r)
            if si in (7,16):
                need(E[:2]==(Z,Z) and r[0]>Z, 'normalized vertical original edge differs')
                m=(Z,E[2],Z)
            h=dot(m,V[i])
            need(h>Z and dot(m,r)==Z and all(dot(m,v)<=h for v in V), 'actual outward ring support differs')
            ns.append(m);hs.append(h)
        normals.append(ns);heights.append(hs)
        H=hull([projection(v,r) for v in V]); J=hull([projection(v,r) for v in M])
        gaps=[turn(a,b,p) for a,b in zip(H,H[1:]+H[:1]) for p in [projection(v,r) for v in M]]
        need(all(g>=Z for g in gaps) and H!=J, 'independent full original hulls do not give proper closed containment')
        hull_records.append({'r':encode(r),'receiving_hull':[encode(p) for p in H],
                             'moving_hull':[encode(p) for p in J],
                             'all_original_hull_gaps':[g.encode() for g in gaps]})
    # ORIGINAL tight antipodal pairs force lambda1 and ORIGINAL t0.
    tight=[]
    for ei,r in enumerate(endpoints):
        n0,n7=normals[ei][0],normals[ei][7];h0,h7=heights[ei][0],heights[ei][7]
        need(n0==(O,1-phi*(1+r[0]),-r[0]) and h0==3*phi+(1+3*phi)*r[0], 'written tight support0 formula differs')
        need(n7==(Z,F(2),Z) and h7==2+4*phi, 'written normalized tight support7 formula differs')
        need(dot(n0,M[32])==h0 and dot(n7,M[47])==h7, 'actual permanent tight source pair differs')
        need(E0[1]!=Z and n7[1]!=Z, 'tight original support normals do not span receiving plane')
        determinant_value=dot(r,cross(n0,n7))
        need(determinant_value==E0[1]*n7[1]*dot(r,r) and determinant_value!=Z, 'original translation rigidity identity differs')
        tight.append({'r':encode(r),'normals':[encode(n0),encode(n7)],'heights':[h0.encode(),h7.encode()],
                      'source_vertices':[32,47], 'spanning_determinant':determinant_value.encode()})
    # A genuine exposed receiving corner absent from the moving shadow,
    # uniformly along the whole closed segment, proves proper containment.
    strict_corner=None
    for vertex in range(18):
        gap_values=[]; records=[]
        for ei,r in enumerate(endpoints):
            n=tuple(a+b for a,b in zip(normals[ei][(vertex-1)%18],normals[ei][vertex]))
            h=dot(n,V[RING[vertex]])
            need(h==heights[ei][(vertex-1)%18]+heights[ei][vertex] and h>Z, 'adjacent actual supports do not expose the claimed vertex')
            gaps=[h-dot(n,v) for v in M]
            gap_values.extend(gaps);records.append({'r':encode(r),'normal':encode(n),'height':h.encode(),'all60_gaps':[g.encode() for g in gaps]})
        if all(g>Z for g in gap_values):
            strict_corner={'receiving_vertex':RING[vertex],'all120_strict_controls':records};break
    need(strict_corner is not None, 'no uniform actual-corner proper-containment certificate')
    # All chosen normalized/raw normals and their support values are affine
    # in x on y0. Permanent tightness, positivity and strict corner controls
    # therefore hold throughout this ENTIRE closed segment.
    mathematical={'agent':'six-rupert-3','role':'researcher','source_cayley':encode(c),
                  'literal_proper_rotation_matrix':[encode(row) for row in R],
                  'actual_body_symmetry_square':encode(squared),'receiving_phase':list(map(encode,phase)),
                  'entire_closed_receiving_segment':list(map(encode,endpoints)),
                  'necessary_original_rows':{'cut40':encode(line40),'cut413':encode(line413)},
                  'all360_necessary_whole_phase_support_gaps':[g.encode() for g in necessary_support_gaps],
                  'all2160_receiving_ring_endpoint_controls':[g.encode() for g in receiving_controls],
                  'all2160_moving_ring_endpoint_controls':[g.encode() for g in moving_controls],
                  'independent_full_hulls':hull_records,'permanent_original_tightness':tight,
                  'uniform_proper_containment_certificate':strict_corner,
                  'actual_named_vertex_sha256':digest(list(map(encode,V))),
                  'scale_and_original_translation_classification':'lambda=1 and t=0 iff r is on the stated segment; lambda>=1,t in r-perp quantified',
                  'source_perturbation_or_local_collar_claimed':False,'global_RID':'OPEN',
                  'proof_status':'author checked, unformalized, independently unreviewed'}
    summary={'proper_fixed_source_family_verified':True,'fixed_source_rotation_degrees':36,
             'exact_receiving_segment':list(map(encode,endpoints)),
             'arbitrary_original_translation_and_scale_classified':True,'only_fitting_scale':'1','only_fitting_translation':['0','0','0'],
             'uniform_shadow_containment_is_proper':True,'receiving_vertex_separated_from_moving_shadow':strict_corner['receiving_vertex'],
             'whole_phase_necessary_support_controls':len(necessary_support_gaps),
             'receiving_ring_controls':len(receiving_controls),'moving_ring_controls':len(moving_controls),
             'strict_corner_controls':120,'all_mathematical_record_sha256':digest(mathematical),
             'global_RID':'OPEN','source_collar_or_perturbation_excluded':False,
             'proof_status':mathematical['proof_status']}
    expected=json.loads((HERE/'EXPECTED.json').read_text())
    need(summary==expected, 'complete mathematical record or claimed scope differs from fixed expected result')
    result={'mathematical':mathematical,'summary':summary,'field_sha256':FIELD_SHA256,
            'input_script_sha256':hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
            'seconds':round(time.monotonic()-start,3),'peak_kib':resource.getrusage(resource.RUSAGE_SELF).ru_maxrss,
            'optimized':not __debug__,'threads':1}
    if args.output is not None: args.output.write_text(json.dumps(result,sort_keys=True,indent=2)+'\n')
    print(json.dumps(summary,sort_keys=True))

if __name__=='__main__': main()
