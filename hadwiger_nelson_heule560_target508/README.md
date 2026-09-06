# Every H560 subgraph through order 508 is four-colourable

**The fixed H560 support contains no non-four-colourable subgraph on at most
508 vertices.** Two new explicit colourings complete the decision, building on
the previously certified mandatory vertices and positive covers.

The complete necessary family has 24,832 labelled 508-vertex supports. Earlier
certificates colour 24,760 of them; the two new witnesses colour all 72 remaining
supports. An independent enumeration and exact unit-edge checks verify every
member. This closes both orders 507 and 508 left by the
[previous order-506 result](../hadwiger_nelson_heule560_cylinder508/README.md).

This is a negative result for deletion within this exact H560 support. No
five-chromatic graph with at most 508 vertices, smaller certified obstruction,
or record improvement was found. General H632 subgraphs and other Euclidean
supports are not excluded. The H560 deletion program for the record target is
complete and is retired at this boundary.

## Support and finite reduction

H560 is the induced unit-distance graph on the `retained` vertices of the
[minimization certificate](../hadwiger_nelson_heule632_minimize/certificate.json).
All labels are the original 0..631 host labels. The coordinates are reconstructed
from pinned exact inputs using rational coefficients in
`(1, sqrt(3), sqrt(5), sqrt(15), sqrt(11), sqrt(33), sqrt(55), sqrt(165))`.
The independent geometry checker scales coordinates by 96 and compares integer
radical coefficients of every squared distance. It checks all 199,396 host
pairs, obtains 3,112 unit edges, and verifies distinct points. No floating-point
distance test is used.

The prior M492 singleton-deletion theorem forces every obstruction to contain
the [492 mandatory vertices](../hadwiger_nelson_heule632_minimize/boundary.json).
Proper colourings of six singleton-deletion complements additionally force

```text
310, 393, 454, 539, 578, 615.
```

Let M498 be their union with M492. The original H560 has 62 other vertices.
Each obstruction must also meet every one of these nine disjoint pairs:

```text
{358,362} {361,379} {406,455} {407,440} {409,542}
{431,505} {434,530} {500,571} {604,613}
```

All pairs lie outside M498. The verifier reconstructs and directly checks the
full-H560 complement colourings establishing all six singleton and nine pair
necessities. Their exact source rows are recorded in
[expected.json](expected.json).

A 508-vertex support satisfying these necessities has M498 plus exactly ten of
the 62 optional vertices. There are precisely two disjoint possibilities:

| Case | Choices | Supports |
| --- | --- | ---: |
| One vertex from each pair, and one of the 44 vertices outside all pairs | `2^9 * 44` | 22,528 |
| Both vertices from one pair, and one vertex from each of the other eight pairs | `9 * 2^8` | 2,304 |
| Total | | **24,832** |

No symmetry quotient is used. Any potential obstruction on fewer than 508
vertices can be extended to a 508-vertex support in H560 while preserving these
necessities. Thus colouring every one of the 24,832 supports proves the
statement for **all** H560 subgraphs through 508, including subgraphs with edges
removed. Supports violating a necessity already inherit one of its proper
complement colourings. This is a complete decision, not merely an outer count.

## Positive witnesses and complete classification

The inherited witnesses are the 35 positive rows of the
[global certificate](../hadwiger_nelson_heule560_global_decision/certificate.json)
followed by the five rows of the
[cylinder certificate](../hadwiger_nelson_heule560_cylinder508/certificate.json).
The checker lifts each to full H560 using an explicit matching left-side
colouring, then checks every unit edge. The left data come from the
[separator](../hadwiger_nelson_heule560_separator/certificate.json) and the
[left-relation positive words](../hadwiger_nelson_heule560_left_relation/certificate.json).
No completeness theorem for those tables is used by the final positive proof.

Exactly 72 necessary supports are outside these 40 colourings. The new
[1,852-byte certificate](certificate.json) contains two 632-position colour
strings, with dots exactly at absent host labels:

| New witness | Omitted from H560 | Coloured vertices | Remaining targets first covered |
| --- | --- | ---: | ---: |
| 1 | `{500,609}` | 558 | 64 |
| 2 | `{440,607,612}` | 557 | 8 |

For every enumerated support, the independent checker finds a checked colouring
whose domain contains that support. All 24,832 receive a witness; zero remain.
It directly checks 109,570 inherited and 5,474 new unit-edge inequalities. The
same positive certificates establish the smaller-order cases by restriction.

The only imported mathematical theorem is the M492 mandatory result. The six
later mandatory vertices and nine pair conditions are re-established here from
explicit full-H560 colourings. The new closure requires neither SAT soundness,
an UNSAT trace, the eight-vertex erasure theorem, nor separator completeness.
The completed left-selector classification is not recomputed.

## Search, independence and reproduction

[plan.json](plan.json) was frozen before any new target query. It requires a
complete decision of the whole defined target family or a directly certified
obstruction. The producer first applies all inherited positive covers, then
decides the lexicographically first uncovered support. It grows positive
colourings by direct extension or bounded arbitrary-interior SAT recolouring.

The search oracle has 196 right vertices, 54 canonical selectors and 20 explicit
full-left words: **858 variables, 4,977 clauses, 66,075 DIMACS bytes**. It uses
the previous reduction for discovery, while the final proof checks complete
original-H560 colourings. Both primary queries were SAT. Nine growth queries
returned five SAT and four UNSAT; none was UNKNOWN. There were 78 direct growth
extensions and one growth trial skipped using an old negative core. No growth
exclusion, maximality of a cover, or new negative certificate is claimed.
The complete recorded search took 2.84 seconds with peak RSS 43,504 KiB.

The producer enumerates two Cartesian-product cases. The verifier imports
neither the producer nor its dense geometry: it uses the prior independent
sparse-radical geometry and an include/exclude recursion over all 62 original
optional vertices. The recursion prunes only impossible cardinalities, an
already passed unhit pair, or more unhit pairs than remaining selection slots.
Each unhit pair needs its own further selected vertex, so those prunings are
complete. The verifier compares every support and its first witness assignment,
not just total counts.

All family, coverage and CNF bytes agree among the producer, normal verifier and
optimized verifier. The normal and optimized JSON reports agree byte for byte.
The verifier rejects eight malformed certificates and checks its recursion
against unpruned enumeration on 150 small paired-support cases, containing
1,807 accepted members. All 64 guarded-edge truth cases pass. These are
independent implementations within one research pass, not an external-author
review or proof-assistant formalization. Timings and versions are in
[validation.json](validation.json) and [run_summary.json](run_summary.json).

Run from the repository root with fresh output directories:

```sh
python3 -B hadwiger_nelson_heule560_target508/verify.py --out /tmp/hn560-target-check
diff -u hadwiger_nelson_heule560_target508/expected.json /tmp/hn560-target-check/result.json
python3 -O -B hadwiger_nelson_heule560_target508/verify.py --out /tmp/hn560-target-check-opt
cmp /tmp/hn560-target-check/result.json /tmp/hn560-target-check-opt/result.json
```

Verification requires only Python's standard library, tested with Python
3.11.2, and the repository's pinned inputs. Optional discovery reproduction
requires `python-sat==1.9.dev15` with bundled Glucose 4.1 (`g4`):

```sh
python3 -B hadwiger_nelson_heule560_target508/build.py --out /tmp/hn560-target-search
```

The complete primary solver has no conflict or time budget. A separate growth
solver has 100,000-conflict and one-second interrupt-request limits; UNKNOWN
would merely leave a vertex omitted. Use `--resume` with the same directory
after interruption; verified saved colourings reconstruct the remaining family.
Different native model choices can yield different valid discovery covers.
The published two-colouring certificate is the fixed object checked here.
Raw logs, checkpoints, DIMACS and full family/coverage streams stay local.

Canonical SHA-256 hashes are:

```text
family.txt    4b509201eb51fc039b37626f0fb6b4be72f98232adff30f91e10b14af16435c5
coverage.bin  ec50a55e6a074113e76041f89886ae8f131fa808060becbb93e3996ffa09dc39
oracle.cnf    a1af2b9632b8f1e4eba2afcb0a72215fe9b1fe33f7bbb79673171e6d97858266
```

The family stream lists the ten optional labels of each support in sorted
lexicographic order, comma-separated, with a final newline per support. The
coverage stream stores its first covering row index as an unsigned two-byte
little-endian integer. Indices 0–34 are global witnesses, 35–39 are cylinder
witnesses, and 40–41 are new witnesses. Input and source hashes are supplied in
the plan and `SHA256SUMS`.

HN-3's new
[finite centre-synthesis boundary](../hadwiger_nelson_finite_centre_synthesis/README.md)
and consolidated geometric handoff were inspected. They are separate context,
not a premise. The earlier global result's
[independent review](../hadwiger_nelson_heule560_global_decision_review1/README.md)
also remains relevant. No new host, order, boundary-word prefix, compression
variant or construction phase begins after this complete H560 closure.
