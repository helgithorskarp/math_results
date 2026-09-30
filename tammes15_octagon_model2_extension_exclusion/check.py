"""Standalone exact octagon cover, obstruction and complete no-K7 verifier."""
from pathlib import Path
from fractions import Fraction as Q
from itertools import combinations,product
from math import lcm
import hashlib,json,sys,time
from model import core_points,LABELS,t_bernstein_forms,exact_rmin,P
from certificates import Rows,verify_dual
from polynomial import lower_bound
from graph import clique,verify_deletions

HERE=Path(__file__).resolve().parent
LO,HI=Q(29,50),Q(593,1000)
CONTACTS=((0,1),(0,7),(1,2),(1,7),(2,3),(2,6),(2,7),
          (3,4),(3,5),(3,6),(4,5),(5,6),(6,7))

def need(ok,message):
    if not ok:raise ValueError(message)

def digest(z):return hashlib.sha256(json.dumps(z,sort_keys=True,separators=(',',':')).encode()).hexdigest()

def cell(z):
    need(type(z) in (list,tuple) and len(z)==3 and all(type(v) is int for v in z),'integer cell')
    d,i,j=z
    need(0<=d<=12 and 0<=i<2**d and 0<=j<2**d,'canonical bounded cell')
    return d,i,j

def under(c,parent):
    d,i,j=c;e,a,b=parent
    return d>=e and i>>(d-e)==a and j>>(d-e)==b

def verify(data,details=False):
    started=time.monotonic()
    need(data['format']==1 and data['model_index']==2 and data['core_size']==8 and data['extra_points']==7,'fixed model and extension target')
    lo,hi=[P.decode(z) for z in data['interval']]
    need((lo,hi)==(LO,HI),'fixed complete closed interval')
    points,D=core_points();contacts=[]
    need(all(P.metric(v,v)==P.mul(D,D) for v in points.values()),'eight unit identities')
    for i,j in combinations(LABELS,2):
        gap=P.sub(P.mul(P.T,P.mul(D,D)),P.metric(points[i],points[j]))
        if not gap:contacts.append((i,j))
        else:need(P.closed_sign(gap,lo,hi)==1,'strict noncontact core packing gap')
    need(tuple(contacts)==CONTACTS,'exact thirteen-contact set')
    rows=Rows(lo,hi);single=[];singlegaps=[]
    for z in data['single_cells']:
        c=cell(z['cell']);singlegaps.append(verify_dual(rows.single(c),z));single.append(c)
    need(len(single)==len(set(single)),'distinct empty-cell certificates')
    pairgaps=[];paircuts=[]
    for k,z in enumerate(data['monomial_pairs']):
        need(type(z) is list and len(z)==3,'cell-pair lower-bound certificate')
        a,b=cell(z[0]),cell(z[1]);bound=lower_bound(a,b,lo,hi)
        need(bound>0 and bound==Q(z[2]),'uniform strict positive pair polynomial')
        pairgaps.append(bound);paircuts.append((a,b))
        if not details and (k+1)%400==0:print('exact monomial pairs '+str(k+1),file=sys.stderr,flush=True)
    condgaps=[]
    for z in data['conditioned_pairs']:
        need(len(z['cells'])==2,'two-cell affine certificate')
        a,b=(cell(v) for v in z['cells']);condgaps.append(verify_dual(rows.pair(a,b),z));paircuts.append((a,b))
    leaves=[cell(z) for z in data['remaining_cover_cells']]
    refinements=[cell(z) for z in data['refined_cells']]
    need(leaves and len(leaves)==len(set(leaves)) and len(refinements)==len(set(refinements)),'unique nonempty finite cover tree')
    need(all(d>=5 for d,i,j in leaves+refinements),'capacity-one tree depths')
    ancestors=set()
    for d,i,j in leaves+refinements:
        while d:
            d-=1;i//=2;j//=2;ancestors.add((d,i,j))
    leafset=set(leaves);refinedset=set(refinements)
    need(not leafset&ancestors and not leafset&refinedset,'nonoverlapping frontier')
    need(not any(under(c,p) for c in leaves for p in single),'no retained cell is certified empty')
    depth=max(d for d,i,j in leaves+refinements)+1;grid=2**(depth-3)
    rational=t_bernstein_forms(2,lo,hi);integer=[]
    for row in rational:
        den=lcm(*(z.denominator for p in row for z in p))
        integer.append(list(zip(*[[int(z*den) for z in p] for p in row])))
    def witness(c):
        d,i,j=c;h=8*grid//2**d;u=-4*grid+i*h;v=-4*grid+j*h
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
    def cover(c):
        visited.append(c)
        if c in leafset:found.append(c);return
        if c in ancestors or c in refinedset:
            d,i,j=c
            for a,b in product((0,1),repeat=2):cover((d+1,2*i+a,2*j+b))
            return
        empty=next((k for k,p in enumerate(single) if under(c,p)),None)
        if empty is not None:discard.append([list(c),'affine',empty]);return
        row=witness(c)
        if row is None and c[0]<5:
            d,i,j=c
            for a,b in product((0,1),repeat=2):cover((d+1,2*i+a,2*j+b))
            return
        need(row is not None,'uncovered chart cell '+str(c))
        discard.append([list(c),'bernstein',row])
    cover((0,0,0))
    need(set(found)==leafset and refinedset<=set(visited),'complete cover and every refinement reached')
    leaves=sorted(leaves);boxes=[];rmins=[];descendants={}
    for k,c in enumerate(leaves):
        d,i,j=c;h=8*grid//2**d
        boxes.append((-4*grid+i*h,-4*grid+j*h,-4*grid+(i+1)*h,-4*grid+(j+1)*h))
        rmins.append(exact_rmin(c,hi))
        while True:
            descendants.setdefault((d,i,j),[]).append(k)
            if not d:break
            d-=1;i//=2;j//=2
    n=len(leaves);adjacency=[0]*n
    A=lo.denominator**2-lo.numerator**2;B=lo.numerator*(lo.denominator-lo.numerator)
    common=lo.denominator**2*grid**2
    for i in range(n):
        a,b,c,d=boxes[i];ri=rmins[i]
        for j in range(i,n):
            e,f,g,h=boxes[j];rj=rmins[j]
            maximum=max(A*(u*u+v*v)+2*B*u*v for u in (a-g,c-e) for v in (b-h,d-f))
            lhs=2*maximum*hi.denominator*ri.denominator*rj.denominator
            rhs=(hi.denominator-hi.numerator)*common*ri.numerator*rj.numerator
            if i==j:need(lhs<rhs,'strict single-cell capacity one')
            elif lhs>=rhs:adjacency[i]|=1<<j;adjacency[j]|=1<<i
    basic_edges=sum(z.bit_count() for z in adjacency)//2
    for a,b in paircuts:
        for i in descendants.get(a,[]):
            for j in descendants.get(b,[]):
                if i!=j:adjacency[i]&=~(1<<j);adjacency[j]&=~(1<<i)
    need(all(not z&(1<<i) for i,z in enumerate(adjacency)),'loop-free graph')
    deletions=data['domination'];active=verify_deletions(adjacency,deletions)
    found_clique,states=clique(adjacency,active=active)
    need(found_clique is None,'a necessary seven-clique remains '+str(found_clique))
    result={'agent':'six-tammes-2','role':'researcher','status':'AUTHOR_AUDITED_EXACT_EIGHT_CORE_EXTENSION_EXCLUSION',
            'model_index':2,'core_size':8,'packing_extension_capacity':6,
            'certified_closed_interval':data['interval'],'contacts':[list(z) for z in contacts],
            'core_coordinates_sha256':digest(points),'cover_cells':n,'refinements':len(refinements),
            'discarded_cells':len(discard),'bernstein_discards':sum(z[1]=='bernstein' for z in discard),
            'affine_discards':sum(z[1]=='affine' for z in discard),'single_cell_certificates':len(single),
            'monomial_pair_certificates':len(pairgaps),'conditioned_pair_certificates':len(condgaps),
            'minimum_monomial_margin':str(min(pairgaps)),'maximum_affine_rhs':str(max(singlegaps+condgaps)),
            'basic_edges':basic_edges,'compatibility_edges':sum(z.bit_count() for z in adjacency)//2,
            'domination_deletions':len(deletions),'reduced_vertices':active.bit_count(),'clique_search_states':states,
            'tree_sha256':digest([leaves,discard]),'graph_sha256':digest(adjacency),'domination_sha256':digest(deletions),
            'global_tammes15_bounds':'unchanged','independent_peer_review':'pending',
            'trust_boundary':'Exact Python arithmetic and complete finite checks; written geometric reduction, not formalized.'}
    if not details:print('completed exact verification in %.3f seconds'%(time.monotonic()-started),file=sys.stderr)
    if details:return result,leaves,adjacency,discard,deletions,active,rmins,integer
    return result

if __name__=='__main__':
    print(json.dumps(verify(json.loads((HERE/'certificate.json').read_text())),indent=2,sort_keys=True))
