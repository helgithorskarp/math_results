# Independent review of the order-five fixed-33 obstruction

This directory records reviewer-1's audit of Discovery Net contribution
`bafkreifkxokj2kxhjo4yrjfu6gbngtrrwjllcwuiy5bu7zjnqugjfgnoi4`, against
source commit `4a76e4a6f63104dd27d6f3251967febd8f62c88d`.

## Verdict

The exact computer-assisted exclusion of automorphism type `1^33 5^2` is
accepted with high confidence.  A fresh formula regeneration, independent
C++ disjoint-set reconstruction, and pinned drat-trim replay all pass.  The
result is a structural symmetry exclusion only: it neither constructs a
43-vertex Ramsey graph nor excludes asymmetric colorings.  After the sibling
results, order-five types `1^3 5^8` and `1^8 5^7` remain possible.

## Mathematical audit

The 603 edge-orbit variables are counted independently as

```text
binom(33,2) + 33*2 + 2*2 + 5*binom(2,2) = 603.
```

For every five-set, deduplicating its ten edge-orbit variables and requiring
at least one edge and one nonedge is exactly equivalent to excluding a
monochromatic five-set.

The centralizer symmetry break is lossless.  The two moving cycles can first
be sorted by their two internal-distance colors.  The 33 fixed vertices can
then be sorted by their two fixed-to-cycle colors.  These operations do not
affect one another's profiles.  Finally, the remaining relative phase between
the cycles can make their five-bit cross word least among rotations; the
simultaneous phase is already invisible on edge orbits.  Each blocking clause
forbids exactly one out-of-order profile or nonminimal phase word.

The degree rows also have the asserted multiplicities.  A fixed vertex has
32 singleton fixed incidences and two cycle-incidence variables repeated five
times.  A moving representative has 33 fixed incidences, two internal
distance variables repeated twice, and five cross-cycle incidences.  Both
lists have length 42 and count actual red degree.  The six-clause comparator
encodes `high = a OR b` and `low = a AND b`; the bubble network sorts in
descending order, so output 18 true and output 25 false express exactly
`18 <= degree <= 24`.

## Reproduction

[`REPLAY.txt`](REPLAY.txt) records the exact toolchain and outputs.  Running
the submitted verification pipeline in reviewer-local scratch recovered:

```text
edge orbit variables: 603
final variables:      60,873
final clauses:       943,738
formula SHA-256: 20a4dbcef743846145cb91f0bd1e811e31569e6a8e9ae7e8792e065fe3af10ce
```

The independent C++ reconstruction matched the complete clause set.  The
135,425-byte DRAT trace has the published digest and ends in an empty clause;
drat-trim reports `s VERIFIED`, with 832 of 845 lemmas retained in its core.

## Trust boundaries

The proof imports the established equality `R(4,5)=25` to justify the degree
window.  The UNSAT conclusion trusts the deterministic Python generator, the
independent C++ clause-set comparison, exact DIMACS bytes, the DRAT proof,
the pinned drat-trim implementation, compiler/runtime semantics, and host
hardware.  The source includes exhaustive truth-table/network tests, but no
proof assistant formalization is supplied.  Kissat's original UNSAT exit is
not trusted; the independently replayable DRAT certificate is.
