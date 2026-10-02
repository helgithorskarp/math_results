# Independent character-pattern phase words at periods 310 and 620

Author: **six-vdw-1**, role: researcher. Exact finite certificate with ordinary
written reductions; unformalized and not independently peer reviewed.

For each pole `p` in F31 and nonzero `u` in F31, set

    (a1,a2,a3) = (p+u,p+2u,p+4u).

Let `L(z)=0` for a nonzero square and `L(z)=1` for a nonsquare; `L(0)` is
undefined. At a field value outside the pole and the three roots, define

    T(r) = (L(r-a1),L(r-a2),L(r-a3)).

Choose **an independent binary phase word for each of the eight patterns**
and a separate independent phase word at each of the three roots. The
phase is `n mod h`, with `h=10` or `20`; the field coordinate is `n mod 31`.
Only the pole column is omitted. All three roots are retained and freely
colored within their periodic phase words. There is no common XOR phase,
field-subgroup invariance, palette gauge, edit budget or imported repair cut.

**Theorem.** Every such regular cyclic word at period `31h` has a
monochromatic cyclic seven-term test with nonzero step and no pole term.
There are 930 distinct pole/root-set configurations at either period.
The statement also allows independently scaled character arguments
`L(bi(r-ai))`, for arbitrary nonzero `bi`.

**Finite consequence.** A binary integer coloring obeying these phase words
outside the pole has a monochromatic seven-term integer AP in `[1,1240]`
when `h=10`, or `[1,2479]` when `h=20`. Pole values may be arbitrary and
nonperiodic. Root phase words must obey the specified periodic template.
These are sufficient bounds, without an optimality claim. No coloring of
length 3704, numerical improvement of W(2,7), unrestricted core exclusion
or exact van der Waerden value follows.

## Original 310-point obstruction

A cyclic test is the sequence `(a+j*d) mod M`, `j=0,...,6`, with
`0<=a<M` and `1<=d<M`. Residues may repeat. Every such test lifts to seven
distinct integer positions with positive step, as justified below.

First take `p=0`, roots `1,2,4` and phase 10. The eight nonroot character
blocks, in binary pattern order, are

    000: 6,9,11,20       001: 3,10,21
    010: 5,8,29          011: 15,17,19,26
    100: 12,18,22        101: 7,16,27,30
    110: 13,14,23,24     111: 25,28.

The three additional rows are the singleton roots `1`, `2`, `4`. CRT gives
every phase at every nonzero field value. Thus there are initially **110
independent bits**, or `2^110` choices of the eleven ten-phase words.

Step 155 fixes the field coordinate and exchanges phases `s` and `s+5`.
If their colors agree, its seven-term test is monochromatic and avoids the
pole. Every AP-free candidate must therefore satisfy antipodality at every
row. It has **55 independent bits**, with physical signed tag

    tag(r,s) = +(5*row+s+1),           0<=s<5,
               -(5*row+(s-5)+1),     5<=s<10.

Rows are numbered 0 through 10. A positive tag reads the bit and a
negative tag its complement. This is forced by actual APs, rather than
an assumed symmetry of a sought coloring.

`AP_KERNEL.json` contains 1,758 triples `(a,d,common_color)`. For each,
the checker explicitly reconstructs all seven physical positions modulo
310, rejects any pole term, computes their tags, and forms the clause
forbidding all seven colors from equaling the recorded common color.
Repeated variables must demand the same value; otherwise the proposed
premise is rejected. All 1,758 clauses are distinct. The checker reconstructs
all 310 physical tags, retains all 30 root/phase points, and checks 12,306
literal AP terms.

`kernel.lrat` gives **859 positive RUP additions**, ending in the empty
clause, with no deletion and 13,559 checked propagation steps. The small
`strict_rup.py` checks each implication by unit propagation under the
negation of the proposed clause. Negative RAT hints, absent hints,
out-of-domain variables and nonfresh addition IDs are rejected. An empty
clause is required. Therefore this subset of necessary original AP
conditions has no assignment, excluding all `2^55` antipodal candidates
and hence all `2^110` original phase-word choices.

The proof does not require enumerating all assignments or all possible
APs: a contradictory subset of actual necessary clauses suffices.
The full native discovery model and its larger trace are not premises.

## Affine transports and leading character scalars

For phase `h`, choose the CRT unit `U` and shift `V` with

    U = u mod31, U = 1 mod h;
    V = p mod31, V = 0 mod h.

The actual map `n -> U*n+V mod(31h)` preserves phase, maps pole 0 to `p`,
and maps roots `1,2,4` in their stated order to `p+u,p+2u,p+4u`.
Character multiplicativity gives

    L((p+u*r)-(p+u*a)) = L(u) XOR L(r-a).

Thus it merely permutes the eight freely chosen pattern rows, and carries
the three free root rows separately. A unit maps every nonzero AP step
to a nonzero AP step. This transports the obstruction without assuming
that the coloring itself is affine invariant. The root set `{1,2,4}` has
trivial multiplicative stabilizer, so the thirty scaled sets at each pole
are distinct. Thirty-one poles give 930 configurations.

Each separate nonzero leading scalar `bi` flips its corresponding input
bit by `L(bi)`. Since the lookup table is arbitrary, these fixed input
flips are absorbed by a permutation of pattern rows. The free root words
remain free. The checker verifies all 900 nonzero multiplicative identities,
all 64 input-flip table entries, and all actual point tags at all 930
configurations at each period: 864,900 point maps in total. Its 620-point
tag audit uses antipodality, which is necessarily forced there by step 310.

## The 620-point consequence and finite bounds

Restrict an alleged AP-free regular word modulo 620 to positions `n=2m`.
It becomes a regular word modulo 310: field pole `p/2`, roots `ai/2`,
phase `m mod10`, and each phase word restricted to the entries `2s mod20`.
The character arguments acquire only the fixed input flip `L(2)`.
The roots retain the relative geometry
`p/2+(u/2)*{1,2,4}`. Every cyclic 310 test maps to an even cyclic 620 test,
with nonzero doubled step. This contradicts the 310-point theorem.
All `2^220` original eleven twenty-phase-word choices are consequently
excluded, not merely those having a common phase word.

Reverse a cyclic 310 test with step greater than 155. Its positive step
then lies in `1,...,155`; take its start in `0,...,309`. Its integer
endpoint is at most `309+6*155=1239`. All seven lifted positions are
distinct, avoid the pole and have the same prescribed regular colors.
Doubling this lift gives the 620-point endpoint bound 2478. The checker
replays this lift for all 95,790 original 310 start/nonzero-step pairs.

For a positive-coordinate coloring on `[1,N]`, apply the argument to
`c(n+1)` on zero-based coordinates. This shifts the pole and roots by
minus one and rotates each phase word, preserving the stated family.
Adding one to the lifted positions gives `[1,1240]` and `[1,2479]`.
Every witness avoids the pole, so no restriction on its finite values is
needed. Arbitrary nonperiodic changes at character roots would leave this
family and are not covered.

## Exact replay and trust boundary

Run `python3 -B reproduce.py --work /tmp/vdw-pattern310-proof` from this
directory, using a fresh output directory. CPython 3.11+ on a POSIX system
and the standard library suffice; no SAT solver, converter, graph access or other source
directory is needed. The runner pins every source file before launching
children, executes three checks sequentially in normal and optimized
Python, and compares **every field of every record**, the full normal/O
output bytes, and both reconstructed CNF files. Each child has a fixed
35-second process-group guard and all six thread variables equal one.
Hashes identify evidence; the AP binding and RUP implications prove it.

Controls reject eight damaged original-AP premises and five damaged proof
records in each mode, and reject `L(0)`. A complete tiny F7/phase10
positive control has three distinct nonroot patterns and three separate
root rows. Every regular AP stays in one field column. Exactly 30 of 32
antipodal phase rows are legal, giving `30^6=729000000` actual tiny cores;
all 4,830 original start/nonzero-step pairs are inspected.

The discovery producer used Euler's criterion and compressed signed NAE
constraints. The independent AP checker uses Gauss's lemma, literal
physical coordinates and no producer import. The strict kernel is a
byte-exact credited copy from our earlier [H3-invariant core source](https://github.com/helgithorskarp/math_results/blob/main/round-two/six-vdw-1/h3-core620-exclusion/strict_rup.py)
(lemma 9625), SHA256
`55543f905d42aaf0955906f97a8484ec8522a182512b1d2e8fe132bb45cb545c`.
That theorem's numerical exclusion is not a premise. Native provenance
is recorded in `VALIDATION.json`. The compact 1,758-premise obstruction
and 90,096-byte RUP proof are a newly checked logical subset, not pieces
of an uploaded large proof corpus. Same-author independent algorithms
and normal/O replay are not independent-person review. Character, CRT,
antipodality, parity-slice and integer-lift bridges remain ordinary proofs.

## Prior work and remaining frontier

Primary background is [Monroe, New lower bounds for Van der Waerden
numbers using distributed computing](https://combinatorialpress.com/jcmcc-articles/volume-128/new-lower-bounds-for-van-der-waerden-numbers-using-distributed-computing/),
whose Table 1 lists length seven/two colors `>3703`, with prime 617 in
Table 2. Both were rechecked live on 2026-10-02. Monroe uses length-first
notation; our W(2,7) uses colors first. [Herwig et al., A New Method to
Construct Lower Bounds for Van der Waerden Numbers](https://www.cs.utexas.edu/~marijn/publications/waerden.pdf)
and [Monroe's source](https://github.com/hmonroe/vdw) provide construction
context. The asymmetric `w(3,k)` problem is separate. Narrow live primary
searches and the current committed team frontier were inspected; no
exhaustive current-world-record or historical-priority claim is made.

Earlier [QR31](https://github.com/helgithorskarp/math_results/blob/main/round-two/six-vdw-1/qr31-x20-obstruction/PROOF.md),
[separable F31 XOR C20](https://github.com/helgithorskarp/math_results/blob/main/round-two/six-vdw-1/separable620/PROOF.md),
[three-field repairs](https://github.com/helgithorskarp/math_results/blob/main/round-two/six-vdw-1/three-column-robust620/PROOF.md),
[phase-power cores](https://github.com/helgithorskarp/math_results/blob/main/round-two/six-vdw-1/phase-powers620/PROOF.md),
[H3 cores](https://github.com/helgithorskarp/math_results/blob/main/round-two/six-vdw-1/h3-core620-exclusion/PROOF.md)
and [phase72 repair9](https://github.com/helgithorskarp/math_results/blob/main/round-two/six-vdw-1/character-phase72-repair620/PROOF.md)
are credited as distinct reductions. Peer [Boolean-three-character
XOR618 repair9](https://github.com/helgithorskarp/math_results/blob/main/round-two/six-vdw-3/boolean-character-obstruction618/PROOF.md)
uses a scalar Boolean rule XOR one common six-phase word; the present
family has an independent phase word per input pattern. Peer [H7 exact-ten
phases](https://github.com/helgithorskarp/math_results/blob/main/round-two/six-vdw-2/order7-phase-ten-singletons-triple/PROOF.md)
concern F617 and a different restriction. None of their repair constants,
native outcomes or review verdicts is imported here. Lookup tables,
character functions, CNF encoding and RUP verification are classical.
The scoped information is this exact independent-phase obstruction for
the specified relative-root class and its quantified transports and lifts.

The broader unrestricted regular 310 core remains unresolved. A separate
150-input parity-quotient proposal returned UNKNOWN after 49,902 conflicts
under the 50,000 hard observed ceiling and is frozen without retry or cap
increase. It is not an exclusion premise. A next construction direction
is pattern-dependent phases over F103/phase6, with all original roots
free; the known scalar XOR618 bound does not exclude that different family.
