# Six two-intersection links and their eight-block obstruction

## Statement

Let `A` consist of twelve five-subsets of a twelve-point set. Assume that
every point belongs to five members, every pair of points is covered, and
distinct members intersect in at most two points. Then:

1. There are exactly six isomorphism classes of such families, where an
   isomorphism permutes points and the family is unordered.
2. The triples not covered by `A` cannot be covered by eight six-subsets.

The second assertion allows arbitrary additional six-subsets: it imposes no
point-degree, pair-degree, intersection, or symmetry constraints on them.
Repeated additional blocks cannot help. An upper bound of nine is **not**
asserted.

This is an exact computer-assisted theorem. The finite computation is the
cycle classification below plus an exhaustive check of six small integer
weight certificates. No solver result is a premise of the proof.

## 1. Disjoint rows are impossible

Suppose two members of `A` are disjoint. Their union has ten points; call the
other two points `u,v`. Each of the other ten five-subsets meets each of
the disjoint members in at most two points, so contains at least one of
`u,v`. The two points have total degree ten, and the first two members
contain neither. Therefore every remaining member contains exactly one of
`u,v`. The pair `{u,v}` is uncovered, a contradiction.

Hence every row intersection is either one or two.

## 2. Both deficit graphs are unions of cycles

Write `X` for the square binary incidence matrix. Its row and column sums
are five. Define a graph `D` on the rows by joining rows that intersect in
one point. A fixed row has total intersection `5*4=20` with the other
eleven rows. Relative to the value two, its deficit is `22-20=2`.
Consequently `D` is a simple 2-regular graph and

\[
XX^t=3I+2J-D. \tag{1}
\]

All eigenvalues of `D` lie in `[-2,2]`, so `3I-D` is positive definite.
Thus `X` is invertible. Put

\[
E=3I+2J-X^tX.
\]

Regularity gives `JX=XJ=5J`, and therefore `DX=XE`. Thus `D` and `E`
are similar. The matrix `E` has integral entries, zero diagonal, and row
sum two. Furthermore

\[
\sum_{i,j}E_{ij}^2=\operatorname{tr}(E^2)
=\operatorname{tr}(D^2)=24=\sum_{i,j}E_{ij}.
\]

Every integer `z` satisfies `z(z-1)>=0`; equality in this sum forces each
entry of `E` to be zero or one. Thus `E` is also a simple 2-regular graph,
and every point pair has multiplicity one or two in `A`.

There are nine partitions of twelve into parts at least three. Their cycle
unions have distinct characteristic polynomials. The checker computes
these polynomials by the recurrence

\[
P_0(x)=2,\quad P_1(x)=x,\quad
P_n(x)=xP_{n-1}(x)-P_{n-2}(x),
\]

with `det(xI-A(C_n))=P_n(x)-2`, and takes products over components.
The identity follows either from the two roots of `t^2-xt+1` or by
diagonalizing the cycle using roots of unity. The separate audit checks
all nine degree-twelve polynomials at thirteen distinct integers by
fraction-free determinants of the explicit twelve-by-twelve matrices.
Hence `D` and `E` have the same component lengths. Relabel rows and columns
so that both equal the standard ordered union of these cycles. Now

\[
DX=XD. \tag{2}
\]

On the all-ones vector `3I-D` has eigenvalue one; adding `2J` changes only
this eigenvalue, to twenty-five. Equation (1) consequently gives

\[
(\det X)^2=25\det(3I-D).
\]

The determinant on the right, after division by twenty-five, must be a
square. The complete check is:

| Cycle lengths | `det(3I-D)` | Square? |
|---|---:|:---:|
| 3,3,3,3 | 65536 | yes |
| 3,3,6 | 81920 | no |
| 3,4,5 | 87120 | no |
| 3,9 | 92416 | yes |
| 4,4,4 | 91125 | no |
| 4,8 | 99225 | yes |
| 5,7 | 101761 | yes |
| 6,6 | 102400 | yes |
| 12 | 103680 | no |

## 3. Component row sums

Let the component lengths be `n_1,...,n_s`. Let `a_ij` be the number of
ones in a row of row-component `i`, restricted to column-component `j`.
This does not depend on the particular row: (2) sends a column-component
indicator, a 2-eigenvector, to another 2-eigenvector, which is constant on
each connected row-component. The analogous column sum is

\[
b_{ij}=n_i a_{ij}/n_j.
\]

Therefore the `a_ij` are integers with `0<=a_ij<=min(5,n_j)`, row sum five,
and integral `b_ij` with column sum five. Summing (1) over a row-component
also gives, for each `i,k`,

\[
\sum_j a_{ij}b_{kj}=2n_k+\mathbf1_{i=k}. \tag{3}
\]

The code exhausts these small integer possibilities. Up to permuting equal
column-components, the only quotient matrices are

```
3+3+3+3:  J_4 + I_4,
3+9:      [[2,3],[1,4]],
4+8:      [[1,4],[2,3]],
6+6:      [[2,3],[3,2]].
```

There is no quotient for `5+7`: integrality makes the number of ones from a
row in the five-cycle into the seven-cycle a multiple of seven, hence zero.
Its other count is five, contradicting the diagonal equation (3), which
would require `25=11`.

For `3+3+3+3`, a row of the quotient has sum five and square-sum seven, hence
one entry two and three entries one. The column sums make the positions of
the twos a permutation matrix. For `3+9` divisibility fixes the displayed
matrix. For `4+8`, the first diagonal entry is one or three, and (3) selects
one. For `6+6`, the first row is `(a,5-a)` with square-sum thirteen, giving
`a=2` or `3`, interchanged by swapping the column-components. These arguments
also explain all quotient normalizations used by the enumeration.

## 4. Complete, small cycle enumeration

Consider consecutive rows `r_0,r_1,...` on a row-cycle. Equation (2) says

\[
r_{i+1}=r_iD-r_{i-1}. \tag{4}
\]

For each row-component, the code lists **every** binary first row having
the required counts in the column-components and every such second row
intersecting it in one point. Equation (4) determines all later rows.
Retain the sequence exactly when all entries are binary, it closes with
`r_m=r_0, r_{m+1}=r_1`, and all row intersections have their required values.
Thus no possible cycle block can be omitted.

The counts of ordered candidate cycle blocks are:

| Cycle lengths | Candidate blocks for each row-component |
|---|---|
| 3,3,3,3 | 1296,1296,1296,1296 |
| 3,9 | 36,216 |
| 4,8 | 0,0 |
| 6,6 | 288,288 |

To shorten the remaining product, quotient the first cycle block by the
product of the column-cycle dihedral groups, without exchanging components.
The code explicitly generates the orbit of each selected first block and
removes exactly those candidates. This leaves respectively one, one, zero,
and two representatives. Every column action preserves the quotient and the
set of possible remaining blocks, so this loses no full matrix.

For each chosen first block, enumerate every compatible choice of remaining
cycle blocks; rows in distinct components must intersect in two points.
The complete results are:

| Cycle lengths | Ordered assemblies | Unordered row sets after the first-block normalization |
|---|---:|---:|
| 3,3,3,3 | 4752 | 22 |
| 3,9 | 36 | 2 |
| 4,8 | 0 | 0 |
| 6,6 | 24 | 2 |

These twenty-six row sets exhaust the problem modulo the explicitly
described label changes. They are not asserted to be all labeled designs.

## 5. Exactly six classes

The certificate gives four representatives with column deficit graph
`4C_3`, one with `C_3+C_9`, and one with `2C_6`. They are checked directly
against the definition. Any point isomorphism must preserve the column
deficit graph. Its full automorphism group consists of independent dihedral
actions on the cycles, together with permutations of equal-length cycles.

The verifier exhausts this group for each representative and sorts the
transformed rows. The resulting point-label orbit sizes, in certificate
order, are

```
4C_3:      216, 1296, 1944, 1296;
C_3+C_9:   12;
2C_6:      24.
```

The four first orbits are pairwise disjoint, and contain respectively
`1,6,9,6` of the twenty-two normalized row sets. The last two orbits each
contain both normalized row sets of their type. Distinct cycle types cannot
be isomorphic. This proves existence, exhaustiveness, and pairwise
nonisomorphism without trusting a graph-isomorphism package.

## 6. Integer weights exclude eight additional blocks

For each representative the certificate assigns nonnegative integer weights
`w(T)` to some triples not covered by `A`; unlisted triples have weight zero.
Let their sum be `W`. It supplies a positive integer `M` such that

\[
\sum_{T\subseteq B}w(T)\le M
\quad\hbox{for every six-subset }B,\qquad W>8M. \tag{5}
\]

The checker verifies all 924 possible six-subsets, not just selected
candidate blocks. If eight six-subsets covered the missing triples, summing
their weighted capacities would yield `W<=8M`, contrary to (5). Transport
the weights by any point isomorphism to obtain the obstruction for every
classified family. All arithmetic here is integral.

Each family covers exactly 120 different triples, since a repeated triple
would force a row intersection at least three. There are exactly 100 missing
triples. The certificate totals and capacities are:

| Case | `W` | `M` | `W-8M` |
|---|---:|---:|---:|
| 3_3_3_3:0 | 216 | 24 | 24 |
| 3_3_3_3:1 | 852 | 98 | 68 |
| 3_3_3_3:2 | 835 | 98 | 51 |
| 3_3_3_3:3 | 829 | 97 | 53 |
| 3_9:0 | 850 | 98 | 66 |
| 6_6:0 | 833 | 96 | 65 |

The same table is checked in `EXPECTED.json`. The upper search for
nine additional blocks was inconclusive in some classes and is not proof
evidence. No exact residual optimum is claimed.

## 7. Consequence for C(13,6,3)

Suppose twenty six-subsets cover the triples of a thirteen-set and the point
degrees are `(12,9^12)`. Let `h` be the degree-twelve point. Delete `h` from
its twelve incident blocks to obtain `A`; the other eight blocks form `B`.

Use the previously proved optimal-link theorem: every point in a nine-block
`(12,5,2)` covering has degree at most five. At each low point `p`, its link
is such a nine-block covering, so the codegree of `{h,p}` is at most five.
The twelve codegrees sum to `12*5=60`, so they are all five. Thus `A` is
five-regular and covers every low pair. If its maximum row intersection
were two or less, the theorem above would require at least nine away blocks,
contradicting `|B|=8`.

Consequently two blocks through `h` share at least three low points, or at
least four original points including `h`. In the predecessor's notation,
`k=max |A_i intersection A_j|` belongs to `{3,4}`, eliminating the complete
`k=2` row of its nine-class frontier. The maximum cannot be five because
repeated blocks could be removed to give a nineteen-block covering,
contradicting the known lower bound twenty.

This does not exclude the whole degree profile, either other degree profile,
or settle the global covering number.

## Trust boundary

The main theorem uses the written reductions, complete finite loops in
`classify.py`, the direct checks in `verify.py`, Python integer semantics,
and the runtime/hardware. `audit.py` independently checks the spectral data
and all six weight obstructions; it does not independently reproduce the
cycle enumeration. The consequence additionally imports the optimal-link
degree bound and the lower bound twenty. No SAT verdict, floating-point LP
answer, graph canonicalizer, downloaded dataset, or large generated file is
needed to run the main proof checker. Independent external review remains
pending.
