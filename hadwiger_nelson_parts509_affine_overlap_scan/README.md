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

A larger positive certificate checks all **16,542** placements with at least
20 overlaps (union order at most 490).  Every one has an explicit proper
four-colouring.  Consequently any five-chromatic union of these fixed `L` and
`S+` gadgets has at most 19 overlaps and at least 491 vertices.  This lower
bound is only for the fixed-gadget affine family; it is not a general lower
bound for five-chromatic unit-distance graphs.

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
g++ -std=c++20 -O3 -Wall -Wextra -Wpedantic \
  emit_graphs.cpp -o emit_graphs
./enumerate_overlaps \
  ../hadwiger_nelson_parts509_completion_census_degree9/points.tsv \
  > overlap_scan.txt
diff -u expected_overlap_scan.txt overlap_scan.txt
python3 verify_high.py high_overlap_certificate.json
./enumerate_overlaps \
  ../hadwiger_nelson_parts509_completion_census_degree9/points.tsv \
  --emit-at-least 20 > /scratch/overlap_atleast20_scan.txt
./emit_graphs \
  ../hadwiger_nelson_parts509_completion_census_degree9/points.tsv \
  /scratch/overlap_atleast20_scan.txt \
  > /scratch/overlap_atleast20_graphs.txt
python3 verify_graph_transcript.py overlap_atleast20_certificate.json \
  /scratch/overlap_atleast20_scan.txt /scratch/overlap_atleast20_graphs.txt \
  > /scratch/verify_graph_transcript.txt
diff -u expected_verify_graph_transcript.txt \
  /scratch/verify_graph_transcript.txt
```

The C++ scan is single-threaded and took about 80 seconds on the research
host.  Emitting the 16,542 exact graphs takes about three minutes and produces
a 300 MB scratch transcript; its expected SHA-256 is
`a774306af43b66eb3159068a16bf6beb1d5d13789c1a45be4978cc00de6a317a`.
The committed threshold-20 certificate has SHA-256
`e1aa967184c9b015ab66e7e7864e70bf7e81cb4c1d0016cd0e4afa7dc7ced5a4`.
The high-placement integer-basis checker takes about 30 seconds; the
independent Fraction checker took about four minutes under concurrent host
load.  The optional independent 1,360-placement check
`python3 verify_threshold.py overlap_atleast40_certificate.json` takes about
fifteen minutes.
The primary high-placement check ends with
`solver_free_high_certificate_checks=true`.
The optional exact arguments `--emit-at-least N` print every transformation
at a lower overlap threshold; the default is 84 and is what
`expected_overlap_scan.txt` uses.

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
/scratch/parts509-affine-overlap-venv/bin/python \
  generate_threshold_certificate.py /scratch/overlap_atleast20_scan.txt 20 \
  regenerated_threshold.json \
  --graph-transcript /scratch/overlap_atleast20_graphs.txt
cmp overlap_atleast20_certificate.json regenerated_threshold.json
```

The threshold-20 scan has the same full histogram as the default scan and
additionally prints all 16,542 relevant transformations.  The graph transcript
accelerates positive-witness discovery and is cryptographically bound into
the certificate.  It is generated rather than committed because of its size.
The generator streams the transcript and stayed below 50 MB resident memory
in the tested run.

## Trust boundary and scope

- The enumerator uses exact signed-integer arithmetic in the eight-element
  basis of `K`.  Every narrowing operation checks for 64-bit overflow, and
  hash-table keys retain exact values.  No floating-point operation is used.
- SAT is used only to discover positive colourings: twelve in the compact
  high certificate and 16,542 in the threshold-20 certificate.
  `verify_graph_transcript.py` checks the exact scan, source hashes, transcript
  digest, graph metadata, every strict-edge list, and every packed colouring
  without invoking a solver.  The transcript itself comes from the exact
  integer-arithmetic `emit_graphs.cpp`.  As an independent audit,
  `verify_threshold.py` reconstructs the geometry and all strict edges in
  Python for the 1,360-placement threshold-40 subcertificate.
- The full histogram and determining-pair checksum establish completeness of
  the maximum.  The Python verifier checks the histogram arithmetic and all
  top-placement transformations, graphs, and colourings; it does not
  independently repeat the 2,840-orientation C++ scan.  The second checker
  independently parses the original Mathematica coordinates into exact
  `Fraction` field elements and repeats the twelve graph checks.
- Nothing is claimed here about four-colourability of the 2,975,536 placements
  with fewer than 20 overlaps, including all candidates of order 491 through
  508.

## Files

- `enumerate_overlaps.cpp` — exact affine-overlap enumerator.
- `expected_overlap_scan.txt` — complete expected output for the exact path.
- `high_overlap_certificate.json` — twelve transformations and proper
  four-colouring witnesses.
- `overlap_atleast20_certificate.json` — all 16,542 transformations with at
  least 20 overlaps and proper four-colouring witnesses.
- `overlap_atleast30_certificate.json` — the preceding 5,468-placement
  subcertificate retained for reproducibility.
- `overlap_atleast40_certificate.json` — independently reconstructed
  1,360-placement subcertificate.
- `overlap_atleast50_certificate.json` — the earlier 372-placement
  subcertificate retained for reproducibility of the preceding commit.
- `verify_high.py` — solver-free exact graph and colouring checker.
- `verify_threshold.py` — solver-free checker for either threshold
  certificate.
- `verify_graph_transcript.py` — streaming checker for the exact bulk graph
  transcript and all threshold-30 witnesses.
- `independent_check.py` — independent SymPy/Fraction graph checker.
- `generate_high_certificate.py` — positive-certificate generator.
- `generate_threshold_certificate.py` — bulk positive-certificate generator.
- `emit_graphs.cpp` — exact graph-transcript emitter for bulk verification.
- `requirements.txt` — pinned generator-only SAT dependency.
