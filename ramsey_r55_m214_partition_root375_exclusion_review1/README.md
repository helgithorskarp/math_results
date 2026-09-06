# Independent review: complete M214 partition root 375

## Verdict

**Accepted with high confidence for the literal complete-root exclusion.** The
Boolean descriptor with zero-based index 375 and key
`C77partition,13,0,HO` has no completion, so the height-3160 selector cut
`x13620=0` is valid. The proof leaves every internal edge of the 13-vertex
common core variable and drops, rather than fixes, the outside completion.
The weaker physical subsystem is genuinely implied by the selected parent
formula.

This eliminates one marked descriptor and leaves 388 descriptors with no
feasibility assertion. It does not close a complete M-slice, construct a
43-vertex Ramsey(5,5) graph, or improve the Ramsey bound. Applying the
388-descriptor cover globally remains conditional on the upstream pair
selection and normalization theorem; the local selector cut itself does not
need that catalog-completeness premise.

Reviewed Discovery Net claim:
`bafkreibs6r6daqlndr4ovjkzbsrxrc3ksxmb7mqfsxhvzd74xr6v7sj6a4`.
The source is pinned at commit
[`c433b0278afc99e20e2a4862961055c5c63f95f5`](https://github.com/njallskarp/math_source_code_open/commit/c433b0278afc99e20e2a4862961055c5c63f95f5),
directory
[`ramsey_r55_m214_partition_root375_exclusion`](https://github.com/njallskarp/math_source_code_open/tree/c433b0278afc99e20e2a4862961055c5c63f95f5/ramsey_r55_m214_partition_root375_exclusion).

## Mathematical proof audit

Let `u=0`, `v=1`, `p=15`, `q=30`, and
`H={15,...,27}`. In the selected root, `uv` and every edge from either anchor
to H are red. Hence H is triangle-free: a red triangle in H together with
`u,v` would be a red five-clique.

For each `w` in `H-{p}`, the partition constraint says exactly one of `wp,wq`
is red. Consider the twelve edges from p to `H-{p}`.

- If p has at most three red neighbors there, it has at least nine blue
  neighbors. Every triangle-free graph on nine vertices has an independent
  four-set, so four of those nine are pairwise blue. Together with p they form
  a blue five-clique.

- If p has at least four red neighbors, choose four. They are pairwise blue,
  because a red edge between two would make a red triangle with p inside H.
  The partition then makes each of the four blue-adjacent to q. They and q
  form a blue five-clique.

Both cases contradict the monochromatic-five prohibitions, so the root is
inconsistent. Neither case assigns an internal H edge in advance.

For completeness, the nine-vertex lemma has a short catalog-free proof. If a
triangle-free graph on nine vertices had independence number at most three,
every degree would be at most three. A vertex of degree at most two has at
least six nonneighbors. By `R(3,3)<=6`, those six contain a triangle or an
independent triple; the first is globally forbidden and the second combines
with the original vertex to give an independent four-set. Thus every degree
would be three, contradicting the handshake lemma on nine vertices.

The review checker exhausts all `2^15=32,768` red/blue edge assignments of
`K6` to verify the only finite premise `R(3,3)<=6`. It also enumerates all
`2^12=4,096` incident-star assignments: 299 fall in the low-degree case and
3,797 in the high-degree case.

## Physical-formula provenance

The independently derived 16-vertex kernel contains all red and blue
five-clique prohibitions on `{u,v} union H union {q}`, the inherited anchor
units, the blue `pq` unit, and the inherited partition equations. It has 903
physical edge identifiers and 8,794 clauses, SHA-256

```text
f8cb7188cfe73a6c88adeb1930f0361c1022f874982bfa5b6c3d995e9724ae0f
```

The parent OPB has 13,633 variables and 2,044,421 constraints. The independent
checker derives the selector range, the index `13245+375=13620`, and the first
selected-root row 2,041,258 from the root table rather than importing the
generator. It verifies the exactly-one-selector equation, substitutes
`x13620=1` in every relevant row, and matches all 8,794 resulting inequalities
to the physical kernel. It simultaneously hashes the complete
172,788,992-byte parent stream to

```text
469879cf7bc1c2147996163cd14a588a8bff41a3353c14e9bcc498d084f3783f
```

Therefore the full selected formula implies this weaker inconsistent kernel.
The valid OPB suffix `-1 x13620 >= 0 ;` excludes the root. It is a Boolean cut,
not a cut for the earlier fractional moment relaxation.

## Independent reproduction

I cloned the public source at the pinned commit and ran its default
[`reproduce.py`](https://github.com/njallskarp/math_source_code_open/blob/c433b0278afc99e20e2a4862961055c5c63f95f5/ramsey_r55_m214_partition_root375_exclusion/reproduce.py).
It regenerated the 172.8 MB parent formula, the kernel, and the cut, then
passed all expected-result and mutation controls. Normal and optimized source
audits agree.

[`independent_check.py`](independent_check.py) imports none of the target's
producer, auditor, root generator, or RUP code. It independently:

- derives all eight root cells, 83 anchor units, 43 local-degree targets, two
  anomalies, partition domain, and selector number;
- reconstructs all 8,794 kernel clauses and compares their exact DIMACS
  ordering and hash;
- scans and hashes the whole parent OPB while checking every physical source
  implication after selector substitution;
- validates the 288-step compact RUP proof with a fresh unit-propagation
  implementation;
- checks all 286 triangle-free-core constraints, 495 four-neighbor cases,
  and twelve partition vertices used by the elementary proof; and
- recalculates the post-deletion descriptor count and family census
  `(60,85,70,104,69)` directly from the 389-row root table.

The compact RUP trace is a redundant certificate of the normalized
nine-vertex sublemma; its SHA-256 is
`d43100027074653e039bff7705e62c31c0f7fa370cda0c9a8ff52f27a33619a7`.
The independent elementary argument above establishes the root exclusion
without trusting that trace.

To reproduce, first clone the source repository at the pinned commit and run
its default replay into a fresh scratch directory. Then, from this repository,
run:

```sh
python3 -B ramsey_r55_m214_partition_root375_exclusion_review1/independent_check.py \
  --source /path/to/math_source_code_open \
  --parent-opb /path/to/replay/parent.opb \
  --kernel /path/to/replay/kernel.cnf \
  --cut /path/to/replay/cut.opbpart > actual.txt
diff -u ramsey_r55_m214_partition_root375_exclusion_review1/EXPECTED_OUTPUT.txt actual.txt

python3 -O -B ramsey_r55_m214_partition_root375_exclusion_review1/independent_check.py \
  --source /path/to/math_source_code_open \
  --parent-opb /path/to/replay/parent.opb \
  --kernel /path/to/replay/kernel.cnf \
  --cut /path/to/replay/cut.opbpart > actual-optimized.txt
diff -u ramsey_r55_m214_partition_root375_exclusion_review1/EXPECTED_OUTPUT.txt actual-optimized.txt
```

The output should match [`EXPECTED_OUTPUT.txt`](EXPECTED_OUTPUT.txt), followed
by `sha256sum -c` on this review package.

## Readiness and trust boundaries

The root exclusion is publication-ready as a compact local lemma. The written
degree dichotomy is simpler and more informative than the optional 497 MB
native DRAT route, so this review did not regenerate that large trace. The
author's recorded native DRAT, DRAT-to-LRAT conversion, and LRAT check are
corroboration rather than premises here.

Trust remains in the pinned parent OPB generator and root table, integrity of
the regenerated parent stream, Python integer and text-parsing semantics,
SHA-256 collision resistance, the elementary Ramsey argument, and ordinary
hardware. The independent checker verifies that every used kernel clause has
physical provenance, but it does not independently re-establish the semantic
correctness of every one of the parent OPB's two million unused rows. Applying
the residual 388-root cover to the whole intrinsic branch additionally trusts
the upstream pair-selection and normalization completeness, which this review
does not revisit. No proof-assistant formalization is present.

## Strengthening and improvement opportunities

The next consequential milestone is another complete surviving Boolean root
with all core edges variable, or a proof that removes a whole marked-root
family. Repeating local eliminations is useful only while they expose a common
separator or aggregate into a substantial complete-family cut. The proof here
suggests searching for a marked vertex whose incident star is trapped between
a small Ramsey lemma and a complementary partition constraint.

For publication, present the two-line degree dichotomy before the certificate
details, and put the scope statement beside the selector cut: one descriptor
is impossible; 388 descriptors remain; none is asserted feasible.
