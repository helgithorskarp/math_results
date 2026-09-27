# Why the existing geometric tail cannot close the small-loss window

This is a uniform obstruction to composing two sufficient certificate
schedules, not a counterexample to Gaussian majorisation. The written
argument is complete; independent review is pending. The unrestricted
three-dimensional problem and accepted global defect cap remain unchanged.

For every bounded-law contraction with centered source radius at most 1/2,
source covariance at least 2^-15 I, positive mean pair loss
`d<=2^-(44m+208)`, and integer m>=4, the accepted moving window signs all
`u>=exp(-m^2/2)`. Every application of the existing mean-support low-tail
formula has cutoff radius **Q>256m**, even with the exact admissible
mean-support gap, optimal cloud-mass floor, and independently chosen centers.
This covers finite atoms and finite-cluster certificates for diffuse laws:
grouping rare atoms into clouds cannot repair the same join.

[PROOF.md](PROOF.md) also gives a general necessary join condition eliminating
the mass floor and geometric gap. Its exposed-cap argument forces a whole
source cloud to pay for the claimed gap in the mean-loss budget. It excludes
a whole parameter search without evaluating a Gaussian hinge. A coupled,
loss-sensitive tail or a
different intermediate sign argument is still needed in this regime.

R2's new dilated-martingale theorem does give a uniform all-threshold
family. Its stated sufficient variance schedule is disjoint from this
normalized small-loss regime; a short compatibility calculation is included.
This does not limit other martingale arguments or actual Gaussian signs.

With CPython 3.11 or later and Git, from this directory:

```sh
python3 -B verify.py
python3 -B -O verify.py
sha256sum -c SHA256SUMS
```

Expected status: `ENDPOINT_JOIN_OBSTRUCTION_PASS`. The checker audits exact
constants and versioned source inputs. Geometry and real inequalities remain
written mathematics, not formalized or proved by finite sampling. No solver,
Gaussian integration, large artifact, or new signed parameter cell is involved.
[Sources and review scope](SOURCES.md) distinguish this result from the prior
dominant-atom schedule test.
