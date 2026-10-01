"""Reject six mathematically false strengthenings; no solver is used."""
import copy,json
from fractions import Fraction as Q
from pathlib import Path
import check as c
import field as f

HERE=Path(__file__).resolve().parent

def run():
    config=json.loads((HERE/'certificate.json').read_text())
    V,H=c.geometry(config)
    vertices,units,_=c.enumerate_polytope(V,H)
    rejected=[]
    def reject(name,claim):
        try:claim()
        except ValueError:rejected.append(name)
        else:raise ValueError('false strengthening accepted: '+name)
    reject('unique_asymmetric_completion',lambda:c.require(len(units)==1,'two actual completions'))
    shorts=[v for v in vertices if c.norm2(v,H)!=f.ONE]
    reject('short_squared_norm_at_most_three_fifths',lambda:c.require(
        all(f.sign(f.sub(c.norm2(v,H),f.scalar(Q(3,5))))<=0 for v in shorts),'actual short vertex exceeds three fifths'))
    gap=f.sub(f.scale(f.ONE,2),f.scale(f.dot(units[0],f.matvec(H,units[1])),2))
    reject('unit_squared_separation_at_least_one_twentieth',lambda:c.require(
        f.sign(f.sub(gap,f.scalar(Q(1,20))))>=0,'actual completion separation below one twentieth'))
    alternate=list(V);alternate[14]=units[1]
    reject('alternate_is_same_labeled_asymmetric_gram',lambda:c.require(
        c.gram(alternate,H)==c.gram(V,H),'alternate has different labeled Gram matrix'))
    larger=copy.deepcopy(config);larger['asymmetric_exclusion_max']='1/1000000000000000'
    reject('asymmetric_local_entry_at_ten_to_minus_fifteen',lambda:c.scalar_bridges(larger))
    # Removing p3's inequality leaves an explicitly feasible exterior vertex.
    normals=[f.matvec(H,v) for v in V]
    rows=[normals[i] for i in (0,4,6)];D=f.det(rows)
    U=tuple(f.det([[f.T if j==k else rows[i][j] for j in range(3)] for i in range(3)]) for k in range(3))
    di=f.inverse(D);v=tuple(f.mul(p,di) for p in U)
    c.require(all(f.sign(f.sub(f.dot(v,normals[i]),f.T))<=0 for i in range(14) if i!=3),
              'exterior vertex satisfies all thirteen remaining constraints')
    reject('thirteen_point_avoidance_polytope_inside_unit_ball',lambda:c.require(
        f.sign(f.sub(c.norm2(v,H),f.ONE))<=0,'explicit exterior vertex after removing p3'))
    c.require(len(rejected)==6,'six actual false claims rejected')
    return {'status':'CONTROLS_PASSED','rejected':rejected}

if __name__=='__main__':print(json.dumps(run(),sort_keys=True))
