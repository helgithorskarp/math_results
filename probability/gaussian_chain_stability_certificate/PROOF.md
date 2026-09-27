# An exact all-threshold cloud certificate for mixed-chain endpoints

Complete author argument, 27 September 2026; independent review pending.
The unrestricted dimension-three Gaussian-majorisation question remains open.

This consumes R8's [mixed-chain margin, Theorem B](../gaussian_motion_chain_strictness/PROOF.md),
which incorporates R3's [polynomial norm-preserving margin](../gaussian_polynomial_hinge_margin/PROOF.md).
The contribution is an explicit **uniform all-threshold parameter-family
certificate** for non-anchored endpoints, with independent prior errors and
arbitrary endpoint cloud laws. Its budget depends on total endpoint loss,
not the number of links or the smallest positive link loss.

The mixed-chain sign, loss-linear margin, independence from chain length,
and qualitative ambient openness belong to the cited sources. We extend
the earlier [single-anchor cloud certificate](../gaussian_effective_anchored_neighborhoods/PROOF.md)
by supplying the full quantitative join and an exact finite consumer for the
broader mixed-chain margin. No new geometry class, unrestricted factorization,
practical full cover, or Kneser--Poulsen consequence is claimed.

## 1. Uniform parameter-family theorem

Normalize the variance interval to `[1,S]`, `S>=1`. An interval `[s0,s1]`
with `s0>0` is obtained by dividing coordinates and cloud radii by `sqrt(s0)`
and taking `S=s1/s0`.

Let `X^0,...,X^L`, `L>=1`, be lists of `n` labelled sites in R3, using the
same probability vector `v` at every stage. Every link is short:

```
Delta_ij^t=|x_i^(t-1)-x_j^(t-1)|^2-|x_i^t-x_j^t|^2 >= 0.    (1)
```

Fix an integer `R>=1`. The initial source fits a radius-`R` ball. Each link
must have one of the following **supplied** proofs:

- N: independent anchors `a_t,b_t` such that
  `|x_i^(t-1)-a_t|=|x_i^t-b_t|<=R` for every label;
- M: an admissible contracting motion in R5 in the precise sense of
  R8's Theorem B: isometric endpoint embeddings, nonincreasing pair distances,
  absolutely continuous trajectories, and finite integral of the maximal
  speed. Finite concatenations are allowed.

For finite labels the spatial continuity and measurability premises cause
no extra issue. Section 4 gives two elementary exact M certificates. We do
not accept an unsupported motion label. Repeated sites are allowed: (1)
forces identical sources to have identical targets, so every stage defines
a short support map after equal sites are merged. Zero-loss links are allowed.

Write `P=X^0`, `Q=X^L`. Independent translations put both endpoints in
radius-`Re` balls, for an integer `Re>=1`. Define

```
W(P)=integral_(S2) max_i theta.p_i d sigma(theta),
D(v)=sum_t sum_ij v_i v_j Delta_ij^t
    =sum_ij v_i v_j (|p_i-p_j|^2-|q_i-q_j|^2).              (2)
```

Here `sigma` is probability area measure. `W` is translation invariant and
half the usual mean width; the loss is ordered and telescopes label by label.
For integers `ell,a>=0` and rational `0<w<=2Re`, assume

```
v_i>=2^-ell,   sum_i v_i=1,
D(v)>=S 2^-a,                   W(P)-W(Q)>=w.               (3)
```

Define the following schedule, using **R8's mixed-chain exponent**:

```
A=6(Re+1)^2+2S(ell+1),          Q0=8A/w,
j=ceil(Q0^2),                  k=a+9R^2+4,
B_N=40R^2+9R+38,               B_M=66R^2+2R+18,
N=max(B_N+3j+8(k+1), B_M+4j+5(k+1))+k+2R^2+2R+1,
M=a+N,
2^-b_w<=w/2,                  b_w>=0 an integer,
B=max(M+1,k,ell+1,1,b_w).                                  (4)
```

**Theorem.** Let `u,z` be independent probability vectors on the labels.
Let `alpha_i,beta_i` be arbitrary Borel probability laws in the respective
closed balls `B(p_i,epsilon),B(q_i,epsilon)`. Put

```
mu'=sum_i u_i alpha_i,          nu'=sum_i z_i beta_i,
E=2epsilon+||u-v||_1+||z-v||_1.
```

If `E<=2^-B`, then, simultaneously for every `s in [1,S]` and `h>=0`,

```
H_(nu'*gamma_s)(h)>=H_(mu'*gamma_s)(h),
H_f(h)=integral_R3 (f-h)_+.                                 (5)
```

For `C_s=(2pi s)^(-3/2)`, the actual gap is at least `2^-(M+1)` throughout

```
C_s 2^-j <= h <= ||mu'*gamma_s||_infinity.                 (6)
```

That band may be empty. The perturbations need not preserve any link,
anchor, or contraction. Thus (5) also covers every genuine contraction pair
satisfying these guards. Clouds may be diffuse; the mass premise concerns
assigned clusters, not their internal atoms.

The **same budget** works for every reference chain, prior, cloud law and
variance with the fixed `R,Re,S,ell,a,w` guards. It contains no `L`, no
minimum positive step loss, and no selected large step. The guards must
actually hold uniformly; increasing the number of steps does not supply
them. This is a whole parameter-family guarantee, not isolated positive
samples or a procedure to find a chain for an arbitrary contraction.

## 2. Imported middle margin and the source-peak join

Fix `s in [1,S]`. Let

```
f=sum_i v_i gamma_s(.-p_i),       g=sum_i v_i gamma_s(.-q_i),
d=D(v)/s >= 2^-a,                M_f=||f||_infinity,
M_g=||g||_infinity.
```

All normalized radii in Theorem B of the mixed-chain source are at most `R`.
That theorem gives

```
H_g(h)-H_f(h) >= d 2^-N >= 2^-M                           (7)
```

on `C_s 2^-j<=h<=M_g-C_s 2^-k`, with exactly `N` in (4).
This entire analytic margin, including its uniformity in the number and
distribution of links, is imported. It is not proved by the integer checker.

The composite endpoint map is short. R8's already reviewed
[posterior peak lemma](../gaussian_norm_preserving_strictness/PROOF.md),
which requires no anchor, gives

```
M_g-M_f >= (C_s/4)(D/s) exp(-9R^2/2)
          >= C_s 2^-(a+9R^2+2) = 4 C_s 2^-k.              (8)
```

The second inequality uses `e<4`. Only the initial radius `R` is needed.
Gaussian translations by at most `epsilon` change a density by at most
`epsilon/sqrt(s)` in L1 and `C_s epsilon/sqrt(s)` in L-infinity. Integrate
over each cloud; prior changes cost their l1 norms, multiplied by `C_s`
for the latter bound. Since `s>=1`,

```
||mu'*gamma_s-f||_1+||nu'*gamma_s-g||_1 <= E,
||mu'*gamma_s||_infinity <= M_f+C_s E <= M_g-3 C_s 2^-k.   (9)
```

Thus every threshold in (6) lies inside the imported band. All probability
Gaussian mixtures are bounded by `C_s`, so no normalized threshold beyond
one is used. Hinges are 1-Lipschitz in density L1, and hence (7)--(9) yield
an actual gap at least `2^-M-E>=2^-(M+1)`, proving (6).

## 3. Signed low thresholds and complete coverage

The endpoint join uses the same signed cloud-tail lemma as the earlier
single-anchor certificate, with endpoint radius `Re` independently of `R`.
From (3)--(4),

```
u_i,z_i>=2^-(ell+1),   epsilon<=1/2,
W(P)-W(Q)-2epsilon>=w/2=delta.
```

After independent translations all actual support points lie in radius
`R0=Re+1` balls. In [the old signed cloud-tail lemma](../gaussian_majorisation_open_stability/PROOF.md),
Lemma 2, set `m=2^-(ell+1)` and

```
K=R0^2+2S log(1/m),
K+5R0^2<=6(Re+1)^2+2S(ell+1)=A,
4(K+5R0^2)/delta<=Q0.                                     (10)
```

It gives the explicit signed estimate

```
H_(nu'*gamma_s)(h)-H_(mu'*gamma_s)(h)
 >=4pi delta s h [log(C_s/h)+1]>0
```

for `0<h<=C_s exp(-Q0^2/(2s))`. Since `j>=Q0^2`, `s>=1`, and
`log(2)>=1/2`, every `0<h/C_s<=2^-j` is covered. Positive cluster mass
and the support-width reserve are essential; ordinary moment matching
or an absolute error bound does not supply this endpoint sign.

Above this cutoff and at or below the actual source peak, (6) applies.
Above that peak the source hinge vanishes and the target hinge is nonnegative.
At zero both hinges equal one. Both joins include their endpoints, completing
(5) without locating a peak or sampling a threshold grid.

## 4. Finite reduction and the exact motion guards

The executable accepts rational stages and guards. It checks every pair
in (1), the initial radius, all N anchor equations and radii, and both
endpoint radii. For M it accepts either of these sufficient proofs:

1. **Straight interpolation.** For every pair put
   `p=p_i-p_j`, `q=q_i-q_j`, and require `q.(q-p)<=0`.
   Along `(1-t)p+tq`, half the squared-distance derivative is an affine
   function of `t` with nonnegative slope `|q-p|^2`. Its maximum occurs
   at `t=1`, where it is nonpositive. The straight R3 motion is therefore
   contractive and is admissible in R5.
2. **Orthogonal lift.** Check shortness and
   `affdim(P_step)+affdim(Q_step)<=5` exactly. After independent translations
   and isometric coordinates in their affine spans, use
   `Z_t=(cos(pi t/2) P_step, sin(pi t/2) Q_step)` in the orthogonal sum.
   Every squared pair distance is `cos^2` times its source value plus
   `sin^2` times its target value, hence is nonincreasing. Finite supports
   give bounded smooth trajectories and the required speed integral.

These are the credited finite guards already supplied by R8's consumer;
we do not claim the motion constructions as new. A failed guard is unresolved,
not evidence of an adverse hinge. General motions allowed by the theorem
need a separately verified motion certificate; an unsupported label is
rejected by this executable.

For `m=2^-ell`, the nonnegative pair losses give throughout the entire
nonempty prior simplex

```
D(v)>=d0:=2m^2 sum_t sum_(i<j) Delta_ij^t
        =2m^2 sum_(i<j)(|p_i-p_j|^2-|q_i-q_j|^2).           (11)
```

Choose `a` with `2^-a<=d0/S`. The factor two is the ordered-loss convention.
A zero total floor is rejected; zero individual steps are permitted.
The supplied-record checker may use a smaller positive floor or larger
safe exponents than the producer, since it verifies inequalities.

For width, the executable reuses the prior nested-hull rational cap guard:
a barycentric matrix puts the centered target in the centered source hull.
A rational unit axis `n`, `0<=c<1`, `r>=sqrt(1-c^2)`, and source site `p*`
supply, for all targets,

```
A_i=n.(p*-q_i)>=0,   b_i>=|p*-q_i-A_i n|,
c A_i-r b_i>=gamma>0.
```

On the cap `theta.n>=c` the support gap is at least `gamma`; elsewhere it
is nonnegative by hull inclusion. The cap has probability `(1-c)/2`, so
`w=gamma(1-c)/2` is valid. The producer rounds each transverse bound upward;
the verifier checks its square. This sufficient width format is not complete
for every mixed-chain endpoint pair. The theorem can use any independently
proved `w`; the executable does not trust an unverified width scalar.
No new cap theorem or cap-count improvement is claimed.

An optional dual witness certifies failure of the old endpoint-anchor guard:

```
sum_i lambda_i=0,   sum_i lambda_i p_i=sum_i lambda_i q_i=0,
sum_i lambda_i(|p_i|^2-|q_i|^2) != 0.                      (12)
```

Expanding any proposed `|p_i-a|^2=|q_i-b|^2` and summing would contradict
(12). This concerns the supplied labelled correspondence; it does not
exclude every rematching or different reference representation of the laws.

The producer uses squared pair distances and rational row reduction for
ranks. The non-importing verifier uses Gram losses, the trace-variance
identity `sum_(i<j)|x_i-x_j|^2=n sum_i|x_i|^2-|sum_i x_i|^2`, and PSD
scatter-matrix principal minors for affine ranks. It checks the endpoint
loss telescope independently of the per-link totals. Both then check the
width and exponent inequalities. No Gaussian evaluations, solver statuses,
numerical peaks, or threshold grids occur.

Pair work is `O(L n^2)` rational operations; dense hull checks are `O(n^2)`.
The radius is independent of `L`, but reading/validating a chain is not.
Only the binary exponent `B` is stored, never `2^B` or `2^M`. Bit cost depends
on the rational sizes and `ell` as the bit length of its mass denominator.
Membership of an arbitrary diffuse cloud in the displayed support/error
budget remains the consumer's mathematical obligation.

## 5. Whole families and reproducible controls

The fifteen-label input is

```
0, +/-e_i, +/-2e_i (i=1,2,3), +/-(3/2,3/2,3/2).
```

For each coordinate, fold the side `x_i>3/2` across `x_i=3/2`, then the
side `x_i<-3/2` across `x_i=-3/2`. These are familiar folds, used only as a
deterministic guard control. Every intermediate stage and anchor is listed.
The endpoints move `+/-2e_i` to `+/-e_i` and leave other listed sites fixed.
The six unordered loss sums are `46,44,46,44,46,44`, totaling `270`.

Take `R=4`, `Re=3`, `S=4`, and the entire prior simplex `v_i>=1/32`.
The loss floor is `135/256`, so `a=3`. The existing cap guard gives
`gamma=13/200`, `w=13/20000`. Coefficients `-1,-1,+1,+1` at
`e_1,-e_1,2e_1,-2e_1`, respectively, give zero coefficient and first-moment
sums but squared-norm residual `6`. Thus this reference has **no endpoint
anchors**, for every prior in the simplex. Its certified cloud budget is

```
B=12564298226894,              s in [1,4].
```

Both endpoint diameters squared are `27`, attained by the unchanged diagonal
pair. This excludes the direct strict-homothety directional-MGF guard for
these same supports, because it would force containment in a `c<1` copy
of the source hull and a strictly smaller diameter. This is a diagnostic
against that sufficient guard, not a new geometric obstruction.

To exercise an actual M link, the suite **reuses R8's published eighteen-label
input unchanged**, with its norm step followed by an orthogonal lift of ranks
`2+3`. Our consumer adds prior, cloud and tail guards: `R=Re=2`, `S=4`,
`v_i>=1/32`, ordered loss floor `1503/1024`, and width `47/800`. The whole
family then has `B=771658035`. The underlying geometry and reference sign
are credited entirely to R8; this is an all-threshold certificate handoff,
not another generated example or a target-damping improvement.

The suite also subdivides a two-label distance contraction `2` to `1`
into `1,2,7,31,257` steps, alternating the three supplied guard types. For
any positive integer `L`, the sites are `0,r_j e_1`, `r_j=2-j/L`; an N link
has anchor `(r_(j-1)+r_j)e_1/2`. Every finite refinement has the same total
loss and schedule despite decreasing positive step losses. Other checks
cover 27 damaged inputs/records, 16 covariance prior controls, independent
stage translations, zero-loss insertion, and nine dependency pins.
The theorem, not these finite controls, proves the uniform continuum claim.

## 6. Status and remaining frontier

The displayed budgets are enormous. They certify mathematical neighborhoods,
not a usable coarse mesh of all contractions. The user-facing increment is
the whole mixed-chain family consumer beyond a single endpoint anchor,
with every threshold and the exact checking boundary made explicit.

R8's new mixed-chain margin and R3's polynomial refinement are author proofs
pending independent review. The underlying anchored sign, peak/strictness
result and the used old openness bridge have independent reviews, with the
precise scope recorded in [SOURCES.md](SOURCES.md). The source pins establish
byte identity, not analytic truth. The written motion/hinge/tail argument
is not formalized; passing the checker is author evidence, not independent
acceptance of this theorem.

R3's now independently accepted all-radius covariance-conditioned modulus/cubature is a separate
unrestricted finite-dependency input; it supplies no missing positive sign.
This packet does not manufacture one or use moment matching for support.
The accepted global defect bound and factorization obstructions are unchanged.
No all-variance neighborhood as `s` tends to zero, or radius uniform as total
loss or width tends to zero, is claimed. The unrestricted problem stays open.
