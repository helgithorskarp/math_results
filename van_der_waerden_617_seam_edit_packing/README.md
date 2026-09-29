# 44 edits are necessary to repair any incompatible affine QR617 seam

Author: **six-vdw-3**, researcher on symmetric two-color/seven-term van der
Waerden numbers. Exact computer-assisted lemma; same-author independent
checker, with no claim of peer review.

Take two consecutive length-617 blocks, each colored by an independently
shifted and optionally complemented quadratic-residue template modulo 617.
Allow arbitrary colors at the two zero residues. If the phases or
orientations differ, **every seven-AP-free binary word differs from the
template at at least 44 non-pole positions**. The repaired word may be
arbitrary. [PROOF.md](PROOF.md) states all quantifiers and gives the proof.

The certificate is a packing of 44 disjoint monochromatic pole-free APs
for each of the 760,761 normalized incompatible parameter triples. It
also supplies necessary edit cuts for a chain of complete blocks:
`r_j+r_(j+1)>=44` at every incompatible seam, and total edits at least
`44*nu`, where `nu` is the maximum matching size of those seams.

This does not produce a coloring of length 3704 or exclude general
colorings there. A coloring of that length would establish `W(2,7)>=3705`,
with two colors and seven terms.

## Reproduce the full proof computation

Dependencies: a C++17 compiler and Python 3 standard library for hashing and
controls. Validated with GCC 12.2.0 and Python 3.11.2 on Linux x86-64.
Run these commands **inside this directory**, sequentially:

```sh
mkdir -p build
g++ -std=c++17 -O2 -Wall -Wextra -Wconversion -pedantic generate.cpp -o build/generate
g++ -std=c++17 -O2 -Wall -Wextra -Wconversion -pedantic verify.cpp -o build/verify
OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1 MKL_NUM_THREADS=1 build/generate 0 617 build/packing44.bin
OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1 MKL_NUM_THREADS=1 build/verify build/packing44.bin
python3 - <<'PY'
from pathlib import Path
import hashlib, json
path = Path('build/packing44.bin')
h = hashlib.sha256()
with path.open('rb') as f:
    for chunk in iter(lambda: f.read(1 << 20), b''):
        h.update(chunk)
expected = json.loads(Path('expected.json').read_text())
assert path.stat().st_size == expected['transcript_bytes']
assert h.hexdigest() == expected['transcript_sha256']
print('TRANSCRIPT_HASH_MATCHED', h.hexdigest())
PY
python3 controls.py build/generate build/verify
```

The full checker must report `status:VERIFIED`, `full_domain:true`,
`cases:760761`, `packing_bound:44`, `progressions:33473484`, and
`points:234314388`. The generator's two successful order counts are
`[750502,10259]`. Exact run results, compiler versions and sanitizer
coverage are in [validation.json](validation.json).

The generator uses about 80 MiB for its two phase tables. The full local
transcript is `133893958` bytes (about 127.7 MiB) and is deliberately
omitted from the repository. Generation takes about a minute on one CPU;
checking is substantially faster. Both programs use one thread. No solver,
external certificate or unpublished input is required.

The recorded sanitizer run uses the following additional sequential
commands. It checks the entire transcript and exercises both packing
orders on phase 22, then repeats the corruption controls:

```sh
g++ -std=c++17 -O1 -g -fsanitize=address,undefined -fno-omit-frame-pointer generate.cpp -o build/generate-san
g++ -std=c++17 -O1 -g -fsanitize=address,undefined -fno-omit-frame-pointer verify.cpp -o build/verify-san
export ASAN_OPTIONS=detect_leaks=1:halt_on_error=1
export UBSAN_OPTIONS=halt_on_error=1:print_stacktrace=1
build/verify-san build/packing44.bin
build/generate-san 22 23 build/phase22-san.bin
build/verify-san --range 22 23 build/phase22-san.bin
python3 controls.py build/generate-san build/verify-san
```

## Resume using phase chunks

The generator accepts a half-open first-phase range. It refuses an existing
output or `.partial` path and only renames a partial file after successful
completion. After interruption, retain or explicitly remove that incomplete
local file before restarting the affected chunk. A partial file is not
mathematical evidence.

For example, two sequential jobs reproduce the full domain:

```sh
build/generate 0 300 build/first.bin
build/generate 300 617 build/second.bin
build/verify build/first.bin build/second.bin
```

Each chunk has its own header, so its file hash differs from the full-file
hash. Their concatenated payloads are the same deterministic witnesses.
`build/verify --range 0 300 build/first.bin` checks only that range and
reports `full_domain:false`. The default checker requires all 617 phases,
rejecting missing or duplicate coverage.

## Transcript format

The format has no native struct layout, padding or host-endian fields.
The 22-byte header consists of ASCII `QRS617P1`, followed by little-endian
`u16` values `p=617`, `k=7`, `bound=44`, `begin`, `end`, then a little-endian
`u32` case count `(end-begin)*1233`.

Implicit cases iterate `s=begin,...,end-1`, then `t=0,...,616`, then
`g=0,1`, skipping `s=t,g=0`. Each case has 44 records, each a little-endian
pair of `u16` values `(a,d)` in zero-based coordinates in `[0,1234)`.
Each AP crosses the boundary at 617. The checker independently reconstructs
these keys, validates every term, and requires exact EOF.

The expected hash identifies one reproducible transcript. The theorem
rests on full definition-level validation, not on the hash or a generator
success message. See the exact trust boundary in [PROOF.md](PROOF.md).
