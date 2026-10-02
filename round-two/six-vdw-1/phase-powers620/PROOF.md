# An exact exclusion for canonical affine phase-power cores

Author: **six-vdw-1, researcher**. Status: an exact finite-family exclusion with
separate author-written producer/checker algorithms and ordinary mathematical
reductions. External independent review and formalization are not claimed.

## The precise family

Identify Z/620 with F31 x Z/20 by x -> (r,s)=(x mod31,x mod20). A residue is
**regular** when r!=0. Fix primitive root **3 modulo31**, and let ell(r) be the
unique integer in {0,...,29} such that 3^ell(r)=r. For any binary row
`b:Z/20->{0,1}` and any affine phase permutation

`phi(s)=u*s+t mod20`, `u in U(20)`, `t in Z/20`,

define on all regular residues

`C_(b,phi)(r,s)=b(phi^ell(r)(s))`.

The logarithm is canonical. This formula is a genuine coloring even when
`b o phi^30 != b`; that extra condition is **not** imposed in the theorem.
The theorem is that **every coloring in this family has a nonconstant regular
monochromatic seven-term cyclic AP**. Each cyclic obstruction has an integer
representative entirely in [0,2479]. Consequently arbitrary pole colors cannot
repair an interval coloring on [0,3703] whose regular entries agree with a
member of this periodic family. Shifting the interval by one gives the usual
3704-point target. The primitive root is fixed to 3; no reduction over all
possible primitive roots is asserted.

This excludes the specified family only. It neither excludes arbitrary
regular period620 cores nor the larger order-three-invariant construction
family described below, and supplies no new bound for W(2,7).

## Cyclic witnesses and bounded integer lifts

A cyclic AP is given by `a+j*d mod620`, j=0,...,6, with d!=0 mod620. Choose
a in {0,...,619} and d in {1,...,619}. If d>310, reverse the progression:
replace a by `a+6*d mod620` and d by `620-d`. Thus 1<=d<=310 and the integer
terms a+j*d lie in [0,2479]. They are distinct integers, retain the cyclic
colors and avoid the poles if their residues are regular. This argument also
applies after any unit affine CRT map. It is essential when transporting a
cyclic certificate into a finite interval: a modular affine map alone need
not preserve the original integer endpoints.

## Necessary local reduction and complete phase conjugacy

Suppose a member of the family were regular-AP-free. In field row r=1 we have
ell(1)=0, so its phase row is exactly b. The actual CRT progression with step
310 alternates phase s and s+10 while retaining field residue 1. It is mixed
if and only if `b(s+10)=1-b(s)`. Thus any possible AP-free member has an
**antipodal binary row**, determined by its ten lower-phase bits, a mask m
in {0,...,1023}. Its full word is

`b_m(s) = bit_(s mod10)(m) XOR floor(s/10)` for 0<=s<20.

For every s and h!=0 in Z/20, the field-constant progression with phases
s+j*h lifts by CRT to a nonconstant regular cyclic AP. Hence b_m must be
mixed on every one of the 20*19=380 local ordered APs. The independent checker
examines all **1,024 masks** and finds exactly **580 admissible rows**.

The affine phase group has 8*20=160 elements `h(s)=v*s+z`, v in U(20).
Its orbits on the 580 rows have minimum-mask representatives and sizes:

| Representative | 8 | 10 | 12 | 16 | 20 | 34 | 72 |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| Orbit size | 160 | 40 | 80 | 160 | 40 | 80 | 20 |

These are complete disjoint orbits. For an arbitrary admissible b_m, choose
h with `b_m o h=b_rep`. Set `phi'=h^-1 o phi o h`. If
phi(s)=u*s+t, then

`phi'(s)=u*s + v^-1*(t+(u-1)*z) mod20`.

For every canonical exponent i, `phi'^i=h^-1 o phi^i o h`. Therefore

`C_(b_rep,phi')(r,s)=C_(b_m,phi)(r,h(s))`.

The map `(r,s)->(r,h(s))` is the unit affine map x->A*x+B mod620 with
A=1 mod31, A=v mod20, B=0 mod31, B=z mod20. It preserves regular cyclic APs
and nonzero differences. No field-transport closure or stabilizer-invariance
premise is needed. Thus all **580*160=92,800 admissible parameter pairs** are
covered by the **7*160=1,120** representative/map pairs. These counts concern
parameters, not necessarily distinct colorings. All other binary b are excluded
by the two necessary local tests above; their full 2^20 input pool is not
being claimed as explicitly enumerated.

The checker reconstructs the 580-row census and every orbit without importing
the generator. For all 92,800 raw parameter pairs, it checks the conjugacy
identity at all 20 phases: **1,856,000 identities**. The ordinary power identity
above supplies its extension to every canonical exponent.

## Actual negative certificates for every remaining profile

[catalogue.csv](catalogue.csv) contains exactly the ordered 1,120 records
`(row,u,t,closed,status,a,d,color)`. Every status is BAD_AP. The independent
checker reconstructs each original 620-word via closed affine-power sums and
the canonical field logarithm, evaluating **672,000 regular point values**.
Every supplied a,d,color is checked directly against all seven integer terms:
0<=a<620, 1<=d<=310, color in {0,1}, all terms regular, all colors equal, and
max(a+6*d)<=2479. There is no native UNSAT flag, timeout or incomplete search
used as a premise.

The generator searches only the 9,600 APs with normalized field difference 1
and finds an actual witness in every case, after 73,924 attempted APs in total.
For nonclosed profiles this search is **not** asserted to cover all APs; its
negative outputs are valid because they are explicit actual witnesses. The
checker would enumerate all 620*619 ordered nonzero-difference pairs before
accepting a CORE proposal; there are no such accepted proposals here.

The complete parameter cover and 1,120 actual bad progressions prove the
theorem. Arbitrary values at any of the 120 actual modulus-31 poles in
[0,3703] cannot change one of these regular obstructions.

## Conditional closed-transport reduction

Now impose the additional condition **`b o phi^30=b`**. This holds for 468
of the normalized pairs, or 36,960 of the admissible raw parameter pairs.
Per representative the normalized closed counts are
60,72,60,60,72,72,72 in the order of the table above. Closed status is invariant
under simultaneous phase conjugacy, giving the weighted raw count.

Let m be the least positive integer with `b o phi^m=b`. Closure makes m divide
30. Since phi is an element of the 160-element affine phase group, its order
divides 160, and m divides that order. Thus m divides gcd(30,160)=10 and
`b o phi^10=b`. As 3^10=25 mod31, the subgroup

`H3=<25>={1,5,25}`

preserves the closed core in its field coordinate with phase unchanged.
The corresponding actual CRT multiplier is 521 (25 mod31, 1 mod20).
The checker verifies all 280,800 regular color identities for the 468 closed
profiles. Every one of the other **652 normalized profiles** has an actual
H3-invariance counterexample. This last fact is checked computationally and
prevents silently extending the conditional lemma to the whole family.

Closure also gives a complete diagonal normalization of cross-field APs.
For nonzero field difference delta, the map

`T_delta(r,s)=(delta^-1*r, phi^ell(delta)(s))`

is a unit affine CRT map preserving C. Indeed
ell(delta^-1*r)+ell(delta) equals ell(r) modulo30, and b is invariant under
phi^30. The map sends field difference delta to 1. The complete normalized
cross-field domain has 24 starts avoiding the seven forbidden field zeros,
20 phase starts and 20 phase differences: **24*20*20=9,600 APs**. Field-constant
APs are already mixed by the local row condition. The checker verifies
8,704,800 actual CRT/color identities, including the mapped pole positions.
This complete positive-check reduction applies only to closed profiles.

## Useful next construction frontier

The subgroup lemma motivates a genuinely broader **chosen construction
ansatz**, arbitrary H3-invariant regular cores, rather than a single affine
phase-map power law. Ten multiplicative H3 cosets cover the thirty nonzero
field residues. Each coset may choose an independent phase row. The mandatory
antipodal relation leaves **100 independent point bits**; fixing the
{1,5,25} row to mask16 would leave **90** raw free bits. Each other row must
pass the 580-row local test. A full actual-AP model and independent audit for
that broader ansatz are still uncomputed here. The 9,600 diagonal reduction
does not transfer, nor do cuts expressed in a previous affine-row decoder.
H3-invariance itself is a construction choice, not a necessity for arbitrary
regular cores.

## Prior work, primary sources and trust

The local 580-row/seven-orbit classification was previously published in
[separable620](https://github.com/helgithorskarp/math_results/tree/main/round-two/six-vdw-1/separable620),
source commit 933d56da9d6865fc7bf82d4e280f8eeeaaf0902e, graph9037/0,
CID bafkreid4raselasdzja2lnyn6tl447cohgoxgl2otctd5ykri76kmrtvli.
Here it is independently reconstructed; that source's separable-core
refutation is not a premise. The earlier
[maximal-affine-rows20](https://github.com/helgithorskarp/math_results/tree/main/round-two/six-vdw-1/maximal-affine-rows20),
source a8557f74b6c3696398fcd28d71f52788c5e8399b, graph9394/0,
CID bafkreihdczz3ilhmuavze3g7jdjcldlkqtsun3ysxkb5jabiz32cojgdpy,
classified the largest affine extension containing a specified row cube.
It motivates considering other constructions but supplies no exclusion for
the present family. Neither prior theorem is relabeled as new.

[Monroe's primary paper](https://combinatorialpress.com/jcmcc-articles/volume-128/new-lower-bounds-for-van-der-waerden-numbers-using-distributed-computing/)
was refreshed live on 2026-10-02: Table1 gives >3703 at length7/two colors;
Table2 lists prime617. Its length-first W(7,2) is our color-first W(2,7).
The [author's repository](https://github.com/hmonroe/vdw) was also refreshed.
The earlier [Herwig et al. construction paper](https://www.cs.utexas.edu/~marijn/publications/waerden.pdf)
provides cyclic/multiplicative construction context. These literature checks
do not establish a comprehensive absence of a newer record or a historical
priority claim for the present elementary reductions. The asymmetric w(3,k)
problem is different. A coloring of [1,3704] would prove W(2,7)>=3705; no such
coloring is produced here.

The trusted mechanisms are exact integer source and the ordinary reductions
written above. The checker shares no generator import or permutation-power
implementation. Tiny physical positives/negatives and deliberately damaged
catalogues calibrate it; normal/optimized modes compare whole mathematical
results. See [VALIDATION.md](VALIDATION.md) and [README.md](README.md) for
counts, commands, source pins and process limits. A same-author separate
algorithm is not an external review or a formal proof-assistant theorem.
