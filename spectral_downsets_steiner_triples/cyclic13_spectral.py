"""Exact mean-point and joint three-layer certificates for Pasch closures.

The criterion applies to any existing simple2-(v,3,lambda), v>=7,
lambda>=2 satisfying the checked hypotheses. The complete cyclic13
base corollary and its <=2/3/4-switch scope are in CYCLIC13_SPECTRAL_CAP.md.
No new design census, lower theorem or general H/I resolution is claimed.
six-downset-2, researcher. Standard library; assertions enabled.
"""
from fractions import Fraction as F
from content_psd import content_psd_rank
from defect_gram import scalar_data
from pasch_defect import point_defect,perturbation_certificate,switch_update
from uniform_lambda_small import centered_certificate as ordinary_centered
from uniform_lambda_small import maximal_certificate as ordinary_maximal


def initial_point_certificate(v,lam,blocks,gamma):
    gamma=F(gamma);assert gamma>=0
    _,_,Z=point_defect(v,lam,blocks)
    form=[[gamma*(v*int(x==y)-1)-v*Z[x][y]for y in range(v)]for x in range(v)]
    assert all(sum(row)==0 for row in form)
    stats={};rank=content_psd_rank(form,stats)
    return Z,{'gamma':gamma,'rank':rank,'integer_Schur':stats}


def comparison_data(v,lam,gamma,bound):
    """A joint PSD comparison replaces, and includes, the old row bound.

    Initial/final point PSD is a separate hypothesis. Failure of this
    sufficient comparison says nothing about H or an arbitrary cap.
    """
    data=scalar_data(v,lam,gamma);bound=F(bound)
    comparison=[[bound*int(i==j)-data['G'][i][j]for j in range(3)]for i in range(3)]
    rank=content_psd_rank(comparison)
    assert all(bound>d for d in data['diagonal'])
    delta=data['N']-bound;assert delta>data['g']>0
    data.update(row_bound=data['B'],row_criterion_sufficient=data['whole_interval_sufficient'],
        B=bound,delta=delta,delta_minus_g=delta-data['g'],
        half_gap_margin=(delta-data['g'])/2,whole_interval_sufficient=True,
        comparison=comparison,comparison_rank=rank)
    return data


def chain_data(v,lam,initial,sequence,gamma0,bound,kappa=F(50,3)):
    """Check an initial mean-point form, legality, and the joint comparison.

    Accumulating the point bound uses the ordinary rank-six stability
    lemma, not a final absolute-row bound or a dense slack elimination.
    """
    sequence=list(sequence);gamma0=F(gamma0)
    Z,initial_info=initial_point_certificate(v,lam,initial,gamma0)
    stability=perturbation_certificate(v,kappa)
    current=sorted(initial);updates=[]
    for groups,reverse in sequence:
        current,Z,Delta,info=switch_update(v,lam,current,groups,reverse)
        updates.append((Delta,info))
    gamma=gamma0+len(sequence)*stability['kappa']
    data=comparison_data(v,lam,gamma,bound)
    data['initial_point_certificate']=initial_info
    return current,Z,data,updates


def certificates(v,lam,initial,sequence,gamma0,bound,kappa=F(50,3),eta=None):
    blocks,Z,data,updates=chain_data(v,lam,initial,sequence,gamma0,bound,kappa)
    D,s,Qc=ordinary_centered(v,lam,blocks)
    if eta is None:eta=F(1,8*v*v)
    _,_,Qm,eta=ordinary_maximal(v,lam,blocks,(D,s,Qc),eta)
    return D,s,Qc,Qm,eta,blocks,Z,data,updates


def cohort_parameters():
    return ((4,20,2,151,23768),(5,18,3,183,40920),(6,18,4,220,988913))


def fixtures():
    from cyclic13_gram import orbit_partition,blocks_from_mask
    orbit,_=orbit_partition()
    paths=[
        [(((0,5),(1,4),(2,8)),True),(((0,5),(1,12),(2,3)),False)],
        [(((0,2),(1,3),(9,10)),False),(((0,5),(1,4),(2,10)),True),
         (((0,5),(1,12),(2,3)),False)],
        [(((0,4),(1,3),(2,7)),False),(((0,2),(1,4),(3,9)),True),
         (((0,4),(1,5),(2,3)),True),(((0,4),(1,6),(2,3)),False)]]
    for (lam,gamma,h,bound,mask),moves in zip(cohort_parameters(),paths):
        assert len(moves)==h
        yield lam,gamma,bound,mask,blocks_from_mask(mask,orbit),moves
