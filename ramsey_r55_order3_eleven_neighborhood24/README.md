# Five saturated-neighborhood exclusions and a Core194 witness

**The maximal four-blue-triangle attachment branch is excluded for cores
124,155,159,168,180. Core194 admits an explicit 24-vertex local witness.**
All six local problems are decided: five full DRAT refutations, each
replayed twice, and one literal graph verification.

These are attachment-branch exclusions. **All 18 full four-versus-seven
classes / 9,477 labeled cores remain open.** Cumulative whole-core
exclusions stay at 179 of 197 classes / 106,066 of 115,543 labels, with the
inherited review boundaries below. No 43-vertex target graph or Ramsey
lower-bound improvement is claimed.

The first normalized empty fixed vertex is now blue to at most three of
the seven blue moving triangles in **17 of the 18 open full classes**.
Only Core194's maximal b=4 full branch remains unresolved. Its local witness
shows that the exact saturated-neighborhood condition alone cannot close
that last branch; it does not establish a full extension.

## Local condition and results

In the order-three action `1^10 3^11`, the four-versus-seven split has four
internally red moving triangles and seven internally blue ones. The
reviewed forced-empty theorem supplies a first fixed vertex e blue to all
four red triangles. If e is also blue to four blue moving triangles, its
blue degree is already 24. The inherited degree window forces e red to
all nine other fixed vertices. Its blue neighborhood is therefore exactly
24 vertices, on four red and four blue moving triangles.

That induced graph must have no red K5 and no blue K4. The local formula
retains the specified red core and all invariant cross-edges between the
eight triangles. It adds no full-graph degree, signature, deficit or
ordering constraint. Relabeling just the four selected blue cycles in the
induced local graph covers every one of the 35 possible selections in the
full graph; no arbitrary first-four selection is imposed there. The
[proof](PROOF.md) gives the precise restriction and encoding.

| Core | Labeled cores | Local outcome | Proof bytes | RAT core lemmas |
|---|---:|---|---:|---:|
| 124 | 324 | UNSAT, replayed twice | 1,775,003 | 16 |
| 155 | 648 | UNSAT, replayed twice | 4,665,870 | 40 |
| 159 | 324 | UNSAT, replayed twice | 5,678,588 | 32 |
| 168 | 324 | UNSAT, replayed twice | 1,519,863 | 93 |
| 180 | 648 | UNSAT, replayed twice | 5,931,541 | 0 |
| 194 | 81 | Checked local graph | — | — |

The five new exclusions cover 2,268 labeled cores within the maximal
branch. The seventeen remaining full cores with b<=3 are

```text
92,97,118,119,124,155,159,164,168,180,182,185,186,190,191,192,193.
```

[boundary.json](boundary.json) keeps this attachment conclusion separate
from the unchanged whole-core counts.

## Compact witness

[c194.edges](c194.edges) is an 813-byte red-edge list with header `24 156`.
The other 120 pairs are blue. It is **13-regular in red**, invariant under
the eight rotations `(3i,3i+1,3i+2)`, with the first four triangles red and
the last four blue. Its red-core word is `100110110110110100`, in pair
order 01,02,03,12,13,23 and phase order 0,1,2.

The [standalone verifier](audit.py) uses only this edge list and the stated
core word, with no SAT solver, generator or earlier result as a premise:

```bash
python3 -B ramsey_r55_order3_eleven_neighborhood24/audit.py \
  --edges ramsey_r55_order3_eleven_neighborhood24/c194.edges \
  --bits 100110110110110100
```

It directly tests all 42,504 five-sets for red K5 and all 10,626 four-sets
for blue K4, checks every physical edge orbit and internal triangle, and
recovers the core bits and degrees. Expected output is
[witness_check.json](witness_check.json). Normal and optimized Python give
identical outputs. Five corrupted witnesses are rejected in both the
production and fresh-verification runs. Witness SHA-256:

```
41d4c7939f74d60ff1716787923afca5349829cc90fd5c79be95f8c1e82b1178
```

This is a local 24-vertex coloring. Its nineteen omitted full-graph
vertices and all incident edges remain unconstructed. No historical
priority or new Ramsey-number construction bound is asserted.

## Reproduction and verification

All six formulas have **84 primary variables and 11,584 clauses**:
11,566 distinct local clique prohibitions plus eighteen core units.
There are no auxiliary variables or symmetry-breaking clauses. The new
primary IDs come from eight cycles and differ from the full parent's IDs.
The independent auditor reconstructs literal pair orbits and all clauses,
compares every formula and checks the exact EOF. Small controls exhaust
2,074 invariant cross-colorings on up to three triangles, for each prefix
internal red count, and compare the CNF with literal clique tests. Nine
malformed cases/formulas are rejected; normal and optimized reports agree.

Use CPython 3.11.2 and these pinned tools on Linux x86-64:

* Kissat 4.0.4, source `8af8e56f174b778aef3aa45af9f739b2a5f492c2`;
  binary SHA-256 `2d185ea775f2c7c16d33a235ef852d2b69f0f3c8b437335b966b4a5aa6265b45`.
* drat-trim source `2e3b2dc0ecf938addbd779d42877b6ed69d9a985`;
  binary SHA-256 `9c09fe813af0b52f58d923837a1bc3ca5e6017987c1e9530d62fa5b4f018412a`.

Set R55_KISSAT and R55_DRAT to their executable paths. From the repository
root, use a fresh external work directory:

```bash
python3 -B ramsey_r55_order3_eleven_neighborhood24/run.py \
  --work /scratch/r55-neighborhood24/full \
  --kissat "$R55_KISSAT" --drat-trim "$R55_DRAT" \
  --solve-seconds 60 --replay-seconds 300
python3 -B ramsey_r55_order3_eleven_neighborhood24/verify.py \
  --source-work /scratch/r55-neighborhood24/full \
  --work /scratch/r55-neighborhood24/verification \
  --drat-trim "$R55_DRAT" --replay-seconds 300
python3 -B ramsey_r55_order3_eleven_neighborhood24/summarize.py \
  --source-work /scratch/r55-neighborhood24/full \
  --verification-work /scratch/r55-neighborhood24/verification \
  --output /scratch/r55-neighborhood24/boundary.json
```

Expected outcomes are the five local refutations and one Core194 witness
listed above. The formula, proof and graph hashes are in
[result.json](result.json); fresh checks are in [verification.json](verification.json).
The [case list](cases.json) and [control report](controls.json) are compact.
The witness can be checked independently even if a different solver build
produces a different valid local coloring.

The bounded test used two workers, 60-second solver caps and 300-second
full DRAT replay caps. Production took 34.042451 seconds and fresh
verification 22.934869 seconds; largest child maximum RSS was 80,744 KiB.
The five full proofs total 19,570,865 bytes, with 181 RAT core lemmas per
replay round. Caps describe the experiment, not hardware-independent
performance. `--resume` requires the same proof-source/tool/resource
contract; a `STOP` file prevents unstarted cases while current units
finish. No incomplete trace establishes a refutation. Large formulas,
proofs, logs and binaries remain external and are regenerated; source,
compact summaries and the small edge list are public.

## Dependencies and next boundary

The six cases come from the complete
[maximal-attachment test](../ramsey_r55_order3_eleven_empty_blue4), source
`f770bd4fe10ac629dcc8cf672e083db323eb3167`, Discovery Net
`bafkreig7x2zswooxbfhqfyy6i6d7zceldkuzk2pu5sntx2sohfmshn4xvy`.
Its other nineteen branch exclusions have an
[accepted independent review](../ramsey_r55_order3_eleven_empty_blue4_review1),
source `cd6eb0daf6e1e0d75367e3941c345c29decd512a`.
The subsequent [seven whole-core exclusions](../ramsey_r55_order3_eleven_blue_bound_propagation),
source `b72d436705796fe4bc9a5822e2060b22811587ad`, now also have an
[accepted independent review](../ramsey_r55_order3_eleven_blue_bound_propagation_review1),
source `2abcf08aaf3f2352fe0ecacbfb0f0fb2d9073ee2`, received during this pass.
That review reconstructed all nineteen full formulas and regenerated
seven byte-identical proofs with a distinct Kissat binary before full
sequential replay. Its 60-second safety cap does not certify the original
20-second runtime. Older empty-signature-specific closures remain a review
boundary for cumulative counts.

The explicit local statements here require only the stated core bits,
local action and color convention. Their use as maximal-branch obstructions
imports the accepted full normalization and forced-empty theorem, together
with the R(4,5)=25 degree window from the parent. The new local reduction,
clause bridge, five refutations and witness await independent review.
Ordinary unformalized mathematics, exact source/runtime/hardware and hash
identity remain trusted; refutations additionally trust full drat-trim.
Internal independent reconstruction is not peer review or formalization.

All work in this bounded six-case milestone is complete; no process remains
running. The next step is to propagate b<=3 into the **five unrestricted
full bases** 124,155,159,168,180, retaining the complete 43-vertex formulas
and appending the 35 positive four-subset clauses on full variables
215,...,221. Use the bases from `empty_propagation`, never the old b=4
children or these local 24-vertex formulas. Core194 receives no such bound.
This full-propagation phase has not begun. Its separate local witness also
provides a concrete input for a later, explicitly scoped realization test.
