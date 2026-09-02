# Exact reconstruction of Haugland's `T5`, `T6`, `G0`, and 740-vertex 7-core

## Certified result

This directory independently reconstructs the finite construction pipeline in
Section 3 of Jan Kristian Haugland's 2026 heptagonal unit-distance construction.
Every equality and unit-distance decision is exact.

Let `U={u_0,...,u_83}` be the 84 directed unit vectors in the paper, let
`A=(0,0)`, and let `B=(0,sqrt(3))`.  The exact radius-3 Cayley ball generated
by `U` has sphere counts

```text
distance 0:      1
distance 1:     84
distance 2:  3,444
distance 3: 80,052
ball total: 83,581
```

The point sets consisting of vertices on an `A`-to-`B` polygonal walk of
length at most 5 and 6 have, respectively,

```text
|T5| = 1,042
|T6| = 12,856.
```

All 12,852,549 unordered pairs of `T6` with at least one endpoint in `T5`
are covered by a no-false-negative modular sieve and exact confirmation.
There are exactly 36,583 strict unit pairs, and every one has difference in
`U`.  Thus the adjacency counts used in the definition

```text
G0 = T6[{v : v in T5 or v has at least 7 neighbours in T5}]
```

are exhaustive for the induced strict unit-distance graph, not merely for the
declared Cayley generators.  The resulting `G0` has 1,294 vertices.  Exhausting
all 836,571 pairs within `G0` gives 6,727 strict unit edges.

Simultaneous deletion of vertices of current degree below 7 removes

```text
302, 144, 72, 24, 12
```

vertices in five rounds.  The remaining 7-core has exactly 740 vertices and
3,985 strict unit edges.  Its exact point set equals the set reconstructed from
the 231 Appendix A paths in arXiv v4, and its edge set in Appendix-path order
equals the sibling exact strict-edge census, with canonical edge SHA-256

```text
3b01cdfc34edc58e6883f5da69cf06457701a5c76110d32a89af8fab30b453f5
```

This replaces the paper's numerical path-discovery and point-identification
step for these particular sets with an exact construction.  It reproduces
known graph sizes; it is not a graph below the 509-vertex record.

## Finite reduction

Write `d(P,x)` for word distance from `P` using the symmetric generator set
`U`.  A point `x` lies on an `A`-to-`B` walk of length at most `n` exactly when

```text
d(A,x) + d(x,B) <= n.
```

The checker proves exactly that `B+u_56+u_70=A`, while `|A-B|^2=3`, so
`d(A,B)=2`.  It follows that

```text
T5 = {x in Ball_3(A) intersect Ball_3(B) : d(A,x)+d(x,B) <= 5},

T6 = Ball_2(A) union Ball_2(B)
     union (Sphere_3(A) intersect Sphere_3(B)).
```

For the second identity, a point on a walk of length at most 6 either lies
within two steps of an endpoint or has endpoint distances `(3,3)`.  Conversely,
every radius-2 point about an endpoint lies on a walk of length at most 6 by
going to the point, returning to that endpoint, and taking the two-step
endpoint walk.  Therefore radius 3 is the complete enumeration frontier; no
floating cutoff or unenumerated longer ball is hidden in the counts.

Coordinates are represented in

```text
Q[x] / (x^24 + x^22 - x^18 - x^16 + x^12 - x^8 - x^6 + x^2 + 1)
  = Q(zeta_84).
```

For the strict-edge censuses, evaluation at an element of exact order 84
modulo a prime is a ring homomorphism because all coordinate denominators are
invertible.  Hence an exact unit pair must survive every modular test.  Every
survivor is checked again in characteristic zero; modular arithmetic never
certifies an edge.  The primary route uses `(p,zeta)=(2521,1397)` and
`(2689,2025)`.

## Independent routes

`exact_cayley_core.py` and `exact_field.py` form the primary route.  They use a
small standard-library rational quotient-field implementation, breadth-first
Cayley-ball expansion, modular unit-circle buckets for the 12.85-million-pair
census, and simultaneous core peeling.

`independent_check.py` imports no primary arithmetic or enumeration code.  It
uses SymPy's `AlgebraicField`, enumerates unordered step multisets directly
(complete because vector addition is commutative), loops over all relevant
unordered pairs instead of using unit-circle buckets, uses the different
specializations `(1009,527)` and `(2521,1397)`, and computes the 7-core by a
queue deletion algorithm.  The two routes agree on every point-set and edge-set
hash, not only on aggregate counts.

The independent route is algorithmically and arithmetically different, but it
shares the formulas for Haugland's 84 vectors and the sibling JSON transcription
of the 231 Appendix paths.  A fresh download of arXiv v4 was checked during the
certificate run: all 231 path rows agree entry-for-entry with that JSON.

## Reproduction

Run from the repository root with CPython 3.11 or newer.  Put environments and
all generated output under `/scratch`:

```bash
python3 -m venv /scratch/haugland-cayley-core-venv
/scratch/haugland-cayley-core-venv/bin/pip install -r \
  hadwiger_nelson_haugland_cayley_core_exact/requirements.txt

/scratch/haugland-cayley-core-venv/bin/python \
  hadwiger_nelson_haugland_cayley_core_exact/exact_cayley_core.py verify \
  hadwiger_nelson_haugland2131_exact_reproduction/graph.json \
  hadwiger_nelson_haugland_cayley_core_exact/certificate.json

/scratch/haugland-cayley-core-venv/bin/python \
  hadwiger_nelson_haugland_cayley_core_exact/independent_check.py \
  hadwiger_nelson_haugland2131_exact_reproduction/graph.json \
  hadwiger_nelson_haugland_cayley_core_exact/certificate.json

python3 hadwiger_nelson_haugland_cayley_core_exact/test_exact_core.py
```

Expected summaries are in `expected.txt`.  On the reference host the primary
and independent routes took 230 and 273 seconds, respectively, and used no SAT
solver or proof trace.  `certificate.json` stores only deterministic counts,
canonical hashes, and the primary sieve parameters; it is not a dump of the
generated point or edge sets.

Optionally download the immutable arXiv v4 source under `/scratch` and check
the shared Appendix transcription:

```bash
curl -fsSL https://arxiv.org/e-print/2608.04542v4 \
  -o /scratch/haugland-2608.04542v4.tar
mkdir -p /scratch/haugland-2608.04542v4
tar -xf /scratch/haugland-2608.04542v4.tar \
  -C /scratch/haugland-2608.04542v4
python3 hadwiger_nelson_haugland_cayley_core_exact/verify_arxiv_source.py \
  /scratch/haugland-2608.04542v4/Moser_spindle_free_UDG_v4.tex \
  hadwiger_nelson_haugland2131_exact_reproduction/graph.json \
  hadwiger_nelson_haugland_cayley_core_exact/certificate.json
```

## Scope and trust boundary

This certificate proves the exact `T5`, `T6`, `G0`, and 7-core reconstruction
and identifies the final strict graph with the published 740-vertex path set.
It does **not** prove Haugland's Lemma 2.2 for all multisets of two through eight
steps, the endpoint-forcing SAT assertion, non-4-colourability of the final
2,131-vertex graph, spindle-freeness, or any improvement to the current bounds
`5 <= chi(R^2) <= 7`.

The trust base is CPython's integer, `Fraction`, set, JSON, and SHA-256
implementations for the primary route; CPython and SymPy 1.14.0 algebraic-field
arithmetic for the independent route; the displayed finite reduction; and the
shared transcription noted above.  No floating-point number affects a set,
equality, adjacency, or graph-core decision.

Primary source: J. K. Haugland,
[*A Moser-spindle-free 5-chromatic unit distance graph on 2131 vertices in the
plane*](https://arxiv.org/abs/2608.04542v4), 2026.
