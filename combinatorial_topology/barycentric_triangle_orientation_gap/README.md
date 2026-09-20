# Exact triangle-packing gap from orientation defects

For a finite pure two-dimensional simplicial complex $T$ with every edge
in at most two triangular facets, let $G=(\operatorname{sd}T)^{(1)}$ and
$f=f_2(T)$. Define $\kappa(T)$ as the fewest original facets one must
delete so that the retained facets can be coherently oriented across
their shared edges. Then

$$
\tau_\triangle(G)=\tau_\triangle^*(G)=\nu_\triangle^*(G)=3f,
\qquad
\nu_\triangle(G)=3f-\kappa(T).
$$

Here $\nu_\triangle$ is maximum edge-disjoint triangle packing,
$\tau_\triangle$ is minimum triangle edge cover, and stars denote the
usual fractional relaxations. Thus the entire additive integrality gap
is an orientation defect. Boundary and singular vertex links are allowed.
For surfaces, the gap vanishes precisely when all components are orientable.

The [proof](PROOF.md) is constructive: each original facet contributes a
six-cycle of flags. A coherent subfamily contributes three flags per facet,
and every remaining facet can greedily contribute two. Any full hexagon
in any packing must correspond to a coherently oriented facet.

For the ten-facet, six-vertex projective plane the values are
$\tau_\triangle=30$, $\nu_\triangle=27$, and $\kappa=3$. This is a compact
test case, not a classification result. A three-face book gives an explicit
eight-edge cover instead of the formula's nine, demonstrating why the
two-facet incidence assumption matters.

## Reproduce

From the repository root:

```sh
python3 combinatorial_topology/barycentric_triangle_orientation_gap/verify.py
cd combinatorial_topology/barycentric_triangle_orientation_gap
sha256sum -c SHA256SUMS
```

Tested with CPython 3.11.2, standard library only; approximately one second.
Normal and `python3 -O` execution give the same output:

```text
VERIFIED: 387 facet families, 6 fixtures, 27 local patterns, 1024 MIS controls
RP2: f=10, tau=tau*=nu*=30, nu=27, kappa=3
```

The third output line supplies the SHA-256 of [expected.json](expected.json).
The checker constructs the graph directly from face containment and
enumerates its three-cliques. It optimizes packing by exact maximum
independent set in the literal conflict graph, independently of the
orientation formula. It computes $\kappa$ by exhaustive facet deletions
and orientation propagation, and separately computes the signed edge
frustration by all binary assignments.

All 387 nonempty facet families on five labels satisfying the incidence
bound are checked (including 12 with nonzero defect), as are six named
fixtures and a relabelling of the projective plane. Packing witnesses are
replayed by literal graph-edge intersection. The half-weight fractional
packing and the $3f$ integral cover are checked directly. All 27 local
side-forbiddance patterns pass the greedy-completion check. The exact
optimizer is cross-checked on all 1,024 labelled graphs on five vertices
with a separate include/exclude recurrence, and also on the smaller
complexes. Invalid input, corrupt packings, and an empty cover are rejected.
Witness indices use sorted facets, sorted edges within each facet, and the
two endpoints of each edge in increasing order, six flags per facet.

The universal claim rests on the unformalized proof, not extrapolation
from these checks. No numerical solver, floating point, random sampling,
downloaded dataset, large certificate, or formal proof assistant is used.
Independent mathematical review is pending.

## Prior work and limits

[SOURCES.md](SOURCES.md) distinguishes the new quantitative packing bridge
from known flag-graph orientability and Sivaraman's equality of vertex and
edge frustration for signed subcubic graphs. The latter identifies
$\kappa$ also with the fewest incoherently directed shared edges over all
facet orientations; it is explicitly credited and reproved for this case.

The elementary consequence $\tau_\triangle\le(6/5)\nu_\triangle$ is neither
claimed sharp nor best known. The main result is the exact gap formula.
The general Tuza conjecture is not resolved. Bounded primary-literature
searches found no identical quantitative theorem; historical priority is
not asserted. No polygonal-face, higher-incidence, or weighted extension
is claimed.
