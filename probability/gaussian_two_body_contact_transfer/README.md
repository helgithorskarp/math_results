# Two-body level contacts can certify Gaussian counterexamples

For a contraction that acts by an isometry on each of two convex bodies,
the following three *universal assertions* are equivalent:

1. Gaussian majorisation for every law on the two bodies and every variance.
2. The union-volume Kneser--Poulsen inequality for every finite selection
   of centres in the bodies and arbitrary individual ball radii.
3. Nondecrease of the volume of the intersection of two Gaussian-mixture
   superlevel sets, one mixture on each body. The two mixtures may have
   **different Gaussian variances**.

[PROOF.md](PROOF.md) proves this equivalence and gives a quantitative
conversion from a strictly negative joint-level contact to a finite
Gaussian hinge counterexample. This makes an adverse joint-level contact
a sufficient counterexample certificate for the full shared question,
after changing the finite measure, weights, and variance. It need not be
a negative hinge for the original two mixtures.

The unrestricted R3 question is **open**. No adverse contact, ball-volume
violation, or Gaussian counterexample is supplied here. This is an author
proof of a conditional transfer and a necessary positive obligation;
independent review is pending. The equivalence does not prove any of its
three assertions. Convexifying each rigid component is essential to the
fixed-domain statement. Testing only the original centres is insufficient.

The Gaussian ball-envelope representation is classical; in particular see
Carlsson--Carlsson, *Alpha shapes in kernel density estimation*, Theorem 1.
The Gaussian-to-ball direction is Aishwarya--Li, Theorem 5.1. The contribution
is their two-body converse/equivalence, the unequal-variance contact
criterion, and an explicit finite witness conversion. Priority for that
combination is unassessed; [SOURCES.md](SOURCES.md) records the attribution.

Run with Python 3.11 or later and no dependencies:

```sh
python3 -B verify.py
python3 -B -O verify.py
sha256sum -c SHA256SUMS
```

Both runs reproduce [EXPECTED.json](EXPECTED.json), with status
`TWO_BODY_CONTACT_TRANSFER_CONTROLS_PASS`. Exact arithmetic checks the
barycentric distance identities, rigidity of one asymmetric rank-six
control, simplex rounding, and the conditional Gaussian tail budget.
It does **not** certify a joint-level volume, ball-union volume, or the
analytic proof. No numerical search output or large certificate is needed.

The [handoff](HANDOFF.md) specifies the single missing adverse-volume
certificate. It also explains why the terminal small-variance conversion
is not another fixed-prior low-noise exclusion: its exponential weights
are selected from a pre-existing certified geometric violation.
