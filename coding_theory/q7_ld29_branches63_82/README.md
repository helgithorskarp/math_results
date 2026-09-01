# Leaf-aware family bounds on the 9-edge `Q_7` LD29 frontier

## Analytic result

Let `C` be an exact 29-word locating-dominating code in the binary
7-cube after the lossless orphan normalization

```text
0 in C;
e_i not in C                         (0 <= i < 7);
e_0+e_j not in C                     (1 <= j < 7).
```

Let `H` be the graph on directions `1,...,6`, with `ij` selected exactly
when `e_i+e_j` is a codeword.  The 20 canonical admissible nine-edge
graphs are branches 63--82.  In the Honkala--Laihonen--Ranto family
partition, let

$$
D=\sum_F (|I(f_F)|-2)
$$

be the total family defect.  Then

$$
D\geq24
$$

holds in every branch except 75.  In branch 75 the method gives

$$
D\geq23.
$$

Fathers of defect six are permitted, so the statement applies to arbitrary
exact 29-codes, including codes obtained by augmenting a hypothetical
smaller code.  The consequences used in the finite search are

$$
\begin{array}{c|cccc}
&p& a&b=29-a&e(Q_7[C])\\\hline
D\geq23&\geq47&\geq18&\leq11&\leq E_7(11)=17\\
D\geq24&\geq48&\geq19&\leq10&\leq E_7(10)=15.
\end{array}
$$

Here `p` is the number of singleton identifying sets and `a` is the number
of isolated codewords.

## Local fathers, leaves, and forced son slots

A direction of degree at least two in `H` is a father.  A degree-one
direction is a son of its unique neighboring father: the admissibility
condition excludes two-vertex components.  If `l` is the number of leaves,
the local fathers consume exactly

$$
\sum_{i:\deg(i)\geq2}(\deg(i)-1)
=(18-l)-(6-l)=12
$$

defect units in every nine-edge branch.

For a defect-`d` father, the maximum family capacity (father plus sons) is

$$
h(d)=1+\binom{d+2}{2},
$$

so

```text
d       1   2   3   4   5   6
h(d)    4   7  11  16  22  29.
```

Let `F` be the father vertices and let

$$
L=\sum_{i\in F}h(\deg_H(i)-1).
$$

Every edge of `H[F]` forces two absent oriented son slots: in the family of
`e_i`, the second common neighbor belonging to the slot
`{0,e_i+e_j}` is the other father `e_j`.  Every triangle forces two more
absent slots, since its weight-three vertex is the candidate for three
different family slots but can be a son of at most one father.  These slots
are distinct, giving

$$
\Delta\geq2|E(H[F])|+2t(H).
$$

The complete canonical data are:

| branch | mask | sorted degrees | triangles | `L` | forced `Delta` | bound on `D` |
|---:|---:|:---|---:|---:|---:|---:|
| 63 | 511 | `(2,2,2,2,5,5)` | 4 | 48 | 26 | 24 |
| 64 | 767 | `(1,2,3,3,4,5)` | 5 | 45 | 26 | 24 |
| 65 | 959 | `(2,2,2,3,4,5)` | 4 | 46 | 26 | 24 |
| 66 | 1022 | `(2,2,3,3,4,4)` | 2 | 44 | 22 | 24 |
| 67 | 1759 | `(1,3,3,3,3,5)` | 4 | 44 | 24 | 24 |
| 68 | 1783 | `(1,2,3,4,4,4)` | 5 | 44 | 26 | 24 |
| 69 | 1789 | `(1,3,3,3,4,4)` | 4 | 43 | 24 | 24 |
| 70 | 1887 | `(2,2,3,3,3,5)` | 4 | 45 | 26 | 24 |
| 71 | 1915 | `(2,2,2,4,4,4)` | 4 | 45 | 26 | 24 |
| 72 | 1917 | `(2,2,3,3,4,4)` | 3 | 44 | 24 | 24 |
| 73 | 2013 | `(2,2,3,3,4,4)` | 3 | 44 | 24 | 24 |
| 74 | 2014 | `(2,3,3,3,3,4)` | 2 | 43 | 22 | 24 |
| 75 | 4060 | `(3,3,3,3,3,3)` | 0 | 42 | 18 | 23 |
| 76 | 5875 | `(1,3,3,3,4,4)` | 5 | 43 | 26 | 24 |
| 77 | 5919 | `(2,2,3,3,3,5)` | 5 | 45 | 28 | 24 |
| 78 | 5943 | `(2,2,3,3,4,4)` | 4 | 44 | 26 | 24 |
| 79 | 5949 | `(2,3,3,3,3,4)` | 3 | 43 | 24 | 24 |
| 80 | 5950 | `(2,2,3,3,4,4)` | 4 | 44 | 26 | 24 |
| 81 | 6010 | `(2,3,3,3,3,4)` | 3 | 43 | 24 | 24 |
| 82 | 7100 | `(3,3,3,3,3,3)` | 2 | 42 | 22 | 24 |

For total defect `D`, the family identities are

$$
p=24+D,\qquad M=104-D-2q,
\qquad a\geq D-5,\qquad 2q\leq34-D.
$$

Let `G(r)` be the largest capacity obtainable from `r` additional defect
units using the displayed `h(d)` values.  For each row, each `D` below the
claimed bound, and every permitted `q`, exact dynamic programming gives

$$
L+G(D-12)-M<2|E(H[F])|+2t(H),
$$

contradicting the forced-slot lower bound, except for a short `D=23`
capacity frontier in eight branches.  There the remaining defect has
maximum capacity only as `(6,5)`, and omitting defect six loses three
capacity units.  If `s` is the capacity slack over the forced local slots,
then `s<=2`.  A defect-six father `f` has `I(f)=N[f]`.  Its seven slots
`{f,c}` can only have the adjacent codeword `c` as son, so at most `s`
missing slots put at least `8-s` codewords in that family.  This exceeds
the global bound

$$
29-(D-5)-2q
$$

on codewords belonging to families.  This eliminates `D=23` in all eight
cases.  Branch 75 has a second-best `(5,5,1)` capacity case and is the sole
exception.  The standard-library program
`verify_local_defect23.py` reconstructs the 115 canonical graph orbits,
every table entry, all capacity cases, and the edge-isoperimetric values.

## Exact finite certificates

The first three nine-edge branches, 63--65, are also impossible.  Thus no
locating-dominating code of cardinality at most 29 has one of these three
canonical orphan-local graphs.

Each deterministic formula contains exact domination and distance-two
separation, cardinality 29, the orphan normalization, all 15 local units,
biconditional indicators, `p+b<=58`, and the proved branch-specific
singleton, nonisolation, and induced-edge bounds.  Repeated literals are
removed clausewise.  Every formula has 10,432 variables and 183,619 clauses.

CaDiCaL 1.5.3 emitted a plain-text DRAT proof for each formula.  DRAT-trim
`0.0~git20240428.effa1dc-2` independently returned `s VERIFIED`; none of
the checked cores uses a RAT lemma.

| branch | CNF SHA-256 | proof bytes | DRAT SHA-256 | core lemmas |
|---:|:---|---:|:---|---:|
| 63 | `b7bb7daa54a9867bb412501504847553f251ea045d224edb0ef9fcb5a36b7ca7` | 248,176,278 | `cb78b6c6ccef819019258569c08b9d2c963b4e5bebc641b663ec595fa1d1fde6` | 956,034 |
| 64 | `264afff56486ad1588bfb4d64455d08b7672611df99e601c5fc72322138425c3` | 338,200,651 | `e2ada6bfaba71da6344409ec523b2355ce8a79c19bc3b10aca307817319fd8d3` | 1,391,872 |
| 65 | `43eca752ef184f70432bb21e801c47309507a12732e095587df3250eee2958ed` | 651,346,783 | `fd369f31772fff1354e7b826b94b285e80851f7173ce51c74cb87a773b6d6efb` | 2,769,209 |

`verify_branches63_82.py` records and regenerates all 20 deterministic CNF
hashes, but the finite exclusion asserted here is deliberately limited to
branches 63--65.  Branches 66--82 remain for subsequent certificate runs.
CNFs, solver output, and proof traces remain under `/scratch` and are not
committed.

## Reproduction

```bash
python3 verify_local_defect23.py

python3 -m venv /scratch/q7-ld29-d23-venv
/scratch/q7-ld29-d23-venv/bin/pip install -r requirements.txt
/scratch/q7-ld29-d23-venv/bin/python verify_branches63_82.py \
  --write-directory /scratch/q7-ld29-d23-cnfs
```

For each certified branch `b` in `63,64,65`:

```bash
cadical -q --binary=false \
  /scratch/q7-ld29-d23-cnfs/branch-${b}.cnf \
  /scratch/q7-ld29-d23-branch-${b}.drat

drat-trim \
  /scratch/q7-ld29-d23-cnfs/branch-${b}.cnf \
  /scratch/q7-ld29-d23-branch-${b}.drat -w
```

The reported environment used Python 3.11.2,
`python-sat[pblib]==1.9.dev15`, CaDiCaL 1.5.3, and DRAT-trim
`0.0~git20240428.effa1dc-2`.

## Scope, trust boundary, and novelty

The hand theorem depends on the Honkala--Laihonen--Ranto family partition,
elementary cube geometry, and the finite capacity calculation.  The finite
exclusions additionally depend on the reviewed orphan-local reduction, the
deterministic exact encoding, PySAT cardinality encodings, and DRAT-trim.
DRAT proves only the three hashed formulas; the analytic bridge is separate.

The family method is from I. Honkala, T. Laihonen, and S. Ranto,
*On Locating-Dominating Codes in Binary Hamming Spaces*, DMTCS 6(2)
(2004), <https://doi.org/10.46298/dmtcs.322>.  The published small-dimension
context is V. Junnila, T. Laihonen, and T. Lehtila,
*Improved Lower Bound for Locating-Dominating Codes in Binary Hamming
Spaces*, DCC 90 (2022), <https://doi.org/10.1007/s10623-021-00963-8>.
The latter improves the general lower bound only from dimension ten and
reported `28 <= gamma^LD(Q_7) <= 32`.

Targeted primary-source and graph searches through 2026-09-01 found no
leaf-aware defect-24/23 specialization for the nine-edge frontier or checked
certificates for branches 63--65.  These are apparently new relative to the
searched sources; no historical-priority claim is made.
