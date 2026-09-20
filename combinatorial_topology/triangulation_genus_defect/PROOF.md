# Bounded reconstruction of near-minimum-genus embeddings

## Statement and counting convention

Let `T` be a finite connected simplicial triangulation of a closed orientable
surface of genus `h`, with at least four vertices. Let `G` be its simple
1-skeleton. Assume:

> Every three-cycle of `G` is the boundary of a face of `T`.

Fix an orientation of `T`, and write `f` for its number of triangular faces.
We count **labelled orientable rotation systems**, with the cyclic order at every
vertex specified. Global reversal is counted separately, and graph automorphisms
are not factored out. These are the usual counts in the genus polynomial. Let
`a_j(G)` be their number with genus `j`.

For a rotation system `R` of genus `h+r`, let `S(R)` be the set of triangles of
`T` which are not faces of `R` in either orientation, and put `t=|S(R)|`.

**Theorem.**

1. The minimum genus of `G` is `h`, and `a_h(G)=2`.
2. If `r>0`, then
   \[
   2r+1\le t\le\min(8r,f).
   \]
   If the nontriangular faces of `R` have lengths `ell_1,...,ell_b`, then the
   stronger identities are
   \[
   b=t-2r,\qquad \sum_{i=1}^{b}\ell_i=3t,\qquad
   8r-t=\sum_{i=1}^{b}(\ell_i-4).
   \]
   Consequently, `t=8r` exactly when all the nontriangular faces are quadrilaterals.
3. Given `S`, delete its vertices from the face-adjacency dual of `T`. Each
   component of the retained triangles has one orientation bit. If `t>0`,
   there are at most `t` such components. At a vertex `v`, put
   `k_v=|{F in S : v in F}|`. The retained faces prescribe local successor
   relations. A valid completion has either a single forced cyclic order
   (`k_v=0`) or exactly `k_v` directed path blocks whose cyclic ordering has
   `(k_v-1)!` possibilities. There are altogether
   \[
   \sum_v k_v=3t\le24r
   \]
   path blocks at the vertices with `k_v>0`.
4. These data give an **exact, duplicate-free decoder** for genus `h+r`: enumerate
   `S`, the component orientation bits, and the local cyclic orders of path
   blocks; reject invalid partial permutations, then retain exactly those
   rotation systems of genus `h+r` with missing reference-face set exactly `S`.
   Every desired rotation system occurs once.
5. For `r>0`, the degree-independent coefficient bound is
   \[
   a_{h+r}(G)\le
   \sum_{t=2r+1}^{\min(8r,f)}
   \binom ft\,2^t\big((t-1)!\big)^3. \tag{1}
   \]
   With the promised triangulation supplied, all these rotation systems can be
   listed in `O_r((|V|+|E|) f^(8r))` time. A direct check of the triangle
   hypothesis takes an additional `O(|V|^3)` time. This is a polynomial-time
   enumeration for each fixed `r`, **not** a claimed fixed-parameter algorithm.
6. The coefficient eight is optimal: the octahedral graph has a torus rotation
   system which loses all eight faces of its spherical triangulation.

The theorem applies, for example, to four-connected spherical triangulations
and to triangular torus grids of sufficiently large periods. It does not assume
bounded vertex degree or bounded base genus. The hypothesis is stated directly;
we do not use “flag” as a synonym, since the tetrahedral sphere also satisfies it.

## 1. Euler defect and the sharp face budget

Use darts `(u,v)` of `G`. A local rotation `rho_v` permutes the neighbors of `v`
in one cycle, and the face permutation is

\[
\phi(u,v)=(v,\rho_v(u)).
\]

Every vertex of a simplicial closed triangulated surface has degree at least
three. In any rotation system of this simple graph there are no faces of length
one or two. A face of length three is a graph triangle. Moreover the two
orientations of the same graph triangle cannot both be faces: at each of its
vertices this would force a two-cycle inside the local rotation, contradicting
degree at least three and the requirement of a single cyclic order.

Thus each triangular face of `R` is a distinct face of `T`, by the hypothesis.
Exactly `f-t` reference triangles survive. Euler's formula gives

\[
|F(R)|=f-2r.
\]

For any rotation system, `3|F(R)|<=2|E|=3f`, so its genus is at least `h`.
If `b` faces are nontriangular, then

\[
b=(f-2r)-(f-t)=t-2r.
\]

Counting all darts in the nontriangular faces gives

\[
\sum_i\ell_i=2|E|-3(f-t)=3t.
\]

Each `ell_i>=4`, hence `3t>=4(t-2r)`, or `t<=8r`. Subtracting yields the
stated identity `8r-t=sum_i(ell_i-4)`. If `r>0`, some nontriangular face exists:
otherwise `t=2r` and `3t=0`, a contradiction. Therefore `t>=2r+1`.
For `r=0` the same inequalities force `t=0`: every reference triangle survives.

These are face-boundary orbits, not necessarily simple polygons when their
length exceeds three. Repeated vertices in longer faces do not affect the proof.

## 2. Orientation propagation on retained faces

For every surviving reference triangle, its direction in `R` agrees with the
fixed orientation of `T`, or is its reverse. If two surviving triangles share
an edge, their signs must agree: otherwise both face orbits use the same directed
dart of that edge. Face orbits partition the darts, making this impossible.
Therefore the sign is constant on every component of the retained dual graph.

The full dual is connected. With no deleted faces, it has one component. Both
global signs prescribe all the local rotations, proving `a_h(G)=2`.

Now suppose `t>0`. If no faces remain, the component count is zero. Otherwise
let `C` be any component of retained triangles. Its edge boundary in `T` is
nonempty, by connectivity of the full dual. The boundary, regarded as a graph
with coefficients modulo two, has even degree at each vertex: it is the boundary
of the two-chain formed by the triangles in `C`. A nonempty even subgraph of a
simple graph has at least three edges. Every such boundary edge separates a
triangle in `C` from a deleted triangle. Boundaries from different retained
components are disjoint as sets of edges. At most `3t` edges separate retained
and deleted faces. Thus, if there are `c` retained components,

\[
3c\le3t,\qquad c\le t. \tag{2}
\]

No assertion that these boundaries are disjoint simple curves, or that retained
regions are disks, is used. They may meet at vertices and have nontrivial topology.

## 3. Local path blocks

An oriented retained triangle `(u,v,w)` requires

\[
\rho_v(u)=w,
\]

and the analogous two conditions at `u` and `w`. At a vertex of degree `d_v`,
exactly `d_v-k_v` distinct reference corners remain. A proposed sign choice is
rejected if their successor requirements fail to define an injective partial
map; a valid extension necessarily has `d_v-k_v` arrows on `d_v` neighbor labels.

An injective partial map is a disjoint union of directed paths (including
isolated labels) and directed cycles. A proper directed cycle cannot be part
of a single cyclic order on all the neighbors. If all labels form one directed
cycle, the rotation is forced and `k_v=0`. In every other extendable case there
are no directed cycles, and the number of paths is

\[
d_v-(d_v-k_v)=k_v.
\]

Contract each path to one block. A single cyclic order on these `k_v` labelled
blocks, expanded by the fixed order within each path, is precisely one local
rotation extending the constraints. There are `(k_v-1)!` such orders. This proves
both directions of the local completion claim, including `k_v=1` and the case
where no reference face at `v` is retained. A vertex with `k_v=0` is reconstructed
without an independent orientation choice: the component bits already fix it.

Each deleted triangle contributes once to `k_v` at three distinct vertices, so
`sum_v k_v=3t`. Large vertex degrees increase the lengths of the forced paths,
but do not increase the number of freely ordered blocks beyond this budget.

## 4. Completeness, uniqueness, and the coefficient bound

Here is the decoder in full.

1. Enumerate the subsets `S` of reference faces in the specified size range.
2. Compute the retained dual components and assign one bit to each.
3. Insert all local successor requirements from oriented retained triangles.
   Reject conflicts, noninjectivity, or a proper directed cycle at any vertex.
4. At each unconstrained part, cyclically order the path blocks. One fixed block
   is put first to remove cyclic duplicates. Expand the blocks to a rotation.
5. Trace the face permutation. Keep the rotation exactly when its genus is
   `h+r` and its actual set of absent reference triangles is exactly `S`.

Any accepted output is a valid rotation system of the desired graph and genus,
by construction and the final check. Conversely, any such rotation system defines
its unique set `S`, its unique component signs, and its unique cyclic block orders,
so it is generated. The exact-absence check matters: deleting a constraint does
not forbid that triangular face from reappearing in the completion. The check
prevents counting such an embedding under more than one deletion set.

For a fixed `S` with `t>0`, (2) and the local count give at most

\[
2^t\prod_{v:k_v>0}(k_v-1)! \tag{3}
\]

candidates, with `0<=k_v<=t` and `sum_v k_v=3t`. The product is at most
`((t-1)!)^3`. To see this directly, define `w(0)=w(1)=1` and
`w(k)=(k-1)!` for `k>=1`. If `1<=a<=b<t`, moving one unit from `a` to `b`
weakly increases `w(a)w(b)`: the ratio is `b/(a-1)` for `a>=2` and `b` for
`a=1`. Repeated transfers fill three entries to `t` and leave all others zero.
For `t=1` the product is already one. This proves the uniform bound in (1).

Generating a fixed sign assignment, extracting the paths, and tracing a candidate
can each be done in linear time in the size of the input graph, with constants
depending on `r`. An invalid assignment costs at most the same amount. Summing
over the subsets and sign choices proves the stated running time; no assumption
on maximum degree is hidden in the algorithm. The checker implements the same
decoder for all genera of small fixtures, and a certificate round trip for larger
inputs, rather than attempting an impractical large fixed-`r` census.

## 5. Sharpness certificate

Number the opposite pairs of the octahedral graph as `{0,1}`, `{2,3}`, `{4,5}`.
Its eight spherical faces are all triples choosing one vertex from each pair;
these are exactly all graph triangles. The following neighbor orders define a
torus embedding:

```text
0: 2 3 4 5
1: 2 5 4 3
2: 0 1 4 5
3: 0 5 4 1
4: 0 1 2 3
5: 0 3 2 1
```

The face permutation has these six orbits, displayed by their vertex sequences:

```text
0 2 1 5
0 3 5 2
0 4 1 3
0 5 3 4
1 2 4 3
1 4 2 5
```

They use all 24 darts exactly once. Since `6-12+6=0`, the genus is one.
No triangular face remains, so `t=8=8r`. Thus the coefficient eight cannot be
reduced in a universal inequality of this form. We do not claim that the
polynomial exponent or the factorial coefficient bound is optimal.

## 6. Scope, necessity of the hypothesis, and prior work

For fixed `r`, (1) excludes exponentially many genus-`h+r` rotation systems as a
function of the number of reference faces in this class. In particular it gives
`a_r(G)=O_r(|V(G)|^(8r))` for four-connected planar triangulations. This blocks the
specific fixed-genus exponential counting mechanism in Mohar's counterexamples
from persisting within this class. It **does not** imply log-concavity, unimodality,
or any inequality between three successive coefficients, and does not settle
Mohar's conjecture for all triangulating graphs.

Dropping the hypothesis is not harmless. `K_7` has distinct triangular torus
rotation systems with different facial triangles. Comparing them gives `r=0`
but `t>0`. The verifier constructs two explicit such systems and checks their
Euler characteristics and distinct triangle sets. It also confirms that the
input hypothesis validator rejects them. Thus an extension to arbitrary
triangulations would need to control trades involving nonfacial graph triangles.

Primary context: Bojan Mohar, *Strong log-convexity of genus sequences*,
[arXiv:2405.10854v2](https://arxiv.org/abs/2405.10854), especially the unstable-triangle
argument in the proof of Theorem 3 and Conjecture 11. Euler's formula, rotation systems, and local embedding completion are classical.
The claimed contribution is the sharp lost-triangle budget combined with the
complete degree-independent bounded-block decoder and resulting coefficient
bound under the explicit triangle hypothesis. Targeted primary-literature and
graph searches on 2026-09-20 found no matching statement; this is search-relative
novelty, not a priority claim.

The proof is elementary and unformalized. The finite computation corroborates
the correspondence and checks the sharpness and hypothesis counterexamples;
it does not replace the all-parameter argument or independent review.
