# Regular triple downsets on six points: capped certificates and extremizers

Authoring agent: **six-downset-3**, role **researcher**, 2026-09-30.
Status: exact computer-assisted finite classification, with written proofs
of the kernel, product, and separation consequences. No formalization,
independent review, or historical priority claim is made.

## Scope and theorem

Let T be a nonempty collection of distinct triples of [6], with every point
in exactly d triples. Define

```
D(T) = {A subset of [6] : |A| <= 2} union T.
```

Thus d is an integer from 1 to 10, |T|=2d, N=|D(T)|=22+2d, and every
coordinate star has size s=6+d. Up to permutations of the six points there
are **34** such downsets, representing **3,435** labeled triple collections;
14 classes are vertex transitive. Every class has an explicitly supplied
rational symmetric matrix M with

```
M[A,B]=0 if A intersects B,     M 1=1,
L=(N-s)M+sI >= 0,             M <= I,
rank L=N-6,                  rank(I-M)=N-1.
```

The empty vertex and its allowed loop are retained; signed entries are
allowed. The rank of L is maximal among all H certificates for D(T).
The six coordinate stars are the **only** maximum intersecting families.
The theorem concerns regular triple collections with the full two-skeleton;
it does not assert the upper cap for every six-point downset.

The certificate domain is given by
[REGULAR_SIX_CERTIFICATES.json](REGULAR_SIX_CERTIFICATES.json), and all
computed counts, ranks, and matrix hashes by
[REGULAR_SIX_RESULTS.json](REGULAR_SIX_RESULTS.json). Its degree counts are:

| Common triple degree d | Permutation classes | Labeled collections |
| ---: | ---: | ---: |
| 1 | 1 | 10 |
| 2 | 2 | 75 |
| 3 | 4 | 330 |
| 4 | 6 | 780 |
| 5 | 7 | 1,044 |
| 6 | 6 | 780 |
| 7 | 4 | 330 |
| 8 | 2 | 75 |
| 9 | 1 | 10 |
| 10 | 1 | 1 |

More generally, choose any k>=1 such factors on pairwise disjoint supports.
Put N_product=product_j N_j, p_j=s_j/N_j, p=max_j p_j, and let c be the
number of factors attaining p. Their product downset has largest star
size s_product=N_product*p and a rational capped H certificate with

```
rank L_product = N_product-6c.
```

This is again the largest possible rank. Its **only** maximum intersecting
families are its 6c largest coordinate stars. For k copies of a single
factor the rank is N^k-6k and there are exactly 6k maximum families.
This includes the fractional exception D_* from [CAP_THEOREM.md](CAP_THEOREM.md).

## Complete finite enumeration

[regular_six.py](regular_six.py) generates the domain in two different ways
and compares the resulting labeled sets entry by entry.

First, number the 20 triples by ascending binary subset mask. The reflected
Gray code g(t)=t xor (t>>1), for 0<=t<2^20, is a bijection on 20-bit words:
the inverse recovers each binary digit by the xor of the Gray digits above
it and itself. Consecutive words differ in the bit numbered by the trailing
zero count of t. Toggling this bit updates exactly three point degrees.
The program keeps every nonempty word whose six degrees agree.

Second, for each d=1,...,10, an include/exclude recursion processes the same
20 triples, starting with six remaining degrees equal to d. A branch is
discarded only if a remaining degree is negative or exceeds the number of
unprocessed triples containing that point. These conditions are necessary
for completion. Once all remaining degrees are zero, every subsequent
triple must be excluded, giving one unique completion. All other branches
are explored. This independently generates the same 3,435 labeled words,
without duplicates.

The first generator computes every orbit under all 720 permutations in
S_6 and uses the least word as representative. Distinct representatives
have disjoint orbits. Their actual relabelings reconstruct the entire
labeled domain, and each orbit size times its automorphism order equals
720. The 34 certificate family masks must equal the independently
enumerated canonical domain exactly once. No previous census dump or
external classification table is an input.

## Rational orbit certificates and the two PSD checks

Let F=D(T) minus the empty set, let J denote an all-ones matrix of the
indicated dimension, and put E=[-1^T; I_(N-1)]. For each certificate, the
verifier enumerates Aut(D(T)) independently through all 720 permutations.
Its listed unordered disjoint-pair orbits must be disjoint and must exhaust
every allowed nonempty pair. On such an orbit the listed rational value
q specifies C[A,B]=q-1. Prescribe the other entries by

```
C[A,A]=s-1,
C[A,B]=-1 on distinct intersecting nonempty pairs.
```

Define

```
L=J_N+E C E^T,       M=(L-sI)/(N-s),
U=N I_(N-1)-J_(N-1)-C.
```

Then L1=N1, and the prescribed entries imply the required disjointness
support for M. Furthermore

```
N I_N-L=E U E^T.
```

Consequently C>=0 proves H, and U>=0 proves M<=I. These empty-vertex lift,
upper-cap, and conditional tensor mechanisms are credited to
six-downset-1's
[structural proof, Sections 2 and 5](https://github.com/helgithorskarp/math_results/blob/main/spectral_downsets_structural_certificates/PROOF.md),
first published at source commit `9ca5a784c01d9307d365fd513911013ecce5b8d8`;
the refreshed source revision is `3e9db97a7d3ed0d1fc2bc5b5451cd2c750c82265`.
The new finite contribution supplies a maximal-rank capped certificate for
every class in the stated cohort, rather than assuming capped factors.

The verifier scales C and U by a common positive denominator. Every
scaled matrix passes both of the following exact checks. Rational Schur
elimination has positive nonzero pivots, and every zero pivot has a zero
remaining row. Independently, integer Faddeev--LeVerrier computes the full
characteristic polynomial, checks trace divisibility at every step, and
checks the final Cayley--Hamilton residual. For coefficients a_k in

```
det(xI-A)=sum_(k=0)^m a_k x^(m-k),     a_0=1,
```

the verifier checks (-1)^k*a_k>=0. Substitution x=-t, t>0, then gives
(-1)^m times a polynomial with nonnegative coefficients and positive
leading coefficient, so there is no negative root. Symmetry makes all
eigenvalues real, proving PSD. The trailing zero coefficients give the
zero-eigenvalue multiplicity and independently reproduce the Schur rank.
For all 34 cases the results are

```
rank C=N-7,     U positive definite with rank N-1.
```

The characteristic polynomials are regenerated, with their exact hashes
recorded in the compact results. The code also checks each maximum-star
kernel equation C x_star=0 and checks symmetry, support, row sums, and the
full upper congruence entry by entry. It reduces each matrix M to an integer
numerator and denominator and records the numerator's compact-JSON SHA-256.

The columns of E have full rank and span 1^perp. Thus the two summands of
L have orthogonal ranges, giving rank L=1+rank C=N-6. Since U is positive
definite, N I-L has rank N-1. Equivalently, with rho=s/(N-s)<1,

```
spectrum(M) subset [-rho,1],
multiplicity(-rho)=6,     multiplicity(1)=1.
```

All eigenvalues other than 1 have absolute value strictly less than 1.

## A maximal-rank H certificate determines every extremizer

The following elementary lemma explains why the computed ranks give a
classification of maximum intersecting families, without their enumeration.

**Kernel lemma.** Let D be any nontrivial finite downset, with N=|D| and
largest star size s>0. Suppose it has an H certificate M, and let
L=(N-s)M+sI. Let r be the number of coordinate stars of size s, counting
only active coordinates. Then rank L<=N-r. If equality holds, those r
stars are the only maximum intersecting families of nonempty members of D.

**Proof.** For an intersecting family I of size a and indicator x, support
implies x^T L x=sa. Since L1=N1, the centered indicator
z=x-(a/N)1 satisfies

```
z^T L z=a(s-a)>=0.
```

Hence a<=s. At a=s, PSD implies Lz=0. In particular the centered
indicators z_i=x_i-(s/N)1 of all largest stars lie in ker L. They are
independent: evaluating sum_i b_i z_i=0 at the empty vertex gives
sum_i b_i=0, and evaluating at each corresponding singleton gives b_i=0.
This proves rank L<=N-r.

If rank L=N-r, those indicators span ker L. For any intersecting I of
size s, express x-(s/N)1=sum_i b_i z_i. At the empty vertex, x is zero,
so sum_i b_i=1. At each largest-star singleton, b_i=x({i}) belongs to
{0,1}. Exactly one coefficient is therefore 1 and the others are zero,
so x equals the corresponding star indicator. Every star itself has size
s, proving the assertion. This proof uses only the original H inequality;
an upper cap is unnecessary. QED.

For each of the 34 factors, r=6 and the certificate attains rank N-6.
The claimed finite extremizer classification follows immediately.

## Mixed products and their equality cases

Represent each member of the product downset as a tuple of factor members.
Take M_product to be the tensor product of their rational matrices. Its
row sums and symmetry multiply. If two product members intersect, some
factor pair intersects, so its factor matrix entry and the tensor entry
are zero. A coordinate star from factor j has size p_j*N_product.

Put rho_j=p_j/(1-p_j) and rho=max_j rho_j<1. Tensor eigenvalues are
products of factor eigenvalues. A negative product has at least one
negative factor, of magnitude at most rho, and every other factor has
magnitude at most one. All positive products are at most one. Thus

```
-rho I <= M_product <= I,
rho=s_product/(N_product-s_product).
```

This proves the capped H inequalities. To attain -rho, exactly one factor
must contribute its lower endpoint -rho_j=-rho, while every other factor
contributes 1: any additional nonunit factor has absolute value strictly
less than one and makes the product's magnitude strictly smaller. There
are c eligible factors, each with lower-endpoint multiplicity six; the unit
eigenspaces of all remaining factors are one dimensional. The lower
eigenspace therefore has dimension 6c, and rank L_product=N_product-6c.
Exactly the 6c coordinate stars from those factors are largest. The kernel
lemma proves both maximality of this rank and the full stated extremizer
classification, for every finite mixed product.

## An obstruction for every convex mixture of partition certificates

For any downset with parameters N,s, partition its N-1 nonempty members
into s pairwise-disjoint classes, allowing empty classes. Let their sizes
be m_1,...,m_s. The associated partition core is

```
C[A,B]=s*[A,B belong to the same class]-1.
```

Writing S=N-1=sq+r, with 0<=r<s, integer balancing gives
sum_i m_i^2 >= r(q+1)^2+(s-r)q^2. Indeed, moving one member from a class
of size at least two more than another decreases that sum; iterating ends
with precisely these balanced sizes. Hence

```
1^T C 1=s*sum_i m_i^2-S^2 >= r(s-r),
M[empty,empty]=(1+1^T C 1-s)/(N-s)
             >= (1+r(s-r)-s)/(N-s).
```

If r(s-r)>S, this diagonal is strictly above 1 for every partition lift,
which precludes M<=I. The diagonal is a linear functional of M. The same
strict lower bound holds for every convex mixture of such lifts, including
all automorphism averages. This separates the entire convex partition
template from capped feasibility; it asserts no obstruction to other H
matrices or to ordinary disjoint partitions.

In the present regular six-point cohort the criterion applies to d=7,8,9,10:

| d | Number of triples | N | s | Lower bound for the empty diagonal |
| ---: | ---: | ---: | ---: | ---: |
| 7 | 14 | 36 | 13 | 24/23 |
| 8 | 16 | 38 | 14 | 4/3 |
| 9 | 18 | 40 | 15 | 8/5 |
| 10 | 20 | 42 | 16 | 24/13 |

The capped certificates supplied for these eight classes consequently lie
outside that convex hull. This is stronger than checking one selected
partition average; no completeness claim about general PSD templates is made.

## A fractional gap for additional mixed products

The exceptional D_* has d=5 and admits the exact fractional dual
x(empty)=0 and x(A)=(|A|-1)/3 for nonempty A, with total weight 35/3.
Its feasibility and matching base upper certificate are proved and checked
in [THEOREM.md](THEOREM.md) and [verify.py](verify.py). Projecting this dual
from a D_* factor of any product gives a feasible dual with total weight

```
(35/96)*N_product.
```

Nonempty projections of a pairwise-disjoint collection cannot repeat and
remain pairwise disjoint; repeated empty projections have weight zero.
Deleting the global empty vertex also removes zero weight.

If a product contains at least one D_* factor and every factor has d<=7,
then p_j=(d+6)/(22+2d)<=13/36. Therefore its fractional value divided by
its largest star is at least

```
(35/96)/(13/36)=105/104>1.
```

Despite this fractional obstruction, the product has the capped maximal-rank
H certificate and the star-only equality classification just proved.
For pure powers of D_* the stronger ratio is 35/33, as established in
[CAP_THEOREM.md](CAP_THEOREM.md). Only these lower bounds are asserted for
products; their exact fractional optima are not claimed, and the mixed-gap
statement does not include arbitrary d=8,9,10 factors.

## Reproduction, literature, and trust boundary

From this directory, using CPython 3.11+ and the standard library only:

```sh
OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1 MKL_NUM_THREADS=1 python3 regular_six.py --check REGULAR_SIX_RESULTS.json
```

This single process regenerates both complete labeled domains, all canonical
classes, all matrices, both exact PSD routes, all kernel equations, ranks,
and recorded hashes. The rational orbit fixture is 19,550 bytes; no numerical
optimizer, omitted private catalog, or classification dataset is an input.
A local complete run took 16.37 seconds and peaked at 19,684 KiB RSS; these
are measurements, not guarantees. Full tensors are never constructed: their
inequalities, ranks, and equality cases follow from the written arguments.

Trust rests on exact Python integer/Fraction arithmetic, the short published
algorithms, and the unformalized written proofs. Floating-point projections
were used to find some rational candidates; every candidate is checked
afresh by exact arithmetic, and the discovery computation is outside the
proof boundary. Independent review and formal verification remain absent.

Primary target, checked 2026-09-30:
[Ellis--Filmus--Friedgut, Section 4, arXiv:2609.28404v1](https://arxiv.org/html/2609.28404v1#S4).
The [current arXiv record](https://arxiv.org/abs/2609.28404) still lists only
v1, with general Conjectures H and I unresolved. The friendly-loop
Hoffman/theta equivalence there is prior context. The standard weighted
Hoffman equality calculation and tensor rule are not claimed new.

Related source, inspected before publication: six-downset-2 proves
[capped certificates for every Steiner triple downset and its products](https://github.com/helgithorskarp/math_results/blob/main/spectral_downsets_steiner_triples/CAPPED_PROOF.md),
source commit `34ae127ca2a6116c58e015bc8a6722000ce06296`. That all-orders
incidence theorem and this even-order-six cohort have distinct hypotheses.
The refreshed peer source at `4b419710be5c9d15b78649707728e26e915dca96`
also gives a finite
[two-STS(9) capped classification](https://github.com/helgithorskarp/math_results/blob/main/spectral_downsets_steiner_triples/TWO_STS9_PROOF.md).
The complete six-point H census already in this directory is an earlier
result. Its reproduction is validation, not the new capped or equality claim.
