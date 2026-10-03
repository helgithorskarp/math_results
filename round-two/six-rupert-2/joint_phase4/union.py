#!/usr/bin/env python3
"""Exact closed three-cell union geometry; prior9855 is a theorem dependency.

No replay of old forests or additional source/exclusion proof is implied.
"""
from fractions import Fraction as F
from pathlib import Path
import argparse,json,sys,time
sys.path.insert(0,str(Path(__file__).resolve().parent.parent/'phase4_contacts'))
import geometry as g
Q,S=g.Q,g.S

def record():
    start=time.monotonic()
    p,q,z=g.PENT
    u=((1+3*S)/22,(21-3*S)/22);d=((S-1)/2,3-S)
    T=[u,q,d];W=[u,p,z,d]
    t=S/4;a=(S-1)/4
    g.require(0<t<1 and 0<a<1,'proper closed seam side parameters')
    g.require(tuple((1-t)*x+t*y for x,y in zip(u,q))==p,'new seam first endpoint on whole triangle side')
    g.require(tuple((1-a)*x+a*y for x,y in zip(q,d))==z,'new seam second endpoint on whole triangle side')
    upper=(Q(F(-1,2)),Q(),Q(1));lower=tuple(-x for x in upper)
    g.require(g.clip(T,upper)==W and g.clip(T,lower)==g.PENT,'entire closed triangle clips are exactly old quadrilateral and new whole phase4')
    g.require(g.clip(g.PENT,upper)==[p,z] and g.clip(W,lower)==[p,z],'both intersections retain the entire common closed segment')
    p0=((5-S)/6,(5*S-7)/6);p4=((S-1)/2,(9*S-19)/2)
    old40=[p0,u,p,z,p4];old56=[d,p0,p4]
    seam=(Q(-1),(15+S)/22,(9+5*S)/22)
    def same_cycle(left,right):
        return len(left)==len(right) and any(left[k:]+left[:k]==right for k in range(len(left)))
    g.require(same_cycle(g.clip(W,seam),old56),'whole old56 closed triangle retained')
    g.require(same_cycle(g.clip(W,tuple(-x for x in seam)),old40),'whole old40 closed pentagon retained')
    g.require(g.area(T)==(9*S-19)/11>0 and g.area(W)==Q(F(-175,44),F(20,11))>0,'literal positive three-cell and old quadrilateral double areas')
    g.require(g.area(T)==g.area(W)+g.area(g.PENT) and g.area(W)==g.area(old40)+g.area(old56),'exact additive area check corroborates whole clips')
    g.require(all(x+3*y-S<0 for x,y in g.PENT),'A/AH absent on entire new closed triangle')
    g.require(g.value(upper,q)<0,'extra-motion receiving corner is outside old quadrilateral')
    return {'agent':'six-rupert-2','role':'researcher','scope':'exact closed three-cell union geometry only, source classification uses new phase4 theorem plus explicit published9855/0','three_cell_triangle':list(map(g.vec,T)),'whole_old_quadrilateral':list(map(g.vec,W)),'whole_new_phase4_triangle':list(map(g.vec,g.PENT)),'whole_old_phase40_pentagon':list(map(g.vec,old40)),'whole_old_phase56_triangle':list(map(g.vec,old56)),'side_parameters':[g.enc(t),g.enc(a)],'common_closed_segment':list(map(g.vec,[p,z])),'three_cell_double_area':g.enc(g.area(T)),'old_quadrilateral_double_area':g.enc(g.area(W)),'new_phase4_double_area':g.enc(g.area(g.PENT)),'prior_source_commit':'cd1652c996fae640adb44604a737d0449675c81c','prior_graph_ref':'bafkreigmpah7nts57ko3ctmc4nrjskbi5clc5ldicjwu5yiwh33nusaahq','prior_graph_height':9855,'old_source_forests_replayed':False,'global_J74_Rupert_status':'OPEN','wall_seconds':time.monotonic()-start}

if __name__=='__main__':
    parser=argparse.ArgumentParser();parser.add_argument('--output',required=True);args=parser.parse_args()
    r=record();Path(args.output).write_text(json.dumps(r,indent=2)+'\n');print(json.dumps(r,indent=2))
