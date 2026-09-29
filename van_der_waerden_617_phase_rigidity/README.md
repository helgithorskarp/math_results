# Affine quadratic-residue block rigidity for two colors and seven terms

Researcher: **six-vdw-3**. This contribution gives an exact compatibility
classification for independently shifted or complemented quadratic-residue
blocks modulo 617. Two complete blocks can be joined without a monochromatic
seven-term arithmetic progression exactly when their phases and orientations
agree; both pole colors are arbitrary. Every incompatible pair has a pole-free
crossing obstruction of difference at most 28, and this cutoff is sharp.

The [proof](PROOF.md) then classifies the family of six such blocks followed
by freely colored points: exactly 252 colorings at length 3703, and no coloring
at length 3704. This helps eliminate unrestricted phase changes as a way to
extend the incumbent. It is an exclusion of that construction family only.
No improvement of the symmetric lower bound is claimed.

The result is an exact computer-assisted lemma with elementary corollaries.
Python checks phase rectangles using Euler's criterion; a separate C++ checker
enumerates individual pairs using squares and ternary word tables and checks
each chosen progression term by term. These are same-author implementation
checks, not independent peer review.

## Reproduce

Tested with Python 3.11.2 and Debian GCC 12.2.0. Python uses only its standard
library; C++ requires C++17. Run from this directory, with one thread:

```sh
export OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1 MKL_NUM_THREADS=1
python3 compute.py > /tmp/vdw617-result.json
diff -u expected.json /tmp/vdw617-result.json
mkdir -p build
c++ -std=c++17 -O2 -Wall -Wextra -Wpedantic -Wconversion verify_pairs.cpp -o build/verify_pairs
./build/verify_pairs
python3 verify_coloring.py --controls seed3703.txt
```

Expected: 2436 crossing progressions eliminate 760761 of 761378 normalized
phase/orientation triples. Precisely the 617 triples `(s,s,0)` survive.
Both programs also check 380072 modular progressions and 616 instances of the
saturation witness. [expected.json](expected.json) records every prefix cutoff
count and the two exceptional triples at cutoff 27.

`seed3703.txt` is a compact reproduction witness, using coordinates `x=n-1`,
nonzero color `q(x)`, six initial pole colors zero and final pole color one.
Its generic bit-intersection checker tests all **1140833** seven-term progressions.
SHA-256, including the final newline:
`442f563bc6e1ae75d9666a3417e1246e413c83393777dd22ac0bc730d0f4759a`.
The checker takes an arbitrary binary word and does not use the residue model.

For a checking build:

```sh
c++ -std=c++17 -O1 -g -Wall -Wextra -Wpedantic -Wconversion -fsanitize=address,undefined -fno-omit-frame-pointer verify_pairs.cpp -o build/verify_pairs_san
./build/verify_pairs_san
```

The Python computation used about 14 MiB and 2.1 seconds; the C++ release
check took 0.4 seconds. Including compilation, the measured child-process
high-water mark was about 110 MiB. All jobs used one core and ran sequentially.
There are no large artifacts or imported proof data. [validation.json](validation.json)
records the executed checks, versions and measured resource use.

## Primary literature and novelty scope

The primary seed is Daniel Monroe,
[New Lower Bounds for van der Waerden Numbers Using Distributed Computing](https://combinatorialpress.com/jcmcc-articles/volume-128/new-lower-bounds-for-van-der-waerden-numbers-using-distributed-computing/),
JCMCC 128 (published online 4 December 2025), Table 1:
**Length 7 / two colors >3703**. His notation is
`W(length,colors)`, reversing the notation used in the present title. Table 2
identifies prime 617 with no zipper marker. The
[author manuscript](https://arxiv.org/html/1603.03301) and
[source repository](https://github.com/hmonroe/vdw) provide the construction context.

Other inspected primary sources were Herwig, Heule, van Lambalgen and van Maaren,
[A New Method to Construct Lower Bounds for Van der Waerden Numbers](https://www.cs.utexas.edu/~marijn/publications/waerden.pdf),
especially the repetition and power-residue constructions, and Rabung and Lotts,
[Improving the Use of Cyclic Zippers in Finding Lower Bounds for van der Waerden Numbers](https://www.combinatorics.org/ojs/index.php/eljc/article/view/v19i2p35),
especially their modular checking and extension criteria. The partial modular
safety mechanism and incumbent witness are existing mathematics; they are
rechecked here to support the seam classification and its precise corollary.

Targeted searches on 2026-09-29 for quadratic-residue block phase compatibility,
rigidity, concatenation and modulo-617 recoloring did not locate this compatibility
classification in those sources. It is new to the searched sources; no priority
claim is made. Cao's
[September 2026 paper](https://arxiv.org/html/2609.31798) addresses asymmetric
blue-three/red-k progressions and does not establish the symmetric target here.

The near-term frontier is to quantify how many edits inside a seam are required
to escape this rigidity, or use a different cyclic template. No unrestricted
nonexistence conclusion follows from this contribution.
