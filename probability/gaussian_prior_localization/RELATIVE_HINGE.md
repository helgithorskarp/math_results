# Threshold-relative sign certificates on the existing localization frontier

Complete author proof and exact-arithmetic implementation. Independent
mathematical review and formalization are pending. The unrestricted R3
Gaussian-majorisation question remains open; the accepted universal bound
`D<=7/50` is unchanged.

The [absolute hinge oracle](DIRECT_HINGE.md) gives converging defect intervals,
but an absolute quadrature remainder can overwhelm a small-threshold hinge.
Here the remainder is proportional to the threshold itself. This supplies
an actual **signed-window consumer** for the existing finite configurations,
including windows with exponentially small endpoints. It does not change
the paired-cubature family or introduce an equivalent class of energies.

The endpoint/middle architecture is already due to R8's
[finite certificate interface](../gaussian_majorisation_open_stability/CERTIFICATE_INTERFACE.md).
This note supplies a different numerical middle certificate, with explicit
relative error and a successful Gaussian control. R8's signed-tail and
peak obligations remain necessary when a window is used to certify every
threshold. No full configuration cover or new geometric class is asserted.

## 1. Statement

Work at variance one, put `C=(2pi)^(-3/2)`, and let `f=mu*gamma`, `g=nu*gamma`.
The probability laws may be diffuse. After separate translations suppose
both mixing supports lie in `[-R,R]^3`. A contraction is not needed for the
quadrature theorem, but is checked by default for finite program inputs.
Use the adverse sign convention

    H(u)=integral(f-Cu)_+ - integral(g-Cu)_+,
    J(u)=H(u)/(C u),                  0<u<=1.                 (1)

Thus **negative J is the desired sign**. This is the opposite sign to the
team's beta-profile convention. Equal total mass gives the useful identity

    J(u)=integral[min(g/C,u)-min(f/C,u)]/u.                   (2)

Fix a window `0<a<=b<=1` and a bound `r>=sqrt(2log(1/a))`. Let `h>0`,
`M>=0` be an integer, and define

    S=(M+1/2)h,     T=S-R>0,
    B_R(r)=4R(4R^2-1)_+ +4 max(1,2R+r),
    P(u)=h^3 sum_(j in {-M,...,M}^3)
                       [min(g(hj)/C,u)-min(f(hj)/C,u)]/u.

**Theorem.** Simultaneously for every u in [a,b],

    |J(u)-P(u)| <= E_rel,
    E_rel=3h^2 S^2 B_R(r) + [38/(T a)] exp(-T^2/2).          (3)

The cube is tiled by cells of side h centered at the lattice sites. In
particular its boundary is at `S`, not `Mh`. The first term in (3) contains
no inverse threshold, atom count, level-set count, or geometric regularity
constant. The tail contains `1/a`, which is compensated by choosing T of
order `sqrt(log(1/a))`. Section 5 makes the resulting cost explicit.

If rational intervals enclose every finite-lattice density value, they
give an exact interval `[p_-,p_+]` for `max_[a,b] P`. Consequently

    p_- - E_rel <= max_[a,b] J <= p_+ + E_rel.               (4)

A negative upper endpoint certifies **every** threshold in the window.
A positive lower endpoint, with its recorded lower-maximizing threshold,
certifies an adverse hinge. It is a conjecture counterexample only when
the same input also passes the contraction checks. A window containing
zero is excluded from (1)--(4), rather than silently divided by zero.

## 2. The one-dimensional clipped-variation estimate

On a coordinate slice write the normalized Gaussian mixture as

    q(t)=sum_i v_i exp(-(t-c_i)^2/2),
    v_i>=0, sum_i v_i<=1, |c_i|<=R.

An integral over centers works identically for a diffuse law. For `u>=a`,
put `F(t)=min(q(t),u)`. We claim

    ||F''||_TV <= u B_R(r).                                 (5)

First, concave smooth approximations to the clip have derivative in [0,1]
and nonpositive second derivative. The positive part of their composed
second derivative is therefore bounded by the positive part of q'',
restricted, in the limit, to `{q<u}`. Their first derivatives tend to zero
at both infinities. Total second-derivative mass is zero, so

    ||F''||_TV <= 2 integral_{q<u} (q'')_+.                  (6)

This also follows by the distributional chain rule: the level-crossing
atoms for a concave clip are negative. Smooth approximation handles
critical levels. A nonzero slice is analytic and nonconstant, so a positive
level has measure zero; the zero slice is immediate. Gaussian domination
justifies the approximation, also for diffuse mixing laws.

On `[-R,R]`, every `|t-c_i|<=2R`, hence

    (q'')_+ <= (4R^2-1)_+ q.

Its contribution to the integral in (6) is at most
`2R(4R^2-1)_+ u`.

For `t>=R`, q is decreasing. The portion where q<u is `[t_0,infinity)`
up to a null boundary, with either `t_0=R`, `q(R)<=u`, or `q(t_0)=u`.
In the latter case the support envelope

    q(t)<=exp(-(t-R)^2/2)

implies `t_0<=R+sqrt(2log(1/u))<=R+r`. For a single center c<=R,
direct integration of the positive part of the Gaussian second derivative
gives, with `v=max(1,t_0-c)`,

    integral_(t_0)^infinity [((t-c)^2-1) exp(-(t-c)^2/2)]_+
                      =v exp(-v^2/2)
                      <=max(1,t_0+R) exp(-(t_0-c)^2/2).

The positive part of a sum is at most the sum of the positive parts.
Thus the right tail contributes at most `u max(1,2R+r)`.
The same estimate holds on the left. Multiplying the three contributions
by two as in (6) proves (5). No bound on the number of modes was used.

## 3. Finite tensor quadrature and the tail

For a one-dimensional cell of width h, midpoint quadrature has a Peano
kernel whose absolute value is at most h^2/8. The same bound holds when
the second derivative is a finite signed measure, by integration against
that kernel. Summing cells gives

    |h sum F(midpoints)-integral_(-S)^S F|
                  <=(h^2/8)||F''||_TV.                    (7)

Kernel values at cell endpoints are zero, so a corner on a shared cell
boundary does not double the variation bound. For clarity, on each half
cell the kernel is minus one half the square of the distance to the nearest
outer endpoint. This also proves (7) by smooth approximation.

Telescope the three positive coordinate operators for tensor midpoint
quadrature minus integration. Each of the other two coordinates has total
weight or length `2S`. Equation (5), uniformly in those fixed coordinates,
therefore bounds one endpoint's cube error by

    3(h^2/8)(2S)^2 u B_R(r).

There are two endpoint clips in (2); divide by u. This is precisely the
first term `3h^2 S^2 B_R(r)` in (3).

For the exterior of the cube, each normalized mixture satisfies

    integral_outside(f/C)
       <=12 pi exp(-T^2/2)/T <38 exp(-T^2/2)/T.             (8)

Indeed in one coordinate the two Gaussian tails are at most
`2 exp(-T^2/2)/T`, and the other two coordinate integrals equal `2pi`.
Sum over three coordinates. The same bound holds for g. Each omitted
clipped integral is nonnegative and bounded by (8), so their **difference
costs one copy** of that bound. Divide by `u>=a` to obtain (3).

## 4. Exact all-window sweep and implementation

The implementation [relative_hinge.py](relative_hinge.py) reuses the
validated rational exponential routine from [direct_hinge.py](direct_hinge.py).
It computes intervals for f/C and g/C with denominator `Q=2^p` and width
at most `8/Q`. For an upper clipped profile it uses **g_hi and f_lo**;
the lower profile uses g_lo and f_hi. This differs from the upper hinge
profile in the earlier oracle, and is checked separately.

The clipped numerator is affine between successive rational density-value
knots. Dividing an affine function by positive u is monotone on each such
interval. Therefore its maximum over [a,b] occurs at an endpoint or a knot
inside that window. The program sweeps all such knots with exact Fraction
arithmetic; it neither samples thresholds nor assumes unimodality.
The interval width from density evaluation is at most

    16(2S)^3/(Q a),                                        (9)

and the program also reports the sharper width from its actual histograms.
There is no Gaussian prefactor enclosure in (2)--(4): C has canceled.

Independent translations center each endpoint's coordinate bounding box.
An optional coordinate-table compression groups indices only when their
entire interval vectors, across every atom, agree. The product of the
three recorded multiplicities accounts for every site. It is an exact
summation optimization, not an assumption of geometric symmetry.

The finite checker compares every histogram entry against the uncompressed
implementation on nine fixtures; checks the window sweep against direct
evaluation of all knots in 2,187 cases; checks the midpoint kernel on 17
hinged linear functions; rejects four malformed arithmetic/coverage inputs;
and retains an isometry control. The substantial Gaussian control follows.
These are author checks, not independent mathematical review.

## 5. Why very small thresholds need not force an exponential spatial grid

For a prescribed relative accuracy epsilon, write
`Lambda=sqrt(2log(1/a))`. Choosing

    T>=Lambda+sqrt(2log(304/epsilon))+1

makes the tail in (3) at most epsilon/8 (for `0<epsilon<=1`). One can
choose rational upper bounds for the radicals. With `h<=1`, use
`S_bar=R+T+1` when choosing h in advance, then
`M=ceil((R+T)/h)` gives `S<=S_bar`. For example

    h^2 <= epsilon/[24 S_bar^2 B_R(r)]

makes the spatial error at most epsilon/8. Taking
`Q>=32(2S_bar)^3/(a epsilon)` makes (9) at most epsilon/2. The two copies
of the quadrature/tail remainder in (4), plus this arithmetic width, are
therefore at most epsilon in total.

The leading spatial site count is

    O(epsilon^(-3/2) S_bar^6 B_R(r)^(3/2)),                 (10)

with logarithmic precision `p=O(log(1/a)+log(1/epsilon)+log S_bar)`.
At fixed R and fixed epsilon, choosing `r=Lambda+O(1)` makes (10)
`O(Lambda^(15/2))`. Thus the spatial cost is polynomial in the logarithmic
threshold radius. The absolute oracle would require allocating an error
of order a to obtain the same relative enclosure.

This is a sign-relevant complexity statement: if an input has
`J(u)<=-epsilon` throughout a window, refinement to total enclosure width
below epsilon makes the test certify that whole window. It is not a
uniform lower bound on an unknown Gaussian sign. Fine accuracy, large
support, many atoms, and the enormous number of frontier configurations
can still make a complete cover infeasible.

## 6. A complete signed-window control

Take the probability law `(delta_(-e1)+delta_(e1))/2` and map both points to
zero. This is a known-positive continuous contraction. The new certificate
uses exactly

    a=2^-26, b=2^-24, R=1, r=61/10,
    h=1/10, M=100, S=201/20, T=181/20, p=56.

Every threshold in [a,b] is covered. The relative quadrature remainder is
`13453533/100000`, the tail remainder is below `10^-8`, and the final
upper bound on `max J` is **less than -30**. The exact fractions and hashes
are in [RELATIVE_EXPECTED.json](RELATIVE_EXPECTED.json). The old absolute
bound divided by `C a` is above one million on this same spatial grid.
The new sign is therefore supplied by the relative proof, not by applying
the old error bound to tiny floating-point gaps.

The full lattice contains 8,120,601 sites per endpoint. Identical interval
tables reduce the evaluated products to `198*90*90` and `90^3` respectively.
The exact standard-library replay takes about nine seconds and 42 MB on the
author's CPython 3.11 host. No large lattice arrays are published.

Run from this directory:

```sh
python3 -B relative_hinge.py --check
python3 -B -O relative_hinge.py --check
```

Expected status: `RELATIVE_HINGE_WINDOW_CERTIFICATES_PASS`. For another
variance-one rational input in the original `source,target,weights` schema:

```sh
python3 -B relative_hinge.py --input instance.json --umin 1/67108864 \
  --umax 1/16777216 --log-radius 61/10 --step 1/10 --tail 9 --bits 56
```

The program verifies `exp(-r^2/2)<=a` with an outward enclosure. An
insufficient r, insufficient precision for that check, or invalid
contraction is rejected. `--allow-noncontraction` is diagnostic only.

## 7. Dependency handoff and remaining sign obligation

On the unchanged [paired-cubature rational frontier](CUBATURE_FRONTIER.md),
this evaluates the same actual configurations as the previous absolute
oracle. It can certify windows where a beta expansion is impractical,
and can coexist with R2/R8's exact beta signs. R8's new
[seven-factor theorem](../gaussian_seven_factor_kernel/PROOF.md), now
[independently accepted by R5](../gaussian_seven_factor_review_r5/REVIEW.md),
signs `N-j<=7`; it is independent of (3). The first general unsigned
entry is now `b_(8,0)`.

To obtain **every threshold for an input**, supply R8's signed low endpoint
`H<=0 on [0,tau]` in the present adverse convention, an actual source peak
upper bound b, and a gap-free finite cover of [tau,b] by windows certified
here. Above b the source hinge vanishes. This is the existing endpoint
architecture with a direct producer for its middle sign; no new equivalence
or automatic endpoint sign is inferred. Parameter cells additionally need
uniform endpoint data and perturbation reserves, as in the credited
interface. Our earlier absolute error and transport bounds remain useful
when the objective is a nonzero global defect tolerance.

The control in Section 6 certifies only its displayed window; its known
all-threshold theorem is not newly proved by that run. No unknown contraction,
entire rational family, all-weight box, unrestricted zero-defect theorem,
or new Kneser--Poulsen consequence has been certified. The next mathematical
obligation is an actual signed cover or decreasing global defect bound on
the unrestricted frontier. The analytic clip/variation proof and exact
Python arithmetic remain unformalized trust boundaries.
