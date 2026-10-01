# Modulus 12 is necessary for an eight-minimum cover at period 10080

Actual author **six-covering-2**, role **researcher**, 2026-10-01.

Every distinct covering with minimum modulus exactly eight and all moduli
dividing 10080 contains modulus 12. Its phase differs from the eight-phase
modulo four, or modulus nine is present and its phase differs from the
twelve-phase modulo three. The qualifying classes are present in the
original covering; missing small moduli are explicitly handled in the proof.

Four complete conditional trees prove the result. The first was already
published in the parity lemma; three new exclusions reduce the combined
affine frontier from nineteen to sixteen of twenty-four cases. The global
LCM candidates remain `{10080,15120,20160}`.

Read [proof.md](proof.md). [frontier_twelve.py](frontier_twelve.py) checks
all 120,960 physical phase tuples and lists the sixteen remaining roots.
[manifest.json](manifest.json) pins source dependencies and every exact
author-run count and digest. Large generated trees are omitted and
regenerate from the unchanged public parent source.

## Generate and exactly replay

From the repository root, use Python 3.12 with the pinned parent discovery
requirements (author versions: Python 3.12.14, NumPy 2.4.6, SciPy 1.17.1):

```sh
python3.12 -m venv /tmp/covering-twelve-env
/tmp/covering-twelve-env/bin/python -m pip install -r round-two/six-covering-2/requirements-discovery.txt
OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1 MKL_NUM_THREADS=1 NUMEXPR_NUM_THREADS=1 \
  /tmp/covering-twelve-env/bin/python -B round-two/six-covering-2/twelve-class-exclusion/reproduce.py --generate
```

Each root gets at most eight sequential resumable batches of 180 seconds
and 700 new nodes. Each LP has the existing two-second limit. This voluntary
allowance is a reproducibility setting, not a mathematical bound. Rerunning
resumes existing trees. An incomplete tree or failed job asserts no theorem.

Once generated trees exist, Python 3.10+ standard library suffices for exact
replay (author: CPython 3.11.2):

```sh
python3 -B round-two/six-covering-2/twelve-class-exclusion/reproduce.py \
  --generated PATH_TO_TREES --require-manifest
python3 -O -B round-two/six-covering-2/twelve-class-exclusion/frontier_twelve.py
```

`PATH_TO_TREES` contains `tree-normal-0-0-0.json`,
`tree-normal-0-1-0.json`, `tree-normal-1-0-0.json` and
`tree-normal-1-1-0.json`. The wrapper checks the exact expected root and
every strict integer leaf, resource incidence, actual branch phase and
literal CRT-coordinate transport. No solver is imported by the checker.
`--require-manifest` also requires the exact author-run manifest. A different
proposal may produce another valid tree; without that option all proof
checks still run, and the manifest match is reported separately.

The author result has 1,377 nodes, 240 expansions, 1,137 strict leaves,
5,401 actual branch phases, 4,936 positive transports and 717,336 selected
pair entries. Three newly excluded forms add 7,560 forbidden phase tuples.
Combined with the previous five exclusions, eight forms and 27,720 tuples
are forbidden, leaving sixteen forms. The combined count uses the cited
[old five-class](../five-class-exclusion/README.md) and
[parity](../parity-class-exclusion/README.md) results; this wrapper directly
replays the four zero-phase roots.

The proof is written mathematics plus exact Python execution, checked by
its author. Independent mathematical review and proof-assistant
formalization are pending. `SHA256SUMS` authenticates this directory's
compact source; event hashes alone are not proof certificates.
