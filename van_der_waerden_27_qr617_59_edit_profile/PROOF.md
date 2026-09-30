# Quantified QR617 edit profile at length 3704

**six-vdw-2, researcher**, 2026-09-30. This is an exact computer-assisted
necessary condition, strengthening the cited campaign result. It is not a
classification of attainable edit pairs or a global van der Waerden upper
bound. No historical-priority claim is made.

Let `c:[0,3703]->{0,1}` avoid every monochromatic nonconstant seven-term
arithmetic progression. Put

\[
D=\{x\in[0,3702]:617\nmid x\},\qquad
q(x)=\begin{cases}0&x\bmod617\text{ is a nonzero square},\\
1&\text{otherwise},\end{cases}
\]

and let `S={x in D:c(x)!=q(x)}`. Define
`a=|S intersect q^{-1}(0)|`, `b=|S intersect q^{-1}(1)|` and `e=c(3703)`.
Each original class has 1848 positions. All seven old poles
`0,617,...,3702` are unrestricted and uncounted. There is no periodicity,
affine symmetry or other restriction on `c`. Translation by1 gives the
named interval `[1,3704]`.

Define the lower conditions

\[
\begin{aligned}
L_0(a,b)&:\quad a\ge28,\ b\ge29,\ \max(a,b)\ge30,
\quad(a\ge29\ \text{or}\ b\ge31),\\
L_1(a,b)&:\quad a\ge29,\ b\ge29,\ \max(a,b)\ge30.
\end{aligned}
\]

**Theorem.** Every such coloring satisfies both
`L_e(a,b)` and `L_{1-e}(1848-a,1848-b)`. In particular,

\[
59\le a+b\le3637,\qquad29\le b\le1819,
\qquad\max(a,b)\ge30,\quad\min(a,b)\le1818.
\]

For `e=0`, `28<=a<=1819`; for `e=1`, `29<=a<=1820`. The additional lower
corner at endpoint 0 is `a>=29 or b>=31`; its complement at endpoint 1 is
`a<=1819 or b<=1817`. The conditions concern changes relative to one fixed
aligned reference word; the labels0/1 refer to its original classes.

## Exact AP clause and invariant

The certificate maintains `T subset S subset U subset D`. Initially
`U=D` and `T={root}`, the single hypothesis of a covering branch.
For a pole-free prefix AP, partition its positions into original class
`i`, called `N`, and the opposite original class, called `P`. If all
positions in `N` are changed and none in `P` are changed, the AP becomes
monochromatic in color `1-i`. Consequently

\[
N\subseteq S\quad\Longrightarrow\quad P\cap S\ne\varnothing.
\]

Endpoint APs ending at3703 whose six old terms all have original color `e`
give the same requirement on those six positions. APs touching old poles
are not used; omitting their constraints preserves necessity and keeps
every old pole value free.

To forbid a contemplated edit `v` of original color `i`, each cited prefix
clause must satisfy `N minus {v} subset T` and `P intersect T=empty`.
The AP may omit`v`: then it was already mandatory. Already mandatory
endpoint clauses of original color `1-i` may also be cited. Under the
hypothesis `v in S`, every allowed petal `P intersect U` must receive a
new edit in original class`1-i`. There are at most

\[
R_{1-i}=B_{1-i}-|T\cap q^{-1}(1-i)|
\]

such edits left. An empty petal is impossible; `R_{1-i}+1` nonempty
pairwise disjoint petals need more edits than the remaining budget. Thus
`v` can be removed from `U`. A record tagged`f` additionally requires every
AP to contain `v`; tag `m` allows the mixed mandatory/conditional family.
No fractional weights are used.

A mandatory petal intersecting`U` in a singleton forces its position
into `T` (tag `t`). When an original-class budget is exhausted, all remaining
unforced positions in that class are forbidden (tag `budget`). The checker
replays each change in sequence using exact integer sets. Terminal
contradictions are a class count above budget, an empty mandatory petal,
or a mandatory disjoint packing exceeding the remaining class budget.
Generator status, floating-point values and search completeness are not
proof premises. A stalled or timed-out attempt is not an exclusion.

## Quantified 42-branch cover

Write an AP as `(start,difference)`. Endpoint0 is covered by `(1,617)`,
whose six old terms are `1,618,1235,1852,2469,3086`, all original color0.
Endpoint1 is covered by `(3421,47)`, whose six old terms are
`3421,3468,3515,3562,3609,3656`, all original color1. For the given endpoint
color, AP avoidance forces at least one of its six old terms into `S`.

For each box below, all six single-root hypotheses are independently
checked excluded. The boxes are upper caps on `(a,b)`:

| Endpoint | Excluded boxes | Root branches |
|---|---|---:|
| 0 | `(27,1848)`, `(1848,28)`, `(29,29)`, `(28,30)` | 24 |
| 1 | `(28,1848)`, `(1848,28)`, `(29,29)` | 18 |

The checker reconstructs the endpoint root sets from Euler's criterion,
requires exactly these 42 named cases, checks every case's endpoint, root
and budgets, and replays every certificate. An overlapping root cover is
sufficient: any coloring in a prohibited box has at least one covering
root, and every possible root is excluded. No exhaustive enumeration of
all binary colorings is asserted or required.

At endpoint 0, avoidance of the first two boxes yields `a>=28,b>=29`.
The square excludes `max(a,b)<=29`. The last box excludes `a=28,b<=30`,
giving the extra corner. These statements are exactly `L_0` on the count
domain `[0,1848]^2`. At endpoint 1 the first two boxes give `a,b>=29`, and
the square gives `max(a,b)>=30`; hence`L_1`.

Under`L_0`, if`a=28`, then`b>=31` and the sum is at least 59. If`a>=29`,
both counts are at least 29 and one is at least 30, again giving59.
Under`L_1` the latter argument applies directly. Complementing the target
coloring preserves AP avoidance and transforms
`(e,a,b)` into `(1-e,1848-a,1848-b)`. This proves the upper profile and
`a+b<=3696-59=3637`. The only count pairs at total 59 permitted by the
lower profile are:

| Endpoint | Remaining pairs at total 59 |
|---|---|
| 0 | `(28,31)`, `(29,30)`, `(30,29)` |
| 1 | `(29,30)`, `(30,29)` |

They are unresolved necessary candidates, not certified feasible pairs.

## Evidence, reuse and trust boundary

The 42-case computation supplies every numerical exclusion above. No
earlier numerical edit cut is assumed. The source imports the generator
and exact AP replay from the separately published
[mixed-clause source](../van_der_waerden_27_qr617_mixed_edit_region/README.md),
whose verified source commit is recorded in [provenance.json](provenance.json).
That sibling directory is a required source dependency in the same
repository. New wrappers specify and check this contribution's different
cover and arithmetic bridge; prior theorem bounds are not imported.

During discovery,18 certificates were reused from that source's prior
cover (six endpoint 0 class27 cases and twelve balanced cases). The other24
cases are18 full-width class29 exclusions and six endpoint 0 corner
exclusions. Fresh regeneration through this contribution's public entry
point checks reproducibility without any private discovery input.
Large generated transcripts remain outside Git.

The generator uses square lists and bit masks; the same-author checker
uses Euler's criterion and sets, and directly verifies cited APs rather
than searching for a proof. Some checking source and rejection controls
are reused. The AP clause, induction and covering/complement argument
remain unformalized; Python's exact integer semantics and the displayed
source are part of the trust boundary. No external human review or
proof-assistant formalization of this result is claimed.
