"""Capped maximal-rank H for K3 joined to K_(u,v), integers2<=u<=v.

The complete all-parameter proof is in THREE_CENTER_BIPARTITE.md.
Custom affine-face weights have no PSD/cap guarantee.
"""
from fractions import Fraction as F
import certificates as base
import clique_bipartite_face as face
from maxrank_mixtures import repaired_core
from bipartite_cones import make_nonconstant


def parameters(u,v):
    face.scope(3,u,v)
    if (u,v)==(2,2):
        return face.centered_face(3,u,v,jL=F(7,16),jR=F(1,2),kL=F(59,96),kR=F(53,96),
                         kT=F(35,96),aL=F(-7,48),aR=F(-7,48),tL=F(-7,48),
                         tR=F(-5,96),bL=F(-7,8),bR=-1,bT=F(-7,8),
                         qL=F(-7,16),qR=F(-9,16))
    return face.centered_face(3,u,v,jL=0,jR=F(1,2),kL=F(3,2) if u==2 else F(2,u-1),
                     kR=F(3,2*(v-1)),kT=0,aL=0,aR=0,tL=0,tR=F(3,2*u),
                     bL=0,bR=-1,bT=0,qL=0,qR=-1)


def family(u,v,shift=0):return face.family(3,u,v,shift)


def core(u,v,weights=None):return face.core(3,u,v,parameters(u,v) if weights is None else weights)


def colors(u,v):
    s=u+v+3;members=family(u,v)[1:];answer=[]
    for x in members:
        vertices=[i for i in range(s) if x & (1 << i)]
        answer.append((2*vertices[0] if len(vertices)==1 else sum(vertices)) % s)
    return make_nonconstant(members,answer,s)


def centered_certificate(u,v,shift=0):
    return family(u,v,shift),base.lift(core(u,v),u+v+3),u+v+3


def certificate(u,v,shift=0):
    repaired,_=repaired_core(core(u,v),colors(u,v),u+v+3)
    return family(u,v,shift),base.lift(repaired,u+v+3),u+v+3
