# Gaussian beta-row certificate for all prior weights

At variance one, all six beta tests `b_(5,k)` are nonnegative on the
classical sixteen-label simplex-flap cell with squared distances allowed
to vary by `1/100`, subject to being a contraction in R3. This includes
every probability vector, including zero weights. The cell belongs to
the compact frontier `K_3` after translations.

[PROOF.md](PROOF.md) gives the exact claim and analytic pruning: every
polarized coefficient involving at most six distinct labels is already
nonnegative by a five-dimensional Gaussian product identity. Only 11440
seven-distinct coefficients need enclosure for each test. This is a
finite-row certificate, not full majorisation or a new Kneser--Poulsen
class. Independent review is pending.

From the repository root, run:

```sh
python3 probability/gaussian_beta_weight_certificate/verify.py
```

Python 3.11 or later, standard library only. The checker reproduces all
68640 sign enclosures and compares every field with
[EXPECTED.json](EXPECTED.json). It prints `PASS` and the deterministic
coefficient-stream hash. The full check took 22 seconds and about 22 MiB
of peak memory in the author's environment. Normal CPython 3.11.2 and
optimized CPython 3.12.14 reproduced the same output. No large certificate
is downloaded or saved.

[certificate.py](certificate.py) contains the reusable `Cell` and
`coefficient_bounds` functions. They enclose this beta row for supplied
exact three-dimensional centre configurations and a squared-distance
radius, at variance one. Calling them on other data does not establish
positivity: the user must check all required coefficient lower bounds
and verify the contraction/domain hypotheses in the proof. The built-in
complete certificate is deliberately limited to the stated cell.

The module imports the existing rational-bounds source and reconstructs
the existing flap fixture, checking both hashes first. [INPUTS.json](INPUTS.json)
records provenance. No third-party Python package is needed. The verifier
also checks homogeneous weight normalization with arbitrary rational
kernels, every subtuple exponent by a centroid formula, exact isometry,
direct Fraction interval assembly, and invalid-input rejection.

For researchers 2 and 3: reuse the rank pruning before subdividing weight
domains. On this cell, the six coefficient margins are explicitly in
`EXPECTED.json`, and `b_(5,k)>=L_k*P(seven distinct labels)`. All repeated-label
coefficients are handled uniformly without a weight grid. This is one
signed cell and one beta row, not the high-degree compact-frontier cover.
The existing full-axis degree barrier and all untested signs remain open.
