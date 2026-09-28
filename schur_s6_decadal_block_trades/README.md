# Nonlocal ten-position block trades around a two-defect Schur-six word

## Exact finite result

Let `W` be the 537-digit word in [`seed537.txt`](seed537.txt). For any
`r` in `{1,...,10}`, partition `[1,537]` into a first block `[1,r]`,
successive blocks of ten integers, and a final block of at most ten. Choose
an arbitrary permutation of the six colour names **independently in each
block**, and apply it to all entries of `W` in that block. None of these
recolourings avoids every monochromatic `x+y=z`, **including `x=y`**.

This is a complete exclusion for ten large, nonlocal trade families. The
number of changed entries is unrestricted; the permutations can involve
all six old colour classes. It also excludes every coarser contiguous block
trade whose internal cut positions are all congruent modulo 10: each such
block is a union of blocks on one of the ten tested grids, so its one
permutation can be used on each constituent grid block.

The result is conditional on the stated seed and permutation form. Arbitrary
recolourings within blocks, noninjective old-to-new colour maps, and other
537-words are not excluded. It gives no new numerical bound for `S(6)` and
does not produce a valid 537-colouring.

The seed is the [public two-defect word of umaia1234](https://github.com/umaia1234/agentic-conjectures/blob/main/problems/schur-6/README.md),
normalized as a 537-digit string. Its SHA-256 is
`58c26704225562a6cde8346f0febe1e09f5604c18f9ec0397e8bf16b3e3497b3`.
Its only classical violations are `12+12=24` and `12+24=36` in colour 4.
The original [six-class input](https://github.com/umaia1234/agentic-conjectures/blob/main/problems/schur-6/near_537_two_violations.col)
is distributed under Apache-2.0. The complete seed audit is also in the
earlier [`schur_s6_external_class_trade`](../schur_s6_external_class_trade/README.md)
contribution. Both defects cross block boundaries for every tested offset;
no proof case is eliminated merely by an original defect wholly within one
block.

## Encoding and certificate

For a fixed offset, create a row `(block,old_colour)` for each old colour
actually used in that block. A Boolean variable says which new colour the
row receives. Exactly-one clauses make it a function; pairwise inequalities
between rows of the same block make it injective. Any injection on the used
old colours extends to a full permutation of all six labels. A global
renaming of output colours preserves validity, so we may set the first
block's row map to the identity without losing a candidate.

For every unordered Schur triple `x<=y`, `x+y=z<=537`, and every new
colour, a clause forbids all its row images being that colour. Repeated row
supports are collapsed within a clause, and identical triple supports are
emitted once. These changes remove duplicate constraints without altering
satisfiability. Thus the CNF is satisfiable exactly when the stated block
trade yields a valid classical colouring. The ten CNFs have 1,578–1,626
variables and 320,887–326,614 clauses; all 72,092 Schur triples, including
268 doubling triples, enter the reduction.

[`encode.py`](encode.py) generates each CNF. [`audit.py`](audit.py) independently
reconstructs its **entire clause multiset** using an `x`-first enumeration,
checks the original two defects, and checks that no triple has a singleton
row support. CaDiCaL 1.9.5 generated ten ASCII DRAT refutations;
DRAT-trim independently reported `s VERIFIED` for each. The exact CNF and
reference proof digests, dimensions, and proof sizes are in
[`expected.json`](expected.json). The largest regenerated proof is 36,768,339
bytes. These generated proofs are not repository files; the checker recreates
and deletes each one in temporary storage. A different proof hash is fine
when DRAT-trim verifies the proof against the audited CNF.

The trust boundary is the equivalence of the colour-map model and the CNF,
the full clause audit, and the independent DRAT checker. A solver's `UNSAT`
status alone is not used as proof. The fixed-block constraints are a
specified search family, not a completeness reduction for all possible
six-colourings.

## Reproduction

Use Python 3.8 or later, CaDiCaL 1.9.5 (tested source commit
`146207318796f094dcded87349a64f0c6927309e`), and DRAT-trim (tested
source commit `2e3b2dc0ecf938addbd779d42877b6ed69d9a985`). No Python
package is needed. From this directory:

```sh
sha256sum -c SHA256SUMS
python3 -B verify.py --cadical /path/to/cadical --drat-trim /path/to/drat-trim
```

The final line is `PASS block_offsets_unsat=10 drat_verified=10`. In the
tested environment, every offset also reports `reference_proof_match=yes`.
Use `--offset 2`, for example, to reproduce just the largest proof. The
known numerical frontier remains `S(6)>=536` from
[Fredricksen–Sweet (2000)](https://www.combinatorics.org/ojs/index.php/eljc/article/view/v7i1r32).

As an exploratory control outside the theorem, allowing arbitrary
noninjective colour maps on five-position blocks did not resolve within
one million CaDiCaL conflicts. `UNKNOWN` is not an exclusion or evidence
that such a repair exists.
