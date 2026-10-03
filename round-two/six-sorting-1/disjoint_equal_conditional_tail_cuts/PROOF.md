Actual author and executing agent: **six-sorting-1, researcher**, 2026-10-03.
Scoped author proof checked by separate packed and scalar algorithms.
Independent-person review and formalization are pending.

**Result.** For each of the six literal routes below, every finite standard
preparation has three fixed forbidden head/tail choices and a fourth forbidden
choice obtained by evaluating that preparation once. The preparation length,
repeated gates and suffix depth are unrestricted. This generalizes the single
adaptive head rule in [9916](https://github.com/helgithorskarp/math_results/blob/main/round-two/six-sorting-1/conditional_maximum_tail_obstruction/PROOF.md)
to all zero heads and five additional literal routes. All five additional
routes were outside the two complete disjoint-route exclusions already published:
[(5,6)/(7,9),9805](https://github.com/helgithorskarp/math_results/blob/main/round-two/six-sorting-1/disjoint_two_prior_56_79_barrier/PROOF.md)
and [(5,6)/(7,10),10024](https://github.com/helgithorskarp/math_results/blob/main/round-two/six-sorting-1/disjoint_two_prior_56_710_barrier/PROOF.md).
The elementary monotonicity and leading-zero facts are known properties, not
new generic theorems; the new result is this uniform literal application.

Use ports 0..12 and standard comparators `(a,b)`, a<b, writing min to a.
Let

```
B23=(0,11),(1,7),(2,4),(3,5),(8,9),(10,12),
    (0,2),(3,6),(4,12),(5,7),(8,10),
    (0,8),(1,3),(2,5),(4,9),(6,11),(7,12),
    (0,1),(2,10),(4,8),(3,6),(9,11),(11,12).
L4=(3,4),(1,2),(1,3).
P26=B23;L4.
```

For each row, P28 is P26 followed by its two disjoint HIGH merges. The roots
a<b are their maximum endpoints, r is the unused member of {5,6,7,9,10},
and M is the increasing tuple of remaining physical ports in {2,...,11}.
Tuples u list Boolean coordinates in the displayed M order.

| Prior HIGH merges | (a,b) | r | M | Original HIGH inputs | u |
|---|---|---|---|---|---|
| (5,6);(7,10) | (6,10) | 9 | (2,3,4,5,7,8) | (1,2) | (0,0,0,1,1,0) |
| (5,6);(9,10) | (6,10) | 7 | (2,3,4,5,8,9) | (0,6) | (0,0,0,1,0,1) |
| (5,7);(6,10) | (7,10) | 9 | (2,3,4,5,6,8) | (1,2) | (0,0,0,1,1,0) |
| (5,9);(6,10) | (9,10) | 7 | (2,3,4,5,6,8) | (0,6) | (0,0,0,1,1,0) |
| (5,10);(6,7) | (7,10) | 9 | (2,3,4,5,6,8) | (1,2) | (0,0,0,1,1,0) |
| (5,10);(6,9) | (9,10) | 7 | (2,3,4,5,6,8) | (0,6) | (0,0,0,1,1,0) |

Let F be any finite standard comparator word supported on M. Put v=F(u).
For every physical p in M with v[p]=0, set r'=max(r,p) and define

```
H_p=(min(r,p),max(r,p)).
T_p=(a,b);(r',11);(b,11).
```

**Lemma.** No thirteen-input sorting network with at most 44 comparators has
the literal prefix `P28;F;H_p;T_p`. In particular this holds, for every F,
for p=2,3,4, and for the unique zero coordinate among the final three
coordinates of v. Thus each preparation has at least four forbidden head/tail
choices for the specified balanced tail. The same result holds when the two
prior disjoint HIGH gates are interchanged, or the first two disjoint gates of
T_p are interchanged.

Other balanced tails, nonzero head choices, the nine other disjoint patterns,
connected or longer event histories, other prefixes and unrestricted 44-sorters
are outside this lemma. The current [primary table](https://bertdobbelaere.github.io/sorting_networks.html)
still gives the thirteen-input minimum-size bounds 44..45. This lemma is not
an exclusion of every preparation/head/tail in any newly covered route.

For each row fix the two specified **original** HIGH inputs to distinct values
2 and 3, in increasing original-port order. Let the other eleven original
inputs range independently over their full Boolean cube. The packed producer
and separate numerical checker reconstruct all 2048 assignments for each row,
without replacing the original domain by a current tag representative. They
agree on all full seed rows and on every deletion, rank and conditional field.
At P28 each of the six witnesses has:

* D=7 marked-touch deletions and R=0 unmarked whole-original identities;
* rank 3 at port 12 and rank 2 at one of a,b;
* unmarked Boolean values at r and 11, with `P28[r] <= P28[11]` on the entire cube;
* on the region `P28[11]=0`, an attained coordinatewise greatest M input u,
  of weight two with its first three coordinates zero.

For the first, third and fifth rows the conditional region has twelve original
assignments; for the others it has eight. Their complete conditional input
patterns, encoded with M coordinate j using bit j, are respectively

```
[0,8,16,24], [0,8,32,40], [0,8,24],
[0,8,16,24], [0,8,16,24], [0,16,24].
```

These are exhaustive defining computations of a fixed original domain. Their
exact rows and independently reconstructed hashes are in the compact certificate.
They are not a search over F and require no preparation catalogue.

Every comparator is coordinatewise monotone and preserves Boolean weight.
Therefore every finite word F has those properties by induction. It follows
that v has weight two. Standard comparators also preserve an initial segment
of zero coordinates: if the smaller endpoint is in that segment its minimum
stays zero; if the larger endpoint is in it, both endpoints are in the zero
segment. Induction gives v[2]=v[3]=v[4]=0. Its other three coordinates contain
exactly two ones and one zero. The four zero heads exist independently of the
length of F. The three masks 24,40,48 are a conservative output envelope;
the proof does not assert that every one is reachable for every u.

Write s=P28[11] and t=P28[r] for a particular original assignment. F avoids
both marked ports and r/11. For any selected zero p, monotonicity gives
`F(x)[p] <= F(u)[p]=0` whenever s=0, since the conditional dead input x<=u.
Then t=0 as well. After H_p, the value at its **actual** maximum endpoint r'
is z=max(F(x)[p],t). If s=0, z=0; if s=1, z<=1=s. Consequently z<=s on
the entire same original cube. The new root really is r', including p>r;
port r is not used as a substitute when the head moves the root.

The first tail gate (a,b) touches original rank 2 once and moves it to b.
It is disjoint from r'/11, so it does not change z or s. The next gate
(r',11) is unmarked and an identity on the **entire original cube**. Finally
(b,11) is another marked passage, moving rank 2 to 11. Rank 3 remains at 12.
F and H_p have no marked passages. Any whole-original identities in F or H_p
only strengthen the bound. The displayed prefix has D=9 and R>=1.

The imported [original-domain pruning theorem8539](https://github.com/helgithorskarp/math_results/blob/main/round-two/six-sorting-2/semantic-pruning/PROOF.md)
states that a sorting completion of total size m obeys

```
m >= D_original + R_original + S(11).
```

Marked passage deletion yields an eleven-wire generalized comparator network.
Unmarked gates that are identities on the full original free Boolean cube are
identities for arbitrary ordered free inputs by thresholding. They can be
removed jointly. The free-carrier permutations and generalized orientations
can be standardized without increasing comparator count. These are the
credited pruning bridges, rather than assumptions about a selected depth.
Using [Harder's arbitrary-depth S(11)>=35](https://arxiv.org/abs/2012.04400)
gives m>=9+1+35=45 and proves the lemma.

The claimed commuting variants follow from equality of the complete comparator
functions and unchanged total size. Both prior gates have disjoint endpoints,
as do (a,b) and (r',11). The canonical sorted word therefore has a sorting
completion whenever a commuting variant does. No original D/R history from
one word is silently assigned to a different word.

`verify.py` imports neither the packed producer nor a campaign numerical helper.
It reconstructs the six full original cubes, all three conservative output
patterns and every actual head/root/tail binding. It also replays 144 actual
literal extensions on 294912 original assignments, including eight cases where
the head moves its root, and both commuting tail orders. These illustrations
exercise the mechanism; the written induction, not their bounded lengths,
establishes the claim for every F. Local corroborating checks comprise 960
conservation cases, 10935 comparable-input monotonicity cases and 120 cases
preserving the leading zero segment. Normal and optimized runs compare entire
mathematical records and full illustrative records.

Eight semantic corruptions, with their complete transport hashes repaired,
are rejected both normally and with `-O`: false original cost, omitted actual
conditional input, false maximum, a nonzero coordinate called a zero head,
erasure of an actual head move, a marked tail gate called the identity, a false
fixed zero port and a whole-route overclaim. The genuine proposal is unchanged.

The first control harness accidentally selected a nonexistent zero-head entry
for the root-move damage. This was corrected to the actual zero head at the
weight-two output40; the packed and scalar mathematics were unchanged. A fresh
source-only cold run of the final code checks all phases and controls before
publication. No failed control run was used as a negative mathematical premise.

Runtime inputs are only the compact fixture and owned source in this directory.
No old negative corpus, graph, signing key, solver or private generated arrays
are needed. The ordinary pruning bridges, the written finite-word induction
and the primary S(11) bound are external or unformalized proof boundaries.
Harder's larger lower-bound corpus is imported as prior literature and is not
rerun here. Separate algorithms by the same author do not constitute independent
review. The global thirteen-input size question remains open.
