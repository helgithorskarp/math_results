# Averaging signs the eighth Gaussian beta obligation

For every bounded probability law on R3, every contraction on its support,
and every Gaussian variance s>0, the author proof establishes

    b_(8,0) >= 167 sqrt(2) d_2/4800 >= 0,
    d_2=(2 pi s)^(3/2) integral(g^2-f^2).

The [proof](PROOF.md) fixes the existing beta normalization and derives the
radius-free nonlinear replica inequality `B_4 B_2^2 >= B_3^3`. A quadratic
minorant of one degree-eight scalar polynomial turns that inequality into
the sign. This averages iid replicas under their common law and does not
require positivity for every fixed conditional tuple.

Combined with the accepted seven-factor result, this signs every entry of
row N=8. It does not establish full majorisation, every later beta entry,
zero coupling defect, or a new Kneser--Poulsen volume case. Independent
review of this new result is pending.

Run from this directory with **Python 3.11 or later**, standard library only
(tested with CPython 3.11.2):

```bash
python3 verify.py
python3 -O verify.py
sha256sum -c SHA256SUMS
```

The checker validates all 72 positive rational Bernstein coefficients on
eight intervals covering [0,1], agrees entry by entry with de Casteljau
subdivision, and checks exact variance identities and normalization. It
rejects a perturbed coefficient and an omitted interval. The minimum is
`10434391/18350080000`; the final bound is `167*sqrt(2)*d2/4800`.
`python3 verify.py --emit` reconstructs [EXPECTED.json](EXPECTED.json).
Execution takes well below one second on the development machine.

The universal Jensen and Gaussian-integration steps are written arguments.
The scalar premise is an exact computer-assisted certificate, not a
floating-point experiment. Python integer/Fraction arithmetic remains a
trust boundary; the internal cross-checks are not external peer review or
formalization. There are no external inputs or omitted large artifacts.
[SOURCES.md](SOURCES.md) records attribution and the dependency boundary.
