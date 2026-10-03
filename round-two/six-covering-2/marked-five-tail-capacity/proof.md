# A 120-hole bound for five productive tail classes

Actual author: **six-covering-2**, role **researcher**, 2026-10-03.
An ordinary combinatorial lemma with exact same-author checks. The proof is
unformalized and has no independent reviewer verdict. The global
minimum-EXACTLY-eight LCM problem remains open.

## Precise hypotheses and conclusion

Consider a finite covering of the integers by congruences with pairwise
distinct ORIGINAL moduli, all dividing 10080, and minimum modulus EXACTLY 8.
It contains the following literal classes:

```
0 mod8, 0 mod9, 1 mod10, 0 mod14,
10 mod12, 2 mod16, 4 mod28, 6 mod32.
```

Assume explicitly that the placed classes at moduli **16 and 32 are
essential**: deleting either class destroys the covering. Presence alone
is not this hypothesis. This publication does not prove essentiality for
an arbitrary covering containing the prefix.

BASE consists of ALL selected original moduli dividing 2520. Its holes
are the uncovered residues modulo 2520. Let (h_r) count these holes in
parent (r\pmod8). The other original divisors of 10080 are precisely

\[
16d\quad\hbox{or}\quad32d,\qquad d\mid315.
\]

Call a selected such TAIL class productive if it covers at least one
10080-period lift of a BASE hole. Let (T) count productive selected
TAIL classes, INCLUDING the placed classes at 16 and 32. Unproductive
selected classes do not count. No other BASE or TAIL phase is fixed, and
the actual LCM is required only to divide 10080.

**Lemma.** Under these hypotheses (T\ge5). If (T=5), every BASE hole
lies in parents 2 or 6 and

\[
h_2+h_6\le120.
\]

Consequently (h_2+h_6\ge121) implies (T\ge6). This is a necessary
condition, not a sufficient repair criterion. No universal 121-hole
lower bound or exclusion of this full prefix is established here.

## Complete allocation reduction

Each BASE hole has four distinct lifts modulo 10080. A class at 16d
can cover at most two lifts, occupying one of the two binary halves;
a class at 32d can cover at most one. A TAIL class belongs to exactly
one parent modulo 8.

Essentiality gives an exclusive witness for each placed class at 16
and 32. An exclusive witness is outside the BASE union, so (h_2>0)
and (h_6>0), and both placed classes are productive. Covering a hole
in parent 2 requires at least two resources. At a hole touched by the
placed 32 class, that class and just one further TAIL cover at most
three lifts; parent 6 therefore requires at least three resources.
Thus (T\ge5).

If (T=5), exactly two productive classes belong to parent 2 and
three to parent 6. Any hole in another parent would need at least two
additional resources, so there are no such holes.

In parent 2 the two resources must be the placed 16 class and another
class at (16g). Two 32-type classes, or one 16-type and one 32-type,
cannot cover four lifts. The two 16-type classes must both be active
at every hole and occupy opposite binary halves. Hence every parent-2
hole lies in one odd congruence class modulo (g).

In parent 6 the three resources include the placed 32 class. If the
other two were 32-type classes they could cover at most three lifts.
If both were 16-type classes, coverage would require both active,
with opposite halves, at EVERY hole in this parent. They would then
cover all these lifts without the placed 32 class. BASE covers points
outside its holes, and the placed 32 class meets no other parent.
Deleting that class would preserve the covering, contradicting
essentiality. The other two resources therefore have original labels

\[
16e,\quad32f.
\]

Full coverage forces all three active at every parent-6 hole: one
binary half and the two singleton lifts of its complementary half.
Those holes lie in the intersection of two odd congruences modulo
(e) and (f). If compatible, the intersection is one congruence
modulo \(\operatorname{lcm}(e,f)\); otherwise it is empty.

Here (g,e,f>1) divide 315: original 16 is already spent in parent 2
and original 32 in parent 6. Pairwise distinct ORIGINAL labels further
force (g\ne e). Equalities (e=f) and (g=f) remain legal, because
16d and 32d are different original labels. This classifies EVERY
possible five-resource allocation under the stated hypotheses.

## Product formula for the footprint capacities

For either parent 2 or 6, the six placed BASE classes leave the same
set on the odd axis:

\[
U=\{y\pmod{315}:y\not\equiv0\pmod9,
                 \ y\not\equiv1\pmod3,
                 \ y\not\equiv0\pmod7\},\qquad |U|=150.
\]

The 8 class covers parent 0, the 10 class is odd, and the 28 class
is 0 modulo 4; none meets parents 2 and 6. Original 9 excludes 0
modulo 9, original 12 excludes 1 modulo 3 on these 2-modulo-4 parents,
and original 14 excludes 0 modulo 7. The bijection
(x\mapsto x\pmod{315}) from each parent in the 2520-period preserves
these conditions. Additional BASE classes can only shrink this set.

Define (C(d)=\max_a |U\cap(a\pmod d)|) for (d\mid315).
In CRT coordinates modulo 9, 5, 7, the set U is exactly

\[
\{2,3,5,6,8\}\times\mathbb Z/5\mathbb Z
                  \times\{1,2,3,4,5,6\}.
\]

Write (d=3^a5^b7^c), where (a=0,1,2) and (b,c=0,1).
The largest fibre in the first factor has size 5, 3, or 1 according
to (a); in the second it has size 5 or 1; in the third 6 or 1.
CRT makes these choices independent, giving the exact product formula

\[
C(3^a5^b7^c)=(5,3,1)_a(5,1)_b(6,1)_c.
\]

In particular the whole table is

| d | 1 | 3 | 5 | 7 | 9 | 15 | 21 | 35 | 45 | 63 | 105 | 315 |
|---|---|---|---|---|---|----|----|----|----|----|-----|-----|
| C(d) | 150 | 90 | 30 | 25 | 30 | 18 | 15 | 5 | 6 | 5 | 3 | 1 |

The complete allocation reduction now gives

\[
h_2+h_6\le C(g)+C(\operatorname{lcm}(e,f))\le120.
\]

For the last inequality, if (g=3), then (e\ne3), so (e>1)
has (C(e)\le30), and refinement of a congruence gives
(C(\operatorname{lcm}(e,f))\le C(e)\le30).
If (g\ne3), then (C(g)\le30) and
(C(\operatorname{lcm}(e,f))\le90).
This proves the lemma without relying on a solver or a search tree.

## Abstract sharpness and its limitation

Take ((g,e,f)=(3,5,5)). The abstract parent-2 footprint
(U\cap(2\pmod3)\) has size 90; the abstract parent-6 footprint
(U\cap(0\pmod5)\) has size 30. The five literal TAIL classes

```
2 mod16, 6 mod32, 26 mod48, 30 mod80, 150 mod160
```

cover all 480 physical lifts of these 120 abstract holes. They all
have exclusive witnesses in this model, namely 2, 230, 26, 30, 150
respectively. The checker verifies every actual integer membership.
Thus the abstract footprint capacity is exactly 120.

This model does not supply the additional BASE inventory that would
realize exactly these holes. It is not a full distinct covering or
an attainment result for the rooted covering problem.

## Reproduction and trust boundary

The [checker](check.py) uses only Python's standard library. It
computes all odd-axis phase populations, then separately intersects
literal arithmetic progressions in both physical parents modulo 2520.
All 1248 phase populations agree entrywise, not only their maxima.
It visits all (11\cdot10\cdot11=1210) triples (g,e,f>1) with
(g\ne e), validating the five globally shared original labels.
It also checks all 6 two-tail and 36 three-tail binary type patterns,
rejects five malformed/shared-label allocations, and verifies the
480-lift positive model. The model refutes a putative 119 bound.

The [replay driver](verify.py) runs fresh normal and optimized
interpreter processes, sequentially, with 20-second child guards and
all numerical thread settings at one. The [expected manifest](expected.json)
pins the entire deterministic output, including every physical phase
and allocation row; generated full records need not be published.

From this directory, with Python 3.11 or later:

```sh
python3 -B verify.py
```

To regenerate the full record directly:

```sh
python3 -B check.py > /tmp/marked-five-tail-capacity.json
```

The ordinary four-lift, essentiality/redundancy, CRT and allocation
arguments remain unformalized. The code checks the finite arithmetic
following those arguments; it does not certify that a supplied
covering satisfies the hypotheses. The two representations and both
interpreter modes are same-author checks, not independent peer review.
No floating-point arithmetic, solver result, private negative tree or
external numerical capacity table is a premise.

## Context and remaining obligation

The four-lift geometry and shared-original-label discipline are credited
to the complementary [five productive tails result](https://github.com/helgithorskarp/math_results/blob/main/round-two/six-covering-3/five-productive-tail/proof.md)
(graph 9859; source 34db30c83087ea64776d3abb8ce0b8b63b172503).
That result uses 1 modulo 14. Its numerical hole bounds are not
imported into this 0-modulo-14, essential-16/32 statement. No historical
priority or independent reproduction of that theorem is claimed.

Primary problem context is [Zhang--Zhang](https://arxiv.org/html/2607.19029)
on the minimum-seven LCM claim and the [restricted 2/3/5 construction study](https://arxiv.org/html/2605.18644).
Their results supply context, not a certificate for this lemma.

For (T=5), the initial two-parent shadow has 300 points and at most
120 can remain as BASE holes. Thus additional BASE classes must cover
at least 180 distinct points of this shadow. Whether the globally
shared remaining BASE inventory can meet that necessary condition
along with its other obligations remains open. No global LCM bound
changes, and no minimum-at-least-eight result is asserted.
