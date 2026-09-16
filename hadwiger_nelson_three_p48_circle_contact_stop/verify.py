"""Exact Cartesian checker. Imports neither the producer nor its field code."""
import argparse,hashlib,itertools,json,math
from fractions import Fraction as F
from pathlib import Path
DEN=336

def need(ok,message):
    if not ok:raise ValueError(message)
def clean(x):return {k:v for k,v in x.items() if v}
def num(x):return {} if not x else {1:F(x)}
def rad(x):return {x:F(1)}
def plus(x,y):
    z=x.copy()
    for k,v in y.items():z[k]=z.get(k,0)+v
    return clean(z)
def times(x,y):
    z={}
    for a,u in x.items():
        for b,v in y.items():
            g=math.gcd(a,b);k=a*b//(g*g)
            z[k]=z.get(k,0)+u*v*g
    return clean(z)
def scaled(x,c):return clean({k:v*c for k,v in x.items()})
def cp(x,y):return plus(x[0],y[0]),plus(x[1],y[1])
def cs(x,c):return scaled(x[0],c),scaled(x[1],c)
def cm(x,y):return plus(times(x[0],y[0]),scaled(times(x[1],y[1]),-1)),plus(times(x[0],y[1]),times(x[1],y[0]))
def cn(x):return plus(times(x[0],x[0]),times(x[1],x[1]))
def row(z):
    x,y=z
    need(not(set(x)-{1,33,105,385}) and not(set(y)-{3,11,35,1155}),'unexpected Cartesian coefficient')
    vals=[x.get(1,0),y.get(3,0),y.get(11,0),-x.get(33,0),y.get(35,0),-x.get(105,0),-x.get(385,0),-y.get(1155,0)]
    need(all(F(a*DEN).denominator==1 for a in vals),'nonintegral scaled coordinate')
    return tuple(int(a*DEN) for a in vals)
def cart(row):
    a,b,c,d,e,f,g,h=row
    return clean({1:a,33:-d,105:-f,385:-g}),clean({3:b,11:c,35:e,1155:-h})
def stream_hash(rows):return hashlib.sha256(''.join(','.join(map(str,r))+'\n' for r in rows).encode()).hexdigest()

def reconstruct():
    one=(num(1),{});zero=({},{});omega=(num(F(1,2)),scaled(rad(3),F(1,2)))
    r=(num(F(5,6)),scaled(rad(11),F(1,6)));A=cp((num(2),{}),omega);B=cm(r,A);delta=cp(B,cs(A,-1))
    v=cs(cm(delta,(num(1),scaled(rad(35),F(1,7)))),F(1,2))
    vp=cs(cm(delta,(num(1),scaled(rad(35),F(-1,7)))),F(1,2))
    need(cn(r)==num(1) and cn(v)==num(1),'rotations not unit')
    need(cn(delta)==num(F(7,3)) and cn(cp(v,cs(delta,-1)))==num(1),'circle contacts')
    need(cp(v,vp)==delta and cm(v,vp)==cs(cm(delta,delta),F(3,7)),'relative polynomial')
    need(any(row(v)[i] for i in range(4,8)),'v not outside E')
    source=[(a,b) for a in range(-8,9) for b in range(-8,9) if a*a+a*b+b*b<=48]
    need(len(source)==169,'P48 count')
    P=[cp((num(a),{}),cs(omega,b)) for a,b in source]
    layers=[[row(z) for z in P],[row(cm(r,z)) for z in P],[row(cp(A,cm(v,z))) for z in P]]
    points=sorted(set(itertools.chain.from_iterable(layers)));idx={p:i for i,p in enumerate(points)}
    need(len(points)%2==1,'odd support order')
    centroid=tuple(F(sum(p[k] for p in points),len(points)) for k in range(8))
    need(centroid not in idx,'central-symmetry exclusion failed')
    images=[[idx[z] for z in layer] for layer in layers];sets=list(map(set,images));xy=list(map(cart,points))
    edges=[]
    for i,j in itertools.combinations(range(len(points)),2):
        d=cp(xy[i],cs(xy[j],-1));n=cn(d)
        if n=={1:DEN*DEN}:edges.append((i,j))
    E=set(edges);inherited=set();internal=[]
    for s in sets:
        e={edge for edge in E if edge[0] in s and edge[1] in s};internal.append(len(e));inherited|=e
    overlaps=[[i,j,len(sets[i]&sets[j])] for i,j in itertools.combinations(range(3),2)]
    need(overlaps==[[0,1,1],[0,2,1],[1,2,0]],'unexpected overlap')
    need(len(points)==505 and internal==[456]*3,'physical cap or source graph')
    special={k:idx[row(z)] for k,z in [('O',zero),('A',A),('B',B),('C',cp(A,v))]}
    need(sets[0]&sets[1]=={special['O']} and sets[0]&sets[2]=={special['A']},'overlap roles')
    need(tuple(sorted((special['B'],special['C']))) in E,'missing cycle contact')
    extra=E-inherited
    cross={f'{i}-{j}':sum((a in sets[i] and b in sets[j]) or (b in sets[i] and a in sets[j]) for a,b in extra) for i,j in itertools.combinations(range(3),2)}
    M=[idx[row(z)] for z in [zero,one,omega,cp(one,omega),r,cm(r,omega),cm(r,cp(one,omega))]]
    me=[(i,j) for i,j in itertools.combinations(range(7),2) if tuple(sorted((M[i],M[j]))) in E]
    need(len(set(M))==7 and len(me)==11,'Moser geometry')
    need(not any(all(w[i]!=w[j] for i,j in me) for w in itertools.product(range(3),repeat=7)),'Moser three-colouring')
    adj=[set() for _ in points]
    for i,j in edges:adj[i].add(j);adj[j].add(i)
    def connected_without(deleted):
        start=next(i for i in range(len(points)) if i!=deleted);seen={start};front=[start]
        while front:
            for j in adj[front.pop()]:
                if j!=deleted and j not in seen:seen.add(j);front.append(j)
        return len(seen)==len(points)-(deleted is not None)
    need(connected_without(None),'disconnected graph')
    cuts=[i for i in range(len(points)) if not connected_without(i)]
    need(not cuts,'articulation found')
    summary=dict(vertices=len(points),edges=len(edges),coordinate_sha256=stream_hash(points),edge_sha256=stream_hash(edges),internal_edges=internal,overlaps=overlaps,extra_edges=len(extra),extra_edges_by_pair=cross,special=special,moser=M)
    return dict(summary=summary,edges=edges,points=points,moser_edges=me,extra_edges=sorted(extra),minimum_degree=min(map(len,adj)),articulations=cuts)

def check_word(word,n,edges,k):
    need(isinstance(word,str) and len(word)==n,'word length')
    need(set(word)<=set('0123456'[:k]),'colour alphabet')
    need(all(word[i]!=word[j] for i,j in edges),'monochromatic unit edge')
def check_certificate(cert,g):
    need(set(cert)=={'expected','four_word','five_word'},'certificate keys')
    need(cert['expected']==g['summary'],'geometry summary mismatch')
    check_word(cert['four_word'],len(g['points']),g['edges'],4)
    check_word(cert['five_word'],len(g['points']),g['edges'],5)
    return {'status':'VERIFIED_EXACT_FOUR_CHROMATIC_FIXED_ASSEMBLY','geometry':g['summary'],'all_physical_pairs_checked':len(g['points'])*(len(g['points'])-1)//2,'connected':True,'articulation_vertices':g['articulations'],'minimum_degree':g['minimum_degree'],'complete_extra_edges':g['extra_edges'],'moser_three_colour_assignments_exhausted':3**7,'four_word_sha256':hashlib.sha256(cert['four_word'].encode()).hexdigest(),'five_word_sha256':hashlib.sha256(cert['five_word'].encode()).hexdigest(),'centrally_symmetric':False,'no_common_point_of_full_lattices':True,'relative_trace_squared_norm':'7/3','unit_trace_field_theorem_applies':True,'record_candidate':False}

def main():
    p=argparse.ArgumentParser();p.add_argument('--certificate',type=Path,default=Path(__file__).with_name('certificate.json'));a=p.parse_args()
    cert=json.loads(a.certificate.read_text());print(json.dumps(check_certificate(cert,reconstruct()),indent=2,sort_keys=True))
if __name__=='__main__':main()
