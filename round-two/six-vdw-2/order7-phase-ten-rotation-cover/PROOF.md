# A complete rotation cover for the H7 phase-ten branch

six-vdw-2, researcher; 2026-10-02. Author-checked corollary and exact finite
reduction. Separate proposal, counting and literal phase-checking algorithms
are used. External independent review and formalization are not claimed.

Let H=<3^88> in F617*. Suppose an H-invariant binary coloring is mixed on
every nonconstant seven-term field AP avoiding zero. Set y_i=c(3^i),
i modulo88, and f_i=y_i XOR y_(i+44), i modulo44. Choose a phase value v
occurring exactly ten times and suppose its occurrences are nonadjacent.

**Corollary.** Some two successive selected gaps are (2,3), in the positive
base3 logarithmic order. Scalar multiplication therefore normalizes selected
positions to0,2,5, with background phases43,1,3,4,6. Both v values must be
retained separately. The j=4 branches of the earlier first-next split are
unnecessary for a complete existential search: its two j=5 branches suffice.

More precisely, the necessary phase family has exactly **127,049 classes
under scalar phase rotation per v**, or254,098 for both phase values.
Every class has a canonical representative starting with gap distances2,3.
Among the classes,29 phase words have least period22 and127,020 have least
period44. These are classes of candidate phase inputs satisfying the stated
necessary constraints. They are not counts of admissible field colorings or
orbits of full field colorings. All44 lower color orientation variables remain
available, with a global-color gauge. No orientation invariance is imposed,
including at the29 phase words with a nontrivial phase stabilizer.

## Why the root exists

The [uniform close-pair lemma9219](../order7-uniform-close-pairs/PROOF.md)
ensures a selected gap two. The
[successor lemma9291](../order7-phase-ten-gap-successors/PROOF.md) says every
gap two is followed by two or three. If none is followed by three, start at
any gap two and follow the cyclic ten-gap word: each subsequent gap is two.
Its sum would be20, contradicting the actual cycle length44. Therefore
a (2,3) pair exists. This argument neither reflects the logarithmic order
nor exchanges phase values.

Field multiplication by3^a preserves H and actual field APs. It rotates f
and transports both halves of y when the logarithmic shift crosses44.
One may subsequently exchange both field colors to make y_0=0. The formula

    y'_i = y_(i+a mod88) XOR y_a

gives f'_i=f_(i+a mod44). This preserves every orientation rather than
fixing an orientation under the phase word's stabilizer.

## Exact candidate family and canonical cover

Let g_0,...,g_9 be the ten positive selected gap distances. Nonadjacency gives
g_i>=2. The inherited [nonconstant phase-eight constraint8787](../order7-antipodal-geography/PROOF.md)
gives g_i<=8. Put r_i=g_i-2. The complete necessary gap family is

    length10, digits0..6, sum24, at least one0,
    r_i=0 implies r_(i+1)<=1, cyclically.

Every such word has a0->1 turn by the preceding cyclic argument.
generate.py enumerates all144,603 words rooted at r_0=0,r_1=1, then keeps
the lexicographically least cyclic rotation among0->1 roots. Its sorted
127,049 representatives are gap distances2..8, one line per class.
The2,540,980-byte generated corpus stays outside Git. Its SHA256 is
`1b2a3a2ae5d0277cbf6de49a71cbd52358c4a26f849d53b2ccdfc85e915509fa`.
The earlier arbitrary-gap-two rooted count178,983 is not an orbit count;
changing to a0->1 root removes34,380 rooted inputs without losing a class.

A binary phase word up to rotation is determined by its selected gap word
up to cyclic permutation: changing the marked selected position rotates
the gaps, and the partial gap sums reconstruct the selected positions.
Thus this canonical gap cover is exactly a cover of the corresponding
phase-word rotation classes. Both v values use the same geometric gap
representatives, but their field models remain separate.

check.py imports no DFS generator. It reconstructs actual selected positions
in Z44 from every proposed gap word, finds roots by membership at origin+2
and origin+5, recovers their actual gaps, checks the smallest allowed root,
and requires strict ordering and uniqueness. It independently computes the
number of classes below. Every proposed class is valid and distinct, and
the number matches the full class count; hence the cover is complete.

## Independent exact counts

Let T(n,t) count cyclic indexed deficit words of length n, digits0..6,
sum t, with a zero and every0 followed by0 or1. A transfer DP fixes its
first digit and tracks (sum,last,has-zero), checking the closing turn.
It gives T(10,24)=1,270,345 and T(5,12)=145.

A rotation of a ten-letter word by k positions fixes words obtained by
repeating a block of length d=gcd(10,k). The block sum must be24d/10.
This is an integer only for d=5 or10. The identity and the shift by5 are
the only relevant rotations. Burnside's lemma therefore gives

    (T(10,24)+T(5,12))/10 = 127,049.

None of the five-letter words has smaller period, since12/5 is not an
integer. Thus145/5=29 classes have gap period5, giving phase period22.
The remaining (1,270,345-145)/10=127,020 classes have full period.

The rooted0->1 count is also computed without the transfer DP. With z zeros,
p=10-z positive digits and q ones, there are

    binomial(p,q) [x^(24-q)](x^2+...+x^6)^(p-q)

ordered positive arrays. Zeros can occur only in the q slots preceding ones.
The sum of the numbers of nonempty slots over all zero allocations is
q*binomial(z+q-2,q-1): distinguish one slot, place one zero there, and
distribute the remaining z-1 zeros. A marked nonempty slot determines its
last zero, the desired0->1 root. Passing from a marked positive to this
root divides the count by p. Summing the resulting exact fractions over
z=1..9 and q=1..p gives144,603, agreeing with the separate transfer DP.

Small literal controls check all applicable sums for cycles2..7 over
digits0..3:4,362 indexed words,668 classes and81 count comparisons.
Separate binary-cycle controls compare gap classes with actual phase-word
rotation classes for lengths8..14:918 words and76 classes, both backgrounds.
Another61,888 signed-rotation controls retain arbitrary lower/upper colors.
Normal and Python -O checks agree; none of these controls asserts a
field-coloring count or enumerates all2^44 phase words.

## Exact field-orientation reduction and unresolved feasibility

For each representative and each v, reconstruct f with selected positions
given by the partial gaps. Introduce44 binary variables x_i=y_i. Then
y_(i+44)=x_i XOR f_i determines the upper colors. For every actual field
seven-AP avoiding zero, let L_j be the signed literal for its color in
these44 variables. Add both OR_j L_j and OR_j NOT L_j, together with x_0=0.
The resulting44-variable model is equivalent to field-AP-freeness for that
fixed phase, modulo global color. Scalar normalization proves that the
254,098 phase models cover the whole selected-count-ten/no-adjacency branch.
These models have not all been generated or solved; the published corpus
and checker certify the phase cover only.

An alternative unspecialized search now needs only the two heads0,2,5,
one per background. It retains36 free phases, exactly seven extra selected
positions, all44 lower orientations, XOR relations, full field constraints
and all44 conditional successor cuts. Its usual eight-level prefix encoding
has376 variables. Removing the j=4 heads is a reduction, not their refutation.

The strengthened j=5/background0 pilot returned UNKNOWN at exactly50,000
conflicts; the sequence stopped and the other three generated heads were
not proposed. Its audited CNF has376 variables,53,707 clauses and SHA256
`31fe1306c1a82fc0a645a74f77b7bd11fdaf88fbb9a7ff5e10217f11c7abfbd3`.
It adds33 proved successor clauses to the older failed model, retaining
every old constraint. UNKNOWN proves no exclusion. No identical failed
instance was retried, and no cap was increased. This corollary uses the
completed earlier lemmas, not the incomplete native search.

There is no full phase-ten exclusion, H7 classification, interval3704
coloring, improved unrestricted W(2,7) bound or exact-value claim.
The inherited phase band remains10..34.

## Provenance and trust

The original graph claim attaches ABOUT problem7194; DEPENDS_ON8787,9219 and9291;
REFINES9291 for the quantified complete rotation cover; CITES the
[unchanged band9187](../order7-phase-ten/PROOF.md). SOURCE_PINS.json records exact graph references,
source commits and the three mathematical input proof hashes.
The trusted bridge consists of these cited lemmas, the written cyclic,
scalar and Burnside arguments, the separate exact checker and Python/runtime
execution. Same-author separate algorithms are not an external review.

[Monroe Tables1 and2](https://combinatorialpress.com/jcmcc-articles/volume-128/new-lower-bounds-for-van-der-waerden-numbers-using-distributed-computing/)
and the [author source](https://github.com/hmonroe/vdw) were live rechecked
2026-10-02: two colors/seven terms >3703, modulus617. His length-first
W(7,2) is our color-first W(2,7); the asymmetric3/7 problem differs.
These are primary-source checks, not an exhaustive current-record or
priority claim. See VALIDATION.md for source reproduction and damage checks.
