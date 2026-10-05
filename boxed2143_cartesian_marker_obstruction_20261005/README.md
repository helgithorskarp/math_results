# A local branching obstruction for boxed-2143 avoidance

Author: Sage (literature-researcher-1), 2026-10-05.

For every integer m>=2, one fixed pair of minimum and maximum Cartesian trees on
3m-2 positions admits a common prefix of m-1 ranks with m different **viable**
positions for the next rank. Each position extends to a complete permutation
avoiding boxed 2143. Consequently no fixed constant bounds viable next-rank
choices over all tree pairs and feasible prefixes.

The written argument proves an exact occurrence correspondence for a band-marker
map, identifies both Cartesian trees for every input, and supplies avoiding
completion witnesses for every one of the m positions. The proof is
[MARKER_OBSTRUCTION_DRAFT.md](MARKER_OBSTRUCTION_DRAFT.md); its original bytes are
preserved so the subsequent internal review can be matched to that exact version.
The word "draft" records the document's original status, rather than replacing
the later review record.

This is a partial obstruction to multiplying constant local branching bounds.
It gives no bound on the total number of avoiding rank assignments. Many choices
at one prefix can have few continuations. The band-restricted slice of this fiber
has exactly as many avoiders as the original class at length m, so the map repairs
no forbidden input.

The full research problem remains unresolved: if a_n counts permutations of [n]
avoiding boxed 2143, does there exist a finite real C>0 with a_n<=C^n for every
n>=1? A solution requires a uniform exponential bound or a proved unbounded
limsup of a_n^(1/n). This packet establishes neither outcome.

## Definition and conventions

A boxed-2143 occurrence has positions i1<i2<i3<i4 and values

    p[i2] < p[i1] < p[i4] < p[i3],

with no **unselected** point strictly inside
(i1,i4) x (p[i2],p[i3]). The selected inner points are not blockers.
Mathematical positions are one based; Python positions and parent arrays are
zero based. A Cartesian-tree root has parent -1.

## Reproduction

Python 3.11.2, standard library only; one process and no external solver,
floating-point certificate or downloaded input. From this directory:

```sh
python3 -B verify_marker_construction.py --literal-checker received/c74ccd624c90_definition_checker.py --rectangle-checker received/93c4be5fa830_rectangle_checker.py --max-base 6 --max-branch-family 12 --output /tmp/sage_marker_replay.json
python3 -B probe_extreme_rank_choices.py --max-n 8 --checker-path received/c74ccd624c90_definition_checker.py --output /tmp/sage_end_choice_replay.json
```

Expected marker controls: all 873 input permutations of sizes 1..6 have exactly
the asserted complete occurrence sets, both explicit tree formulas, and correct
decoding. For m=2..12, the common prefix has exactly m available positions and all
m specified witnesses avoid according to both checkers. These finite controls
test the separately written uniform proof; they do not establish its infinite
quantifiers. Entry-stream hashes in artifacts/marker_controls_m6_branch12.json
allow comparison without retaining raw exhaustive outputs.

The earlier binary end-choice proposal fails first at length 7, for 4163725:
after ranks 1 and 2 occupy positions 1 and 5 (zero based), the available positions
are 0,3,6, and rank 3 occupies the interior position 3. The finite probe establishes
no smaller counterexample through length 6. This is a separate, precisely scoped
failed rule; it does not characterize all avoidance.

Optional known-encoding audit:

```sh
python3 -B cartesian_fibers.py --max-n 8 --audit-max-n 7 --checker-path received/c74ccd624c90_definition_checker.py --output /tmp/sage_fiber_replay.json
```

It compares the stack and recursive Cartesian constructions and all complete
poset fibers on the 5,914 permutations of sizes 0..7. The larger census is finite
control only. The public evidence omits its bulky family listing.

The literal checker is Lyra's four-index/interior-scan implementation, SHA256
c74ccd624c909386ad151947ae5a4f9c534b58602940ba39371e214d1e5b2149.
The separately derived rectangle checker is Theo's value-interval implementation,
SHA256 93c4be5fa830f6628bc9f2031917f9f05d7bcb729bd2ca151180075df2f00a33.
Explicit exceptions keep the controls active under Python -O.

## Internal review

Theo (literature-researcher-4) accepted all three uniform claims at proof SHA256
bb901334aba7735664bfe9668a16617305e5b4834e2b0944a722eafaef2125d6.
His unchanged full written reconstruction is
[review/SAGE_MARKER_REVIEW.md](review/SAGE_MARKER_REVIEW.md), SHA256
7b595bde7de8b7d486e41b5af9721665dd7bb094ae3013d6ac37738764cde8dd.
It separately accepts the exact H1 counterexample and length-7 minimality;
lexicographic firstness within size 7 and the size-8 fiber table are outside
that review's scope. This is an internal team check, not external peer review
or novelty certification. The generic Cartesian/linear-extension framework is
known prior work.

The review's independently designed replay covers all 873 base inputs, all
77 viable witnesses for m=2..12 and all 874 permutations of sizes 0..6 for
the H1 length assertion. It builds images, interval-extremum trees and ordinary
predecessor sets separately, and compares complete occurrence sets with direct
quadruples and its rectangle checker. Run:

```sh
python3 -B review/check_sage_marker.py --author-dir . --output /tmp/sage_independent_replay.json
```

PORTABILITY_EDITS.json records the sole reviewer-code change: its default
author directory now resolves to this public directory. No mathematical check,
proof or written-review bytes changed. The original independent evidence is
review/sage-marker-reproduction.json. Source-file inventories and manifest hashes
reflect the original reviewed packet; compare the mathematical controls and
entry streams when replaying the compact public layout. The omitted full
fiber listing is not required to reproduce the accepted marker/H1 claims.

## Primary sources and scope

- Avgustinovich, Kitaev and Valyuzhenich, *Avoidance of boxed mesh patterns on
  permutations*, Discrete Applied Mathematics 161 (2013), 43–51, Section 5:
  https://doi.org/10.1016/j.dam.2012.08.015 .
- Kitaev, Qiu and Xu, *Coincidences and Growth of Boxed Mesh Patterns* (2026),
  https://arxiv.org/html/2609.13764v1 , Theorem 4.4(iii), Section 7, Conjectures
  7.4–7.5. The manuscript still labels this growth orbit unresolved when checked
  on 2026-10-05. Its increasing-block doubling result is a different construction.
- Giraudo, *Algebraic and combinatorial structures on pairs of twin binary trees*,
  https://arxiv.org/pdf/1204.4776 , Proposition 4.10 and Theorem 6.3: known
  common-linear-extension and tree-pair framework.
- Chakraborty, Jo, Kim and Sadakane, *Succinct Data Structures for Baxter
  Permutation and Related Families*, ISAAC 2024:
  https://doi.org/10.4230/LIPIcs.ISAAC.2024.17 . Existing min/max-tree encodings
  for Baxter permutations do not count every boxed-2143 avoiding fiber.

No priority claim follows from a targeted search returning no match. Source
publication and graph submission also do not certify a theorem or resolve growth.
