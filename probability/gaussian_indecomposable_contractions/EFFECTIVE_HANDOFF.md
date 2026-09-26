# Consumer handoff: an effective indecomposable witness

This is a quantitative supplement to the accepted indecomposable-map
reduction, not another positive flap or cap class. The [new proof](EFFECTIVE_BOUND.md)
is author-side and awaits independent review. The reviewed orthocentric
depth-one theorem and its two finite templates remain closed at their
[recorded scope](../gaussian_flap_selector_motion/REVIEW_STATUS.md).

For an N-atom contraction with negative hinge gap at least delta>0, define

    h_N = 512*2^N*(N+6) + 3N + binom(N,3) + 6,
    M_N = 12 h_N [1+h_N+binom(h_N,2)+binom(h_N,3)].

There is a negative **indecomposable** step with at most 4M_N labels,
every labelled weight at least delta/[8M_N(1+delta)], and a negative gap
of magnitude greater than delta*2^(-M_N). It fixes a tetrahedron and
preserves a common facet-connected tetrahedral framework. The finite
interval includes all three-dimensional intermediate placements.

The geometric extension has at most 512*2^N convex isometric pieces,
each with at most N+6 facets, before making a conforming tetrahedral
mesh. Rational prescribed coordinates give rational mesh coordinates
and rational representatives of all the finite interval's states.
The original proof supplied no bound in N and did not assert rationality.
Its reviewed qualitative assertions are unchanged.

## Composition with the measure lane

The accepted [paired cubature](../gaussian_prior_localization/CUBATURE_FRONTIER.md)
and its [independent review](../gaussian_paired_cubature_review2/REVIEW.md)
supply the following producer. For any hypothetical unrestricted defect
delta>0, choose k=ceil(6/delta). Set

    ell=ceil(log2 k),
    h=floor(sqrt(ell+1)), n=ceil(k/h),
    A_k=min {k^3[2 binom(2ell+6,3)-1],
             n^3[2 binom(4ell+11,3)-1]}.

There is a variance-one finite contraction with at most A_k atoms, both
supports in B(0,2k), and defect at least delta/2. Use N=A_k and
`d=delta/2` in the new theorem. It produces an indecomposable negative
step with

    at most 4M_(A_k) labels,
    each labelled weight >= delta/[8 M_(A_k)(2+delta)],
    negative gap magnitude > delta*2^(-M_(A_k)-1).             (1)

All centres can be placed in B(0,7k) after aligning the fixed root
tetrahedron: the original convex hull has diameter at most 4k when
full-dimensional, and otherwise a containing cube [-2k,2k]^3 has
diameter 4sqrt(3)k<7k. Every intermediate pair distance is bounded by
its source value. The threshold may change; variance is one. These
statements do not preserve a specified dominant atom or a source grid.

Equation (1) is a **defect-dependent complexity bound**. It removes the
unquantified mesh size in this composition. It does not give a universal
fixed atom count independent of delta, nor a favorable computational cost.

## Numerical and certificate boundary

The rationality statement has no denominator or bit-length bound. It does
not put the new maps into the existing finite rational input family with
its specified coordinate and weight denominators. The arbitrary-input
[direct hinge oracle](../gaussian_prior_localization/DIRECT_HINGE.md)
could consume a constructed rational step, with parameters and precision
chosen for that actual input. Its small-frontier budget cannot be copied
to the enlarged mesh. No oracle run or new Gaussian sign is claimed here.

The conservative gap scale is doubly exponential in the original atom
count. Thus an absolute numerical error must be smaller than the surviving
gap, not merely the original delta. Finite-state factorization does not
justify a constant-fraction gap transfer. Bounds on coordinate heights,
mesh angles, site separation, or analytic sign remain separate tasks.

No existing accepted template needs to be replayed for this supplement.
The current next mathematical obligation is still a sign argument on
indecomposable steps, or a decisively more useful complexity bound. The
new statement does not settle the unrestricted conjecture or give a new
Kneser--Poulsen positive case.
