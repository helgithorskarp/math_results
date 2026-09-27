# A uniform Lipschitz certificate for the full high-variance hinge curve

27 September 2026. Complete author proof; independent acceptance pending.
The unrestricted dimension-three Gaussian-majorisation problem remains open.

## 1. Uniform family

Let X be a bounded probability law in R3, let `|X-E X|<=R`, and put
`V=E|X-E X|^2>0`. Suppose that, for one number `0<q<1`, the prescribed map T
satisfies on the entire source support

\[
 27|T(x)-T(x')|^2\le q^2|x-x'|^2.                         \tag{1}
\]

Write Y=T(X), and let gamma_s have covariance sI_3. Then for **every**

\[
 s\ge\frac{4224R^4}{(1-q)V}\quad\hbox{and every }t\ge0,
 \qquad
 \int(\operatorname{law}(Y)*\gamma_s-t)_+
 \ge\int(\operatorname{law}(X)*\gamma_s-t)_+.              \tag{2}
\]

The inequalities hold simultaneously for the entire threshold curve and all
variances above this cutoff. In particular, **every map with Lipschitz
constant at most 1/6** satisfies (2) for

\[
 s\ge33792 R^4/V,                                        \tag{3}
\]

by choosing `q=7/8`, since `27/36=3/4<=49/64`.
More generally any fixed Lipschitz bound below `1/sqrt(27)` is allowed.
For a uniform parameter family fix `R>0`, `v>0` and `q in(0,1)`; every
source with scatter at least v and every map satisfying (1) share the
cutoff `4224R^4/((1-q)v)`. No covariance eigenvalue, minimum atom weight,
support cardinality or martingale hypothesis enters this family.

The pair loss obeys `D>=2(1-q^2/27)V`. The source and target may both be
full dimensional, including paired affine rank six. Arbitrary bounded
diffuse laws are included. This is a high-variance result, not an
all-variance result or a new Kneser--Poulsen consequence. The constants
are sufficient; their optimization is not the objective.

Since `D<=2V`, (9) below also gives the loss-normalized spherical margin
`J(lambda)/D >= (1-q)/(192R^2)` on `lambda>=1/(2R)`. This is uniform in
atom count, weights and covariance conditioning within the stated family.

## 2. Spherical comparison from pair distances

For any bounded law Z in R^d define, with normalized sphere measure,

\[
 S_Z(\lambda)=\int_{S^{d-1}}\log\mathbb E
                       e^{\lambda\theta\cdot Z}\,d\sigma(\theta).
\]

This quantity is unchanged by translating Z. Let Z' be an independent
copy, and put

\[
 A_Z(v)=\mathbb E\cosh(v\cdot(Z-Z'))\ge1.
\]

Independence and symmetry of the difference give the exact identity

\[
 2S_Z(\lambda)=\int_{S^{d-1}}\log A_Z(\lambda\theta)\,d\sigma.
                                                               \tag{4}
\]

There is a useful lower bound involving only pair distances. Put
`F_X(lambda)=E cosh(lambda |X-X'|/sqrt(d))`. For every orthonormal basis
`e_1,...,e_d`, the function `u -> cosh(sqrt(u))` is convex on `[0,infinity)`:
its power series has nonnegative coefficients and so does its second
derivative. Consequently

\[
 \cosh\left(\frac{\lambda|z|}{\sqrt d}\right)
 \le\frac1d\sum_{j=1}^d\cosh(\lambda e_j\cdot z).
\]

After taking expectation, each term `A_X(lambda e_j)` is at least one.
Their arithmetic mean is at most their product, because the product is
at least each term. Taking logarithms and averaging over orthonormal
bases with rotation-invariant probability measure proves

\[
 \log F_X(\lambda)
 \le\sum_{j=1}^d\mathbb E_{\rm frame}\log A_X(\lambda e_j)
 =2d S_X(\lambda).                                      \tag{5}
\]

Every frame marginal is the normalized sphere measure. Boundedness
justifies the integrations; all logarithms are finite and nonnegative.

Suppose `|Y-Y'|<=L|X-X'|` under the paired independent-copy law. Jensen
for the logarithm in (4), followed by `|theta.z|<=|z|`, gives

\[
 S_Y(\lambda)\le\frac12\log\mathbb E\cosh(\lambda|Y-Y'|)
 \le\frac12\log\mathbb E\cosh(\lambda L|X-X'|).           \tag{6}
\]

For `0<=alpha<=1`, convexity of log cosh with value zero at the origin
gives `cosh(alpha u)<=cosh(u)^alpha`. Concavity of the power alpha then
implies `E cosh(alpha U)<=(E cosh U)^alpha` for any bounded U.
Taking `alpha=L sqrt(d)<=1` in (6), and then using (5), proves

\[
 \boxed{S_Y(\lambda)\le d^{3/2}L S_X(\lambda)
        \quad(\lambda\ge0, L\sqrt d\le1).}               \tag{7}
\]

This is a uniform spherical comparison for arbitrary bounded laws and
the prescribed strong contraction. It does not use convex order of the
endpoint vectors, or a componentwise positive Gaussian replica kernel.
The stronger restriction `d^(3/2)L<1` produces a positive gap. In R3,
(1) permits `L=q/sqrt(27)`, so (7) gives

\[
 J(\lambda):=S_X(\lambda)-S_Y(\lambda)
              \ge(1-q)S_X(\lambda).                      \tag{8}
\]

This proof is deliberately insensitive to covariance collapse. The frame
average is an analytic identity, not an enumerated or sampled mesh.

## 3. Quantitative gap and every threshold

Center X. For a unit theta, set Z=theta.X. Since EZ=0,
`d E exp(lambda Z)/d lambda=E[Z(exp(lambda Z)-1)]>=0` for lambda>=0.
At `lambda0=1/(2R)`, the Taylor integral remainder gives
`e^z>=1+z+z^2/4` for `|z|<=1/2`. For example `e^(1/2)<2` follows by
strict comparison of its power series with the geometric series, proving
the required lower bound on the second derivative. Hence

\[
 \mathbb E e^{\lambda_0 Z}\ge1+\frac{\mathbb E Z^2}{16R^2},
 \qquad
 \log\mathbb E e^{\lambda Z}\ge\frac{\mathbb E Z^2}{32R^2}
 \quad(\lambda\ge\lambda_0),
\]

using `log(1+u)>=u/2` for `0<=u<=1/16`. The normalized sphere covariance
is `I_3/3`, so (8) yields

\[
 J(\lambda)\ge\eta:=\frac{(1-q)V}{96R^2}>0
            \quad\hbox{for every }\lambda\ge1/(2R).       \tag{9}
\]

This elementary scatter bound also appeared in the preceding
[dilated-martingale packet](../gaussian_dilated_martingale_certificate/PROOF.md).
It is rederived here; that packet's additional coupling condition is not
used or inferred. The substantive new obligation discharged here is (7).

The independently accepted [spherical-gap endpoint](../gaussian_majorisation_eventual_endpoint/PROOF.md),
Theorem 1, with [review](../gaussian_majorisation_eventual_endpoint_review2/README.md),
applies to (9) and proves every hinge for
`s>=R^2 max(8,44/eta)`. Since `V<=R^2` and `0<q<1`, `eta<1/96`;
this cutoff is exactly (2). The source lies in a radius-R ball about EX;
Kirszbraun extends T if necessary, and the target lies in a radius-R ball
about T(EX). Centered target radius R is not assumed. Independent
translation invariance of J permits these anchors.

For clarity, the endpoint signs the tail
`0<t<=C_s exp[-s/(8R^2)]` with error at most `44R^2/s`, and its accepted
high-noise window signs `t>=C_s exp[-9s/(64R^2)]`. The positive overlap
`9/64-1/8=1/64` covers every positive threshold. At zero both hinges are
one. The earlier analytic tail and high-noise arguments are credited
inputs, not repeated independent audits or checks performed by this code.

## 4. Exact certificate and a genuine separation from the coupling premise

For finite rational paired data the producer computes the maximum squared
distance ratio beta on active unequal source pairs. Equal source points
must have equal images. It accepts a rational `q in(0,1)` with
`27 beta<=q^2`, or chooses `q=(1+27 beta)/2` when `beta<1/27`.
The latter is valid because `(1-z)^2>=0` implies `(1+z)^2/4>=z`.
With `B=max|x_i-E X|^2`, it records
`eta=(1-q)V/(96B)` and `s_*=4224 B^2/((1-q)V)`.

The separate checker uses all ordered pairs to reconstruct source scatter,
the centered radius and the loss, then checks each prescribed pair against
the certified factor. The additional witness has constant size; the
operation count is O(n^2) in exact rationals and storage O(n), with bit
cost depending on the input. No covariance inverse, linear program,
quadrature, replica degree or minimum atom mass is needed. This is not
a complexity bound for unrestricted majorisation.

The uniform family is not restricted to the previous coupling premise.
Here is an exact calibration for the separation. For any
`0<epsilon<=1/100`, take the uniform 18-point law

    X=(u,v,z),  u,v in{-1,0,1}, z in{-epsilon,epsilon},
    Y=(|u|,|v|,|u+v|)/12.                               (10)

The map has squared Lipschitz constant at most `1/48`; this follows from
the squared operator norm 3 of `(u,v)->(u,v,u+v)` and the nonexpansion of
absolute values. Thus `q=3/4` certifies the entire epsilon interval,
with `V=4/3+epsilon^2` and `B=2+epsilon^2`.
Both endpoint covariances are full rank and the paired rank is six.
One common variance `s>=51000` covers the entire displayed epsilon interval,
because `16896(2+1/10000)^2/(4/3)<51000`.

The source covariance is `diag(2/3,2/3,epsilon^2)`. The target covariance is

\[
 \Sigma_Y=\begin{pmatrix}
 1/648&0&1/1944\\0&1/648&1/1944\\1/1944&1/1944&11/2916
 \end{pmatrix}\succeq I_3/972.                          \tag{11}
\]

Subtracting `I/972` leaves a symmetric diagonally dominant matrix with
nonnegative diagonal, hence a positive semidefinite matrix. Explicitly,
such matrices are sums of nonnegative multiples of `(e_i+e_j)(e_i+e_j)^T`
and coordinate squares here. As `epsilon^2<=1/10000<1/972`, the least
source covariance eigenvalue is strictly below the least target one.
No coupling `E[U|W]=aW`, even for a=1 and after arbitrary independent
isometries, can exist: squared conditional Jensen would imply
`Cov(U)>=a^2 Cov(W)`, contradicting least-eigenvalue monotonicity.

For the source labels with indices `0,1,2,4,6,12,16` in lexicographic
`(u,v,z)` order, the determinant with rows `(1,x_i,y_i)` is `-epsilon/54`.
Only its source-z column depends on epsilon, so determinant multilinearity
makes this an identity on the entire interval. This calibration certifies separation of sufficient
conditions; its folded geometry is already positive by known low-rank
compositions. It is not offered as a new geometric example class. The
new result is the universal map/law family (1)--(3), including arbitrary
maps with the uniform Lipschitz bound.

## 5. Cubature and limitations

The accepted same-pair degree-two cubature and loss-preserving refinement
preserve the means, source covariance and V on at most 19 original pairs.
The radius bound persists and every selected pair retains (1). Unlike a
newly tested compressed input, the original map already satisfies the
uniform pair bound. Passing a finite subset alone does not prove the
bound for discarded support. There is no equality of compressed hinges,
common cubature choice over a cell or unspecified diffuse-law oracle.

The accepted uniform-middle, zero-loss, covariance-boundary and loss-modulus
results are preserved. The present global strong-contraction condition
supplies a signed infinite spherical range directly. If it fails, the
checker reports unresolved, not a counterexample. The boundary beta=1/27
has no positive gap from this argument, and the full beta<=1 regime is
not reached. Smaller variances also remain outside this sufficient theorem.
No further adjacent factor tuning or catalogue is proposed here.

The preceding covariance/damping corollary is included with its stated
variance bound: its `c<=kappa/(4R^2)<=1/12` meets (1) with q=1/2, and
`V>=3kappa` gives `s_*<=2816R^4/kappa`. The present theorem also applies
without a positive covariance floor. The general dilated-martingale
theorem is retained: it can certify maps with preserved pairs, which (1)
cannot. Thus the two general sufficient tests have complementary scope.

The finite checker's exact-zero-loss branch uses distance rigidity.
Its point-target branch is all-variance: the source density is a mixture
of translates of one Gaussian, and convexity of each hinge bounds its
integral by that Gaussian's hinge. These are credited elementary equality
and point-target facts, not conclusions of a finite spherical computation.
