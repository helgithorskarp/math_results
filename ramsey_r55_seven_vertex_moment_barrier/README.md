# A strict seven-vertex moment control for the good43 decision problem

**This package closes no physical Ramsey case.** It gives an exact certificate
that the particular finite moment relaxation described below is strictly
feasible. Its purpose is to preserve a failed global exclusion approach and
identify its precise limitation. The campaign frontier remains
`43 <= R(5,5) <= 46`.

A good43 is a graph on 43 vertices containing neither a clique nor an
independent set of size five. For an edge in either color, its own-color
codegree is the number of common neighbors in that color. The attempted
exclusion target was **every good43 with all these codegrees at most 10**.
Goodman's identity makes this the entire `M=10` maximum-codegree branch,
including all 313 preserved core identities in the earlier normalization.
No core was fixed and no old physical SAT formula was used.

The relaxation averages induced seven-vertex graph counts over vertex labels
and color complementation. Exhaustive enumeration gives 1,044 unlabeled
seven-vertex graphs, of which 928 avoid both forbidden five-sets. They form
464 complementary pairs. The variables are their nonnegative densities,
with total one. The conditions comprise:

- 1,584 inequalities conditioning the degree interval `18..24` and the
  own-color codegree upper bound 10 on every applicable six-vertex flag;
- 63 nonnegative integer-domain degree and codegree polynomial inequalities;
- 56 positive semidefinite count matrices, with 1,303 total rows, including
  every allowed five-root type and the maximal odd-root square counts through
  seven vertices, together with the specified degree/codegree localizers.

The supplied rational vector has 464 positive entries and denominator
`1000000173109`. All 1,647 scalar inequalities are strict. The smallest
integer numerator of a scalar slack is `317116206`. All 56 matrices are
positive definite: fraction-free integer elimination checks all 1,303
leading principal minors. This rules out an exclusion certificate formed
solely from nonnegative combinations of these scalar inequalities and
positive semidefinite combinations of these matrices. It does **not** rule
out stronger moment conditions, integer constraints on actual subgraph
counts, or other physical arguments. The rational vector is not a graph.

The finite lifting identities are derived in [METHOD.md](METHOD.md).
Direct counts in the cycle and cube on eight vertices match all 1,647
scalar rows and all 56 matrices entry by entry after finite rescaling.
These are implementation checks, not independent peer review or a formal
proof of the generator.

## Replay

Python 3.11.2 and NumPy 2.4.6 were used. The exact replay does not need a
numerical solver. Generated tensors stay in a fresh external directory.

```sh
python3 -m pip install -r requirements.txt
python3 -B replay.py --work-dir /tmp/r55-seven-moment-replay --validate-counting
```

Expected final status: `EXACT_REPLAY_MATCH`; terminal physical decisions: 0.
The certificate is [exact_density.json](exact_density.json), and exact
verification statistics and principal-minor hashes are in
[expected.json](expected.json). [verify.py](verify.py) uses arbitrary-precision
integer arithmetic for certificate checking and exact Bareiss divisions.

Optional discovery uses `requirements-discovery.txt` and `discover.py` after
generating the three tensor files in the same work directory:

```sh
python3 -m pip install -r requirements-discovery.txt
cp discover.py /tmp/r55-seven-moment-replay/
python3 -B /tmp/r55-seven-moment-replay/discover.py
```

CVXPY 1.9.2
with CLARABEL returned `optimal_inaccurate`, with a positive normalized dual
objective of approximately `1.3907652314e-7`. That status is not evidence of
feasibility: the supplied rational certificate and exact checks establish
the stated result. No floating-point assumption enters that check.

## Trust and stopping boundary

The degree interval is the elementary consequence of `R(4,5)=25`: each
neighborhood and each nonneighborhood is a `(4,5)`-good graph. The target
assumption supplies the codegree bound. No external graph catalogue, fixed
automorphism, carrier task, edge-window theorem, or conditional structural
receiver is used in the tensors. Enumeration completeness follows from
traversing every one of the `2^21` labeled seven-vertex graphs under adjacent
vertex transpositions. Complement averaging asserts no automorphism of an
individual graph.

This was pass 38, the second granted whole-physical-class pass. It missed
the terminal-coverage gate: all 431 preserved cases in branches
`M=10,11,12,13` remain unresolved. The next pass requires another genuinely
different mathematical approach. Increasing this moment order or switching
the numerical backend is not the declared continuation. All older carrier
and maximum-codegree physical formulas remain parked.

Primary source context and the overlap audit are in
[DEPENDENCIES.md](DEPENDENCIES.md). Large tensors and exploratory logs are
reproducible local artifacts and are deliberately outside this source
package.
