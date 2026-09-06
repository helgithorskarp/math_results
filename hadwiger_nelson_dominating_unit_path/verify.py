"""Independent polarization, exact circle/line root counts, and positive patch checks."""
from pathlib import Path
from itertools import combinations,product
from collections import Counter
import argparse,copy,hashlib,json,math,time

HERE=Path(__file__).resolve().parent
Z=(0,)*8
ONE=(1,)+(0,)*7
SQRT3=(0,1)+(0,)*6
ORIGIN=(Z,Z)

def require(ok,why):
    if not ok:raise ValueError(why)

def plus(a,b):return tuple(x+y for x,y in zip(a,b))
def minus(a,b):return tuple(x-y for x,y in zip(a,b))
def scale(a,s):return tuple(s*x for x in a)
def mul(a,b):
    out=[0]*8
    for i,x in enumerate(a):
        if not x:continue
        for j,y in enumerate(b):
            if not y:continue
            common=i&j
            out[i^j]+=x*y*(3 if common&1 else 1)*(5 if common&2 else 1)*(11 if common&4 else 1)
    return tuple(out)
def cplus(a,b):return (plus(a[0],b[0]),plus(a[1],b[1]))
def cminus(a,b):return (minus(a[0],b[0]),minus(a[1],b[1]))
def cmul(a,b):
    return (minus(mul(a[0],b[0]),mul(a[1],b[1])),plus(mul(a[0],b[1]),mul(a[1],b[0])))
def norm(a):return plus(mul(a[0],a[0]),mul(a[1],a[1]))
def distance(a,b):return norm(cminus(a,b))

def decode(v):
    require(len(v)==16 and all(type(x) is int for x in v),'coordinate encoding')
    return (tuple(v[:8]),tuple(v[8:]))

def cart2(a,b):return (scale(ONE,2*a+b),scale(SQRT3,b))
def evaluate(form,beta,beta_scale):
    s=cart2(*form[:2]);t=cart2(*form[2:])
    return cplus((scale(s[0],beta_scale),scale(s[1],beta_scale)),cmul(t,beta))

CENTRES=[(0,0,0,0),(1,0,0,0),(0,0,1,0)]
ROOTS=[(1,0),(0,1),(-1,1),(-1,0),(0,-1),(1,-1)]
DIRECTIONS=[(a,b,0,0) for a,b in ROOTS]+[(0,0,a,b) for a,b in ROOTS]

def canonical(eq):
    g=math.gcd(*eq)
    require(g>0,'nonzero equation')
    e=tuple(x//g for x in eq)
    return e if next(x for x in e if x)>0 else tuple(-x for x in e)

def polarized(f,g,target):
    # Squared distances at beta=1,-1,i, with coordinates scaled by2.
    values=[]
    for b in [(ONE,Z),(scale(ONE,-1),Z),(Z,ONE)]:
        n=distance(evaluate(f,b,1),evaluate(g,b,1))
        require(all(x%4==0 for x in n),'integral polarized norm coefficients')
        values.append(tuple(x//4 for x in n))
    v1,vm,vi=values
    require(v1[1:]==vm[1:]==Z[1:],'real root evaluations')
    require((v1[0]-vm[0])%2==0 and (v1[0]+vm[0])%2==0,'polarization parity')
    A=(v1[0]-vm[0])//2;C0=(v1[0]+vm[0])//2
    require(vi[0]==C0 and vi[2:]==Z[2:],'affine unit-circle restriction')
    return (A,vi[1],C0-target)

def masks(n,centres,owners,coincident=False):
    out=[]
    for j in range(n):
        if coincident:out.append(7)
        elif j in centres:out.append(1<<(2,3,0)[centres.index(j)])
        elif owners[j]=={1}:out.append(3)
        elif owners[j]=={2}:out.append(12)
        else:out.append(15)
    return out

def positive(row,lists,edges):
    require(len(row)==len(lists) and all(type(c) is int and c in range(4) for c in row),'colour dimensions')
    require(all(lists[i]&(1<<c) for i,c in enumerate(row)),'list-colour restriction')
    require(all(row[i]!=row[j] for i,j in edges),'positive unit-edge inequalities')

def audit(data):
    require(data['denominator']==24,'fixed denominator')
    forms=sorted({tuple(x+y for x,y in zip(d,u)) for d in CENTRES for u in DIRECTIONS})
    require(len(forms)==30 and data['forms']==list(map(list,forms)),'complete formal patch')
    equations=set();unit={};collision={};polarity_checks=0
    for i,j in combinations(range(30),2):
        for target,out in [(1,unit),(0,collision)]:
            eq=polarized(forms[i],forms[j],target);out[i,j]=eq;polarity_checks+=1
            if eq[:2]!=(0,0):equations.add(canonical(eq))
    equations=sorted(equations)
    require(len(equations)==46 and data['equations']==list(map(list,equations)),'complete event equation set')
    parameters=[decode(row['parameter']) for row in data['cases']]
    require(len(parameters)==len(set(parameters))==14,'fourteen distinct parameters')
    require(all(norm(b)==scale(ONE,576) for b in parameters),'unit parameters')
    named={(scale(cart2(a,b)[0],12),scale(cart2(a,b)[1],12)) for a,b in ROOTS}
    for sign in (-1,1):
        rho=(scale(ONE,20),tuple(4*sign if j==4 else 0 for j in range(8)))
        for a,b in [(1,-1),(1,0),(0,1)]:
            z=cmul(rho,cart2(a,b))
            require(all(x%2==0 for axis in z for x in axis),'named exceptional direction')
            named.add(tuple(tuple(x//2 for x in axis) for axis in z))
        named.add((scale(ONE,21),tuple(3*sign if j==3 else 0 for j in range(8))))
    require(named==set(parameters),'closed-form exceptional set')
    histogram=Counter();used=set();line_tests=0;incidences=0
    for A,B,C in equations:
        L=A*A+3*B*B;delta=L-C*C
        expected=0 if delta<0 else 1 if delta==0 else 2
        hits=[]
        for j,beta in enumerate(parameters):
            value=plus(plus(scale(beta[0],A),scale(mul(SQRT3,beta[1]),B)),scale(ONE,24*C))
            line_tests+=1
            if value==Z:hits.append(j)
        require(len(hits)==expected,'complete circle-line intersections')
        used.update(hits);histogram[expected]+=1;incidences+=len(hits)
    require(used==set(range(14)),'no spurious exceptional parameter')
    require({str(k):v for k,v in sorted(histogram.items())}==data['root_count_histogram'],'root-count histogram')
    centres=[forms.index(c) for c in CENTRES]
    generic_edges=[(i,j) for (i,j),e in unit.items() if e==(0,0,0)]
    generic_owners=[{h for h,c in enumerate(centres) if j!=c and unit[tuple(sorted((j,c)))]==(0,0,0)} for j in range(30)]
    generic_lists=masks(30,centres,generic_owners)
    require(data['generic']['edges']==len(generic_edges)==72,'generic edge count')
    require(data['generic']['lists']==generic_lists,'generic lists')
    positive(data['generic']['colouring'],generic_lists,generic_edges)
    pair_tests=0;edge_checks=len(generic_edges);case_hist=Counter();coincident_count=0
    for beta,row in zip(parameters,data['cases']):
        evaluated=[evaluate(f,beta,24) for f in forms]
        V=[];idx={};aliases=[]
        for z in evaluated:
            if z not in idx:idx[z]=len(V);V.append(z)
            aliases.append(idx[z])
        require(aliases==row['aliases'],'exact vertex identifications')
        ci=[aliases[j] for j in centres]
        coincident=ci[1]==ci[2]
        require(row['coincident']==coincident,'coincident-centre classification')
        if coincident:
            require(beta==(scale(ONE,24),Z),'only beta=1 has coincident outer centres')
            coincident_count+=1
        E=[(i,j) for i,j in combinations(range(len(V)),2) if distance(V[i],V[j])==scale(ONE,2304)]
        pair_tests+=len(V)*(len(V)-1)//2
        own=[{h for h,d in enumerate(ci) if distance(v,V[d])==scale(ONE,2304)} for v in V]
        lists=masks(len(V),ci,own,coincident)
        require(lists==row['lists'] and len(E)==row['edges'],'complete exceptional graph and lists')
        positive(row['colouring'],lists,E)
        case_hist[len(V),len(E)]+=1;edge_checks+=len(E)
    require(coincident_count==1,'one separate coincident case')
    # A classical lower-bound witness makes the four-colour bound sharp.
    sharp=data['sharpness'];V=[decode(z) for z in sharp['vertices']]
    require(len(V)==len(set(V))==7,'seven sharpness points')
    E={(i,j) for i,j in combinations(range(7),2) if distance(V[i],V[j])==scale(ONE,576)}
    need={(0,2),(0,3),(1,2),(1,3),(2,3),(0,5),(0,6),(4,5),(4,6),(5,6),(1,4)}
    require(E==need,'exact spindle graph')
    path=sharp['dominating_path']
    require(path==[0,2,1] and all(tuple(sorted(e)) in E for e in zip(path,path[1:])),'connected three-vertex path')
    require(all(v in path or any(tuple(sorted((v,d))) in E for d in path) for v in range(7)),'path dominates all seven vertices')
    require(distance(V[path[0]],V[path[-1]])==scale(ONE,3*576),'opening angle120 degrees')
    positive(sharp['colouring'],[15]*7,E)
    valid3=sum(all(c[i]!=c[j] for i,j in E) for c in product(range(3),repeat=7))
    require(valid3==0,'sharpness three-colour obstruction')
    return {'status':'PASS','formal_patch_vertices':30,'formal_pair_target_checks':polarity_checks,
            'event_equations':46,'closed_form_exceptional_set_checked':True,'event_root_count_histogram':{str(k):v for k,v in sorted(histogram.items())},
            'circle_line_parameter_tests':line_tests,'circle_line_root_incidences':incidences,
            'exceptional_parameters':14,'coincident_parameter_cases':1,'generic_cases':1,
            'generic_vertices':30,'generic_edges':72,'exceptional_pair_norms':pair_tests,
            'exceptional_size_histogram':{str(k[0])+','+str(k[1]):v for k,v in sorted(case_hist.items())},
            'patch_positive_edge_checks':edge_checks,'all_angles_four_colourable':True,
            'all_distinct_centre_precolourings_extend':True,
            'sharpness_vertices':7,'sharpness_pair_norms':21,'sharpness_edges':11,
            'sharpness_three_colour_assignments':2187,'sharpness_three_colourings':0,
            'connected_dominating_path_vertices':3,'native_solver_calls':0}

def main():
    p=argparse.ArgumentParser();p.add_argument('--work',required=True);p.add_argument('--discover',action='store_true')
    a=p.parse_args();work=Path(a.work);start=time.monotonic()
    raw=(work/'certificate.json').read_bytes()
    require(raw==(HERE/'certificate.json').read_bytes(),'published bytes')
    data=json.loads(raw);report=audit(data)
    mutants=[]
    b=copy.deepcopy(data);b['equations'].pop();mutants.append(b)
    b=copy.deepcopy(data);b['cases'].pop();mutants.append(b)
    b=copy.deepcopy(data);b['cases'][0]['parameter'][0]+=1;mutants.append(b)
    b=copy.deepcopy(data);b['generic']['lists'][0]=0;mutants.append(b)
    b=copy.deepcopy(data);b['cases'][0]['colouring']=[0]*len(b['cases'][0]['colouring']);mutants.append(b)
    b=copy.deepcopy(data);b['sharpness']['dominating_path']=[0,1,4];mutants.append(b)
    rejected=0
    for bad in mutants:
        try:audit(bad)
        except ValueError:rejected+=1
        else:raise ValueError('malformed certificate accepted')
    report.update(malformed_certificate_rejections=rejected,certificate_bytes=len(raw),certificate_sha256=hashlib.sha256(raw).hexdigest())
    if not a.discover:require(report==json.loads((HERE/'expected.json').read_text()),'expected result')
    (work/'verification.json').write_text(json.dumps(report,indent=2)+'\n')
    (work/'timing.json').write_text(json.dumps({'seconds':time.monotonic()-start},indent=2)+'\n')
    print(json.dumps(report,sort_keys=True))
if __name__=='__main__':main()
