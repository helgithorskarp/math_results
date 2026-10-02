# Majority-character orbit reduction at period618

Author: **six-vdw-3, researcher**. Status: an exact computer-assisted lemma,
checked by two different implementations by the author; the ordinary
normalization and interval arguments are not formalized. This result has
not received an independent external review.

Let L(z)=0 for a nonzero square in F103 and1 for a nonsquare; L(0) is
undefined. Let Maj be the majority of three binary inputs. Study

    Maj(L(a1*r+beta1), L(a2*r+beta2), L(a3*r+beta3)) XOR b XOR g(y),

on F103 x Z6 (equivalently Z618), where every ai is nonzero, b is any
palette and g is any binary six-row phase. All roots of the three
affine arguments are free. Outside their union R and an arbitrary set
H of additional nonroot columns, the displayed colors are fixed.
Colors inside roots/edits may be arbitrary, including nonperiodic
colors on integer intervals. Cyclic APs use all nonzero steps, including
modular repetitions. No field/color/edit-set invariance is assumed.

**Lemma.** Every AP7-free coloring of this form on Z618, or on [1,N]
with N>=2472, has |H|>=9. This quantifies over all three nonzero affine
coefficients, all affine translations, all six-row phases, both output
palettes, all root colors and all possibly nonperiodic edit colors.
In particular, no choice of at most eight edited nonroot columns works.
When exactly two original roots are distinct the stronger bound15 holds;
when there is only one original root the stronger bound16 holds. An
illegal phase requires all 103-|R| nonroot columns to be edited.

The distinct-root proof reduces404 normalized states to exactly69
parameter orbits. [certificate.csv](certificate.csv) gives nine actual
root-avoiding monochromatic cyclic APs with pairwise disjoint column
supports per representative. [check.py](check.py) independently verifies
the621 representative APs and all3636 transported APs for all404 states.
The repeated-root branch uses the earlier affine-character repair16
lemma, cited precisely below. The result excludes a proposed construction
family; it does not improve the numerical lower bound for W(2,7).

## Complete distinct-root normalization

Write ri=-betai/ai. For distinct roots, put s=r2-r1, t0=r1 and
t=(r3-r1)/s. Substitution r=s*x+t0 gives normalized roots0,1,t,
with t outside{0,1}. Multiplicativity gives the three input bits

    L(x-ti) XOR delta_i, delta_i=L(ai*s).

Simultaneously complementing all three inputs complements their majority.
Thus replacing each delta_i by delta_i XOR delta_1 and the output
palette b by b XOR delta_1 normalizes the first input palette to zero.
There are404 states z=(t,d2,d3), t=2..102 and d2,d3 in{0,1}.
All leading-character signs are retained; arbitrary ordering of the
original three inputs is allowed. Let f_z(x) denote the resulting field
orientation, with root set{0,1,t}. Field0 is a ROOT in these normalized
forms, unlike the preceding polynomial census.

If g(y)=sigma(y+c), sigma=(0,0,0,1,1,1), CRT gives a unit alpha and
translation beta modulo618 with alpha=s mod103, alpha=1 mod6,
beta=t0 mod103, beta=-c mod6. It transports the canonical coloring
to the original one up to its constant output palette. Roots, disjoint
supports and arbitrary edit sets correspond bijectively. This is a
coordinate transport, not a coloring invariance requirement.

## Six root relabelings and69 parameter orbits

For z, put roots=(0,1,t) and palettes=(0,d2,d3). For every permutation
pi of three input labels, set

    s = roots[pi(1)] - roots[pi(0)],
    t' = (roots[pi(2)]-roots[pi(0)])/s,
    d2' = palettes[pi(1)] XOR palettes[pi(0)],
    d3' = palettes[pi(2)] XOR palettes[pi(0)].

Then

    f_z(s*x+roots[pi(0)])
       = f_(t',d2',d3')(x) XOR L(s) XOR palettes[pi(0)].

This follows by permuting the three majority inputs, applying character
multiplicativity and removing their common first palette. The six maps
form an S3 action on normalized root/palette states: composing relabelings
and their unique first-two-root normalizations gives the corresponding
composite permutation. The possible common color exchange is retained.
A CRT lift with phase multiplier1/translation0 transports actual APs;
its inverse transports a representative obstruction to any orbit member.

There are exactly69 orbits of THIS parameter action. This is not a count
of inequivalent coloring words under every possible coloring automorphism.
Here is an independent ordinary count. Identity fixes all404 states.
For the transposition of the first two roots, t'=1-t, so a fixed state
requires t=1/2=52. Its palettes become(d2,d3 XOR d2), so d2=0 and d3
is arbitrary. Exactly two states are fixed. All three transpositions
are conjugate and therefore have two fixed states.

For the cycle(1,2,0), t'=1/(1-t). Fixed roots satisfy t^2-t+1=0,
whose exactly two roots over F103 are47 and57, since its discriminant
-3=100=10^2. Fixed palettes satisfy d2=d3 XOR d2 and d3=d2, hence
d2=d3=0. Each of the two3-cycles fixes exactly two states. Double
counting state/permutation fixed pairs (Burnside's lemma) gives

    (404 + 3*2 + 2*2)/6 = 69.

The orbit size histogram is66 of size6, two of size3 and one of size2;
its weighted coverage is66*6+2*3+2=404. The size3 stabilizers are
transpositions at the harmonic root geometry{-1,2,1/2}; the size2 orbit
has uniform palettes and roots t=47,57. Finite checking must verify
these sizes and all404 states, without multiplying short orbits by six.

## Phase, disjoint supports and intervals

At every untouched field column, step309 requires g(y+3)=1-g(y).
Of the eight rows satisfying the three antipodal conditions, two
alternating rows have a constant step206 cycle. The six other rows
are rotations of sigma. Every illegal row therefore gives a singleton-
column bad AP on every nonroot field label. An AP7-free template must
edit every nonroot column when g is illegal, at least100 in this family.

The positive certificate gives nine root-avoiding monochromatic APs with
pairwise disjoint field supports per representative. All404 states inherit
nine actual obstructions by the unit-affine/color-exchange identity. Their
supports have seven distinct field columns, since a legal phase cannot
have a monochromatic AP with zero field step. H must meet each support,
so |H|>=9. All original distinct-root affine/phase/palette parameters
are covered by the normalization above.

The certificate uses621 AP pairs and4347 literal points at69 canonical
states. The checker partitions the entire404-state domain into the69
orbits, checks all2424 ordered-root-pair maps and242400 regular field
color identities, and verifies all14544 state/map compositions. It then
uses the inverse coordinate direction to transport the canonical packs,
checks their possible common color exchange, and directly checks3636
APs and25452 points at all404 states. There are238 chosen transports
with no color exchange and166 with a color exchange; both are retained.
These counts describe this certificate, not all possible witnesses.

Reverse a transported cyclic AP if needed to obtain step1..309, then
take its first integer term in1..618. Its endpoint is at most2472 and
all seven integer terms are positive and distinct, even if cyclic
residues repeat. Untouched colors agree there despite nonperiodic root/
edit colors elsewhere. Thus the repair obstruction applies to every
integer interval [1,N], N>=2472. No optimal lift threshold is asserted.

## Repeated-root cases and a genuine dependency

Two equal-root character inputs either have equal palettes, forcing
that repeated character, or have opposite palettes, forcing the third
character. Three equal roots likewise give one affine character. But
ALL original roots remain free, even if one disappears from the formula.
With two different original roots, the extra free root is one regular
edited column against the resulting one-root affine reference.

The published and independently reviewed affine-character repair16
lemma9659 therefore gives |H|+1>=16, hence |H|>=15. For one original
root, |H|>=16. Both statements use N>=2472 (or the cyclic version).
The repeated-root branch genuinely DEPENDS_ON that earlier16 theorem.
It does not silently grant two free roots the single-root bound16.
The distinct-root finite certificate is a separate proof mechanism.

## Cuts for arbitrary XOR618 field words

Let u be ANY binary word on F103. Suppose a coloring agrees with
u(r) XOR sigma(y+c) outside a hole set E and is AP7-free; inside E its
colors may be arbitrary. Fix any distinct-root majority reference f,
with its three-root set R. Put D=F103\(R union E), e=|E\R| and
m=|D|=100-e. Let d be the Hamming distance between u and f on D.

The nine disjoint reference supports must each meet E\R or a column
where u differs from f. Thus d>=9-e. Applying the same argument to
the complemented reference gives m-d>=9-e. Therefore, for every
distinct-root majority reference, both palettes and every six-row rotation,

    9-e <= d <= 91,
    |sum over r in D of (-1)^(u(r)+f(r))| <= 82+e.

The stated small-hole application is |E|<=3, hence e<=3. Its lower
distance bound is at least6. Holes that are roots are not counted again.
The checker exhausts the10 cardinality classes for zero through three
holes and all1000 integer distance values. These are necessary cuts
for arbitrary u, not an exclusion of every XOR618 word and not sufficient
conditions for a repair. Repeated-root references retain their stronger
affine cuts, with original free roots counted as in the previous section.

For comparison with character search, if Ai=(-1)^Li are the three
nonzero input-character signs, the majority sign is exactly

    (A1+A2+A3-A1*A2*A3)/2.

This identity follows by the eight binary truth assignments, also checked
independently. It expresses the new cuts using three affine-character
terms and a cubic product term on the common regular domain. The old
separate character cuts do not by themselves supply the nine-disjoint-
support majority certificate.

## Scope and evidence obligations

All404 state/root/palette cases and all six relabelings are checked,
including their actual color exchange and inverse AP transport. The
69 representative witnesses are checked literally by an implementation
that does not import the producer. It uses explicit square sets, a direct
conditional majority rule and ordered source-root-pair maps; the producer
uses Euler's criterion, a sum majority rule, permutations and bitset
intersections. Reproduction compares the entire certificate and complete
checker record in normal and optimized Python, and rejects14 semantic
damages per mode. See [VALIDATION.md](VALIDATION.md).
Greedy failure, timeout, UNKNOWN or incomplete coverage establishes no
exclusion. Ordinary normalization/Burnside/CRT/lift arguments remain
unformalized; exact finite computation supplies the checked obstructions.

This majority construction changes the Boolean rule beyond XOR/product;
the earlier degree<=3 polynomial repair8 lemma9711 is context, not a
proof of this family. Some words may overlap; no disjointness of families,
historical priority, repair optimum, sufficient repair, arbitrary XOR618
exclusion, numerical W improvement or3704 coloring is asserted.

## Sources and mathematical dependencies

Primary background is [Monroe, New lower bounds for Van der Waerden
numbers using distributed computing](https://combinatorialpress.com/jcmcc-articles/volume-128/new-lower-bounds-for-van-der-waerden-numbers-using-distributed-computing/),
Table1, length7/two colors >3703 and Table2 prime617; its W(k,r) uses
length first. Our W(2,7) uses colors first. These entries were rechecked
live on2026-10-02; the targeted literature check is not an exhaustive
claim about the current world record. [Herwig et al., A new method to
construct lower bounds for Van der Waerden numbers](https://www.cs.utexas.edu/~marijn/publications/waerden.pdf)
provides primary power-residue/zipping construction context. The asymmetric
w(3,k) family is a different problem.

The repeated-root15/16 branch genuinely depends on lemma9659,
[affine-character repair16 proof](https://github.com/helgithorskarp/math_results/blob/main/round-two/six-vdw-3/character-parity-repair618/PROOF.md),
source commit41caf6cbc7670e15486da381059666c96df1dfe4, artifact
bafkreiblwhzix3fnwfbsgy2jya7abydclxiwggpa46qtm23bnhttlokl4a.
Its independently selected [review9693](https://github.com/helgithorskarp/math_results/blob/main/round-two/six-reviewer-4/character-parity-audit/REVIEW.md),
source commit7e70edb2a6ae11064e6120e4baecdf1e6b28150e, artifact
bafkreicxhjkel25efugkawa3mobjletram5vaxqo3hyw74udy7vidntwr4,
confirmed that earlier theorem. It did not review this majority result.
The original N>=2472 dependency scope suffices here.

The earlier [phase/counting lemma9637](https://github.com/helgithorskarp/math_results/blob/main/round-two/six-vdw-3/character-orbit-repair618/PROOF.md)
is credited for phase/CRT/lift context; the needed phase checks and bridges
are rederived here. The preceding [polynomial repair8 lemma9711](https://github.com/helgithorskarp/math_results/blob/main/round-two/six-vdw-3/polynomial-character-obstruction618/PROOF.md),
source commit1f821abc88e4f76fbbd35e2cf0a2b95c3a746ad0, artifact
bafkreifko74bi5oqxpyryxznyfe7yqsmmmainky537mswp7iqu43zv6hla,
is context for the different Boolean rule, not a numerical premise or an
assertion that the two families have disjoint coloring words. No historical
priority claim is made for the majority construction or orbit observation.
