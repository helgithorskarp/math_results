# Composite-modulus multiplier restrictions

## Statements and conventions

A symmetric sum-free colouring of `Z/n minus {0}` assigns colours to all
nonzero residues, satisfies `c(x)=c(-x)`, and forbids monochromatic `x+y=z`
when all three residues are nonzero. Repeated summands are included.
The number of colours means the number of nonempty colour classes.

For such a colouring define

    G = {a in (Z/n)^* : c(ax)=pi_a(c(x)) for some colour permutation pi_a}.

For a six-colouring:

1. At `n=538`, `|G|` is 2 or 4. An order-four generator has colour action
   identity, a single transposition, or two disjoint transpositions.
2. At `n=539`, `|G|` is 2 or 4 and every `pi_a` is the identity.

Both statements apply to strictly reflection-symmetric classical colourings
of `[1,n-1]`. Indeed a wrapping modular equation `x+y=z+n` reflects to
`(n-x)+(n-y)=n-z`. Sums equal to zero modulo n are outside the domain.
These results do not decide the existence of any unrestricted six-colouring
of `[1,537]` or `[1,538]`. No remaining symmetry family is claimed to exist.

We also establish sharp restricted colour counts at modulus 539: exactly nine
colours are needed when multiplier 67 permutes the colours, and exactly ten
when multiplier 344 permutes them. These are symmetry costs, not Schur bounds.

## Basic colour lower bounds

Write q_r for an upper bound on the number of vertices of a complete graph
with r edge colours and no monochromatic triangle. A vertex's neighbours
split into r sets, each avoiding that colour internally. Thus

    q_0=1,  q_r=r*q_(r-1)+1,
    q_1=2, q_2=5, q_3=16, q_4=65, q_5=326.

A symmetric sum-free r-colouring of the nonzero elements of an additive group
A edge-colours the complete graph on A by the colour of a difference. It has
no monochromatic triangle, so `|A|<=q_r`. In particular Z/11 needs at least
three colours; Z/49 and Z/77 need at least four. A colouring modulo 538 or
539 with at most six colours must use all six, because both moduli exceed
q_5. Its colour permutations are therefore unique, and `a -> pi_a` is a
homomorphism on G.

One known stronger bound is used: **classical S(4)=44**, with the largest
colourable endpoint convention. It implies that Z/49 minus zero needs at
least five colours, since a modular four-colouring would restrict to an
integer four-colouring of `[1,48]`. This is established prior work, stated
with this convention in [Heule (2018), Schur Number Five](https://cdn.aaai.org/ojs/12209/12209-13-15737-1-2-20201228.pdf),
Section "Schur Numbers and Variants". We do not reprove S(4)=44 here.
The included 48-entry witness shows that five colours suffice modulo 49.

## Separation of fixed and moved colours

Let A and B be finite additive groups and let an automorphism rho of A have
prime order ell. Suppose every nonzero a has a Schur triple in
`{+/- rho^j(a)}`. In any symmetric sum-free colouring of
`(A x B) minus {(0,0)}` equivariant under `(rho,id_B)`, fixed colours of the
induced palette permutation cannot occur on `A minus {0}` times `{0}`:
otherwise the whole signed rho-orbit of an occurrence has that colour and
contains a forbidden triple. On `{0}` times `B minus {0}`, every colour is
fixed, since the elements themselves are fixed.

Thus these two axes use disjoint parts of the palette. The moved part is a
union of ell-cycles. If the axes need at least u and v colours respectively,
the full colouring needs at least

    ell * ceil(u/ell) + v.                              (1)

The action on the used palette has order dividing ell because the spatial
automorphism does. This also handles the case of a trivial palette action:
it cannot provide any colour for the first axis. No assumption of a faithful
palette action is being made.

For `539=49*11`, use the Chinese remainder identification `Z/49 x Z/11`.
Multiplier 67 is `(18,1)`, has order 3, and

    1+18=-18^2 (mod 49).

Hence its signed orbit of every nonzero element of Z/49 contains a Schur
triple. The axis lower bounds are u=5 and v=3, so (1) gives `3*2+3=9`.
Even the elementary bound u=4 would suffice for nine.

Multiplier 344 is `(1,3)`, has order 5, and

    1+3=3^4 (mod 11).

Apply (1) with the axes reversed: u=3 for Z/11, v=5 for Z/49. The lower
bound is `5+5=10`. In particular, neither order-3 nor order-5 symmetry is
possible with six colours, including actions that move labels.

## Explicit colourings attaining nine and ten

The symmetric pair classes `{+/-1}`, `{+/-2}`, `{+/-3}` give a three-colouring
of Z/7 minus zero. For `a in Z/49 minus zero`, use the first nonzero base-7
digit: nonmultiples of 7 use one copy of these three colours, and multiples
of 7 use another copy. This is a six-colouring. A monochromatic sum either
projects to a forbidden sum in Z/7 or has zero first digit and moves to the
other palette. Multiplication by 18 rotates the pair labels in both copies
as `(0 2 1)(3 5 4)`.

Z/11 has a symmetric three-colouring with classes

    {1,4,7,10}, {2,3,8,9}, {5,6}.

For the nine-colouring of Z/49 x Z/11, colour `(a,b)` with the six-colouring
of a when `a!=0`; when `a=0`, use three fresh colours for b. This standard
product construction is sum-free and makes `(18,1)` rotate two triples of
colours while fixing the other three. It proves equality in the nine-colour
lower bound.

For ten colours, first colour every `b!=0` by its five symmetric pairs in
Z/11. On the axis `b=0`, use five fresh colours from the included Z/49
witness. Multiplier `(1,3)` cycles the first five colours and fixes the last
five. This proves equality in the ten-colour lower bound.

`construct.py` specifies these rules. `witnesses.json` contains each full
colour word, including the five-colour Z/49 input. The independent checker
verifies the words by literal addition, reflection, and multiplication.
These product constructions are standard in form; no new general product
method or nine-/ten-colour Schur lower bound is claimed.

## The order-7 obstruction at modulus 539

An order-7 multiplier must fix all six colours, since S_6 has no element of
order 7. The unique subgroup of order 7 in the unit group is generated by
`u=78=1+77`. Let `T=77(Z/539)`, an additive subgroup of order 7.

For every x not divisible by 7, its multiplier orbit is exactly the additive
coset `x+T`: indeed `u^j*x = x+77*j*x (mod 539)`, and x is invertible modulo
7. For x divisible by 7 the multiplier fixes x. Symmetry and doubling on
`T minus {0}` force three distinct colours, since the three pairs in Z/7
give the triangle of conflicts `1--2`, `2--3`, `3--1`.

None of those three colours can occur on a nonmultiple of 7. If t in T is
nonzero and x has its colour, then x+t has the same colour as x, being in
the same multiplier orbit. The three entries x, t, and x+t are then a
monochromatic Schur triple.
Thus the nonmultiples of 7 use at most three other colours. They descend,
by the cosets of T, to a symmetric sum-free three-colouring of

    D = (Z/77) minus 7(Z/77)
      = {(a,b) in Z/7 x Z/11 : a!=0}.

The following finite fibre lemma is the crucial step.

**Fibre lemma.** In every symmetric sum-free three-colouring of D, each
colour occupies at least ten points in some fibre `{a} x Z/11`.

Here is the complete finite proof, implemented in `fibres.py`. For a single
colour, write `B_a` for the set of second coordinates over a. Symmetry gives
`B_(-a)=-B_a`, so the three sizes `(s_1,s_2,s_3)` determine all six sizes.
Whenever a+b is nonzero modulo 7, sum-freeness requires

    (B_a+B_b) intersect B_(a+b) = empty.

For nonempty X,Y in Z/11 we use

    |X+Y| >= min(11,|X|+|Y|-1).                         (2)

Rather than importing a sumset theorem, the verifier checks (2) directly.
Independently translating X and Y puts zero in each, without changing any
of these cardinalities. There are 1024 subsets containing zero, so by
commutativity all 524800 unordered pairs suffice. Bitmasks represent the
subsets and exact cyclic shifts compute their sums.

The resulting necessary size inequalities admit 206 triples of integers
between 0 and 11. Enumerating three such rows that sum columnwise to
`(11,11,11)`, up to permutation of colours, gives exactly these seven profiles:

```text
(0,0,11), (0,11,0), (11,0,0)
(0,1,10), (1,10,0), (10,0,1)
(3,3,3),  (4,4,4), (4,4,4)
(3,3,4),  (4,4,3), (4,4,4)
(3,4,3),  (4,3,4), (4,4,4)
(3,4,4),  (4,3,3), (4,4,4)
(3,4,4),  (4,3,4), (4,4,3)
```

The first two profiles have the required large fibre for every colour.
The last five are excluded as follows. If a doubling source fibre and its
target both have size four, (2) and disjointness force the source sumset
to have size seven and the target to be its complement, with the appropriate
sign. Doubling permutes pair indices as `1->2->3->1`, with negative signs
in `2*2=-3` and `2*3=-1`. Enumerate all 330 possible four-element source
sets, determine the target, then enumerate the remaining three- or four-
element fibre and test every required sumset disjointness.

This gives exactly five valid `(4,4,4)` fibre triples. Every one omits zero
in all three fibres. Such a colour is absent from the zero-coordinate copy
of Z/7 minus zero, which requires all three colours by the doubling triangle.
This eliminates the four profiles containing `(4,4,4)`.

There are exactly thirty valid fibre triples of each type `(3,4,4)`,
`(4,3,4)`, `(4,4,3)`. Checking the 30-by-30 pairs of the first two types,
requiring disjointness and testing whether their coordinatewise complement
is of the third type, finds zero covers. This eliminates the final profile.
The enumeration omits no assignment: the target fibre is forced, and every
remaining set is explicitly enumerated. It proves the fibre lemma.

Return to modulus 539. For any one of the three colours on nonmultiples of
7, take a fibre with at least ten second coordinates. Its difference set is
all of Z/11, since any two translates of a subset of size at least ten in an
eleven-element group intersect. Thus, for every residue z divisible by 7,
there are nonmultiples x and x+z with that colour, using the quotient fibres
and then their full additive-coset lifts. If z had the same colour, there
would be a monochromatic Schur triple.

Consequently the entire nonzero additive subgroup `7(Z/539)`, of order 77,
can use only the other three colours. This contradicts `77>q_3=16`.
The order-7 multiplier is therefore impossible.

## The full multiplier group at 539

The unit group is `C_42 x C_10`, of order 420. Its subgroups of prime orders
3,5,7 are unique; the generators above are checked directly. A subgroup
whose order is divisible by one of these primes would contain the excluded
prime-order subgroup. Thus `|G|` divides four. Since reflection puts -1 in G,
its order is two or four.

The unit involutions other than the identity are `197,342,538`. On the
mod-49 axis, 197 is +1 and 342 is -1, while 538 is global negation. Each
therefore fixes the colour of every point on that axis. At least five
different colours occur there, by S(4)=44. A permutation of six colours
fixing at least five fixes all six. This proves that every multiplier in G
is colour-preserving, including the possible order-four Klein group.

## The full multiplier group at 538

The unit group modulo `538=2*269` is cyclic of order `268=4*67`. An order-67
multiplier has trivial palette action on six colours. The unique subgroup
of order 67 is generated by 5. Modulo 269 it contains `1,23,24`, with
`1+23=24`. On the even additive subgroup of Z/538 this gives the monochromatic
triple `2+46=48` inside the orbit of 2. Thus factor 67 is excluded from |G|,
leaving only two or four.

The order-four generator 187 squares to -1, so its palette action is an
involution. It fixes residue 269, whose colour must be fixed. An involution
of six labels with a fixed label has cycle type identity, `(2)(1)(1)(1)(1)`,
or `(2)(2)(1)(1)`. Three transpositions have no fixed label and are excluded.

## Prior work, evidence, and limits

Symmetric sum-free group partitions and colour-permuting automorphisms are
established methods; see [Penfold Street and Wallis (1976)](https://www.cambridge.org/core/services/aop-cambridge-core/content/view/7CB4302CC906B92797B934C93A7DD235/S1446788700013343a.pdf/sum-free-sets-coloured-graphs-and-designs.pdf).
[Fredricksen and Sweet (2000)](https://www.combinatorics.org/ojs/index.php/eljc/article/view/v7i1r32)
give the 536-colouring and multiplicative equivalence of symmetric partitions.
The [July 2026 shifted-template paper](https://arxiv.org/abs/2607.15034) still
uses S(6)>=536. The exact composite-modulus restrictions and fibre
classification here were not found in targeted primary-source and committed-
graph searches on 2026-09-28; this does not establish historical priority.

The proof uses elementary group arguments, exact finite subset enumeration,
the explicitly stated prior theorem S(4)=44, and direct witness checking.
The finite proof runs with the Python standard library. The counts in
`expected.json` are comparison evidence, not assumptions used to omit cases.
The checker does not formalize the displayed group-theoretic bridges or
reprove the imported S(4) theorem. No floating point, SAT/SMT soundness,
external dataset, or omitted certificate is part of the reproduction.

The results do not exclude reflection alone or the remaining order-four
families. Bounded construction searches in those families returned UNKNOWN.
No valid classical six-colouring of `[1,537]` is asserted.
