#!/usr/bin/env python3
"""six-reviewer-1: exact phase/rank-grid verifier; no author imports.

Diagnostics for the written motion lemmas, plus a direct polynomial
certificate verifier independent of any SAT/CNF encoding. Fractions only.
"""
import argparse
from collections import Counter, deque
from fractions import Fraction as F
from hashlib import sha256
from itertools import combinations, product
import json
from pathlib import Path

FOUR = ((1,0),(-1,0),(0,1),(0,-1))
NINE = tuple(product((-1,0,1), repeat=2))


def need(ok, message):
    if not ok:
        raise ValueError(message)


def normal(cells):
    cells = tuple(tuple(c) for c in cells)
    need(cells and all(len(c)==2 and all(type(v) is int for v in c) for c in cells), 'invalid integer cells')
    need(len(set(cells)) == len(cells), 'repeated tile cell')
    x0, y0 = min(x for x,y in cells), min(y for x,y in cells)
    return tuple(sorted((x-x0,y-y0) for x,y in cells))


def views(cells):
    return sorted({normal((sx*(y if swap else x),sy*(x if swap else y)) for x,y in cells)
                   for swap,sx,sy in product((False,True),(-1,1),(-1,1))})


def components(cells):
    remaining, count = set(cells), 0
    while remaining:
        count += 1
        queue = [remaining.pop()]
        for x,y in queue:
            for dx,dy in FOUR:
                p=(x+dx,y+dy)
                if p in remaining:
                    remaining.remove(p);queue.append(p)
    return count


def topology(cells):
    cells=set(cells)
    if not cells:
        return {'foreground_components':0,'holes':0,'diagonal_pinches':0,'disc':False}
    x0,x1=min(x for x,y in cells)-1,max(x for x,y in cells)+1
    y0,y1=min(y for x,y in cells)-1,max(y for x,y in cells)+1
    background={(x,y) for x in range(x0,x1+1) for y in range(y0,y1+1)}-cells
    holes=components(background)-1
    vertices={(x+dx,y+dy) for x,y in cells for dx,dy in product((0,1),repeat=2)}
    pinches=0
    for x,y in vertices:
        quadrants=[(x-1,y-1) in cells,(x,y-1) in cells,(x,y) in cells,(x-1,y) in cells]
        pinches += quadrants in ([True,False,True,False],[False,True,False,True])
    foreground=components(cells)
    return {'foreground_components':foreground,'holes':holes,'diagonal_pinches':pinches,
            'disc':foreground==1 and holes==0 and pinches==0}


def halo(cells):
    return {(x+dx,y+dy) for x,y in cells for dx,dy in NINE}


def rectangles(pose):
    level,shape,tx,ty=pose
    return tuple((tx+x,ty+y,tx+x+1,ty+y+1) for x,y in shape)


def all_rectangles(poses):
    return [(i,p[0],r) for i,p in enumerate(poses) for r in rectangles(p)]


def interval_axes(rects):
    xs=sorted({q for _,_,r in rects for q in (r[0],r[2])})
    ys=sorted({q for _,_,r in rects for q in (r[1],r[3])})
    # The guards distinguish exterior from a boundary of the finite grid.
    xs=[xs[0]-1,*xs,xs[-1]+1];ys=[ys[0]-1,*ys,ys[-1]+1]
    if (len(xs)-1)*(len(ys)-1)>2_000_000:
        raise RuntimeError('diagnostic grid exceeds resource boundary; no exclusion')
    return xs,ys


def occupancy(rects,xs,ys,depth):
    """Four range updates per rectangle, then an exact 2D prefix sum."""
    ix,iy={x:i for i,x in enumerate(xs)},{y:j for j,y in enumerate(ys)}
    delta=[[0]*len(ys) for _ in xs]
    for _,level,(x0,y0,x1,y1) in rects:
        if level>depth:continue
        a,b,c,d=ix[x0],iy[y0],ix[x1],iy[y1]
        delta[a][b]+=1;delta[c][b]-=1;delta[a][d]-=1;delta[c][d]+=1
    cells=set()
    for i in range(len(xs)-1):
        for j in range(len(ys)-1):
            delta[i][j]+=(delta[i-1][j] if i else 0)+(delta[i][j-1] if j else 0)-(delta[i-1][j-1] if i and j else 0)
            need(delta[i][j] in (0,1),'overlapping interiors')
            if delta[i][j]:cells.add((i,j))
    return cells


def contacts(poses):
    rects=[rectangles(p) for p in poses]
    boxes=[(min(r[0] for r in R),min(r[1] for r in R),max(r[2] for r in R),max(r[3] for r in R)) for R in rects]
    def meet(a,b):return max(a[0],b[0])<=min(a[2],b[2]) and max(a[1],b[1])<=min(a[3],b[3])
    edges=[]
    for i,j in combinations(range(len(poses)),2):
        if meet(boxes[i],boxes[j]) and any(meet(a,b) for a in rects[i] for b in rects[j]):edges.append((i,j))
    return edges


def check(tile,H,poses,holes_last=False):
    tile=normal(tile);need(type(H) is int and H>=0,'invalid depth')
    m,w,h=len(tile),max(x for x,y in tile)+1,max(y for x,y in tile)+1
    L=max(w,h);B=((w+2*H*L)*(h+2*H*L))//m
    need(poses and len(poses)<=B,'copy budget exceeded')
    allowed=views(tile)
    for level,shape,tx,ty in poses:
        need(type(level) is int and 0<=level<=H and tuple(shape) in allowed,'invalid level or orientation')
        need(isinstance(tx,F) and isinstance(ty,F),'nonrational diagnostic placement')
    roots=[i for i,p in enumerate(poses) if p[0]==0]
    need(len(roots)==1,'unique root required');root=roots[0]
    need(poses[root][1:]==(tile,F(0),F(0)),'wrong root')
    need(set(p[0] for p in poses)==set(range(H+1)),'missing layer')
    R=all_rectangles(poses)
    need(all(-H*L<=r[0] and r[2]<=w+H*L and -H*L<=r[1] and r[3]<=h+H*L for _,_,r in R),
         'contact-chain box exceeded')
    xs,ys=interval_axes(R)
    prefixes=[];old=set()
    for k in range(H+1):
        used=occupancy(R,xs,ys,k)
        need(not k or halo(old)<=used,'incomplete strict surround')
        t=topology(used)
        need((holes_last and k==H and k>0) or t['disc'],'prefix is not a closed disc')
        area=sum((xs[i+1]-xs[i])*(ys[j+1]-ys[j]) for i,j in used)
        tiles=sum(p[0]<=k for p in poses)
        need(area==m*tiles,'prefix area mismatch')
        prefixes.append({'level':k,'copies':tiles,'physical_area':str(area),**t})
        old=used
    E=contacts(poses)
    adjacency=[[] for _ in poses]
    for i,j in E:adjacency[i].append(j);adjacency[j].append(i)
    need(all(p[0]==0 or any(poses[j][0]<p[0] for j in adjacency[i]) for i,p in enumerate(poses)),
         'new tile does not meet the previous prefix')
    distances={root:0};queue=[root]
    for i in queue:
        for j in adjacency[i]:
            if j not in distances:distances[j]=distances[i]+1;queue.append(j)
    need(len(distances)==len(poses) and all(distances[i]==p[0] for i,p in enumerate(poses)),'rank/distance invariant failed')
    need(all(abs(poses[i][0]-poses[j][0])<=1 for i,j in E),'nonconsecutive levels touch')
    return {'copies':len(poses),'depth':H,'area_per_copy':m,'box':[w,h],'mesh_budget':B,
            'prefixes':prefixes,'contact_edges':len(E),'contact_graph_sha256':sha256(json.dumps(E,separators=(',',':')).encode()).hexdigest(),
            'rank_grid_cells':(len(xs)-1)*(len(ys)-1),'unit_rectangles':len(R),'ranks_equal_contact_distances':True}



def certificate(tile,H,rows,holes_last=False):
    need(type(H) is int and H>=0,'invalid certificate depth')
    tile=normal(tile);m=len(tile);w=max(x for x,y in tile)+1;h=max(y for x,y in tile)+1;L=max(w,h)
    q=((w+2*H*L)*(h+2*H*L))//m
    need(len(rows)<=q,'invalid certificate budget')
    allowed=views(tile);poses=[]
    for row in rows:
        need(len(row)==4 and all(type(v) is int for v in row),'invalid certificate row')
        level,orientation,nx,ny=row
        need(0<=orientation<len(allowed) and abs(nx)<=q*(w+H*L) and abs(ny)<=q*(h+H*L),
             'unbounded numerator or invalid orientation')
        poses.append((level,allowed[orientation],F(nx,q),F(ny,q)))
    return check(tile,H,poses,holes_last)


def compact_rows(tile,poses,q):
    allowed=views(normal(tile));rows=[]
    for level,S,x,y in poses:
        need((q*x).denominator==(q*y).denominator==1,'certificate is not on the mesh')
        rows.append([level,allowed.index(S),int(q*x),int(q*y)])
    return rows


def growth_components(seed,added=3):
    """Enumerate partitions of the extra connected components, not growth paths."""
    root=set(normal(seed))
    boundary={(x+dx,y+dy) for x,y in root for dx,dy in FOUR}-root
    clusters={1:{frozenset((p,)) for p in boundary}}
    for size in range(2,added+1):
        clusters[size]={C|{p} for C in clusters[size-1]
                        for x,y in C for dx,dy in FOUR
                        for p in ((x+dx,y+dy),) if p not in root and p not in C}
    raw=set()
    if added==1:raw=clusters[1]
    elif added==2:
        raw=clusters[2]|{a|b for a,b in combinations(clusters[1],2) if len(a|b)==2}
    elif added==3:
        raw=clusters[3]|{a|b for a in clusters[1] for b in clusters[2] if len(a|b)==3}
        raw|={a|b|c for a,b,c in combinations(clusters[1],3) if len(a|b|c)==3}
    else:raise ValueError('bounded component enumeration supports one to three additions')
    family=sorted({min(views(root|extra)) for extra in raw if topology(root|extra)['disc']})
    return family,{'extra_component_counts':{str(k):len(v) for k,v in clusters.items()},
                   'distinct_rooted_addition_sets':len(raw),'free_disc_shapes':len(family)}


def arithmetic_bounds(seed,manifest):
    family,details=growth_components(seed)
    family_hash=sha256((json.dumps(family,separators=(',',':'))+'\n').encode()).hexdigest()
    need(family_hash==manifest['family_sha256'] and len(family)==len(manifest['cases'])==1233,
         'component-family reconstruction differs')
    histogram,by_radius=Counter(),{};tilers=0
    for i,(S,row) in enumerate(zip(family,manifest['cases'])):
        need(row['i']==i and len(S)==20,'invalid case index or area')
        w=max(x for x,y in S)+1;h=max(y for x,y in S)+1;L=max(w,h)
        if 'radius' in row:
            r=row['radius'];need(type(r) is int and r>=0,'invalid blocking radius')
            upper=((w+2*r+2*L)*(h+2*r+2*L))//20-1
            histogram[upper]+=1;by_radius.setdefault(str(r),[]).append(upper)
        else:
            need('periodic' in row,'case has no supplied status');tilers+=1
    return {'component_enumeration':details,'family_sha256':family_hash,
            'conditional_unrestricted_upper_histogram':dict(sorted(histogram.items())),
            'conditional_finite_cases':sum(histogram.values()),'prior_periodic_cases_not_reverified':tilers,
            'by_supplied_blocking_radius':{r:{'cases':len(a),'min_upper':min(a),'max_upper':max(a)} for r,a in sorted(by_radius.items())},
            'trust':'arithmetic transfer only; the supplied SAT/periodic statuses are separate dependencies'}


def compress(poses,q):
    maps=[]
    for axis in (2,3):
        phases=sorted({p[axis]%1 for p in poses}|{F(0)})
        need(type(q) is int and q>=len(phases),'not enough mesh phases')
        maps.append({v:F(i,q) for i,v in enumerate(phases)})
    return [(k,S,F(x//1)+maps[0][x%1],F(y//1)+maps[1][y%1]) for k,S,x,y in poses]


def floored(poses):
    return [(k,S,F(x//1),F(y//1)) for k,S,x,y in poses]


def covered_area(poses,cell):
    x,y=cell
    return sum(max(F(0),min(c,x+1)-max(a,x))*max(F(0),min(d,y+1)-max(b,y))
               for _,_,(a,b,c,d) in all_rectangles(poses))


def load_fractional(raw):
    tile=normal(raw['cells']);poses=[]
    for p in raw['patch']:
        S=normal(p['shape'])
        need(list(p['shape'])==[list(c) for c in S],'unnormalized explicit orientation')
        x,y=p['translation'];poses.append((p['level'],S,F(x),F(y)))
    return tile,raw['depth'],poses


def load_integer(seed,witness):
    tile=normal(seed['cells']);poses=[]
    for p in witness['patch']:
        S=p['cells'];x0,y0=min(x for x,y in S),min(y for x,y in S)
        poses.append((p['level'],normal(S),F(x0),F(y0)))
    return tile,3,poses


def boundary_disc(cells):
    """Controls only: one simple boundary cycle, independent of floodfill."""
    cells=set(cells);edges=set()
    for x,y in cells:
        for a,b in (((x,y),(x+1,y)),((x+1,y),(x+1,y+1)),((x+1,y+1),(x,y+1)),((x,y+1),(x,y))):
            e=tuple(sorted((a,b)))
            if e in edges:edges.remove(e)
            else:edges.add(e)
    adjacent={}
    for a,b in edges:adjacent.setdefault(a,set()).add(b);adjacent.setdefault(b,set()).add(a)
    if not adjacent or any(len(n)!=2 for n in adjacent.values()):return False
    reached=set();queue=[next(iter(adjacent))]
    for p in queue:
        if p in reached:continue
        reached.add(p);queue.extend(adjacent[p]-reached)
    return reached==set(adjacent)


def controls(square_poses):
    grids=0
    for bits in range(512):
        cells={(i%3,i//3) for i in range(9) if bits>>i&1}
        need(topology(cells)['disc']==boundary_disc(cells),'small topology disagreement')
        grids+=1
    # Direct closed-set vertex stars versus the rank-grid halo criterion.
    strict=0
    oldchoices=[{(1,1)},{(0,0)},{(0,0),(1,0)},{(1,1),(2,2)}]
    for old in oldchoices:
        for bits in range(512):
            new={(i%3,i//3) for i in range(9) if bits>>i&1}
            vertices={(x+dx,y+dy) for x,y in old for dx,dy in product((0,1),repeat=2)}
            direct=old<=new and all(all((x-dx,y-dy) in new for dx,dy in product((0,1),repeat=2)) for x,y in vertices)
            need((halo(old)<=new)==direct,'strict containment disagreement')
            strict+=1
    # A difference-array grid is checked against exact midpoint predicates.
    arrangements=0
    for x,y in product((F(-2,3),F(0),F(3,5)),repeat=2):
        poses=[(0,((0,0),),x,y),(1,((0,0),),x+1,y)]
        R=all_rectangles(poses);xs,ys=interval_axes(R);actual=occupancy(R,xs,ys,1)
        literal={(i,j) for i in range(len(xs)-1) for j in range(len(ys)-1)
                 if any(a<(xs[i]+xs[i+1])/2<c and b<(ys[j]+ys[j+1])/2<d for _,_,(a,b,c,d) in R)}
        need(actual==literal,'difference-array/midpoint disagreement');arrangements+=1
    whole_cells=0
    for w,h in ((1,1),(2,1),(1,2),(2,2)):
        S=tuple(product(range(w),range(h)))
        for a,b in product(range(5),repeat=2):
            poses=[(0,S,F(i*w)+F(a,5),F(j*h)+F(b,5)) for i,j in product((-1,0),repeat=2)]
            for c in S:
                need(covered_area(poses,c)==covered_area(floored(poses),c)==1,'whole-cell flooring disagreement')
                whole_cells+=1
    # The shifted floor cannot save the seven-square surround for either x order.
    for offset in (F(0),F(1,4),F(1,2),F(3,4)):
        p=[(k,S,F((x+offset)//1)-F(offset//1),F(y//1)) for k,S,x,y in square_poses]
        try:check(((0,0),),1,p)
        except ValueError as e:need('surround' in str(e),'shifted-floor failed for an unrelated reason')
        else:raise ValueError('a shifted floor falsely preserved the surround')
    rejected=0
    corrupt=[]
    corrupt.append(square_poses[:-1]);corrupt.append([*square_poses,square_poses[0]])
    bad=list(square_poses);bad[0]=(0,bad[0][1],F(1,3),F(0));corrupt.append(bad)
    bad=list(square_poses);bad[1]=(2,*bad[1][1:]);corrupt.append(bad)
    bad=list(square_poses);bad[1]=(1,((0,0),(1,0)),bad[1][2],bad[1][3]);corrupt.append(bad)
    for bad in corrupt:
        try:check(((0,0),),1,bad)
        except ValueError:rejected+=1
        else:raise ValueError('bad corona accepted')
    rows=compact_rows(((0,0),),compress(square_poses,9),9)
    corrupt_rows=[]
    for column,value in ((0,True),(1,1),(2,19)):
        bad=[r[:] for r in rows];bad[1][column]=value;corrupt_rows.append(bad)
    bad=[r[:] for r in rows];bad[0][2]=1;corrupt_rows.append(bad)
    bad=[r[:] for r in rows];bad[1]=bad[1][:3];corrupt_rows.append(bad)
    for bad in corrupt_rows:
        try:certificate(((0,0),),1,bad)
        except ValueError:pass
        else:raise ValueError('bad compact certificate accepted')
    # Preserve the exact weak orders of all constituent rectangle endpoints.
    coords=[F(-7,3),F(-1),F(-2,7),F(0),F(2,7),F(1),F(19,8)]
    poses=[(0,((0,0),),x,F(0)) for x in coords]
    moved=compress(poses,len(coords)+1);comparisons=0
    for i,j,a,b in product(range(len(coords)),range(len(coords)),range(-2,3),range(-2,3)):
        u,v=coords[i]+a,coords[j]+b;mu,mv=moved[i][2]+a,moved[j][2]+b
        need((u>v)-(u<v)==(mu>mv)-(mu<mv),'phase compression changes endpoint order')
        comparisons+=1
    tiny=[]
    for added,count in ((1,1),(2,2),(3,5)):
        family,_=growth_components(((0,0),),added)
        need(len(family)==count,'tiny free-polyomino count differs')
        tiny.append({'cells':added+1,'free_shapes':count})
    # Resource refusal must remain distinct from a mathematical rejection.
    R=[(i,0,(F(2*i),F(2*i),F(2*i+1),F(2*i+1))) for i in range(712)]
    try:interval_axes(R)
    except RuntimeError:pass
    else:raise ValueError('resource refusal control failed')
    # All ordered connected-sector partitions of a filled contact star.
    def partitions(n):
        if n==0:return [()]
        return [(a,)+tail for a in (1,2,3) if a<=n for tail in partitions(n-a)]
    return {'complete_small_topology_patterns':grids,'strict_vertex_star_patterns':strict,
            'literal_midpoint_arrangements':arrangements,'whole_unit_cells_before_after_flooring':whole_cells,
            'shifted_floor_regimes_rejected':4,'malformed_coronas_rejected':rejected,
            'malformed_compact_certificates_rejected':len(corrupt_rows),
            'phase_endpoint_weak_order_comparisons':comparisons,'tiny_free_polyomino_controls':tiny,
            'operational_resource_refusals_distinct_from_rejections':1,
            'ordered_quarter_turn_sector_partitions':partitions(4)}


def main():
    parser=argparse.ArgumentParser(description=__doc__)
    here=Path(__file__).resolve().parent
    parser.add_argument('--motion-dir',type=Path,default=here.parent/'heesch_polyomino_motion_bridge')
    parser.add_argument('--prior-dir',type=Path,default=here.parent/'heesch_polyomino_euler_cnf')
    parser.add_argument('--write',type=Path)
    args=parser.parse_args()
    files={'fractional':args.motion_dir/'fractional_square.json','seed':args.prior_dir/'kaplan17.json',
           'seed_witness':args.prior_dir/'kaplan17_depth3.witness.json','growth_manifest':args.prior_dir/'growth20_manifest.json'}
    data={k:json.loads(p.read_text()) for k,p in files.items()}
    result={'agent':'six-reviewer-1','role':'independent mathematical reviewer',
            'input_sha256':{k:sha256(p.read_bytes()).hexdigest() for k,p in files.items()}}
    for name,loader in (('seven_square',lambda:load_fractional(data['fractional'])),
                        ('kaplan17',lambda:load_integer(data['seed'],data['seed_witness']))):
        tile,H,poses=loader();original=check(tile,H,poses);moved=compress(poses,original['mesh_budget']);compressed=check(tile,H,moved)
        need(contacts(poses)==contacts(moved),'contact graph changed under compression')
        need(original['prefixes']==compressed['prefixes'],'physical area/topology changed under compression')
        need(all((v*original['mesh_budget']).denominator==1 for p in moved for v in p[2:]),'not on the prescribed mesh')
        rows=compact_rows(tile,moved,original['mesh_budget'])
        need(certificate(tile,H,rows)==compressed,'compact certificate verifier differs')
        result[name]={'original':original,'compressed':compressed,'compact_certificate_rows':rows,'contact_graph_preserved':True}
    square=load_fractional(data['fractional'])[2]
    result['seven_square']['northeast_whole_cell_area']=str(covered_area(square,(1,1)))
    result['seven_square']['no_seven_copy_integer_grid_surround']=len(square)<9
    result['controls']=controls(square)
    result['conditional_growth_bounds']=arithmetic_bounds(data['seed']['cells'],data['growth_manifest'])
    result['kaplan17']['conditional_unrestricted_upper_from_radius10']=(38*37)//17-1
    # Every complete integer square-ring is a positive higher-depth fixture.
    rings=[]
    for H in range(4):
        poses=[(max(abs(x),abs(y)),((0,0),),F(x),F(y)) for x,y in product(range(-H,H+1),repeat=2)]
        r=check(((0,0),),H,poses);need(r['copies']==r['mesh_budget'],'square ring did not attain the area budget')
        rings.append(r)
    result['square_ring_controls']=rings
    result=json.loads(json.dumps(result))
    if args.write:args.write.write_text(json.dumps(result,indent=2,sort_keys=True)+'\n')
    else:need(result==json.loads((here/'expected.json').read_text()),'reviewer manifest differs')
    print(json.dumps(result,indent=2,sort_keys=True))


if __name__=='__main__':main()
