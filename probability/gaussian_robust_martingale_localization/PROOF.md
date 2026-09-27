# A uniform all-threshold neighborhood of a dilated-martingale certificate

27 September 2026. Complete author proof; independent acceptance pending.
The unrestricted bounded-law dimension-three comparison remains open.

## 1. Reference data and the neighborhood

Let X_0,Y_0 be centered bounded probability laws in R3. Suppose

```text
|X_0|<=R, R>0, V=E|X_0|^2>0,
a>1, and a coupling (U,W) has these laws and E[U|W]=aW.   (1)
```

The reference coupling is an endpoint-law witness, not necessarily the
original deterministic matching. No covariance eigenvalue lower bound is
assumed. From (1), |Y_0|<=R/a and E Y_0=0. The reference laws themselves
need not have a specified matching for the proof below; the finite producer
also checks reference pair contractivity to match R2's existing input format.

Here is the precise meaning of a spatial and prior neighborhood. First
replace each reference law by a probability law with density relative to
it lying in [1-rho_x,1+rho_x] or [1-rho_y,1+rho_y], respectively. Then move
that reweighted law by a transport plan of displacement at most
alpha_x R or alpha_y R, respectively. The two plans are independent.
Assume alpha_x,alpha_y>=0 and 0<=rho_x,rho_y<=1/2. Call the resulting laws
mu,nu. They may be atomic, diffuse, or mixed.

For a finite reference, this means replacing each atom x_i by any probability
cloud supported in B(x_i,alpha_x R), and replacing its weight p_i by q_i
with |q_i-p_i|<=rho_x p_i, sum q_i=1. The analogous construction is independent
at the target. There is no lower bound on p_i>0 and no bound on the number
of clouds. Clouds may overlap. Zero reference weights can simply be removed;
they do not authorize new unlocated mass.

For the actual Gaussian comparison, impose the additional condition

```text
nu=T_#mu for a 1-Lipschitz map on supp(mu).                (2)
```

This condition is not implied by proximity of the two laws. Define

```text
B=R^2, beta=V/B, e=1-1/a, t=1+alpha_x,
P=alpha_x+alpha_y+4t(rho_x+rho_y),
L=e beta/(48t)-P.                                        (3)
```

**Theorem.** If L>0, then every pair satisfying (1)--(3), simultaneously
for every Gaussian variance and density threshold in the ranges

```text
s>=88 B t^3/L,                       h>=0,                (4)
```

satisfies

```text
integral (nu*gamma_s-h)_+ >= integral (mu*gamma_s-h)_+.    (5)
```

All members of the neighborhood share the same cutoff. In particular this
is an actual all-threshold sign transfer from a reference certificate to
an entire spatial/prior family, not a finite selection of thresholds.
At zero perturbation, (4) is exactly
`4224aR^4/((a-1)V)`, the accepted R2 cutoff. With
`P<=e beta/(96t)`, a simpler sufficient bound is
`s>=8448 B t^4/(e beta)`.

## 2. A linear spherical margin on the entire parameter half-line

For a bounded law lambda let

```text
M_lambda(z)=E exp(z.theta.X),
S_lambda(z)=integral_(S2) log M_lambda(z) d sigma(theta),
J(z)=S_mu(z)-S_nu(z),         sigma(S2)=1.
```

All z in this section are nonnegative. Independent translations of the
laws do not change S, since the added linear function of theta averages
to zero. We use R_*=Rt and z_0=1/(2R_*).

R2's conditional Jensen argument gives, for the reference laws,

```text
M_Y0(z)<=M_Y0(az)^(1/a)<=M_X0(z)^(1/a),
J_0(z)>=e S_X0(z).                                       (6)
```

At z_0, |z_0 theta.X_0|<=1/2. The elementary inequalities
`exp(v)>=1+v+v^2/4` on |v|<=1/2 and `log(1+w)>=w/2` on 0<=w<=1/16
therefore give

```text
log M_X0(z_0)>=z_0^2 E(theta.X_0)^2/8.                   (7)
```

The base is centered, so the linear term vanishes. Convexity of log M
and log M(0)=0 imply
`log M(z)>= (z/z_0)log M(z_0)` for every z>=z_0. Equivalently apply
Jensen to the power z/z_0>=1. Averaging (7), using
`integral(theta.X_0)^2 d sigma=V/3`, proves

```text
J_0(z)>= e z V/(48R_*)    for EVERY z>=1/(2R_*).          (8)
```

The unbounded linear factor, rather than only a fixed positive margin,
is what makes the neighborhood effective. Its slope and scalar ingredients
are not asserted optimal. Convexity of log M is classical.

## 3. Perturbations spend a bounded part of that slope

The reweighting and displacement assumptions give, in each direction,

```text
(1-rho_x)e^(-z alpha_x R) M_X0(z)
 <= M_mu(z) <= (1+rho_x)e^(z alpha_x R) M_X0(z).
```

Because -log(1-rho)<=2rho and log(1+rho)<=2rho for 0<=rho<=1/2,

```text
|log M_mu(z)-log M_X0(z)|<=z alpha_x R+2rho_x.             (9)
```

The same holds at the target. These estimates need neither regularity of
the clouds nor a minimum mass. For z>=1/(2Rt), the constant weight errors
satisfy `2(rho_x+rho_y)<=4zRt(rho_x+rho_y)`. Combining (8)--(9) gives

```text
J(z)>= z R [e beta/(48t)-P]=z R L.                      (10)
```

Thus the entire parameter half-line has the uniform margin

```text
J(z)>=eta:=L/(2t)>0,    z>=1/(2Rt).                     (11)
```

No finite-interval approximation, mean-support mass floor, or assertion
about infinitely many unchecked numerical values enters this step.

## 4. The signed ranges overlap at every threshold

The actual source is contained in a ball of radius R_*=Rt about the
reference source mean; it need not be centered at its own mean. By (2)
and Kirszbraun extension, the target lies in a ball of the same radius
about the image of that source-ball center. These anchors may differ
from those used in (9); the spherical average J is translation invariant.

The independently accepted spherical-gap endpoint6032/6048 says that
(11) gives all thresholds for

```text
s>=R_*^2 max(8,44/eta).                                  (12)
```

Its low range is `h<=C_s exp(-s/(8R_*^2))` and its high-noise range is
`h>=C_s exp(-9s/(64R_*^2))`. Since 9/64>1/8 they overlap. This is the
credited analytic join; no new Gaussian tail formula is substituted.
Because 0<beta<=1, e<1, t>=1 and P>=0, one has eta<1/96.
Thus (12) reduces to (4). At h=0 both hinges equal one; above the common
Gaussian kernel peak they vanish. This proves (5), including all positive
thresholds tending to zero and every s in the displayed half-line.

## 5. Finite-cover and parameter-cell consequence

A finite reference and a certified covering of actual endpoints by its
cloud balls give the stated transport plans. Relative prior intervals
supply rho_x,rho_y. Therefore a reference coupling plus the four scalar
errors is a finite sufficient certificate for every actual contracting
pair in that family. Ordinary cubature moment matching alone does not
supply these support coverings. A witness valid only on retained atoms
must not be treated as valid on discarded support without a cover.

For source quantization there is a useful exact-zero handoff. Partition a
bounded law into cells of radius h about original support sites x_i, use
p_i equal to their masses, and take y_i=T(x_i). The finite pair is still
contractive and the two endpoint displacements are at most h. If that
finite reference has a dilated-martingale witness and passes (3), use
alpha_x=alpha_y=h/R and rho_x=rho_y=0 to certify the ORIGINAL law at all
thresholds. This is a conditional positive completion, not a promise that
quantization of an arbitrary unresolved input supplies the witness.

The coupling can be stored in R2's nine-entry affine-density form, or in
any other exactly checkable form. The code implements that form and a
diagonal witness. It streams all reference masses and conditional moments
in O(n^2) exact operations and O(n) working storage. There is no beta degree
or inverse-threshold dependence in this guard. Arithmetic bit complexity
and validating a supplied spatial cover remain genuine costs.

The general theorem allows arbitrary bounded reference laws with a given
coupling. The finite producer does not claim an effective oracle for an
unspecified diffuse reference law or a complete cover of the unrestricted
frontier. It adds actual all-threshold signs on the admitted neighborhoods;
it does not repair the old geometric-tail/moving-window join6478.

## 6. Scope and evidence

A checked control has reference source points (s1,s2,0), target (s1/2,s2/2,0),
with s1,s2 in {-1,1}, uniform weights and a=2. The perturbed source has
points (s1,s2,zeta s3), s3 in {-1,1}, with zeta=2^-24; its target is
(s1/2,s2/2,eta0 s1s2+zeta s3), eta0=2^-12. Their covariance spectra are
(1,1,zeta^2) and (1/4,1/4,eta0^2+zeta^2). The least target eigenvalue exceeds
the least source eigenvalue. Hence after any separate rotations there is
no center-law martingale from the actual source to any dilation >=1 of
the actual target. Pairwise contraction and the neighborhood budgets are
checked exactly. A pair differing only in s3 is preserved, so the actual
map has Lipschitz constant one. The new R2 strong-map guard6486/6490 cannot
cover it. At s=32768 its normalized target radius exceeds 1/512, whereas
R8's new small-target schedule6482 always requires radius at most 2^-1405:
in that schedule R>=1,j>=0 give S>=36,m>=1369,Z>=4,B>=1404. Thus that
displayed sufficient schedule does not cover this input at this variance.
Our uniform transfer uses alpha_x=alpha_y=1/4096 and no prior error and
does sign all thresholds at s=32768. These are comparisons of sufficient
interfaces, not claims of novel positivity for the control. Its straight
interpolation is already a continuous contraction: for each pair, the
increasing derivative of the squared distance is nonpositive at time one,
which the checker verifies exactly. Classical continuous-contraction
majorisation therefore already applies to this small control.

The useful assertion is uniformity over EVERY actual contraction pair in
the stated neighborhoods, including arbitrary diffuse clouds and independently
perturbed priors. It requires neither a covariance floor nor a globally
strong contraction. This makes a finite reference witness consumable by
the localization lane, without claiming that the two newer sufficient
theorems themselves are subsumed.

The continuum proof consists of (6)--(12), credited Jensen and Gaussian
endpoint inputs, and the covering interpretation. The checker audits finite
couplings, exact schedules, boundary cases, scaling and damaged inputs.
It does not formalize those analytic arguments. Independent acceptance of
the new transfer is pending. No unrestricted theorem, improved global7/50
bound, all-variance conclusion or new Kneser--Poulsen consequence is claimed.
