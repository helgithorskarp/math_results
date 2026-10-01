# An order-eight logarithmic-defect cut at modulus 617

Actual author: **six-vdw-2**, role **researcher**, 2026-10-01.
Status: an exact computer-assisted lemma, with separate encoding and proof
checkers. External review and proof-assistant formalization are pending.

Let F be the field of order 617. The number 3 is primitive, and
616 = 8 * 77. Put H = <3^77>, the unique multiplicative subgroup of order
eight. Suppose c:F* -> {0,1} is H-invariant and has no monochromatic
progression a,a+d,...,a+6d with d != 0 and every term nonzero in F.
Define the cyclic word y_i=c(3^i), with i in Z/77Z, and

    E(c) = #{i in Z/77Z : y_i = y_(i+1)}.

**Lemma.** E(c) >= 13. Consequently,

    #{x in F* : c(3x) = c(x)} >= 104.

This is a necessary condition on the residual order-eight construction
family. It does not decide whether this family contains an AP-free pattern,
classify arbitrary interval colorings, or change a bound for W(2,7).
Throughout, W(2,7) means two colors and seven terms.

## Exact finite model

H-invariant colorings are exactly the 77-bit words y. A nonzero x=3^e
has coset coordinate e modulo 77. For every permitted (a,d), let S(a,d)
be the set of coset coordinates of its seven terms. Collapsing repeated
coordinates preserves the condition that both colors occur. The two clauses

    OR(y_i : i in S(a,d)),  OR(NOT y_i : i in S(a,d))

are therefore equivalent to progression freedom on the punctured field.
Progressions through zero are omitted; no color at zero is fixed.

The generator normalizes the difference to one: multiply the progression
by d^-1, enumerate its start, then add the quotient coordinate of d to
every occupied coset. This covers every permitted (a,d). The independent
auditor instead labels x by its quotient image x^8, whose kernel is H,
and enumerates all 617*616 = 380072 original pairs directly. It omits
exactly 4312 zero-containing pairs and retains 375760 pairs. Both produce
exactly the same 23177 coset supports, with rank counts

    rank 4: 77; rank 5: 231; rank 6: 4543; rank 7: 18326.

This is an entry-level comparison of the complete constraints, not a
comparison of aggregate counts alone.

## Complete normalization and the defect counter

The number of color changes around a binary cycle is even, since returning
to its starting value requires an even number of toggles. Thus E(c) is
odd because 77 is odd, and every cyclic word has an equal adjacent pair.
Rotate that pair to coordinates 0,1 by multiplying field coordinates by
a power of 3, then complement colors if necessary to make y_0=y_1=0.
These operations preserve the complete AP constraints and E(c). The two
unit clauses enforcing these values lose no candidate in the claimed
bounded family.

Introduce z_i iff y_i=y_(i+1), including the wrap from 76 to 0. Its four
CNF clauses are the exact equality truth table. The assumption E(c)<=11
is enforced by a forward prefix counter with variables s_(i,j),
1<=i<=77, 1<=j<=12. Its clauses say:

* z_i implies s_(i,1).
* s_(i-1,j) implies s_(i,j).
* z_i and s_(i-1,j-1) imply s_(i,j), for j>=2.
* s_(i,j) is false for j>i, and s_(77,12) is false.

Induction on i shows that any satisfying assignment must set s_(i,j)
true whenever at least j of the first i inputs z are true. Thus 12 true
inputs force the forbidden s_(77,12). Conversely, if at most 11 inputs
are true, assigning s_(i,j) its actual prefix-count value satisfies every
clause. These forward implications give an exact existential encoding
of the bound, despite not including reverse implications.

The resulting CNF has 1078 variables and 48556 clauses. Its SHA256 is
`29c6b68844ea2a82dc9b2e9e25ddb28a145956a3aeec697fbe93dcbb8c0214a9`.
The independent auditor checks every clause against this mathematical
model. Exhaustive counter checks cover 3586 inputs at dimensions 1..8;
the equality gadget is checked on all eight assignments.

## Checked contradiction and quantified conclusion

A bounded CaDiCaL 1.9.5 run proposes a DRAT refutation. A pinned DRAT-trim
converter produces a trace containing only positive RUP hints. The small
Python checker imports neither the solver nor the encoder. For each added
clause it assumes that clause false and replays the cited unit clauses
until a contradiction. Such a clause is entailed by the current formula;
deletions preserve this inference rule. A checked empty clause establishes
unsatisfiability. Negative RAT hints, missing clauses, unsupported syntax,
and an absent empty conclusion are rejected.

The reference replay checks 84215 additions and 2000751 propagation hints.
Its trace SHA256 is
`8c3febf1cf122cae2bf65131b6f670a27158939ec3539a4114ada64dcf32f360`.
This excludes E(c)<=11. Since E(c) is odd, it proves E(c)>=13. Each coset
contains eight elements, proving the 104-element conclusion.

For exact coverage, each odd subset D of cyclic adjacent positions determines
two binary words, interchanged by global complementation: keep the color on
D and toggle outside D. The cycle closes because 77-|D| is even. This is a
bijection between those words and their equal-pair sets with a chosen first
color. Hence the excluded labeled family has size

    2 * sum(binomial(77,k), k=1,3,5,7,9,11)
      = 13690868597134.

These are 77-coset templates, not that many unrestricted interval colorings.
No attainment at E=13 is established. The unrestricted order-eight system
timed out in a 30-second probe; a different, library-counter E<=13 probe
returned UNKNOWN at 150000 conflicts. Neither supplies an exclusion.

## Trust boundary and provenance

The proof requires the written field/counter/symmetry bridges, the published
auditor and positive-RUP checker, and Python's exact integer arithmetic and
runtime. Solver and converter soundness are not premises once the trace
passes the checker. Regeneration needs Python-SAT and a C compiler, but no
private input. The bulky generated CNF/DRAT/RUP files are omitted and stay
in the user's work directory. Their hashes and expected replay counts are
compact evidence, not replacements for regeneration and checking.

The RUP checker is reused byte-for-byte from six-vdw-1's published
[period618 three-AP work](https://github.com/helgithorskarp/math_results/tree/main/van_der_waerden_618_three_ap_obstruction).
Its file SHA256 is pinned in expected.json. That work's mathematical
period618 results are not premises here. The previously published
[order11 rigidity](https://github.com/helgithorskarp/math_results/tree/main/van_der_waerden_617_order11_rigidity)
identifies order eight as an unresolved residual family; its proof is not
used to establish the present conditional lemma.

Multiplicative prepartitioning is established prior work in
[Heule, Section 4.3](https://www.cs.cmu.edu/~mheule/publications/JOC_08_03_A01.pdf).
[Monroe, Tables 1 and 2](https://combinatorialpress.com/jcmcc-articles/volume-128/new-lower-bounds-for-van-der-waerden-numbers-using-distributed-computing/)
list the >3703 seed and modulus 617, using W(length,colors).
[Herwig et al.](https://www.cs.utexas.edu/~marijn/publications/waerden.pdf)
give cyclic construction context. These primary sources and bounded
617/618/defect graph searches were refreshed on 2026-10-01. The exact
order-eight defect cut was not found in that comparison; no historical
priority or exhaustive latest-record assertion is made.
