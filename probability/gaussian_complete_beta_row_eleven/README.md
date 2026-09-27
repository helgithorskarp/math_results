# Complete Gaussian beta row N=11

Complete author proof with exact scalar certificates, 27 September 2026.
Independent review and formalization are pending.

For every bounded R3 probability law, every 1-Lipschitz image and every
Gaussian variance, **all beta entries b_(N,j) with N<=11 are nonnegative**.
They are strictly positive whenever a support distance is shortened.
There are no radius, atom-count, mass, covariance or small-loss restrictions.

The [proof](PROOF.md) uses shifted positive moment measures and exact
convex-dual certificates to close the four unresolved entries of row11.
The other eight entries use the credited seven-factor theorem; an exact
degree-elevation identity then gives every lower row. The retained-interaction
inequality is credited prior machinery, not a new claim here.

This advances the complete-row endpoint beyond the accepted N=8 result.
It does not establish all beta rows, full majorisation, unrestricted
Hankel positivity, or a new Kneser--Poulsen class.

From this directory, with standard-library Python 3.11+:

```
python3 verify.py
python3 -O verify.py
sha256sum -c SHA256SUMS
```

Both Python runs must print `COMPLETE_BETA_ROW_ELEVEN_PASS`, with 2688
positive Bernstein coefficients, 2688 exact polynomial identity controls,
66 degree-elevation controls and 4 rejected corruptions. They reconstruct
[CERTIFICATE.json](CERTIFICATE.json) and compare to
[EXPECTED.json](EXPECTED.json). The finite scalar premises are exact;
the Gaussian and Jensen arguments remain written mathematics. No solver,
floating search, external dataset or omitted certificate is needed.

See [SOURCES.md](SOURCES.md) for attribution and dependency boundaries.
