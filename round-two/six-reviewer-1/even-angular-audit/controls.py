"""Later primitive, physical-projection and fixture controls; no author imports."""
from fractions import Fraction as Q
from pathlib import Path
import copy
import importlib.util
import json
import signal
import subprocess
import sys

spec = importlib.util.spec_from_file_location('own_check', Path(__file__).with_name('check.py'))
c = importlib.util.module_from_spec(spec)
spec.loader.exec_module(c)
P, vars, zero = c.P, c.vars, c.zero


def require(test, name):
    if not test:
        raise ValueError(name)


def typed(expected, actual, where='root'):
    require(type(expected) is type(actual), 'fixture type '+where)
    if isinstance(expected, dict):
        require(set(expected)==set(actual), 'fixture fields '+where)
        for k in expected:typed(expected[k],actual[k],where+'.'+k)
    elif isinstance(expected,list):
        require(len(expected)==len(actual), 'fixture length '+where)
        for j,(x,y) in enumerate(zip(expected,actual)):typed(x,y,where+'.'+str(j))
    else:require(expected==actual, 'fixture value '+where)


def mm(a,b):
    return [[sum((a[i][k]*b[k][j] for k in range(len(b))),Q(0))
             for j in range(len(b[0]))] for i in range(len(a))]


def ma(a,b):
    return [[x+y for x,y in zip(ra,rb)] for ra,rb in zip(a,b)]


def scale(t,a):
    return [[t*x for x in row] for row in a]


def physical(rad, damage=False):
    """Literal ambient 8x8 full-eigenspace projectors of H², not residues."""
    u=[Q(x) for x in rad]
    n=len(u);require(n==8 and sum(u)==0,'balanced physical input')
    eye=[[Q(i==j) for j in range(n)] for i in range(n)]
    p=[[Q(i==j)-Q(1,n) for j in range(n)] for i in range(n)]
    h=mm([[p[i][j]*u[j] for j in range(n)] for i in range(n)],p)
    h2=mm(h,h)
    nonzero=sorted(set(x*x for x in u if x))
    if len(nonzero)==2 and rad.count(1)==3:
        rr=nonzero[-1];nodes=[Q(0),Q(1),(3*rr+1)/4]
    elif len(nonzero)==1 and rad.count(0)>0:
        rr=nonzero[0];k=rad.count(0);nodes=[Q(0),rr*k/8,rr]
    else:raise ValueError('physical family not declared')
    require(len(set(nodes))==3,'distinct squared-eigenvalue nodes')
    if damage:nodes[1]+=Q(1,100)
    annihilator=eye
    for x in nodes:annihilator=mm(annihilator,ma(h2,scale(-x,eye)))
    require(all(x==0 for row in annihilator for x in row),'literal physical spectral annihilator')
    masses=[];projectors=[]
    for x in nodes:
        proj=eye
        for y in nodes:
            if x!=y:proj=mm(proj,scale(1/(x-y),ma(h2,scale(-y,eye))))
        require(mm(proj,proj)==proj,'physical full projector idempotent')
        projectors.append(proj)
        masses.append(sum((u[i]*proj[i][j]*u[j] for i in range(8) for j in range(8)),Q(0)))
    require(sum(masses)==sum(x*x for x in u),'physical mass completeness')
    require(all(x>=0 for x in masses),'physical mass nonnegative')
    for i in range(3):
        for j in range(i):require(all(x==0 for row in mm(projectors[i],projectors[j]) for x in row),'physical projections orthogonal')
    N=sum(x*x for x in u);D=sum(x**4 for x in u)-N*N/8
    eta=masses[0]**2+sum((x*x/2 for x in masses[1:]),Q(0))
    C=(N*N-eta)/D
    require(C<Q(47,2),'literal physical refined angular bound')
    return {'u':[str(x) for x in u],'squared_nodes':[str(x) for x in nodes],
            'full_pair_masses':[str(x) for x in masses], 'N':str(N),'D':str(D),'eta':str(eta),'C':str(C)}


def run():
    a,=vars(1)
    zero((4*a*a*(64*a-5)).sub([Q(15,208)])+Q(20,13)*Q(15,208)**2,'G exceptional denominator')
    require(15-112*Q(3,32)==Q(9,2),'legal F denominator')
    require(448*Q(3,32)-45==-3,'legal F ratio denominator')
    rectangle=c.boundary()['rectangles']
    for left in [Q(0),Q(1,2),Q(1),Q(3,2)]:
        intervals=sorted((Q(r['box'][2]),Q(r['box'][3])) for r in rectangle if Q(r['box'][0])==left)
        require(intervals[0][0]==0 and intervals[-1][1]==1,'closed phase cover endpoints')
        require(all(x[1]==y[0] for x,y in zip(intervals,intervals[1:])),'closed phase cover joins')
    examples=[]
    for r in [Q(3,2),Q(2),Q(3),Q(5)]:
        examples.append(physical([1,-1,1,-1,1,-1,r,-r]))
    for zeros in [2,4,6]:
        ones=(8-zeros)//2
        examples.append(physical([0]*zeros+[1,-1]*ones))
    try:physical([1,-1,1,-1,1,-1,2,-2],True)
    except ValueError:pass
    else:raise ValueError('wrong physical spectral data accepted')
    rec=c.run()
    damaged=[]
    s,w=vars(2)
    poly=P(2,{tuple(e):Q(z) for e,z in rec['collision_boundary']['gap_polynomial']})
    def reconstruct(rect):
        from math import comb
        out=P(2)
        for (i,j),z in rect['coefficients']:
            out+=Q(z)*comb(6,i)*comb(4,j)*s**i*(1-s)**(6-i)*w**j*(1-w)**(4-j)
        return out
    first=copy.deepcopy(rec['collision_boundary']['rectangles'][0])
    lo,hi,l,r=map(Q,first['box']);original=poly.sub([lo+(hi-lo)*s,l+(r-l)*w])
    zero(reconstruct(first)-original,'whole literal certificate control')
    first['coefficients'][0][1]=str(Q(first['coefficients'][0][1])+1)
    try:zero(reconstruct(first)-original,'changed Bernstein coefficient')
    except ValueError:damaged.append('changed Bernstein coefficient')
    else:raise ValueError('changed Bernstein coefficient accepted')
    for name,p in [('gap numerator shifted by -1',poly-1),('uncertified unit gap substituted for half gap',4*poly-(1+s*(1-w)/2)**2*((s-2)**2+2*s*s*w)*((s-2)**2+8*s*s*w))]:
        try:
            bs=c.bernstein(p.sub([Q(3,2)+s/2,w]),(6,4))
            require(min(bs.values())>=0,name)
        except ValueError:damaged.append(name)
        else:raise ValueError('incorrect sign certificate accepted: '+name)
    fixture=Path(__file__).with_name('expected.json')
    data=json.loads(fixture.read_text());typed(data,rec)
    variants=[]
    v=copy.deepcopy(data);v['cubic']['identity_terms']=False;variants.append(v)
    v=copy.deepcopy(data);del v['cubic'];variants.append(v)
    v=copy.deepcopy(data);v['unexpected']=1;variants.append(v)
    v=copy.deepcopy(data);v['collision_boundary']['rectangles'][0]['coefficients'][0][1]='-1';variants.append(v)
    v=copy.deepcopy(data);v['collision_boundary']['quantitative_refinements'][3]['delta']='1';variants.append(v)
    for v in variants:
        try:typed(v,rec)
        except ValueError:pass
        else:raise ValueError('damaged fixture accepted')
    return {'physical_projection_examples':examples,'literal_spectral_damage_rejected':True,
            'type_sensitive_fixture_damages':len(variants),'certificate_damages':damaged,
            'zero_bounds':{str(q):str(Q(8*(q-1),8-q)) for q in range(2,7)}}


if __name__=='__main__':
    signal.alarm(45)
    rec=run()
    if '--record' in sys.argv:print(json.dumps(rec,sort_keys=True,separators=(',',':')))
    else:
        typed(json.loads(Path(__file__).with_name('controls_expected.json').read_text()),rec)
        print(json.dumps({'status':'PASS','physical_full_projectors':len(rec['physical_projection_examples']),
                          'fixture_damages':rec['type_sensitive_fixture_damages']}))
