# Full extensions after the first-empty attachment bound

**Seven further whole-core classes are excluded: 109,114,122,154,167,177,188.**
These represent 6,480 labeled cores. The four-versus-seven boundary shrinks
from 25 classes / 15,957 labels to **18 classes / 9,477 labels**. Cumulative
whole-core exclusions become **179 of 197 classes / 106,066 of 115,543 labels**,
with the inherited review boundaries stated below. No target graph or
Ramsey lower-bound improvement is claimed.

This completes the bounded full-extension test following the
[19 maximal-attachment exclusions](../ramsey_r55_order3_eleven_empty_blue4).
The other twelve tested cores returned UNKNOWN:
92,97,118,119,164,182,185,186,190,191,192,193.
Together with the six untested cases, these form the remaining 18-class
boundary. Core164 is now the sole one-anchor case; sixteen two-anchor
cases and the four-anchor core194 also remain. The three-versus-eight
split and other moving-cycle counts are unchanged.

The action is `1^10 3^11`, with four internally red and seven internally
blue moving triangles. In each of the 19 selected cores, the first
normalized fixed vertex e=33 has an empty red-core signature and is blue
to at most three blue moving triangles. This necessary bound is propagated
into the **unrestricted complete 43-vertex base** through 35 positive
four-subset clauses on primary variables 215,...,221. No fixed edge is
newly fixed, and no normalization or auxiliary variable is introduced.

The formulas retain all parent, core, anchor, empty-prefix and sharp
singleton/pair constraints. Six one-anchor cases have 34,290 variables
and 617,467 clauses; thirteen two-anchor cases have 34,300 variables and
617,517 clauses. The six cores without a proved maximal-branch exclusion,
124,155,159,168,180,194, are untested and receive no new bound.

The [proof and encoding](PROOF.md) explain why an UNSAT result would be a
whole-core exclusion. Both the producer and independent auditor explicitly
reject the previous b=4 branch formula as a starting base: its exact-three
red-link condition must not be combined with the new at-least-four bound.
The checked starting hashes instead come from the earlier
[full-extension package](../ramsey_r55_order3_eleven_empty_propagation).

## Completed evidence

| Check | Result |
|---|---:|
| Complete unrestricted bases rebuilt twice | 25 |
| Complete strengthened full formulas rebuilt twice | 19 |
| Full refutations replayed twice | 7 |
| New whole-core / labeled exclusions | 7 / 6,480 |
| Tested UNKNOWN / untested cores | 12 / 6 |
| Full proof bytes / largest proof | 153,723,022 / 25,429,506 |
| RAT core lemmas, sum per replay round | 5,580 |
| Production / fresh verification elapsed | 356.703836 / 276.291853 seconds |
| Largest child maximum RSS in production | 261,516 KiB |

The seven new whole-core exclusions combine the now independently accepted
maximal-branch closures with the seven new complementary full-formula
refutations. These seven new refutations and the 35-clause propagation
bridge await independent review. Timeouts are inconclusive.

All computations are complete; no job remains running. The next bounded
structural direction is to examine the saturated 24-vertex blue
neighborhood in the six unresolved maximal-attachment cases, seeking a
local obstruction or an explicit checked local witness. This pass does
not start that new phase or extend a solver limit. The other twelve full
cores retain the at-most-three-blue attachment bound.

## Reproduction

From the repository root, use CPython 3.11.2, GCC 12.2.0 (Debian
12.2.0-14+deb12u1), and these pinned Linux x86-64 tools:

* Kissat 4.0.4, source `8af8e56f174b778aef3aa45af9f739b2a5f492c2`;
  binary SHA-256 `2d185ea775f2c7c16d33a235ef852d2b69f0f3c8b437335b966b4a5aa6265b45`.
* drat-trim source `2e3b2dc0ecf938addbd779d42877b6ed69d9a985`;
  binary SHA-256 `9c09fe813af0b52f58d923837a1bc3ca5e6017987c1e9530d62fa5b4f018412a`.

Set R55_KISSAT and R55_DRAT to their executable paths. Keep large generated
state outside the repository:

```bash
python3 -B ramsey_r55_order3_eleven_blue_bound_propagation/run.py \
  --work /scratch/r55-blue-bound/full \
  --kissat "$R55_KISSAT" --drat-trim "$R55_DRAT" \
  --solve-seconds 20 --replay-seconds 300
python3 -B ramsey_r55_order3_eleven_blue_bound_propagation/verify.py \
  --source-work /scratch/r55-blue-bound/full \
  --work /scratch/r55-blue-bound/verification \
  --drat-trim "$R55_DRAT" --replay-seconds 300
python3 -B ramsey_r55_order3_eleven_blue_bound_propagation/summarize.py \
  --source-work /scratch/r55-blue-bound/full \
  --verification-work /scratch/r55-blue-bound/verification \
  --output /scratch/r55-blue-bound/boundary.json
```

The contract uses two workers, 20-second solver caps, and 300-second full
DRAT replay caps. These are bounded experimental limits, not a promise
of hardware-independent completion. `--resume` checks source/tool/resource,
case, base, formula and trace identities. A `STOP` file prevents unstarted
cases while the current solve/replay units finish. UNKNOWN traces are
neither refutations nor saved solver states.

Preparation reconstructs all 25 unrestricted bases and matches the entire
preceding preparation to its public record entry by entry. The new auditor
recovers all 320 primary meanings directly from the literal 43-vertex
edge orbits, checks every retained base and exact new tail, and exhausts
128 moving patterns and 65,536 moving/fixed incidence assignments.
Exactly 64 moving patterns satisfy the new bound. All 17,728 degree-valid
complementary incidence assignments satisfy the tail. Thirteen malformed
inputs are rejected under normal and optimized Python with identical
reports. Fresh verification rebuilds all bases and all 19 strengthened
formulas, and replays any completed full proof a second time.

The [case list](cases.json), [controls](controls.json), [production result](result.json),
[fresh reconstruction report](verification.json) and [boundary](boundary.json)
record exact identities and outcomes. Large formulas, traces, logs and
binaries stay outside Git and are regenerated by the commands above.

## Dependencies and trust

The full bases come from `ramsey_r55_order3_eleven_empty_propagation`,
source `f7f8339fcf0e7c0b48cd18df1c5f84975eef1d6e`, Discovery Net
`bafkreicxnbie6cijmgq6b3dh3heom7utz7ghbea632xbynavk4wzauclpa`.
The 19 necessary bounds come from `ramsey_r55_order3_eleven_empty_blue4`,
source `f770bd4fe10ac629dcc8cf672e083db323eb3167`, Discovery Net
`bafkreig7x2zswooxbfhqfyy6i6d7zceldkuzk2pu5sntx2sohfmshn4xvy`.
The latter now has an [accepted independent review](../ramsey_r55_order3_eleven_empty_blue4_review1),
source `cd6eb0daf6e1e0d75367e3941c345c29decd512a`, received during this
pass's final refresh. Reviewer-1 reconstructed all 25 formulas and
regenerated the exact nineteen proof traces with a distinct Kissat binary,
then performed full sequential DRAT replay. The review used a 60-second
safety cap and does not certify the original 20-second performance limit.

The parent, core cover, intrinsic-anchor strengthening, forced-empty
theorem and core123 exclusion have accepted independent reviews at their
stated scopes. Older empty-signature-specific exclusions remain a review
boundary for cumulative whole-core counts. The degree window imports
R(4,5)=25 through the parent. The new propagation bridge also awaits
independent review. Ordinary unformalized reductions, exact source,
runtime/compiler/hardware, SHA-256 and the full DRAT checker remain
trusted. Internal audits are not peer review or formalization. Compact
reports and hashes alone do not establish UNSAT.
