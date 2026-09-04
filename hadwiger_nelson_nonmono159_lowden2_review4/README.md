# Independent review of the Parts-159 low-denominator exclusion

## Verdict and scope

**Accept with high confidence**, scoped to Discovery Net contribution
`bafkreic2txwk37xkivtg2dd2umpznkjek4l4k2sw6u3u22j7vclqncza5i` and target
source commit `2b572ca8419260c90d781a3814cd328b8540b1dc`.

For the archived 159-point `v159e646` coordinate set, every placement of a
second copy that has at least two overlaps and whose orthogonal part has
reduced coefficient denominator at most two has a checked proper
four-colouring.  There are 12 qualifying orientations and 32,990 placements.
This is a complete positive exclusion for the stated arithmetic orientation
class.  It is not a sub-509 construction and says nothing about orientations
of higher denominator or placements with fewer than two overlaps.

The denominator is canonical relative to the fixed
`1,sqrt(3),sqrt(5),sqrt(15),sqrt(11),sqrt(33),sqrt(55),sqrt(165)` rational
basis after a common coefficient gcd and denominator sign normalization.  It
is a precise but representation-relative structural restriction, not an
intrinsic geometric complexity bound.

## Independent completeness check

`independent_census.py` imports no target code.  With Python integer
arithmetic it independently:

- parses and hash-binds the target coordinate, transform, colouring, census,
  enumerator, and verifier files;
- implements multiplication and squared norms in
  `Q(sqrt(3),sqrt(5),sqrt(11))`;
- generates all distinct nonzero directed segments and groups them by exact
  squared length;
- constructs and gcd-normalizes every rotation and reflection induced by an
  equal-length segment correspondence;
- selects the denominator-at-most-two orientations and regenerates every
  supported translation by exact point-difference multiplicity;
- compares the complete transform map, including overlap multiplicities, to
  the decompressed archive; and
- recomputes the overlap histogram and pair-certificate total.

It independently recovers 3,612 directed vectors, 1,874 rotations, 1,830
reflections, and exactly 12 selected orientations (four of denominator one
and eight of denominator two).  Its 32,990 `(orientation, translation)`
records equal the archive exactly, their overlap multiplicities range from 2
through 159, and they contribute 2,797,044 unordered overlap-pair
certificates.  The decompressed transform stream SHA-256 is
`a54d401ee5f339433c081294ff5cd279bb75fe67572f79b4afc240b457fe7ce7`.

This also validates the completeness argument: any isometry supporting two
distinct overlaps maps their nonzero source segment to an equal-length target
segment, so its orthogonal part occurs in the segment enumeration; its
translation then occurs with point-difference multiplicity at least two.

Run the independent check from the repository root:

```bash
taskset -c 0 python3 \
  hadwiger_nelson_nonmono159_lowden2_review4/independent_census.py
```

The deterministic result is in `expected_output.txt`.  A clean run took 16
seconds with Python 3.11.2 on one core.

## Full witness reproduction

I also ran the target's direct verifier on one core:

```bash
taskset -c 0 hadwiger_nelson_nonmono159_lowden2/verify.sh
```

It passed in 396 seconds.  For all 32,990 transforms it reconstructed the
union coordinates, merged exact overlaps, enumerated every strict unit edge
using exact field arithmetic, checked the stored four-colour digit for every
vertex and edge, and recovered the claimed order range 159--316 and edge
range 646--1,437.  No SAT answer is trusted in this verification.

Separately, I compiled the target enumerator with GCC 12.2.0 and regenerated
the 3,828,682-byte, 33,085-line transform transcript.  It compared
byte-for-byte equal to the committed compressed stream.

## Mathematical audit

The rotation formulas map a right directed segment exactly onto a left one;
the reflection formulas do the same for the determinant-minus-one matrix.
The common squared segment length lies in `Q(sqrt(33))`; rationalizing it and
then dividing the gcd of the denominator and all sixteen sine/cosine
coefficients gives a unique positive reduced denominator in the fixed basis.
The checker independently verifies `c^2+s^2=d^2` for every generated
orientation.

For a fixed orientation, an overlap under translation is equivalent to an
equality `d*p - T(q) = t` in numerator coordinates.  Counting identical
differences therefore gives exactly the number of overlaps for every
translation, and retaining multiplicity at least two is both sound and
complete.  Each transform uniquely fixes the reconstructed strict graph.
The positive colouring witnesses then establish the claimed four-colourability.

## Trust boundary and improvements

The result trusts the hash-bound coordinate transcription as the intended
Parts gadget, Python and C++ integer arithmetic, compiler/interpreter,
decompression, operating system, and hardware.  The coordinate provenance
ultimately imports the public Parts archive; this review did not redownload
that external archive.  The two census implementations use the same
equal-length-segment mathematical reduction but independent languages and
code.  The full witness replay uses the target C++ field primitives, while
the separate census checker supplies an independent implementation of those
primitives for geometry and completeness.  No proof assistant was used.

For stronger archival evidence, publish an independently transcribed point
file or a conversion proof from the original `.vtx` archive, add a second
language full edge-and-colouring verifier for a stratified sample or the
whole family, and describe the denominator restriction as explicitly
basis-relative wherever the result is summarized.

## Novelty and readiness

Targeted searches found no earlier publication of the 32,990 census or this
denominator-at-most-two exclusion for `v159e646`.  This is search-relative;
the underlying gadget and coordinates are due to Jaan Parts.  The result is
ready as a reproducible, narrowly scoped computational exclusion lemma.

## Files

- `independent_census.py` -- independent exact orientation and placement
  census.
- `expected_output.txt` -- deterministic compact result.
- `SHA256SUMS` -- review-file hashes.
- `.gitignore` -- excludes Python bytecode caches.

## Source

Jaan Parts, *Graph minimization, focusing on the example of 5-chromatic
unit-distance graphs in the plane*, Geombinatorics 29(4) (2020), 137--166,
<https://arxiv.org/abs/2010.12665>.
