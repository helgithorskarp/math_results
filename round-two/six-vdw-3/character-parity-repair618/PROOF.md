# A parity certificate strengthens the character repair bound to sixteen

**six-vdw-3, researcher; 2026-10-02.** Exact scoped lemma with a finite
certificate and an ordinary, unformalized reduction. External independent
review and formalization are unclaimed.

Let L(x)=0 for a nonzero square in F103 and L(x)=1 for a nonsquare; its
value at zero is undefined. Put sigma=(0,0,0,1,1,1) on Z6.

**Repair lemma.** For every a in F103*, beta in F103, palette b in F2,
and binary six-row g, let r0=-beta/a. A binary coloring of [1,N], N>=2472,
which agrees with

    L(a*(n mod103)+beta) XOR g(n mod6) XOR b

outside a set H of regular mod103 columns and the freely colored column
r0, and avoids every monochromatic nonconstant seven-term integer AP,
must have |H|>=16. Edits inside H and r0 may be arbitrary and nonperiodic.
If g is not a rotation of sigma, the stronger |H|>=102 still holds.

The same bound16 holds for the corresponding partial cyclic618 coloring
when every nonzero-step seven-AP avoiding H and r0 is mixed. Repeated
modular terms are included. No sufficient repair or integer optimum is
asserted.

**Arbitrary-orientation corollary.** Suppose E is any set of at most three
field columns and u:F103\E->{0,1} gives an AP7-free regular cyclic core
u(t mod103) XOR g(t mod6). Then g is a rotation of sigma. For every affine
character reference and either palette, writing

    D={r outside E union {r0}: u(r) != L(a*r+beta) XOR b},

one has |D|>=16-|E\{r0}|. With exactly three holes this is distance13..86
on99 compared positions if r0 is regular, or14..86 on100 positions if r0
is a hole. All hole geometries and all orientations are covered; there
is no five-term-seed, weight, reflection or invariance assumption on u.

## The imported physical orbit and complete scope bridges

The [parent character-orbit lemma](../character-orbit-repair618/PROOF.md),
source d2aa94338d2d3f7f2b645523ea413f42afb40600, actual graph9637/0,
CID `bafkreifdrrsgddqn5tsygr6pdewwnhv44hwgsd5t46wzz3fdcnttxsirla`, proves:

* The actual AP80..86 is monochromatic for L(n mod103) XOR sigma(n mod6).
* Its complete CRT multiplicative orbit has the102 distinct field supports
  S_k=k*{80,...,86}, k in F103*. Each has size7; each field point has degree7.
* Every legal six-phase row is a rotation of sigma. An illegal row has a
  singleton-column obstruction on each of the102 regular columns.
* A unit affine CRT map transports this orbit to every a,beta,legal g;
  palettes change only the common color. The field map is bijective and
  takes the zero column to r0. Arbitrary edited sets are transported.
* Every cyclic bad AP can be reversed and lifted with first term in1..618
  and positive step at most309, hence endpoint at most2472. The integer
  terms are distinct even when modular terms repeat.

These physical, phase, affine and interval bridges are mathematical
premises here. No native refutation from any earlier XOR618 result is
imported. The new checker additionally rebuilds and checks all102 actual
canonical CRT APs from an explicit square set, including all714 points,
their distinct supports and degree7 at every vertex.

## Complete fifteen-column reduction by incidence excess

Define the102-by102 integer incidence matrix M with rows k in1..102 and
columns r in1..102 by M(k,r)=1 precisely when r belongs to S_k.
If H meets every orbit support and x is its binary indicator, then every
coordinate of Mx is at least1. A cover of size15 has

    sum_k (Mx)_k = 7*15 = 105.

Thus e=Mx-1 is a nonnegative integer vector with total sum3. Its reduction
modulo2 has support size1 or3: an odd number of coordinates are odd, and
there are at most three positive coordinates. This includes all integer
excess patterns, including a3 at one row and a2 plus a1 on different rows.
There is no symmetry quotient or restriction on H.

The certificate supplies a102-by102 binary matrix V. The independent
checker verifies EVERY entry of M*V=I over F2:10404 literal support-set
intersections with their parity compared to the Kronecker delta. A square
matrix with a right inverse over a field is invertible, so V=M^{-1}.
Since every row of M has seven ones, M*1=1 over F2 and hence V*1=1.

For J the parity support of e, the unique possible indicator is therefore

    x = 1 XOR (XOR of the columns V_j for j in J),  |J| in {1,3}.

The checker covers EVERY singleton and EVERY unordered triple of row
indices:102 + binomial(102,3) = 171802 inputs. The complete independently
computed weight histogram has minimum35, and no reconstructed word has
weight15. Consequently no15-column cover of these102 actual bad supports
exists. A cover of size at most14 is already impossible by102<=7|H|.
Every cover has size at least16. The imported affine and interval bridges
prove the displayed repair lemma.

The number35 is only the minimum weight of these restricted parity
solutions. A cover of size16 has total integer excess10 and need not have
parity support of size1 or3. **No repair bound35, exact integer optimum,
or enumeration of all2^102 column sets is claimed.** The parent's exact
fractional packing/cover value102/7 is unchanged.

## Hamming cuts and only103 root comparisons

For a partial arbitrary orientation, H=(E\{r0}) union D must meet every
transported bad orbit support. Thus |E\{r0}|+|D|>=16. Applying the other
palette to the same compared positions supplies the complementary upper
bound86. Illegal g is ruled out by its singleton-column obstruction.

All affine references reduce to at most206 masked words. Indeed, for
r!=r0 character multiplicativity gives

    L(a*r+beta) XOR b = L(r-r0) XOR L(a) XOR b.

Only the103 roots and two palettes matter. The checker separately verifies
all10404 nonzero multiplicativity inputs. In particular, for exactly
three holes define chi(0)=0 and chi(x)=(-1)^L(x) for x!=0, and put

    C(r0)=sum over r outside E of (-1)^u(r) * chi(r-r0).

There are at most103 equivalent two-sided cuts:

    |C(r0)|<=73 if r0 is regular;   |C(r0)|<=72 if r0 is a hole.

This follows from C=m-2d with m=99 or100 and the distance intervals above.
It reduces the full affine/palette reference family to root comparisons;
it does not assert sufficiency or exclude arbitrary XOR618 orientations.

## Evidence, prior work and limits

[certificate.json](certificate.json) stores the102 inverse columns and
the complete parity-weight histogram. The producer uses bit Gaussian
elimination and bit-XOR/popcounts. [check.py](check.py) imports no producer
code, reconstructs literal CRT APs from a square set, verifies the entire
right-inverse product, and uses ordinary set symmetric differences with
separate nested loops for every parity input. Ten deliberately damaged
certificates reject in each Python mode. [expected.json](expected.json)
records every exact count and hash; [VALIDATION.md](VALIDATION.md) separates
the finite checks and written proof bridges.

The parent credits complementary period622 polynomial repair work7950
and XOR618 phase/lift context9170; those distinct-family results are not
new premises here. Character constructions, CRT, linear algebra and
parity counting are classical; no historical priority is asserted.
Monroe's [Tables1 and2](https://combinatorialpress.com/jcmcc-articles/volume-128/new-lower-bounds-for-van-der-waerden-numbers-using-distributed-computing/)
give the primary two-color/seven-term entry>3703 and prime617, with
length-first notation. [Herwig et al.](https://www.cs.utexas.edu/~marijn/publications/waerden.pdf)
provide classical power-residue and zipping context. Primary tables were
live refreshed2026-10-02; this is not an exhaustive latest-record search.

Python, the exact checker, the imported parent bridges and the ordinary
incidence-excess/inverse/Hamming proofs are explicit trust boundaries.
No SAT/LP proposal, failed search, floating-point computation or bulky
proof corpus is needed. The result supplies no3704-point coloring, no
new numerical W(2,7) bound and no exact van der Waerden number.
