# Cell-preserving switches and a certified strict-descent barrier

## General switch lemma

Fix an exceptional vertex set E, fix every edge incident with E, and let
C be the remaining vertices. Partition C by the red signature
`X_v=N_R(v) intersect E`. Write `z_XY` for the number of red edges between
signature cells X,Y, counting internal cell edges once.

Let a,b,c,d be distinct vertices of C. Suppose ac and bd are red, ad and bc
are blue, and `X_a=X_b`. Change the colors of precisely those four edges.

1. Every individual degree and every fixed exceptional incidence is unchanged.
2. Every z_XY is unchanged: the removed ac edge has the same cell pair as the
   added bc edge, and removed bd has the same cell pair as added ad.
3. Both exceptional local edge counts are unchanged. Directly, an exceptional
   red neighborhood includes a exactly when it includes b; its net edge
   change is `(1[a in N]-1[b in N])*(1[d in N]-1[c in N])=0`. The same
   argument applies to blue neighborhoods and blue edges.
4. For every union S of signature cells together with fixed exceptional
   vertices, the red degree into S of any vertex other than a,b is unchanged.
   At c,d the exchanged vertices a,b either both belong to S or both do not;
   all other rows are untouched. At a the change is `1[d in S]-1[c in S]`,
   and at b it is the negative. Blue degrees behave oppositely.

Thus previously satisfied aggregate constraints in the fixed core, signature
multiplicities and z_XY remain satisfied. This does NOT automatically preserve
pointwise bounds at a,b, local counts at central vertices, or mixed K5s.
Those are checked separately, not inferred from the aggregate invariants.

### Exact characterization of four-edge edits

Every nonempty four-edge color change that preserves all individual degrees
is an alternating four-cycle: two disjoint red edges are removed and two
disjoint blue edges on the same four vertices are added. In the notation
above, preserving the multiset of signature-cell pairs is equivalent to

```text
X_a=X_b or X_c=X_d.
```

For necessity, the removed cell pair `{X_a,X_c}` must equal one of the added
pairs `{X_a,X_d}` or `{X_b,X_c}`. Equality with the first gives X_c=X_d;
equality with the second gives X_a=X_b. Sufficiency follows by pairing the
removed and added edges as in item 2. Reorienting the four-cycle handles the
second case. Hence enumerating opposite same-cell pairs a,b covers ALL
central four-edge degree-and-quota-preserving edits, not just a subclass.

The search enumerates those opposite pairs and their distinct-color neighbor
differences. The verifier instead enumerates all `binom(40,4)=91,390` four-sets,
the three pairs of perfect matchings on each, and literal cell-quota equality.
Their complete endpoint support sets agree entry for entry.

## Local-triangle update formula

Write x_uv for the old red edge bit and `Q={a,b,c,d}`. No triple inside Q is
monochromatic red before or after an alternating switch: each contains one
red and one blue edge of the changed cycle. For a vertex u outside Q,

```text
Delta t_R(u) = (x_ua-x_ub)(x_ud-x_uc).
```

Indeed, its four potentially changed triangles give
`x_ua*x_ud+x_ub*x_uc-x_ua*x_uc-x_ub*x_ud`. For endpoints the formulas are

```text
Delta t_R(a) = sum_(u outside Q) x_ua (x_ud-x_uc),
Delta t_R(b) = sum_(u outside Q) x_ub (x_uc-x_ud),
Delta t_R(c) = sum_(u outside Q) x_uc (x_ub-x_ua),
Delta t_R(d) = sum_(u outside Q) x_ud (x_ua-x_ub).
```

These identities give an O(|V|) exact score update. The verifier does not use
them: it enumerates every triple containing at least one changed edge and
compares its three literal colors before and after the edit.

## Mixed-clique and pointwise gates

Assume initially that no monochromatic K5 meets E. Any newly forbidden K5
must contain a changed edge uv and an exceptional vertex. For each of the
four changed central edges in its NEW color, it suffices to check for a
same-color triangle in the common neighborhood of u,v that meets E.

The search chooses its exceptional vertex first and checks for an edge in
the remaining common set with bitsets. The verifier enumerates literal
three-subsets of the common set and records an actual five-set whenever the
gate fails. During the path replay it additionally enumerates all same-color
four-sets in each exceptional color neighborhood, without an incremental
assumption. Exhaustive endpoint K5 checking uses two independent algorithms
in the pinned predecessor graph verifier.

For pointwise constraints, let A,B be disjoint red/blue cliques in E and
let S be the vertices outside the roots that are red to A and blue to B.
The retained root bounds are

```text
u red to A  => d_R(u,S) <= U(4-|A|,5-|B|)-1,
u blue to B => d_B(u,S) <= U(5-|A|,4-|B|)-1.
```

Here U is the elementary parity-refined Ramsey recurrence from the parent.
Root membership and S are fixed throughout the path. The search checks just
the potentially changed rows at a,b. The verifier independently expands and
checks ALL 884 literal inequalities, without merging rows or using locality.

## The fixed target-specific experiment

Use the explicit predecessor graph, SHA256
`a57fc26ea50196d82537220cf057c659860f9842dd35351d33445781f019eae5`.
Its exceptional red triangle E={0,1,2} has degree20, and all40 central vertices
have degree21. Signature multiplicities in mask order0..7 are
`(0,8,8,6,10,4,4,0)`. All exceptional local profiles are (92,107).

This graph has450 red edges. The elementary neighborhood identity gives

```text
t_R(v)+t_B(v) = 201-|X_v|       (v in C).
```

Consequently the hard-branch central caps t_R,t_B<=100 are equivalent to
`101-|X_v| <= t_R(v) <= 100`. Define the nonnegative integer objective

```text
Phi(G) = sum_(v in C) max(0, t_R(v)-100, 101-|X_v|-t_R(v)).
```

The interpretation of these caps uses the earlier local-extremal hard-branch
reduction and its catalog boundary. The present exact graph and local-neighbor
claims can instead be read with Phi simply as the displayed integer function;
their verification needs no Ramsey catalog or SAT solver.

Best strict descent, breaking ties by the deterministic generator order,
takes twelve admissible switches. All signatures, degrees, z_XY, exceptional
profiles, mixed-K5 constraints, and pointwise root bounds hold throughout:

```text
Phi: 143,133,125,118,112,108,102,98,95,92,89,86,83.
```

The endpoint is GRAPH.json, SHA256
`7a832f229bb3fd97f5c3e5dceb060988fb5c5d2df074d1cb37ddbb1dcd5fc8a6`.
PATH.json provides all twelve switches and the discovery census. The independent
verifier proves the path invariants and endpoint; optimal tie-breaking at
every intermediate step is not needed for the theorem.

## Complete one-switch boundary

The endpoint has 11,453 central four-edge degree-and-quota-preserving edits.
Exactly 2,855 would strictly decrease Phi without the extra gates:

- 618 fail a pointwise root bound;
- all remaining 2,237 create a monochromatic K5 meeting E.

Thus NONE is an admissible strict improvement. Checking every edit, including
nondecreasing ones, leaves 193 admissible neighbors: four are neutral and 189
increase Phi. Failure counts use pointwise-first classification:1,640 fail
that gate, and 9,620 of the rest fail the mixed-K5 gate. Counts can overlap
under a different gate ordering; the displayed partition is explicit.

The four neutral supports are listed in report.json. They have not been
traversed and their plateau component has NOT been exhausted. This is a
local minimum allowing ties, NOT a strict local minimum, an isolated graph,
or a global minimum over its fiber. Another path, a neutral step, an uphill
step, a larger simultaneous edit, or changing cell quotas may escape.

The two literal move constructions agree on every support; canonical support
SHA256 is `f535ee2f32db29900550ffc1767bb43cfe6ad4f1da7c35d2a3a655806ded77f7`.
An exact sorted classification with an explicit failed root row or five-set
for each rejected move has SHA256
`3b7c7ad0819528559b444f64e4e31d4019ae99a8a0ac4fadca13234cf8c54846`.
The small verifier regenerates it; the large per-move list is not published.
These hashes are provenance, not substitute certificates.

## Scope and novelty

The endpoint is NOT a Ramsey(5,5;43) graph. It still has 240 red and 252 blue
central K5s and 29 central local-cap failures. Its exceptional neighborhoods
also retain opposite-color K5s. No whole profile, any of the470 retained
signature cases, or any SAT formula has been excluded. Global counts remain
66 profiles/271 anchored splits. In particular this fixed-z boundary does not
settle the earlier, less restrictive central-profile SAT checkpoint.

Restricted switches are standard; see [Czabarka et al., On Realizations of a
Joint Degree Matrix](https://arxiv.org/abs/1302.3548). Fixed partition quotas
are also studied in the [partition-adjacency/skeleton framework](https://arxiv.org/abs/1508.00542).
No novelty or connectivity claim is made for those general operations. In
particular, their realization-space connectivity results are not imported
into our smaller space with mixed-clique and pointwise constraints. The
contribution is the explicit Ramsey signature-preserving update mechanism,
its independent finite validation, and the exactly delimited graph-repair
boundary for this retained witness.
