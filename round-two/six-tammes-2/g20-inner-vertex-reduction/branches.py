"""Explicit three-variable polynomial circuits; no search or solver verdict.

The operations are only integral addition, multiplication and nonnegative
powers. The guarded determinant is the actual Gram determinant, never a
discarded geometric stratum. A zero determinant disqualifies this selected
vertex BASIS; a real polytope vertex always has another independent basis.
"""
import json,hashlib
from frame import make,CORE,CONTACTS
from polynomials import dot

def branch(t,z,w,target):
    if len(target)!=3 or tuple(sorted(set(target)))!=tuple(target) or any(i not in (*CORE,98,99) for i in target):raise ValueError('one regular labelled triple')
    m=make(t,z,w);O=m['Omega'];V=dict(m['points']);V[98]=[O*x for x in (-8,12,-5)];V[99]=[O*x for x in (-5,-14,20)]
    rhs={i:O*(9 if i==98 else 15 if i==99 else t) for i in V}
    i,j,k=target;aa=dot(V[i],V[i],t);bb=dot(V[i],V[j],t);cc=dot(V[i],V[k],t);dd=dot(V[j],V[j],t);ee=dot(V[j],V[k],t);ff=dot(V[k],V[k],t)
    adj=((dd*ff-ee*ee,cc*ee-bb*ff,bb*ee-cc*dd),(cc*ee-bb*ff,aa*ff-cc*cc,bb*cc-aa*ee),(bb*ee-cc*dd,bb*cc-aa*ee,aa*dd-bb*bb))
    det=aa*adj[0][0]+bb*adj[0][1]+cc*adj[0][2];rr=[rhs[x] for x in target]
    lam=[sum((row[j]*rr[j] for j in range(3)),t*0) for row in adj]
    numerator=[sum((lam[j]*V[target[j]][v] for j in range(3)),t*0) for v in range(3)]
    q=sum((rr[j]*lam[j] for j in range(3)),t*0)
    eq=[('w-square',w*w-m['root_squared'])]+[('unit-'+str(i),dot(V[i],V[i],t)-O*O) for i in CORE]+[('contact-'+str(i)+'-'+str(j),dot(V[i],V[j],t)-t*O*O) for i,j in CONTACTS]
    strict=[('positive-root',w),('imported-regularity',2*m['G']-m['a']**4*m['C']**2),('selected-Gram-determinant',det)]
    domain=[('t-lower',25*t-14),('t-upper',593-1000*t),('z-lower',5*z-6),('z-upper',7-5*z),('core-chart',1-(1-t)**2*z*z)]
    packing=[('core-'+str(i)+'-'+str(j),t*O*O-dot(V[i],V[j],t)) for p,i in enumerate(CORE) for j in CORE[p+1:]]
    packing += [('vertex-'+str(j),rhs[j]*det-dot(V[j],numerator,t)) for j in (*CORE,98,99)]
    packing.append(('long-vertex',q-det))
    return {'equalities':eq,'strict_positive':strict,'closed_domain':domain,'nonnegative':packing}

class Circuit:
    def __init__(self):self.nodes=[];self.lookup={}
    def node(self,op,args):
        key=(op,tuple(args))
        if key not in self.lookup:self.lookup[key]=len(self.nodes);self.nodes.append([op,*args])
        return Expr(self,self.lookup[key])
    def constant(self,n):
        if type(n)is not int:raise TypeError('integer circuit coefficient')
        return self.node('integer',[n])
    def variable(self,n):
        if n not in ('t','z','w'):raise ValueError('three named variables only')
        return self.node('variable',[n])

class Expr:
    def __init__(self,c,index):self.c,self.index=c,index
    def cv(self,x):
        if isinstance(x,Expr):
            if x.c is not self.c:raise ValueError('one circuit ring')
            return x
        return self.c.constant(x)
    def __add__(self,x):return self.c.node('add',[self.index,self.cv(x).index])
    __radd__=__add__
    def __neg__(self):return self.c.node('multiply',[self.c.constant(-1).index,self.index])
    def __sub__(self,x):return self+-self.cv(x)
    def __rsub__(self,x):return self.cv(x)+-self
    def __mul__(self,x):return self.c.node('multiply',[self.index,self.cv(x).index])
    __rmul__=__mul__
    def __pow__(self,n):
        if type(n)is not int or n<0:raise ValueError('nonnegative polynomial power')
        out=self.c.constant(1)
        for _ in range(n):out*=self
        return out

def certificate(triples):
    c=Circuit();t,z,w=[c.variable(x) for x in ('t','z','w')];records=[]
    for triple in triples:
        s=branch(t,z,w,triple)
        if list(map(len,s.values()))!=[33,3,5,81]:raise ValueError('complete branch grammar')
        if s['strict_positive'][-1][0]!='selected-Gram-determinant':raise ValueError('rank guard')
        records.append({'triple':triple,'constraints':{name:[[label,p.index] for label,p in rows] for name,rows in s.items()}})
    # A compact complete digest of the deterministically reproducible circuits.
    stream=(json.dumps({'variable_order':['t','z','w'],'nodes':c.nodes,'branches':records},separators=(',',':'))+'\n').encode()
    return {'coefficient_ring':'Z[t,z,w]','arithmetic_operations':['integer','variable','add','multiply'],'branches':len(records),'constraints_per_branch':[33,3,5,81],'all_rank_guards_strict':True,'dag_node_count':len(c.nodes),'whole_circuit_sha256':hashlib.sha256(stream).hexdigest(),'no_solver_feasibility_verdict':True}
