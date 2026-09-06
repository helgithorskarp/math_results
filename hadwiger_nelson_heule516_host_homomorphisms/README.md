# A pinned 516-vertex obstruction has only the identity map into H632

**Theorem.** Let S be the certified 516-vertex obstruction specified below,
and let H be the exact 632-point unit-distance host. Every graph homomorphism
`f:S -> H` fixing the 375 source vertices in the large field block is the
identity inclusion. In particular, **no such map has at most 508 distinct
image vertices**.

This completely decides one finite construction family. A map was allowed
to identify nonadjacent source vertices and to use any of the 632 host points,
including points outside the preceding H560 support. Only preservation of
source edges and the 375 pointwise pins were required. A successful small
image would have inherited a chromatic lower bound of five from S.

The result does not exclude other five-chromatic subgraphs of H632, maps
with fewer pins, maps into other hosts, or arbitrary placements in the plane.
It is not a record improvement. The earlier H560 504--508 frontier remains
open.

## Exact source, target and family

Use the established H632 host labels and coordinate inputs from the
[exact host package](../hadwiger_nelson_heule632_pair_pilot/README.md).
The coordinates are rational coefficient vectors in

```text
(1,sqrt(3),sqrt(5),sqrt(15),sqrt(11),sqrt(33),sqrt(55),sqrt(165)),
```

with integer coefficients after multiplication by 96. The host has 632
distinct points and 3,112 unit edges. All 199,396 pairs are tested exactly.
Both generators first reconstruct the entire host, then restrict its edge
set to the source vertices.

In the [global-decision certificate](../hadwiger_nelson_heule560_global_decision/certificate.json),
take zero-based `negative_cores[52]`, the row also named by
`minimality_evidence_core_index`. Its mask uses `optional_order`. The source
vertex set is M492 from the
[mandatory boundary](../hadwiger_nelson_heule632_minimize/boundary.json)
union the 24 optional vertices in that mask. Its full induced unit graph S
has **516 vertices and 2,538 edges**. Its five-chromaticity and
vertex-criticality have an
[independent accepted review](../hadwiger_nelson_heule560_global_decision_review1/README.md).
Neither theorem is recomputed here. They motivate the construction test;
the new identity theorem itself needs only the finite graph definition.

The fixed set L consists of those source vertices whose two coordinates
have zero coefficients on every displayed radical divisible by five. There
are **375** such vertices. The other **141** source vertices are initially
allowed to map anywhere in H. Thus this is a fixed, explicitly specified
family of all functions `f:V(S)->V(H)` satisfying

```text
f(v)=v                       for v in L,
{f(v),f(w)} in E(H)           for every {v,w} in E(S).
```

There is no injectivity constraint, field-block constraint on the unpinned
images, or requirement to preserve nonedges. The target is a simple graph,
so endpoints of a source edge cannot identify. No host automorphism or
geometric normalization is used to justify the pins: they are a restriction
defining this particular construction family.

## The complete domain certificate

For a source vertex v, start with `D_0(v)={v}` if it is pinned and
`D_0(v)=V(H)` otherwise. Repeatedly apply the synchronous rule

```text
D_(r+1)(v) = { x in D_r(v) :
                for every w adjacent to v in S,
                some y in D_r(w) is adjacent to x in H }.
```

**Soundness.** For any permitted homomorphism f, induction on r gives
`f(v) in D_r(v)` for every v. The initial claim is the pin condition. If it
holds in round r, each source neighbour w supplies the required witness
`y=f(w)` for `x=f(v)` in the next round. Thus deleting a value by this rule
never deletes an actual homomorphism.

The domains decrease inside a finite universe, so the process terminates.
An independent synchronous computation gives:

| Strict round | Removed values | Values remaining | Singleton domains |
| --- | ---: | ---: | ---: |
| 0, initial | 0 | 89,487 | 375 |
| 1 | 18,956 | 70,531 | 375 |
| 2 | 53,342 | 17,189 | 375 |
| 3 | 14,634 | 2,555 | 381 |
| 4 | 1,328 | 1,227 | 425 |
| 5 | 700 | 527 | 509 |
| 6 | 11 | 516 | 516 |

At the fixed point, every domain is **exactly `{v}`**, not merely some
unspecified singleton. The verifier compares all 141 unpinned domains with
[certificate.json](certificate.json), checks all pinned domains from their
definition, and checks all 2,538 edges of the identity assignment. Therefore
the identity is both necessary and an actual homomorphism, proving uniqueness
and the image size 516. No SAT query or negative proof trace is needed.

Arc consistency is not generally a complete homomorphism decision procedure.
The conclusion here follows because this instance reaches singletons and
the resulting assignment is valid. In particular, the verifier's small
controls include six systems whose stable domains are nonempty despite there
being no homomorphism; it does not interpret nonempty domains as existence.

## Construction significance and limits

If a proper four-colouring existed on the induced host graph on `f(V(S))`,
pulling it back along f would give a proper four-colouring of S. Hence any
homomorphic image of this certified source is non-four-colourable. An image
on at most 508 host points would therefore provide a candidate lower-bound
certificate, with a separate five-colouring needed for an exact chromatic
number of five. The present theorem rules out every such image under the
stated pins.

This method tests finite graph homomorphisms, with possible vertex
identification, into a larger fixed host. It does not classify all induced
host subgraphs: a five-chromatic graph need not receive a map from S with
these pins. It also gives no rigidity theorem for an unrestricted geometric
target. No claim that 375 is a minimal pin set is made.

## Reproduction and independent checking

Python 3.11 or later and the standard library suffice. From the repository
root, with fresh output directories:

```sh
sha256sum -c hadwiger_nelson_heule516_host_homomorphisms/SHA256SUMS
python3 -B hadwiger_nelson_heule516_host_homomorphisms/build.py \
  --out /tmp/hn516-map-build
diff -u hadwiger_nelson_heule516_host_homomorphisms/certificate.json \
  /tmp/hn516-map-build/certificate.json
python3 -B hadwiger_nelson_heule516_host_homomorphisms/verify.py \
  --out /tmp/hn516-map-check
diff -u hadwiger_nelson_heule516_host_homomorphisms/expected.json \
  /tmp/hn516-map-check/result.json
```

The producer uses the host's dense XOR field arithmetic and an asynchronous
queue of directed arcs with integer bitmask domains and cached neighbour
unions. The verifier imports no new producer code. It uses sparse-radical
norms and ordinary Python sets, with all vertices revised simultaneously
from the preceding round. Entrywise domains, source labels, pin labels and
forced target labels are compared; aggregate agreement alone is insufficient.

The producer performs 7,803 arc revisions, of which 947 strictly reduce a
domain, removing 88,971 values in about 0.012 seconds after 1.29 seconds of
input geometry. Its queue schedule differs from the verifier's six strict
rounds. [run_summary.json](run_summary.json) records measured timings; these
are provenance and do not affect termination or the proof.

The verifier exhaustively considers all eight labelled simple graphs on three
vertices as source, all eight as target, and all eight subsets of identity
pins: **512 cases**. It enumerates every actual map in each case and confirms
that all **1,320 valid map instances** survive the domain revisions. It also
checks the stable-domain property and that an empty domain implies no valid
map. Five malformed certificates are rejected. Normal and optimized-Python
outputs agree. [validation.json](validation.json) records the checks and
interpreter version.

[plan.json](plan.json) was frozen before the domain calculation. It allowed
one conditional native decision only if the domain calculation did not force
at least 509 distinct images. That condition was not reached; no solver was
called. The implementation and published proof cover the completed domain
branch, with no hidden native fallback or omitted negative trace. The compact
certificate and committed inputs are sufficient for reproduction. Raw run
logs and local checkpoints remain outside the repository.

The trust boundary is pinned input data, the independence of the radical
basis, exact Python arithmetic, and the domain soundness induction above.
The claim transferring a chromatic lower bound to any hypothetical image
additionally uses the accepted five-chromatic source theorem. This is
author-run independent algorithmic checking, not independent-author review
or proof-assistant formalization. No novelty claim is made for arc consistency
or the graph-homomorphism colouring principle.

## Completed pass

This family is closed: its sole map has 516 images. No relaxed pin set,
different host, larger search, or further construction family was started.
The prior [H560 closure through 503](../hadwiger_nelson_heule560_criticality_bound/README.md)
and its incomplete 504--508 frontier remain preserved. HN-3's
[parallel-line support theorem](../hadwiger_nelson_parallel_line_supports/README.md)
was inspected as separate geometric work and is not a premise here.
