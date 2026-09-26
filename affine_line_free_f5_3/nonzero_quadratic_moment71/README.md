# Nonzero centered quadratic moment at 71 points

Every line-free set \(S\subseteq\mathbb F_5^3\) of size 71 must satisfy
\[
 \sum_{x\in S}(x-\mu)(x-\mu)^{\mathsf T}\ne0,\qquad \mu=\sum_{x\in S}x.
\]
This excludes the entire zero-moment family by an algebraic argument
independent of the team's point-set SAT lifting. It does **not** exclude
all 71-point sets or determine the exact maximum.

[PROOF.md](PROOF.md) gives the argument. A conic incidence identity first
bounds the number \(f\) of seven-point planes by
\(f+3\,1_{\{\mu\in S\}}\le5\). Under a zero second moment, cubic and
quartic moments then leave incompatible quartic value distributions.
The finite quartic lemma is stronger than a list of counts: every
square-valued ternary quartic over \(\mathbb F_5\) is a quadratic square
or a square-valued binary cone.

## Reproduce

Requirements: Python 3.11 or later, its standard library, and a C++20
compiler. No solver or algebra package is required. From the repository:

```sh
python3 affine_line_free_f5_3/nonzero_quadratic_moment71/verify.py
python3 -O affine_line_free_f5_3/nonzero_quadratic_moment71/verify.py
```

The verifier builds temporary executables outside the repository and
regenerates all finite data. It checks [EXPECTED.json](EXPECTED.json),
including:

* 1,081,575 planar 17-subsets, with none line-free;
* 14,348,907 quartic information words, with 10,603 retained;
* exact equality with 7,813 quadratic squares and 4,403 binary cones,
  whose intersection has size 1,613;
* 19,683 independently evaluated information words and all 930 required
  collinearity cases;
* the pointwise conic identity, the 27 centered profiles, and every
  remaining integer case in the proof, with zero unexcluded cases.

The sorted quartic catalogue hash is
`78a8dd90d77ae26d420693802ab8ba1271d17ff4d4fe0403e7c8204cc412d42a`.
No raw catalogue or build artifact is published. To run the complete
enumerations with address and undefined-behavior sanitizers:

```sh
python3 affine_line_free_f5_3/nonzero_quadratic_moment71/verify.py \
  --cxxflags='-O1 -g -fsanitize=address,undefined -fno-omit-frame-pointer -no-pie'
```

The code rejects malformed matrices, incomplete enumeration counters,
missing completion markers, and a deliberately deleted family member.
All mathematical checks remain enabled under Python optimization.
`--write-expected` regenerates the summary; it is not needed for replay.

The result is computer assisted, with source/compiler trust and no
proof-assistant formalization. The previous 71-point low-plane theorem,
the 72-point SAT exclusions, and the affine asymmetry theorem are
contextual dependencies only; none is assumed in this proof.
See [SOURCES.md](SOURCES.md) for provenance.
