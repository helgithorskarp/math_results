#!/usr/bin/env python3
"""Scoped semantic controls for independent bridge coverage and root exclusion."""
import json
from fractions import Fraction as Q
import check as c

def rejects(fn):
    try:fn()
    except ValueError:return True
    raise ValueError('a mathematical damage was silently accepted')

def run():
    tests=[]
    tests.append(('both identically-zero equations',rejects(lambda:c.bezout(c.ZERO,c.ZERO))))
    h,u,v=c.bezout(c.ZERO,(2,1))
    c.need(c.add(c.mul(u,c.ZERO),c.mul(v,(2,1)))==h,'single-zero legitimate equation')
    tests.append(('single-zero nonzero other equation passes',True))
    # Having a divisor with no root is insufficient: arbitrary 1 divides BOTH equations.
    f=(-Q(29,40),1);g=c.scale(f,7)
    trueh,_,_=c.bezout(f,g)
    tests.append(('common interior root cannot get a strict certificate',not c.strict_sign(c.bernstein(trueh,c.J))))
    tests.append(('closed left endpoint is included',not c.strict_sign(c.bernstein((-c.J[0],1),c.J))))
    tests.append(('closed right endpoint is included',not c.strict_sign(c.bernstein((-c.J[1],1),c.J))))
    tests.append(('mixed Bernstein signs are not exclusion',not c.strict_sign((Q(-1),Q(1)))))
    h,u,v=c.bezout((1,2),(1,3))
    tests.append(('damaged explicit identity',rejects(lambda:c.need(c.add(c.mul(c.add(u,c.ONE),(1,2)),c.mul(v,(1,3)))==h,'bad identity'))))
    cases=c.typed_cases();raw,keep,_=c.exhaustive_long()
    dropped=set(keep);dropped.pop()
    tests.append(('omitted labeled placement',rejects(lambda:c.need(dropped==keep,'coverage loss'))))
    wrong=set(keep);wrong.add(tuple(sorted(((0,6,1),(1,2,3),(2,4,3)))))
    tests.append(('introduced wrong physical placement',rejects(lambda:c.need(wrong==keep,'case corruption'))))
    # Three distinct triangles on one edge give K3; deleting its third edge fabricates a path.
    fan=((0,1,2),(0,1,4),(0,1,5))
    tests.append(('all actual adjacencies retained',len(c.adjacencies(fan))==3 and not c.tree(fan)))
    first=next(iter(cases));fs,p,ce,f,g=c.construct(first)
    q=dict(p);q[7]=tuple(c.add(t,c.ONE) for t in q[7])
    tests.append(('changed physical corner vector',rejects(lambda:c.need(c.numerator(q[7],q[7])==(2,-1),'unit corruption'))))
    q=dict(p);q[7],q[9]=q[9],q[7]
    tests.append(('wrong original contact labels',any(c.numerator(q[x],q[y])!=c.R for x,y in ce)))
    # Actual certificate is invariant under a simultaneous permutation of all three basis axes.
    q={i:(v[2],v[0],v[1]) for i,v in p.items()}
    tests.append(('consistent basis permutation passes',all(c.numerator(q[x],q[y])==c.numerator(p[x],p[y]) for x in p for y in p)))
    tests.append(('face ordering is immaterial',set(c.adjacencies(tuple(reversed(fs))))!=set() and c.tree(tuple(reversed(fs)))))
    tests.append(('profile occurrence is necessary only',c.profiles()['removed']==[[1,10],[11]]))
    c.need(all(v for _,v in tests),'a semantic control failed')
    return dict(agent='six-reviewer-2',role='independent mathematical reviewer',controls=[dict(name=n,pass_=v) for n,v in tests],count=len(tests))

if __name__=='__main__':print(json.dumps(run(),sort_keys=True,separators=(',',':')))
