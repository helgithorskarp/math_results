# An obstruction to shadow convexity for orthant projections

Discovery Net researcher 6, 22 September 2026.

This note closes one proposed route to the global sharp planar
orthant-projection inequality. It does **not** settle that inequality.
The result is an exact counterexample to convexity under parallel chord
movements, even after the origin is optimally chosen. A closed formula
for every member of a kite family supplies the counterexample.

For a planar convex body $Q$ and $t\in Q$, define

$$
E_Q(t)=\{x-y:x,y,x+y-t\in Q\},\qquad
F(Q)=\max_{t\in Q}\frac{|E_Q(t)|}{|Q|}.                 \tag{1}
$$

Equivalently, $E_Q(t)=\mathcal E(Q-t)$, where
$\mathcal E(R)=\{x-y:x,y,x+y\in R\}$.
The [preceding envelope theorem](../sharp_simplex_orthant_projections/PROOF.md)
shows that for polytopal $Q$ this is exactly the best full-to-positive
orthogonal projection ratio, with positive image affinely equivalent
to $Q$, over all finite ambient dimensions and origin placements.

## 1. The theorem and the failed convexity step

Let

$$
K_b=\operatorname{conv}\{(-1,0),(1,0),(0,1),(0,-b)\},
\qquad 0<b<1.
$$

Then the unique maximizing origin is

$$
t_b=(0,c_b),\qquad c_b=\frac{1+3b^2}{3+b^2},
$$

and

$$
F(K_b)=4+\frac{4(1-b)}{3+b^2}.                         \tag{2}
$$

At $b=0$, the body is a triangle, the maximum is $16/3$, and its
unique maximizing origin is $(0,1/3)$. At $b=1$, it is a
parallelogram, the maximum is $4$, and every origin in the body
maximizes (1). Parameters $b>1$ reduce to $1/b$ by an affine map.

Now consider the area-preserving parallel chord movement

$$
Q_s=\operatorname{conv}\{(-1,0),(1,0),(s,1),(0,-1)\},
\qquad 0\leq s\leq2.
$$

Its optimized ratio is

$$
F(Q_s)=6-\frac{8}{s^2+2s+4}.                          \tag{3}
$$

This function is strictly concave for $0<s<2$:

$$
\frac{d^2}{ds^2}F(Q_s)
 =-\frac{48s(s+2)}{(s^2+2s+4)^3}<0.
$$

In particular,

$$
F(Q_0)=4,\qquad F(Q_{1/2})=\frac{94}{21},\qquad
F(Q_1)=\frac{34}{7},
$$

and the midpoint exceeds the average of the endpoints by

$$
\frac{94}{21}-\frac12\left(4+\frac{34}{7}\right)=\frac1{21}>0. \tag{4}
$$

Thus optimizing the origin does not restore convexity under parallel
chord movements. The usual convexity-based reduction from polygons
to triangles cannot be applied to $F$.
The classical shadow-volume theorem itself is not contradicted:
we disprove its proposed applicability to this derived functional.
The example also does not disprove a weaker endpoint or
quasiconvexity principle, nor the candidate global bound $F(Q)\leq16/3$.

## 2. Concavity in the origin

For any fixed $Q$, $E_Q(t)$ is compact, convex, centrally symmetric,
and has positive area. Indeed, it contains $Q-t$: given $q\in Q$,
take $x=q,y=t$, so that $x+y-t=q$.
The maximum in (1) exists. To see this, all fibers lie in the fixed
compact set $Q-Q$, and their graph is closed. If $t_j\to t$, then
for every $\varepsilon>0$ the fibers eventually lie in
$E_Q(t)+\varepsilon B_2$. Continuity of area for these outer
parallel bodies gives upper semicontinuity, hence attainment on $Q$.

If $z_i=x_i-y_i\in E_Q(t_i)$, taking convex combinations of
$x_i,y_i,x_i+y_i-t_i$ proves

$$
\theta E_Q(t_1)+(1-\theta)E_Q(t_2)
 \subseteq E_Q(\theta t_1+(1-\theta)t_2).
$$

Brunn–Minkowski implies that

$$
t\longmapsto |E_Q(t)|^{1/2}
$$

is concave on $Q$. Consequently an interior local maximum is global.
A strict interior local maximum is the unique global maximum:
if a second maximizer existed, concavity would make the segment
between the two maximizers constant.

For $K_b$, reflection across the vertical axis also shows that an
axis origin is at least as good as the average of it and its
reflected partner. The strict local argument below rules out
off-axis maximizers as well.

## 3. Explicit supporting inequalities

The four inequalities for $K_b$ are

$$
X+Y\leq1,\quad -X+Y\leq1,\quad
bX-Y\leq b,\quad -bX-Y\leq b.                          \tag{5}
$$

Write $t=(a,c)$ and $z=(u,v)=x-y$.
Every point of $E_{K_b}(a,c)$ satisfies the following eight
absolute-value inequalities:

$$
\begin{aligned}
|u+v|&\leq2,& |u-v|&\leq2,\\
|bu+v|&\leq1+b,& |bu-v|&\leq1+b,\\
|u+bv|&\leq2+b-c-ba,&
|u-bv|&\leq2+b-c+ba,\\
|(1+3b)u+(3+b)v|&\leq3+5b+(1-b)c-(1-b)a,\\
|(1+3b)u-(3+b)v|&\leq3+5b+(1-b)c+(1-b)a.
\end{aligned}                                                     \tag{6}
$$

Here is a direct certificate, avoiding any unproved elimination
claim. If normals $n_i$ from (5), bounds $d_i$, and positive
weights $\lambda_i$ satisfy $\sum\lambda_i n_i=0$, then use

$$
n_i\cdot(x+y)\pm n_i\cdot z\leq2d_i,\quad\hbox{or}\quad
n_i\cdot(x+y)\leq d_i+n_i\cdot t.
$$

Multiply the chosen inequalities by $\lambda_i$ and sum, cancelling
the $x+y$ terms.

The first two rows of (6) are ordinary support inequalities for
$K_b-K_b$. For the third row use normals
$(1,1),(-1,1),(-b,-1)$, weights
$(1+b)/2,(1-b)/2,1$, respectively, and choices $+,-,$ constant.
The resulting normal is $(1,b)$ and the bound is
$2+b-c-ba$.
For the fourth row use normals $(1,1),(-b,-1),(-1,1)$,
weights $1+b,2,1-b$, and the same choices.
The resulting normal is $(1+3b,3+b)$ and the stated bound.
Swapping $x,y$ gives the negative normals, while reflecting the
horizontal coordinate gives the remaining inequalities.

Let $P_b(a,c)$ be the polygon defined by (6).
We have proved the universal inclusion

$$
E_{K_b}(a,c)\subseteq P_b(a,c).                        \tag{7}
$$

## 4. Exact axis polygons and their preimages

Suppose $b<c<1$ and $a=0$. The polygon $P_b(0,c)$ is invariant
under both coordinate reflections. Its consecutive first-quadrant
vertices, including the axes, are

$$
\begin{aligned}
p_0&=(2+b-c,0),\\
p_1&=\left(\frac{2-b-c}{1-b},\frac{c-b}{1-b}\right),\\
p_2&=\left(\frac{3-c}{2},\frac{1+c}{2}\right),\\
p_3&=\left(\frac{b+c}{1+b},\frac{1+2b-bc}{1+b}\right),\\
p_4&=(0,1+b).
\end{aligned}                                                     \tag{8}
$$

The four supporting edges in this quadrant are, in order, the
positive versions of the third-row first inequality, $u+v\leq2$,
the fourth-row first inequality, and $bu+v\leq1+b$.
The coordinates in (8) are their intersections. The successive
coordinates are strictly ordered when $b<c<1$, and the reflected
inequalities are satisfied, so these give the complete polygon.

All five vertices actually lie in $E_{K_b}(0,c)$.
The following explicit choices give $x-y=p_i$ and
$x,y,x+y-(0,c)\in K_b$:

- At $p_0=(U,0)$, take
  $x=(U/2,(c-b)/2)$ and $y=(-U/2,(c-b)/2)$.
  The third point is $(0,-b)$.
- At $p_1=(U,V)$, take $y=(-1,0)$ and $x=(1-V,V)$.
  The third point $(-V,V-c)$ lies on the lower-left edge.
- At $p_2=(U,V)$, take $y=(-1,0)$ and $x=(U-1,V)$.
  The third point $(U-2,V-c)$ lies on the upper-left edge.
- At $p_3=(U,V)$, take $x=(0,1)$ and $y=(-U,1-V)$.
  The third point is $(-U,1-U)$ on the upper-left edge.
- At $p_4$, take $x=(0,1)$ and $y=(0,-b)$.
  The third point is $(0,1-b-c)$, on the vertical axis in $K_b$.

These membership statements follow immediately from (5) and
$b<c<1$. Reflection and swapping $x,y$ give the other vertices.
Convexity, together with (7), therefore proves

$$
E_{K_b}(0,c)=P_b(0,c)\qquad (b<c<1).                   \tag{9}
$$

## 5. A strict local quadratic bound proves global optimality

Set $D=3+b^2$, $c_b=(1+3b^2)/D$. Then

$$
c_b-b=\frac{(1-b)^3}{D}>0,\qquad
1-c_b=\frac{2(1-b^2)}{D}>0.
$$

Thus the axis polygon (8) at $c_b$ has sixteen distinct vertices,
all adjacent supporting lines being nonparallel. Its combinatorial
type persists in a neighborhood of $(a,c)=(0,c_b)$.

For completeness, the local upper-right boundary vertices of
$P_b(a,c)$ are

$$
\begin{aligned}
v_0&=(2+b-c,-a),\\
v_1&=\left(\frac{2-b-c-ba}{1-b},\frac{c-b+ba}{1-b}\right),\\
v_2&=\left(\frac{3-c+a}{2},\frac{1+c-a}{2}\right),\\
v_3&=\left(\frac{b+c-a}{1+b},\frac{1+2b-bc+ba}{1+b}\right),\\
v_4&=(0,1+b).
\end{aligned}                                                     \tag{10}
$$

After $v_4$, take the horizontal reflections of
$v_3(-a,c),v_2(-a,c),v_1(-a,c)$; complete the polygon by central
reflection. Substitution into the shoelace formula gives

$$
|P_b(a,c)|
=\frac{5+4b-9b^2-4b^3+2(1+3b^2)c
 -(1+3b^2)a^2-(3+b^2)c^2}{1-b^2}.                    \tag{11}
$$

Equivalently, putting
$M_b=(1+b)\left(4+4(1-b)/(3+b^2)\right)$,

$$
|P_b(a,c)|=M_b
 -\frac{1+3b^2}{1-b^2}a^2
 -\frac{3+b^2}{1-b^2}(c-c_b)^2.                       \tag{12}
$$

All coefficients of the two squares are positive. By (7) and (9),
$|E_{K_b}(0,c_b)|=M_b$, and nearby distinct origins have strictly
smaller envelope area. Section 2 promotes this strict local maximum
to the unique global maximum on $K_b$.
Since $|K_b|=1+b$, formula (2) follows.

The calculation (11) is short exact algebra. The checker additionally
verifies it by polynomial interpolation: after multiplication by
$1-b^2$, both sides have degree at most3 in $b$ and at most2 in
each of $a,c$. Equality on a $4\times3\times3$ rational grid is
therefore an exact identity certificate, not a heuristic sample.
The degree bound follows directly from the denominators in adjacent
terms of (10); no adjacent pair introduces a squared denominator.
At grid points outside the local geometric chamber, the checker
evaluates the ordered shoelace expression as an algebraic expression;
it does not identify it with the area of the actual upper polygon.

For $b=0$, direct triangle coordinates give
$|E_{K_0}(a,c)|=5+2c-3c^2-a^2$ on the triangle, with maximum
$16/3$ at $(0,1/3)$.
For $b=1$, central symmetry gives $E_{K_1}(t)=2K_1$ for every
$t\in K_1$: every $2x$, $x\in K_1$, is realized by $x,-x$,
whose third point is $-t\in K_1$.

## 6. The parallel chord movement and affine change of coordinates

Every $Q_s$ is the image of the diamond $Q_0$ under

$$
(x,y)\longmapsto (x+s\max(y,0),y).
$$

At each fixed height $y$, the horizontal interval is translated,
so its length and total area2 are preserved. The resulting polygon
is convex for $0\leq s\leq2$; only the right vertex becomes collinear
at $s=2$. Thus this is a genuine parallel chord movement throughout
the closed parameter interval.

The functional $F$ is affine invariant. For an affine map
$T(x)=Lx+d$ and an origin $t$, the pair and third-point conditions
transform to those for $TQ$ and $Tt$, and differences transform by
$L$. Both areas acquire $|\det L|$.

For $0<s<2$, the affine map

$$
T_s(x,y)=\left(y,\frac{s-2x+sy}{2+s}\right)
$$

maps $Q_s$ onto $K_b$ with $b=(2-s)/(2+s)$.
Applying (2) gives (3). The unique maximizing origin in $Q_s$ is

$$
t_s=\left(\frac{s^2+2s-4}{s^2+2s+4},0\right).          \tag{13}
$$

The endpoint values follow from the parallelogram and triangle cases.
Differentiation proves strict concavity and (4) proves the finite
counterexample to convexity.

There is also no general rule that the area centroid is optimal.
For $K_{1/3}$ it is $(0,2/9)$, whereas the unique optimizer is
$(0,3/7)$. Direct exact polygon calculation gives respective ratios
$1031/216$ and $34/7$, a positive difference $127/1512$.

## 7. What remains unresolved and what was checked

The global planar maximum over all shapes $Q$ remains unresolved
by this work. Every member of this family satisfies $F(Q)\leq16/3$,
with equality only at the triangular endpoint. The obstruction is
to the standard convexity hypothesis, not to the proposed sharp
constant or to every possible deformation argument.

The continuum proof uses the explicit dual inequalities, vertex
preimages, local area identity, and classical Brunn–Minkowski.
The exact checker supplies complete four-dimensional active-constraint
enumeration from the original $x,y,x+y-t$ definition for finite
fixtures, checks all envelope vertices and optimal origins, verifies
the algebraic identity by interpolation, and rejects corrupt data.
It uses integer/rational arithmetic and no external solver.
Finite fixtures alone do not prove origin optimality; Sections 2–5 do.
Independent review is pending, and there is no proof-assistant
formalization or exhaustive historical-priority claim.
