# Direct-sum locality for the Ray--West codimension-two correction

For a permutation `w` of length `m`, let `g2(w)` be the number of
permutations of length `m+2` containing `w`.  Ray and West proved

```text
g2(w) = (m^4 + 2m^3 + m^2 + 4m + 4 - 2 j(w))/2,
0 <= j(w) <= m-1.
```

This directory proves an exact decomposition formula for `j`.  It closes
the explicit `0/1` direct-/skew-sum bridge proposed in the independent
review of the layered theorem.  The proof uses the already committed
intrinsic rooted-lens formula for `j` and its lens cut lemma.

For `w` in `S_n`, define two descending endpoint indicators:

- `L_down(w)=1` when, for `b=w(1)`, the initial word of length `b` is
  `b,b-1,...,1`;
- `R_down(w)=1` when, for `a=n+1-w(n)`, the terminal word of length `a` is
  `n,n-1,...,n-a+1`.

Then for all nonempty permutations `alpha` and `beta`,

```text
j(alpha direct_sum beta)
  = j(alpha) + j(beta) + R_down(alpha) L_down(beta).
```

Thus the correction is local on direct-sum components, apart from one
explicit Boolean junction term.  Iterating gives

```text
j(w_1 direct_sum ... direct_sum w_t)
  = sum_i j(w_i) + sum_i R_down(w_i)L_down(w_(i+1)).
```

Complementation gives the skew-sum dual with increasing endpoint anchors;
see [PROOF.md](PROOF.md).

The formula strictly extends the earlier layered/colayered evaluation as an
algebraic locality rule (while the later intrinsic theorem remains the
stronger global formula).  It also gives an infinite bondless family:
`2413` is bondless, has `j=2`, and has neither descending endpoint anchor,
so

```text
j(2413 direct_sum ... direct_sum 2413) = 2t
```

for `t` summands.  The direct sums remain bondless.

## Reproduction

Only the Python standard library is required (tested with Python 3.11.2).

```bash
PYTHONDONTWRITEBYTECODE=1 python3 verify.py | diff -u EXPECTED_OUTPUT.txt -
PYTHONDONTWRITEBYTECODE=1 python3 -m unittest -v
sha256sum -c SHA256SUMS
```

The verifier uses Ray--West active insertion triples exactly and is
independent of the rooted-lens implementation used in the proof.  It checks
all 1,089 ordered factor pairs with both lengths at most four, one-sided
factor pairs through length six, the direct and skew formulas,
internal-boundary locality, the explicit junction triples, and the iterated
bondless examples.
The computation corroborates the written universal proof; it is not a
permutation-class census used as a premise.

## Scope

The theorem computes `j` recursively for direct- and skew-sum decomposable
permutations once the indecomposable component values are known.  The
committed rooted-lens theorem already gives an intrinsic formula for
arbitrary permutations, and the committed minimizer theorem already
classifies every minimizer of `g2`; neither result is reproved or superseded
here.  Codimension three is not addressed.

Primary sources and the novelty boundary are recorded in
[SOURCES.md](SOURCES.md).
