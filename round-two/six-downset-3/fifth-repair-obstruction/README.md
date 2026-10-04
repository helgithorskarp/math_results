# An obstruction to the fifth original sparse repair

Actual author: **six-downset-3**, role **researcher**.

For **every integer k>=5**, put q=2k. On the original triangle-majority
downset with k deleted bcx triples, the entire real affine capped Hoffman
face

    C=C0+kappa Delta+t_b R_b+t_c R_c+sigma B+rho T

is empty. Here T joins each outside singleton to the proper nonempty member
bc, with symmetric entry1. The two trades are independent and all five
parameters are unrestricted real numbers. No strict-rank assumption is used.

This enlarges the four-repair obstruction from the credited classification
10222. It rules out this proposed repair mechanism on a complete infinite
family. It makes no assertion of nonexistence for arbitrary or uncapped H,
and no assertion for k2..4. The general spectral conjectures remain open in
the cited primary preprint.

The author proof is ordinary and unformalized; this new leaf is
**independently unreviewed**. Neither a parent's review nor a numerical
search status is its verdict. See [PROOF.md](PROOF.md).

Reproduce the separate exact original-member checker, standard library only:

```sh
python3 -I -B check.py --out work/normal.json
python3 -I -B -O check.py --out work/optimized.json
```

Use CPython3.12.14 or another compatible CPython with exact Fraction
arithmetic. The finite certificate comprises two original member vectors
at each k5..10. The checker compares all seven complete physical forms
against independently counted literal member pairs, checks all six affine
coefficients, and checks the entire uniform degree5 polynomial and its
strict negative translation at11. Generated outputs are untrusted.

The discovery used one bounded NumPy1.24.2 phase-I Newton pilot at k8;
approximate separating vectors were rounded, then constrained to cancel
both trades, sigma and rho exactly. Numerical programs, inverse matrices,
status and approximate eigenvalues are **not proof inputs**. Exact rational
vectors and affine coefficients are fully supplied in CERTIFICATE.json.
The proof checker imports neither NumPy nor those discovery/recovery programs.

The defining literal table is copied whole and hash pinned, with the old
small-domain helper unused. References, original-coordinate interpretation
and ordinary completeness bridges are explicit in PROOF.md. No resources
beyond a single1CPU/2GiB, single-thread child with60-second guard are needed.
