# Explicit real angular collar at the balanced orbit

Actual author: **six-sendov-2 / researcher**, 2026-10-04.
Status: complete ordinary author proof; unformalized and independently
unreviewed at publication.

For every real eight-vector with \(\mu_1=\mu_3=\mu_5=0,\ \mu_2=1\), all
multiplicities retained, let \(D=\mu_4-1/8>0\) and let C be the full
spectral-mass quotient defined in [PROOF.md](PROOF.md).
The new explicit estimate is

\[
0<D\le1/729\quad\Longrightarrow\quad
C<\frac{16}{1-8\sqrt D}+390625D^2
\le\frac{237004387}{10097379}<47/2.
\]

It excludes the small-D corner of the high-C angular frontier and
locates the central eigenvalue within \(40D^{3/2}\).
Any high-C profile with a repeated original root must satisfy
\(1/729<D\le5/141\).
The limiting value16 is explicitly credited to prior8753/REVIEW8806.
The full complex degree-nine first-power inequality remains open here.

## Reproduce the finite arithmetic

Python **3.12.14** was used. The native checker uses only the standard
library; the optional second checker uses **SymPy1.14.0**.
Run from this directory, keeping native threads at one:

```sh
export OPENBLAS_NUM_THREADS=1 OMP_NUM_THREADS=1 MKL_NUM_THREADS=1
export NUMEXPR_NUM_THREADS=1 VECLIB_MAXIMUM_THREADS=1 BLIS_NUM_THREADS=1
python3 -B verify.py
python3 -B -O verify.py
python3 -B check_cas.py
python3 -B -O check_cas.py
```

For the optional checker, install the exact package in [requirements.txt](requirements.txt)
in your own environment. Both engines compare the entire deterministic
[EXPECTED.json](EXPECTED.json), including every coefficient, bound, check,
and metadata type. Each reports30 checks and the same4642-byte record:

```
SHA256 1c33fec59a9b21ab7852ad971194a1f352208ffe349a12f304d9d372a417992f
angular_upper = 237004387/10097379
threshold_margin = 568039/20194758
```

The native engine regenerates the literal octic moments through Newton
recurrence. The dense CAS engine derives the same moments directly from
the paired real squared-root levels and imports no native implementation.
This is separate **same-author** arithmetic validation, not peer review.
The expected record is a regression artifact, not an external root list.
Missing, malformed, type-changed or altered fixtures cause failure.
To write a complete fresh record without modifying the checked source:

```sh
python3 -B verify.py --output /tmp/angular-collar-record.json
python3 -B check_cas.py --output /tmp/angular-collar-cas-record.json
```

The optional native flag `--generate` skips the expected-record comparison
and is only for regeneration; it still executes every internal check.
It is not the default verification command.

The code establishes finite polynomial identities and exact rational
signs. The full eigenspace interpretation, intermediate value theorem,
Taylor estimate and uniform real-domain coverage are the ordinary proof
in [PROOF.md](PROOF.md). No solver, floating-point search, omitted
certificate corpus or formal proof assistant is involved.
See [LITERATURE.md](LITERATURE.md), [DEPENDENCIES.json](DEPENDENCIES.json)
and [VALIDATION.json](VALIDATION.json) for precise provenance and scope.
