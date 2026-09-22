# The sparse appearance window for full-feedback resolving probes

All logarithms are natural. Graphs are finite, simple, and labelled. In
`G(n,p)` distinct edges are independent Bernoulli variables of parameter `p`.
Limits are as `n` tends to infinity. Constants implicit in error terms may
depend on a fixed band bound `C` and on a fixed number of designated probes.

## 1. Statement and scope

For a connected graph, the response to a probe at `v`, with target `x`, is

```
D(v,v)={v},
D(v,x)={u in N(v): dist(u,x)=dist(v,x)-1},  x != v.
```

A **resolving probe** is a vertex whose responses to all targets are distinct.
Let `R` count these vertices, and let `R_2,R_3` count those of eccentricity
two and three respectively. Set all these counts to zero on disconnected
graphs. This convention records the connected-graph localization question.

Write

```
L=log n,       lambda=np^2,
u=n exp(-lambda),       v=n lambda exp(-lambda),
a=n exp(-u-v),          theta=a(1+u).
```

**Theorem 1 (uniform sparse-band law).** For every fixed `C<infinity`, uniformly
over `|lambda-L|<=C`,

```
E R = (1+o(1)) theta,
P(R>0) = 1-exp(-theta)+o(1).
```

If `theta -> infinity` in this band, then `R/theta -> 1` in probability.
If `theta -> 0`, then `P(R>0)->0`. If `theta -> t` for `0<t<infinity`, then

```
(R_2,R_3) -> (Poisson(t/2), Poisson(t/2)), independently,
P(R=R_2+R_3)->1.
```

**Corollary 2 (critical window).** If

```
np^2 = L+s/L+o(1/L),       s in R,
```

then `R_2,R_3` converge to independent Poisson variables, each of mean
`exp(s-1)`. Consequently

```
R -> Poisson(2 exp(s-1)),
P(R>0) -> 1-exp(-2 exp(s-1)).
```

Equivalently, at `np^2=L+(1-log 2+c)/L+o(1/L)`, the total mean is `exp(c)`.
The width in `p` is of order `1/(sqrt(n) (log n)^(3/2))`.
The limiting probability is uniform for `s` in a compact interval. More
generally, if `s=s_n` tends to positive or negative infinity with
`|s|=o(sqrt(L))`, the probability tends to one or zero respectively.

This is a complete appearance-window statement for existence of a successful
*single initial probe*. It does not identify the first hitting time in a
coupled edge-addition process, assert monotonicity, determine an adaptive
multi-round localization threshold, or settle whether the adaptive
full-feedback localization number can exceed two. In particular, absence of
a resolving probe need not imply that one adaptive probe per round loses.

The earlier two-hop certificate requires every nonneighbor to have at least
two common neighbors with the probe. It captures `R_2` asymptotically here,
and misses the equally frequent `R_3` vertices. The previously published
universal-probe threshold is on the different scale
`np^2=2 log n+log log n+O(1)`.

## 2. Two-hop defects and a deterministic comparison

Fix a vertex `w`, put `D=N(w)`, `d=|D|`, and `T=V\(D union {w})`, `m=|T|`.
For `x in T` write `C(x)=D intersect N(x)`. Define

```
X_w = #{x in T: |C(x)|=1},
Z_w = #{x in T: |C(x)|=0},
M_w = {X_w=0},
F_{w,k} = {X_w=0, Z_w=k},  k=0,1,
F_w=F_{w,0} union F_{w,1}.
```

Every resolving probe satisfies `M_w`: a singleton code `{b}` is the same
response as the neighbor `b`. This is necessary without any diameter
assumption.

Suppose `d>=2`. Define the auxiliary event `H_w` by three requirements:

1. All codes of size at least two are distinct, and none equals `D`.
2. For each zero-code target `z` and each `b in D`, there exists
   `y in T` with `b~y~z`.
3. There is at least one target at distance two, unless `Z_w>0`.

On `M_w intersect H_w`, every target is at distance at most three. Each
zero-code target is at distance exactly three and returns precisely `D`;
every target with nonzero code returns its code. Thus

```
w resolves  iff  Z_w<=1.
```

On this event, `F_{w,0}` gives eccentricity two and `F_{w,1}` gives
eccentricity three. Requirement 3 only excludes a universal vertex when
recording the eccentricity-two mark. In our sparse band, `d<n-1` and
`m` is of order `n`; if `X_w=0` and `Z_w<=1`, requirement 3 is automatic
for large `n`. When `Z_w>=2`, it is immaterial to the equivalence.

We will prove a relative approximation, not just an error that tends to zero:
for each fixed `C`, uniformly in its band,

```
P(1_{w resolves} != 1_{F_w}) = o(exp(-u-v)),                    (1)
P(1_{w resolves, ecc(w)=k+2} != 1_{F_{w,k}})
                              = o(exp(-u-v)),  k=0,1.         (2)
```

The right side is of order `o(1/n)` in the critical window. An unconditioned
high-probability diameter or collision estimate would not suffice.

## 3. The one-probe relative approximation

Condition on `N(w)=D`. The `m` codes are independent random subsets of `D`,
and a particular set of size `j` has probability `p^j q^(d-j)`, where
`q=1-p`. Edges inside `T` remain independent Bernoulli variables, independent
of all these codes. Put

```
b_0=q^d,            b_1=d p q^(d-1).
```

The exact identities are

```
P(M_w | D) = (1-b_1)^m,
P(F_{w,0} | D) = (1-b_0-b_1)^m,
P(F_{w,1} | D) = m b_0 (1-b_0-b_1)^(m-1).                    (3)
```

For a degree in the range

```
|d-np| <= sqrt(np) L + 2,                                    (4)
```

elementary expansions, uniformly in the band, give

```
q^d=exp(-lambda)(1+o(1/L)),
m b_0=u+o(1),             m b_1=v+o(1).                      (5)
```

Indeed the error in the logarithm of the first expression is
`O(p sqrt(np) L + np^3 + p)`, whose product with `L` tends to zero.
Also `m=n-O(np)` and `pL=o(1)`. Since `v=O(L)`, (3) now gives

```
P(M_w | D)=(1+o(1)) exp(-v),
P(F_{w,k} | D)=(1+o(1)) exp(-u-v) u^k,  k=0,1.               (6)
```

Chernoff's inequality makes the probability of failure of (4)
`exp(-Omega(L^2))`, smaller than every fixed inverse power of `n`.
This is negligible relative to all the probabilities in (6), because
`u` stays in a compact subinterval of `(0,infinity)` and `v=O(L)`.

Conditional on `D,M_w`, the codes are still independent, with their original
distribution conditioned not to be singletons. The expected number of pairs
of equal codes of size at least two is at most

```
binom(m,2) q^(2d)/(1-b_1)^2
  * [(1+(p/q)^2)^d - 1 - d(p/q)^2] = O(L^3/n)=o(1).           (7)
```

To see the order, `m^2 q^(2d)=O(1)` and `d(p/q)^2=O(np^3)
=O(L^(3/2)/sqrt(n))`. The expected number of full codes is at most
`m p^d/(1-b_1)=o(1)`.

It remains to control the actual response of a zero-code target. For
`b in D` let

```
S_b={y in T: b in C(y)}.
```

Under the same conditioning, `|S_b|` is binomial with `m` trials and success
probability

```
beta = p(1-q^(d-1))/(1-b_1) = (1+o(1))p.                    (8)
```

Consequently, a union bound and Chernoff's inequality give

```
P(min_{b in D}|S_b| < 0.9 np | D,M_w)
       <= d exp(-Omega(np))=o(1).                           (9)
```

Every `S_b` is disjoint from the zero-code targets. After all codes have been
exposed, the edges from any zero-code target `z` to `S_b` are untouched edges
inside `T`. Thus, on the complement of the event in (9),

```
P(no edge from z to S_b | all codes) <= q^(0.9 np).
```

The conditional mean of `Z_w` is
`m b_0/(1-b_1)=O(1)`. A further union bound, averaged over the codes, bounds
the chance that some required two-edge path is absent by

```
O(d q^(0.9 np)) = n^(-0.4+o(1))=o(1).                     (10)
```

This argument does not assume independence between different missing-path
events. Repeated edges in those tests are harmless to the union bound.

Equations (7)--(10) prove the deterministic comparison with conditional
failure probability `o(1)` under `D,M_w`. For the eccentricity marks, a
universal vertex is already excluded by (4); when `Z_w<=1` there are
distance-two targets because `m` tends to infinity. Every successful probe
is in `M_w`, and the comparison on the auxiliary event includes connectivity.
Multiplying by `P(M_w | D)`, using (6), and then averaging proves (1)--(2).
It also gives

```
P(w resolves, ecc(w)>=4)=o(exp(-u-v)).                      (11)
```

No asymptotic independence between different candidate probes has yet been
used or inferred from the one-probe calculation.

## 4. Joint rare events for finitely many probes

Fix distinct probes `w_1,...,w_r`, with `r` independent of `n`, and marks
`k_i in {0,1}`. We prove, uniformly in the band,

```
P(intersection_i F_{w_i,k_i})
   = (1+o(1)) exp(-r(u+v)) u^(sum_i k_i).                  (12)
```

Expose all edges incident with the probe set `Q={w_1,...,w_r}`. Write

```
D_i=N(w_i)\Q,    B=union_i D_i,
T=V\(Q union B),    M=|T|.
```

Call this initial exposure regular if

```
||D_i|-np| <= sqrt(np)L+2r   for every i,
|D_i intersect D_j| <= L^2   for every i!=j.                (13)
```

The failure probability is smaller than every inverse power of `n`.
For the first condition this follows as in (4). For the second, an overlap
is binomial with mean `(n-r)p^2=O(L)`; the standard upper tail bound
`P(Bin(N,t)>=h)<=(eNt/h)^h` at `h=L^2` is superpolynomially small.
Since the target in (12) is bounded below by an inverse power of `n`,
irregular exposures may be discarded even in this rare-event calculation.

For each `x in T` and each `i`, the common-neighbor code is exactly
`N(x) intersect D_i`: `x` has no neighbor in `Q`. The vectors of code sizes,
as `x` varies in `T`, are independent and identically distributed. Within
one vector they need not be independent.

Let `A_i` mean that the `i`th code is empty, and `B_i` that it is a
singleton. The one-coordinate probabilities are

```
P(A_i)=q^(d_i),       P(B_i)=d_i p q^(d_i-1),   d_i=|D_i|.
```

For two neighborhoods of sizes `d_i,d_j` and overlap `h`, direct separation
of their common and exclusive coordinates gives the exact identity

```
P(|C_i|<=1, |C_j|<=1)
 = q^(d_i+d_j-h)
   * [(1+(d_i-h)p/q)(1+(d_j-h)p/q)+h p/q].                 (14)
```

On a regular exposure, (14) is `O(L^2/n^2)`: here `hp=o(1)`,
`d_i p=lambda+o(1/L)`, and `lambda=L+O(1)`.

Encode a single outside target by the polynomial

```
f(z_1,...,z_r)
 = E[ 1_{no B_i occurs} product_{i:A_i occurs} z_i ]
 = sum_{J subset [r]} c_J product_{i in J} z_i.
```

A union bound for intersections in (14) yields, uniformly,

```
c_empty = 1-sum_i[P(A_i)+P(B_i)] + O(L^2/n^2),
c_{ {i} } = P(A_i)+O(L^2/n^2),
0 <= c_J <= O(L^2/n^2),  |J|>=2.                         (15)
```

Since `M=n-O(np)`, the expansions in (5) give

```
c_empty^M = (1+o(1)) exp(-r(u+v)),
M c_{ {i} } = u+o(1).                                    (16)
```

The outside-target event with no singleton codes and exactly `k_i` empty
codes in coordinate `i` has probability `[product z_i^k_i] f(z)^M`.
Let `K={i:k_i=1}`. An exact way of taking this coefficient is to partition
`K` into nonempty blocks, assigning one distinct outside target to each
block. The singleton-block partition contributes

```
(M)_{|K|} c_empty^(M-|K|) product_{i in K} c_{ {i} }
   = (1+o(1)) exp(-r(u+v)) u^|K|.                         (17)
```

Every other partition has a block of size at least two. Its contribution,
divided by `c_empty^M`, contains a factor `M c_J=O(L^2/n)=o(1)`;
all remaining factors are bounded. There are only finitely many partitions.
This proves (17) for the full coefficient. In particular the probability
of the outside event with *at most* one empty code per probe and no
singleton codes is `O(exp(-r(u+v)))`, uniformly in a regular exposure.
This multiplicative control is why the intersection error in (14) cannot
simply be union-bounded without using the polynomial.

We must still restore targets in `B union Q`.

For `x in B\D_i`, with `x` not a probe, its common-neighbor count with `w_i`
includes an independent `Bin(d_i,p)` count from the unexposed edges between
`x` and `D_i`. Contributions from other probes only increase the count.
Thus, conditional on any regular initial exposure, the probability that
one such target has code size at most one is `O(L/n)`. There are `O(np)`
such targets for each of the fixed `r` probes, so their total failure
probability is `O(pL)=o(1)`. These tests use only edges inside `B`, whereas
the outside event uses only edges between `B` and `T`. They are conditionally
independent. Multiplying their failure probability by the preceding uniform
outside-event bound shows an error `o(exp(-r(u+v)))`.

A different probe `w_j` is an offending target only if `w_i,w_j` are
nonadjacent and their common-neighbor count is at most one. This event is
already decided in the initial exposure and has unconditional probability
`O(L/n)`, by the binomial codegree formula (it suffices to count neighbors
outside `Q`). The same *uniform* conditional bound on the outside event
makes its contribution `o(exp(-r(u+v)))` after averaging over exposures.

If no inside target is offending, the outside marks are the full marks.
Conversely, a full marked event always implies the outside event with
at most one zero per probe. The error estimate therefore applies in both
directions, including when an inside zero would change a mark. This proves
(12) with every target restored.

## 5. Moments, Poisson limits, and the uniform law

Let `Y_k=sum_w 1_{F_{w,k}}`, `k=0,1`, and `Y=Y_0+Y_1`. For fixed
nonnegative integers `b,c`, (12) implies

```
E[(Y_0)_b (Y_1)_c] = (1+o(1)) a^(b+c) u^c,                (18)
```

where `(x)_j=x(x-1)...(x-j+1)`. Roots shared between different marks
contribute zero because `F_{w,0}` and `F_{w,1}` are disjoint. All remaining
ordered choices are the distinct-root cases of (12).

In particular `E Y=(1+o(1))theta` and
`E[(Y)_2]=(1+o(1))theta^2`. The one-root approximation gives

```
E|R-Y|=o(a),
E|R_2-Y_0|+E|R_3-Y_1|=o(a),
E(R-R_2-R_3)=o(a).                                       (19)
```

The last difference counts all other eccentricities. Eccentricity-one
resolvers require a universal vertex and have superpolynomially small
expectation in this band; eccentricities at least four are covered by (11).
Since `u` is bounded above and below, `a` and `theta` are comparable.
This proves the expectation assertion of Theorem 1.

If `theta` tends to infinity, (18) for total order at most two and
Chebyshev's inequality show `Y/theta -> 1`. Equation (19) and Markov's
inequality transfer this to `R`. If `theta` tends to zero, the expectation
assertion gives absence with high probability.

If `theta -> t` in `(0,infinity)`, write `lambda=L+d_n`, with bounded `d_n`.
Then

```
log theta = L-e^(-d_n)(L+d_n+1)+log(1+e^(-d_n)).           (20)
```

Boundedness of this expression forces `d_n -> 0`; otherwise the coefficient
of `L` stays bounded away from zero along a subsequence. Therefore `u -> 1`
and `a -> t/2`. The joint factorial moments (18) converge to
`(t/2)^(b+c)`, those of two independent Poisson variables. The factorial
moment theorem applies; Poisson laws are moment-determinate, and the bounds
on every fixed higher moment supply uniform integrability. One may also
apply the same moments to each nonnegative linear combination and use the
ordinary method of moments. Thus `(Y_0,Y_1)` has the claimed joint limit.
Now (19) is `o(1)`, so with probability tending to one the integer counts
agree with their actual marked counterparts. This proves the marked claim
and the probability limit `1-exp(-t)`.

Finally the probability formula is uniform over the entire band. Otherwise
a sequence with a fixed error would have a subsequence on which `theta`
converges in the extended interval `[0,infinity]`. Each of the three cases
just proved contradicts that error. This proves Theorem 1.

For the critical scaling, substitute `d_n=s/L+o(1/L)` in (20), obtaining

```
u=1+o(1),       v=L-s+o(1),
a=exp(s-1)+o(1),        theta=2 exp(s-1)+o(1).
```

This proves Corollary 2. The same calculation has error
`O((s^2+|s|+1)/L)+o(1)` when `|s|=o(sqrt(L))`; hence the stated one-sided
limits follow from Theorem 1. For this last claim, the perturbation
`o(1/L)` in `lambda` must still hold along the chosen sequence.

## 6. Evidence boundary

The theorem is the probabilistic proof above. The accompanying exact checker
does not certify an infinite asymptotic limit. It audits the full response by
independent shortest-path calculations, the deterministic comparison, exact
one-probe finite probabilities, overlapping-neighborhood row probabilities,
and the coefficient/partition calculation used for joint rare events.

No numerical simulation, independence assumption across probes, unpublished
dataset, solver, or computational extrapolation is used in the proof.
Classical Chernoff bounds and the factorial-moment criterion are standard
probabilistic tools. Definitions and prior work are credited in LITERATURE.md.
