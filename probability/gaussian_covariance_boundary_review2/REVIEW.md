# Independent acceptance: arbitrary-radius covariance-boundary signs

## Verdict

**Accept for correctness in the stated scope.**  At Gaussian variance one,
let a centered source satisfy `|X|<=R`, where integer `R>=1`, let the mean
pair loss obey `D>=2^-k`, and restrict thresholds to `u>=2^-m`, with
`m>=1,k>=0`.  Put

```text
q = ceil(sqrt(2(m+1))),
B = 31+47R^2+2(2R+q)^2+5k,
L = 2B+4.
```

If either marginal has variance at most `2^-L` in some unit direction, the
reviewed argument proves every such hinge nonnegative.  For
`2^-m<=u<=||f||_infinity/C`, it proves the strict gap `H(u)>=2^(-B-1)`.
Consequently an adverse point in this fixed positive-loss/positive-threshold
slab has both covariance matrices strictly above `2^-L I`.

The exact target is Discovery Net artifact
`bafkreibispqtfpr3v5zk6n3pnjxql25oaznxpt6tdtzu4r6gecbjycdiwq` at source
commit `262439aa29c2ce7f7f14b7ab1bdd85c92bd13338`.  The eight target files and
the material target-peak dependency are content-pinned in
`TARGET_INPUTS.json`.  The target author checker passes under normal and
optimized CPython 3.11.2 and reproduces record SHA-256
`aa538a5a2eb95362e2a8c524945d8d926e2befcadb03d3a7e49a87d91219a916`.

This theorem does not sign the positive-covariance interior, close the joint
zero-loss/covariance corner, cover a threshold tending to zero uniformly, or
settle the full dimension-three majorisation frontier.  The constants are
sufficient, not sharp.  Historical novelty was not exhaustively checked.

## Projection and endpoint comparison

For a thin source direction, projecting to `X0=PX` and comparing with
`Y0=T(PX)` is legitimate after a Kirszbraun extension.  Centered `L2`
triangle inequalities give

```text
|D-D0| <= 2 lambda + 4R sqrt(lambda) <= 6R sqrt(lambda).
```

For a thin target direction, projection is itself contractive and the exact
identity is `D0=D+2 lambda`.  The corresponding `R2+R3` and `R3+R2` paths
have squared pair distances affine and nonincreasing in time, so they are
eligible `R5` motions.  Moving-anchor translations in the target case do not
change peaks or hinges.

Gaussian translation gives global endpoint errors at most `eta=sqrt(lambda)`
in `L1`, at most `C eta` in peak height, and at most `2 eta` in the hinge.
At a source mode the posterior density is at least `exp(-2R^2)` on every
label.  Jensen's posterior pair-loss identity therefore yields

```text
G0-F0 >= (C/4) exp(-9R^2/2) D0.
```

With `Z=k+4+9R^2` and `zeta=2^-Z`, the retained-loss and approximation
budgets correctly imply `G0>=F+C zeta`.  This is the essential bridge from
the projected reference comparison to every threshold through the actual
source peak.

## Independent audit of the target-peak dependency

The target consumes Theorem H2 from `HINGE_MARGIN.md` at exact dependency
commit `32f04f8f67c0dae00eda7443912cb5b3a0ca2f02`.  Because no prior independent
acceptance of H2 was present, this review checked that theorem rather than
treating it as a black box.

The primary arXiv v2 source derives equation (66), the needed
Lebesgue--Stieltjes pressure identity for a continuous contracting motion.
Taking the energy density `U(r)=rQ(r)` makes its pressure `r^2 Q'(r)`, exactly
the integrand used in H2.  Uniform polynomial approximation of `Q'` controls
both endpoints and the Gaussian-product integral, so the extension from
polynomial energies to smooth steps is valid.

In `R5`, the peak lower bound and global Gaussian gradient bound produce an
inner ball of radius

```text
r0 = (sqrt(e s)/2) ((a-h)/C3).
```

Radial integration over `S4`, followed by the uniform two-kernel floor,
reduces to the stated coefficient
`A=exp(5/2)/(96 sqrt(2 pi))`.  Marginalizing two Gaussian coordinates is
exact because `gamma_2(Y)/C2` is uniform on `(0,1)`; the lifted threshold
mass is therefore precisely the three-dimensional hinge.

For the target-peak completion, the posterior at a target mode gives
`log(G/F)<=exp(R^2/s)d/(4s)`.  The continuous remaining-loss function selects
a terminal time with retained loss

```text
min{D, 4s exp(-R^2/s) log(2M/(M+h))}.
```

Every later lifted peak is at least `C2(M+h)/2`.  The Stieltjes integrand is
nonnegative, and continuity of every pair distance makes its Stieltjes
measure atomless, so restricting to the terminal interval loses no endpoint
mass.  This proves the exact H2 bound used by the target.  No product
decomposition of the intermediate `R5` law is assumed.

## Exponent assembly

For `h=Cu`, `M=G0`, the peak separation gives `M-h>=C zeta`.  Hence the
fourth-power shell factor contributes at least `zeta^4/16`, while the
terminal loss contributes at least `exp(-R^2)zeta`.  The elementary bounds
`A>2^-7`, `log(2/u)<=m+1`, and `e<4` give

```text
H0(u) >= 2^-11 zeta^5 exp(-R^2-(2R+q)^2) >= 2^-B.
```

The formula for `B` is exactly
`11+5Z+2R^2+2(2R+q)^2`.  Also `B+2>=Z` and
`B+2-k>=4R^2`; since `12R<=2^(4R^2)`, the covariance hypothesis supplies all
three side conditions

```text
eta <= zeta,   eta <= 2^-k/(12R),   eta <= 2^-B/4.
```

Thus the projected loss is retained, the peak gap is valid, and subtracting
the `2 eta` hinge error leaves `2^(-B-1)`.  Above the actual source peak its
hinge vanishes, so the target hinge alone gives nonnegativity.

## Exact evidence and trust boundary

`independent_check.py` imports no target module.  It pins nine exact inputs,
reconstructs 60 schedules and 840 exact dyadic implications, checks the H2
constant cancellation, and verifies both projection/loss identities on a
fresh rational contraction.  Reproduce with:

```sh
python3 -B independent_check.py
python3 -B -O independent_check.py
sha256sum -c SHA256SUMS
```

The checker guarantees provenance, integer schedules, dyadic rounding,
side-condition closure, and the independent rational projection controls.
The Stieltjes pressure identity, smooth-step limiting argument, radial shell
estimate, Gaussian posterior inequalities, diffuse-law passages, and
Kirszbraun extension remain independently reviewed written mathematics, not
proof-assistant output.  The arXiv equation is a cited primary theorem rather
than a newly formalized result.
