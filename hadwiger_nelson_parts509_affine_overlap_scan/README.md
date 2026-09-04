# Maximum affine overlap of the Parts L/S gadgets

## Exact result

Let `L` be labels `0..373` of the Parts 509-vertex construction.  Let `S+`
be its 135-label small gadget together with a second copy of the origin, so
the two gadgets have 510 labels before identifications.  Among all Euclidean
isometries `f` of the plane,

> the maximum of `|L intersect f(S+)|` is exactly **85**, attained by exactly
> six isometries.  Exactly six further isometries have overlap 84, and no
> isometry has overlap between 64 and 83.

The twelve unions at the top two overlap levels have the following exact
census.

| overlap | placements | union order | strict edges | chromatic conclusion |
|---:|---:|---:|---:|---|
| 85 | 6 | 425 | 2,185 | explicit proper 4-colouring |
| 84 | 6 | 426 | 2,203 | explicit proper 4-colouring |

Thus none of the most heavily collapsed placements is five-chromatic.  This
is a geometric maximum theorem and a restricted family exclusion, **not a new
five-chromatic graph and not an improvement of the 509-vertex record**.

## Finite exact enumeration

All coordinates lie in `K=Q(sqrt(3),sqrt(5),sqrt(11))`.  Two distinct
overlaps `q1,q2 -> p1,p2` force equal nonzero segment lengths and determine
the linear orientation and translation.  The exact squared-distance classes
common to `L` and `S+` all lie in `Q(sqrt(33))`, so the orientation formulas
are evaluated by conjugating `a+b sqrt(33)`; no general algebraic-number
package is needed.

The enumerator first deduplicates directed segment vectors.  The 11,650
distinct nonzero `L` vectors and 1,666 distinct nonzero `S+` vectors yield
exactly 1,420 orientation-preserving and 1,420 orientation-reversing linear
maps that can support two overlaps.  For each map `T`, the multiplicity of a
cross difference

```text
p - T q
```

is exactly the number of overlaps produced by the corresponding translation.
Hash collisions cannot change the result because the full 16-coefficient
field elements are retained and compared for equality.  The complete scan
finds 2,992,078 affine placements with at least two overlaps.  As an internal
checksum, summing `binomial(m,2)` over their overlap multiplicities gives
17,658,256, exactly the independently derived determining-pair count.

An isometry outside the 2,840 enumerated orientations cannot have two
overlaps: any two overlaps themselves contribute one of the equal directed
segment pairs used to construct the list.  Isometries with zero or one
overlap plainly cannot exceed the reported maximum.  This proves global
completeness over all real Euclidean isometries, not only `K`-rational maps
assumed in advance.

## Reproduction

From this directory:

```bash
g++ -std=c++20 -O3 -Wall -Wextra -Wpedantic \
  enumerate_overlaps.cpp -o enumerate_overlaps
./enumerate_overlaps \
  ../hadwiger_nelson_parts509_completion_census_degree9/points.tsv \
  > overlap_scan.txt
diff -u expected_overlap_scan.txt overlap_scan.txt
python3 verify_high.py high_overlap_certificate.json
```

The C++ scan is single-threaded and took about 80 seconds on the research
host.  The integer-basis certificate checker takes about 30 seconds; the
independent Fraction checker took about four minutes under concurrent host
load.  The primary ends with `solver_free_high_certificate_checks=true`.

The positive colouring certificate can be regenerated after installing the
pinned requirement:

```bash
python3 -m venv /scratch/parts509-affine-overlap-venv
/scratch/parts509-affine-overlap-venv/bin/pip install -r requirements.txt
/scratch/parts509-affine-overlap-venv/bin/python \
  independent_check.py high_overlap_certificate.json
/scratch/parts509-affine-overlap-venv/bin/python \
  generate_high_certificate.py overlap_scan.txt regenerated.json
cmp high_overlap_certificate.json regenerated.json
```

## Trust boundary and scope

- The enumerator uses exact signed-integer arithmetic in the eight-element
  basis of `K`.  Every narrowing operation checks for 64-bit overflow, and
  hash-table keys retain exact values.  No floating-point operation is used.
- SAT is used only to discover twelve positive colourings.  `verify_high.py`
  reconstructs the exact union points and all strict unit edges, then checks
  those colourings directly without a solver.
- The full histogram and determining-pair checksum establish completeness of
  the maximum.  The Python verifier checks the histogram arithmetic and all
  top-placement transformations, graphs, and colourings; it does not
  independently repeat the 2,840-orientation C++ scan.  The second checker
  independently parses the original Mathematica coordinates into exact
  `Fraction` field elements and repeats the twelve graph checks.
- Nothing is claimed here about four-colourability of the remaining 2,992,066
  placements, including all candidates of order 447 through 508.

## Files

- `enumerate_overlaps.cpp` — exact affine-overlap enumerator.
- `expected_overlap_scan.txt` — complete expected output for the exact path.
- `high_overlap_certificate.json` — twelve transformations and proper
  four-colouring witnesses.
- `verify_high.py` — solver-free exact graph and colouring checker.
- `independent_check.py` — independent SymPy/Fraction graph checker.
- `generate_high_certificate.py` — positive-certificate generator.
- `requirements.txt` — pinned generator-only SAT dependency.
