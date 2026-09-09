# Exact-frontier interface for team-hn-3

HN-2 retains construction synthesis and candidate ownership. The completed
four-module theorem is in PROOF.md and independently audited by verify.py.
It is a mathematical result with two author-run implementations; these
internal checks do not substitute for reviewer-1's independent verdict.

The next support interface concerns five modules and is **not run here**.
It is available after HN-3 completes its current h4047 rotational-sum milestone;
that separate viability result was inspected and is not a premise of this proof.
Do not repeat the four-module enumeration, start a coordinate candidate
search, or minimize an A159 gadget in parallel with synthesis.

## Concrete viability question

Let T1,...,T5 be five equilateral triangles of side sqrt(7), embedded in the
Euclidean plane. Repeated triangles and shared terminal vertices are allowed.
Suppose their union T has at most **eight distinct physical points**. Does
there always exist a proper four-colouring of the strict unit-distance graph
on T for which no Ti is monochromatic?

A useful bounded output is a proof with an exact, independently checkable
obstruction certificate, or an exact terminal configuration with a certified
non-four-colourability result for these *unit-edge plus nonmono-triangle*
constraints. Abstract counterexamples without plane coordinates remain
viability information, not a physical candidate or an HN result. A weaker
quantified necessary condition can be valuable if it rules out the eight-
terminal budget with a clearly stated, sufficient relaxation.

This is a terminal viability decision, not a search for the same candidate
family by both researchers. HN-2 has not begun the five-module phase.

## Why eight terminals matters

If five replacement modules each have 100 private vertices, then an
at-most-508 assembly leaves at most eight distinct terminals. Each has the
same equilateral sqrt(7) terminal geometry as A159. A proof of universal
terminal extension in the stated budget would exclude this specific
five-module cost regime regardless of the modules' internal structure,
provided all nonmono terminal assignments extend through each module.

No such 103-vertex negative forcing module is claimed to exist. Positive
extension survives vertex deletion; the prohibition of monochromatic
terminals does not automatically survive. Both are required before this
architecture could yield a physical record candidate.

## Exact contract and reductions available

Label the distinct terminals 0,...,n-1, n<=8. Each Ti is a three-element
subset with all three squared side lengths exactly 7. Any physical certificate
must identify coincidences, include every unit edge, and use exact coordinates.
For colours c_v in {0,1,2,3}, the logical constraints are:

- c_u != c_v whenever the squared physical distance is 1;
- not(c_a=c_b=c_c) for every listed triangle {a,b,c}.

One may encode a nonmono constraint by choosing a bichromatic pair, but the
quantifiers matter. The mixed constraints are SAT iff **there exists** one
choice of a pair per triangle whose augmented ordinary graph is
four-colourable. They are UNSAT iff **every** one of the at most 3^5 choices
is non-four-colourable. One bad selected-pair graph is not an obstruction.

The proved K5 lemma remains available with five chosen long edges: a K5
whose edges have lengths 1 or >2 needs at least six long edges. The elementary
one-neighbour-per-other-terminal-set bound also remains valid, now giving
maximum auxiliary degree at most five. The eight-vertex 4-regular reduction
from the four-module proof does not apply when the maximum degree is five.

Keep the no-extra-connector, private-interior, and terminal-only-interaction
hypotheses visible. A counterexample to this terminal question would still
need a separate negative forcing-gadget realization and full-graph exact
verification before it could establish the <=508 record target.
