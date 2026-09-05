# Complete split by the number of empty fixed signatures

Consider a hypothetical Ramsey(5,5;43) graph with an order-three
automorphism of type `1^10 3^11`. Four moving triangles C0,...,C3 are
internally red and seven are internally blue. Its ten fixed vertices
are uniform to each moving triangle. Write S(f) for the subset of the
four red triangles adjacent red to a fixed vertex f, and write z for
the number of empty signatures.

This package concerns precisely four marked-action core classes:
`131,139,162,173`. Their red offset words on pairs 01,02,03,12,13,23 are

| class | words |
|---|---|
| 131 | 100,100,100,001,010,101 |
| 139 | 100,100,100,001,110,101 |
| 162 | 100,100,110,011,010,100 |
| 173 | 100,100,110,101,010,101 |

The [preceding theorem](../ramsey_r55_order3_eleven_empty_signature)
proves z >= 1 for each: all four complementary three-triangle cores
contain a blue triangle. Its proof couples singleton uniqueness and
the fixed incidence budget to all seven majority triangles and the
full color-degree bound. The present split imports that theorem; it
does not independently establish the theorem's hand proof. Its exact
core hypotheses and witnesses are rechecked by the inherited separate
checker during preparation.

## Exhaustive disjoint branches

Label moving vertices 3i+s for i=0,...,10 and s modulo three, and fixed
vertices 33,...,42. The complete parent sorts each fixed vertex's full
eleven-bit red attachment row lexicographically, with the four minority
bits first. This also sorts the four-bit prefixes. Therefore all empty
minority signatures precede every nonempty one.

The inherited base already sets fixed vertex 33's prefix to zero.
Consequently the following conditions are equivalent in the base:

* z = 1: the four-bit prefix of fixed vertex 34 is nonzero;
* z >= 2: the four-bit prefix of fixed vertex 34 is zero.

These alternatives are disjoint and exhaustive. No additional relabeling
or normalizer is imposed. Within an equal-prefix class, the parent still
sorts the other seven coordinates. Exactly one empty signature does not
specify the other nine signatures. In particular, the equality multiset
from the three-versus-eight branch is not a premise here.

The primary red variable for triangle Ci and fixed vertex f is
`211 + 11*(f-33) + i`. The new second-prefix constraints are therefore

```text
z = 1:    222 223 224 225 0

z >= 2:  -222 0
         -223 0
         -224 0
         -225 0
```

The new auditor reconstructs these variable meanings directly from
unordered-pair rotation orbits on all 43 vertices. It separately checks
the disjoint partition on all sixteen second prefixes and the inherited
prefix-order implication on all 2,048 full eleven-bit rows.

## Entire inherited formulas

The accepted r=4 parent has 34,280 variables and 615,920 clauses, including
all 43 vertices, the full Ramsey constraints, both color-degree bounds,
local constraints, auxiliary counters and justified normalization. Its
SHA256 is

```text
c8f355b256de55727b18efcbd47ef9e777ac2b3b4ae69e09676fcddd51afa05f
```

The eighteen selected-core units and four first-empty-prefix units are
retained exactly, giving each inherited base 615,942 clauses. Each of the
four reconstructed base hashes must equal its preceding published hash:

| class | inherited complete-base SHA256 |
|---|---|
| 131 | 22bfaaff6d28f07244e6dccdb7ec48fe2cd6275ce80847c343a28a2b42f0adfb |
| 139 | 03084092d9584762a0060a5cd356a35b1a975464f3449a965eefce18069d0a76 |
| 162 | cbe92ce3388541fff99b5ea357fa19c9106b7da7dc96771368b0bdeaf90f5377 |
| 173 | 96889e7365d319ecaac07c76302289e509b5aac48dc552595c1760b2295d8f9e |

The one-empty formula has **615,943 clauses**, while the multiple-empty
formula has **615,946 clauses**; both have 34,280 variables. The complete
base body remains byte for byte intact, followed by the displayed tail.
There is no selected fixed graph, further signature count, degree profile,
majority attachment or additional automorphism.

The parent is generated from source and independently reconstructed by
the inherited C++ checker. The new base auditor reconstructs all 320
primary meanings, compares the entire parent body and all 22 base units,
and checks EOF. The new split auditor then checks the entire base body,
every new clause and final EOF. Thus a verified refutation excludes its
entire normalized full-extension subcase, not a weakened local projection.

## Certificate and coverage obligations

The fixed domain consists of all eight pairs (core, empty-multiplicity
branch). Each receives one Kissat call with a sixty-second solver limit.
There are two workers and a 300-second limit per full DRAT replay.

An UNSAT exit requires successful full DRAT verification against the
audited formula. A fresh verifier reconstructs the entire parent, all four
inherited bases and all eight final formulas, checks their exact hashes
and all primary meanings, and replays every successful proof a second
time. General RAT steps require full DRAT; a RUP-only substitute would
be insufficient for such traces.

A SAT exit must decode to a 43-vertex edge list and pass literal graph
verification before being called a target. An open case requires an
explicit UNKNOWN verdict and solver exit zero. Unexpected exits, source
drift, invalid proofs or candidates, and incomplete cases are errors,
not exclusions. Timeouts never prove nonexistence or feasibility.

The final mathematical summary respects the complete split:

* both branches refuted excludes that core entirely;
* only z=1 refuted leaves the core open with z>=2;
* only z>=2 refuted leaves the core open with z=1;
* both branches unresolved leaves the inherited z>=1 boundary unchanged.

The exact outcomes are in `result.json` and `verification.json`; the
derived core-level consequences and cumulative residual list are in
`boundary.json`. No whole-core exclusion is inferred from one refuted
branch. The other 34 four-versus-seven cores and both three-versus-eight
cores are outside this sweep.

## Checked outcome and structural corollary

Both branches of all four cores have refutations replayed twice. Thus
131,139,162,173 are excluded entirely. With the preceding seven exclusions,
all eleven then-open cores satisfying the four-blue-triangle hypothesis
are now excluded. The other 34 classes do not satisfy that hypothesis,
by the preceding complete per-core triple checks, repeated during both
preparations here. Therefore every full four-versus-seven candidate must
have a complementary three-triangle subcore with no blue triangle.
This property is preserved by every marked-action relabeling. The
corollary imports the complete core cover and preceding full exclusions;
it does not classify the full extensions of the remaining nine-vertex
subcore or change the color of the fourth red triangle.

## Controls, reproducibility and trust

Seven malformed formulas test omitted disjunction literals, using the
first prefix instead of the second, reversed disjunction polarity,
an inserted empty clause, a changed inherited prefix, a missing multiple
unit and a wrong multiple-unit polarity. All must be rejected. The
sixteen-prefix partition, 2,048-row ordering and normal/optimized Python
control reports are checked. Inherited arithmetic/counter/normalization
controls and the preceding lemma's exact application checker rerun during
both preparations.

Sources, inputs, executable hashes and resource bounds are fixed in the
run contract. Each case is saved atomically. A STOP file prevents new
cases while active ones finish; resume requires the same contract and
retains completed UNKNOWN results at their original limit. The fresh
verification directory must not already exist. Large formulas, traces,
partial UNKNOWN traces, logs and binaries stay outside Git. Public source
regenerates them; reported hashes identify evidence but do not replace
the omitted proof traces. Partial UNKNOWN traces are not certificates
or resumable solver states.

The complete parent and marked-action cover are independently accepted.
The inherited empty-signature theorem, its four-unit bridge and preceding
seven refutations still await independent review. The new split bridge
and computational results also await independent review. Other trust is
the imported R(4,5) theorem and unformalized normalization/counter reasoning,
exact Python/C++ source semantics, compiler/runtime/hardware, SHA256 and
the external full DRAT checker. Internal reconstruction is not peer
review or proof-assistant formalization. No priority claim is made.

This is one bounded milestone, ending at the eight-case sweep and fresh
verification. It neither starts another multiplicity stratum nor enlarges
a timeout. No target graph, Ramsey lower-bound improvement or global
eleven-cycle exclusion is inferred unless the exact reported evidence
actually establishes it.
