# An exact two-switch interaction and escape certificate

## Shared-vertex interaction identity

Represent red edges by x_e in {0,1}. Let S and T be two four-edge switch
supports whose vertex sets meet in exactly one vertex w. The supports are
edge-disjoint, so the edge-color operations commute. Write

```text
epsilon_e = 1-2*x_e
```

for the change of a flipped red-edge bit. Let I be the two vertices joined
to w by switched edges of S, and J the corresponding two vertices for T.
For the local red-triangle vector t, define

```text
Gamma = t(G_ST)-t(G_S)-t(G_T)+t(G).
```

For every i in I and j in J, add

```text
epsilon_(wi) * epsilon_(wj) * x_(ij)
```

to Gamma at each of w,i,j. The sum of these four contributions is exactly
Gamma; all other entries vanish.

Proof: expand the product of the three red-edge bits for each triangle.
Its mixed difference is zero unless it contains an edge from both supports.
Since their vertex sets meet only at w, such a triangle must be {w,i,j}
with i in I and j in J. Its edge ij is unmodified. Therefore its mixed
difference is precisely the displayed bilinear term. No triangle contains
two edges from one support and an edge from the other in this overlap
configuration. Summing the triangle indicators at their three vertices
proves the vector identity.

Thus, given the two single-switch local-triangle updates, a joint update
requires only four extra cross-edge tests. The final local-cap objective
still has to be evaluated on the corrected vector: it is not additive in
these single-switch scores. Feasibility gates must also be checked for the
combined graph; the identity alone supplies no Ramsey-feasibility guarantee.
No novelty claim is made for the general finite-difference principle.

## The explicit square

Let G be the graph in the predecessor
[cell-preserving repair certificate](../ramsey_r55_cell_preserving_repair),
SHA256 `7a832f229bb3fd97f5c3e5dceb060988fb5c5d2df074d1cb37ddbb1dcd5fc8a6`.
Exceptional vertices 0,1,2 form a red triangle and have degree 20; the other
40 vertices have degree 21. Their red-signature vector in mask order 0..7 is
`(0,8,8,6,10,4,4,0)`. All exceptional local profiles are (92,107).

Use these two alternating switches, with removed red edges first:

```text
S: remove(4,40),(7,41); add(4,41),(7,40).
T: remove(5,14),(9,40); add(5,40),(9,14).
```

The same-signature opposite pairs are (4,7) and (5,9). Hence both switches
preserve every degree, every signature-cell edge quota and every exceptional
local edge count. Their vertex sets meet only at 40, their edge supports are
disjoint, and their alternating patterns remain valid in either order.
Both paths therefore end at the same graph G_ST.

For central v, the degree identity gives t_R(v)+t_B(v)=201-|X_v|. Write

```text
Phi(G)=sum_(v in C) max(0,t_R(v)-100,101-|X_v|-t_R(v)).
```

All four graphs G,G_S,G_T,G_ST satisfy the previous mixed-K5 and pointwise
root conditions on actual individual edges. All 884 pointwise inequalities
are checked, not just their aggregates. Their values of Phi are

```text
G:83,  G_S:83,  G_T:84,  G_ST:78.
```

Consequently S followed by T is a nonincreasing two-step escape from the
previous local minimum, while T alone is uphill by one. This is a score
interaction, not a claim that S was needed to make T feasible: T alone
passes every retained feasibility gate too.

## Where the six-unit interaction comes from

The four cross-edge bits are x_45=0, x_49=0, x_75=1, x_79=1. The general
formula therefore gives Gamma_5=1, Gamma_9=-1, and zero elsewhere. In
particular, the interaction does not change the total number of red triangles
(the sum of the local interaction vector is zero). It changes their local
distribution. The interval-distance objective introduces additional nonlinear
effects, including at vertex 34 outside both switch supports.

The only nonzero per-vertex mixed differences of the penalty are:

| vertex | t_R in G,G_S,G_T,G_ST | penalties in that order | mixed difference |
|---:|---|---|---:|
| 5 | 100,100,97,98 | 0,0,3,2 | -1 |
| 9 | 100,101,100,100 | 0,1,0,0 | -1 |
| 14 | 101,102,99,100 | 1,2,1,0 | -2 |
| 34 | 100,101,99,100 | 0,1,1,0 | -2 |

Their sum is Phi(G_ST)-Phi(G_S)-Phi(G_T)+Phi(G)=-6. Neither isolated move
strictly lowers Phi, but their combination lowers it by five. The exact
local vector, not just the aggregate edge counts or total triangle count,
is therefore material to this repair decision.

## Minimum permitted switch depth, and limitations

The predecessor's complete four-edge neighborhood audit proves that no
single admissible central degree/quota-preserving switch lowers Phi at G.
The present verifier replays that audit as an explicit dependency, obtaining
the same complete classification digest. The displayed path uses two such
admissible switches and ends below Phi(G). Hence the minimum number of
permitted four-edge switches needed to reach ANY lower-Phi graph from G is
exactly two. The path can be chosen nonincreasing in Phi.

This is NOT a minimum changed-edge-support claim: the two supports change
eight distinct edges on seven vertices, but simultaneous six-edge changes
are not excluded. It is not an optimal two-switch endpoint or a complete
neutral-component classification. The other neutral directions were not
exhausted, and no local-minimum claim is made for G_ST.

The endpoint still contains 229 red and 253 blue K5s and has 28 central local-cap
failures. All 482 monochromatic K5s lie inside C. It is NOT a Ramsey(5,5;43)
graph and does not exclude a degree profile or settle either earlier UNKNOWN
SAT model. Global 66 profiles/271 anchored splits and the 470 aggregate case
filters remain unchanged.

## Evidence boundary

The proof of the interaction identity is the displayed polynomial expansion.
All 8,192 seven-vertex completions of the two fixed switches are checked by
literal triangle enumeration, with 7,168 nonzero interaction vectors. The
explicit four graph states are exhaustively checked against all 962,598
five-sets, with complete monochromatic lists compared to an independent
recursive clique algorithm in the pinned graph verifier. The earlier
one-switch census is freshly replayed; this is dependency verification,
not new-radius enumeration or independent peer review.

The new proof path imports no search code or solver. Remaining trust lies
in the unformalized arguments, exact Python source/runtime, pinned explicit
inputs, SHA256 and hardware. Interpreting Phi=0 as the hard-branch local-cap
target retains the earlier Ramsey-extremal catalog boundary; the direct graph,
interaction and minimum-switch-depth statements need no catalog or SAT verdict.
