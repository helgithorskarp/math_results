"""Independent quadratic-tower verifier for the frozen F3 completion."""
from fractions import Fraction as Q
from itertools import combinations
from pathlib import Path
import copy, hashlib, json

def need(ok,msg):
    if not ok: raise ValueError(msg)
def kadd(a,b): return a[0]+b[0],a[1]+b[1]
def kmul(a,b): return a[0]*b[0]+3*a[1]*b[1],a[0]*b[1]+a[1]*b[0]
def add(a,b): return tuple(x+y for x,y in zip(a,b))
def neg(a): return tuple(-x for x in a)
def sub(a,b): return add(a,neg(b))
def scale(a,q): return tuple(q*x for x in a)
def mul(a,b):
    # A+eta B, with A,B in Q(sqrt(3)) and eta^2=2sqrt(3).
    A,B=a[:2],a[2:]; C,D=b[:2],b[2:]
    return kadd(kmul(A,C),kmul((Q(0),Q(2)),kmul(B,D)))+kadd(kmul(A,D),kmul(B,C))
ZERO4=(Q(0),)*4; ONE4=(Q(1),Q(0),Q(0),Q(0)); SQRT3=(Q(0),Q(1),Q(0),Q(0)); ETA=(Q(0),Q(0),Q(1),Q(0))
def ca(a,b): return add(a[0],b[0]),add(a[1],b[1])
def cn(a): return neg(a[0]),neg(a[1])
def cs(a,b): return ca(a,cn(b))
def cm(a,b): return sub(mul(a[0],b[0]),mul(a[1],b[1])),add(mul(a[0],b[1]),mul(a[1],b[0]))
def norm(a,b):
    x,y=cs(a,b); return add(mul(x,x),mul(y,y))
ZERO=(ZERO4,ZERO4); ONE=(ONE4,ZERO4)
OMEGA=(scale(ONE4,Q(1,2)),scale(SQRT3,Q(1,2)))
U=[ONE]
for _ in range(5): U.append(cm(U[-1],OMEGA))

def coeff(a): return a[0],a[2],a[1]/2,a[3]/2
def key(z): return coeff(z[0]),coeff(z[1])
def encode(z): return [[[x.numerator,x.denominator] for x in coeff(a)] for a in z]
def raw(x): return (json.dumps(x,sort_keys=True,separators=(',',':'))+'\n').encode()
def digest(x): return hashlib.sha256(raw(x)).hexdigest()

def source():
    zeta=U[2]; a1=U[4]
    u=(scale(SQRT3,Q(1,2)),scale(ONE4,Q(-1,2)))
    y=cm(u,(scale(sub(ONE4,SQRT3),Q(1,2)),scale(ETA,Q(1,2))))
    z=cm(u,(scale(sub(ONE4,SQRT3),Q(1,2)),scale(ETA,Q(-1,2))))
    centres=[ZERO,a1,cs(cn(ONE),y),ca(cn(zeta),z)]
    tips=[cn(ONE),cn(zeta)]
    cross=[(0,2),(0,3),(1,2),(1,3)]
    roots=[sorted([tips[j-2],cs(ca(centres[i],centres[j]),tips[j-2])],key=key) for i,j in cross]
    directions=[set(),set()]
    for group in range(2):
        seeds=[cs(centres[2*group+1],centres[2*group])]
        for (i,j),row in zip(cross,roots):
            seeds.extend(cs(x,centres[i if group==0 else j]) for x in row)
        for seed in seeds: directions[group].update(cm(seed,r) for r in U)
    return sorted({ca(c,d) for h,c in enumerate(centres) for d in directions[h//2]},key=key)

def edge_list(points):
    return [(i,j) for i,j in combinations(range(len(points)),2) if norm(points[i],points[j])==ONE4]

def construct():
    old=source(); old_edges=edge_list(old); old_set=set(old)
    adjacency=[set() for _ in old]
    for i,j in old_edges: adjacency[i].add(j); adjacency[j].add(i)
    candidates=set(); route_checks=0
    for r in range(len(old)):
        for p,q in combinations(sorted(adjacency[r]),2):
            x=cs(ca(old[p],old[q]),old[r]); route_checks+=2
            need(norm(x,old[p])==norm(x,old[q])==ONE4,'rhombus route')
            if x not in old_set: candidates.add(x)
    histogram={}; selected=[]; contact_checks=0
    for x in sorted(candidates,key=key):
        contacts=0
        for v in old:
            contacts+=norm(x,v)==ONE4; contact_checks+=1
        histogram[contacts]=histogram.get(contacts,0)+1
        if contacts>=3: selected.append(x)
    points=sorted(old+selected,key=key); indices=[points.index(v) for v in old]
    graph_edges=edge_list(points); edge_set=set(graph_edges)
    return {'old':old,'old_edges':old_edges,'candidates':candidates,'histogram':histogram,
            'selected':selected,'points':points,'indices':indices,'graph_edges':graph_edges,
            'edge_set':edge_set,'route_checks':route_checks,'contact_checks':contact_checks}

def audit(data,built=None):
    need(data.get('schema')==1 and data.get('completion_threshold')==3,'schema/threshold')
    need(data.get('target_found') is False and data.get('chromatic_number')==3,'scope/chromatic claim')
    b=construct() if built is None else built
    old=b['old']; old_edges=b['old_edges']; candidates=b['candidates']; histogram=b['histogram']
    selected=b['selected']; points=b['points']; indices=b['indices']; graph_edges=b['graph_edges']; edge_set=b['edge_set']
    route_checks=b['route_checks']; contact_checks=b['contact_checks']
    need((len(old),len(old_edges))==(data['source_vertices'],data['source_edges'])==(74,198),'source graph')
    need(len(candidates)==data['all_new_candidates']==506,'candidate count')
    need([[k,histogram[k]] for k in sorted(histogram)]==data['candidate_contact_histogram']==[[2,374],[3,100],[4,22],[5,10]],'contact histogram')
    need(len(selected)==data['selected_new_points']==132,'selected count')
    need((len(points),len(graph_edges))==(data['vertices'],data['edges'])==(206,834),'complete graph')
    need(data['source_index_sha256']==digest(indices),'source index hash')
    need(data['point_sha256']==digest(list(map(encode,points))) and data['edge_sha256']==digest(graph_edges),'graph hashes')
    colour=data['colouring']; need(isinstance(colour,str) and len(colour)==len(points) and set(colour)<={'0','1','2'},'colour word')
    word=list(map(int,colour)); need(all(word[i]!=word[j] for i,j in graph_edges),'proper three-colouring')
    triangle=data['source_triangle']; need(isinstance(triangle,list) and len(triangle)==3 and triangle==sorted(triangle) and len(set(triangle))==3,'triangle format')
    need(all(i in set(indices) for i in triangle),'triangle lies in source')
    need(all(tuple(sorted((i,j))) in edge_set for i,j in combinations(triangle,2)),'unit triangle')
    need(data['colour_search_nodes']==239,'producer search statistic')
    return {
      'status':'PASS','source_vertices':len(old),'source_edges':len(old_edges),
      'all_new_candidates':len(candidates),'candidate_contact_histogram':data['candidate_contact_histogram'],
      'selected_new_points':len(selected),'vertices':len(points),'edges':len(graph_edges),
      'source_pair_norm_checks':len(old)*(len(old)-1)//2,
      'candidate_old_contact_checks':contact_checks,'rhombus_route_contact_checks':route_checks,
      'final_pair_norm_checks':len(points)*(len(points)-1)//2,
      'proper_colour_edge_checks':len(graph_edges),'triangle_edge_checks':3,
      'point_sha256':data['point_sha256'],'edge_sha256':data['edge_sha256'],
      'chromatic_number':3,'target_found':False
    }

def controls(data,built):
    bad=[]
    x=copy.deepcopy(data); x['completion_threshold']=4; bad.append(x)
    x=copy.deepcopy(data); x['candidate_contact_histogram'][0][1]+=1; bad.append(x)
    x=copy.deepcopy(data); x['selected_new_points']-=1; bad.append(x)
    x=copy.deepcopy(data); x['colouring']='1'+x['colouring'][1:]; bad.append(x)
    x=copy.deepcopy(data); x['source_triangle'][2]=x['source_triangle'][1]; bad.append(x)
    x=copy.deepcopy(data); x['edge_sha256']='0'*64; bad.append(x)
    x=copy.deepcopy(data); x['target_found']=True; bad.append(x)
    for x in bad:
        try: audit(x,built)
        except (ValueError,TypeError,KeyError,IndexError): continue
        raise ValueError('malformed certificate accepted')
    return len(bad)

def main():
    here=Path(__file__).parent; blob=(here/'certificate.json').read_bytes(); data=json.loads(blob)
    need(raw(data)==blob,'canonical certificate')
    built=construct(); report=audit(data,built); report['malformed_certificate_rejections']=controls(data,built)
    report['certificate_bytes']=len(blob); report['certificate_sha256']=hashlib.sha256(blob).hexdigest()
    need(report==json.loads((here/'expected.json').read_text()),'expected report')
    print(json.dumps(report,sort_keys=True))
if __name__=='__main__': main()
