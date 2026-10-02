#!/usr/bin/env python3
"""Author controls: an independent Fraction polarization oracle and damages."""
from fractions import Fraction as F
from pathlib import Path
import argparse,copy,hashlib,itertools,json,resource,sys,time
import verify_shell as L
import local as C
E,H,S=L.E,L.H,L.S

def need(b,s):
    if not b:raise ValueError(s)
def dot(a,b):return sum(x*y for x,y in zip(a,b))
def cross(a,b):return(a[1]*b[2]-a[2]*b[1],a[2]*b[0]-a[0]*b[2],a[0]*b[1]-a[1]*b[0])
def add(a,b):return tuple(x+y for x,y in zip(a,b))
def mul(a,b):return tuple(a*x for x in b)
def middle(a,b):return mul(F(1,2),add(a,b))
def cleared(P,c):
    return add(add(mul(1-dot(c,c),P),mul(2*dot(c,P),c)),mul(2,cross(c,P)))
def direct(r,c,ds,anchors,moving):
    normals=[cross(d,r)for d in ds]
    # Independent plane cofactor minors. Here r_x=1, so these equal
    # the affine triple weights without using any dot(cross(d,d),r).
    w=[normals[j][1]*normals[k][2]-normals[j][2]*normals[k][1]
       for j,k in [(1,2),(2,0),(0,1)]]
    need(tuple(sum(w[i]*normals[i][j]for i in range(3))for j in range(3))==(0,0,0),'full actual force cancellation')
    return sum(w[i]*((1+dot(c,c))*dot(normals[i],anchors[i])-dot(normals[i],cleared(moving[i],c)))for i in range(3))
def oracle(r,s,u,v,ds,anchors,moving):
    def source(z):
        if u==v:return direct(z,u,ds,anchors,moving)
        return 2*direct(z,middle(u,v),ds,anchors,moving)-(direct(z,u,ds,anchors,moving)+direct(z,v,ds,anchors,moving))/2
    if r==s:return source(r)
    return 2*source(middle(r,s))-(source(r)+source(s))/2
def enclosed(interval,value):return F(interval.lo,E.SCALE)<=value<=F(interval.hi,E.SCALE)

def run(args):
    started=time.monotonic();damages=[];oracle_count=0;bary_count=0
    def rejected(name,f):
        try:f()
        except (ValueError,KeyError,IndexError,TypeError):damages.append(name);return
        raise ValueError('Damaged or feasible case wrongly accepted: '+name)
    ds=[(F(0),F(0),F(1)),(F(0),F(-1),F(0)),(F(0),F(1),F(-1))]
    anchors=[(F(0),F(1),F(0)),(F(0),F(0),F(1)),(F(0),F(-1),F(-1))]
    receivers=[(F(1),F(0),F(0)),(F(1),F(1,8),F(0)),(F(1),F(0),F(1,8)),(F(1),F(-1,16),F(0)),(F(1),F(0),F(-1,16))]
    corners=[(F(0),F(0),F(0)),(F(1,32),F(0),F(0)),(F(0),F(1,32),F(0)),(F(0),F(0),F(1,32))]
    triangles=[[0,1,2],[0,2,3],[0,3,4]]
    geom=dict(receiver_triangle_indices=triangles)
    rows={}
    for i,(d,P)in enumerate(zip(ds,anchors)):
        rows[(i,i+3)]=(i,[(tuple(E.B.rational(x)for x in cross(d,r)),E.B.rational(dot(cross(d,r),P)))for r in receivers])
    pairs={'0:1':[E.ONE]*5,'0:2':[-E.ONE]*5,'1:2':[E.ONE]*5}
    root=H.V.I(F(17,10),F(18,10));tet=tuple(tuple(S.Q(x)for x in c)for c in corners)
    qpair=list(itertools.combinations_with_replacement(range(4),2))
    for factor in (2,3,4,5):
        moving=[mul(F(factor),P)for P in anchors]
        points=[tuple(E.B.rational(x)for x in P)for P in moving]+[(E.ZERO,)*3]*89
        for no,tri in enumerate(triangles):
            stress=dict(receiver_triangle=no,edges=[[0,3],[1,4],[2,5]],moving_originals=[0,1,2],cofactor_orientation=1)
            _,coeff=L.stress_coefficients(stress,tet,geom,rows,pairs,points,root)
            reference=[oracle(receivers[a],receivers[b],corners[u],corners[v],ds,anchors,moving)for a,b in itertools.combinations_with_replacement(tri,2)for u,v in qpair]
            need(all(enclosed(c,z)for c,z in zip(coeff,reference)),'independent double-midpoint coefficients inside production enclosures')
            oracle_count+=len(reference)
            L.verify_stress(stress,tet,geom,rows,pairs,points,root)
            rpair=list(itertools.combinations_with_replacement(range(3),2))
            for rb,sb in [([F(1),F(0),F(0)],[F(1),F(0),F(0),F(0)]),([F(1,3)]*3,[F(1,4)]*4),([F(1,2),F(1,3),F(1,6)],[F(1,10),F(2,10),F(3,10),F(4,10)])]:
                r=tuple(sum(rb[i]*receivers[tri[i]][j]for i in range(3))for j in range(3))
                c=tuple(sum(sb[i]*corners[i][j]for i in range(4))for j in range(3))
                tensor=sum(reference[ri*10+si]*rb[a]*rb[b]*(1 if a==b else 2)*sb[u]*sb[v]*(1 if u==v else 2)
                           for ri,(a,b)in enumerate(rpair)for si,(u,v)in enumerate(qpair))
                need(tensor==direct(r,c,ds,anchors,moving),'independent tensor reconstruction equals direct cleared Cayley stress');bary_count+=1
    g=json.loads(Path(args.geometry).read_text());forest=json.loads(Path(args.forest).read_text())
    need(hashlib.sha256(Path(args.geometry).read_bytes()).hexdigest()==args.geometry_sha,'fresh exact geometry fingerprint')
    tets,internals=L.tree_cover(forest,g)
    config=json.loads((Path(__file__).resolve().parent/'configuration.json').read_text())
    need(len(tets)==config['source_leaf_count'] and internals==config['source_midpoint_count'],'complete actual forest')
    def damaged(label,mutate):
        z=copy.deepcopy(forest);mutate(z);rejected(label,lambda:L.tree_cover(z,g))
    damaged('missing_leaf',lambda z:z['leaves'].pop())
    damaged('duplicate_leaf',lambda z:z['leaves'].append(copy.deepcopy(z['leaves'][0])))
    damaged('root_count',lambda z:z['roots'].pop())
    damaged('wrong_frustum_order',lambda z:z['roots'].reverse())
    damaged('unfinished_search',lambda z:z.update(pending=1))
    def ancestor(z):z['leaves'][0].update(path='',depth=0)
    damaged('leaf_ancestor',ancestor)
    def edge(z):
        x=z['leaves'][0];token=x['path'][:2];other=next(p for p in ('01','02','03','12','13','23')if p!=token)
        x['path']=other+x['path'][2:]
    damaged('inconsistent_sibling_edge',edge)
    actual_rows={tuple(row['edge']):(i,[(tuple(L.bdecode(z)for z in v['m']),L.bdecode(v['h']))for v in row['vertices']])for i,row in enumerate(g['actual_edge_rows'])}
    actual_pairs={k:[L.bdecode(z)for z in v]for k,v in g['actual_edge_pair_cofactor_vertex_enclosures'].items()}
    points=[tuple(L.bdecode(z)for z in p)for p in g['original_point_enclosures']]
    exactroot=H.V.I(*[F(s)for s in g['root_interval']]);stress=forest['leaves'][0]['receiver_stresses'][0]
    def call(s=stress,t=tets[0]):return L.verify_stress(s,t,g,actual_rows,actual_pairs,points,exactroot)
    good=call()
    for label,modify in [('wrong_moving_original',lambda s:s['moving_originals'].__setitem__(0,92)),('wrong_cofactor_sign',lambda s:s.update(cofactor_orientation=-s['cofactor_orientation'])),('unproved_reversed_edge',lambda s:s['edges'].__setitem__(0,s['edges'][0][::-1])),('repeated_support',lambda s:s['edges'].__setitem__(1,s['edges'][0])),('wrong_receiver_triangle',lambda s:s.update(receiver_triangle=len(g['receiver_triangle_indices'])))]:
        z=copy.deepcopy(stress);modify(z);rejected(label,lambda z=z:call(z))
    rejected('true_zero_pose_is_not_excluded',lambda:call(t=((S.Z,)*3,)*4))
    damaged_args=argparse.Namespace(geometry=args.geometry,geometry_sha='0'*64,forest=args.forest,seconds=45.,start=0,count=1,compare=None,output=str(Path(args.output).with_name('unreachable_damaged_geometry.json')))
    rejected('geometry_hash_damage',lambda:L.run(damaged_args))
    def decode(z):return H.K(tuple(H.V.Q(*q)for q in z))
    original=[tuple(decode(z)for z in p)for p in g['exact_original_points']]
    exactr=[(H.O,*[decode(z)for z in p])for p in g['receiver_polygon']]
    physical=[]
    for index in (0,len(tets)//2,len(tets)-1):
        st=forest['leaves'][index]['receiver_stresses'][0]
        dd=[H.M.sub(original[b],original[a])for a,b in st['edges']]
        A=[original[a]for a,b in st['edges']];X=[original[i]for i in st['moving_originals']]
        cc=tuple(sum((H.K.coerce(H.V.Q(q.a,q.b))for q in vv),H.Z)/4 for vv in zip(*tets[index]))
        for rr in (exactr[0],tuple(sum(v[i]for v in exactr)/len(exactr) for i in range(3))):
            mm=[H.M.cross(d,rr)for d in dd]
            ww=[st['cofactor_orientation']*H.M.dot(H.M.cross(dd[j],dd[k]),rr)for j,k in [(1,2),(2,0),(0,1)]]
            need(tuple(sum(ww[i]*mm[i][j]for i in range(3))for j in range(3))==(H.Z,)*3,'actual named-model force balance')
            den=1+H.M.dot(cc,cc);T=tuple(H.K.coerce(F(x,7))for x in (2,-3,5))
            HH=[H.M.dot(mm[i],A[i])for i in range(3)]
            clearedX=[H.transformed(P,cc)for P in X]
            ff=sum(ww[i]*(den*HH[i]-H.M.dot(mm[i],clearedX[i]))for i in range(3))
            error=sum(ww[i]*(H.M.dot(mm[i],tuple(z/den+t for z,t in zip(clearedX[i],T)))-HH[i])for i in range(3))
            need(error==-ff/den,'actual physical translation cancels without centering')
            for lam in (H.O,H.K.coerce(F(9,8))):
                scaled=sum(ww[i]*(H.M.dot(mm[i],tuple(lam*z/den+t for z,t in zip(clearedX[i],T)))-HH[i])for i in range(3))
                need(scaled==lam*error+(lam-1)*sum(ww[i]*HH[i]for i in range(3)),'actual enlargement stress identity')
            physical.append(hashlib.sha256(json.dumps(H.encode(ff),sort_keys=True).encode()).hexdigest())
    local_record=json.loads(Path(args.geometry).with_name('local.json').read_text())
    need(hashlib.sha256(Path(args.geometry).with_name('local.json').read_bytes()).hexdigest()==config['expected_local_record_sha256'],'complete fresh triangle local proof fingerprint')
    cert=json.loads((Path(__file__).resolve().parent/'local_certificate.json').read_text())
    named=dict(points=original,normals=[tuple(decode(z)for z in n)for n in g['outward_facet_normals']],root=exactroot,record=g['complete_named_geometry_record'])
    def malformed_local(label,mutate):
        damaged=copy.deepcopy(cert);mutate(damaged)
        rejected(label,lambda:C.prepare(damaged,named,time.monotonic()+45))
    malformed_local('local_wrong_actual_facet10_phase',lambda z:z['facet_signs'].__setitem__(10,-z['facet_signs'][10]))
    malformed_local('local_nonendpoint_contact',lambda z:z['duals'][0]['contacts'][0].__setitem__(2,0))
    malformed_local('local_missing_signed_dual',lambda z:z['duals'].pop())
    bound=F(local_record['uniform_dual_weight_sum_upper'])
    for label,field,value in [('local_insufficient_dual_mass','dual_sum_bound',14),('local_nonlinear_closure_boundary','closed_cayley_infinity_radius','1/90'),('local_excessive_physical_gap','physical_gap_coefficient','1/1000')]:
        damaged=copy.deepcopy(cert);damaged[field]=value
        rejected(label,lambda damaged=damaged:C.close_bounds(damaged,bound))
    need(C.close_bounds(cert,bound)['contraction_product']=='90/91','actual stronger closed local collar survives')
    need(g['exact_parent_boundary']['shared_wall']==13 and g['receiver_exact_side_wall_indices']==[[50],[13],[43]],'actual closed shared boundary inventory')
    record=dict(agent='six-rupert-1',role='researcher',status='AUTHOR_INDEPENDENT_ALGEBRA_AND_SEMANTIC_CONTROLS_PASSED',independent_fraction_coefficients=oracle_count,independent_tensor_identities=bary_count,actual_translation_and_scale_cases=len(physical),physical_case_hashes=physical,damages_rejected=damages,actual_stress_control=good,local_record_sha256=config['expected_local_record_sha256'],closed_shared_boundary=g['exact_parent_boundary'],trust_boundary='Author controls, not independent review or formalization.')
    raw=(json.dumps(record,indent=2,sort_keys=True)+'\n').encode()
    if args.compare:need(raw==Path(args.compare).read_bytes(),'normal/optimized whole control records match')
    Path(args.output).write_bytes(raw)
    print(json.dumps(dict(status=record['status'],sha256=hashlib.sha256(raw).hexdigest(),bytes=len(raw),elapsed_seconds=time.monotonic()-started,peak_rss_kib=resource.getrusage(resource.RUSAGE_SELF).ru_maxrss)))

if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('--geometry',default=str(Path(__file__).resolve().parent/'.generated/geometry.json'));p.add_argument('--forest',default=str(Path(__file__).resolve().parent/'.generated/forest.json'));p.add_argument('--geometry-sha',required=True);p.add_argument('--compare');p.add_argument('--output',default=str(Path(__file__).resolve().parent/'.generated/controls.json'));run(p.parse_args())
