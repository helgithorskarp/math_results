# Additive maps on the complement of a sum-free set

An additive-map construction for Schur colourings can first choose one
sum-free colour class and then pull back a smaller colouring on its
complement. The result below reduces the additive map, for **every** such
class in an integer interval, to at most two values and explicit linear
relations. A second elementary lemma gives an exact obstruction for one
residue-based attempt at a 537-colouring.

These are structural lemmas, not a new Schur bound. There is no valid
537-colouring in this package. In particular, a five-colouring of a
complement need not arise from an additive map. All definitions include
equal summands. Historical priority for these elementary lemmas is not
asserted; targeted literature and committed-graph searches found no exact
prior statement.

## Determination by at most two values

Let N be a positive integer, let T be a sum-free subset of [1,N], and put
M=[1,N] minus T. Let G be any abelian group. Consider functions f:M -> G
such that

    f(x)+f(y)=f(x+y) whenever x,y,x+y belong to M.

Only these three-term relations are required. No preservation of arbitrary
four-term additive relations is assumed.

**Lemma.** There is a subset of M of size at most two such that restriction
to this subset determines every such f uniquely. The generators below
depend only on T. Additional relations between their values can occur;
arbitrary choices of two values are not asserted to extend.

**Proof.** First suppose 1 belongs to M. If T is empty, all values are
determined by f(1). Otherwise put t=min(T). If M has no member greater
than t, then M=[1,t-1], again requiring only f(1). In the remaining case
let b be the least member of M greater than t. Below b, the members of M
are exactly 1,...,t-1, and b-1 belongs to T.

For v>b in M, the positive integers v-1 and v-b cannot both belong to T:
otherwise (v-b)+(b-1)=v-1 is a Schur triple in T. Thus at least one belongs
to M. In the first case f(v)=f(v-1)+f(1); in the second case
f(v)=f(v-b)+f(b). Induction determines f from f(1),f(b).

Now suppose 1 belongs to T. The case N=1 has empty M. For N>=2, doubling
forces 2 into M. Also, no two consecutive integers lie in T. If no odd
integer belongs to M, all even integers belong to M and f(2) determines f.
Otherwise let b be the least odd member of M. All smaller odd integers
lie in T, all smaller even integers lie in M, and b-2 belongs to T.
For v>b in M, the positive integers v-2 and v-b cannot both lie in T,
because (v-b)+(b-2)=v-2 would violate sum-freeness. Hence f(v) is determined
recursively from f(2),f(b). This covers all cases. QED.

The proof uses neither division nor a property special to the integers
as target group. Over any field, the vector space of these additive maps
therefore has dimension at most two. The bound is sharp: T={2,3} in [1,5]
has M={1,4,5}, whose only equation is f(1)+f(4)=f(5).

## Exact parameterization

Choose a=1 or a=2 as in the proof, and b when it is needed. Choose one
permitted subtraction at each later v. This gives nonnegative integers
r_v,s_v with

    v=a*r_v+b*s_v,       f(v)=r_v*A+s_v*B,

where A=f(a), B=f(b). With only one generator use s_v=0. With empty M
there are no parameters. For every ordinary triple x+y=z wholly in M,
require

    (r_x+r_y-r_z)*A + (s_x+s_y-s_z)*B = 0 in G.

These conditions are necessary and sufficient: substitution verifies
every required equation, and the recursion proves that every additive
map is obtained. `parameterize.py` outputs the generators, coefficients,
and all distinct nonzero relation rows. It does not divide rows by gcds,
which would lose equivalence for target groups with torsion.

## Exact height on three residue classes

Let d>=4 and q>=1, and define

    M(d,q)={1<=v<=d*q+1 : v mod d is 0, 1, or d-1}.

For a nonzero integer-valued additive map on M(d,q), define its height
as max |f(v)|. Here nonzero means f(v) is nonzero for every v in the
domain. The complement of M(d,q) is not asserted to be sum-free for
arbitrary d; the following lemma does not need that hypothesis.

**Lemma.** The minimum height is exactly 2q+1.

**Proof.** Write A=f(d), B=f(1). Repeated addition of d, and the equations
1+(dj-1)=dj, force

    f(dj)   = j*A       (1<=j<=q),
    f(dj+1) = j*A+B     (0<=j<=q),
    f(dj-1) = j*A-B     (1<=j<=q).

Negating all values if necessary gives A>0. Also B is nonzero. If A>=2,
the maximum of |qA+B| and |qA-B| is qA+|B|>=2q+1. If A=1, avoiding zero
in the second sequence forbids B in [-q,0], and avoiding zero in the third
forbids B in [1,q]. Thus |B|>=q+1, and the same two endpoint values have
maximum at least 2q+1.

For the upper bound take A=2 and B=1. All values are nonzero and their
maximum absolute value is 2q+1. Use representatives 0,+1,-1 for the allowed
residues. For d>=4, a sum of two +1 residues or two -1 residues cannot land
in an allowed residue. Every remaining permitted sum makes the displayed
formulas add exactly. QED.

## Application to a proposed sixth colour at 537

Take T={v in [1,537] : v mod5 belongs to {2,3}}. This is sum-free modulo 5
and hence in the ordinary integers; it includes 537 and has 215 elements.
Its complement is M(5,107), so its exact minimum additive height is 215.
The parameterization gives generators 1 and 4, with no further relations.

In general, if a sum-free T has complement M carrying a nonzero integer
additive map of height at most L, any Schur k-colouring c of [1,L] gives
a (k+1)-colouring by assigning the new colour to T and c(|f(v)|) elsewhere.
Indeed, for a triple wholly in M the three nonzero signed labels obey
a+b=c. Their absolute values, after a permutation, obey an ordinary
Schur equation, including the doubling case.

For this particular T at 537, no such construction can pull back a
five-colouring of [1,160]: the required height is 215. This rules out
that additive mechanism for the stated T. It does **not** rule out arbitrary
five-colourings of the complement, other sixth-colour classes, other lift
mechanisms, or unrestricted 537-colourings.

The established value [S(5)=160](https://arxiv.org/abs/1711.08076) supplies
the natural base length; neither lemma relies on its proof. The
[July 2026 template paper](https://arxiv.org/abs/2607.15034) still uses
S(6)>=536. This package does not improve that numerical bound.

## Reproduction and trust boundary

Only Python 3.11 or later and its standard library are required. From
this directory run:

    sha256sum -c SHA256SUMS
    python3 -B parameterize.py
    python3 -B verify.py

The demo reports 215 deleted positions, 322 remaining positions,
generators [1,4], and no parameter relations. `verify.py` checks the
recursive determination on all 2,498 sum-free deletions in [1,n], 1<=n<=14.
For n<=9 it independently forms the literal equation matrix and computes
its rational rank, including doubled coefficients. It also compares the
parameter equations with all literal sums over small target groups with
torsion, verifies 90 three-residue upper constructions, and exhausts
55,440 parameter pairs below their claimed optimal heights. A separate
check establishes the height-215 application numerically from its forced
two-parameter form. Full expected counts are in `expected.json`.

The general proofs above establish the lemmas for all parameters. The
finite checks audit implementations and boundary cases; they are not a
replacement for those proofs. No SAT or SMT status, proof trace, numerical
approximation, external colouring fixture, or unproved general height
conjecture is part of the argument. The checking code is a separate audit
within this research lane, not independent peer review.
