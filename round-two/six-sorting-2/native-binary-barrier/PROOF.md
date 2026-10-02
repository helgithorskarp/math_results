# Native H21 requires a singleton first increase on at least one side

Actual author and executing agent: **six-sorting-2, researcher**, 2026-10-02.
This is a restricted author proof, with exact finite certificates and
separate same-author algorithms. The universal bridges are unformalized;
no external-person review, formalization or unrestricted size45 lower bound
is claimed.

Ports are `0..12`. A standard comparator `(a,b)`, `a<b`, writes min to `a`.
Use the literal prefixes

```
N19 = (0,11),(1,7),(2,4),(3,5),(8,9),(10,12),
      (0,2),(3,6),(4,12),(5,7),(8,10),
      (0,8),(1,3),(2,5),(4,9),(6,11),(7,12),(0,1),(2,10).
H21 = N19;(9,11);(11,12).
```

For every original pair of LOW inputs, clamp them to distinct ranks below
all eleven free middle inputs. Follow the unordered marked pair and count
every gate touching a mark once, obtaining `D`. At a prefix group the
original histories by their current marked pair, take the maximum `D`
in each class, and sum `2^D` over the classes. This is the ordinary LOW
mass. HIGH is the dual two-large-input construction. Each original free
cube is preserved; sharing current marked ports does not identify two
original conditional functions.

H21 holds the minimum at0 and maximum at12. Its complete ordinary classes
have the following secondary ports and costs:

| Family | `(port,D)` |
|---|---|
| LOW | `(1,7),(2,7),(3,5),(4,6),(6,5),(8,6)` |
| HIGH | `(3,5),(5,6),(6,5),(7,6),(9,6),(10,6),(11,7)` |

Both masses are448; there is no HIGH secondary at8. A **binary event** for
a family touches two of its current secondary candidates, a **singleton**
touches one, and a preparation touches none. That family's **first strict
increase** is its first suffix gate raising its mass above448.

**Theorem.** Every standard sorting completion of H21 of total size at
most44 has a singleton first strict increase in at least one of LOW/HIGH.
Equivalently, their first strict increases cannot both be binary.

The first strict increases exist on both sides. The theorem allows
arbitrary suffix order, repetition, interleaving, preparation length and
depth. It does not say that the globally first increase must be singleton.
It does not decide H21's244-state eleven-input,23-gate completion problem,
or the [unrestricted44..45 interval](https://bertdobbelaere.github.io/sorting_networks.html).

## Ordinary ceiling and the forced joint gate

The ordinary pruning transport theorem gives, at every prefix of a
total-size-`m<=44` sorter,

```
W_LOW, W_HIGH <= 2^(m-S(11)) <= 512.
```

We import `S(11)>=35`, and the pruning/standardization setting of
[Harder's primary paper](https://arxiv.org/abs/2012.04400), using the precise
transport interface in [lemma8539](../semantic-pruning/PROOF.md).
The lower-bound proof corpus is not replayed. A touch of held0 doubles
every LOW weight, and a touch of held12 doubles every HIGH weight. Either
gives at least896. Thus all suffix gates use physical ports1..11.

A singleton replaces weight `2^d` by `2^(d+1)`. A binary event with costs
`d,e` replaces their weights by `2^(1+max(d,e))`; LOW retains the smaller
port, HIGH the larger. Mass cannot decrease, and a binary event is zero
precisely when `d=e`. Binary events shrink the secondary support.

Assume, for contradiction, both first strict increases are binary. Before
the globally first strict increase, all events on either side are equal
binary merges or preparations. Until the joint gate

```
J = (3,6)
```

occurs, the only common secondary ports remain3/6, both at cost5 in both
families. Any zero gate other than J avoids both. For a positive gate to be
binary in both families, both endpoints would have to lie in that common
support; the only such gate is J, which is zero. A gate increasing both
families therefore has a singleton event in at least one of them and
contradicts the first-binary hypothesis.

Consequently the globally first increase affects exactly one side and is
binary there. If J has not occurred, this gate avoids3/6: a touch of just
one shared cost5 leaf also strictly increases the other family or violates
its ceiling. All its relevant costs are then at least6. Of the unequal
binary merges, only `6+7 -> 8` fits the slack64; it raises that side's mass
from448 to512. If J occurred earlier, all costs already are at least6 and
the same conclusion holds.

If J has not occurred at this saturation, the saturated side still has
the two cost5 leaves at3/6. Any later touch of one of them with an endpoint
other than the other cost5 leaf would strictly increase that saturated
mass. It is forbidden. These two leaves must eventually join the unique
terminal secondary class of a sorter, so J must eventually occur. Every
preceding suffix gate avoids its endpoints. It therefore commutes left
across all of them, without altering the full network function or number
of gates. J can be placed immediately after H21, even when it originally
occurred after one or both first strict increases.

This is an exact disjoint-gate argument, not an enumeration of preparation
functions. As a finite independent control, the standalone checker follows
all admissible necessary profile transitions under the first-binary
predicate:3150 states,15044 nonidentity edges,173250 next-gate controls,
and one terminal profile. It verifies that every pre-J admissible gate
other than J avoids3/6, and that the globally first mass pairs are exactly
`(448,512)` and `(512,448)`. Identity preparations are unrestricted self
loops; the finite projection is not a preparation-function quotient.

## All remaining secondary events are binary

After J the profiles are disjoint:

```
LOW  : 1/2 at cost7; 3/4/8 at cost6.
HIGH : 11 at cost7; 5/6/7/9/10 at cost6.
```

Each mass is still448. In a sorter each side finishes in one secondary
class, so its final mass is a power of two. Nondecrease and the512 ceiling
force a strict increase and final mass512.

Before a side's first strict increase, a singleton would itself be strict
and violate the hypothesis. The allowed first binary increase is exactly
the unequal6/7 merge, reaching512. After that, only equal binary events or
preparations are allowed. Hence *every* secondary event on both sides is
binary. Their supports only shrink; a released port never reappears. An
event on one side must avoid the other's support, because a cross-support
gate would be singleton on each affected side.

A preparation preceding a future binary event avoids that event's two
endpoints: both are still live at the preparation, since supports only
shrink. Thus the preparation commutes with every later binary event.
Move all preparations after all secondary events, preserving their mutual
order. LOW and HIGH events also commute with each other, since their
original supports after J are disjoint. Keep their internal dependency
order. This places exactly four LOW events and five HIGH events at the
front after J, with the entire network function and gate count unchanged.
No preparation-length or depth bound is imposed.

## Complete native binary genealogies

Use weight units64. Each family starts with total7 and ends at8. Exactly
one unequal event `1+2 -> 4` raises the total by1; all other events are
equal merges. The weight8 root has two weight4 children, exactly one of
which contains this unequal node.

LOW starts with three unit leaves3/4/8 and two weight2 leaves1/2.
If the unequal node uses an original weight2 leaf, choose its unit sibling
in3 ways and that original leaf in2 ways. The other two units pair and
merge with the unused original2, giving6 trees. If the weight2 child is
formed from two units, choose its remaining unit sibling in3 ways, while
the two original2 leaves form the other root child. This gives3 more,
for **9 LOW trees**, each using four gates.

HIGH starts with five unit leaves5/6/7/9/10 and original weight2 leaf11.
An original2 child gives5 unit-sibling choices times3 pairings of the
other four units:15 trees. A paired-unit2 child gives5 sibling choices
times6 choices of its unit pair:30 trees. Thus there are **45 HIGH trees**,
each using five gates. This45-tree classification credits the earlier
[six-sorting-1 lemma9420](../../six-sorting-1/both_first_binary_barrier/PROOF.md).

The producer uses these explicit partitions. The checker independently
enumerates all bottom-up forests and all cost-allowed pairs under512,
including unequal pairs. It finds328 states,1123 local pair controls and
54 terminal genealogies in total. It reconstructs every complete Boolean
function on the five/six initial candidate inputs and compares the entire
9/45 sets, entry by entry. Equality of min/max Boolean functions lifts to
all totally ordered inputs by thresholding. Disjoint child subtrees
commute; any dependency-respecting gate order of a genealogy is equivalent
to its canonical child-before-parent word.

The complete product gives **405 literal fronts**

```
H21;J;LOW_tree;HIGH_tree
```

of length31. All hold ranks0/1/11/12 and leave physical2..10 as a
nine-input core with at most13 remaining gates at total44. Full replay of
all8192 original H21 inputs and its entire246-element output image checks
the ranks and target images. Their sizes range75..102. There are403
distinct core images; the405 literal fronts are certified separately,
with no quotient of their original conditional domains.

The earlier changed B23 equals `H21;J;(4,8)` by disjoint commutations.
Its three LOW binary functions, `(4,8);L1/L2/L4`, equal native LOW
genealogies0/3/8; HIGH has the same45 functions. Therefore135 of these405
product functions belong to the earlier B23 cover. The new theorem
generalizes that B23 both-first-binary restriction to its native ancestor
H21. Every native front is checked afresh here; no old negative certificate
or review verdict is imported. This result also differs from our
[first-(512,512) H21 exclusion9469](../first-joint-saturation/PROOF.md), whose
405 fronts have length32 and12 remaining gates.

## Original-domain certificates exclude all405 fronts

For each selected original clamping `f` of three LOW and three HIGH inputs,
retain its full seven-free-input cube. Count marked-touch deletions `D_f`
and free gates that are identities on *that entire original cube* as
`R_f`. The two deleted sets are disjoint; write `C_f=D_f+R_f`. Track the
free carriers through marked exchanges to obtain an oriented seven-input
prefix `Q_f`. Global carrier permutations and oriented pairs are retained.

Use the generic original-domain nested operator of
[lemma9007](../native24-kernel-cover/NESTED.md):

```
B_7(Q_f) = max(16, LOW semantic anchor, HIGH semantic anchor)
lambda_f = C_f + B_7(Q_f)
lambda_z = max_(selected f with current LOW/HIGH tag pair z) lambda_f
M = sum_z 2^lambda_z <= 2^m       for every sorting extension of size m.
```

The semantic anchor theorem is [lemma8604](../semantic-pruning/ANCHORS.md).
It imports `S(5)>=9,S(6)>=12,S(7)>=16`. Constant16 is a valid smaller
inner bound; no unnecessary inner data are a certificate premise.

The97 original proposal domains comprise81 credited published native20
proposals and16 additional domains selected from complete3+3 scans of two
unclosed branches. This pool only proposes candidates. Every selected
domain is recomputed independently; neither the proposal pool nor a
failed candidate bound is an exhaustive mathematical premise.

The certificate selects5020 original-domain occurrences, always in
distinct current classes within a front. Of these,4648 use constant16
and372 use nested bounds; the latter contain278 distinct oriented inner
words. On every front the selected mass strictly exceeds

```
2^44 = 17592186044416.
```

The minimum is

```
17660905521152 = 257*2^36 = (257/256)*2^44.
```

Thus each of the405 fronts needs at least45 total comparators. The exact
commutations and complete product cover contradict the assumption that
both first strict increases are binary, proving the theorem.

## Reproduction and trust boundary

[README.md](README.md) gives commands; [SOURCE-CREDITS.md](SOURCE-CREDITS.md)
pins reused primitives and mathematical dependencies. The compact
[certificate](certificate.json) stores original-domain selectors and
derived fingerprints, rather than bulky outer/inner truth tables. The
standalone checker recomputes complete original cubes, each used identity,
pruned carrier functions, exact inner bounds and strict masses. Hashes are
provenance checks, not replacements for recomputing the inequalities.

The producer's packed truth tables, explicit pair partitions and dyadic
aggregation differ from the checker's numeric distinct ranks, bottom-up
forests and heap `1+max` aggregation. This is same-author algorithmic
checking, not independent-person review. Universal pruning/commutation
bridges, imported optimal-size inputs and the threshold argument remain
unformalized. No timeout, partial search, UNKNOWN or heuristic failure is
a proof premise. Normal and optimized Python checks retain every condition;
validation fields and damaged controls are recorded in [checks.json](checks.json).

The remaining native H21 completion problem and unrestricted44..45 gap
remain open. First singleton events may use prepared operands; their
preparation functions are outside this reduction. This packet does not
transfer a four-port preparation closure to a five-, six- or seven-port
problem.
