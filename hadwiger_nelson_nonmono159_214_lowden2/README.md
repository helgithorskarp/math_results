# Exact low-denominator mixed-gadget overlap exclusion

Let `A` be Parts' archived 159-point `v159e646` nonmonochromatic-triple
configuration and `B` his 214-point `v214e977` nonmonochromatic-pair
configuration. If an exact Euclidean isometry `g` has orthogonal part with
canonical denominator at most 2 over `K = Q(sqrt(3),sqrt(5),sqrt(11))`, and
`|A intersection g(B)| >= 2`, then the strict unit-distance graph on
`A union g(B)` is 4-colorable.

There are exactly **39,004 distinct placements**, supported by 12 orthogonal
maps. Their strict graphs have 250--371 vertices and 1,207--1,787 edges.
Every placement in this class is included, without a further overlap cutoff.
This is an exact computational exclusion of this family, not a record
improvement. Higher-denominator orientations, fewer than two overlaps, and
larger compositions remain outside the claim.

## Why the orientation list is complete

Use the field basis

```
1, sqrt(3), sqrt(5), sqrt(15), sqrt(11), sqrt(33), sqrt(55), sqrt(165).
```

Write the orthogonal map as `(x,y) -> (cx-sy,sx+cy)`, or as
`(x,y) -> (cx+sy,sx-cy)` for a reflection, where `c*c+s*s=1`.
A common denominator for the sixteen rational coefficients of `c,s`, with
the common gcd removed, is the canonical denominator. This restriction is
relative to the displayed radical basis, not an intrinsic measure of geometric
complexity.

**Trace bound.** If that denominator is at most 2, write
`c = sum a_i sqrt(r_i)/2` and `s = sum b_i sqrt(r_i)/2`, with integral
coefficients and the eight radicands `r_i` in the order above. All eight
embeddings of `K` are real, and each sends `c*c+s*s=1` to the same equation.
Averaging them cancels all mixed radical terms and gives

```
sum r_i (a_i*a_i + b_i*b_i) = 4.
```

Thus every coefficient with radicand at least 5 is zero. Enumerating the
remaining four integer coefficients subject to this equation, and testing
`c*c+s*s=1` exactly, gives precisely the 12 rotations by multiples of
30 degrees. With the reflected versions there are 24 orthogonal maps.
This is a complete classification of the denominator-at-most-two orthogonal
maps in this field, independently of the two input configurations.

For each of those 24 maps `T`, every translation supporting an overlap is
`a - T(b)` for some `a in A, b in B`. The number of representations of that
translation is exactly the number of overlaps, since both point sets have
distinct points. `enumerate_lowden.py` enumerates these differences in exact
Python integers and retains multiplicity at least two. Twelve maps have a
supported translation; their 39,004 placements recover 4,310,748 determining
unordered overlap pairs. The histogram is in `CENSUS.txt`.

The new trace-based enumeration was compared **placement by placement** with
the previously implemented equal-length-segment enumeration. All 39,004
canonical transform rows agree. It does not depend on that implementation
for enumeration completeness.

## Exact coloring verification

`verify_colorings.cpp` reconstructs each union, identifies coincident points,
tests every unordered pair for exact unit distance, and checks the supplied
four-coloring. The geometry uses integer coefficients in the eight-element
basis. The verifier shares field arithmetic and geometry code with the
existing graph emitter; it is independent of the SAT solver, not an
independent geometry implementation. The placement enumerator uses a
separate arbitrary-precision implementation and a different completeness
argument.

The coordinates have denominator 12 and coefficient magnitude at most 18.
The selected maps have denominator at most 2 and coefficient magnitude at
most 2; their products and translations are small. A conservative bound of
1000 on each coefficient entering a squared-distance calculation makes even
`128 * 165 * 1000^2 < 2^35`; 128-bit products and checked narrowing to 64 bits
are sufficient for these fixed inputs. The code is not claimed overflow-safe
for arbitrary unbounded inputs. This is not a proof-assistant formalization.

## Reproduction and omitted generated files

Only source, coordinates, hashes, and compact output are published. The
plain-text coloring checkpoint is 16,171,656 bytes; its graph stream is
488,178,389 bytes. These and the 4,529,252-byte canonical placement stream
remain outside Git. `GENERATED.json` gives their sizes and SHA-256 digests.
Hashes identify the checked run; hashes alone do not certify colorability.

Full reproduction needs Python 3.11+, GCC with C++20, `sha256sum`, and
`python-sat==1.8.dev24` for witness generation:

```bash
cd hadwiger_nelson_nonmono159_214_lowden2
python3 -m venv .venv
.venv/bin/pip install -r ../hadwiger_nelson_nonmono159_overlap10/requirements.txt
./verify.sh --work-dir /scratch/mixed-lowden2-rebuild \
  --solver-python "$PWD/.venv/bin/python" --jobs 4
```

The work directory must be new and is preserved on success or failure.
Allow roughly 1 GB disk and several GB RAM; the inherited SAT generator
loads the graph stream into memory. All assignments are checked directly;
a false solver UNSAT answer or an invalid assignment makes verification fail.
No solver UNSAT assertion enters the theorem.

For someone already holding the plain-text coloring checkpoint, the complete
family and all colorings can be checked without installing a SAT solver:

```bash
./verify.sh --work-dir /scratch/mixed-lowden2-check \
  --colorings /absolute/path/to/colorings.txt
```

The generated census and canonical placement hash must agree before the
coloring check. Any properly formatted valid assignment file is accepted;
matching the original coloring hash is reported as provenance only. Headline
output is in `expected_verify.txt`. `VALIDATION.md` records this pass's checks.

## Prior sources and scope

- Jaan Parts, [Graph minimization, focusing on the example of 5-chromatic
  unit-distance graphs in the plane](https://arxiv.org/abs/2010.12665),
  Geombinatorics 29(4) (2020), 137--166.
- Jan Kristian Haugland, [A Moser-spindle-free 5-chromatic unit distance
  graph on 2131 vertices in the plane](https://arxiv.org/html/2608.04542v4),
  introduction, still names 509 as the unrestricted record (checked
  4 September 2026).

`SOURCE.md` records coordinate provenance. The coloring result applies to the
pinned point sets regardless of their advertised forcing properties; neither
those properties nor their minimality is needed here. No historical priority
claim is made for this family exclusion or the elementary trace argument.
