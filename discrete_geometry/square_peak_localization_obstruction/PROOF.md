# A robust obstruction to locating an inscribed square at the maximum gap

An admissible pair consists of functions f,g on [A,B], each with Lipschitz
constant strictly less than 1, equal at the endpoints, and f<g inside.
Write Γ=graph(f)∪graph(g), M=max(g−f), and π_x(S) for the closed horizontal
projection of a square S. “Inscribed” means its four vertices lie on Γ;
its edges need not lie inside the enclosed region.

The proposed **maximum-gap localization property** is:

> There exist an inscribed nondegenerate square S and a maximizer x* of
> g−f such that x*∈π_x(S).

This is a proof route considered here, not a conjecture attributed to
Rifford or another source. Section 1 explains why it would imply a square
of side at least M/2. Sections 2–4 refute it, even for polynomial branches,
by an exact computer-assisted finite witness and a compactness argument.
They do not refute the M/2 size conjecture or square existence.

## 1. The localization-to-size implication

Every square on an admissible pair has exactly two vertices on each
branch, and these pairs are opposite sides. Indeed, three square vertices
include two perpendicular sides at their common vertex. Both sides cannot
have absolute slope less than 1, so a strict-Lipschitz graph contains at
most two square vertices. A common endpoint belongs to both graphs;
if it were a square vertex, the total of the two branch membership counts
would be at least five, again forcing three vertices on a branch. Thus
no square vertex is a common endpoint, and the split is exactly two/two.
The two same-branch pairs cannot be the diagonals: those are perpendicular,
whereas both secants must be horizontally dominant.

Label the lower vertices from left to right P=(t,y), Q=(t+a,y+b),
where a>0 and |b|<a. The upper vertices must then be

    R=(t+a−b,y+b+a),  S=(t−b,y+a).                 (1)

The other possible orientation places an upper vertex at (t+b,y−a).
The Lipschitz bound for g would give g(t)≤y−a+|b|<y=f(t), a contradiction.
Thus (1) covers every square, with P,Q,R,S in cyclic order.

Suppose first b≥0 and put z=x−t. On the overlap 0≤z≤a−b of the
lower and upper chord projections, the 1-Lipschitz inequalities give

    f(x) ≥ y + max(−z,b−a+z),
    g(x) ≤ y+a + min(z+b,a−z).

Consequently

    g(x)−f(x) ≤ 2a−2|z−(a−b)/2| ≤ 2a.

On the remaining left part −b≤z≤0, compare P and S to obtain
f(x)≥y+z and g(x)≤y+a+z+b, so the gap is at most a+b.
On the right part a−b≤z≤a, compare Q and R to obtain
f(x)≥y+b−a+z and g(x)≤y+z+2b, giving the same bound a+b.
Reflecting the horizontal coordinate handles b<0. Thus throughout the
*whole* square projection, not only the chord overlap,

    g(x)−f(x) ≤ 2a ≤ 2 sqrt(a²+b²).              (2)

A square whose projection contains a maximum-gap point therefore has
side at least M/2. Failure of localization does not imply failure of
this size bound: (2) is a sufficient condition, not a necessary one.

## 2. An eight-edge rational counterexample

Use piecewise affine interpolation on the following common knots:

| x | 0 | 4 | 6 | 8 | 10 |
|---|---|---|---|---|---|
| f(x) | 0 | −9/5 | −18/5 | −93/50 | 0 |
| g(x) | 0 | 9/5 | 0 | 9/5 | 0 |

The lower slopes are −9/20,−9/10,87/100,93/100; the upper slopes
are 9/20,−9/10,9/10,−9/10. Both Lipschitz constants are at most 93/100.
The gap is positive inside and has knot values 0,18/5,18/5,183/50,0.
Its unique maximum is M=183/50 at x*=8.

**Exact finite assertion.** This curve inscribes precisely three
nondegenerate squares. In the parameters (t,y,a,b) of (1), they are:

| square | t | y | a | b | largest x-coordinate |
|---|---|---|---|---|---|
| 1 | 1016/497 | −2286/2485 | 1206/497 | −648/497 | 410/71 |
| 2 | 104/49 | −234/245 | 18/7 | −72/49 | 302/49 |
| 3 | 44202/10439 | −104958/52195 | 37872/10439 | 324/10439 | 82074/10439 |

In particular, every square lies strictly left of x*=8, with separation

    8−max_S max π_x(S) = 1438/10439 > 0.          (3)

The largest squared side is 1434393360/108972721. It is larger than
M²/4 (indeed its side is close to M). Thus this example supplies no
counterexample to Rifford's proposed half-gap bound.

### Exact certificate and completeness

The finite assertion is computer-assisted. The self-contained `verify.py`
uses rational arithmetic, with `fixture.json` giving the inputs and the
three displayed parameter vectors. It does not use floating point or
ignore singular cases.

Number the four lower segments 0,…,3 and the four upper segments 4,…,7,
all from left to right. By Section 1, P,Q belong to lower segments i≤j
and S,R to upper segments 4+k≤4+l. There are exactly 10²=100 assignments
(i,j,4+l,4+k). For each, substituting (1) into its four supporting-line
equations produces a rational affine system in (t,y,a,b). Segment bounds
and a≥0, −a≤b≤a are closed linear inequalities. These polytopes are
bounded, since all four points lie on bounded segments and the four
parameters are linear functions of their coordinates.

Row reduction writes the solution as p+Σu_i v_i. If its affine dimension
is d, enumerate every set of d active inequalities and solve exactly;
retain solutions satisfying all inequalities. Every vertex of a nonempty
bounded polytope occurs this way, including polytopes of lower dimension
inside the supporting-line solution space. Inconsistent systems and
infeasible segment assignments are explicitly distinguished.

Of the 100 assignments, 97 supporting-line systems have dimension zero,
two have dimension one, and one is inconsistent. Precisely five
assignments are feasible: two give zero-size squares at the common
endpoints, and the remaining three give the displayed squares. Neither
singular system is feasible. Their nonzero edge assignments, in the
same order as the table, are (0,1,5,4), (0,1,6,4), (1,2,6,5).
This proves completeness of the three-square list under the geometric
reduction. Every decoded point is separately checked for line incidence,
segment membership, equal side lengths, and right angles.

As a second formulation, the checker sets the vertices to
c+v,c+Jv,c−v,c−Jv and enumerates **all 8⁴=4096 edge assignments**, without
assuming a two/two split or imposing an orientation relative to the
branches. It obtains the same three squares. Eight feasible singular
assignment polytopes occur, but all their vertices have v=0. Since such
a polytope is the convex hull of its vertices, every point in it is
also a zero-size square. Thus no continuum or singular nonzero square
is omitted. These two formulations share rational elimination code;
they are not independent software implementations or independent review.

A rational rotation and translation preserves exactly the three squares
in another 4096-assignment run. A 2-by-1 rectangle supplies a control with
nonzero singular square families, testing that the code does not discard
them. This control is not used to infer the theorem. Source and expected
output contain the exact statistics and square coordinates.

## 3. A reusable stability lemma

**Lemma (persistence of a square-free projection band).** Let (f_0,g_0)
be admissible and J a compact subinterval of (A,B). Suppose no inscribed
nondegenerate square on their union has horizontal projection meeting J.
Then there is η>0 such that the same statement holds for every admissible
(f,g) on [A,B] with max(||f−f_0||∞,||g−g_0||∞)<η.

*Proof.* Otherwise choose uniformly convergent admissible pairs
(f_n,g_n)→(f_0,g_0) and squares S_n whose projections meet J. Label
P_n,Q_n,R_n,S_n by (1). The vertices stay in a fixed bounded set, so a
subsequence converges to a square, possibly of side zero. Uniform
convergence places the two lower limits on f_0 and the two upper limits
on g_0. If the limiting side were zero, all four vertices would coincide
at a point with x∈J, since the projection intervals meet the compact
set J. This would force f_0(x)=g_0(x), impossible on J. Thus the limit
is nondegenerate and its projection still meets J, contradicting the
hypothesis. No uniform bound below 1 on the sequence's Lipschitz constants
is needed; strictness for each pair supplies its two/two labeling. ∎

Apply the lemma to the explicit example with J=[63/8,65/8]. Equation (3)
gives max π_x(S)=82074/10439<63/8, so J is square-free. Moreover

    max_{x outside int J}(g_0(x)−f_0(x)) = 117/32
                                            = M−3/800.

If both branch errors are less than η<3/3200, the perturbed gap is within
2η of the original gap; its value at 8 exceeds every value outside
int J. Therefore **every maximum-gap point lies inside J**, while
**no inscribed square projection meets J**, provided η is also smaller
than the stability-lemma threshold.

Hence the failure is open in the relative uniform topology on admissible
pairs. The proof establishes a positive perturbation threshold but does
not compute its numerical value. It does not assert that all perturbed
squares remain to the left of J: new small squares near an endpoint are
allowed, as long as their projections avoid J.

## 4. Counterexamples with polynomial branches

For h=f_0 or g_0 define the Bernstein polynomial on [0,10]

    B_n h(x)=Σ_{k=0}^n h(10k/n) binom(n,k)
                           (x/10)^k (1−x/10)^(n−k).

These polynomials preserve the endpoint values. For n≥2, B_n g_0−B_n f_0
is strictly positive on (0,10), because each interior sampled gap is
positive and the Bernstein weights are positive there. The derivative
is a convex combination of the numbers

    (n/10)(h(10(k+1)/n)−h(10k/n)),

all of absolute value at most 93/100. Thus each polynomial branch is
93/100-Lipschitz. Uniform convergence is elementary: if K is binomial
with parameters (n,x/10), then

    |B_n h(x)−h(x)| ≤ (93/100) E|10K/n−x|
                    ≤ (93/20)/sqrt(n),

using the binomial variance and Cauchy–Schwarz. For all sufficiently
large n, both branches therefore lie in the neighborhood of Section 3.
Their square projections avoid every maximum-gap point.

This proves existence for real-analytic polynomial branches, with rational
coefficients since all sampled values of the original branches are
rational. No explicit degree threshold is certified. The *closed Jordan
curve* may still have corners where the two branches join at the endpoints;
no globally smooth closed-curve claim is made.

## Scope and attribution

Tao establishes square existence for this strict-Lipschitz class. Rifford's
Theorem 1.1 gives a universal 0.018M size bound for two 1-Lipschitz branches
and suggests the value 1/2 in the discussion. Greene–Lobb prove a stronger
existence theorem under larger Lipschitz bounds. This note does not improve
those results. It closes the sufficient maximum-gap localization route,
including the stronger request that *both* opposite-side projections
contain a maximum. It does not contradict the earlier graph result for
an affine branch: neither branch of this example is affine.

The finite certificate is exact but unformalized; it trusts the displayed
geometric reduction, the rational polytope enumeration, Python and its
standard rational arithmetic. Compactness, the envelope estimate, and
the polynomial approximation are written mathematical arguments. Prior
literature and search-relative novelty limits are in REFERENCES.md.
