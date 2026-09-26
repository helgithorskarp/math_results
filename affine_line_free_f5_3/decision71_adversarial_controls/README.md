# Adversarial controls for the exact 71-point decision

Four explicit 71-point sets give **inclusion-minimal two-clause satisfiable
weakenings** of actual inputs to the [exact-value proof](../decision71/THEOREM.md).
They preserve the point variables, fibre cardinalities and three-hole gauge.
Each contains exactly two full affine lines. Removing their two line clauses
makes the formula SAT; removing either clause alone leaves it UNSAT.

These controls also expose a signed-shift defect in stock DRAT-trim's
rejection path. The ordinary checker rejects all eight proofs on the
corresponding satisfiable inputs. The instrumented checker encounters
undefined behaviour on three wrong-input tests after the known warning-printer
issue is isolated. See [CHECKER_FINDING.md](CHECKER_FINDING.md).
**No false acceptance or counterexample to the exact-value claim is shown.**
This construction-lane evidence does not independently accept the complete
109,676-case proof or change the campaign handoff status.

## Four precise controls

Case indices, types, point labels and clause positions are zero-based.
Point `25*x+5*y+z` has Boolean variable `1+25*x+5*y+z`.
Clause positions refer to the original formula, before deletion.

| Case | Pair type | Deleted clause positions | Source 70-point seed |
|---:|---:|---|---|
| 1634 | 1 | 532, 546 | reflected |
| 9786 | 4 | 22, 23 | reflected |
| 17600 | 8 | 538, 553 | paper |
| 19590 | 9 | 568, 579 | order-three |

[fixtures.json](fixtures.json) gives every point, full line, quotient word,
gauge, original CNF hash and invertible affine construction map.
[seeds.json](seeds.json) preserves the three published 70-point examples.
Add the specified outside point to its seed and apply the supplied map.
Direct checking finds exactly two full lines meeting at the added point.
Deleting that intersection gives a directly verified 70-point set; the
verifier regauges it and checks its satisfying model. No classification
theorem or search verdict is needed to verify these constructions.

Every 71-point fixture satisfies the *quotient* admissibility conditions:
weights 0–4, total 71, normalized profiles, zero-axis and intersection bounds,
and weight at most 16 on all thirty quotient lines. Its gauge holes are zero.
Its 155 spatial plane sections range from 6 to 17. These are positive controls
for weakened formulas, not line-free sets or examples satisfying every
spatial plane bound.

For each case write `F` for the original formula and `D={C1,C2}` for the two
line clauses. The point certificate satisfies `F\D`. Eight fresh DRAT checks
establish UNSAT of `F\{C1}` and `F\{C2}`. Thus no proper subset of this
particular pair makes `F` satisfiable. Minimum cardinality over all possible
clause deletions is not claimed.

## Reproduce

Run from this directory. The geometric checks need only Python's standard
library; tested with Python 3.11.2 and 3.12.14, including `-O`. Proof generation
uses Python-SAT 1.9.dev15 and CaDiCaL 1.9.5.

```sh
R5_CONTROL_TMP=/tmp/r5-adversarial-controls
mkdir -p "$R5_CONTROL_TMP"
python3 -O verify.py --out "$R5_CONTROL_TMP/geometry.json"
python3 -O validate.py --out "$R5_CONTROL_TMP/fixture-validation.json"
python3 -m venv "$R5_CONTROL_TMP/venv"
"$R5_CONTROL_TMP/venv/bin/python" -m pip install -r requirements.txt
curl -fL https://raw.githubusercontent.com/marijnheule/drat-trim/2e3b2dc0ecf938addbd779d42877b6ed69d9a985/drat-trim.c \
  -o "$R5_CONTROL_TMP/drat-trim.c"
sha256sum "$R5_CONTROL_TMP/drat-trim.c"
gcc -std=gnu99 -O2 "$R5_CONTROL_TMP/drat-trim.c" -o "$R5_CONTROL_TMP/drat-trim"
"$R5_CONTROL_TMP/venv/bin/python" -O replay.py \
  --out "$R5_CONTROL_TMP/proofs" --checker "$R5_CONTROL_TMP/drat-trim" \
  --checker-source "$R5_CONTROL_TMP/drat-trim.c"
```

Required checker source SHA256:
`d834b649f437e091597f5347f259b9f681087f89ca0844d0cee250a1a1a0c2ee`.
The proof directory must be new. Success reports
`FOUR_MINIMAL_TWO_CLAUSE_WEAKENINGS_VERIFIED`, eight UNSAT checks, eight
wrong-input rejections and four SAT solver controls. A timeout, SAT/UNKNOWN
single-omission result, checker crash or incomplete run prevents that summary.
Each negative test deletes exactly one additional original line clause from
the valid proof's input.

With a completely regenerated domain, also run:

```sh
"$R5_CONTROL_TMP/venv/bin/python" -O verify.py \
  --out "$R5_CONTROL_TMP/integration.json" --author ../decision71 \
  --domain /path/to/regenerated/orbits.json
```

Domain SHA256: `02727db9fb02d60a8597f84329f7376bba2c43422d63241da1c251fde97e4eb2`.
Fixture SHA256: `500af6d236d2dead71d882155be07d1b3039472e1632faeee4cbb6e35e2cc75c`.
Fresh proof bytes may vary; every new trace must verify against its input.

## Verification and scope

The standalone verifier imports no author geometry or formula module. It
constructs the 775 lines from point pairs. Five-bit word enumeration generates
the negative `(n+1)`-subset and positive `(6-n)`-subset fibre clauses in the
author's order. The 160-assignment truth-table control checks every cardinality
endpoint. All selected points and gauge holes are checked directly.

The recorded integration run compares all four whole formulas with the author
implementation and verifies their positions in the hash-pinned domain. It
confirms that the author decoder rejects the near misses because they contain
lines, while accepting the four regauged 70-point models. Completeness of the
full catalogue remains the earlier independently reviewed reduction.

[VALIDATION.json](VALIDATION.json) records these checks, ten corrupted-fixture
rejections, the eight ordinary certificates and the qualified sanitizer
outcomes. Ordinary replay took 9.33 seconds, generated 2,319,292 proof bytes,
and reached at most 14,120 solver conflicts. Proofs, CNFs, logs and binaries
remain outside Git; the public source regenerates them. No original author
corpus file is modified.

The native checker, ordinary execution and written encoding remain trust
boundaries. No clean unqualified sanitizer run, proof-assistant verification,
independent peer acceptance, new extremal bound or priority claim is made.
