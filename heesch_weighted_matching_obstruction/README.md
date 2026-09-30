# Additive matching charges and finite corona certificates

Author: **six-heesch-3**, role: researcher, updated 2026-09-30.

This note gives an exact classification of scalar additive charges for an
atomic boundary matching table, and turns any positive charge into an explicit
upper bound on complete corona depth. It is a structural reduction for the
finite-Heesch-number search, **not a seven-corona construction**.

[quartic_realization.md](quartic_realization.md) closes the geometric matching
bridge for complementary colored unit-edge polyforms using explicit rational
quartic profiles. It preserves valid grid corona constructions under rotations
and reflections and proves finiteness without assuming that all geometric
patches align with the original grid.

[hex_grid_locking.md](hex_grid_locking.md) proves the converse for complete
coronas of quartic decorated regular polyhexes, including flat edges:
arbitrary Euclidean placements align with the central honeycomb, and disc
prefixes correspond exactly to the complementary marked-grid model.
[marked_corona.md](marked_corona.md) gives the constructive port-graph
criterion, a marked SAT adapter with independent witness checks, a checked
1260-marking rectangle exclusion, and an exact `H_c=5` curved hexapillar
baseline reproduction. There is still no seven-corona construction.

[atomic_grid_locking.md](atomic_grid_locking.md) now extends grid locking to
fully nonflat polyominoes and polyiamonds as well as polyhexes. Its local
filled-contact cycle uses whole-port endpoint matching, including at
collinear joins. [quintic_realization.md](quintic_realization.md) realizes
self-compatible colors and directed states with positive odd quintic
profiles: complete geometric coronas force a common handedness and exactly
the specified rotations-only grid model. Color-only outer-hole coronas
also correspond exactly. The explicit matching/motion table is essential.

[self_color_refinement.md](self_color_refinement.md) gives a canonical
refinement rule and a checked dead end: after the five-corona baseline is
reinterpreted with uniform handedness, both port components have self-loops,
all directed states vanish, and its strongest two-color marking tiles
periodically. No compatible color/state refinement of that fixed patch
yields a finite record. Both new checkers use only the standard library:

```
python3 heesch_weighted_matching_obstruction/quintic_profiles.py
python3 heesch_weighted_matching_obstruction/self_color_refinement.py
```

[mixed_hand_profiles.md](mixed_hand_profiles.md) retains the original
reflections of that five-corona fixture and characterizes all function-valued
normal profiles preserving its full unit-port contacts. Every odd part
vanishes; the even parts are signed copies of one symmetric function and
port 17 stays flat. An 18-equation geometric core has determinant four.
This excludes this fixed-patch profile-refinement route without classifying
other five-corona patches. Run the standard-library certificate with
`python3 heesch_weighted_matching_obstruction/mixed_hand_profiles.py`.

[endpoint_rigidity.md](endpoint_rigidity.md) now allows the original 18
boundary vertices and all surrounding poses to vary near that fixture. An
exact `2410 x 426` endpoint Jacobian has rank 422; its kernel consists precisely
of translations, rotation and scaling. The implicit function theorem gives
local rigidity modulo similarities, provided the same complete labelled
endpoint network is preserved. A 422-square minor has determinant 379 modulo
1009. Run `python3 heesch_weighted_matching_obstruction/endpoint_rigidity.py`.
Other contact networks and large deformations remain open.

Combinatorial imbalance as a reason for nontiling is established prior art.
Mann discusses it for marked hexagons and polyhexes, including a size-dependent
upper bound. The contribution here is the explicit matching-table criterion,
optimal charge ratio within this class, and the integer depth certificate with
its geometric assumptions exposed. No priority claim is made for the general
imbalance principle or for the elementary graph linear algebra.

## Model and geometric obligations

Let a compact planar tile have area at least `a > 0` and squared diameter at
most `d2 > 0`. Every copy carries the same finite multiset of boundary ports.
Port types form a finite set `L`; `c(l)` is the number of ports of type `l` on
one tile. An undirected graph `G` on `L`, with loops allowed, overapproximates
the types that may match.

The essential **atomic matching hypothesis** is the following: when a tile is
contained in the interior of the union of an admissible patch, each of its
ports is paired with exactly one port on a different tile of that patch;
pairings are one-to-one, and the paired types are an edge of `G`. Ports of
boundary tiles may be unpaired. All rotations and reflections allowed in the
geometric problem must obey this hypothesis and the same per-copy counts.

The theorem applies directly to a marked, edge-to-edge model with these rules.
For an unmarked polygon, one must separately prove that its geometry enforces
atomic matching and that `G` includes **every** actual pairing. Assigning colors
to a drawing does not prove either fact. Partial-edge contacts, splitting a
port among several tiles, or a reflection that invalidates the labeling can
destroy the argument. There is no claimed geometric realization of the
synthetic fixtures below.

For complete coronas write `P_i` for the union of the central tile and its
first `i` coronas. Require disjoint tile interiors, `P_(i-1)` contained in the
interior of `P_i`, and each new tile touching a tile in an earlier corona.
Touching only the immediately preceding corona is also allowed. The usual
hole-free convention is a special case. The proof also permits holes in the
outermost corona when strict containment of the previous patch is retained.

## Lemma 1: classify all scalar matching charges

A scalar additive charge is a function `w: L -> R` satisfying

`w(l) + w(m) = 0` for every allowed pair `{l,m}`.

On a nonbipartite connected component, including a component containing a
loop, `w` is identically zero. On a bipartite component with parts `U,V`, it
has the form `+t` on `U` and `-t` on `V`. An isolated vertex is a bipartite
component with an empty second part.

Consequently a charge with strictly positive total charge on a tile exists
if and only if some bipartite component has

`p = sum(c(l), l in U) != q = sum(c(l), l in V)`.

Proof: following an edge changes the sign of `w`. An odd cycle forces its
starting value to be its own negative. In a bipartite component the parity of
a path is well defined, giving precisely the stated one-dimensional space.
The charge on one tile is the sum of `t*(p-q)` over bipartite components.
This sum can be positive exactly when at least one coefficient is nonzero.

## Lemma 2: optimal growth ratio in this charge class

For any charge let `B` be the sum of its positive port weights on one tile
and `S` the absolute sum of its negative port weights. A positive tile charge
means `B > S`. For each bipartite component orient its parts so `p >= q`.

If `p > 0` and `q = 0` for some component, one corona is impossible: there is
no occurrence of a matching negative type on any copy. Otherwise the largest
ratio `B/S > 1` among all additive charges is

`alpha = max(p/q)` over the imbalanced bipartite components.

It is attained by assigning weights `+1,-1` to that single component and zero
to all other types. In particular mixing multiple components cannot improve
the ratio.

Proof: a component with amplitude `|t|` contributes either `(p|t|,q|t|)` or
`(q|t|,p|t|)` to `(B,S)`. For positive denominators the combined ratio is a
weighted average of the component ratios, with weights equal to their
contributions to `S`. Components with no port occurrences contribute nothing.
The zero-denominator case is handled separately above.

## Lemma 3: an explicit finite-depth obstruction

Take a component with integer counts `p > q > 0`. Define

`m_0 = 1`, `m_(i+1) = ceil(p*m_i/q)`,

`u_i = floor((22/7)*(d2/a)*(i+1)^2)`.

If `m_k > u_k`, there is no admissible complete `k`-corona patch; hence the
Heesch number in this model is at most `k-1`. Such a `k` always exists. These
statements require no finite-neighbor assumption or underlying lattice.

Proof: let `N_i` count the tiles in `P_i`. Every positive port on every tile of
`P_(i-1)` must match a distinct negative port in `P_i`, so

`p*N_(i-1) <= q*N_i`.

Induction and integrality give `N_i >= m_i`. Fix a point `x` in the central
tile. A tile in corona `j` has a chain of at most `j+1` mutually touching tiles
back to the central tile. Any of its points is at distance at most
`(j+1)*sqrt(d2)` from `x`, by the triangle inequality across the contact
points. Thus `P_i` is contained in a disk of radius `(i+1)*sqrt(d2)`.
Disjoint interiors and the area lower bound give

`N_i*a <= pi*d2*(i+1)^2 < (22/7)*d2*(i+1)^2`,

so `N_i <= u_i`. Finally `m_i >= (p/q)^i`, and an exponential with base
greater than one eventually exceeds this quadratic upper bound.

The bound is deliberately conservative. For fixed geometry, Lemma 2 selects
the strongest recurrence obtainable from this scalar charge method. It does
not claim to give the true Heesch number or the best possible obstruction.
When the classifier finds no charge, it reports only failure of this method;
it gives no evidence that the tile tiles the plane.

## Lemma 4: a compact upper certificate without a depth search

There is also a closed integer bound. Put

`c = (22/7)*(d2/a)`, `r = ceil(q/(p-q))`,

`C = ceil(c*(r+1)^2)`, `s = max(8, bit_length(C))`, `K = 2*r*s`.

Then no complete `K`-corona patch exists, so `H <= K-1`. All these quantities
are calculated exactly using integer and rational arithmetic. The compact
certificate records `r,C,s,K`; it does not require calculating a huge power
or running a long recurrence.

Proof: Bernoulli's inequality gives `(p/q)^r >= 1+r*(p-q)/q >= 2`.
By the definition of bit length, `2^s > C`. For every integer `s >= 8`,
`2^s >= 4*s^2`: equality holds at eight, and induction follows from
`2*s^2 >= (s+1)^2`. Hence

`(p/q)^K >= 2^(2*s) > C*4*s^2 >= c*(r+1)^2*(2*s)^2 >= c*(K+1)^2`.

Lemma 3 now excludes depth `K`. This also gives an explicit quantitative
bound when the finer first-failure recurrence is stopped at an operational
depth limit. It is a proof-derived bound, not an interpretation of a timeout.

## Reproduce and check

Python 3.11.2 was used; Python 3.10+ and its standard library suffice. No
solver, floating-point arithmetic, generated geometric data, or external
certificate is involved.

```sh
python3 heesch_weighted_matching_obstruction/obstruction.py examples
python3 heesch_weighted_matching_obstruction/obstruction.py self-check
python3 heesch_weighted_matching_obstruction/obstruction.py solve MODEL.json
```

The model JSON has `counts`, `pairs`, `area_lower` and
`diameter_squared_upper`; rational numbers can be integers or fraction
strings. Geometry bounds and the matching hypothesis are inputs, not facts
verified by the program. `--max-depth` bounds the optional refinement of the
closed bound by the recurrence; hitting it reports that refinement as
`incomplete`. The independent closed bound remains justified by Lemma 4.

Compact fixtures include a standard marked-hexagon count model with three
nicks, two bumps and one flat side; a globally balanced two-color model in
which a single color nevertheless gives an obstruction; an odd-cycle table;
and a type with no possible matching occurrence. They test the structural
lemmas, without certifying any lower corona bound. The marked-hexagon example
uses `d2=4` and `a=5/2` for its undecorated regular hexagonal footprint:
`area=3*sqrt(3)/2 > 5/2`. Those numbers are not asserted for an unmarked
polygon obtained by modifying that footprint.

The independent finite check enumerates all matching graphs, including loops,
on one to three types and all nonzero count vectors with entries in
`{0,1,2}`. It compares the component classifier and optimum ratio against
direct enumeration of charge vectors in `{-2,-1,0,1,2}^L`: **1,732 models**.
This check validates the implementation on those instances; the all-size
claims rest on the proofs above. Integer recurrence and malformed-input
checks are also performed. Expected output is in `expected.json`.

## Universal color-family upper certificate

[cover_tiling_dichotomy.md](cover_tiling_dichotomy.md) proves that every
self-color marking of the bent four-hex base
`{(0,0),(1,0),(2,0),(2,1)}` admitting a rooted radius-seven cover has one of
eleven checked periodic tilings. This covers all Bell(18) port partitions;
every finite zero-state quintic realization has **Hc,Hh<=6**. The final
346,961-clause CNF has an independently checked RUP contradiction.

A compact five-color fixture has **Euclidean Hc=2**, with two directly
checked coronas and an independent third-corona RUP exclusion. Its profile
matching-table additive charge is zero. The documented Hh interval is2–3.

```sh
python3 heesch_weighted_matching_obstruction/cover_tiling_certificate.py check
python3 heesch_weighted_matching_obstruction/cover_tiling_certificate.py check-corona
```

The linked proof gives the full encoding, pinned dependencies, regeneration
commands, hashes and trust boundaries. Large generated inputs and proofs
stay in scratch. The old directed-state numeric inputs returned UNKNOWN;
the stronger result below resolves that branch. No seven-corona finite
record is claimed.

[directed_cover_tiling.md](directed_cover_tiling.md) strengthens this to **all
self-colors and ternary directed states** on the same bent base: a rooted
radius-five cover forces one of twelve checked periodic tilings. Direct
equivalence-relation variables remove numeric color naming. The cold
80,679-clause formula has an independently verified RUP contradiction.
Every finite curved member therefore has **Hc<=4 and Hh<=5**; with zero
states Hh<=4. The known Hc=2 fixture has a checked radius-four cover, so the
cover/tiling threshold is sharp while actual corona depth remains distinct.

```sh
python3 heesch_weighted_matching_obstruction/equivalence_certificate.py check
python3 heesch_weighted_matching_obstruction/validate_equivalence.py
```

The second command needs Python-SAT and the pinned Circuit dependency.
The proof supplies the independent checker commands, hashes and limits.

[zigzag_cover_tiling.md](zigzag_cover_tiling.md) proves the same sharp
radius-five criterion on the distinct zigzag base
`{(0,0),(1,0),(1,1),(2,1)}` for **all self-colors and ternary states**.
Its 22 checked periodic motifs and independently verified RUP contradiction
exclude finite curved **Hc>4 or Hh>5** in this second family. A new two-color,
zero-state example has a checked radius-four cover and exact **Euclidean
Hc=2**, with a direct two-corona witness and a third-corona RUP exclusion.
The rooted-cover criterion is sharp; the maximum finite corona depth over
all markings is not determined.

```sh
python3 heesch_weighted_matching_obstruction/zigzag_cover_certificate.py check
python3 heesch_weighted_matching_obstruction/zigzag_cover_certificate.py audit
```

The contact audit needs the pinned Circuit dependency and checks every pair
in the full research instance. The proof gives exact regeneration and
independent checking commands for both contradictions.

## Literature and remaining frontier

- C. Mann, *Heesch's Tiling Problem*, American Mathematical Monthly 111
  (2004), 509-517. [Author's manuscript](https://faculty.washington.edu/cemann/Heesch.pdf).
  The imbalance principle and the marked-polyhex context are prior work.
- B. Bašić, *A Figure with Heesch Number 6: Pushing a Two-Decade-Old Boundary*,
  Mathematical Intelligencer 43 (2021), 50-53.
  [Open full text](https://pmc.ncbi.nlm.nih.gov/articles/PMC7812982/).
  Its triangle/hexagon resource deficit is a different specific realization;
  we do not reprove the omitted grid-alignment cases or its corona exclusion.
- C. S. Kaplan, *Heesch Numbers of Unmarked Polyforms*.
  [Primary manuscript](https://arxiv.org/abs/2105.09438),
  [data page](https://cs.uwaterloo.ca/~csk/heesch/).
  Grid alignment is part of the polyform model, and outer-hole conventions
  must be distinguished.
- C. S. Kaplan, *The Path to Aperiodic Monotiles* (2025).
  [Primary manuscript](https://arxiv.org/html/2509.12216v1).
  It still reports six as the largest known finite Euclidean Heesch number.

The concrete next frontier is a new seven-corona patch admitted by one of
the explicit matching/motion tables above, with a sound finite upper
obstruction. An imbalanced complementary or directed color supplies the
additive upper bound. A complete checked grid upper exclusion or a separate
marked nontiling proof is another route for the realized subclasses.
The canonical refinement result excludes using the specified uniform
five-corona strip patch to obtain finiteness; other patches remain open.
The seven-corona construction is still missing.

The unlimited-size unmarked-polyform-five target needs a prior-art
qualification: six-heesch-2's
[215-cell polyiamond reproduction](../heesch_polyiamond_hexapillar/README.md)
realizes Mann's known hexapillar with five directly checked coronas and a
written finite all-motion upper bound. The remaining construction target
for this lane is the general Euclidean finite-seven frontier.
