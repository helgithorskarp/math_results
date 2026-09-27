# An effective all-threshold neighborhood of an anchored contraction

Complete author argument, 27 September 2026; independent review pending.
This completes the quantitative R2/R3 handoff in
[R8's strictness theorem](../gaussian_norm_preserving_strictness/PROOF.md),
using the subsequent [polynomial hinge envelope](../gaussian_polynomial_hinge_margin/PROOF.md).
That source already proves qualitative ambient openness for every
nonisometric norm-preserving bounded contraction. We do not claim that
openness, or the unperturbed class, as a new result. The increment is a
finite, explicit **uniform parameter-family certificate**, including the
low and high thresholds, independent cloud laws, independent prior errors,
and one common spatial budget over a prescribed positive variance interval.

The unrestricted R3 problem remains open. The bounds below are very small
and do not give a practical coarse cover of that entire frontier. There is
no new all-variance class or Kneser--Poulsen limit.

## 1. Uniform family theorem

Work in spatial units in which the variance interval is `[1,S]`, `S>=1`.
An arbitrary interval `[s0,s1]`, `s0>0`, is obtained by dividing both
endpoint coordinates and cloud radii by `sqrt(s0)` and taking `S=s1/s0`.
The two endpoint anchors can be translated to zero independently.

Let `R>=1`, `ell>=0`, `a>=0` be integers, and `w>0` rational, `w<=2R`.
Consider **every** finite reference pair `P=(p_i), Q=(q_i)` and common
probability vector `v` satisfying

```
|p_i|=|q_i|<=R,
Delta_ij=|p_i-p_j|^2-|q_i-q_j|^2>=0,
v_i>=2^-ell,
D(v)=sum_ij v_i v_j Delta_ij >= S 2^-a,
mean_support(P)-mean_support(Q)>=w.                         (1)
```

Here mean support is the integral of the support function over the unit
sphere with probability area measure. The loss is ordered. There is no
covariance assumption. Repeated target sites are allowed. Repeated source
sites necessarily have the same target, by the pair guard, so the reference
is a well-defined short map after merging labels.

The following schedule depends only on the parameters in (1):

```
A = 6(R+1)^2 + 2S(ell+1),
Q0 = 8A/w,
j = ceil(Q0^2),
k = a+9R^2+4,
N = 40R^2+9R+38+3j+8k,
M = a+N.
```

Let `b_w` be any nonnegative integer with `2^-b_w<=w/2`, and put

```
B = max(M+1, k, ell+1, 1, b_w).                            (2)
```

Let `u,z` be two probability vectors on the same labels. Let `alpha_i`
and `beta_i` be arbitrary Borel probability laws supported in the closed
balls `B(p_i,epsilon)` and `B(q_i,epsilon)`, respectively. If

```
E = 2 epsilon + ||u-v||_1 + ||z-v||_1 <= 2^-B,              (3)
mu' = sum_i u_i alpha_i,       nu' = sum_i z_i beta_i,
```

then, simultaneously for every `s in [1,S]` and every `h>=0`,

```
H_(nu'*gamma_s)(h) >= H_(mu'*gamma_s)(h),
H_f(h) = integral_R3 (f-h)_+ .                              (4)
```

The perturbations are independent; neither an anchor equation nor a
contraction between the actual endpoint laws is required. Thus (4) also
covers every genuine contraction pair admitted by these support/prior
guards. Individual clouds may have arbitrarily many atoms or be diffuse.
The mass floor applies to the assigned clusters, not to their internal
atoms. The number of reference clusters is implicitly at most `2^ell`;
we make no claim of removing aggregate mass information.

There is also an explicit strict middle margin. Write
`f=sum_i v_i gamma_s(.-p_i)`, `g=sum_i v_i gamma_s(.-q_i)`,
`C_s=(2 pi s)^(-3/2)` and `M_g=||g||_infinity`. Throughout

```
C_s 2^-j <= h <= M_g-C_s 2^-k,
```

the actual hinge gap in (4) is at least `2^-(M+1)`. The band may be empty;
the all-threshold assertion does not require it to be nonempty.

The theorem is uniform over all reference geometries, priors, cloud laws,
and variances satisfying its displayed guards. It is not a finite sample
of positive density values. Section 6 gives one whole prior/cloud family
whose reference supports cannot satisfy the strict-homothety MGF buffer.

## 2. Consuming the polynomial middle margin

We import the [whole-curve polynomial bound, Theorem 1](../gaussian_polynomial_hinge_margin/PROOF.md):
write `u=h/C_s`, `m_s=M_g/C_s`, and `d=D/s`. Under the anchor/radius and
shortness hypotheses,

```
H_g(C_s u)-H_f(C_s u)
 >= d 2^-(40R^2+9R+38) u^3 (m_s-u)_+^8.                   (5)
```

Throughout `2^-j<=u<=m_s-2^-k` this is at least `d 2^-N` with the
exponent in Section 1. At every `s in [1,S]`, the normalized radius is
at most `R` and `d>=2^-a`; hence the reference middle margin is at least
`2^-M`. No recentering at a prior-dependent mean is performed.

The polynomial source uses the accepted positive spherical kernel and
R8's radial crossing, with a logarithmic radial endpoint. That entire
margin improvement belongs to the imported source. Its analytic proof,
including the smooth-hinge limit at critical levels, is not proved by our
integer guard checker. The present contribution is the quantitative
all-threshold perturbation join, not a duplicate middle-margin derivation
or an improvement to the global defect bound.

## 3. The low-threshold cover

Set `R0=R+1`, `delta=w/2`. From (2)--(3), `epsilon<=1/2`,
`u_i,z_i>=2^-ell-E>=2^-(ell+1)`, and

```
mean_support(P)-mean_support(Q)-2 epsilon >= w-E>=delta.
```

The explicit cloud tail estimate in
[the old stability proof, Lemma 2](../gaussian_majorisation_open_stability/PROOF.md)
therefore applies. All actual support points have norm at most `R0`.
In that lemma take

```
K=R0^2+2S log(1/m),    m=2^-(ell+1),
K+5R0^2 <= 6R0^2+2S(ell+1)=A,        log(2)<1.
```

Its cutoff `4(K+5R0^2)/delta` is at most `Q0`. For clarity, the signed
estimate being imported is

```
H_(nu'*gamma_s)(h)-H_(mu'*gamma_s)(h)
 >= 4 pi delta s h [log(C_s/h)+1] >0
```

whenever `0<h<=C_s exp(-Q0^2/(2s))`. It follows by enclosing the unique
large-radius superlevel boundary between quadratic roots, integrating its
cubic radial volume, and then using
`H_g(h)-H_f(h)=integral_0^h (V_f(r)-V_g(r)) dr`.
Positive assigned cloud mass is essential; ordinary moment cubature alone
does not supply it.

Since `j>=Q0^2`, `s>=1`, and `log(2)>=1/2`,

```
2^-j <= exp(-Q0^2/(2s)).
```

Consequently every normalized threshold `0<h/C_s<=2^-j` is covered,
uniformly in the variance and every admitted cloud law. No unsigned tail
error is subtracted from a vanishing hinge gap.

## 4. Peaks and the gap-free join

R8's [posterior peak lemma, Section 2](../gaussian_norm_preserving_strictness/PROOF.md)
gives, even without the anchor condition,

```
M_g-M_f >= (C_s/4)(D/s) exp(-9R^2/2)
          >= C_s 2^-(a+9R^2+2) = 4 C_s 2^-k.              (6)
```

Here the normalized radius is at most `R` and `e<4`. For a cloud shift
of at most `epsilon`, Gaussian directional derivative estimates give
an `L1` change at most `epsilon/sqrt(s)` and an `L-infinity` change at
most `C_s epsilon/sqrt(s)`. Prior changes cost their `l1` norm and `C_s`
times that norm, respectively. Since `s>=1`, the sum of the two `L1`
errors is at most `E`, and the source peak increases by at most `C_s E`.

Equations (2)--(3) and (6) therefore imply

```
||mu'*gamma_s||_infinity <= M_g-3 C_s 2^-k
                         <= M_g-C_s 2^-k.                 (7)
```

The hinge functional is 1-Lipschitz in density `L1`. On the band in
Section 2, its actual gap is at least

```
2^-M-E >= 2^-(M+1)>0.                                     (8)
```

Now let `h>0`. Below `C_s 2^-j`, Section 3 applies. If `h` is above that
cutoff and no greater than the actual source peak, (7) puts it inside the
closed middle band, so (8) applies. Above the source peak its hinge is
zero, while the target hinge is nonnegative. This covers every threshold,
including both join endpoints. At `h=0` both hinges equal one. This proves
the theorem without numerical peak location or a sampled middle grid.

## 5. Reduction to finite rational input

The supplied producer accepts rational sites and rational anchors,
an integer radius `R`, a mass exponent `ell`, a rational `S>=1`, and a
verified width witness. It first translates each anchor to zero and
checks every radius, norm equality and pair loss exactly. For the whole
nonempty prior region `v_i>=m=2^-ell`, it uses

```
D(v) >= d0 := 2m^2 sum_(i<j) Delta_ij.                      (9)
```

All terms in (9) have the correct sign. It selects an integer `a>=0`
with `2^-a<=d0/S`. Thus no optimization of a quadratic over a prior
simplex is hidden in the certificate. A zero loss floor is rejected.

A positive width value can be supplied by any proved support certificate,
including [R3's accepted support-cover quadrature](../gaussian_support_cap_localization/PROOF.md).
The current executable accepts the following inexpensive exact witness,
which suffices for a whole class of nested hulls. It is a guard, not a new
cap-comparison theorem:

1. Rational barycentric coefficients put every target site in `conv(P)`.
   Hence `h_P-h_Q>=0` on the entire sphere.
2. A rational unit vector `n`, `0<=c<1`, a rational `r>=0` with
   `r^2>=1-c^2`, and a source site `p_*` specify the cap `theta.n>=c`.
   For each target, put `v=p_*-q_i`, `A_i=n.v>=0`, and supply or compute
   `b_i>=0` with `b_i^2>=|v|^2-A_i^2`.
3. Check `c A_i-r b_i>=gamma>0` for every target. For every cap direction,
   `theta.v>=c A_i-r b_i`: write `theta.n=t>=c` and observe that
   `A_i t-b_i sqrt(1-t^2)` is increasing on `[c,1]`.
   The cap has probability `(1-c)/2`, so `w=gamma(1-c)/2` is valid.

All these checks are rational; the producer rounds each `b_i` upward
to a dyadic with the supplied precision (16 bits by default). This width
format is deliberately sufficient, not complete
for arbitrary anchored finite configurations. The theorem can consume
other rigorously established `w`; the executable never accepts an
unverified scalar width value or treats ordinary moment matching as a
support certificate.

The certificate stores the integers `j,k,N,M,B`, not the denominator
`2^B`. It checks the full continuum by the proof above; it does not list
an astronomical collection of thresholds or construct dyadic coordinates
with billions of digits. The exact pair and containment checks and the
integer schedule have polynomial bit complexity in the label count, the
bit lengths of the rational data, the supplied dyadic rounding precision,
and `ell` (the bit length of its dyadic
mass denominator, not the shorter encoding length of the integer `ell`).
Testing membership of a separately specified
cloud law in (3) remains that consumer's mathematical responsibility.

## 6. A whole undamped family and a precise buffer separation

The compact input uses

```
P=(0, e1,-e1, e2,-e2, e3,-e3),
Q=(0, e1,-e1, e2,-e2, e3, e3),
R=1, ell=4, S=4.
```

Every prior in the six-dimensional simplex `v_i>=1/16` is admitted. The
only strictly lost unordered pair is `(e3,-e3)`, with squared loss 4;
the other 20 pairs preserve distance. Thus `D(v)>=1/32`, and `a=7` works
simultaneously over `[1,4]`. On the cap `theta.(-e3)>=4/5`, the source
support exceeds the target support by at least `1/5`; the cap probability
is `1/10`. Globally `Q` is contained in `P`, so `w=1/50` is certified.
The complete integer schedule is recorded in `CERTIFICATE.json`.

Both reference supports have diameter 2, because the target retains
`e1,-e1`. Suppose the MGF of any translated/rotated target law were
dominated in every direction by that of a strict homothety `c<1` of any
translated/rotated source law with these supports. The large-ray Laplace
limit would put the target convex hull inside the homothetic source hull.
Their diameters would then satisfy `2<=2c`, a contradiction. Positive
weights on all seven labels ensure the specified supports. This rules
out the strict-homothety MGF buffer **for these reference endpoints**,
including independent endpoint rigid motions. It does not rule out some
different reference construction or a chain of other sufficient classes.

The unperturbed fold is already an all-variance example. Its purpose here
is to instantiate the entire independent-prior and arbitrary-cloud family
in (3), with a strictly positive computable radius, outside that direct
buffer premise. Neither the fold itself nor one selected cloud is offered
as a newly solved configuration. Qualitative existence of this neighborhood
was already implied by R8's strictness and the older openness theorem.

## 7. Verification boundary

`certificate.py` is an exact producer. `verify.py` imports no producer code
in supplied-certificate mode. It checks the Gram form of every loss,
recovers the uniform ordered loss through sums of endpoint vectors,
checks the barycentric and cap inequalities, and checks integer schedule
inequalities without expanding a huge dyadic number. Its guards quantify
over the entire prior region, variance interval and cloud family.

The accompanying tests corrupt geometric, width and schedule data and
check boundary schedules. These are author controls, not independent peer
review. The positive spherical identity, smooth-hinge integration,
posterior variational argument, Gaussian derivative estimates and signed
tail-volume lemma are written analytic trust boundaries. Source pins and
attribution are in `SOURCES.md` and `DEPENDENCIES.json`. No floating-point
evaluation, SAT solver, numerical cubature or infinite search is involved.
