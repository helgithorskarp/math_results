"""Rebuild ALL C22 true phase horizon edges and five-wrench rows exactly.

Uses the fresh current-mode named-model reconstruction after full-byte checking. No C30 contacts,
signs, masses or motion certificate are used. Cone and nonlinear fit stay open.
"""
from pathlib import Path
from fractions import Fraction as F
import argparse, hashlib, json, resource, sys, time
import local as C
H=C.H
HERE=Path(__file__).resolve().parent

def run(args):
    start=time.monotonic();deadline=start+40
    work=Path(args.work);cfg=json.loads((HERE/'configuration.json').read_text())
    target_raw=(HERE/'target.json').read_bytes();target=json.loads(target_raw)
    H.require(hashlib.sha256(target_raw).hexdigest()==cfg['target_sha256'],'entire literal current target bytes')
    H.require(target['receiver_index']==22,'literal target C22')
    domain=json.loads((work/'domain.json').read_text())
    H.require(domain['exact_polygon']==target['exact_polygon'] and domain['exact_facet_signs']==target['exact_facet_signs'] and all(v>=0 for row in domain['image_rejection_side_indices'] for v in row),'same whole target and all strict prior-image rejections')
    raw=(work/'named_geometry.json').read_bytes()
    data=C.verified_cache(raw,cfg['expected_fresh_named_geometry_sha256'])
    points,root=data['points'],data['root']
    faces=json.loads((H.MODEL_DIR/'model.json').read_text())['faces']
    polygon=[tuple(C.decode(z) for z in p) for p in target['exact_polygon']]
    phase=target['exact_facet_signs'];center=tuple(C.decode(z)for z in target['exact_barycenter'])
    edges={}
    for fi,face in enumerate(faces):
        for a,b in zip(face,face[1:]+face[:1]):edges.setdefault(tuple(sorted((a,b))),[]).append(fi)
    H.require(len(edges)==150 and all(len(fs)==2 for fs in edges.values()),'all150 original edges with exactly two original incident facets')
    horizon=[(ab,fs)for ab,fs in sorted(edges.items())if phase[fs[0]]!=phase[fs[1]]]
    basis=[tuple(H.O if i==j else H.Z for i in range(3))for j in range(3)]
    supports=[];rows=[];comparisons=0;ties=0;offendpoint=0;collapsed=[]
    all_support_m2=F(0);point_m2=max(sum(z.interval(root).square().hi for z in p)for p in points)
    for (a,b),fs in horizon:
        d=H.M.sub(points[b],points[a]);m=H.M.cross(d,(H.O,*center));h=H.M.dot(m,points[a])
        orientation=H.sign(h,root);H.require(orientation!=0,'genuine noncollapsed center silhouette edge')
        if orientation<0:a,b=b,a;d=tuple(-z for z in d)
        corner_m=[H.M.cross(d,(H.O,*p))for p in polygon]
        m2=max(sum(z.interval(root).square().hi for z in m)for m in corner_m)
        H.require(m2>0,'nonzero affine silhouette support')
        k=0
        while (F(4)**k)*m2>=2:k-=1
        while (F(4)**(k+1))*m2<2:k+=1
        H.require(-12<=k<=12,'bounded literal positive dyadic scale')
        gamma=F(2)**k;all_support_m2=max(all_support_m2,gamma*gamma*m2)
        support_ties=[];heights=[]
        for ci,(s,t)in enumerate(polygon):
            H.require(time.monotonic()<deadline,'original support audit within unchanged40s guard')
            r=(H.O,s,t);m=tuple(gamma*z for z in H.M.cross(d,r));h=H.M.dot(m,points[a])
            H.require(H.M.dot(m,r)==H.Z and H.M.dot(m,d)==H.Z,'exact physical perpendicular and endpoint equalities')
            H.require(H.sign(h,root)>=0,'nonnegative closed-boundary physical support height')
            if h==H.Z:
                H.require(all(z==H.Z for z in m),'zero support height occurs only at collapsed actual edge')
                collapsed.append(dict(edge=[a,b],corner=ci,exponent=k))
            heights.append(H.encode(h));tt=[]
            for vi,p in enumerate(points):
                gap=h-H.M.dot(m,p);sg=H.sign(gap,root)
                H.require(sg>=0,'all92 actual originals satisfy all closed-corner support inequalities')
                comparisons+=1
                if sg==0:
                    tt.append(vi);ties+=1;offendpoint+=(vi not in(a,b))
            H.require(a in tt and b in tt,'original endpoint ties retained')
            support_ties.append(tt)
        supports.append(dict(edge=[a,b],incident_original_facets=fs,dyadic_exponent=k,closed_corner_heights=heights,closed_corner_original_ties=support_ties))
        for v in (a,b):
            coeff=[]
            for r in basis:
                m=tuple(gamma*z for z in H.M.cross(d,r))
                coeff.append(tuple(H.M.cross(points[v],m))+(m[1],m[2]))
            rows.append(dict(contact=[a,b,v,k],five_wrench_affine_coefficients=[[H.encode(coeff[j][i])for j in range(3)]for i in range(5)]))
    H.require(len(rows)==2*len(horizon),'both endpoints of every genuine actual phase-horizon edge')
    H.require(4*point_m2*all_support_m2<16 and all_support_m2<4,'new actual norm bounds give remainder<4 and support norm<2')
    record=dict(agent='six-rupert-1',role='researcher',status='EXACT_ALL_ORIGINAL_C22_HORIZON_SUPPORTS_AND_FIVE_WRENCH_ROWS_REBUILT_CONE_FIT_OPEN',receiver_index=22,
                target_sha256=hashlib.sha256(target_raw).hexdigest(),named_model_fresh_this_mode_sha256=cfg['expected_fresh_named_geometry_sha256'],
                all_original_edges=150,genuine_phase_horizon_edges=len(horizon),endpoint_rows=len(rows),
                closed_corner_all_original_support_comparisons=comparisons,exact_closed_support_ties=ties,
                exact_offendpoint_grazing_ties=offendpoint,collapsed_boundary_supports=collapsed,
                supports=supports,rows=rows,actual_original_squared_norm_upper=str(point_m2),actual_support_squared_norm_upper=str(all_support_m2),
                physical_translation='At r_x=1, every b in r-perp is pi_r(alpha*e_y+beta*e_z); translation wrench coordinates m_y,m_z. Cayley first derivative is2*(P cross m).c; this invertible scaling preserves the five-dimensional feasibility cone.',
                mathematical_scope='All true original horizon edges and both endpoint rows are rebuilt from C22 phase and original facets. Affinity extends every support inequality from all closed corners to the entire convex C22. No first-order cone, nonlinear collar, arbitrary-source exclusion or passage assertion yet.',
                resources=dict(guard_seconds=40,threads=1,maximum_intensive_jobs=1,no_escalation=True))
    H.require(time.monotonic()<deadline,'entire support reconstruction complete')
    out=(json.dumps(record,indent=2,sort_keys=True)+'\n').encode()
    if args.compare:H.require(out==args.compare.read_bytes(),'whole normal/O original support and wrench reconstruction agrees')
    args.output.write_bytes(out)
    print(json.dumps(dict(status=record['status'],horizon_edges=len(horizon),endpoint_rows=len(rows),original_comparisons=comparisons,ties=ties,offendpoint_ties=offendpoint,collapsed=collapsed,bytes=len(out),sha256=hashlib.sha256(out).hexdigest(),elapsed_seconds=time.monotonic()-start,peak_rss_kib=resource.getrusage(resource.RUSAGE_SELF).ru_maxrss)))

if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('--work',required=True);p.add_argument('--output',type=Path,required=True);p.add_argument('--compare',type=Path);run(p.parse_args())
