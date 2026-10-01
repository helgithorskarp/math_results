"""Depth-one eligibility and the first pair peel, with audited negatives."""
from geometry import affine,inverse,pose


def eligible(p,root_cover):
    supported=root_cover.support()
    domain={t for t in supported if affine(p.tile,inverse(pose(p.tile,t))) in supported}
    p.check_domain(domain)
    return domain


def first_peel(p,eligible_domain):
    domain=set()
    for t in sorted(eligible_domain):
        # Only TESTED fixed pairs are prefiltered. New neighbors remain E0.
        if p.cover((p.tile,t),p.raw).find() is not None:domain.add(t)
    p.check_domain(domain)
    return domain
