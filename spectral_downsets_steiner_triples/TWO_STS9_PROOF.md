# An upper spectral cap for every union of two STS(9)

Author: **six-downset-2**, role **researcher**, 2026-09-30.
Status: exact computer-assisted finite theorem and an ordinary written product
proof. No formalization, independent review or historical priority is claimed.

## 1. The result

Let T_1,T_2 be any block-disjoint Steiner triple systems on the same nine
points. Their generated downset contains the empty set, all nine singletons,
all 36 pairs and their 24 triples. It has N=70 and largest star s=17.

**Theorem.** For every such input there is an explicit rational symmetric M
with M1=1, zero entries on intersecting pairs, and

```
-17/53 I <= M <= I.
```

The empty vertex and its loop are retained. There is such a matrix with
Q=53M+17I of rank 60 and 70I-Q of rank 69. Hence the lower endpoint has
multiplicity ten and the eigenvalue 1 is simple. Every product of k>=1 such
downsets, allowing different input pairs in different factors, has a rational
capped H certificate with

```
N_k=70^k,  s_k=17*70^(k-1),
rank((N_k-s_k)M_k+s_k I)=70^k-10k.
```

Ordinary H for this class is already supplied by the earlier layered formula
and the partition construction below. The additional upper bound is the
increment. This is a two-system order-nine theorem, not a result for arbitrary
twofold triple designs or other orders.

## 2. Two exact matrix inputs

Sets are integer masks, bit i representing point i in 0,...,8. The fixed
first system consists of the affine lines of F_3^2, with lexicographic point
labels. The representative second systems are

```
11 21 44 70 112 152 162 193 274 289 328 388
11 21 44 82 97 134 176 200 280 290 324 385.
```

[two9_certificates.json](two9_certificates.json) gives these inputs, two
checked automorphism subgroups, and rational weights for the orbits of
unordered disjoint pairs of vertices. The subgroup orders are 6 and 18;
there are 235 and 82 orbit weights. They need not be assumed to be the full
automorphism groups of the union downsets.

Put Q[A,A]=17 at nonempty vertices and Q[A,B]=0 on distinct intersecting
vertices. For each disjoint pair, including the empty diagonal, use the
lexicographically least ordered mask pair in its subgroup orbit to select
the table entry. The decoder verifies that the subgroup preserves D, is
closed under composition, and that the table covers exactly all required
orbits. All empty entries are 1. The entries have common denominators 11
and 18. No numerical search is needed to reconstruct these matrices.

The checker verifies downset closure, symmetry, support, row sums Q1=70*1,
the actual maximum stars and their equality constraints. Both PSD bounds and
both ranks are checked by two different exact algorithms. Normalizing
M=(Q-17I)/53 gives the claimed certificate.

## 3. Complete coverage of all input pairs

Enumerate STS(9) by exact-cover branching. At each state choose the first
uncovered pair, branch over every triple containing it whose three pairs are
still uncovered, delete those pairs and recurse. A complete system has one
triple covering the chosen pair, and that triple is available in its branch.
Induction on the remaining pairs proves completeness. No selected triples
repeat a pair; at a leaf all pairs are covered. The first-pair rule also
gives each system a unique path. The source finds 840 labelled systems.

Independently, start at the fixed affine system and close under the eight
adjacent point transpositions. They generate S_9, so this is precisely its
full relabelling orbit. Its actual set equals the exact-cover set, not just
its cardinality. Every input first system can therefore be relabeled to
the fixed one.

The 432 maps x->Ax+t, A invertible over F_3, are distinct and preserve the
fixed system. Orbit-stabilizer gives its full automorphism group size as
9!/840=432, so these maps supply every first-system automorphism. Among
all enumerated systems, 192 are disjoint from the fixed first one. Removing
their complete orbits under that group gives sizes 144 and 48 and precisely
the two listed representatives. No system remains afterward.

Every ordered block-disjoint pair is thus simultaneously relabeled to one
of the two checked representatives. Permutation congruence preserves both
PSD inequalities and ranks, while support and row sums transfer directly.
This proves coverage of every union in the theorem. The two orbit counts
refer to ordered pairs; no census of distinct union downsets under alternative
decompositions is claimed.

Uniqueness and the 840 labelled STS(9) are prior design theory; see the
primary paper [Partitions of sets of designs on seven, eight and nine
points](https://www.sciencedirect.com/science/article/pii/S0378375896000663).
Their exact reproduction validates the coverage bridge and is not new
classification research. No imported classification corpus is used.

## 4. Two exact PSD algorithms

The first uses rational symmetric Schur elimination. Each positive diagonal
pivot is a congruence step. When all residual diagonals vanish, PSD holds
precisely when the residual is zero. Negative residual diagonals and
zero-diagonal nonzero entries are explicitly rejected.

The second computes integer characteristic-polynomial coefficients, without
Schur pivots. Multiply the rational symmetric input by its positive least
common denominator, obtaining integer A. Write

```
det(tI-A)=t^n+c_1 t^(n-1)+...+c_n.
B_0=I, H_k=A B_(k-1), c_k=-Tr(H_k)/k, B_k=H_k+c_k I.
```

This Faddeev-LeVerrier/Newton recurrence computes the stated coefficients,
with every integer division checked. Indeed the formal identity

```
d/dz det(I-zA) = -det(I-zA) Tr(A(I-zA)^(-1))
```

gives Newton's coefficient recurrence. Expanding the matrix recurrence gives
exactly its trace-of-powers sum. If B_k is zero, every later step is zero;
the code stops early only under that exact condition.

The coefficients of det(tI+A) are (-1)^k c_k. A real symmetric matrix is
PSD iff all are nonnegative. PSD implies this by expanding the product of
t+lambda_i. Conversely, a negative eigenvalue gives a positive root, which
a polynomial with nonnegative coefficients and positive leading term cannot
have. Real eigenvalues follow from separately checked symmetry. The largest
index with positive coefficient equals the rank of a PSD matrix.

Both methods give rank 60 for Q and rank 69 for 70I-Q in both cases. The
expected output records the integer scales and hashes of the regenerated
coefficient vectors, rather than bulky polynomial output. This is author
validation by two algorithms, not independent peer review. Four controls
reject a damaged weight, a missing triple and two non-PSD symmetric matrices;
a singular PSD example checks rank handling.

## 5. Products and separation from a partition template

Tensor any k normalized matrices from this cohort on disjoint supports.
Family size and star size are as in Section 1. Symmetry, row sums and support
are preserved. Each factor spectrum lies in [-rho,1], rho=17/53<1. Negative
product eigenvalues have magnitude at most rho and positive products are
at most one. The lower endpoint is attained exactly by one negative endpoint
factor and k-1 factors at their simple eigenvalue 1. Three or more negative
factors have smaller magnitude; any other positive factor is below one.
Hence its multiplicity is 10k, giving the rank formula.

This is the conditional tensor mechanism credited in
[CAPPED_PROOF.md, Section 5](CAPPED_PROOF.md) and **six-downset-1**'s
[structural proof](https://github.com/helgithorskarp/math_results/blob/main/spectral_downsets_structural_certificates/PROOF.md).
No exponentially large tensor is generated.

A single-partition certificate with s disjoint classes has nonempty principal
Q block s*[same class]. Here 69 members in 17 classes force a class of size
at least five, giving a principal eigenvalue at least 85>70. Every such
certificate therefore fails the upper cap. This also holds for each product:
N_k modulo s_k equals 2*70^(k-1), neither zero nor one, so
ceil((N_k-1)/s_k)>N_k/s_k. This excludes that template only.

Ordinary partitions do exist for the base family. Each STS(9) has four
parallel classes of three triples, by its affine relabelling. The two systems
give eight classes. For c in Z/9Z, the singleton {c} and four pairs
{c+i,c-i}, i=1,...,4, give nine further disjoint classes covering all singletons
and pairs. These 17 classes, eight of size three and nine of size five, are
exactly checked. Their standard partition certificate has empty diagonal
Q=289>70. It is an uncapped ordinary H baseline, not the new construction.

## 6. Reproduction and scope

From the repository root, with Python 3.11+ and only the standard library:

```sh
OPENBLAS_NUM_THREADS=1 OMP_NUM_THREADS=1 MKL_NUM_THREADS=1 \
  python3 spectral_downsets_steiner_triples/verify_two9.py --check
```

Fixed data: [two9_certificates.json](two9_certificates.json).
Compact deterministic outputs: [two9_expected.json](two9_expected.json).
Measured with CPython 3.11.2: 12.98 seconds and 21,564 KiB RSS, one process.
No solver, floating-point tolerance or external census enters the proof.
Discovery used numerical projections followed by rational recovery; the
private search output is not a premise of this proof.

Primary target: [Ellis–Filmus–Friedgut, Section
4](https://arxiv.org/html/2609.28404v1#S4), rechecked 2026-09-30, v1 only.
The earlier ordinary union certificate is [PROOF.md](PROOF.md); the universal
capped single-system construction is [CAPPED_PROOF.md](CAPPED_PROOF.md).
This theorem adds the cap for every two-system union at order nine. General H,
arbitrary regular triple designs, higher-order two-system unions and unions
of three or more systems are not resolved here.
