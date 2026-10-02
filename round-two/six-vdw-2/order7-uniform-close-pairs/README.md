# H7/F617: uniform close phase pairs

Author: six-vdw-2, researcher. Exact restricted lemma: any phase value occurring at least ten times has a cyclic pair at distance one or two. With the published phase band10..34, BOTH phase values have such pairs. Four normalized construction cases retain41/39 free phase bits and all44 lower color orientations. See PROOF.md. No interval3704 witness or unrestricted W(2,7) bound.

Tested with Python3.11.2, python-sat1.8.dev24 (CaDiCaL195), six1.17.0. All jobs are serial, threads1. From a fresh full clone of https://github.com/helgithorskarp/math_results on main:

```sh
python3 -m venv /tmp/vdw-close-env
/tmp/vdw-close-env/bin/python -m pip install python-sat==1.8.dev24 six==1.17.0
curl -L https://raw.githubusercontent.com/marijnheule/drat-trim/2e3b2dc0ecf938addbd779d42877b6ed69d9a985/drat-trim.c -o /tmp/drat-trim.c
sha256sum /tmp/drat-trim.c
cc -O2 /tmp/drat-trim.c -o /tmp/drat-trim
/tmp/vdw-close-env/bin/python round-two/six-vdw-2/order7-uniform-close-pairs/reproduce.py --work /tmp/vdw-close-run --converter /tmp/drat-trim
/tmp/vdw-close-env/bin/python round-two/six-vdw-2/order7-uniform-close-pairs/guards.py --checked-work /tmp/vdw-close-run --work /tmp/vdw-close-damage
```

Converter C source SHA256 must be d834b649f437e091597f5347f259b9f681087f89ca0844d0cee250a1a1a0c2ee before compilation. The driver checks it. The interpreter path must preserve its virtual environment; do not resolve its symlink to a system Python.

Expected complete status EXACT_H7_UNIFORM_CLOSE_PAIR_LEMMA: four audited CNFs, four strict RUP certificates normally and under -O,93635 additions/1744307 hints per mode for the pinned proposer run. The fixture records hashes and counts; a fresh valid proof may use other bytes/counts and is accepted only through exact replay. Native budget50000 conflicts/30s, converter25s internal/30s external, strict replay30s/mode, semantic audit55s/stage. Never enlarge these caps or repeat an identical UNKNOWN model. Incomplete/UNKNOWN/timeout status proves no exclusion; retain the generated work.

Large proof corpora, raw CNFs, binaries and environments are omitted from Git. An optional --certificate-cache DIRECTORY supplies candidate CNF/LRAT files under close/; their canonical hashes are checked and proofs are independently replayed, without trusting producer status flags. Explicit --resume replays already checked positives; it rejects identical UNKNOWN/timeout retries. The old constant-phase classification and phase band9187 are declared mathematical inputs, with their proof text pinned. Normalization controls use tiny cycles5..12; the general44-cycle argument is in PROOF.md.
