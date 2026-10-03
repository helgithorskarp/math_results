# A live-head reduction for zero-singleton preparations after LOW(3,4)

Actual author and executing agent: **six-sorting-2, researcher**, 2026-10-03.
Author checked by separate packed and scalar algorithms and cold reproduction;
independent-person review and formalization remain pending.

**Claim.** Use the literal 28-comparator prefix Q in `fixture.json` and the
same ordinary LOW/HIGH route as [the complete two-binary exclusion](../high3-low34-two-binary-exclusion/PROOF.md),
actual LEMMA9982/0. Consider a putative thirteen-input sorting network of
size at most44 extending Q. Its first strict ordinary two-LOW mass increase
after Q is a singleton, with no additional preceding two-LOW binary.
Let F be all the intervening preparation before that singleton. If F has
zero third-HIGH singleton events and at least two third-HIGH binary events,
the singleton's DEAD partner cannot be a surviving third-HIGH live port.
Thus any still possible partner must be a port freed by those binaries.

The claim covers every finite preparation word, arbitrary repeats and
arbitrary allowable suffix depth. It does not exclude freed-port heads,
third-HIGH singleton separators, other prior-LOW routes, or all44-sorters.
At two binaries the stronger published lemma already excludes every head.
Here the new conclusion also covers three, four and five binary events.

## Literal route and imported principles

Comparators `(a,b)`, a<b, put the minimum at a and maximum at b; ports are
0 through12. The literal Q is

```
(0,11),(1,7),(2,4),(3,5),(8,9),(10,12),
(0,2),(3,6),(4,12),(5,7),(8,10),
(0,8),(1,3),(2,5),(4,9),(6,11),(7,12),(0,1),(2,10),
(9,11),(11,12),(3,6),
(6,7),(5,7),(9,10),(10,11),(7,11),(3,4).
```

Its compact-JSON SHA256 is
`89c4715b824b7cf4cee8a5698a612f336abdf20497ed48c5132dca514486afd4`.
Every event here is counted **after Q**. Freed port4 is the true maximum
of the last gate's old values, not a substituted constant.

The credited [ordinary original-domain pruning theorem](../semantic-pruning/PROOF.md)
associates charge D to each original extreme-mark domain. D counts every
gate touching a marked value once, including stationary marked gates.
For fixed original mark counts, take maximum D within each actual current
tag class. The sum of2^D over distinct classes is at most2^(m-S(k)) for an
m-comparator sorting network, where k is the number of unmarked inputs.
It cannot decrease under a further comparator. We also use exact original
identity deletions R: `D+R+S(k)<=m`. R counts gates that are identities on
the entire original free Boolean cube while neither endpoint is marked.
No one original's charge is assigned to a different original domain.

The imported arbitrary-depth lower bounds are S(10)>=29 and S(11)>=35;
S(12)>=39 is retained for the published route context. These are primary
literature results, not newly reproduced lower-bound proof corpora.
See [source credits](SOURCE-CREDITS.md).

Fresh original-domain replay at Q gives ordinary two-LOW secondary roots
1,2,3,8 with exponents7,7,7,6 and mass448, common held LOW at0. With no
additional LOW binary, the only allowed strict singleton selects root8.
It compares8 with a partner q in DEAD={4,5,6,7,9,10}. The subsequent
equal-cost LOW merges collect the second minimum at1; they act only on
`{1,2,3,min(8,q)}`. There are six legal orders and three complete Boolean
tail functions. These scope facts and their arbitrary-word reduction are
proved in the cited two-binary source; no additional prefix is assumed.

For three HIGH marks the common held ports are11/12. At Q the secondary
ordinary exponents are

| Port | 4 | 5 | 6 | 7 | 9 | 10 |
|---|---|---|---|---|---|---|
| Exponent | 11 | 11 | 11 | 13 | 11 | 12 |

The initial mass is20480 and the ceiling is2^(44-29)=32768. A third-HIGH
binary merges two live roots a<b into b, with exponent `1+max(e_a,e_b)`.
It frees a and reduces support by one. A zero-singleton F therefore has
at most five binary events.

## Normalize F and separate the selected component

The [continuously-live endpoint argument](../one-sided-forest-frontier/PROOF.md)
moves every binary left over earlier preparations: an endpoint of a later
binary has remained live, so cannot be touched by an earlier preparation.
The crossed gates are literally disjoint. Thus F has an equal, same-length
normal form `B1;...;Bj;G`, where2<=j<=5 and G is any finite word on the
physical ports freed by all j binaries. G is not bounded in length or depth.

The binaries form a labelled merge forest. A component's leaves are its
initial physical labels and its root is their largest label. Different
components have disjoint leaves; every binary endpoint of a component
belongs to those leaves. Let q be a final live root, and let r be the number
of events in its component. Then that component has r+1 leaves.

If r<=2, move its r events to the beginning of the binary word, keeping
their relative order and keeping the other events' relative order.
Every crossed pair is disjoint. Take these r events and the first2-r
outside events as a two-binary prefix. All remaining binaries are outside
q's component. The head H=(8,q), and every gate of any balanced LOW tail T,
are disjoint from those remaining events and from every gate of G.
Move H and T left across them, preserving H/T order. The entire sorter is
now exactly equal, at the same length, to

```
Q; two legal third-HIGH binaries; H; T; arbitrary suffix.
```

This sorter is excluded by LEMMA9982. The implication concerns equal
complete sorting functions and total size, not equal original D/R histories.
No quotient, unordered output image or hypothetical conditional profile
is used in this reduction.

## Larger components and the balanced exception

For a merge the new weight2^(1+max(e_a,e_b)) is at least2^e_a+2^e_b,
with equality exactly when e_a=e_b. Every leaf weight is at least2048.
If r>=4, there are at least five leaves and the final root weight, being
a power of two, is at least16384: e_q>=14. The total mass M before H is
at least20480. G avoids every live third-HIGH mark and leaves ordinary D
unchanged. H touches precisely q's secondary class, increases its D by
one and leaves all classes distinct, even when q<8 moves its mark to8.
The new mass is M+2^e_q>=36864>32768, a contradiction.

For r=3 there are four leaves and e_q>=13. An exponent at least14 is
excluded by the same argument. If e_q=13, the leaf weights must sum to
8192 and no merge may increase weight. Consequently all four leaves have
exponent11 and every merge is equal-cost. They are exactly {4,5,6,9},
with two disjoint11+11 merges followed by their12+12 merge. The final
root is q=9. Other components, outside events and G never touch8 or9.

Fix the **original** HIGH inputs0 and1 to distinct extreme values2 and3,
and let the other eleven original inputs range over their full0/1 cube.
At Q the actual record is

```
[original_LOW=0, original_HIGH=3, current_LOW=0, current_HIGH=6144,
 D=9, R=0, original_identity_positions=0].
```

Every one of its2048 assignments satisfies

```
Q_output[8] <= max(Q_output[4],Q_output[5],Q_output[6],Q_output[9]).
```

The balanced component puts exactly this maximum at9. Outside binary
events and any G leave8 and9 untouched. Thus H=(8,9) is an identity on
the **entire same original cube**, with unmarked endpoints. D remains9
through F and H, while H contributes at least one R. Therefore
`m>=9+1+S(11)>=45`, contradicting the size budget.

This identity is conditional on the specified original domain. It fails
on ten unclamped thirteen-bit inputs, the first being2069; the source
checks this boundary and does not assert a global identity. The ordinary
mass equality case at j=4, M24576 and head mass32768, is handled by this
identity argument, not by replacing strict inequality with equality.

All final live roots are covered, proving the claim.

## Reproducibility and trust boundary

Run `python3 run.py` using Python3.11.2 and the standard library. The packed
producer and separate scalar checker reconstruct the complete ground
families and all6450 labelled binary histories without pruning generation.
They agree on the **entire mathematical record**, including every stage,
component, live-head proof binding and all2048 relation rows. The scalar
checker independently routes every actual original triple through each
forest, replays every disjoint swap, and checks all64 ordered local inputs
for each component commutation. It separately replays all six labelled
balanced trees as numerical original-domain gates. A known45-sorter is
checked on all8192 Boolean inputs; it is a positive control only.

`certificate.json` is compact; all bulky forest/row records are regenerated
under ignored `generated/`. The source-only cold copy starts with eight
runtime/input files and no produced records, old negative corpus or private
input. Normal and `-O` runs compare full mathematical records; all checks
use explicit exceptions rather than assertions. Sixteen damage checks pass
per mode. Each child is serial, native threads1, with a55-second guard.
Timeout, kill or incomplete execution is an operational failure, never
mathematical nonexistence.

The arbitrary-word normalization, ordinary mass theorem, threshold/zero-one
bridges and component argument are written proofs and remain unformalized.
The published two-binary exclusion and primary small-network lower bounds
are imported logical premises; their old large proof corpora are not rerun
by this package. Same-author algorithmic separation is not independent-person
review. The thirteen-input44-versus45 problem remains open.
