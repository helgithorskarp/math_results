# Point-transitive seven-point triple downsets: exact capped H classification

Authoring agent: **six-downset-3**, role **researcher**, 2026-09-30.
Status: exact computer-assisted finite result with written completeness,
kernel and product proofs. Author-checked; no independent-review,
formalization or historical-priority claim is made.

## Precisely quantified result

Let T be a nonempty collection of distinct triples of a seven-point set,
whose full point automorphism group acts transitively. Include the full
two-skeleton:

```
D(T) = {A subset of [7] : |A| <= 2} union T.
```

There are exactly **11** permutation classes, representing **3,181**
labelled triple collections. Every one has a supplied rational symmetric
matrix M, indexed by all members including the empty vertex, such that

```
M[A,B]=0 whenever A intersects B,       M 1=1,
L=(N-s)M+sI >= 0,                      M <= I,
rank L=N-7,                           rank(I-M)=N-1.
```

Here N=|D(T)| and s is its largest star size. The rank of L is maximal
among **all real H certificates** for that downset, whether capped or not.
The seven stars are its only maximum intersecting families. Entries may
be signed; the empty loop is retained. The theorem assumes point
transitivity, not just equal triple degrees.

| Triples | Common triple degree | N | s | Classes | Labelled collections | Rank L |
| ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| 7 | 3 | 36 | 10 | 2 | 390 | 29 |
| 14 | 6 | 43 | 13 | 3 | 1,200 | 36 |
| 21 | 9 | 50 | 16 | 3 | 1,200 | 43 |
| 28 | 12 | 57 | 19 | 2 | 390 | 50 |
| 35 | 15 | 64 | 22 | 1 | 1 | 57 |

For any nonempty finite mixed product of these factors on disjoint
supports, put N_product=product N_j, p=max_j(s_j/N_j), and let c count
the factors attaining p. Its rational capped tensor certificate has

```
s_product=p*N_product,
rank L_product=N_product-7c,
exactly 7c maximum intersecting families, all largest coordinate stars.
```

The rank is again maximal among all H certificates. If at least one
factor is the full rank-three truncation D_full={A subset of [7]:|A|<=3},
the fractional independence bound divided by the largest star is at
least **91/88**, despite exact capped H tightness. The base fractional
value 91/4 is already stated in the primary paper; the exact primal/dual
witnesses below reproduce it, and the projection argument supplies the
mixed-product lower bound. No exact fractional product optimum is claimed.

The rational matrices are encoded in
[POINT_TRANSITIVE_SEVEN_CERTIFICATES.json](POINT_TRANSITIVE_SEVEN_CERTIFICATES.json).
The regenerated counts, ranks and exact matrix/polynomial hashes are in
[POINT_TRANSITIVE_SEVEN_RESULTS.json](POINT_TRANSITIVE_SEVEN_RESULTS.json).

## Completeness of the finite domain

Let G=Aut(T). Transitivity on seven points makes 7 divide |G| by the
orbit-stabilizer theorem. Cauchy's theorem gives an element of order seven.
An order-seven permutation of seven points is a seven-cycle. Relabel the
points to make this cycle the shift i -> i+1 modulo seven.

Every triple orbit of the shift has size seven: a triple fixed by a
nonidentity power would be fixed by the whole shift, whose only invariant
subsets are the empty and full sets. Thus the 35 triples form five orbits.
T is a nonempty union of these orbits, so the **31** nonempty unions
represent every point-transitive class. Conversely each such union has a
transitive seven-cycle in its automorphism group. The full two-skeleton
does not change this automorphism group.

[point_transitive_seven.py](point_transitive_seven.py) regenerates those five
orbits directly and compares them to another description by positive cyclic
gaps a,b,c with a+b+c=7. The latter uses all seeds {0,a,a+b} and their seven
translations. Every cyclic triple has such a seed; repeated gap descriptions
are removed only by equality of the resulting literal orbits.

Number the 35 triples by ascending binary subset mask and encode T by a
35-bit word. For each of the 31 candidates the checker computes all its
images under **every permutation in S7** and takes their minimum. The 11
distinct minima have disjoint labelled orbits. Their union contains 3,181
words. Their automorphism groups are independently the full stabilizers
among all 5,040 permutations, and each stabilizer order times its labelled
orbit size is 5,040. Each point's orbit is checked to be all seven points.

A second labelled-domain enumeration uses all **120 order-seven cyclic
subgroups of S7**. Write a seven-cycle uniquely as (0,a1,...,a6), giving
720 cycles, and identify a subgroup by its six nonidentity powers. For each
subgroup enumerate all 31 nonempty unions of its triple orbits. This avoids
canonical representatives and full-group image orbits. Its labelled set
must agree **entry by entry** with the first enumeration, not just in
cardinality. Their sorted-word compact-JSON SHA-256 is

```
cd00edd6f2ce5113fd34dda6b4af2bfb10119e885c33d5df115f17ef34854a47
```

The certificate class words and literal triples must match the regenerated
canonical domain exactly once. No external catalogue, numerical search or
private enumeration dump is an input to the verification.

## Matrix decoding and exact positivity

Let F=D(T) without the empty member, m=N-1, and E=[-1^T;I_m]. For each
class, the fixture lists representatives of unordered disjoint nonempty
pairs and their **actual C-entry values** as rational strings. Apply every
element of the freshly computed full automorphism group to each
representative. The resulting pair orbits must be disjoint and exhaust
every allowed pair. Set

```
C[A,A]=s-1,
C[A,B]=-1 for distinct intersecting nonempty members,
C[A,B]=the fixture value on each disjoint-pair orbit.
```

Define, with J an all-ones matrix of the indicated dimension,

```
L=J_N+E C E^T,       M=(L-sI)/(N-s),
U=N I_m-J_m-C.
```

Since E^T 1=0, L1=N1. The prescribed nonempty entries give precisely the
required diagonal and intersection support. Moreover

```
N I_N-L=E U E^T.
```

Thus C>=0 proves H, and U>=0 proves M<=I. This lift and cap criterion are
prior mechanisms from six-downset-1's
[structural proof](https://github.com/helgithorskarp/math_results/blob/main/spectral_downsets_structural_certificates/PROOF.md),
first published at source commit `9ca5a784c01d9307d365fd513911013ecce5b8d8`.
The new finite input is the complete seven-point cohort of rational cores.

Every C and U is scaled by its positive common denominator. Two different
exact positivity routes are required:

1. Integer fraction-free Schur elimination has positive nonzero pivots,
   exact divisions and zero residual rows at every zero pivot. At each
   stage the residual is a positive scalar times the ordinary Schur
   complement; splitting a positive pivot is a congruence. The number of
   positive pivots is the rank. This is the same congruence criterion used
   in [nine_point_exceptions.py](nine_point_exceptions.py).
2. Integer Faddeev--LeVerrier regenerates det(xI-A), checking every trace
   divisibility and the final Cayley--Hamilton residual. For its
   coefficients a_j, it checks (-1)^j*a_j>=0. Then det(tI+A) has
   nonnegative coefficients and positive leading coefficient, hence is
   positive for every t>0. A negative eigenvalue would give a positive
   root of that polynomial. Symmetry makes the eigenvalues real, so A
   is PSD. The trailing zero coefficients give the nullity and must
   reproduce the Schur rank. The published integer implementation is in
   [verify.py](verify.py).

Both routes give, for all 11 cases,

```
rank C=N-8,       U positive definite with rank N-1.
```

The checker separately verifies the definition of the downset, every
actual star size, symmetry, all support entries, exact row sums, all seven
centered-star kernel equations and their independence. Matrix and
characteristic-polynomial hashes are recorded. Eight negative, asymmetric
or damaged-orbit controls are rejected, while four positive/singular rank
controls pass. All guards survive Python -O.

E has independent columns spanning 1^perp, so the two summands of L have
orthogonal ranges and rank L=1+rank C=N-7. U positive definite makes
rank(NI-L)=N-1. Equivalently, with rho=s/(N-s)<1,

```
spectrum(M) subset [-rho,1],
multiplicity(-rho)=7,       multiplicity(1)=1,
every eigenvalue other than 1 has absolute value strictly less than 1.
```

The two exact algorithms corroborate positivity; they are not independent
peer reviews or proof-assistant formalizations.

## Why the ranks are maximal and classify equality

Apply the kernel lemma proved in
[REGULAR_SIX_PROOF.md](REGULAR_SIX_PROOF.md). For completeness, for any H
matrix on a downset, an intersecting indicator x of size a satisfies

```
(x-(a/N)1)^T L (x-(a/N)1)=a(s-a)>=0.
```

Support gives x^T L x=sa and L1=N1 gives the equality. Hence a<=s.
At a=s, PSD puts the centered indicator in ker L. The centered indicators
of every largest coordinate star are independent: a linear dependence
evaluated at the empty vertex makes the coefficient sum zero; evaluation
at each associated singleton then makes each coefficient zero.

There are seven largest stars here, so any H matrix has rank L<=N-7.
Our cores attain it. Consequently those seven centered stars span ker L.
For any maximum intersecting family I, write

```
1_I-(s/N)1 = sum_i b_i (1_star_i-(s/N)1).
```

I excludes the empty vertex, so evaluation there gives sum_i b_i=1.
Evaluation at each singleton gives b_i=1_I({i}), an element of {0,1}.
Exactly one coefficient equals one, and I is that star. This argument
requires no upper cap and proves maximality among uncapped certificates too.

The classical rank-three EKR and equality context is prior:
[Czabarka--Hurlbert--Kamat, Theorem 1.4, arXiv:1703.00494](https://arxiv.org/pdf/1703.00494).
The contribution here is exact capped spectral rank attainment over a
complete cohort; the kernel argument recovers the classical base equality
conclusion rather than claiming it as historically new.

## Every finite mixed product

Let M_product=tensor_j M_j. Symmetry and row sums multiply. If two product
members intersect, at least one factor pair intersects, making its factor
entry and the tensor entry zero. A coordinate star from factor j has size
(s_j/N_j)*N_product. Let rho_j=(s_j/N_j)/(1-s_j/N_j), and let rho=max rho_j.
Every tensor eigenvalue is a product of factor eigenvalues.

A negative product has a negative factor of magnitude at most rho and
all remaining factors have magnitude at most one. Hence it is at least
-rho, while all positive products are at most one. This proves both
H and the upper cap at the actual largest star size.

To attain -rho, exactly one factor must contribute its lower endpoint
-rho_j=-rho; every other factor must contribute its simple unit
eigenvalue. Any additional nonunit factor has absolute value strictly
below one and would strictly reduce the product magnitude. Thus the
lower endpoint has multiplicity 7c. There are exactly 7c largest
coordinate stars, so the same kernel lemma proves the product rank is
maximal and that these stars are all maximum families. Arbitrarily large
tensors are not generated; this is a written spectral consequence of the
exact finite certificates and the prior conditional tensor rule.

## Exact fractional baseline and mixed separation

For D_full with the empty vertex deleted, set

```
x(A)=(|A|-1)/4 for nonempty A.
```

The weights on singletons, pairs and triples are 0,1/4,1/2, giving total
21/4+35/2=91/4. For a disjoint collection of k nonempty members, its weight
is (sum |A|-k)/4. For k=1 it is at most 1/2; for k=2 at most (6-2)/4=1;
for k>=3 at most (7-k)/4<=1. This proves fractional-dual feasibility.

A matching fractional clique cover uses all 105 partitions into blocks
of sizes 3,2,2 with coefficient 1/10, and all 70 partitions of sizes
3,3,1 with coefficient 7/40. Each pair occurs in ten partitions of the
first type, each triple in three of the first and four of the second,
and each singleton in ten of the second. Coverage is therefore 1 for
pairs/triples and 7/4 for singletons. The cover cost is

```
105/10+70*(7/40)=91/4.
```

Weak duality proves the exact base value 91/4, agreeing with the already
published primary example. The checker regenerates all small-block
partitions by choosing the block containing the smallest remaining point,
then recursing, giving all 652 partitions. Every disjoint collection extends to such a partition
by adding uncovered singletons. It checks all these dual inequalities,
all 175 positive cover cliques, every vertex coverage and matching costs.

Now take a mixed product containing a D_full factor. Give each product
member its projected base weight from that factor. Nonempty projections
of any disjoint product collection are distinct and pairwise disjoint;
repeated empty projections have weight zero. Thus the projection is a
feasible fractional dual. Each base member has N_product/64 preimages,
so the total is (91/256)*N_product.

Writing |T|=7t for t=1,...,5, every cohort density equals
(7+3t)/(29+7t), an increasing function of t whose maximum is
22/64=11/32. Therefore

```
fractional_bound/s_product >= (91/256)/(11/32)=91/88>1.
```

The presence of a D_full factor actually attains that maximum star density.
This proves the claimed separation for all such finite mixed products.

## Reproduction, attribution and limits

From the authorized repository root, CPython 3.11+ and standard library only:

~~~sh
OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1 MKL_NUM_THREADS=1 python3 -O spectral_downset_six_exact/point_transitive_seven.py --check spectral_downset_six_exact/POINT_TRANSITIVE_SEVEN_RESULTS.json
~~~

The literal orbit fixture is 25,667 bytes. No numerical optimizer or
omitted classification input is needed. Floating alternating projections
were used privately to find candidates; only the rational fixture and
regenerated exact checks are proof inputs. Exact arithmetic and the short
published algorithms, plus the ordinary written mathematical bridges,
remain the trust boundary.

A measured final complete local check took 42.84 seconds and peaked at 30,016 KiB
RSS with one CPU job and all native thread settings one. These are
measurements, not runtime guarantees.

The Fano class (canonical word 1241792641, N=36,s=10, automorphism order
168) is an already established STS(7) case. Its capped maximal-rank
existence and products follow from six-downset-2's all-orders
[Steiner refinement](https://github.com/helgithorskarp/math_results/blob/main/spectral_downsets_steiner_triples/MAXRANK_PROOF.md),
source commit `b2182e5b6fc53001dff7e6d1dde9aa541fb704d2`, and also from
the attributed sparse trade in [KERNEL_TRADE_PROOF.md](KERNEL_TRADE_PROOF.md).
The earlier centered STS matrix has rank N-8, whereas the repaired matrix
has rank N-7. Our new fixture supplies another certificate for this
known baseline; the additional ten classes and complete quantified
seven-point coverage are the campaign increment. The six-point regular
classification and the two nine-point exceptional domains are distinct
cohorts, not completeness inputs here.

The prior sparse-trade mechanism has an independent
[review and refinement by six-reviewer-1](https://github.com/helgithorskarp/math_results/blob/main/spectral_downset_sparse_trade_review1/REVIEW.md),
source commit `671b4b28ea840200520f25b2731e4c468f170f81`. That review
does not review the present seven-point matrices or the newer nine-point
addition. The present result remains author-checked.

Primary target and status refreshed live on 2026-09-30:
[Ellis--Filmus--Friedgut, Section 4, arXiv:2609.28404v1](https://arxiv.org/html/2609.28404v1#S4).
Its [current arXiv record](https://arxiv.org/abs/2609.28404) still lists
only v1; general H and I remain open. Section 4 already supplies the
fractional 91/4 example and the spectral conjectures. Neither our finite
cohort nor its products resolves general H or I. No historical priority
claim is made for the group census, classical EKR, or that fractional value.
