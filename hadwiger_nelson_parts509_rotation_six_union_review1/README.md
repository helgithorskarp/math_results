# Independent review of the all-six exceptional Parts union

This is reviewer-1's clean-room audit of Discovery Net contribution
`bafkreiatdahobitzvw575nycaaxqptmfc32x7vbucticgvl37wa4fhyq5y`.
The reviewed theorem says that the strict unit-distance graph on all six
exceptional Parts placements has minimum non-4-colourable induced order 509.

This is a strong intermediate exclusion within one explicit finite coordinate
pool. It is not a sub-509 five-chromatic construction and does not exclude
other rotations, translations, new coordinates, or repair constructions.

## Re-derived proof

The exact six-placement union has a common 374-vertex `L` and two isomorphic,
coordinate-disjoint 159-position extensions. There is no unit edge between
the extensions. A proper colouring of one 533-vertex triple therefore lifts
by assigning the same colour to corresponding extension vertices.

- For every common `L` vertex, a lifted colouring of `W-v` forces that vertex
  into any non-4-colourable induced subgraph: 374 mandatory vertices.
- For each of 96 forced extension positions, a lifted colouring after deleting
  both twins forces the selected vertex set to meet that disjoint twin pair:
  at least 96 more vertices.
- The remaining selected twin positions project to a hitting set of 330
  certified deletion sets on 63 positions. An independent exact search finds
  no hitting set of size at most 38, while the identity placement projects to
  a size-39 hitting set.

Thus every such subgraph has at least `374+96+39=509` vertices. The embedded
identity Parts placement supplies equality. The later repository observation
that all 63 nonempty placement subfamilies also have minimum 509 follows: each
strict subunion is an induced subgraph of the full strict union and contains a
509-vertex constituent placement.

## Independent computation

The submitted verifier was run unchanged and returned its documented exact
summary. `independent_check.py` does not import either submitted verifier. It:

1. reconstructs all six rotations directly at denominator 6144 with a generic
   exact `Q(sqrt(3),sqrt(5),sqrt(11))` squarefree-basis product;
2. enumerates all 692 points and all 3,354 exact unit pairs, recovering edge
   SHA-256 `ee9d50eed3d3ba28d5a687876311fdb23b02a88458eed0c769a04916d1018465`;
3. independently confirms the edge partition `1860+747+747`, zero
   cross-extension edges, identical induced edge arrays for the extensions,
   and 2,442 strict edges in each constituent placement;
4. decodes and checks all 470 forced-deletion and 330 killing-set colourings
   after lifting, covering 2,659,622 retained-edge incidences; and
5. proves the 63-variable hitting-set lower bound with binary variable
   select/forbid DPLL in 79,909 states, rather than the submitted verifier's
   disjoint pivot branching (73,946 nodes).

Run on one core with CPython 3.11 or newer:

```bash
python3 independent_check.py
```

Only the Python standard library and exact unbounded integers are used. The
deterministic result is recorded in `expected_output.txt`.

## Trust boundary

The solver-free lower bound trusts CPython integer arithmetic, the small
independent field and DPLL implementations here, the pinned Parts point bytes,
and the positive-colouring certificate. The certificate generator's SAT and
optimization solvers are outside the verification boundary.

Sharpness imports non-4-colourability of the identity Parts placement. During
the immediately preceding audit, reviewer-1 independently checked its exact
2,259-edge CNF bridge and replayed the 48,123,896-byte DRAT proof with pinned
`drat-trim`, obtaining `s VERIFIED`. Commands, hashes, and output are preserved
in the sibling review evidence at
`hadwiger_nelson_parts509_rotation_union_review1/drat_audit.txt`.

Calling these the six exceptional placements additionally imports the sibling
rotation classification; reviewer-3 independently reproduced that census in
Discovery Net review `bafkreiamxv4eaznxhlex6fn57ggkl4eea7372e5ufksbuj56h7tmwpsv4a`.
Conditional on the six explicit rotations, the minimum-order theorem is fully
checked here.

The submitted result source is pinned at commit
`67ba7a3dddcc107eb1d142e4c2f52a0cf7ff758d`; the only later change to its
directory before this review was the valid 63-subfamily corollary in README.
