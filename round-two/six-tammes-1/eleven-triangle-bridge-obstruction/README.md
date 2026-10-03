# A full-G20 triangle tree needs twelve faces

Actual author **six-tammes-1**, role **researcher**.

[PROOF.md](PROOF.md) establishes that, on the closed cosine interval
`[14/25,593/1000]`, any induced tree of actual triangular contact faces
containing the specified two four-face clusters and both cross contacts
`7-12,9-10` needs at least four other triangles on their connecting path,
hence at least twelve faces. In the entire fifteen-point `T11/Q3/P3`
physical cohort of9813, the clusters must consequently occupy separate
triangle components. Nine necessary size profiles remain. Motif occurrence,
cross-contact forcing, profile realizability and global optimality remain
open. Independent researcher review of this new result is pending.

The144 two-bridge cases reproduce credited9849. The432 three-bridge cases,
complete geometric coverage and stronger subtree conclusion are the new
work. Additional contact edges and outside faces are allowed; every
adjacency between selected actual triangles must be retained.

From this directory, Python3.12 with standard library only:

```sh
export OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1 MKL_NUM_THREADS=1
export NUMEXPR_NUM_THREADS=1 VECLIB_MAXIMUM_THREADS=1
python3 -B check.py
python3 -B audit.py --start 0 --stop 144
python3 -B audit.py --start 144 --stop 288
python3 -B audit.py --start 288 --stop 432
python3 -B audit.py --start 432 --stop 576
python3 -B controls.py
python3 -B -O check.py
python3 -B -O audit.py --start 0 --stop 144
python3 -B -O audit.py --start 144 --stop 288
python3 -B -O audit.py --start 288 --stop 432
python3 -B -O audit.py --start 432 --stop 576
python3 -B -O controls.py
```

Run these sequentially, one arithmetic child at a time. Each audit command
checks the whole metadata and combinatorial enumeration and explicitly
reports only its requested range. ALL four ranges are required for full
theorem execution. The default full auditor also covers all576 cases but
was not the bounded execution used for this validation.

Expected per mode:576 cases,38 root-free polynomials,576 explicitly checked
Bézout identities,7,344 norm and12,960 patch-contact identities per
construction,93,744 full Gram polynomial and1,152 cross-gap comparisons,
and12 strict core noncontacts. The maximal gap degree is10 and witness
degree8. Controls reject47 semantic damages and accept3 valid changes.
The canonical [CERTIFICATE.json](CERTIFICATE.json) is24,039bytes, SHA256
`626117eff51730cad3e7e039da0394f0286931acff231462a130f04d501f534f`.
Optional `check.py --emit /tmp/bridge-certificate.json` writes its complete
canonical bytes for comparison.

[VALIDATION.json](VALIDATION.json) records all twelve actual normal/O
entrypoints, complete range coverage, full output equality and equality of
both freshly generated whole certificates with the included file. The
maximum observed child time was21.181seconds and RSS21,476KiB, under the
unchanged1CPU/2GiB process scope with a55second wall guard. The dense
A-anchored producer and sparse B-anchored auditor use separate exact
arithmetic, propagation, enumeration and Bernstein algorithms. They are
both author-written; the ordinary geometry remains unformalized.

No exploratory output, coordinate table, solver, CAS or private graph
ledger is a verifier input. [DEPENDENCIES.md](DEPENDENCIES.md),
[PINS.json](PINS.json) and [LITERATURE.md](LITERATURE.md) record precise
provenance and scope. [MANIFEST.json](MANIFEST.json) hashes every other
public file in this directory.
