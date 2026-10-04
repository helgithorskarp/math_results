"""separate complete QQ[h,q] certificate reconstruction.

Imports no producer/recipe/sector/polynomial engine. Integer binomial
composition proves each sign. Degree-complete Cartesian grids prove the
closed-form and every local Gaussian polynomial identity. Exact matching
factor cancellation reduces the latter grids without expanding products.
"""
import os
for v in ('OPENBLAS_NUM_THREADS','OMP_NUM_THREADS','MKL_NUM_THREADS','BLIS_NUM_THREADS','NUMEXPR_NUM_THREADS','VECLIB_MAXIMUM_THREADS'):
    os.environ[v]='1'
from pathlib import Path
import sys,json,signal,time,resource,argparse
sys.path.insert(0,str(Path(__file__).resolve().parent))
from fractions import Fraction as F
from math import comb,gcd,prod
from collections import Counter
from hashlib import sha256
from independent_harmonic import forms,Degree,require,add_degree,max_degree
from pack_certificate import unpack

SIZES={'x-alpha':1,'x-beta':1,'x-mu':1,'x-nu':1,'y-alpha':1,'y-beta':1,'y-mu':1,'y-nu':1,'tau':1,'anti-x':2,'anti-y':2,'standard-x':4,'standard-y':4,'aggregate':10,'untouched-even':1,'untouched-odd':1}

class Polynomial:
    def __init__(self,record):
        require(set(record)=={'denominator','terms'},'entire polynomial encoding')
        den=record['denominator'];require(type(den) is int and den>0,'positive integer coefficient denominator')
        require(type(record['terms']) is list and len(record['terms'])<=512,'unchanged512 polynomial-term guard')
        terms={}
        for ex,coefficient in record['terms']:
            require(type(ex) is list and len(ex)==2 and all(type(e) is int and 0<=e<=512 for e in ex),'bounded bivariate exponent')
            value=int(coefficient);key=tuple(ex)
            require(str(value)==coefficient and value!=0 and key not in terms,'unique canonical nonzero integer coefficient')
            terms[key]=value
        require(record['terms']==[[list(k),str(v)] for k,v in sorted(terms.items())],'sorted whole polynomial')
        self.terms=terms;self.den=den;self.key=(tuple(sorted(terms.items())),den)
        self.degree=tuple(max((k[i] for k in terms),default=0) for i in range(2))
    def value(self,h,q):
        hp=[1];qp=[1]
        for _ in range(self.degree[0]):hp.append(hp[-1]*h)
        for _ in range(self.degree[1]):qp.append(qp[-1]*q)
        numerator=sum(v*hp[a]*qp[b] for (a,b),v in self.terms.items())
        return F(numerator,self.den)
    def shifted(self):
        out={}
        for (a,b),value in self.terms.items():
            for i in range(a+1):
                for j in range(b+1):
                    key=(i,j);out[key]=out.get(key,0)+value*comb(a,i)*3**(a-i)*comb(b,j)*4**(b-j)
        out={k:v for k,v in out.items() if v}
        require(len(out)<=512,'unchanged shifted512-term guard')
        return Polynomial({'denominator':self.den,'terms':[[list(k),str(v)] for k,v in sorted(out.items())]})
    def positive(self):
        return self.terms.get((0,0),0)>0 and all(v>=0 for v in self.terms.values())
    def primitive(self):
        if not self.terms:return None,F(0)
        content=0
        for value in self.terms.values():content=gcd(content,abs(value))
        if self.terms[max(self.terms)]<0:content=-content
        primitive=Polynomial({'denominator':1,'terms':[[list(k),str(v//content)] for k,v in sorted(self.terms.items())]})
        return primitive,F(content,self.den)

class Decoder:
    def __init__(self):self.polynomials={};self.positive=set();self.factor_occurrences=0
    def polynomial(self,record,positive=False):
        key=json.dumps(record,sort_keys=True,separators=(',',':'))
        if key not in self.polynomials:self.polynomials[key]=Polynomial(record)
        p=self.polynomials[key]
        if positive and p.key not in self.positive:
            require(p.shifted().positive(),'EVERY full denominator factor positive on h>=3,q>=4')
            self.positive.add(p.key)
        return p
    def field(self,record):
        require(set(record)=={'numerator','denominator_factors'},'entire rational field encoding')
        numerator=self.polynomial(record['numerator']);denominator={}
        for term in record['denominator_factors']:
            require(set(term)=={'factor','power'},'entire factor record')
            p=self.polynomial(term['factor'],True);power=term['power']
            require(type(power) is int and 0<power<=512 and p.key not in denominator,'unique positive factor exponent')
            denominator[p.key]=(p,power);self.factor_occurrences+=1
        return Field(numerator,denominator)

class Field:
    def __init__(self,numerator,denominator):
        self.n=numerator;self.d=denominator
        self.key=(numerator.key,tuple(sorted((key,power) for key,(p,power) in denominator.items())))
        self.degree=sum_degrees((p.degree,power) for p,power in denominator.values())
    def value(self,h,q):
        return self.n.value(h,q)/prod(p.value(h,q)**power for p,power in self.d.values())

def sum_degrees(terms):
    out=[0,0]
    for degree,power in terms:
        for i in (0,1):out[i]+=degree[i]*power
    require(max(out)<=512,'unchanged degree guard512')
    return tuple(out)

def product_term(left,right,sign,polynomials):
    unit=F(sign);numerator=Counter();denominator=Counter()
    for field in (left,right):
        p,scale=field.n.primitive()
        if p is None:return F(0),Counter(),Counter()
        unit*=scale;polynomials[p.key]=p;numerator[p.key]+=1
        for factor,power in field.d.values():
            p,scale=factor.primitive();require(p is not None,'nonzero positive denominator')
            unit/=scale**power;polynomials[p.key]=p;denominator[p.key]+=power
    common=numerator&denominator;numerator-=common;denominator-=common
    return unit,numerator,denominator

def verify_update(pivot,before,after,left,right):
    # Three exact rational terms: pivot*before-pivot*after-left*right.
    polynomials={}
    terms=[product_term(x,y,sign,polynomials) for x,y,sign in ((pivot,before,1),(pivot,after,-1),(left,right,-1))]
    terms=[term for term in terms if term[0]]
    if not terms:return dict(h_degree=0,q_degree=0,nodes=1,exact_matching_factors_removed=0)
    common_denominator=Counter()
    for unit,num,den in terms:common_denominator|=den
    numerators=[num+(common_denominator-den) for unit,num,den in terms]
    common_numerator=numerators[0].copy()
    for num in numerators[1:]:common_numerator&=num
    numerators=[num-common_numerator for num in numerators]
    bound=(0,0)
    for num in numerators:bound=max_degree(bound,sum_degrees((polynomials[k].degree,e) for k,e in num.items()))
    nodes=0
    for h in range(3,4+bound[0]):
        for q in range(4,5+bound[1]):
            values={}
            total=F(0)
            for (unit,_,_),num in zip(terms,numerators):
                value=unit
                for key,power in num.items():
                    if key not in values:values[key]=polynomials[key].value(h,q)
                    value*=values[key]**power
                total+=value
            require(total==0,'EVERY degree-complete exact local Gaussian identity');nodes+=1
    return dict(h_degree=bound[0],q_degree=bound[1],nodes=nodes,exact_matching_factors_removed=sum(common_numerator.values()))

def check(data):
    require(data['domain']=='Auxiliary real h>=3,q>=4; physical h integer,q=2^(n-1),n>=3','exact two-variable domain')
    require(data['guards']==dict(child_seconds=60,polynomial_terms=512,packing_bytes=33554432,native_threads=1),'unchanged producer guards')
    require(set(data['forms'])==set(SIZES),'complete151 original normalized form entries')
    obligations=[(name,k) for name,n in SIZES.items() for k in range(1,n+1)]
    require([(row['group'],row['order']) for row in data['rows']]==obligations,'complete33 pivot obligations')
    decoder=Decoder();matrices={};closed_degrees=forms(Degree(1,(0,1)),Degree(1,(1,0)))
    bound=(0,0);identities=[]
    for name,n in SIZES.items():
        raw=data['forms'][name]
        require(len(raw)==n and all(len(row)==n for row in raw),'every entire square original form')
        matrices[name]=[[decoder.field(z) for z in row] for row in raw]
        for i,row in enumerate(matrices[name]):
            for j,z in enumerate(row):
                d=Degree(closed_degrees[name][i][j])
                b=max_degree(add_degree(z.n.degree,d.d),add_degree(d.n,z.degree))
                require(b is not None and max(b)<=512,'closed original coefficient identity degree guard')
                if d.n is None:require(not z.n.terms,'separate closed zero entry agrees identically')
                bound=max_degree(bound,b);identities.append(dict(group=name,i=i,j=j,h_degree=b[0],q_degree=b[1]))
    original_nodes=0
    for h in range(3,4+bound[0]):
        for q in range(4,5+bound[1]):
            live=forms(F(q),F(h))
            for name,n in SIZES.items():
                for i in range(n):
                    for j in range(n):
                        require(matrices[name][i][j].value(h,q)==live[name][i][j],'EVERY degree-complete closed original formula identity')
            original_nodes+=1
    require(len(identities)==151,'all original entries, no selected prefix')
    print(json.dumps(dict(stage='separate closed original identities complete',entries=151,grid_bound=bound,grid_nodes=original_nodes)),flush=True)
    positive_coefficients=0;pivots={}
    for row in data['rows']:
        pivot=decoder.field(row['pivot']);shifted=decoder.polynomial(row['shifted_numerator'])
        require(pivot.n.shifted().key==shifted.key and shifted.positive(),'whole independent binomial composition and strict positive coefficients')
        require(row['positive'] is True and row['denominator_positive'] is True and row['degree']==max((sum(k) for k in pivot.n.terms),default=-1) and row['terms']==len(pivot.n.terms) and row['shifted_terms']==len(shifted.terms),'entire sign metadata')
        pivots[(row['group'],row['order'])]=pivot;positive_coefficients+=len(shifted.terms)
    updates=data['updates'];cursor=0;checks=[]
    for name,n in SIZES.items():
        working=[row[:] for row in matrices[name]]
        for k in range(n):
            pivot=pivots[(name,k+1)];require(pivot.key==working[k][k].key,'each claimed pivot is the actual entire working matrix diagonal')
            for i in range(k+1,n):
                for j in range(k+1,n):
                    require(cursor<len(updates),'complete Gaussian update list');record=updates[cursor];cursor+=1
                    require((record['group'],record['k'],record['i'],record['j'])==(name,k,i,j),'every Gaussian update in exact full order')
                    before,left,right,claimed_pivot,after=[decoder.field(record[key]) for key in ('before','left','right','pivot','after')]
                    require(before.key==working[i][j].key and left.key==working[i][k].key and right.key==working[k][j].key and claimed_pivot.key==pivot.key,'every local update linked to original complete matrix')
                    result=verify_update(pivot,before,after,left,right)
                    checks.append(dict(group=name,k=k,i=i,j=j,**result));working[i][j]=after
        print(json.dumps(dict(stage='separate full Gaussian group complete',group=name)),flush=True)
    require(cursor==len(updates)==315,'all315 local elimination coefficient identities')
    return dict(complete=True,domain=data['domain'],original_field_coefficient_identities=151,original_identity_grid_bound=bound,original_identity_grid_nodes=original_nodes,original_identity_nodes=151*original_nodes,whole_shift_coefficient_identities=33,strict_positive_coefficients=positive_coefficients,all_positive_denominator_polynomials=len(decoder.positive),all_positive_denominator_factor_occurrences=decoder.factor_occurrences,complete_Gaussian_coefficient_identities=315,Gaussian_degree_complete_grid_nodes=sum(z['nodes'] for z in checks),original_checks=identities,Gaussian_checks=checks,trust='Separate same-author standard-library integer/Fraction computation and conservative polynomial-degree argument. Physical completeness and original Schur bridges require ordinary written proof; no proof assistant or independent reviewer verdict.')

def main():
    ap=argparse.ArgumentParser();ap.add_argument('certificate',nargs='?',default=str(Path(__file__).resolve().parent/'CERTIFICATE.json'));ap.add_argument('--output');args=ap.parse_args()
    def alarm(a,b):raise TimeoutError('unchanged60s separate variable-q reconstruction guard')
    signal.signal(signal.SIGALRM,alarm);signal.alarm(60);start=time.monotonic()
    raw=Path(args.certificate).read_bytes();result=check(unpack(json.loads(raw)));signal.alarm(0)
    out=dict(agent='six-downset-1',role='researcher',status='PASS: separate complete variable-q identities and signs',certificate_sha256=sha256(raw).hexdigest(),result=result,seconds=time.monotonic()-start,peak_KiB=resource.getrusage(resource.RUSAGE_SELF).ru_maxrss,optimized=sys.flags.optimize)
    path=Path(args.output or Path.cwd()/'CHECKED.json');path.write_text(json.dumps(out,indent=2)+'\n')
    print(json.dumps({k:v for k,v in out.items() if k!='result'}|{k:v for k,v in result.items() if k not in ('original_checks','Gaussian_checks')}),flush=True)
if __name__=='__main__':main()
