# A branchwise family-defect ladder for the lower `Q_7` LD29 frontier

## Result

Consider an exact 29-word locating-dominating code `C` in the binary
7-cube after the lossless orphan normalization

```text
0 in C;
e_i not in C                         (0 <= i < 7);
e_0+e_j not in C                     (1 <= j < 7).
```

Let `H` be the graph on directions `1,...,6`, with `ij` selected exactly
when `e_i+e_j` is a codeword.  Branches 0--62 are precisely the canonical
admissible local graphs with four through eight edges.  In the
Honkala--Laihonen--Ranto family partition, write

$$
D=\sum_F (|I(f_F)|-2)
$$

for the total family defect.  Combining the universal predecessor bound
`D>=18` with the branchwise local collisions and new near-full
defect-six/defect-five occupancy tests gives the following exact ladder.

| proved bound | canonical branches | count |
|---:|:---|---:|
| `D>=18` | 0--4, 6 | 6 |
| `D>=19` | 5, 7, 8, 10 | 4 |
| `D>=20` | 9, 11--20, 24 | 12 |
| `D>=21` | 21--23, 25--28, 31, 33--36, 39 | 13 |
| `D>=22` | 29, 30, 32, 37, 38, 40--42, 44, 47, 50--52, 57, 58 | 15 |
| `D>=23` | 43, 45, 46, 48, 49, 53--56, 60--62 | 12 |
| `D>=24` | 59 | 1 |

Thus 57 of the 63 lower-frontier branches have a strictly stronger bound
than the previous universal theorem.  These are structural search bounds,
not exclusions of the branches and not a proof that a size-29 code is
impossible.

For a row with bound `D>=d`, the standard family identities imply

$$
p\geq24+d,\qquad a\geq d-5,\qquad b=29-a\leq34-d.
$$

The binary edge-isoperimetric recurrence then bounds the induced code
edges as follows.

| `d` | `p` | `a` | `b` | `e(Q_7[C]) <= E_7(b)` |
|---:|---:|---:|---:|---:|
| 18 | 42 | 13 | 16 | 32 |
| 19 | 43 | 14 | 15 | 28 |
| 20 | 44 | 15 | 14 | 25 |
| 21 | 45 | 16 | 13 | 22 |
| 22 | 46 | 17 | 12 | 20 |
| 23 | 47 | 18 | 11 | 17 |
| 24 | 48 | 19 | 10 | 15 |

## Local collision count

Let `F` be the vertices of `H` of degree at least two.  These directions
are fathers; every degree-one direction is a son of its unique neighboring
father because admissibility excludes two-vertex components.  If `H` has
`m` edges, the local fathers use exactly

$$
d_0=\sum_{i\in F}(\deg_H(i)-1)=2m-6
$$

defect units and have maximum total family capacity

$$
L=\sum_{i\in F}h(\deg_H(i)-1),\qquad
h(d)=1+\binom{d+2}{2}.
$$

Every edge of `H[F]` forces two absent oriented son slots.  Every triangle
forces two further absent slots because its weight-three candidate occurs
in three distinct father slots but can belong to at most one family.  The
forced local deficit is therefore

$$
\delta_0=2|E(H[F])|+2t(H).
$$

All these local family members are noncodewords: the normalized
weight-one vertices are absent from `C`, and a weight-three son whose
I-set is a pair of weight-two words cannot itself be a codeword.

## Near-full high-defect obstructions

For any exact 29-code, with `q` codeword couples and `M` family vertices,

$$
p=24+D,\qquad M=104-D-2q,
\qquad a\geq D-5,\qquad 2q\leq34-D.
$$

After accounting for the local fathers, distribute the remaining
`D-d_0` defect units into a multiset `P` of parts in `{1,...,6}`.  Its
largest possible extra family capacity is `sum(h(d): d in P)`, so the
total number of absent son slots is at least determined by

$$
\Delta=L+\sum_{d\in P}h(d)-M.
$$

Any state with `Delta<delta_0` is impossible.  Put
`s=Delta-delta_0`.  The local forced slots and all other-family slots are
disjoint, so at most `s` missing slots remain available to the high-defect
families.

A defect-six father has an I-set of size eight, hence its entire closed
neighborhood consists of codewords and the father is itself a codeword.
Its seven slots pairing the father with a neighboring codeword can only
have that neighboring codeword as son.  Consequently `k` defect-six
families contain at least

$$
8k-s
$$

codewords.

There is a complementary defect-five test.  An `F_7` father covered by
seven codewords may itself be a codeword or a noncodeword.

- If it is a codeword and its family is missing `t` slots, the father and
  its six adjacent-pair slots force at least `7-t` nonisolated family
  codewords.
- If it is a noncodeword, its seven neighbors are codewords.  A neighbor
  is isolated whenever all six family slots incident with it are present,
  so `t` missing slots leave at least `7-2t` guaranteed isolated codewords.

These guaranteed isolated sets may be added over distinct noncodeword
`F_7` fathers.  Two such radius-one balls can share codewords only when
their centers are at distance two.  Then the shared codewords form the
pair whose other common neighbors are the two fathers, so that slot is
missing in both families and the shared words have already been removed
from both guaranteed sets.

The verifier exhausts which defect-five fathers are codewords and every
allocation of the `s` remaining missing slots.  Forced family codewords
are nonisolated, so together with forced isolated words and the `2q`
couple codewords they cannot exceed 29.  Independently, isolated codewords and the `2q` codewords
in couples lie outside all families, so the total number of family
codewords is at most

$$
29-(D-5)-2q=34-D-2q.
$$

The verifier exhausts every `D` below each displayed bound, every permitted
`q`, and every integer partition `P`.  Each state fails either raw capacity,
the forced local deficit, or a high-defect occupancy inequality.  It also
finds a surviving arithmetic state at the displayed bound; thus the table
states exactly what this method proves, without implying existence of a
code.

## Reproduction

The verifier uses only the Python standard library:

```bash
python3 verify_lower_frontier_bounds.py
```

It independently reconstructs all 115 admissible local-graph orbits under
`S_6`, checks the canonical masks and edge counts of branches 0--62,
recomputes every local defect/capacity/collision value, exhausts the full
integer frontier, and reconstructs the binary edge-isoperimetric values.

Reported environment:

```text
Python 3.11.2
verify_lower_frontier_bounds.py SHA-256:
acde98fb29c8673d57ceddc47b36e5b46a62a0cfa13ed542886e96fbaf0c4852
```

## Trust boundary, scope, and novelty

The hand theorem depends on the Honkala--Laihonen--Ranto family partition,
the predecessor's lossless orphan-local reduction and universal `D>=18`
theorem, and elementary Hamming-cube geometry.  Its finite component is a
small transparent enumeration of graphs and integer partitions.  No SAT
solver or external proof trace is used.

The family method originates in I. Honkala, T. Laihonen, and S. Ranto,
*On Locating-Dominating Codes in Binary Hamming Spaces*, DMTCS 6(2)
(2004), 265--282, <https://doi.org/10.46298/dmtcs.322>.  V. Junnila,
T. Laihonen, and T. Lehtila, *Improved Lower Bound for Locating-Dominating
Codes in Binary Hamming Spaces*, DCC 90 (2022), 67--85,
<https://doi.org/10.1007/s10623-021-00963-8>, improves the general lower
bound only from dimension ten and records the prior small-dimension
context.  Targeted primary-source and Discovery Net searches through
2026-09-01 found no branchwise defect ladder for these 63 canonical local
graphs.  The result is apparently new to the searched sources; no
historical-priority claim is made.
