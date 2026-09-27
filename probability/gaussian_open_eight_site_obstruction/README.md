# An open eight-site obstruction to five-dimensional lifts

An explicit box of **strict contractions in R3** has no continuous
contracting motion in R5. All 48 endpoint coordinates can vary independently
within the stated box, and every squared-distance loss stays above `2^(-18)`.

The [proof](PROOF.md) uses an intrinsic linear separator in squared
distances. Every path between the endpoints must cross it; every
configuration on it would require three residual dimensions in addition
to the three-dimensional core. The certified residual lower bound is 877.
This excludes all motions, including asynchronous and nonlinear motions.

The family is a finite benchmark outside the standard two-auxiliary-coordinate
Gaussian/Kneser--Poulsen transfer route. **It is not a counterexample to
Gaussian majorisation or to Kneser--Poulsen.** Independent review is pending;
no minimality or historical priority is claimed. [SOURCES.md](SOURCES.md)
separates the new finite certificate from classical dimension barriers and
existing team results.

Reproduce with Python 3.11+, standard library only:

```sh
python3 probability/gaussian_open_eight_site_obstruction/verify.py --check
python3 -O probability/gaussian_open_eight_site_obstruction/verify.py --check
```

Both commands reproduce [EXPECTED.json](EXPECTED.json), with status
`OPEN_EIGHT_SITE_INTERVAL_OBSTRUCTION_PASS`. The code checks exact finite
identities and bounds; the universal rank and continuity argument is written
mathematics. No solver, floating-point computation or external data is used.
