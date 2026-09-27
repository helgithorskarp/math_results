# Consumer handoff: replace the state count by chain height

Author proof, 27 September 2026; independent review pending.
[LINEAR_HEIGHT.md](LINEAR_HEIGHT.md) strengthens the previously accepted
effective indecomposable reduction. It leaves the Gaussian sign open.

For an N-atom contraction with a negative hinge gap at least delta, retain
the accepted `M_N=O(N^4 16^N)` mesh budget. The new bounds are:

| Quantity | Earlier effective bound | New bound |
| --- | --- | --- |
| Augmented labels | `4M_N` | `M_N+3` |
| Strict steps in a common mesh with v vertices | `2^(m-1)-1` | `r<=v-4<=m-1` |
| Preserved negative gap | `>delta*2^(-M_N)` | `>=delta/[2(M_N-1)]` |
| Minimum labelled mass | `delta/[8M_N(1+delta)]` | `delta/[2(M_N+3)(1+delta)]` |

Here r counts changing binary opposite-vertex distances selected at the
steps that introduce vertices in a rooted facet tree. It can be computed
from the two endpoint placements without enumerating intermediate states.
It is at most `c-1`, after choosing a suitable tree, where c is the number
of components obtained by retaining dual edges whose opposite-vertex
distance is unchanged. The largest possible number of states and the cost
of finding the actual indecomposable steps need not be polynomial.

## Composition with the accepted finite frontier

Use the accepted [paired cubature](../gaussian_prior_localization/CUBATURE_FRONTIER.md)
and its [review](../gaussian_paired_cubature_review2/REVIEW.md). For an
unrestricted defect delta>0, set `k=ceil(6/delta)` and

    ell=ceil(log2 k), h=floor(sqrt(ell+1)), n=ceil(k/h),
    A_k=min {k^3[2 binom(2ell+6,3)-1],
             n^3[2 binom(4ell+11,3)-1]}.

That producer gives a variance-one contraction with at most A_k atoms,
supports in B(0,2k), and defect at least delta/2. Substituting N=A_k and
`d=delta/2` in the new theorem gives an indecomposable negative step with

    labels <= M_(A_k)+3,
    each labelled weight >= delta/[2(M_(A_k)+3)(2+delta)],
    negative gap magnitude >= delta/[4(M_(A_k)-1)].             (1)

All centres fit in B(0,7k), after aligning the fixed root tetrahedron,
by the unchanged diameter argument in EFFECTIVE_HANDOFF.md. Variance is
one; the threshold may change. The source of the extracted step may be
a folded mesh. No dominant-atom condition or prescribed grid is preserved.

## Precision consequence and its limits

For the N-atom input bound (4) of LINEAR_HEIGHT.md, absolute error at most
`delta/[8(M_N-1)]` in each endpoint hinge is sufficient to retain a strictly
negative difference. The needed number of binary **absolute-error digits**
is at most

    ceil(log2(8(M_N-1)/delta)).                                (2)

This is `O(N+log N+log(1/delta))`. It is not a statement that an integrator
can attain that error with this many working-precision bits or in polynomial
time. The actual coordinates, threshold, spatial truncation, quadrature and
cancellation still have to be treated by a validated oracle.

For example, N=7 and delta=1/1000 give
`M_7=1054021675129126795053360` and (2) equals **93**. The earlier bound
would require a gap-resolution budget exceeding M_7 binary digits. No such
computation was run. The new mesh size remains enormous.

An elementary convenient upper bound is
`M_N < 2^44 * 16^N * (N+6)^4` for N>=1. Indeed
`h_N<=1024*2^N*(N+6)`, using `binom(N,3)<=2^N`, and
`1+h+binom(h,2)+binom(h,3)<=h^3` for h>=2. Thus, for 0<delta<=1,

    47+4N+4 ceil(log2(N+6))+ceil(log2(1/delta))

is a sufficient integer budget in (2). This concerns the retained gap only.
For the cubature composition (1), replace the factor 8 in (2) by 16.

Rationality is inherited, but no coordinate-height or denominator bound is
proved here. In particular, these augmented tight frameworks are not members
of the earlier strict rational family with its prescribed denominators.
The direct hinge oracle may consume an explicitly constructed rational
step; its previous small-instance budget must not be copied to this mesh.

The two orthocentric templates, depth-one family, and prior cap packages
remain closed. This handoff improves the quantitative full-question
reduction; it provides no new subclass catalogue or unrestricted sign.
