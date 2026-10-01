# A nonlocal J74 receiving arc with four isolated closed-fit motions

**six-rupert-2, researcher; 2026-10-01.** Author-checked exact finite
certificate and written continuum proof. Unformalized and independently
unreviewed. The full Rupert property of J74 remains **OPEN**.

Let `K=conv(V)` be the original unit-edge J74 metabigyrate
rhombicosidodecahedron in [model.py](../model.py). Its constructive named-solid
identification is the input from the [original geometry](../PROOF.md),
source `25fc9695745b6832d068d18544452b7852b5847f`, graph
`bafkreig4wvsmlau4koaib63i3cefofih67cczseu3hgdv2r6r54ga572aq`.
Only that model and its exact arithmetic are pinned inputs here.

Write `s=sqrt(5)>0`, `phi=(1+s)/2`, and put

\[
 m=\frac{(1,-\phi,-\phi^2)}{2\phi},\qquad
 d=\left(\frac{-5+3s}{8},\frac{11-3s}{8},-\frac14\right),
 \quad u(t)=m+td,\quad \frac35\le t\le\frac7{10}.
\]

Here `m` is unit and `m dot d=0`. Define the actual orthogonal projection
and reflection for this nonunit normal by

\[
 P_u=I-\frac{uu^T}{u\cdot u},\qquad M_u=I-\frac{2uu^T}{u\cdot u}.
\]

Let `G=diag(-1,-1,1)`, `H_x=diag(-1,1,1)` and
`H_y=diag(1,-1,1)`. The checker verifies that all three preserve the
**entire original 60-vertex body**. The four proper reference motions are

\[
 \mathcal S(u)=\{I,G,M_uH_x,M_uH_y\}.
 \tag{1}
\]

They all have exactly the receiver shadow for every `u`, since the first
two preserve `K` and `P_uM_u=P_u`. An improper symmetry of a projected
prototype is not used in this assertion.

**Theorem.** Suppose `t` is in the closed interval above, `S in S(u(t))`,
`Q in SO(3)`, `lambda>=1`, and `b in u(t)-perp` is an arbitrary physical
translation. Write

\[
 QS^T=(I+[c]_\times)(I-[c]_\times)^{-1},\qquad
 \|c\|\le\frac1{6000},\quad [c]_\times v=c\times v.
 \tag{2}
\]

If the original closed fit

\[
 \lambda P_u(QK)+b\subseteq P_uK
 \tag{3}
\]

holds, then `Q=S`, `lambda=1`, and `b=0`. Conversely these reference
poses give closed fits. Thus every strict passage is excluded from these
four **conditional motion neighborhoods** on the specified receiving arc.
The Cayley radius is `tan(relative rotation angle/2)`; it is not a
receiving-normal radius or a bound on all sources.

The entire arc is at projective unit-normal chord **strictly greater than
1/3 from each of the six global minimum axes**. Its receiving domain is
one-dimensional. No surrounding receiving tube, complete all-source
classification, global non-Rupert theorem, or whole-body assertion of
non-local-Rupertness follows.

## 1. Complete physical shadows and affine positive stresses

The literal [certificate](certificate.json) gives the full 18-corner
receiver cycle

```
17,32,44,8,28,10,46,54,26,23,35,51,15,31,13,49,57,21
```

For an oriented cycle edge `v_a->v_b`, put

\[
 a_e(t)=(v_b-v_a)\times u(t),\qquad h_e(t)=a_e(t)\cdot v_a.
 \tag{4}
\]

These are affine in `t`. At both closed endpoints the checker requires
`h_e>0` and evaluates `a_e dot (v_a-v)` at all 60 originals. All signs
are nonnegative, and those of every nonincident listed corner are strictly
positive. Each physical edge has length one. These inequalities interpolate
over the interval, so they give the complete convex cyclic shadow for
every real `t` in the interval. This uses actual projected support normals;
the spatial edges themselves need not be perpendicular to `u`.

Use both original endpoints `p=v_a,v_b` of each edge as contacts, for
36 rows. Set `z=20t-13 in[-1,1]`. The certificate supplies exact
`alpha_i,gamma_i in Q(sqrt5)` with

\[
 \beta_i(z)=\alpha_i+z\gamma_i>\frac1{50},\qquad
 \sum_i\beta_i(z)=1.
 \tag{5}
\]

Positivity and normalization are checked at both endpoints. Define the
five-column row

\[
 A_i(t)=\big(p_i\times a_i(t),\ (a_i(t))_x,(a_i(t))_y\big).
 \tag{6}
\]

Every coefficient of the quadratic polynomial
`sum_i beta_i(z) A_i(t)` is exactly zero. This is 15 field identities.
Consequently the contacts balance their torque and both x/y force
components continuously. Because all `a_i perpendicular u` and `u_z<0`
throughout the interval, they also balance the z force. This gives an
actual spatial force balance, hence cancellation of physical translations.

The minor using rows `28,2,20,6,15` is invertible throughout the interval.
With polynomial variable `x=10t-6 in[0,1]`, all six Bernstein coefficients
of its oriented determinant have the same strict sign. The absolute
determinant has lower bound

\[
 D=\frac{843}{3200}+\frac{26339}{400000}\sqrt5>0.
 \tag{7}
\]

The checker expands all 25 four-by-four cofactors as polynomials and uses
their Bernstein coefficient bounds on `[0,1]`. After dividing the
transpose-cofactor row sums by `D`, each is at most six. Thus for the
selected matrix `B(t)` we have the uniform induced norm bound

\[
 \|B(t)^{-1}\|_\infty\le6.
 \tag{8}
\]

All bounds are exact ordered-field comparisons. No floating LP status
or sampled determinant sign is used in (5)--(8).

## 2. A quantitative positive-spanning bound

For any vector `Z in R5`, write `r_i=A_i Z` and `L=max_i r_i`.
The positive normalized balance (5) implies `L>=0`. For a row attaining
the minimum, `sum beta_i r_i=0` and the other rows are at most `L`, so

\[
 \min_i r_i\ge-50L,
 \qquad |r_i|\le50L.
\]

Apply (8) to the five selected rows and use `sqrt5<3`:

\[
 \|Z\|_2\le3\|Z\|_\infty\le3\cdot6\cdot50L=900L.
 \tag{9}
\]

This is a uniform positive-spanning statement for rotation and translation
together. The five-dimensional norm below retains the actual translation.

Indeed, write any `b in u-perp` as

\[
 b=(\tau_x,\tau_y,-w\cdot\tau),\qquad
 w=(u_x/u_z,u_y/u_z),\quad T=I_2+ww^T.
\]

For any contact normal, `a dot b=a_xy dot T tau`. Also
`||b||^2=tau^T T tau<=||T tau||^2`, since `T^2-T` is positive
semidefinite. Therefore the variables `T tau` used in (6) control the
physical translation and vanish only when `b=0`.

## 3. Exact Cayley control with arbitrary scale and translation

Fix a reference `S`. For the fixed references `I,G`, each contact `p_i`
has an original preimage under `S`. For the reflected references
`S=M_uH_x,M_uH_y`, the corresponding source contact is `p_i'=M_u p_i`.
In either case its support value is `h_i`, and its norm is the original
circumradius `R`, with `R^2=(11+4sqrt5)/4` and `R<9/4`.

Let `C=QS^T` be the Cayley motion in (2). The exact identity is

\[
 C p=p+\frac{2}{1+\|c\|^2}
       \big(c\times p+c\times(c\times p)\big).
\]

Set `v=2lambda*c/(1+||c||²)`. The original constraint for every selected
source contact in (3) is

\[
 (\lambda-1)h_i+a_i\cdot(v\times p_i'+b)+E_i\le0,
 \qquad E_i=a_i\cdot\big(c\times(v\times p_i')\big).
 \tag{10}
\]

For a fixed reference use `p_i'=p_i`. For a reflected reference,
`a_i perpendicular u` implies `M_u a_i=a_i`, and the cross-product
identity under an orthogonal reflection gives

\[
 (M_u p_i)\times a_i=-M_u(p_i\times a_i).
\]

Thus in both cases the linear term in (10) is the row (6) applied to
`Z=(v_*,T tau)`, where `v_*=v` or `v_*=-M_u v`. In particular,
`||v_*||=||v||<=||Z||`.

The checker verifies `||u||<9/8` at both interval endpoints. Squared
norm is convex in `t`, so this holds on the entire interval. Since every
physical edge in (4) is unit, `||a_i||<9/8`. Therefore, writing
`kappa=1/6000`,

\[
 |E_i|\le\|a_i\|R\|c\|\|v\|
       \le\frac{81}{32}\kappa\|Z\|.
\]

The scale term in (10) is nonnegative, with no assumed upper bound on
`lambda`. Hence

\[
 L=\max_i A_iZ\le\frac{81}{32}\kappa\|Z\|.
\]

Combining this with (9) gives

\[
 \|Z\|\le\frac{900\cdot81}{32\cdot6000}\|Z\|
       =\frac{243}{640}\|Z\|.
\]

Since `243/640<1`, `Z=0`. As `lambda>=1`, `v=0` implies `c=0`, and
the translation argument gives `b=0`. Equation (10) then gives
`(lambda-1)h_i<=0`, so `lambda=1`. This proves the theorem, including
the closed radius boundary and all actual translations.

## 4. Receiving separation and research scope

For each of the six unit minimum normals `m_j` in the original geometry,
the checker expands

\[
 (17/18)^2\|u(t)\|^2-(u(t)\cdot m_j)^2.
\]

All its degree-two Bernstein coefficients on the receiving interval are
strictly positive. Thus `|u dot m_j|/||u||<17/18`, and the projective
unit-normal chord is greater than `sqrt(2-2*17/18)=1/3`. This establishes
the stated nonlocal receiving region.

The preceding [all-six minimum receiving caps](../quantitative_minimum_caps/PROOF.md)
exclude all sources on a different receiving domain. Their constants,
paired prototypes, and coupled mirror proof are not inputs to this result.
The present certificate covers a nonlocal arc with conditional source
motions, which can be excised from a construction search. Other motions
on this arc and every receiver off it require further analysis.

Local rotation analysis is established Rupert theory; see
[Scott (2022)](https://arxiv.org/abs/2208.12912). The present claim is this
explicit original-J74 certificate and its translated motion neighborhoods;
no generic positive-spanning, Cayley, LP, or Bernstein method is claimed new.
[Gosain--Grimmer, Table4](https://arxiv.org/html/2509.08190) still lists
J72,J73,J74,J75,J77 without passages. The two mandated seeds concern the
[stellated tetrahedron](https://arxiv.org/html/2604.26531) and the
[Noperthedron](https://arxiv.org/abs/2508.18475). Their conclusions do not
resolve J74. Negative numerical searches also give no nonexistence theorem.
