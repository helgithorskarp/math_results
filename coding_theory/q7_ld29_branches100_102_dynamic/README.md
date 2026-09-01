# Dynamic-pair DRAT exclusion of Q7 size-29 branches 100--102

## Certified finite result

There is no locating-dominating code of cardinality at most 29 in `Q_7`
whose lossless orphan normalization has canonical local-graph index 100,
101, or 102.

These are three of the nine canonical 11-edge graphs on the six non-orphan
coordinate directions.  Their masks and missing edges are:

| branch | mask | missing edges |
|---:|---:|:---|
| 100 | 6015 | `(2,5), (3,6), (4,6), (5,6)` |
| 101 | 6142 | `(1,2), (3,6), (4,6), (5,6)` |
| 102 | 6655 | `(3,4), (3,5), (4,6), (5,6)` |

The checked predecessor reduced the global search to 103 branches after
excluding 97--99.  The three exclusions here sharpen the lossless frontier
to exactly 100 branches: 0--96 and 103--105.

## Stronger exact formulas

These formulas implement the review's recommendation to use all proved
distance-two information.  In addition to exact domination, essential
distance-two separation, cardinality 29, the orphan normalization, 15
local-graph unit clauses, and the defect-18 bounds

\[
p\ge42,\qquad a\ge13,\qquad p+(29-a)\le58,
\qquad e(Q_7[C])\le32,
\]

they impose both

\[
A_2(C)\ge26,
\qquad
A_2(C)\ge2p-58.
\]

The second inequality is encoded as

\[
A_2(C)+2(128-p)\ge198.
\]

Each deterministic DIMACS formula has 90,177 variables, 1,215,249 clauses,
and 25,599,172 bytes.  CaDiCaL 1.5.3 returned `UNSATISFIABLE` and emitted a
plain-text DRAT proof for each exact formula.  DRAT-trim
`0.0~git20240428.effa1dc-2` independently checked every CNF/proof pair and
returned `s VERIFIED`.

| branch | CNF SHA-256 | proof bytes | DRAT SHA-256 |
|---:|:---|---:|:---|
| 100 | `fc6a90431f7d71b665ea97ade16472825b6e3a956c3ec27bf8f53974f0731686` | 355,885,392 | `dc6aa6e156fd0bd1088e321483e08e4ed3ec878e64036a0f744ffbe9a53a6bc6` |
| 101 | `c825e0cfd82e920c91b709b8ee0e87d685335819782c0104ab007c30872bf619` | 196,323,383 | `f1e3db6f5e289cf766c8c263a4a72e2b5d30876d3c74949573a1ed85b5134cb2` |
| 102 | `a1a410dad343156c009b64dfbc750f1836f2df14701bf7f76d323891785951e4` | 405,726,932 | `0ac16529d65dee12bbbc4114cf9460241ce070fe5a1f56d9e6f1c9274b6c1bde` |

The checker cores used 924,510, 439,579, and 1,210,303 lemmas respectively,
with no RAT lemma required.  The proof files remain under `/scratch` and are
deliberately not committed.

## Reproduction

Install the pinned dependency, then regenerate and hash all three CNFs:

```bash
python3 -m pip install -r requirements.txt
python3 verify_branches100_102_dynamic.py \
  --write-directory /scratch/q7-ld29-d18-dynamic-branches100-102
```

For each branch `i` in `100 101 102`, produce and check a fresh proof:

```bash
cadical -q --binary=false \
  /scratch/q7-ld29-d18-dynamic-branches100-102/branch-i.cnf \
  /scratch/q7-ld29-d18-dynamic-branch-i.drat

drat-trim \
  /scratch/q7-ld29-d18-dynamic-branches100-102/branch-i.cnf \
  /scratch/q7-ld29-d18-dynamic-branch-i.drat
```

Replace `i` by the decimal branch number.  The verifier imports the reviewed
base encoding from `../q7_ld29_family_reduction` and the sharper structural
bounds from `../q7_ld29_defect18`.

## Scope, novelty, and trust boundary

This is an exact computer-assisted batch exclusion, not a proof that no
29-word code exists.  The trust boundary consists of the reviewed structural
reduction and exact SAT encoding, the defect-18 and distance-two bounds,
deterministic CNF generation, Python/PySAT's cardinality and PB encodings,
and DRAT-trim's checker.  Branches 0--96 and 103--105 remain unresolved.

The result is new to the refreshed Discovery Net graph and implements its
reviewer's explicit strengthening request.  It is a new finite consequence
of graph results rather than an independent historical-priority claim.  The
family method originates in Honkala--Laihonen--Ranto, *DMTCS* 6(2) (2004),
<https://doi.org/10.46298/dmtcs.322>.  Junnila--Laihonen--Lehtilä still
reported `28 <= gamma^LD(Q_7) <= 32` in *Designs, Codes and Cryptography* 90
(2022), 67--85, <https://doi.org/10.1007/s10623-021-00963-8>.
