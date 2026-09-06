# Induced pentagons are unavoidable in Ramsey graphs of order 42

**Every graph on at least 42 vertices contains a K5, an independent 5-set,
or an induced C5.** Therefore a hypothetical Ramsey(5,5;43) graph must contain
an induced pentagon. This completely excludes the family of induced-C5-free
43-vertex graphs, with no symmetry, degree profile, fixed core, connectivity
or catalog restriction.

This is a finite combinatorial proof with compact executable checks. It
does not construct a Ramsey graph, improve the unrestricted bound for R(5,5),
close a global degree profile, or force one of the earlier excluded pentagon
product cores. No historical priority or optimality of the order-42 threshold
is claimed.

## Proof mechanism

The [complete proof](PROOF.md) establishes the sharp small-order fact that
every triangle-free, C5-free graph on ten vertices has an independent 5-set;
the nine-cycle witnesses sharpness. An assumed counterexample has degrees
two or three. The cubic case forces twelve incidences where only ten are
available. A degree-two vertex has a seven-cycle as its nonneighbors, and a
short contact argument produces an independent five-set.

The classical mixed-triangle identity then forces a same-color edge with
ten common neighbors in every coloring of a complete graph of order at
least 42. Applying the small lemma to ten common neighbors gives either a
monochromatic five-set or an induced pentagon. This supplies the full global
bridge; the seven-cycle check alone is not the claimed result.

The proof imports no graph enumeration, small Ramsey value, SAT verdict,
or asymptotic constant. It is an ordinary mathematical proof, not a
proof-assistant formalization or an external peer review.

## Reproduction

Python 3.11 or newer, standard library only; tested with CPython 3.11.2.
From this directory:

```sh
python3 -B reproduce.py
python3 -B -O reproduce.py
sha256sum -c SHA256SUMS
```

Expected status: `REPRODUCED_INDUCED_PENTAGON_FORCING`.
The certificate regenerates byte for byte. No private input, solver,
downloaded data, large certificate or omitted proof trace is needed.

The main evidence is:

| Check | Exact coverage |
| --- | --- |
| Physical contact classification | All 128 seven-bit contacts |
| Rooted contact pairs | All 16,384 pairs: 15,543 with triangles, 700 with induced pentagons, 141 with certified independent five-sets |
| Compact certificate | All 15 admissible contacts and 141 compatible ordered pairs, matched entry by entry |
| Degree-two component controls | All 20 and 32 eligible component types at orders seven and eight |
| Triangle identities | All 33,867 labeled graphs of orders one through six |
| Global extractor | 96 graphs of orders 42–44, including complements and scrambled labels; all three proof outcomes exercised |
| Negative controls | Four damaged kernel certificates, five malformed graphs, five invalid five-set certificates rejected |

The ten-vertex cubic argument and the coverage of all ten-vertex graphs rely
on the explicit universal proof in PROOF.md. The computation does not claim
to enumerate all `2^45` graphs on ten vertices. The independent contact
checker imports no producer, cyclic-distance classifier, or solver; it
expands physical edges and checks forbidden sets directly. The global
triangle identity is proved by double counting and checked independently
on small graphs.

## Executable obstruction certificates

Input graphs have the form `{"n": 43, "edges": [[0,1], ...]}`. Each red edge
is listed once with smaller endpoint first; all other pairs are blue.
The extractor accepts any order at least 42:

```sh
python3 -B extract.py fixture.json > /tmp/r55-pentagon-certificate.json
python3 -B verify.py fixture.json /tmp/r55-pentagon-certificate.json
```

The included fixture produces an induced pentagon. It has two joined
vertices above a ten-vertex Petersen graph, with all remaining vertices
isolated. It is explicitly **not** a Ramsey graph. It exercises the pentagon
outcome of the extractor, not a construction search or a new low-defect graph.

The extractor finds a qualifying physical edge, examines ten common
neighbors, and returns five original vertex labels. Its certificate includes
the anchor as provenance. The separate verifier trusts only the final five
labels and the input graph: it checks all ten pairs and the claimed clique
color or induced-cycle degree pattern. It imports no extractor, kernel,
enumeration, or mathematical theorem. A guaranteed extractor output relies
on the universal proof; verification of an actual output does not.

## Prior work and campaign scope

The mixed-triangle identity is classical:
A. W. Goodman, [On Sets of Acquaintances and Strangers at any Party](https://doi.org/10.1080/00029890.1959.11989408),
American Mathematical Monthly 66 (1959), 778–783. Its needed form is derived
in PROOF.md, so no inaccessible theorem or optimal multiplicity formula is
an imported premise.

Chudnovsky, Scott, Seymour and Spirkl,
[Erdős–Hajnal for graphs with no 5-hole](https://arxiv.org/abs/2102.04994),
give the broader polynomial Ramsey property of the induced-C5-free class.
The present finite argument uses no exponent or constant from that work.
Targeted searches did not identify this exact finite statement, but do not
establish novelty of the statement or of the sharp ten-vertex sublemma.

The preceding complete order-22 (4,5), induced-C5-free SAT attempt remains
UNKNOWN at its original limit. This proof closes the intended 43-vertex
family by a different structural bridge. It does not prove that sufficient
order-22 premise, change its formula, or turn its partial trace into a
certificate. The old checkpoint remains separate and unchanged.

The earlier [deleted pentagon product exclusion](../ramsey_r55_deleted_pentagon_product)
concerns a prescribed 24-vertex induced product core. The present result
forces one induced pentagon, and supplies no implication that such a product
core exists. The teammate's [module resilience theorem](../ramsey_r55_module_resilience)
also concerns a separate global construction family and is not a proof input.
The current result changes neither the retained M216 keys nor the inherited
global degree-profile and symmetry counts.

All source and compact evidence are included here. Remaining trust is the
unformalized proof, the author's implementations, Python integer semantics,
and ordinary hardware. Matching internal checks are not external review.
