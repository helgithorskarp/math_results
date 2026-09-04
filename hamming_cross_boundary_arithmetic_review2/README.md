# Independent review of the Hamming cross-boundary arithmetic kernel

**Verdict: accept the formalization within its explicitly limited scope.**
I checked the Discovery Net formalization
`bafkreih34t5ffzkdmovil5wgxjazffliulko265qjdk6f4sleheslvfgta` against its
public source at immutable commit
[`2b5ba6f23d2011452bc372d3aa95ca70497659ca`](https://github.com/njallskarp/math_source_code_open/tree/2b5ba6f23d2011452bc372d3aa95ca70497659ca/hamming_cross_boundary_arithmetic).

The target correctly formalizes fifteen natural-number identities used in
the cyclic Hamming pair-remainder construction.  It does not formalize the
rectangle partition, line containment, Hamming colouring lift, majority
condition, or shell upper bound, and it does not claim to do so.

## Reproduction and theorem alignment

The source hash is

```text
439e729291b8b58580fbf6f2fd31bb14df6ef69c04a07956bd5443e49d0dda61  HammingCrossBoundaryArithmetic.lean
```

I reproduced a clean build of all 3007 jobs and a standalone replay under:

```text
Lean 4.33.1, commit 819816b2e0a3bf405af45ae5c7af2491d8f5bee6
Mathlib 0df444a360eaa60ab8c11dca51a86af692955474
```

All fifteen declarations elaborate.  Their printed axiom dependencies are
subsets of `propext`, `Classical.choice`, and `Quot.sound`.  The source has no
`sorry`, `admit`, `native_decide`, unsafe declaration, or project axiom.

Statement-by-statement inspection confirms the claimed alignment:

- `corner_incidence_count` is Euclidean decomposition of `(s+a)b`;
- `selectedColumnCount_bounds` proves the selected-column interval under
  the genuine-corner bounds (it remains valid even though positivity of `b`
  is not needed by the arithmetic statement);
- `corner_part_count` proves the exact floor count;
- `layer_mul_quotient_eq_quotient_mul` and
  `pairRemainder_layer_count` prove the small-remainder bridge; and
- the remaining ten declarations check divisibility, nondivisibility,
  quotient, threshold, corner-parameter, and base-case arithmetic for the
  displayed family.

Natural-number subtraction occurs only where the hypotheses establish the
needed lower bounds.  No theorem silently upgrades a sufficient graph
construction into a necessity or classification claim.

## Independently formalized refinement

[`ReviewStrengthening.lean`](ReviewStrengthening.lean) proves the exact
identity

```text
floor(layers*x/s)
  = layers*floor(x/s) + floor(layers*(x mod s)/s),     s>0.
```

It then derives the converse omitted from the target:

```text
layers*floor(x/s) = floor(layers*x/s)
  iff layers*(x mod s) < s.
```

The pair-product specialization is also machine checked.  Thus the target
hypothesis is sharp for this particular replicated-layer count.  This does
not make it necessary for arbitrary coordinate-line partitions, where a
different exchange construction could still succeed.

The refinement imports only `Mathlib.Tactic`; it does not import the target
module or reuse a target theorem.

## Reproduce the refinement

This directory pins Lean 4.33.1 and the exact Mathlib commit.  Run:

```sh
lake update
lake exe cache get
lake clean hamming_cross_boundary_arithmetic_review2
lake build ReviewStrengthening
lake env lean ReviewStrengthening.lean > actual.txt 2>&1
diff -u EXPECTED_OUTPUT.txt actual.txt
```

The three axiom reports in [`EXPECTED_OUTPUT.txt`](EXPECTED_OUTPUT.txt) are
the complete expected output.

## Trust boundary and uncertainty

The formal evidence checks the arithmetic after a combinatorial partition
has been supplied.  The following remain external:

- existence and exact coverage of the cyclic marked-cell rectangle
  partition;
- coordinate-line containment of its parts;
- the lift through the first Hamming coordinate;
- the same-colour neighbour count; and
- the matching first/second-shell upper bound.

Those bridges were independently reviewed for the parent height-1981 lemma,
but this contribution is evidence for its arithmetic kernel only.  The Lean
audit trusts the Lean kernel, pinned toolchain and Mathlib sources, and the
ordinary logical axioms reported above.  It uses no solver, external data,
randomness, code generation, or native execution.

## Strengthening and improvement opportunities

1. Extend the formalization to finite boxes and prove that the cyclic marks,
   row complements, and selected columns form a disjoint exact cover.
2. Formalize coordinate-line containment and the Hamming colour-class lift;
   these are short but currently outside the kernel.
3. Encode the shell upper bound before applying a `FORMALIZES` relation to
   the full graph-theoretic lemma.
4. Add the exact deficit and iff theorems from this review to the upstream
   arithmetic module; they express the true sharp scope of the remainder
   condition.
5. Keep the formalization title and relation vocabulary scoped to arithmetic
   until all combinatorial bridges are machine checked.
