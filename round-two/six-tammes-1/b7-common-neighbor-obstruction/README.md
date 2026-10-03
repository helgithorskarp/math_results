# B7 pairs without any common unit c-neighbor

Actual author **six-tammes-1**, role **researcher**, 2026-10-03.
Six explicit nine-point B7 contact cores admit no unit common neighbor
for a specified pair throughout CLOSED J=[7/13,3/5]. This excludes nine
previously surviving15-point A4/B7 masks. Under ALL imported physical
hypotheses,15 closed-band/14 strict-improvement necessary maps remain.
The [ordinary proof](PROOF.md) gives every mask and the exact argument.
No global Tammes15 bound or remaining-map realization is asserted.
Independent review and formalization of the new lemma are pending.

Run from this directory using standard-library Python; actual validation
used CPython3.12.14. No external package or remote runtime input is needed.

```sh
OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1 MKL_NUM_THREADS=1 NUMEXPR_NUM_THREADS=1 python3 -B check.py --certificate CERTIFICATE.json
OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1 MKL_NUM_THREADS=1 NUMEXPR_NUM_THREADS=1 python3 -B audit.py
OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1 MKL_NUM_THREADS=1 NUMEXPR_NUM_THREADS=1 python3 -B controls.py
```

Repeat each with `python3 -B -O`. Each producer/auditor prints the same
complete status,6 cases,9 excluded masks,15/14 residual counts and canonical
certificate SHA256
`84667b20ec5ff4b77ace9b878dca03bc5ab7d44c4bbed53cc41766b3b22a5022`.
To regenerate the complete5223-byte certificate, use
`python3 -B check.py --emit /tmp/b7-common-neighbor-certificate.json`.
Controls print [CONTROLS.json](CONTROLS.json):9 arithmetic/boundary obligations,
15 damaged records rejected by BOTH FULL geometric rebuilds,2 valid JSON
presentations and a valid zero-gap common-neighbor example retained.

[check.py](check.py) uses forward reflection/dense fractions/Bernstein.
[audit.py](audit.py) imports neither it nor the dense ring; it uses reverse
leaf peeling/sparse fractions/metric matrix multiplication, an independent
closed derivative bound and a complete Bernstein basis identity.
Both check every coefficient, contact and case mapping in the WHOLE
[certificate](CERTIFICATE.json). They are two SAME-AUTHOR algorithms,
not independent mathematical review. Prior external theorem inputs and
unformalized scope bridges are explicit in [DEPENDENCIES.md](DEPENDENCIES.md).

The entire [PARENT.json](PARENT.json) is the frozen43286-byte9972 finite case
certificate. The entire [PREVIOUS.json](PREVIOUS.json) is the frozen26295-byte
10068 residual certificate. Only their finite cover correspondence is
rechecked here; no new audit of the old29 exclusions is claimed. The new
six common-neighbor obstructions are fully rebuilt by both programs.
[PINS.json](PINS.json) credits source and separates logical imports from
review/context. [LITERATURE.md](LITERATURE.md) records fresh primary status.
[MANIFEST.json](MANIFEST.json) binds the compact source and inputs.

[VALIDATION.json](VALIDATION.json) records all six actual serial normal/O
runs, whole paired outputs and resources. Maximum final child2.924336s,
peak21488KiB, native threads1, unchanged1CPU/2GiB and55-second guard.
A separate private map36 generalized-anchor/resultant pilot reached that
guard and was paused; it is NOT evidence or a certificate input. Three
private one-conjugate Gram cuts are incomplete mask exclusions. No resource
settings were increased. The remaining14 full masks, other profiles and
global occurrence are the substantive next frontier.
