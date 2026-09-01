# Defect-24 rigidity and DRAT exclusion of `Q_7` LD29 branches 72--74

## Certified result

There is no locating-dominating code of cardinality at most 29 in the
binary 7-cube whose lossless orphan normalization has canonical local-graph
index 72, 73, or 74.

| branch | mask | sorted degrees | triangles | independence number |
|---:|---:|:---|---:|---:|
| 72 | `1917` | `(2,2,3,3,4,4)` | 3 | 3 |
| 73 | `2013` | `(2,2,3,3,4,4)` | 3 | 3 |
| 74 | `2014` | `(2,3,3,3,3,4)` | 2 | 3 |

The proof combines a hand-checkable branch-local family-defect bound with
one exact, DRAT-certified SAT formula per branch.  Relative to the current
checked source frontier, these were the last three unresolved nine-edge
local graphs.  The result does not exclude every possible 29-word code.

## Branch-local proof of `D>=24`

After the lossless orphan normalization

```text
0 in C;
e_i not in C                         (0 <= i < 7);
e_0+e_j not in C                     (1 <= j < 7),
```

let `H` be the graph on directions `1,...,6`, with `ij` selected when
`e_i+e_j` is a codeword.  For total Honkala--Laihonen--Ranto family defect
`D`, couples `q`, family vertices `M`, singleton count `p`, and isolated
codeword count `a`, the established identities are

$$
p=24+D,\qquad M=104-D-2q,\qquad
a\ge D-5,\qquad 2q\le34-D.
$$

Every nine-edge local graph uses 12 local defect units.  A defect-`d`
father has maximum family capacity

$$
h(d)=1+\binom{d+2}{2},
\qquad (h(1),\ldots,h(6))=(4,7,11,16,22,29).
$$

If `F` is the set of local father vertices, then the local capacity is

$$
L=\sum_{i\in F}h(\deg_H(i)-1).
$$

Every local father--father edge forces two absent oriented son slots, and
every local triangle forces two more distinct absent slots.  The exact data
are

| branch | local defect | `L` | forced missing slots |
|---:|---:|---:|---:|
| 72 | 12 | 44 | 24 |
| 73 | 12 | 44 | 24 |
| 74 | 12 | 43 | 22 |

The universal predecessor gives `D>=18`.  Exact integer-partition
enumeration leaves no capacity state for `D=18,...,22`.  At `D=23`, each
branch has exactly one raw state:

| branch | `q` | extra defects | free missing slots | family-codeword budget |
|---:|---:|:---|---:|---:|
| 72 | 5 | `(5,6)` | 0 | 1 |
| 73 | 5 | `(5,6)` | 0 | 1 |
| 74 | 5 | `(5,6)` | 1 | 1 |

The defect-six father has `I(f)=N[f]`.  Its seven father--neighbor slots
can only use those neighbors as sons, so with `s` free missing slots its
family contains at least `8-s` codewords.  This is at least seven in all
three rows, contradicting the global family-codeword budget one.  Hence

$$
\boxed{D\ge24}
$$

in branches 72--74.  The verifier reconstructs every partition and all
local graph quantities exactly.

## Exact formulas and certificates

The defect bound gives

$$
p\ge48,\qquad a\ge19,\qquad b=29-a\le10,
\qquad e(Q_7[C])\le E_7(10)=15,
$$

and the family identities also give `p+b<=58`.  Each deterministic formula
contains these bounds together with exact domination of all 128 vertices,
all essential distance-two separation clauses, exact cardinality 29, the
complete orphan normalization, all 15 local-graph units, and biconditional
singleton, nonisolation, and code-pair indicators.

Every formula has 10,432 variables and 183,619 clauses.

| branch | CNF SHA-256 | proof bytes | DRAT SHA-256 |
|---:|:---|---:|:---|
| 72 | `c6d5047b8dc7b79227bda5801bbd485af32db416851b8841695e0d1ec987de78` | 401,513,150 | `ade49b2c9ed5592fa94438c6ee3bd8cf1de47632f792e9b158911a005205b30b` |
| 73 | `a9fe582da3b94771a7517e69949ca4e3edcee87ca1bc1a81a67ccd011cbb58ec` | 353,603,557 | `9fcad1d5c5abe3f8cc801ea08739fea2685b9766d2745e96bd0a9f0e303f3c69` |
| 74 | `c54ae62e5223fc3b00c5b0946f08580f84abf1856a32f7419664699e7c50f512` | 419,544,119 | `9ac49b886b1cb6a44d42c49f4d5beacb20a5ed0eafad5776c7a8fa4eadd12c94` |

CaDiCaL 1.5.3 returned `UNSATISFIABLE` on all three.  DRAT-trim at git
commit `2e3b2dc0ecf938addbd779d42877b6ed69d9a985` independently returned
`s VERIFIED`:

| branch | core/total lemmas | resolution steps | RAT lemmas |
|---:|---:|---:|---:|
| 72 | 1,552,658/2,647,499 | 73,934,436 | 0 |
| 73 | 1,487,299/2,457,915 | 70,674,302 | 0 |
| 74 | 1,766,664/2,789,588 | 77,966,472 | 0 |

PySAT's independent Kissat 4.0.4 binding also returned UNSAT on freshly
rebuilt, hash-matched formulas in 294.6, 300.1, and 310.2 seconds,
respectively.  CNFs, solver output, DRAT files, and checker logs remain under
`/scratch` and are deliberately not committed.

## Reproduction

Create an environment under `/scratch` and regenerate all three formulas:

```bash
python3 -m venv /scratch/q7-ld29-branches72-74-venv
/scratch/q7-ld29-branches72-74-venv/bin/pip install -r requirements.txt
/scratch/q7-ld29-branches72-74-venv/bin/python \
  verify_branches72_74.py \
  --write-directory /scratch/q7-ld29-branches72-74
```

For each `b` in `72 73 74`, produce and check a proof:

```bash
cadical -q --binary=false \
  /scratch/q7-ld29-branches72-74/branch${b}-d24.cnf \
  /scratch/q7-ld29-branches72-74/branch${b}-d24.drat

drat-trim \
  /scratch/q7-ld29-branches72-74/branch${b}-d24.cnf \
  /scratch/q7-ld29-branches72-74/branch${b}-d24.drat -w
```

Run the independent solver check with

```bash
/scratch/q7-ld29-branches72-74-venv/bin/python \
  verify_branches72_74.py --solve-kissat
```

Reported environment and source hashes:

```text
Python                            3.11.2
python-sat[pblib]                 1.9.dev15
CaDiCaL Debian package            1.5.3-2
DRAT-trim git commit              2e3b2dc0ecf938addbd779d42877b6ed69d9a985
verify_branches72_74.py SHA-256   53474298377acb52a02b3350b63ac28700b0ac99367accb6fc5cf3a58d356625
requirements.txt SHA-256          639afc203e4b12224d62c9426902d5784099ba876c5ac2faed92e4659b56caca
```

## Trust boundary, scope, and novelty

The analytic bridge depends on the reviewed orphan-local reduction, the
Honkala--Laihonen--Ranto family partition, the universal defect-18 theorem,
and the stated local slot-counting argument.  The transparent verifier
reconstructs the integer frontier exactly.  The finite exclusions
additionally depend on the deterministic SAT encoding, PySAT totalizers,
Python, CaDiCaL, and DRAT-trim.  DRAT establishes unsatisfiability only for
the three hashed formulas, not the analytic bridge.

The family method originates in I. Honkala, T. Laihonen, and S. Ranto,
*On Locating-Dominating Codes in Binary Hamming Spaces*, DMTCS 6(2)
(2004), 265--282, <https://doi.org/10.46298/dmtcs.322>.  V. Junnila,
T. Laihonen, and T. Lehtila, *Improved Lower Bound for Locating-Dominating
Codes in Binary Hamming Spaces*, Designs, Codes and Cryptography 90 (2022),
67--85, <https://doi.org/10.1007/s10623-021-00963-8>, records the published
interval `28 <= gamma^LD(Q_7) <= 32`.

Targeted primary-source and refreshed Discovery Net searches through
2026-09-01 found no branch-local defect-24 theorem or exact certificate for
branches 72--74.  The result is apparently new relative to the searched
sources, not a historical-priority claim.
