# Center-split certificates raise five `Q_7` LD29 branches to `D>=24`

## Certified result

Let `C` be an exact 29-word locating-dominating code in the binary 7-cube,
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

be the total Honkala--Laihonen--Ranto family defect.  If `H` has canonical
index 44, 47, 50, 52, or 57, then

$$
\boxed{D\geq24}.
$$

| branch | mask | sorted degrees | triangles | local capacity | forced deficit |
|---:|---:|:---|---:|---:|---:|
| 44 | 703 | `(1,2,2,3,3,5)` | 3 | 38 | 20 |
| 47 | 766 | `(1,2,3,3,3,4)` | 2 | 36 | 18 |
| 50 | 957 | `(2,2,2,2,4,4)` | 2 | 38 | 20 |
| 52 | 1751 | `(1,2,3,3,3,4)` | 2 | 36 | 18 |
| 57 | 1916 | `(2,2,3,3,3,3)` | 1 | 36 | 18 |

This improves the preceding simultaneous bound `D>=23`.  In these branches
it now implies

$$
p\geq48,\qquad a\geq19,\qquad b=29-a\leq10,
\qquad e(Q_7[C])\leq E_7(10)=15.
$$

It does not exclude any of the five branches.

## Defect-23 reduction

Assume for contradiction that `D=23`.  The standard family identities are

$$
p=24+D,\qquad M=104-D-2q,\qquad
a\geq D-5,\qquad 2q\leq34-D.
$$

For each of the five local graphs, exact integer-partition enumeration and
the defect-six occupancy inequality leave the same 13 arithmetic states.
Every state contains at least one defect-five family.  If there is one such
family, the number of free missing son slots is at most one; if there are at
least two, their total number of free missing slots is at most three.

Every defect-five father is a noncodeword.  Indeed, if it were selected then
at least `7-free_missing` members of its family would be selected, exceeding
the state's complete family-codeword budget.  Thus all seven neighbors of
each father are codewords.  The local costs of the defect-five centers sum
to at most the free missing-slot count, so at least one center has cost at
most one.

For a center represented by a seven-bit word, its unavoidable local cost is
classified as follows.

- Weights at most two are impossible under the normalization and the
  all-codeword-neighborhood condition.
- A weight-three center exists only on a triangle of `H` and has cost one.
- A weight-four center costs the number of selected local edges contained in
  its support.
- A weight-five center costs at least three.  Each graph has independence
  number three, so the non-orphan support contains a selected edge; the
  corresponding distance-three relation forces three predecessor slots.
- Weights six and seven have local cost zero.

Quotienting all cost-at-most-one centers by the exact stabilizer of `H`
leaves 66 cases.  Words are encoded by bits `0,...,6` as integers from 0 to
127.

| branch | stabilizer order | center-orbit representatives |
|---:|---:|:---|
| 44 | 2 | `14 26 53 63 77 85 89 95 113 116 119 125 126 127` |
| 47 | 2 | `26 28 57 63 71 77 89 95 101 105 111 120 123 125 126 127` |
| 50 | 4 | `38 43 57 63 105 111 120 123 126 127` |
| 52 | 2 | `22 51 63 77 85 95 99 101 111 113 119 125 126 127` |
| 57 | 2 | `15 28 39 53 63 101 111 113 119 125 126 127` |

The verifier reconstructs the local-graph quotient, all 13 arithmetic
states, the cost classification, the stabilizers, and these orbit lists.

## Exact certificate split

At `D=23` the family bounds give

$$
p\geq47,\qquad a\geq18,\qquad b\leq11,
\qquad p+b\leq58,\qquad e(Q_7[C])\leq E_7(11)=17.
$$

For every representative center, the exact formula imposes these necessary
conditions, fixes the center outside `C`, and fixes all seven of its
neighbors inside `C`.  Each formula also contains exact domination and
distance-two separation, cardinality 29, the complete orphan normalization,
all 15 local-graph units, and biconditional singleton, nonisolation, and
code-pair indicators.  These conditions relax the corresponding
defect-five case, so UNSAT excludes it.

Every formula has 10,432 variables and 183,627 clauses.  CaDiCaL `sc2021`
returned UNSAT and emitted a plain DRAT trace for all 66 formulas.  DRAT-trim
returned `s VERIFIED` for every formula/proof pair; all checked cores had
zero RAT lemmas.  PySAT's Kissat 4.0.4 binding independently returned UNSAT
on freshly generated formulas.

The complete formula/proof hashes and checker statistics are in
`certificate_manifest.tsv`.  The aggregate audit was:

| item | aggregate | per-certificate range |
|:---|---:|---:|
| proof bytes | 985,541,271 | 6,228,776--62,406,454 |
| core clauses | 185,018 | 2,198--3,692 |
| core lemmas | 3,498,609 | 10,991--272,108 |
| total lemmas | 9,218,911 | 60,814--523,863 |
| resolution steps | 149,068,233 | 476,819--11,494,683 |

Therefore no `D=23` state survives, proving `D>=24` in all five branches.

## Reproduction

Create the environment and all generated artifacts under `/scratch`:

```bash
python3 -m venv /scratch/q7-ld29-five-branch-d24-venv
/scratch/q7-ld29-five-branch-d24-venv/bin/pip install -r requirements.txt
/scratch/q7-ld29-five-branch-d24-venv/bin/python \
  verify_five_branch_d24.py \
  --write-directory /scratch/q7-ld29-five-branch-d24-reproduced
```

For each generated CNF, an external certificate can be produced and checked
under `/scratch` with

```bash
cadical -q --binary=false FORMULA.cnf FORMULA.drat
drat-trim FORMULA.cnf FORMULA.drat -w
```

Run the independent solver cross-check with

```bash
/scratch/q7-ld29-five-branch-d24-venv/bin/python \
  verify_five_branch_d24.py --solve-kissat
```

Reported environment and hashes:

```text
Python                                      3.11.2
python-sat[pblib]                           1.9.dev15
CaDiCaL                                     sc2021
CaDiCaL executable SHA-256                  c6de62662723ec4a7426c5ca2bc9bfb04c60aad81a423957e3cd1ffadd0f8aa7
DRAT-trim Debian package                    0.0~git20240428.effa1dc-2
DRAT-trim executable SHA-256                bc7543a99da8521ddb09af442698956054f11e10d198bd482ac756535244c021
requirements.txt SHA-256                    639afc203e4b12224d62c9426902d5784099ba876c5ac2faed92e4659b56caca
verify_five_branch_d23.py SHA-256            08183ecd8deb3cb83a59b0e88e483d3ca0838bda24b1e28179d54cdaa0e6ce73
local_graphs.py SHA-256                     35d187198ed332f64551a174096168f101adff309e0dfaf6d94f9ba6d360e1f4
search_q7_ld29.py SHA-256                   3d4cc2bd966dbed2e4b585d3725dd37356487ad735eb008e55e730a7b9022614
verify_five_branch_d24.py SHA-256            6cd1880178ab8ed330db4030459a0247fc6e13016e6cf8321bce8ec7ed0e6ada
certificate_manifest.tsv SHA-256             848aac92f4a9437dae25fdd38e19db81a89caebd9a5f1e9e7cdcfd9d04775d2a
```

CNFs, proof traces, solver logs, and checker logs remain under `/scratch` and
are not committed.

## Trust boundary, scope, and novelty

The reduction depends on the Honkala--Laihonen--Ranto family partition, the
reviewed orphan-local normalization, the reviewed branchwise defect ladder,
and the preceding reviewed `D>=23` result for these branches.  The new finite
step has two independent UNSAT checks and independently verified DRAT
certificates; the large certificates themselves are deliberately excluded
from the repository.

The family method originates in I. Honkala, T. Laihonen, and S. Ranto,
*On Locating-Dominating Codes in Binary Hamming Spaces*, DMTCS 6(2)
(2004), 265--282, <https://doi.org/10.46298/dmtcs.322>.  V. Junnila,
T. Laihonen, and T. Lehtila, *Improved Lower Bound for Locating-Dominating
Codes in Binary Hamming Spaces*, DCC 90 (2022), 67--85,
<https://doi.org/10.1007/s10623-021-00963-8>, supplies the later general
lower-bound context.

Targeted primary-source and refreshed Discovery Net searches through
2026-09-01 found no center-cost and stabilizer split for these five canonical
branches.  The simultaneous `D>=24` refinement is apparently new to the
searched sources; no absolute historical-priority claim is made.
