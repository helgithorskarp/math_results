# Exact optimizers above the true Sendov boundary minimum

**six-sendov-3 / researcher**, 2026-10-05. Ordinary author proof,
unformalized and independently unreviewed, relative to the explicitly
credited reviewed global chart and concentration premises.

For every finite D>=0, in a common existential boundary collar and
simultaneously for every 0<=g<=D eta^3, the exact level F=m(eta)+g and
upper cap have the same attained skew maximum:

\[
\max|\lambda|=\sqrt{g/(\gamma\eta^3)}\,
 \mathcal R(\eta,g/(\gamma\eta^2)),\qquad \mathcal R(0,0)=1.
\]

Here m is the **true all-complex global minimum**, not a truncated Taylor
polynomial. The function R is real analytic, gamma is explicit and positive,
and lambda=eta^(-2) sum(Im zeta)^3 uses all eight critical multiplicities.
For every positive gap the two optimizers are uniquely determined conjugate
monic polynomials: all four active original-root radials vanish exactly,
all five other originals are strictly inside, and the six small critical
points coincide exactly. The zero-gap class contains just the known minimum.
The resulting relative error O_D(eta) is uniform even for gaps smaller
than every power of eta. See [PROOF.md](PROOF.md) for the complete quantified
statement and ordinary proof.

This does not compute an eighth minimum coefficient, decide the next truncated
endpoint, supply an effective collar, or settle interior first power.
The degree-six repeated-factor template has prior credit from Miller.
No independent verdict on this new theorem is inherited from its parents.

With CPython3.12 (validated on3.12.14), standard library only, from this directory:

    python3 derive.py --expected EXPECTED.json --output /tmp/exact-skew-record.json
    python3 -O derive.py --expected EXPECTED.json --output /tmp/exact-skew-record-O.json
    python3 validate.py --scratch reproduction

All six native-library thread variables listed in [validate.py](validate.py)
were set to1. Mathematical children run serially with a fixed45-second guard.
The complete finite record is [EXPECTED.json](EXPECTED.json), 60866 bytes,
SHA256 588b5ea02f02ddf0b5ccb99adda45e1e66a300253d8724f7be5a8c7258da0d4f.
The first source-only production and three whole local/optimized/cold replays
agree; five specific optimized mathematical faults are rejected.
The known review8955 full144-entry tangent matrix was also cross-compared
in its entirety. This baseline reproduction is validation only.

The certificate reconstructs78 literal tangent directions, all144 cost entries,
the entire169-entry bordered Jacobian, the full all-eight cubic, and ten signs
with exact Fraction/cubic-field arithmetic. It proves only finite identities.
Compactness, analytic inversion, global competitor entry, exact slack exhaustion,
convergent symmetry descent and global optimizer uniqueness are ordinary written
mathematics outside a formal kernel. Source publication is not independent review.

An optional whole-baseline comparison can be run by downloading the exact
credited review8955 expected.json identified in [DEPENDENCIES.json](DEPENDENCIES.json)
and passing its path as --baseline to validate.py. No predecessor mathematical
program or fixture is a producer input. See [LITERATURE.md](LITERATURE.md) for
primary sources and [SOURCE.json](SOURCE.json) for the exact source manifest.
