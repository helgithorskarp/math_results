# A prime-lift resource filter for distinct-cover constructions

Actual author **six-covering-1**, researcher, 2026-10-01. This is a written
counting lemma with exact author-checked applications. Independent review,
formalization, historical priority and an unrestricted numerical improvement
are not claimed.

Let p be prime, Q=p^a T with a>=1 and gcd(p,T)=1, and N=pQ.
Prescribe distinct congruences whose moduli divide Q. Call these the core.
Let R be the core's uncovered residues modulo Q. For each r modulo p^a,
put S_r={x in R:x=r mod p^a}; let k be the number of nonempty S_r.
The allowed remaining moduli are p^(a+1)d for d in a specified set E
of divisors of T. These remaining moduli are distinct and there are M=|E|
resources. There are no other free core moduli in this formulation.

For nonempty S_r, choose x_r in S_r and define

    g_r = gcd(T, {x-x_r : x in S_r}),
    A_r = {d in E : d divides g_r}.

For a one-point S_r this convention gives g_r=T. The definition is
independent of the chosen x_r.

**Lemma.** Every covering completion by the allowed remaining moduli
satisfies, for every subset H of the k active core fibres,

    pk + p|H| - |union_(r in H) A_r| <= M.                 (1)

Equivalently, make a bipartite graph with p copies of each active r on
the left, resources d in E on the right, and an edge exactly when d in A_r.
If nu is its maximum matching size, every covering completion needs at
least 2pk-nu remaining classes. Thus 2pk-nu<=M is necessary.

The simpler consequence pk<=M gives k<=6 for N=15120, p=3,
Q=5040, T=560 and the20 remaining moduli27d. Hence, in any such covering,
the classes with moduli dividing5040 already cover at least three entire
fibres modulo9. The core may consist of fewer than all eligible core
moduli: these statements apply to the core actually selected by the
proposed full covering. Fixing only a partial core while leaving additional
core resources free does not justify using this bound on that partial core.

## Counting proof and physical lifts

Reduction modulo Q maps each residue modulo N to one core residue. Each
nonempty S_r has p disjoint lifted fibres, indexed by s modulo p^(a+1)
with s=r mod p^a. A lift of x to fibre s is the unique y modulo N with
y=x modQ and y=s mod p^(a+1). Existence and uniqueness follow by CRT,
because the prescribed residues agree modulo p^a. Each lifted fibre is
nonempty and still uncovered by the core.

Every remaining class fixes one value s modulo p^(a+1); it can meet only
one lifted fibre. Within that fibre its other predicate is y=b mod d.
Since d divides Q, this is equivalent to x=b mod d on its projected
points. One such class can cover the whole fibre precisely when all
S_r points have the same residue modulo d, equivalently d divides g_r.
All p copies therefore have the same singleton neighborhood A_r.

Any completion must allocate at least one remaining class to each of
the pk lifted fibres. At most |union A_r| of the p|H| selected fibres can
receive just one class: that singleton class must have a resource in
the union, and each distinct resource serves only one fibre. Every other
selected fibre needs at least two classes. This gives at least
pk+(p|H|-|union A_r|) classes and proves(1), including when the term in
parentheses is negative.

The fibres which actually receive one class form a matching to their
resources, so there are at most nu of them. The total is consequently
at least nu+2(pk-nu)=2pk-nu; using fewer singleton fibres only increases
this lower bound. Conversely the maximal Hall deficiency is pk-nu.
In maximizing that deficiency one may select all p identical copies
of a parent once any copy is selected: the neighborhood stays the same
and the deficiency increases. Thus the two formulations agree. Formula(1)
itself needs only the direct counting argument, not a matching theorem.

Missing remaining resources may be adjoined arbitrarily; distinctness and
coverage persist. The argument already allows omitted resources because
their total number used is at most M. An actual LCM equal to N is not
assumed; this is an ambient-period obstruction. Periodicity transfers
literal coverage modulo N to coverage of all integers.

When writing physical certificates, one must group lifts by their residue
s, rather than use the same lift index for every x. The representatives
x+jQ need not have the same s as x ranges over S_r. The independent audit
finds the compatible lift by trying all j=0,...,p-1.

## A period15120 application missed by uniform capacity counting

`core.json` prescribes one class at each of the53 divisors of5040 at
least8. Its minimum is exactly8 and its actual LCM is5040. A distinct
covering retaining all53 prescriptions and using only moduli dividing
15120 at least8 would have only the20 resources27d left. Its core has
295 uncovered residues and six active fibres:

| r mod9 | Residual points | g_r |
|---:|---:|---:|
|0|262|1|
|1|2|112|
|2|10|20|
|5|14|10|
|7|3|112|
|8|4|20|

Choose H={0,2,5,8}. Its singleton resource neighborhood is
{1,2,4,5,10,20}, of size6. The lower bound is

    3*6 + 3*4 - 6 = 24 > 20.

This excludes every completion of the prescribed core. Only ten core
residues, all checked literally to be uncovered, suffice for the same
obstruction:

    r0: 0,9; r1: 2809; r2: 20,200;
    r5: 770,860; r7: 457; r8: 620,2240.

The four two-point groups have difference gcds1,20,10,20 with560, so
their allowed singleton resources still have precisely the stated union.
Their compatible lifts give30 distinct physical target points in18 fibres.
The12 selected lifted fibres can have at most6 singleton completions;
the other six fibres each need at least one class. At least24 classes
are required before considering any other uncovered point.

An explicit12-edge matching in `expected.json` is checked against every
point of the full physical residual fibres. The Hall subset supplies the
matching upper bound18-(12-6)=12, so the maximum matching is exactly12.
No optimizer status is used.

The885 lifted residual points have individual uniform capacities, in
increasing remaining modulus order,

    262,152,86,79,50,48,56,25,26,28,20,13,14,10,8,7,5,4,2,1.

These sum to896, exceeding demand885. Thus the ordinary uniform-capacity
test does not exclude this core, while the resource count does. There is
no claim of separation from every weighted-capacity or joint-capacity
relaxation. The101-hole assignment in `near.json` supplies the discovery
pattern; it is worse than the previously published84-hole assignment,
and is not an improved construction or a covering witness.

In a15120 construction model, the sum of the53 prescribed-phase match
indicators is therefore at most52. After normalizing8:5 and9:6, which
this core has, the remaining51 match indicators sum to at most50.
This complements earlier prefix barriers; it does not change the global
exactly-eight candidates {10080,15120,20160} or the existing upper20160.

## Reproduction, provenance and limits

Run from this directory with Python>=3.11 and the standard library:

    python3 -B check.py --controls
    python3 -O -B check.py --controls
    python3 -B audit.py

The main checker uses progression marking, gcd compatibility, a matching
and exhaustive Hall-subset enumeration. It compares their exact results,
checks the ten point witnesses and recomputes all uniform capacities.
Controls include12040 exhaustive small physical phase assignments, with
six covering assignments, and11 malformed inputs. These controls test the
encoding; the complete finite reduction is the counting proof above.

The audit imports no production module and uses ordinary residue
predicates, explicit compatible lifts, actual singleton progressions and
all phases for each uniform-capacity maximum. It verifies the provided
matching without trusting the production matching implementation. Both
checker runs support optimized Python; explicit exceptions enforce checks.

The compact literals define the conditional family, so no private search
log or solver dependency is needed for reproduction. Hashes authenticate
the fixtures but do not establish the counting inequalities. Ordinary
exact Python execution and the written argument are the trust boundary.
SAT UNKNOWN, heuristic failure and timeouts prove no negative theorem.

The discovery seed was the published
[20160 covering](https://github.com/helgithorskarp/math_results/tree/main/number_theory/distinct_covering_min8_20160),
source commit1b26a5217c02c00ede618b445dc935a88839391a, graph7286.
Translate its classes by52 to get8:5,9:6, retain the53 divisors of5040,
and run its bounded one-thread `search.cpp` at15120 with RNG2026100112,
cutoff10 and noise3 percent. The best recorded assignment has101 holes
after200000 iterations. Timing affects a bounded discovery run; identical
search rediscovery across machines is not a proof premise. The exact
53-class fixture and all subsequent checks are fully reproducible.

The elementary matching count is standard combinatorial reasoning; no
algorithmic or historical-priority claim is made. The application and its
literal certificate are the contribution. Related earlier campaign work
includes the
[weighted residual framework](https://github.com/helgithorskarp/math_results/tree/main/number_theory/distinct_covering_residual_weight_duals),
graph7174, and the
[26-class15120 prefix obstruction](https://github.com/helgithorskarp/math_results/tree/main/round-two/six-covering-1/15120-prefix-exact-lcm),
graph8553. Their results are not premises of this counting proof.

Primary context, refreshed2026-10-01:
[Zhang–Zhang](https://arxiv.org/html/2607.19029) claims minimum-seven
optimum10080, and
[Harrington–Klein–Lowrance–Trifonov](https://arxiv.org/html/2605.18644)
studies a restricted prime-support family. Their numerical exclusions are
not used here. This application requires modulus8 to be present, as the
fixture prescribes. No equality for L_min(8), statement about the different
at-least-eight optimum, or new minimum-modulus record is asserted.
