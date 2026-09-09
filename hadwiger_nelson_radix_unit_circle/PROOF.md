# The complete unit-circle branch is exactly three-chromatic

Let ω=(1+i√3)/2, E=Z[ω], T={0,1,ω}, and

    A5(z)={Σ(j=0..4) a_j z^j : a_j in T}.

**Theorem.** For every complex z with |z|=1, the strict Euclidean
unit-distance graph on the physical point set A5(z) has chromatic number
exactly three. Coincident labels are identified, and all unit pairs are included.

The proof is an exact factor-and-colouring certificate for one complete branch
of the existing complex-radix architecture. It does not settle non-unit-modulus
parameters and does not produce a five-chromatic graph.

## 1. Physical reduction to 1,272 univariate events

The 243 labels are lexicographically ordered words in {0,1,2}^5, denoting
coefficients 0,1,ω. A difference of two labels gives
P(z)=Σ d_j z^j, where each d_j is zero or one of the six units of E.
Remove its initial and trailing zero coefficients. This writes P(z)=z^l Q(z)
with Q(0) nonzero and degree n≤4. For |z|=1,

    |P(z)|²−1 = |Q(z)|²−1,
    z^n(|Q(z)|²−1)=Q(z) z^n conjugate(Q)(1/z)−z^n.

Here conjugate(Q) means conjugating coefficients. Denote the last polynomial
by H before normalization. If n=0 it is identically zero: a monomial digit
difference is a unit vector at every parameter in this branch. These pairs are
exactly the 1,215 edges of the Cartesian product of five triangles.

If n>0, H has degree 2n, and its leading coefficient is
q_n conjugate(q_0), a unit of E. Divide by that unit. The resulting monic
H in E[X] has exactly the same roots. Its constant term is also nonzero.
Thus every extra unit edge forces z to satisfy a monic Eisenstein polynomial
of degree at most eight. No division by a vanishing parameter or coefficient
is used: |z|=1 and the leading coefficient is a unit.

The producer enumerates all 2,801 nonzero displacement words modulo common
unit phase and forms H by convolution with a reversed coefficient conjugate.
The independent checker instead enumerates **all 29,403 unordered label pairs**
and directly accumulates the Laurent norm coefficients

    coefficient at n+i−j: d_i conjugate(d_j),

then subtracts one at the middle coefficient and normalizes the leading unit.
This recovers exactly 1,272 distinct nonzero monic polynomials, of degrees

| degree | count |
|---|---:|
| 2 | 6 |
| 4 | 27 |
| 6 | 168 |
| 8 | 1,071 |

The canonical catalog SHA256 is
`b1d070b53ee5cd13713f598f2baeaa5e0d6dc1a3b9faf20635c28730a97d668d`.
The checker also preserves the complete mapping from each event to its actual
label pairs. Thus graph edges are checked from physical difference formulas,
not from a proposed abstract adjacency list.

If no additional event vanishes, the word c(a)=Σ a_j mod3, treating the label
symbols as 0,1,2, properly colours the five triangle layers. This gives the
generic case whenever labels are injective.

## 2. Complete factor cover, without trusting irreducibility labels

The certificate stores 820 distinct monic polynomials in E[X] and a product
factorization of each of the 1,272 event polynomials. Every coefficient is an
integer Eisenstein pair; every product is multiplied out exactly and compared
coefficient by coefficient. Hence every exceptional parameter is a root of
at least one listed factor. The list has degree histogram

| degree | count |
|---|---:|
| 1 | 6 |
| 2 | 3 |
| 3 | 28 |
| 4 | 87 |
| 5 | 144 |
| 6 | 258 |
| 7 | 168 |
| 8 | 126 |

The degree sum is 4,896. This is a conservative bound on the union of complex
roots; it is **not** a count of distinct unit-circle parameters. No root
isolation or real/unit-circle viability decision is required for coverage.

SymPy's exact factorization over Q(i√3) discovers the factors. The final proof
does not assume those factors are irreducible or pairwise coprime. Product
identities establish root coverage, and the separate coprimality checks below
establish the necessary edge exclusions for each colour word.

The 124 factors of degrees at most four are monic over E, so the h4119 theorem
applies to every one of their roots: the full unit graph on E[z] admits an
additive three-colouring. Its proof and compact residue certificates remain an
explicit dependency. The degree sum of these low-degree blocks is 444.

## 3. Three words cover every remaining factor block

The other 696 factors have degrees five through eight. Only these three linear
F3 words are needed, with coefficient weights listed in increasing digit order:

    w0=(1,1,1,1,1)
    w1=(1,1,1,2,1)
    w2=(1,1,1,1,2).

A label (a0,...,a4) receives Σ w_j a_j mod3, where the symbols of T are encoded
as 0,1,2. This is also reduction of the Eisenstein digits under ω↦−1.
All five weights are nonzero, so every monomial unit pair is properly coloured.

For each word, the checker identifies every nonzero event H that contains
**at least one monochromatic label pair**. Such an event is called bad for
that word. Each high-degree factor F is assigned a word: 396 use w0, 45 use
w1, and 255 use w2. For every bad H, the checker proves gcd(F,H)=1 over
Q(ω). Consequently no root of F can simultaneously realize any unit edge
that is monochromatic under its assigned word.

The proof of coprimality uses a small exact modular certificate. For a prime p
and a root r of r²−r+1 modulo p, reduce E→Fp by ω↦r. Both F and H are monic,
so their degrees are preserved. A Euclidean gcd of degree zero over Fp implies
a nonzero reduced resultant. Since the resultant is a polynomial in the
integer Eisenstein coefficients, its characteristic-zero value cannot be zero.
Therefore F and H have no common complex root. A modular gcd that is not
constant is inconclusive, and the checker tries another prime.

Every required exclusion is certified by one of three primes:

| prime | successful coprimality checks |
|---|---:|
| 7 | 376,116 |
| 13 | 5,730 |
| 19 | 42 |
| total | 381,888 |

The larger fixed prime list in the checker is only a deterministic fallback;
no check needs a prime beyond 19. No rational reconstruction, probabilistic
identity test, or inferred nonvanishing is used.

Let z be an injective unit-circle parameter lying on F. If an actual unit edge
were monochromatic under F's assigned word, its event H would be bad and
would satisfy F(z)=H(z)=0, contradicting one of the certified coprimalities.
Thus the word is a proper colouring of the full strict physical graph.

## 4. Collisions and conclusion

The h4119 theorem closes every noninjective A5(z), without a modulus condition,
at chromatic number three. Indeed a collision polynomial has degree at most
four and unit leading coefficient, so becomes monic over E. This is why no
label colouring is assumed to descend automatically at a collision.

First handle collisions by h4119. For an injective parameter, either no extra
event vanishes (the generic three-colouring), or one of the 820 factor blocks
contains the parameter. Low-degree blocks are again handled by h4119, and
high-degree blocks by their checked words. These cases exhaust every |z|=1.
Finally T is a unit equilateral triangle contained in every A5(z), so three
colours are necessary. This proves the theorem.

## 5. An exact physical control, beyond the collision theorem

For an explicit 243-point fixture, let t be the unique real root in
(-1/7,-1/8) of

    g(t)=81t^7+27t^6+261t^5−81t^4−189t^3−15t^2+39t+5,

and set z=(1+i√3 t)/(1−i√3 t). This specifies exact complex coordinates for
all A5 labels. The denominator cannot vanish for real t, and |z|=1 exactly.
The control checks uniqueness in the rational interval by a rational Sturm
sequence. It expands the Cayley substitution into the degree-seven factor

    F(X)=X^7+(1+ω)X^6+2ωX^5+(1+2ω)X^4
          +(-3+2ω)X^3+(-2+2ω)X^2+(-2+ω)X−1,

obtaining (1−i√3 t)^7 F(z)=i√3 g(t) coefficientwise.
The reduction of F modulo 31, with ω↦6, is irreducible: the checker verifies
X^(31^7)=X modF and gcd(F,X^31−X)=1. Since seven is prime these are the
complete Frobenius irreducibility conditions. A monic factorization over Q(ω)
would be integral over the integrally closed ring E and would reduce to a
factorization over F31, so F is irreducible over Q(ω).

It follows that no nonzero degree≤4 digit difference vanishes at z: all 243
points are distinct. Direct characteristic-zero division of every event H by F
then gives all strict unit edges, since F is the minimal polynomial of z over
Q(ω). There are **1,221** such edges. The first colour word checks every edge,
so this exact physical fixture has chromatic number three. It is a control
for the realization and edge bridge, not a positive target candidate.

## 6. Scope and trust boundary

This result retires the complete unit-circle branch of the current architecture.
It is compatible with the earlier collision closure and with HN3's h4117 D3
quotient. Remaining candidates must have |z|≠1 in addition to being injective,
having at least four active curves, satisfying 1/2<|z|≤2, and avoiding the
h4119 monic degree≤4 exclusion. The unit-circle locus can be removed from every
parameter system, not just from systems that explicitly include its equation.
The correct global-representative versus chamber interface is preserved.

The final checker uses only CPython integer and finite-field arithmetic. Its
Laurent all-pair event derivation is separate from the producer's canonical-word
convolution; it does not import producer code. The h4119 theorem, the standard
resultant reduction argument, and the written physical-to-algebraic reduction
are mathematical trust boundaries, not proof-assistant formalizations. The
producer uses SymPy 1.14.0, but all factor product identities are checked without
it. No SAT solver call or floating-point decision is a proof premise.

Reviewer-1 independently accepted the input h4105 finite-frontier theorem at
h4123. The present unit-circle theorem and the h4119 dependency have no
reviewer-1 verdict claimed by this package. No priority claim or improvement
to the Parts-509 record is made. The retired three-wheel architecture is not
reopened.

## Late shared frontier integration

During the ordinary push, HN3 advanced main with its h4135 exact-four-active
classification. That durable source was integrated before publication. Among
the 2,554 compatible global systems, 26 can support exactly four active curves
only through a pattern containing the circle. All 26 are excluded from that
exact-four branch. Of these, 22 explicitly contain the circle and are deleted
as whole systems; the other four remain in the full search with the stronger
at-least-five-active requirement.
Thus every exactly-four-active counterexample must lie on one of 2,528 no-circle
systems (allowance 155,648). Of the full retained list of 131,788 systems, the
other 129,260 require at least five active curves for a counterexample; this
does not exclude higher-incidence roots on the 2,528 compatible systems. The
new interface is necessary only. Its pinned 30,225-byte source is consumed by
frontier_effect.py, which checks subset membership and the revised sums. It
is a dependency only for these combined frontier counts, not for the unit-circle
three-colouring theorem.
