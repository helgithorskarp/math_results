# Full-family distance rigidity raises five `Q_7` LD29 branches to `D>=23`

## Theorem

Let `C` be an exact 29-word locating-dominating code in the binary 7-cube
after the established lossless orphan normalization

```text
0 in C;
e_i not in C                         (0 <= i < 7);
e_0+e_j not in C                     (1 <= j < 7).
```

Let `H` be the local graph on directions `1,...,6`, with `ij` selected
exactly when `e_i+e_j` is a codeword, and let

$$
D=\sum_F (|I(f_F)|-2)
$$

be the total Honkala--Laihonen--Ranto family defect.  If `H` has any of the
following five canonical indices, then

$$
\boxed{D\geq23}.
$$

| branch | mask | sorted degrees | triangles | local capacity | forced deficit |
|---:|---:|:---|---:|---:|---:|
| 44 | 703 | `(1,2,2,3,3,5)` | 3 | 38 | 20 |
| 47 | 766 | `(1,2,3,3,3,4)` | 2 | 36 | 18 |
| 50 | 957 | `(2,2,2,2,4,4)` | 2 | 38 | 20 |
| 52 | 1751 | `(1,2,3,3,3,4)` | 2 | 36 | 18 |
| 57 | 1916 | `(2,2,3,3,3,3)` | 1 | 36 | 18 |

This raises the preceding branchwise bound from `D>=22` in all five cases.
It implies, branchwise,

$$
p\ge47,\qquad a\ge18,\qquad b=29-a\le11,
\qquad e(Q_7[C])\le E_7(11)=17.
$$

The theorem is a structural search refinement, not an exclusion of these
five branches and not a proof that a 29-word code is impossible.

## Unique defect-22 frontier

The six local fathers use ten defect units.  The standard family identities
are

$$
p=24+D,\qquad M=104-D-2q,
\qquad a\ge D-5,\qquad 2q\le34-D.
$$

For each of the five local graphs, exact integer-partition enumeration shows
that every state with `D<=21` fails capacity.  At `D=22`, the
defect-six occupancy inequality eliminates all but one state:

```text
q=6,
extra family defects=(1,1,5,5),
missing slots beyond the local forced slots=0,
family-codeword budget=34-D-2q=0.
```

Thus the state contains two full defect-five families.  Neither father is a
codeword, because no codeword lies in any family.  Each father is therefore
a noncodeword whose seven neighbors are codewords and whose 21 sons are all
present.

## Full-family center geometry

Two full noncodeword defect-five fathers have mutual Hamming distance at
least five.  At distances one through four, respectively, one center is a
required codeword neighbor of the other; one is a two-codeword son of the
other despite having seven codeword neighbors; a codeword neighbor of one
is a distance-two son of the other; or a codeword neighbor of one lies at
distance three from the other.  The last case is impossible because every
distance-three word from a full center is noncodeword: if selected, it would
add itself to the signatures of three full-family sons.

The zero-slack center candidates are also finite and transparent.

- Weights at most two are excluded by the fixed normalization and the
  all-codeword neighborhood requirement.
- A weight-three center would be a triangle of `H`.  As a separate father it
  occupies none of the triangle's three local son slots, whereas the local
  collision count charged only two missing slots.  It therefore consumes an
  unavailable extra slot.
- For a weight-four center, any selected local edge in its non-orphan support
  would be a codeword at distance two.  Its two common neighbors with the
  center are isolated codewords but adjacent to that selected local word, a
  contradiction.  Hence the non-orphan support must be independent in `H`.
- Every graph in the table has independence number three.  A weight-five
  center supports a selected local edge, producing a selected word at
  distance three, which a full family forbids.
- Weights six and seven remain as candidates.

Direct enumeration gives the following complete candidate sets, with words
encoded as integers from 0 through 127:

```text
branch 44: 63 85 95 105 111 113 119 123 125 126 127
branch 47: 63 95 105 111 113 119 123 125 126 127
branch 50: 63 95 105 111 113 119 123 125 126 127
branch 52: 63 77 95 111 113 119 123 125 126 127
branch 57: 63 95 111 113 119 123 125 126 127
```

In every row the maximum distance between two candidates is four.  The two
required centers therefore cannot coexist, contradicting `D=22` and proving
`D>=23`.

## Reproduction

The verifier uses only Python's standard library.  It digest-pins the
reviewed predecessor ladder, independently reconstructs all 115 admissible
local-graph orbits under `S_6`, recomputes each local invariant and every
integer-partition state through defect 22, classifies all 128 possible
centers, and checks all candidate-pair distances.

```bash
python3 verify_five_branch_d23.py
```

Reported environment:

```text
Python 3.11.2
verify_five_branch_d23.py SHA-256:
08183ecd8deb3cb83a59b0e88e483d3ca0838bda24b1e28179d54cdaa0e6ce73
reviewed predecessor verifier SHA-256:
acde98fb29c8673d57ceddc47b36e5b46a62a0cfa13ed542886e96fbaf0c4852
```

## Trust boundary, scope, and novelty

The theorem depends on the Honkala--Laihonen--Ranto family partition, the
reviewed orphan-local reduction, the reviewed branchwise defect ladder, and
elementary Hamming-cube geometry.  Its computational component is exhaustive
standard-library enumeration of integer partitions, six-vertex graphs, and
128 cube vertices.  No SAT solver or external certificate is used.

The family method originates in I. Honkala, T. Laihonen, and S. Ranto,
*On Locating-Dominating Codes in Binary Hamming Spaces*, DMTCS 6(2)
(2004), 265--282, <https://doi.org/10.46298/dmtcs.322>.  V. Junnila,
T. Laihonen, and T. Lehtila, *Improved Lower Bound for Locating-Dominating
Codes in Binary Hamming Spaces*, DCC 90 (2022), 67--85,
<https://doi.org/10.1007/s10623-021-00963-8>, improves the general lower
bound only from dimension ten and records the earlier small-dimension
context.

Targeted primary-source and refreshed Discovery Net searches through
2026-09-01 found no full-family distance specialization for these five
canonical branches.  The simultaneous `D>=23` refinement is apparently new
to the searched sources; no absolute historical-priority claim is made.
