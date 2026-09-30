# Attainable primitive-partition budgets and a closed prime-cube formula

Actual author: **six-covering-3**, role **researcher**, structural/combinatorial
covering lane. These are written elementary proofs with exact author controls.
No independent review, historical priority, covering construction, complete
period43200 exclusion or numerical LCM improvement is claimed.

This refines the partition portion of the author's
[primitive-block capacity lemma](https://github.com/helgithorskarp/math_results/blob/main/number_theory/distinct_covering_primitive_block_capacity/proof.md),
source234569d6f32f1ad96958ed3300050d9ce7acef1e, graph7420
(bafkreif6bscwv7wqq4m26wb2ryapjmbifo6f3usxbegdlj7mnzcbihn46e).
That lemma proved the necessary partition budget and the square-of-prime
formula. It left realization of independently maximizing block phases
unclaimed. We prove realization and reduce the prime-cube case to two budgets.

## Definitions and physical units

Let N=B p^c, B>=2, c>=1, p prime, gcd(B,p)=1. Put rho=rad(B) and T=B/rho.
Assume b|T and Q=b p^c. CRT writes a Q-periodic nonnegative weight on the
physical residues moduloN as W_z(t), z modulo p^c, t modulo b. The values may
be real; the code handles nonnegative integers exactly.

There is one top resource of each modulus B p^j, j=0,...,c. Its actual phase
a_j determines a primitive-block label q_j=a_j modT and a cofactor phase
r_j=a_j mod p^j, with r_0=0. A block in the B coordinate is

    q + T ell,  ell modulo rho.

At a fixed cofactor fibrez, define

    k_q(z) = #{j : q_j=q and z=r_j mod p^j}.
    h(k)   = k for k>=2, and0 otherwise.

The **useful top mass** is the sum of the weights of actual top-class points
whose primitive block has at least two active top classes. Points are counted
once for each top class containing them. Thus it counts multiplicity. Since
each compatible top class has exactly one physical point in that fibre and
its weight is constant on the primitive block, its mass is exactly

    A((a_j)) = sum_q sum_z h(k_q(z)) W_z(q modb).

This is not the weight of the literal top-class union.

For a partition pi of {0,...,c}, put

    k_G(z) = #{j inG : z=r_j mod p^j},
    F_c(W) = max_{pi,(r_j)} sum_{G inpi}
               max_{t modb} sum_z h(k_G(z)) W_z(t).

These are physical top-resource mass units. In particular, F_c is not
multiplied by N/Q in the physical inequality below. Its maxima are finite.

## Exact realization theorem

**Theorem1.** Under these hypotheses,

    F_c(W) = max_{all actual top phases (a_j)} A((a_j)).

Moreover, a maximizing set of actual phases can be chosen with a_j modB in
{0,...,b-1}, constant within groups. This is a statement about useful mass;
it does not assert that those phases admit a covering completion.

**Proof.** Any actual phases partition the indices by equality of q_j.
For each group its weight is evaluated at the single common t=q_j modb.
Replacing that value by the group's maximum and then maximizing the cofactor
phases gives A<=F_c.

For the converse choose a maximizing partition and cofactor phases, and for
each group choose an attaining t_G modulo b. The elementary functionh is
superadditive:

    h(u+v) >= h(u)+h(v),  u,v nonnegative integers.

If u+v<=1 both sides are zero; otherwise the left side is u+v and the right
side is at most u+v. By induction the same holds for any number of terms.

Merge all groups choosing the same t. For eachz, the merged active count is
the sum of the previous counts. Superadditivity and nonnegativity of W_z(t)
show that the sum of group charges cannot decrease. There are at mostb
merged groups, with distinct chosen t values.

Since b|T, the integers t=0,...,b-1 are available distinct block labels q=t.
For every j in the merged group of labelq choose a_j by

    a_j=q modB,  a_j=r_j mod p^j.

CRT supplies a unique phase modulo B p^j. Its block label is exactlyq and its
weight phase is t=q. These actual phases realize the merged charge, at least
the old optimumF_c. The upper bound already proved gives equality. QED.

The previous independent group maxima therefore introduce **no loss in the
useful-mass maximum**. It remains a necessary covering budget, and it can
still exceed what a covering completion can realize together with all other
resources. No compatibility or cover-existence conclusion is added.

**Support-aware version.** In A, replace the condition of at least two active
classes by the condition of at least two *distinct actual B-coordinates* in
the primitive block. Count the retained top points with class multiplicity
as before. Call this mass A_distinct. Then

    max_{actual top phases} A_distinct = F_c(W).

Indeed, A_distinct<=A<=F_c. Start from the maximizing partition and equal-phase
merging just proved. In each merged group the cofactor footprints
{z:z=r_j mod p^j} are nested or disjoint. Form their inclusion forest, connecting
each footprint to the closest strictly larger footprint present in the group.
Color each root0 and each child with the opposite color to its parent.

For everyz, the active footprints form a chain. If its length is at least two,
it contains an edge of that inclusion forest and hence both colors. If its
length is at most one, its useful charge is zero. In the group of block labelq
choose actual B-coordinates

    t_j=q+T*color(j).

They lie in0..B-1 because rho>=2. Their block label remainsq and their weight
phase remainsq modb because b|T. CRT with the same r_j produces actual top
phases. In each fibre all k>=2 active classes now have two distinct physical
positions, while all their weights remain W_z(q). Thus A_distinct attains the
full merged F_c charge. This construction uses only two positions per block,
independently ofc.

The primitive-period sign argument can ignore a block whenever its top
classes occupy at most one actual B-coordinate: the other footprints meet
its demand by the same one-exception-point argument. The support-aware
useful-mass maximum therefore shows that this strengthening of the ignored
blocks alone leaves the worst-case F_c budget unchanged. It still counts
class multiplicity, and it is still not a top-class union bound.

## Explicit prime-cube formula

Now c=3. For r modulo p and u modulo p^2 define

    U1_r(t)=sum_{z=r modp} W_z(t),
    U2_u(t)=sum_{z=u modp^2} W_z(t),
    M1=max_{r,t} U1_r(t),  M2=max_{u,t} U2_u(t),
    M3=max_{z,t} W_z(t).

For r modulo p, u modulo p^2, s modulo p^3 let

    alpha(r,u)=1 if u=r modp, and2 otherwise,
    beta(r,u,s)=1 if s=r modp or s=u modp^2, and2 otherwise.

Set the coupled common-block budget

    K3=max_{r,u,s,t}
           [2U1_r(t) + alpha(r,u)U2_u(t) + beta(r,u,s)W_s(t)].

**Theorem2.** The fifteen-partition optimization has the closed form

    F_3(W) = H3(W) := max(K3(W), 2M1+2M3).

**Proof.** When all four indices are in one group, the index0 class is active
in every fibre. The other footprints are a modp cosetC1, a modp^2 cosetC2 and
one point{s}. Their useful charge is their union weight plus their three
individual weights. C2 is either contained in or disjoint fromC1. The point
is either in their union or outside it. This gives precisely the displayed
linear expression forK3.

Any partition other than a pair-and-pair partition has at most one group of
size at least two; its singleton groups have zero charge. Add all the other
indices to that group, retaining its cofactor phases. Pointwise h(k) is
nondecreasing, so some common-block choice has at least its old charge.
Maximizing gives an upper boundK3. This covers one block, triple/singleton,
pair/two-singletons and all-singleton partitions.

For a pair{i,j}, i<j, its intersection is either empty or the finer modp^j
coset. Both classes are active precisely there. Maximizing compatible phases
and the block weight gives exactly2M_j. Thus the three pair-and-pair
partitions give

    {0,1}|{2,3}:  2M1+2M3,
    {0,2}|{1,3}:  2M2+2M3,
    {0,3}|{1,2}:  2M3+2M2.

Every modp^2 coset is contained in a modp coset, so nonnegative weights give
M2<=M1. The independent cofactor phases of two disjoint index pairs do not
constrain one another. Their group maxima can therefore be attained
independently in the definingF_3 optimization. Both K3 and the first
pair-and-pair value occur among its partitions, and all other values are
bounded by their maximum. QED.

The extra pair budget is necessary. Taking onlyK3 would be an incorrect
replacement forF_3.

## Strict fixture and actual useful-mass realization

Take B20,p3,c3,b2. Then rho10,T2,Q54,N540. Set

    W_z(0)=1 for z=0 mod3, and0 otherwise;
    W_1(1)=4, and all other W_z(1)=0.

At t0 the all-in-one-block maximum is 2*9+3+1=22. At t1 it is4*4=16.
Therefore K3=22. But M1=9 and M3=4, so

    F_3=H3=26 > K3=22.

Actual top phases (20,0),(60,0),(180,1),(540,1) have block labels0,0,1,1.
The first pair contributes18 useful mass in the nine mod3 fibres; the
second contributes8 atz1. Literal physical progression counting confirms26.
The separated-position phases (20,0),(60,42),(180,1),(540,163) also attain26
in A_distinct: their B-coordinates are0,2,1,3. The block label of each first
pair remains0 and each second pair remains1, with two distinct positions in
each useful block.
This fixture is a component comparison, not a distinct covering at540 or an
exclusion there. The earlier square-of-prime formula cannot be transferred
unchanged to the cube.

## Consequence for covering completions

Let R be the distinct actual unused eligible divisors ofN and contain
S_c={B,Bp,...,Bp^c}. A completion may use any subset ofR, one phase per selected
modulus. The weight is nonzero and vanishes on all prescribed classes.
Let D_N be its total physical weight, and

    C_n=max_a sum_{x=a modn, x modN} w_N(x).

The prior primitive-block argument gives the necessary inequality

    D_N <= sum_{n inR outside S_c} C_n + F_c(W).

For clarity, its proof uses blocks q+T ell at every cofactorz. Every resource
outside S_c has a proper B-part m=gcd(B,n)<B. A missing prime exponent supplies
a prime l|rho with m|B/l. Its footprint in a block is invariant under
ell -> ell+rho/l and hence has proper local period. If at most one top class
is active, the primitive-period sign lemma applied to the other weighted
footprints minus the constant block weight shows that they alone meet the
block demand. If at least two are active, ordinary weighted counting charges
the useful top mass. Sum the blocks, fibres and other actual resources, each
charged once. Missing top classes can be adjoined with arbitrary phases.
The full sign proof and its classical ancestry are in the linked prior source.

Theorem1 makes the top component exact, and for c3 Theorem2 substitutesH3.
This does not turn the necessary whole-cover budget into a sufficient
condition. It requires no earlier period exclusion or exponent barrier.

The cube formula also has a direct LP epigraph. Ordinary progression
epigraphs give M1 and M3 on the base moduli bp andQ. Introduce h at least
each displayed K3 linear expression and at least2M1+2M3. For a fixed weight
the least such h is exactlyH3. Ordinary epigraph variables for bp andQ must
be included even when those gcd groups have zero ordinary resource
coefficient. The code here evaluates formulas; no cube LP, numerical
exclusion or solver certificate is claimed.

Potential applications, with all eligibility/support hypotheses still needed:

| Physical periodN | B | p | c | b | Q |
|---|---:|---:|---:|---:|---:|
|15120|560|3|3|8|216|
|43200|1600|3|3|80|2160|
|43200|1600|3|3|160|4320|

For15120, Q216 is coprime to35. A prefix prescribing any class modulo35
admits no nonzero Q216-periodic weight vanishing on that class: CRT makes
every base residue meet it in the physical period. Thus that parameter row
must be used before such a class is prescribed, or with another justified
decomposition; it is not a direct replacement for a later15120 search model.

For43200, the existing Q3600 five-square weights do not meet this ternary
block-period hypothesis unchanged: their B-side period includes25, whereas
T160 includes only one factor5. New weights would have to satisfy the stated
support and periodicity conditions. These rows settle none of those periods.
The ongoing pure235 period43200 root remains open. Global exactly-eight
candidates remain10080,15120,20160 among the checked campaign inputs.

## Reproduction and trust boundary

Python3.10+, standard library only, from repository root:

~~~bash
python3 -B number_theory/distinct_covering_primitive_partition_realization/check.py
python3 -B -O number_theory/distinct_covering_primitive_partition_realization/check.py
~~~

The checker compares the defining partition maximum to all raw cofactor-phase
and base weight-phase label tuples for eight specified integer matrices,
including exponents1..4. Labels in this oracle run through0..b-1. It separately
counts actual useful physical progression mass
at the constructed CRT phases, checks the cube formula where applicable,
verifies the strict fixture, keeps genuine covers admissible, and rejects
malformed hypotheses. The compact expected manifest records exact counts
and weight hashes. Explicit exceptions remain active under optimization.
Its20-second control limit raises without a proof conclusion if incomplete.

The compact manifest records289971 complete raw phase/block-label tuples,
eighteen genuine-cover weights, ninety literal outside-resource maxima and
seven rejected hypotheses. The exponent-four case tests all52 set partitions.
All eight alternating-color CRT witnesses separately attain the support-aware
maximum using at most two positions per block. The constant-position witnesses
have zero support-aware mass, which checks the distinction between the two
definitions.

The universal results are the written proofs; the finite controls supplement
the implementation. The proof is unformalized, and the code is ordinary exact
CPython. No solver, orbit library, private frontier or external generated data
is required. No graph review of this contribution is asserted.

Classical primitive-period and CRT ancestry follows the prior proof, including
Filaseta–Ford–Konyagin–Pomerance–Yu and Ekhad–Fraenkel–Zeilberger. Their method
is not presented as new. The extra step is the explicit equal-phase merging
and prime-cube partition reduction; no historical-priority determination is
claimed.
