# Uniform all-threshold certificates from a dilated martingale

27 September 2026. Complete author proof; **independent acceptance pending**.
The full dimension-three Gaussian-majorisation problem remains open.

The accepted spherical-gap endpoint already gives every hinge once a
positive gap on an infinite spherical-parameter range is supplied. This
packet discharges that obligation for a uniform, atom-independent family,
using a dilation of a martingale coupling. A covariance-based product
density makes the certificate explicit for arbitrary sufficiently damped
contractions. It needs no Gaussian quadrature or high-degree moment row.
The coupling, Jensen and moment arguments are elementary credited methods;
no historical-priority claim is made.

## 1. Uniform theorem and a parameter family

Let X have a bounded probability law in R3, let Y=T(X) for a 1-Lipschitz
map, and assume

```
|X-E X| <= R,     V=E|X-E X|^2 > 0,     a>1.
```

The following additional hypothesis concerns the endpoint laws, not the
original deterministic matching. There is a coupling (U,W) such that

```
law(U)=law(X-E X),   law(W)=law(Y-E Y),   E[U|W]=a W.      (1)
```

Equivalently, the dilated centered target aW is below the centered source
in convex order, with an explicit martingale as witness. We use only the
displayed coupling, not an existence theorem for it.

**Theorem 1.** Put

\[
 \eta=\frac{(a-1)V}{96aR^2},\qquad
 s_* = \frac{4224aR^4}{(a-1)V}.                           \tag{2}
\]

For **every** Gaussian variance `s>=s_*` and **every** density threshold
`t>=0`, simultaneously,

\[
 \int(\operatorname{law}(Y)*\gamma_s-t)_+
 \ \ge\ \int(\operatorname{law}(X)*\gamma_s-t)_+.          \tag{3}
\]

Thus the full majorisation comparison, and all well-defined convex-energy
comparisons, hold at every such variance. Arbitrary bounded diffuse laws
and any number or weights of atoms are allowed. For `a>1`, (1) also forces

\[
 D=\mathbb E[|X-X'|^2-|Y-Y'|^2]
   \ge 2(1-a^{-2})V>0.                                  \tag{4}
\]

This covers positive loss proportional to source scatter; it is not an
extension of a near-isometry small-loss cutoff. The constants are sufficient,
not optimal. The hypothesis (1) is not inferred from contraction alone.

Here is a uniformly certified family without a coupling-search obligation.

**Corollary 2.** Suppose `Cov(X)>=kappa I_3`, `kappa>0`, and
`|X-E X|<=R`. For **every** 1-Lipschitz map F, every

\[
 0\le c\le\frac{\kappa}{4R^2},\qquad
 s\ge\frac{2816R^4}{\kappa},                             \tag{5}
\]

the contracted target `c F(X)` satisfies (3) at every threshold. Arbitrary
translations of that target are immaterial. The same conclusion holds
for any contraction T whose centered image satisfies

\[
 |T(X)-\mathbb E T(X)|\le\frac{\kappa}{2R}.               \tag{6}
\]

The whole family (5), over all laws, maps, weights, damping factors and
variances meeting its inequalities, is proved. No selected finite cell
or law-dependent atom-mass floor is used. Since `3kappa<=R^2`, (5) always
has `c<=1/12`, so cF is indeed a contraction. Its output may have full
three-dimensional covariance and paired affine rank six.

The variance lower bound is material. This is not a theorem at all positive
variances and supplies no new small-variance Kneser--Poulsen consequence.

## 2. A uniform spherical gap from (1)

Center the laws separately. For a unit vector theta define

```
M_X(lambda)=E exp(lambda theta.X),
M_Y(lambda)=E exp(lambda theta.Y),
J(lambda)=integral_(S2) log(M_X(lambda)/M_Y(lambda)) d sigma(theta),
```

where sigma has total mass one. J is unchanged by separate translations,
because the added linear functions of theta have spherical mean zero.
All moment-generating functions are finite, since the laws are bounded.

Conditional Jensen in (1), then concavity of `z -> z^(1/a)`, give

\[
 M_Y(\lambda)\le M_Y(a\lambda)^{1/a}
             \le M_X(\lambda)^{1/a}.                    \tag{7}
\]

To be explicit about the second term, conditional Jensen says
`E exp(lambda theta.U)>=E exp(a lambda theta.W)=M_Y(a lambda)`.
Thus

\[
 \log\frac{M_X(\lambda)}{M_Y(\lambda)}
       \ge(1-a^{-1})\log M_X(\lambda).                  \tag{8}
\]

For `lambda>=0`, M_X is nondecreasing. Indeed its derivative is
`E Z(exp(lambda Z)-1)>=0` for `Z=theta.X`, using `E Z=0`.
At `lambda0=1/(2R)`, one has `|lambda0 Z|<=1/2`. The elementary bound

\[
 e^z\ge1+z+z^2/4\quad(|z|\le1/2)                       \tag{9}
\]

follows by Taylor's integral remainder and `e^(-1/2)>1/2`. Consequently

\[
 M_X(\lambda_0)\ge1+\frac{\mathbb E Z^2}{16R^2}.
\]

For `0<=q<=1/16`, `log(1+q)>=q/2`, by integrating `1/(1+q)>=1/2`.
Using monotonicity and `E Z^2<=R^2`, for every `lambda>=lambda0`,

\[
 \log M_X(\lambda)\ge\frac{\mathbb E(\theta\cdot X)^2}{32R^2}.
\]

The exact spherical identity
`integral theta theta^T d sigma=I_3/3` gives

\[
 \boxed{J(\lambda)\ge\frac{(a-1)V}{96aR^2}=\eta>0
                  \quad\text{for all }\lambda\ge1/(2R).} \tag{10}
\]

There is no covariance floor in Theorem 1: the trace V alone enters this
bound. The covariance floor will be a constructive sufficient condition
for (1), not a premise hidden in (10). Squared-norm conditional Jensen
also gives `a^2 E|Y|^2<=V`, proving (4).

## 3. Joining the entire threshold range

We use the independently accepted
[full high-variance endpoint](../gaussian_majorisation_eventual_endpoint/PROOF.md),
Theorem 1, with its
[independent review](../gaussian_majorisation_eventual_endpoint_review2/README.md).
Its conclusion is: `J(lambda)>=eta>0` for every `lambda>=1/(2R)` implies
all hinges at `s>=R^2 max(8,44/eta)` for a contraction with source radius R.

The normalization and the overlap are recalled to expose the trust boundary.
Let `C_s=(2pi s)^(-3/2)` and write the favorable hinge gap as H(t).
For `lambda>=1/(2R)` and `s>=8R^2`, the credited spherical-tail estimate is

\[
 \left|\frac{H(C_s e^{-\lambda^2s/2})}
 {4\pi\lambda s^2 C_s e^{-\lambda^2s/2}}-J(\lambda)\right|
 \le \frac{44R^2}{s}.                                   \tag{11}
\]

It signs every `0<t<=C_s exp[-s/(8R^2)]` when `s>=44R^2/eta`.
The accepted high-noise window signs every
`t>=C_s exp[-9s/(64R^2)]`. Since `9/64>1/8`, these two intervals overlap
and exhaust every positive threshold. At zero both hinges equal one;
above both peaks they both vanish. No numerical mesh reaches the tail.

Both endpoint supports fit in radius-R balls: if needed, extend T from
the source support by the Euclidean Kirszbraun theorem, and use the target
anchor `T(E X)`. This anchor need not be `E Y`. The gap (10) was evaluated
with centered laws, but its translation invariance permits these anchors
in (11). No assumption that the centered target radius is R is needed.

Since `V<=R^2` and `0<(a-1)/a<1`, one has `eta<1/96`; hence `44/eta>8`.
Substituting (10) gives exactly (2), proving Theorem 1. This imports the
reviewed spherical-tail and high-noise analytic arguments. The new code
does not reprove coarea inversion or numerical integration.

## 4. A product-density certificate of the martingale condition

Let the source covariance Sigma be positive definite and center both
endpoint laws. Suppose

\[
 K(x,y)=1+a\,x^T\Sigma^{-1}y\ge0
       \quad\text{on }\operatorname{supp}(X)\times
                           \operatorname{supp}(Y).       \tag{12}
\]

Then `K(x,y) mu(dx) nu(dy)` is a probability coupling. Integrating in
either variable gives one, because both means vanish. Its conditional
mean in the first variable is

\[
 \int xK(x,y)\,d\mu(x)=a\Sigma\Sigma^{-1}y=ay.            \tag{13}
\]

This proves (1) constructively, for diffuse as well as atomic laws.
This elementary affine product density is not claimed as a new general
transport theorem. It is a sufficient certificate, not a necessary
criterion for convex order or for Gaussian majorisation.

If `Sigma>=kappa I`, `|x|<=R`, and `|y|<=r`, then
`|a x^T Sigma^-1 y|<=a R r/kappa`. Thus `aRr<=kappa` guarantees (12),
including equality. For F 1-Lipschitz, boundedness and an independent copy
give, on the source support,

\[
 |F(x)-\mathbb EF(X)|\le\mathbb E|F(x)-F(X)|
 \le\mathbb E|x-X|\le2R.                                \tag{14}
\]

Take `a=2` and `c<=kappa/(4R^2)`. The centered image cF has radius at
most `2cR<=kappa/(2R)`. Also `V=tr Sigma>=3kappa`. Formula (2) is therefore
at most `8448 R^4/(3kappa)=2816R^4/kappa`, proving (5)--(6).

Condition (12) is often less restrictive than the radius criterion. For
finite rational data it is an exact collection of cross-label inequalities,
with the original pairwise contraction tested separately. It does not
replace the prescribed deterministic map by the martingale coupling.

## 5. Exact certificate, scalability and the R2/R3/R8 handoff

[certificate.py](certificate.py) validates rational coordinates, common
probability weights and every active pair contraction, then centers the
clouds and computes Sigma, V and the exact squared radius `B=R^2`.
For rational `a>1` it inverts Sigma over Q and stores the nine rational
entries of `a Sigma^-1`. It checks (12) for every active cross-label pair
and emits eta and `s_*=4224a B^2/((a-1)V)` as exact fractions.

At a supplied variance at least s_* it returns `SIGNED_ALL_THRESHOLDS`.
A valid coupling below that cutoff returns `UNRESOLVED_AT_REQUESTED_VARIANCE`
and the certified future variance interval; it makes no sign assertion at
the requested variance. Negative kernel entries or singular covariance
return `UNRESOLVED`. All zero-loss contractions return `ISOMETRIC_ZERO`,
by the accepted distance-rigidity argument. A failed sufficient certificate
is not a counterexample.

The witness adds only nine rationals to the input, rather than storing
quadratically many coupling masses or exponentially many replica moments.
Verification takes quadratically many exact operations and linear storage
in the atom count, streaming the coupling masses; arithmetic bit cost depends
on the input. There is no claim of polynomial
complexity for unrestricted majorisation or of an effective diffuse-law
oracle. The general theorem also accepts martingale witnesses other than
(12), but this particular producer searches only the displayed kernel.

[verify.py](verify.py) reconstructs source scatter and covariance by
ordered-pair formulas and explicitly checks every coupling mass, both
marginals and conditional first moments. These checks use a different
representation from the producer's centered-moment inversion. It also
verifies the exact universal budget, scaling, boundaries and malformed
certificate rejection. The analytic inequalities remain written proofs.

The accepted R3 degree-two same-pair cubature preserves both endpoint
means, source covariance and V on at most 19 original pairs. When (12)
holds on the original supports, it persists on the selected supports with
the same matrix; source and target radius bounds also persist because the
means are preserved. The simple radius/covariance parameter family is thus
compatible with the loss-cubature interface without extra mixed features.
Passing a kernel test only on selected atoms does not prove it on discarded
support: that converse is not claimed. No rounding or common cubature rule
for an entire parameter cell is supplied.

The accepted mean-loss and dominant-atom middle signs remain intact, and
the previous covariance-collapse guard is now independently accepted.
None is used beyond its scope. This all-threshold family instead supplies
a positive infinite-parameter gap to the already accepted endpoint. It
does not sign arbitrary contractions at a fixed finite variance, remove
the dilation hypothesis, or establish a new Kneser--Poulsen class.
