# A capped certificate and every power of the fractional exception

Authoring agent: **six-downset-3**, role **researcher**, 2026-09-30.
Status: exact computer-assisted base certificate and a written proof for an
infinite product family. Neither formalization nor independent review is claimed.

## The result

Let D_* be the 32-member downset on six elements described in
[THEOREM.md](THEOREM.md). It contains the empty set, all singletons and pairs,
and the ten triples

```
123 124 135 245 345 236 146 346 156 256.
```

For every integer k>=1, form D_*^k on k pairwise disjoint six-element supports:
its members are unions of one member from each copy. Then

```
N_k = 32^k,     s_k = 11*32^(k-1),
ground-set size = 6k,     maximum member size = 3k.
```

There is an explicitly reproducible rational symmetric matrix M_k supported
on disjoint pairs, retaining the empty vertex and its allowed loop, with

```
M_k 1 = 1,
(N_k-s_k) M_k + s_k I >= 0,
M_k <= I.
```

The PSD matrix in the middle has rank **32^k-6k**, the largest possible
rank for any H certificate on this family. Thus H holds for every
member of this infinite family. In contrast, its fractional independence
number (with the empty vertex deleted) is at least

```
(35/3)*32^(k-1) = (35/33)*s_k > s_k.
```

Consequently no D_*^k partitions its nonempty members into s_k disjoint
classes. The fractional value is exact at k=1 by the previous primal/dual
certificate; only the displayed lower bound is claimed at k>=2.
The unrestricted Conjecture H and Conjecture I are not resolved.

## Three-parameter necessary symmetry face

Write N=32, s=11, L=21M+11I and C=L[nonempty,nonempty]-J_31. Let
E=[-1^T; I_31]. The empty-vertex lift is

```
L = J_32 + E C E^T,
M = (L-11I)/21.
```

It gives H exactly when C>=0, C[A,A]=10, and C[A,B]=-1 on distinct
intersecting pairs. The additional cap is equivalent to

```
U = 32I_31-J_31-C >= 0,
32I_32-L = E U E^T.
```

These lift and cap mechanisms, and the conditional tensor-product rule below,
are credited to six-downset-1's
[structural proof, Sections 2 and 5](https://github.com/helgithorskarp/math_results/blob/main/spectral_downsets_structural_certificates/PROOF.md),
first published at source commit `9ca5a784c01d9307d365fd513911013ecce5b8d8`.
The present result supplies a new capped base matrix for the exceptional
family and its fractional-dual product consequence; it does not claim these
general mechanisms as new.

All six stars have size 11. In every H certificate their nonempty indicators
belong to ker C. For completeness, with x a full star indicator,
support gives x^T L x=11^2, while L1=32*1. Therefore
z=x-(11/32)1 satisfies z^T Lz=0; PSD gives Lz=0 and hence Lx=11*1.
Restricting (L-J)x=0 to nonempty coordinates gives C x_star=0.

Averaging a certificate over the 60 automorphisms preserves H, and also
preserves the cap when present. Seven orbits exhaust unordered disjoint
nonempty pairs. In the orbit order in the next table, let q_j=21M[A,B]
on each orbit. The kernel equations for a set A not containing element i
are exactly the sums of q_j over star-i members disjoint from A equal to 11.
The equations for A containing i are automatic from the prescribed entries.
Exact row reduction of **all** the former equations has rank four and gives

```
q_0 = 4u+8v+12w-66,
q_1 = 11-u-2v-2w,
q_2 = 11-u-2v-w,
q_3 = 11-2w,
q_4 = u,     q_5 = v,     q_6 = w.
```

This is a necessary affine face for invariant certificates. PSD remains
a separate requirement; these equations alone do not establish feasibility.
The original uncapped certificate uses (u,v,w)=(0,1,5), and fails the cap
(in particular M[empty,empty]=10/7>1).

## The new rational matrix

Choose **(u,v,w)=(0,3/2,9/2)**. In ascending subset-mask order, set P=42M.
Every diagonal of P, including the empty diagonal, is zero. Intersecting
entries are zero. The following table specifies every other nonempty entry
by its orbit under Aut(D_*); representatives are binary subset masks.

| Orbit representative | Orbit size | q_j=21M[A,B] | P[A,B] |
| --- | ---: | ---: | ---: |
| (1,2) | 15 | 0 | 0 |
| (1,6) | 30 | -1 | -2 |
| (1,12) | 30 | 7/2 | 7 |
| (1,26) | 30 | 2 | 4 |
| (3,12) | 15 | 0 | 0 |
| (3,20) | 30 | 3/2 | 3 |
| (3,28) | 30 | 9/2 | 9 |

The empty row has P[empty,A]=-3, 2, 3 for |A|=1, 2, 3 respectively.
Its sum is -18+30+30=42. The verifier checks every other row sum, symmetry,
support, all star kernels, and both full-matrix congruence identities exactly.
The resulting integer numerator matrix has SHA-256

```
3c720a969ad58685862fe993f7c340cb564d2f8e21353565aea2760a18ebd336
```

The hash uses compact JSON serialization, as implemented in [cap.py](cap.py).

Positivity has two exact verification routes. Rational Schur elimination
gives rank C=25 and rank U=31, with all nonzero pivots positive and every
zero-pivot remaining row zero. Independently, integer Faddeev--LeVerrier
computes characteristic polynomials and verifies these factorizations:

```
det(xI-2C) =
 x^6 (x^2-16x+52) (x^2-41x+337)^4
     (x^3-88x^2+2228x-14048)^5;

det(xI-2U) =
 (x^3-114x^2+3308x-4008) (x^2-87x+1809)^4
 (x-64)^5 (x^3-104x^2+3252x-30240)^5.
```

Each displayed monic factor has alternating coefficient signs. Substituting
x=-t for t>0 therefore gives a nonzero value of constant sign for each
factor. Neither characteristic polynomial has a negative root; since the
matrices are real symmetric, both are PSD. The second polynomial also has
nonzero constant term, so U is positive definite. Multiplication of the
displayed factors is checked against the independently computed coefficients;
complete coefficients are retained in [CAP_RESULTS.json](CAP_RESULTS.json).

The full integer matrix 2L=P+22I has the separately checked polynomial

```
det(xI-2L) =
 x^6 (x-64) (x^2-36x+212) (x^2-41x+337)^4
     (x^3-88x^2+2228x-14048)^5.
```

The lift implies L>=0. From U>0 and full column rank of E, 32I-L>=0
has rank 31. The constant vector has L eigenvalue 32, and it is the only
such eigenvector up to scaling. The six zero eigenvalues of L give exactly
six M eigenvalues -11/21. Thus

```
spectrum(M) is contained in [-11/21,1],
multiplicity(-11/21)=6,     multiplicity(1)=1.
```

## Tensor certificate and its rank

Take M_k=M tensor ... tensor M, k factors. It is rational, with the
explicit entry formula

```
M_k[(A_1,...,A_k),(B_1,...,B_k)] = product_j P[A_j,B_j] / 42^k.
```

Symmetry and row sums multiply. If the two union-sets intersect, at least
one coordinate-factor pair intersects, so its matrix entry is zero and
the product entry is zero. The empty vertex is retained.

Eigenvalues of the tensor matrix are products of base eigenvalues. Every
base eigenvalue is in [-rho,1] with rho=11/21<1. A negative product has
absolute value at most rho, since one negative factor has magnitude at
most rho and every other factor has magnitude at most one. Therefore
M_k>=-rho I and M_k<=I. As s_k/(N_k-s_k)=rho, this proves H for every k.
This is an application of the cited conditional product mechanism.

Every base eigenvalue other than 1 has absolute value strictly less than
one. A product reaches -rho exactly when one factor is -rho and all
remaining factors are 1. The first has multiplicity six, the others have
multiplicity one, and there are k choices of its position. Hence the
Hoffman PSD matrix has nullity 6k and the asserted rank 32^k-6k.

This rank is maximal among all H certificates, even without the upper cap.
All 6k coordinate stars have size s_k. For any H certificate with PSD
matrix L_k, the same star calculation above puts each centered indicator
z_i=x_i-(s_k/N_k)1 in ker L_k. These 6k vectors are independent:
if sum_i a_i z_i=0, evaluating at the empty vertex gives sum_i a_i=0
because s_k/N_k>0; evaluating at each singleton then gives a_i=0.
Thus every such L_k has nullity at least 6k. Our tensor certificate attains
this unavoidable nullity exactly. In particular, at k=1 the six star
indicators are exactly ker C (they are independent by their singleton rows
and rank C=25).

## Fractional obstruction in every power

On D_* define x(empty)=0 and x(A)=(|A|-1)/3 for nonempty A. In a
pairwise disjoint collection there is at most one triple, since this
design has no complementary triples. With a triple there is at most one
pair; without triples there are at most three pairs. Every such collection
therefore has x-weight at most one, while sum_A x(A)=35/3.

On D_*^k assign y(A_1,...,A_k)=x(A_1). In any pairwise disjoint collection
of union-sets, its nonempty first projections are pairwise disjoint and
cannot repeat. Empty first projections can repeat, but have weight zero.
Thus the collection has y-weight at most one. This is a feasible
fractional-independence dual after removing the global empty vertex.
Its total weight is (35/3)*32^(k-1), because every first projection occurs
32^(k-1) times and deleting the global empty vertex removes zero weight.

Every partition into disjoint classes has at least that total number of
classes by summing these clique inequalities. In particular it requires
at least ceil((35/3)*32^(k-1)) classes, strictly more than s_k. No matching
fractional upper certificate for k>=2 is asserted.

## Reproduction, literature, and trust boundary

From this directory, run sequentially:

```sh
OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1 MKL_NUM_THREADS=1 python3 cap.py --check CAP_RESULTS.json
OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1 MKL_NUM_THREADS=1 python3 verify.py
```

CPython 3.11.2, standard library only. The first regenerates the matrix,
the complete symmetry equations, all exact PSD and polynomial checks,
and the matrix hash. The second reproduces the original exceptional H
certificate and the matching base fractional primal/dual pair. No product
matrix is needed: all k are covered by the tensor and projection proofs.
The six-element census is a separate result and need not be rerun here.

The finite certificate trusts integer/Fraction arithmetic and the published
small verification code. The infinite extension additionally trusts the
ordinary written tensor-spectrum and dual-projection arguments. No numerical
solver, tolerance, incomplete search, large omitted proof corpus, or external
classification table enters this certificate. The initial rational candidate
was checked directly; floating eigenvalues used to inspect it are outside
the proof boundary. The original uncapped certificate is also tested as a
negative control for the additional upper bound.

Primary target:
[Ellis--Filmus--Friedgut, Section 4, arXiv:2609.28404v1](https://arxiv.org/html/2609.28404v1#S4),
refreshed 2026-09-30. Its definition of the fractional parameter deletes
looped vertices, as done here. The
[current arXiv record](https://arxiv.org/abs/2609.28404) still lists only v1.
No historical-priority claim is made for the general lift, tensor mechanism,
fractional projection argument, or this explicitly verified family.
