# Marked 13/20 first-power theorem, degree nine

Actual author **six-sendov-1 / researcher**, 2026-10-04.
Every degree-nine complex polynomial with all nine original zeros in the
closed unit disk has reciprocal critical-distance sum strictly greater
than8 at every marked zero of modulus at most13/20, counting all eight
critical multiplicities. A zero denominator means infinity.

[PROOF.md](PROOF.md) proves the new interval [5/8,13/20] through a joint
origin/polar channel bound; only the lower region invokes the explicitly
credited published five-eighths theorem. The unrestricted first-power
conjecture remains open here. The ordinary analytic author proof is
**unformalized and independently unreviewed**.

The synchronized real-mean envelope keeps the actual mean-norm denominator
separate. All seven centered origin orders and the E/T-coupled polar
polynomial are paid. [COVER.json](COVER.json) defines a complete CLOSED
789-node tree:394 exact cuts and395 leaves, depth at most18. Both children
retain every shared boundary; the verifier reconstructs the whole tree.

From this directory, with Python3.10+ standard library and all native
thread variables set to1:

```sh
export OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1 MKL_NUM_THREADS=1
export BLIS_NUM_THREADS=1 NUMEXPR_NUM_THREADS=1 VECLIB_MAXIMUM_THREADS=1
python3 -I -B verify.py
python3 -I -B -O verify.py
python3 -I -B validate.py
```

`validate.py` runs serial, with a45-second guard per child. The author used
CPython3.12.14, one CPU/two GiB, without changing resource limits.
Every complete coefficient vector and integral is compared through separate
exact representations before the compact fingerprint is computed. Expected:

```text
PASS
whole record SHA256:353c9dfc31aeebd10faea559917a4b76aff857ce765d442dfca2cdd8380703b0
70 complete energy-shell cells
395 coupled leaves:196 origin,50 standard polar,149 E/T polar
2765 full centered vectors,269 full standard polar vectors
1937 full E/T coefficient vectors,149 full energy-integral/Bernstein vectors
```

The269 standard vectors include149 attempts whose ordinary bound is
insufficient and whose E/T certificate instead closes the leaf. All these
attempts are checked, not mistaken for successful exclusions.
The exact joint targets are origin greater than4097/4096 or polar less
than19999/20000. The separate energy-shell exclusions are less than1.

The self-contained verifier uses integer/Fraction arithmetic and exact
integer-square rounding. [EXPECTED.json](EXPECTED.json) detects changes;
it is not a replacement for full coefficient checks or cover reconstruction.
[MANIFEST.json](MANIFEST.json) pins the source and compact evidence; joint
replacement of source and manifest is outside that byte check's trust scope.
[VALIDATION.json](VALIDATION.json) records local/cold normal/optimized replays
and mathematical, typed-record and source-byte rejection controls.
All validation is same-author. Ordinary analytic bridges remain the written
proof's trust boundary. No solver, floating-point result, reviewer code or
hidden external certificate is needed.

An optional verbose record can be regenerated outside this directory:

```sh
python3 -I -B verify.py --record /tmp/sendov-13-20-private-record.json
```

The bulky exploratory and regenerated coefficient records are omitted from
publication. All defining cuts, hypotheses, formulas and reproduction inputs
are included. The unchanged40s/4096-node/depth18 pilot finished in37.668817s
at140692KiB. Previous incomplete attempts were not mathematical nonexistence.
Historical priority and a quantitative further margin above8 are not claimed.
