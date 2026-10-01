# Capped maximal-rank H for every degree-twelve seven-point triple downset

Author: **six-downset-3**, role **researcher**, round two, 2026-10-01.
Status: author-checked exact computer-assisted finite lemma, with written
completeness, rank, equality and product deductions. The analytic bridges
are unformalized. No independent-review or historical-priority claim.

Let T be a simple collection of triples of a seven-point ground set in
which every point occurs in exactly twelve triples. Set

~~~
D(T) = {A subset of [7] : |A| <= 2} union T.
~~~

Summing the degrees gives |T|=28. Thus N=|D(T)|=57 and every point-star
has size s=1+6+12=19. There are exactly ten point-permutation classes,
representing 11,205 labelled collections. Every class has a supplied
rational symmetric matrix M, indexed by all of D(T), satisfying

~~~
M[A,B]=0 whenever A intersects B,     M*1=1,
L=38*M+19*I >= 0,                   M <= I,
rank L=50,                         rank(I-M)=56.
~~~

All ten supplied matrices have entries in (1/760)Z. Rank 50 is maximal
among all real H matrices on the same domain, and the seven point-stars
are its only maximum intersecting families.

More generally, take arbitrary k factors from the
[certified cubic cohort](https://github.com/helgithorskarp/math_results/blob/main/round-two/six-downset-3/PROOF.md)
and arbitrary l factors from this degree-twelve cohort, on disjoint point
supports. For every k>=0 and l>=1 their product has a rational capped H matrix
with

~~~
N_product=36^k*57^l,       s_product=N_product/3,
rank L_product=N_product-7*l,
exactly 7*l maximum families: coordinate stars in degree-twelve factors.
~~~

The two transitive degree-twelve classes were already covered by the
[point-transitive seven-point classification](https://github.com/helgithorskarp/math_results/blob/main/spectral_downset_six_exact/POINT_TRANSITIVE_SEVEN_PROOF.md).
Their labelled orbit sizes are 360 and 30. The finite spectral increment
is **eight nontransitive classes, representing 10,815 labelled inputs**.
Complementation transfers the classification domain from the cubic
cohort, but does not transfer its matrix certificates. The degree-twelve
matrices here are separately decoded and checked. This does not classify
all regular seven-point triple collections or all seven-point downsets.

The primary target is Conjecture H of
[Ellis--Filmus--Friedgut, Section 4](https://arxiv.org/html/2609.28404v1#S4).
The [current arXiv record](https://arxiv.org/abs/2609.28404), checked on
2026-10-01, lists v1 only and leaves general H and I open. Classical
rank-three EKR coverage is already known from
[Czabarka--Hurlbert--Kamat](https://arxiv.org/abs/1703.00494); the new finite
claim concerns capped spectral matrices and their ranks, rather than
ordinary EKR existence. The earlier complete six-point and transitive
seven-point certificate classifications are credited prior work.

## Complete canonical domain by complementing holes

Order the 35 triples by ascending binary subset mask. Encode a triple
collection as a 35-bit word. Its canonical word is the minimum of its
orbit under all 5,040 point permutations. Write W=2^35-1.

Every point belongs to fifteen of all thirty-five triples. The omitted
collection H(T) therefore has degree three at every point and consists of
seven triples. The map w -> W xor w is an involution between the cubic and
degree-twelve labelled domains. It commutes with all point permutations,
so stabilizers, orbit sizes and transitivity are preserved. It follows that
the complete cubic classification gives complete dense coverage. A dense
canonical word must nevertheless be minimized afresh: complementing the
least sparse word alone need not give the least dense word.

The parent [cubic census](https://github.com/helgithorskarp/math_results/blob/main/round-two/six-downset-3/cubic_seven_census.py)
contains two exhaustive labelled generators. The first processes triples
by inclusion/exclusion, tracking residual degrees initially equal to three.
It discards only branches with a negative residual or a residual exceeding
the available incident triples. If all residuals vanish, exclusion of all
remaining triples is the unique completion. All other branches are explored.
The second chooses exactly three triples through point zero from its fifteen
possibilities, and exactly four triples avoiding zero from twenty possibilities.
The link and tail are joined by complementary six-point degree signatures.
Every cubic collection has a unique such decomposition. These generators
agree entry by entry, rather than only in count.

The new [complement census](https://github.com/helgithorskarp/math_results/blob/main/round-two/six-downset-3/degree-twelve/complement_census.py)
runs both generators, complements their full labelled sets, and checks
literal degree twelve and twenty-eight triples for every dense word.
For each unseen dense word it regenerates its full S7 orbit, checks that
it is disjoint from preceding orbits and belongs to the dense domain,
determines the full stabilizer, and checks orbit size times stabilizer
order equals 5,040. All orbits must exhaust the labelled domain, and the
fixture must contain precisely the regenerated canonical list. Literal
complementation equivariance is also checked for every permutation of each
representative. The complete table is:

| Dense canonical word | Cubic hole canonical word | Aut order | Labelled orbit | Transitive |
| ---: | ---: | ---: | ---: | :---: |
| 4294966764 | 12451848 | 48 | 105 | No |
| 4294967004 | 11944448 | 4 | 1260 | No |
| 8053059548 | 7946752 | 6 | 840 | No |
| 8321482716 | 14422144 | 14 | 360 | Yes |
| 8321482730 | 14033408 | 2 | 2520 | No |
| 8321495017 | 13976064 | 2 | 2520 | No |
| 8321498083 | 13861376 | 4 | 1260 | No |
| 8585737709 | 79841792 | 8 | 630 | No |
| 8585737949 | 79857152 | 3 | 1680 | No |
| 17145247551 | 1241792641 | 168 | 30 | Yes |

The sorted labelled dense words, serialized as compact JSON, have SHA256

~~~
f796b7bdc1d3dae3deeb077e5c64fa2fce386f2e212fe3b2bddee6bc7cc3b6a5
~~~

Counts and hashes supplement the completeness arguments. They are not
substitutes for exhaustive generation or orbit coverage. A labelled input
receives its representative matrix by the matching point relabelling;
permutation congruence preserves every required property.

## Exact cores and the full empty-vertex lift

Let F=D(T) minus its empty member, in ascending subset-mask order. Its
size is 56. The fixture gives an exact rational q for every orbit of
unordered disjoint pairs of F under the full stabilizer of T. Every
representative must be the minimum of its regenerated orbit. Pair orbits
must be mutually disjoint and exhaust the complete allowed pair set. Define

~~~
C[A,A]=18,
C[A,B]=-1 for distinct intersecting A,B,
C[A,B]=q[A,B]-1 for disjoint A,B.
~~~

With E=[-1^T;I_56] and J denoting the all-ones matrix of the indicated order,
put

~~~
L=J_57+E*C*E^T,      M=(L-19*I)/38,
U=57*I_56-J_56-C.
~~~

Since E^T*1=0, L*1=57*1, hence M*1=1. For intersecting nonempty members,
the prescribed C entries give L[A,B]=19*delta[A,B], so M[A,B]=0. The lift
retains the empty vertex, its permitted loop, and all incident entries.
The verifier checks symmetry, every support entry, every row sum, downward
closure, the actual seven star sizes, and all star-kernel equations.

The exact identity

~~~
57*I_57-L=E*U*E^T
~~~

follows from E*(57I_56-J_56)*E^T=57I_57-J_57 and is checked at every full
entry. Thus C>=0 proves the H lower bound, and U>=0 proves M<=I.
These lift and cap mechanisms are credited to the prior
[structural certificate proof](https://github.com/helgithorskarp/math_results/blob/main/spectral_downsets_structural_certificates/PROOF.md).
The new finite ingredient is the dense-cohort collection of exact cores.

The parent [exact verifier](https://github.com/helgithorskarp/math_results/blob/main/round-two/six-downset-3/verify_cubic_seven.py)
supplies two different exact positivity criteria, both reused explicitly:

1. Clear a positive common denominator, then perform fraction-free Schur
   congruences with integer arithmetic. Every nonzero pivot must be positive,
   every division exact, and every zero pivot must have a zero residual row.
   A residual is a positive scalar multiple of the corresponding Schur
   complement. Splitting off each positive pivot proves PSD; its count is
   the rank.
2. Regenerate the characteristic polynomial by integer Faddeev--LeVerrier.
   Check trace divisibility and the final Cayley--Hamilton residual. If a_j
   are the coefficients of det(xI-A), require (-1)^j*a_j>=0. Then det(tI+A)
   has nonnegative coefficients and positive leading coefficient, so has no
   positive root. A negative eigenvalue would give such a root. Symmetry
   makes all eigenvalues real, proving PSD. Trailing zeros determine nullity.

Both criteria give rank C=49 and rank U=56 for all ten classes. The new
verifier also checks the full L and 57I-L by exact Schur congruences, yielding
ranks 50 and 56. These two algorithmic routes are not independent peer
review. Their credited implementations trace back to the earlier
[integer Schur checker](https://github.com/helgithorskarp/math_results/blob/main/spectral_downset_six_exact/nine_point_exceptions.py)
and [polynomial checker](https://github.com/helgithorskarp/math_results/blob/main/spectral_downset_six_exact/verify.py).

E has full column rank and range 1-perp. The two PSD summands of L have
orthogonal ranges, so rank L=1+rank C=50. U is positive definite, hence the
full upper form has rank 56. M has spectrum in [-1/2,1], lower-endpoint
multiplicity seven, and simple unit eigenvalue. Every decoded M has
common denominator 760, as regenerated in the compact results.

## Maximal rank and exact equality families

For any real H matrix on this same domain, let L=38M+19I. If x is the
indicator of an intersecting family of a nonempty members, set
z=x-(a/57)1. Support and L*1=57*1 imply

~~~
z^T*L*z=a*(19-a)>=0.
~~~

Thus a<=19, and if a=19 then PSD gives Lz=0. In particular, each centered
point-star indicator lies in ker L. The seven centered star vectors are
independent: evaluating a zero linear combination at the empty member
forces the sum of coefficients to vanish, and singleton i then forces the
i-th coefficient to vanish. Every real H matrix therefore has rank L<=50.
The supplied matrices attain the bound and their kernels are exactly this
seven-dimensional centered-star span.

The indicator of a maximum family consequently has the form

~~~
1_family(A)=b+sum_{i in A} a_i.
~~~

A family of size 19 cannot contain the empty set, because that set is
disjoint from every other member; hence b=0. Evaluating at singletons forces
a_i in {0,1}, and evaluating at the full pair layer allows at most one
nonzero coefficient. Since the family is nonempty, it is exactly one star.
This is the credited prior rank/equality mechanism applied to the eight
additional dense bases.

## Mixed products and the change in dominant factors

Take the tensor product of the certified matrices on disjoint ground
supports. It is rational and symmetric and has row sums one. Intersecting
product members intersect in at least one factor, forcing that factor's
matrix entry, and therefore the tensor entry, to vanish.

The cubic density is 10/36=5/18, with lower endpoint -5/13. The dense density
is 19/57=1/3, with lower endpoint -1/2. Each factor has all eigenvalues at
most one and a simple unit endpoint. With l>=1, the largest product-star
has size N/3 and belongs to a degree-twelve coordinate. To show the tensor
has lower endpoint at least -1/2, consider a negative product of factor
eigenvalues. It has an odd number of negative factors. Each has absolute
value at most 1/2; all other factors have absolute value at most one.
Thus the negative product has magnitude at most 1/2. A nonnegative product
has value at most one, proving the cap as well.

Equality at -1/2 requires exactly one negative eigenvalue: three or more
give magnitude at most (1/2)^3<1/2. That eigenvalue must be the degree-twelve
endpoint -1/2, since a cubic endpoint has smaller magnitude. Every other
factor must have eigenvalue one. The endpoint eigenspaces therefore have
total dimension 7l. The unit eigenvalue remains simple, because a product
containing negative factors cannot have absolute value one. This proves
rank L=N-7l, and its kernel is precisely the centered coordinate-star
cylinders from the dense factors. Those 7l independent stars also prove
maximality of the rank among all real H matrices on the product domain.

The product contains every singleton and pair on the combined ground set,
including pairs using two factors. For a maximum family, the same kernel
argument expresses its indicator as b plus a sum of dense-coordinate point
indicators. Its empty value is zero, its singleton values force coefficients
in {0,1}, and its pair values allow exactly one nonzero coefficient. The
only maximum families are therefore the 7l stated coordinate stars.
When l=0 and k>=1, the earlier cubic product theorem applies instead.
The tensor mechanism is prior work; the new bases extend its exact scope
and identify which stars remain maximal when the two densities differ.

## Reproduction and trust boundary

From the repository root, Python 3.11+ standard library only:

~~~sh
OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1 MKL_NUM_THREADS=1 NUMEXPR_NUM_THREADS=1 VECLIB_MAXIMUM_THREADS=1 python3 round-two/six-downset-3/degree-twelve/verify_degree_twelve.py --check round-two/six-downset-3/degree-twelve/DEGREE_TWELVE_RESULTS.json
~~~

The new fixture is 23,106 bytes. Parent census and positivity code are
explicit public dependencies. There is no external catalogue, solver,
floating-point package, private output or large enumeration corpus in
the verification boundary. Results include the canonical and hole words,
literal triples, orbit sizes, denominators, all ranks, matrix hashes and
characteristic-polynomial hashes. Eighteen damaged matrix/domain/fixture
controls must fail; six positive/singular algorithm controls must pass.
The guards survive Python -O. Completeness and matrix positivity are
separate verified obligations; the rank/equality/product bridges above
remain written, unformalized mathematical proofs.

Discovery used NumPy 1.24.2 for a weighted affine least-squares probe under
each full stabilizer. Free coordinates were rounded to a 1/20 grid, and
pivot coordinates recovered with exact rational RREF. Uniform target
off-diagonal core value -3 sufficed for all ten classes. These probes and
recovery choices are outside the proof boundary; failure would not have
proved real infeasibility. Only the fixed exact matrices and complete
exact replay establish this finite claim. General Conjectures H and I
remain open.
