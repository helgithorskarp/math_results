# A 29-point frozen-centre source and its reflected-chord transfer boundary

This package supplies an exact small physical forcing source. The strict
unit-distance graph **F29** has 29 distinct points and 75 edges. If its centre
is deleted, the remaining 28-point, 61-edge graph still forces its 14 marked
centre-neighbours to use **at least three colours in every proper
four-colouring**. The induced graph on those terminals is bipartite, so this
removes otherwise valid terminal patterns. Restoring the centre gives a
four-chromatic graph in which the centre has exactly one available colour
when all other colours are fixed.

The source is a reduction of the Polymath16 seven-coset construction. Its
forcing property has a four-case palette proof, replayed without a SAT solver.
This is **not a new record for frozen-centre sources**: Heule reported
24-point examples in 2018. It is also not a five-chromatic graph or an
improvement of the 509-point Hadwiger–Nelson record.

The first budgeted transfer test is now complete and negative. Reflect F29
through every line joining two distinct centre-neighbours, excluding lines
through the centre. Merge all coincident points and include every unit edge.
There are 86 labelled frames, with 41–56 distinct points and 124–176 edges.
For every frame, **every proper four-colour pattern of the bare four-point
interface**—the two centres and the two chord endpoints—extends to the whole
physical graph. The certificate supplies all 298 pattern/frame witnesses.
Thus these placements produce neither a forced equality of the two centres
nor any extra relation on that joint interface. All 86 graphs are exactly
four-chromatic.

This closes the declared reflected-chord transfer mechanism. It does not
classify other interfaces, arbitrary placements or all compositions of
frozen-centre sources. No larger host, additional phase window or next
composition was started.

## Source, labels and exact geometry

An integer row `[a,b,c,d]` in [points.tsv](points.tsv) represents

```text
z = (a + b sqrt(33) + i(c sqrt(3) + d sqrt(11)))/12.
```

The file's first column is the source label, starting with centre 0. It is a
readable derived fixture; the verifier reconstructs it from the seven cosets.
[PROOF.md](PROOF.md) gives the complete construction and selected labels.
The marked terminal list is

```text
4,5,6,7,9,10,12,14,15,17,18,22,25,28.
```

Their induced graph is a six-cycle and paths on five and three vertices,
with 12 unit edges in total. A proper two-colouring of this terminal graph
does not extend to F29 with the centre deleted. A proper four-colouring of
F29 is supplied separately, so the negative statement is an actual boundary
restriction and does not rely on an inconsistent source.

All 28 noncentral vertices are necessary **within this selected support for
this particular palette restriction**: for each deletion, a checked proper
four-colouring uses just two colours on the surviving terminals. This is not
a global minimum-size theorem or a statement of ordinary vertex-criticality.

For chord endpoints A,B on the unit circle, the reflection is particularly
simple:

```text
r(z) = A+B - AB conjugate(z).
```

Its moved centre is A+B. Five of the 91 terminal pairs are antipodal and
are excluded by the stated nondegeneracy condition. No numerical incidence,
abstract quotient realization or missing collision assumption enters the
result. All 123,033 unordered point pairs in the reconstructed source pool,
selected source and 86 compositions are checked exactly.

## Reproduction

Python 3.11 or later and its standard library suffice for proof replay:

```sh
python3 -B hadwiger_nelson_frozen_centre_transfer/verify.py --check-expected
python3 -O -B hadwiger_nelson_frozen_centre_transfer/verify.py --check-expected
python3 -B hadwiger_nelson_frozen_centre_transfer/controls.py
```

The expected status is
`VERIFIED_FROZEN_CENTRE_SOURCE_AND_JOINT_TRANSFER_BOUNDARY`.
[expected.json](expected.json) gives the complete compact output, including
the four palette cases and physical census. The certificate has SHA-256

```text
f6bcc2110c1ac26bd5cfa9223229b2cd8c4cebf13a19ccf46b722c5a06417a3e.
```

The solver-free verifier checks 47,643 positive edge inequalities. In addition
to the four-case proof, a complete colour-domain search independently exhausts
the forbidden source prescription in 39 nodes and 20 conflicts. The controls
compare that search with brute force on all 1,024 four-vertex graph/domain
cases, compare the two arithmetic implementations on all 121,724 composition
pairs, and reject eight corrupt certificates.

Optional positive-witness regeneration uses `python-sat==1.8.dev17` and its
CaDiCaL 1.5.3 backend:

```sh
python3 -m venv /tmp/hn-frozen-env
/tmp/hn-frozen-env/bin/pip install -r hadwiger_nelson_frozen_centre_transfer/requirements.txt
/tmp/hn-frozen-env/bin/python -B hadwiger_nelson_frozen_centre_transfer/produce.py \
  --out /tmp/hn-frozen-certificate.json
cmp /tmp/hn-frozen-certificate.json hadwiger_nelson_frozen_centre_transfer/certificate.json
```

Every query is capped at 200,000 conflicts and must return a directly checked
positive word. The producer uses at-least-one colour variables with edge
exclusions. Several colour variables at a vertex may be true; decoding
honours each prescribed interface colour. The proof replay relies on the
words, not SAT status or the producer's completeness.

## Construction value, attribution and limits

The source provides a 14-terminal lower bound on the number of colours at a
cost of 28 physical points; it is an available local constraint for a future
composition. The tested transfer aimed to turn this into a forced-equal
marked pair. A four-colourable forced-equal source of order at most 254,
with marked distance at least 1/2, would allow a two-copy unit-bridge spindle
of order at most 507. This pass finds no such pair among the two centres.
The reflected-chord route is retired rather than enlarged.

The seven-coset construction and the idea of excluding a bichromatic centre
are prior Polymath16 work:

- [Polymath Wiki: Excluding bichromatic vertices](https://michaelnielsen.org/polymath/index.php?title=Excluding_bichromatic_vertices).
- [The fourth Polymath16 thread](https://dustingmixon.wordpress.com/2018/05/05/polymath16-fourth-thread-applying-the-probabilistic-method/), including Heule's May 9, 2018 report of 24-point examples and the discussion of Hubai's 43-point source.
- Frankl, Hubai and Pálvölgyi, [Almost-Monochromatic Sets and the Chromatic Number of the Plane](https://drops.dagstuhl.de/entities/document/10.4230/LIPIcs.SoCG.2020.47), especially its 34-point example and discussion of the extra composition requirement.

The present source, explicit four-case reduction and finite transfer gate are
author-run research evidence; no priority claim or independent-author review
is made. The trust boundary is the written finite reductions, exact rational
arithmetic and radical independence, the source reconstruction, positive-word
checks and ordinary Python/runtime correctness. The package is self-contained
and imports no prior graph theorem. The four-colourable field containing all
these points, with an explicit checker in the
[field-obstruction package](../hadwiger_nelson_nonmono_field_obstruction/README.md),
explains why a *new relation*, rather than a direct non-four
result in the same field, was the intended milestone.

Live primary-source calibration on September 14, 2026 still found the
[Parts 509-point construction](https://arxiv.org/abs/2010.12665), also used as
the comparison in [Haugland's August 2026 paper](https://arxiv.org/html/2608.04542v4).
This bounded source check is not proof that no later unpublished construction
exists.
