# Disjoint mixed506 placements: one hub, degree at most ten

Fix `B=A union ((5+i sqrt(11))/6)A`, where `A` is the archived 159-vertex
Parts gadget, and let `V` be the archived 214-vertex gadget. A disjoint
`B union g(V)` has 506 vertices. Count only edges joining the two components
when referring to **cross degree**; call a vertex of cross degree at least
three a **hub**.

**Every disjoint placement that is not already covered by the base-field
four-coloring has at most one hub, on either side, and its degree is at
most ten.** All other cross degrees are at most two. Exact examples attain
ten with the hub on either side. Moreover, a non-four-colorable disjoint
placement with a hub must use a rotation multiplier of degree exactly two
over `E=Q(i sqrt(3),i sqrt(11))`.

The general argument is short: three unit neighbors in `E` determine their
center in `E`; two distinct points of `E intersection g(E)` force `g(E)=E`.
The finite computation sharpens this for the fixed gadgets by determining
all possible external centers.

| Component | Vertices | External unit-circle centers with at least three neighbors | Maximum degree |
|---|---:|---:|---:|
| Fixed inner union `B` | 292 | 881 | 10 |
| Gadget `V` | 214 | 534 | 10 |

Every disjoint placement with a hub lies in one of
`881*214 + 534*292 = 344,462` labeled center/anchor families. These are
families with a continuous rotation parameter, not enumerated placements.
The argument closes higher-degree and transcendental rotations within these
families: their only cross edges form a star, which can be four-colored.

[PROOF.md](PROOF.md) states all quantifiers, gives the general reduction,
the exact census and its independent algorithmic audit, and two explicit
sharpness examples. No priority claim is made for the elementary geometric
argument.

**This does not close all disjoint placements or the quadratic angular
families.** Placements with no hub remain open. Both displayed 506-vertex
graphs are four-colorable; no record improvement or five-chromatic graph is
produced. This pass does not enumerate another overlap stratum, the sealed
Parts pool, or the parked Parts two-overlap family.

## Reproduce

Use Python 3.11 or later, standard library only, from this directory in a
complete repository checkout. Keep the regenerable catalogs outside git:

```bash
python3 verify.py --catalog-dir /tmp/mixed506-centers > /tmp/mixed506-summary.json
cmp expected.json /tmp/mixed506-summary.json
python3 audit_triangles.py --catalog-dir /tmp/mixed506-centers > /tmp/mixed506-audit.json
cmp expected_audit.json /tmp/mixed506-audit.json
python3 check_examples.py > /tmp/mixed506-examples.json
cmp expected_examples.json /tmp/mixed506-examples.json
sha256sum -c SHA256SUMS
```

The circle-intersection generator classifies all 65,277 unordered pairs,
finds every unit-circle center in `E` and retains those with at least three
neighbors. The independent auditor accounts for all 5,717,544 triples,
tests the 3,631,478 with all sides at most two using an integer Heron identity,
and reconstructs centers by linear equations. It matches every retained
center and complete neighbor set. The catalogs are generated on request and
hash-bound in `expected.json`; no catalog dump is committed.

The standalone example checker uses a different real radical basis and tests
all 127,765 pairs for each of two exact coordinate sets. Each has 506 distinct
vertices and 2,238 strict unit edges, with exactly ten cross edges forming
a single star. Proper four-colorings are checked on every edge.

On the producing host, CPython 3.11.2 ran the generator in 7.54 seconds
(31.4 MiB peak RSS), the triangle audit in about 17 seconds (30 MiB), and the
two direct examples in 3.97 seconds (16.2 MiB). No solver or approximate
arithmetic is required.

## Coloring-library screen and scope

For each center, the generator also computes which colors remain free at
that center under each row of the existing eight-`B`/seven-`V` library.
Every row is checked on the component's internal edges. For a row, the free
mask is the complement of the colors present among the center's neighbors.
This tests adding that center individually, not coloring all external centers
simultaneously.

The original first row already leaves a free color at every external center
on each side. Thus local star attachments do not even require the previous
coloring repairs. Additional cross edges, or a placement with no hub, are
needed for any chromatic obstruction. A local extension mask is not a
coloring certificate for the whole angular family.

## Dependencies and trust

Coordinates and their [provenance](../hadwiger_nelson_nonmono159_214_lowden2/SOURCE.md),
the fixed [inner union](../hadwiger_nelson_nonmono159_moser_triple/README.md),
the [whole-field coloring](../hadwiger_nelson_nonmono_field_obstruction/PROOF.md)
and existing [positive rows](../hadwiger_nelson_mixed505_high_degree_attachments/README.md)
are reused with hashes. The main program uses the prior integer input
constructor and rational field implementation. The triangle auditor parses
the coordinates separately, performs integer arithmetic in `Z[sqrt(33)]`,
and solves two linear equations instead of intersecting circles. The direct
example checker imports neither of those programs.

These are author cross-checks with different mathematical reductions,
not external peer review or proof-assistant formalization. The analytical
center, field and degree arguments remain unformalized. Other trust boundaries
are the exact programs, pinned coordinates and dependencies, and ordinary
software execution. No SAT verdict, floating-point distance or omitted
large proof certificate is used.
