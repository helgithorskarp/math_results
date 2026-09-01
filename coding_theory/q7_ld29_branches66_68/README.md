# DRAT closure of `Q_7` LD29 nine-edge branches 66--68

## Certified result

There is no locating-dominating code of cardinality at most 29 in the
binary 7-cube whose lossless orphan normalization has canonical local-graph
index 66, 67, or 68.  These are three consecutive nine-edge graphs on the
six non-orphan coordinate directions:

| branch | mask | sorted degrees | triangles |
|---:|---:|:---|---:|
| 66 | 1022 | `(2,2,3,3,4,4)` | 2 |
| 67 | 1759 | `(1,3,3,3,3,5)` | 4 |
| 68 | 1783 | `(1,2,3,4,4,4)` | 5 |

Together with the preceding certificates for branches 63--65, this closes
the first six nine-edge branches.  It is a finite search reduction, not a
proof that a 29-word code is impossible.

## Analytic input and corrected exact formulas

The preceding leaf-aware family theorem proves total family defect

$$
D\geq24
$$

in all three branches.  Fathers of defect six are permitted in that proof,
so it applies to arbitrary exact 29-word codes, including a code obtained by
augmenting a hypothetical smaller code.  The standard consequences are

$$
p\geq48,\qquad a\geq19,\qquad b=29-a\leq10,
\qquad e(Q_7[C])\leq E_7(10)=15,
$$

and `p+b<=58`.

The first nine-edge generator encoded only the weaker `D>=23` consequences
for branches 66 and 67, despite proving `D>=24` analytically.  That was not
unsound, but made the formulas unnecessarily difficult.  The present
generator applies the proved `D>=24` bounds consistently to all three rows.
For branch 68 it reproduces the earlier formula byte for byte.

Each deterministic formula contains exact domination of all 128 vertices,
all essential distance-two separation clauses, exact cardinality 29, the
complete orphan normalization, all 15 local-graph units, biconditional
singleton/nonisolation/code-edge indicators, and the four numerical bounds
above.  Repeated literals are removed clausewise, a Boolean identity.

Every formula has 10,432 variables and 183,619 clauses.  CaDiCaL 1.5.3
emitted a plain-text DRAT proof for each.  DRAT-trim
`0.0~git20240428.effa1dc-2` returned `s VERIFIED` on every exact pair, with
no RAT lemma in any checked core.  PySAT's Kissat 4.0.4 binding independently
returned UNSAT.

| branch | CNF SHA-256 | proof bytes | DRAT SHA-256 | core lemmas | resolution steps |
|---:|:---|---:|:---|---:|---:|
| 66 | `a1114814daf11367f5f0de7523307ec0990c529f0f3814f2fe49e1ded4002ace` | 221,232,761 | `2af3f9e47a1a3ab35ffaa53497c4e0b89a29a6feb123d7db5a3cfd1968455841` | 953,793 | 42,195,055 |
| 67 | `c8df988078649ad8b7613a13a647c63ba91da7f1170612de34671e086d14db71` | 590,113,396 | `ca83b4810f77c52913463dbc07df73a772da4b58312797a5de690867bf470cd2` | 2,428,139 | 98,353,470 |
| 68 | `f1114e5860c93de7730218e9f96f1bb8aa293e6e79b2d1362be59b2ea902c737` | 499,372,854 | `687c3f73523a270d6e7c3b039f572970bb93c945fa506c474e8bf97b2e9b1c4e` | 1,813,618 | 85,904,681 |

As an additional cross-check, the predecessor's weaker branch-66 formula
(`D>=23`) also has a hash-matched 435,027,812-byte DRAT proof that verified
with 1,759,911 core lemmas and no RAT lemma.  It is not needed for the
displayed result; the smaller sharp certificate is the primary record.

## Reproduction

Create an environment and regenerate the exact formulas under `/scratch`:

```bash
python3 -m venv /scratch/q7-ld29-d24-branches66-68-venv
/scratch/q7-ld29-d24-branches66-68-venv/bin/pip install -r requirements.txt
/scratch/q7-ld29-d24-branches66-68-venv/bin/python \
  verify_branches66_68.py \
  --write-directory /scratch/q7-ld29-d24-branches66-68
```

For each `b` in `66,67,68`, produce and verify the certificate:

```bash
cadical -q --binary=false \
  /scratch/q7-ld29-d24-branches66-68/branch-${b}.cnf \
  /scratch/q7-ld29-d24-branch-${b}.drat

drat-trim \
  /scratch/q7-ld29-d24-branches66-68/branch-${b}.cnf \
  /scratch/q7-ld29-d24-branch-${b}.drat -w
```

Run the independent solver cross-check with

```bash
/scratch/q7-ld29-d24-branches66-68-venv/bin/python \
  verify_branches66_68.py --solve-kissat
```

Reported environment and source hashes:

```text
Python                         3.11.2
python-sat[pblib]              1.9.dev15
CaDiCaL Debian package         1.5.3-2
DRAT-trim Debian package       0.0~git20240428.effa1dc-2
requirements.txt SHA-256       639afc203e4b12224d62c9426902d5784099ba876c5ac2faed92e4659b56caca
verify_branches66_68.py SHA-256 fd42705e97c15d25aa375949431122d05637524161d2b0c643ee4daac50b6e1e
```

The CNFs, proofs, and checker outputs remain under `/scratch` and are not
committed.

## Trust boundary, scope, and novelty

The mathematical conclusion depends on the reviewed family/orphan
reduction, the leaf-aware `D>=24` theorem, the deterministic exact encoding,
PySAT's cardinality encodings, and DRAT-trim.  DRAT proves only the three
hashed formulas; the analytic bridge is separate.  Kissat is an independent
solver cross-check, not the proof checker.

The family method originates in I. Honkala, T. Laihonen, and S. Ranto,
*On Locating-Dominating Codes in Binary Hamming Spaces*, DMTCS 6(2) (2004),
<https://doi.org/10.46298/dmtcs.322>.  V. Junnila, T. Laihonen, and
T. Lehtila, *Improved Lower Bound for Locating-Dominating Codes in Binary
Hamming Spaces*, DCC 90 (2022),
<https://doi.org/10.1007/s10623-021-00963-8>, records
`28 <= gamma^LD(Q_7) <= 32` and improves the general lower bound only from
dimension ten.

Targeted primary-source and refreshed graph searches through 2026-09-01
found no exact certificate for branches 66--68.  The exclusions are
apparently new to the searched sources; no historical-priority claim is
made.
