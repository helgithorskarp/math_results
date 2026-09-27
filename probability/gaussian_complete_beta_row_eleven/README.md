# Complete Gaussian beta rows through N=12

Complete author proof with exact scalar certificates, 27 September 2026.
Independent review and formalization are pending.

For every bounded R3 probability law, every 1-Lipschitz image and every
Gaussian variance, **all beta entries b_(N,j) with N<=12 are nonnegative**.
They are strictly positive whenever a support distance is shortened.
There are no radius, atom-count, mass, covariance or small-loss restrictions.

The original [row-eleven proof](PROOF.md) uses shifted positive moment measures and exact
convex-dual certificates to close the four unresolved entries of row11.
The other eight entries use the credited seven-factor theorem; an exact
degree-elevation identity then gives every lower row. The retained-interaction
inequality is credited prior machinery, not a new claim here.

The [multilevel supplement](MULTILEVEL.md) completes row12 by combining
averaged Young inequalities at several replica counts against a common
positive measure. Its four exact certificates sign j=1,2,3,4; the existing
retained-interaction and seven-factor theorems supply the other positions.
The original row11 source and certificate remain intact.

This advances the complete-row endpoint beyond the accepted N=8 result.
It does not establish all beta rows, full majorisation, unrestricted
Hankel positivity, or a new Kneser--Poulsen class.

From this directory, with standard-library Python 3.11+:

```
python3 verify.py
python3 -O verify.py
python3 multilevel_verify.py
python3 -O multilevel_verify.py
sha256sum -c SHA256SUMS
```

The original runs print `COMPLETE_BETA_ROW_ELEVEN_PASS`, with 2688
positive Bernstein coefficients, 2688 exact polynomial identity controls,
66 degree-elevation controls and 4 rejected corruptions. They reconstruct
[CERTIFICATE.json](CERTIFICATE.json) and compare to
[EXPECTED.json](EXPECTED.json). The finite scalar premises are exact;
the Gaussian and Jensen arguments remain written mathematics. No solver,
floating search, external dataset or omitted certificate is needed.

The supplement prints `MULTILEVEL_COMPLETE_ROW_TWELVE_PASS`, with 13
verified Young inequalities, 3328 positive Bernstein coefficients,
3328 identity controls, 78 degree-elevation controls and 5 rejected
corruptions. Its exact inputs and outputs are
[MULTILEVEL_CERTIFICATE.json](MULTILEVEL_CERTIFICATE.json) and
[MULTILEVEL_EXPECTED.json](MULTILEVEL_EXPECTED.json). It imports the
unchanged polynomial routines from the original checker.

See [SOURCES.md](SOURCES.md) for attribution and dependency boundaries.
