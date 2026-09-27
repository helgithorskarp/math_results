# Polynomial Gaussian hinge margins

For every bounded norm-preserving contraction in R3, the
[author proof](PROOF.md) gives the whole-curve lower bound

    H(u) >= d 2^-(40R²+9R+38) u³ (m-u)_+^8.

Here H is the favorable normalized hinge gap, d is the ordered mean
squared-distance loss divided by the Gaussian variance, m is the normalized
target peak, and R>=1 bounds the anchored radius in noise units.
The coefficient is uniform in the law, atom count, covariance and loss.

The new cutoff uses Gaussian tail decay in R8's positive radial-crossing
argument. It changes the supplied middle-margin exponent from exponential
to linear in the threshold bit depth. This is a quantitative refinement
of an existing positive class, not a new class or the unrestricted theorem.

[Proof Sections 4--5](PROOF.md) provide positive rational beta margins and
precise interfaces to the reviewed paired cubature and prior finite sign tests.
At R=1 on 1/8<=u<=m-1/4, the certified margin improves from d*2^-723
to d*2^-112. With the separately verified high-noise modulus K<=2^20,
the compressed sufficient degree N+2=2^533 replaces2^2977. These remain
enormous degrees; no practical global enumeration is claimed.

From this directory with standard-library CPython3.11 or later:

```sh
python3 -B verify.py
python3 -B -O verify.py
python3 -B verify.py --input INPUT.json --row 8
sha256sum -c SHA256SUMS
```

Expected status: POLYNOMIAL_HINGE_MARGIN_CONTROLS_PASS.
[EXPECTED.json](EXPECTED.json) records364 exact beta-integral comparisons,
205 square controls, independent-frame/variance scaling, small and zero
loss controls,11 rejections, and the conditional budgets.
[INPUT.json](INPUT.json) reuses R8's seven-site fold solely as a calibration.
Its half-scale version satisfies the radius guard for the displayed
loss-independent degree. The original fixture does not satisfy that guard;
the output distinguishes this explicitly.

The checker tests rational finite hypotheses, not Gaussian integrals.
UNRESOLVED is a failed sufficient geometric guard, not a counterexample.
Floats and malformed inputs raise an error. To check a saved input-mode
record, add --verify RECORD.json. Supplied-input mode is self-contained;
the complete audit also checks nine adjacent public source byte pins.
It runs in under one second on the author's CPython3.11.2 host.

The analytic proof is unformalized and awaits independent review. Its
positive spherical identity is reviewed prior work; the radial crossing is
credited to R8's now independently accepted strictness proof. No all-radius loss-normalized
modulus, new endpoint transfer, KP limit or improvement of the unrestricted
7/50 defect bound is asserted. [SOURCES.md](SOURCES.md) records attribution.

Expected-record SHA256: c67106bf21733748ad7f9f1be1f9018789dbf298024bbcdd4bd8db75d2469bac.
