"""Exact extra original half-turn closed fit at the new triangle corner.

Finite explicit witnesses, no source enumeration or numerical library input.
The whole-triangle six-parent all-source classification is FALSE.
"""
from fractions import Fraction as F
from pathlib import Path
import argparse,json,time
import geometry as g
Q,a,S=g.Q,g.a,g.S

def screen(v,point):
    x,y=point
    return (v[0]-x*v[1],v[2]+y*v[1])

def hull(points):
    points=sorted(set(points))
    def turn(u,v,w):return (v[0]-u[0])*(w[1]-u[1])-(v[1]-u[1])*(w[0]-u[0])
    lo=[];hi=[]
    for v in points:
        while len(lo)>=2 and turn(lo[-2],lo[-1],v)<=0:lo.pop()
        lo.append(v)
    for v in reversed(points):
        while len(hi)>=2 and turn(hi[-2],hi[-1],v)<=0:hi.pop()
        hi.append(v)
    return lo[:-1]+hi[:-1]

def record():
    started=time.monotonic();point=g.PENT[1];raw=g.raw(point);r2=a.dot(raw,raw)
    axis=(-g.bb,g.aa,g.cc)
    g.require(a.dot(axis,axis)==1,'literal unit exact half-turn axis')
    G=tuple(tuple(2*axis[i]*axis[j]-int(i==j) for j in range(3)) for i in range(3))
    g.require(G==((g.aa,-g.cc,-g.bb),(-g.cc,-g.bb,g.aa),(-g.bb,g.aa,-g.cc)),'literal named extra original half-turn matrix')
    g.proper(G);g.require(g.mm(G,G)==g.I and sum((G[i][i] for i in range(3)),Q())==-1,'original absolute half-turn retained')
    Mn=tuple(tuple(g.I[i][j]-2*raw[i]*raw[j]/r2 for j in range(3)) for i in range(3))
    old=g.POSES[:6]+[g.mm(g.mm(Mn,pose),g.MX) for pose in g.POSES[:6]]
    names=g.NAMES[:6]+['Cn('+name+')' for name in g.NAMES[:6]]
    right=hull([screen(v,point) for v in g.V]);motions=[G,g.mm(G,g.H),g.mm(g.H,g.B),g.mm(g.mm(g.H,g.B),g.H)]
    motions.extend([g.mm(g.mm(Mn,pose),g.MX) for pose in motions.copy()])
    distinct=list(dict.fromkeys(motions));motion_records=[];common_left=None
    g.require(len(distinct)==4,'four distinct extra proper motions, with companions retained as a set')
    for pose in distinct:
        g.proper(pose)
        images=tuple(g.act(pose,v) for v in g.V)
        left=hull([screen(v,point) for v in images])
        if common_left is None:common_left=left
        g.require(left==common_left,'the four extra motions have the same complete exact source projection hull')
        def inside(poly,v):
            return all((u[0]-p[0])*(v[1]-p[1])-(u[1]-p[1])*(v[0]-p[0])>=0 for p,u in zip(poly,poly[1:]+poly[:1]))
        g.require(all(inside(right,v) for v in left),'independent full exact projected hull containment')
        g.require(left!=right and not inside(left,screen(g.V[20],point)),'proper projected containment with original receiver20 outside source shadow')
        traces=[sum((a.dot(rr,ee) for rr,ee in zip(pose,e)),Q()) for e in old]
        g.require(all(trace<3 for trace in traces),'extra original fit is outside every old parent/companion equality motion')
        g.require(max(traces)==(1+S)/2<Q(F(1261,421)),'extra original fit lies outside all old1/29 trace collars')
        motion_records.append({'literal_matrix':[g.vec(row) for row in pose],'all_twelve_relative_traces':[{'old_motion':name,'trace':g.enc(v)} for name,v in zip(names,traces)],'maximum_old_relative_trace':g.enc(max(traces)),'projected_source_hull_corners':len(left),'receiver20_outside_source_shadow':True})
    parents=[]
    for name,pose in zip(g.NAMES[6:],g.POSES[6:]):
        images=tuple(g.act(pose,v) for v in g.V)
        gaps=[h-a.dot(m,v) for i,j in g.EDGES for m,h in [g.support(i,j,raw)] for v in images]
        g.require(min(gaps)>=0,'all1020 original point support inequalities')
        region=g.polygon(g.constraints(images),g.PENT.copy())
        g.require(region==[point],'entire finite-motion closed fit region is exactly the corner singleton')
        pre=[next((k for k,v in enumerate(images) if v==g.V[i]),None) for i in g.CYCLE]
        g.require([g.CYCLE[k] for k,v in enumerate(pre) if v is None]==[20],'literal single missing spatial original corner preimage')
        rows=[]
        for i,j,k in [(4,0,{'G':15,'GH':9,'HB':12,'HBH':10}[name])]:
            line=g.line(i,j,images[k]);vals=[g.value(line,p) for p in g.PENT]
            g.require(vals[1]==0 and vals[0]<0 and vals[2]<0,'one affine actual support excludes every other point of the closed triangle')
            rows.append({'edge':[i,j],'original_source_vertex':k,'gap_affine_line':g.vec(line),'corner_values':list(map(g.enc,vals))})
        parents.append({'name':name,'original_spatial_corner_preimages':pre,'exact_fit_region':[g.vec(point)],'point_support_comparisons':len(gaps),'minimum_point_gap':g.enc(min(gaps)),'complete_point_support_stream_sha256':g.digest(list(map(g.enc,gaps))),'strict_exclusion_off_corner_rows':rows})
    M=Q(F(15,4));U=Q(F(-4,15));V=Q(F(8,15),F(-4,15));w=Q(1)
    qw=(1+M*U,-1+M*U,M*V+w,w-M*V)
    g.require(qw==(Q(),Q(-2),3-S,S-1),'literal original canonical boundary world quaternion')
    scalar,x,y,z=qw;norm=a.dot(qw,qw)
    Rh=((scalar*scalar+x*x-y*y-z*z,2*(x*y-scalar*z),2*(x*z+scalar*y)),(2*(x*y+scalar*z),scalar*scalar-x*x+y*y-z*z,2*(y*z-scalar*x)),(2*(x*z-scalar*y),2*(y*z+scalar*x),scalar*scalar-x*x-y*y+z*z))
    g.require(tuple(tuple(v/norm for v in row) for row in Rh)==G,'boundary canonical quaternion produces the original G exactly')
    rx,ry=point
    gauges=((rx+ry*w-M*V)*(rx+ry*w-M*V)-r2,(ry-rx*w+M*U)*(ry-rx*w+M*U)-r2)
    g.require(gauges==(Q(),Q()) and w==1 and all(-1<=v<=1 for v in (U,V,w)),'extra fit lies on BOTH actual canonical closed gauges and source boundary')
    return {'agent':'six-rupert-2','role':'researcher','scope':'explicit original extra boundary half-turn PROPER CLOSED fit, with boundary contacts retained; finite four-extra-motion singleton feasibility; six-parent all-source classification on this NEW triangle is refuted, no strict Rupert passage or exhaustive source classification','receiving_corner':g.vec(point),'receiving_raw':g.vec(raw),'halfturn_unit_quaternion':g.vec((Q(),*axis)),'extra_distinct_motion_count':len(distinct),'extra_motions':motion_records,'projected_convex_hull_corner_count':len(right),'complete_original_projection_hull_sha256':g.digest(list(map(g.vec,right))),'finite_parent_audits':parents,'canonical_source_M':g.enc(M),'canonical_source_U_V_w':g.vec((U,V,w)),'canonical_world_quaternion':g.vec(qw),'both_exact_canonical_gauges':list(map(g.enc,gauges)),'no_six_parent_strict_physical_or_old_collar_gauge_cover_can_contain_this_corner':True,'global_J74_Rupert_status':'OPEN','wall_seconds':time.monotonic()-started}

if __name__=='__main__':
    parser=argparse.ArgumentParser();parser.add_argument('--output',required=True);args=parser.parse_args()
    r=record();Path(args.output).write_text(json.dumps(r,indent=2)+'\n')
    print(json.dumps({k:v for k,v in r.items() if k not in ('extra_motions','finite_parent_audits')},indent=2))
