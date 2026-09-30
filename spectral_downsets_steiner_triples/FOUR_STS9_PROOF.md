# Capped maximal-rank H for four block-disjoint STS(9)

Author: **six-downset-2**, role **researcher**, 2026-09-30.
Status: exact computer-assisted subclass theorem with ordinary written
coverage, kernel and product arguments. Author-checked, unformalized.
No independent review or historical priority is claimed for this extension.

## 1. Quantified theorem

Let T_1,T_2,T_3,T_4 be Steiner triple systems on the same nine points whose
block sets are pairwise disjoint. Their union generates a downset D containing
empty, nine singletons, all 36 pairs, and 48 triples. Every point star has
size s=1+8+16=25, and N=|D|=94.

**For every such input** there is a rational symmetric matrix M, indexed by D,
with M1=1, M[A,B]=0 when A intersects B, and

```
-(25/69)I <= M <= I.
Q=69M+25I has rank 85; 94I-Q has rank 93.
On 1-perp, Q <= (94-1/4)I, hence M <= (275/276)I.
ker Q is the span of the nine centered point-star indicators.
```

The rank 85 is the greatest possible among **all real H certificates** on D,
including certificates lacking the upper cap. Every maximum intersecting
family is a point star. Every finite product of these downsets on disjoint
coordinate supports has a capped certificate with greatest possible H rank.
For k factors, allowing different input types,

```
N_k=94^k,  s_k=25*94^(k-1),  rank Q_k=94^k-9k.
```

Its only maximum intersecting families are the 9k coordinate stars.

The new ingredient is the complete four-system cohort of capped rational
matrices. Ordinary H is already proved by the [layered formula](PROOF.md).
The quantitative rank repair is the prior [maximal-rank lemma](MAXRANK_PROOF.md),
and the three-system [coverage theorem](THREE_STS9_PROOF.md) supplies parent
types. Base strict-EKR is already classical, as qualified in Section 6.
Neither general H nor Conjecture I is resolved.

## 2. Complete input coverage and full point symmetries

[verify_four9.py](verify_four9.py) regenerates all inputs with the standard
library. It reuses [verify_two9.py](verify_two9.py)'s exact-cover enumeration
of all 840 labelled STS(9), independently compared entry by entry with the
affine system's orbit under adjacent transpositions. The orbit includes an
explicit transport q_S from the affine first system to each S. The 432
affine transformations are its full point stabilizer G_0: they preserve the
system, and 9!/840=432. These historical baselines are validation.

The three-system generator exhausts the two relative second-system orbits,
their 41 and 34 disjoint third systems, and all 27 ordered-triple orbits.
Its full point-isomorphism reduction has nine union types. Any four-system
input contains a three-system subunion. Normalize that subunion to one of
the nine parent types, then choose a fourth system disjoint from its blocks.
For parent types in the three-system canonical order the numbers of choices
are 7,6,8,6,10,8,11,10,8. Quotienting each entire candidate set by the parent's
**full union group** leaves 5,3,4,3,5,2,5,3,2 extension orbits, or 32 total.
Every four-system input is thus represented, whether or not its supplied
decomposition is the parent's originally chosen decomposition.

For each 48-block union U the verifier filters all 840 systems to find every
STS contained in U. An automorphism of U sends the fixed first system to a
contained S; all maps with that image form exactly the coset q_S G_0.
Filtering all those maps for preservation of U therefore computes full
Aut(U). The minimum of g q_S^(-1) U over all contained S and g in G_0 is
a complete point-isomorphism key. Under a point isomorphism f, each map
q_(fS)^(-1) f q_S fixes the first system and belongs to G_0, so normalized
image sets agree; conversely equal minima supply an explicit isomorphism.
This argument does not require uniqueness of the supplied decomposition.

The 32 extension cases reduce to 12 union types. Exact increasing-subsystem
enumeration finds every unordered decomposition into four systems, including
alternatives. Here is the coverage summary in canonical-key order:

| Type | Extension cases | Full group order | Contained STSs | Four-system decompositions | Supported pair orbits |
|---|---:|---:|---:|---:|---:|
| 0 | 2 | 54 | 8 | 2 | 59 |
| 1 | 2 | 3 | 11 | 1 | 698 |
| 2 | 1 | 24 | 8 | 2 | 160 |
| 3 | 2 | 6 | 10 | 1 | 359 |
| 4 | 2 | 2 | 10 | 1 | 1036 |
| 5 | 4 | 1 | 7 | 1 | 2032 |
| 6 | 4 | 1 | 6 | 1 | 2032 |
| 7 | 4 | 1 | 7 | 1 | 2032 |
| 8 | 4 | 3 | 7 | 1 | 682 |
| 9 | 1 | 4 | 8 | 1 | 520 |
| 10 | 4 | 1 | 7 | 1 | 2032 |
| 11 | 2 | 18 | 8 | 2 | 130 |

A separate unquotiented enumeration checks **all actual unions** with the
first system in a complete decomposition. It visits every increasing triple
of its 192 disjoint candidate systems and retains precisely pairwise
block-disjoint triples. The 10,048 resulting unions agree entry by entry
with all affine normalization images of the 12 types. For the latter images
only contained systems participating in a full decomposition are used.
Extra contained STSs are retained in the symmetry calculation, but are not
automatically eligible for this fixed-first decomposition comparison.

Point-orbit sizes give 2,068,080 labelled unions. Counting their complete
decompositions with multiplicity gives 2,110,080 labelled decompositions,
consistent with 840*10,048/4. This is finite coverage validation, not a new
historical design-classification claim. In particular, 32 is a number of
extension representatives, not a number of distinct downsets; nor does the
theorem cover every simple 2-(9,3,4) design.

## 3. Explicit rational matrices and exact PSD proof

[four9_certificates.json](four9_certificates.json) specifies one block
decomposition and a fixed rational matrix Q_c for each of the 12 union types.
Regenerate its full group as above. For each supported unordered pair {A,B},
including {empty,empty}, take the least sorted pair of integer masks in its
group orbit and sort all these keys. The stored integer numerators divided
by a positive case denominator define the entries on those orbits. Nonempty
diagonals are 25, and all intersecting off-diagonals are zero. The decoder
expands the complete orbits, rejecting overlap and incomplete coverage.
No floating discovery or external census is a reproduction input.

For every fixed matrix the checker verifies downward closure, actual stars,
symmetry, supported entries, row sums, all star equations and the empty
column. It checks

```
Q_c >= 0,                    rank Q_c=84;
94I-Q_c >= 0,                rank(94I-Q_c)=93;
94I-Q_c-(1/2)(I-J/94) >= 0,  rank=93.
```

PSD and ranks use rational positive-pivot Schur congruence with explicit
handling of zero residual rows. Independently, both Q_c and 94I-Q_c are
checked by the integer characteristic-polynomial method in verify_two9.py.
After positive integer scaling, exact Faddeev--LeVerrier division gives
the coefficients of det(tI+A). Nonnegative coefficients and leading term
t^N preclude a positive root, which any negative eigenvalue of a symmetric
A would produce. Conversely PSD gives nonnegative coefficients. The last
nonzero elementary-symmetric coefficient index is its rank. These two
methods certify both inequalities and ranks without tolerance or a solver.

Write z_i=x_i-(25/94)1 for a star indicator x_i, and
w=e_empty-(1/94)1. The checked equations Q_c x_i=25*1 and Q_c 1=94*1
kill all z_i; the empty column equal to one kills w. Their independence
follows by evaluating at singletons, then pairs and empty; the verifier
also checks Gram rank 10. Since Q_c has nullity 10, its kernel is exactly
span(z_1,...,z_9,w).

## 4. Repair, rank optimality and equality

Let Q_o be the ordinary layered matrix on the **same specified** four
systems. [PROOF.md](PROOF.md) proves it is PSD. The finite checker also
verifies every input directly. For each case,

```
rank Q_o=45,  Q_o[empty,empty]=1027,  Tr(Q_o)=3352;
Q_o[singleton,empty]=-131,  (Q_o w)[singleton]=-132.
```

Set epsilon=1/13408 and Q=(1-epsilon)Q_c+epsilon Q_o. Convexity preserves
the H equations and PSD. Positivity implies Q_o<=Tr(Q_o)I. Together with
the half-unit gap of Q_c on 1-perp, the prior quantitative mixture lemma
gives Q<=(94-1/4)I there. The constant vector remains an eigenvector of
eigenvalue 94, so the upper cap and its simple endpoint hold. The public
checker directly verifies Q, its upper slack and quarter-unit buffer as
additional exact validation.

The kernel of a positive convex combination of PSD matrices is the
intersection of their kernels, since its zero quadratic form forces both
nonnegative terms to vanish. Q_o kills all z_i and has Q_o w nonzero.
Hence ker Q=span(z_i) and rank Q=85.

For any real H matrix L on this downset, a maximum-star centered indicator
has zero quadratic form and therefore lies in ker L. The nine star vectors
are independent by empty and singleton evaluation, so rank L<=94-9=85.
This is the general maximum-star rank criterion credited to
six-downset-3's [regular-six proof](https://github.com/helgithorskarp/math_results/blob/main/spectral_downset_six_exact/REGULAR_SIX_PROOF.md),
not a new general lemma here.

If an intersecting family has indicator x and size a, support and row sums
give (x-(a/94)1)^T Q (x-(a/94)1)=a(25-a). PSD implies a<=25; at equality,
the centered indicator is in span(z_i). Evaluation at empty forces the sum
of its star coefficients to be one, and evaluation at each singleton makes
every coefficient either zero or one. Exactly one is one. Thus the maximum
families are the nine stars. This recovers a previously known base equality
statement through the new spectral construction.

## 5. Product closure and its exact spectral rank

For any k factors from this cohort, tensor their M matrices. Row sums and
support multiply. Each spectrum lies in [-rho,1], rho=25/69<1, with a simple
eigenvalue one. Any negative product eigenvalue has an odd number of negative
factors and magnitude at most rho. It reaches -rho exactly when one factor
is at its negative endpoint and all others are at one. Three or more
negative factors have smaller magnitude, as does any nonconstant positive
factor. The endpoint multiplicity is therefore 9k. These endpoint vectors
are precisely the lifted centered coordinate-star indicators, proving the
displayed product rank, its unrestricted optimality, and star-only equality.

More generally the same argument combines these factors with the previously
published maximal-rank single-STS and two- or three-STS(9) factors. If factor
j has parameters N_j,s_j,r_j, put p=max_j(s_j/N_j). Then

```
N_product=product_j N_j,  s_product=p*N_product,
rank Q_product=N_product-sum_(j:s_j/N_j=p) r_j.
```

Only the stars of those critical factors can be maximum families. The
capped six-point factors of six-downset-3 may be included with the same
criterion. In particular 25/94<11/32, so h>=1 exceptional D_* factors
dominate any factors from this four-system cohort and give rank
N_product-6h. The existing fractional-dual ratio lower bound 35/33 persists;
no mixed fractional optimum is asserted. The tensor mechanism is credited
to six-downset-1's [structural proof](https://github.com/helgithorskarp/math_results/blob/main/spectral_downsets_structural_certificates/PROOF.md),
and the mixed fractional premise to six-downset-3's
[capped exceptional proof](https://github.com/helgithorskarp/math_results/blob/main/spectral_downset_six_exact/CAP_THEOREM.md).

## 6. Literature, verification and trust boundary

The separate [seven-weight obstruction](TEMPLATE_OBSTRUCTION.md) proves
that no centered H matrix in its displayed template exists on any simple
2-(v,3,2) design, v>=9, and its broader completing-point variation scope.
The nine-point even pair degrees m=2,4,6 are included. Its proof uses only necessary
row/star equations and a negative singleton quadratic form, independent of
the four-system tables. Thus these capped matrices require finer seed
weights than that natural seven-parameter extension of the STS formula.
The fresh [clique-center construction](https://github.com/helgithorskarp/math_results/blob/main/spectral_downsets_structural_certificates/CLIQUE_CENTERS.md)
by six-downset-1, source b95d1958dfa2817dd875aeeedb81f69b90f3e0d1, uses
a different rank-two incidence decomposition and credits our prior repair.
Its author-checked structural matrices are related context for this pass.

The target is [Ellis--Filmus--Friedgut, Section 4](https://arxiv.org/html/2609.28404v1#S4).
Its [current arXiv record](https://arxiv.org/abs/2609.28404), checked 2026-09-30,
lists v1 only and retains H and I as conjectures. The classical Chvatal and
projection-packing results are separate. Historical affine/counting context
is [Bryant--Grannell--Griggs (2003)](https://grannell.net/Papers/lsls9.pdf),
which recalls 840 labelled STS(9), their 432 automorphisms and the two large
sets. Reproducing those facts or the present coverage counts is validation,
not claimed mathematical novelty.

The base star-only conclusion already follows from
[Czabarka--Hurlbert--Kamat, Theorem 1.4 (2017)](https://arxiv.org/pdf/1703.00494).
Its first exception has largest star seven. Its second requires largest
star 3|B|+3 or 3|B|+4 for a set B outside a distinguished three-set.
On nine points |B|<=6, so neither reaches 25. The new contribution is
the exact capped matrices, their maximal H ranks and spectral product
consequences, not a new base strict-EKR theorem.

Related fresh work includes six-downset-3's
[sparse trade theorem](https://github.com/helgithorskarp/math_results/blob/main/spectral_downset_six_exact/KERNEL_TRADE_PROOF.md),
verified source 15154d29fc0f9d1bd6f06b2736847c2aa808323e, and
six-reviewer-4's [two-center refinement](https://github.com/helgithorskarp/math_results/blob/main/spectral_downset_two_centers_review4/REVIEW.md),
source e30f3d55efa4823c6e19bbfcff0b97da9c1d3983. Those supply alternative
rank lifts on their stated inputs; neither establishes the four-system
cap used here. We use the previously published convex repair, rather than
claiming the general removal of the empty-centered direction anew.

From the repository root, with CPython 3.11.2, standard library, and
assertions enabled:

```sh
OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1 MKL_NUM_THREADS=1 \
  python3 spectral_downsets_steiner_triples/verify_four9.py --check
```

[four9_expected.json](four9_expected.json) records complete cohort summaries,
matrix and polynomial hashes, exact ranks and quantitative buffers. Four
controls reject a wrong row entry, a malformed fourth system, and the
ordinary matrix's failed upper cap by both PSD methods. All finite checks
trust Python integer/Fraction arithmetic, the inspected complete generator
and the small decoder and verifiers. Coverage, perturbation and product
bridges are ordinary written mathematics; no proof assistant was used.
Private exact affine elimination and bounded floating projection served
only discovery. Neither a solver status nor unsuccessful recovery is a
nonexistence proof. The theorem supplies no uniform cross-incidence formula,
no cap for every regular rank-three downset, and no unrestricted H theorem.

The complete four-system verification took 566.32 seconds and 31,332 KiB
maximum child resident memory, one process and one thread. The private
complete union reduction took 19.06 seconds and 20,852 KiB. The largest
measured exact affine reduction used 341,096 KiB with 2,032 variables and
1,278 free parameters. All jobs respected the existing scope limits.
