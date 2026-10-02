# Matched six-seed exclusion in partial XOR618/F103 colorings

six-vdw-3, researcher. With holes `{6,54,102}` and wholly regular cyclic
seven-APs mixed, the orientation seed `0..5` must be mixed.
[PROOF.md](PROOF.md) gives the full conditional statement and endpoint
corollary: for holes `{0,1,2}`, monochromatic adjacent five-seeds in
`15,30,45,60,75,90` force the other endpoint opposite. Nineteen strictly
refuted classes cover all34 necessary local inputs after the cited9311/9359
premises. Every model leaves88 other orientation bits free. This does not
produce a3704 coloring or improve the symmetric two-color/seven-term W bound.

The standalone pipeline requires Python3.11.2, a C compiler and access to
byte-pinned public dependencies. From this directory:

```sh
python3.11 -m venv build/venv
build/venv/bin/pip install python-sat==1.8.dev24 six==1.17.0
OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1 MKL_NUM_THREADS=1 BLIS_NUM_THREADS=1 NUMEXPR_NUM_THREADS=1 build/venv/bin/python reproduce.py --work build/reproduce
```

This downloads seven credited source files, checks their exact byte pins,
compiles the untrusted converter and rebuilds all artifacts under `--work`.
Both normal and optimized child processes reconstruct the64-input cover,
all19 models, the actual-cyclic relation,38912 literal signed-unit inputs,
complete small controls and damaged-source guards. The default command
then makes19 fresh CaDiCaL195 proposals and checks all19 LRAT candidates
strictly in both Python modes. It writes incremental `progress.json` and a
completed `verification.json`. Expected final status:
`MATCHED_SIX_SEED_EXCLUSION_AUTHOR_CHECKED`;606173 additions/16178753 hints
per mode. All CPU work is serial, threads one, with unchanged native
100000-conflict/35-second, converter25s internal/30s external and strict
replay50s per child guards. An incomplete proposal aborts without retry
or an exclusion claim.

For resumable validation use `--resume-dir DIR`, where DIR has private
`case-1.lrat` through `case-19.lrat`. Every candidate remains untrusted:
all source audits and both strict replays still run. No proof corpus is
supplied in Git. `--fresh-case 19` with `--resume-dir` freshly regenerates
that case while checking the other18 cached candidates. `--tools DIR`
reuses downloads, checking all source byte pins again; a reused converter
executable remains untrusted. A missing candidate aborts.

[expected.json](expected.json) freezes all model/proof hashes, exact counts
and imported provenance. [cover.json](cover.json) records every raw orbit
member. [VALIDATION.md](VALIDATION.md) and [verification.json](verification.json)
describe the completed author source reconstruction. The explicit written
9311/9359 mathematical premises and ordinary bridges are not reproved or
formalized by this pipeline. No external independent verdict is claimed.
