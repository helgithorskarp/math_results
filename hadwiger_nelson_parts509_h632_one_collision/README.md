# No one-identification image of Parts-509 in H632

Let **S** be the certified five-chromatic graph with 509 vertices and 2,259
unit edges from the Parts construction, and let **H632** be the exact
632-point, 3,112-edge host defined below. There is **no graph homomorphism**

    f : S -> H632

with **508 or 509 distinct images**. Thus this host contains neither an
injective copy of S nor an image obtained by identifying exactly one pair of
source vertices. No source vertex is pinned, no host symmetry is quotiented,
and nonedges need not be preserved. This is a complete exclusion for that
specified family, not a sample of placements.

This result does **not** exclude maps with 507 or fewer images, arbitrary
508-vertex subgraphs of H632, or maps into other unit-distance hosts. It does
not improve the 509-vertex record. The independent H560 deletion closure and
the capped H632 colouring-cover pilot are not resumed.

## Why this is a target-facing family

A graph homomorphism sends each source edge to a host edge. A proper colouring
of its image would pull back to a proper colouring of S. Since S is not
four-colourable, a 508-point image would not be four-colourable either. Its
exact host coordinates would give a unit-distance graph on 508 points. An
inclusion-minimal non-four-colourable induced subgraph would be exactly
five-chromatic and would meet the record target.

The present certificate rules out that image size and also the injective
case. The source's known chromatic number motivates the construction; the
nonexistence proof itself uses only the two finite graph definitions. No
source chromatic proof is recomputed here.

## Finite reduction without pins

For any function on n vertices with at least n-1 distinct images, every subset
A of its domain satisfies

    |f(A)| >= |A|-1.

Indeed, the whole function has at most one lost image: either it is injective,
or exactly one fibre contains two vertices and every other fibre is a
singleton. Apply this to the neighbours of a source vertex v. If f(v)=h and f
preserves edges, then f(N_S(v)) is contained in N_H(h), so

    degree_H(h) >= degree_S(v)-1.

This initializes a domain D(v) with every host vertex satisfying that
inequality. There are 225,100 initial source/host pairs. No geometric
normalization, injectivity assumption stronger than the stated image count,
or arbitrary pinned set is introduced. For example, the source's degree-36
vertex can initially map only to the host's degree-40 vertex; that is a
consequence of the degree inequality, not an imposed pin.

Maintain the invariant that every admissible map has f(v) in D(v). Each
certificate row removes one currently allowed h from D(v) by one of two rules:

- **A, unsupported edge.** Some u in N_S(v) has
  D(u) intersect N_H(h) empty. The edge vu cannot be mapped.
- **H, neighbour-union deficit.** The row supplies a set A contained in N_S(v).
  Form B as the union, for u in A, of D(u) intersect N_H(h). If
  |B| <= |A|-2, the required inequality |f(A)| >= |A|-1 is impossible.

Both rules preserve the invariant. The verifier checks these literal set
conditions and then removes h. An empty source domain proves nonexistence
for every admissible map at once. There is no SAT verdict, matching-engine
verdict, or assumed completeness of a colouring library in this implication.

## Certificate generation and independent verification

The producer searches for the second kind of witness using maximum bipartite
matching between source neighbours and allowed host neighbours. If the
matching has deficiency at least two, alternating reachability supplies a
Hall witness A. Discovery uses synchronous rounds. Every round removes at
least one value or reaches a fixed point, so the process is finite.

For this input, seven rounds remove 185,254 of the initial 225,100 values and
empty 20 source domains. The producer then follows witness dependencies
backwards and retains one complete proof for source vertex **156**. This
certificate has **24,072 removals**: 19,055 unsupported-edge rows and 5,017
neighbour-union rows. It takes **548,087 bytes** as deterministic compact JSON.
Its SHA-256 is

```
f0851eb8becbde17b53e246a629df33de34a7d5cfe5cc523f5c86672cc08f227
```

The generated certificate remains outside the repository and is reproducible
from the published source in about 28 seconds on the recorded machine.
There is no external download or solver dependency. `certificate_manifest.json`
records its format, size, hash and reproduction command.

The independent checker imports no producer or matching code. It starts with
the degree domains, checks each supplied neighbour set and cardinality
inequality directly, and ends with D(156) empty. The backward slice is checked
sequentially: omitted producer steps cannot be presumed. This makes the
certificate self-sufficient even if the matching or slicing code is wrong.
It directly evaluates 127,006 neighbour-union incidences.

## Exact graph inputs

All inputs are existing files in the authorized repository and are pinned in
`inputs.json`. Source labels are the original Parts labels 0 through 508.
The source edge list is
`../hadwiger_nelson_parts509_edge_criticality/reduced_edges.json`; its canonical
lines `u v` have SHA-256

```
93f5ff096936613b61fcbdba3bca27addd5d59868c10561385c4ada7606d2305
```

Source coordinates use labels 0 through 508 in the existing D7 exact-coordinate
certificate. All 2,259 source edges are rechecked as unit pairs. The graph
intentionally omits 183 other unit pairs from the Parts point set. Preserving
only the reduced edge set makes the exclusion stronger than the corresponding
statement for the full 2,442-edge source graph.

The host uses the 510 archived Heule points, in increasing original union
label order, followed by the 122 archived fresh centres in increasing
`centre_index` order. Both coordinate sets are rational vectors in

    (1, sqrt(3), sqrt(5), sqrt(15), sqrt(11), sqrt(33), sqrt(55), sqrt(165)).

Scaling by 96 makes every coefficient integral. The producer uses ordered
XOR convolution in that basis. The verifier instead uses sparse radicands
and the identity sqrt(r)sqrt(s)=gcd(r,s)sqrt(rs/gcd(r,s)^2), accumulating square
and cross terms separately. It verifies distinct points and tests all 199,396
host pairs, recovering 3,112 unit edges. The host edge stream `u,v` has SHA-256

```
8dd36c195b3e252ec2be150ea6a029375707293fec70b63da9fc157eed4140f0
```

The proof trusts exact Python integer/Fraction arithmetic, the input
interpretation, independence of the eight radical basis elements, finite set
operations and the written invariant. It uses no floating-point distance
comparison. This is independent implementation checking within this research
pass, not external-author review or proof-assistant formalization.

## Reproduce

On Linux, Python 3.11 or later and its standard library suffice. From the repository root,
choose a new output directory outside the repository:

```sh
python3 -B hadwiger_nelson_parts509_h632_one_collision/generate.py \
  --out /tmp/parts-h632-one-collision
python3 -B hadwiger_nelson_parts509_h632_one_collision/verify.py \
  --certificate /tmp/parts-h632-one-collision/certificate.json
python3 -B hadwiger_nelson_parts509_h632_one_collision/controls.py \
  --certificate /tmp/parts-h632-one-collision/certificate.json
```

The verifier prints `expected.json`; controls print `controls_expected.json`.
Normal and optimized Python production runs generated byte-identical
certificates, and their verifier reports also agree byte for byte. The
recorded production interpreter is CPython 3.11.2; production used about
151,976 KiB peak RSS. Runtime and the full round transcript are compactly recorded
in `validation.json`; raw generated certificates and operational logs stay
outside the public package.

The matching controls compare the producer against subset dynamic programming
on **74,963** complete small bipartite cases. The graph controls check **741,407**
functions with at most one identification across all **5,625** pairs of simple
graphs on one through four vertices. All **119,892** proper homomorphisms
survive the sound reductions. Twelve malformed certificate variants are
rejected, including false Hall sets, missing or repeated removals, incorrect
headers and invalid source/host labels.

## Prior work and scope

The source is the Parts 509-point construction, with the reduced edge set from
Mohammed Amer's release. The relevant primary sources are
[Parts's minimization paper](https://arxiv.org/abs/2010.12665) and
[Amer's graph and proof data](https://github.com/md-amer/hadwiger-nelson-e5).
The previously checked lower bound and edge-criticality are preserved in the
[sibling source package](../hadwiger_nelson_parts509_edge_criticality/README.md).
The exact H632 labels come from the
[host package](../hadwiger_nelson_heule632_pair_pilot/README.md).

The earlier
[pinned H516 map theorem](../hadwiger_nelson_heule516_host_homomorphisms/README.md)
uses another source and fixes 375 vertices. This theorem imposes no pins and
tests every map with at most one identification of this 509-vertex source.
It is not a pin-relaxation step for the old source. The
[accepted H560 deletion closure](../hadwiger_nelson_heule560_target508_review1/README.md)
and HN3's separate
[953-vertex spindle closure](../hadwiger_nelson_overlapping_forcing_seed/README.md)
were inspected as coordination context, not used as premises.

No novelty is claimed for graph homomorphisms, neighbourhood matching, Hall
witnesses, or domain propagation. The contribution is the exact unpinned
source/host exclusion with a directly checked certificate. Its complete
one-identification family is now closed. No smaller-image threshold, different
host, or additional search phase was started.
