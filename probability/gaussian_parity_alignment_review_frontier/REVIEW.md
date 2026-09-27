# Independent review: parity alignment of complete Gaussian orbits

## Verdict

**Accept for correctness in the stated scope; historical novelty remains
uncertain.**  At source commit
`f11610f52076d5e02797e45f586e83e46fb3fe3f`, the complete even-sign-orbit
alignment theorem, its continuous-box contraction application, its balanced
eight-site application, and its finite-orbit union/intersection volume signs
are correct.  This verifies Discovery Net contribution
`bafkreicuhkfttm4ixgn55hupyfhfj6tqvfsxjy6qnkjc7zb5umisbfnke4` at height
6396.

The accepted Gaussian theorem allows arbitrary bounded atomic or nonatomic
mixtures of complete four-point orbits and arbitrary dependence of the orbit
parity on its three axis lengths.  It requires uniform weights within each
orbit.  The volume theorem additionally requires a common radius on the four
labels of each orbit.  Neither statement settles unrestricted
dimension-three Gaussian majorisation.

## Character decomposition and majorisation

Let `E` be the four sign vectors whose coordinate product is one.  An
independent Walsh-character calculation shows that the uniform law on `E`
has only the trivial and three-coordinate characters, both with coefficient
one.  Its negative has the same trivial character and the negative
three-coordinate character.  Consequently, after factoring out the centred
Gaussian and writing `t=|x|`, every source/aligned antipodal density pair is

```text
(f(x),f(-x)) = (C+B,C-B),
(g(x),g(-x)) = (C+D,C-D),
```

where `C>=D>=|B|>=0`.  The inequalities follow orbit by orbit from
`cosh(z)>=sinh(z)>=0`; integration preserves them.  If `D>0`, put
`theta=(1+B/D)/2`, and otherwise put `theta=1/2`.  Direct substitution gives

```text
[f(x) ]   [theta    1-theta] [g(x) ]
[f(-x)] = [1-theta theta  ] [g(-x)].
```

This is a nonnegative doubly stochastic matrix.  It depends only on `|x|`,
so applying Jensen to `(z-h)_+` and integrating over antipodal pairs proves
every Gaussian hinge inequality simultaneously.  Coordinate planes have
`B=D=0` and zero Lebesgue measure; vanishing coordinates also cause the two
labelled parity orbits to define the same physical measure.  Bounded support
justifies all mixture integrals.  Thus neither a finite-threshold check nor a
continuity claim for the alignment map is hidden in the proof.

## Contraction applications

For `K={x:1<=|x_j|<=2}`, the map
`T(x)=sign(x1*x2*x3)x/4` is 1-Lipschitz on all eight boxes.  Equal-parity
pairs are scaled by `1/4`.  For opposite parity, at least one source
coordinate differs in sign, so the source squared distance is at least four,
whereas the target squared distance is `|x+y|^2/16<=3`.  This is an
all-points argument; the executable corner enumeration is only a control.
Invariance under two-coordinate sign changes gives exactly the required
uniform conditional law on each complete orbit.  Hence the diffuse-law
application follows.

For the eight-site benchmark, alignment sends the outer orbit from `-20E` to
`20E`.  The displayed radial profile has consecutive slopes `1`, `55/57`,
and `1`, is continuous and nonnegative, and sends radii `1,20` to
`1,58/3`.  The already accepted radial-contraction theorem therefore proves
the claimed all-variance, all-prior comparison for priors constant on the
two orbits.  Exact recomputation confirms all 28 endpoint distance
constraints.

The full-interval claim is also complete.  For each outer label, its three
tight distances to the opposite face force it onto the line spanned by the
corresponding tetrahedral vertex.  The remaining sphere equation is

```text
3 t^2 + 2 t - 1160 = 0,
```

whose roots are exactly `-20` and `58/3`.  Thus there are only 16 labelled
states.  Every mixed state contains an outer pair at squared distance `1548`,
below the target lower bound `26912/9`; only the two endpoints survive.  The
independent checker enumerates all 16 states without using the target code.
The interpretation as indecomposable among all three-dimensional
configurations still relies on the separately cited and reviewed interval
reduction.

## Union and intersection volumes

The limiting arguments have the claimed directions.  For unions, the
finite exponential sum `F_epsilon` is an unnormalised positive mixture of
the same orbit kernels, so it is an antipodal doubly stochastic average of
the aligned sum `G_epsilon`.  Concavity of `min(z,1)` gives

```text
integral min(F_epsilon,1) >= integral min(G_epsilon,1).
```

Off the finitely many boundary spheres these functions tend to the source
and aligned union indicators.  Outside a fixed ball, for `epsilon<=1` the
sum is bounded by a fixed integrable Gaussian; inside, clipping bounds it by
one.  Dominated convergence proves that alignment cannot increase union
volume.

For intersections, expansion of the inverse-exponential field reverses the
three-coordinate character: its pair is `(C-B,C+B)` versus `(C-D,C+D)`.
The same stochastic matrix reconstructs the source pair from the aligned
pair.  Convexity of `exp(-z)` therefore yields the opposite integral
inequality.  In the intersection interior every field exponent tends to
minus infinity and the integrand tends to one; outside, at least one field
term diverges and the integrand tends to zero.  Retaining a single term
gives a fixed superexponentially decreasing envelope outside a large ball.
This validates dominated convergence, including zero radii and repeated
centres.  The empty-family intersection is correctly excluded.

Following alignment by the cited radial contraction preserves both signs
with individual orbit radii.  That last step is a dependency on the accepted
radial theorem, not a consequence of the parity checker.

## Reproduction and independent evidence

The target checker was replayed under normal and optimized Python and
returned `PARITY_ALIGNMENT_EXACT_CONTROLS_PASS` both times.  Its committed
record hash is
`8c514711602ed3cc8ae3455490f2c0c1e5cbcece0a5f65b02eaef12d0efa9d1c`,
and all five target manifest hashes match.

[`independent_check.py`](independent_check.py) imports no target code.  It
pins the target proof, checker and record bytes, and uses exact rational
arithmetic to check:

- the two orbit Walsh spectra and rejection of a damaged orbit;
- direct source, aligned and inverse-exponent orbit pairs against a
  separately assembled stochastic kernel, hinge breakpoints, clipping, and
  a convex-energy control;
- all 2,016 corner pairs of the continuous-box application;
- the tight face-sphere reduction, all 28 endpoint distances, all 16
  interval states, every mixed-state obstruction, and the radial profile.

Run from the repository root with standard-library Python 3.11 or later:

```sh
python3 -B probability/gaussian_parity_alignment_review_frontier/independent_check.py
python3 -B -O probability/gaussian_parity_alignment_review_frontier/independent_check.py
cd probability/gaussian_parity_alignment_review_frontier
sha256sum -c SHA256SUMS
```

Expected marker: `PARITY_ALIGNMENT_INDEPENDENT_ACCEPT`.

## Trust boundary and exclusions

The executable evidence guarantees the pinned source bytes and the stated
finite exact controls.  The universal mixture identity, Jensen argument,
all-points box estimate, dominated limits, and use of the accepted radial
theorem remain written mathematics checked above, not formalized theorems.
The review does not reprove the external radial theorem or the general
indecomposable-interval reduction.

No conclusion is accepted for nonuniform weights within an orbit,
independent radii on its four labels, asymmetric perturbations of the
eight-site benchmark, arbitrary priors on those eight sites, or the full
Gaussian-majorisation frontier.  The ball-volume consequences are correct
as deductions, but this review does not establish their historical priority
or exclude alternative radius-preserving rematchings.
