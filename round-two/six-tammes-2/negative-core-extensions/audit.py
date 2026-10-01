"""Separate same-author arithmetic audit of supplied vertex witnesses.

This module does not call a witness selector.  It shares the pinned interval
kernel and the validated curve model; it is not an independent researcher
review or an independent implementation of the whole curve enclosure.
"""
from dependency import e
import model as m
I,Q,S=e.I,e.Q,e.S
BOUND=10
def need(ok,message):e.require(ok,message)
def inner(a,b):return sum((x*y for x,y in zip(a,b)),I())
def minors(rows,rhs):
    u,v,w=rows
    cofactors=[e.cross(v,w),e.cross(w,u),e.cross(u,v)]
    determinant=inner(u,cofactors[0])
    numerator=[sum((rhs[j]*cofactors[j][i] for j in range(3)),I()) for i in range(3)]
    return numerator,determinant
def homogeneous(triple,C,D,rows,rhs,witness):
    need(type(witness)in (tuple,list) and len(witness)==2,'two sign-regime witnesses')
    for wanted,index in ((1,witness[0]),(-1,witness[1])):
        if (wanted==1 and D.sign()<0) or (wanted==-1 and D.sign()>0):continue
        need(type(index)is int and 0<=index<len(rows) and index not in triple,'avoidance witness index')
        residual=inner(rows[index],C)-rhs[index]*D
        need(residual.l>0 if wanted==1 else residual.h<0,'strict homogeneous infeasibility')
def dual_inner(a,b):return sum((x*y for x,y in zip(a,b)),m.D())
def dual_minors(rows,rhs):
    u,v,w=rows
    cofactors=[m.cross(v,w),m.cross(w,u),m.cross(u,v)]
    determinant=dual_inner(u,cofactors[0])
    numerator=[sum((rhs[j]*cofactors[j][i] for j in range(3)),m.D()) for i in range(3)]
    return numerator,determinant
def centered(triple,model):
    rows,rows0,rhs,rhs0=(model[k] for k in ('A','A0','rhs','rhs0'))
    C,D=dual_minors([rows[i] for i in triple],[rhs[i] for i in triple])
    C0,D0=dual_minors([rows0[i] for i in triple],[rhs0[i] for i in triple])
    radius=model['radius']
    return [m.recondition(c,c0,radius) for c,c0 in zip(C,C0)],m.recondition(D,D0,radius),C0,D0
def verify(triple,result,rows,rhs,H,model):
    kind,witness=result
    need(tuple(sorted(triple))==triple and len(triple)==3 and 0<=triple[0]<triple[-1]<14,
         'literal independent-triple candidate')
    if kind=='analytic-critical':
        need(triple==(1,3,6) and witness is None,'only labels1,4,7 may use lemma9003')
        return
    C,D=minors([rows[i] for i in triple],[rhs[i] for i in triple])
    if kind=='coordinate':
        need(type(witness)is int and 0<=witness<3,'coordinate witness')
        c=C[witness]
        need(c.sign()!=0 and min(abs(c.l),abs(c.h))>BOUND*max(abs(D.l),abs(D.h)),
             'Cramer numerator exceeds proved outer coordinate bound')
    elif kind=='homogeneous':homogeneous(triple,C,D,rows,rhs,witness)
    elif kind=='norm':
        need(D.sign()!=0,'independent triple determinant')
        value=e.dot([c/D for c in C],[c/D for c in C],H)
        need(type(witness)is int and value.h==witness and witness<S,'strict direct vertex norm')
    elif kind in ('mvt-coordinate','mvt-homogeneous','mvt-norm'):
        C,D,C0,D0=centered(triple,model)
        if kind=='mvt-coordinate':
            need(type(witness)is int and 0<=witness<3,'centered coordinate witness')
            c=C[witness].v
            need(c.sign()!=0 and min(abs(c.l),abs(c.h))>BOUND*max(abs(D.v.l),abs(D.v.h)),
                 'strict centered coordinate exclusion')
        elif kind=='mvt-norm':
            need(D.v.sign()!=0 and D0.v.sign()!=0,'centered independent determinant')
            x0=[c/D0 for c in C0]
            x=[m.recondition(c/D,z,model['radius']) for c,z in zip(C,x0)]
            value=m.recondition(m.dot(x,x,model['H']),m.dot(x0,x0,model['H0']),model['radius']).v
            need(type(witness)is int and value.h==witness and witness<S,'strict centered vertex norm')
        else:
            need(type(witness)in (tuple,list) and len(witness)==2,'centered sign-regime witnesses')
            for wanted,index in ((1,witness[0]),(-1,witness[1])):
                if (wanted==1 and D.v.sign()<0) or (wanted==-1 and D.v.sign()>0):continue
                need(type(index)is int and 0<=index<14 and index not in triple,'centered avoidance index')
                residual=m.recondition(dual_inner(model['A'][index],C)-model['rhs'][index]*D,
                    dual_inner(model['A0'][index],C0)-model['rhs0'][index]*D0,model['radius']).v
                need(residual.l>0 if wanted==1 else residual.h<0,'strict centered homogeneous exclusion')
    elif kind=='gram-norm':
        need(triple[-1]==13,'cut-plane Gram witness')
        labels=(0,1,2,4,5,6,7,8,9,10,11,12,13,'cut')
        contacts={(0,5),(0,6),(0,7),(0,11),(1,2),(1,4),(1,10),(1,12),(2,4),(2,8),
                  (2,10),(2,13),(4,8),(5,7),(5,9),(5,11),(6,8),(6,11),(7,12),(8,13),
                  (9,10),(9,11),(10,12)}
        a,b=(labels[i] for i in triple[:2]);t=model['t'];n=model['n'];P=model['P']
        s=t if (a,b)in contacts else m.dot(P[a],P[b],model['H'])
        need((1-s*s).v.l>0,'independent pair of unit normals')
        products=[Q(14,5)*t if i==4 else m.dot(n,P[i],model['H']) for i in (a,b)]
        na,nb=products
        perpendicular=model['nn']-(na*na+nb*nb-2*s*na*nb)/(1-s*s)
        need(perpendicular.v.l>0,'strict perpendicular Gram pivot')
        height=Q(893,1000)*model['length']-t*(na+nb)/(1+s)
        value=(2*t*t/(1+s)+height*height/perpendicular).v
        need(type(witness)is int and value.h==witness and witness<S,'strict cut vertex norm')
    else:raise ValueError('unknown vertex proof strategy')
