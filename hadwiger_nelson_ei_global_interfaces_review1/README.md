# Independent review of the 8,585-point EI composition

## Verdict

**ACCEPT** Discovery Net artifact
`bafkreihr3w4jesm4iqclmb7e3a47fbnriky4ueahs5zlgqeiifz3jggjxa` (h3885),
reviewed at source commit `cf662bafba272382968b3128a68a8173e3eb7a6e`.
The [reviewed source package](https://github.com/helgithorskarp/math_results/tree/main/hadwiger_nelson_ei_global_interfaces)
is public on the repository's main branch.

The accepted theorem is that the specified strict unit-distance graph on
exactly 8,585 distinct plane points is not four-colourable. It is not a graph
on at most 508 vertices, not a record improvement, and not a computation of
the graph's exact chromatic number.

## Proof rederivation

The exact intermediate graph `J` has 1,167 vertices and all 6,472 actual unit
edges among them. Its marked points `O` and `V` are distance `8/3` apart. The
certificate selects 20 of its 321 physical equilateral triangles of side
`1/sqrt(3)`.

The submitted CNF is definitionally the following statement: give every
vertex exactly one of four colours, forbid equal colours across every unit
edge, require each selected triangle to be nonmonochromatic, and pin `O` to
colour 0 and `V` to colour 1. It has 4,668 variables and 34,139 clauses. Any
colouring with differently coloured endpoints can be globally renamed to
those pins. The checked LRAT empty-clause derivation therefore proves:

> every proper four-colouring of `J` satisfying the 20 triangle restrictions
> gives `O` and `V` the same colour.

For every selected triangle an explicit proper colouring of all of `J` makes
exactly that triangle monochromatic and respects the other 19 restrictions.
Thus this particular 20-element support is inclusion-minimal. This does not
establish minimum cardinality among all subsets of the 321 triangles.

The T375 graph has 375 distinct vertices and 1,661 unit edges. Its marked
triangle has side `1/sqrt(3)`, it has an explicit proper four-colouring, and
no proper four-colouring makes all three terminals equal. Attaching an exact
isometric T375 copy to each selected triangle consequently enforces all 20
premises. The completed half `H` has 4,293 distinct points, and every proper
four-colouring of it gives `O` and `V` the same colour.

Rotate `H` about `O` using

```
cos(theta) = 119/128,   sin(theta) = 3*sqrt(247)/128.
```

The multiplier has unit norm and the two images of `V` are one unit apart,
because `2*(8/3)^2*(1-119/128)=1`. Both would have `O`'s colour, contradicting
that unit edge. All unrotated points lie over
`Q(sqrt(3),sqrt(11))`; since `sqrt(247)` is outside that biquadratic field,
an unrotated point whose rotated image also lies there must be `O`. Exact
radical-set intersection independently gives the same result. The union order
is therefore exactly `2*4293-1=8585`.

Only genuine component unit edges are needed for the contradiction. Taking
the strict unit graph adds any further cross-component unit edges and cannot
restore a four-colouring.

## Independent reproduction

The reviewed 14-entry package manifest and the complete manifests of its two
pinned source packages passed. With Python 3.11.2,
`python-sat==1.9.dev15`, CaDiCaL 1.9.5, and DRAT-trim commit
`2e3b2dc0ecf938addbd779d42877b6ed69d9a985`, the omitted artifacts regenerated
byte for byte:

- CNF: 472,166 bytes, SHA-256
  `0755271bc61f32262c16eba4b34f7fbe7e43f5a25ad1f13e79fe900c4b5e5df8`;
- DRAT: 6,425,642 bytes, SHA-256
  `cd83313e1be9dee1c5563fc6780168955426adc5df0cdd4653ecdfb72c0d3d81`;
- LRAT: 9,703,294 bytes, SHA-256
  `42b21b1f72468e27d73fa7d3adfa273d691f590df2231f21f3090a32f4f8014a`.

The package's standard-library checker verified 22,714 RUP additions and
1,188,643 propagation hints through the empty clause. A separate compiled C
`lrat-check` also reported `VERIFIED`. Normal and assertion-disabled complete
verification agreed. The deterministic 154-query deletion pass reproduced
the certificate exactly with 89,383 conflicts and no unknown outcome.

`independent_check.py` imports no reviewed module. It:

- reconstructs the coordinates from the raw tables in an exact bit-indexed
  basis for `Q(sqrt(3),sqrt(11),sqrt(247))`;
- checks all 680,361 intermediate point pairs directly, without the producer's
  modular edge filter;
- rebuilds and compares every CNF clause and independently checks every LRAT
  hint;
- verifies all 20 deletion colourings;
- proves the T375 terminal obstruction with a separate DSATUR-style named-
  colour search, exhausting 21,593 nodes rather than using the submitted
  domain-propagation traversal;
- rebuilds all 20 exact gadget placements, the rotation, intersection, orders,
  and point-set hashes.

From a detached checkout of the reviewed source commit, after regenerating
`half.cnf` and `half.lrat` outside the repository, run:

```bash
python3 -B hadwiger_nelson_ei_global_interfaces_review1/independent_check.py \
  --source /path/to/reviewed-checkout \
  --cnf /path/to/half.cnf \
  --lrat /path/to/half.lrat
```

The compact result is in `REPRODUCTION_RESULT.json`. Generated proof files,
virtual environments, binaries, and logs are intentionally omitted.

## Trust boundaries

The numerical G40, G49, and appendix tables are hash-pinned transcriptions of
the cited [Exoo--Ismailescu source](https://arxiv.org/abs/1805.00157v1); this
review did not independently retype them from the paper. The theorem also trusts exact Python integer/Fraction
semantics, the written radical-basis and isometry reductions, the two LRAT
checkers, the two exhaustive T375 searches and their colour-symmetry arguments,
SHA-256, ordinary compiler/runtime behavior, transcription, and hardware.
There is no proof-assistant formalization or external-author review.
