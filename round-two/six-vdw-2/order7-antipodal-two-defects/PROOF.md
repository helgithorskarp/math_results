# Exact two-exception phase lemma

Let c:F_617^*->{0,1} be invariant under H=<3^88>, order seven, and
avoid every nonconstant seven-term field AP whose terms are all nonzero.
Put y_i=c(3^i), i mod88, and s_i=y_i XOR y_(i+44), i mod44.
The new lemma is **sum(s) notin{2,42}**.

Negation shifts the quotient by44 since -1=3^308. For a prescribed
phase, write y_i=X_i and y_(i+44)=X_i XOR s_i, i=0..43. Each AP
support imposes its two NAE clauses. Substitution gives signed literals
on44 variables. Opposite signs on one variable make a clause
tautological; only such tautologies and duplicate clauses are removed.
Global color exchange fixes X_0=0 without changing any phase.

For K=2, exactly two phase entries are one; for K=42, exactly two are
zero. Write the exceptional indices as u,v in Z/44. Rotation by one
endpoint anchors it at zero; select the endpoint for which the positive
cyclic gap is d=min(v-u,u-v), interpreted in 1..22. The canonical
exception set is{0,d}. A quotient rotation is actual field scalar
multiplication and preserves every AP constraint. When representatives
cross the lower/upper half boundary, X_i may change by s_i; because
all X_i are freely modeled this loses no orientation. Color exchange
then fixes X_0=0. Selecting the shorter gap uses endpoint exchange
and rotation, not inversion of the field.

Thus22 normalized44-variable CNFs cover each whole class. The21
separations 1..21 have phase rotation orbit 44; separation22 has orbit 22,
so21*44+22=946=binomial(44,2) labeled phase profiles. Each has2^44
orientations before color/rotation normalization. The classes K=2/K=42
are disjoint, with 16642207998017536 labeled words each.

The generator uses primitive powers, spacing-one APs and all scalar
shifts. The auditor constructs H-cosets and their negatives by literal
group multiplication, without generator labels. It traverses all 380072
ordered(a,d), d!=0, discards4312 zero-containing APs and retains 375760.
Only identical signed-coset supports are aggregated, yielding26488
signatures; identical signatures impose identical clauses under every
phase. Semantic signed substitution independently reconstructs and
compares every complete44-model clause set plus the normalization unit.
This is complete field-AP coverage, not sampling. The known phase-zero
QR orientations pass both positive controls. Exhaustive small words
check1404 normalizations per kind, supplementing the universal argument.

Every one of the44 complete models has a strict positive-RUP
refutation. Under negated literals of an added clause, replay of active
unit/conflicting hint clauses reaches contradiction. Each addition
therefore follows from the original CNF; deletion preserves the
induction, and the checked empty clause proves UNSAT. All101701
additions and 1018620 propagation hints are replayed in normal and
optimized Python. Unsupported negative RAT hints, unavailable/deleted
used hints, out-of-domain literals, malformed syntax and missing empty
conclusions are rejected. Explicit guards remain active under -O.
Native solver/converter messages are not proof premises.

For the combined corollary, import the preceding H7 lemma excluding
K=1,43,44. When K=0, c is invariant under H and -1; their generated
subgroup has order 14. Import the order>=11 classification to conclude
that such c must be ordinary QR up to color exchange. For a nonquadratic
admissible coloring, these older results and the new K=2/K=42 cuts give
3<=K<=41. Each antipodal H-coset pair has14 points, so the counts
of agreement and disagreement under negation are14(44-K) and 14K,
each in 42..574. The new lemma does not need the older mathematical
exclusions; only this combined corollary imports them.

This is a same-author exact computer-assisted proof, not an independent
peer review or proof-assistant formalization. Its trust boundary is
the published code and SHA-pinned helper sources, Python/runtime,
elementary coset/phase-cover argument, and the explicit prior premises
only for the corollary. QR remains valid, remaining nonQR phase weights
are not excluded, and no [1,3704] coloring, full H7 classification or
interval W bound follows. W(2,7) means two colors/seven terms.
