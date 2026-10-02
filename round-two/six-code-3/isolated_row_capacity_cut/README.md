# Isolated-row capacity cut: three hubs P10, four hubs P20

Actual author **six-code-3**, role **researcher**, 2026-10-02.
[PROOF.md](PROOF.md) states every hypothesis. At71 words on18 points,
generic23-star coverage8933/universal8323 and local three-point9249
give the exact cut2E+Q>=W+2X for at most four unsaturated points.
Complete boundary categories and ordinary odd handshake sharpen it
toP>=10 for both three-hub profiles andP>=20 for four hubs.
No SS-unit hypothesis or whole-code symmetry. Independent
[9293](../../six-reviewer-4/three-point-star-audit/REVIEW.md) confirms the
imported local9249 theorem. The new cut and boundary refinements remain
independently unreviewed; unrestricted69--71 is unchanged and no
historical priority is claimed.

Python3.11+ standard library only; author runs use CPython3.11.2.
From the repository root choose fresh, separate work directories:

```sh
OPENBLAS_NUM_THREADS=1 OMP_NUM_THREADS=1 MKL_NUM_THREADS=1 \
python3 round-two/six-code-3/isolated_row_capacity_cut/reproduce.py \
  --work scratch/capacity-normal

OPENBLAS_NUM_THREADS=1 OMP_NUM_THREADS=1 MKL_NUM_THREADS=1 \
python3 -O round-two/six-code-3/isolated_row_capacity_cut/reproduce.py \
  --work scratch/capacity-optimized
```

Each command builds all426 actual high-hub subset rows, checks all418
within scope, and retains eight actual five-hub negative controls.
All actual coordinates agree with the independent point-mask checker.
Both recursive and iterative category enumerations agree on every
necessary boundary template, including the h1/e4 margin9 case that
must be kept until the global margin budget excludes it.
The run rejects23 semantic damages and transports1278 actual marked
rows under three point bijections. Whole RESULT bytes must match
frozen [expected.json](expected.json) in both modes. Interpreter/timing
information is separate in METADATA. [VALIDATION.json](VALIDATION.json)
records the author's complete runs.

This runner checks the new row and category certificates; it does not
replay the earlier local9249 finite carrier or the independent combined
carrier9293. The latter confirms the local theorem directly from
8933/8323 without older numerical branch premises. The precise scope is in
[DEPENDENCIES.json](DEPENDENCIES.json). Same-author independent
algorithms are not an independent mathematical review. Ordinary
projection/incidence and parity bridges remain unformalized.

One serial CPU job, all threads1, unchanged1CPU2GiB. Fixed guards:
10s/subprocess,100000 category states,10s/category branch. An incomplete
run supplies no nonexistence. Generated catalog/category arrays, logs
and operational state stay in scratch. The supplied fixture groups
are unused: all high subsets are checked directly. Scope is m<=4;
no five-hub or whole71-code exclusion is claimed.
