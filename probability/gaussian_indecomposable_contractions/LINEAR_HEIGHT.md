# Linear chain height and a larger surviving Gaussian gap

Complete author proof, 27 September 2026; independent review pending.
This strengthens the quantitative part of the accepted
[indecomposable reduction](PROOF.md) and [mesh bound](EFFECTIVE_BOUND.md).
It does not prove a new Gaussian sign or a positive Kneser--Poulsen class.
The previously reviewed files are preserved unchanged.

The old argument bounded the length of a descending chain by the number of
possible mesh placements. That loses exponentially more than necessary.
Selected opposite-vertex distances take only two values, and decrease at
most once along any contraction chain. They determine the placement after
fixing a root tetrahedron. This gives a bound linear in the number of labels.

## 1. Framework and statement

Let a finite labelled tetrahedral complex have `v` vertices and `m` distinct
tetrahedra, with connected facet-adjacency graph. In a reference placement
`P` in R3 every tetrahedron is nondegenerate. Consider all placements having
the same lengths on every tetrahedron edge, modulo Euclidean isometries.
Their complete squared-distance vectors form a set `D`. Placements may
overlap, and vertices from different tetrahedra may coincide.

For `d(Q)<=d(P)`, let

    I = {d(Z) in D : d(Q)<=d(Z)<=d(P)}.

When all the tetrahedron edges are tight at the two endpoints, this is the
**full** three-dimensional distance interval, as in the accepted reduction.
No intermediate configuration outside the common-edge framework is omitted.

**Theorem 1.** There are `v-4` selected pairs of labels, and constants
`a_j<b_j` depending only on the tetrahedron shapes, for which

    beta_j(Z) = (|z_(u_j)-z_(w_j)|^2-a_j)/(b_j-a_j) in {0,1}

define an injective map `beta:D -> {0,1}^{v-4}`. It is order preserving:

    d(Z')<=d(Z)  implies  beta(Z')<=beta(Z).

Consequently, put `r=sum_j[beta_j(P)-beta_j(Q)]`. Every strict descending
chain in `I` has at most `r` steps, where

    r <= v-4 <= m-1.                                         (1)

The interval has at most `2^r` states. Every saturated chain consists of
indecomposable contractions among **all** R3 configurations. The encoding
need not reflect order: decreasing its bits does not suffice for a valid
contraction, and most bit strings may be infeasible.

**Data-dependent refinement.** In the full facet-adjacency graph, mark an
edge zero when its two opposite vertices have the same distance at P and Q.
If the graph of zero edges has `c` connected components (including isolated
tetrahedra), the selected pairs can be chosen so that

    r <= min(v-4,c-1).                                       (2)

In particular `c=1` forces congruent endpoints. This is a bound on chain
height, not a polynomial-time procedure for finding all states or covers.

## 2. A monotone binary measurement at a face

Two adjacent tetrahedra share a nondegenerate triangular face F. Write
their opposite vertices as u,w. Once the first tetrahedron is placed, the
three distances from w to F leave exactly two positions for w. Their
orthogonal projection onto aff(F) is the same; their signed heights are
opposite. If the positive heights of u,w above their respective face planes
are h_u,h_w, the two possible squared distances between them are

    a = |proj_F(u)-proj_F(w)|^2 + (h_u-h_w)^2,
    b = |proj_F(u)-proj_F(w)|^2 + (h_u+h_w)^2.

Thus `b-a=4h_u h_w>0`. These constants depend only on the edge lengths of
the two tetrahedra. In particular they are independent of the placement
of earlier cells. In a contraction, this binary distance can only change
from b to a. Nondegeneracy of **both** cells is essential here.

For rational reference coordinates the same two constants are obtained
without square roots: reflect the reference w in the reference face and
take the two squared distances to the reference u. Both are rational.

## 3. Select only the steps that introduce a vertex

Fix a spanning tree of the facet-adjacency graph, root it at one tetrahedron,
and process parents before children. Align the root to its reference
placement. Each child shares three vertices with its parent, so introduces
at most one previously unplaced label. Every nonroot label is introduced
exactly once. There are therefore exactly `v-4` introducing steps, and
`v<=m+3`.

At each introducing step select the pair consisting of the new opposite
vertex w and the parent's opposite vertex u. All four parent vertices are
already placed. Section 2 shows that its bit distinguishes the two possible
positions of w. Knowing all the selected bits reconstructs every labelled
point successively. Nonintroducing steps and cycles can impose additional
consistency conditions; they create no new labels or ambiguity. This proves
injectivity on feasible placements. Fixing a full tetrahedron removes all
ambient isometries, including reflection.

Each bit is a positive affine function of a coordinate of the complete
distance vector. It is therefore order preserving. The integer

    Psi(Z) = sum_j beta_j(Z)

decreases by at least one at each strict contraction: if it did not, all
bits would agree, hence the placements would agree. On I, only the r bits
that differ at its endpoints can vary. This proves (1), the state count,
and the chain bound. The finite-interval argument in PROOF.md, Lemma 2,
then proves the assertion about saturated chains.

For (2), first take a spanning tree within each zero-edge component, then
connect these trees using `c-1` other adjacency edges. This is a spanning
tree of the whole dual graph with exactly `c-1` nonzero edges. Use that tree
in the construction above. Every selected bit that changes between P,Q
comes from one of these nonzero edges; some such edges may not introduce
a vertex. Hence `r<=c-1`, as well as `r<=v-4`. QED.

## 4. Improved transfer of a negative hinge

Write `Phi(Z)=H_(sum_i w_i gamma_s(.-z_i))(a)`. Suppose a prescribed
N-atom contraction has `Phi(Q)-Phi(P)<=-delta<0`. Use the accepted
effective Brehm extension, with at most `M_N` tetrahedra, where

    h_N = 512*2^N*(N+6) + 3N + binom(N,3) + 6,
    M_N = 12 h_N [1+h_N+binom(h_N,2)+binom(h_N,3)].

Let v be the actual mesh vertex count. Add uniform positive mass on its
vertices with `epsilon=delta/[2(1+delta)]`, scaling the old masses by
`1-epsilon` and the threshold by `1-epsilon`. The accepted perturbation
estimate gives total new endpoint gap at most `-delta/2`. A genuine failure
has a nontrivial interval, so `1<=r<=v-4`.

Along a saturated chain of length `L<=r`, telescoping produces an
indecomposable step with gap at most

    -delta/(2L) <= -delta/(2r) <= -delta/[2(v-4)].             (3)

Every labelled weight is at least `epsilon/v`. Since `v<=m+3<=M_N+3`,
there is an indecomposable witness with

    labels <= M_N+3,
    each labelled weight >= delta/[2(M_N+3)(1+delta)],
    negative gap magnitude >= delta/[2(M_N-1)].              (4)

All previous conclusions about a fixed tetrahedron, common tight framework,
rationality for rational prescribed data, and bounded diameter survive.
Merging coincident input labels can only increase weights and preserves the
contraction, interval, and hinge. Equation (3) refers to the mesh label
count before any such merge; no post-merge framework is silently assumed.

The earlier bound `delta*2^(-M_N)` remains true but is superseded by (4).
Since `M_N=O(N^4 16^N)`, the new guaranteed gap loses a single exponential
in N, instead of a double exponential. State enumeration may still be
exponential in v and is not performed here.

## 5. Contribution, provenance, and scope

Binary placement by intersecting three spheres is standard distance
geometry; see Liberti, Lavor, Masson and Mucherino,
[Polynomial cases of the Discretizable Molecular Distance Geometry Problem](https://arxiv.org/abs/1103.1264).
That paper provides background on binary search spaces, not the present
Gaussian conclusion. Brehm extension and its rational bounded construction
are the cited dependencies of EFFECTIVE_BOUND.md. No priority claim is made
for the elementary face-reflection observation.

The contribution here is its use as a **monotone integer potential** on the
full distance interval, replacing the state-count loss in the team's
Gaussian reduction by its linear chain height. The
[consumer handoff](LINEAR_HANDOFF.md) composes the improvement with the
accepted support-independent cubature frontier and states the numerical
boundary precisely. It supplies no denominator bound, new positive map
class, negative Gaussian example, or proof of the unrestricted sign.

`linear_height.py --check` uses exact rational arithmetic on small generic
frameworks. It checks a full eight-state interval of height three, a
partly fixed interval, a cycle consistency obstruction, and an interval
in which decreasing selected bits can violate another pair bound. It also
rejects malformed geometry and checks the new loss budgets. These are
finite controls of the definitions; the universal theorem and analytic
transfer are the written proof, pending independent review. No prior
cap/flap classification, certificate corpus, or Gaussian quadrature is rerun.
