# An open eight-site obstruction to five-dimensional contraction paths

Complete author proof, 27 September 2026; independent review pending.
The unrestricted dimension-three Gaussian-majorisation question remains open.

We give an explicit open family of strict contractions for which **no
continuous path in five dimensions can stay in the endpoint squared-distance
intervals**. In particular, these contractions have no continuous contracting
lift to `R^5`. The obstruction is a rank inequality with a positive margin,
not the failure of a chosen motion formula. It supplies a finite geometric
benchmark for the Gaussian sign problem. It proves neither a negative
Gaussian hinge nor a Kneser--Poulsen volume inequality.

## 1. Statement and coordinates

Put

```text
v_0=(1,1,1), v_1=(1,-1,-1),
v_2=(-1,1,-1), v_3=(-1,-1,1),
r=20, c=r-2/3=58/3, e=1/100.
```

There are eight labelled sites, four core sites `a_i` and four moving sites
`b_i`. Define template configurations in `R^3` by

```text
P: a_i=v_i, b_i=-r v_i;
Q: a_i=v_i, b_i= c v_i.                         (1)
```

For configurations `X,Y` with this labelling, suppose every endpoint squared
distance is within `e` of the corresponding template squared distance:

```text
|d_X(j,k)^2-d_P(j,k)^2| <= e,
|d_Y(j,k)^2-d_Q(j,k)^2| <= e.                    (2)
```

**Theorem 1 (metric-interval obstruction).** There is no continuous motion
from `X` to `Y` in `R^5` during which every squared distance stays between
`d_Q(j,k)^2-e` and `d_P(j,k)^2+e`. Consequently, when `Y` is a contraction
of `X`, no continuous contracting motion between them exists in `R^5`.
The conclusion also holds in every smaller ambient dimension.

The endpoint configurations in this statement may themselves lie in `R^5`;
only their squared distances matter. Reflections, translations, rotations,
and arbitrary continuous changes of frame are included. No differentiability
of the motion or synchronisation of the moving sites is assumed.

An explicit full coordinate box consists entirely of strict contractions
to which Theorem 1 applies. Write

```text
eta=2^(-20), lambda=1-eta, h=2^(-28), Qhat=lambda Q.
```

**Corollary 2 (strict coordinate box).** Perturb each of the 24 coordinates
of `P` independently by at most `h`, and each of the 24 coordinates of
`Qhat` independently by at most `h`. Every resulting pair `(X,Y)` satisfies
(2), and every distinct pair of labels has squared-distance loss greater
than `2^(-18)`. Nevertheless no pair has a contracting lift in `R^5`.
Thus the interior of this 48-coordinate box is an open family of strict
three-dimensional contractions with the obstruction.

The general fact that some contractions need six dimensions is classical.
We claim no minimal number of sites or historical priority. The useful
addition here is the explicit finite interval separator and its strict
perturbation box. The four moving sites in (1) are reflected face centroids,
not the twelve face-vertex sites of the classical simplex-flap example.
Sources and the precise relationship to team results are in [SOURCES.md](SOURCES.md).

## 2. Endpoint geometry and the separator

The tetrahedral identities are

```text
sum_i v_i=0, v_i.v_i=3, v_i.v_j=-1 (i!=j),
sum_i v_i v_i^T=4 I_3.                          (3)
```

The opposite face to `v_i` lies in `v_i.x=-1`; reflecting `-r v_i`
in that plane gives `(r-2/3)v_i`. Thus (1) is the restriction of the
reflected metric projection onto this tetrahedron at these four exterior
normal rays, together with the fixed vertices. This geometric interpretation
is not used as a shortcut to nonexpansiveness: all distances are as follows.
Let `K=3r^2-2r=1160`.

| Pair | Source squared distance | Target squared distance |
| --- | ---: | ---: |
| `a_i,a_j`, `i!=j` | `8` | `8` |
| `b_i,a_j`, `i!=j` | `K+3=1163` | `1163` |
| `b_i,a_i` | `3(r+1)^2=1323` | `3(c-1)^2=3025/3` |
| `b_i,b_j`, `i!=j` | `8r^2=3200` | `8c^2=26912/9` |

All 28 template pair losses are nonnegative. There are 18 tight pairs and
10 strictly contracted pairs. The source and target sites are distinct.

For any instantaneous configuration define the intrinsic scalar

```text
Xi = sum_(i,j) |b_i-a_j|^2 - 4 sum_i |b_i-a_i|^2.          (4)
```

At the two templates, `Xi(P)=-1920` and `Xi(Q)=1856`. Perturbing every
squared distance by at most `e` changes `Xi` by at most `24e`: the twelve
off-diagonal cross entries have coefficient 1 and the four diagonal entries
have coefficient -3. Therefore (2) preserves the opposite signs. Every
continuous path between such endpoints must meet `Xi=0`.

We will prove that no configuration in the indicated distance intervals
and with `Xi=0` can be realised in `R^5`.

## 3. Recovering an approximate tetrahedral frame

Translate the core centroid to zero, and write its four vectors as `A_i`
and the moving vectors, relative to the same centroid, as `B_i`. Define

```text
M=(1/4) sum_i A_i v_i^T, G=M^T M.
```

Equation (3) gives `A_i=M v_i` exactly. The six core squared distances
are in `[8-e,8+e]`. It follows that

```text
||G-I||_op <= delta=3e/8 < 1/100.                (5)
```

Here and below all matrix norms are Euclidean operator norms. To see (5),
given `u` put `alpha_i=v_i.u/4`. Then `sum alpha_i=0`,
`sum alpha_i v_i=u`, and `sum alpha_i^2=|u|^2/4`. The centred Gram identity
gives

```text
|u^T(G-I)u| <= e sum_(i<j) |alpha_i alpha_j|
             <= (3e/2) sum_i alpha_i^2 = (3e/8)|u|^2.
```

Thus the core span `L=im M` has dimension three. Write

```text
w_i=M^T B_i=s_i v_i+h_i,  h_i.v_i=0,
B_i=Proj_L(B_i)+z_i,      z_i in L-perp.          (6)
```

For `j,k!=i`, the two tight cross distances are each in
`[K+3-e,K+3+e]`. Their difference yields

```text
|w_i.(v_j-v_k)| <= e+3delta = 17e/8.
```

The three unordered differences among the three vertices opposite `v_i`
have frame matrix `12 Proj_(v_i-perp)`. Consequently

```text
|h_i| <= 17e/16 <= 2e.                          (7)
```

Using any of these same three cross distances and `v_i.v_j=-1` gives

```text
|B_i|^2=K-2s_i+E_i,     |E_i|<=10e.              (8)
```

Indeed the error is bounded by `3delta+2 sqrt(3)|h_i|+e`, which is at
most `10e` by (7) and `sqrt(3)<7/4`.

The separator has a particularly simple meaning in this frame. Since
`sum A_i=0`, direct expansion of (4) gives

```text
Xi=8 sum_i A_i.B_i=24 sum_i s_i.                 (9)
```

No orthogonal frame needs to be chosen continuously for this identity.

## 4. Rank contradiction on the separator

Assume `Xi=0`, hence `sum s_i=0`. The lower bound on the six outer
distances and (8) imply

```text
|sum_i B_i|^2
 =4 sum_i |B_i|^2-sum_(i<j)|B_i-B_j|^2
 <=16K-48c^2+166e
 =32r-64/3+166e < 621.                          (10)
```

Applying `M^T`, and using (5) and (7), gives

```text
|sum_i s_i v_i| <= sqrt((101/100)*621)+8e < 26.
```

The tetrahedral Gram matrix and `sum s_i=0` now imply

```text
sum_i s_i^2 < 169,
sum_i |Proj_L(B_i)|^2
 =sum_i w_i^T G^(-1)w_i
 <=(100/99)(3*169+4*(2e)^2) < 513.               (11)
```

Next let `alpha` be any four-vector with `sum alpha_i=0`. Write
`|B_i-B_j|^2=8r^2-E_ij`. The interval constraints give

```text
-e <= E_ij <= D+e,     D=8(r^2-c^2)=1888/9.
```

The centred Gram identity therefore yields

```text
|sum_i alpha_i B_i|^2
 >= [4r^2-D-2e] sum_i alpha_i^2
 > 1390 sum_i alpha_i^2.                        (12)
```

For completeness, the elementary uniform bound behind (12) is
`sum_(i<j,alpha_i alpha_j<0) |alpha_i alpha_j| <= sum_i alpha_i^2`.
If the positive and negative supports have sizes `k` and `4-k` and their
common total absolute mass is `m`, Cauchy--Schwarz gives
`m^2 <= k(4-k) sum alpha_i^2/4 <= sum alpha_i^2`.
Also `sum_(i<j)|alpha_i alpha_j| <= (3/2)sum alpha_i^2`.
Thus the error term is actually at most `(D+3e/2)sum alpha_i^2`;
the weaker constant in (12) is sufficient. Zero entries cause no problem.

Subtract the contribution of the projections in (11), using
Cauchy--Schwarz for their linear combination. Equations (11)--(12) imply

```text
|sum_i alpha_i z_i|^2 > 877 sum_i alpha_i^2
              whenever sum alpha_i=0 and alpha!=0.          (13)
```

The space of such coefficient vectors has dimension three. Equation (13)
says its linear map into `L-perp` is injective. But in `R^5`, the orthogonal
complement of the three-dimensional core span has dimension two. This is
impossible. The argument rules out every configuration on the separator,
and the intermediate value theorem proves Theorem 1.

## 5. The strict open family

All template coordinates have absolute value at most 20. Perturbing each
coordinate of a configuration with that bound by at most `h` changes each
squared distance by at most

```text
480h+12h^2 <= 481h.                              (14)
```

The same applies to `Qhat`. Since the largest target template squared
distance is less than 3200, scaling `Q` by `lambda=1-eta` changes each
squared distance by at most `6400eta`. Exact rational comparison gives

```text
6400eta+481h < e.                                (15)
```

Thus the entire coordinate box satisfies (2). The smallest template target
squared distance is 8. Every central pair loss obeys

```text
d_P^2-lambda^2 d_Q^2
 =(d_P^2-d_Q^2)+(1-lambda^2)d_Q^2 > 8eta.
```

After both endpoint perturbations, the loss is greater than

```text
8eta-962h =1086h > 2^(-18).                       (16)
```

This proves Corollary 2, including all boundary points of the coordinate
box. Applying Theorem 1 to its interior proves the open-family assertion.

## 6. Relation to Gaussian measures and validation

Every finite pair in Corollary 2 defines a 1-Lipschitz map on its eight
source sites, and hence has a full-space 1-Lipschitz extension by the
classical Euclidean Lipschitz extension theorem. Any positive weights
therefore give an admissible bounded-law instance of the named Gaussian
problem. This extension fact is used only for that interpretation; it is
not a premise of the metric obstruction.

For a version where deterministic rematching cannot remove the obstruction,
assign weights `1,2,4,...,128`, divided by 255, to the eight labels in order
`a_0,...,a_3,b_0,...,b_3`, at both endpoints. Distinctness of the target
sites and uniqueness of binary subset sums force every deterministic map
with this target law to use the prescribed labelled matching. The statement
does not rule out nondeterministic couplings or other proofs of majorisation.

This family lies outside every positive class whose specified labelled
contraction has an `R^5` contracting motion, including finite compositions
of such motions with intermediate configurations in `R^3`. It does not
establish that Gaussian comparison fails there. No hinge is computed, and
no Gaussian sign, indecomposability, or exhaustive extremal-map
classification is claimed. In particular it does not reopen the accepted
orthocentric depth-one sign theorem.

The obstruction is dimensionally sharp for these endpoints in the usual
sense: the classical six-dimensional leapfrog connects every contraction.
An exact check at the template separator makes the distinction visible.
Take the core in the first `R^3` and `B_i=(0,b v_i)` in the other `R^3`,
where `b^2=1160/3`. These eight points have `Xi=0` and all required distance
intervals, but their joint span has dimension six. Their residual Gram
matrix has rank three, as required by (13).

[verify.py](verify.py) checks the 28 template distances, the intrinsic
separator, the tetrahedral and face frame identities, all rational margins
in the proof, the strict coordinate box, the six-dimensional control and
the binary-weight claim. It also checks the central paired affine rank is
six and rejects deliberate invalid constant/endpoint controls. It uses
Python 3.11+, standard library rational arithmetic only. The continuum
path exclusion and the stated universal inequalities are the written proof;
the code is compact exact supporting evidence, not a numerical path search
or a formal proof assistant.
