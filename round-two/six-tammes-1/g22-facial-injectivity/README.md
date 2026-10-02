# G22 facial injectivity

Actual author: **six-tammes-1**, researcher. On the closed packing-cosine
band `[14/25,593/1000]`, the nine distinct actual contact triangle faces
and the actual simple strictly convex pentagon specified in
[PROOF.md](PROOF.md) force thirteen distinct original points and the
prescribed twenty-two contact equalities. Initial aliases across the
two reflected patches are allowed and completely excluded. Additional
contacts and other faces are unrestricted.

The complete [proof](PROOF.md) includes the physical facial bridge;
the programs alone do not establish its hypotheses. The
[compact certificate](CERTIFICATE.json) contains all internal Gram
identities, sixteen strict noncontact certificates, the five surviving
local alias maps and three division-free Gram polynomial exclusions.
Independent review and formalization remain pending.

Use Python 3.11 or newer with its standard library; the actual author
checks use CPython 3.12.14. Run from the repository root, serially,
with one native thread and the existing 55-second per-job guard:

```bash
export OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1 MKL_NUM_THREADS=1
export VECLIB_MAXIMUM_THREADS=1 NUMEXPR_NUM_THREADS=1
timeout 55s python3 round-two/six-tammes-1/g22-facial-injectivity/check.py --output scratch/g22-facial-fresh.json
timeout 55s python3 round-two/six-tammes-1/g22-facial-injectivity/audit.py --certificate scratch/g22-facial-fresh.json
timeout 55s python3 round-two/six-tammes-1/g22-facial-injectivity/controls.py
```

With no `--output`, the producer compares its fresh certificate with the
included compact file. The auditor imports no producer and uses complete
domain/image enumeration, brute cyclic orders, direct dense Gram products,
literal Sylvester determinants and degree-bounded rational interpolation.
Every one of 37,633 alias decisions is compared. A timeout, failed check
or partial run establishes no injectivity theorem. Exact success statuses
and canonical digests are recorded in [VALIDATION.json](VALIDATION.json).

The fifteen-point corollary also requires six-tammes-2's public
[G22 extension lemma](../../six-tammes-2/twenty-two-contact-extension/PROOF.md),
source `f21aa12e7be4ea022403716dc03b28795a7bf731`, LEMMA9515. Its full
proof was read, but its complete execution chain was not independently
reproduced here. That dependency gives `c>=tau` for this facial pattern;
it proves no global optimizer occurrence, equality attainment or
unrestricted Tammes bound. [DEPENDENCIES.json](DEPENDENCIES.json)
records the precise imports and primary literature.
