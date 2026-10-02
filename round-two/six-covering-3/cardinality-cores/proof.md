# Fifteen exact predicates for the two-class erasure cuts

Actual author **six-covering-3**, role **researcher**, 2026-10-02.
Ordinary finite combinatorial corollary of the actually committed
[few-class erasure lemma 9241](https://github.com/helgithorskarp/math_results/blob/main/round-two/six-covering-3/few-class-erasers/proof.md),
reference `bafkreifrgrohpsbtnrgmbq5jtb53ej5uirhro65lmv762xyjzuqxmqq3he`,
source `c879ddf506e22fd0632b7e638bb15550b7f91acb`.
The source includes an independently implemented exact implication checker.
No independent reviewer verdict, formalization or priority claim is asserted.

## Statement and root scope

Let

\[
D=\operatorname{Div}(315)=\{1,3,5,7,9,15,21,35,45,63,105,315\}.
\]

Consider seven labeled sets \(H_r\subseteq\mathbb Z/315\mathbb Z\), including
empty sets. For \(B\subseteq D\), let \(Q(B)\) count those \(H_r\) which are
empty or contained in the union of at most two congruence classes with
**distinct** labels from \(D\setminus B\). One class may suffice.
Witnesses for different fibers are separate ability tests; they do not
allocate simultaneous tail resources.

**Theorem.** The entire family

\[
24Q(B)+10|B|\ge72\qquad(B\subseteq D)                         \tag{1}
\]

is equivalent to the fifteen predicates in the following table.
Each displayed pair means two distinct cofactor resource labels. A fiber
qualifies exactly when it fits one or two classes using a displayed pair;
empty fibers always qualify. All phases remain available.

|Index|B|required Q(B)|complete minimal pair family|
|---:|---|---:|---|
|0|1,3|3|5/7, 5/9, 5/15, 7/9, 7/21|
|1|1,5|3|3/7, 3/9, 3/15, 7/35|
|2|1,7|3|3/5, 3/9, 3/21, 5/35|
|3|1,3,5,7|2|9/15, 9/21, 9/35, 15/21, 15/35, 21/35|
|4|1,3,5,9|2|7/15, 7/21, 7/35, 15/45|
|5|1,3,5,15|2|7/9, 7/21, 7/35, 9/45|
|6|1,3,7,9|2|5/15, 5/21, 5/35, 21/63|
|7|1,3,7,21|2|5/9, 5/15, 5/35, 9/63|
|8|1,5,7,35|2|3/9, 3/15, 3/21|
|9|1,3,5,7,9,15,21|1|35/45, 35/63, 35/105, 45/63|
|10|1,3,5,7,9,15,35|1|21/45, 21/63, 21/105|
|11|1,3,5,7,9,15,45|1|21/35, 21/63|
|12|1,3,5,7,9,21,35|1|15/45, 15/63, 15/105|
|13|1,3,5,7,9,21,63|1|15/35, 15/45|
|14|1,3,5,7,15,21,35|1|9/45, 9/63, 9/105|

This is equivalence, not a claim that the fifteen predicates are logically
irredundant or that they are sufficient for a completing covering.

For the owned period 10080 root

\[
P=(8:0,9:0,10:1,14:1,12:10),
\]

choose exactly one phase for each of the 36 unused divisors of 2520 at least8.
Let \(H_r\) be the resulting holes in binary parent \(r\bmod8\), projected
to their cofactor coordinate modulo 315. The unused original tail moduli
are exactly \(16d\) and \(32d\), one resource at each depth per \(d\in D\).
All24 tail moduli are free. If these tail moduli complete the covering,
all fifteen predicates must hold. No 16 or 20 phase has been consumed or
normalized, and all four largest original moduli remain free.

## Empty padding and cardinality reduction

Let \(m\) be the number of nonempty parents and \(e=7-m\). For each \(B\),
let \(A(B)\) count nonempty parents coverable by fewer than three classes
with distinct labels outside \(B\). The q=3 specialization of 9241 says

\[
24A(B)+10|B|\ge12m+6\max(0,2m-6)-60.                       \tag{2}
\]

For \(m\ge3\), adding \(24e\) to both sides gives (1), because the right
side of(2) is \(24(m-4)\) and \(Q=e+A\). For \(m\le2\), both inequalities
hold automatically. This treats empty fibers without reusing resources.

The integer lower bounds on \(Q\) from(1), for \(|B|=0,\ldots,12\), are

\[
3,3,3,2,2,1,1,1,0,0,0,0,0.
\]

Since \(Q(B)\) cannot increase when \(B\) grows, it suffices to check
sets of sizes2,4,7, requiring3,2,1 fibers respectively. Conversely these
are instances of(1). If \(1\notin B\), the class modulo 1 covers any fiber,
so \(Q(B)=7\). It therefore suffices to check \(1\in B\): there are
\(11+165+462=638\) such predicates.

## Injective resource domination

For unordered distinct-label pairs \(p=\{u,v\}\), \(q=\{d,f\}\), write
\(p\preceq q\) if one bijection assigns \(u,v\) to \(d,f\), with each
smaller label dividing its assigned larger label. Given any phases at
\(d,f\), reduce them modulo the corresponding labels of \(p\).
The old union is contained in the new union. The bijection is necessary:
mapping both resources to one label would clone a resource.

For any allowed label set with at least two labels, every allowed pair
lies above a minimal pair in this finite order. A one-class witness can
be extended by an arbitrary phase at a different allowed label before
this replacement. Hence minimal pairs give exactly the same qualification
predicate as all one/two-class witnesses. Their labels remain legal.

Let \(M_i\) be the pair family for table row i. A predicate from row i
implies an original predicate for B whenever:

1. the required count in row i is at least the count required at B; and
2. for every \(p\in M_i\), some distinct-label pair \(q\subseteq D\setminus B\)
   satisfies \(q\preceq p\).

Condition 2 maps every row-i qualifying fiber to a B-qualifying fiber;
the same labeled fibers are retained, so the cardinality implication follows.
Empty fibers are retained as well.

The compact [certificate](certificate.json) gives such a row index for
**every** one of the 638 original B masks. Bit j represents label j in
the displayed increasing list D. The standalone [checker](check.py)
reconstructs the exact original universe, checks all 638 mappings and 2950
pair implications, and checks the complete pair families against all 363
original pairs in the fifteen allowed pools. It uses direct bijections
instead of the producer's frontier algorithm. It independently finds 155
distinct intermediate families and verifies each displayed minimal family.
Thus the fifteen rows imply all 638 predicates. They are themselves among
the 638 predicates, proving the reverse implication and the theorem. QED.

Literal phase-set checks on all 315 residues additionally verify 5610
divisor/phase containments and all 133055 full phase pairs for B={1,3}
under their fixed injective replacement. Only 365 phase pairs per fiber
remain for that B; the fifteen minimal families have 31037 phase pairs
per fiber in total. The ordinary containment proof applies to all sets,
not only the checked fixtures.

## Shared base-phase encoding

The [CNF generator](encode.py) retains all 9279 phase variables of the 36
original base moduli. Each modulus has exactly one selected phase, with
an ordinary sequential counter enforcing at most one. No local fiber
normalization or independent base assignment is introduced.

For each table row and parent r, a Boolean z selects that parent as a
qualifying witness. The generator permits cofactor resources appearing
in that row's minimal pairs, at most two active distinct labels, with
at most one phase per active label. An active resource implies z; if a
resource is active, one of its phases is selected. All its labels are
outside the row's B. Conversely, replacing any legal witness by a minimal
pair shows that restricting to this resource union loses no qualification.

For each original2520 residue x left by P in parent r, the point clause is

\[
\neg z\ \lor\ \bigvee_{n\in\mathrm{BASE}}X_{n,x\bmod n}
\ \lor\ \bigvee_{d\text{ permitted}}W_{r,d,x\bmod d}.       \tag{3}
\]

The same original base variables occur in all rows and all parents. Row
cardinality clauses require at least its stated number of distinct z's.
For an empty after-base fiber, no cofactor resource need be active.

If a formula model exists, its selected original base phases give a state
satisfying every table predicate: the chosen local cofactor classes cover
every remaining point in each selected parent by(3). Conversely, given
any base assignment satisfying the table, choose the requisite distinct
parent witnesses and their legal minimal-pair class phases; set all other
witness variables false. Sequential-counter auxiliaries can be extended
by prefix OR. This gives a formula model. Therefore this is a complete
finite encoding of the **necessary cut problem**.

The full formula has 46333 variables, 103984 clauses and 1056452 literal
occurrences. Its clause-body SHA256 is
`4cbef87311f79b71d1aad3282026b7c79288ddf21cff237aa6ecc025a99f7f33`.
The B={1,3} subproblem has 19327 variables/30744 clauses. The literal audit
checks every 20970 full-formula and1398 subproblem point clause against
the actual physical residue and all original resource incidences.
SAT would only supply a necessary core; passing does not allocate the
actual16d/32d resources globally. No full-formula decision is asserted.

## Literal positive subproblem control and limitations

The [small frozen control](core-control.json) specifies all 36 legal base
phases. Literal enumeration of all 10080 residues gives after-base parent
sizes

\[
(20,13,92,88,16,86,54),
\]

with 1476 physical holes. Parents1,2,5 fit respectively
\(5:4\cup9:5\), \(5:0\cup9:3\), \(5:4\cup9:5\). Thus the B={1,3}
predicate and its generated CNF have a literal positive model. Labels5
and9 are repeated across these **ability tests**, not assigned repeatedly
in an actual tail. The same full base assignment violates seven table
predicates and 135 of the 638 original predicates. Its small parent sizes
do not replace the necessary shape predicates.

The proposal was found by a 10-second/node 2000 HiGHS search with an incumbent,
while the solver returned its time-limit status. The frozen original
phases, containment witnesses and every Boolean clause are subsequently
checked exactly; the solver is neither required for replay nor a proof
of optimality or nonexistence. Large generated CNF and maps stay in scratch.

Checks cover both normal and optimized Python, 468 empty-padding cases,
six abstract literal-shape controls, this fully specified original base
assignment, twelve damaged certificates, six malformed base inventories,
six damaged Boolean models, all 255 sequential-counter primary truth cases
of lengths 0 through 7, and 1920 complete seven parent cardinality truth cases.
No negative bounded search is treated as a universal exclusion.

The q=3 predicates also do **not** replace the credited
[q=2 single-eraser cuts 9160](https://github.com/helgithorskarp/math_results/blob/main/round-two/six-covering-3/eraser-matching/proof.md).
For example, take all seven labeled fibers to be \(\{2,3\}\). This abstract
state is inside the initial P holes. Every fiber fits any two distinct-label
class resources, one through each point, so every q=3 predicate passes.
But each difference gcd is1. The prior q=2 cover C empty, B={1} has cost 3
against the required 20 and excludes completion. No realization of this
abstract state by the 36 base phases is asserted. It explains why a later
core search must retain the q=2 cuts as well as the new fifteen predicates.

Fresh complementary work by six-covering-1 is the
[110-point overlap bound and 82-point tail 9287](https://github.com/helgithorskarp/math_results/blob/main/round-two/six-covering-1/four-coset-tail-overlap/proof.md),
source `106223e6ce40150aa987e64dce7e2725df9e65d4`. It concerns a separate
period 15120 route and also excludes first-stage compatibility for that
particular tail. Its full original signed body and source proof were read;
numerical checks were not replayed and none of its bounds are imported here.

The global EXACTLY8 candidates10080/15120/20160 are unchanged, with 20160
the credited witnessed candidate. The owned root remains open and is one
of the twelve forms left by the current
[original-fourteen theorem 9239](https://github.com/helgithorskarp/math_results/blob/main/round-two/six-covering-2/aligned-twelve-fourteen-presence/proof.md).
Its aligned condition does not apply to our12:10 phase. Primary context:
[Zhang--Zhang, claimed L_min(7)=10080](https://arxiv.org/html/2607.19029),
and [HKLT restricted-prime constructions](https://arxiv.org/html/2605.18644),
both reopened 2026-10-02. These are prior art, not new claims here.
Minimum-at-least-eight remains separate. No minimum-over42 construction
or global L_min(8) bound is asserted.
