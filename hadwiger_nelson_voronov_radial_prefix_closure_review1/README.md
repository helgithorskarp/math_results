# Independent review: VND M2 radial-prefix closure

## Verdict

**ACCEPT** as a valid intermediate exclusion theorem, not as a construction of a
sub-509-vertex five-chromatic unit-distance graph.

The reviewed contribution is Discovery Net artifact
`bafkreiewtuds4t3hdtjb63kmll633g6e5tanhmjqtrzm6hsxsuekxg4e7q` at source
commit `ae25d720d91050a7861b1daf1a825882f9771f6e`.  Its claim is correct for the
stated family: two origin-centred, uniformly radial prefixes of the clipped VND
set M2, with nominal combined budget at most 508, are four-colourable for every
relative rotation.

## Independent checks

[`independent_verify.py`](independent_verify.py) is a clean implementation that
does not import the submitter's code.  It reconstructs the two generators and
M1/M2 over `Q(sqrt(2),sqrt(3))`; enumerates and exactly orders all radial shells;
enumerates every budget-admissible oriented shell pair; checks domination by the
six maximal pairs; recomputes the exact radius-sum margins; reconstructs all
127,260 candidate pairs of K505 and its 216 unit edges; and validates both the
published bipartition and bipartiteness independently with a parity disjoint-set
structure.

The checker also differs materially in its exact sign procedure.  The submitted
checker encloses radicals by rational intervals.  This checker writes a field
element as `u + v sqrt(3)`, with `u,v in Q(sqrt(2))`, and decides both nested
quadratic comparisons by exact rational square comparisons.  All checks use an
explicit exception-raising `require`, and normal and `python -O` runs agree.

The recomputed values are recorded in [`review_result.json`](review_result.json):

- `|M1| = 73`, `|M2| = 865`, and 21 radial shells;
- 50 budget-admissible oriented pairs, all dominated by exactly
  `(241,241)`, `(289,217)`, `(361,145)`, `(433,73)`, `(457,25)`, `(505,1)`;
- strictly positive exact linear and squared radius-sum margins for every one of
  those six pairs;
- K505 has exactly 216 unit edges and is bipartite (307 components, including
  isolated vertices);
- byte identity with the certificate having SHA-256
  `443047ca455bfd1bf8ebf2cc6c7632e1b06fb455d4e4ea66c96f7e4360225b4f`.

## Proof audit

For squared radii `u,v`, the two checked inequalities

```text
L = 1-u-v > 0,        L^2-4uv > 0
```

are exactly equivalent to `sqrt(u)+sqrt(v)<1`.  Thus for any relative rotation,
every point in one maximal prefix and every point in the other have separation
at most `sqrt(u)+sqrt(v)<1`; no cross-copy unit edge exists.  Componentwise
domination transfers this to all 50 admissible shell pairs, and every arbitrary
radial cutoff is one of these shell prefixes.

The next shell after K505 has 553 vertices, so every single-copy prefix relevant
to a nominal budget at most 508 is an induced subgraph of K505.  The verified
bipartition therefore two-colours both copies.  Colouring a union vertex by the
pair of its two copy-colours gives at most four colours: every unit edge internal
to the first copy changes the first bit, every edge internal to the second changes
the second bit, and the strict radius bound excludes all remaining cross edges.
Extra coincidences under a special rotation only identify vertices and do not
invalidate this argument.

## Reproduction

From a checkout containing the submitted certificate:

```bash
python3 -B independent_verify.py /path/to/hadwiger_nelson_voronov_radial_prefix_closure/certificate.json
python3 -O -B independent_verify.py /path/to/hadwiger_nelson_voronov_radial_prefix_closure/certificate.json
```

Tested with Python 3 from a clean detached checkout of the source commit.  Both
commands print the data in `review_result.json` and exit zero.

## Scope and trust boundary

This result closes only the uniformly radial two-copy M2 family at the stated
nominal budget.  It does **not** exclude non-radial subsets, larger prefixes made
possible by rotation-specific coincidences, constructions using M3 or other
seeds, or unions of more copies.  It is consequently useful negative structural
progress toward the sub-509 target, not the target result itself.

The review trusts Python's integer and rational arithmetic, the checked-in source
commit and certificate bytes, Git/SHA-256 for identity, and the standard algebraic
description of the Voronov-style generators.  The generator formulas and the
reported 73-point M1/M2 setup agree with the construction described in the
[referenced preprint](https://arxiv.org/abs/2106.11824); the prefix theorem itself
is established by the exact reconstruction above rather than imported from that
paper.
