# Two-round localization and slowdown under independent edge addition

All graphs are finite, simple, and labelled. All logarithms are natural.
Random graphs have independent Bernoulli edges. Every parameter called
fixed is independent of `n`. High probability means probability tending
to one as `n` tends to infinity.

## 1. Statements and scope

A full-feedback probe at `w` returns `{w}` when the robber is at `w`, and
otherwise returns the set of all neighbors of `w` on shortest paths to
the robber. After an unresolved round the robber may stay or move one
edge. The cop knows the graph and may choose probes adaptively. Let `T(G)`
be the least worst-case number of rounds needed by one cop, with value
infinity if one cop cannot win or the graph is disconnected.

**Theorem 1 (two-round interval).** If

```
np^2 / log n -> c,              15/32 < c < 1/2,
```

then `T(G(n,p))=2` with high probability. More precisely, one can choose
a fixed integer `K=K(c)` and distinct labels `w_0,v_1,...,v_K` before
sampling the graph, probe `w_0` first, and choose a successful second
probe from `v_1,...,v_K` after seeing the first response.

It is sufficient to take any positive integer `K` with

```
1/2 + K(15/8-4c) < 0,
2   + K(7/8-2c)  < 0.                                           (1)
```

The value `15/32` is a sufficient endpoint of this proof, not a claimed
sharp boundary. The theorem does not determine `T` throughout `c<=1/2`.

The following prior result is used only for the slowdown corollaries:

**Prior hierarchy theorem.** If `np^2/log n -> c>1/2` and
`1/(2c-1)` is not an integer, then

```
T(G(n,p)) = ceil(1/(2c-1))       with high probability.             (2)
```

A complete written proof is in
[full_feedback_capture_rounds](https://github.com/helgithorskarp/math_results/tree/main/probabilistic_combinatorics/full_feedback_capture_rounds).
Theorem 1 below is independent of that proof. The next two corollaries
explicitly depend on (2).

**Corollary 2 (arbitrary fixed slowdown).** For every fixed integer `M>=3`
there are constants `c_-<1/2<c_+` and an independent edge-addition coupling
`G_- subseteq G_+`, with marginals
`G(n,sqrt(c_- log n/n))` and `G(n,sqrt(c_+ log n/n))`, such that

```
T(G_-)=2,                  T(G_+)=M                              (3)
```

simultaneously with high probability. Both graphs have full-feedback
localization number one.

**Corollary 3 (vanishing relative addition, unbounded slowdown).** There
exist deterministic sequences `0<p_-(n)<p_+(n)<1`, with

```
p_+(n)/p_-(n) -> 1,        np_-(n)^2/log n -> 1/2,
```

and independent edge-addition couplings with these marginals, for which
`T(G_-)=2` with high probability, while `T(G_+)` tends to infinity in
probability and is finite with high probability. Moreover,

```
|E(G_+)\E(G_-)| / |E(G_-)| -> 0    in probability.                 (4)
```

This last construction is existential, obtained by a diagonal choice of
parameters. It supplies no explicit rate of divergence and is not a
uniform theorem for a prescribed growing number of rounds.

Nonmonotonicity itself is not claimed as a new phenomenon: closing a path
on at least five vertices into a cycle already changes the full-feedback
cop number from one to two, by Jones--Kinnersley's elementary results.
The conclusions here concern sparse random graphs, keep the cop number
equal to one, and allow an asymptotically negligible relative edge addition.
They do not answer the question whether any graph needs more than two cops.

## 2. Regularity and the opposite behavior of distance-three responses

Put `q=1-p`, `L=log n`, and `lambda=np^2`. Throughout the proof of Theorem 1,
`lambda/L -> c` in its stated interval. The following hold with high
probability by Chernoff bounds and elementary binomial upper tails:

```
all degrees are np+O(sqrt(np)L);
all pair codegrees are at most L^2;
the graph is connected.                                         (5)
```

The degree failure probability is at most `n exp(-Omega(L^2))`. For the
codegrees, use `(e mu/t)^t` at `mu=O(L)`, `t=L^2` and union over pairs.
Connectivity follows by summing `binom(n,s)q^(s(n-s))` over `1<=s<=n/2`,
since `np/log n -> infinity`.

For a probe `w` write `D=N(w)`, `d=|D|`. A nonneighbor `x!=w` has code
`C_w(x)=D intersect N(x)`. If the code is nonempty, `dist(w,x)=2` and
the response is exactly that code. An empty code is called a zero code.

**Lemma 4 (global visibility of zero codes).** For every fixed `0<c<1/2`,
if `np^2/L -> c`, then with high probability, simultaneously at all probes:

1. Every zero-code target has distance three and a response of size
   greater than half the probe's degree.
2. No two zero-code targets have the same response.

Consequently every zero-code target is globally identified by its response:
positive codes have size at most `L^2`, and neighbor responses are singletons.

**Proof.** First fix `w,x` and expose all edges incident to them. On the
event that `x` is a zero-code nonneighbor, `D` is disjoint from `N(x)`.
The edges joining these two sets are still independent. For each `b in D`,
the probability that no vertex of `N(x)` gives a path `b-y-x` is
`q^deg(x)=n^(-c+o(1))`, uniformly on the local degree bounds of (5).
The tests for distinct `b` use disjoint edges. Except with probability
`exp(-n^(1/2+o(1)))`, more than `d/2` tests succeed. The target then has
distance three and every successful `b` belongs to its response. The
failure bound is more than sufficient for a union bound over `w,x`.

For distinct zero-code targets `x,y` at `w`, expose the edges incident to
`w,x,y`. Set

```
A=N(x)\{y},               B=N(y)\{x}.
```

The removals matter if `x~y`: edges from `D` to `x,y` are already known
to be absent. The sets `A,B` avoid `D` and the three exposed vertices;
their sizes are `np+o(np)` and their intersection has size at most `L^2`
on the local regular event. For a fixed `b in D`, its two reachability
indicators through `A,B` differ with exact probability

```
q^|A| (1-q^|B\A|) + q^|B| (1-q^|A\B|) = n^(-c+o(1)).             (6)
```

These tests are independent over `b`, so equality of the two indicator
vectors has probability at most

```
exp(-n^(1/2-c+o(1))).                                            (7)
```

Since `c<1/2`, this is smaller than every fixed inverse power of `n`.
Union over triples. The first part identifies the indicators with actual
full-feedback responses, proving the lemma. In both calculations, first
intersect with the *local* regular event determined by the exposed
incident edges. The global event (5) is used only to ensure all such
local bounds. Independence is not asserted after conditioning on global
regularity. QED.

This is a different mechanism from the prior `c>1/2` hierarchy: here a
zero-code target usually misses many response directions, and those
missing directions distinguish it from every other zero-code target.

## 3. First-response classes and a fixed set of alternative probes

Fix `K` satisfying (1), and choose distinct labels
`Q={w_0,v_1,...,v_K}` before sampling. Expose all edges incident to `Q`.
For each probe `u_i` in this list put `D_i=N(u_i)\Q`, with `u_0=w_0`.
Let `E_i` be the vertices of `D_i` belonging to no other `D_j`.

With high probability, the following additional facts hold:

```
Q is independent;
lambda/2 <= |D_i intersect D_j| <= L^2,  i!=j;
no outside vertex belongs to three D_i;
|E_i|=np+O(sqrt(np)L+L^2).                                      (8)
```

The failure probabilities of independence and the triple-intersection
assertion are `O(K^2 p)` and `O(K^3 np^3)`, both `o(1)`. Each fixed
pair codegree is asymptotic to `lambda` with high probability, since
`lambda` tends to infinity. In particular, the lower bound in (8) holds
simultaneously for this fixed list.

Every target in `Q` is globally identified by each probe in `Q`, with
high probability. Its positive code at a different probe has at least
`lambda/2` entries. Conditional on the incident-edge exposure, any
nonneighbor target outside `Q` contains this entire code with probability
at most `p^(lambda/2)`; the relevant edges remain unexposed. A union
bound over the bounded probe pairs and at most `n` targets suffices.
Neighbor targets have singleton responses, while zero-code targets have
large responses by Lemma 4. The latter cannot equal a positive code of
size at most `L^2`.

At the first probe `w_0`, with high probability every positive-code
response class of code size at least two has at most two members.
Indeed, conditional on `D_0` and independence of `Q`, or simply exposing
`N(w_0)` alone, the expected number of triples of identical codes of size
at least two is bounded by

```
n^3 q^(3d) [(1+(p/q)^3)^d - 1 - d(p/q)^3]
    = n^(1-3c+o(1)) = o(1).                                    (9)
```

Here `d(p/q)^3=O(np^4)=n^(-1+o(1))`. Our range has `c>1/3`.

The singleton response `{b}`, for a neighbor `b` of `w_0`, has exactly
the class

```
U_b={b} union {a not in N[w_0]: C_{w_0}(a)={b}}.                  (10)
```

Lemma 4 excludes extra zero-code targets from this class. The response
at `w_0` itself is unique. Thus every unresolved first-response class is
either a set (10) or a pair. It contains no vertex of `Q`.

After a first-response class `U`, the possible robber positions are
`N[U]`. It suffices to show that some `v_j` has pairwise distinct full
responses on `N[U]`. The following two lemmas establish this
simultaneously for every class needed by the strategy.

## 4. Failure witnesses and a spanning-tree charge

For a set `U` disjoint from `Q`, classify an alternative `v_j` as follows.
If `v_j in N[U]`, discard it and call its type **E**. Since `v_j notin U`,
choose a witness `z_j in U intersect N(v_j)`.

Otherwise `v_j` is outside `N[U]`. If it fails to resolve `N[U]`, choose
an ambiguous pair in that set. By Lemma 4 and the uniqueness of targets
in `Q`, the pair is outside `Q` and is one of two types:

- **NN:** distinct nonneighbors `x_j,y_j` of `v_j` have the same nonempty
  code. Choose a common code member `z_j`, requiring the edges
  `z_j x_j,z_j y_j` and `z_j in D_j`.
- **NT:** a neighbor `z_j` of `v_j` and a nonneighbor `x_j` have the
  same response, so `C_{v_j}(x_j)={z_j}` and the edge `z_j x_j` is required.

Every non-E center `z_j` is outside `U`, because `v_j` has no neighbor
in `U`. For every pair endpoint in `N[U]`, choose a predecessor in `U`
at distance at most one. If the endpoint itself belongs to `U`, choose
that endpoint as its predecessor. Identical vertices and identical edges
in all chosen witnesses must be merged; stays require no graph edge.

Let `h` denote the number of E positions, and put

```
t=2(number of NN positions)+(number of NT positions).             (11)
```

The integer `t` is the exponent count of the second-probe code tests.

**Charging lemma.** Form a connected base tree on the predecessor set,
then attach each distinct endpoint outside that set by one predecessor
edge, and each distinct NN center that is not an endpoint by one of its
witness edges. This gives a spanning tree `F` of the required witness
graph (with virtual base edges in the pair case below). Let `beta` be
the number of required graph edges outside `F`. Let `ell` count the
surplus formal vertex roles after the predecessor set is fixed, as
defined precisely in Sections 5 and 6. Then

```
K-h <= 4 beta + ell,       hence beta+ell >= (K-h)/4.              (12)
```

**Proof.** Every NN position has a witness edge outside `F` incident to
its center. A center that is not an endpoint was attached just once,
whereas its two witnesses are distinct endpoints. If the center is an
endpoint, the only tree edge from it to another endpoint or predecessor
is its own predecessor edge, so again the two distinct witness edges
cannot both belong to `F`. Edges attaching other pure centers do not
change this argument: their other endpoints are endpoints, whereas a
pure center is not an endpoint anywhere in the template.

In an NT position, if the other endpoint `x_j` is outside the predecessor
set, then both `z_j,x_j` are endpoints outside that set and their edge
is not in `F`. The only positions not charged this way are NT positions
whose other endpoint lies in the predecessor set. Each such position
uses a separate surplus formal endpoint role, so their number is at
most `ell`.

Assign each remaining non-E position one of these nonforest edges.
It is incident to the center `z_j`. By (8), a vertex can be a center
for at most two distinct alternative probes. An edge has two endpoints,
so it receives at most four charges. There are `beta` such edges,
proving (12). A center reused by two positions is attached to the
spanning tree **once**, not once for each occurrence. QED.

## 5. All singleton classes have a usable second probe

**Lemma 5.** With high probability, for every neighbor `b` of `w_0`,
some alternative `v_j` resolves `N[U_b]`.

**Proof.** If all alternatives fail or are discarded, choose witnesses
as in Section 4. Let `B` consist of `b`, all chosen predecessors, and
all E centers. All its vertices belong to `U_b`. Write `s=|B|-1`.
The required graph contains the star edges `b-a` for `a in B\{b}`,
all nontrivial predecessor-to-endpoint edges, and all response-witness
edges. Let it have `v` distinct vertices and `e` distinct edges. It is
connected. Define

```
beta=e-v+1,
ell=1+s+K+t-h-v >= 0.                                           (13)
```

For this count, begin with the `1+s` distinct predecessor vertices.
There is one formal center for each alternative and `t` other endpoint
roles. Each of the `h` E centers is already in `B`. All other
identifications contribute to `ell`. In particular each NT other-endpoint
role in `B` contributes one to this surplus, even if several such roles
use the same vertex. The tree in the charging lemma starts from the
actual star on `B`, so (12) applies. Also,

```
s+t <= 4K-3h.                                                   (14)
```

An NN position uses at most two predecessors and two code-target roles,
an NT position at most two predecessors and one target role, and an E
position at most one predecessor. Reuse only decreases `s`.

Condition on the incident edges of `Q` satisfying (8). For fixed `K`
there are only finitely many types and vertex-identification templates.
The anchor requirements are `b in D_0` and `z_j in D_j` for each
alternative. A vertex with no anchor has at most `n` label choices, with
one at most `n^(1/2+o(1))`, with two at most `L^2=n^o(1)`, and with three
none. The number of labelings of a template is therefore at most

```
n^(v-(K+1)/2+o(1)).                                              (15)
```

All template vertices lie outside `Q`, so its required edges have
conditional probability `p^e`. Remove every template vertex from every
exclusive reservoir `E_i`. For each of the `s` distinct vertices of
`B\{b}`, the first-probe singleton condition implies at most one
neighbor in the remaining `E_0`, with probability `n^(-c+o(1))`.
These tests are independent over those vertices.

For an NN position, equality of its two codes implies equality of their
adjacency indicators at every vertex of the remaining `E_j`. The two
targets are distinct, so the probability is exactly

```
(q^2+p^2)^(|E_j|-O(K)) = n^(-2c+o(1)).                           (16)
```

For an NT position the singleton-code condition costs at most
`n^(-c+o(1))`. E positions need no second code test. The tests for
different probes use disjoint reservoirs, and every template vertex
has been removed from every reservoir. Thus their edge sets are disjoint
even when targets repeat, and are disjoint from the required graph edges.
The probability for a fixed labeling is at most

```
p^e n^(-c(s+t)+o(1)).                                           (17)
```

Combining (13), (15), and (17), its total counting exponent is

```
v-(K+1+e)/2-c(s+t)
 = 1/2+(1/2-c)(s+t)-h/2-(beta+ell)/2
 <= 1/2+K(15/8-4c)+h(3c-15/8)
 <= 1/2+K(15/8-4c),                                             (18)
```

by (12), (14), and `c<1/2`. The final bound is negative by (1).
Summing the finitely many templates proves the lemma. The choices of
all `b` and all singleton-class predecessors are already included in
the labeling count; no additional union factor is missing. The
high-probability response and regularity events were used to obtain
necessary witnesses, not imposed on the independent-edge calculation.
QED.

## 6. Every pair has a usable second probe

**Lemma 6.** With high probability, for every two-element set
`U subseteq V\Q`, some alternative `v_j` resolves `N[U]`.

**Proof.** Choose all-failure witnesses as above. The two vertices of
`U` are now free labels, with no first-probe code requirement. The
required graph need not be connected. Introduce a virtual root and two
virtual edges from it to the elements of `U`, solely for the spanning-tree
argument. These are not random edges and incur no probability cost.

If the actual graph has `v` vertices and `e` required edges, define

```
beta=e-v+2,
ell=2+K+t-h-v >= 0.                                             (19)
```

The augmented graph is connected. Its tree starts with the two virtual
edges, attaches each endpoint outside `U` by one predecessor edge, and
attaches each pure NN center once. Therefore `beta` counts the actual
nonforest edges and the charging lemma applies. NT other-endpoints in
`U` consume surplus roles in `ell` as before.

There are `K` anchor requirements, one center in each `D_j`. The number
of labelings is at most `n^(v-K/2+o(1))`; this already includes the
choices of the two elements of `U`. Required edges cost `p^e`, and the
exclusive-reservoir code tests cost `n^(-ct+o(1))`. The exponent is

```
v-(K+e)/2-ct
 = 2+(1/2-c)t-h/2-(beta+ell)/2
 <= 2+(7/8-2c)(K-h)-h/2
 <= 2+K(7/8-2c),                                                (20)
```

using `t<=2(K-h)`, (12), and `c<1/2`. This is negative by (1), proving
the lemma after summing the finitely many templates. QED.

## 7. Completing the adaptive two-round theorem

On the intersection of the high-probability events above, probe `w_0`.
If its response identifies the robber, stop. Otherwise its class `U` is
a singleton-code class (10) or a pair by Lemma 4 and (9). After the
robber's move its position belongs to `N[U]`. By Lemma 5 or 6 at least
one of the fixed alternatives has injective responses on this set.
Choose one, after inspecting the known graph and the first response,
and the second probe identifies the robber. This is a valid adaptive
strategy; its second probe need not be the same for different replies.

For the matching lower bound, no initial probe resolves all targets with
high probability in this range. Conditional on a typical degree `d`,
the nonneighbor codes at a fixed probe are independent and each has
singleton probability `d p q^(d-1)`. A singleton code collides with its
neighbor target. Thus

```
P(the probe resolves | degree d)
 <= (1-d p q^(d-1))^(n-d-1)
 <= exp(-n^(1-c+o(1))).                                         (21)
```

This bound is uniform over the typical degrees in (5). Union over `n`
probes and add the `n exp(-Omega(L^2))` degree exception. Since `c<1`,
the probability of any resolving initial probe tends to zero. One
round therefore cannot guarantee success, proving `T(G)=2`. QED.

## 8. Couplings and arbitrarily thin relative additions

For Corollary 2, take

```
c_-=31/64,                  c_+=1/2+1/(2M-1).
```

Theorem 1 applies to `c_-`. At `c_+`, the reciprocal in (2) is `M-1/2`,
so that theorem gives exactly `M` rounds. Put
`p_-=sqrt(c_- L/n)`, `p_+=sqrt(c_+ L/n)`. Sample `G_-` with parameter
`p_-`, then add each missing edge independently with probability

```
rho=(p_+-p_-)/(1-p_-).
```

The upper marginal is `G(n,p_+)`. A union bound on the two exceptional
events proves (3); independence between the two capture-time events is
neither needed nor asserted. Their finite round counts imply one cop
suffices on both graphs. QED.

For Corollary 3, for each fixed integer `j>=1` set

```
c_-(j)=1/2-1/(64j),       M_j=4j+1,
c_+(j)=1/2+1/(2M_j-1).
```

For each fixed `j`, Theorem 1 and (2) apply. Choose a strictly increasing
sequence of integers `N_j`, tending to infinity, so that for all
`n>=N_j` each of the two conclusions fails with probability at most
`1/j` (the bound for `j=1` is vacuous). Increase the cutoffs if necessary
to ensure the relevant fixed probe lists fit and both edge probabilities
are less than one. Let `j(n)` be the largest `j` with `N_j<=n`, using
arbitrary valid parameters before `N_1`, and use the preceding coupling
with the constants for `j(n)`.

Then `j(n)->infinity`, both coefficients tend to `1/2`, and
`p_+/p_-=sqrt(c_+(j(n))/c_-(j(n)))->1`. With probability at least
`1-2/j(n)`, the two times are exactly `2` and `M_{j(n)}`. This proves
the capture-time assertions. It is a diagonal consequence of fixed-parameter
theorems, not their unjustified substitution at a varying parameter.

Finally let `X=|E(G_-)|` and `Y=|E(G_+)\E(G_-)|`. Their means satisfy

```
E X=binom(n,2)p_- -> infinity,
E Y/E X=(p_+-p_-)/p_- -> 0.
```

Chernoff's inequality gives `X>=E X/2` with high probability. For any
fixed `epsilon>0`, Markov's inequality gives
`P(Y>epsilon E X/2) <= 2 E Y/(epsilon E X)->0`. This proves (4), with
any harmless convention when `X=0`. QED.

## 9. Attribution and evidence boundary

Jones and Kinnersley introduced this full-feedback game in
[arXiv:2609.01745](https://arxiv.org/abs/2609.01745), Section 2.1.
Their Proposition 2.2 gives the path and cycle facts noted above;
Question 6.4 concerns the number of cops, which this work does not settle.
The earlier campaign hierarchy (2) is an explicit external premise for
Corollaries 2 and 3. Its status is a written proof awaiting independent
review, not a formally verified theorem. Theorem 1 is proved here without
using it. The earlier one-round appearance and universal laws are background.

The new mechanism is the combination of globally distinct distance-three
responses and the forest charge controlling all second-probe alternatives
at once. Merely checking a generic second probe for a single first-response
class would not prove the adaptive theorem. Likewise, nonmonotonicity of
the number of cops is not the novelty claim.

The exact checker enumerates finite identification templates, constructs
their forests, checks the edge-charge and exponent inequalities, verifies
finite response and adaptive-strategy semantics, and checks the response
separation identity by rational enumeration. These checks corroborate the
proof and expose bookkeeping errors; they do not supply the asymptotic
quantifiers. There is no formal verification or independent acceptance
claim. Literature searches and bounded graph refreshes support novelty
only relative to the searched sources. The sufficient endpoint `15/32`,
the behavior elsewhere below `1/2`, and explicit rates in Corollary 3
are not claimed optimal or determined.
