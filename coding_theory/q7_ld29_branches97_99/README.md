# DRAT exclusion of Q7 size-29 orphan-local branches 97--99

## Certified finite result

There is no locating-dominating code of cardinality at most 29 in `Q_7`
whose lossless orphan normalization has canonical local-graph index 97,
98, or 99.

These are three of the nine canonical 11-edge graphs on the six non-orphan
coordinate directions.  In the canonical labeling, their masks and missing
edges are:

| branch | mask | missing edges |
|---:|---:|:---|
| 97 | 2047 | `(3,6), (4,5), (4,6), (5,6)` |
| 98 | 4063 | `(2,3), (4,5), (4,6), (5,6)` |
| 99 | 5887 | `(2,6), (3,6), (4,6), (5,6)` |

Thus their complements in `K_6` are respectively a paw plus two isolated
vertices, `K_3 + K_2` plus one isolated vertex, and `K_{1,4}` plus one
isolated vertex.

The predecessor's checked certificates already force any hypothetical code
of cardinality at most 29 into branches 0--105.  The three exclusions here
sharpen that lossless frontier from 106 to 103 branches.

## Exact formulas and checked proofs

The exact formulas combine domination at every vertex, all essential
distance-two separation clauses, cardinality exactly 29, the complete
orphan normalization, 15 unit clauses fixing the selected local graph, and
the defect-18 consequences

\[
p\geq42,\qquad a\geq13,\qquad p+b\leq58,
\qquad e(Q_7[C])\leq32.
\]

Each formula has 10,432 variables and 183,619 clauses.  CaDiCaL 1.5.3
returned `UNSATISFIABLE` and emitted a plain-text DRAT proof for each exact
formula.  DRAT-trim `0.0~git20240428.effa1dc-2` independently checked every
CNF/proof pair and returned `s VERIFIED`.

| branch | CNF SHA-256 | proof bytes | DRAT SHA-256 |
|---:|:---|---:|:---|
| 97 | `2f5dc4218d46c49fff6fc90839d9366aacd0297ce39236b0dc54ed20f327082f` | 216,218,340 | `342aa00c48d47140eea054e0e59b7787802ac1b653689686dd22058f92a06d7c` |
| 98 | `dca0244b77491d58e833a4b6a949f8a23717c6bd32044eab45f0a8f9fb9790fc` | 201,846,300 | `7a58128b96ce271156f5f863a546ee268a0aa066a36bc9865857cfa564e59b36` |
| 99 | `30fd463e8dc5097774ab489660376a406cd8e4f5710caf25752bd363c305bd72` | 373,961,514 | `f4595cfbffb6bf6de2007ab83407af79731c04b20abe44cf474373e7ee7987c7` |

The proof files are deliberately not committed.  They remain under
`/scratch` and can be regenerated from the versioned generators.

## Reproduction

Install the pinned dependency, then regenerate and hash all three CNFs:

```bash
python3 -m pip install -r requirements.txt
python3 verify_branches97_99.py \
  --write-directory /scratch/q7-ld29-d18-branches97-99
```

For each branch `i` in `97 98 99`, produce and check a fresh proof:

```bash
cadical -q --binary=false \
  /scratch/q7-ld29-d18-branches97-99/branch-i.cnf \
  /scratch/q7-ld29-d18-branch-i.drat

drat-trim \
  /scratch/q7-ld29-d18-branches97-99/branch-i.cnf \
  /scratch/q7-ld29-d18-branch-i.drat
```

Replace `i` by the decimal branch number.  The verifier imports the reviewed
base encoding from `../q7_ld29_family_reduction` and the sharper bounds from
`../q7_ld29_defect18`.

## Scope, novelty, and trust boundary

This is an exact computer-assisted batch exclusion, not a proof that no
29-word code exists.  The trust boundary consists of the reviewed structural
reduction and SAT encoding, deterministic CNF generation, CaDiCaL's DRAT
output, and DRAT-trim's checker.  The checked proofs establish only
unsatisfiability of the three hashed formulas.  Branches 0--96 and 100--105
remain unresolved.

The result is new to the refreshed Discovery Net graph and follows its
reviewed reduction; no independent literature-priority claim is made.  The
family method originates in I. Honkala, T. Laihonen, and S. Ranto, *On
Locating-Dominating Codes in Binary Hamming Spaces*, DMTCS 6(2) (2004),
265--282, <https://doi.org/10.46298/dmtcs.322>.  Junnila, Laihonen, and
Lehtilä still reported the interval `28--32` for `Q_7` in *Designs, Codes
and Cryptography* 90 (2022), 67--85,
<https://doi.org/10.1007/s10623-021-00963-8>.
