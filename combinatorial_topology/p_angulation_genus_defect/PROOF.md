# Uniform face-defect reconstruction for clean p-angulations

## Statement and conventions

Let `p>=3`.  Let `T` be a finite connected cellular embedding of a simple
graph `G` in a closed orientable surface of genus `h`.  Assume:

1. every face boundary of `T` is a simple `p`-cycle;
2. `delta(G)>=3` and `G` has girth `p`; and
3. every `p`-cycle of `G` is the boundary of a face of `T`.

Call such a specified embedding a **clean p-angulation**.  Fix an orientation
of `T`, let `f` be its number of faces, and count labelled orientable rotation
systems of `G`; global reversal counts separately and graph automorphisms are
not factored out.  Write `a_j(G)` for the number having genus `j`.

For a rotation system `R` of genus `h+r`, let `S(R)` be the reference faces
that are not faces of `R` in either orientation, and put `t=|S(R)|`.

**Theorem.**

1. The minimum orientable genus of `G` is `h`, and `a_h(G)=2`.
2. If `r>0`, then

   ```text
   2r+1 <= t <= min(2(p+1)r,f).
   ```

   If the `b` non-reference faces of `R` have lengths
   `ell_1,...,ell_b`, then

   ```text
   b = t-2r,
   sum_i ell_i = pt,
   2(p+1)r-t = sum_i (ell_i-(p+1)).                 (1)
   ```

   Hence equality in the upper bound is equivalent to every non-reference
   face having length `p+1`.
3. Delete `S` from the face-adjacency dual of `T`.  Every retained component
   has one orientation bit, and, when `t>0`, there are at most `t` retained
   components.  If `k_v` is the number of deleted reference faces incident
   with `v`, then the retained faces leave exactly `k_v` directed path blocks
   at `v` in every extendable non-forced partial rotation.  Thus there are
   exactly

   ```text
   sum_v k_v = pt
   ```

   local blocks, independently of the vertex degrees.
4. These data give a complete duplicate-free decoder: enumerate `S`, the
   component bits, and cyclic orders of the local path blocks; reject
   inconsistent partial permutations, and finally retain exactly the
   rotations of genus `h+r` whose actual missing set is `S`.
5. For `r>0`,

   ```text
   a_(h+r)(G)
     <= sum_{t=2r+1}^{min(2(p+1)r,f)}
          binom(f,t) 2^t ((t-1)!)^p.                (2)
   ```

   Given `T`, all such rotations can be listed in
   `O_(p,r)((|V|+|E|) f^(2(p+1)r))` time.  This is a fixed-parameter-degree
   polynomial statement, not an FPT claim.

For `p=3`, this specializes to the earlier sharp `8r` triangulation theorem.
For `p=4`, it gives a `10r` defect bound and at most `4t` local blocks for
clean quadrangulations.

## 1. Every short face is a reference face

Use darts `(u,v)` of `G`.  If `rho_v` is the cyclic order at `v`, the face
permutation is

```text
phi(u,v)=(v,rho_v(u)).
```

A face orbit is a closed non-backtracking walk: an immediate reversal would
make the local cyclic permutation at its middle vertex fix a neighbor, which
is impossible because every degree is at least three.  A closed
non-backtracking walk of length less than `p` contains a graph cycle of
length less than `p`.  The girth assumption therefore makes every face orbit
at least `p` long.

A face orbit of length exactly `p` cannot repeat a vertex, for the same
reason, and hence is a graph `p`-cycle.  By cleanliness it is a reference
face.  The two directions of a fixed `p`-cycle cannot both be face orbits:
at each of its vertices that would require both successor arrows `x->y` and
`y->x`, a proper two-cycle inside a single cyclic permutation of at least
three labels.  Thus the `p`-faces of any rotation system are distinct
reference faces, each with one of its two orientations.

Since `2|E|=pf`, every rotation system `R` satisfies

```text
p|F(R)| <= 2|E| = pf.
```

Euler's formula now gives `genus(R)>=h`.

## 2. Exact Euler defect

Suppose `R` has genus `h+r`.  Euler's formula gives

```text
|F(R)|=f-2r.
```

Exactly `f-t` of these faces are reference `p`-faces, so the number `b` of
remaining faces is

```text
b=(f-2r)-(f-t)=t-2r.
```

Counting the darts outside the retained `p`-faces gives

```text
sum_i ell_i = 2|E|-p(f-t)=pt.
```

Every remaining face has length at least `p+1`, by Section 1.  Consequently

```text
pt >= (p+1)(t-2r),
```

which is `t<=2(p+1)r`.  Subtracting the right side from the exact length sum
gives the last identity in (1).  If `r>0`, then `b>0`: otherwise `t=2r`
and the displayed length sum would give `pt=0`.  Hence `t>=2r+1`.

When `r=0`, the same argument forces `t=0`.  Every reference face survives.

## 3. Orientation propagation and the retained-dual bound

Give a surviving reference face sign `+` or `-` according as its direction
agrees with the fixed orientation of `T` or reverses it.  Two surviving faces
sharing an edge have the same sign.  Otherwise their face orbits would use
the same directed dart of that edge, although face orbits partition the
darts.  Thus the sign is constant on each component of the retained
face-adjacency dual.

The full dual is connected.  If `t=0`, it has one component, whose two signs
recover exactly the reference rotation system and its global reversal.
This proves `a_h(G)=2`.

Now let `t>0`, and let `C` be a nonempty component of retained faces.  Its
edge boundary is nonempty by dual connectivity.  Over `F_2` it is an even
subgraph of `G`, because it is the boundary of the two-chain formed by the
faces in `C`.  Every nonempty even subgraph contains a cycle, and girth `p`
therefore makes its boundary contain at least `p` edges.  Boundaries of
distinct retained components are edge-disjoint, and every boundary edge is
incident with a deleted face.  There are at most `pt` such incidences.  If
there are `c` retained components, then

```text
pc <= pt,
```

so `c<=t`.

## 4. Local path blocks and exact decoding

At a vertex `v`, an oriented retained face prescribes one successor arrow in
the cyclic order of the neighbors of `v`.  Exactly `deg(v)-k_v` reference
corners remain, hence that many arrows are prescribed.  Reject a proposed
component-sign assignment if the arrows are not an injective partial map or
contain a proper directed cycle.

If `k_v=0`, all labels form one directed cycle and the local rotation is
forced.  Otherwise an extendable partial map is a disjoint union of directed
paths, isolated labels included.  The number of paths is

```text
deg(v)-(deg(v)-k_v)=k_v.
```

Contracting each path to a labelled block shows that the extending cyclic
orders are in bijection with cyclic orders of the blocks, so there are
`(k_v-1)!` of them.  Because every deleted face is a simple `p`-cycle,

```text
sum_v k_v=pt.                                      (3)
```

The decoder in the theorem now follows.  Its final exact-missing-set test is
essential: omitting a reference-face constraint does not itself prevent that
face from reappearing after the local blocks are joined.  Every accepted
rotation has the requested genus and missing set.  Conversely, a target
rotation uniquely determines its missing set, retained-component signs, and
cyclic block orders, so it is produced exactly once.

## 5. Counting and running time

For fixed `S`, the component and local counts give at most

```text
2^t product_{v:k_v>0} (k_v-1)!                    (4)
```

candidates.  Here `0<=k_v<=t` and their sum is `pt`.  Put
`w(0)=w(1)=1` and `w(k)=(k-1)!` for `k>=2`.  If `1<=a<=b<t`, moving one unit
from `a` to `b` weakly increases `w(a)w(b)`: the ratio is `b/(a-1)` for
`a>=2`, and `b` for `a=1`.  Repeated transfers leave `p` entries equal to
`t` and all other positive entries equal to one or zero.  Therefore

```text
product_v (k_v-1)! <= ((t-1)!)^p.
```

Summing (4) over the allowed missing sets proves (2).  For fixed `p,r`,
generating constraints, extracting blocks, and tracing one rotation are all
linear in the input size; the other factors depend only on `p,r`.  Enumerating
at most `f^(2(p+1)r)` missing sets proves the stated running time.

## 6. Verification and scope

The exact checker uses the definition of a face permutation.  On the
tetrahedron (`p=3`) and cube (`p=4`) it:

- validates every clean-angulation hypothesis;
- enumerates every labelled orientable rotation system directly;
- reconstructs them independently from missing faces, component bits, and
  local path blocks;
- compares the two maps entry by entry, not only by aggregate counts; and
- checks (1), (3), and the defect bound for every rotation.

It also rejects a degree-two square, showing why the minimum-degree hypothesis
is explicit.  These finite tests corroborate the definitions and decoder;
they do not replace the all-parameter proof.

The result supplies a parameter-uniform obstruction and reconstruction theorem
for clean `p`-angulations.  It does not address embeddings whose short graph
cycles are nonfacial, nor does it prove log-concavity or unimodality.  The
constant `2(p+1)` is not claimed optimal for `p>3`.

## Primary context and novelty boundary

Bojan Mohar, *Strong log-convexity of genus sequences*,
[arXiv:2405.10854](https://arxiv.org/abs/2405.10854), uses unstable triangles
in counterexamples to genus-distribution log-concavity and asks for positive
structure around graphs that triangulate surfaces.  The triangular `8r`
face-defect theorem and its exact decoder were the direct graph-theoretic
input to the present generalization.

Targeted searches on 2026-09-21 for `p`-angulation or quadrangulation genus
distributions, missing-face bounds, and rotation-system reconstruction found
map-enumeration and special-family literature, but no statement matching
(1)--(3).  This is a bounded literature check, not an exclusive historical
priority claim.  Euler's formula, rotation systems, dual boundaries, and
local embedding completion are classical.
