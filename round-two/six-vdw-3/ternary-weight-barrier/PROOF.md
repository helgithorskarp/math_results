# A weight barrier for three-periodic seven-term restrictions

Author: **six-vdw-3, researcher**, 2026-10-01. Colors are binary and color
addition means XOR. Arithmetic in the first coordinate is in the prime
field. A finite-group seven-term progression has nonzero step; repeated
points are included.

For a word `u:F_q -> {0,1}`, define condition (T):

```
For every a in F_q and every r != 0, some j in {0,1,2,3} satisfies
u(a+j*r) != u(a+(j+3)*r).
```

Thus the seven-bit restriction on any nonconstant field progression is
never three-periodic. The eight forbidden strings are the repetitions of
three-bit prefixes, truncated after seven bits. This condition forbids an
all-zero four-place difference ladder. It permits an all-one ladder.

**Computer-assisted lemma.** If `q=103` and (T) holds, then
`24 <= |u^{-1}(1)| <= 79`. Equivalently, both color classes have at least
24 points. No existence or attainment at either endpoint is asserted.

**Pair-extension lemma.** Let `q>=11` be prime, let (T) hold, and let `S`
be either color class. For distinct `x,y in S`, put `r=(y-x)/3`. Then

```
S intersects {x-r,x+r,x+2r,x+4r},
or both x-2r and x+5r belong to S.
```

Write `n=|S|`, and let the following counts range over all `x in F_q`
and all `r != 0`:

```
A = #{(x,r): x,x+r,x+3r in S},
B = #{(x,r): x,x+r,x+4r in S},
R = #{(x,r): x-2r,x,x+3r,x+5r in S}.
```

Then `2*A+2*B+R >= n*(n-1)`. These are ordered incidence counts, not
counts of unlabeled subsets. The lemmas are necessary conditions; neither
is a characterization of (T).

## 1. Products and the period618 application

The order-three forcing argument is established in
[six-vdw-1's QR23/order-nine proof](../../six-vdw-1/crt23x27/PROOF.md),
Section 1, source commit `d5ec681534b8a8bc168d06120cbb4a1397719779`, graph
`bafkreif6aaiyp74upte3rgxv3haqh5b7z7u3n562cl4n3lygsaswtkf22q` (8629).
We repeat the short argument to state the scope precisely; neither its
23-point classification nor its order-nine exclusion is a premise of the
new 103-point weight barrier.

Let `G` be a finite abelian group containing an element `h` of order three.
Suppose `c(x,y)=u(x) XOR v(y)` on `F_q x G` has no monochromatic nonzero-step
seven-term progression. Step `(0,h)` forces each `h`-coset triple in `v`
to be mixed. A mixed triple, its rotations and its color complement give
all six nonconstant three-bit patterns. Step `(r,0)` already forbids a
constant seven-bit restriction of `u`. If a nonconstant three-periodic
restriction existed in `u`, choose the start of a mixed triple of `v` so
that the two restrictions agree up to a constant color. Step `(r,h)` in
the product would be monochromatic. Therefore (T) is necessary. At
`q=103`, the weight lemma applies to every such product.

For `G=Z3` and `v=(0,0,1)`, (T) is also sufficient. If the field component
of the step vanishes, the nonzero second step cycles a mixed triple. If
only the second component vanishes, a monochromatic product would give a
constant, hence three-periodic, field restriction. If both components
are nonzero, a monochromatic product would give a three-periodic field
restriction matching `v` up to complement. Conversely a forbidden
nonconstant three-periodic restriction matches a rotation/complement of
`v`, and a forbidden constant restriction uses second step zero. This is
an exact equivalence with cyclic words
`c(t)=u(t mod q) XOR [t mod3=2]` when `q` is coprime to three.

In the original period618 separable family

```
c(t)=u(t mod103) XOR [t mod6 in {3,4,5}],
```

the second factor contains order-three steps. Thus (T), and the new
range 24..79, are necessary. The stronger exact characterization in
[parity-ladders](../parity-ladders/PROOF.md), graph
`bafkreiensnfvevjsgj2lowwszcvrwecpinqmp7sahc6urkwoletzjmgqca` (8565),
also forbids all-one ladders. The previous orientation range 20..83 in
[derivative-run-cuts](../derivative-run-cuts/PROOF.md), graph
`bafkreicyehlot4bifjk33ecolam64kdhd7fwtry43tnugmzbob4fijvns4` (8709),
is therefore strengthened to24..79. Its derivative range 32..72 remains
an additional restriction of that stronger family; we do not transfer it
to every (T) word.

The application includes a period618 repetition on `[1,3704]`: any cyclic
monochromatic nonzero-step tuple can reverse to step at most 309 and start
at a residue from0 through 617. Its integer lift ends at most 2471 in
zero-based coordinates, inside the target interval. Hence a valid
interval repetition must pass every cyclic constraint used above. General
interval colorings and nonseparable words are outside this result.

## 2. Weight-preserving normalization and quantified coverage

(T) is invariant under the pullback `u(x) -> u(p+s*x)`, with `s != 0`,
and under color complement. For a nonconstant word of weight at most 23,
choose any zero point `p` and any one point `z`. The word

```
U(x)=u(p+(z-p)*x)
```

has the same weight, satisfies (T), and has `U(0)=0,U(1)=1`. No color
complement is used in this low-weight normalization. Constant words fail
(T) directly. Thus it suffices to refute a *single at-most23 model* with
these anchors. Color complement then excludes weights 80..103.

The normalized fiber represents all
`sum_{j=0}^{22} binom(101,j) = 12830332301444490889792` anchored input
assignments. A full equivalent CNF encoding adds uniquely determined
auxiliary variables; there is no unproved symmetry quotient or partial
enumeration. The two excluded tails together contain
`2*sum_{w=0}^{23} binom(103,w) = 148289516201940983649536` labeled binary
words, with no overlap between the tails. This is coverage of the stated
word domain, not a count of solutions or of arbitrary 3704-point words.

## 3. Exact cut encoding and an independent word encoding

Normalize `U(0)=0`. The cut encoding has one variable `e_xy` for each
unordered pair `{x,y}`; pairs are lexicographically labeled1..5253.
In particular `e_0x` has label `x`. For `1<=x<y<=102`, four clauses impose
`e_xy = e_0x XOR e_0y`. These 20604 clauses uniquely extend all 102 word
bits. For each start and one reversal representative `r=1..51`, add

```
e_(a,a+3r) OR e_(a+r,a+4r) OR e_(a+2r,a+5r) OR e_(a+3r,a+6r).
```

The 5253 distinct positive ladder clauses are exactly (T). Reversal maps
`(a,r)` to `(a+6r,-r)` and reverses the four edges. It preserves both
three-periodicity and the clause. The independent auditor visits all
10506 directed `(a,r)` pairs and reconstructs the complete clause set;
reversal pruning is not accepted on numerical counts alone.

The alternative word encoding has only the102 field bits before adding
the counter. For each progression it forbids its eight three-periodic
seven-bit assignments with signed clauses. The fixed bit `U(0)=0` is
substituted exactly: an incompatible forbidden assignment makes the
clause true, and a compatible assignment removes that literal. Its
40596 distinct criterion clauses are audited by evaluating all 128
seven-bit strings and all 10506 directed progressions. The encoder uses
three-bit prefixes and reversal representatives instead. Both encodings
therefore describe the same word fiber through separate representations.
Only the cut encoding is used for the finite exclusion.

For either encoding, a full prefix counter has variables `C_i,k` meaning
`sum_{x=1}^i U(x) >= k`, for `1<=k<=min(i,24)`. Each variable is defined by

```
C_i,k <=> C_(i-1),k OR (U(i) AND C_(i-1),(k-1)),
C_i,0=True, C_i,k=False if k>i.
```

The encoder writes the Boolean equivalence, with constants substituted.
The independently pinned auditor derives prime implicates from the truth
relation, and checks full clause and variable coverage. We impose only
`NOT C_102,24`, together with `U(1)`. There is **no** lower-threshold unit
`C_102,23`: the model covers all weights at most 23, not just weight 23.
All 2172 counter variables have unique truth values given the word bits.

The production cut CNF has 7425 variables and 34421 clauses. Its SHA256 is
`baa98fd4c6e6574e89e81ae26a2ec73a1d32ce4261ddafdf30d21fe87cad6e0d`.
The second encoding has 2274 variables and 49160 clauses, SHA256
`0718fc3ababf30acee48480063ee397cdedeba1e9b2b12f5115ed5964807eaef`.
The public [expected.json](expected.json) records the complete metadata.

## 4. Independently checked refutation

CaDiCaL195, exposed through Python-SAT1.8.dev24, is a proof proposer.
It terminated with UNSAT within a 100000-conflict cap, using 77706
conflicts. A pinned `drat-trim` converter proposed a positive-hint
RUP-LRAT trace. The independent strict checker from
[six-vdw-1's binary-fiber source](../../../van_der_waerden_618_binary_fibers/check_rup_lrat.py)
checked every propagation hint and the final empty clause against the
exact independently audited cut CNF. No solver or converter verdict is a
mathematical premise. The trace contains 55363 accepted RUP additions,
89144 deletions and 1893670 checked hints. Its SHA256 is
`5495f681a05c850308663302f5cdef40997ac936285f2c8d39e92da757d12234`.

All model audits and proof replays run normally and with `python -O`,
so correctness checks cannot disappear with disabled assertions.
Complete q7/q13 controls compare both models to literal (T) on all
origin-normalized words, validate weight-preserving affine normalization,
and check accepted actual cyclic products on all starts and nonzero
steps. Four corrupted models, eight malformed generic proofs, two
damaged production proofs, and a changed pinned auditor are rejected.
At-most counter truth controls cover 6152 small signed-input assignments.
A one-conflict solver control remains UNKNOWN and produces no exclusion.
The full scripts, source pins and commands are in [README.md](README.md).

The proof corpus and model files are generated locally and omitted from
Git. Their absence is not an imported computational assumption: the
reproduction command regenerates and checks them. Independent source
paths separate the mathematical-model audit from both the generator and
the solver. Implementation independence is not an independent peer
review; the result is author checked and has no proof-assistant claim.

## 5. Proof of pair extension and its moment inequality

Put `y=x+3r`. Suppose the four inner test points `x-r,x+r,x+2r,x+4r`
all lie outside `S`. On the progression from `x-r` to `x+5r`, the first
six membership bits are `010010`. If `x+5r` were outside `S`, its seventh
bit would complete the forbidden three-periodic string `0100100`.
Therefore `x+5r` lies in `S`. Applying the same argument to the window
from `x-2r` to `x+4r` forces `x-2r` into `S`. This proves the pointwise
alternative for either color. The prime condition makes division by
three legitimate; q>=11 keeps all eight displayed local positions
distinct.

For each ordered pair `(x,x+3r)` in `S`, count the four inner extensions
and also the indicator that both outer points belong to `S`. The sum is
at least one. Summing over `(x,r)` gives exactly `n*(n-1)` on the right.
The inner point `x+r` contributes `A`. Reflecting the progression turns
the `x+2r` count into another `A`. Translation turns the `x-r` count into
`B`, and reflection turns the `x+4r` count into another `B`. The outer
indicator contributes `R`. This proves `2*A+2*B+R >= n*(n-1)`.

[elementary.py](elementary.py) checks all 256 assignments on the eight
local positions, and all 5120 origin-normalized words at q11/q13 for the
double-counting identities. It checks the inequality on all 240 (T)
words in those normalized domains. These finite controls substantiate
the identities; the written argument proves the lemma for every allowed
prime, without extrapolating a finite census.

## 6. Context, limitations and next frontier

[Monroe Table1](https://combinatorialpress.com/jcmcc-articles/volume-128/new-lower-bounds-for-van-der-waerden-numbers-using-distributed-computing/)
was rechecked on2026-10-01: two colors/seven terms is `>3703`, with prime 617
in Table 2. Monroe orders length before number of colors. A valid coloring
of `[1,3704]` would establish `W(2,7)>=3705`; none is supplied here. The
primary cyclic-construction context is
[Herwig et al.](https://www.cs.utexas.edu/~marijn/publications/waerden.pdf).

The new quantified content is the 103-point color-class barrier and the
general pair-extension incidence lemma. Equality ladders, XOR products,
order-three forcing and prefix counters are credited prior mechanisms.
Bounded current source/graph/primary-literature checks found no duplicate
of these two quantified claims; historical priority is not asserted.

At-most24 and at-most 26 exploratory models returned UNKNOWN under the
same 100000-conflict cap; at-most 24 did so in both encodings. They imply
no exclusion. Neither the complete (T) family nor the stronger separable
period618 family has been excluded. The next exact frontier is whether
weight 24 can occur under (T), using pair-extension structure to seek
better proof or construction mechanisms while retaining fixed resource
caps.
