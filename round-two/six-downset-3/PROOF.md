# Every cubic seven-point triple collection has a maximal-rank capped H matrix

Author: **six-downset-3**, role **researcher**, round two, 2026-10-01.
Status: exact computer-assisted finite result with written completeness,
rank, equality and product proofs. Author-checked, unformalized; no
independent-review or historical-priority claim.

Let T be any collection of distinct triples of a seven-point set such that
**every point belongs to exactly three triples**. Include the full two-skeleton:

~~~
D(T) = {A subset of [7] : |A| <= 2} union T.
~~~

Then T has seven triples, N=|D(T)|=36, and all seven stars have size s=10.
There are exactly ten point-permutation classes, representing 11,205 labelled
collections. Every class has a supplied rational symmetric matrix M, indexed
by all of D(T) including the empty vertex, satisfying

~~~
M[A,B]=0 when A intersects B,     M*1=1,
L=26*M+10*I >= 0,               M <= I,
rank L=29,                     rank(I-M)=35.
~~~

Rank 29 is maximal among **all real** H matrices on the same domain. Its
seven stars are its only maximum intersecting families. For every k>=1,
any choice of k factors from this cohort on disjoint point supports has a
rational capped H matrix with

~~~
N_product=36^k,           s_product=10*36^(k-1),
rank L_product=36^k-7*k,  exactly 7*k maximum families, all coordinate stars.
~~~

The two transitive classes, representing 390 labelled collections, are
already covered by the published
[point-transitive seven-point classification](https://github.com/helgithorskarp/math_results/blob/main/spectral_downset_six_exact/POINT_TRANSITIVE_SEVEN_PROOF.md).
The finite spectral increment removes point transitivity at common triple
degree three: **eight additional classes, representing 10,815 labelled
collections**. This does not classify all regular seven-point triple
collections or all seven-point downsets. The ordinary rank-three EKR theorem is
[already known](https://arxiv.org/abs/1703.00494); we make no classical EKR
novelty claim. The new claim is the capped spectral construction and maximal ranks.

The target is Conjecture H in
[Ellis--Filmus--Friedgut, Section 4](https://arxiv.org/html/2609.28404v1#S4).
The arXiv record checked on 2026-10-01 lists v1 only and leaves H and I open.
The classical Chvatal/projection-packing proofs do not supply H matrices.
The [complete six-element certificate census](https://github.com/helgithorskarp/math_results/blob/main/spectral_downset_six_exact/THEOREM.md)
is prior work. [Stephen--Yusun](https://arxiv.org/pdf/1209.4623) is historical
bounded-classification context, not an input to the new checker.

## Exhaustive labelled and canonical coverage

Number the 35 triples by ascending binary subset mask; point i is bit i,
for i=0,...,6. A collection is a 35-bit word. Its canonical word is the
minimum of its full S7 orbit.

The first generator processes these triples in order, exploring exclusion
and inclusion. Inclusion decrements exactly three point residual degrees,
initially all three. A branch is discarded only when a residual is negative
or exceeds the number of remaining triples incident with that point. These
are necessary conditions for completion. When every residual vanishes,
all later triples must be excluded, yielding the unique completion.
Every other branch is explored. Thus this generator is complete and has
no duplicates.

The second generator decomposes T at point zero. Exactly three selected
triples contain zero; exactly four avoid it, because summing degrees gives
21=3|T|. Enumerate all C(15,3)=455 possible three-edge links and all
C(20,4)=4,845 possible four-edge tails. Group tails by their degree vectors
on the other six points. A link with degree vector d is joined to precisely
the tails with degree vector (3,...,3)-d. This split is unique and exhaustive.
The verifier compares the two labelled sets **entry by entry**.

For each unseen word, apply every one of the 5,040 point permutations.
The resulting orbit must lie in the labelled domain and be disjoint from
earlier orbits. The least word must be the current representative. Its
full stabilizer is independently determined by literal equality under
those same permutations. Orbit size times stabilizer order must be 5,040.
The union of all ten orbits must equal the complete labelled domain, and
the certificate class list must equal the regenerated canonical list
exactly once. Transitivity is tested on the full stabilizer, rather than
inferred from equal degrees. A labelled input receives its canonical
class matrix by the corresponding point relabelling; permutation congruence
preserves support, row sums, PSD and ranks.

| Canonical word | Aut order | Labelled orbit | Transitive |
| ---: | ---: | ---: | :---: |
| 7946752 | 6 | 840 | No |
| 11944448 | 4 | 1260 | No |
| 12451848 | 48 | 105 | No |
| 13861376 | 4 | 1260 | No |
| 13976064 | 2 | 2520 | No |
| 14033408 | 2 | 2520 | No |
| 14422144 | 14 | 360 | Yes |
| 79841792 | 8 | 630 | No |
| 79857152 | 3 | 1680 | No |
| 1241792641 | 168 | 30 | Yes |

The sorted labelled word list, serialized as compact JSON, has SHA256

~~~
dfd1a50ac1b7b3ec8675cf9c10417a0a69564f09e4b9670e1cdaf42c8d7058c6
~~~

Counts and hashes are compact evidence. Completeness rests on the two
exhaustive generation arguments and full-orbit checks, rather than on a
count match alone.

## Exact cores, empty-vertex lift and positivity

Let F=D(T) without the empty member, in ascending subset-mask order.
The fixture supplies a rational value q for each orbit of unordered disjoint
pairs of F under the full point stabilizer. Representatives must be the
least pairs in their orbits. The verifier regenerates those orbits and
requires them to be disjoint and to exhaust all allowed pairs. Define

~~~
C[A,A]=9,
C[A,B]=-1 for distinct intersecting A,B,
C[A,B]=q[A,B]-1 for disjoint A,B.
~~~

Put E=[-1^T; I_35] and let J be the all-ones matrix of the indicated order:

~~~
L=J_36+E*C*E^T,       M=(L-10*I)/26,
U=36*I_35-J_35-C.
~~~

Because E^T*1=0, L*1=36*1 and M*1=1. The prescribed intersecting entries
and nonempty diagonals give the support requirement for M. The empty
vertex, its permitted loop, and every incident entry are retained by this
lift. The verifier checks all support entries, symmetry, row sums, downward
closure and actual star sizes directly from the full decoded matrix.

Furthermore 36I-L=E*U*E^T, checked at every full entry. Thus C>=0 proves H
and U>=0 proves M<=I. These are credited prior mechanisms from
[six-downset-1's structural certificate proof](https://github.com/helgithorskarp/math_results/blob/main/spectral_downsets_structural_certificates/PROOF.md).
The encoding and rank/equality strategy build on the published
[regular-six proof](https://github.com/helgithorskarp/math_results/blob/main/spectral_downset_six_exact/REGULAR_SIX_PROOF.md)
and point-transitive seven-point proof. The new finite input is the complete
cubic seven-point cohort of exact cores.

For every class, C is PSD of rank 28 and U is positive definite of rank 35.
Two exact algorithms separately establish these facts:

1. Clear a common positive denominator and use integer fraction-free Schur
   elimination. Every nonzero pivot must be positive, every division exact,
   and every zero pivot must have a zero residual row. The residual is a
   positive scalar times the ordinary Schur complement; each positive
   pivot splits off a positive one-dimensional form by congruence. The
   number of positive pivots is the rank.
2. Regenerate det(xI-A) by integer Faddeev--LeVerrier, checking trace
   divisibility and the final Cayley--Hamilton residual. For coefficients
   a_j require (-1)^j*a_j>=0. Then det(tI+A) has nonnegative coefficients
   and positive leading coefficient, hence no positive root. A negative
   eigenvalue would produce a positive root; symmetry makes all eigenvalues
   real, proving PSD. Trailing zero coefficients give the nullity and
   reproduce the Schur rank.

These are different exact positivity criteria, not independent peer review.
The standard algorithms follow the credited earlier
[integer Schur checker](https://github.com/helgithorskarp/math_results/blob/main/spectral_downset_six_exact/nine_point_exceptions.py)
and [polynomial checker](https://github.com/helgithorskarp/math_results/blob/main/spectral_downset_six_exact/verify.py).
The new verifier also checks both full forms L and 36I-L by Schur elimination,
all seven exact star-kernel equations, and the full upper-lift identity.

E has full column rank, with range 1-perp. The two summands in L have
orthogonal ranges, so rank L=1+rank C=29. Since U is positive definite,
36I-L has rank 35. M therefore has spectrum in [-5/13,1], lower-endpoint
multiplicity seven, and a simple unit endpoint.

## Maximal rank and equality families

For any real H matrix on the same domain, let L=26M+10I. An intersecting
family of a nonempty members has indicator x. Set z=x-(a/36)1. Support
and L*1=36*1 give z^T*L*z=a(10-a)>=0, so a<=10. If a=10, PSD implies
Lz=0. In particular, all seven centered star indicators lie in ker L.
They are independent: evaluation of a zero linear combination at the empty
member forces its coefficient sum to vanish; evaluation at singleton i
then forces its i-th coefficient to vanish. Thus every real H matrix has
rank L<=29. Our matrices attain this bound and their kernels are exactly
this seven-dimensional star span.

For any maximum family its indicator therefore has the form

~~~
1_family(A)=b+sum_{i in A} a_i.
~~~

The empty vertex cannot belong to an intersecting family because it is
disjoint from itself, hence b=0. Singleton values force each a_i to be
zero or one. Since every pair belongs to D(T), at most one a_i is one.
The maximum family is nonempty, so it is exactly one coordinate star.
This is the credited prior kernel mechanism applied to the eight new bases.

## All finite products

Use M_product=M_1 tensor ... tensor M_k for arbitrary certified factors.
It is rational and symmetric, with row sums one. Intersecting product
members intersect in some coordinate factor where the matrix entry is zero,
so support is preserved. Its largest star has size 10*36^(k-1), giving the
same target spectral endpoint -5/13.

Each factor eigenvalue belongs to [-5/13,1]. A negative product has an odd
number of negative factors, so its magnitude is at most 5/13. Positive
products are at most one. Equality at the negative endpoint is possible
precisely when one factor is at -5/13 and every other factor is at its simple
eigenvalue one. Three or more negative factors have strictly smaller
magnitude, as does any product containing another positive eigenvalue below
one. Hence the lower endpoint multiplicity is 7k and the unit endpoint
remains simple. This proves the stated rank and cap for every k.

The centered coordinate-star cylinders form the product kernel. The same
indicator argument applies on the 7k-point ground set: the product domain
contains every singleton and every pair, including pairs in different
factors. Its only maximum families are the 7k coordinate stars. The tensor
mechanism is prior work; the new finite bases extend its certified scope.

## Reproduction and trust boundary

From the repository root, Python 3.11+ standard library only:

~~~sh
OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1 MKL_NUM_THREADS=1 NUMEXPR_NUM_THREADS=1 VECLIB_MAXIMUM_THREADS=1 python3 round-two/six-downset-3/verify_cubic_seven.py --check round-two/six-downset-3/CUBIC_SEVEN_RESULTS.json
~~~

The fixed exact fixture is 13,640 bytes. No external catalogue, solver,
floating-point library, private output, or omitted enumeration corpus is
needed. The compact results give all class words, orbit sizes, denominators,
ranks, matrix hashes and polynomial hashes. Eighteen damaged matrix/domain/
fixture controls must fail, and six positive/singular algorithm controls
must pass. Guards survive Python -O.

Discovery used NumPy 1.24.2 least squares for the exact affine star-kernel
system under each full stabilizer. Free coordinates were rounded to a 1/20
grid; pivot coordinates were recovered with rational RREF. Floating discovery
is outside the proof boundary. Failure of this recovery would not show real
infeasibility. The evidence is the fixed exact matrices, complete enumeration,
exact checker and written linear-algebra/product bridges. Those bridges are
unformalized; source publication and hashes do not replace them. General
Conjectures H and I remain open.
