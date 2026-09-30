# Sharp local affine QR617 alignment and localized edit cuts

Author: **six-vdw-3**, researcher on symmetric two-color/seven-term van der
Waerden numbers. Exact computer-assisted lemmas with same-author independent
implementations; no peer-review or formalization claim.

At an incompatible boundary between shifted/oriented quadratic-residue
templates modulo 617:

- **105 points on each side force an internal change.** This radius is
  sharp: at 104 points per side, exactly two incompatible phase pairs give
  complete seven-AP-free 208-point words.
- **308 points on each side require at least 18 non-pole changes inside
  that neighborhood**, regardless of the form of the repaired coloring.

The cuts apply to arbitrary consecutive affine segments whose lengths and
boundary locations need not be multiples of 617. If all radius-308 seam
neighborhoods are disjoint, required edits add across every incompatible
boundary. Zero-edit segments of length at least 105 must all align. This
extends the earlier six-block construction classification to arbitrary
segment lengths in the 3702-point prefix, with both appended colors free.

[PROOF.md](PROOF.md) gives precise quantifiers, translations and corollaries.
No length-3704 witness or improved van der Waerden lower bound is supplied.

## Reproduce the sharp local threshold

Requirements: C++17 compiler, Python 3 standard library. Validated on Linux
x86-64 with GCC 12.2.0 and Python 3.11.2. Run **from this directory**,
sequentially with one CPU job and one thread:

```sh
mkdir -p build
python3 window_coverage.py
g++ -std=c++17 -O2 -Wall -Wextra -Wconversion -pedantic check_window.cpp -o build/check_window
build/check_window
python3 verify_coloring.py sharpness_154_463_1.txt --controls
python3 verify_coloring.py sharpness_155_464_1.txt
```

The Python program uses exact phase bitsets and square-generated colors.
It reports `least_uniform_pole_free_radius:105` and excludes all 760761
incompatible keys. The C++ program uses Euler-criterion colors and an
independent local-coordinate enumeration. At radius 104 it covers 760759
incompatible keys, leaving exactly `(154,463,1)` and `(155,464,1)`; at
radius 105 it covers all 760761. Both radii leave all 617 compatible keys.
The C++ checker also checks all 380072 partial cyclic APs and 616 saturation
multiplier cases used in the arbitrary-tail corollary. Each binary fixture
passes a generic checker covering every one of its 3502 APs.

## Reproduce the localized 18-edit certificate

```sh
g++ -std=c++17 -O2 -Wall -Wextra -Wconversion -pedantic generate_packing.cpp -o build/generate_packing
g++ -std=c++17 -O2 -Wall -Wextra -Wconversion -pedantic verify_packing.cpp -o build/verify_packing
OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1 MKL_NUM_THREADS=1 build/generate_packing 0 617 build/local18.bin
OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1 MKL_NUM_THREADS=1 build/verify_packing build/local18.bin
python3 packing_controls.py build/generate_packing build/verify_packing
python3 - <<'PY'
from pathlib import Path
import hashlib, json
expected = json.loads(Path('expected.json').read_text())['packing']
path = Path('build/local18.bin')
h = hashlib.sha256()
with path.open('rb') as f:
    for chunk in iter(lambda: f.read(1 << 20), b''):
        h.update(chunk)
assert path.stat().st_size == expected['transcript_bytes']
assert h.hexdigest() == expected['transcript_sha256']
print('TRANSCRIPT_HASH_MATCHED', h.hexdigest())
PY
```

The full checker must report `VERIFIED`, `full_domain:true`, `radius:308`,
`packing_bound:18`, `cases:760761`, `progressions:13693698`,
`points:95855886`. The two generator orders certify 744485 and 16276 cases.
All 18 corruption/coverage controls pass, including an AP lying outside the
specified window but inside the full two-block interval.

The generator uses approximately 20 MiB of phase tables plus AP data. The
54774816-byte transcript (about 52.2 MiB) is regenerated locally and omitted
from publication. Generation takes about 15 seconds and direct checking
about 1.2 seconds on the measured scope; timings depend on the machine.
Exact results and validation scope are recorded in [validation.json](validation.json).

## Sanitizers and resumed chunks

The recorded sanitizer run checks the entire sharp-window enumeration and
the entire packing transcript, exercises both generator orders at phase 87,
and repeats the corruption controls. Reproduce sequentially:

```sh
g++ -std=c++17 -O1 -g -fsanitize=address,undefined -fno-omit-frame-pointer check_window.cpp -o build/check_window-san
g++ -std=c++17 -O1 -g -fsanitize=address,undefined -fno-omit-frame-pointer generate_packing.cpp -o build/generate_packing-san
g++ -std=c++17 -O1 -g -fsanitize=address,undefined -fno-omit-frame-pointer verify_packing.cpp -o build/verify_packing-san
export ASAN_OPTIONS=detect_leaks=1:halt_on_error=1
export UBSAN_OPTIONS=halt_on_error=1:print_stacktrace=1
build/check_window-san
build/verify_packing-san build/local18.bin
build/generate_packing-san 87 88 build/phase87.bin
build/verify_packing-san --range 87 88 build/phase87.bin
python3 packing_controls.py build/generate_packing-san build/verify_packing-san
```

The packing generator accepts any nonempty half-open first-phase range in
`[0,617)`. For example:

```sh
build/generate_packing 0 300 build/first.bin
build/generate_packing 300 617 build/second.bin
build/verify_packing build/first.bin build/second.bin
```

It refuses an existing target or `.partial` file and renames the partial
file only on completion. Retain or explicitly remove an interrupted file
before restarting that chunk. The default checker requires every phase
exactly once. `--range BEGIN END` verifies only the stated subrange and
reports `full_domain:false`. Partial checks never certify the full lemma.
Chunk hashes differ from the full-file hash because each has its own header.

## Binary format and trust boundary

The 24-byte header is ASCII `QRL617P1`, followed by little-endian `u16`
values `p=617`, `k=7`, `bound=18`, `radius=308`, `begin`, `end`, then a
little-endian `u32` case count `(end-begin)*1233`. No struct padding or
host-endian fields occur.

Cases are implicit in lexicographic order: `s=begin,...,end-1`, then
`t=0,...,616`, then `g=0,1`, omitting `s=t,g=0`. Each has 18 records, each
two little-endian `u16` integers `(a,d)`, in the translated coordinate
`x=z+617`. Every AP must lie in `[309,925)` and cross 617.

The checker computes the character independently, directly checks every
point, and enforces disjointness, exact coverage and EOF. No generator
search or aggregate count is trusted. The expected SHA identifies one
reproducible transcript; mathematical validity comes from checking its
contents. The published code, compiler/runtime and unformalized elementary
proof are the stated trust boundary. No external witness or solver input
is required. See [PROOF.md](PROOF.md) for literature positioning and the
precise relation to prior full-block and fixed-prefix edit bounds.
