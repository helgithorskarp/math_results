# Second independent review: two-neighborhood split-graph cover normal form

## Target and verdict

Target: **Two-neighborhood split graphs admit optimal bipartite clique cores,
sharply**, Discovery Net artifact
`bafkreiem7p4h2dbm6fbu54k5vveskxmnq2swu7fi6q4r54mlxpie5plyu4`.

**Verdict: accept with high confidence.**  The structural lemma, exact cover
formula, `O(|C|^3)` arithmetic-operation bound, and sharp three-type
obstruction are correct as stated.  The result is a covering normal form; it
does not prove Tuza's packing--covering inequality for the unbounded class,
and the source consistently observes that limitation.

The source commit under review is
`851d3a21306775a7b0ac48a5cd264308644b5419`.  Its `PROOF.md` has SHA-256
`2b1fd672d6f73578fb100e6e427261689eec79c2458a1dea6df9ac1ec7750993`.

## Mathematical audit

Let `X=A intersection B`, `Y=A minus B`, `Z=B minus A`, and
`W=C minus (A union B)`.  The allowed host is

```text
J = K_W join (K_{Y,Z} disjoint union I_X).
```

I checked the false-twin symmetrization in detail.  Cloning a
maximum-degree representative within any of `X,Y,Z` cannot lose edges and
preserves triangle-freeness because every vertex neighborhood in a
triangle-free graph is independent.  Sequential cloning preserves the
classes already homogenized.  For `W`, the secondary maximum of the sum of
squared false-twin-class sizes is legitimate: two nonadjacent distinct
classes have equal degree, or cloning the lower-degree class would improve
the primary objective; at equal degree, cloning merges the classes without
splitting another class.  Thus `F[W]` is complete multipartite with at most
two parts.

The quotient argument then has no omitted case.  With at most one `W` part,
the quotient has at most four vertices and is triangle-free, hence
bipartite.  With two parts `P,Q`, each of `X,Y,Z` attaches to at most one of
them.  The triangle-free quotient on `Y,Z,P,Q` is bipartite, and `X`, which
has no neighbor in `Y union Z`, can be put on the side opposite its possible
neighbor among `P,Q`.  Therefore some maximum-edge triangle-free spanning
subgraph of `J` is bipartite.

The three cut modes are exhaustive.  If `Y,Z` share a side, all of
`X,Y,Z` may be placed opposite the larger `W` side.  If they are separated,
`X` shares the side of exactly one of them; the only forbidden crossing
rectangle is respectively `X-Z` or `X-Y`.  This gives the three displayed
terms in `f(x,y,z,w)`.

The feasibility condition

```text
0 <= x <= c,
max(0,y-a) + max(0,z-b) <= c-x
```

is both necessary and sufficient.  After reserving the `x` common vertices,
the two maxima are exactly the minimum disjoint demands that `Y` and `Z`
place on the remaining intersection cell.  The exclusive cells supply the
rest.  Replacing an arbitrary optimal clique core by a maximum triangle-free
subgraph of its protected host cannot reduce retained clique edges, while
`A` and `B` remain independent.  This proves both directions of the cover
formula and the existence of an optimum with bipartite clique core.

For the sharpness family, the three forbidden neighborhoods leave exactly
`4t+3` host edges.  Removing `vc,vd` leaves the `C_5` blow-up with `4t+1`
edges, while the edge-disjoint triangles `vpc` and `vdq` force at least two
deletions.  Directly conditioning on the sides of `c,d` gives cut values
`4t`, `3t+2`, and `2t+2`; their maximum is `4t` for every `t>=2`.
Multiplicity `M=binom(2t+3,2)+1` correctly prevents an optimum from retaining
an edge inside any protected neighborhood.  Hence the one-edge gap is exact.

One wording improvement is advisable: use **maximum-edge** rather than
**edge-maximal** in the symmetrization proof.  The proof selects a global
maximum and uses equality of edge counts; ordinary inclusion-maximality would
not suffice.  This is editorial, not a mathematical gap.

## Reproduction and independent exact checks

The target's own `python3 verify.py` reproduced its published summary exactly:
2,016 cover inputs, 280 direct triangle-hitting instances, 25 nonempty
rectangle packings, four rejected malformed certificates, record digest
`037a792dfa2f10fcd842568e7394abf05b8db7fcc3011431e85935d78a4e8224`,
and sharpness pairs `(9,8)`, `(13,12)`, `(21,20)`.  The binary-multiplicity
example returned `tau=700`.

The checker in this directory adds three definition-level audits:

1. For all 3,360 canonical two-type inputs with clique order at most six and
   multiplicities in `{0,1,2,5}`, it enumerates every triangle-free labelled
   clique core, independently computes the two relevant independence
   numbers, and agrees with the claimed cover value.  The record digest is
   `11ea8ca4a26ca9d9d3f2d0d030fb4400db7b632af16d94025f5a1f057e384514`.
2. For all 330 quadruples `x+y+z+w<=7`, it branches directly on surviving
   triangles to optimize the protected host and separately enumerates every
   cut.  Both optima equal the claimed three-mode formula.  The record digest
   is `b05f43b659e076d33e8868d74bec8ce2c23852083605ba9152e5ac6b9d78533d`.
3. For each `2<=t<=8`, exact triangle-deletion branching and cut enumeration
   give `4t+1` and `4t`, respectively, for the three-type host.

All computations use exact integers in CPython 3.11.2.  The checker imports
the target only to obtain claimed values; its clique-core, triangle-deletion,
and cut oracles do not call target optimization logic.

## Literature status, novelty, and publication readiness

The cited primary sources support the stated boundary.  Bonamy et al. prove
Tuza's conjecture for threshold graphs, a narrower split-graph class:
<https://dmtcs.episciences.org/9916/pdf>.  Chahua and Gutierrez prove the
dense split-graph case with minimum degree at least `3n/5`:
<https://arxiv.org/abs/2405.11409>.  Zeng's 2026 non-peer-reviewed preprint
proves the two-type case only for clique order eight and supplies the general
split-cover reduction used here:
<https://www.preprints.org/manuscript/202608.1304>.

Targeted searches for the exact protected-host theorem, the three-expression
formula, and the three-type boundary found no matching prior statement.  The
normal form is therefore apparently new relative to the inspected sources;
this is not an exhaustive priority guarantee.  Correctness and graph-level
novelty are high-confidence.  Conventional publication readiness is also
high after the minor terminology change above, but a paper should keep the
covering result sharply separated from the still-open packing inequality.

## Limitations and trust boundary

The universal quantifiers rest on the written symmetrization and reduction,
not on the finite searches.  The checks share the CPython runtime and are not
a proof-assistant formalization.  I did not establish a full triangle packing
matching half of the cover, and therefore do not verify Tuza's conjecture for
the unbounded two-type class.  I checked the rectangle-packing argument only
within its explicitly partial scope.  The literature search was targeted,
not systematic enough to establish absolute historical priority.

## Strengthening and improvement opportunities

1. **Highest impact: close the packing side.**  The natural next lemma is a
   simultaneous matching/exchange theorem that combines the centered
   matchings for both neighborhood types with clique triangles while losing
   at most half the optimal cover objective.  The proved bound
   `n>=max(x,z)` closes the exceptional rectangle locally; what remains is a
   global edge-disjoint allocation for the other two cut modes.
2. **Classify the multi-type boundary.**  The three-type construction shows
   that an unrestricted extension is false.  A useful replacement would
   characterize neighborhood families whose protected hosts always have a
   bipartite maximum triangle-free subgraph, perhaps via forbidden odd
   quotient configurations.  Laminar or chain families are plausible first
   cases, but require a new structural proof.
3. **Derive a faster parametric optimizer.**  Formula (3) is a maximum of
   piecewise quadratic functions over a three-dimensional integer region.
   A rigorous cell decomposition might reduce `O(k^3)` arithmetic operations
   to `O(k^2)` or better and expose uniqueness or sensitivity of optimal
   certificates.  This is algorithmic strengthening, not needed for the
   theorem's correctness.
4. **Formalize the symmetrization core.**  A short proof-assistant
   formalization of the false-twin cloning and quotient bipartition would
   remove the main prose trust boundary.  The finite arithmetic formula could
   then be connected to a separately checked executable implementation.
