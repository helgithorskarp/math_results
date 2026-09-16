"""Integer denominator-12 verifier for the alternating-Moser P36 stop."""
from collections import Counter,deque
from fractions import Fraction as F
from itertools import combinations
from pathlib import Path
import copy,hashlib,json

# A point is eight integer coefficients divided by 12, in x/y copies of
# (1,sqrt(3),sqrt(11),sqrt(33)).
def need(ok,msg):
    if not ok: raise ValueError(msg)
def s_add(a,b): return tuple(x+y for x,y in zip(a,b))
def s_mul(a,b):
    out=[0]*4
    for i,x in enumerate(a):
        for j,y in enumerate(b):
            common=i&j
            out[i^j]+=x*y*(3 if common&1 else 1)*(11 if common&2 else 1)
    return tuple(out)
def p_add(a,b): return tuple(x+y for x,y in zip(a,b))
def sqnorm_delta(a,b):
    dx=tuple(a[i]-b[i] for i in range(4)); dy=tuple(a[i]-b[i] for i in range(4,8))
    return s_add(s_mul(dx,dx),s_mul(dy,dy))
UNIT=(144,0,0,0)
def raw(x): return (json.dumps(x,sort_keys=True,separators=(',',':'))+'\n').encode()
def digest(x): return hashlib.sha256(raw(x)).hexdigest()
def encode(point):
    axes=[]
    for start in (0,4):
        row=[]
        for n in point[start:start+4]:
            q=F(n,12); row.append([q.numerator,q.denominator])
        axes.append(row)
    return axes

def make_patch():
    rows=[]
    for a in range(-12,13):
        for b in range(-12,13):
            if a*a+a*b+b*b<=36:
                point=(6*(2*a+b),0,0,0,0,6*b,0,0)
                rows.append((point,(a,b)))
    rows.sort()
    return [p for p,_ in rows],[label for _,label in rows]

def rotate_rho(label):
    a,b=label
    return (5*(2*a+b),0,0,-b,0,5*b,2*a+b,0)

def construct():
    P,labels=make_patch(); v=(132,0,0,0,0,0,12,0); w=(-66,0,0,-6,0,66,-6,0); c=p_add(v,w)
    R=[rotate_rho(label) for label in labels]
    patches=[P,[p_add(v,p) for p in R],[p_add(c,p) for p in P],[p_add(w,p) for p in R]]
    occurrences={}
    for k,Q in enumerate(patches):
        for j,p in enumerate(Q): occurrences.setdefault(p,[]).append((k,j))
    points=sorted(occurrences); index={p:i for i,p in enumerate(points)}
    edges=[(i,j) for i,j in combinations(range(len(points)),2) if sqnorm_delta(points[i],points[j])==UNIT]
    patch_edges=[(i,j) for i,j in combinations(range(len(P)),2) if sqnorm_delta(P[i],P[j])==UNIT]
    inherited=set()
    for Q in patches:
        for i,j in patch_edges: inherited.add(tuple(sorted((index[Q[i]],index[Q[j]]))))
    return P,labels,patches,points,occurrences,edges,patch_edges,inherited

def tarjan(adjacency):
    n=len(adjacency); disc=[-1]*n; low=[0]*n; parent=[-1]*n; time=0; arts=set(); bridges=[]; comps=0
    def visit(u):
        nonlocal time
        disc[u]=low[u]=time; time+=1; children=0
        for v in adjacency[u]:
            if disc[v]<0:
                parent[v]=u; children+=1; visit(v); low[u]=min(low[u],low[v])
                if parent[u]<0 and children>1: arts.add(u)
                if parent[u]>=0 and low[v]>=disc[u]: arts.add(u)
                if low[v]>disc[u]: bridges.append(tuple(sorted((u,v))))
            elif v!=parent[u]: low[u]=min(low[u],disc[v])
    for u in range(n):
        if disc[u]<0: comps+=1; visit(u)
    return comps,arts,bridges

def geometry():
    P,labels,patches,points,occurrences,edges,patch_edges,inherited=construct()
    adjacency=[set() for _ in points]
    for a,b in edges: adjacency[a].add(b); adjacency[b].add(a)
    comps,arts,bridges=tarjan(adjacency)
    collisions=[]; pair_counter=Counter()
    for p,rows in sorted(occurrences.items()):
        if len(rows)>1: collisions.append([[k,*labels[j]] for k,j in rows])
        owners=sorted({k for k,_ in rows})
        for a,b in combinations(owners,2): pair_counter[a,b]+=1
    patch_adj=[set() for _ in range(4)]
    for a,b in pair_counter: patch_adj[a].add(b); patch_adj[b].add(a)
    pcom,parts,pbridges=tarjan(patch_adj)
    degree=list(map(len,adjacency)); alive=[True]*len(points); queue=deque(i for i,d in enumerate(degree) if d<4); peel=[]
    while queue:
        u=queue.popleft()
        if not alive[u]: continue
        alive[u]=False; peel.append(u)
        for v in sorted(adjacency[u]):
            if alive[v]:
                degree[v]-=1
                if degree[v]==3: queue.append(v)
    return {'P':P,'labels':labels,'patches':patches,'points':points,'occurrences':occurrences,
            'edges':edges,'edge_set':set(edges),'patch_edges':patch_edges,'inherited':inherited,
            'components':comps,'arts':arts,'bridges':bridges,'collisions':collisions,
            'pair_counter':pair_counter,'pcom':pcom,'parts':parts,'pbridges':pbridges,'alive':alive,'peel':peel}

def audit(data,b=None):
    need(data.get('schema')==1 and data.get('target_found') is False,'schema/scope')
    need(data.get('rho')=='(5+i*sqrt(11))/6' and data.get('translation_v')=='11+i*sqrt(11)' and data.get('translation_w')=='omega^2*v','frozen formulas')
    b=geometry() if b is None else b
    P=b['P']; labels=b['labels']; patches=b['patches']; points=b['points']; occurrences=b['occurrences']; edges=b['edges']
    need((len(P),len(b['patch_edges']))==(data['patch_vertices'],data['patch_edges'])==(127,342),'source patch')
    need(data['raw_labels']==508 and (len(points),len(edges))==(data['vertices'],data['edges'])==(504,1368),'physical graph counts')
    need(data['collision_multiplicity_histogram']==[[1,500],[2,4]],'collision histogram')
    need(data['collisions']==b['collisions'],'collision labels')
    pair_rows=[[a,c,n] for (a,c),n in sorted(b['pair_counter'].items())]
    need(data['patch_collision_pairs']==pair_rows==[[0,1,1],[0,3,1],[1,2,1],[2,3,1]],'patch contact cycle')
    need(len(b['inherited'])==data['inherited_union_edges']==1368 and len(set(edges)-b['inherited'])==data['extra_edges_beyond_inherited_union']==0,'no extra contacts')
    need((b['components'],len(b['arts']),len(b['bridges']))==(data['physical_components'],data['physical_articulations'],data['physical_bridges'])==(1,0,0),'physical nonseparability')
    need((b['pcom'],len(b['parts']),len(b['pbridges']))==(data['patch_contact_components'],data['patch_contact_articulations'],data['patch_contact_bridges'])==(1,0,0),'contact-cycle nonseparability')
    need(sum(b['alive'])==data['four_core_vertices']==0 and data['four_core_patch_memberships']==[],'empty four-core')
    need(data['peel_order_sha256']==digest(b['peel']),'peel commitment')
    need(data['point_sha256']==digest(list(map(encode,points))) and data['edge_sha256']==digest(edges),'graph hashes')
    word=data['colouring']; need(isinstance(word,str) and len(word)==len(points) and set(word)<={'0','1','2'},'three-colour word')
    need(all(word[a]!=word[c] for a,c in edges),'proper three-colouring')
    formula=[]
    for p in points:
        colours={(labels[j][0]-labels[j][1])%3 for _,j in occurrences[p]}
        need(len(colours)==1,'collision formula disagreement'); formula.append(str(colours.pop()))
    need(word==''.join(formula),'residue formula word')
    tri=data['source_triangle']; need(tri==[191,201,211] and all(i in {points.index(x) for x in patches[0]} for i in tri),'source triangle indices')
    need(all(tuple(sorted(e)) in b['edge_set'] for e in combinations(tri,2)),'source triangle edges')
    need(data['chromatic_number']==3,'exact chromatic claim')
    return {'status':'PASS','patch_vertices':len(P),'patch_edges':len(b['patch_edges']),'raw_labels':508,
            'vertices':len(points),'edges':len(edges),'all_pair_checks':len(points)*(len(points)-1)//2,
            'collisions':len(b['collisions']),'extra_edges_beyond_inherited_union':0,
            'physical_components':b['components'],'physical_articulations':len(b['arts']),'physical_bridges':len(b['bridges']),
            'patch_contact_components':b['pcom'],'patch_contact_articulations':len(b['parts']),'patch_contact_bridges':len(b['pbridges']),
            'four_core_vertices':sum(b['alive']),'peel_vertices':len(b['peel']),'proper_colour_edge_checks':len(edges),
            'triangle_edge_checks':3,'chromatic_number':3,'point_sha256':data['point_sha256'],'edge_sha256':data['edge_sha256'],'target_found':False}

def controls(data,b):
    bad=[]
    x=copy.deepcopy(data);x['translation_v']='10+i*sqrt(11)';bad.append(x)
    x=copy.deepcopy(data);x['collisions'].pop();bad.append(x)
    x=copy.deepcopy(data);x['extra_edges_beyond_inherited_union']=1;bad.append(x)
    x=copy.deepcopy(data);x['physical_articulations']=1;bad.append(x)
    x=copy.deepcopy(data);x['four_core_vertices']=1;bad.append(x)
    x=copy.deepcopy(data);x['colouring']='0'*len(x['colouring']);bad.append(x)
    x=copy.deepcopy(data);x['edge_sha256']='0'*64;bad.append(x)
    x=copy.deepcopy(data);x['target_found']=True;bad.append(x)
    for x in bad:
        try: audit(x,b)
        except (ValueError,TypeError,KeyError,IndexError): continue
        raise ValueError('malformed certificate accepted')
    return len(bad)

def main():
    here=Path(__file__).parent; blob=(here/'certificate.json').read_bytes(); data=json.loads(blob)
    need(raw(data)==blob,'canonical certificate'); b=geometry(); report=audit(data,b)
    report['malformed_certificate_rejections']=controls(data,b); report['certificate_bytes']=len(blob); report['certificate_sha256']=hashlib.sha256(blob).hexdigest()
    need(report==json.loads((here/'expected.json').read_text()),'expected report')
    print(json.dumps(report,sort_keys=True))
if __name__=='__main__': main()
