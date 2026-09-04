# Reviewed dependency chain for Albertson's conjecture at `r=27`

This package consolidates the now-reviewed campaign argument into one
reader-facing proof and pins every imported campaign artifact and review by
an exact Git commit, Discovery Net contribution, and source-file hash.

> **Theorem.** Every graph of chromatic number 27 has crossing number at
> least that of `K_27`.

The proof uses four primary-source inputs at the exact versions recorded in
[`dependency_manifest.json`](dependency_manifest.json): Sadhu's finite
frontier, the Büngener--Kaufmann crossing and forbidden-configuration bounds,
the Pach--Radoicic--Tardos--Toth inequality with its equality induction, and
Ackerman's simple 4-planar density theorem. The new terminal-triangulation
step has two independent high-confidence reviews on Discovery Net; neither
review found a mathematical gap.

## 1. The four-row frontier

Sadhu's `r=27` reduction says that a counterexample can survive only in the
four order/size rows

```text
(53,713), (53,714), (53,715), (54,726).
```

The standard drawing number is

```text
Z(27) = floor(27/2) floor(26/2) floor(25/2) floor(24/2) / 4
      = 6084,
```

and `cr(K_27)<=Z(27)`. It therefore suffices to prove crossing number at
least 6084 in every frontier row.

Two reviewed exact induced-sampling certificates already give

```text
cr(54,726) >= 6084,
cr(53,714) >= 6100,
cr(53,715) >= 6129.
```

Only `(53,713)` remains.

## 2. Reduction of the last row to `cr(24,132)>=165`

Assume temporarily that every 24-vertex, 132-edge simple graph has crossing
number at least 165. The rounded Büngener--Kaufmann `37/9` bound below 132
edges and Ackerman deletion above 132 edges extend this point to

```text
cr(H) >= 5|E(H)|-495
```

for every 24-vertex simple graph `H`.

Close the universal integer crossing tables under convex induced sampling.
The exact table at order 52 has the pointwise supporting line

```text
5 F_52(q) >= 136q-65166.
```

For a 53-vertex, 713-edge graph, sum this line over all 53 vertex deletions.
Every crossing survives 49 deletions and the edge counts sum to 36363, so

```text
49 cr(G) >= (136*36363-53*65166)/5
           = 298314
           = 49*6088+2.
```

Thus `cr(G)>=6089`. The conditional propagation and an independent QuickHull
reconstruction both emit table digest
`79e615e691c84d697b2dbc3d6fded0d9657c37d3f91f4bebc1a61097fb39f7f6`.

## 3. The two equality profiles on 24 vertices

Suppose instead that a 24-vertex, 132-edge graph has a good drawing with at
most 164 crossings. The reviewed deletion-profile enumeration leaves exactly

| row | `e(D2)` | `x(D2)` | `Delta` | `m0` | full pentagons | crossing `C5`s |
|---|---:|---:|---:|---:|---:|---:|
| A | 103 | 57 | 0 | 0 | 9 | 10 |
| B | 106 | 64 | 0 | 0 | 11 | 12 |

Here `D2` is 2-planar and its edge-crossing graph consists only of `C5` and
`K2` components. In either row exactly one crossing `C5` is not a full
2-planar pentagon. The exact definition of `m0` is the number of absent
crossing-free boundary edges of the forbidden configurations, so `m0=0`
means that every boundary edge of each already-full pentagon is present.

## 4. Global terminal triangulation

In every crossing cycle label the edges

```text
b -- a -- c -- d -- f -- b
```

and delete `b,c`. The edge `a` becomes free and `d,f` retain one crossing.
After doing this in every `C5`, the terminal good 1-planar drawing `T` has

| row | `e(T)` | `x(T)` | `x(T)-e(T)+3(24-2)` |
|---|---:|---:|---:|
| A | 83 | 17 | 0 |
| B | 82 | 16 | 0 |

Its planarization `P(T)` is simple: original edges are simple, every good
crossing has four distinct endpoints, and 1-planarity prevents a segment
between two crossing vertices. Since

```text
|E(P(T))| = e(T)+2x(T) = 3(24+x(T))-6,
```

the planar inequality forces connectedness as well as equality in every
face. Hence `P(T)` is a plane triangulation globally, without any appeal to a
block-local face surviving reassembly.

## 5. The five-face disk

Select the unique non-full component, write `a=zw`, and let `x` be the
terminal crossing of `d,f`. The segment of the deleted arc `c` between its
crossings with `a` and `d` lies in a triangular face. Therefore `a` and the
relevant planarized segment of `d` share an original endpoint. Relabel so

```text
d=zr,   f=wt,
```

with kite rotation `(z,w,r,t)` around `x`. Tracing the two deleted arcs
through adjacent triangular faces forces

```text
c=ut,   b=ur.
```

The oriented local map is

```text
             u
            / \
           z---w
           |\x/|
           |/ \|
           t---r
```

with five triangular faces

```text
uzw, zwx, ztx, trx, rwx.
```

Opposite orientations cancel on every internal edge. The remaining boundary
is the simple cycle `u-z-t-r-w-u`; the complex has six vertices, ten edges,
five faces, Euler characteristic one, an interval link at each boundary
vertex, and a circular link at `x`. Thus it is a combinatorial disk. These
checks are encoded independently in
[`rotation_system.json`](rotation_system.json).

The five original crossing edges reconstructed from the terminal map are

```text
zw, ur, ut, zr, wt,
```

exactly the complementary diagonals of that boundary in `K5`. The vertices
are distinct: the terminal crossing has four distinct endpoints; `u` cannot
be `z` or `w` because `b,c` cross `a`; and `u=r` or `u=t` would make `b` or
`c` a loop.

It remains only to check provenance of the five outer sides. Every other
crossing `C5` is a full pentagon, and `m0=0` supplies its entire uncrossed
boundary. The five diagonals and boundary form a vertex-empty drawn `K5`.
Its disk is sealed: its diagonals already have two crossings, its boundary
is uncrossed, and simplicity leaves no unused pair of boundary vertices.
Therefore a survivor freed in another component remains inside that disk and
cannot be one of the exceptional disk's outer sides. All five sides were
already crossing-free in `D2`.

The exceptional component is consequently a full pentagon as well. This
contradicts `10=9+1` in row A and `12=11+1` in row B. Hence

```text
cr(24,132) >= 165.
```

Section 2 now gives `cr(53,713)>=6089`; together with the other three row
bounds in Section 1, this proves the theorem.

## 6. Reproduction and trust boundary

Run the compact manifest, local-map, and arithmetic audit with CPython 3.9
or later; there are no third-party Python dependencies:

```sh
PYTHONDONTWRITEBYTECODE=1 python3 verify_chain.py
PYTHONDONTWRITEBYTECODE=1 python3 -m unittest -v test_verify_chain.py
PYTHONDONTWRITEBYTECODE=1 python3 verify_git_history.py
PYTHONDONTWRITEBYTECODE=1 python3 -m unittest -v test_verify_git_history.py
```

The exact six-line mathematical-checker transcript is in
[`EXPECTED_OUTPUT.txt`](EXPECTED_OUTPUT.txt); its final certificate digest is

```text
1d21c61a84c4357c1062d60a105d99284195c7235e1e5b2a79dbef0a128a8be2
```

The history checker requires a full Git checkout. It independently reads each
of the 18 pinned files from the recorded source commit, compares both that Git
object and the working-tree copy to the manifest hash, verifies every recorded
commit object, and checks that each of the five review commits descends from
its source. Its exact transcript is in
[`EXPECTED_HISTORY_OUTPUT.txt`](EXPECTED_HISTORY_OUTPUT.txt), with digest

```text
c421c281d6b37b91a95015cf1b48f2aeeee5632ba5ba04fc20d6659a982517cb
```

The checker verifies all pinned source hashes, graph-reference syntax, the
oriented five-face disk including every vertex link, both terminal profiles,
the exact planarization triples `(vertices,edges,faces)=(41,117,78)` and
`(40,114,76)`, all four frontier floors, and `Z(27)=6084`. The longer source
verifiers remain the authorities for the exhaustive profile enumeration and
recursive convex tables; their exact commands and commits are in the manifest.

The mathematical trust boundary consists of the four versioned primary
results, standard good-drawing normalization, the reviewed PRTT equality
classification, convex induced sampling, and the Jordan-curve interpretation
of the oriented local map. The executable uses only exact CPython integers,
`Fraction`, finite sets, JSON, and SHA-256. It uses no floating point, solver,
randomness, network input, or uncommitted data. The separate provenance audit
also trusts the installed Git executable and the completeness of the local
repository history.

## 7. Post-review Lean assurance

The separate
[`albertson_r27_terminal_map_lean`](../albertson_r27_terminal_map_lean/README.md)
package now kernel-checks two layers that the historical manifest originally
left to finite Python computations and a general combinatorial-disk
recognition:

- a universal exhaustion of the complete nonnegative deletion-profile system,
  proving that every feasible record is exactly row A or row B; and
- a constructive shelling of the five oriented triangles, with every shared
  edge, shared vertex, attachment arc, and intermediate boundary computed
  from the face list.

The assurance version used here is immutable commit
[`2675bc9a4cba87b1375533a44746ad096378ba38`](https://github.com/helgithorskarp/math_results/tree/2675bc9a4cba87b1375533a44746ad096378ba38/graph_theory/albertson_r27_terminal_map_lean),
whose Lean source has SHA-256
`dbb5ff53c6a89419a35edc412ecdb6c57bfae36dfcce51a077cf737fb5bc2539`.
This is post-review evidence and does not change any source or review object
pinned by `dependency_manifest.json`. Its trust boundary remains explicit: it
assumes the mapping from the cited drawing inequalities to the encoded integer
system, the geometric derivation of the five-face list, and the elementary
topological lemma that a triangle glued to a disk along an exact connected
proper boundary arc preserves a disk.

The terminal closure has independent `VERIFIES`/`REPRODUCES` reviews at
Discovery Net heights 2025 and 2027. This establishes a reviewed mathematical
chain under the stated imported results; it is not a literature-wide priority
claim. The remaining proof-assistant frontier is the geometric face trace,
sealed-region provenance, the standard triangle-gluing lemma, and the imported
primary drawing theorems rather than the finite profile exhaustion or local
five-face incidence.
