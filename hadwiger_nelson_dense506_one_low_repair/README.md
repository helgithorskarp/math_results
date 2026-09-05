# Dense506: one arbitrary point plus two completion points is four-colourable

For either pinned dense506 host H, let C be its 1,420 nonhost points with
at least three unit neighbours in H. **The fixed host four-colouring
extends after any two points of C and one arbitrary Euclidean plane point
are added.** Deleting host vertices afterward cannot produce a
five-chromatic graph. This closes one specific repair stratum beyond the
previously closed 1,926-point support.

The [proof](PROOF.md) gives the complete geometric and list-colouring
reduction. A 52,550,758-triple exact census gives 1,085 possible outside
points and 1,262 relevant triples of added points. All receive explicit
four-colour extensions. A separate arithmetic audit reproduces every
point and incidence and checks both embeddings. No SAT solver is needed.

Three-point additions using two or three points outside H union C, other
placements and larger addition patterns remain unresolved. It constructs no
five-chromatic graph with at most 508 vertices.

## Reproduce

Use CPython 3.11.2 and only the standard library, in a full checkout. From
this directory choose two work directories that do not yet exist:

```bash
candidate_work=/tmp/hn-one-low-candidates
repair_work=/tmp/hn-one-low-repair
python3 ../hadwiger_nelson_dense506_two_point_extension/verify.py \
  --work "$candidate_work" > "$candidate_work.census.json"
cmp ../hadwiger_nelson_dense506_two_point_extension/expected.json \
  "$candidate_work.census.json"
python3 verify.py --candidate-work "$candidate_work" --work "$repair_work" \
  > "$repair_work.verify.json"
cmp expected.json "$repair_work.verify.json"
python3 audit.py --candidate-work "$candidate_work" --work "$repair_work" \
  > "$repair_work.audit.json"
cmp expected_audit.json "$repair_work.audit.json"
python3 controls.py --candidate-work "$candidate_work" \
  > "$repair_work.controls.json"
cmp expected_controls.json "$repair_work.controls.json"
sha256sum -c SHA256SUMS
```

The inherited complete candidate table was reused from its prior checked
run during development; the first command regenerates it from public
source. This pass's primary table is 77,422 bytes and is regenerated as
`centres.json` in the repair work directory. Tables, modular survivors,
verbose traces and raw colour-witness streams remain local. Only source,
compact expected outputs, provenance and manifests are published.

The primary screen benchmark processed 832,130 eligible triples in
0.453 seconds. The full prototype used 26.214 seconds for its screen and
27.131 seconds including exact reconstruction/pair checks, excluding
initial input loading. This justified retaining the direct Python
implementation. The public producer was replayed and its entire centre
table matched the prototype byte for byte. The public audit and controls
were also run; see [validation.json](validation.json) for measured costs.

The [controls](controls.py) compare the complete three-vertex list criterion
with brute force in all 10,704 applicable cases. They compare the modular
screen with an unscreened exact run on the first twelve host vertices and
exercise both obstruction types, a flexible colourable palette and wrong
modular roots. The primary and audit independently generate the same
1,262-row colour-witness stream hash in the expected results.

## Dependencies and claim status

- [Exact hosts, full C3 census and two-point extension](../hadwiger_nelson_dense506_two_point_extension/README.md):
  `dc57db82a86037be322374b20b31a65fb73df452`, Discovery Net
  `bafkreie4zkk4azkvyuq5fhjctirmnt36shmedrcaw7d46bykgfuvl4kz4i`.
- [Independent exhaustive review](../hadwiger_nelson_dense506_two_point_extension_review1/README.md):
  `de9cd586d128b12df93d3fdb228d573fe373575c`, Discovery Net
  `bafkreigf3qsv2knb6xy2rohmyujl52skntuavdh6azhowuaypx2ikoeziy`.
- [Entire first-completion support is four-colourable](../hadwiger_nelson_dense506_completion_closure/README.md):
  `b20e53348fd367cb9d9ad182371414b3d23edac8`, Discovery Net
  `bafkreig5fgihcm4dezue62ylojpbsa527yqbz5gkp2qzr5icmpohhmd2my`.

The simultaneous-completion dependency was also
[independently accepted](../hadwiger_nelson_dense506_completion_closure_review1/README.md)
at source `7cbe117f52d85926033e40e140b732d8a000138a` during this pass.

This is an exact computer-assisted exclusion theorem. The new audit uses
independently derived, published arithmetic but is run by the author;
external review of this new claim remains pending. The proof states the
imported completeness assumptions and ordinary code/runtime trust boundary.
No priority claim is made for circle equations or elementary list colouring.

For record calibration, [Parts's primary manuscript](https://arxiv.org/abs/2010.12665)
gives a 509-vertex, 2,442-edge example. The introduction of
[Haugland's August 2026 manuscript](https://arxiv.org/html/2608.04542v4)
still identifies 509 as the record. Both were checked live on 2026-09-05.
