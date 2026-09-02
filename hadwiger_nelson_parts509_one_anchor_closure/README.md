# The one-anchor family of the delete-5-add-4 closure of the Parts 509-graph: exact enumeration and declared-set computation

**Claim status:** exact computer-assisted theorem (closure of the one-anchor family).  Solver-free certificate: every undeclared pair (A, u) is covered by an explicit proper 4-colouring of G − u that extends to A, replayed by the verifier; declared pairs are conservative; the maximal |Û(A)| is 1 < 5, so no 5-subset D can satisfy D ⊆ Û(A).  Completeness of the enumeration rests on the exact incidence lists of the sibling closures, on the exact identification rule and the audited geometric constants stated below, and on the canonical digest that ties the certificate to the regenerated configuration list.

**Revision (review repairs, chain height 1258).**  Compared with the first published version (commit 6a49f05): (1) the circle-intersection screen is outward-rounded (`d <= 2 + 2^-40`) so that the 79 exact tangencies whose binary64 distance rounds above 2 are no longer omitted, and `tangency_audit.py` classifies every tangency midpoint exactly; (2) the discard of candidate points is a per-member identification rule with residual splitting that does not depend on the radius of a single-linkage component, the run certifies the maximal residual radius, and `config_digest.py` gives a canonical order-independent digest tying `certificate.json.gz` to the regenerated configuration list; (3) `pack_one_anchor.py` and `enumerate_one_anchor.py` take the universe directory as an argument (no host-specific path); (4) the notation n_V / n_D below distinguishes the neighbour counts in V and in V \ D, and the theorem is stated as "A ⊄ Q implies 4-colourable".  The certificate `certificate.json.gz` is unchanged (SHA-256 of the gzip file `58e5e2d9806c2d31e608cf07a0a7606755b3b019cb6a048b64ecf6fd5276c634`); the regenerated configuration list differs from it in nine configurations, all accounted for below (eight over-inclusive near-coincidence configurations covered by `certificate_supplement.json.gz`, one configuration identified exactly as a point of Q).

## Setting, notation and lemma

G = (V, E) is Parts's 509-vertex 5-chromatic unit-distance graph, V ⊂ K² with
K = Q(√3, √5, √11).  For D ⊆ V and a set A of points outside V, G − D + A is the strict
unit-distance graph on (V \ D) ∪ A.  For a point x ∉ V write n_V(x) = |N(x) ∩ V| for its number of
unit neighbours among all vertices and n_D(x) = |N(x) ∩ (V \ D)| ≤ n_V(x) for the surviving ones; m(x) =
|N(x) ∩ A| is the number of unit neighbours inside A.  Q is the set of points outside V with n_V ≥ 2:
1,158 points Q3 (n_V ≥ 3, K-rational), 2,705 points Q2K (n_V = 2, K-rational), 135,468 non-K
intersection points (n_V = 2; all from the committed delete-4-add-3 closure; 139,331 points).

The committed closures give: G − D + A is 4-colourable for |A| ≤ 3, |D| ≥ |A| + 1.  For |A| = 4,
|D| = 5 the committed one-anchor lemma shows: if G − D + A is 5-chromatic then in a vertex-critical
5-chromatic subgraph every added point x has n_D(x) + m(x) ≥ 4, and a point with n_D(x) ≤ 1 has
n_D(x) = 1, m(x) = 3.  (The lemma's neighbour count is n_D; the chain text of the lemma writes n(x).)
Applied to a point x with n_V(x) ≤ 1, i.e. x ∉ V ∪ Q, this gives n_V(x) = n_D(x) = 1 and m(x) = 3, and
A is of

* **type I**: A = {x, y₁, y₂, y₃} with y₁, y₂, y₃ ∈ Q at unit distance from x, or
* **type II**: A = {x, y, b, d} with b, d ∈ Q, |b − d| = √3, {x, y} the two common unit
  neighbours of b and d, and y ∉ V (y may or may not lie in Q; if y ∈ Q the same set is also a type I
  configuration of x).

**Theorem (this directory).**  For every set A of four points outside V with A ⊄ Q and every D ⊆ V
with |D| = 5, G − D + A is 4-colourable.  Consequently a 5-chromatic G − D + A with |A| = 4, |D| = 5 (if
one exists) has A ⊆ Q: every added point has at least two unit neighbours in V (the *all-anchored*
family, treated in `../hadwiger_nelson_parts509_quad_closure`).  Note that a point of Q may have only one
surviving neighbour (n_D = 1) after the deletion; such points are *not* excluded here — they are part of
the all-anchored family, and the quad closure handles them with the necessary condition
m(y) ≥ 4 − n_V(y).

## Enumeration (`enumerate_one_anchor.py`, version 2)

For every anchor v ∈ V and every q ∈ Q with binary64 |v − q| ≤ 2 + 2⁻⁴⁰ the two intersection points
of the unit circles around v and q are generated (tangent pairs give the midpoint; pairs slightly above
2 give a spurious midpoint, harmless by over-inclusion); coincident points (single-linkage components at
radius CL = 10⁻⁶, scipy) are grouped.  A member X_k (generator q_k) of a group is *identified* with an
exact point w ∈ V ∪ Q when w is a unit neighbour of v, w is a unit neighbour of q_k, and
|X_k − w| < TD = 10⁻⁶.  All unit incidences are looked up in the committed exact lists (V–V and V–Q3 edges
of `ambient_w3_edges.json`, the vertex-neighbour lists of Q3, Q2K and non-K points, the K-internal edges
Q3–Q3, Q2K–Q3, Q2K–Q2K of `q2k_extra.json`, the exact non-K unit pairs of `nonk_exact.json`; a non-K point
has no unit neighbour in K² other than its two generating vertices).

*Soundness of the identification.*  The exact point x_k* of the member lies on circle(v) and
circle(q_k), so x_k* ∈ {w, w′} with w′ the second intersection point; |x_k* − w| ≤ TD + E, where
E ≤ 10⁻⁷ bounds the forward error of a member (for a non-tangent pair the error of
h = sqrt(1 − d²/4) is at most 10⁻¹⁵/(2h) ≤ 2·10⁻¹⁰ by the gap bound below; for an exact tangency the
binary64 h is at most 3·10⁻⁸); while |w − w′| = 2 sqrt(1 − |v − q_k|²/4) ≥ 7.45·10⁻⁶ for every
non-tangent anchor–Q pair (audited: the minimum of 2 − |v − q| over all exactly non-tangent pairs is
1.3887·10⁻¹¹, `tangency_audit.json`), and w = w′ for a tangent pair.  Hence x_k* = w.  Identified
members are removed (w is a vertex or has n_V ≥ 2, never an added one-anchor point); the
identification is repeated from the residual centroid (candidate points w within CL + radius); the
residual members, if they have at least two distinct generators, form the candidate point x (their
centroid) with generator set G_x.  A true one-anchor point x* ≠ w never loses a member (its members
have x_k* = x* ≠ w), its members lie within 2E of each other and are therefore in one component, so
G_x ⊇ N_Q(x*) for the residual containing them.  Nothing else is discarded (over-inclusive).

*Radius certificate.*  The vertex-neighbour list of x and the internal edges of the configuration use
the over-inclusive tolerance TOLX = 10⁻⁵ around the residual centroid; this contains every true
incidence of every exact point represented by the residual provided the residual radius r (largest
member–centroid distance) satisfies r + E < TOLX.  The run records the maximal r over all kept residuals
and asserts r_max < TOLX − 2·10⁻⁷ (`radius certificate` line of the log): r_max = 8.293·10⁻⁶ (bound 9.8·10⁻⁶).  Extra
(false) edges and extra (spurious) configurations only make the colouring tests more conservative.

*Tangency audit (`tangency_audit.py`, output `tangency_audit.json`).*  Over all 509 × 139,331 anchor–Q
pairs with binary64 distance within 10⁻⁶ of 2 (4,567 pairs) the distance is decided exactly: 3,558
exact tangencies (binary64 deviation at most 6.7·10⁻¹⁶; 79 of them round above 2 and were omitted by
the first version's screen `d <= 2.0`), 992 non-tangent pairs below 2 and 17 above.  Every tangency
midpoint (the unique common unit neighbour of the pair) is classified exactly: 2,614 are vertices, 660
are points of Q3, 240 of Q2K, and 44 are K-rational points with exactly one vertex neighbour (one-anchor
candidate points, all with binary64 d ≤ 2, hence enumerated by both versions).  The 79 omitted
midpoints are 59 vertices, 18 points of Q3 and 2 of Q2K, so the first version missed no admissible
one-anchor point; the second version includes them and discards them by the identification rule.

Type I configurations are the 3-subsets of G_x satisfying the necessary degree condition (a point
with n_V = 2 needs a second neighbour inside A); type II configurations come from pairs of G_x at
distance √3 whose mirror point y has a vertex at unit distance (tolerance TOLX).  Q-points keep their
exact neighbour lists.

**Post-filter (`filter_configs.py`).**  A type II configuration whose mirror point y is
exactly a vertex w ∈ V (exact test: w at unit distance from b and from d in K, hence
w ∈ {x, y}, and w = y since |x − y| = 1 and y is within 10⁻⁶ of w) re-adds a vertex: for
D ∌ w the point y is a twin of w, for D ∋ w the graph G − D + A contains
G − (D \ {w}) + (A \ {y}), a delete-4-add-3 instance, 4-colourable by the committed closure.
Such configurations cannot give a 5-chromatic graph on 508 vertices and are dropped
(they are exactly the configurations that made the SAT phase slow: for u = w the instance
G − w + A contains a copy of G).

**Counts.**  First version (`summary.log`, the run that produced the certificate; 509 anchors, 3,836
CPU-seconds): 4,180,637 candidate groups with ≥ 2 generators; discarded exactly: 4,884 (x is a vertex),
9,680 (x ∈ Q3 ∪ Q2K), 126,485 (x is a non-K point of Q); kept 4,039,588 candidate points (669
near-coincidences kept).  Configurations: 133,415 type I and 22,213 type II before deduplication;
153,892 distinct point sets (133,403 type I, 20,489 type II); the post-filter dropped 11,195 type II
configurations with y ∈ V (3 near-vertex cases kept), leaving **142,697 configurations** (133,403 type I,
9,294 type II).  Second version (`summary_v2.log`; 3,877 CPU-seconds): 4,180,637 groups;
discarded 4,242 (vertex), 8,674 (Q3 ∪ Q2K), 115,957 (non-K point of Q); 12,177
groups split (residual with fewer than two generators: 11,208); kept 4,040,556 candidate points;
155,635 configurations, 153,899 distinct, 142,704 after the post-filter.  Canonical
digest (`config_digest.py`, key = type, sorted Q-references, sorted one-anchor neighbour lists, internal
edge pattern; independent of enumeration order and of which one-anchor point of a symmetric type II set
is called x): the regenerated list (digest `25276cb7fef914471afc667b1fcdec103b5fceb3ad8c67619475a0584a6f865f`, 142,704 configurations, 142,611 distinct keys) differs from the certificate (digest `81071150684f76cfdaa6837dbf9593f19102933594af24a460e62e89416fd47c`, 142,697 configurations, 142,604 distinct keys) in exactly nine configurations.  Eight configurations occur only in the regenerated list: type I sets whose one-anchor candidate x ≈ (±0.229889, −0.132727) lies within 10⁻⁵ of the unit circles of two vertices (221, 222 or 223, 224) and is therefore kept with the over-inclusive vertex list {221, 222} or {223, 224} (two non-K points and one of the Q3 points 126, 322, 148, 247); over-inclusive lists only add constraints, so covering them is conservative.  All eight are covered by the existing libraries at every vertex (|Û(A)| = 0, no solver call): `certificate_supplement.json.gz` (`pack_one_anchor.py run3/extra_configs.json run3/cover_extra.json …`), verified by `verify_one_anchor.py` (`expected_supplement.txt`, all_checks=true).  One configuration occurs only in the certificate: a type II set whose candidate x (vertex list {218, 221}) lies within 1.2·10⁻⁶ of the non-K point of Q with exact unit distances to vertices 218 and 221; the first version kept it over-inclusively, the second identifies it exactly as a point of Q (n_V(x) = 2, all-anchored family) and discards it.  Hence every configuration of the first list that is a genuine one-anchor configuration is in the second list, and every configuration of the second list is covered.

## Declared sets (`declared_sets.py`)

For each configuration A and each vertex u, (A, u) is *covered* if a stored proper
4-colouring of G − u (the committed base, swap, pair and triple witness libraries plus the
fresh rows found here) extends to A (list colouring with the internal edges); uncovered pairs
are decided by CaDiCaL (one incremental solver per u, configuration clauses under a selector
literal, conflict budget 20,000).  Û(A) = declared vertices ('unsat' or 'budget') ⊇ U(A) =
{u : G − u + A is 5-chromatic}.  A 5-chromatic G − D + A with |D| = 5 needs D ⊆ U(A) ⊆ Û(A),
so |Û(A)| ≥ 5 is necessary; every such configuration is tested directly on all 5-subsets.

**Result.**  Over the 142,697 configurations and 509 vertices: 2,457 declared pairs
(budget: 74, unsat: 2,383), 1 fresh witness colourings, 2,458 SAT calls,
3714 s with 2 workers.  Histogram: |Û(A)| = 0: 140,240, |Û(A)| = 1: 2,457.  Candidates with |Û(A)| ≥ 5: 0.
Hence no configuration of the one-anchor family gives a 5-chromatic G − D + A with |D| = 5.

The verifier (`verify_one_anchor.py certificate.json.gz --workers 2`, output in `expected_verify.txt`)
reports `all_checks=true` in 1898 s: all fresh rows proper, every uncovered pair declared,
max |Û(A)| = 1.

## Trust boundary

* Solver-free and exact: the identification of candidate points (lookups in the exact incidence lists
  of the sibling closures), the post-filter (K arithmetic of the sibling `kfield.py`, exact non-K
  unit-pair list), the replay of every fresh witness colouring against the edge list of G − u, and the
  coverage recomputation of the verifier (`verify_one_anchor.py`): every undeclared pair (A, u) is
  covered by a stored proper 4-colouring of G − u that extends to A.
* Completeness of the geometric enumeration: the coordinates of V, Q3, Q2K are converted with
  `kfield.to_float` (relative error < 10⁻¹⁵); the non-K coordinates carry the exact interval certificate
  of the triple-closure directory (`nonk_interval_certificate.json`: enclosure width < 2·10⁻³⁷, float
  deviation < 3·10⁻¹⁶); the forward error of an intersection point is E ≤ 10⁻⁷ (bound above, using the
  audited gap constant); the identification rule and the radius certificate are as stated; the
  outward-rounded screen includes all exact tangencies (audited).  Over-inclusion (spurious
  configurations, extra edges) is harmless: the colouring tests are then run on supergraphs.  The
  certificate contains the configuration list (compact references) and its canonical digest equals the
  digest of the regenerated list; the verifier does not itself regenerate the geometry.
* Declared pairs are conservative (CaDiCaL UNSAT answers and budget exhaustions are not
  certified); they only enlarge Û(A) ⊇ U(A), and the closure needs |Û(A)| ≤ 4 only.
* The reduction to the two configuration types is the committed one-anchor lemma (with n_D as its
  neighbour count), which depends on the committed closures (vertex-criticality, delete-2-add-1,
  delete-3-add-2, delete-4-add-3) and on V ⊂ K²; the pool Q is the exact census of those closures.
* Not formalised in a proof assistant; the exact checks trust CPython integers/Fractions, SymPy parsing
  of the coordinates and the sibling field implementation.

## Files and reproduction

* `paths.py`, `libraries.py` — sibling-directory layout; witness libraries (base, swap, pair rows from
  `pair_closure.py` / `pair_certificate.json`, triple rows decoded from `triple_certificate.json`).
* `build_universe.py OUTDIR` — builds the float universe V, Q (needs `q2k_extra.json`, regenerated in the
  triple-closure directory by `two_neighbour_points.py`; about 5 minutes).  All tools below take the same
  directory through `--universe OUTDIR` (or the environment variable `ONE_ANCHOR_UNIVERSE`; default `./universe`).
* `enumerate_one_anchor.py RUNDIR --workers 2 --universe OUTDIR` — the enumeration with the identification
  rule and the radius certificate (needs `nonk_exact.json` of the triple closure; 509 anchors, about
  3,995 s wall, one worker); `filter_configs.py RUNDIR/configs.json RUNDIR/configs_f.json` — exact post-filter.
* `tangency_audit.py --universe OUTDIR --out tangency_audit.json` — exact audit of the cutoff (15 s).
* `config_digest.py RUNDIR/configs_f.json certificate.json.gz --universe OUTDIR` — canonical digests and
  multiset comparison (expected: IDENTICAL, digest above).
* `declared_sets.py` — coverage against the libraries and incremental CaDiCaL for uncovered pairs
  (about 60 minutes with 2 workers); `pack_one_anchor.py CONFIGS_F COVER OUT.json.gz --universe OUTDIR` —
  certificate packer (checks the universe labels against `q2k_extra.json`).
* `verify_one_anchor.py certificate.json.gz --workers 2` — solver-free verifier (expands the compact
  references from the committed completion list and triple certificate); `summarize_results.py RUNDIR`.
* `kfield.py` — copy of the sibling exact arithmetic (Q(√3, √5, √11)), for convenience.
* `certificate.json.gz`, `expected_verify.txt`, `summary.log` (first version), `summary_v2.log`,
  `tangency_audit.json`.
