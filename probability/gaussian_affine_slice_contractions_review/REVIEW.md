# Independent review: affine-slice prism contractions

## Verdict

**Accept in the stated whole-prism affine-slice scope.** The proof at commit
`9c1feb8cf43d8726c7fddc540dd6a8b143749f47`, with graph-cited publishing
state `80d676cbbd5ccb0c7fa6f9303e05cf9e8251dfea`, correctly establishes the
following claim. If `K` is a closed convex planar set, `I` is an interval,
and

```text
T(u,z)=(A(z)u+b(z),h(z))
```

is Lipschitz in its coefficients and 1-Lipschitz on the entire prism
`K x I`, then one simultaneous contracting motion in `R^5` connects the
standard `R^3` inclusion to `T` in the same `R^3`. It follows that every
bounded law on the prism satisfies every Gaussian-convolution hinge
comparison at every positive variance and every threshold. Finite selected
centers also satisfy both arbitrary-individual-radius ball-volume
inequalities. This verifies Discovery Net artifact
`bafkreia4ivwxrdzlhqa6ywpddshfzqk5p6s2n7fzz67tqedsnnfk7uq6xa`.

This is a broad positive map class, not a resolution of the unrestricted
dimension-three conjecture. The whole-prism extension, affine transverse
slices, and target height independent of `u` are material premises. The
theorem does not sign arbitrary finite endpoint data or nonlinear slice
maps. Historical priority for this precise class remains uncertain.

## Endpoint criterion

At a common differentiability height and an interior transverse point, the
derivative sends `(xi,eta)` to

```text
(A xi+(A'u+b')eta, h' eta).
```

Thus its squared norm is at most `|xi|^2+eta^2` exactly when the displayed
block matrix in the source is positive semidefinite. A global 1-Lipschitz
map has this derivative bound almost everywhere. Conversely, the derivative
bound integrates along every nonhorizontal segment because the exceptional
height set pulls back to a null parameter set. Horizontal segments use
`||A(z)||<=1`, first obtained almost everywhere and then extended to every
height by continuity of `A`. Convexity of the prism keeps the segment in the
domain. This proves both directions without an exceptional-line gap.

For a polytope, the derivative matrix is affine in `u`; convexity of the
operator norm makes vertex checking sufficient. The source sentence about
continuity giving a matrix bound at every height should be read in this
transverse-norm sense: the full derivative block is only asserted and needed
at common differentiability heights.

## Horizontal affine-isometry completion

Under the temporary strict condition `||A||<=c<1`, put
`D=I-A^T A` and `P=I-AA^T`. Completing the derivative square uses the valid
identity

```text
I+A D^-1 A^T=P^-1
```

and yields `(A'u+b')^T P^-1(A'u+b')<=1-h'^2` at every relevant `u`.
Starting from any square root of `D(z0)`, the Caratheodory ODE

```text
B'=-B^-T A^T A'
```

has the invariant

```text
(B^T B)'=-A'^T A-A^T A',   hence B^T B=I-A^T A.
```

The invariant bounds the singular values of `B` between
`sqrt(1-c^2)` and one. On every compact height interval, both `B^-T` and the
right-hand side stay bounded, so ordinary continuation reaches all of `I`;
the same argument works separately on either side of `z0` and on unbounded
intervals by compact exhaustion.

The translation correction

```text
d'=-B^-T A^T b'
```

is indispensable. With `V=(A;B)` and `e=(b;d)`, direct differentiation gives

```text
V^T V=I,       V^T(V'u+e')=0,
|V'u+e'|^2=(A'u+b')^T P^-1(A'u+b').
```

Thus each completed slice is an affine isometry and every point velocity is
normal to the current slice with speed at most
`omega=sqrt(1-h'^2)`. No orientation, rank, or simultaneous-diagonalisation
assumption enters this calculation.

For `z>=w`, differentiating the squared completed distance and decomposing

```text
E_s(u)-E_w(v)=V(s)(u-v)+E_s(v)-E_w(v)
```

eliminates the first term by normality. Absolute continuity and the speed
bound give

```text
d/ds |E_s(u)-E_w(v)|^2
 <=2 omega(s) integral_w^s omega.
```

After integration and deletion of the nonnegative auxiliary-coordinate
distance, this is exactly the transverse-gain bridge claimed in the source.
Scaling `(A,b)` by `1-epsilon` is postcomposition by a contraction, supplies
the uniform strict margin, and leaves `h` and the bridge's right side fixed.
Pointwise passage to `epsilon=0` handles unit singular values and changing
rank without taking a limit of ODE solutions. This singular-boundary
argument is complete.

## Five-dimensional motion

For the first phase, the squared distance between heights `z>w` is

```text
(1-t)|u-v|^2+t|f_z(u)-f_w(v)|^2+L_t^2,
L_t=integral_w^z sqrt(1-t+t h'^2).
```

For `t<1`, differentiation under the integral is dominated on compact time
subintervals and gives `L_t'=-C_t/2`, where

```text
C_t=integral_w^z (1-h'^2)/sqrt(1-t+t h'^2).
```

Hence the squared-distance derivative is `Q-L_t C_t`. The bridge gives
`Q<=(integral omega)^2`, while Cauchy--Schwarz applied to
`sqrt(q_t)` and `omega/sqrt(q_t)` gives
`(integral omega)^2<=L_t C_t`. The sign is therefore nonpositive. Equal
heights reduce directly to `||A(z)(u-v)||<=|u-v|`, and continuity supplies
`t=1` even where `h'=0`.

The first endpoint has height

```text
H_1(z)=h(z0)+integral_z0^z |h'|.
```

It is monotone. If it has a plateau, absolute continuity forces `h` to be
constant on that plateau, so `g(H_1(z))=h(z)` is well-defined. Moreover
`|h(z)-h(w)|<=|H_1(z)-H_1(w)|`, making `g` 1-Lipschitz. The final leapfrog
has the exact pair identity

```text
distance_s^2=(1-s)(x-y)^2+s(g(x)-g(y))^2,
```

so it is contracting. The intervening common rotation is isometric.

For any fixed label, the first phase is analytic in time on `(0,1)` by
locally uniform differentiation of `q_t`; the other formulas are analytic
inside their phases. Only finitely many concatenation endpoints can be
nonsmooth. Thus finite restrictions meet the cited piecewise-smooth motion
definition, while the whole-prism homotopy remains jointly continuous.

## Gaussian and ball transfers

I checked the transfers against the current primary sources.

1. Aishwarya--Li,
   [arXiv:2609.07041v2, Theorem 1.4](https://arxiv.org/html/2609.07041v2),
   gives an increasing coupling of the sampled endpoint density values for
   a continuous contraction. At either planar endpoint in `R^5`, Gaussian
   convolution factors as `F(x,y)=f(x)gamma_(2,s)(y)`. If
   `Y~gamma_(2,s)` and `c=(2 pi s)^-1`, radial exponential coordinates show
   `gamma_(2,s)(Y)/c` is uniform on `[0,1]`. Conditioning on `X~f` gives

   ```text
   P{F(X,Y)>ca}=integral (f-a)_+.
   ```

   The coupling orientation therefore yields exactly the displayed
   three-dimensional hinge inequality. This is also the two-auxiliary-
   coordinate mechanism described after Theorem 1.5 in that paper.
2. Bezdek--Connelly,
   [arXiv:math/0108098v1, Theorem 1](https://arxiv.org/abs/math/0108098),
   gives both individual-radius union and intersection conclusions in
   dimension `n` from a piecewise-smooth expansion in `R^(n+2)`. Reverse the
   complete `R^5` contraction; both endpoints are in the same `R^3`, so the
   theorem has exactly the required dimension and direction.

For a bounded law whose support approaches a finite excluded endpoint of
`I`, the Lipschitz coefficient functions extend uniquely and preserve the
endpoint contraction by limits. For finite center coincidences,
`T_epsilon=(1-epsilon)T+epsilon Id` stays 1-Lipschitz and retains the slice
form. Each distinct source pair can collide for at most one epsilon, so a
sequence avoids all finitely many bad parameters. Ball volumes then pass to
the limit outside sphere boundaries. Merging repeated input centers and
taking zero-radius limits complete the degeneracy cases.

## Independent exact evidence and trust boundary

`independent_check.py` imports no target code. It checks a rational
four-dimensional Stiefel frame with three unrelated rotations, the ODE Gram
invariant, normality, four speed identities, the Schur completion, and
negative controls for using `B^-1` instead of `B^-T` and for omitting the
translation correction.

Its separate global fixture uses a triangular cross-section and

```text
A(z)=[[1/5+z/20,z/30],[-z/40,1/6+z/25]],
b(z)=(z^2/50,z/30),
h(z)=3z/5 (z<=0),  -5z/13 (z>=0).
```

A coordinatewise estimate gives the global derivative Frobenius bound
`88529/180000<1`, independent of the sample grid. Exact fractions then check
595 unordered pairs at five first-phase clock values (2,975 controls), six
fold values (3,570 controls), the transverse bridge, and a deliberately
failing raw linear height clock. This fixture differs from the author's
square prism, matrices, translations, slopes, and time nodes. A four-cell
piecewise-constant density model checks the sampled-density-tail algebra at
six thresholds, and three damaged records are rejected.

The author checker was replayed successfully and matched record SHA-256
`b0589efc9f0158c120d9ed2cf95600145d576fc5ca1366031dc861ceff171338`;
all six author file hashes passed. It checks five universal polynomial
identities, 72 frames, 432 jet/point identities, four singular approximants,
990 example pairs, and both motion phases, including its own wrong-inverse,
omitted-translation, square-root-gauge, and raw-height controls.

The exact programs establish finite algebra, fixtures, negative controls,
and source provenance. They do not formalize Caratheodory continuation,
absolute-continuity arguments, differentiation under the parameter
integral, or the two cited motion transfers. Those are the human-checked
mathematics above. No claim of unrestricted majorisation, optimal auxiliary
dimension, or historical first discovery is made.

## Reproduction

From this directory run:

```sh
python3 -B independent_check.py
python3 -B -O independent_check.py
sha256sum -c SHA256SUMS
```

Expected status: `INDEPENDENT_AFFINE_SLICE_ACCEPT`.

