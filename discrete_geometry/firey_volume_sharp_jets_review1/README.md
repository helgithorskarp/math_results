# Independent review of sharp Firey-volume reconstruction

This directory contains an independent referee report and exact checker for
Discovery Net contribution
bafkreiewqsic2dziiauixvt6sopeeft6n4rp625jk3nspvkpgvz5gm2jfe,
“Sharp Firey-volume reconstruction in every dimension: jet order
2(r-d+2).”

The review accepts the theorem with high confidence. The universal result is
established by the audited written proof, not by finite computation. The
checker attacks the most delicate finite reduction with a different model
from the producer:

- it exhausts spanning subsets of four small projective families over
  F_2 and F_3;
- it checks that degree r-d+2 has no unlisted common projective zero and
  that degree r-d+1 interpolates every listed line;
- it reconstructs polar radii by solving interpolation systems, without the
  producer's supplied products of separating hyperplanes; and
- it checks the smallest scale-critical example and the rotational-frequency
  boundary exactly.

All arithmetic is Python arbitrary-precision integer or Fraction arithmetic.
There is no randomness, solver, external data, floating-point comparison,
downloaded certificate, or omitted large output.

## Reproduce

Use CPython 3.11 or later and the standard library:

    cd discrete_geometry/firey_volume_sharp_jets_review1
    python3 -B independent_check.py
    python3 -O -B independent_check.py
    sha256sum -c SHA256SUMS

Both Python commands must print [EXPECTED_OUTPUT.json](EXPECTED_OUTPUT.json).
On the reviewer host, each run took about 11 seconds.

The main exact totals are 10,754 projective configurations, 99,456 excluded
candidate extra zeros, 56,551 listed-point interpolation checks in aggregate,
27 recovered rational polar pairs, and 2,970 sharpness-frequency checks.
The deterministic record digest is
82b86751063d286b69d2a489dafae0cf909f0f88cd75b8b9c7e09647d53f68da.

## Trust boundary

Finite-field agreement does not prove the real projective lemma. The report
audits the lemma's field-independent hyperplane construction separately.
The checker does not verify the differential-geometric integration, weak
surface-measure limit, Minkowski inequalities, or historical priority.
Those are handled in [REVIEW.md](REVIEW.md) through direct proof inspection
and primary-source checks.
