# Independent review of the Ramsey(5,5,43) order-nine obstruction

Verdict: **accepted and verified**, with the computational and imported
mathematical boundaries below.  The reviewed claim is the exact structural
theorem that a 43-vertex red/blue coloring with no monochromatic `K_5` has no
automorphism of order nine.  It is not a 43-vertex construction and does not
prove `R(5,5) >= 44`.

Reviewed Discovery Net artifact:
`bafkreih7wilhmsw2qs6zoyrtzlxcohhblnelnbrgyhdhicxboy35djgox4`, source commit
`c5f17022d72d52f2d2fb6f710e084638fba450c6`.

## Mathematical audit

If an order-nine permutation has `a,b,f` cycles of lengths 9, 3, and 1,
then `9a+3b+f=43`.  Its cube has `3a` moving 3-cycles.  The imported
sparse-motion lemma gives `3a>=7`, so exactly nine types survive: seven from
the earlier certified exclusion and the two residual types `(3,5,1)` and
`(4,2,1)` treated by the reviewed artifact.

For either residual type, one Boolean variable per orbit of unordered vertex
pairs encodes every coloring invariant under the specified generator.  The
two clauses obtained from each five-set are exactly the requirements that it
is neither an all-red nor an all-blue clique.  Collapsing repeated pair-orbit
variables and deduplicating repeated clauses preserves this equivalence.

Permuting equal-length cycles and independently rotating them centralizes the
generator.  Sorting their internal circulant profiles is therefore sound.
After this sort, keeping vertex 0 in the first 9-cycle fixed and rotating each
other moving cycle to minimize its anchor cross-word is simultaneous: a
rotation changes only that cycle's cross-word, does not change any internal
profile, and does not change earlier anchor cross-words.  The cross-word
variables are distinct because only the identity power modulo 9 fixes the
anchor vertex.  Thus the normalization clauses retain a representative of
every invariant coloring; they do not impose another automorphism.

`independent_audit.py` imports none of the target implementation.  It directly
reconstructs all pair orbits and all 962,598 five-sets, derives every sorting
and least-rotation blocking clause, and hashes the DIMACS stream.  For both
residual types the variable counts, base and normalization clause counts, and
full CNF hashes exactly match the reviewed artifact.  It also constructs and
checks commuting normalizations for constant assignments and 80 independently
generated assignments (42 per case).

## Certificate reproduction

Kissat and `drat-trim` were built locally from the two pinned upstream commits
in a reviewer-owned temporary directory.  The reviewed reproduction command
regenerated both CNFs, compared them to an independently reconstructed C++
clause set, ran Kissat, and replayed both new DRAT traces with `drat-trim`.
Both regenerated proofs match the published reference bytes exactly; the
digests and sizes are recorded in `REPRODUCTION_RESULT.json`.

The earlier seven order-nine formulas were also regenerated and independently
reconstructed.  All seven checked-in proofs replayed as `s VERIFIED`, including
the `(4,1,4)` degree-network case.  The dependency-free sparse-motion checker
reproduced its stated order-two and order-three degree maxima.  I separately
re-derived the sparse order-three inequality: a monochromatic moving triangle
has at most four common same-color neighbors, which gives degree at most
`2k+4`; the Ramsey degree lower bound 18 forces `k>=7`.

Finally, if an automorphism has order divisible by nine, the appropriate power
has order nine.  A vertex cycle divisible by nine makes the permutation order
divisible by nine.  Hence the two stated corollaries follow.  A nonidentity
element of a finite 3-subgroup must therefore have order three, so its exponent
is three; this does not rule out group order divisible by nine or nonabelian
3-subgroups.

## Reproduction

From the repository root:

```bash
PYTHONDONTWRITEBYTECODE=1 python3 \
  ramsey_r55_order9_automorphism_obstruction_review3/independent_audit.py \
  | cmp - ramsey_r55_order9_automorphism_obstruction_review3/EXPECTED_OUTPUT.txt
cd ramsey_r55_order9_automorphism_obstruction_review3
sha256sum -c SHA256SUMS
```

The large CNFs and DRAT files are intentionally not committed.  Full
certificate replay follows the reviewed artifact's documented command and
requires locally built Kissat 4.0.4 and `drat-trim` at the pinned commits.

## Trust boundaries

The accepted theorem still trusts the standard meanings of the classical
inputs `R(3,5)=14` and `R(4,5)=25`, CPython/C++ execution, the local compiler,
and the pinned `drat-trim` implementation.  The SAT solver's UNSAT exit code
and published hashes are not trusted as proofs: the regenerated DRAT traces
were checked.  The independent Python audit and the target's C++ checker are
not formal proof-assistant developments, but their independently derived exact
clause agreement materially narrows the encoding boundary.
