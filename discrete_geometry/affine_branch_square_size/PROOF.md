# A sharp square-size theorem for a graph lens with one affine branch

## Theorem

Let I=[A,B], with A<B. Let f,g:I→R be 1-Lipschitz functions satisfying
f(A)=g(A), f(B)=g(B), and f(x)<g(x) for A<x<B. Suppose one of the functions
is affine. Set M=max_I(g−f)>0. Then the Jordan curve

`Γ = graph(f) ∪ graph(g)`

inscribes a square of side at least **2M/3**, with one side on its affine
branch. The constant **2/3 is optimal, even when squares of every orientation
are allowed**. An explicit rational pentagon attains it and has exactly one
nondegenerate inscribed square.

If the affine branch has slope m, the proof gives the refined lower bound

`s ≥ [2 sqrt(1+m²)/(3+m²)] M ≥ 2M/3`.

The endpoint and strict-gap assumptions force |m|<1. Optimality is claimed
for the uniform constant 2/3, not separately for each nonzero slope in the
refined bound. No convexity or concavity of the other branch is assumed.

“Inscribes” means that all four vertices lie on Γ. It does not require the
whole square to be inside the bounded component of the complement of Γ.
All sizes here are Euclidean side lengths, not horizontal projections.

## 1. A horizontal square straddling a height maximum

**Lemma.** Let h:[a,b]→[0,∞) be continuous, zero at the endpoints and positive
inside. Let H=max h and choose t with h(t)=H. There exist x and s>0 with

`x ≤ t ≤ x+s`, and `h(x)=h(x+s)=s`.

Thus `(x,0),(x+s,0),(x+s,s),(x,s)` is an inscribed square whose upper side
straddles the abscissa of a maximum. Moreover, if, for u<v,

`−p(v−u) ≤ h(v)−h(u) ≤ q(v−u)`

for positive p,q, then

`s ≥ H (p+q)/(p+q+pq)`.

**Proof.** Extend h by zero outside [a,b]. Put Φ(x)=x+h(x). Since
Φ(a)=a<t and Φ(t)=t+H>t, the equation Φ(x)=t has a solution in (a,t).
Let x₀ be its *last* solution in [a,t], which exists by compactness. Then
Φ(x)≥t for every x∈[x₀,t]. This last-crossing choice matters: Φ need not
be monotone.

Define F(x)=h(Φ(x))−h(x). We have F(x₀)=H−h(x₀)≥0 and
F(t)=h(t+H)−H≤0. The intermediate value theorem supplies a zero x∈[x₀,t].
Set s=h(x)>0. Then h(x+s)=s, so x+s is inside [a,b], and Φ(x)≥t gives
the required straddling. The four displayed points lie on the graph and
its horizontal base.

For the estimate, the one-sided slope bounds yield

`H−s ≤ q(t−x)`, and `H−s ≤ p(x+s−t)`.

Divide by q and p, respectively, and add. Since (t−x)+(x+s−t)=s,

`(H−s)(1/p+1/q) ≤ s`.

Rearrangement proves the bound. ∎

This is an elementary intermediate-value argument. We make no novelty claim
for the square-existence part of this lemma.

## 2. Rotating the affine branch without losing the graph property

A reflection across the horizontal axis exchanges the upper and lower
branches while preserving M and side lengths. We may therefore assume that
f(x)=mx+c is the lower branch. Translate vertically to set c=0.

If m=1, the endpoint value g(A)=A and the 1-Lipschitz inequality give
`g(x) ≤ A+(x−A)=x=f(x)`, a contradiction. If m=−1, use the right endpoint
instead. Thus −1<m<1.

Write r=sqrt(1+m²), and apply the Euclidean rotation

`ξ=(x+my)/r`, `η=(y−mx)/r`.

The affine base becomes a horizontal segment. On the upper branch, for
x₁<x₂, the Lipschitz inequality gives

`ξ(x₂)−ξ(x₁) ≥ (1−|m|)(x₂−x₁)/r > 0`.

Hence the rotated upper branch remains the graph of a continuous function h.
Its endpoint abscissae match those of the rotated base, and h is zero there
and positive inside. Its maximum is `H=M/r`.

If k=(g(x₂)−g(x₁))/(x₂−x₁), then k∈[−1,1] and the rotated secant slope is

`(η(x₂)−η(x₁))/(ξ(x₂)−ξ(x₁)) = (k−m)/(1+mk)`.

This expression increases with k, so every secant slope of h lies between

`−p=−(1+m)/(1−m)` and `q=(1−m)/(1+m)`.

These are reciprocal bounds: `pq=1`, and
`p+q=2(1+m²)/(1−m²)`. Applying the lemma gives

`s ≥ H(p+q)/(p+q+1) = 2 sqrt(1+m²) M/(3+m²)`.

Rotating back preserves side lengths and puts one side on the affine branch.
Finally, with z=m²∈[0,1),

`9(1+z)−(3+z)² = z(3−z) ≥ 0`.

Both sides being positive, this proves
`3 sqrt(1+m²) ≥ 3+m²`, and hence s≥2M/3.

## 3. A sharp pentagon, including every orientation

Take f=0 on I=[−5/3,5/3], and let the upper graph be

```
g(x) = 1−|x|,              if |x|≤1/3;
       (5/3−|x|)/2,        if 1/3≤|x|≤5/3.
```

This is continuous, 1-Lipschitz, positive inside I and zero at the endpoints.
Its maximum M is 1. The closed curve is the simple pentagon with successive
vertices

`(−5/3,0), (−1/3,2/3), (0,1), (1/3,2/3), (5/3,0)`.

We show that its only square has vertices `(±1/3,0),(±1/3,2/3)`.

**Three vertices cannot lie on the upper graph.** Any three vertices of a
square form a right isosceles triangle. If they lie on a 1-Lipschitz graph,
none of their pairwise joining lines is vertical. The two perpendicular legs
at its right-angle vertex must have slopes +1 and −1: both slopes have
absolute value at most one, and their product is −1. The equal leg lengths
then give equal absolute horizontal displacements. These displacements must
have opposite signs, since otherwise the other two vertices would share an
abscissa but have different ordinates.

Consequently the three points form a symmetric peak or trough, and equality
in the Lipschitz bounds forces the graph to be linear with slopes ±1 on
both intervening intervals. Our g has such opposite unit-slope segments only
at its peak (0,1). Thus the other two vertices would be
`(−t,1−t),(t,1−t)`, for 0<t≤1/3. The fourth vertex of the square would be
`(0,1−2t)`. It is not on the upper graph, whose value at 0 is 1, and it is
not on the base, since 1−2t≥1/3>0. This rules out a square with three or
four upper-graph vertices, including cases where an endpoint could be
counted on both branches.

Every inscribed square therefore has exactly two base vertices and two upper
vertices. The base vertices cannot be opposite: the other two would lie on
opposite sides of the base line, while the whole curve lies on or above it.
They are adjacent, so the square is horizontal. Since g is even and strictly
decreasing on [0,5/3], its upper vertices must be `(−t,g(t)),(t,g(t))`.
The square equation is `g(t)=2t`. The left side decreases strictly and the
right side increases strictly; their unique meeting is t=1/3.

The sole square consequently has side 2/3. This proves uniform sharpness
without any computational assumption. It also explains why the simpler
right-isosceles triangle is not a sharp example: it has the additional
rotated square with vertices `(0,0),(1/2,1/2),(0,1),(−1/2,1/2)`, of side
1/sqrt(2)>2/3.

## 4. What the exact checker verifies

The checker gives a separate, definition-level corroboration of the sharpness
argument. Represent an oriented square by z=(c_x,c_y,v_x,v_y), with vertices
`c+v,c+Jv,c−v,c−Jv`, where J rotates by π/2. Every square is represented.
For each assignment of its four vertices to boundary edges, the supporting
line conditions are linear equations in z. Membership in the four closed
segments adds two linear inequalities per vertex. Shared polygon vertices
are covered by multiple assignments, which is harmless.

The solution set for an assignment is a bounded convex polytope: all four
square vertices lie in fixed bounded segments, and their center and the
vector v are linear combinations of those four vertices. Gaussian elimination
determines its affine solution space, including singular cases. In an affine
space of dimension d, the checker intersects every d-element set of active
inequalities and checks feasibility. A nonempty bounded polytope has vertices;
at each vertex the active normals span that affine space. Thus the procedure
finds every polytope vertex, even if inequalities lower its dimension.

The squared side is `2(v_x²+v_y²)`, a convex function, so its maximum over each
polytope occurs at a vertex. The sharp pentagon's maximum is exactly 4/9.
Every positive-dimensional feasible assignment has only v=0 at all its
vertices and hence throughout; all nondegenerate assignments are isolated
and decode to the single square above. This verifies uniqueness as well.

The right-isosceles triangle catches omission of rotated squares. A rectangle
with a continuum of inscribed squares tests nondegenerate singular assignment
polytopes. An exact rational rigid motion of the sharp pentagon tests that
the enumeration does not assume horizontal sides. No floating-point test,
external solver, or sample of orientations enters the enumeration.
