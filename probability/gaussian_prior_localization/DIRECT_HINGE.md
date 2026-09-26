# Direct, error-controlled hinge certificates on the paired-cubature frontier

Complete author proof and exact-arithmetic implementation. Independent
mathematical review is pending. The full bounded-law R3 Gaussian-majorisation
question remains open, and its accepted universal bound `D<=7/50` is unchanged.

This supplies a usable **evaluation and sign-detection step** for the existing
paired-cubature configurations. It computes an interval for the maximum defect
over **every threshold**, without density moments, alternating beta sums,
replica enumeration, or a sampled threshold grid. A refinement makes that
interval converge to the actual defect. It is not a new class of equivalent
test functions or a proof that all the intervals contain only zero.

The analytic ingredient is a uniform second-order quadrature error for a
Gaussian hinge, despite its corner at a density level. The method is classical
trapezoidal quadrature and piecewise-linear maximization; no invention of those
methods or historical priority is claimed. All constants needed here are
proved below. The new campaign deliverable is the certified all-threshold
oracle, its polynomial cost per existing rational input, and its explicit
composition with the accepted localization.

## 1. The oracle and the actual certificate

Work at variance one; common spatial scaling treats any positive variance.
Let f and g be Gaussian convolutions of two probability laws in R3, with
mixing supports in `[-R,R]^3`, after separate translations. No contraction is
needed for the oracle. Write

    C=(2 pi)^(-3/2),
    H(u)=integral(f-Cu)_+ - integral(g-Cu)_+,  0<=u<=1,
    Delta=max H(u).

Here positive H is an adverse hinge. This is the **opposite sign** to the
team's beta-profile convention. Both endpoint values of H are zero, so
`Delta>=0`. Let h>0, choose an integer M with `T=Mh-R>0`, and put

    Lambda={h j : j in Z^3, |j_l|<=M},
    P(u)=C h^3 sum_(z in Lambda) [(f(z)/C-u)_+-(g(z)/C-u)_+],
    G_h=1+h^2/8,
    E(h,T)=(h^2/4)(1+G_h+G_h^2)
                       +(3G_h^2/T) exp(-T^2/2).                 (1)

**Theorem 1.** Uniformly over all thresholds and all such laws,

    |H(u)-P(u)| <= E(h,T).                                    (2)

Consequently an interval `[p_-,p_+]` enclosing `max P(u)` gives

    max(0,p_- - E) <= Delta <= min(1,p_+ + E).                 (3)

The exact implementation returns this interval, separate quadrature/tail
errors, a maximizing threshold for each discrete bound, stream hashes, and
the number of lattice sites covered. If the lower endpoint is positive,
its recorded lower-maximizing threshold is a certified adverse hinge.
It is a contraction counterexample only if the input contraction checks
also pass. A positive lower endpoint on the deliberately noncontracting
control below is not a counterexample to the campaign problem.

Increasing M alone does not remove the quadrature error. For convergence,
take `h->0`, `T->infinity`, and precision high enough that `p_+-p_->0`.
Running maxima of lower endpoints and running minima of upper endpoints
then give nested intervals converging to Delta. They tend to zero exactly
when that input has Delta=0. Isometry, collisions and zero weights require
no positive margin, and no finite termination of an exact zero test is claimed.

## 2. Why the hinge still has a second-order quadrature bound

Let `phi(t)=(2pi)^(-1/2) exp(-t^2/2)`. Integration at the sign changes
of `phi''=(t^2-1)phi` gives

    integral |phi''| = 4 phi(1) < 1.                           (4)

Indeed `2pi e>16`, using `pi>3` and `e>8/3`.

For a decaying one-dimensional function F whose distributional second
derivative is a finite signed measure, the composite trapezoidal rule has

    |h sum_j F(jh)-integral F| <= (h^2/8) ||F''||_TV.           (5)

On one interval `[jh,(j+1)h]`, its error is the integral of F'' against
`(t-jh)((j+1)h-t)/2`, whose absolute value is at most `h^2/8`.
Sum over intervals and pass to the infinite limit. This also proves the
measure-valued version by approximation, including a corner at a grid point.

If p is a positive smooth Gaussian mixture on a line and `F=(p-a)_+`, then

    ||F''||_TV <= integral |p''|.                              (6)

To include critical levels, approximate the hinge by smooth convex functions
with derivative between zero and one. The second derivative of their
composition with p is

    psi'(p)p'' + psi''(p)(p')^2.

The second term is nonnegative, so the negative part of this second
derivative is at most the negative part of p''. Both second derivatives
have integral zero: their first derivatives tend to zero at both infinities.
Their total variations are therefore twice their respective negative masses,
which proves the bound without a factor two. Lower semicontinuity of
variation proves (6) for the limiting hinge.
For a=0, apply (5) directly to p. Smooth hinges may be chosen to vanish at
zero, so there is no spurious constant in an integral over the line.

For a slice of a three-dimensional mixture, in coordinate i, (4) gives

    integral |partial_i^2 p| dz_i
      <= integral product_(l!=i) phi(z_l-x_l) dmu(x).            (7)

All these bounds hold for diffuse mixing laws as well. Fubini and domination
follow from the Gaussian envelope of a bounded mixing support.

Let S_i mean lattice summation with factor h in coordinate i, and I_i mean
integration. For any translated one-dimensional Gaussian, (4)-(5) imply
`S_i phi <= G_h`. Telescope

    S_1 S_2 S_3 - I_1 I_2 I_3
       =(S_1-I_1)I_2I_3 + S_1(S_2-I_2)I_3
                              + S_1S_2(S_3-I_3).

Apply positivity of each S_i,I_i to the absolute bounds (5)-(7).
For **one endpoint hinge** the infinite-lattice error is at most

    (h^2/8)(1+G_h+G_h^2).                                    (8)

It has no atom-count, diameter or threshold factor. Two endpoints give the
first term in (1). No bound on the number or regularity of level-set components
was assumed. Simply applying a smooth-function quadrature theorem directly
to an unsmoothed hinge would not justify (8); (6) is the needed step.

## 3. Finite lattice tails cost one endpoint, not two

For a center coordinate `|x_i|<=R`, monotonicity on either Gaussian tail and
the integral comparison give

    h sum_(|j|>M) phi(jh-x_i)
       <= 2 integral_T^infinity phi(t) dt
       <= 2 phi(T)/T < exp(-T^2/2)/T.                        (9)

The last inequality uses `sqrt(2pi)>2`. A union bound over three coordinates,
and the full-lattice mass bound G_h in the other coordinates, bound the omitted
lattice mass of each three-dimensional probability mixture by

    tau=(3G_h^2/T) exp(-T^2/2).                               (10)

Each omitted hinge sum is nonnegative and at most its mixture's omitted mass.
Their **difference** is therefore in `[-tau,tau]`. It costs one copy of tau
in (2), rather than two. Adding (8) at the two endpoints proves Theorem 1.

## 4. A finite exact sweep treats all thresholds

Suppose all finite-lattice normalized density values have been enclosed by
integers divided by `Q=2^p`:

    f_lo(z)<=f(z)/C<=f_hi(z),
    g_lo(z)<=g(z)/C<=g_hi(z).

Pointwise monotonicity of the hinge gives lower and upper discrete profiles
by using respectively `(f_lo,g_hi)` and `(f_hi,g_lo)`. Each is piecewise
linear in u, with knots at its finitely many rational density values and at
zero. Beyond the largest knot it is exactly zero. Its global maximum is
therefore found **exactly** by sorting the knots and updating its slope.
There is no threshold interpolation error and no search over floating roots.

The density values are computed as follows. For each coordinate of each
center, enclose `exp(-(jh-x_i)^2/2)`. Positive tensor products and the
nonnegative rational weights then enclose the whole mixture. The executable
uses integer fixed-point endpoints, rounds outwards, and checks every width.
Each one-dimensional interval has width at most `2/Q`, and each final
three-dimensional normalized density interval has width at most `8/Q`.
These follow respectively from the validated exponential calculation and
the telescoping product inequality for three numbers in [0,1], followed by
one outward rounding at the mixture level. Upper values may be capped at one
because the exact normalized mixture never exceeds one.

For an exponent q>=0, the program halves q until `r<=1/8`. Consecutive even
and odd Taylor sums for exp(-r) give upper/lower bounds. It continues until
their difference is below its stated fixed-point tolerance, then squares
the interval back with outward integer divisions. Extra guard bits account
for every squaring. More explicitly, for L squarings the working denominator
is `S=2^(p+2L+16)`. Initial width after outward rounding is below `33/(16S)`.
Each squaring on [0,1] multiplies width by at most two and adds at most `2/S`,
so the width before final rounding is below `5*2^L/S<1/Q`. Final outward
rounding gives an integer width below three, hence at most two units.
The width check fails explicitly if its invariant fails;
no approximate real number is silently accepted. All loops terminate since
the Taylor remainders tend to zero. Large exponents can have a zero lower
endpoint, which is valid. For tails one may additionally use
`exp(-q)<=2^(-floor(q))`; the implementation takes the better certified bound.

Machin's identity `pi=16 atan(1/5)-4 atan(1/239)`, alternating arctangent
bounds, and integer square-root enclosures give rational endpoints for C.
The code checks `1/16<C_lo<=C_hi<1/8` and
`C_hi-C_lo<=1/(256Q)`. Machin's identity follows from the tangent addition
formula and the quadrant, as in the existing uniform-defect certificate.
The arctangent tolerances give a pi interval narrower than `2^(-p-15)`.
On pi>3 the derivative magnitude of `(2pi)^(-3/2)` is below 1/16;
the two final square-root roundings have mesh `2^(-p-10)`. These bounds
give the stated prefactor width, rather than assuming the check will pass.
Multiplying the nonnegative maximum of each rational profile by the
appropriate endpoint of C is safe. No floating arithmetic is used.

Let `V=h^3(2M+1)^3`. For h<=1/4, the resulting maxima obey

    p_+-p_- <= (2V+1)/Q.                                    (11)

The density-width sums cost at most `C_hi h^3 *16(2M+1)^3/Q <2V/Q`.
For the prefactor error, the lower profile maximum is at most the full source
lattice mass divided by C, hence its contribution is at most
`(C_hi-C_lo)G_h^3/C <1/Q`, since C>1/16 and G_h^3<2.
The executable also computes the sharper actual width from its interval
histograms and checks the finite-lattice masses against the known mass one.

## 5. Uniform consumer contract on the unchanged rational family

Use **exactly** the rational family from [paired cubature](CUBATURE_FRONTIER.md):
at most A_k labels, `L=256k^3`, `W=4kA_k`, matched anchor zero, integer radii
at most `3kL`, and squared integer pair losses at least `256k^2` for distinct
labels. Zero weights and target collisions remain allowed. Its all-hinge
maximal defect D_Rk satisfies, by the accepted cubature and rational rounding,

    0<=D-D_Rk < 11/(4k)+161/(256k) =865/(256k).                (12)

No beta approximation term is needed when evaluating the hinge itself.
This does not change the family or the earlier producer's historical fields.

For k>=1 take

    ell=ceil(log2 k),
    h=1/[4 ceil(sqrt(k))],
    T=2 ceil(sqrt(ell+2)),
    M=ceil((3k+T)/h), V=[(2M+1)h]^3,
    p=max(16,ceil(log2[100k(2V+1)])), Q=2^p.                 (13)

Then `G_h<=129/128`. The first term in (1) is below `1/(20k)` because

    [1+129/128+(129/128)^2]/64 <1/20.

Also `T>=4`, `T^2/2>=2ell+4`, and e>2, so the tail in (1) is below

    3(129/128)^2/(64k^2) <1/(20k^2).

Thus `E<1/(10k)`. Equations (3), (11) and (13) give, for every rational input,
a certified defect interval of width **less than `21/(100k)`**. The same
parameters work for an input's smaller actual support box. The program's
`frontier_budget(k)` produces (13); it does not enumerate that family.

If every rational configuration is covered, let L_k be the maximum of its
computed lower endpoints and let U_k be the maximum of its upper endpoints
plus `865/(256k)`. Then

    L_k<=D<=U_k,
    U_k-L_k < [865/256+21/100]/k =22969/(6400k).             (14)

Running maxima of L_k and running minima of U_k, optionally also capped by
the separately accepted 7/50, converge to D. In particular these upper
bounds can decrease to zero if the conjecture is true. **No complete cover
or value of U_k is computed in this packet.** Evaluating one input does not
give a universal bound. For a requested epsilon, k=ceil(8/epsilon) and
upper endpoints <=epsilon/2 on EVERY input would give
`D<1889 epsilon/2048<epsilon` by (12).

The number of spatial sites per endpoint in (13) is `O(k^(9/2))`, while
`p=O(log k)`. For m atoms, construction uses `O(m k^(9/2))` fixed-point
products/additions, plus `O(k^(9/2) log k)` sorting comparisons. Rational
exponential setup and bit costs are polynomial in the input bit length and
log k; they are not unit-cost real-oracle calls. With
`A_k=O(k^3(1+log k)^(3/2))`, the leading arithmetic count per configuration
is `O(k^(15/2)(1+log k)^(3/2))`. This replaces the literal
`A_k^(2048k^5-1)` replica expansion and its exponentially amplified
moment-error requirement **for evaluating a defect**. It does not replace
symbolic moment proofs when an exact sign is available.

These remain large worst-case grids: the k=64 budget already has about
2.04 trillion sites per endpoint. No practical exhaustive frontier search,
exact-zero decision algorithm, or optimal complexity is claimed. The
finite configuration count is unchanged and is still the dominant unresolved
global coverage problem. Small individual inputs and modest defect accuracy
are practical, as the replay below demonstrates.

For adaptive parameter covers there is a further direct handoff. If a center
instance has a certified upper defect U, another labeled instance with
`||w-w0||_1<=omega`, endpoint displacements at most r_x,r_y, and probability
weights satisfies

    Delta <= U+omega+(r_x+r_y)/sqrt(2pi).                    (15)

Each mixture changes in TV by at most half the weight L1 distance plus the
weighted Gaussian-translation bound; equal-mass hinges are 1-Lipschitz in TV.
Take the supremum over thresholds. Formula (15) is valid even if a convenient
cell center is not itself a contraction, since the oracle handles any two
laws. Feasibility of the configurations being covered remains a separate
check. This supplies an error budget for R2/R8 to use with geometric or
weight cells, not a claim that such a cover has been supplied.

## 6. Reproduction, meaningful controls, and scope

From this directory, with standard-library CPython 3.11+:

```sh
python3 -B direct_hinge.py --check
python3 -B -O direct_hinge.py --check
python3 -B direct_hinge.py --budget 64
```

For a user-supplied rational probability instance at variance one:

```sh
python3 -B direct_hinge.py --input instance.json --step 1/8 --tail 4 --bits 40
```

The schema is `source`, `target` (lists of triples), and `weights`, using
integers or rational strings. All pairwise contraction inequalities are
checked exactly by default. `--allow-noncontraction` is explicitly diagnostic.
Steps, supports, variance normalization, and precision must match the theorem.

[DIRECT_FIXTURES.json](DIRECT_FIXTURES.json) includes a genuine member of
R^c_1: the origin and the six points `+-e_i/2`, mapped to zero and `e_i/4`.
Their weights have numerator 24 at the origin and 22 at each other site,
with denominator W=156; L=256 and A_1=39. The code checks rank six, all
integer pair margins, radii, masses and anchors. This map already has a
classical coordinatewise contracting motion; it is a **control**, not a new
positive subclass. At h=1/2,1/4,1/8 with T=4, its certified maximum-defect
upper endpoints are below respectively

    0.194, 0.048, 0.012.

The final run covers 389,017 lattice sites per endpoint and every threshold.
Its numerical remainder decreases rather than being interpreted as a sign.
A deliberately invalid map from one source point to two targets separated
by four has a certified defect above 0.16 at h=1/4, testing the adverse-sign
and lower-bound branches. It is rejected without the diagnostic override.

The exact controls also compare 4,096 complete profile sweeps with direct
evaluation at every knot; test the Peano identity on polynomials and hinged
linear functions; compare fixed-point exponentials with independently formed
degree-100/101 Taylor enclosures; verify separate translations, split atoms,
and zero weights; compare three actual Gaussian hinges against a separately
integrated radial formula; reject malformed inputs; and pin the dependencies.
For that last numerical control, at u=exp(-t),
`H_phi(Cu)=(4t^(3/2)/sqrt(pi)) [sum_(j>=0) (-t)^j/(j!(2j+3))-exp(-t)/3]`.
Direct even/odd integrated Taylor bounds enclose this expression at
t=1/4,1,4, separately from the lattice implementation.
All checks remain active under Python -O. [DIRECT_EXPECTED.json](DIRECT_EXPECTED.json)
contains the compact exact bounds, stream hashes and budgets. Lattice values
are regenerated, not published as a large array.

The analytic variation/tail proof and the exact integer implementation are
the trust boundary. The controls are not independent mathematical review or
formal proof. The paired-cubature premise has separate
[independent acceptance](../gaussian_paired_cubature_review2/REVIEW.md), which
does not review this new oracle. The earlier square-root beta-degree
supplement is not a dependency of this proof. The primary open problem
remains [Aishwarya--Li, Conjecture 1.1 in R3](https://arxiv.org/html/2609.07041v2).
No unrestricted sign, counterexample, or new Kneser--Poulsen consequence is
claimed here.
