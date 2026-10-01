#!/usr/bin/env python3
"""Exact complete cover for the four remaining two-double sections.

Actual author six-sendov-2, researcher. Public transport/trace/filter
source is openly adapted, not an independent implementation or review.
The twelve complete strict/grouped kernels are derived by verify.py.
"""
import hashlib,importlib.util
from fractions import Fraction as F
from pathlib import Path

HERE=Path(__file__).resolve().parent
SOURCE=HERE.parent/'sendov_degree9_two_double_strict_sectors'/'cover.py'
PIN='3af5ceb23c91ab2b6a9c3d28bee37d8cfa16e3570810574b9ea221ec579c42c4'
if hashlib.sha256(SOURCE.read_bytes()).hexdigest()!=PIN:raise ValueError('credited transport source pin mismatch')
spec=importlib.util.spec_from_file_location('credited_transport',SOURCE)
c=importlib.util.module_from_spec(spec);spec.loader.exec_module(c)
m=c.m
PAIRS=((1,5),(1,6),(2,5),(2,6))
KEYS=(((None,2),(None,3),(None,4),(0,4),(1,4)),
      ((None,2),(None,3),(0,3),(0,4),(1,4)),
      ((None,2),(1,3),(None,3),(0,3),(1,4)))

def paths(pair):
    if pair not in PAIRS:raise ValueError('not a remaining section')
    w,M,low,neutral,high=c.data(pair)
    m.require(low==[0,1] and neutral==[2] and high==[4,3],'entire remaining clipping type')
    cells=[(list(keys),[c.vertex(M,i,j) for i,j in keys]) for keys in KEYS]
    m.require(len(cells)==3,'all three reversed-row monotone paths')
    return w,M,low,neutral,high,cells
c.path_cells=paths
c.SECTIONS=PAIRS

def mapping(pair):
    w,M,*_=c.data(pair)
    return [F(0),F(0),F(6,5),F(2*(3-M[0]),5-M[0]),F(2*(M[4]-5),M[4]-3)]

def common():
    record=c.all_geometry()
    for row in record:
        pair=tuple(row['doubled_ranks']);S_coeff=mapping(pair)
        row['reversed_low_rows']=[2,1,'dummy']
        row['local_cell']=2
        row['local_S_coefficients']=list(map(str,S_coeff))
        row['local_x_coefficients']=['1','0','0','0','0']
        for index in range(5):
            levels=list(map(F,row['cells'][2]['level_vertices'][index]))
            theta=[levels[j] for j in range(6) for _ in range(row['weights'][j])]
            S=sum(1+t for t in theta[:3])+sum(1-t for t in theta[5:])
            x=(theta[4]-theta[3])/2
            m.require(S==S_coeff[index] and x==int(index==0),'whole all-balanced affine local map')
        m.require(max(S_coeff)<=F(6,5),'whole local deficit mass bound')
    m.require(F(6,5)/120000==F(1,100000),'all-balanced local S guard')
    m.require((F(119999,120000)*F(147,500))**2>=F(2,25) and F(37,125)**2<=F(9,100),'all-balanced exact central scalar guards')
    m.require(m.j_value(F(87,1000))-F(785753,1000)>F(1,1250),'retained exact strict gap below scalar optimum')
    return record

def full_controls(pair,cell,rows,meta):
    # Same complete definition-level controls as the pinned backend,
    # with the new four physical affine maps printed explicitly.
    roots,mu,traces,base,gram,rhs,d,n,target=rows;scale=meta['scale'];big=8*scale
    profiles=[tuple(F(int(i==j)) for i in range(5)) for j in range(5)]
    profiles.append((F(1,5),)*5)
    grouped=(cell==2)
    if grouped:
        t=F(59,200)
        for q in (F(0),F(1,240000),F(1,120000),F(1,60000)):
            profiles.append(((1-q)*t,(1-q)*(1-t),q/3,q/3,q/3))
    records=[]
    for bary in profiles:
        m.require(sum(bary)==1 and all(a>=0 for a in bary),'full control barycentric domain')
        theta=[p.evaluate(bary)/scale for p in roots]
        m.require(sum(theta)==0 and max(map(abs,theta))==1,'full control physical normalization')
        moments=[sum(t**r for t in theta) for r in range(1,9)]
        for r in range(1,9):m.require(mu[r-1].evaluate(bary)==scale**r*moments[r-1],'full control scaled moment')
        cc=[[(theta[i] if i==j else F(0))-(theta[i]+theta[j])/8 for j in range(8)] for i in range(8)]
        ww=[[theta[i]*theta[j]/8 for j in range(8)] for i in range(8)]
        identity=[[F(int(i==j)) for j in range(8)] for i in range(8)]
        powers=[identity]
        for r in range(1,9):powers.append(m.mm(powers[-1],cc))
        ss=[F(7)]+[m.tr(powers[r]) for r in range(1,9)]
        for r in range(1,9):m.require(traces[r].evaluate(bary)==big**r*ss[r],'full trace versus cyclic words')
        bb=[m.tr(m.mm(ww,powers[r])) for r in range(5)]
        for r in range(5):m.require(base[r].evaluate(bary)==8*scale**2*big**r*bb[r],'full coupling numerator scale')
        matrices=[[[powers[r][i][j]-powers[r+2][i][j] for j in range(8)] for i in range(8)] for r in range(3)]
        gg=[[m.tr(m.mm(matrices[i],matrices[j]))-F(int(i==j==0)) for j in range(3)] for i in range(3)]
        rr=[m.tr(m.mm(ww,p)) for p in matrices]
        for i in range(3):
            m.require(rhs[i].evaluate(bary)==F(big**(i+4),8)*rr[i],'full filtered rhs scaling')
            for j in range(3):m.require(gram[i][j].evaluate(bary)==big**(i+j+4)*gg[i][j],'full filtered Gram scaling')
        det=gg[0][0]*(gg[1][1]*gg[2][2]-gg[1][2]*gg[2][1])-gg[0][1]*(gg[1][0]*gg[2][2]-gg[1][2]*gg[2][0])+gg[0][2]*(gg[1][0]*gg[2][1]-gg[1][1]*gg[2][0])
        m.require(d.evaluate(bary)==big**18*det,'full determinant scaling')
        psi,commutant_rank=m.pinching(theta)
        actual=122*moments[1]+(224*moments[3]-5760*psi)/moments[1]
        lower=None
        if det:
            m.require(det>0,'full control positive nonsingular Gram')
            solution=m.solve(gg,rr);lower=sum(a*b for a,b in zip(rr,solution))
            m.require(n.evaluate(bary)==64*scale**4*big**18*det*lower,'full adjugate numerator versus Gaussian solve')
            m.require(lower<=psi,'full commutant versus filtered projection')
            cleared=(F(785753,1000)*moments[1]-122*moments[1]**2-224*moments[3])*det+5760*det*lower
            m.require(target.evaluate(bary)==1000*scale**4*big**18*cleared,'entire strict target normalization')
        else:
            m.require(n.evaluate(bary)==0 and target.evaluate(bary)==0,'singular cleared numerators without division')
        local=False;normal=None;x=None
        if grouped:
            minus=[1+t for t in theta[:3]];plus=[1-t for t in theta[5:]]
            normal=sum(minus+plus);x=(theta[4]-theta[3])/2;q=sum(bary[2:])
            m.require(all(t>=0 for t in minus+plus),'physical two-sided deficits')
            m.require(normal==sum(a*b for a,b in zip(mapping(pair),bary)) and x==bary[0],'full four-section two-sided local chart mapping')
            local=(q<=F(1,120000) and F(147,500)<=bary[0]/(1-q)<=F(37,125))
            if local:
                m.require(normal<=F(1,100000) and F(2,25)<=x*x<=F(9,100),'all-balanced local physical guard')
                m.require(actual<=m.j_value(x*x)-200*normal,'full defining local loss control')
        if not local:m.require(actual<=F(785753,1000),'full defining strict-region inequality')
        records.append({'bary':list(map(str,bary)),'theta':list(map(str,theta)),
            'D':str(det),'Psi':str(psi),'J':str(actual),
            'filtered_lower':str(lower) if lower is not None else None,
            'commutant_rank':commutant_rank,'branch':'local' if local else 'strict',
            'total_deficit':str(normal) if normal is not None else None,
            'singleton_half_difference':str(x) if x is not None else None})
    return records

