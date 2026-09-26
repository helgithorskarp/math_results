# Affine asymmetry of every hypothetical 71-point line-free set

**Result:** a line-free subset of \(\mathbb F_5^3\) invariant under a
plane reflection has at most **70 points**, and an explicit 70-point
example attains the bound. Combined with the earlier
[reflection-rigidity theorem](../reflection_rigidity/PROOF.md), this
proves that **every 71-point line-free set is affine-asymmetric**.

This closes the remaining affine-symmetry construction family. It
does not decide whether a 71-point set exists; the campaign interval
remains \(70\le r_5(\mathbb F_5^3)\le71\). Independent peer review of
this contribution is pending.

The [complete proof](PROOF.md) reduces a reflected set to five planar
sections \(A,B,C,C,B\). It checks all 124 possible affine types of the
larger paired section and all compatible labelled second sections.
The exact census covers 213,309,450 representative pairs; the two
calculations of allowed central points agree entrywise for all of them.

[witness70.json](witness70.json) is affine-inequivalent to both the
paper's Figure 4 example and the previous order-three example. The
proof includes a plane-profile invariant certifying this distinction.
It is a new seed for unrestricted construction searches, with no
claim to classify all 70-point examples.

## Reproduce

Requirements: Python 3.10 or newer with its standard library, and a
C++20 compiler available as `g++`. The recorded run used Python
3.11.2 and GCC 12.2.0. No solver or third-party Python package is used.
From the repository root:

```sh
python3 affine_line_free_f5_3/affine_asymmetry71/verify.py --check-expected
```

The command compiles all three C++ programs, regenerates the affine
catalogue, checks its full group action again in Python, verifies the
planar cap twice, and completes both section enumerations. It also
checks the 70-point witness, all nine extremal examples, the two older
70-point controls, and positive/negative Cartesian controls.

The result is deterministic JSON with status
`COMPLETE_REFLECTION_BOUND_70`, equal to
[EXPECTED.json](EXPECTED.json). Progress goes to stderr. Build files
and the compact result are written to a temporary directory; use
`--out /tmp/my-reflection-check` to choose it.
The complete recorded replay took 151 seconds. The bounded checking
build took 19 seconds, with peak child memory including compilation
of about 191 MiB. Runtime depends on hardware and concurrent work.

A bounded address/undefined-behavior sanitizer replay is:

```sh
python3 affine_line_free_f5_3/affine_asymmetry71/verify.py \
  --sanitize --check-expected
```

It covers the full planar catalogue, all orbit checks, both cap checks,
all six `b=c=16` cases, and applicable geometric controls.
Its status is `SANITIZED_C16_CHECK_PASSED`; it compares the
corresponding restriction of `EXPECTED.json`. It does not replace
the complete release replay.

Check published file integrity from this directory with:

```sh
sha256sum -c SHA256SUMS
```

## Source and evidence

- [PROOF.md](PROOF.md): mathematical reduction, complete bounds,
  sharpness, group deduction, and trust boundary.
- [catalogue.cpp](catalogue.cpp): labelled planar census and all
  affine orbit representatives.
- [paired_sections.cpp](paired_sections.cpp): paired-slope census
  with a direct geometric cross-check on every allowed-set mask.
- [direct_lines.cpp](direct_lines.cpp): separate complement census
  using normal-equation planar lines and all 25 transverse slopes.
- [verify.py](verify.py): complete replay, coverage checks, independent
  complement-orbit action, and 775-line witness verification.
- [REPRESENTATIVES.txt](REPRESENTATIVES.txt): 124 compact orbit records.
- [EXPECTED.json](EXPECTED.json): nine complete weighted histograms,
  compact partition hashes, and geometric controls.
- [VALIDATION.json](VALIDATION.json): measured replay provenance.
- [SOURCES.md](SOURCES.md): primary literature and exact dependencies.

The verifier reads the two existing small witness fixtures at
`../known70.json` and `../odd_symmetry/witness70.json` for
the inequivalence comparison. They are rechecked geometrically; no
earlier program or solver is imported. The sharp reflection bound
otherwise has no external mathematical computation as a premise.

The affine-asymmetry corollary imports the prior reflection-rigidity
theorem. Its earlier computations are not replayed by this command.
Source publication and agreement between same-author programs are not
independent peer review.
