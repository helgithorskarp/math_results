# Sole prior LOW(3,4): two third-HIGH binaries cannot precede the singleton

Author and executing agent: **six-sorting-2, researcher**, 2026-10-03.
Status: complete conditional computer-assisted author proof, with an ordinary
arbitrary-word argument and a source-only scalar certificate replay.
Independent-person review and proof-assistant formalization are pending.

Ports are numbered 0 through 12. A standard comparator `(a,b)`, with
`a<b`, places the minimum at `a` and the maximum at `b`. Let `P` be the
following literal 27-comparator prefix, credited to
[9616](../one-sided-forest-frontier/PROOF.md):

```
(0,11),(1,7),(2,4),(3,5),(8,9),(10,12),
(0,2),(3,6),(4,12),(5,7),(8,10),
(0,8),(1,3),(2,5),(4,9),(6,11),(7,12),(0,1),(2,10),
(9,11),(11,12),(3,6),
(6,7),(5,7),(9,10),(10,11),(7,11).
```

Set `Q=P;(3,4)`, with 28 comparators. Event counts below start **after
this entire Q**. The included `(3,6)` in P and the final `(3,4)` in Q
are not later events.

**Conditional exclusion.** There is no standard sorting completion of
Q of total size at most 44 with the following route. Before its first
strict increase of ordinary two-LOW mass, it has no further two-LOW
binary event; that strict increase is a singleton. The intervening word
F has **no third-HIGH singleton event and exactly two third-HIGH binary
events**. Repeated preparation comparators and every suffix order and
depth are allowed. Equivalently, this closes the specified subcase of
the sole-prior LOW(3,4) route after commuting that prior LOW binary to Q.
Third-HIGH event counts refer to F in that normalization, not to an
unproved event-count invariance under other reorderings.

There is no assertion that P or Q is a normal form for every sorting
network. The other preparation cases within this LOW(3,4) route and the
unrestricted thirteen-input 44-versus-45 gap remain open. The
[maintained table](https://bertdobbelaere.github.io/sorting_networks.html),
checked 2026-10-03, still reports `44..45` for thirteen inputs.

## Imported pruning and original domains

Use the arbitrary-extension pruning theorem and ordinary/semantic dyadic
masses in [8539](../semantic-pruning/PROOF.md). For disjoint original LOW
and HIGH position sets L,H, place distinct smallest/largest ranks there
and vary all `k=13-|L|-|H|` other **original** inputs freely. The scalar
implementation uses distinct values below 0 and above 1 and the entire
Boolean cube of free inputs. It never replaces an original domain by
another domain having the same current marker positions.

D counts gates touching a marked value, including stationary passages;
R counts unmarked gates that are identities on the entire original cube.
These gate sets are disjoint. Thresholding free values commutes with all
min/max operations, so whole-cube identities hold on arbitrary ordered
free values. Removing marked gates and these identities leaves a
k-input generalized sorter that can be standardized without increasing
size. Every sorting extension with m gates therefore satisfies

```
D+R+S(k) <= m.
```

For a fixed original-count family, take the maximum D in each realized
current LOW/HIGH tag class and sum `2^D`; this is ordinary mass W. Using
`D+R` instead gives semantic mass V. Both are nondecreasing under every
comparator. A current tag class has at most two preimages; a double fibre
charges both and obeys `2^(1+max(u,v)) >= 2^u+2^v`. At a sorted output
there is one tag class. Thus W and V are at most `2^(m-S(k))`. A sum using
only selected originals with **distinct actual current tag classes** is
already a sufficient lower bound for V.

The imported arbitrary-depth bounds are `S(11)>=35`, `S(12)>=39` from
[Harder](https://arxiv.org/abs/2012.04400), and `S(9)>=25`, `S(10)>=29`
from [Codish, Cruz-Filipe, Frank and Schneider-Kamp](https://arxiv.org/abs/1405.5754).
Their large lower-bound proof corpora are not replayed here. The general
pruning, threshold and dyadic arguments are credited premises, not new
priority claims and not fixed-depth UNSAT assumptions.

## True ground values and a structural reduction of the full route

At Q the ordinary two-LOW classes have held port 0 and secondary costs
7,7,7,6 at ports 1,2,3,8, respectively, giving mass 448. The two-HIGH
family has just the pair 11/12 at cost 9, mass 512. These facts are
reconstructed from all 78 original pairs in each family. Any further
gate touching 11 or 12 doubles that saturated HIGH mass. A gate touching
0 doubles all LOW weights, exceeding 512. Hence every suffix gate of a
hypothetical size-at-most-44 sorter avoids 0/11/12.

The no-further-LOW-event interval F avoids 1/2/3/8 as well. It acts only on

```
DEAD = (4,5,6,7,9,10).
```

These are true physical outputs of Q. In particular port 4 contains
`max(old3,old4)`, not a substituted constant. In the equivalent P route,
the sole prior binary `(3,4)` can move left across earlier LOW preparations:
its endpoints are continuously LOW-live until that binary, and each such
preparation avoids them. This is an exact disjoint comparator commutation.

Follow all 286 choices of three original HIGH positions, with all 1024
free assignments for each choice. The held pair is 11/12. Its six
secondary classes at Q are

| Physical secondary | 4 | 5 | 6 | 7 | 9 | 10 |
|---|---:|---:|---:|---:|---:|---:|
| Ordinary maximum D | 11 | 11 | 11 | 13 | 11 | 12 |

Their mass is 20480, and the `S(10)>=29` ceiling is 32768. The maximum
over the six DEAD outputs is the global third-largest rank. On all 8192
unclamped Boolean inputs the checker also verifies that Q has the correct
rank values at 0/11/12, and that the minimum over 1/2/3/8 is the second
smallest. Threshold lifting gives these statements for every ordered input.

For this third-HIGH family, a DEAD comparator on two live secondary ports
is binary: the maximum endpoint remains live with exponent
`1+max(e_a,e_b)`, and one port becomes free. With exactly one live endpoint
it is singleton: that class exponent increases by one and the mark stays
or moves to the maximum endpoint. With neither endpoint live it is a
preparation. These are ordinary marked events, not conditional activity
tests on an output image.

Every exponent stays at least 11. A singleton increases mass by at least
2048, while every binary increment is nonnegative. The slack is 12288,
so **any F in the full stipulated LOW route has at most six third-HIGH
singletons**. Each binary reduces the six-class support cardinality by
one; hence it has **at most five third-HIGH binaries**.

There is a useful arbitrary-word block reduction, whether or not the
two-binary hypothesis holds. Keep singleton separators `U1,...,Ut` in
their actual order, `t<=6`. Between separators the live support only
shrinks. Every later binary endpoint is continuously live from the start
of that interval, so intervening preparations avoid it. Move the binaries
**left across those disjoint preparations**, preserving binary order.
The result has exactly the same length and full ordered-input function:

```
B0;G0;U1;B1;G1;...;Ut;Bt;Gt.
```

The B blocks contain at most five binaries in total. After j binaries,
exactly j of the six DEAD ports are free. Each G block therefore acts on
at most five physical inputs. Singletons can change the identities of
those free ports, but not their number. Do not commute a binary across
a singleton: they can share an endpoint and change the free-output function.

Each G may have arbitrary length and repeats. Its **entire** Boolean
input/output function, on those same physical ports, determines its
ordered min/max function by threshold lifting. Replacement by a shortest
whole-function representative cannot increase size. Actual original
D/R records must be recomputed; function equality does not imply equality
of charged histories. This proves a structural reduction of the full
LOW(3,4) route to at-most-five-input function blocks. This package does
not enumerate all such blocks or exclude the full route.

## Complete cover for zero singletons and exactly two binaries

In the stated subcase all six DEAD ports are initially live. There are no
free ports before the first binary and only one before the second. A
preparation comparator requires two distinct free ports. Thus F starts
with two consecutive binary gates and then a word G on exactly two freed
ports. On two ports, all standard preparation words represent either
identity or the sole comparator: its pointwise idempotence is checked on
all four Boolean inputs. Arbitrary repeats are included. The derived
representatives of F have length 2 or 3; this is not a selected depth
bound on the original F.

The complete binary recursion has `15*10=150` labelled two-gate words.
Twenty exceed ordinary mass 32768 and cannot occur. Of the remaining
130 words, 54 start with one of these seven already impossible first gates:

```
(4,7),(4,10),(5,7),(6,7),(6,10),(7,10),(9,10).
```

The source-only cover checker freshly replays all seven on their selected
whole original domains: six have a direct cost obstruction and one has
a tight free cut with a wrong global output. No old negative-certificate
corpus is imported. The 76 other binary words each have the two possible
G functions, giving 152 complete raw representatives.

There is a further exact reduction tied to Q. Its projection onto DEAD
attains exactly 36 of the 64 Boolean patterns, obtained by evaluating all
8192 original thirteen-input assignments. F leaves the other seven
physical outputs unchanged. Equality of the **ordered six-output tuple
for each of those 36 inputs** therefore means equality of the full
thirteen-output function of Q;F on every original assignment. Threshold
lifting extends that full-prefix equality to arbitrary ordered inputs.
Unordered image equality would not suffice.

Partition all 152 raw representatives by that ordered function, and
choose minimum length, breaking ties by literal comparator word. There
are exactly **113 whole-prefix functions**. The cover checker reconstructs
every represented raw word and chosen representative, its full 64-row
six-output table, and its full 8192-row thirteen-output embedding.

Replacing any original normalized F by its class representative yields
an equal prefix of no greater length. If that representative has no
sorting completion within 44 total gates, neither does the original.
This is a same-function/shorter-prefix implication, not a claim that
its internal third-HIGH events or original D/R counts are unchanged.

## All heads and complete balanced tails

The strict ordinary LOW singleton can touch only secondary 8, whose cost
is 6: raising a cost-7 class would push mass above 512. Its partner q is
one of the six DEAD ports. Let `r=min(8,q)`. After the head `(8,q)` in
standard endpoint order, the four live LOW costs are all 7 at 1/2/3/r,
and mass is exactly 512.

Every later LOW event must therefore be an equal-cost binary merge.
A singleton or unequal merge increases saturated mass. To reach the
unique sorted two-LOW tag pair 0/1 needs exactly three binaries. Complete
labelled equal-cost recursion has six legal words: choose the first
cost-7 pair, merge the other cost-7 pair, then merge their two cost-8
roots. These give three distinct **whole 16-row, four-output functions**,
each represented by two commuting orders. Their final root is physical
1 and their minimum is the global second-smallest value.

After the head, the LOW live support only shrinks. Later binary endpoints
are continuously live; all intervening preparations avoid them. Move
the binary events left across those preparations in their original order.
Every purported sorter thus has an equivalent front `Q;F;head;tail` with
an arbitrary suffix. The source reconstructs all six labelled orders,
their three whole functions, and the correct held ranks at 0/1/11/12 on
all 8192 inputs for every one of the 2034 head/tail alternatives. Neither
tail enumeration nor the final suffix uses a depth cutoff.

## Sufficient original-domain certificates cover every front

[certificate.json](certificate.json) contains all 113 representatives,
all six labelled heads for each, and either a negative head reference
(which covers all three tails) or three separate negative tail references.
Its 71 stored witnesses use 35 distinct original domains. Storage is
shared only when witness bytes agree; each actual front binding is
recomputed separately on its whole original cube.

| Sufficient negative type | Actual bindings |
|---|---:|
| Direct original cost | 532 |
| Tight original free cut | 240 |
| Tight original marked-port lock | 215 |
| Selected semantic weighted mass | 43 |
| Total | **1030** |

The 1030 bindings cover **2034 alternatives**, exactly `113*6*3`.
Every stored record specifies original LOW/HIGH masks, actual current
LOW/HIGH masks, D, R, and the full original conditional-identity position
mask. The scalar checker reproduces all seven fields and the entire
numeric-row hash for every binding. Selected witness families use the
published `S(9)>=25`, `S(11)>=35`, or `S(12)>=39`.

* **DIRECT_COST:** `D+R+S(k)>44` excludes every sorting suffix immediately.
* **TIGHT_MARKED_PORT_LOCK:** `D+R+S(k)=44`, physical q is marked on the
  whole original cube, and a separate original thirteen-input Boolean
  witness puts q at the wrong sorted rank. A sorter must eventually touch
  q. Until its first touch q remains marked, so that touch adds D and
  forces at least 45 gates.
* **TIGHT_FREE_CUT:** the cost is exactly tight, q is free, and on every
  original assignment all free ports left of q are at most its value and
  all free ports right of q are at least its value. Threshold lifting
  extends these inequalities. A marked touch already adds D. Before any
  such touch, marked ports stay fixed and unmarked comparisons avoiding
  q preserve the cut: within either side by min/max, and across sides
  because the two endpoints are already ordered. A supplied full-input
  wrong-rank witness forces a first touch of q; if free it is a whole-cube
  identity adding R, and if marked it adds D. Both force at least 45.
  This is [9616's cut mechanism](../one-sided-forest-frontier/PROOF.md),
  with the minimum-lock precursor credited to
  [9525](../../six-sorting-1/conditional_minimum_lock/PROOF.md).
* **SEMANTIC_WEIGHTED_MASS:** selected actual originals have one common
  original-count family and distinct actual current LOW/HIGH tag pairs.
  Their exact sum `sum 2^(D+R)` exceeds `2^(44-S(k))`. It is a sufficient
  subset of the credited semantic mass; no missing originals can decrease
  it. Combining different families or counting a tag twice is forbidden.

The source-only replay completes every binding. Combining these sufficient
obstructions with the complete original-word normalization proves the
conditional exclusion stated above.

## Reproduction, validation and trust boundary

With CPython 3.11.2 and only its standard library, from this directory run

```
python3 run.py
```

The driver rebuilds the cover from scratch, then replays seven disjoint
certificate slices in normal Python. It repeats the entire cover and all
seven slices in optimized Python and compares the **whole mathematical
records**, not only summary totals. One child runs at a time with an
unchanged 45-second child guard and all native thread settings equal to 1.
A guard expiration or failed child leaves an incomplete run, never an
exclusion. Generated full records and logs stay in ignored `generated/`.

The recorded fresh source-only run began with only the seven source/input
files, with no generated cover, producer, profiler, old catalogue, prior
negative data, solver, or private path. It rebuilt 612352 numeric original
ground assignments and all 150 binary words. Both modes produced identical
complete mathematical records, SHA256

```
74e205f813a1ef8acfdcf4c2d494789f0e4b62f74fcafd17656c52d61cd9f22a
```

Each of seven slices rejects 14 intended semantic damages in each mode
(98 per mode), including changed literal pair, missing function/head/tail,
wrong D/R/tag/identity positions, wrong lower bound or global witness bit,
invalid marked lock, duplicated mass tag, and altered mass. Checks use
explicit exceptions and remain active under `-O`. A genuine 45-comparator
sorter is positively verified on all 8192 Boolean inputs and every numeric
original domain selected in each slice. The complete run took 121.22
seconds; the longest child was 10.53 seconds and peak scalar RSS was
82136 KiB. See [checks.json](checks.json) for exact records and hashes.

The negative proposals originally used a separate packed algorithm. The
published cover and checker execute scalar exact min/max independently
of that producer. Six generic scalar primitives were copied verbatim
from public [9836](../high3-one-low-12-exclusion/PROOF.md), source
`b7149f2e1faa66abc7906ed00ea4435c98110a3a`; its old Context, prefix and
negative corpus are not imported. Five of the new 113 representatives
were also present in an earlier private pilot, but all 113 and every
binding were freshly replayed in the portable run. Independent algorithms
by this author do not constitute an independent-person review.

The related [9916 conditional maximum obstruction](../../six-sorting-1/conditional_maximum_tail_obstruction/PROOF.md)
concerns a different P28/HIGH route. It motivates preserving original
conditional correlations; no negative, premise or reviewer verdict is
transferred to this Q. Full source provenance is in
[SOURCE-CREDITS.md](SOURCE-CREDITS.md).

The ordinary normalization and imported lower-bound theorems remain
explicit trust boundaries. The next open obligations are zero-singleton
third-HIGH forests with three through five binaries, then the singleton
separator cases in the at-most-five-input block reduction. This package
claims no total fraction of all networks, full LOW(3,4) exclusion, global
size-44 exclusion, or 44-comparator construction.
