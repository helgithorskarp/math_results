"""Definition-level audit: fixed-basis exact geometry and implication closure.

Imports no producer or earlier research executable. Explicit checks survive -O.
"""
from fractions import Fraction as Q
from itertools import combinations,product
from collections import Counter
from pathlib import Path
import argparse,copy,hashlib,json
RAD=(1,2,3,6,19,38,57,114)
POS={r:i for i,r in enumerate(RAD)}
ZERO=(Q(0),)*8
ONE=(Q(1),)+(Q(0),)*7
MUL=[]
for a in RAD:
    row=[]
    for b in RAD:
        overlap=1
        for p in (2,3,19):
            if a%p==0 and b%p==0:overlap*=p
        row.append((POS[a*b//overlap**2],overlap))
    MUL.append(row)

def require(ok,message):
    if not ok:raise ValueError(message)

def add(a,b):return tuple(x+y for x,y in zip(a,b))
def neg(a):return tuple(-x for x in a)
def mul(a,b):
    out=[Q(0)]*8
    for i,x in enumerate(a):
        if not x:continue
        for j,y in enumerate(b):
            if y:
                k,m=MUL[i][j];out[k]+=m*x*y
    return tuple(out)
def sub(a,b):return add(a,neg(b))
def ca(a,b):return add(a[0],b[0]),add(a[1],b[1])
def cs(a,b):return sub(a[0],b[0]),sub(a[1],b[1])
def norm(a,b):
    x,y=cs(a,b);return add(mul(x,x),mul(y,y))
SQRT3=tuple(Q(i==2) for i in range(8))
def rotate(z):
    x,y=z
    return tuple(v/2 for v in sub(x,mul(SQRT3,y))),tuple(v/2 for v in add(mul(SQRT3,x),y))
def encode(z):return [[[r,x.numerator,x.denominator] for r,x in zip(RAD,a) if x] for a in z]
def key(z):return tuple(tuple((r,x) for r,x in zip(RAD,a) if x) for a in z)
def raw(x):return (json.dumps(x,sort_keys=True,separators=(',',':'))+'\n').encode()
def digest(x):return hashlib.sha256(raw(x)).hexdigest()
def decode(z):
    require(isinstance(z,list) and len(z)==2,'point shape');axes=[]
    for axis in z:
        require(isinstance(axis,list),'axis shape');out=[Q(0)]*8;last=0
        for item in axis:
            require(isinstance(item,list) and len(item)==3 and all(type(x)is int for x in item),'coefficient shape')
            r,n,d=item;require(r in POS and r>last and n!=0 and d>0,'coefficient domain');x=Q(n,d)
            require(x.numerator==n and x.denominator==d,'reduced rational');out[POS[r]]=x;last=r
        axes.append(tuple(out))
    return tuple(axes)
def orbit(u):
    items=[u]
    for k in range(5):items.append(rotate(items[-1]))
    require(rotate(items[-1])==u,'sixth rotation')
    rep=min(items,key=key);z=rep
    for k in range(6):
        if z==u:return rep,k
        z=rotate(z)
    raise ValueError('orbit encoding')

def implications_sat(n,clauses):
    # Literal (v,b) means X_v=b. Build implications between truth literals.
    reach=[{i} for i in range(2*n)]
    for clause in clauses:
        if not clause:return False
        a,b=clause if len(clause)==2 else (clause[0],clause[0])
        i=2*a[0]+a[1];j=2*b[0]+b[1]
        reach[i^1].add(j);reach[j^1].add(i)
    for k in range(2*n):
        for i in range(2*n):
            if k in reach[i]:reach[i]|=reach[k]
    return all(not (2*v+1 in reach[2*v] and 2*v in reach[2*v+1]) for v in range(n))

def obstruction_type(clauses):
    if len(clauses)!=4:return None
    supports=[{v for v,b in c} for c in clauses]
    if any(len(x)!=2 for x in supports):return None
    for c,d in combinations(clauses,2):
        if not any((v,1-b) in d for v,b in c):return None
    used=set.union(*supports)
    if len(used)==2:return 'four_signs'
    common=set.intersection(*supports)
    if len(used)==3 and len(common)==1:
        h=next(iter(common));groups=[[c for c in clauses if (h,b) in c] for b in (0,1)]
        if all(len(g)==2 for g in groups):return 'two_opposite_forcing_pairs'
    raise ValueError('unclassified pairwise-incompatible four clauses')

def audit_census(data):
    rows=[];unsat=[];types=Counter();minimal=0
    for n in (2,3,4):
        options=[((i,a),(j,b)) for i,j in combinations(range(n),2) for a,b in product((0,1),repeat=2)]
        counts=[];hist=Counter()
        for m in range(5):
            for inds in combinations(range(len(options)),m):
                clauses=[options[i] for i in inds]
                # Inclusion-exclusion counts solutions from forbidden subcubes.
                count=0
                for mask in range(1<<m):
                    fixed={};consistent=True
                    for i,c in enumerate(clauses):
                        if mask>>i&1:
                            for v,b in c:
                                if v in fixed and fixed[v]!=1-b:consistent=False
                                fixed[v]=1-b
                    if consistent:count+=(-1)**mask.bit_count()*(1<<(n-len(fixed)))
                sat=implications_sat(n,clauses);require(sat==(count>0),'implication/count mismatch')
                kind=obstruction_type(clauses);require((kind is None)==sat,'classification mismatch')
                counts.append(count);hist[count]+=1
                if not sat:
                    unsat.append({'n':n,'clauses':[[list(l) for l in c] for c in clauses]});types[kind]+=1
                    for i in range(4):require(implications_sat(n,clauses[:i]+clauses[i+1:]),'not minimal');minimal+=1
        rows.append({'variables':n,'clause_options':len(options),'formulas':len(counts),'satisfying_assignment_histogram':{str(k):v for k,v in sorted(hist.items())},'count_stream_sha256':digest(counts)})
    require(data=={'rows':rows,'unsatisfiable':unsat},'census certificate mismatch')
    return {'formulas':sum(r['formulas'] for r in rows),'unsatisfiable':len(unsat),'obstruction_types':dict(sorted(types.items())),'minimal_clause_deletions':minimal}

def audit_geometry(data,positive):
    D=list(map(decode,data['centres']));require(len(D)==4 and len(set(D))==4,'four distinct centres')
    expected=([[[],[]],[[[1,1,1]],[]],[[[1,12,7]],[[3,1,7]]],[[[1,17,14]],[[3,9,14]]]] if positive else [[[],[]],[[[1,1,1]],[]],[[],[[3,1,1]]],[[[1,1,1]],[[3,1,1]]]])
    require(data['centres']==expected,'wrong placement')
    require(norm(D[0],D[1])==ONE and norm(D[2],D[3])==ONE,'unit segments')
    cross=((0,2),(0,3),(1,2),(1,3));roots=data['intersections'];require(len(roots)==4,'four root slots')
    I=[];dist=[];root_checks=0
    for (a,b),row in zip(cross,roots):
        q=norm(D[a],D[b]);require(all(v==0 for v in q[1:]) and q[0]>0,'squared distance rational positive');q=q[0];dist.append([q.numerator,q.denominator])
        want=0 if q>4 else 1 if q==4 else 2
        r=list(map(decode,row));require(len(r)==want and len(set(r))==want,'complete root multiplicity')
        require(r==sorted(r,key=key),'root order')
        for z in r:require(norm(z,D[a])==ONE and norm(z,D[b])==ONE,'root unit distances');root_checks+=2
        I.append(r)
    require(data['cross_squared_distances']==dist,'cross distances')
    reps=sorted({orbit(cs(z,D[h]))[0] for (a,b),row in zip(cross,I) for z in row for h in (a,b)},key=key)
    require(data['orbit_representatives']==list(map(encode,reps)),'orbit representatives');oi={z:i for i,z in enumerate(reps)}
    assignments=list(product((0,1),repeat=len(reps)));clauses=data['slot_clauses'];require(len(clauses)==4,'four clauses')
    checks=0;solutions=0
    for assignment in assignments:
        global_ok=True
        for ((a,b),row,c) in zip(cross,I,clauses):
            if c is not None:
                require(isinstance(c,list) and 1<=len(c)<=2,'clause length')
                require(c==sorted(c) and len({tuple(l) for l in c})==len(c),'clause normalization')
                for lit in c:require(len(lit)==2 and all(type(x)is int for x in lit) and 0<=lit[0]<len(reps) and lit[1] in (0,1),'literal domain')
                require(len({l[0] for l in c})==len(c),'unit/tautology normalization')
            formula=True if c is None else any(assignment[v]==value for v,value in c)
            for z in row:
                if z in D:continue
                v,k=orbit(cs(z,D[a]));w,l=orbit(cs(z,D[b]))
                colour_a=(assignment[oi[v]]+a+k)%2
                colour_b=2+(1-assignment[oi[w]]+(b-2)+l)%2
                eligibility=(colour_a!=(b-2) or colour_b!=2+a)
                require(eligibility==formula,'geometric clause truth table');checks+=1
            if not any(z not in D for z in row):require(c is None,'empty root slot')
            global_ok &= formula
        if global_ok:solutions+=1
    require(solutions==data['solutions'] and data['satisfiable']==(solutions>0),'solution count')
    active=[tuple(map(tuple,c)) for c in clauses if c is not None]
    require(implications_sat(len(reps),active)==bool(solutions),'geometric implication decision')
    report={'cross_squared_distances':dist,'direction_orbits':len(reps),'phase_solutions':solutions,'root_unit_distance_checks':root_checks,'clause_root_assignment_checks':checks}
    if not positive:
        require(not solutions,'negative control');z=decode(data['common_neighbour']);require(z not in D and all(norm(z,d)==ONE for d in D),'common neighbour')
        require(sorted(len(c) for c in clauses if c is not None)==[1,1],'two unit clauses')
        small=D+[z];edges=[(a,b) for a,b in combinations(range(5),2) if norm(small[a],small[b])==ONE]
        require(edges==[(0,1),(0,4),(1,4),(2,3),(2,4),(3,4)],'two triangles')
        colour=data['five_point_colouring'];require(colour==[0,1,0,1,2] and all(colour[a]!=colour[b] for a,b in edges),'three-colour witness')
        report['five_point_edges']=len(edges);report['five_point_colouring']=colour
        return report
    require(all(Q(*q) not in (1,4) for q in dist) and any(Q(*q)==3 for q in dist),'regular theorem hypotheses')
    require(sorted(len(c) for c in clauses if c is not None)==[2,2,2],'three proper binary clauses')
    S=[set(),set()]
    for g in (0,1):
        seeds=[cs(D[2*g+1],D[2*g])]
        for row in I:
            for z in row:
                for h in (2*g,2*g+1):
                    if norm(z,D[h])==ONE:seeds.append(cs(z,D[h]))
        for u in seeds:
            for k in range(6):S[g].add(u);u=rotate(u)
    V=sorted({ca(d,u) for h,d in enumerate(D) for u in S[h//2]},key=key)
    E=[(a,b) for a,b in combinations(range(len(V)),2) if norm(V[a],V[b])==ONE]
    require(data['directions']==[len(s) for s in S],'direction counts')
    require(data['vertices']==len(V) and data['edges']==len(E),'graph counts')
    require(data['point_sha256']==digest(list(map(encode,V))) and data['edge_sha256']==digest(E),'graph hashes')
    colours=data['colouring'];require(isinstance(colours,str) and len(colours)==len(V) and set(colours)<={'0','1','2','3'},'colour string');colours=list(map(int,colours))
    assignment=data['assignment'];require(len(assignment)==len(reps) and all(type(x)is int and x in (0,1) for x in assignment),'phase assignment')
    require(all(any(assignment[v]==b for v,b in c) for c in active),'assignment satisfies clauses')
    owners=0;phase_checks=0
    for z,c in zip(V,colours):
        own=[h for h,d in enumerate(D) if norm(z,d)==ONE];require(own,'owned point');owners+=len(own)
        if z in D:require(c==(2,3,0,1)[D.index(z)],'centre pin');continue
        group=c//2;require(any(h//2==group for h in own),'colour ownership')
        for h in own:
            require(c!=(2,3,0,1)[h],'owner colour')
            if h//2==group:
                v,k=orbit(cs(z,D[h]));alpha=assignment[oi[v]] if v in oi else 0
                expected=2*group+(alpha+group+h%2+k)%2;require(c==expected,'phase extension');phase_checks+=1
    for a,b in E:require(colours[a]!=colours[b],'monochromatic unit edge')
    report.update({'vertices':len(V),'edges':len(E),'point_pairs':len(V)*(len(V)-1)//2,'owner_incidences':owners,'phase_checks':phase_checks,'point_sha256':data['point_sha256'],'edge_sha256':data['edge_sha256']})
    return report

def audit(data):
    require(data.get('schema')==1 and data.get('target_found') is False,'scope/schema')
    return {'status':'PASS','regular_example':audit_geometry(data['regular_example'],True),'tangent_pin_obstruction':audit_geometry(data['tangent_pin_obstruction'],False),'boolean_census':audit_census(data['boolean_census']),'native_solver_calls':0,'target_found':False}

def controls(data):
    mutations=[]
    x=copy.deepcopy(data);x['regular_example']['intersections'][0].pop();mutations.append(('missing root',x,'geometry'))
    x=copy.deepcopy(data);x['regular_example']['intersections'][0][0][0][0][1]+=1;mutations.append(('bad root',x,'geometry'))
    x=copy.deepcopy(data);x['regular_example']['slot_clauses'][0]=[[0,0]];mutations.append(('false tautology',x,'geometry'))
    x=copy.deepcopy(data);x['regular_example']['slot_clauses'][1][0][1]^=1;mutations.append(('wrong literal sign',x,'geometry'))
    x=copy.deepcopy(data);x['regular_example']['colouring']='0'*x['regular_example']['vertices'];mutations.append(('monochromatic colouring',x,'geometry'))
    x=copy.deepcopy(data);x['regular_example']['point_sha256']='0'*64;mutations.append(('wrong graph',x,'geometry'))
    x=copy.deepcopy(data);x['tangent_pin_obstruction']['common_neighbour']=[[],[]];mutations.append(('false common neighbour',x,'negative'))
    x=copy.deepcopy(data);x['boolean_census']['unsatisfiable'].pop();mutations.append(('missing obstruction',x,'census'))
    x=copy.deepcopy(data);x['target_found']=True;mutations.append(('false record flag',x,'full'))
    for label,x,mode in mutations:
        try:
            if mode=='geometry':audit_geometry(x['regular_example'],True)
            elif mode=='negative':audit_geometry(x['tangent_pin_obstruction'],False)
            elif mode=='census':audit_census(x['boolean_census'])
            else:audit(x)
        except (ValueError,KeyError,TypeError,IndexError):continue
        raise ValueError('accepted malformed control: '+label)
    return len(mutations)

def main():
    ap=argparse.ArgumentParser();ap.add_argument('--out',required=True);args=ap.parse_args();out=Path(args.out);out.mkdir(parents=True,exist_ok=False)
    blob=(Path(__file__).parent/'certificate.json').read_bytes();data=json.loads(blob);require(raw(data)==blob,'canonical certificate')
    report=audit(data);report['malformed_certificate_rejections']=controls(data);report['certificate_bytes']=len(blob);report['certificate_sha256']=hashlib.sha256(blob).hexdigest()
    expected=Path(__file__).parent/'expected.json'
    if expected.exists():require(json.loads(expected.read_text())==report,'expected report mismatch')
    (out/'report.json').write_text(json.dumps(report,indent=2)+'\n');print(json.dumps(report))
if __name__=='__main__':main()
