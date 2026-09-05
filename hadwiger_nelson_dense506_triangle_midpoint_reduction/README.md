# Dense506: a quadratic-field and midpoint reduction

Any failure to extend the fixed colouring of either pinned dense506 host
after three points are added must be a unit equilateral triangle outside
the completed support, with the same two-colour available list at all
three vertices. The [new reduction](PROOF.md) shows that its vertices are
either all in the host coordinate field or all in a single real quadratic
extension. In the latter case the three host-pair midpoints form a
nondegenerate equilateral triangle of side strictly between zero and one,
and the three host-pair lines are concurrent.

The coincident-midpoint case is excluded by a complete exact compatibility
graph: 144,650 host-pair pairs give 1,152 edges, whose components are
686 P2, 160 P3, 34 P4 and 11 P5. Thus no triple can be an obstruction.
The [path-order certificate](path_types.tsv) is 48 bytes. The two remaining
geometric cases have not been enumerated. No <=508 five-chromatic graph
is established, and failure of the fixed colouring alone would not prove
five-chromaticity.

## Reproduce

Use CPython 3.11.2 and the standard library. From this directory in a full
checkout, choose a work path that does not yet exist:

```bash
triangle_work=/tmp/hn-triangle-midpoints
python3 verify.py --work "$triangle_work" > "$triangle_work.verify.json"
cmp expected.json "$triangle_work.verify.json"
python3 audit.py --work "$triangle_work" > "$triangle_work.audit.json"
cmp expected_audit.json "$triangle_work.audit.json"
python3 controls.py > "$triangle_work.controls.json"
cmp expected_controls.json "$triangle_work.controls.json"
sha256sum -c SHA256SUMS
```

No old 52.5-million-triple scan or completion table is needed for the new
finite computation. It regenerates the host pairs directly. Large group,
edge and path streams remain local in the work directory. The source,
small histogram and expected digests reproduce the result.

The primary implementation checks a path decomposition. The audit rebuilds
the other host embedding with independent eight-basis arithmetic, computes
scalar products by polarization, matches every group and edge entry, and
checks all 581,432 possible within-group triples directly. No approximate
equality or modular filter is used. The controls compare exact rational
circle roots with the compatibility equation in all 171 fixture cases,
including 12 positive cases, and reject false path certificates.

All new public entry points passed. The direct exploratory 144,650-pair
check took 8.332 seconds. The full public producer and audit were not
individually timed; [validation.json](validation.json) records this limit
and the measured controls. A separate exploratory reconstruction tested
19,100 possible third-pair incidences after the 1,152 positive pairs and
found none; the published proof uses the simpler path/triple certificates.
This exploratory reconstruction is not an additional premise.

## Dependencies and status

The [preceding two-arbitrary-point/one-C3 theorem](../hadwiger_nelson_dense506_two_low_repair/README.md),
source `1cd7e59a87ff10ba462f9f0dc8e43d4fa94b0fa2`, is Discovery Net
`bafkreiggaf3yoa65tbpt72c5p2k6xbuulcxjdmv2qndhkapjhjuesxc5ha`.
It removes all three-addition cases using a C3(H) point. The
[original arbitrary-two-point/C3 theorem](../hadwiger_nelson_dense506_two_point_extension/README.md)
specifies the exact host geometry and fixed colour row, and has an
[accepted independent review](../hadwiger_nelson_dense506_two_point_extension_review1/README.md).
The new audit imports that review's arithmetic; it is an author check,
not external review of this new theorem. Such review remains pending.

For record calibration, [Parts's manuscript](https://arxiv.org/abs/2010.12665)
gives a 509-vertex, 2,442-edge example, and
[Haugland's August 2026 introduction](https://arxiv.org/html/2608.04542v4)
still identifies 509 as the record. Both were checked live on 2026-09-05.
No priority claim is made for the elementary circle, field or list methods.

At this checkpoint the next geometric choice is between the all-field
case and the finite nondegenerate midpoint/concurrent-line case. The saved
group generator is available for that later choice; neither phase has
been started. HN2's sealed Parts-support certification is a separate lane.
