"""Second exact vertex census from the moving triangle and release interval.

This does not enumerate active-facet subsets. The ordinary interpolation
argument justifying the construction is written in PROOF.md.
"""
from binding import check_current
check_current()
from fractions import Fraction as F
import json
from polyhedron import facets, vertices_of
from joint import model

P0=F(8421443,65536)
A0=F(1043037,16384)
B0=F(1080063,16384)
C0=F(649645,16384)
R=F(91211,16384)
b=F(827,32768)
t_mass=F(70957,3964928)
t_max=F(19967,229376)


def A(t):return A0-18*t
def B(t):return B0-F(9,2)*t
def C(t):return C0-5*t
def P(t):return P0+38*t
def H(t):return A(t)+B(t)+C(t)-P(t)
def J(t):return A(t)+B(t)-P(t)
def U(t):return (R-32*t)/45
def low(t):return max(F(0),t-b)
def coords(t,u,v,d):return (t,A(t)-u,B(t)-v,d)


def run():
    model.require(F(0)<t_mass<b<t_max and J(t_mass)==0 and U(t_max)==t_max-b,
                  'exact ordering and all two moving-face transition identities')
    model.require(t_max==(R+45*b)/77 and t_mass==2*(A0+B0-P0)/121,
                  'exact mass and release breakpoints')
    endpoint_fields=[]
    for t in (F(0),t_max):
        values=dict(A=A(t),B=B(t),C=C(t),H=H(t),
                    A_minus_H=A(t)-H(t),B_minus_H=B(t)-H(t))
        model.require(all(a>0 for a in values.values()),
                      'all affine mass caps positive and mass nonnegativity redundant on entire interval')
        endpoint_fields.append(dict(tau=str(t),values={k:str(v) for k,v in values.items()}))
    V=set()
    for u,v in ((J(F(0)),F(0)),(F(0),J(F(0))),
                (H(F(0)),F(0)),(F(0),H(F(0)))):
        for d in (F(0),U(F(0))):V.add(coords(F(0),u,v,d))
    for d in (F(0),U(t_mass)):V.add(coords(t_mass,F(0),F(0),d))
    for u,v in ((F(0),F(0)),(H(b),F(0)),(F(0),H(b))):
        V.add(coords(b,u,v,F(0)))
    for u,v in ((F(0),F(0)),(H(t_max),F(0)),(F(0),H(t_max))):
        V.add(coords(t_max,u,v,low(t_max)))
    enum,coverage=vertices_of(facets())
    model.require(len(V)==16 and V==set(enum),
                  'ENTIRE independently constructed geometric vertex set equals all active-facet vertices')
    # Every additional slice endpoint needed for interpolation is a convex
    # combination of the sixteen vertices, with explicit rational weights.
    redundant=[]
    for t in (t_mass,b):
        for u,v in ((H(t),F(0)),(F(0),H(t))):
            x=coords(t,u,v,U(t))
            start=coords(F(0),H(F(0)) if u else F(0),H(F(0)) if v else F(0),U(F(0)))
            end=coords(t_max,H(t_max) if u else F(0),H(t_max) if v else F(0),U(t_max))
            w=t/t_max
            model.require(start in V and end in V and
                          all((1-w)*a+w*z==y for a,z,y in zip(start,end,x)),
                          'every outer/upper intermediate point has a full explicit vertex decomposition')
            redundant.append(dict(point=[str(a) for a in x],weight=str(w),
                                  start=[str(a) for a in start],end=[str(a) for a in end]))
    for u,v in ((H(t_mass),F(0)),(F(0),H(t_mass))):
        x=coords(t_mass,u,v,F(0))
        start=coords(F(0),H(F(0)) if u else F(0),H(F(0)) if v else F(0),F(0))
        end=coords(b,H(b) if u else F(0),H(b) if v else F(0),F(0))
        w=t_mass/b
        model.require(start in V and end in V and
                      all((1-w)*a+w*z==y for a,z,y in zip(start,end,x)),
                      'every outer/lower intermediate point has a full explicit vertex decomposition')
        redundant.append(dict(point=[str(a) for a in x],weight=str(w),
                              start=[str(a) for a in start],end=[str(a) for a in end]))
    x=coords(b,F(0),F(0),U(b))
    start=coords(t_mass,F(0),F(0),U(t_mass))
    end=coords(t_max,F(0),F(0),U(t_max))
    w=(b-t_mass)/(t_max-t_mass)
    model.require(start in V and end in V and
                  all((1-w)*a+w*z==y for a,z,y in zip(start,end,x)),
                  'middle origin/upper point has a full explicit vertex decomposition')
    redundant.append(dict(point=[str(a) for a in x],weight=str(w),
                          start=[str(a) for a in start],end=[str(a) for a in end]))
    return dict(agent='six-downset-2',role='researcher',
                geometric_vertex_count=len(V),vertices=[[str(a) for a in x] for x in sorted(V)],
                independent_of_active_subset_enumeration=True,
                entire_active_subset_vertex_sets_equal=True,
                affine_endpoint_bounds=endpoint_fields,
                all_seven_redundant_slice_points=redundant,
                coverage_counts=dict(all=210,singular=len(coverage['singular_subsets']),
                                     nonsingular=coverage['nonsingular_subsets'],
                                     infeasible=len(coverage['infeasible_subsets'])),
                exact_tau_projection=['0',str(t_max)],
                sharp_template_obstruction='45*(827/32768-tau+d)+(91211/16384-32*tau-45*d)=77*(19967/229376-tau)',
                full_optimizer_domain_or_H_nonexistence_not_inferred=True)


if __name__=='__main__':print(json.dumps(run(),sort_keys=True,indent=2))
