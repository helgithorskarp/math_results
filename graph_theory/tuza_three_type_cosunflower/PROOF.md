# Tuza's inequality for three-neighborhood co-sunflower split graphs

Let `nu(G)` be the maximum size of an edge-disjoint triangle packing and
`tau(G)` the minimum size of a set of edges meeting every triangle. Fix a
split partition `V(G)=C disjoint-union I`, where `C` is a clique and `I` is
independent. A neighborhood is **active** when it has at least two vertices.

**Theorem (computer-assisted).** Suppose the vertices in `I` have at most
three distinct active neighborhoods in `C`. If three occur, write them as
`S0,S1,S2` and assume

    S0 union S1 = S0 union S2 = S1 union S2 = U.             (1)

Then `tau(G)<=2nu(G)`, with no restriction on clique order, neighborhood
sizes, or multiplicities. Vertices of `C` outside `U` are allowed. No
maximality assumption on the split partition is made.

Equivalently, in the three-type case the complements `Pi=U\Si` are pairwise
disjoint. We call this the co-sunflower condition. The neighborhoods may
cross and need not be nested. The theorem does not settle arbitrary
three-neighborhood split graphs or Tuza's conjecture for all split graphs.

Cases with at most two active types use the previously proved
[two-type theorem](../tuza_two_type_complete/PROOF.md), independently reviewed
in [the review directory](../tuza_two_type_complete_review1/README.md).
Hereafter there are exactly three distinct active types. The new argument
proves a uniform gap for this class and closes its entire finite remainder.
The exact-cover C5 normal form is contextual work, not a dependency.

## 1. Parameters and cap

Put `pi=|Pi|`, `c=|S0 intersect S1 intersect S2|`, `d=|C\U|`,
`u=p0+p1+p2+c`, `k=u+d`, and `si=u-pi`. Then

    |Si intersect Sj|=u-pi-pj,   |S0 intersect S1 intersect S2|=c.

Relabel so `p0<=p1<=p2`. Distinctness is equivalent to not having two empty
`Pi`, hence `p1>=1`. All types are active exactly when `s2>=2`. In
particular `u>=3`.

The multiplicity of a neighborhood of size `s>=2` can be capped at `s-1`
without changing `tau`, while capping cannot increase `nu`. This general
cap lemma, already used in the two-type work, is valid for any number of
types. To recall the proof, take a minimum cover in the capped graph and
let `F` be its surviving triangle-free clique core. Retain the same maximum
independent set `A` of `F[S]` at all `s-1` copies. Since every edge of `F[S]`
meets `S\A`,

    e(F[S]) <= (s-1)|S\A|.

Delete these core edges and restore every spoke of this type. The extra
core deletions cost no more than the restored spokes; all extra copies can
now be added freely. Repeating for each capped type cannot create a
triangle at another type. Subgraph monotonicity gives the opposite cover
inequality. Vertices of degree at most one lie in no triangle and can be
omitted. Thus the complete multiplicity domain is

    1<=mi<=si-1,   i=0,1,2.                               (2)

## 2. A uniform quadratic gap

For the capped graph put `xi=mi/si`, `Ei=mi si`, `E=E0+E1+E2`, and

    delta = [sum_i xi si^2
             -sum_(i<j) xi xj (u-pi-pj)^2
             +x0 x1 x2 c^2]/k^2.                          (3)

Use the edge coloring `a+b mod si` of each neighborhood clique. Each of its
`si` colors is a matching. Choose `mi` colors uniformly and independently
for the three types, one per center. Keep exactly one centered triangle
for each selected base edge. Inclusion-exclusion gives an expected packing
size `(delta k^2-V)/2`, where

    V=sum_i xi si-sum_(i<j)xi xj(u-pi-pj)+x0 x1 x2 c.

For each vertex the summand in `V` is the probability that at least one of
its neighborhood types selects it in a model with independent type events
of probabilities `xi`. Hence `0<=V<=u<=k`. Also `delta` is nonnegative and
nondecreasing in each `xi`: its numerator is the sum over ordered pairs of
vertices of the probability of at least one successful type shared by the
pair. Thus a centered packing of size `h0` exists with

    h0 >= delta k^2/2-k/2.                                (4)

For any graph `R` on `k` vertices with `e` edges, the degree-sum inequality
and Cauchy--Schwarz give

    t(R) >= e(4e-k^2)/(3k).                               (5)

Triangles with the same sum of vertex labels modulo `k` are edge-disjoint:
two triangles sharing an edge have different third labels. Therefore `R`
has a triangle packing of size at least `t(R)/k`. Remove the `h0` distinct
base edges of the centered packing from `K_C`. Combining the two packings
and expanding (5) yields

    nu(G) >= h0+(q-h0)(4(q-h0)-k^2)/(3k^2)
          = k^2/6-k/2+1/3+4h0/(3k)+4h0^2/(3k^2),
    q=binomial(k,2).

This quadratic is nondecreasing for `h0>=-k/2`. Substituting (4) cancels the
constant and linear-in-delta terms, giving

    2nu(G) >= k^2(1/3+2delta^2/3)-k.                      (6)

For a cover use a bipartite cut, with all centers opposite one clique side
of size `ell`. For `ell<=u`, choose that side uniformly from `U`; the mean
number of deleted spokes is `E(1-ell/u)`. For `ell>=u`, put all of `U` on
that side and fill from outside; no spokes need be deleted. Put
`alpha=u/k` and `r=E/(uk)`. If `alpha<=1/2`, the whole union fits on a
balanced side. If `alpha>1/2`, minimize the quadratic real cut cost over
`k/2<=ell<=u`. With `R=min(r,2alpha-1)` this gives

    tau(G) <= k^2 F-k/2+1/4,
    F=1/4                                      if alpha<=1/2,
    F=1/4+R(alpha-1/2)-R^2/4                    otherwise. (7)

An interior quadratic minimum changes by at most `1/4` upon rounding to a
nearest integer; the endpoint `ell=u` is integral. Some subset has cost no
larger than the mean, so the averaging in this cover argument is legitimate.

Condition (1) implies, for `i!=j`,

    si sj >= |Si intersect Sj| u,
    xi xj |Si intersect Sj|^2 <= Ei Ej/u^2.

Since `sum_(i<j)Ei Ej<=E^2/3`, dropping the nonnegative triple term in (3)
gives `delta>=alpha r-r^2/3`. When `r>2alpha-1`, first multiply all `xi` by
`R/r`; monotonicity of (3) and the same argument at the smaller values give

    delta >= alpha R-R^2/3 =: D >=0,
    0<=R<=2alpha-1<=1.                                   (8)

For `alpha>1/2`, equations (6)--(8) imply

    2nu(G)-tau(G) >= k^2 g_alpha(R)-k/2-1/4,
    g_alpha(t)=1/12-t(alpha-1/2)+t^2/4
               +(2/3)(alpha t-t^2/3)^2.

At fixed `t` in this domain, `alpha t-t^2/3<=2/3`, so

    partial g_alpha(t)/partial alpha
        = t[(4/3)(alpha t-t^2/3)-1] <= -t/9 <=0.

Increase `alpha` to one to obtain `g_alpha(t)>=g_1(t)`, where

    g_1(t)=1/12-t/2+(11/12)t^2-(4/9)t^3+(2/27)t^4.

Here is a rational certificate for its strictly positive minimum on `[0,1]`:

    g_1''(t)-1/18=(8/9)(1-t)(2-t)>=0.

For `a=9/25`, integration of this curvature bound and completion of the
square give

    g_1(t) >= g_1(a)+g_1'(a)(t-a)+(t-a)^2/36
           >= g_1(a)-9g_1'(a)^2
           = 3855551/1464843750 > 1/400.

The exact values are `g_1(a)=6191/2343750` and `g_1'(a)=16/15625`.
For `alpha<=1/2`, equations (6),(7) give the stronger leading gap `1/12`.
Consequently, in all cases,

    2nu(G)-tau(G) >= k^2/400-k/2-1/4.                      (9)

The right side is `-299/400>-1` at `k=199` and strictly increases thereafter.
Integrality proves Tuza for every `k>=199`. The cap lifts this assertion to
all original multiplicities. The argument extends the earlier two-type
uniform-gap method; the new pairwise-union estimate and quartic certificate
are what allow the third type.

### Outside-vertex reduction for the finite verification

The same estimate also proves Tuza whenever `k>=55` and `d=k-u>=3`.
For `alpha<=1/2`, the leading gap `1/12` already suffices at such `k`.
For `alpha>1/2`, first suppose `R` lies outside `[1/4,1/2]`. The curvature
bound makes `g_1'` increasing, while

    g_1'(1/4)=-13/108,   g_1'(1/2)=13/108,
    g_1(1/4)=31/3456,    g_1(1/2)=5/432.

Hence `g_alpha(R)>=g_1(R)>=31/3456`. At `k=55` the resulting lower
bound `31k^2/3456-k/2-1/4` is `-2129/3456>-1`, and it increases thereafter.
If `1/4<=R<=1/2`, integrate the alpha derivative more accurately. For every
`alpha<=beta<=1`,

    -partial g_beta(R)/partial beta
      >= R[1-(4/3)(R-R^2/3)] = R(1-2R/3)^2 >=25/144.

The last polynomial is nondecreasing on `[1/4,1/2]`, since its derivative
is `(1-2R/3)(1-2R)>=0`. Therefore

    g_alpha(R) >= 1/400+(25/144)(1-alpha),
    2nu-tau >= k^2/400+(25/144)kd-k/2-1/4
             >= k^2/400+k/48-1/4 > -1.

Integrality proves the stated reduction. It certifies the entire omitted
outside-vertex tail, independent of multiplicities, and is used only to
accelerate the finite computation below.

## 3. Exact finite bounds

The remaining domain has `3<=u<=k<=198`, nonnegative `p0<=p1<=p2,c`,
`p1>=1`, `p0+p1+p2+c=u`, `s2>=2`, and (2).

Write `q(z)=binomial(z,2)` and `r(z)=z-1` for even `z>=2`, `r(z)=z` for
odd `z>=3`, and `r(z)=1` for `z<2`. A round-robin factorization partitions
`K_z` into `r(z)` matchings. Independent palettes, as in Section 2 but now
with this exact color count, give the centered-packing expectation

    H1=sum_i mi q(si)/r(si)
       -sum_(i<j)mi mj q(u-pi-pj)/(r(si)r(sj))
       +m0 m1 m2 q(c)/(r(s0)r(s1)r(s2)).                  (10)

Alternatively use a single palette on `U`, giving different types disjoint
sets of colors and restricting each matching to its corresponding `Si`.
The optimal expected packing in this construction is

    H2=max [sum_i ai q(si)]/r(u),
    0<=ai<=mi integer, sum_i ai<=r(u).                    (11)

Because `s0>=s1>=s2`, fill the available colors greedily in that order.
Every `mi<=r(si)<=r(u)`, so this is feasible. Set `h=ceil(max(H1,H2))`.
Some centered packing has size `j0>=h`; no double-counted base edge survives.

Let `p=nu(K_k)` be the classical exact complete-graph triangle-packing number:

    p=(q(k)-L)/3,
    L=0 if k=1,3 mod 6;  L=4 if k=5 mod 6;
    L=k/2 if k=0,2 mod 6;  L=k/2+1 if k=4 mod 6.          (12)

See [SOURCES.md](SOURCES.md) for the external design-existence theorem
underlying (12). Randomly relabel a fixed such packing and retain triangles
inside the residual clique graph. Equation (5) then gives

    f(z)=z+p(q(k)-z)(4(q(k)-z)-k^2)/(3k binomial(k,3)),
    B=max(p,h,ceil(f(h))) <= nu(G).                       (13)

To justify substituting `h` for `j0`, note that `f` is convex and `f(0)=p`.
If `f(h)<=p` it adds nothing; otherwise `f'(h)>0` and `f(j0)>=f(h)`.
Ceilings are exact, including for a negative residual term.

For a cover, choose signs `sigma_i` specifying which side's neighbors each
type retains. Fix `sigma_0=+1` by symmetry and try all four remaining sign
choices. For clique vertices put `w(v)=sum_i sigma_i mi 1_(v in Si)` and
`Eplus=sum_(sigma_i=+1)mi si`. At a clique side of size `ell`, the smallest
cover from this sign choice has size

    q(k)-ell(k-ell)+Eplus-(sum of the ell largest weights). (14)

There are five constant-weight cells: `P0,P1,P2`, the triple intersection,
and the outside cell. On each interval between successive cell boundaries,
(14) is quadratic in `ell`, minimized by clamping
`floor((k+w)/2)` to that interval. Denote the minimum over all intervals and
signs by `Ubound`. The kept graph is bipartite, so `tau(G)<=Ubound`.

## 4. Complete enumeration and validation

For each `u,p0,p1,p2,c`, the complete four-dimensional parameter box is

    1<=mi<=si-1,   0<=d<=198-u.

Section 2 certifies its whole tail `d>=3, u+d>=55`. The numerical
checker therefore initially takes only

    0<=d<=min(198-u,max(2,54-u)),   1<=mi<=si-1.

It separately counts all analytically certified tuples in the removed tail;
the combined coverage is the original complete domain.

Both actual graph parameters `nu` and `tau` are nondecreasing in each `mi`
and in `d`, by adding centers or outside clique vertices. A box is therefore
certified if `2B(lower corner)>=Ubound(upper corner)`. This inference uses
monotonicity of the graph parameters, not of the numerical bound formulas.
Otherwise bisect a nontrivial coordinate and recurse. The subboxes are
disjoint and exhaust the original box. Each split shortens an integer
interval; every failing singleton is printed and forces a nonzero exit.

The driver exhausts the canonical shapes above. The precise totals and
per-union-size counts, including the analytically certified tails, are in
[EXPECTED.txt](EXPECTED.txt). A standard-library
Python audit verifies their coverage independently by decreasing
neighborhood sizes `s0>=s1>=s2>=2`, with `s1<u` and
`s0+s1+s2>=2u`. Each such shape contributes
`(s0-1)(s1-1)(s2-1)(199-u)` parameter tuples.

The completed count is 11,539,903 shapes and
497,893,855,660,344 parameter tuples. The outside-vertex lemma
certifies 441,165,614,683,344 tuples; the remaining
56,728,240,977,000 are covered by 2,317,590,705
certified boxes after 4,623,641,507 visited boxes. There are
zero failures. The full C++ run took about 815 seconds on one CPU thread;
the Python audit took about 4.4 seconds on the test host.

The audit also compares every tuple through clique order seven against
Python rational arithmetic and every literal clique cut. Through order six
it enumerates actual independent palettes and a dynamic program assigning
disjoint shared colors. Through order five it builds the graph and finds
an actual edge-disjoint packing meeting (13), checking every witness edge.
It also computes the exact triangle-cover number there by enumerating every
triangle-free clique core and every independent set within each neighborhood.
It checks the round-robin factorizations through order 198, the rational
quartic certificate, and rejected out-of-range inputs. These are checks by
the author, not independent peer review or a proof-assistant formalization.

## 5. Arithmetic and trust boundary

The finite checker uses signed 64-bit integers, with inputs limited to
`3<=k<=198`. We have `mi<=197`, `q(k)<=19503`, `p<=6501`, and
`0<=h,e<=19503`. Every single term in the numerator of (10) has absolute
value below `198^5/2`; its partial sums are below `7*198^5/2<2*10^12`.
The denominator in (13) is below `3*198*binomial(198,3)<10^9` and the
absolute residual numerator is at most `6501*19503*4*19503<10^13`.
All cover intermediates are below a million. There are fewer than `199^4`
canonical shape candidates and fewer than `199^4` tuples per box, so every
counter is below `2*199^8<5*10^18<2^63-1`, including recursion nodes.
The count bound is deliberately loose; actual totals are much smaller.
Negative ceilings use division toward zero correctly.

No floating point, solver, external dataset, graph catalogue, or hidden
certificate is used in the theorem's verification. Exploratory numerical
search was not evidence for any assertion here. The universal reductions
remain unformalized mathematics; the finite lemma trusts this C++ source,
compiler/runtime, and execution hardware. Formula (12) and the at-most-two-
type branch have the explicit external mathematical dependencies above.
Source, compact reports, and exact reproduction commands suffice to repeat
the entire computation. Full three-type Tuza without (1) remains open.
