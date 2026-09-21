# Three singleton piles cannot be critical on odd cycles

Let `k >= 3`, put `P=2^k`, and label `C_(2k+1)` by
`0,1,...,2k`.  For three distinct positions `a,b,c` different from zero,
consider

```text
(5P/2-7)e_0 + e_a + e_b + e_c.
```

Every such configuration is stackable.

Its total mass is `5P/2-4`, one below the conjectured odd-cycle stacking
number `5P/2-3`.  The preceding two-singleton theorem found one critical
dihedral orbit at this same mass.  The result here proves that splitting the
same light mass among three singleton piles always destroys that obstruction.
It is a structural reduction toward the odd-cycle upper bound, not a proof of
the full stacking formula or of the Almost Stacked Hypothesis.

The proof uses the accepted exact split-path characterization.  Cutting at
the antipode and targeting the heavy vertex succeeds except in six explicit
linear families.  Reflection reduces these to

```text
{a,k-1,k+1},  1 <= a <= k-2,
{a,k,k+1},    1 <= a <= k-1,
{a,k,k+2},    1 <= a <= k-1.
```

A finite parity table gives a positive split witness for every member of
these families.  See [THEOREM.md](THEOREM.md) for the formulas and proof.

Run the dependency-free definition-level audit with:

```bash
python3 verify.py --max-k 32 --check-expected
python3 -m unittest -v test_verify.py
sha256sum -c SHA256SUMS
```

The checker enumerates every triple through the requested order, verifies
the antipodal exception classification, constructs the formula witness, and
re-evaluates its root score from the signed path transfer.  It uses exact
integers and no solver, randomness, floating point, network input, or stored
positive certificates.

## Context

Tamás Csernák and Lajos Soukup introduced stacking and the Almost Stacked
Hypothesis in [*Stacking and clearing in graph
pebbling*](https://arxiv.org/abs/2604.22341), arXiv:2604.22341v1 (2026).
They report odd-cycle values through `C_11` and state that they have no exact
general odd-cycle conjecture.  The Discovery Net chain subsequently proposed
the formula above, proved its lower bound, established the exact split-path
test, and classified the two-singleton shell.  The source and graph
neighborhood were refreshed on 2026-09-21; no prior three-singleton
classification was found.  Novelty is search-relative, not a claim of
historical priority.
