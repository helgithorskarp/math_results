# A 9/8 Tuza bound from a bridgeless facet dual

Let `T` be a finite nonempty pure two-dimensional abstract simplicial
complex in which every edge belongs to at most two triangular facets.  Let
`f` be its number of facets, let `D(T)` be its facet-dual graph, and put

```text
G = (sd T)^(1).
```

If `D(T)` is 2-edge-connected, then

```text
tau_triangle(G) = 3f,
nu_triangle(G) >= 3f-floor(f/3),
tau_triangle(G) <= (9/8) nu_triangle(G).            (1)
```

The previously proved exact identity is

```text
nu_triangle(G)=3f-kappa(T),
```

where `kappa(T)` is the minimum number of facets whose deletion makes the
remaining orientation constraints coherent.  Sivaraman identifies this
vertex-frustration number with edge frustration for signed subcubic graphs.
Chen--Li--Wang then give `kappa<=f/3` apart from five signed graphs.

The new point is that none of those five exceptions can be a signed facet
dual of `T`.  Four are cubic and would normalize to a closed nonorientable
triangulated surface with only four or eight facets; every such surface has
at least ten facets.  The fifth would force exactly one boundary edge, while
the boundary-edge degree at every vertex of an abstract triangle complex is
even.

The complete proof is in [THEOREM.md](THEOREM.md).

## Reproduction

The theorem is structural and does not depend on computation.  A compact
exact checker transcribes the five primary-source exceptions, verifies their
degrees and frustration indices by definition, and exhausts the canonical
triangle-side gluings.  Independent cyclic relabeling at each facet reduces
the raw `6^f` assignments to exactly `2^f` representatives; every orbit is
covered and no exception produces an abstract simplicial complex.

```bash
cd graph_theory/barycentric_tuza_nine_eighths
PYTHONDONTWRITEBYTECODE=1 python3 -m unittest -v test_verify.py
PYTHONDONTWRITEBYTECODE=1 python3 verify.py
sha256sum -c SHA256SUMS
```

Expected output is recorded in `EXPECTED_OUTPUT.txt`.  The checker requires
CPython 3.11 or later and only the standard library.

## Files and trust boundary

- `THEOREM.md`: universal proof and dependency boundary.
- `verify.py`: exact signed-graph and canonical-gluing audit.
- `test_verify.py`: focused positive, negative, and boundary tests.
- `SOURCES.md`: primary-source and Discovery Net status audit.
- `EXPECTED_OUTPUT.txt`: compact frozen output.
- `SHA256SUMS`: integrity manifest.

The checker uses integers and finite sets, with no solver, floating point,
randomness, network input, external dataset, or omitted certificate.  The
finite scan corroborates the five-exception elimination; it is not an
extrapolation to arbitrary complexes.
