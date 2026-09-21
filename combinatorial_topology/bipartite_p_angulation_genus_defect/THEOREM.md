# The bipartite parity gap for clean even angulations

## 1. Statement

Let `p>=4` be even. Let `T` be a finite connected cellular embedding of a
simple bipartite graph `G` in a closed orientable surface of genus `h`. Assume

1. every reference face boundary is a simple `p`-cycle;
2. `delta(G)>=3` and `G` has girth `p`; and
3. every graph `p`-cycle is the boundary of a reference face.

Call this a **clean bipartite `p`-angulation**. Fix one orientation of `T`
and let `f` be its number of faces. We count labelled orientable rotation
systems of `G`, with global reversal separate and without quotienting by graph
automorphisms. Write `a_j(G)` for the number of such systems of genus `j`.

For a rotation system `R` of genus `h+r`, let `S(R)` be the reference faces
which are not faces of `R` in either orientation and put `t=|S(R)|`. Let
`ell_1,...,ell_b` be the lengths of the non-reference faces of `R`.

**Theorem.** The minimum orientable genus of `G` is `h` and `a_h(G)=2`. If
`r>0`, then

```text
b = t-2r,
sum_i ell_i = pt,
(p+2)r-t = (1/2) sum_i (ell_i-(p+2)),               (1)
2r+1 <= t <= min((p+2)r,f).                         (2)
```

Equality `t=(p+2)r` holds exactly when every non-reference face has length
`p+2`.

The missing-face reconstruction of the general clean-angulation theorem
therefore gives

```text
a_(h+r)(G)
  <= sum_{t=2r+1}^{min((p+2)r,f)}
       binom(f,t) 2^t ((t-1)!)^p.                  (3)
```

For fixed `p,r`, all rotations of genus `h+r` can be listed in

```text
O_(p,r)((|V|+|E|) f^((p+2)r))                      (4)
```

time. This is a fixed-degree polynomial statement, not an FPT claim.

For `p=4`, (2) is the uniform bound `t<=6r`, improving the general clean
quadrangulation bound `t<=10r`. The cube attains the new endpoint at `r=1`:
eight of its labelled rotation systems lose all six reference squares and
replace them by four hexagonal faces.

## 2. Short faces and minimum genus

Write a dart as `(u,v)`. If `rho_v` is the cyclic order at `v`, the face
permutation sends

```text
(u,v) -> (v,rho_v(u)).
```

Every face orbit is a closed non-backtracking walk. An immediate reversal
would make a cyclic permutation on at least three neighbours fix a neighbour.
A closed non-backtracking walk shorter than the girth contains a shorter graph
cycle, so every face has length at least `p`. A face of length exactly `p` is
a simple graph `p`-cycle and hence, by cleanliness, a reference face. The two
orientations of one reference cycle cannot both be faces: locally that would
put a proper 2-cycle inside a cyclic permutation of at least three labels.

Since `2|E|=pf`, any rotation system has at most `f` faces. Euler's formula
then gives genus at least `h`. Equality forces all `f` faces to be reference
faces. Adjacent retained faces must have a common orientation sign, because
opposite signs would use one directed edge twice. The reference dual is
connected, so the only genus-`h` systems are `T` and its global reversal.

## 3. Exact Euler defect and the new parity step

Euler's formula gives `|F(R)|=f-2r`. Exactly `f-t` faces are retained
reference faces. Hence

```text
b=(f-2r)-(f-t)=t-2r.                               (5)
```

The retained faces use `p(f-t)` darts, so the other face orbits use

```text
sum_i ell_i = 2|E|-p(f-t)=pt.                      (6)
```

This is where bipartiteness produces a strict structural gain. Every closed
walk in a bipartite graph has even length. Thus every `ell_i` is even. It is
larger than `p`, by the short-face argument, and `p` is even; consequently

```text
ell_i >= p+2.                                      (7)
```

Substitute (5) and (6):

```text
sum_i (ell_i-(p+2))
  = pt-(p+2)(t-2r)
  = 2((p+2)r-t).
```

This proves (1), including integrality and nonnegativity of its right side,
and gives the upper bound in (2). If `r>0`, then `b>0`: otherwise (5) would
give `t=2r`, while (6) would give `pt=0`. Hence `t>=2r+1`. The equality
criterion follows term by term from (7).

The same proof can be viewed as a face-length-gap principle. The general
clean-angulation argument only knows `ell_i>=p+1` and therefore gives
`t<=2(p+1)r`. Bipartite parity deletes that entire first length layer.

## 4. Reconstruction and counting

For completeness, recall why the remaining decoder depends only on `p` and
the number `t` of missing faces.

Delete `S` from the reference face-adjacency dual. Each retained component
has one orientation bit. A nonempty retained component has a nonempty
mod-two edge boundary in `G`; that boundary is an even subgraph and therefore
contains a cycle. Girth `p`, edge-disjointness of component boundaries, and
the `pt` incidences supplied by deleted faces show that there are at most `t`
retained components.

At a vertex `v`, let `k_v` be the number of deleted reference faces incident
with `v`. The surviving oriented face corners prescribe an injective partial
successor map on the neighbours of `v`. If it is extendable and not already
forced, it is a disjoint union of exactly `k_v` directed path blocks. Its
cyclic completions are the cyclic orders of these blocks, numbering
`(k_v-1)!`. Since deleted faces are simple `p`-cycles,

```text
sum_v k_v=pt.                                      (8)
```

Enumerating `S`, component signs, and local block orders, followed by an
exact face check, is complete and duplicate-free. Convex transfer under
`0<=k_v<=t` and (8) gives

```text
product_v (k_v-1)! <= ((t-1)!)^p,
```

where the factors for `k_v=0,1` are one. Equations (2) and (3) now follow.
For fixed `p,r`, all remaining work for one candidate is linear in the input
size, and the missing-face enumeration has degree at most `(p+2)r`; this
proves (4).

## 5. Exact audit and trust boundary

`verify.py` uses only the definition of a rotation system. It fixes the
labelled cube, enumerates its `2^8=256` local cyclic-order choices, traces all
24 darts into face orbits, computes genus by Euler's formula, and determines
the missing reference squares up to direction. For every system it checks:

- all face lengths are even;
- every 4-face is a reference square;
- (5), (6), and the exact parity identity (1);
- both bounds in (2); and
- the equality characterization.

The code also freezes the complete `(r,t,non-reference lengths)` profile and
rejects a deliberately odd face-length record. This checks conventions and
the endpoint, but the universal theorem rests on the proof above.

## 6. Relation to prior work and novelty boundary

The direct dependency is the committed clean-`p`-angulation face-defect and
decoder theorem:

- Discovery Net `bafkreihfpo6myja6hw2zczn3ypmueq5mly3pdrdopie7o7qk3ifdqb23re`;
- public source: <https://github.com/helgithorskarp/math_results/tree/main/combinatorial_topology/p_angulation_genus_defect>.

Bojan Mohar's *Strong log-convexity of genus sequences*,
<https://arxiv.org/abs/2405.10854>, is the primary genus-distribution context.
Chen--Reidys, *On the local genus distribution of graph embeddings*,
<https://arxiv.org/abs/1601.02574>, treats rotation changes locally. Liu,
Ellingham, and Ye, *Minimal quadrangulations of surfaces*,
<https://arxiv.org/abs/2106.13377>, gives current quadrangulation context.

Targeted primary-source searches on 2026-09-21 for bipartite
quadrangulation/`p`-angulation genus distributions, rotation systems, and
missing-face reconstruction found no matching parity-gap identity or decoder
exponent. The novelty claim is therefore bounded-search relative, not an
exclusive claim of priority. Closed walks in bipartite graphs, Euler's
formula, and rotation systems are classical; the claimed increment is their
use in the exact all-parameter defect identity (1) and the resulting
reconstruction bound (3)--(4).

The theorem does not assert optimality of `(p+2)r` for every `p,r`, address
nonbipartite angulations, or prove log-concavity or unimodality of a genus
distribution.
