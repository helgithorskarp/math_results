# Linear triangle-packing loss for comparable twin classes

For fixed `d` and `alpha>0`, every mixed-template graph with at most `d`
classes, each of size at least `alpha N`, has

```text
nu*(G) - nu(G) = O_{d,alpha}(N).
```

Here `nu*` is the **full** fractional triangle-packing optimum, and `nu` is
the maximum number of edge-disjoint triangles. Each class is a clique or
independent set; each cross pair is complete or empty. The result applies
to every feasible profile, including zeros and arbitrarily small positive
coordinates. It requires no positive profile margin, fixed ray or rationality.

This is a complete author proof awaiting independent mathematical review.
Its new constructive step preserves every local role count while realizing
small profile components by swaps. A finite threshold hierarchy then makes
the remaining large components suitable for Keevash's generalized partite
family decomposition theorem. That universal existence theorem is imported.
See [PROOF.md](PROOF.md) and [SOURCES.md](SOURCES.md).

More precisely, put

```text
M = binom(d+2,3) + binom(d+1,2),       lambda = 8M/alpha.
```

For every full real profile `z` of triangles plus unused single edges, and
every sufficiently large `N`, define

```text
t_P = floor((1-lambda/N) z_P),
m_P = t_P if t_P >= N, and 0 otherwise.
```

A packing realizes exactly `m_T` triangles of each type. Thus, above a
uniform threshold `N_0(d,alpha)`,

```text
nu*(G) - nu(G) <= M(1 + 4/(3alpha)) N.
```

The threshold is existential and not made effective here. Enlarging the
constant handles all smaller orders, giving the stated `O(N)` result.
Linear order is necessary already for even complete graphs, whose gap is
at least `N/6`. Our coefficient is not claimed sharp.

This removes the positive-coordinate lower bound from the main profile
theorem in the [preceding robust-profile package](../tuza_uniform_profile_realization/README.md).
The class-size condition remains: classes of size `o(N)` are excluded.
There is no unrestricted uniform `O_d(N)` claim and no solution of all-order
three-neighborhood Tuza. The previous package's sharper exact split-template
decomposition criterion is a separate result, not an unconditional conclusion
of the present packing theorem.

## What crosses the profile boundary

Coordinates below the integer cutoff cost only `O_d(N)` when discarded.
The retained sparse coordinates are realized with exactly balanced
vertex-pattern roles. Initially, consecutive cyclic role lists may repeat
edges. Swapping two same-type positions in copies of the same pattern
preserves all those roles and strictly decreases the number of repeated
edge occurrences. The proof bounds the rejected candidate positions.

A second switching lemma realizes small complement degrees while avoiding
the already packed sparse edges. A finite list of decreasing thresholds,
fixed before the profile is supplied, has an empty interval because there
are only boundedly many coordinates. This makes the sparse deletion small
enough for the dense family theorem while retaining the exact local lattices.
The argument does not infer uniformity from compactness.

Complete split graphs provide explicit optimum profiles approaching the
boundary. With core size `t^2` and independent size `t^2-1-t`, the clique-only
triangle mass is `t^3/6`; on the other side, at independent size `t^2-1+t`,
the spare spoke mass is `t^3`. These positive masses have order `N^(3/2)`.
The formulas are checked exactly and demonstrate the scope change; the
complete-split examples themselves are not claimed new.

## Reproduce the exact audit

Python 3.11.2 was used; all code requires only the standard library. From
this directory:

```bash
python3 check.py > /tmp/comparable-classes-audit.json
cmp /tmp/comparable-classes-audit.json AUDIT.json
python3 -O check.py > /tmp/comparable-classes-optimized.json
cmp /tmp/comparable-classes-optimized.json AUDIT.json
sha256sum -c SHA256SUMS
```

Expected output is byte-identical to [AUDIT.json](AUDIT.json), with `PASS`.
[RUN.json](RUN.json) records the interpreter, runtime and audit hash.
[switching.py](switching.py) constructs the finite objects;
[check.py](check.py) separately formulates the edge, role and degree checks.
[FIXTURES.json](FIXTURES.json) specifies five deterministic sparse instances.

The audit checks:

- all 62,152 swaps, including strict conflict decrease and fresh replacement
  edges, across five instances with repeated types and spare-edge components;
- every final component and vertex-pattern role count, with compact hashes
  of the regenerated components and traces;
- 25 degree-list realizations avoiding forbidden edges, including both
  one-vertex and two-vertex augmentation cases;
- the two constructions together on a 2,048-vertex host: 30,720 sparse edges
  and 4,096 disjoint remainder edges of maximum degree four;
- 669 compressed role intervals on all 74 mixed templates with at most
  three classes and six explicit optimum boundary profiles;
- 64 threshold-endpoint cases and eight invalid constructions, all rejected.

Large profile instances are checked by exact compressed intervals, not by
claiming to materialize enormous triangle packings. All literal components
and swap traces are regenerated and replayed in memory. No omitted external
certificate, solver, floating-point calculation or private input is needed.

The finite checker establishes the listed constructive identities and
witnesses. It does not prove Keevash's universal theorem, formalize the
present argument, supply its threshold constants, or constitute independent
peer review. No new general design-existence or absolute novelty claim is
made.
