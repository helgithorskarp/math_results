# Linear-loss rounding of centered triangle packings

Write `nu` for the maximum number of edge-disjoint triangles and `tau` for
the minimum number of edges meeting every triangle.

Let a finite simple graph have vertex set `C disjoint-union I`, where `I`
is independent. The graph on `C` can initially be arbitrary. Group the
vertices of `I` into classes with neighborhoods `S_i subset C` and positive
integer multiplicities `m_i`, for `1<=i<=r`. Write

    k=|C|,   s_i=|S_i|,   D=sum_i s_i,   E=sum_i m_i s_i.

Classes need not be distinct, although merging equal neighborhoods reduces
`D`. A centered triangle has one vertex in `I`. Let `nu_c` and `nu_c*`
denote the integer and fractional packing optima restricted to these
triangles. These differ from the unrestricted parameters `nu` and `nu*`.

**Theorem 1.** For every such graph,

    nu_c >= nu_c* - 3D/2.                                  (1)

The proof gives a construction from an optimal basic LP solution and
ordinary simple-graph edge coloring. In particular, the loss is at most
`3rk/2`, independent of the multiplicities. No asymptotic packing theorem
is used.

**Theorem 2.** Now suppose `C` is a clique, `k>=2`, and `s_i>=2`. Assume
there is a fractional centered packing saturating every edge between `C`
and `I`, equivalently `nu_c*=E/2`. Then

    2nu-tau >= k^2/66 -(1/2+12r/11)k
                         +5/12-4r-48r^2/11.                (2)

Consequently, if `k>=80r+40`, then `tau<2nu`. All neighborhood overlaps are
allowed. A sufficient, exactly checkable saturation condition is

    sum_{i: u,v in S_i} m_i/(s_i-1) <= 1
    for every distinct u,v in C.                           (3)

Condition (3) is sufficient, not necessary. Saturation itself is an LP
feasibility condition. It is not automatic, even after the earlier
multiplicity cap `m_i<=s_i-1`. This does not prove an additive linear bound
for `nu*-nu`, unrestricted Tuza for split graphs, or an effective cutoff
for every fixed-type split graph.

## 1. The centered LP is exact

For each base edge `e=uv` in `G[C]` contained in `S_i`, introduce `y_(i,e)`.
The LP is

    maximize H=sum_(i,e) y_(i,e),
    y_(i,e)>=0,
    sum_{i: e subset S_i} y_(i,e)<=1              (each base edge e),
    sum_{e incident with v} y_(i,e)<=m_i          (each i and v in S_i).

Aggregate the weights of centered triangles over the `m_i` copies to map
any fractional centered packing to this LP. Conversely, distribute each
`y_(i,uv)` equally among the `m_i` triangles on that base edge. Each spoke
then has load at most one, and base-edge loads are unchanged. Thus the
optimum is exactly `H=nu_c*`. Also `2H<=E`. Equality holds if and only if
all spoke constraints are saturated.

The LP is a bounded nonempty polytope. Choose an optimal extreme point.
Let `P` be its positive variables and `T` its tight base-edge constraints.
Then

    |P| <= |T|+D.                                         (4)

Otherwise a nonzero perturbation supported on `P` would preserve every
tight constraint (there are at most `|T|+D`), and a sufficiently small
perturbation of either sign would remain feasible. This contradicts
extremality. This dimension argument uses all tight spoke constraints,
of which there are at most `D`; it does not assume their independence.

Retain only variables equal to one. Such variables use distinct base
edges. Call a base edge fractional if it supports a variable strictly
between zero and one. Suppose `a` fractional base edges have tight base
constraints, and `b` have slack base constraints. A tight fractional edge
supports at least two positive variables, and a slack fractional edge at
least one. After cancelling the unit variables and their distinct tight
base rows from (4), we get

    2a+b <= a+D,   hence a+b<=D.                           (5)

Each discarded base edge carries total mass at most one. The retained
integer assignments therefore number at least `H-D`. For each type `i`
they form a simple graph `F_i` on `S_i`, of maximum degree at most `m_i`.
The edge sets of the `F_i` are mutually disjoint.

By Vizing's theorem, `F_i` has an edge coloring using at most `m_i+1`
colors. Keep its `m_i` largest color classes. If one class must be dropped,
it has at most

    |E(F_i)|/(m_i+1) <= s_i m_i/[2(m_i+1)] <= s_i/2

edges. Interpret the remaining color classes as matchings at distinct
vertices of the independent class. Proper coloring prevents spoke reuse;
disjoint base assignments prevent base-edge reuse. The extra loss is at
most `D/2`, proving (1). The supplied implementation uses the constructive
fan-and-alternating-path proof of Misra and Gries; see [SOURCES.md](SOURCES.md).

Extremality matters: on `K_7`, the feasible one-type assignment `y_e=1/2`
with `m=3` is optimal but not extreme. It has 21 fractional base edges,
whereas `D=7`. One cannot simply floor an arbitrary optimal LP solution.

The linear order of the loss is necessary even with one neighborhood and
a complete base. Let `k` be odd, let `S_1=C`, and take `m_1=k-1`. Assigning
unit mass to every base edge is feasible, so `nu_c*=k(k-1)/2`. Each center
can use at most `(k-1)/2` base edges. A `k`-color decomposition of `K_k`
into near-perfect matchings attains that bound at all `k-1` centers.
Consequently `nu_c=(k-1)^2/2`, and `nu_c*-nu_c=(k-1)/2`. The constant
`3/2` in (1) is not claimed sharp.

## 2. Adding triangles in the clique

Return to the split case and put `q=k(k-1)/2`. A centered packing of size
`h` removes exactly `h` distinct clique edges. Let `R` be the remaining
graph on `C`, with `e=q-h` edges. It need not be chordal.

For an arbitrary graph on `k` vertices, summing common-neighbor bounds
over its edges and applying Cauchy--Schwarz gives

    3t(R) >= sum_v d_R(v)^2-ke >= 4e^2/k-ke,
    t(R) >= e(4e-k^2)/(3k).

Label the vertices by distinct residues modulo `k`. Triangles with the
same sum of vertex labels share no edge: a shared edge determines the
third label. One of the `k` classes has at least `t(R)/k` triangles.
Together with the centered packing this proves

    nu >= f_k(h):=h+(q-h)(4(q-h)-k^2)/(3k^2)
       = k^2/6-k/2+1/3+4h/(3k)+4h^2/(3k^2).              (6)

Negative values of the residual estimate cause no problem; it is only a
lower bound. The polynomial `f_k` is increasing for `h>=0` and convex.
For `H=nu_c*`, choose the packing from Theorem 1, so `h>=H-3D/2`. The
tangent inequality for this convex polynomial gives

    2nu >= 2f_k(H)-3D f_k'(H).                            (7)

This remains valid when `H-3D/2` is negative. It avoids substituting a
negative value into a monotonicity argument outside its justified range.
Equation (6), with `h=max(0,H-3D/2)`, is also an unconditional computable
packing lower bound for every split instance.

## 3. Explicit Tuza inequality under spoke saturation

Assume `H=E/2`. Since every centered triangle uses a clique edge,
`E/2<=q`, hence `0<=t:=E/k^2<=1`. Substitution in (7) yields

    2nu >= k^2/3-k+2/3+4E/(3k)+2E^2/(3k^2)
                         -4D/k-4DE/k^2.                  (8)

For a cover, place every independent vertex on one side of a cut and
choose uniformly a set of `ell` clique vertices for the other side. The
expected number of uncut edges is

    q-ell(k-ell)+E(1-ell/k).

The complement of every cut is a triangle cover. The real minimizing
choice is `ell=(k+E/k)/2`, which lies in `[0,k]`. Rounding to a nearest
integer increases this quadratic by at most `1/4`. Thus

    tau <= k^2/4-k/2+E/2-E^2/(4k^2)+1/4.                 (9)

Subtract (9) from (8), use `D<=rk`, and drop the nonnegative term
`4E/(3k)`. We obtain

    2nu-tau >= k^2(1/12-t/2+11t^2/12)
                             -k/2+5/12-4r-4rkt.

Completing the square, with no restriction on real `t`, gives

    k^2(1/12-t/2+11t^2/12)-4rkt
        >= k^2/66-(12r/11)k-48r^2/11.

This proves (2). More explicitly, put `k=80r+40+u`, `u>=0`. Its right
side is exactly

    u^2/66+(4r/3+47/66)u+16r^2/3+28r/3+205/44 > 0.

Finally, under (3), set `y_(i,uv)=m_i/(s_i-1)` for every pair in `S_i`.
Each type-vertex has load exactly `m_i`, and (3) is precisely base-edge
feasibility. The converse distribution in Section 1 gives the required
fractional spoke saturation.

## 4. Scope and a nonvacuous example

Take `k=280`, with clique labels `0,...,279`, and neighborhoods

    S_1=[0,140), S_2=[70,210), S_3=[140,280),
    m_1=m_2=m_3=34.

Every pair occurs in at most two neighborhoods, so the left side of (3)
is at most `68/139<1`. Pairwise unions have sizes 210, 280, 210: this
example is outside the earlier three-type co-sunflower theorem. The full
union is the entire clique. Here (2) is `3549/44`, so integrality gives

    tau <= 2nu-81.

The audit additionally builds and verifies a concrete triangle packing
and cut for this graph without using an LP solver at this large order.

The saturation hypothesis excludes real instances. For example, on a
four-vertex clique take `S_1={0,1,2}`, `S_2={0,1,3}`, both with `m_i=2`.
All spoke loads can be saturated only if each neighborhood's three base
edges receives unit mass of its own type. Both types would then require
unit mass on edge `01`, which is impossible. The centered LP optimum is
5, whereas `E/2=6`.

The earlier dense chordal result supplied eventual Tuza inequalities via
general fractional packing approximation. This work isolates an effective
integer realization for centered triangles and gives a numerical cutoff
under a genuine additional feasibility hypothesis. Realizing the clique
part of an arbitrary optimal fractional packing remains unresolved.
