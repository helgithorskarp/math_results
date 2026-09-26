# Every small-variance Gaussian hinge for asymmetric paired layers

Complete analytic author proof, 26 September 2026. Independent mathematical
review and formalization are pending. The exact finite checker supplements
the proof; no floating-point experiment is a premise. This document gives
the new small-variance endpoint. [ALL_VARIANCES.md](ALL_VARIANCES.md) combines
it with credited team results to obtain a uniform all-variance neighborhood.

## 1. The class and the full comparison at small variance

Let A and B be nonempty finite sets in the plane z = 1. Suppose each is
invariant under J(x,y,1) = (-x,-y,1), and assume

```
7/5 <= |a| <= 2       (a in A),
17/10 <= |b| <= 2     (b in B),
a dot b >= 0         (a in A, b in B).                         (1)
```

There is a distinguished a* in A such that

```
|a* - b| >= 9/10 for every b in B,
|a* - b*| <= 101/100 for some b* in B.                         (2)
```

Use the labelled supports X = (0,A,-B), Y = (0,A,B). Give them the same
probability weights w, with origin weight c and a* weight alpha, satisfying

```
every site weight >= 1/32,       c <= 1/16,       alpha >= 1/5. (3)
```

In particular, the number N of labelled sites is at most 32. Put
mu = sum w_i delta_Xi, nu = sum w_i delta_Yi. The map T fixing 0 and A
and sending -b to b is a contraction: the only changed squared distances
have losses |a+b|^2 - |a-b|^2 = 4 a dot b >= 0. It has a global
1-Lipschitz extension by Kirszbraun's theorem.

Let gamma_s be the Gaussian density of covariance s I_3, and let
H_f(a) = integral (f-a)_+ dx.

**Theorem.** Under (1)--(3), for every 0 < s <= 10^-10 and every a >= 0,

```
H_(nu*gamma_s)(a) >= H_(mu*gamma_s)(a).                        (4)
```

Thus the entire Gaussian density majorisation comparison holds at these
variances. Equivalently, every convex energy density has the conjectured
comparison, with the usual integrability interpretation. The sufficient
variance bound is intentionally conservative; its optimization is not the
claim. Equal norms within a cloud, equal weights on reflected partners,
and a fixed number of sites are not assumed.

Section 8 exhibits undamped sheared dual cones satisfying these conditions.
The team's original square-cone benchmark is already covered at *every*
variance by the [square-cone orbit theorem](../gaussian_majorisation_square_cone_orbits/PROOF.md).
This proof addresses more general geometry at small variance. The companion
all-variance theorem covers a smaller neighborhood with an existential spatial
radius. Neither resolves the full dimension-three problem or asserts a new
Kneser--Poulsen consequence. The origin of the argument is to exclude an actual Gaussian
counterexample regime on the asymmetric frontier, rather than only a
particular proof mechanism.

Put C_s = (2 pi s)^(-3/2). Thresholds a = 0 and a >= C_s are immediate,
since both densities have total mass one and are bounded above by C_s.
Otherwise write

```
a = C_s t,       t = exp(-r^2/(2s)),       r > 0.              (5)
```

We split at r = 3/5. Section 3 treats r >= 3/5 by a union-volume gap.
Sections 4--7 treat r <= 3/5 by localization of signed density comparisons.

## 2. A uniform union-volume gap

Write U_Z(r) for the union of the radius-r balls centered at Z, and V_Z(r)
for its volume. We first prove

```
V_X(r) - V_Y(r) >= r/2000000       for every r >= 3/5.         (6)
```

Both transverse clouds are centrally symmetric. Consequently -B has the
same transverse centers as B, at height -1. At height z >= 0 let E,E' be
the sections of the upper and lower A unions, F,F' the sections of the
upper and lower B unions, and C the origin-ball section. Then E' is
contained in E and F' in F. Pair heights z and -z. The input sections are
E union F' union C and E' union F union C; the output sections are
E union F union C and E' union F' union C. Their input-minus-output
indicator difference is exactly

```
1_((E \ E') intersect (F \ F') \ C).                         (7)
```

This is a pointwise identity in the five membership bits, with the two
nesting constraints. Thus the volume gap equals the volume in the upper
half-space lying in both upper unions and in neither lower union nor the
origin ball. This elementary folding and relabeling observation is not
claimed as a new Kneser--Poulsen theorem.

Let m be the transverse midpoint of a* and b*. For 3/5 <= r <= 8 use
the ball of radius 1/100 centered at (m,r+1/10). Its squared distance to
either a* or b* is

```
|a* - b*|^2/4 + (r-9/10)^2.
```

The difference between (r-1/100)^2 and this expression is at least

```
(89/50)r - 42597/40000 >= 123/40000 > 0.                     (8)
```

The ball therefore lies inside both relevant upper radius-r balls.
Its points have z >= r+9/100, excluding the origin ball and every lower
ball. Its volume is 4 pi/(3*10^6) >= 4/10^6, using pi >= 3, and this is
at least r/2000000 for r <= 8.

For r >= 8 use instead the box

```
|x-m_1|, |y-m_2| <= sqrt(r)/4,    r+1/4 <= z <= r+1/2.
```

Each coordinate offset from m to a* or b* is at most 101/200 < 1.
Thus the squared distance to either center is at most

```
2 (sqrt(r)/4 + 1)^2 + (r-1/2)^2
  = r^2 - (7/8)r + sqrt(r) + 9/4 <= r^2.
```

The last inequality follows from sqrt(r) <= r/2 and 3r/8 >= 9/4.
The box has volume r/16, and z > r again excludes the origin and lower
balls. This proves (6), including its unbounded radius range.

## 3. All low thresholds: r >= 3/5

Since every weight is at least 1/32, the superlevel set of f = mu*gamma_s
at level a contains U_X(r_-), where

```
r_- = sqrt(r^2 - 2s log 32).
```

The radicand is positive, since log 32 < 4 and s <= 10^-10. Therefore

```
(1-H_f(a))/a = integral min(f/a,1) >= V_X(r_-).
```

For g = nu*gamma_s, the Gaussian mass outside U_Y(r) is at most the
weighted sum of the tails outside the corresponding centered balls.
The weights sum to one. Dividing this single Gaussian tail by a gives

```
4 pi exp(r^2/(2s)) integral_r^infinity u^2 exp(-u^2/(2s)) du
  <= 4 pi (sr + s^2/r).
```

Integration by parts and the bound
integral_r^infinity exp(-u^2/(2s)) du <= (s/r) exp(-r^2/(2s))
prove the displayed inequality. Inside U_Y(r), min(g/a,1) <= 1. Hence

```
(1-H_g(a))/a <= V_Y(r) + 4 pi sr(1+s/r^2).                    (9)
```

Decreasing all N <= 32 radii costs at most the sum of their annulus volumes:

```
V_X(r)-V_X(r_-) <= (4 pi N/3)(r^3-r_-^3)
                 <= 4 pi N s r log 32
                 <= 128 pi s r log 32.                     (10)
```

For the middle inequality, integrate the derivative of (r^2-L)^(3/2)
over 0 <= L <= 2s log 32. By (6), (9), (10), pi < 4, log 32 < 4, and
s <= r^2,

```
[H_g(a)-H_f(a)]/a >= r(1/2000000 - 2080s) > 0.               (11)
```

Indeed 2080/10^10 < 1/2000000. This includes arbitrarily small positive
thresholds. The bound log 32 < 4 follows already from the first five
terms of the positive series for exp(4).

## 4. Antipodal comparison outside a thin slab

Use unnormalized components, with the weights of A and B denoted alpha_i
and beta_j:

```
C(x) = c exp(-|x|^2/(2s)),
A(x) = sum_i alpha_i exp(-|x-a_i|^2/(2s)),
B(x) = sum_j beta_j exp(-|x-b_j|^2/(2s)),
F = C+A+B(-x),       G = C+A+B(x).
```

Thus f = C_s F and g = C_s G. Let phi_t(u) = (u-t)_+, and define

```
D(x) = phi_t(G(x)) + phi_t(G(-x))
       - phi_t(F(x)) - phi_t(F(-x)).
```

The raw hinge gap is the integral of D over x_3 >= 0, and the actual
hinge gap is C_s times that integral. Reindex a cloud by J. A center and
its J-partner have the same norm; reflecting x changes the squared
vertical displacement by 4x_3. The weight ratio bound 32 therefore gives

```
A(-x) <= 32 exp(-2x_3/s) A(x),
B(-x) <= 32 exp(-2x_3/s) B(x).                               (12)
```

For x_3 >= 2s, the factor 32 exp(-4) is below one. Then G(x) is at
least F(x) and F(-x), and the sums of the two paired values are equal.
For any convex phi, the pair with this larger maximum has the larger
sum of phi-values. Consequently D(x) >= 0, at every threshold.
Only the slab 0 <= x_3 < 2s can contribute negatively.

From now on r <= 3/5, so

```
t >= exp(-9/(50s)).                                         (13)
```

Let Gamma be the ball centered at 0 of radius R = 13/20. In the thin
slab outside Gamma, the origin component has displacement at least R.
Every non-origin component of F(x),G(x),F(-x),G(-x) has vertical
displacement at least 1-2s. Both R^2/2 = 169/800 and (1-2s)^2/2
exceed 9/50. Since the weights sum to one, all four values are below t
there, and D = 0. All negative contributions are confined to Gamma.

## 5. A uniform bound for the origin contribution

Write H_Gamma(U) = integral_Gamma phi_t(U(x)) dx. We prove

```
|H_Gamma(G)-H_Gamma(F)| <= 512s exp(-261/(400s)).              (14)
```

For 0 <= u <= 1 put U_u = C+uA+B(-x). On Gamma, the ratio of any
non-origin component to the core has the extra exponential bound
exp[-(|z|^2/2-R|z|)/s], where z is its center. The function
ell^2/2-R ell is increasing for ell >= 7/5. At ell = 7/5 its value
is 7/100, and at ell = 17/10 its value is 17/50. Both exceed 1/40.
Since c >= 1/32, the total non-origin/core ratio is at most

```
eta = 32 exp(-1/(40s)).
```

The Gaussian log-mixture Hessian is

```
D^2 log U_u = -I/s + Cov_tilt(centers)/s^2
            <= -I/s + [128 exp(-1/(40s))/s^2] I
            <= -I/(2s).                                    (15)
```

Here the tilted non-origin probability is at most eta, every center has
squared norm at most 4, and covariance is bounded by the second moment.
The final bound follows from exp(-1/(40s)) <= 3200s^2 and
819200s <= 1. The exponential inequality follows from exp(v) >= v^2/2.
Also eta <= 102400s^2 <= 1/2. On the boundary of Gamma,

```
U_u <= c exp(-R^2/(2s))(1+eta) < c <= U_u(0).
```

For example, R^2/(2s) > 1 and exp(1) > 2 suffice for the strict bound.
Strict log concavity gives a unique interior maximum.

We use the following coarea estimate. If a positive smooth function U
on this ball has an interior maximum and D^2 log U <= -I/(2s), then
for almost every positive v,

```
integral_(Gamma intersect {U=v}) 1/|grad U| dS
    <= 16 pi s R/v.                                         (16)
```

To prove it, center polar rays at the unique maximizer. Convexity of
Gamma makes the segment on each ray an interval of length at most 2R.
Strong concavity gives -partial_r log U >= r/(2s), so each ray meets
each noncritical level at most once. Its radial coarea contribution is
r^2/|partial_r U| <= 2sr/v <= 4sR/v. Integrating over the unit sphere
proves (16). The sole critical level is attained only at the maximum,
so contributes no volume atom. Integrating (16) bounds the volume of
any positive level band.

Let P = A and Q = B(x)-B(-x). The reverse triangle inequality and the
lower norm bounds in (1) imply on Gamma

```
P <= P0 = exp(-9/(32s)),
|Q| <= Q0 = 2 exp(-441/(800s)),       Q0 <= t/2.              (17)
```

Indeed (7/5-R)^2/2 = 9/32 and (17/10-R)^2/2 = 441/800.
The last inequality in (17) follows from (13) and
exp(297/(800s)) >= 4, using exp(v) >= 1+v.

Central symmetry of Gamma gives H_Gamma(C+B) = H_Gamma(C+B(-x)).
Integrating the first directional derivative in the A direction gives

```
H_Gamma(G)-H_Gamma(F)
  = integral_0^1 integral_Gamma
       A(x)[1_(U_u(x)+Q(x)>t) - 1_(U_u(x)>t)] dx du.          (18)
```

An indicator difference requires |U_u-t| <= Q0. By (15)--(17), this
band's volume is at most 64 pi s R Q0/t: its width is 2Q0, and all
its levels are at least t/2. Multiplying by P0 bounds the absolute
value of (18) by 128 pi s R exp(-261/(400s)), at most the right side
of (14). The directional derivative identity follows pointwise from
the fundamental theorem for the positive-part function and integration
of bounded integrands. No second differentiation of a singular hinge
is assumed.

## 6. A larger positive contribution near the heavy anchor

First suppose t <= alpha/2. In the ball E centered at a* with radius
rho = sqrt(s)/10, the anchor contribution ensures

```
F(x) >= alpha exp(-1/200) > alpha/2 >= t.
```

The target b* is at distance at most 101/100 from a*, while every
source -b is at distance at least 2, by its vertical coordinate.
Since rho <= 1/1000, on E we have

```
G-F >= (1/32) exp(-13/(25s)) - exp(-3/(2s))
    >= (1/64) exp(-13/(25s)).                               (19)
```

The constants use (101/100+1/1000)^2/2 < 13/25,
(2-1/1000)^2/2 > 3/2, and exp(49/(50s)) >= 64.
Every source and target center has distance at least 9/10 from -a*:
this is (2) for the -B centers, the vertical separation for upper
centers, and (1) for the origin. Consequently, on E,

```
F(-x), G(-x) <= exp(-(9/10-rho)^2/(2s)) < t,
```

by (13) and (9/10-1/1000)^2/2 > 9/50. Thus D = G-F on E.
The ball lies outside Gamma and above the slab x_3 < 2s. Its volume
is at least s^(3/2)/250, using pi >= 3. Its positive raw contribution
is therefore at least

```
s^(3/2)/16000 * exp(-13/(25s)).                              (20)
```

The integral of D over the upper half of Gamma equals exactly the
raw gap H_Gamma(G)-H_Gamma(F). Everywhere else D is nonnegative,
by Section 4. Subtracting (14) from (20) leaves a positive number:
it suffices that

```
sqrt(s) exp(53/(400s)) > 8192000.
```

As 53/400 > 1/10, exp(v) >= v^2/2 gives the lower bound
1/(200s^(3/2)) >= 5*10^12. Hence the positive signal strictly dominates
all the possible negative contribution.

## 7. Remaining high thresholds

If t > alpha/2, the same ratio estimate on Gamma applies to both F
and G, giving

```
F,G <= c(1+eta) <= 3/32 < 1/10 <= alpha/2 < t.
```

There is no hinge contribution there. Outside Gamma, Section 4 gives
nonnegative antipodal contributions, including zero in the remaining
thin slab. This proves (4) also in this case. Sections 3--7 cover every
0 < t < 1 and every 0 < s <= 10^-10; Section 1 handles the endpoint
thresholds. In particular, no restriction on the way t varies with s
was used.

## 8. A sheared nonsimplicial family and the remaining obligation

For every real |epsilon| <= 1/1000, set

```
A_e = ((1,0,1), (epsilon,1,1), (-1,0,1), (-epsilon,-1,1)),
B_e = ((1,1-epsilon,1), (-1,1+epsilon,1),
       (-1,-1+epsilon,1), (1,-1-epsilon,1)).                   (21)
```

Both clouds are invariant under J. Every cross dot product is exactly
0 or 2, independently of epsilon. The cone generated by B_e is the
full dual of the cone generated by A_e: the latter's dual section at
height one is the parallelogram given by
|x| <= 1 and |epsilon*x+y| <= 1, whose vertices are B_e. These are
proper nonsimplicial four-ray cones, and the reflection is undamped.

The A squared norms are 2 or 2+epsilon^2; the B squared norms are
2+(1+epsilon)^2 or 2+(1-epsilon)^2. They satisfy (1) on this interval.
With a* = (-epsilon,-1,1), the four squared cross distances are

```
5-2epsilon+2epsilon^2,   5+2epsilon+2epsilon^2,
1-2epsilon+2epsilon^2,   1+2epsilon+2epsilon^2.                 (22)
```

All are at least (9/10)^2; each of the last two is at most
1+2/1000+2/10^6 < (101/100)^2. Thus the theorem gives every Gaussian
hinge for all s in (0,10^-10] and every weight vector obeying (3),
throughout the whole shear interval. This is a continuum of geometric
instances, with no sampling of epsilon.

For example, in the order (0,A_e,-B_e),

```
p = (8,12,7,15,44,21,11,23,43)/184
```

satisfies (3), as does every probability w with ||w-p||_1 <= 1/4000.
All these weights may be asymmetric. The geometric hypotheses themselves
also permit other centrally symmetric transverse clouds, subject to (1)--(3).

At epsilon = 0, the entire displayed weight neighborhood is already
settled for all s > 0 by the team's square-cone orbit theorem; our small-
variance result is not a new claim about that previously closed case.
Nonzero shear changes the ray geometry. For a concrete exact distinction,
at epsilon = 1/1000 the squared cosine between the first two A rays is

```
(1+epsilon)^2 / [2(2+epsilon^2)],
```

which is not one of 0, 1/4, 1/9, 2/3, the squared cosines between
distinct rays in the original eight-ray system. Orthogonal maps and
individual positive radial rescalings preserve these quantities.
Accordingly this sheared support, with the displayed center at zero,
is outside the stated fixed-ray support hypotheses of that theorem.
This is not a classification of every alternative representation or
of all possible extensions of the orbit method.

The theorem supplies a uniform positive obligation for the full problem:
for the general paired-layer class above, a Gaussian counterexample must
have s > 10^-10 in these coordinates. The scale is explicit: after a
common similarity of spatial scale L > 0, the variance bound is
10^-10 L^2. The companion [ALL_VARIANCES.md](ALL_VARIANCES.md) proves
all variances in a smaller positive spatial neighborhood, with no certified
numerical radius. It uses the present uniform endpoint and additional
credited team theorems. The entire explicit shear interval 1/1000 at all
variances, arbitrary three-dimensional contractions, and new unequal-radius
Kneser--Poulsen cases remain outside the claims. The team results in
SOURCES.md are not premises of this self-contained small-variance proof.

The exact checker audits the finite section identity, the rational
inequality budgets, the polynomial shear identities and uniform interval
bounds, and inclusion of the stated weight neighborhood. The continuum
coarea, Gaussian-tail, and localization arguments above require ordinary
mathematical review; they are not formalized by that checker.
