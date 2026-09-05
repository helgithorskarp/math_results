# A complete 1,926-point repair support is four-colourable

The fixed four-colouring of each pinned dense506 host extends to all 1,420
nonhost points having at least three unit neighbours in that host. The
resulting strict graph has 1,926 vertices and 12,074 edges. One compact
colouring therefore closes **every subgraph of this support**, including
all deletion/addition repairs of order at most 508 confined to it.

The [proof](PROOF.md) gives the exact placements and finite reduction.
Singleton propagation leaves a 53-vertex forest with seven edges and lists
of size at least two; tree colouring finishes the construction. The
[certificate](colors.txt) is 1,927 bytes. It is regenerated deterministically
and checked directly. No SAT package is needed for any public command.

This excludes one explicit geometric support. It does not exclude arbitrary
three-point additions, a second completion round, or other placements.
No five-chromatic graph with at most 508 vertices is established. Parts's
[primary paper](https://arxiv.org/abs/2010.12665) gives a 509-vertex,
2,442-edge graph; the introduction of
[Haugland's August 2026 paper](https://arxiv.org/html/2608.04542v4) still
identifies 509 as the record. Both were checked live on 2026-09-05.

## Reproduce

Use CPython 3.11.2 (standard library only) in a full checkout. From this
directory choose a work directory that does not exist:

```bash
completion_work=/tmp/hn-dense-closure
python3 ../hadwiger_nelson_dense506_two_point_extension/verify.py \
  --work "$completion_work" > "$completion_work.census.json"
cmp ../hadwiger_nelson_dense506_two_point_extension/expected.json \
  "$completion_work.census.json"
python3 construct.py --work "$completion_work" > "$completion_work.colors.txt"
cmp colors.txt "$completion_work.colors.txt"
python3 verify.py --work "$completion_work" > "$completion_work.verify.json"
cmp expected.json "$completion_work.verify.json"
python3 audit.py --work "$completion_work" > "$completion_work.audit.json"
cmp expected_audit.json "$completion_work.audit.json"
python3 controls.py > "$completion_work.controls.json"
cmp expected_controls.json "$completion_work.controls.json"
sha256sum -c SHA256SUMS
```

The prior producer writes the 245,622-byte candidate table to the work
directory. This generated table, temporary traces and edge lists remain
local; source and the compact colour row suffice for reproduction. The
new audit reconstructs both complete strict unit graphs using the
independent reviewer's exact arithmetic. See [validation.json](validation.json)
for measured run costs and [expected_audit.json](expected_audit.json) for
both root results. No background process or incomplete certificate is
required.

The constructor is a sufficient method, not a general list-colouring
solver: it rejects a cyclic residual even when that residual is colourable.
[Controls](controls.py) exhaust every nonempty four-colour list assignment
and every graph on zero through three vertices, checking positive outputs
by direct enumeration and every propagation contradiction by brute force.
They also check a colourable four-cycle rejection and ten invalid input or
colour-certificate fixtures.

## Durable dependencies

- [Complete geometric census and arbitrary two-point extension](../hadwiger_nelson_dense506_two_point_extension/README.md),
  source `dc57db82a86037be322374b20b31a65fb73df452`, Discovery Net
  `bafkreie4zkk4azkvyuq5fhjctirmnt36shmedrcaw7d46bykgfuvl4kz4i`.
- [Independent exhaustive review](../hadwiger_nelson_dense506_two_point_extension_review1/README.md),
  source `de9cd586d128b12df93d3fdb228d573fe373575c`, Discovery Net
  `bafkreigf3qsv2knb6xy2rohmyujl52skntuavdh6azhowuaypx2ikoeziy`.
- [Source coordinate provenance](../hadwiger_nelson_nonmono159_214_lowden2/SOURCE.md)
  and the [dense host construction](../hadwiger_nelson_dense506_origin_attachment/PROOF.md).
  Relevant source and data files are pinned in SHA256SUMS.

The previous theorem received external review. This new simultaneous
extension was checked by its author using a separate arithmetic engine and
verification method; external review of this new claim remains pending.
The next distinct construction frontier must use a new point with at most
two neighbours in the original host. The proof derives a necessary
four-neighbour condition for one-deletion/three-point repairs, whose full
candidate universe consists of at most 255,530 intersections of pairs of
host-centred unit circles. That enumeration and all further completion
rounds are unstarted at this checkpoint.
