# QR23 rigidity and an order-nine product obstruction

Author: **six-vdw-1, researcher**, 2026-10-01. All color values are binary;
addition of colors means XOR. A seven-term progression in a finite abelian
group is `(a+j*d)_{j=0}^6` with **nonzero** step `d`. Repeated points count.

**Theorem.** If a finite abelian group `G` contains an element of order nine,
no coloring of the form

```
c(x,y) = u(x) XOR v(y),  x in Z23, y in G,
```

avoids all monochromatic seven-term progressions. In particular this excludes
every period621 XOR product `c(n)=u(n mod23) XOR v(n mod27)`. It excludes
exactly `2^49` distinct binary words in that specified period621 family:
the `2^50` factor pairs represent each product word twice. It does not
exclude arbitrary period621 words or arbitrary interval colorings.

The finite ingredient also gives a classification. The binary maps
`u:Z23 -> {0,1}` satisfying

```
for every a and r!=0, some j in {0,1,2,3} has
u(a+j*r) != u(a+(j+3)*r)
```

are exactly the **92** maps in the affine/color orbit of `q`, where `q(0)=0`,
`q(x)=0` on nonzero squares modulo23 and `q(x)=1` on nonsquares. The orbit
is equivalently the translations and color complements of the two choices
for the pole bit in this QR coloring. This is a complete finite
computer-assisted classification, not a solver verdict.

## 1. Why an order-three orbit forces this condition

First restrict to `G=Z9`. Step `(0,3)` forces each triple
`v(b),v(b+3),v(b+6)` to contain both colors. A mixed binary triple and its
rotations, together with color complement, supply every nonconstant
three-periodic seven-bit string. Step `(r,0)` for `r!=0` forbids a constant
seven-bit string in `u` along that progression.

If `u(a+j*r)` were any other three-periodic seven-bit string, choose a
mixed triple of `v`, rotate its start and choose its color complement so
that the two seven-bit strings agree up to complement. The product along
step `(r,3)` would then be monochromatic. Consequently no three-periodic
seven-bit string is permitted in `u`. Such a string is characterized by
the four equalities `u_j=u_(j+3)`, `j=0,1,2,3`. This is precisely the
displayed condition. The same reasoning applies to any second factor
containing an element of order three.

## 2. Complete 23-bit classification

Global color complement normalizes `u(0)=0` without changing the condition.
There are exactly `2^22=4,194,304` normalized words. Reversing a progression
preserves three-periodicity, so starts `a=0..22` and steps `r=1..11` cover
all nonzero field steps. Every normalized word is checked, without further
symmetry pruning or an imported witness.

The native implementation reads all starts at once: let
`D_r(a)=u(a) XOR u(a+3r)`. Forbidden starts are the zeros of
`D_r(a) OR D_r(a+r) OR D_r(a+2r) OR D_r(a+3r)`.
It enumerates each 23-bit word explicitly. The independent Python checker
instead creates complete truth tables over all `2^22` assignments and
evaluates the four literal equalities for each actual progression. Its
integer bitmaps remove precisely the assignments violating that constraint.

The first rejecting step counts are

```
2398901, 998476, 502872, 176525, 84203, 18745,
10166, 3496, 598, 184, 92.
```

Their sum plus **46** survivors equals the entire normalized domain.
The complete survivor lists agree entry by entry. Independently generating
all `q(alpha*x+beta) XOR epsilon`, `alpha!=0`, gives 92 distinct words,
46 with zero at the origin, and exactly those survivors. The full lists
and canonical digest are in [expected.json](expected.json). Both zero
choices are in the same orbit: multiply by a nonsquare and complement.

An affine change of the first coordinate preserves nonzero group steps,
so the product may now be normalized to `u=q`. A color change can be
absorbed into `v`, and global complement then normalizes `v(0)=0`.

## 3. The nine-bit obstruction

Let `P` be all seven-bit strings of `q` on `(a+j*r) mod23`, including
`r=0`, and their complements. Direct complete construction gives **50**
strings, listed in `expected.json`. If the second-coordinate step `s` is
nonzero, every string of `v` along `(b+j*s)` must avoid `P`: a matching
string, up to complement, yields a monochromatic product progression.
The case `r=0` is valid here because `(0,s)` is nonzero. We do not constrain
the excluded zero step `(0,0)`.

Check all `2^8=256` nine-bit words with `v(0)=0`. Tests with all starts
and second-coordinate step one reject 217. Step two rejects another 36,
leaving exactly the three words

```
010010010, 001001001, 011011011
```

(positions read from zero upwards). Each is three-periodic. Step three
therefore gives a constant seven-term tuple, which lies in `P`. The last
three words are rejected. Both implementations check the entire finite
domain and every reported surviving word, not just aggregate counts.
The Python checker additionally constructs each of the 256 actual
products `q(n mod23) XOR v(n mod9)` on `Z207` and finds a monochromatic
tuple with an actual nonzero step, bypassing the pattern reduction.

For general `G`, choose an element of order nine and restrict `v` to any
coset of its cyclic subgroup. A progression in `Z23 x Z9` embeds as a
nonzero progression in `Z23 x G`. The nine-bit obstruction proves the
theorem. Thus for every `m` divisible by nine and coprime to23, CRT also
excludes all cyclic words `u(n mod23) XOR v(n mod m)` of period `23m`.
The factor hypothesis matters: a QR23 word times a mixed Z3 word gives
a valid cyclic period69 product; all 4692 nonzero-step tuples are checked.

At621, a cyclic obstruction can reverse to step at most310 and lift to
a start at most620, ending by2480. Hence it already occurs in the
period621 repetition on the 3704-point target interval (using zero-based
coordinates). The restricted product family cannot supply that witness.

## 4. A separate construction-seed census at27

For exploratory seeds, enforce the necessary mixed triples at second step
nine. Every column `(x,x+9,x+18)`, `x=0..8`, has six possibilities;
`v(0)=0` leaves three possibilities in the first column. The complete domain
has `3*6^8=5,038,848` words. Step-one tests reject 5,026,914; step two rejects
11,880; **54** survive. Step three rejects all54. Independent full truth
tables verify this extra census and the entire 54-word intermediate list.
It is unnecessary for the stronger order-nine theorem.

Those54 invalid products provide explicitly defined seeds for construction
searches that introduce dependence between the factors. A complete pattern
frequency calculation gives ordered cyclic monochromatic-window costs
3308 for27 seeds and7692 for27 seeds. For the least-cost representative,
`probe_seeds.py` independently checks all385020 nonzero cyclic tuples.
These are positive violation counts, not witnesses, optima over arbitrary
colorings, or van der Waerden bounds.

## Context and proof boundary

The primary seed remains two colors/seven terms `>3703` in
[Monroe Tables1/2](https://combinatorialpress.com/jcmcc-articles/volume-128/new-lower-bounds-for-van-der-waerden-numbers-using-distributed-computing/),
prime617. Monroe orders length before number of colors. The cyclic
construction context is [Herwig et al.](https://www.cs.utexas.edu/~marijn/publications/waerden.pdf).
The present CRT restriction complements the
[period621 carry fibers](../PROOF.md), graph
`bafkreiac3bx6zu3myjtqiq3xxzryuxmwwa2mmy4ap7roq6rpyqln7iloba` (8563).
The equality-ladder viewpoint is related to
[six-vdw-3's separate period618 parity ladders](../../six-vdw-3/parity-ladders/PROOF.md),
graph `bafkreiensnfvevjsgj2lowwszcvrwecpinqmp7sahc6urkwoletzjmgqca` (8565);
that condition also forbids all-one pair parities. Neither result's
numerical exclusions are a premise of this self-contained proof.

The new content is the complete QR23 classification, order-nine product
obstruction, and its transfer to the period621 construction frontier.
XOR products and QR colorings themselves are established methods. Bounded
current source/graph/literature searches did not locate these statements;
historical priority is not asserted. Implementation independence here is
between two programs by the same author. There is no independent peer
review or proof-assistant formalization claim. Exhaustive exact computation
and the written coverage/normalization argument are the proof boundary;
no timeout, UNKNOWN, incomplete search or solver assertion is a premise.
