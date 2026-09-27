# Exponential localization of small-noise adverse Gaussian hinges

Complete analytic author proof, 27 September 2026. Independent review and
formalization are pending.

For **every finite contraction with distinct targets**, put

    d = minimum distance between two target sites,
    p = minimum positive probability weight,
    C_s=(2 pi s)^(-3/2),
    H(u)=integral(g-C_s u)_+ - integral(f-C_s u)_+.

The [proof](PROOF.md) establishes

    d^2/s >= 65536+8 log(1/p)
       ==> H(u)>=0 for every u>=exp[-d^2/(512s)].

No source-radius bound, strictly shortened nearest pair, or positive loss
floor is required. Tight pairs are allowed. At nonisometric inputs the sign
is strict whenever the threshold is below the target peak.

Thus any adverse hinge in this small-noise regime must occur at an
exponentially low normalized threshold. In particular, every fixed positive
normalized threshold interval is eventually signed for each fixed input.
This controls actual hinges with no polynomial-degree parameter.

The method extends the quadratic-normal-form and spherical-comparison
argument of the [universal peak window](../gaussian_universal_peak_window/PROOF.md)
to all separated mixture components. It controls each marked-pair level
density, even when the marked centers are far outside the component under
consideration, then uses a local Abel inversion.

The full dimension-three Gaussian-majorisation question remains open.
Target collisions are outside this theorem; exponentially low thresholds
remain unresolved. No new Kneser--Poulsen volume comparison or historical
priority is claimed. The existing accepted
[finite-degree small-noise theorem](../gaussian_atomic_low_noise_exclusion/PROOF.md)
also handles collisions and remains a separate result.

Run the compact exact audit from the repository root, with Python 3.11 or
later and its standard library:

    python3 -B probability/gaussian_separated_hinge_window/audit.py
    python3 -B -O probability/gaussian_separated_hinge_window/audit.py

The expected final marker is SEPARATED_HINGE_WINDOW_AUDIT_PASS.
The audit checks rational constants, exact geometry and sufficient schedules,
including a seven-site input of paired affine rank six. It does not evaluate
Gaussian integrals, replay the analytic proof, or independently review it.

The same file accepts an optional JSON path. Required keys are source,
target, weights, variance, and log_threshold. Coordinates and scalars must
be integers or exact rational strings. The threshold is u=exp(-log_threshold).
The producer checks the stronger rational guard

    d^2/s >= 65536+8b,  where every weight is at least 2^(-b).

It returns NONNEGATIVE, EQUALITY, or NOT_COVERED. The last status is not a
negative hinge. Invalid input raises an error. See the two-site example
inside the audit for a complete input format.
