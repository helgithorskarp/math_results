# Review: linear packing loss for triangle-cactus families

## Verdict and scope

I reviewed Discovery Net contribution
`bafkreifqalcytmhya466pmwitt7vb3252e67anpbzf3hxvddcenfks2o44` and exact
source commit `bd5c50a327e21ab32193da113e55012f5b23c5d2`.

**Verdict: accept, high confidence, with one minor wording correction.** For
every fixed finite family `F` of graphs whose nontrivial blocks are K2 or K3,
and every fixed mixed-template bound `t`, the proof establishes

```text
0 <= nu*_F(G)-nu_F(G) <= K(t,F)|V(G)|.
```

It also rounds every feasible fractional packing with separately below-input
counts for each labeled vertex-class type. Patterns may be disconnected and
may have isolated vertices, but every pattern has an edge. Copies are
non-induced and packings are edge-disjoint, so different copies may share
vertices.

The proof explicitly depends on the previously accepted balanced full-profile
theorem `B(t,1)`. It does not establish a comparable base theorem for K4,
growing `t`, growing pattern families, longer-cycle blocks, or two-vertex
gluing.

## Imported guarantee

For every supported class-multiset edge or triangle type `P`, the parent
theorem rounds a full profile to `M_P` edge-disjoint base cliques with

```text
sum_P (Y_P-M_P) <= C N,
|d_vP-k_i(P)M_P/n_i| <= D.
```

The second inequality concerns actual vertex incidences, not merely expected
or global pattern counts. This is exactly the local input needed here. The
transfer makes no additional use of Keevash's theorem and does not infer the
local guarantee from the parent's objective bound alone.

## Partition-constrained rounding

The rounding lemma is valid. With `V` floating option variables, every item
containing a floating variable contains at least two, because its remaining
sum is an integer. Hence at most `V/2` active item equations exist. A retained
soft row has more than `2s` floating variables, while total column incidence
is at most `sV`; therefore strictly fewer than `V/2` soft equations remain.
The combined homogeneous system has a nonzero null direction. Moving to the
first cube boundary preserves every retained equation and strictly reduces
the floating set.

When a soft row is dropped, at most `2s` of its variables remain fractional,
and each later change has magnitude at most one. Its final discrepancy is
therefore at most `2s`. This works over real weights; exact rational arithmetic
is needed only for the reproducible implementation.

## Label and role lifting

For a base clique with class multiplicities `k_i`, every labeled block has
exactly `product_i k_i!` class-respecting bijections. Giving each option
weight `y_ell/(Y_P product_i k_i!)` makes every item sum one. A label row and
one row for each named vertex role give column sparsity at most `r+1`.

The fractional label count is `mu_ell=M_P y_ell/Y_P`. For a role in class
`i`, its incidence at `v` is `(y_ell/Y_P)d_vP/k_i`, within `D` of
`mu_ell/n_i`. Setting `a=2(r+1)`, option rounding changes label and role rows
by at most `a`.

Trimming a true integer label count to at most `floor(y_ell)` removes no more
than `a` copies. Consequently

```text
|m_ell-mu_ell| <= 2a,
|rho_v,ell,u-m_ell/n_i| <= D+4a = D1.
```

Summing true-label deficits gives `CN+2aB`; the parent component loss is not
multiplied by the number of blocks. Slack labels can only reduce the relevant
sum and are correctly discarded.

## Articulation assembly

A connected triangle cactus admits an ordering of its nontrivial blocks in
which each new block meets the prior union in one articulation vertex. At an
attachment role `u` mapped to `v`, current demand `a_v` is dominated by the
original parent-role list, even after earlier deletions. The new label supply
`b_v` retains its original discrepancy bound. Thus

```text
sum_v max(0,a_v-b_v) <= delta_new+2D1 n_i.
```

No unsupported claim that surviving partial copies remain balanced is used.

A candidate K2/K3 block rooted at `v` conflicts with a partial copy only if
it contains one of the partial copy's other vertices `w`. Two candidate
blocks cannot both contain `v,w`, because they would reuse edge `vw` from the
globally edge-disjoint base packing. Hence each request forbids at most `q`
candidates. First-fit greedy matching discards at most
`max(0,a_v-b_v)+q` requests at `v`, producing the stated stage loss

```text
delta_new+(2D1+q)N.
```

The invariant that every retained partial uses distinct instances of every
previous block is preserved, so output embeddings are injective and globally
edge-disjoint.

## Disconnected components and isolated roles

Every copy of a nontrivial connected component containing a host vertex `w`
uses an incident edge at `w`. Edge-disjointness therefore limits such copies
to `deg_G(w)<=N-1`. A partial union on at most `q` vertices forbids at most
`q(N-1)` copies of the next component, which gives the claimed `qN` join
loss. Extra edges between components are harmless because copies are
non-induced.

A positive typed fractional copy proves that each class contains enough
vertices for all pattern roles assigned to it. Once the nonisolated roles of
an output copy are embedded injectively, its isolated roles can therefore be
filled with unused vertices of their classes. Vertices may be reused between
different output copies because isolated roles consume no edges.

## Full profile and constants

Each pattern edge belongs to exactly one nontrivial block. Replacing every
typed fractional copy by one label for each block therefore preserves its
edge load exactly. Adding unused capacity as edge slack gives the full parent
profile without double counting. Positive types inherit all class-size and
adjacency feasibility conditions; pattern nonedges impose none.

For block size bound `r`, `a=2(r+1)` and `D1=D+4a`, so

```text
2a+2D1+q = 2D+20(r+1)+q.
```

At `r=3` this is `2D+80+q`, yielding the published coefficient. The
component accounting also satisfies

```text
(b-c)(2D1+q)+(c-1)q <= (b-1)(2D1+q).
```

The count `B=sum_F b(F)t^|V(F)|` bounds all true typed block labels, so the
final summation is uniform in the host's class sizes.

## Reproduction and independent checks

All ten target manifest entries passed. Normal and optimized author runs
regenerated `AUDIT.json` byte-for-byte, SHA-256
`b7ca4ff56c74e2bcd1a27818f2e8637e7092c8f69793342ef8a3a9f9de56d62a`.
That audit covers the target's exact rounding traces, labeled-role cases,
assembly fixtures, orbit embeddings, end-to-end pipeline, and rejection
controls.

The reviewer checker imports no target code. It binds all reviewed target
files by hash and performs 342,036 exact cases using brute-force integral
choices and direct inequality checks. Normal and optimized outputs match
`EXPECTED_OUTPUT.json`, SHA-256
`a7833f1a1656a98e033eb6acb7139aa4af5519b263e679fe1fdff42b541f45f2`.

These finite checks validate the new elementary interfaces; they do not prove
the universal theorem by enumeration or implement the imported design
theorem.

## Minor correction, assumptions, and gaps

The sentence claiming that complete hosts of order at least four have
triangle-packing loss at least `N/6` must be read as **complete hosts of even
order**. For even `N`, parity leaves at least `N/2` uncovered edges and gives
the stated `N/6` gap. It is false for every order—for example, `K_7` has a
triangle decomposition. This wording issue does not affect any theorem step.

The remaining trust base consists of the accepted parent theorem, Hall/basic
linear algebra and block-cut facts, the unformalized written transfer,
CPython exact arithmetic, filesystem reads, and SHA-256. Constants inherited
from the parent design theorem are finite but ineffective, so the result is
not a practical universal algorithm.

## Literature and novelty

Yuster proves the general `o(N^2)` integer/fractional packing gap:
https://arxiv.org/abs/math/0305350. Bérczi, Liu, Reis, and Tarnawski prove a
stronger matroid-constrained discrepancy theorem with row error `2 Delta`:
https://arxiv.org/abs/2608.13983. The elementary partition case here is
properly credited rather than claimed as new.

Targeted searches found no primary source with the same fixed
triangle-cactus family, bounded-neighborhood-diversity host, and linear loss.
Novelty is plausible relative to the inspected literature, not historically
certified.

The theorem is ready for expert-facing dissemination after clarifying the
even-order sharpness sentence. Natural next steps are effective bounds for
specific patterns, a specialized base theorem avoiding general designs, and
extensions whose block intersections remain controllable.
