# `K_{3,3}` family split and DRAT exclusion of `Q_7` LD29 branch 75

## Certified result

There is no locating-dominating code of cardinality at most 29 in the
binary 7-cube whose lossless orphan normalization has canonical local-graph
index 75.  Its mask is `4060`; the local graph is `K_{3,3}`, with parts
`{1,2,3}` and `{4,5,6}` in the canonical labeling.

This is a computer-assisted finite result.  A hand-checkable family split
reduces the only exceptional total-defect case to one labeled pair of
centers.  Two exact SAT formulas, both with checked DRAT certificates, then
cover that pair and every larger-defect case.  The result closes one finite
branch, not the complete size-29 problem.

## Family-defect split

Use the standard orphan normalization

```text
0 in C;
e_i not in C                         (0 <= i < 7);
e_0+e_j not in C                     (1 <= j < 7).
```

Let `H` be the graph on directions `1,...,6`, with `ij` selected exactly
when `e_i+e_j` is a codeword.  Let

$$
D=\sum_F (|I(f_F)|-2)
$$

be total Honkala--Laihonen--Ranto family defect, let `q` count codeword
couples, and let `M` count family vertices.  The standard identities and
inequalities are

$$
p=24+D,\qquad M=104-D-2q,\qquad
a\ge D-5,\qquad 2q\le34-D.
$$

The predecessor proves `D>=23` for branch 75.  All six vertices of the
local `K_{3,3}` are defect-two fathers, with total capacity 42.  Its nine
oriented edges force 18 missing local son slots, and it has no triangles.
Exact integer-partition enumeration followed by the defect-six occupancy
inequality leaves exactly one state at `D=23`:

```text
q=5, extra family defects=(1,5,5), free missing slots=1,
family-codeword budget=1.
```

### The two defect-five centers

Each defect-five father has seven codewords in its identifying set.  It
cannot itself be a codeword: its father--neighbor slots would put at least
six codewords in families, above the global budget one.  Hence both
defect-five fathers are noncodeword centers with all seven neighbors in
the code.

Only one missing family slot remains.  Elementary cube geometry gives the
following necessary classification for either center.

- Weights at most two are inconsistent with the normalization and the
  all-codeword neighborhood.
- A weight-three center would require a triangle in `H`; `K_{3,3}` has
  none.
- At weight four, each selected local edge inside the support costs a
  missing local-family slot.  Cost at most one is possible only when the
  center contains coordinate zero and the other three coordinates form one
  part of `K_{3,3}`; the cost is then zero.
- A weight-five center contains a selected local edge at distance three,
  forcing three missing predecessor slots.
- Weights six and seven have the safe lower-bound cost zero.

Thus exactly ten labeled center candidates remain: the two weight-four
part centers and all eight words of weight at least six.  Two such centers
must be at distance at least five.  Distance one is immediately impossible;
distances two and three force one missing slot in each family, and distance
four forces at least three.  Among the ten candidates, the sole pair at
distance at least five is

```text
(15,113),
```

the two weight-four part centers.  The verifier checks the complete
128-vertex classification directly.  No symmetry quotient or heuristic is
used in this reduction.

## Exact formulas and certificates

The exceptional formula uses the valid `D>=23` consequences

$$
p\ge47,\qquad b\le11,\qquad p+b\le58,
\qquad e(Q_7[C])\le17,
$$

and fixes centers 15 and 113 absent and all fourteen of their neighbors
present.  This is a relaxation of the unique family state.

The strong formula covers `D>=24` through

$$
p\ge48,\qquad b\le10,\qquad p+b\le58,
\qquad e(Q_7[C])\le15.
$$

Both formulas also contain exact domination of all 128 vertices, all
essential distance-two separation clauses, cardinality exactly 29, the
complete orphan normalization, the 15 local-graph units, and biconditional
singleton, nonisolation, and code-pair indicators.

| formula | variables | clauses | CNF SHA-256 | proof bytes | DRAT SHA-256 |
|:---|---:|---:|:---|---:|:---|
| `branch75-d23-f15-g113` | 10,432 | 183,635 | `c2847656e6d4774bfa7c46a740e8ce29a26f9d72875ac0dd1a6e0d168c21e262` | 754,041 | `59489771d4cec6b5bc218866802faec5f3845b62209db18409c37b0f37a926ac` |
| `branch75-d24` | 10,432 | 183,619 | `dae5dfbd19fb3cacb48ba5782bbcff6c86f331b70ea6cee530ef3aa48907555e` | 366,206,399 | `633521280ea1d3089d766e0418640905ea40739139e3b9376c757a6647c393ea` |

CaDiCaL 1.5.3 returned `UNSATISFIABLE` on both formulas.  DRAT-trim at git
commit `2e3b2dc0ecf938addbd779d42877b6ed69d9a985` independently returned
`s VERIFIED`:

| formula | core/total lemmas | resolution steps | RAT lemmas |
|:---|---:|---:|---:|
| `branch75-d23-f15-g113` | 318/10,036 | 10,692 | 0 |
| `branch75-d24` | 1,335,072/2,537,698 | 55,159,259 | 0 |

PySAT's independent Kissat 4.0.4 binding also returned UNSAT on freshly
rebuilt copies of both formulas.  Solver traces, checker logs, CNFs, and
DRAT files remain under `/scratch` and are deliberately not committed.

## Reproduction

Create an environment under `/scratch` and regenerate the exact formulas:

```bash
python3 -m venv /scratch/q7-ld29-branch75-venv
/scratch/q7-ld29-branch75-venv/bin/pip install -r requirements.txt
/scratch/q7-ld29-branch75-venv/bin/python verify_branch75_k33.py \
  --write-directory /scratch/q7-ld29-branch75
```

Produce and check each proof:

```bash
cadical -q --binary=false \
  /scratch/q7-ld29-branch75/branch75-d23-f15-g113.cnf \
  /scratch/q7-ld29-branch75/branch75-d23-f15-g113.drat
drat-trim \
  /scratch/q7-ld29-branch75/branch75-d23-f15-g113.cnf \
  /scratch/q7-ld29-branch75/branch75-d23-f15-g113.drat -w

cadical -q --binary=false \
  /scratch/q7-ld29-branch75/branch75-d24.cnf \
  /scratch/q7-ld29-branch75/branch75-d24.drat
drat-trim \
  /scratch/q7-ld29-branch75/branch75-d24.cnf \
  /scratch/q7-ld29-branch75/branch75-d24.drat -w
```

Run the independent solver check with

```bash
/scratch/q7-ld29-branch75-venv/bin/python \
  verify_branch75_k33.py --solve-kissat
```

Reported environment and source hashes:

```text
Python                          3.11.2
python-sat[pblib]               1.9.dev15
CaDiCaL Debian package          1.5.3-2
DRAT-trim git commit            2e3b2dc0ecf938addbd779d42877b6ed69d9a985
verify_branch75_k33.py SHA-256  03b9fd360b726edea6fafeac0a0523671245a94fa3457aa644f3a686a5695e74
requirements.txt SHA-256        639afc203e4b12224d62c9426902d5784099ba876c5ac2faed92e4659b56caca
```

## Trust boundary, scope, and novelty

The family split depends on the reviewed orphan normalization, the
Honkala--Laihonen--Ranto partition, the preceding `D>=23` theorem, and the
stated elementary Hamming-cube arguments.  The finite center classification
is reconstructed exhaustively from transparent code.  The exact exclusions
add the deterministic SAT encoding, PySAT totalizers, Python, CaDiCaL, and
DRAT-trim to the trust boundary.  DRAT establishes unsatisfiability only for
the two hashed formulas; the analytic bridge from a hypothetical code to
those formulas is separate.

The family method is from I. Honkala, T. Laihonen, and S. Ranto,
*On Locating-Dominating Codes in Binary Hamming Spaces*, DMTCS 6(2)
(2004), 265--282, <https://doi.org/10.46298/dmtcs.322>.  The published
small-dimension context is V. Junnila, T. Laihonen, and T. Lehtila,
*Improved Lower Bound for Locating-Dominating Codes in Binary Hamming
Spaces*, Designs, Codes and Cryptography 90 (2022), 67--85,
<https://doi.org/10.1007/s10623-021-00963-8>, which records the published
dimension-seven interval `28 <= gamma^LD(Q_7) <= 32`.

Targeted primary-source and refreshed Discovery Net searches through
2026-09-01 found no `K_{3,3}` family split or exact branch-75 certificate.
This result is apparently new relative to the searched sources, not a
historical-priority claim.
