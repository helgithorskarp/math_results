# An explicit all-threshold Gaussian neighborhood certificate

[PROOF.md](PROOF.md) joins R3's polynomial hinge margin, R8's strict peak
bound and the signed cloud tail estimate into an **explicit uniform family
certificate**. Both endpoints can be independently moved and reweighted,
including arbitrary diffuse clouds, throughout a prescribed positive
variance interval. No extra target homothety or covariance floor is needed.

The qualitative ambient openness and the unperturbed norm-preserving class
are already known in the campaign. The new object is their complete
quantitative join, with finite rational guards and no unverified middle
minimum, peak location or missing threshold interval. This does not settle
unrestricted dimension-three Gaussian majorisation.

For anchored rational reference sites, the producer verifies shortness,
equal anchor norms, a support radius, a uniform loss over a whole prior
region, and a signed support-width witness. It produces one perturbation
budget valid for every threshold and variance in the specified interval.
The theorem permits any rigorous width certificate. The current executable
supports the sufficient nested-hull/cap witness described in the proof;
it is not a complete detector for arbitrary finite configurations.

The supplied compact reference is the coordinate fold

```
P=(0,e1,-e1,e2,-e2,e3,-e3),
Q=(0,e1,-e1,e2,-e2,e3,e3).
```

For **every** prior `v_i>=1/16`, all independent clouds and priors with

```
2*cloud_radius + ||u-v||_1 + ||z-v||_1 <= 2^-1966080255
```

satisfy full Gaussian majorisation simultaneously for every `s in [1,4]`.
The interval can be rescaled to any specified positive spatial unit. The
reference retains the source diameter at the target, so it cannot meet a
strict-homothety directional-MGF buffer for these reference endpoints,
even after independent rigid motions. The fold itself is an old positive
example; the certificate covers the entire prior/cloud region, rather
than claiming a new result about that single fold.

The budget is extremely conservative. We store its exponent, never its
billions-of-bits denominator. This is an effective uniform theorem, not
a useful coarse cover of the remaining unrestricted frontier. It gives
no common neighborhood down to zero variance and no new KP consequence.

**Status:** complete author proof awaiting independent review. The
polynomial middle-margin input is also an author result pending review;
the strictness/peak input has independent campaign acceptance. Source
publication and successful exact checks do not constitute peer acceptance.
[SOURCES.md](SOURCES.md) gives attribution and the dependency boundary.

Reproduce with standard-library CPython 3.11 or later:

```sh
python3 -B certificate.py INPUT.json > /tmp/anchored-family-certificate.json
cmp /tmp/anchored-family-certificate.json CERTIFICATE.json
python3 -B verify.py --input INPUT.json --certificate CERTIFICATE.json
python3 -B verify.py > /tmp/anchored-family-check.json
cmp /tmp/anchored-family-check.json EXPECTED.json
python3 -B -O verify.py > /tmp/anchored-family-opt.json
cmp /tmp/anchored-family-opt.json EXPECTED.json
sha256sum -c SHA256SUMS
```

Expected audit status: `EFFECTIVE_ANCHORED_FAMILY_EXACT_CONTROLS_PASS`.
Certificate SHA256:
`9d9a182294760b1122bd2e7d3a3a49fce129d95f1bf5897ccd192ecc479a9f19`.
The [checker](verify.py) imports no producer module. Its supplied-record
mode checks inequalities and allows conservative nonminimal schedules.
The author suite checks 19 damaged records/inputs, eight covariance-loss
controls, four rescaled parameter schedules, independent endpoint
translations, producer-byte reproduction and six source pins.
No Gaussian quadrature or heavy computation is run. The analytic
kernel, peak and tail bridges remain written mathematics.

On the author's CPython 3.11.2 host, the normal and optimized suites took
0.39 and 0.74 seconds; peak child RSS was below 21 MiB. Their identical
record SHA256 is
`76b56fb200a3427e6581a6ee8738d8b79324009b549a8eaaa129121e4f7a352e`.
