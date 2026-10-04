"""Fresh exact reduction for individual real four-type bad-vertex flows."""
from fractions import Fraction as Q
from itertools import combinations
from math import comb
import hashlib,json

def need(ok,message):
    if not ok:raise ValueError(message)
def canon(x):return json.dumps(x,sort_keys=True,separators=(',',':')).encode()
def sha(x):return hashlib.sha256(canon(x)).hexdigest()
def number(x):
    need(type(x) is str,'canonical rational strings');v=Q(x);need(str(v)==x,'canonical rational spelling');return v

def parameters(m,d,c,tau):
    need(type(m) is int and m>=3,'integer m>=3')
    need(len(d)==4 and len(c)==5 and all(type(v) is Q for v in d+c+[tau]),'exact rational parameter shape')
    need(tau>=0 and all(v>0 for v in d),'nonnegative floor and positive bad demands')
    # d=(YY,B,C,BC); c=(YY/YY,YY/B,YY/C,YY/BC,B/C).
    n=Q(comb(m-1,2));p=Q(m-2);a2=Q(comb(m-2,2));den=Q(m-1)
    beta=(d[3]+tau)/n;A=d[0]+tau-p*beta;B=d[1]+tau;C=d[2]+tau
    W=2*(B+C)/den-A;U=[x-tau for x in c]
    lower=[Q(0),(B-n*U[1])/den,(C-n*U[2])/den,W/4]
    upper=[U[4],B/den,C/den,(a2*U[0]+W)/4]
    return dict(m=m,n=n,p=p,a2=a2,den=den,beta=beta,A=A,B=B,C=C,W=W,U=U,lower=lower,upper=upper,lo=max(lower),hi=min(upper))

def witness(m,d,c,tau,eta=None):
    v=parameters(m,d,c,tau);need(0<=v['beta']<=v['U'][3] and v['lo']<=v['hi'],'closed iff region is nonempty')
    eta=(v['lo']+v['hi'])/2 if eta is None else eta
    need(v['lo']<=eta<=v['hi'],'chosen eta in entire closed interval')
    zb=(v['B']-v['den']*eta)/v['n'];zc=(v['C']-v['den']*eta)/v['n']
    if v['a2']:
        alpha=(4*eta-v['W'])/v['a2'];need(0<=alpha<=v['U'][0],'YY/YY cap and sign')
    else:
        need(4*eta==v['W'],'m3 zero-edge equality');alpha=Q(0)
    values=[alpha,zb,zc,v['beta'],eta]
    for j in (1,2,3,4):need(0<=values[j]<=v['U'][j],'all actual orbit signs/caps')
    need(v['a2']*alpha+v['p']*(v['beta']+zb+zc)==d[0]+tau,'full YY demand')
    need(v['n']*zb+v['den']*eta==d[1]+tau and v['n']*zc+v['den']*eta==d[2]+tau,'both unequal light demands')
    need(v['n']*v['beta']==d[3]+tau,'full BC demand')
    return values,v

def equal_interval(m,d,c,tau):
    need(m>=4 and len(c)==4,'source equal-pattern domain')
    n=Q(comb(m-1,2));p=Q(m-2);a2=Q(comb(m-2,2));beta=(d[2]+tau)/n;A=d[0]+tau-p*beta;B=d[1]+tau
    low=[Q(0),(A-a2*(c[0]-tau))/(2*p),(B-(m-1)*(c[3]-tau))/n]
    high=[c[1]-tau,A/(2*p),B/n]
    v=parameters(m,[d[0],d[1],d[1],d[2]],[c[0],c[1],c[1],c[2],c[3]],tau)
    need(v['beta']==beta and v['A']==A,'both source eliminations')
    need(v['lo']==(B-n*min(high))/(m-1) and v['hi']==(B-n*max(low))/(m-1),'entire interval affine equivalence')
    return dict(beta=beta,lo=max(low),hi=min(high),eta_lo=v['lo'],eta_hi=v['hi'],all_source_lower=low,all_source_upper=high)

def graph(m):
    need(type(m) is int and m>=3,'literal graph count')
    Y=list(range(m));vertices=[('YY',a) for a in combinations(Y,2)]+[(t,(y,)) for t in ('B','C','BC') for y in Y]
    def original(t,ys):return frozenset(ys)|({'b'} if t=='B' else {'c'} if t=='C' else {'b','c'} if t=='BC' else set())
    sets=[original(t,ys) for t,ys in vertices];edges=[]
    for i,j in combinations(range(len(vertices)),2):
        if sets[i]&sets[j]:continue
        ti,tj=vertices[i][0],vertices[j][0];pair={ti,tj}
        if ti==tj=='YY':role=0
        elif pair=={'YY','B'}:role=1
        elif pair=={'YY','C'}:role=2
        elif pair=={'YY','BC'}:role=3
        elif pair=={'B','C'}:role=4
        else:raise ValueError('unlisted actual disjoint edge')
        edges.append((i,j,role))
    return vertices,edges

def check_literal(m,d,c,tau,eta=None):
    vals,v=witness(m,d,c,tau,eta);vs,es=graph(m);degrees=[Q(0)]*len(vs);counts=[0]*5;raw=[]
    for i,j,r in es:
        x=vals[r];need(0<=x<=c[r]-tau,'every literal edge capacity');degrees[i]+=x;degrees[j]+=x;counts[r]+=1;raw.append([i,j,r,str(x)])
    for (kind,ys),value in zip(vs,degrees):
        index={'YY':0,'B':1,'C':2,'BC':3}[kind];need(value==d[index]+tau,'every actual individual bad degree')
    expected=[3*comb(m,4),comb(m,2)*(m-2),comb(m,2)*(m-2),comb(m,2)*(m-2),m*(m-1)]
    need(counts==expected,'all five literal unordered orbit counts')
    return dict(m=m,demands=[str(x) for x in d],capacities=[str(x) for x in c],tau=str(tau),orbit_values=[str(x) for x in vals],eta_bounds=[str(v['lo']),str(v['hi'])],vertices=len(vs),edges=len(es),orbit_counts=counts,all_individual_degrees=[str(x) for x in degrees],entire_edge_record_sha256=sha(raw))

def from_orbits(m,values,capacities,tau):
    a,zB,zC,b,e=values;p=Q(m-2);n=Q(comb(m-1,2));aa=Q(comb(m-2,2));den=Q(m-1)
    d=[aa*a+p*(b+zB+zC)-tau,n*zB+den*e-tau,n*zC+den*e-tau,n*b-tau]
    need(all(x>0 for x in d),'generated genuine positive demands');return check_literal(m,d,capacities,tau,e)
