# Phase-ten gap-two successor lemma

Agent six-vdw-2, researcher. Read PROOF.md for the exact quantified claim:
with ten occurrences of a selected phase value and no selected adjacency,
every gap two is followed by two or three. The endpoints10/34 remain open.

Tested native environment: Python3.11.2, python-sat1.8.dev24 (CaDiCaL195),
six1.17.0. All jobs are serial; solver/BLAS/OpenMP threads are one.
The original full fourteen-model definition audits also ran on Python3.12.14.
Use a full main clone of https://github.com/helgithorskarp/math_results:

```bash
python3 -m venv /tmp/vdw-turn-env
/tmp/vdw-turn-env/bin/python -m pip install python-sat==1.8.dev24 six==1.17.0
curl -fL https://raw.githubusercontent.com/marijnheule/drat-trim/2e3b2dc0ecf938addbd779d42877b6ed69d9a985/drat-trim.c -o /tmp/drat-trim.c
sha256sum /tmp/drat-trim.c
cc -O2 -DNDEBUG /tmp/drat-trim.c -o /tmp/drat-trim
/tmp/vdw-turn-env/bin/python round-two/six-vdw-2/order7-phase-ten-gap-successors/reproduce.py --work /tmp/vdw-turn-run --converter /tmp/drat-trim
/tmp/vdw-turn-env/bin/python round-two/six-vdw-2/order7-phase-ten-gap-successors/guards.py --checked-work /tmp/vdw-turn-run --work /tmp/vdw-turn-damage
```

Converter source SHA256:
`d834b649f437e091597f5347f259b9f681087f89ca0844d0cee250a1a1a0c2ee`.
The runner verifies this pin before use. The virtual environment path must
be preserved; resolving its Python symlink can select an environment
without python-sat.

The ten canonical cases have326..366 variables. Successful output is
`EXACT_H7_PHASE10_GAP_SUCCESSOR_LEMMA`, ten exact refutations,174147
additions and2968781 hints PER replay mode. Each proof is checked normally
and with -O; EXPECTED.csv pins CNF/proof hashes and expected counts.
`all_proof_bytes_reproduced` reports byte identity separately from strict
mathematical verification. A different valid strict proof is still a
certificate; a different canonical CNF is rejected.

The serial limits are native50000 conflicts/30s, converter25 internal/30s
external, strict checker30s per mode, definitions55s per stage, phase
coverage30s. UNKNOWN, timeout, unchecked FALSE or partial coverage never
produces the success status. --resume replays only previously checked
positive certificates and refuses to retry an identical bounded failure.

For an untrusted local candidate cache containing `head/STEM.cnf` and
`head/STEM.lrat`, add `--certificate-cache /path/to/cache`. A fresh model
directory is still generated, full actual-field audits still run in both
modes, and all ten proofs still undergo strict replay. The completed
compact-source check used this cache path after stopping the unresolved
search case; it did not rerun a failed native solver model.

The independent field/counter auditor reconstructs all375760 actual APs
and complete clause multisets. coverage.py additionally proves the rooted
phase-input count178983 by transfer DP and a different zero-run formula,
with literal tiny-cycle controls. These are phase profiles, not field
colorings or rotation-orbit counts. Forty-four lower orientation variables
are retained per admitted phase input, along with the global-color unit.

Generated CNFs, DRAT/LRAT certificates, cache candidates and verbose logs
belong in the separate work directory. They are not publication artifacts.
Only this compact source, EXPECTED.csv and verification summary belong
in Git. VALIDATION.md records finished checks and operational limits.
