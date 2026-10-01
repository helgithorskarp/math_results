"""Explicit capped maximal-rank H matrices for K4 join K_(u,v).

Integers2<=u<=v. FOUR_CENTER_BIPARTITE.md supplies the quantified proof.
The u=v=2 corner uses the credited matching deletion plus a new repair;
the other cases use centered affine-face cores and partition repair.
"""
from fractions import Fraction as F
import certificates as base
import clique_bipartite_face as face
import deletions
from maxrank_mixtures import repaired_core,mix_cores,partition_core
from bipartite_cones import make_nonconstant


def family(u,v,shift=0):return face.family(4,u,v,shift)


def parameters(u,v):
    face.scope(4,u,v)
    if (u,v)==(2,2):raise ValueError('The matching corner has no centered recipe in this construction')
    kappa=F(2);eta_ratio=F(-1,2)
    if (u,v)==(3,3) or u==2 and v==3:
        kappa=F(3,2);eta_ratio=F(-1,8)
    elif u==2 and 4<=v<=12:
        kappa=F(3,2);eta_ratio=F(-1,4)
    elif u==2 and 13<=v<=20:
        kappa=F(3,2);eta_ratio=F(-3,8)
    return face.centered_face(4,u,v,eta=eta_ratio*v,jR=F(3,4),
        kL=kappa/(u-1),kR=F(1,2*(v-1)),tR=F(3,2*u),bR=-1+F(9,4*v),qR=F(-3,2))


def core(u,v,weights=None):
    return face.core(4,u,v,parameters(u,v) if weights is None else weights)


def colors(u,v):
    s=u+v+4;members=family(u,v)[1:];answer=[]
    for x in members:
        vertices=[i for i in range(s) if x & (1 << i)]
        answer.append((2*vertices[0] if len(vertices)==1 else sum(vertices)) % s)
    return make_nonconstant(members,answer,s)


def matching_corner_data():
    members=family(2,2)[1:]
    inherited=[[deletions.core_entry(8,a,b) for b in members] for a in members]
    assignment=[]
    for x in members:
        vertices=[i for i in range(8) if x & (1 << i)]
        assignment.append((2*vertices[0] if len(vertices)==1 else sum(vertices)) % 8)
    assignment[members.index(1)]=1
    assignment[members.index(4)]=5
    part=partition_core(assignment,8)
    return inherited,part,assignment


def matching_corner_core():
    inherited,part,_=matching_corner_data()
    return mix_cores(inherited,part,F(1,128))


def centered_certificate(u,v,shift=0):
    return family(u,v,shift),base.lift(core(u,v),u+v+4),u+v+4


def certificate(u,v,shift=0):
    members=family(u,v,shift);s=u+v+4
    if (u,v)==(2,2):patched=matching_corner_core()
    else:patched,_=repaired_core(core(u,v),colors(u,v),s)
    return members,base.lift(patched,s),s
