# Local-neighborhood propagation excludes full Core159

**Core159 has no complete Ramsey(5,5;43) extension in the eleven-cycle
four-red/seven-blue triangle branch.** Its full refutation passed DRAT
replay twice, the second time after fresh reconstruction. This removes
one class representing **324 labeled cores**.

The full boundary shrinks to **17 classes / 9,153 labels**. Cumulative
whole-core exclusions become **180 of 197 classes / 106,390 of 115,543
labels**, importing the older exclusion chain and its review boundaries.
No 43-vertex target graph or Ramsey lower-bound improvement is claimed.

This pass tests the five full cores newly constrained by the
[saturated-neighborhood theorem](../ramsey_r55_order3_eleven_neighborhood24):
124,155,159,168,180. The other four tested formulas return UNKNOWN at the
20-second cap. Thirteen current full cores are untested here. Core194
receives no new bound; its independently accepted 24-vertex local witness
still supplies no full extension.

## Reduction and exact evidence

In the existing normalized action `1^10 3^11`, the first fixed vertex e=33
is blue to all twelve vertices in the four internally red moving triangles.
If b of the seven internally blue moving triangles are blue to e and h
other fixed neighbors are red, then

```
d_red(e)=3(7-b)+h,  d_blue(e)=21+3b-h.
```

The inherited 18..24 degree window implies b<=4. At b=4, h=9 and e's blue
neighborhood is exactly a 24-vertex graph on four red and four blue moving
triangles, with no red K5 and no blue K4. The preceding five local
refutations exclude this entire maximal branch for the five tested cores,
covering all selections of four blue triangles. That local premise now
has an [accepted independent review](../ramsey_r55_order3_eleven_neighborhood24_review1).
Thus each unrestricted full extension satisfies b<=3.

Each complete base receives the 35 positive clauses on four-subsets of
full primary variables 215,...,221, asserting at least four red moving
links. Every parent/core/anchor/empty-prefix/pair-cut constraint remains.
No fixed edge, auxiliary variable or normalization is added. All five
formulas have **34,300 variables / 617,517 clauses**.

The [proof](PROOF.md) distinguishes the unrestricted full base, the old
b=4 child, and the 84-variable local neighborhood formula. Only the first
is a valid input to this propagation. A full extension would either be in
the already excluded b=4 branch or satisfy the new full formula; refuting
that formula therefore excludes the whole core.

Core159's eighteen red-core bits are `100100110011001110`, in pair order
01,02,03,12,13,23 and phase order 0,1,2. Its exact identities are:

| Artifact | Bytes | SHA256 |
|---|---:|---|
| Unrestricted full base | 24,954,137 | `9772e64d76c977c28c2124ca2fe8a86f7f0ca91ece107a082f71c15f4ac76199` |
| Strengthened full formula | 24,954,767 | `41e63a4cd59da7c2445025d3e00c567d8322700f5c9cc0f7b046b99f20972ff4` |
| Complete DRAT proof | 21,652,748 | `7f6596418b637d855b0ff4406fcdf7ded9a44e56b736fa3a325d5fe234555653` |

Both proof replays verify **1,046 RAT core lemmas**. Production took
146.959473 seconds and fresh verification 108.415620 seconds; largest child
maximum RSS was 261,488 KiB. The complete five-case experiment used two
workers, 20-second solver caps and 300-second full replay caps.

The remaining full cores are

```text
92,97,118,119,124,155,164,168,180,182,185,186,190,191,192,193,194.
```

All except194 have b<=3 for the first normalized empty fixed vertex.
Core194 is the sole unresolved maximal b=4 branch. The statement is about
the first fixed vertex in the accepted canonical representation, not
every empty fixed vertex. The three-versus-eight split and other moving
counts remain unchanged.

## Reproduction

Use CPython 3.11.2 and these pinned Linux x86-64 tools:

* Kissat 4.0.4, source `8af8e56f174b778aef3aa45af9f739b2a5f492c2`;
  binary SHA256 `2d185ea775f2c7c16d33a235ef852d2b69f0f3c8b437335b966b4a5aa6265b45`.
* drat-trim source `2e3b2dc0ecf938addbd779d42877b6ed69d9a985`;
  binary SHA256 `9c09fe813af0b52f58d923837a1bc3ca5e6017987c1e9530d62fa5b4f018412a`.

The inherited full-base reconstruction also uses GCC 12.2.0 (Debian
12.2.0-14+deb12u1). Set R55_KISSAT and R55_DRAT to their executable paths.
From the repository root, use fresh external work directories:

```bash
python3 -B ramsey_r55_order3_eleven_local_bound_propagation/run.py \
  --work /scratch/r55-local-bound/full \
  --kissat "$R55_KISSAT" --drat-trim "$R55_DRAT" \
  --solve-seconds 20 --replay-seconds 300
python3 -B ramsey_r55_order3_eleven_local_bound_propagation/verify.py \
  --source-work /scratch/r55-local-bound/full \
  --work /scratch/r55-local-bound/verification \
  --drat-trim "$R55_DRAT" --replay-seconds 300
python3 -B ramsey_r55_order3_eleven_local_bound_propagation/summarize.py \
  --source-work /scratch/r55-local-bound/full \
  --verification-work /scratch/r55-local-bound/verification \
  --output /scratch/r55-local-bound/boundary.json
```

Expected new exclusion:159. Expected UNKNOWN cases:124,155,168,180.
All 25 historical unrestricted bases are reconstructed twice and compared
with the preceding published preparation and base identities, but only
five receive solver tests. The full-base C++ audit and earlier exact
checks are retained through the isolated reconstruction chain.

The new auditor imports no producer, recovers all 320 primary meanings
from literal edge orbits on 43 vertices, compares full base bytes, derives
the exact 35-clause tail and checks EOF. All 128 moving patterns and
65,536 moving/fixed assignments are checked. Exactly 64 moving patterns
satisfy the bound, and all 17,728 degree-valid complementary assignments
are retained. Fourteen malformed inputs are rejected, including a local24
formula, a maximal b=4 child, and an unproved Core194 case. Normal and
optimized control reports agree. Fresh verification reconstructs all
five formulas and replays the complete Core159 proof a second time.

[Cases](cases.json), [controls](controls.json), [result](result.json),
[fresh verification](verification.json) and [boundary](boundary.json)
record exact inputs, full formula identities, outcomes and unchanged scopes.
All 90 transitive source identities were frozen before production and
remain matched. Large CNFs, traces, logs and binaries stay outside Git;
source and compact evidence are public. Hashes alone are not refutations.

`--resume` checks the same source/tool/resource contract and stored case,
base, formula and trace identities. A `STOP` file prevents unstarted cases
while active solve/replay units finish. Caps specify a bounded experiment,
not a hardware-independent runtime theorem. UNKNOWN traces are neither
proofs nor saved solver states. A target SAT claim would require an explicit
43-vertex edge list and a literal check of every five-set.

## Dependencies, review and stopping boundary

The unrestricted full bases are from
[empty-signature propagation](../ramsey_r55_order3_eleven_empty_propagation),
source `f7f8339fcf0e7c0b48cd18df1c5f84975eef1d6e`, graph
`bafkreicxnbie6cijmgq6b3dh3heom7utz7ghbea632xbynavk4wzauclpa`.
The five local premises are from [neighborhood24](../ramsey_r55_order3_eleven_neighborhood24),
source `795a95fc920b6e750cd9b7293a6705aa7c50f072`, graph
`bafkreibtyzbvbtqviibojcy633en2veivksvqzpnwzey2ff5yh44g56xza`.
Their [independent review](../ramsey_r55_order3_eleven_neighborhood24_review1),
source `32775f8609d663966c40c32a4207829421ef9dd9`, graph
`bafkreiddoyofmpkshge4j3a3dwkcxfg4jx2qog2wlxnzksr55mvmaja45a`,
arrived during this pass and accepts the reduction, six local formulas,
five regenerated refutations and literal Core194 witness. It used a
separately built Kissat binary and full sequential replay.

The preceding [seven whole-core exclusions](../ramsey_r55_order3_eleven_blue_bound_propagation),
source `b72d436705796fe4bc9a5822e2060b22811587ad`, are independently
accepted and supply the current starting boundary of 18 classes. The
parent, core cover, intrinsic anchors, forced-empty theorem and earlier
maximal-branch results are accepted at their stated scopes. Older
empty-signature-specific whole-core closures remain the cumulative-count
review boundary. The new Core159 full refutation and this propagation
package await independent review.

The R(4,5)=25 degree window is imported through the parent. Ordinary
unformalized reductions, exact source/runtime/compiler/hardware, SHA256
and full drat-trim remain trusted. Internal independent reconstruction
is not peer review or proof-assistant formalization. The teammate's
conditional marked H20/O22 density obstruction supplies no premise here.

This five-case milestone is complete; no process remains running. The
next structural direction is Core194's sole remaining maximal branch,
using the certified local witness to design a scoped full-extension test
or an exhaustive local-family reduction. A single local witness must not
be assumed to represent every neighborhood, and fixed-neighborhood tests
must justify their labeling and retained normalizers. No such new phase,
new stratum or increased solver cap is begun here.
