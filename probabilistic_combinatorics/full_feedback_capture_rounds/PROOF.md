# Optimal constant capture times in sparse random graphs

All graphs are finite, simple, and labelled. All logarithms are natural.
The probability space is `G(n,p)`, with independent Bernoulli edges. Constants
in this proof may depend on a fixed positive real `c` and a fixed positive
integer `r`. No assertion uniform in growing `r` is made.

## 1. Game and theorem

On a connected graph, a full-feedback probe at `w` with target `x` returns

```
D(w,w)={w},
D(w,x)={b in N(w): dist(b,x)=dist(w,x)-1},  x != w.
```

One cop probes one vertex per round. If the observations determine the
target's current vertex, the cop wins. Otherwise the robber may stay or
move across one edge before the next round. The cop knows the graph and
may choose each probe from the full observation history. The robber may
know the cop's strategy. Let `T(G)` be the least worst-case number of rounds
in which one cop can win, and set `T(G)=infinity` if there is no such
strategy. For definiteness also set `T(G)=infinity` on disconnected graphs.
This convention is immaterial in the regime below.

**Theorem.** Suppose

```
np^2 / log n -> c,                 c > 1/2.
```

For every fixed positive integer `r`:

1. If `c > (r+1)/(2r)`, any `r` distinct labels fixed before the graph is
   sampled form, with probability tending to one, a winning probe schedule.
   In fact every robber walk encounters a round in which its response
   identifies its vertex from that round alone. Thus `T(G)<=r` with high
   probability.
2. If `1/2 < c < (r+1)/(2r)`, with probability tending to one no one-cop
   strategy wins within `r` rounds. This includes strategies chosen after
   seeing the graph and strategies adaptive to all prior responses.

Consequently, if `1/(2c-1)` is not an integer, then

```
T(G) = ceil(1/(2c-1))              with probability tending to one.       (1)
```

At `c=(r+1)/(2r)`, the theorem only implies
`T(G) in {r,r+1}` with probability tending to one. It does not identify
the transition window or the probabilities of these two values.

In particular the full-feedback localization number is one with high
probability throughout `c>1/2`. For `1/2<c<1` every single initial probe
fails, while a bounded number of rounds suffices. The number of cops and
the number of rounds are different parameters: this does not resolve the
general question whether some graph needs more than two full-feedback cops.
No conclusion about the optimal number of cops or rounds when `c<=1/2`
is claimed.

The upper bound uses an explicit fixed schedule. The lower bound produces
two vertex-disjoint robber walks for **every** possible length-`r` probe
sequence, all giving the response `N(w)` to a probe at `w`. The quantifier
over every sequence is what makes that bound valid for adaptive strategies.

## 2. Elementary estimates and exposure convention

Write `q=1-p`, `L=log n`, and `lambda=np^2`. In this regime

```
p=n^(-1/2+o(1)),       np=n^(1/2+o(1)),       np^3=o(1).
```

The following event holds with probability tending to one:

```
all degrees are np+O(sqrt(np) L);
all pair codegrees are at most L^2.                                 (2)
```

The harmless difference between `(n-1)p` and `np` is absorbed in the
degree error. Chernoff bounds give failure at most
`n exp(-Omega(L^2))` for the degree statement. The binomial upper-tail
bound `(e mu/t)^t`, with `mu=O(L)` and `t=L^2`, and a union bound over
pairs give the codegree statement. These estimates also show connectivity:
for a disconnected graph some set of `s<=n/2` vertices has no edge leaving
it, and

```
sum_{s=1}^{floor(n/2)} binom(n,s) q^(s(n-s)) = o(1),
```

since `np/log n -> infinity`.

If a bounded set `Q` of probes has all incident edges exposed, put

```
D_j=N(w_j)\Q,             D=union_j D_j,
S={b in D: b belongs to at least two D_j},
E_j=D_j\S,               T=V\(Q union D).
```

Here the `w_j` enumerate the distinct probes in `Q`. On the local degree
and codegree conditions supplied by (2), uniformly in the exposed edges,

```
|D_j|=np+O(sqrt(np)L+|Q|),       |S|=O(L^2),
|E_j|=np+O(sqrt(np)L+L^2),     |T|=n-O(np).
```

In particular, after deleting any bounded number of vertices from `E_j`,

```
q^|E_j| = n^(-c+o(1)),
P(Bin(|E_j|-O(1),p)<=1) = n^(-c+o(1)).                             (3)
```

The errors are uniform over all incident-edge exposures satisfying these
bounds. Indeed `p sqrt(np)L`, `pL^2`, and `np^3` tend to zero; the binomial
tail in (3) adds only a factor `O(L)`. All edges with both ends outside
`Q` remain independent Bernoulli variables after this exposure. We never
condition on a global event involving those unexposed edges when asserting
their independence.

## 3. A small cover of ambiguous vertices at a fixed probe

A vertex is *ambiguous at w* if another vertex gives exactly its response
to `w`. Fix a probe `w`, expose its neighborhood `D_w`, and put
`d=|D_w|`, `T_w=V\(D_w union {w})`, `m=|T_w|`. For `x in T_w` set
`C_w(x)=N(x) intersect D_w`. Define

```
A_w={x in T_w: |C_w(x)|<=1},
H_w={b in D_w: C_w(y)={b} for some y in T_w}.
```

**Lemma 1.** If `c>1/2`, then with probability tending to one all ambiguous
vertices at this fixed `w` lie in `A_w union H_w`.

**Proof.** Conditional on `D_w`, the codes `C_w(x)` are independent random
subsets of `D_w`. On a typical degree, the expected number of equal pairs
of codes of size at least two is at most

```
binom(m,2) q^(2d)
 * [(1+(p/q)^2)^d - 1 - d(p/q)^2]
 = n^(1-2c+o(1)) = o(1).                                          (4)
```

For the equality estimate, `d(p/q)^2=O(np^3)=o(1)`, so the bracket is
`O((np^3)^2)`. Thus these codes are pairwise distinct with high probability.
Also, with high probability every code has size at most `L^2`, by (2).

We must keep distance-three responses separate from these small codes;
it is not correct simply to assume that every zero code returns all of
`D_w`. Let `M_w` count pairs `(z,b)` such that `z in T_w`, `C_w(z)` is
empty, `b in D_w`, and no `y in T_w\{z}` satisfies `b~y~z`. Independence
of the relevant edges gives the exact conditional identity

```
E(M_w | D_w) = m d q^d (1-p^2)^(m-1)
              = d n^(1-2c+o(1)).                                 (5)
```

By Markov's inequality, `M_w<d/2` with probability tending to one. On
this event every zero-code target has a length-three path from `w` and
its response contains more than `d/2` neighbors of `w`: each successful
`b~y~z` supplies one. Its distance is exactly three because its code is
empty and it is not adjacent to `w`. Since `L^2<d/2` for large `n`, these
responses cannot equal any nonzero code.

The probe itself has the unique response `{w}`. Its neighbors give
distinct singleton responses; a neighbor can collide only with a
singleton code and therefore belongs to `H_w`. Codes of size at least
two are distinct by (4), and cannot collide with a zero-code response.
Every remaining target belongs to `A_w`. This proves the lemma. QED.

The lemma holds simultaneously at any fixed bounded collection of probes.
For `r` distinct labels fixed before sampling, with high probability we
also have:

```
Q is independent;
2 <= |D_i intersect D_j| <= L^2  for i != j;
no vertex outside Q belongs to three of the D_i.                    (6)
```

The failure probabilities of the extra assertions are respectively
`O(p)`, `n^(-c+o(1))+o(1)`, and `O(np^3)=o(1)`. In the middle assertion,
the intersection for a fixed pair is binomial with mean asymptotic to
`lambda`. On (6) and the events in Lemma 1, every probe in `Q` gives a
unique response to every other probe: its code has at least two entries.
In particular no ambiguous walk vertex, and no singleton-code witness
used below, belongs to `Q`.

## 4. Counting unresolved walks, including repeated vertices

Take `r` distinct fixed probes `w_1,...,w_r`. If the cop has not won from
a globally unique response in any of these rounds, the robber's positions
form a walk `x_1,...,x_r` with `x_i` ambiguous at `w_i`. Stays are allowed.
On the preceding high-probability events, choose for each `i` one of:

```
type A: x_i in A_{w_i};
type H: x_i in H_{w_i}, with a witness y_i satisfying C_{w_i}(y_i)={x_i}.
```

For type H the edge `x_i y_i` is required and `x_i in D_i`. Let `h` be
the number of H positions. Identify any repeated vertices among the
`r+h` formal symbols `x_i,y_i`, obtaining a finite template with `v`
vertices. Its required graph consists of the walk edges between unequal
successive positions and the H witness edges, with duplicate edges
counted once. Let it have `e` edges. An H loop is impossible and may be
discarded. The required graph is connected, so

```
v <= r+h,           e >= v-1,
v-(h+e)/2 <= (r+1)/2.                                             (7)
```

Expose only the edges incident to `Q`, and restrict to their regular
configurations (2), (6). There are only finitely many templates for fixed
`r`. In a template, a vertex with one H requirement must be labelled in
one `D_i`, giving at most `n^(1/2+o(1))` choices; one with two such
requirements has at most `L^2=n^o(1)` choices. Three requirements are
impossible by (6). A vertex with none has at most `n` choices. Thus the
number of possible injective labelings is at most

```
n^(v-h/2+o(1)).                                                   (8)
```

For each labeling let `U` be its at most `2r` vertices, all outside `Q`.
For each round define the low-code target `t_i=x_i` for type A and
`t_i=y_i` for type H. The necessary code condition implies that `t_i`
has at most one neighbor in `E_i\U`. These reservoirs are pairwise
disjoint and avoid all template vertices. Consequently the edge sets
used for these `r` tests are disjoint, even if some `t_i` coincide. They
are also disjoint from all required graph edges, whose endpoints lie
in `U`. By (3), the probability of the tests and the required edges is
at most

```
p^e n^(-cr+o(1)) = n^(-e/2-cr+o(1)).                              (9)
```

Combining (7)--(9) and summing the finitely many templates bounds the
conditional probability of any covered walk by

```
n^((r+1)/2-cr+o(1)).                                              (10)
```

When `c>(r+1)/(2r)` this tends to zero, uniformly over the regular
exposures. Adding the exceptional probabilities from Lemma 1 and (6)
proves the upper half of the theorem. This argument includes stationary
walks, repeated vertices, reused witnesses, and edges shared by a walk
and a witness. Treating their appearances as independent edges would
not justify (10); the connected-template inequality is needed.

## 5. Uniform distance-three layers for any probe sequence

Fix `r` and `1/2<c<(r+1)/(2r)`. We prove a statement holding simultaneously
for every ordered length-`r` sequence `w_1,...,w_r`, allowing repetitions
and edges between probes.

First fix one such sequence, let `Q` be its distinct probes, and expose
all edges incident to `Q`. Use the sets `D_j,D,S,E_j,T` from Section 2,
where `j` indexes distinct probes. Assume only the local degree/codegree
bounds of that section. Put

```
eta=(2c-1)/(4c),              (1-eta)c > 1/2.
```

Partition `T`, deterministically from these exposed edges, into a buffer
`P` with `|P|=(1-eta+o(1))n` and `2r` disjoint blocks `W_{i,s}`, for
`1<=i<=r`, `s in {0,1}`, each of size `(eta/(2r)+o(1))n`. Rounding by a
bounded number of vertices is irrelevant. The two values of `s` will
give disjoint robber walks.

Expose all edges between `D` and `P`. Choose a small fixed `delta>0` such
that `(1-delta)(1-eta)c>1/2`. Except with probability
`exp(-n^(1/2+o(1)))`, simultaneously for every `b in D`,

```
|N(b) intersect P| >= (1-delta)|P|p.                              (11)
```

This is a Chernoff bound and a union bound over `|D|=O(np)` vertices.
The bound and its constants are uniform over the regular incident-edge
exposures.

For a candidate vertex `x` in one of the blocks, define `F_x` to mean
that for every `b in D` there is `z in P` with `b~z~x`. Conditional on
the just-exposed edges and (11), only the edges from `x` to `P` are used
to decide `F_x`. A union bound gives, uniformly in `x`,

```
P(F_x fails) <= |D| q^((1-delta)|P|p)
              = n^(1/2-(1-delta)(1-eta)c+o(1)) = o(1).              (12)
```

For distinct candidates these tests use disjoint edges. They are also
independent of all candidate-to-`D` edges and of all edges between
candidates.

For a vertex in the block belonging to round `i`, let `j(i)` index its
probe in `Q`. Retain `x` in `Z_{i,s}` if `F_x` holds and

```
N(x) intersect S is empty;
N(x) intersect E_{j(i)} is empty;
N(x) intersect E_l is nonempty for every l != j(i).                 (13)
```

All these decisions are independent across candidates. Their retention
probabilities, uniformly over the current regular exposure, are

```
alpha_i = P(F_x) q^|S| q^|E_{j(i)}|
                       product_{l != j(i)} (1-q^|E_l|)
        = n^(-c+o(1)).                                            (14)
```

Here `p|S|=o(1)`. Conditional on all retained sets, all edges between
candidate blocks are still independent Bernoulli variables.

Every retained `x in Z_{i,s}` gives exactly `N(w_i)` as its full response.
To check this, `x in T` has no neighbor in `Q`, and (13) eliminates all
common neighbors of `w_i,x` outside `Q`. Thus their distance is at least
three. Every external neighbor `b in D_{j(i)}` is at distance two from
`x` by `F_x`. If a neighbor of `w_i` is another probe `w_l`, the last
condition of (13) supplies a length-two path `w_l-y-x` with `y in E_l`.
The typical positive external degree supplies a length-three path from
`w_i` to `x`, so its distance is exactly three and every neighbor of
`w_i` lies on a shortest path. This also explains why the nonempty-code
conditions in (13) are necessary when probes are adjacent. Repeated
probes cause no problem: `j(i)` merely repeats.

## 6. Layered paths with a stretched-exponential failure bound

Set

```
a_i=(i+1)/2-ic,           1<=i<=r.
```

Our assumptions give `a_1>=...>=a_r>0`. From (14) and Chernoff bounds,
except with probability `exp(-n^(1-c+o(1)))`, all `2r` retained layers
have size `n^(1-c+o(1))`. The error exponents and the `o(1)` terms can be
chosen uniformly over all exposures satisfying the previous bounds.

For each `s`, start with `R_{1,s}=Z_{1,s}` and inductively let

```
R_{i,s}={x in Z_{i,s}: x has a neighbor in R_{i-1,s}}.
```

Expose edges between successive layers only as needed. Conditional on
the previous exploration and the retained sets, the exact law is

```
|R_{i,s}| ~ Bin(|Z_{i,s}|, 1-q^|R_{i-1,s}|).                      (15)
```

The vertices of all layers are disjoint, so none of these edges was
previously exposed. Since `|R_{i-1,s}|<=|Z_{i-1,s}|` and `c>1/2`,
`p|R_{i-1,s}|=o(1)`. Therefore the mean in (15) is asymptotic to
`|Z_{i,s}| p |R_{i-1,s}|`. Iterated Chernoff bounds now give

```
|R_{i,s}|=n^(a_i+o(1)),
```

with failure at most `exp(-n^gamma)` for some fixed `gamma>0` depending
only on `c,r`, uniformly in the regular exposures. To make the polynomial
slack explicit, choose a fixed sufficiently small `epsilon>0`, bracket
each layer size between `n^(1-c-epsilon)` and `n^(1-c+epsilon)`, and
bracket `p` between `n^(-1/2-epsilon)` and `n^(-1/2+epsilon)`. At each
of the at most `r-1` steps, a factor two in the Chernoff bracket and the
bound `ps/2<=1-q^s<=ps` are absorbed in another `n^epsilon`. Choose
`epsilon<a_r/(10r)`. Every conditional mean then exceeds
`n^(a_r/2)` for large `n`; the preceding failure bound follows, for
example with any fixed `gamma<a_r/2`, also reduced below the exponents
in the buffer and initial-layer estimates if necessary.

Both final reachable sets are nonempty with that failure bound. Tracing
back one path in each produces two walks of length `r-1`, one in the
`s=0` blocks and one in the `s=1` blocks. The walks are vertex-disjoint
and at round `i` both give precisely the response `N(w_i)`.

For each fixed probe sequence, conditional on any regular incident-edge
exposure, the construction fails with probability at most
`exp(-n^gamma)`, after decreasing `gamma` to absorb constant factors.
There are at most `n^r` ordered sequences, including repeats. On the
global regular event (2), every one has a regular local exposure.
Consequently

```
P(some sequence lacks the two walks AND (2))
 <= n^r exp(-n^gamma) = o(1).                                     (16)
```

More formally, for each sequence intersect its failure event with its
*local* regular event before applying the conditional estimate; the
global event is contained in every local event. We are not conditioning
the independent-edge calculation on global regularity. Adding the
`o(1)` failure probability of (2) proves the uniform statement.

## 7. From the uniform transcript to an adaptive lower bound

Consider any proposed one-cop strategy, even one chosen after inspecting
the graph. Follow its hypothetical branch in which a probe at `w` always
returns `N(w)`. It determines a length-`r` probe sequence. If the strategy
purports to stop earlier, extend that hypothetical sequence arbitrarily.
The simultaneous property from (16) supplies two vertex-disjoint walks
realizing the entire response sequence. At each round their current
positions are distinct, their moves are legal, and their full histories
agree. Thus the cop cannot have uniquely determined the current vertex
at any of these rounds. This contradicts winning within `r` rounds.

This is an information-set argument, not an assertion that the robber
can teleport between independently chosen layer vertices. Each of the
two certificates is an actual walk. It also matches the game's bounded,
guaranteed-win convention; allowing private random guesses does not
constitute a guarantee against the omniscient robber.

This proves the lower half. Applying the two halves with the consecutive
integers around `1/(2c-1)` proves (1). At an integer reciprocal, apply
them with `r-1` and `r+1` (with the trivial lower bound one when `r=1`)
to obtain the stated two-value bracket. QED.

## 8. Validation, prior work, and limits

The proof is ordinary unformalized mathematics. Its probabilistic inputs
are elementary Chernoff/Markov bounds, independence under explicit edge
exposure, and union bounds. The asymptotic theorem is not a computer-assisted
claim and is not inferred from finite examples.

`verify.py` checks response definitions by two independent shortest-path
computations, checks the deterministic ambiguity-cover implication,
compares fixed-schedule information sets with literal robber-walk histories,
audits exact adaptive game recursion on known controls, replays positive
and negative walk certificates, checks finite
quotient templates including stays and shared witness edges, and checks
the elementary binomial-layer formula by exact enumeration. See the README
and EXPECTED.json for the exact scope and commands. These checks cannot
certify an omitted analytic estimate or replace independent review.

Jones and Kinnersley introduced the game and its full-feedback variant in
[The directional localization game on graphs, arXiv:2609.01745v1](https://arxiv.org/abs/2609.01745).
Their Section 2.1 specifies the response and movement conventions used
here; Section 6 asks whether more than two cops are ever necessary in
the full-feedback model. Our theorem concerns optimal **rounds with one
cop** in a random graph and leaves that general question open.

Earlier campaign results establish the
[universal one-round phase diagram](https://github.com/helgithorskarp/math_results/tree/main/probabilistic_combinatorics/full_feedback_phase_diagram)
and the
[sparse existence window for a resolving initial probe](https://github.com/helgithorskarp/math_results/tree/main/probabilistic_combinatorics/first_full_feedback_resolvers).
Those results do not control moving robber trajectories. The present
proof is self-contained and needs neither asymptotic theorem as a lemma.
The new mechanism is the unresolved-walk template bound together with a
buffer construction giving a uniformly valid indistinguishable transcript.

Bounded graph-neighborhood inspection and targeted live primary-literature
searches on 2026-09-22 found no matching adaptive capture-time hierarchy.
This is search-relative novelty, not a priority guarantee. Critical-window
laws, the regime `c<=1/2`, and round bounds with `r` growing with `n` remain
outside this contribution. No independent peer acceptance or formal
verification is claimed.
