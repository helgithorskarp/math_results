# A 26-versus-28 obstruction removes the ten-edge critical cell

In all seven surviving patterns of the hard-branch profile
`19^2 20^3 21^38`, the forced eight-vertex cell W **cannot have ten red
edges**. It must be one of the two remaining `(3,4;8)` types, with eleven
or twelve edges. The new mechanism is a local typed-extension bound:
**a fixed 13-vertex template permits at most 26 relevant outside vertices,
whereas the target patterns require 28**.

The underlying lemma applies to a Ramsey `(5,5)` graph of any order. It
does not require global degrees, deficiency caps, the two common-neighbor
vertices U, or a graph catalog. A hand proof is below. The small `(3,4;8)`
classification needed for the campaign corollary is independently enumerated.

No whole profile is excluded. All seven patterns still have exact integer
witnesses for the preceding aggregate edge relaxation plus the new bound
`11<=e_R(W)<=12`. Those witnesses are not graph realizations. The inherited
global totals **67 profiles / 273 anchored splits** are unchanged. No
43-vertex target graph or improved Ramsey lower bound is claimed.

## 1. The template and localized theorem

Let G have no red or blue K5. Suppose it contains disjoint sets

```text
R = {0,1},       L = {2,3,4},       W = {w0,...,w7}.
```

The edge `01` is red; within L, `23,24` are red and `34` is blue.
Every L--W edge is red, and every R--W edge is blue. The six R--L
edges are arbitrary. Inside W the red edges are exactly

```text
high C4:       w0w2, w0w3, w1w2, w1w3;
spokes:        w0w4, w1w5, w2w6, w3w7;
low matching:  w4w5, w6w7.
```

Thus W is the ten-edge triangle-free eight-vertex graph with independence
number three. Let X be any set outside this 13-vertex core such that every
`v in X` has exactly one red neighbor in R and exactly one in L. There are
six possible types `{0,i}` or `{1,i}`, `i in {2,3,4}`; no assumption is
made about their multiplicities or the edges inside X.

**Lemma. `3|X|<=80`, hence `|X|<=26`.**

The bound is not claimed optimal or attained. Vertices outside the core
and X may exist; ignoring them only weakens the upper bounds below.

## 2. A pointwise eight-bit inequality

For `v in X`, let `T={j: vw_j is red}`. Its blue neighbors in W cannot
contain an independent triple: together with v and its unique blue
neighbor in R, such a triple would form a blue K5. Thus `W\T` has no
independent triple.

Give weight one to each spoke of W and weight two to each low matching
edge. The high C4 edges have weight zero. Define

```text
A(T) = 1[{0,4} subset T] + 1[{1,5} subset T]
     + 1[{2,6} subset T] + 1[{3,7} subset T]
     + 2*1[{4,5} subset T] + 2*1[{6,7} subset T],

B(T) = sum_(a in {4,5}, b in {6,7}) 1[a,b not in T].
```

Then

```text
A(T)+B(T) >= 3.                                            (1)
```

Here is a short case proof, rather than a reliance on an LP separator.
Put `l=|T intersect {4,5}|`, `r=|T intersect {6,7}|`. The low matching
and B already contribute

```text
g(l,r)=2*1[l=2]+2*1[r=2]+(2-l)(2-r).
```

Swapping the two low pairs, or swapping both endpoints of a low edge and
their attached high vertices, preserves this explicit W. These relabelings
reduce the nine pairs `(l,r)` to the six cases below. They are not
automorphism assumptions on G.

| `(l,r)` | Normalized low part of T | `g(l,r)` | Independent triples forcing counted spokes |
|---|---|---:|---|
| `(0,0)` | empty | 4 | none needed |
| `(0,1)` | `{6}` | 2 | `{2,4,7}` forces `2 in T`, so spoke `2--6` counts |
| `(0,2)` | `{6,7}` | 2 | `{2,3,4}` forces 2 or 3 into T |
| `(1,1)` | `{4,6}` | 1 | `{0,5,7}` and `{2,5,7}` force both 0 and 2 into T |
| `(1,2)` | `{4,6,7}` | 2 | `{2,3,5}` forces 2 or 3 into T |
| `(2,2)` | `{4,5,6,7}` | 4 | none needed |

Each listed triple is independent in W. Since it cannot be contained in
`W\T`, the asserted high vertices must lie in T. The required one or two
spokes complete (1).

## 3. Sum only 26 root inequalities

The common neighborhood, in its own color, of a monochromatic triangle
has at most four vertices. Any edge of the same color inside it would
give a K5 with the triangle; therefore it is a clique in the other color,
also of order at most four. This is just `R(2,5)=R(5,2)=5`.

For the B contribution, take each of the eight blue root triangles

```text
{r,w_a,w_b},       r in R, a in {4,5}, b in {6,7}.
```

Exactly two vertices of the fixed core already lie in its blue common
neighborhood: the two high W vertices not attached to `w_a,w_b`.
Consequently at most two vertices of X can join each such common
neighborhood. Every v in X is counted only with its unique blue R root.
It follows that

```text
sum_(v in X) B(T_v) <= 8*2 = 16.                           (2)
```

For A, take each red root triangle `{i,w_a,w_b}`, where `i in L` and
`w_aw_b` is one of the four spokes or two low matching edges. Use the
weights in A. The weights sum to eight for each i. Because W is
triangle-free, no W vertex is a red common neighbor of a W edge.
The fixed red common neighbors are precisely L's red neighbors of i:
two for i=2, and one for each of i=3,4. Thus the outside capacities are
respectively two, three, three. Since every vertex of X is red to
exactly one L vertex,

```text
sum_(v in X) A(T_v) <= 8*2 + 8*3 + 8*3 = 64.               (3)
```

Combining (1)--(3) gives `3|X|<=16+64=80`. The arbitrary R--L edges
never enter this argument. This proves the localized lemma with no
degree, density, solver, or enumeration assumption.

## 4. Application to the seven M=217 patterns

The preceding [paired-neighborhood reduction](../ramsey_r55_paired_neighborhood_budget/README.md)
supplies the exceptional core with red edges

```text
01,02,04,12,13,23,24
```

and central cells U, W, `A_i`, `B_i`. A cell label lists its red
exceptional neighbors:

```text
U={0,1}: size 2;                W={2,3,4}: size 8;
A_i={0,i}, B_i={1,i}: i=2,3,4.
```

The six A/B cells have total size 28, in each of the seven possible
incidence patterns. Their internal edges have not been fixed.
The W cell has no red triangle, since vertices 2 and 3 are adjacent
red roots common to all of W. It has no blue K4, since all of W is
blue to 0. Hence it is a `(3,4;8)` graph.

There are three such graphs up to relabeling, with 10, 11, and 12 edges.
If W had ten edges, normalize it to the template above; its joins to
the exceptional core are uniform, so this permutation loses no graph.
The union of the A/B cells would give `|X|=28`, contradicting `84<=80`.
Therefore

```text
W is the 11-edge or the 12-edge critical type; e_R(W)>=11.  (4)
```

This excludes one W type uniformly across all seven patterns, not one
entire pattern or profile. Counting pattern/type templates without the
parent's relabeling quotient changes 21 candidates to 14. These are
structural templates, not realized graphs or completed solver leaves.
Nothing here reopens the symmetry or catalog-radius lanes, and the
M=214 whole-stratum encoding belongs to a different profile.

### Scope of the revised positive witnesses

[EDGE_WITNESSES.json](EDGE_WITNESSES.json) contains seven integer vectors
in exactly the parent cell-pair order. They satisfy all 153 two-sided
parent aggregate rows and their boxes, plus `11<=e_WW<=12`.
Five old witnesses already satisfied (4); those for `(4,2,8)` and
`(5,2,7)` had `e_WW=10` and have been replaced by checked vectors.

These revised vectors do **not** certify a compatible critical W graph,
individual edge realization, the full 13-core union-cut relaxation,
or any central vertex's prescribed triangle count. They establish
only that adding the scalar consequence (4) to the documented parent
relaxation does not yet eliminate a pattern. The two surviving actual
W types remain the next feasibility boundary.

## 5. Independent finite checks and provenance

[verify.py](verify.py) uses Python's standard library and explicit
exceptions, so its checks remain active under `python3 -O`.

- Vertex augmentation enumerates all labeled `(3,4)` graphs through
  order eight. A new vertex must have an independent red neighborhood
  of size at most three, meeting every independent triple of the old
  graph. These conditions are necessary and sufficient; deleting the
  last vertex proves complete labeled coverage by induction.
- A separate full edge-bit enumeration through order six compares
  complete graph sets, not only counts (33,868 graph assignments).
- At order eight, all 17,640 graphs split into three disjoint full
  permutation orbits of sizes 5,040, 10,080, 2,520. Their edge counts
  are 10, 11, 12 and automorphism orders 8, 4, 16. The natural ten-edge
  template is explicitly matched to its full orbit.
- All 256 W-neighborhood masks are tested; precisely 113 satisfy the
  no-independent-triple condition, and all satisfy (1).
- Every one of the 64 arbitrary R--L cross-link choices is checked.
  All 26 root capacities are reconstructed from literal common neighbors.
  All 43,392 allowed typed single-vertex extensions are independently
  tested against actual monochromatic four-cliques in the 13-core,
  and their root-weight scores agree with the hand formula.
- The complete parent verifier is replayed, its source hash is pinned,
  and all seven adjusted integer witnesses are checked exactly.
  Four negative tests reject a weakened pointwise certificate, a
  non-blue root, a forbidden blue triple, and an altered W graph.

The small three-type classification is classical, not a novelty claim.
For an external comparison, [McKay's Ramsey graph catalog](https://users.cecs.anu.edu.au/~bdm/data/ramsey.html)
lists the three eight-vertex graphs. Its exact
[r34_8.g6](https://users.cecs.anu.edu.au/~bdm/data/r34_8.g6) is retained
here as a 21-byte comparison fixture, SHA256
`3068e421da9548f92c0c16196d8dc8f032eb83401716b01d96de8025a9614798`.
The checker decodes its three entries and matches each to an enumerated
orbit. Catalog completeness is **not needed**: the local augmentation
proves the full small classification independently.

The M=217 application inherits the parent core/profile reduction and its
reviewed local-extremal inputs. The parent artifact itself has not been
independently peer reviewed as of this pass; replay is internal checking,
not independent review. The localized lemma needs none of these inputs.
Its proof and the new checker are unformalized and not peer reviewed.
Ordinary exact Python execution, the displayed induction/orbit coverage,
and runtime/hardware remain computational trust boundaries.

Exploratory signature LPs suggested the obstruction. Their exact separator
simplified to the 26 root inequalities and the hand argument above; no
infeasibility status or opaque solver trace is used as proof. Tests of the
eleven- and twelve-edge signature relaxations supplied no exclusion and
are not presented as graph-feasibility evidence.

## Reproduction and pass boundary

From this directory, using Python 3.11.2 and the repository's pinned
parent artifacts:

```bash
python3 verify.py --report /tmp/r55_ten_edge_report.json
cmp report.json /tmp/r55_ten_edge_report.json
python3 -O verify.py --report /tmp/r55_ten_edge_optimized.json
cmp report.json /tmp/r55_ten_edge_optimized.json
sha256sum -c SHA256SUMS
```

Compare stdout with [EXPECTED_OUTPUT.txt](EXPECTED_OUTPUT.txt). The verifier
requires no solver and no network connection. The final replay took
8.373 seconds with 23,328 KiB peak resident memory on the research host;
no large generated file is needed.

Optional bounded discovery of replacement aggregate witnesses uses
`requirements-discovery.txt` (NumPy 2.2.6, SciPy 1.15.3 with its bundled
HiGHS). Run `python3 find_witnesses.py` in that environment and check any
saved JSON with `verify.py --edge-witnesses PATH`. Only the two obsolete
witnesses are regenerated, with at most 20 seconds per case; a missing
exact-checked primal aborts. The reference positive witnesses already
make these numerical dependencies unnecessary for verification.

This completes the ten-edge W obstruction. Preserve both remaining W
types and the seven patterns; pursue their actual extension/triangle
compatibility in the next pass, not as another phase of this one.
