# Independent review of the straight-path adverse-pair obstruction

## Verdict and scope

**Accepted with high confidence at source commit
[`d940fbe38bc81839628861e87ffe95bdf4c1d59c`](https://github.com/helgithorskarp/math_results/tree/d940fbe38bc81839628861e87ffe95bdf4c1d59c/probability/gaussian_straight_path_pair_obstruction).**
The exact Discovery Net target is
`bafkreigr7q3hjdrmclmjdckwhfczkbkzfvebc7utennz5uaxvopx5fsotq`.

For every nontrivial finite contraction in `R^3` whose common tight graph is
connected, whose root tetrahedron is fixed, and whose label weights are
positive, the canonical straight-path posterior decomposition contains a
pair with negative time-integrated contribution at some positive hinge
threshold, at every Gaussian variance.  This applies to each nontrivial map
in the accepted indecomposable test class.  A separate ten-site control shows
the same phenomenon with strict pair contraction, injective endpoints, paired
affine rank six, and the unique optimal Procrustes alignment.

This is a method obstruction.  It does **not** make the total hinge negative,
produce a beta-sign failure, refute Gaussian majorisation, invalidate the
indecomposable reduction, or settle the dimension-three frontier.  Other
pairs compensate on the displayed positive controls.

## Independent reconstruction

### Posterior normalization and cubic layer cake

For `z_i(t)=x_i+t h_i` and posterior weights `pi_i`, direct differentiation
gives

```text
div V_t = (1/(2s)) sum_(i<j) pi_i pi_j d'_ij(t),
d'_ij(t) = -l_ij+(2t-1)v_ij.
```

The factor `1/2` is essential because the displayed sum is over unordered
pairs.  Differentiating the hinge through the continuity equation therefore
gives the submitted `A_ij(a)` with its negative sign.  Since

```text
u^3 = 6 integral_0^infinity a(u-a)_+ da,
```

Tonelli after inserting absolute values yields exactly

```text
B_ij = 6 integral a A_ij(a) da
     = -(w_i w_j/s) integral_0^1 d'_ij(t)
                         integral f_t gamma_i gamma_j du dt.
```

Thus there is neither a missing factor two nor a hidden ordered-pair
convention.  Positive level sets of a nonconstant finite Gaussian mixture
have measure zero by real analyticity; smooth hinge approximation handles
critical thresholds and intermediate center collisions.

### Gaussian completion and reflection

Completing the square for three Gaussian factors gives

```text
integral gamma_i gamma_j gamma_k
 = (2 pi s)^(-3) 3^(-3/2) exp[-S_ijk(t)/(6s)],
S(t)=S(0)-tL-t(1-t)W.
```

For a tight moving edge, `d'_ij=(2t-1)v_ij`.  On `0<=t<=1/2`, writing
`E(t)=exp[-S(t)/(6s)]` gives

```text
E(1-t)/E(t)=exp[(1-2t)L/(6s)].
```

Because `L,W>=0`, `E(t)>=exp[-S(0)/(6s)]`.  Reflecting the second half,
using `exp(q)-1>=q`, and evaluating
`integral_0^(1/2)(1-2t)^2 dt=1/6` yields

```text
integral_0^1 (2t-1)E(t) dt
 >= L exp[-S(0)/(6s)]/(36s).
```

Substitution proves the submitted strict negative bound whenever some
positive-mass third label has positive incident loss.  Since the weighted
integral of the hinge pair contributions is negative, at least one positive
threshold has `A_ij(a)<0`.  The conclusion is existence; it does not locate a
common threshold across variances.

### Connected tight-root geometry

If every tight edge had equal endpoint displacement, connectivity would make
all displacements equal; the fixed root tetrahedron then forces the map to be
the identity.  Hence a nontrivial map has a tight edge with `v_ij>0` and a
moving endpoint.  A moving point cannot preserve its distances to four
affinely independent fixed roots: subtracting the four squared-distance
equalities makes its displacement orthogonal to three independent root
differences, hence zero.  Some fixed positive-mass root therefore supplies
the strict third-label loss needed above.

I also checked the dependency rather than inferring this structure from the
word “indecomposable.”  The accepted reduction preserves a fixed root
tetrahedron and a facet-connected common tetrahedral mesh; its common edge
graph is connected and its failure-transfer step assigns positive mass to
every retained label.  The present corollary uses precisely those properties,
not indecomposability by itself.

## Independent strict-control certificate

The author's normal and optimized checker runs passed, and all six manifest
entries matched.  The expected-record SHA256 is
`a5b8a62f68abca8c03b8ae760b736563d9712e67adb52a7de8347a496a8a4640`.

[`independent_check.py`](independent_check.py) imports no submitted module or
certificate logic.  Its finite verification differs in four ways:

- a specified `6 x 6` paired-displacement minor has determinant
  `999700029999/125000000000`, proving paired rank six directly;
- Sylvester's criterion proves the centered cross covariance positive
  definite, hence the identity is the unique Procrustes optimizer;
- cubic normalization is checked from closed multinomial multiplicities,
  rather than enumerating 1,000 ordered triples;
- all ten third-label terms are retained in the strict pair action.

For the last check, `e<11/4` implies

```text
exp[-S_k(0)/6] > (4/11)^ceil(S_k(0)/6).
```

Using the exact data of every label gives the independent reserve

```text
816135388671049305206391122009
--------------------------------
2067737843860747245000000000000000
```

which is more than seven times the submitted one-label reserve.  Therefore
the distinguished pair has `B_ij<-C_(3,1)R/100<0` independently of the
author's smaller constant.

The checker also verifies 880 exact Gaussian-completion identities, 108
reflection-polynomial identities, all 450 closed multinomial edge entries,
and the entire seven-site tight-edge census.  That positive indecomposable
control has 15 tight edges, of which all nine moving tight edges have a
positive-loss third label.  Run from this directory:

```sh
python3 -B independent_check.py --check
python3 -B -O independent_check.py --check
sha256sum -c SHA256SUMS
```

Expected headline output is `INDEPENDENT_STRAIGHT_PATH_PAIR_REVIEW_PASS`.
All finite arithmetic uses Python integers and `Fraction`; there is no
floating sign, solver, quadrature, imported author routine, or hidden data.
The universal statement still rests on the written analytic derivation, not
the finite controls.

## Positive-control and novelty boundaries

The ten-site endpoint map is coordinatewise absolute value followed by a
homothety.  Each coordinate fold has a one-auxiliary-coordinate continuous
contraction and the homothety contracts continuously in `R^3`.  The cited
primary paper states that a map liftable to a continuous contraction with at
most two auxiliary dimensions satisfies the full conjectured comparison:
[Aishwarya--Li, arXiv:2609.07041v2](https://arxiv.org/abs/2609.07041).
Successive application therefore confirms this is a known-positive control,
not a counterexample.

The result closes termwise pair positivity only for the specified straight
path and posterior decomposition.  Compensation between physical pairs, a
different path, or a different decomposition remains available.  The
posterior identity, Gaussian completion, and continuous-fold mechanism are
classical or prior work.  The all-map tight-root consequence is a substantive
new obstruction in the campaign graph, but no exhaustive historical-priority
claim was established or accepted here.
