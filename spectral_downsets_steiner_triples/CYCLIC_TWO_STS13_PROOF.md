# Capped maximal-rank H for common-cycle two-STS(13) downsets

Author: **six-downset-2**, role **researcher**, 2026-09-30.
Status: exact finite certificate and ordinary written bridges, author-checked
and unformalized. No historical priority or independent review is asserted.
General Spectral Chvátal Conjecture H remains open.

## Statement and exact scope

Let S_1,S_2 be block-disjoint Steiner triple systems on thirteen points.
Assume **both systems are invariant under the same thirteen-cycle**.
Let D be their generated downset, including the empty set. Then
N=|D|=144 and every coordinate star has size s=25.

**Theorem.** D has an explicit rational symmetric matrix M supported on
disjoint pairs, with M1=1 and

```
-25/119 I <= M <= I,
Q=119M+25I,          rank Q=131,
rank(144I-Q)=143.
```

The upper endpoint is simple and Q<=108I on the constant complement.
Its kernel is exactly the span of the thirteen centered coordinate-star
indicators. Rank131 is the greatest possible rank of an H certificate on
this D, including certificates without an upper cap.

Every finite product of k such downsets on disjoint coordinates has a
capped H certificate of rank 144^k-13k and maximum star size
25*144^(k-1). Its maximum intersecting families are exactly its 13k
coordinate stars. The same critical-factor rank rule applies to finite
mixed products with the previously certified single-STS(v), v>=7, and
two-, three- or four-block-disjoint-STS(9) factors: if
p=max_j s_j/N_j and r is the sum of their ground-set sizes over factors
with s_j/N_j=p, the product rank is product_j N_j-r and the only maximum
families are those r coordinate stars.

The cyclic hypothesis concerns **each input system**, not merely their
union. This is not a certificate for every pair of STS(13), every cyclic
twofold triple system, or all downsets on thirteen points. No full point
automorphism-group assertion is needed. The spectral certificate is the
new increment relative to our prior constructions; the cyclic design
and small design classification are not claimed new. The base star-only
conclusion is also already covered by Czabarka--Hurlbert--Kamat's
[2017 rank-three theorem](https://arxiv.org/pdf/1703.00494), Theorem1.4.

## Complete input coverage within the cyclic hypothesis

Relabel the common cycle as x->x+1 on F_13. Every translation orbit of
a triple has length13: a smaller orbit would be fixed by a nonidentity
translation, whose point cycles have length13, impossible for a
three-element set. The 286 triples therefore have 22 orbits.
An STS(13) has26 triples, so each cyclic system is a union of exactly
two of those orbits.

[verify_cyclic13.py](verify_cyclic13.py) regenerates all22 orbits and
checks every one of the binom(22,2)=231 possible systems by actual pair
counts. Exactly four are STSs. It checks all six unordered pairs of
these four and finds exactly two block-disjoint pairs. Their unions
are identical, entry by entry. That common set is

```
U = {{x,x+d,x+4d}: x in F_13, d in F_13\{0}},
```

with52 distinct blocks. The verifier checks this identity and checks
that every affine map x->a*x+b, a!=0, preserves U. Thus all156 affine
maps form a verified symmetry subgroup for D. This is sufficient for
construction and validation; the full S_13 automorphism group is not
used or claimed. Every input satisfying the stated common-cycle
hypothesis is a point relabelling of this D. Matrix permutation
congruence transfers every proved condition and rank to that input.

## Fixed rational matrix and exact positivity

Order D by cardinality then integer mask. The supported symmetric
matrix positions, including the allowed empty diagonal, number6631.
The affine subgroup has54 orbits on these positions. On nonempty
diagonals put25, on intersecting off-diagonals put0, and on a supported
orbit put its fixed numerator divided by9 from
[cyclic13_certificate.json](cyclic13_certificate.json). Representatives
are the lexicographically least **index pairs** in this ordering.
The verifier regenerates the orbits and checks their representative
hash, so a weight list is never decoded in an assumed ordering.

Call the decoded matrix Q_c. Direct rational checks give

```
Q_c1=1441, Q_c x_i=251 for all thirteen star indicators x_i,
Q_c e_empty=1, Q_c>=0, rank Q_c=130,
144I-Q_c>=0, rank(144I-Q_c)=143,
72I-Q_c+(1/2)J>=0, rank=143.                       (1)
```

The last form annihilates constants and proves Q_c<=72I on their
orthogonal complement. Every matrix equation, support entry, actual
star size, and symmetry is checked on the full144-member downset.
PSD is checked by rational Schur elimination and, independently, by
integer characteristic-polynomial coefficients on the affine fixed
spaces. The [affine reduction lemma](AFFINE_REDUCTION.md) proves
that restrictions of orders12 and15 suffice. The compressed ranks for
Q_c are (10,12,2) for T,H,G, giving10+12(12-2)=130;
each upper form in (1) has ranks (11,14,3), giving143.

These compressed checks use a written invariant-space bridge. The
`--full` verification also checks the original144-by-144 forms by
rational Schur elimination, without that bridge. No floating
eigenvalue, tolerance, optimizer, or external design table is in the
proof boundary. Numerical projection and rational recovery were
discovery steps only; only the fixed weights are needed to reproduce.

## Explicit maximal-rank repair

For each of the two cyclic decompositions, construct the existing
ordinary layered H matrix in [PROOF.md](PROOF.md). Each has rank95.
A single decomposition need not be affine-invariant. Average their
two matrices to obtain Q_o. The affine group permutes the complete
decomposition set, so this average is invariant. Averaging preserves
PSD, symmetry, support, diagonal and row/star equations. Exact checks
give rank Q_o=107 and

```
Q_o[empty,empty]=6256/3, Tr(Q_o)=16981/3,
w=e_empty-(1/144)1,  (Q_o w)[singleton]=-182.
```

Put epsilon=108/16981=36/Tr(Q_o) and
Q=(1-epsilon)Q_c+epsilon Q_o. This is an explicit rational matrix.
The prior [quantitative repair](MAXRANK_PROOF.md), with input gap72,
gives on the constant complement

```
Q <= (1-epsilon)72I + epsilon*Tr(Q_o)I <=108I.      (2)
```

Its kernel is the intersection of the two PSD kernels. Define
z_i=x_i-(25/144)1. The thirteen z_i and w are independent; subtracting
their empty value from singleton values proves the star coefficients
vanish, and then w cannot be in their span. A rational Gram-rank
check reproduces these dimensions. Equation (1) and rank130 show
ker Q_c=span(z_1,...,z_13,w). Each Q_o z_i=0 but Q_o w!=0.
Consequently ker Q=span(z_1,...,z_13) and rank Q=131.
The direct exact verifier checks this repaired rank, upper rank143 and
the36-unit buffer in (2), by both reduced methods and with the
full-matrix fallback. Put M=(Q-25I)/119 to obtain the theorem.

Every real H certificate has all thirteen independent z_i in its
kernel. Indeed, support gives x_i^T Q x_i=25^2; row sums give
z_i^T Q z_i=0; and PSD implies Qz_i=0. This forces rank<=131.
This maximal-star rank principle is credited to **six-downset-3** in
[MAXRANK_PROOF.md](MAXRANK_PROOF.md). The convex mixture and trace
estimate are standard matrix facts, applied here with a new input.

## Products and equality

The product is the downset of tuples of members, identified with their
unions on disjoint coordinate supports. Take the tensor product of
the normalized M matrices. It has the correct row sums and disjoint
support. Each factor has spectrum in [-beta_j,1], where
beta_j=s_j/(N_j-s_j)<1, and its eigenvalue1 is simple.
Thus the smallest product eigenvalue is -max_j beta_j: it is attained
by one critical factor's bottom eigenspace and constants in all other
factors. Several negative factors have strictly smaller absolute
product; any additional nonconstant factor also prevents equality.
The bottom multiplicity is exactly r, so the product H rank is N-r.
This is the existing [capped product mechanism](MAXRANK_PROOF.md).

For a maximum intersecting family, Hoffman equality puts its centered
indicator in the span of the r critical coordinate indicators. Its
uncentered indicator is an affine function of those coordinates.
The empty member forces constant term0, singleton members force the
coefficients to be0 or1, and all two-coordinate members are present,
so at most one coefficient is1. The nonempty maximum family is
therefore exactly one critical star. This proves the stated equality
and product claims; it does not use an unproved product EKR assumption.

## Reproduction and compact evidence

CPython3.11.2, standard library only, from the repository root:

```sh
OPENBLAS_NUM_THREADS=1 OMP_NUM_THREADS=1 MKL_NUM_THREADS=1 \
  python3 spectral_downsets_steiner_triples/verify_cyclic13.py --check
OPENBLAS_NUM_THREADS=1 OMP_NUM_THREADS=1 MKL_NUM_THREADS=1 \
  python3 spectral_downsets_steiner_triples/verify_cyclic13.py --full --check
```

[cyclic13_expected.json](cyclic13_expected.json) records exact coverage,
matrix and polynomial hashes, compressed/full ranks, the repaired
epsilon, three independently replayed Boolean cube baselines, and
seven rejection controls. The centered matrix SHA-256 is
`22a81a47f9afc4377a119b33af427f2a52ac68b494a5d58251cafae5aca3c1f2`;
the repaired matrix SHA-256 is
`fe7b5620eed89632addce8ba9e50ae8320606981a4d04a3c7cfeb0722b320b9a`.
Hash serialization is the existing reduced Fraction-string full-matrix
serialization in [verify.py](verify.py). Hashes identify artifacts;
the exact checks and written bridges establish their properties.

The default reduced validation took 8.05 seconds and 40,516 KiB RSS.
The full fallback passed in 278.91 seconds and 40,780 KiB RSS, checking all
nine original, averaged, centered, repaired and buffered full forms.
It proves the finite claim with the explicit invariant-space bridge;
the full fallback independently checks that bridge on this instance.
All calculations use one process and one native thread. Large arrays,
exploratory candidates and raw logs remain private scratch state.
The checked primary target is
[Ellis--Filmus--Friedgut, arXiv:2609.28404v1, Section4](https://arxiv.org/html/2609.28404v1#S4),
whose arXiv record was refreshed2026-09-30 and still lists only v1.
Its numerical tests and projection-packing result do not supply this
particular H matrix; this restricted result does not resolve H or I.
