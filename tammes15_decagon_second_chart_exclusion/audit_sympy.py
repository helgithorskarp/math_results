"""Separate QQ[t,u,v] chart/cover audit and definition-level graph audit.

The exact compatibility graph arithmetic and written geometry are shared.
This is additional mathematical validation, not independent peer review.
"""
from pathlib import Path
from fractions import Fraction as Q
from itertools import combinations
from math import comb
import json,time,resource
import sympy as s
from sympy.polys.rings import ring
import check
from model import forms,core_points,LABELS

R,t,u,v=ring('t,u,v',s.QQ)
TABLE={2:[[1],[],[]],6:[[],[1],[]],7:[[],[],[1]],
       1:[[0,1],[-1],[0,1]],0:[[-1,0,1],[0,-1],[0,1,1]],
       5:[[0,1],[0,1],[-1]],3:[[0,1,1],[-1,0,1],[0,-1]],
       4:[[-1,0,2,1],[0,-1,1,1],[0,-1,-1]],
       11:[[0,-1,1,1],[0,-1,-1],[-1,0,2,1]],
       12:[[0,-2,0,1],[1,0,-1],[0,0,1,1]]}

def need(ok,message):
    if not ok:raise ValueError(message)

def native(p):return sum((R(s.QQ(c))*t**i for i,c in enumerate(p)),R.zero)

def metric(x,y):
    return sum((x[i]*(1 if i==j else t)*y[j] for i in range(3) for j in range(3)),R.zero)

def ordered_triangle_edge_check(adjacency):
    n=len(adjacency);allbits=(1<<n)-1;triangles=0;tests=0
    for a in range(n):
        bs=adjacency[a]&allbits&~((1<<(a+1))-1)
        while bs:
            bit=bs&-bs;b=bit.bit_length()-1;bs^=bit
            cs=adjacency[a]&adjacency[b]&allbits&~((1<<(b+1))-1)
            while cs:
                bit=cs&-cs;c=bit.bit_length()-1;cs^=bit;triangles+=1
                ds=adjacency[a]&adjacency[b]&adjacency[c]&allbits&~((1<<(c+1))-1)
                while ds:
                    bit=ds&-ds;d=bit.bit_length()-1;ds^=bit;tests+=1
                    need(not adjacency[d]&ds,'five-clique by direct ordered triangle/edge definition')
    return {'ordered_triangles':triangles,'common_neighbor_edge_tests':tests}

if __name__=='__main__':
    started=time.monotonic();S=1+t;D=S**3
    points={i:[sum((c*(2*t)**k*S**(3-k) for k,c in enumerate(p)),R.zero) for p in row] for i,row in TABLE.items()}
    py_points,py_D=core_points()
    need(D==native(py_D),'denominator identity')
    need(all(x==native(py_points[i][k]) for i,row in points.items() for k,x in enumerate(row)),'all30 explicit coordinate comparisons')
    need(all(metric(z,z)==D*D for z in points.values()),'ten direct unit identities')
    G=(1-t*t)*(u*u+v*v)+2*t*(1-t)*u*v;rho=1+G
    Y=[rho-2-2*t*(u+v),2*u,2*v]
    need(metric(Y,Y)==rho*rho,'universal chart unit identity')
    need(Y[0]+t*(Y[1]+Y[2])==rho-2,'chart pole/inverse identity')
    direct=[metric(points[i],Y)-t*D*rho for i in LABELS]
    for F,row in zip(direct,forms(1)):
        f,l,m,a,b=map(native,row)
        need(F==f+l*u+m*v+a*(u*u+v*v)+b*u*v,'all10 core chart-gap identities')
    B,T,U,V,X,Z=ring('t,u,v,x,z',s.QQ)
    def chart(a,b):
        denominator=1+(1-T*T)*(a*a+b*b)+2*T*(1-T)*a*b
        return [denominator-2-2*T*(a+b),2*a,2*b],denominator
    left,rl=chart(U,V);right,rr=chart(X,Z)
    diff=[a*rr-b*rl for a,b in zip(left,right)]
    square=sum((diff[i]*(1 if i==j else T)*diff[j] for i in range(3) for j in range(3)),B.zero)
    delta=(1-T*T)*((U-X)**2+(V-Z)**2)+2*T*(1-T)*(U-X)*(V-Z)
    need(square==4*delta*rl*rr,'universal chord-distance identity')
    degree=max(F.degree(t) for F in direct)
    certificate=json.loads((Path(__file__).parent/'certificate.json').read_text());summaries=[]
    for piece in certificate['pieces']:
        result,leaves,graph,discard=check.verify_piece(piece)
        lo,hi=[s.QQ(*pair) for pair in piece['interval']]
        coefficient_checks=0
        for cell,row in discard:
            depth,i,j=cell;h=s.QQ(8,2**depth);a=-4+i*h;b=-4+j*h
            shifted=direct[row].compose(u,a+h*u).compose(v,b+h*v).compose(t,lo+(hi-lo)*t)
            coefficients=shifted.to_dict()
            for k in range(degree+1):
                for r in range(3):
                    for z in range(3):
                        coefficient=sum((c*s.QQ(comb(k,p),comb(degree,p))*s.QQ(comb(r,q),comb(2,q))*s.QQ(comb(z,w),comb(2,w))
                                         for (p,q,w),c in coefficients.items() if p<=k and q<=r and w<=z),s.QQ.zero)
                        need(coefficient>0,'native strict tensor-Bernstein cover witness')
                        coefficient_checks+=1
        independent=ordered_triangle_edge_check(graph)
        summaries.append({'interval':piece['interval'],'cover_witnesses':len(discard),
                          'native_positive_coefficients':coefficient_checks,'graph_sha256':result['graph_sha256'],
                          'definition_level_clique_audit':independent})
    print(json.dumps({'agent':'six-tammes-2','role':'researcher','status':'SEPARATE_EXACT_CHART_COVER_AND_CLIQUE_AUDIT',
                      'sympy':s.__version__,'coordinate_comparisons':30,'unit_identities':10,'chart_gap_identities':10,
                      'universal_chart_identities':3,'pieces':summaries,
                      'seconds':time.monotonic()-started,'RSS_KiB':resource.getrusage(resource.RUSAGE_SELF).ru_maxrss,
                      'trust_boundary':'Shared certificate and compatibility graph arithmetic; independently rebuilt coordinates/chart/cover signs and different exhaustive clique mechanism; written geometry unformalized, independent review pending.'},indent=2))
