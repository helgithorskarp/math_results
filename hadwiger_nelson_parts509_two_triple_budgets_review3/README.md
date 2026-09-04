# Independent review of two Parts triple repair budgets

Verdict: **accepted and verified**.  For each deletion triple

```text
R1 = {374,375,383},       R2 = {396,412,479},
```

every addition of at most six vertices from the specified 168-point `Q5`
pool leaves the induced unit-distance graph four-colourable.  The same is true
after any further deletions from `S`.

This is a load-bearing intermediate lemma: it supplies budget-at-least-seven
justifications for two of 817 higher-order constraints in an unfinished local
`a=6` certificate.  It does not verify the other constraints, finish that
certificate, or construct a five-chromatic graph below 509 vertices.

Reviewed Discovery Net contribution:
`bafkreidbiortofxbb2yajjal6m4so5wq23wik4gjaakwmaq42dpm73drqa`, source commit
`7f6686b3ebd2d9ce15794b241792c911b2410af2`.

## Reduction audit

For a stored proper colouring, let `E` be its deleted subset of `Q5`.  The
colouring covers the full graph on

```text
L union (S minus R) union (Q5 minus E).
```

Therefore an addition set `A` that made
`L union (S minus R) union A` non-four-colourable would have to meet every
stored `E`; otherwise the corresponding colouring restricts to the desired
graph.  Conversely, Boolean variables selecting pool points encode such a
transversal with one positive clause for each `E`.  The forward prefix counter
forces its seventh counter after any seven selected points, and forbidding
that counter imposes cardinality at most six.  UNSAT thus rules out every bad
`A`.  Removing more vertices can only restrict an already proper colouring,
which proves the stated monotonic extension.

The factor directions and quantifiers in this argument are correct: `A` must
be disjoint from at least one `E`, while a countermodel to the theorem would
hit them all.  No completeness property of the 20 stored `L` interface
classes is used; only the explicitly indexed colouring in each witness is
needed.

## Independent exact checks

[`independent_check.py`](independent_check.py) imports no code from the target
verifier or its exact-geometry module.  It reads the independent scale-96
integer table for the original 509 Parts points and parses the completion
coordinates directly as `Fraction` vectors in
`Q(sqrt(3),sqrt(5),sqrt(11))`.  After rescaling to denominator 288, direct
all-pairs field arithmetic finds 677 distinct selected points and exactly
3,400 unit edges.  The canonical edge-list SHA-256 is
`64a0f52154cb05b657a320c16569316cd1cba90748ed6dff71d4f45ca862b550`.

Every one of the 930 plus 485 stored colourings is reconstructed and checked
on every surviving exact unit edge.  The checker confirms that the only
deleted `S` vertices are precisely the relevant triple, that all other dots
belong to `Q5`, that the `E` sets are nonempty and distinct, and that only 13
of the explicit `L` colourings are referenced.  The `E` sizes range from 10
to 46 for `R1` and 8 to 34 for `R2`.

A separately written prefix-counter generator reproduces the two source CNFs
byte-for-byte:

| Triple | witnesses | variables | clauses | CNF SHA-256 |
|---|---:|---:|---:|---|
| `374,375,383` | 930 | 1,323 | 3,234 | `e4baa3fc9947c31a065fecd6a49fc4377a1281759f576e46f684692f4e8768f8` |
| `396,412,479` | 485 | 1,323 | 2,789 | `fedf92e241f9434222c015d18e603d6e778490edbccf02601526980f87d0ac0d` |

For every length one through eight, every smaller cardinality bound, and
every Boolean input assignment, the checker verifies the intended counter
extension when the bound holds and derives a unit-propagation conflict when
it fails.  This covers all 3,586 assignment/bound cases and independently
checks the counter semantics rather than relying on the matching CNF hashes.

Finally, fresh Kissat 4.0.4 runs regenerated the exact two recorded DRAT
proofs.  A separately built `drat-trim` accepted both, including 388 and 145
RAT lemmas respectively.  Tool commits, binary hashes, proof hashes, sizes,
and compact checker statistics are recorded in
[`PROOF_REPLAY.txt`](PROOF_REPLAY.txt).  The generated 12.6 MB and 1.7 MB
proofs remain under the reviewer temporary directory rather than in git.

## Reproduction

The independent geometry, colouring, CNF, and counter checks need Python 3.11
or later and the standard library.  From the repository root:

```bash
PYTHONDONTWRITEBYTECODE=1 python3 \
  hadwiger_nelson_parts509_two_triple_budgets_review3/independent_check.py \
  | cmp - hadwiger_nelson_parts509_two_triple_budgets_review3/EXPECTED_OUTPUT.txt
cd hadwiger_nelson_parts509_two_triple_budgets_review3
sha256sum -c SHA256SUMS
```

To regenerate and replay the UNSAT proofs, run the target verifier with
SymPy 1.14, Kissat 4.0.4, and `drat-trim`, placing `--work` under a suitable
scratch directory as documented in the target README.

## Trust boundaries and uncertainty

The geometry check trusts the committed scale-96 Parts coordinates and exact
completion-point coefficient lists; it does not independently derive those
coordinates from the original geometric construction.  It reimplements all
field multiplication, exact distance tests, colouring assembly, and CNF
generation.  The positive witnesses do not depend on the claimed completeness
of any interface classification.

The UNSAT conclusions trust the regenerated CNF bytes, Kissat proof output,
the independently built `drat-trim`, ordinary hardware, and the small Python
checker.  The argument is not proof-assistant formalized.  The earlier claim
that adjoining all of `Q5` is non-four-colourable is compatible context but is
not required for this lower-bound proof.  Most importantly, the review says
nothing about the remaining 815 higher-order constraints or whether the local
`a=6` certificate can ultimately be completed.
