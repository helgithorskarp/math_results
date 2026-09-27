# A signed polynomial cone at logarithmic noise

For every bounded probability law in a radius-R ball in R3 and every
1-Lipschitz image, Gaussian variance s>=8k R^2, k>=12, signs **every**
convex polynomial energy through degree 2^(k-4)+1. In particular s>=96R^2
signs the whole cone through degree257. The proof includes a quantitative
margin proportional to mean pair-distance loss, with no lower loss floor.

This is a complete author theorem, pending independent review. It does not
prove the full dimension-three Gaussian-majorisation conjecture. At any fixed
finite variance the signed degree is finite. No new KP conclusion is claimed.

Read [PROOF.md](PROOF.md) for the universal reduction and
[SOURCES.md](SOURCES.md) for attribution and precise review boundaries.
The new step uses Legendre reproduction to pay for the entire potentially
adverse low-density tail, using the accepted loss modulus and the high-noise
window. It is not a collection of numerically positive configurations.

Run with standard-library CPython3.11 or later, from this directory:

```sh
python3 -B verify.py
python3 -B -O verify.py
sha256sum -c SHA256SUMS
python3 -B certificate.py --curvature-degree 255
```

The checker prints `LOGARITHMIC_NOISE_CERTIFICATE_PASS` and a deterministic
record hash. It checks nine exact source pins,1,025 moderate schedules and
seven boundary scales,289 Legendre orthogonality identities,225 reproducing
controls,17 Laplace integral identities and12 rejection controls.
Two actual Gaussian calibrations compare the marginal-moment producer against
19,312 total replica multisets, including a full-rank-six paired configuration
and a prior with tiny positive distance loss. These known-positive controls
validate arithmetic and normalization; they are not new signed examples.

[EXPECTED.json](EXPECTED.json) contains the compact deterministic record.
`verify.py --write-expected` intentionally regenerates it; ordinary checks
compare against it and fail on mismatch. No assertions are used as proof
predicates, and optimized Python performs the same checks.
Author replays on CPython3.11.2 took about4.2--4.4seconds and24MiB peak
resident memory. These costs describe the compact controls, not the large
moment budgets in the theorem.

[certificate.py](certificate.py) emits a compressed uniform theorem schedule.
Its supplied radius is a mathematical premise. It does not test whether an
arbitrary supplied polynomial is convex or a law lies in that ball.
[moments.py](moments.py) validates finite rational3D data, pairwise contraction,
weights and radii, then computes exact marginal Taylor moments and outward
radical intervals. It is consumed by the calibration, with every Taylor error
paid. For diffuse laws, the R3 paired cubature remains an existence theorem;
no rational rounding or computable oracle is presumed.

The uniform Taylor order and atom count in the schedule are conservative
existence budgets. For degree255 they are Q=2112 and25,157,483,649 pairs.
The checker does **not** construct this cubature or expand those moments.
Its Gaussian controls use Q=4 with a separately checked, much smaller actual
remainder. State space is O(Q^4); exact convolution costs and coefficient
growth prevent a claim of practical replay at the very large degrees.

The universal mathematical theorem uses unformalized coarea/Abel and
orthogonal-polynomial facts. Exact finite checks are author validation,
not independent acceptance or a proof-assistant formalization.
