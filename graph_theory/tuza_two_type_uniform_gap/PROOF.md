# A uniform Tuza gap for two-neighborhood split graphs

All graphs are finite, simple, and unweighted. Write `tau(G)` for the
minimum number of **edges** meeting every triangle, and `nu(G)` for the
maximum number of edge-disjoint triangles.

## The theorem

Let `V(G)=C disjoint-union I` be a specified split partition, where `C` is
a clique of order `k>=3` and `I` is independent. After discarding vertices
of `I` of degree at most one, suppose there are at most two distinct
neighborhoods in `C`. There is no bound on their multiplicities.

**Theorem.** There are an explicitly constructible triangle edge cover `D`
and triangle packing `P` such that

    2|P| - |D| >= k^2/228 - k/2 - 1/4.                     (1)

Consequently the same lower bound holds for `2 nu(G)-tau(G)`. In particular:

1. Tuza's inequality holds for every such graph with `k>=113`.
2. If a counterexample exists in this class, one exists with `k<=112`
   and at most `334` triangle-active vertices, including the clique.
3. Uniformly over this class,

       tau(G) <= (227/114) nu(G) + k/2 + 1/4.

The last assertion gives a strict asymptotic gap below two as `k` grows.
The constants are convenient, not claimed optimal. The theorem does
**not** settle all two-neighborhood split graphs, let alone all split
graphs or the general Tuza conjecture. No finite census is used.

The proof consists of a multiplicity cap, a modular-sum packing, and a
one-variable comparison. In particular, it does not depend on a theorem
about optimal clique triangle packings, a design existence theorem, or
the preceding bipartite-clique-core normal form.

## 1. A neighborhood-size multiplicity cap

Suppose a neighborhood `S` has size `s>=2` and multiplicity `M`. Replacing
`M` by `min(M,s-1)` leaves the triangle cover number unchanged. This can
be done for every type in an arbitrary split graph, not only two types.

To prove it, monotonicity gives one direction. For the other, consider
a minimum cover of the capped graph and its surviving triangle-free
clique core `F`. We may make the retained neighborhood identical at all
vertices of a given type: choose a largest independent set `A` of `F[S]`
and retain precisely the spokes to `A`. This cannot increase the cover.

If the type was capped, delete all edges of `F[S]` and restore all of its
spokes. Since `A` is independent in `F`, each edge of `F[S]` has an endpoint
in `S\A`, so

    e(F[S]) <= (s-1)|S\A|.

The newly deleted clique edges therefore cost no more than the restored
spokes at the `s-1` capped copies. Deleting further clique edges cannot
create triangles or invalidate the retained sets of other types. Repeat
for all capped types, and then add the missing copies with all their
spokes. The cover has not grown. This proves the cap, including simultaneous
capping. Inactive types can be discarded for free.

Henceforth use capped multiplicities `m<=s-1` and `n<=t-1` for neighborhoods
`S,T`, of sizes `s,t`. An absent type may be represented by the empty set
and multiplicity zero. Equal neighborhoods are also harmless if their
copies have been separated into two groups. Any cover constructed on the
capped graph can be lifted without increasing its size by the same repair;
any packing of the capped graph embeds in the original graph.

Put

    c = |S intersect T|,  u = |S union T| = s+t-c,
    x = m/s,  y = n/t,
    E = ms+nt,
    H = (x s^2 + y t^2 - xy c^2)/2,
    delta = 2H/k^2.

A fraction belonging to an empty type is defined to be zero. Always
`0<=x,y<=1`. The case `u=0` is handled separately where division by `u`
would occur.

## 2. A centered packing with at least `H-k/2` triangles

Label the vertices of `S` by residues `0,...,s-1`. Give its edge `{i,j}`
color `i+j mod s`. Every color class is a matching, since a color and
one endpoint determine the other endpoint. Choose `m` distinct colors,
and assign each chosen matching to a different `S`-type independent
vertex, forming centered triangles. Do the same independently for `T`
with `n` of its `t` colors.

For uniformly selected color sets, each `S` edge is chosen with probability
`x`, and each `T` edge with probability `y`. A common edge is chosen twice
with probability `xy`, since the two choices are independent. Delete one
of its two triangles whenever this happens. All remaining triangles are
edge-disjoint: triangles at a common center came from a matching, different
centers have different spokes, and their base edges are now distinct.
The expected number `h` is

    x binom(s,2) + y binom(t,2) - xy binom(c,2)
      = H - (xs+yt-xyc)/2.

The expression `xs+yt-xyc` is nondecreasing in each of `x,y` on `[0,1]^2`,
as its partial derivatives are `s-yc>=0` and `t-xc>=0`. Thus it is at most
`s+t-c=u<=k`. Some choice therefore gives

    h >= H-k/2.                                            (2)

### Deterministic choice of the colors

This averaging argument needs no random search. Score an `S` color class
`M` by `|M|-y|M intersect E(K_T)|`, and choose the `m` highest-scoring
classes. Their total score is at least the average total for `m` classes.
Once these classes are fixed, score each `T` class by its number of base
edges not already used, and choose the `n` highest-scoring classes.
This second choice is again at least its conditional average. All scores
are rational; multiplication by `t` makes the first comparison integral.
The resulting centered packing satisfies (2).

## 3. Completing a centered packing inside the clique

Two elementary facts suffice. First, every graph `R` on `k` labeled vertices
has a triangle packing of size at least `t(R)/k`, where `t(R)` is its number
of triangles. Color a triangle `{i,j,l}` by `i+j+l mod k`. Triangles of the
same color are edge-disjoint, because two vertices and the color determine
the third. Take a largest color class.

Second, if `R` has `e` edges, then

    t(R) >= e(4e-k^2)/(3k).                                (3)

Indeed, every edge `vw` has at least `d(v)+d(w)-k` common neighbors. Summing
over edges and applying Cauchy--Schwarz gives

    3t(R) >= sum_v d(v)^2 - ke >= 4e^2/k - ke.

The right side of (3) may be negative; the inequality is still valid.
This is the usual elementary Goodman-type triangle bound, with its proof
included here.

Delete the `h` distinct base edges of the centered packing from `K_C`.
The residual graph has `e=binom(k,2)-h` edges. A largest modular-sum triangle
class in it can be appended to the centered packing, so the constructed
packing has size at least

    f_k(h) = h + e(4e-k^2)/(3k^2)
           = k^2/6-k/2+1/3 + 4h/(3k) + 4h^2/(3k^2).

The function `f_k(z)` is nondecreasing for real `z>=-k/2`, since
`f'_k(z)=8(z+k/2)/(3k^2)`. As `H>=0`, equation (2) implies

    |P| >= f_k(H-k/2) = k^2/6 + 4H^2/(3k^2) - k/2.

Also `|P|>=h>=H-k/2`. Therefore, on defining

    p(delta) = max { delta, 1/3 + 2 delta^2/3 },

we have the uniform constructive lower bound

    2|P| >= k^2 p(delta) - k.                              (4)

No optimal packing computation enters this argument.

## 4. Compressing the cover to the neighborhood union

We first construct a bipartite residual on the capped graph. For an integer
`l<=u`, choose an `l`-subset `L` of `S union T`, put all other clique vertices
on the opposite side, and put all independent vertices opposite `L`.
Delete all within-side edges. For a uniformly chosen `L`, the expected
number of deleted spokes is `E(1-l/u)`. The number of deleted clique edges
is

    binom(l,2)+binom(k-l,2) = l^2-kl+k^2/2-k/2.

In fact one can do at least as well by choosing the `l` clique vertices
with largest weights `m 1_S(v)+n 1_T(v)`. If `l>=u`, include the entire union
and fill with outside vertices, at zero spoke cost.

When `u=0`, or `u<=k/2`, a balanced cut retaining all spokes gives cover
size at most `k^2/4-k/2+1/4`. Suppose now that `u>k/2`, and define

    alpha = u/k,  r = E/(uk).

Allowing `l` to be real and normalizing by `k^2`, the relevant expression is

    z^2-z+1/2+r(alpha-z),     1/2<=z<=alpha.

Its minimum, denoted `F(alpha,r)`, is attained at
`z=min(alpha,(1+r)/2)`. Explicitly,

    F(alpha,r) = 1/4+r(alpha-1/2)-r^2/4, if r<=2alpha-1;
                 alpha^2-alpha+1/2,     if r>=2alpha-1.

For `alpha<=1/2` set `F=1/4`. Rounding the minimizing `l=kz` to a nearest
integer costs at most `1/4`: the interior expression is a quadratic of
leading coefficient one, and the endpoint `l=u` is already an integer.
Thus the constructed cover, after the lifting repair from Section 1,
satisfies

    |D| <= k^2 F - k/2 + 1/4.                              (5)

The lifting step can destroy whole-residual bipartiteness; no claim of
whole-residual bipartiteness is made for the original uncapped graph.

## 5. A two-set overlap inequality

The reason two types admit a uniform comparison is

    st-cu = (s-c)(t-c) >= 0.                               (6)

Together with `(ms+nt)^2>=4mn st`, this implies, when `u>0`,

    mn c^2/(st) <= E^2/(4u^2).

Zero denominators again mean an absent term. Consequently

    delta >= alpha r-r^2/4,       0<=r<=2alpha.             (7)

The second bound follows from `E<=s^2+t^2<=2u^2`. Moreover the expression
`x s^2+y t^2-xyc^2` is nondecreasing in each of `x,y` on `[0,1]^2`, so

    0<=delta <= (s^2+t^2-c^2)/k^2 <= alpha^2 <= 1.         (8)

The penultimate inequality is again (6), since
`u^2-(s^2+t^2-c^2)=2(s-c)(t-c)`.

**Envelope lemma.** For every parameter choice above,

    F <= g(delta) := delta+sqrt(1-delta)-3/4,  if delta<=3/4;
    F <= 1/2,                                otherwise.   (9)

Proof: if `alpha<=1/2`, use `F=1/4` and
`sqrt(1-delta)>=1-delta`. Otherwise fix `delta<=3/4`.
If `delta<=alpha^2-1/4`, (7), (8), and `r<=2alpha` give

    r <= 2alpha-2sqrt(alpha^2-delta) <= 2alpha-1.

The first branch of `F` is increasing up to `r=2alpha-1`. Substitution
therefore yields

    F <= 1/4+delta-alpha+sqrt(alpha^2-delta)
       <= 1/4+delta-1+sqrt(1-delta) = g(delta).

For the second inequality, the function
`sqrt(alpha^2-delta)-alpha` is nondecreasing in `alpha>=sqrt(delta)`;
this follows by differentiation on the interior and continuity at the
endpoint (and is constant when `delta=0`).

If instead `delta>=alpha^2-1/4`, simply use

    F <= alpha^2-alpha+1/2
       <= delta+3/4-sqrt(delta+1/4),

because `1/2<alpha<=sqrt(delta+1/4)<=1` and the first quadratic is
increasing on `[1/2,1]`. This last bound is at most `g(delta)`: for
`0<=delta<=3/4`,

    (delta+1/4)(1-delta) = 1/4+delta(3/4-delta) >= 1/4,

which implies `sqrt(delta+1/4)+sqrt(1-delta)>=3/2` by squaring nonnegative
quantities. Finally `F<=1/2` follows directly from `F=1/4` when
`alpha<=1/2`, and `F<=alpha^2-alpha+1/2<=1/2` otherwise. This proves (9).

## 6. A fixed positive gap

For `0<=delta<=1/2`, the polynomial
`q(delta)=1-delta/2-delta^2/8` is nonnegative and satisfies

    q(delta)^2-(1-delta) = delta^3(8+delta)/64 >= 0.

Hence `sqrt(1-delta)<=q(delta)`. Equations (9) and the definition of `p`
give the exact comparison

    p(delta)-F
       >= 1/12-delta/2+19delta^2/24
        = (19/24)(delta-6/19)^2 + 1/228
       >= 1/228.                                         (10)

For `1/2<=delta<=3/4`, we have `p(delta)=delta`, so (9) gives

    p(delta)-F >= 3/4-sqrt(1-delta)
                >= 3/4-sqrt(1/2) > 1/24 > 1/228.

Here `sqrt(1/2)<17/24` follows from `288<289`. Finally, for
`3/4<=delta<=1`, `p(delta)=delta` and `F<=1/2`, giving a gap at least `1/4`.
Thus (10) holds throughout `[0,1]`. Combining (4) and (5) proves (1).

## 7. Consequences and boundaries

At `k=113`, the right side of (1) is `-85/114`, strictly greater than `-1`.
It is increasing for `k>=113`. Since `2|P|-|D|` is an integer, it is
nonnegative for every integer `k>=113`.

If the original graph violates Tuza, the capped graph from Section 1
also violates it: it has the same cover number and no larger packing
number. The theorem forces its clique order to be at most112. It has at
most `k+2(k-1)<=334` active vertices. For `k<=2` the inequality is immediate:
all triangles, if any, share the single clique edge, so both parameters
are one. Thus the counterexample reduction has no omitted small case.

Every triangle in a split graph uses at least one clique edge, so
`nu(G)<=binom(k,2)<k^2/2`. Replacing `k^2/228` in (1) by the weaker
`nu(G)/114` proves the ratio assertion. Also `nu(G)>=nu(K_k)>=binom(k,3)/k`
by the modular-sum argument, so `k/nu(G)` tends uniformly to zero. Therefore
the asymptotic ratio bound is genuinely below two, not merely an additive
reformulation with an uncontrolled error term.

The finite kernel is a mathematical reduction, **not** a proposal to run
an order334 census. The unresolved small-order part needs another uniform
exchange/deletion argument or a genuinely compressed certificate.

## Prior work and trust boundary

The threshold, dense-split, and clique-order-eight results listed in
[SOURCES.md](SOURCES.md) are context, not dependencies of this proof. The
general split cover reduction and an earlier, coarser multiplicity cap
are credited there. Our preceding two-type cover-normal-form result
motivated this pass but is not needed in Sections 1--7.

The proof is elementary and parameter-uniform. The accompanying exact
Python constructs the two witnesses and checks compact regression cases.
Those cases check implementation; they do not establish the universal
quantifiers, novelty, or independent peer review. No solver, floating-point
bound, large certificate, exhaustive graph census, formal proof assistant,
or external dataset is part of the proof.
