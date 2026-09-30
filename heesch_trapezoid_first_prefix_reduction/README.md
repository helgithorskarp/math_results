# Necessary first-prefix subsets for a curved Heesch tile

**six-heesch-3, researcher.** For the unchanged connected unmarked curved
tile T, every first prefix of at least three strict coronas contains the
root and one of 115 exact subsets. All real translations, rotations,
reflections and arbitrary prefix topology are allowed. The subsets are
necessary partial configurations, not complete first coronas.

A new four-copy strip-cap lemma localizes a previously closed 11-copy branch:
the four copies have no two successive strict surrounds. One is possible.
The inherited `4 <= Hc(T) <= Hh(T) <=85` is unchanged; finite seven is open.

From the repository root, CPython 3.11+ standard library, assertions enabled:

```sh
python3 -B heesch_trapezoid_first_prefix_reduction/check.py --expected heesch_trapezoid_first_prefix_reduction/expected.json
python3 -B heesch_trapezoid_first_prefix_reduction/check.py --expected heesch_trapezoid_first_prefix_reduction/expected.json --controls
```

Expected: 110 pose variables,501 validated clauses,115 necessary subsets,
316 root-gap trials,57 RUP additions, and the unchanged12/45/94/147-copy
positive prefixes. Five malformed input controls reject. `-O` is rejected
because imported geometry uses assertions.

[proof.md](proof.md) gives the precise theorem, new protected-feature lemma,
generation guards and phase-locking argument. [input.json](input.json)
defines T, the pose dictionary,115 subsets and positive fixture.
[certificate.json](certificate.json) contains the compact geometric core;
[proof.rup](proof.rup) is its small checkable Boolean refutation.
[dependency_pins.json](dependency_pins.json) records the required existing
repository files. Geometry primitives and earlier mathematical checks are
deliberately reused with provenance; exact Python and written geometric
bridges remain trust boundaries. No independent review or formalization.

No native solver or large search corpus is required. Private adaptive SAT
inventories, dense discovery formulas, graph projections and logs are omitted.
The public result does not depend on enumeration completeness of those files.
