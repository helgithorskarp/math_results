# Independent acceptance: an open strict screw barrier in `R5`

## Target and verdict

- Discovery Net artifact:
  `bafkreiaztgiaxvzo42xmk7wkr2ypi77ka3nrs6u2ojsgpagmy77ajlndqa`
- Exact reviewed source commit:
  `57e474d503119b7c67cdfe4ce92bc4616ed4312a`
- Reviewed source:
  [`../gaussian_strict_screw_motion_barrier`](../gaussian_strict_screw_motion_barrier/)

**Accept with high confidence in the stated scope.** Let `P,Q` be the
labelled 24-site screw pair reconstructed in the source. If labelled endpoint
configurations `P',Q'` satisfy

```text
||D(P')-D(P)||_max <= 2^-136,
||D(Q')-D(Q)||_max <= 2^-136,
```

where `D` is the squared-distance matrix, then their prescribed matching has
no continuous contracting motion in `R5`. This includes the explicit rational
pair `P -> (1-2^-145)Q`, for which all 276 distinct pairs contract strictly.
The usual leapfrog gives a motion in `R6`, so its minimum motion dimension is
exactly six.

This is a robust obstruction to one proof mechanism. It is not a negative
Gaussian hinge, a Gaussian-majorisation counterexample, or an effective
mixed-chain obstruction. It does not certify the particular strict witness
against arbitrary finite compositions of motion and norm-preserving steps.
The unrestricted dimension-three problem remains open. Historical priority
and optimality of the very conservative radius are not determined.

## Intrinsic halfway reduction

The coefficient vectors `r,s` both have sum zero. Therefore

```text
tau(D)=-(1/2) sum_(i,j) r_i s_j D_ij
```

is the scalar product of two affine differences and depends only on the
squared-distance matrix. Direct reconstruction gives `tau(D(P))=0`,
`tau(D(Q))=1`, and

```text
|tau(D)-tau(E)| <= (||r||_1 ||s||_1/2)||D-E||_max
                 = 3||D-E||_max.
```

The two perturbed endpoint values remain on opposite sides of `1/2`. Along a
continuous contracting motion every intermediate distance matrix lies
entrywise between its endpoint matrices, so the intermediate-value theorem
produces a placement `Z` satisfying

```text
D(Q)-delta <= D(Z) <= D(P)+delta,    tau(D(Z))=1/2.
```

Thus it is enough to exclude one arbitrary placement with these intrinsic
conditions; no motion schedule or monotonicity of `tau` is assumed.

## Repairing the two nearly rigid groups

For a centered reference matrix `X` and a centered candidate `Z`, double
centering gives

```text
G_Z-G_X=-(1/2)H(D_Z-D_X)H,
||G_Z-G_X||_F <= 2n delta.
```

With `M=(X^T X)^(-1)X^T Z` and `E=Z-XM`, projection orthogonality gives

```text
||E||_F^2 <= 2n^2 delta,
||MM^T-I||_op <= 2n delta/k,
```

where the independently recomputed scatter floor is `k=1/16`. The row-polar
factor `V=(MM^T)^(-1/2)M` is an isometric embedding into the same ambient
space. The singular-value estimate and the reference diameter bound imply

```text
||X(M-V)||_F^2 <= n^2 delta.
```

The two errors are orthogonal. Since `n<=16`, every point moves by less than
`32 sqrt(delta)`. Applying this separately to the two groups repairs a single
hypothetical placement into two exact rigid copies inside the original `R5`;
it does not assume or construct a rigid motion through time.

The pair-vector displacement is at most `64 sqrt(delta)`. Because all old
distances are below 12, the squared-distance error is at most
`1600 sqrt(delta)`. The exact constant guards correctly give

```text
delta+1600 sqrt(delta) < eta=2^-56,
|tau(D(W))-1/2| <= 4800 sqrt(delta).
```

## Axis repair

After an ambient normalization fixing the `A` group in the physical `R3`, the
other group is `Ub+t`. For the five matched parameters `u=xe_1`,
`x=-2,-1,0,1,2`, the matched cross losses have absolute value at most `eta`.
Their fourth finite difference is exactly

```text
48(1-M_33).
```

Since `M_33<=1`, this gives `|Ue_3-e_3|<=sqrt(eta)`. A minimal-plane rotation
of the rigid `B` copy sends `Ue_3` exactly to `e_3` inside the same `R5`. It
leaves the translation `t`, and hence the occurrence of its axial coordinate
in `tau`, unchanged. Its cross-distance cost is below `145 sqrt(eta)`.
Consequently all cross losses obey

```text
-e <= L(v,u) <= |v-Cu|^2+e,   e=2^-20,
|tau-1/2|<e.
```

The independent checker proves the fourth-difference identity on zero and
the 16 coordinate basis assignments. Both sides are affine in those entries,
so this is a complete identity check rather than numerical sampling.

## Two auxiliary dimensions force the contradiction

Axis alignment writes the embedding and translation as

```text
U(x,z)=(Nx,z,Kx),    t=(v,tau,w),    K:R2->R2.
```

The six matched samples at `0,+/-e_1,+/-e_2,e_1+e_2` isolate the constant,
linear, diagonal, and mixed coefficients of the cross-loss quadratic. They
give the stated bounds on `d-tau`, `C^T v-c_perp`, and
`sym(C^T(N-I))+2tau I`. Writing the remaining skew coefficient as `2alpha J`
then yields

```text
N=alpha(I+J)+E_N,    |(E_N)_ij|<=3e.
```

The three actual quarter-step probes imply

```text
|v_j|<=9/128,    |alpha-1/2|<=9/64.
```

Hence `k_0^2=1-2alpha^2>=367/2048` and `|v|^2<=81/8192`.

The matrix `H` in the proof is the Gram matrix of the two columns of `K` and
the vector `w`. These are three vectors in the two-dimensional auxiliary
space, so `det H=0`. The comparison matrix has the exact determinant

```text
det H_0=k_0^2(k_0^2/4-3|v|^2) >= 11377/2^22.
```

Every entry perturbation is at most `12e`; telescoping the six determinant
products gives `|det H-det H_0|<=864e`. The surviving margin is therefore

```text
11377/2^22-864/2^20 = 7921/2^22 > 0,
```

contradicting `det H=0`.

As a methodologically different control, the independent checker evaluates
the determinant identity on a `5 x 3 x 3` exact rational grid. The two sides
have coordinatewise degrees at most `(4,2,2)`, so tensor-product polynomial
interpolation makes the 45 checks conclusive for the universal identity.

## Strict witness and upper bound

The checker reconstructs the eight `B` parameters, all sixteen `A`
parameters, and both paraboloid embeddings directly from the formulas. It
then decodes the saved witness separately. All 128 cross-pair losses equal
`|v-Cu|^2`; all 148 within-group pairs are rigid; and exactly 156 of the 276
reference pairs are tight.

Scaling the complete target by `lambda=1-2^-145` adds the positive term
`(1-lambda^2)D(Q)_ij` to every old loss. The target sites are distinct, so all
276 losses become strict. Their maximum squared-distance ratio is exactly
`lambda^2`, attained on an old contact, and the target metric displacement is
strictly below `2^-136`. The augmented anchor matrix has rank eight, so no
single pair of norm anchors can explain this witness.

For any matching in `R3`, the path

```text
((1-s)p_i+s q_i, sqrt(s(1-s))(p_i-q_i))
```

lies in `R6` and has squared pair distances
`(1-s)D(P)_ij+sD(Q)_ij`. With `s=sin^2(theta)` it is analytic through the
endpoints. This supplies the claimed six-dimensional upper bound without a
motion search.

## Reproduction and trust boundary

The author checker passes in normal mode, optimized mode, direct-witness
mode, and under its full SHA-256 manifest. The new
[`independent_check.py`](independent_check.py) imports no author module and
pins seven immutable inputs. It records:

- 276 definition-level pair checks from a fresh formula reconstruction;
- 17 affine-basis checks for the contact fourth difference;
- 45 exact interpolation checks for the determinant polynomial;
- 55 independent perturbation and determinant constant checks;
- exact ranks six and eight for the paired and anchor-augmented matrices; and
- the full strict witness and metric-box inclusion.

Its status is `INDEPENDENT_STRICT_SCREW_R5_REVIEW_PASS`, with exact-state
SHA-256 `348581d8b041753827ede13568876b2c5ba0af097a97e3ce6e44a29b0af73d88`.

The code establishes these finite exact facts and guards against source drift.
It does not formalize polar decomposition, the universal perturbation lemma,
the intermediate-value reduction, or continuity of a contracting motion.
Those are independently audited mathematical steps above. The original
two-body geometry and the earlier intrinsic functional remain explicitly
credited dependencies; no prior motion checker or claimed Gaussian sign is
silently imported.
