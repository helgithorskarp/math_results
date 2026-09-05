"""Independent full Python screen, circle certificates, Cartesian projection and colours."""
from pathlib import Path
from fractions import Fraction as Q
from itertools import product,permutations,combinations
from collections import Counter
from math import gcd,lcm,isqrt
from hashlib import sha256
import importlib.util,json,argparse,sys
HERE=Path(__file__).resolve().parent
PRIMES=(131,181,229,239,359,421)
ROOTS=((38,23,50),(33,27,83),(71,66,34),(106,31,49),(163,148,27),(74,200,46))

def require(ok,msg):
    if not ok:raise ValueError(msg)

def source():
    p=HERE.parent/'hadwiger_nelson_mixed506_single_hub_reduction/check_examples.py'
    require(sha256(p.read_bytes()).hexdigest()=='8405039707b294ace3af5fd9deffc0a738c17133d442056a4013b9b4b588a50f','independent source pin failed')
    s=importlib.util.spec_from_file_location('generic_source',p);R=importlib.util.module_from_spec(s);s.loader.exec_module(R)
    def extract(z):
        x,y=z
        require(all(x[i]==0 for i in range(8) if i not in (0,6)) and all(y[i]==0 for i in range(8) if i not in (2,4)),'wrong radical support')
        return x[0],x[6],y[2],y[4]
    A,V=R.read(159),R.read(214)
    B=list(dict.fromkeys([R.cscale(x,6) for x in A]+[R.cmul(R.e(5,0,0,1),x) for x in A]))
    return [extract(x) for x in B],[tuple(6*a for a in extract(x)) for x in V]

def sub4(x,y):return tuple(a-b for a,b in zip(x,y))
def add4(x,y):return tuple(a+b for a,b in zip(x,y))
def source_edges(G):
    out=[]
    for i,j in combinations(range(len(G)),2):
        a,b,c,d=sub4(G[i],G[j])
        if a*a+33*b*b+3*c*c+11*d*d==5184 and a*b+c*d==0:out.append((i,j))
    return out

def fimage(x,p,r):
    a,b,c,d=x
    return (a+b*r)*pow(72,-1,p)%p,(c+d*r*pow(3,-1,p))*pow(72,-1,p)%p

def modular_distance(x,y,p,r,t):
    a,b=fimage(x,p,r);c,d=fimage(y,p,r);i8=pow(8,-1,p)
    aa=(a-(7*c-3*t*d)*i8)%p;bb=(b-(7*d+t*c)*i8)%p
    return (aa*aa+3*bb*bb)%p

def screen(X,Y):
    tables=[]
    for p,roots in zip(PRIMES,ROOTS):
        require(all(p%d for d in range(2,isqrt(p)+1)) and all(r*r%p==d for r,d in zip(roots,(3,5,11))),'prime data failed')
        r3,r5,r11=roots;qr={a*a%p for a in range(p)}
        accept=[d*(4-d)*pow(3,-1,p)%p in qr for d in range(p)]
        for s1,s2 in product((1,-1),repeat=2):
            r,t=r3*r11*s1%p,r5*s2%p;i8=pow(8,-1,p)
            xx=[fimage(x,p,r) for x in X];yy=[]
            for y in Y:
                a,b=fimage(y,p,r);yy.append(((7*a-3*t*b)*i8%p,(7*b+t*a)*i8%p))
            tables.append((p,xx,yy,accept))
    stages=[0]*24;out=[]
    for i in range(len(X)):
        for j in range(len(Y)):
            for k,(p,xx,yy,ok) in enumerate(tables):
                a,b=xx[i];c,d=yy[j];norm=((a-c)**2+3*(b-d)**2)%p
                if not ok[norm]:break
                stages[k]+=1
            else:out.append((i,j))
        if i and i%4000==0:print('independent modular rows',i,file=sys.stderr,flush=True)
    return stages,out

# Generic real radical ring with basis sqrt3^e sqrt5^f sqrt11^g.
Z=(0,)*8;ONE=(1,)+(0,)*7
FACT=(1,3,5,15,11,33,55,165)
def add(x,y):return tuple(a+b for a,b in zip(x,y))
def scale(x,k):return tuple(k*a for a in x)
def mul(x,y):
    z=[0]*8
    for i,a in enumerate(x):
        if a:
            for j,b in enumerate(y):
                if b:z[i^j]+=a*b*FACT[i&j]
    return tuple(z)
def ca(x,y):return add(x[0],y[0]),add(x[1],y[1])
def cs(x,k):return scale(x[0],k),scale(x[1],k)
def cm(x,y):return add(mul(x[0],y[0]),scale(mul(x[1],y[1]),-1)),add(mul(x[0],y[1]),mul(x[1],y[0]))
def cn(x):return add(mul(x[0],x[0]),mul(x[1],x[1]))
def cart(x):
    a,b,c,d=x;re=[0]*8;im=[0]*8
    re[0]=a;re[5]=b;im[1]=c;im[4]=d
    return tuple(re),tuple(im)
UNUM=((7,0,0,0,0,0,0,0),(0,0,0,1,0,0,0,0))
def wnum(x,y):return ca(cs(cart(x),8),cs(cm(UNUM,cart(y)),-1))
def hcart(raw):
    v=[Q(x) for row in raw for x in row];require(len(v)==8,'invalid proposed centre')
    den=lcm(*(x.denominator for x in v));a,b,c,d,e,f,g,h=[int(x*den) for x in v]
    return den,((a,0,c,0,0,b,0,d),(0,e,0,g,3*f,0,3*h,0))
def canonical(den,nums):
    g=gcd(den,*nums);return (den//g,)+tuple(a//g for a in nums)
def pack(z):
    x,y=z
    require(all(x[i]==0 for i in (1,3,4,6)) and all(y[i]==0 for i in (0,2,5,7)),'wrong K Cartesian support')
    return x[0],x[2],x[5],x[7],y[1],y[3],y[4],y[6]
def to_k(key):
    D,a,c,b,d,e,g,f,h=key
    return canonical(3*D,(3*a,3*b,3*c,3*d,3*e,f,3*g,h))

def proposals(work,X,Y,survivors):
    raw=json.loads((work/'positive.json').read_text());negative=[tuple(x) for x in json.loads((work/'negative.json').read_text())]
    positives=[];seen=set();centres=0;tangencies=0
    for i,j,hs in raw:
        require((i,j) in survivors and (i,j) not in seen,'duplicate or unscreened positive pair');seen.add((i,j))
        w=wnum(X[i],Y[j]);d=cn(w);require(d!=Z,'zero offset pair')
        tangent=d==scale(ONE,4*576**2)
        require(len(hs)==(1 if tangent else 2),'missing circle intersection')
        checked=[];keys=[]
        for h in hs:
            D,z=hcart(h);require(cn(z)==scale(ONE,D*D),'first unit circle failed')
            L=lcm(D,576);delta=ca(cs(z,L//D),cs(w,-L//576))
            require(cn(delta)==scale(ONE,L*L),'second unit circle failed')
            keys.append(canonical(D,pack(z)));checked.append((D,pack(z)))
        require(len(set(keys))==len(hs),'duplicate circle intersection')
        positives.append((i,j,checked));centres+=len(hs);tangencies+=int(tangent)
    negset=set(negative);require(len(negset)==len(negative) and not (negset&seen),'invalid negative partition')
    witnesses=[];p=29
    require(all(p%d for d in range(2,isqrt(p)+1)) and 2*2%p==33%p and 11*11%p==5,'negative prime data failed')
    for i,j in negative:
        for r,t in ((2,11),(2,18),(27,11),(27,18)):
            d=modular_distance(X[i],Y[j],p,r,t);f=d*(4-d)*pow(3,-1,p)%p
            if pow(f,14,p)==28:witnesses.append((i,j,r,t,f));break
        else:raise ValueError('unproved square-root rejection')
    zeros={(i,j) for i,j in survivors if X[i]==Y[j]==(0,0,0,0)}
    require(len(zeros)==1 and seen|negset|zeros==set(survivors) and not (zeros&(seen|negset)),'incomplete pair partition')
    return positives,{'positive_pairs':len(positives),'centres':centres,'tangent_pairs':tangencies,'negative_pairs':len(negative),'negative_witnesses_sha256':digest(witnesses)},witnesses

def project(B,V,X,Y,positive):
    lookup=[{x:i for i,x in enumerate(G)} for G in (B,V)]
    def incidents(G,d,look):return [(a,look[add4(x,d)]) for a,x in enumerate(G) if add4(x,d) in look]
    ip={i:incidents(B,X[i],lookup[0]) for i,_,_ in positive}
    iq={j:incidents(V,Y[j],lookup[1]) for _,j,_ in positive}
    left=[cs(cart(p),8) for p in B];right=[cm(UNUM,cart(q)) for q in V]
    offsets=[pack(ca(p,cs(q,-1))) for p in left for q in right]
    known={canonical(576,x) for x in offsets};require(len(known)==62488,'wrong overlap list')
    out={};events=overlaps=0;seen=set()
    for i,j,hs in positive:
        for D,num in hs:
            den=lcm(D,576);n=tuple(x*(den//D) for x in num);fac=den//576
            for a,b in ip[i]:
                for c,d in iq[j]:
                    e0,e1=214*a+c,214*b+d
                    if e0>=e1:continue
                    key=canonical(den,[x+fac*y for x,y in zip(n,offsets[e0])]);events+=1
                    if key in known:overlaps+=1;seen.add(key);continue
                    if key not in out:out[key]={e0,e1}
                    else:out[key].update((e0,e1))
    rows=[]
    while out:
        key,ee=out.popitem();rows.append((to_k(key),sorted(ee)))
    rows.sort()
    require(all(rows[i][0]!=rows[i-1][0] for i in range(1,len(rows))),'noninjective basis conversion')
    return rows,{'pair_intersection_events':events,'overlap_events':overlaps,'overlap_translations':len(seen)}

def libraries(B,V,EB,EV):
    libs=[]
    for side,G,ee in zip(('B','V'),(B,V),(EB,EV)):
        first='hadwiger_nelson_nonmono159_moser_triple/colors_B.txt' if side=='B' else 'hadwiger_nelson_mixed505_anchor0/colors_H.txt'
        paths=[HERE.parent/first,HERE.parent/f'hadwiger_nelson_mixed505_high_degree_attachments/new_{side}.txt',HERE.parent/f'hadwiger_nelson_mixed505_spindle_rotation/new_{side}.txt',HERE/f'new_{side}.txt'];rows=[]
        for path in paths:
            for line in path.read_text().splitlines():
                c=tuple(map(int,line));require(len(c)==len(G) and set(c)<=set(range(4)) and all(c[i]!=c[j] for i,j in ee),'bad component colouring');rows.append(c)
        libs.append(rows)
    return libs

def witness(ee,libs):
    perms=list(permutations(range(4)))
    for ib,cb in enumerate(libs[0]):
        for iv,cv in enumerate(libs[1]):
            bad={(cb[e//214],cv[e%214]) for e in ee}
            for ip,pi in enumerate(perms):
                if all(pi[b]!=a for a,b in bad):return ib,iv,ip
    return None

def digest(obj):return sha256((json.dumps(obj,separators=(',',':'))+'\n').encode()).hexdigest()
def run(work,expected):
    B,V=source();EB,EV=source_edges(B),source_edges(V)
    require([len(B),len(V),len(EB),len(EV)]==[292,214,1251,977],'source graph differs')
    X,Y=[sorted({sub4(x,y) for x in G for y in G}) for G in (B,V)]
    stages,survivors=screen(X,Y)
    require(stages==expected['modular_stages'] and digest(survivors)==expected['modular_survivor_sha256'],'complete modular screen differs')
    screen_record=json.loads((work/'screen.json').read_text())
    require(stages==screen_record['stages'] and [list(x) for x in survivors]==screen_record['survivors'],'native stream differs entry by entry')
    positive,certs,witnesses=proposals(work,X,Y,survivors)
    (work/'negative_witnesses.json').write_text(json.dumps(witnesses)+'\n')
    print('all circle and nonsquare certificates passed',file=sys.stderr,flush=True)
    rows,projection=project(B,V,X,Y,positive)
    require(all(projection[k]==expected[k] for k in projection),'projection counts differ')
    libs=libraries(B,V,EB,EV);hist=Counter();coverage_hash=sha256();geometry_hash=sha256()
    with (work/'translations.jsonl').open() as f:
        for key,ee in rows:
            w=witness(ee,libs);require(w is not None,'uncovered independent placement')
            line=json.dumps([key,ee,w],separators=(',',':'))+'\n'
            require(f.readline()==line,'complete placement/colour stream differs entry by entry')
            coverage_hash.update(line.encode());geometry_hash.update((json.dumps([key,ee],separators=(',',':'))+'\n').encode());hist[len(ee)]+=1
        require(f.read()=='','producer contains additional rows')
    require(coverage_hash.hexdigest()==expected['coverage_stream_sha256'] and geometry_hash.hexdigest()==expected['geometry_stream_sha256'],'full stream hashes differ')
    require(len(rows)==expected['disjoint_translations'] and [list(x) for x in sorted(hist.items())]==expected['cross_edge_histogram'],'census histogram differs')
    return {'all_difference_pairs':len(X)*len(Y),'full_modular_stream_matches':True,**certs,
            'independent_cartesian_projection_matches':True,'every_translation_and_colouring_compared':len(rows),
            'source_colour_rows':list(map(len,libs)),'solver_or_square_root_completeness_trusted':False}
if __name__=='__main__':
    p=argparse.ArgumentParser(description=__doc__);p.add_argument('--work',type=Path,required=True);p.add_argument('--expected',type=Path,default=HERE/'expected.json');args=p.parse_args()
    print(json.dumps(run(args.work,json.loads(args.expected.read_text())),indent=2))
