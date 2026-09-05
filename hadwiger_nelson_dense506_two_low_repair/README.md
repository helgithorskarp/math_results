# Dense506: two arbitrary points and one completion point are harmless

**For either pinned dense506 host, its fixed four-colouring extends after
any two plane points and any one triple-neighbour completion point are
added.** Restriction therefore excludes all one-deletion/three-point
repairs of order 508 that use at least one such completion point.

The [proof](PROOF.md) reduces every possible failure to a unit-distance
pair in the saved 1,085-point census. Among 588,070 pairs, exactly 607
have the necessary common palette and eligible neighbour. Their squared
distances have 30 exact values, none equal to one. The complete
[distance-spectrum certificate](squared_distances.tsv) is **499 bytes**.

No five-chromatic graph with at most 508 vertices is established. The
remaining three-point case has all three additions outside the completed
support. In a minimal counterexample they form a unit equilateral triangle,
each with exactly two retained host neighbours. This family remains
unstarted, as do other placements and larger addition patterns.

## Reproduce

Use CPython 3.11.2 and only the standard library. From this directory in a
full checkout, choose three work paths that do not yet exist:

```bash
candidate_work=/tmp/hn-two-low-candidates
centre_work=/tmp/hn-two-low-centres
pair_work=/tmp/hn-two-low-pairs
python3 ../hadwiger_nelson_dense506_two_point_extension/verify.py \
  --work "$candidate_work" > "$candidate_work.census.json"
cmp ../hadwiger_nelson_dense506_two_point_extension/expected.json \
  "$candidate_work.census.json"
python3 ../hadwiger_nelson_dense506_one_low_repair/verify.py \
  --candidate-work "$candidate_work" --work "$centre_work" \
  > "$centre_work.census.json"
cmp ../hadwiger_nelson_dense506_one_low_repair/expected.json \
  "$centre_work.census.json"
python3 verify.py --candidate-work "$candidate_work" \
  --centre-work "$centre_work" --work "$pair_work" > "$pair_work.verify.json"
cmp expected.json "$pair_work.verify.json"
python3 audit.py --candidate-work "$candidate_work" \
  --centre-work "$centre_work" --work "$pair_work" > "$pair_work.audit.json"
cmp expected_audit.json "$pair_work.audit.json"
python3 controls.py > "$pair_work.controls.json"
cmp expected_controls.json "$pair_work.controls.json"
sha256sum -c SHA256SUMS
```

The first two commands regenerate imported tables. This pass reused their
checked outputs, with canonical hashes verified, and ran every new entry
point. The primary verifier took 0.194 seconds, independent-organization
arithmetic audit 0.140 seconds, and controls 0.283 seconds. See
[validation.json](validation.json) for resource measurements. No earlier
52.5-million-triple scan was repeated to perform this pair check.

`pairs.json` (10,023 bytes) and `norms.json` (14,091 bytes) are regenerated
in the pair work directory. They and the raw 629-row colour-witness stream
remain local. Source, the distance certificate and compact expected outputs
are sufficient for reproduction. No SAT dependency or binary is required.

The [controls](controls.py) compare every graph and list assignment on
three vertices with two lists of size at least two and the third nonempty:
14,520 cases, exactly 18 noncolourable. Six exact norm fixtures cover a unit
edge, coincident points, imaginary and radical coordinates, and rational
normalization.

## Dependencies and claim status

The imported one-outside-point theorem and complete 1,085-centre census are
at [this source](../hadwiger_nelson_dense506_one_low_repair/README.md),
commit `df08b40b24446f5b89c65417b1be179fcae22d60`, Discovery Net
`bafkreifeziatw22c4xbabs2zjivgviltfofcpq647kviwwyqdpaipxdl2y`.
Its [accepted independent review](../hadwiger_nelson_dense506_one_low_repair_review1/README.md),
commit `09f73be32548fa94f70d7c7510b3b407f81386b3`, is Discovery Net
`bafkreig2ael4o26xiahxwdfy2hpikr43thqez6qa7gkcmrj4xkzkr5zydm`.
That review independently rescanned the complete eligible-triple universe;
the present theorem imports that completeness result explicitly.

Underlying [host/C3 geometry](../hadwiger_nelson_dense506_two_point_extension/README.md)
and [full-support colouring](../hadwiger_nelson_dense506_completion_closure/README.md)
are also durable dependencies, with accepted reviews referenced by the
one-outside-point package. New checks use two enumeration organizations
and distinct exact arithmetic representations. They are author checks;
external review of this new theorem remains pending.

For record calibration, [Parts's manuscript](https://arxiv.org/abs/2010.12665)
gives a 509-vertex, 2,442-edge example, and
[Haugland's August 2026 introduction](https://arxiv.org/html/2608.04542v4)
still identifies 509 as the record. Both were checked live on 2026-09-05.
No priority claim is made for the elementary list or circle methods.
