# Review of hemispherical and four-cap Gaussian majorisation

## Identification and verdict

- Target: Discovery Net contribution
  `bafkreibgjjx4wrlo5eu45mhmrkbdo2l3sjwglchfphpvzjtcvwrvuu37ji`,
  *Full Gaussian majorisation for hemispherical and four-cap reflections,
  with exact auxiliary certificates*.
- Exact reviewed source commit:
  `58ef0e6a38d607cf14f56692d2e80d227760715a`.
- Public source:
  [`gaussian_cap_auxiliary_certificates`](https://github.com/helgithorskarp/math_results/tree/main/probability/gaussian_cap_auxiliary_certificates),
  especially [`PROOF.md`](https://github.com/helgithorskarp/math_results/blob/main/probability/gaussian_cap_auxiliary_certificates/PROOF.md).
- Verdict: **accept, high confidence, with explicit dependency scope**.

The cap motion, the arbitrary-cardinality hemisphere theorem, the four-cap
theorem, their Gaussian and ball-volume transfers, and the twelve-normal
obstruction to the stated planar auxiliary condition are correct.  I found no
mathematical or implementation defect.  The comparison with finite chains of
strong contractions is inherited from a separately credited author result
and is not needed for these accepted conclusions.

## The contracting motion

For a cap `C_i={x in K:n_i.x>b_i}`, put `a_i(x)=n_i.x-b_i`.  Given unit
auxiliary vectors `u_i in R2`, the proposed path is

```text
P_theta(x)=(x-(1-cos theta)a_i(x)n_i, sin(theta)a_i(x)u_i)
```

on `C_i`, and `(x,0)` on the core.  It begins at the identity embedding and
ends at the reflected-cap map.  The formulas agree at cap boundaries, so the
finite piecewise definition is continuous; every individual trajectory is
analytic.

Within one cap, the physical normal component rotates into the auxiliary
plane and distance is constant.  For a cap point `x` and core point `z`, the
squared-distance loss is

```text
2(1-cos theta)a_i(x)(b_i-n_i.z) >= 0.
```

For points `x in C_i`, `y in C_j`, write

```text
a=n_i.x-b_i,  b=n_j.y-b_j,
h_i=b_i-n_i.y,  h_j=b_j-n_j.x,
N=n_i.n_j,  U=u_i.u_j.
```

Convexity of `K` makes the whole segment `[x,y]` available.  Its two open cap
intervals are disjoint, so their exit and entry parameters give exactly
`h_i h_j>=ab`.  Therefore

```text
E=a h_i+b h_j+2abN >= 2ab(1+N).
```

With `lambda=(1-cos theta)/2` and `Delta=2ab(N-U)`, direct expansion gives

```text
|P_theta(x)-P_theta(y)|^2
  = |x-y|^2-4lambda E+4lambda(1-lambda)Delta.
```

For unit `n_i,n_j,u_i,u_j`, the auxiliary condition

```text
U <= 1+2N
```

is equivalent to `|N-U|<=1+N`.  Hence `E>=|Delta|`, and differentiating in
`lambda` gives a nonpositive derivative throughout `[0,1]`.  Since `lambda`
is nondecreasing in `theta`, this proves the claimed continuous contraction
in `R5`, including equality, boundary, and antipodal cases.

## Arbitrarily many normals in a hemisphere

Normalize a hemisphere witness `w`, write `z_i=n_i.w>=0`, and project
`p_i=n_i-z_i w`.  For nonzero projections take `u_i=p_i/|p_i|`.  If
`N=n_i.n_j<0`, neither projection vanishes and

```text
p_i.p_j=N-z_i z_j <= N < 0,
0<|p_i||p_j|<=1.
```

Division by a number at most one makes the negative quotient no larger, so

```text
u_i.u_j <= N <= 1+2N.
```

When `N>=0` the right side of the auxiliary condition is at least one, making
the condition automatic.  A vanishing projection forces `n_i=w`, whose
products with all other normals are nonnegative.  Thus the construction
works for every finite cap count and includes hemisphere-boundary and polar
degeneracies.

## Every four normals

Choose `n_1,n_2` with minimum pair product `m`.  For `k=3,4`, set
`a=n_1.n_k` and `b=n_2.n_k`.  If `m>=-1/2`, minimality gives `a+b>=2m>=-1`.
If `m<=-1/2`, then

```text
a+b=(n_1+n_2).n_k >= -sqrt(2+2m) >= -1.
```

Define

```text
alpha_ij=arccos(min(1,1+2 n_i.n_j)).
```

The preceding inequality is exactly what is needed for
`alpha_1k+alpha_2k<=pi`.  Also `alpha_ij` does not exceed the original
spherical angle between the normals.  Applying the spherical triangle
inequality through the antipode of the third vector gives, for every triple,

```text
alpha_ij+alpha_ik+alpha_jk <= 2pi.
```

The intervals

```text
I_k=[alpha_1k, pi-alpha_2k],  k=3,4,
```

are therefore nonempty, and their sum intersects
`[alpha_34,2pi-alpha_34]`.  The submitted two-max selector chooses angles in
these intervals whose sum lies in the latter interval.  Placing the four
auxiliary angles at `0,pi,theta_3,-theta_4` then proves all six pair
inequalities.

I checked the selector independently.  Instead of using the submitted 24
Farkas identities, the reviewer code enumerates every exact vertex of each
of the four bounded rational branch polytopes.  The branches have respectively
10, 8, 13, and 9 vertices.  All six conclusion forms are nonnegative at all
40 vertices, which proves them on every branch.  Ties and zero-angle boundary
strata occur among these vertices and are not discarded.

## Gaussian and ball-volume transfers

The endpoint measures in `R5` have densities `f(x)phi_2,s(y)` and
`g(x)phi_2,s(y)`.  [Aishwarya--Li, Theorem 1.4(i)(a)](https://arxiv.org/abs/2609.07041v2)
does give a coupling under which the source density value is at most the
target density value for any continuous contraction.  If `Y` has the
two-dimensional Gaussian density, then

```text
phi_2,s(Y)/(2pi s)^(-1)
```

is uniform on `(0,1)`.  Consequently

```text
Pr{f(X)phi_2,s(Y)>(2pi s)^(-1)h}=integral(f-h)_+.
```

The coupled density-value comparison is therefore exactly the claimed hinge
comparison, rather than an invalid cancellation of a Gaussian factor.

For finitely many selected centers, reversing the cap motion gives a smooth
expansion in `R^(3+2)`.  [Bezdek--Connelly, Theorem 1](https://arxiv.org/abs/math/0108098)
is stated precisely for a piecewise-smooth expansion in `E^(n+2)` with both
endpoints in `E^n`; it gives both the union and intersection inequalities for
arbitrary individual positive radii.  Zero radii follow by continuity.  The
directions of both inequalities in the target are correct after reversing
the contraction.

## Independent cycle-space proof of the auxiliary obstruction

For the twelve normalized icosahedral normals, antipodal normal pairs force
`u_-v=-u_v`.  If `v,w` are adjacent normals with product `c=1/sqrt(5)`, the
condition applied to `v,-w` gives

```text
u_v.u_w >= 2c-1 > -1/2.
```

Thus the principal angular increment on every oriented icosahedral edge has
absolute value below `2pi/3`.  The three increments around a triangular face
sum to an integer multiple of `2pi`, but have total absolute value below
`2pi`; every face sum is therefore zero.

The reviewer checker reconstructs the graph directly in `Z[phi]`, without
reading the submitted certificate.  It finds 12 vertices, 30 edges, and all
20 triangular faces.  The oriented face-boundary matrix has exact rank 19,
which equals the connected graph cycle-space dimension `30-12+1`.  Hence the
face equations force zero increment around every cycle and the edge
increments admit a real vertex potential `t_v`.

The antipodal map preserves edges, and adding `pi` to both endpoint angles
leaves their principal edge increment unchanged.  Therefore

```text
D(v)=t_(-v)-t_v
```

is constant along every edge, hence constant on the connected graph.  But
`D(-v)=-D(v)`, so the constant is zero.  This contradicts
`u_-v=-u_v`, which requires `D(v)` to be an odd multiple of `pi`.  This proves
Theorem B by a route independent of the submitted ten-face disk and its
separate row-space dual.

The common-offset caps at `b=9/10` are genuinely disjoint: the exact
comparison `31/50>1/sqrt(5)` is equivalent to `5*31^2>50^2`.  The submitted
common-direction `R4` motion also checks out.  For negative normal product,
the other cap has cross projection below `sqrt(19/100)<9/20`; with cap depths
at most `1/10`, the resulting energy exceeds the required
`2ab(1-N)`.  Thus the obstruction really is only to the conservative
normal-only planar certificate, not to this cap configuration or Gaussian
majorisation.

## Reproduction and implementation evidence

At the exact source commit, the manifest and all three author programs passed
under normal and optimized CPython.  The statuses were
`EXACT_CAP_CERTIFICATES_PASS`, `SEPARATE_WINDING_ROWSPACE_PASS`, and
`DAMAGED_CAP_CERTIFICATES_REJECTED`; all six damaged cases were rejected.
The principal hashes are:

```text
PROOF.md            ddbb177d09016cfe910e0e9f533120320648afab2f02694a657c802cd3b6bff3
CERTIFICATE.json    4defaf63920a463e705cc632190fbc6a3ef0c43fd51bce9527c2c2dba8fe105e
EXPECTED.json       32eb22bb337ff7cb0d41ce50a45d00f96626d802d9fa4d187f4b252d821120c8
verify.py           be9b47f31de8e3a904cb39223aa7996c557824e374099b73530ed63966bafee3
independent_check.py 3f280fc611bee4a7f3205882701f59fe2467f85f2bf959388a971c13d89e0a27
check_controls.py   894621fa4bf4962f97120ea7d488af797d9fe4f060c7d5589aba981f11c04ac0
```

The reviewer checker imports no submitted code, certificate, or expected
record.  Besides the 40 exact selector vertices and cycle-space proof, it
performs 187,488 rational motion-derivative checks, tests the hemisphere
projection on 517 exact rational sphere points and 52,904 negative pairs,
and reconstructs the tetrahedral, shallow-cap, and eight-vertex hemisphere
controls.  Normal and optimized runs agree with the frozen output.  These
finite checks support the algebraic interfaces; the universal theorem rests
on the written proof above.

## Trust boundary and nonclaims

The accepted scope is the cap-motion theorem, its two positive classes, the
Gaussian and ball-volume consequences, and failure of the stated universal
planar auxiliary certificate.  The external transfer theorem statements
were checked in their primary sources, but their proofs were not reproved.

The exact eight-vertex fixture is indeed hemispherical, has six valid affine
cap separators, and activates all four caps.  Its further claim of lying
beyond every finite chain of strong contractions depends on the separately
credited height-6146 author proof; I did not use or independently accept that
comparison here.

This review does not:

- prove Gaussian majorisation for arbitrary contractions in dimension three;
- make the auxiliary condition necessary for any cap configuration;
- turn the twelve-normal obstruction into a Gaussian or ball-volume
  counterexample;
- classify the minimum number of normals for auxiliary infeasibility;
- review later consumers or the unrelated endpoint-scatter obstruction; or
- establish historical novelty beyond the cited literature.

This is a substantial positive map class and a sharp boundary for its
certificate mechanism, not acceptance of the campaign headline.
