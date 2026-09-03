# Independent audit of the Albertson r=27 frontier

This directory independently checks Theorem 1.3 of Ankan Sadhu,
[*Albertson's Conjecture Holds for r at Most 26*](https://arxiv.org/abs/2609.01682v1).
That theorem says that a 27-critical graph `G` with
`cr(G) < cr(K_27)` must have order 53 or 54 and connected complement.

## Verdict and scope

The reduction is correct, conditional only on the cited published graph-theory
bounds.  The proof's new join bound was checked line by line.  Its two cases
are exhaustive: a component of the complement either is a singleton or none
is; the first case legitimately applies the Barát--Tóth subdivision-free edge
bound after deleting the corresponding universal vertex, and the second case
minimizes a convex sum over component chromatic numbers at the boundary
`(3,...,3,r-3(t-1))`.  The displayed algebra and positivity range are correct.

The clean-room program `verify.py` then checks, using exact rational arithmetic:

1. every order `32 <= n <= 96` and every sampling size `4 <= k <= n`, rather
   than trusting the paper's grouped table, leaving exactly `n=52,53,54`;
2. the new disconnected-complement edge floors and every sampling size at all
   three remaining orders, excluding every disconnected-complement case;
3. Gallai's `n <= 2r-2` consequence, which then removes `n=52`;
4. the residual edge counts: `m in {713,714,715}` at `n=53`, and `m=726` at
   `n=54`; and
5. all relaxed Gallai component profiles at `n=52,53,54`, including the two
   orders omitted from the exhaustive profile cross-check in the authors'
   supplementary script.

The per-order optimization also slightly strengthens the paper's weakest
ordinary excluded case: at `n=55`, `k=25` gives
`15530749/2530 = 6138.63...`, whereas the table's interval-wide choice `k=26`
gives `4208147/690 = 6098.76...`.  This refinement does not remove either
remaining order.

The profile enumeration deliberately admits even-order `3`-critical blocks,
which are not realizable (real ones are odd cycles).  It is therefore an
over-enumeration: successfully bounding every emitted profile cannot hide a
real counterexample.

This audit does **not** prove Albertson's conjecture at `r=27`.  It validates
only the reduction to the stated two-order connected-complement frontier.  It
also does not reprove the substantial imported theorems from first principles.

## Reproduction

Python 3.9 or later is sufficient; there are no third-party dependencies.

```sh
python3 verify.py
```

The first and last output lines are:

```text
PASS independent exact audit of arXiv:2609.01682v1, Theorem 1.3
final frontier: orders [53, 54], connected complement
```

The computation is deterministic and uses `fractions.Fraction`; it has no
floating point, solver, randomness, external data, or imported project code.

## Sources and trust boundary

- Sadhu, [arXiv:2609.01682v1](https://arxiv.org/abs/2609.01682v1), especially
  Lemma 2.2, Proposition 3.2, and Theorem 1.3.
- Büngener--Kaufmann,
  [arXiv:2409.01733v2](https://arxiv.org/abs/2409.01733v2), Theorem 6(b), for
  `cr(G) >= 5m - 203(n-2)/9` without a density hypothesis.
- Barát--Tóth,
  [EJC 17 (2010), R73](https://www.combinatorics.org/ojs/index.php/eljc/article/view/v17i1r73),
  Lemma 3 and Corollaries 7 and 11.
- Kostochka--Yancey,
  [JCTB 109 (2014), 73--101](https://doi.org/10.1016/j.jctb.2014.05.002), for
  the unconditional critical-edge bound.
- Gallai, *Kritische Graphen II* (1963), for the join decomposition below
  order `2r-1` and the small-order edge bound.  The exact formulations used
  here are also restated as Lemmas B and G in
  [arXiv:2512.08020](https://arxiv.org/abs/2512.08020).

The executable trust boundary is CPython's integer arithmetic and
`fractions.Fraction`.  The mathematical trust boundary is the cited imported
theorems and the elementary reduction encoded here.  The authors' own
supplement was run separately and passed all 72 checks, but it is corroboration
only and is not used by this program.

## Strengthening and improvement opportunities

1. **Exploit equality at `(n,m)=(54,726)` (highest impact).**  Classify equality
   in the Kostochka--Stiebitz excess bound under 27-criticality and connected
   complement.  Any structural feature incompatible with connected complement
   or forcing one additional edge closes the entire order-54 branch.
2. **Raise the order-53 edge floor from 713 to 716.**  Three edges suffice for
   the present crossing inequality.  A targeted refinement using the connected
   complement, or exclusion of the equality/near-equality critical families,
   would close order 53 without improving crossing-number technology.
3. **Sharpen the crossing inequality locally.**  At `(54,726)`, the current
   method needs only the next integer edge threshold, 727.  Equivalently, the
   paper computes that replacing `203/9` by `22.53`, or `5` by `5.004`, is
   enough.  A theorem for this narrow density/order regime would bypass a full
   equality classification.
