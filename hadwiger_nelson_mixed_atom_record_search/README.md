# Mixed-atom search for a sub-509 plane unit-distance graph

No record improvement was found. This package records a direct construction
search with a 490-point budget, followed by exact geometric additions to two
selected seeds. Every retained sum case was four-coloured. The two augmented
supports also have checked four-colourings, so every sub-509 subset of either
support is excluded.

This is a restricted construction checkpoint. It gives no global lower bound
on the order of a five-chromatic unit-distance graph and does not exclude
arbitrary first rotations, arbitrary points in the same fields, or arbitrary
circle-intersection additions.

## Concrete construction and record comparison

Let E=Q(i sqrt(3),i sqrt(11)), let M be the seven-point Moser spindle, and let
G be the ten-point Golomb graph. Both atoms have exact coordinates in
[atoms.py](atoms.py) and its pinned arithmetic dependency. The new supports
are sums of physical plane points, P+vC, rather than abstract graph products.
The principal mixed case G+uM+vM has at most 490 distinct points. A
five-chromatic member would therefore improve the 509 record by at least 19
vertices. Source coincidences can only reduce this count.

The initial source pool takes P=A+uB for (A,B) equal to (G,M), (M,M), (G,G),
or (G,conj(G)). The unit u lies in E and arises from a unit-contact or collision
equation between atom differences. C is M, G, or conj(G), with |P||C|<=508.
The three-Moser case is omitted from this pool. Also included is the distinct
four-factor construction (M+M+M)+vM: its coefficient source has 70 points.
Sixth-root rotations, translations, and the stated reflection equivalences
remove duplicate sources. The resulting pool has 106 cases, of order 260--490.

For each source, the search enumerates exceptional unit phases v outside E.
Every extra unit edge satisfies |a+vb|=1, with nonzero source differences a,b.
Writing c=conj(a)b and S=|a|²+|b|²-1 gives

    v² - T v + J = 0,  T=-S/c,  J=conj(c)/c.

Irreducible quadratic cases have two physical unit roots with identical
complete edge relations. The map P x C -> P+vC is injective when v is outside
E. The accepted base-field and local trace results discard v in E and the
relative-trace strata of valuation at least -1. Generic phases have only the
Cartesian edges. Both source atoms are locally integral at the fixed embedding
sqrt(33)=1 mod 8; the filter is not applied to arbitrary nonintegral sources.
The remaining 99,080 quadratic cases all admitted four-colourings.

A stronger finite experiment uses u=(7+i sqrt(15))/8 in E(sqrt(5)), or
u=(5+i sqrt(39))/8 in E(sqrt(13)). Here P is G+uM or M+uM, with C=M or G,
respectively. Every unit-contact or collision phase v **in that fixed field**
is enumerated, subject to v and v/u being outside E. These tests cover 6,738
phase choices, all four-colourable. They do not claim that the skipped
base-related phases or phases outside those two fields have been closed.

| Seed field | Support | Retained phase choices | Result |
|---|---|---:|---|
| E(sqrt(5)) | G+uM+vM | 1,402 | all four-colourable |
| E(sqrt(5)) | M+uM+vG | 1,788 | all four-colourable |
| E(sqrt(13)) | G+uM+vM | 1,520 | all four-colourable |
| E(sqrt(13)) | M+uM+vG | 2,028 | all four-colourable |

## Exact additions beyond the sum family

For two selected 490-point seeds, generate intersections of every pair of
unit circles centred at seed vertices. Retain new points in the seed's exact
coordinate field that have **at least four unit neighbours in the seed**.
Include all unit edges between the resulting points. A 490-point seed leaves
room for 18 additions in a record candidate; testing the full augmented
support excludes every such selection when the full support is four-colourable.

| Seed | Seed edges | New points | Augmented order | Unit edges | Result |
|---|---:|---:|---:|---:|---|
| G+u conj(G)+vM, source 0/contact 44 | 2,685 | 357 | 847 | 5,024 | checked four-colouring |
| G+uM+vM, field 5/contact 0 | 2,435 | 28 | 518 | 2,567 | checked four-colouring |

The first seed uses u=(-5+i sqrt(11))/6 before canonical rotation/reflection;
its two-Golomb coefficient set has 70 points and 264 edges. Its final
radicand is (-11+3 sqrt(33))/18; the second seed has radicand 5.
[fixtures.json](fixtures.json) specifies the exact phases, compact construction
recipes, two seed words, and two augmented-support colour words. Its hashes
pin the regenerated physical point and complete edge streams. No point-cloud
or search dump is needed for verification.

These two seeds are retired. Enlarging the number of already four-coloured
phase cases or selecting subsets of these same augmented supports cannot
produce a record. A further candidate must change the source, the phase
architecture, or the allowed added-point set. In particular, this pass did
not test additions with fewer than four seed neighbours, points outside the
seed field, or a second generation of circle intersections. Such extensions
would require a new vertex budget and a reason to expect stronger colouring
constraints before expansion.

## Evidence and limits

The broad phase census is a reproducible exact-arithmetic computational
observation. The retained graphs have decoded positive SAT witnesses checked
against every generated edge. Their completeness uses the displayed contact
polynomial reduction; the package does not include a separate all-pairs
metric replay for all 99,080 quadratics. It does include a **solver-free**
regeneration of both selected seeds and their augmentations, with all pairs
checked by two separately derived exact metric formulas. The shell certificates
establish the two stated physical-host exclusions without trusting SAT.

No UNKNOWN or UNSAT result occurred. If one had occurred, the search would
have preserved it as such. Any proposed record would require a fresh exact
realization/edge audit, a checked five-colouring, and an independently checked
non-four-colourability proof. None is claimed here.

[REPRODUCE.md](REPRODUCE.md) gives commands and versions.
[EXPECTED.json](EXPECTED.json) is the compact structural census.
[VALIDATION.md](VALIDATION.md) records completed checks and trust boundaries.

## Context and provenance

The current published vertex record was checked against
[Parts, *Graph minimization, focusing on the example of 5-chromatic unit-distance graphs in the plane*](https://arxiv.org/abs/2010.12665)
and the 2026 primary-source introduction at
[arXiv:2608.04542v4](https://arxiv.org/html/2608.04542v4).
The comparison is a realized five-chromatic plane unit-distance graph on 509
vertices. Auxiliary chromatic graphs are not record candidates.

Arithmetic is reused from
[the independent-Moser-sum package](../hadwiger_nelson_independent_moser_sum_collisions/),
source commit `55f27a5af19948be8ddd9e0d0015b178bdc20936`. The local filters use
[the base-field proof](../hadwiger_nelson_integral_trace_gluing/) and
[the first-negative-trace proof](../hadwiger_nelson_first_negative_trace/).
The prior collision theorem concerns three Moser factors with a collision;
it does not close these mixed-atom sums or the mixed two-Golomb source used for the dense shell.
The closed C13 triple-sum shell and the other lane's common-neighbour phase
sumsets were checked for overlap; neither is the host tested in this package.

Discovery Net's committed local index remained stale at height 4363.
Repository and durable teammate reports were refreshed through `ae5fc18`
before packaging. This author's checks are not an independent peer review.
