# A single frame-normalized case for every 72-point candidate

**Proved with an exact counting certificate:** every line-free 72-subset of
`F_5^3` has `3a_8+a_9>=11`, where `a_m` counts its `m`-point plane sections.
The prior theorem `a_8<=1` therefore forces at least eight nine-point planes.
Four of their normals form a projective frame.

Consequently **BBB alone is an exhaustive normal form**, strengthened by
five additional nine-point planes and a fourth plane whose normal has no
zero coordinate. Here `B=(9,15,16,16,16)` is the ordered profile of each
coordinate parallel class. See the [proof](THEOREM.md) for the exact
normalization and complete decision specification.

This gives the certificate team one global case to settle. It does not
exclude 72, settle 71, or exclude the presence of an eight-point plane.
The durable numerical interval remains **70--72**. Independent review is
pending.

## Replay

Python 3.10+ and a C++20 compiler suffice. Tested with CPython 3.11.2 and
GCC 12.2.0. From this directory:

```sh
python3 verify.py --out /tmp/nine-plane-frame72 > /tmp/nine-plane-frame72.json
diff -u EXPECTED.json /tmp/nine-plane-frame72.json
python3 -O verify.py --out /tmp/nine-plane-frame72-opt > /tmp/nine-plane-frame72-opt.json
diff -u EXPECTED.json /tmp/nine-plane-frame72-opt.json
sha256sum -c SHA256SUMS
```

The expected status is `NINE_PLANE_FRAME72_VERIFIED`. The replay takes
about eight seconds, including compilation. Peak child memory, including
the compiler, was about 97 MiB.

The replay:

* re-enumerates all 33,554,432 planar subsets using the prior complete
  enumeration, recovering the same 70 section spectra;
* independently rebuilds the 61-row, 463-column incidence matrix and
  checks every new integer certificate inequality;
* verifies all affine incidence constants, 3,875 projective triangles,
  372,000 frame-extension cases and 256 affine normalizations;
* verifies the published 70-point witness and rejects a corrupted dual
  certificate.

The exact lower bound is `10082223/1000000>10`. Certificate SHA-256:
`240abbef6ecd5e1a3ca4632cd2426a5ee33ab3e18319a245bd94fa62e47e4958`.
No optimizer, third-party Python package, network or external catalogue is
needed for replay. The script expects the parent repository directories.

The two-eight-plane dependency has its own 164 checked SAT proofs. This
replay does not re-run them. The mathematical reduction, ordinary C++
enumeration and that prior theorem are explicit trust boundaries; the
new inequality itself uses no solver conclusion. See [SOURCES.md](SOURCES.md).

## Handoff

Use the BBB coordinate profile `(9,15,16,16,16)` on all three axes. Require
at least five further nine-point planes outside those classes and at least
one nine-point plane of the form

```text
x+b y+c z=d,   b,c in {1,2,3,4}, d in F_5.
```

There are exactly 80 planes in this latter family. Indicators for these
conditions must encode selected **nine-point** sections, not arbitrary
sections of size at most nine. The proof supplies an affine representative
with all these conditions simultaneously. No plane shape is fixed.

The next structural target is compatibility between low planes across
different pencils. Exploratory pair-of-plane incidence tests remain
feasible and are not used by the theorem.
