# Independent six-order deletion-corridor review

Actual reviewer **six-reviewer-2**, role **independent mathematical reviewer**.
Target LEMMA9478, source ea16136611129587959bd5b9504679a6f984ec88.

[PROOF.md](PROOF.md) confirms the universal all-k exclusion q<=b(k)-6
within the specified capped affine/four-edge ansatz, with the9195
constructive q>=b(k)+1 theorem explicitly imported. It proves a new
infinite Pell family for which ALL SIX corridor orders pass the scalar
four-coordinate necessary test and fail B0>0. Six is therefore sharp
for these two criteria, without certifying actual corridor feasibility.

Reproduce with CPython3.12.14/standard library:

```sh
export OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1 MKL_NUM_THREADS=1
export NUMEXPR_NUM_THREADS=1 VECLIB_MAXIMUM_THREADS=1 BLIS_NUM_THREADS=1
python3 verify.py
python3 -O verify.py
sha256sum -c SHA256SUMS
```

Each command regenerates the ENTIRE35kB own frozen record; explicit
exceptions survive-O. There are13 exact coefficient/sign records,
9604 literal q5/k3 original entries, all ten labeled deletion transports
checking96040 original entries,42 Pell calibration orders and12 damages.
Universal completeness is the ordinary root/sign/Pell proof, not these
finite calibrations. Guards60s internal/90s outer are fixed; no large
matrices are allocated for unbounded parameters.

The unchanged affine.py/linear.py helpers are credited reuse of own
REVIEW9488/source84a7d6ac9bf8e8896fabd51398032a00c4e04a06, ultimately
own9303. Their mathematical table is credited to9145. The prior finite
family guard4<=q<=23 is retained and used only at q5; exact scalar
formulas need no such allocation. New9478 programs/oracles were unread
until the independent proof/code/whole records were sealed. Later
comparison and author replay are corroboration only, documented in
PROVENANCE.json/VALIDATION.json. Ordinary bridges remain unformalized,
and9195 is an imported sufficient tail, not a fresh independent audit.
