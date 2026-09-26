# Six beta columns signed for every Gaussian contraction

For every bounded probability law in R3, every 1-Lipschitz image and every
Gaussian variance, the [author proof](PROOF.md) establishes

    sum_(l=0)^r (-1)^l binom(r,l) a_(k+l) >= 0
                       for every k>=0 and 0<=r<=5,

where a_j is the normalized Gaussian moment gap in the existing global
criterion. All these signs are strict whenever the expected squared
pair-distance loss is positive.

Equivalently, the six rightmost entries of **every** beta row are
nonnegative, before or after averaging the prior weights. The entire
fifth row is therefore positive for nonisometric pairs, without a
support, weight, metric-cell or variance restriction. The projection
identity extends researcher 8's positive-product calculation: center
the positive Gaussian factors at their centroid and project onto the
span of the at most five remaining centers. The lost Gaussian energy
is independent of the alternating subset and contributes a positive factor.

For the compact-frontier consumer, skip these six columns at every
degree. A negative beta certificate must have at least six factors of
1-u. This does not rule out a seven-atom counterexample, sign the other
columns, or prove all convex polynomial comparisons. **The full question
remains open; no new Kneser--Poulsen consequence is claimed.** Independent
mathematical and historical-priority review are pending.

Run from this directory with standard-library CPython 3.11 or later:

```sh
python3 audit.py --check
python3 -O audit.py --check
sha256sum -c SHA256SUMS
```

The deterministic output is `GAUSSIAN_BETA_PROJECTION_EXACT_AUDIT_PASS`
followed by the SHA256 of the canonical [expected record](EXPECTED.json).
With CPython 3.11.2, both modes produce

```text
3239be5d96ed4c74be4d9a51e953e2a4c2c6c28375df4f4dd8178c930afe2865
```

One run takes about four seconds on the author's host. The record contains
267 projection subset checks, 364 product checks, 12 exchangeability
checks, five coupled-replica checks, 969 coefficient identities and four
rejected corruptions or out-of-scope inputs. It includes an actual
seven-site contraction with paired rank six at the interior lift time.
The audit checks exact projection and multiplicity identities; it performs
no floating-point sign test, quadrature or exhaustive Gaussian search.
Its finite controls supplement the written proof and do not constitute
independent review or formalization. [SOURCES.md](SOURCES.md) records the
dependencies and the relationship to the existing cell certificate.
