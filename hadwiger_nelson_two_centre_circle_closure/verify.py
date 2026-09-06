"""Independent rotations, exact circle coverage and finite colouring audit."""
import argparse, hashlib, json, math, time
from fractions import Fraction as R
from itertools import combinations, permutations, product
from pathlib import Path
HERE = Path(__file__).resolve().parent

def need(ok, message):
    if not ok:
        raise ValueError(message)

# Real quadratic numbers a+b*sqrt3, used as real/imaginary coordinates.
def add(a,b): return (a[0]+b[0],a[1]+b[1])
def neg(a): return (-a[0],-a[1])
def mul(a,b): return (a[0]*b[0]+3*a[1]*b[1],a[0]*b[1]+a[1]*b[0])
def pointadd(x,y): return tuple(add(a,b) for a,b in zip(x,y))
def pointsub(x,y): return pointadd(x,tuple(neg(a) for a in y))
def cmul(x,y): return add(mul(x[0],y[0]),neg(mul(x[1],y[1]))),add(mul(x[0],y[1]),mul(x[1],y[0]))
def sqdist(x,y):
    a,b = pointsub(x,y)
    return add(mul(a,a),mul(b,b))

def patch_audit(c):
    need(c['coordinate_map']=='(s,t) -> (s*sqrt3/2,t/2)','wrong map')
    u = ((R(0),R(0)),(R(0),R(0)))
    v = ((R(0),R(1)),(R(0),R(0)))
    rho = ((R(1,2),R(0)),(R(0),R(1,2)))
    p = ((R(0),R(1,2)),(R(1,2),R(0)))
    A = [p]
    for _ in range(5): A.append(cmul(A[-1],rho))
    need(cmul(A[-1],rho)==p and len(set(A))==6,'rotation orbit')
    B = [pointadd(v,x) for x in A]
    expected = list(dict.fromkeys([u,v]+A+B))
    need(all(len(x)==2 and all(type(a) is int for a in x) for x in c['vertices']),'bad patch coordinate')
    V = [((R(0),R(s,2)),(R(t,2),R(0))) for s,t in c['vertices']]
    need(V==expected and len(set(V))==12 and c['centres']==[0,1],'patch domain')
    rings = [[V.index(x) for x in ring] for ring in (A,B)]
    need(c['rings']==rings and len(set(rings[0])&set(rings[1]))==2,'ring domain')
    dist = {e:sqdist(V[e[0]],V[e[1]]) for e in combinations(range(12),2)}
    edges = [list(e) for e,d in dist.items() if d==(1,0)]
    need(edges==c['edges'] and len(edges)==23,'patch graph')
    colors = c['colours']
    need(len(colors)==12 and all(type(a) is int and 0<=a<4 for a in colors),'colour range')
    need(colors[0]==2 and colors[1]==0 and all(colors[a]!=colors[b] for a,b in edges),'patch colouring')
    common = set(rings[0])&set(rings[1])
    need(sorted(colors[i] for i in common)==[1,3],'common edge colours')
    closure = []
    intersections = 0
    for side, ring in enumerate(rings):
        other = V[1-side]
        for i in ring:
            squared = sqdist(V[i],other)
            need(squared in ((1,0),(4,0),(7,0)),'unexpected other-centre distance')
            ys = [j for j,y in enumerate(V) if sqdist(y,V[i])==sqdist(y,other)==(1,0)]
            # Two distinct unit circles have2 intersections for centre
            # distance1,1 for distance2, and0 for distance sqrt7>2.
            need(len(ys)=={1:2,4:1,7:0}[squared[0]],'incomplete circle witnesses')
            need(all(j in rings[1-side] for j in ys),'witness outside other ring')
            closure.append([side,i,int(squared[0]),ys])
            intersections += len(ys)
    need(closure==c['cross_circle_closure'],'closure rows mismatch')
    ordered_centres = set()
    for perm in permutations(range(4)):
        row = [perm[a] for a in colors]
        need(all(row[a]!=row[b] for a,b in edges),'colour permutation')
        ordered_centres.add((row[0],row[1]))
    need(len(ordered_centres)==12 and all(a!=b for a,b in ordered_centres),'distinct centre coverage')
    return {'patch_vertices':12,'patch_pair_norms':66,'patch_edges':23,
            'directed_circle_closure_cases':len(closure),'certified_circle_intersections':intersections,
            'patch_colour_permutations_checked':24,'prescribed_distinct_centre_pairs':12}

def orbit_audit(c):
    rho = ((R(1,2),R(0)),(R(0),R(1,2)))
    one = ((R(1),R(0)),(R(0),R(0)))
    roots = [one]
    for _ in range(5): roots.append(cmul(roots[-1],rho))
    need(cmul(roots[-1],rho)==one and len(set(roots))==6,'sixth roots')
    rows = []
    for j,z in enumerate(roots):
        d = sqdist(z,one)
        need(d[1]==0 and d[0].denominator==1,'nonintegral orbit chord')
        rows.append([j,j%2,int(d[0]),4-int(d[0])])
    need(c['columns']==['step','parity','chord_squared','centre_distance_squared'] and c['rows']==rows,'orbit rows')
    edges = [(j,(j+1)%6) for j in range(6)]
    binary = [row for row in product(range(2),repeat=6) if all(row[a]!=row[b] for a,b in edges)]
    need(len(binary)==2,'circle not an even cycle')
    for j in range(6):
        need(any(row[0]==row[j] for row in binary)==(j%2==0),'parity compatibility')
    need({row[3] for row in rows if row[1] and row[3]>0}=={3},'exceptional positive separation')
    return {'orbit_chord_cases':6,'binary_circle_assignments_checked':64,
            'proper_circle_bipartitions':2,'positive_exceptional_squared_separations':[3]}

def sharp_audit(c):
    need(c['coordinate_scale']==12 and c['basis']==['1','sqrt3','sqrt11','sqrt33'],'sharpness field')
    V = c['vertices']
    need(len(V)==7 and all(len(p)==2 and all(len(a)==4 and all(type(t) is int for t in a) for a in p) for p in V),'sharpness coordinates')
    need(len({tuple(tuple(a) for a in p) for p in V})==7,'coincident sharpness vertices')
    radicals = (1,3,11,33)
    def squared(a,b):
        total = dict.fromkeys(radicals,0)
        for x,y in zip(a,b):
            delta = [s-t for s,t in zip(x,y)]
            for i,r in enumerate(radicals):
                for j,s in enumerate(radicals):
                    g = math.gcd(r,s)
                    total[r*s//(g*g)] += delta[i]*delta[j]*g
        return tuple(total[r] for r in radicals)
    E = [list(e) for e in combinations(range(7),2) if squared(V[e[0]],V[e[1]])==(144,0,0,0)]
    need(E==c['edges'] and len(E)==11,'sharpness graph')
    need(c['dominating_pair']==[0,3],'wrong dominating pair')
    covered = {0,3}
    for a,b in E:
        if a in (0,3): covered.add(b)
        if b in (0,3): covered.add(a)
    need(covered==set(range(7)),'not dominated')
    need(squared(V[0],V[3])==(432,0,0,0),'wrong sharpness centre separation')
    row = c['colours']
    need(len(row)==7 and all(type(x) is int and 0<=x<4 for x in row) and all(row[a]!=row[b] for a,b in E),'sharpness positive colouring')
    examined = 0
    for row in product(range(3),repeat=7):
        need(any(row[a]==row[b] for a,b in E),'sharpness has a three-colouring')
        examined += 1
    return {'sharpness_vertices':7,'sharpness_pair_norms':21,'sharpness_edges':11,
            'sharpness_dominating_pair_verified':True,'sharpness_three_colour_assignments_refuted':examined,
            'sharpness_chromatic_number':4}

def audit(c):
    return {**patch_audit(c['patch']),**orbit_audit(c['orbit_chords']),**sharp_audit(c['sharpness'])}

def main():
    p = argparse.ArgumentParser()
    p.add_argument('--work',required=True)
    a = p.parse_args()
    start = time.monotonic()
    raw = (HERE/'certificate.json').read_bytes()
    c = json.loads(raw)
    r = audit(c)
    for label in ('coordinate','colour','closure','orbit','sharpness'):
        bad = json.loads(raw)
        if label=='coordinate': bad['patch']['vertices'][2][0] += 1
        elif label=='colour': bad['patch']['colours'][2] = 2
        elif label=='closure': bad['patch']['cross_circle_closure'][0][3].pop()
        elif label=='orbit': bad['orbit_chords']['rows'][1][3] = 2
        else: bad['sharpness']['edges'].pop()
        try: audit(bad)
        except ValueError: pass
        else: raise ValueError('malformed certificate accepted: '+label)
    r.update({'status':'PASS','malformed_certificate_rejections':5,'certificate_bytes':len(raw),
              'certificate_sha256':hashlib.sha256(raw).hexdigest(),'native_solver_calls':0})
    if (HERE/'expected.json').exists():
        need(r==json.loads((HERE/'expected.json').read_text()),'expected mismatch')
    out = Path(a.work)
    out.mkdir(parents=True,exist_ok=True)
    (out/'verification.json').write_text(json.dumps(r,indent=2)+'\n')
    print(json.dumps({**r,'seconds':time.monotonic()-start},sort_keys=True))
if __name__=='__main__':
    main()
