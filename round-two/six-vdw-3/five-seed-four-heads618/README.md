# Matched mono-five three-satellite rule in partial XOR618

six-vdw-3, researcher. Under regular cyclic AP7 avoidance, holes{5,53,101}
and a mono-five orientation seed0..4 of color b force an opposite bit at
one of52,54,55, in addition to the earlier forced endpoint102.
[PROOF.md](PROOF.md) states the complete conditional result and two
harmonic-hole corollaries. Four new exact heads, justified by four literal
integer APs, are strictly refuted. Unspecified orientations remain free.
The3704 coloring and unrestricted W(2,7) frontier remain open.

The pipeline needs Python3.11.2, a C compiler and access to byte-pinned
public dependencies. From this directory:

```sh
python3.11 -m venv build/venv
build/venv/bin/pip install python-sat==1.8.dev24 six==1.17.0
OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1 MKL_NUM_THREADS=1 BLIS_NUM_THREADS=1 NUMEXPR_NUM_THREADS=1 build/venv/bin/python reproduce.py --work build/reproduce
```

The default command downloads seven credited source files, checks their
exact byte pins, compiles an untrusted converter and rebuilds all artifacts
under `--work`. Both Python modes audit the complete four-head cover,
1236 CRT identities, all381306 actual cyclic start/step pairs for the
common base, all20480 signed-unit inputs, small positive controls and
damaged models/sources. It then makes four fresh CaDiCaL195 proposals and
strictly checks all four positive-RUP LRAT candidates in both modes.

Expected final status:
`MATCHED_FIVE_SEED_THREE_SATELLITE_RULE_AUTHOR_CHECKED`, with97664 additions
and2486245 propagation hints per mode. All CPU work is serial and threads
one. Native proposals retain the100000-conflict/35-second guard;
conversion retains25s internal/30s external; strict replay retains50s per
child. UNKNOWN, timeout or an incomplete certificate aborts without retry
or an exclusion claim. Generated proof traces and environments are ignored.

For resumable validation `--resume-dir DIR` takes private `case-1.lrat`
through `case-4.lrat` candidates. Every candidate is untrusted: the complete
source audits and both strict replays still run. `--fresh-case N`, with
`--resume-dir`, replaces the selected cached candidate by a fresh proposal.
`--tools DIR` reuses fetched sources with all pins checked again; a reused
converter executable remains untrusted. No proof corpus is supplied in Git.

[expected.json](expected.json) freezes model/proof hashes and exact counts.
[cover.json](cover.json) records the four-AP cover, ordinary premise bridge
and two harmonic transports. The downloaded9311/9402 written mathematical
dependencies are not reproved by this restart. The ordinary bridges are
not formalized, and no external independent-review verdict is claimed.
[VALIDATION.md](VALIDATION.md) and [verification.json](verification.json)
describe the completed author reconstruction.
