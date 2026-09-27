# Covariance-free small-loss signs at arbitrary radius

Complete author proof, 27 September 2026; independent review pending.
The full dimension-three Gaussian-majorisation conjecture remains open.

For any bounded R3 law and any contraction of its support, define

    C_s=(2 pi s)^(-3/2), f=law(X)*gamma_s, g=law(TX)*gamma_s,
    H(u)=integral(g-C_s u)_+ - integral(f-C_s u)_+,
    d=E[|X-X'|^2-|TX-TX'|^2]/s,       m=max(g)/C_s.

Assume the actual centered source radius is at most R sqrt(s), with
integer R>=1. For every integer j>=1, [PROOF.md](PROOF.md) gives an explicit
integer N(R,j) such that

    d<=2^-N(R,j)  implies  H(u)>=0 for every u>=2^-j.

There is no covariance, minimum-weight, atom-count, or positive-loss floor.
Diffuse laws and simultaneous loss/covariance collapse are included. For
integer k>=0, the same guard also implies

    H(u)>=d 2^-P(R,j,k) on 2^-j<=u<=m-2^-k,
    P(R,j,k)=2[(6R+1)^2+R^2]+2R+2j+5k+19.

The mechanism uses covariance-free Procrustes alignment to make three
transverse directions of the standard R6 lift almost Gaussian. Spherical
averaging controls the otherwise unsigned radial term, making a local
Abel inversion positive. Entropy order alone is not used as a sign bridge.

**Consequence for the R2/R3/R8 frontier.** At fixed R,j, any adverse hinge
has d>2^-N. Combining this with the accepted covariance-boundary theorem
also forces both actual marginal covariances above an explicit dyadic
floor. R3's accepted all-radius loss-relative localization then applies
to the remaining frontier. This removes their previous simultaneous
zero-loss/covariance corner; the remaining interior and thresholds tending
to zero are unsigned. No new motion or Kneser--Poulsen case is claimed.

From this directory, with CPython 3.11.2 and the standard library only:

```sh
python3 -B verify.py
python3 -B -O verify.py
python3 -B verify.py --input INPUT.json
sha256sum -c SHA256SUMS
```

The first two commands reproduce [EXPECTED.json](EXPECTED.json), status
`COVARIANCE_FREE_SMALL_LOSS_PASS`. The [input](INPUT.json) is a weighted
version of the team's familiar 16-label simplex-flap control. Its paired
affine rank is six, and its exact loss is `(8/5) epsilon`. The whole family
`0<epsilon<=2^-487` passes `R=3,j=3,N=482`, although both covariance
eigenvalue minima tend to zero. At `k=2`, the margin is `d 2^-781`; the
explicit band `[1/8,1/2]` is nonempty for that family. This is a boundary
calibration, not new geometry.

Input fields are exactly `source,target,weights,variance,R,j,k`.
Coordinates, weights and variance are rational strings or integers;
`R,j,k` are integers. Coordinates have length three. Zero-weight labels are
discarded, active pairs must contract, and the actual centered radius is
checked. The consumer returns `UNRESOLVED` outside the sufficient loss
guard, `SUPPORT_ISOMETRY` at zero loss, or `SIGNED_ABOVE_CUTOFF`. It never
reports an adverse hinge or an all-threshold sign from failure of a guard.

The code checks a formal Laurent-polynomial radial identity, exact replica
and margin constants, 40 dyadic schedules, all-epsilon loss/covariance
polynomials, frame/variance invariance, and malformed-input rejection.
These checks and the content pins do not formalize the spherical estimate,
operator inequalities, coarea, or Abel inversion. See
[SOURCES.md](SOURCES.md) for precise dependencies and adjacent team work.
