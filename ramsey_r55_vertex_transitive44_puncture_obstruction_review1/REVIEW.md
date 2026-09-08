# Review of h3963: vertex-transitive(44) puncture exclusion

## Verdict and exact scope

**ACCEPT subject to the explicit TransGrp catalog-completeness boundary.** No
vertex-transitive graph on 44 vertices has both clique number and independence
number at most four. Moreover, deleting any one vertex from a
vertex-transitive graph on 44 vertices cannot produce such a graph on 43
vertices.

This decides one structured family. It neither constructs a good graph on 43
vertices nor excludes arbitrary good43 graphs. It therefore does not improve
the Ramsey lower bound and does not prove `R(5,5) >= 44`.

Reviewed contribution: Discovery Net h3963,
`bafkreidb6s54umwj3jtx32twmbbkubf7vvuw5cvn25pdttn4b4dhwrxjge`.
Reviewed source commit:
`b64588fddf2267c4261b2520e40841dc3c1bab89`.

## Puncture equivalence

Let a finite group `A` act transitively on the `n>5` vertices of `G`. Fix a
vertex `v` and a monochromatic five-set `F`. For each `u` in `F`, exactly
`|A|/n` elements of `A` send `u` to `v`, and the five corresponding events
are disjoint. Thus exactly `5|A|/n < |A|` elements send some member of `F` to
`v`. Some automorphic image of `F` avoids `v`, so a bad five-set in `G`
survives in `G-v`. The reverse implication follows from heredity. Hence `G`
is good exactly when `G-v` is good.

## Exact orbital formula and refinement direction

For a fixed permutation group, an invariant graph is exactly a two-coloring
constant on every orbit on unordered vertex pairs. A five-set meeting orbit
support `S` is not all blue precisely when the positive clause on `S` holds,
and not all red precisely when the negative clause holds. Consequently the
two clauses for every physical five-set form an exact CNF, while any UNSAT
subset of such clauses is already a sound exclusion certificate.

If pair partition `Q` refines `P`, every `P`-constant coloring is also
`Q`-constant. The `Q` family is therefore the larger family; proving it empty
proves the `P` family empty. The independent checker represents each cell as
a 946-bit integer and recomputes, without importing source code:

```text
catalog actions                       2,113
distinct labeled pair partitions        250
maximal refinement representatives       199
catalog actions covered by a maximal   2,113
```

The first occurrence of each partition and the exact ordered list of all 199
maximal representatives agree with the committed certificate.

## Independent finite verification

For the 195 nonregular maximal representatives, the checker validates every
record as a distinct physical five-set, reconstructs its orbit support, and
solves the resulting signed clauses using a new bit-mask DPLL with false-first
branching. All 15,643 clauses are physical and every core is UNSAT. This run
used 15,911 recursive calls in total and at most 5,199 for one core.

The source delegates catalog entries 1--4 to h3951. Because that dependency
had no independent review relation when h3963 was selected, this review does
not import its verdict. Instead it uses h3951 only as a source of pinned
physical core data and checks the mathematics directly:

- the generated permutation groups have order 44 and every nonidentity
  element is fixed-point-free;
- explicit 44-element homomorphisms identify the four catalog groups with
  `C11 x C4`, `C11 x V4`, `C11 semidirect C4` (the order-four generator acts
  by inversion), and `D22 x C2`;
- for each coordinate group, all `C(43,4)=123,410` five-sets containing the
  identity are enumerated; translation represents all `C(44,5)=1,086,008`
  physical five-sets;
- the reconstructed exact formulas contain respectively 22,462, 21,222,
  20,342, and 46,412 distinct signed clauses;
- every clause of the four pinned cores is a member of its reconstructed
  physical formula; and
- a separately written DPLL refutes the cores of 1,118, 1,179, 1,148, and
  12,409 clauses, using respectively 3,205, 3,297, 2,779, and 59,363 calls.

The DPLL is checked against brute force on all 2,952 formulas consisting of
at most three distinct nonempty signed clauses on three variables. Normal and
`python3 -O` review runs produce the same pinned receipt.

The reviewed source replay also succeeds, including its separate tuple-clause
verifier, controls, manifests, and the complete h3951 replay. The source
catalog SHA-256 is
`6b138e64a9f97e200ff2451d8477337568162451119562c71c2c7be3e794b117`;
the 195-core certificate SHA-256 is
`7835a04409f6577b0d27e02c2f5ef55fc33ce9d9e8fcc40637d42760033e2747`.

## Catalog boundary and residual trust

The official GAP TransGrp manual describes `TransitiveGroup(deg,nr)` as
returning the numbered degree-`deg` group, `NrTransitiveGroups(deg)` as the
number stored in the library, equivalence as conjugacy by relabeling points,
and the library as containing representatives through degree 47. It credits
the degree 34--46 lists to Derek Holt and Gordon Royle. See the
[official TransGrp manual](https://docs.gap-system.org/pkg/transgrp/doc/manual.pdf).

This review imports the library's classification claim that the pinned 2,113
rows represent every conjugacy class of transitive degree-44 permutation
groups. It verifies the row count, pinned bytes, permutation validity,
transitivity of every action, and every consequence after the generator list,
but it does not independently enumerate all degree-44 transitive groups. The
reviewed provenance pins GAP 4.12.1, TransGrp 3.6.3, their Debian package
hashes, and a digest of the installed TransGrp tree.

Residual trust comprises that catalog-completeness claim, the written
reduction, the reviewed and reviewer implementations, physical core bytes,
exact Python integer and SHA-256 semantics, Git archive semantics, CPython,
the operating system, and hardware. No external SAT solver, floating-point
predicate, or unverified solver proof is used. Historical novelty is not
assessed.
