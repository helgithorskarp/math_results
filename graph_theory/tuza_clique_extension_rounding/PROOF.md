# Linear triangle-packing loss with a growing clique cell

Complete author proof. Independent review of this extension is pending.
Write nu(G) for maximum edge-disjoint triangle packing and nu*(G) for the
full fractional packing optimum. All graphs are finite and simple.

Fix d>=1 and 0<alpha<=1. H has n>=1 vertices in at most d clique/independent
classes, each of size n_i>=alpha*n, with complete/empty cross pairs. X is
a clique of size 0<=s<=n, complete or empty to every core class.

**Theorem 1.** There is a finite K(d,alpha) such that

    0 <= nu*(H+X)-nu(H+X) <= K(d,alpha)n,

uniformly in every integer 0<=s<=n and every feasible full fractional
profile. More precisely, every feasible fractional packing rounds with
this additive loss. The added cell has the same neighborhood into H at
every vertex. Constants are existential through the accepted balanced-deletion lemma.

The comparable-core input used below is the **balanced-deletion lemma**
from [the accepted independent-extension proof](../tuza_independent_extension_rounding/PROOF.md),
Section 4, independently audited in
[review h5861](../tuza_independent_extension_rounding_review1/REVIEW.md).
For fixed d,alpha,A there exist eta_core>0 and n0 such that, for every
n>=n0, every such core H and F contained in H with Delta(F)<=eta_core*n
and incident type-degrees within A of each class average, every nonnegative
triangle-plus-spare profile y satisfying

    sum_P a_eP y_P = b_e-|F_e|

has an edge-disjoint realization of the triangle counts
floor((1-lambda/n)y_T) if this integer is at least n, and zero otherwise.
Here M=binom(d+2,3)+binom(d+1,2), lambda=8(M+A)/alpha. The loss from the
profile triangle objective is at most (lambda/6+M)n. This is an explicit
mathematical dependency, ultimately on Keevash Theorem 5.15; its full
specialization is in the linked source. The acceptance of that lemma does
not constitute acceptance of the new construction below.

Only the small case 1<=s<=eta*n needs a new construction. For eta*n<s<=n,
all classes of H+X have size at least min(alpha,eta)(n+s)/2. Apply comparable
class rounding. For the finitely many small n, enlarge K using |E(G)|/3.

## Profile

Let u be XXX mass, v_i the XXH_i mass, w_e the XHH mass on core edge type e,
and z_T the core-only masses. Include all repeated-type triangles. The exact
capacity inequalities include

    3u+sum_i v_i <= binom(s,2),
    2v_i+sum_e k_i(e)w_e <= s*n_i,
    sum_T a_eT z_T+w_e+z_e(spare)=b_e.

Here k_i(ij)=1, k_i(ii)=2, and unsupported masses vanish. It suffices to
round the exterior triangles with O(s) loss, leaving a used core graph F of
maximum degree <=s and incident type-degree discrepancy bounded by d alone.
Then y_T=z_T, y_e(spare)=z_e(spare)+w_e-|F_e| is a nonnegative residual
capacity profile, to which the accepted balanced-deletion lemma applies.
All spoke constructions below are restricted to core classes adjacent to X.
For every other class, v_i and all incident w_e vanish and no spoke graph
is used. The core-completion input is the displayed capacity profile; it
requires no separate fractional realization on the surviving triangles.

## Nearly regular triangle packing inside X

Use the classical Ray-Chaudhuri–Wilson existence theorem for a resolvable
Steiner triple system on every v congruent to 3 modulo 6, stated in the
[primary author report, printed page 224](https://www.mathunion.org/fileadmin/ICM/Proceedings/ICM1970.3/ICM1970.3.ocr.pdf).
Take the least such v>=s, with delta=v-s<=5.
Its (v-1)/2 parallel classes partition the v vertices. Choose

    k=floor(3u/v)

classes, then delete delta vertices and all triples meeting them. The
remaining m triples are edge-disjoint and m<=u. Their loss is less than
v/3+delta*(v-1)/2, hence at most 7s for s>=3; s=1,2 has u=0. Every retained
vertex belongs to k-l_x triples, where 0<=l_x<=delta, since it shares at
most one original triple with each deleted vertex. Therefore the remainder
R of K_s has degree spread at most 2delta<=10.

Proper-color R with p=Delta(R)+1 colors by Vizing. Include empty colors in
this palette. Every vertex misses at most 11 palette colors. Put

    k_i=floor(2v_i/s).

Since sum k_i <= 2sum v_i/s <= (2binom(s,2)-6u)/s <= average_degree(R),
there are enough palette colors to allocate disjoint groups of k_i colors.
Let D_i be the edges in the ith group, and v'_i=|D_i|. Then

    0<=v'_i<=v_i,
    v_i-v'_i < 6s,
    k_i-11 <= deg_Di(x) <= k_i <= 2v_i/s.

All these D_i are edge-disjoint and avoid the XXX packing. The degree of
each D_i differs from its own mean by at most A=11.

Recolor each D_i properly with n_i colors (n_i>=s), then make color-class
sizes differ by at most one. This classical equitability step follows by
swapping the two colors along an alternating path with one more edge in
the larger color whenever their total sizes differ by at least two. The
sum of squared color-class sizes strictly decreases. Assign each color to
a distinct vertex of H_i and replace each edge xy by the triangle xyh.
No spoke repeats. At x in X the used H_i-spoke degree is deg_Di(x), while
at h in H_i it is twice a color-class size, within 2 of 2v'_i/n_i.

Thus the unused bipartite spoke graph B_i between X and H_i has row degrees
within A=11 of their mean D_i^0=n_i-2v'_i/s, column degrees within 2 of
s*D_i^0/n_i, and every row has degree at least n_i-2v_i/s.

## Integral spoke allocation with bounded discrepancy

Consider an s by N bipartite graph with row degrees d_x, mean D, and
|d_x-D|<=A. Suppose column degrees b_y obey |b_y-sD/N|<=delta. For an
integer a<=min_x d_x, assign fractional value a/d_x to every available edge.
All row sums are a. The column sums are f_y=a*sum_{x~y}1/d_x. An integral
flow chooses a subgraph with row degree exactly a and column degrees between
floor(f_y) and ceil(f_y); the fractional assignment proves feasibility.

If D>=Q>=2A, s/N<=1/(8A), delta<=B and Q>=8AB, then

    |f_y-a*b_y/D| <= A*b_y/(D-A)
                    <= 2A*s/N+2A*delta/D <= 1/2.

Since a<=D, |a*b_y/D-sa/N|<=delta. The selected subgraph therefore has
column discrepancy at most delta+2 about sa/N. After removal, row degrees
all decrease by exactly a (their discrepancy stays A), and column
discrepancy is at most 2delta+2 about the new mean.

Each core class participates in at most d core edge types. Starting at
delta=2, after j allocations delta<=2^(j+2)-2. Set

    A=11, B=2^(d+2), Q=8B(A+d).

All selected column discrepancies are <B, and all hypotheses above hold
when the allocation degree is at least Q and s/n_i<=1/(8A).

## Increasing-quota pairing

For each supported core edge type e set q_e=floor(w_e/s), retaining this
integer if it is at least Q and setting it to zero otherwise. The retained
count is m_e=s*q_e. Loss on each coordinate is <(Q+1)s.

Process positive types in nondecreasing q_e. For e=ij allocate q_e spokes
at EACH x from both B_i and B_j. For e=ii allocate 2q_e from B_i. This is
always row-feasible: total requested row degree at class i is

    sum_e k_i(e)q_e <= sum_e k_i(e)w_e/s <= n_i-2v_i/s,

which does not exceed any initial available row degree. Earlier allocations
subtract the same amount at every row. At a current nonempty allocation
its row mean is at least its demand, hence at least Q, so the flow lemma
applies. Used spokes for different types and the XXH triangles are disjoint.

For e=ij and each x, match its two assigned q_e-sets, avoiding core edges
used earlier. For e=ii split the assigned 2q_e-set into two q_e-sets and
match them in the same way. All relevant core pairs are complete.

Let q be the current quota. Even including ALL core edges that this step
will eventually use, each core vertex has degree at most

    2d*s*q/(alpha*n)+dB.

There are at most d incident edge types; their processed quotas are <=q;
the allocated type degrees have discrepancy <B. Choose

    eta <= min(alpha/(8A), alpha/(16d), eta_core(d,alpha,B)).

Since s<=eta*n and q>=Q>=8dB, this maximum degree is at most q/4. In each
q by q matching problem every vertex thus has more than q/2 available
neighbors, so Hall's theorem gives a perfect matching. This also covers
loop types and all earlier centers of the current type. Each chosen pair
forms an XHH triangle with its assigned center x.

The resulting used core graph F has Delta(F)<=s, because a core vertex uses
at most one spoke to each of the s exceptional centers. Its degree in each
incident core edge type differs from its class average by <B, exactly the
column discrepancy of that type's allocated spokes. No subsequent pairing
changes these endpoint counts.

## Core completion and loss

Apply the accepted balanced-deletion profile lemma (h5857, Section 4) with
discrepancy parameter B to H-F and the profile given above. It loses at most
(lambda/6+M)n core triangles, where

    M=binom(d+2,3)+binom(d+1,2), lambda=8(M+B)/alpha,

above its existential threshold. This is a genuine dependency on the
accepted prior lemma and ultimately Keevash Theorem 5.15; finite checks do
not replace it. Exterior losses sum to at most

    [7+6d+E(Q+1)]s, where E=d(d+1)/2.

All four categories XXX, XXH, XHH and HHH are mutually edge-disjoint by
construction. This proves the small-extension theorem. Absorbing s>eta*n
as another comparable class proves the stated theorem for 0<=s<=n. Small
core orders are covered by an enlarged fixed constant since |V(G)|<=2n.

Consequently every fixed mixed template with at most one class smaller than
a fixed fraction of the total order has linear additive full-LP packing
loss: the exceptional cell is either independent (previous theorem) or a
clique (this theorem), and the other cells form a comparable core. Restrict
that fraction to <=1/2 without loss when using s<=n. This does not handle
several unrelated vanishing clique cells or arbitrary class proportions.

## Explicit triangle-free-core consequence

**Theorem 2.** If H is triangle-free, there are no z_T coordinates and no dense completion
is needed. For every n,s>=1 with

    s/n <= eta_explicit=min(alpha/88, alpha/(16d)),

the elementary construction alone proves

    nu*(G)-nu(G) <= [7+6d+E(Q+1)]s,
    E=d(d+1)/2, B=2^(d+2), Q=8B(11+d).

There is no unspecified lower-order threshold in this statement. Its loss
is in the EXCEPTIONAL clique order s. The imported existence input is the
classical all-order Kirkman theorem, with Vizing coloring and integral flow;
Keevash is not needed for this consequence. The implementation below checks
affine Kirkman fixtures and does not implement all-order Kirkman construction.
This is an explicit numerical theorem, not a claim of a practical complete
rounding implementation. If desired E may be replaced by the number of
supported core edge types, using exactly the same loss calculation.

## Verification and unresolved scope

The accompanying author checker verifies affine Kirkman fixtures, deleted-point
degree bounds, palette groups, equitable recoloring traces, integral spoke
allocations (each floor/ceiling column bound), matching triangles, all edge
disjointness and type discrepancies. Large-order witnesses are not a proof
of the imported existence theorems. K and the final threshold remain
ineffective through the prior dense completion. The old acceptance does
not transfer to this new flow/matching argument.

The classical inequality tau(G)<=2nu*(G), due to Krivelevich and recorded
in [Chapuy et al., Theorem 1.2(ii)](https://arxiv.org/pdf/1012.0372), gives
tau(G)<=2nu(G)+2K*n in Theorem 1 and
tau(G)<=2nu(G)+2[7+6d+E(Q+1)]s in Theorem 2. These are immediate
corollaries, not resolutions of Tuza's conjecture.

External inputs, proof status and the limits of the literature comparison
are recorded in [SOURCES.md](SOURCES.md). Exact reproduction commands and
the finite evidence are in [README.md](README.md).
