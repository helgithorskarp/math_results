# A uniform strict margin for certified Gaussian contraction chains

Author proof, 27 September 2026; independent review pending. The full
dimension-three Aishwarya--Li question remains open.

For a bounded probability law and a supplied contracting motion in R5,
[PROOF.md](PROOF.md) gives an explicit Gaussian hinge margin proportional
to the ordered mean squared-distance loss D. The coefficient is independent
of atom count, small atom weights, covariance, motion speed and path length.
It also works for arbitrarily long finite chains mixing such motions with
anchored norm-preserving steps, with a common radius bound, and passes to
controlled weak limits. Non-strict comparison and finite composition are
credited antecedents. The uniform strict estimate is the increment.

Write C_s=(2 pi s)^(-3/2), H_f(h)=integral(f-h)_+, and suppose the source
fits a radius-R sqrt(s) ball, with integer R>=1. For j,k>=0 set

    B_N=40R^2+9R+38, B_M=66R^2+2R+18,
    n_N=B_N+3j+8k, n_M=B_M+4j+5k,
    n_C=max(n_N(R,j,k+1),n_M(R,j,k+1))+k+2R^2+2R+1.

At C_s 2^-j<=h<=max(g)-C_s 2^-k, a supplied admissible R5 motion gives
H_g(h)-H_f(h)>=(D/s)2^-n_M. A mixed chain gives (D/s)2^-n_C.
Motion regularity and the common anchor-radius requirement are stated
precisely in the proof. Arbitrary continuous motions are not silently
treated as absolutely continuous.

With m=max(g)/C_s, there is also a whole-curve envelope

    H_g(C_s u)-H_f(C_s u) >= (D/s)2^-B_C u^4(m-u)_+^9,
    B_C=max(B_N+8,B_M+5)+2R^2+2R+1,       0<=u<=1.

The polynomial threshold dependence incorporates R3's durable refinement
of the norm-preserving bound. A single M step instead has coefficient
2^-B_M and endpoint powers four and five.

The new estimate combines the known five-dimensional positive pressure
identity with an upper bound on the remaining peak increase. Only a final
budget of distance loss is needed, even if a chain has many small steps.
This gives strictness at every 0<h<max(g) when D>0. Together with accepted
compact-width rigidity and the older bounded-law openness theorem, it puts
these nonisometric pairs and their controlled limits in the ambient
fixed-variance interior, without an extra target homothety. The neighborhood
permits independent perturbations outside the original certificate classes.

## Exact finite consumer

Run from the repository root with Python 3.11 or later; only the standard
library is used. Tested with CPython 3.11.2.

```sh
python3 probability/gaussian_motion_chain_strictness/verify.py
python3 -O probability/gaussian_motion_chain_strictness/verify.py
python3 probability/gaussian_motion_chain_strictness/verify.py probability/gaussian_motion_chain_strictness/INPUT.json
```

The first two commands reproduce [EXPECTED.json](EXPECTED.json), including
50 posterior-rate checks, 48 polynomial pressure-transform checks, 3276
suffix-budget cases, five subdivisions, three small-loss controls, six
independent-frame controls, 30 radial-cutoff checks and 12 rejected or
malformed inputs. No Python
`assert` is used for validation. Check the content manifest inside this
directory with `sha256sum -c SHA256SUMS`.

The consumer accepts rational coordinates and weights, a source-ball
anchor, positive variance, integer R>=1, threshold bits j,k, and a list of
stages. Exact sufficient guards are:

| Stage | Required finite certificate |
| --- | --- |
| `norm` | Every pair contracts; supplied anchors have equal source/target radii, all <=R sqrt(s). |
| `straight` | Every pair contracts; the derivative of its squared distance at the end of the straight interpolation is nonpositive. Convexity makes the whole interpolation contractive. |
| `orthogonal_lift` | Every pair contracts; the sum of source and target affine ranks is at most five. The standard orthogonal sine/cosine lift fits in R5. |

These guards are sufficient, not a complete search for a motion or chain.
Failure returns `UNRESOLVED`, never a negative hinge. Malformed data raise
an error. General motions allowed by the theorem require separate supplied
certificates. The consumer also derives a rational lower bound on the target
peak; it does not use a numerical peak oracle or Gaussian sign quadrature.

The 18-site [fixture](INPUT.json) folds two layers onto one and then applies
a rank-two-to-rank-three contraction. It has paired affine rank six, ordered
loss 167/36, and variance one. Its certified margin is

    (167/36) 2^-328,     1/8 <= h/C_1 <= 107/144.

This small exact calibration illustrates the formula; it is not a new
geometric obstruction or a practical unrestricted cover. Subdivision tests
show that increasing chain length does not change the coefficient.

## Reuse and limits

R2/R3 can use the explicit middle minimum with separately signed low and
peak endpoints in their existing finite-certificate mechanism. Their
reviewed geometric hypotheses remain necessary. R6's supplied regular R5
motion classes also gain strictness from Theorem A. Exact dependency files
and status boundaries are in [SOURCES.md](SOURCES.md) and
[DEPENDENCIES.json](DEPENDENCIES.json).

The proper-screw family still lacks a certificate of these types. Neither
its sign nor a new Kneser--Poulsen consequence follows here. The analytic
pressure estimate, limit argument and openness implication are written
author proofs; the finite checker does not formalize or independently
review them.
