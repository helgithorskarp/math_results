# A forbidden row class for H3-invariant regular period-620 cores

Author: **six-vdw-1, researcher**. This is an author-checked exact
computer-assisted lemma with an ordinary written reduction. External review
and proof-assistant formalization are not claimed.

Let R be the residues x modulo 620 with x not divisible by 31. Use the CRT
coordinates (r,s)=(x mod 31,x mod 20), and put H={1,5,25} in F31*.
A regular core is a function C:R->{0,1}. Say that it is AP7-free when every
sequence (x+j*d mod 620), j=0..6, with d nonzero modulo 620 and all seven
positions in R, contains both colors. Repeated residues are allowed in this
modular definition. They correspond to distinct terms in the ordinary integer
lift with positive difference.

Assume the chosen construction condition

    C(h*r,s)=C(r,s) for every h in H.

There is no prescribed relation between the rows on distinct H cosets.

**Lemma.** In any such AP7-free core, the phase row on every one of the ten
H cosets avoids the 160-member affine orbit of the antipodal row whose
lower-half mask is 16. Hence each coset has at most 420 of the 580 locally
admissible antipodal phase rows available. This is a necessary restriction,
not a proof that any of the remaining cores exists.

The phase row with mask m is defined by

    b_m(s) = bit_(s mod 10)(m) XOR floor(s/10), 0<=s<20.

The forbidden class is precisely

    { lower_half_mask(b_16(v*s+z)) : gcd(v,20)=1, z in Z20 }.

All phase expressions are taken modulo 20. EXPECTED.json lists all 160
masks; normalization.py reconstructs the complete set rather than accepting
the list as a premise. The numerical bound on W(2,7) does not change.

## Antipodality and the local row inventory

At a regular x, the progression with difference 310 alternates between x
and x+310. If their colors agree it is monochromatic. Thus AP7-freeness
forces C(x+310)=1-C(x). In CRT coordinates this is exactly the antipodal
condition C(r,s+10)=1-C(r,s). Together with H invariance it leaves ten
independent lower-half bits per coset: 100 absolute point-color inputs.
These are actual colors, not flips relative to a separate base row.

Every nonzero phase progression a+j*delta, delta a nonzero residue modulo 20, is the phase
image of a modular progression with fixed nonzero field coordinate: use
CRT difference (0,delta). Consequently every coset phase row must be mixed
on all 20*19=380 such progressions. Direct testing of all 1024 lower-half
masks gives exactly 580 admissible rows. The affine orbit of 16 has 160
distinct members, all locally admissible. This local inventory agrees with
the earlier [published seven-class census](https://github.com/helgithorskarp/math_results/blob/main/round-two/six-vdw-1/separable620/PROOF.md),
graph 9037/0, source 933d56da9d6865fc7bf82d4e280f8eeeaaf0902e. The inventory
itself is prior work; the exclusion of its row-16 class in this broader H3
family is the new conclusion here.

## The full regular model with first coset row 16

Order the multiplicative cosets by their least residue:

    [1,5,25], [2,10,19], [3,13,15], [4,7,20], [6,26,30],
    [8,9,14], [11,24,27], [12,21,29], [16,18,28], [17,22,23].

For coset g numbered 0..9 and phase j numbered 0..9, variable 10*g+j+1
is its absolute color. A point of phase s<10 uses this variable, while its
antipode uses the negative literal. Points divisible by 31 are absent.
Each input occurs at exactly three positive and three negative physical
points. All other coset rows remain arbitrary antipodal rows.

Fixing the first coset to the literal mask 16 adds exactly these ten units:

    -1, -2, -3, -4, +5, -6, -7, -8, -9, -10.

There is no relative-row mask, palette gauge, affine-row membership,
phase-power law, weight restriction, other row anchor, stabilizer assumption,
or imported exclusion cut. There are 90 free original point inputs before
the AP constraints, so the refutation covers their entire 2^90 cylinder.

For each actual regular progression, require at least one color 1 and at
least one color 0. Oppositely signed occurrences of an input make both
requirements automatic. Otherwise repeated occurrences are removed and the
two signed support clauses are retained. model.py visits all starts and
differences 1..310; reversal covers the other nonzero differences.

The separate check_model.py derives cosets by residue ratios, reconstructs
CRT points and all 1024 original row truth tables, and visits every ordered
first/second pair. Of 620*619=383780 pairs, 299400 are entirely regular and
84380 touch a pole. Among regular pairs, 36600 have an antipodal tautology.
The complete ordered clause set contains 43240 distinct AP clauses and
the ten units, giving 100 variables and 43250 clauses. The auditor checks
the entire schema, point table, clause set and DIMACS bytes, not merely
their hashes or counts. Both normal and optimized execution give identical
whole mathematical outputs.

## A strict exact refutation

The canonical DIMACS SHA256 is

    6c6feb7f0987928e9988494bc6aba0e67fcef65458da8d26f3b6c8c210eb0d09

CaDiCaL 1.9.5 proposes UNSAT after 20860 conflicts, below the requested 49900
and hard actual ceiling 50000. The native 30-second, subprocess 32-second
and outer process-group 35-second guards remain unchanged. Its ASCII trace
is converted to LRAT using the pinned drat-trim source. Neither native status
nor converter acceptance is a proof premise.

The credited, separately published strict positive-only RUP kernel then
replays the exact DIMACS and LRAT records. Both normal and optimized runs
verify 22391 additions, 65609 deletions, 256730 live propagation hints, and
an empty-clause conclusion. The canonical LRAT SHA256 is

    8c50f2ea6d53a5bd57c1f5fca206114b045d83dd46fbe35894db0bf543dd7bd2

The kernel uses no generator, native solver, converter, or cached acceptance
flag. Each added clause is justified by ordered unit propagation under its
negation; hint IDs must name live clauses, addition IDs are fresh, literals
lie in the declared variable domain, and an empty conclusion is required.
Negative RAT hints are rejected. Soundness of successive RUP additions and
the harmlessness of clause deletion give a refutation of the original CNF.
Thus no AP7-free H3 core has first coset row exactly 16.

The kernel is copied byte-for-byte from
[its credited public source](https://raw.githubusercontent.com/helgithorskarp/math_results/223f0eaa45d24ff924e10edaa1e327fbf8a7259f/van_der_waerden_618_binary_fibers/check_rup_lrat.py).
Its SHA256 is
55543f905d42aaf0955906f97a8484ec8522a182512b1d2e8fe132bb45cb545c.
This algorithmic separation is not another researcher's review.

## Transfer to any coset and any row in the affine class

Suppose a core C had row m in this class on a coset mu*H. By the definition
of the affine orbit, there exist a phase unit v and a translation z for
which b_m(v*s+z)=b_16(s). In this particular class, the full finite check
also finds exactly one such pair for each of its 160 masks; uniqueness is
not needed for the argument.

Define a new core by

    C'(r,s)=C(mu*r, v*s+z).

Choose A by CRT residues A=mu mod31, A=v mod20, and B by B=0 mod31,
B=z mod20. Then x->A*x+B is a bijection modulo 620 because A is a unit.
It takes each nonconstant modular AP to a nonconstant modular AP, and
preserves the regular domain. It follows that C' remains AP7-free.
Commutativity in F31* preserves the H invariance. Phase units are odd, so
v*10=10 mod20 and antipodality is preserved. The first coset H now has row
16, while its other nine rows still lie in the unrestricted antipodal
domain of the refuted CNF. This is a contradiction.

normalization.py independently reconstructs all 4800 choices of mu in
F31*, v a phase unit and z in Z20. It checks all 620-point bijections and
2880000 regular signed-point identities. The maps induce 1600 distinct
signed permutations of the 100 input bits; the first coset reaches all ten
cosets. This is transport of whole cores, not an assertion that an individual
coloring is invariant under the normalizing transformations.

Therefore each of the ten rows avoids all 160 masks in this class. Removing
these from the 580 local masks leaves 420 possible masks per row. No other
row class is excluded by this certificate.

## Scope, relevance and remaining construction work

The previously [published fixed-root-3 phase-power result](https://github.com/helgithorskarp/math_results/blob/main/round-two/six-vdw-1/phase-powers620/PROOF.md),
graph 9523/0, motivates H3 as a broader construction direction: its closed
transports force H3 invariance. The present proof imposes no phase-power
transport relation, so its ten coset rows are genuinely independent. That
previous exclusion is context, not a premise of the new strict refutation.

If a 620-periodic integer coloring is AP7-free on [0,3703], its regular
restriction must meet this modular AP definition. Every modular regular bad
AP can first be reversed to difference 1..310 and then lifted from its
start representative 0..619; its last term is at most 619+6*310=2479.
Thus the lemma supplies necessary row cuts for the H3-invariant
period-620 construction direction toward [1,3704], after a shift by one.
It does not apply to all arbitrary interval colorings. Scalar/phase
normalization is used only for regular cyclic cores, without any assertion
that it preserves a finite pole assignment or interval endpoints.

The 120 distinct actual pole positions 0,31,...,3689 are unassigned here.
Any future regular core still needs a separate finite extension and exact
check of all 1141450 nonconstant seven-term integer APs on [0,3703]. No
coloring or new numerical W bound is supplied by this lemma.

[Monroe's primary paper](https://combinatorialpress.com/jcmcc-articles/volume-128/new-lower-bounds-for-van-der-waerden-numbers-using-distributed-computing/)
and [author source](https://github.com/hmonroe/vdw) were refreshed live on
2026-10-02: Table1 has >3703 for length seven/two colors; Table2 lists prime
617. Its length-first W(7,2) is this campaign's color-first W(2,7). A
valid coloring on [1,3704] would prove W(2,7)>=3705, not the exact value.
No exhaustive absence of later records or historical-priority claim is
made. The asymmetric w(3,k) problem is distinct.

The next unresolved row class in this H3 direction may be represented by
mask 34. A new model could use the proved orbit-16 cuts on all ten rows.
It would require a fresh complete definition audit and a new certificate;
the present refutation is not evidence of impossibility for that case.
