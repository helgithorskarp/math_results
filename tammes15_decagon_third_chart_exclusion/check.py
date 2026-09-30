"""Standalone exact closed-interval chart-cover and clique certificate checker."""
from pathlib import Path
from fractions import Fraction as Q
from itertools import combinations,product
from math import lcm
import argparse,copy,hashlib,json,sys,time
from model import core_points,LABELS,t_bernstein_forms,exact_rmin,P
from graph import five_clique

HERE=Path(__file__).resolve().parent
TARGETS=(((581,1000),(59,100)),((59,100),(1183,2000)),((1183,2000),(593,1000)))

def need(ok,message):
    if not ok:raise ValueError(message)

def digest(z):return hashlib.sha256(json.dumps(z,sort_keys=True,separators=(',',':')).encode()).hexdigest()

def verify_piece(data):
    started=time.monotonic();index=2
    lo,hi=[Q(*z) for z in data['interval']]
    need(Q(1,2)<lo<=hi<Q(3,5),'closed parameter domain')
    leaves=[tuple(z) for z in data['remaining_cover_cells']]
    refinements=[tuple(z) for z in data['refined_cells']]
    need(len(leaves)==len(set(leaves)) and len(refinements)==len(set(refinements)),'unique tree cells')
    need(all(type(x) is int for c in leaves+refinements for x in c),'integer cell indices')
    need(all(5<=d<=12 and 0<=i<2**d and 0<=j<2**d for d,i,j in leaves+refinements),'bounded canonical cells')
    ancestors=set()
    for d,i,j in leaves+refinements:
        while d:
            d-=1;i//=2;j//=2;ancestors.add((d,i,j))
    leafset=set(leaves);refinedset=set(refinements)
    need(not leafset&ancestors and not leafset&refinedset,'nonoverlapping frontier')
    depth=max(d for d,i,j in leaves+refinements)+1;grid=2**(depth-3)
    rational=t_bernstein_forms(index,lo,hi);integer=[]
    for row in rational:
        den=lcm(*(z.denominator for p in row for z in p))
        integer.append(list(zip(*[[int(z*den) for z in p] for p in row])))
    def witness(cell):
        d,i,j=cell;h=8*grid//2**d;u=-4*grid+i*h;v=-4*grid+j*h
        for ri,row in enumerate(integer):
            valid=True
            for f,l,m,a,b in row:
                c00=4*f*grid**2+4*l*u*grid+4*m*v*grid+4*a*(u*u+v*v)+4*b*u*v
                c10=2*h*(l*grid+2*a*u+b*v);c01=2*h*(m*grid+2*a*v+b*u)
                c20=4*h*h*a;c11=h*h*b
                for r,s in product(range(3),repeat=2):
                    if c00+r*c10+s*c01+(int(r==2)+int(s==2))*c20+r*s*c11<=0:
                        valid=False;break
                if not valid:break
            if valid:return ri
        return None
    discard=[];found=[];visited=[]
    def cover(cell):
        visited.append(cell)
        if cell in leafset:
            found.append(cell);return
        if cell in ancestors or cell in refinedset:
            d,i,j=cell
            for a,b in product((0,1),repeat=2):cover((d+1,2*i+a,2*j+b))
            return
        row=witness(cell)
        if row is None and cell[0]<5:
            d,i,j=cell
            for a,b in product((0,1),repeat=2):cover((d+1,2*i+a,2*j+b))
            return
        need(row is not None,'uncovered chart cell '+str(cell))
        discard.append([list(cell),row])
    cover((0,0,0))
    need(set(found)==leafset,'full exact cover matches all leaves')
    need(refinedset<=set(visited),'every requested refinement is reached')
    # G'(t) eigenvalues -1 and1-4t imply G decreases on this domain.
    # R minima at hi; all positive box quadratics are minimized exactly.
    leaves=sorted(leaves);boxes=[];rmins=[]
    for d,i,j in leaves:
        h=8*grid//2**d;boxes.append((-4*grid+i*h,-4*grid+j*h,-4*grid+(i+1)*h,-4*grid+(j+1)*h))
        rmins.append(exact_rmin((d,i,j),hi))
    n=len(leaves);adjacency=[0]*n;A=lo.denominator**2-lo.numerator**2;B=lo.numerator*(lo.denominator-lo.numerator)
    common=lo.denominator**2*grid**2
    def qmax(left,right):
        a,b,c,d=left;e,f,g,h=right
        return max(A*(u*u+v*v)+2*B*u*v for u in (a-g,c-e) for v in (b-h,d-f))
    for i in range(n):
        for j in range(i,n):
            maximum=qmax(boxes[i],boxes[j]);ri,rj=rmins[i],rmins[j]
            lhs=2*maximum*hi.denominator*ri.denominator*rj.denominator
            rhs=(hi.denominator-hi.numerator)*common*ri.numerator*rj.numerator
            if i==j:need(lhs<rhs,'single cell packing capacity1')
            elif lhs>=rhs:adjacency[i]|=1<<j;adjacency[j]|=1<<i
    need(all(not adjacency[i]&(1<<i) for i in range(n)),'no graph loops')
    clique,states=five_clique(adjacency,maxstates=2000000)
    need(clique is None,'remaining possible five-clique '+str(clique))
    result={'agent':'six-tammes-2','role':'researcher','status':'EXACT_CLOSED_INTERVAL_CHART_GRAPH_EXCLUSION',
            'type_index':index,'interval':[[z.numerator,z.denominator] for z in (lo,hi)],
            'cover_cells':n,'discarded_cells':len(discard),'refinements':len(refinements),
            'compatibility_edges':sum(z.bit_count() for z in adjacency)//2,'clique_search_states':states,
            'tree_sha256':digest([sorted(found),discard]),'graph_sha256':digest(adjacency),

            'trust_boundary':'Exact Python arithmetic and complete finite tree/graph; cited core coordinates and written chart, monotonicity and clique implication. Independent review pending.'}
    return result,leaves,adjacency,discard


def verify(certificate):
    need(certificate['format']==1 and certificate['core_key']==[6,50,-1],'fixed certificate/core')
    need(len(certificate['pieces'])==3,'complete three-piece interval cover')
    need([z['interval'] for z in certificate['pieces']]==[[list(v) for v in pair] for pair in TARGETS],'fixed consecutive closed intervals')
    points,D=core_points();contacts=[]
    need(all(P.metric(v,v)==P.mul(D,D) for v in points.values()),'all ten unit identities')
    for i,j in combinations(LABELS,2):
        gap=P.sub(P.mul(P.T,P.mul(D,D)),P.metric(points[i],points[j]))
        if not gap:contacts.append([i,j])
        else:need(P.closed_sign(gap,Q(581,1000),Q(593,1000))==1,'all core packing gaps')
    need(len(contacts)==17,'complete contact set')
    summaries=[verify_piece(z)[0] for z in certificate['pieces']]
    return {'agent':'six-tammes-2','role':'researcher','status':'AUTHOR_AUDITED_EXACT_CHART_GRAPH_EXCLUSION',
            'core_key':[6,50,-1],'canonical_mask':22644191811521,
            'certified_closed_interval':[[581,1000],[593,1000]],
            'core_coordinates_sha256':digest(points),'contacts':contacts,'pieces':summaries,
            'packing_extension_capacity':4,'fifteen_point_extensions':'excluded on the entire stated interval',
            'global_tammes15_bounds':'unchanged','independent_review':'pending',
            'trust_boundary':'Exact Python arithmetic; complete tree/graph; written chart and metric proof, not formalized.'}

def definition_clique(adjacency):
    return any(all(adjacency[i]&(1<<j) for i,j in combinations(v,2)) for v in combinations(range(len(adjacency)),5))

def selftest(certificate):
    # Every graph on five or six vertices, compared with the definition.
    count=0
    for n in (5,6):
        pairs=list(combinations(range(n),2))
        for mask in range(2**len(pairs)):
            adjacency=[0]*n
            for k,(i,j) in enumerate(pairs):
                if mask&(1<<k):adjacency[i]|=1<<j;adjacency[j]|=1<<i
            found,_=five_clique(adjacency)
            need((found is not None)==definition_clique(adjacency),'definition-level clique control')
            count+=1
    variants=[]
    z=copy.deepcopy(certificate);z['core_key']=[6,1,1];variants.append(z)
    z=copy.deepcopy(certificate);z['pieces']=z['pieces'][:1];variants.append(z)
    z=copy.deepcopy(certificate);z['pieces'][0]['interval'][1]=[589,1000];variants.append(z)
    z=copy.deepcopy(certificate);z['pieces'][0]['remaining_cover_cells'].append(z['pieces'][0]['remaining_cover_cells'][0]);variants.append(z)
    z=copy.deepcopy(certificate);z['pieces'][0]['refined_cells'].append(z['pieces'][0]['refined_cells'][0]);variants.append(z)
    z=copy.deepcopy(certificate);z['pieces'][0]['remaining_cover_cells'][0]=[5,-1,0];variants.append(z)
    z=copy.deepcopy(certificate);z['pieces'][0]['remaining_cover_cells'][0]=[0,0,0];variants.append(z)
    z=copy.deepcopy(certificate);z['pieces'][0]['remaining_cover_cells']=[];variants.append(z)
    for z in variants:
        try:verify(z)
        except (ValueError,KeyError,TypeError):pass
        else:raise ValueError('false certificate accepted')
    return count,len(variants)

if __name__=='__main__':
    parser=argparse.ArgumentParser();parser.add_argument('--selftest',action='store_true');args=parser.parse_args()
    data=json.loads((HERE/'certificate.json').read_text())
    if args.selftest:
        controls=selftest(data);print('controls: graphs='+str(controls[0])+', false certificates='+str(controls[1]),file=sys.stderr)
    print(json.dumps(verify(data),indent=2,sort_keys=True))
