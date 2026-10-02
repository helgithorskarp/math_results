# Five productive TAIL classes for the literal P prefix

Actual author: **six-covering-3**, role **researcher**, 2026-10-02.
Status: **author-checked computer-assisted lemma**, independently unreviewed.
Two different integer algorithms reconstruct every numerical record under
normal and optimized Python. Ordinary bridges remain unformalized; source
publication is not an independent mathematical verdict.

## Claim and exact domain

Let

    P=((8,0),(9,0),(10,1),(14,1),(12,10)).

Consider a finite covering of all integers by congruences with pairwise
distinct original moduli, each at least8 and dividing10080, which contains
these five literal classes. Define BASE as the unused divisors of2520 at
least8, and TAIL as

    {16d,32d : d divides315}.

These inventories, together with the five P labels, partition all65
divisors of10080 at least8. All original phases and omissions are allowed;
in particular original16,32 and all other TAIL labels remain optional.
Let H be the residues modulo2520 left uncovered by P and the selected BASE
classes. A TAIL class is **productive** if it covers any physical10080 lift
of any x in H. Its parent is its phase modulo8.

**Lemma. Every such covering has at least five productive original TAIL
classes.**

This is a condition on the specified literal prefix and divisor inventory.
No normalization of every minimum-EXACTLY-eight covering to P is asserted.
It gives no new global numerical bound on L_min(8), no full-P exclusion,
and no covering witness. Minimum exactly8 and minimum at least8 remain
separate parameters.

## 1. The two-parent input

The published author result [9762](https://raw.githubusercontent.com/helgithorskarp/math_results/main/round-two/six-covering-3/multi-parent-tail-obstruction/proof.md)
states that every partial or completed P/BASE inventory has holes in at
least two distinct parents modulo8. Its verified source commit is
b66fc56a11fe07e61f8b9342ef6a637afc104848; the committed LEMMA9762/0 reference is

    bafkreid2hvngnmkjaru7uc2mi5ousqyts6zkuel2zvwhhlsrvw25wsuvpm.

This is the sole external mathematical premise of the lemma.
The new 127-hole calculation below does not depend on the private
7006-record mixed-support proof, digit-tree phase normalization, or any
other agent's numerical case. A prior independent review of a different
lemma is not a verdict on this new result.

## 2. Four original TAIL classes can repair at most126 BASE holes

Every x modulo2520 has four physical lifts

    x, x+2520, x+5040, x+7560 modulo10080.

For d dividing315, gcd(16d,2520)=8d. A16d class meets either zero or two
of these four lifts. Its BASE projection is one congruence modulo8d.
For a32d class the corresponding gcd is also8d, but the lift step has
order4 modulo32d: it meets either zero or one lift. Every TAIL class
belongs to one parent modulo8, so different parents cannot share its
original label/phase.

Consequently each nonempty parent needs at least two productive TAIL
classes. If exactly four classes are productive, section1 forces exactly
two occupied parents, with exactly two classes assigned to each. Both
classes in either parent must be of type16d; including a32d would repair
at most three of the four lifts of a hole.

For the two classes16d1:a1 and16d2:a2 in one parent, every hole must lie
in both projected classes modulo8d1 and8d2. Distinct original moduli mean
d1!=d2. The intersection is empty or a congruence modulo8*lcm(d1,d2),
containing exactly315/lcm(d1,d2) residues modulo2520. The two phases
must additionally differ by8 modulo16 to hit opposite lift halves. The
intersection-size bound is valid even if that extra condition fails.

Thus the total number of holes that four productive originals can repair
is at most

    315/lcm(d1,d2) + 315/lcm(d3,d4),                 (1)

where all four d's are distinct divisors of315. Single-use original labels
couple the two parents: the same d cannot be used once in each parent.

There is a short ordinary bound for(1). If either pair has lcm3, its
labels are1 and3. The other pair avoids both; its lcm is at least15, giving
at most105+21=126. Indeed the divisors of315 below15 are1,3,5,7,9,
and none contains two distinct allowed divisors after1 and3 are removed.
If neither pair has lcm3, each lcm is at least5, giving at most63+63=126.
Therefore **four productive classes repair at most126 BASE holes**.

As a numerical cross-check only, the producer lists all66 unordered
two-label pairs and the ordered disjoint edge matchings. The separate
checker lists all495 four-label subsets, their three perfect pairings,
and both parent orders. These2970 cases have maximum capacity sum126.
This abstract capacity maximum does not assert that an actual completed
BASE inventory attains126 holes or that a full four-class repair exists.

## 3. Every literal P/BASE inventory leaves at least127 holes

The36 original BASE labels are

    15 18 20 21 24 28 30 35 36 40 42 45 56 60 63 70 72 84
    90 105 120 126 140 168 180 210 252 280 315 360 420 504 630 840 1260 2520.

Original21 is included. There are9279 raw BASE phase actions. Let R be
all residues modulo2520 uncovered by P: |R|=1398. For any fixed original
phase tuple F, let U be the union of its hits inside R. With N the
remaining original BASE labels, define

    K(F)=|U| + sum_{n in N} max_{0<=a<n} |(R minus U) intersect(a mod n)|. (2)

For every extension of F, (2) upper-bounds the number of points of R
covered by the entire BASE inventory: each remaining original selects at
most one phase, and the sum may overcount overlaps. To leave at most126
holes, the BASE inventory would need to cover at least1398-126=1272
points of R. We discard only tuples with K<1272, and keep that **same
cutoff at every stage**.

First enumerate all270 raw15/18 phase pairs, without symmetry reduction.
Extend every retained actual tuple over all24 raw phases of original24,
and then all36 phases of original36:

| Fixed originals | Complete records | K range | Retained tuples |
| --- | ---: | --- | ---: |
| 15,18 | 270 | 1119..1290 | 16 |
| 15,18,24 | 384=16*24 | 1170..1280 | 8 |
| 15,18,24,36 | 288=8*36 | 1210..1269 | 0 |

Every initial raw pair is either discarded by a valid upper bound or
appears in the next complete stage. The same is true of every extension.
The final complete frontier is empty, so no completed BASE phase
assignment covers1272 points of R. Hence every completed assignment
leaves at least127 holes. Any omitted BASE original can be completed by
an arbitrary phase without destroying coverage; the partial inventory
has at least as many holes as its completion. This proves the same bound
for all allowed omissions.

No16/32 presence hypothesis, coloring, row model, or prescribed TAIL
allocation enters this calculation. All original18 phases, including3
and12 separately, remain in the raw root domain. Each stage carries all
remaining original marginals, including large moduli; none is dropped
because of a projected modulus collision.

Combining at least127 actual BASE holes with section2 contradicts an
allocation of only four productive originals. Three or fewer already
contradict the two-parent input. This proves the lemma.

## 4. Exact replay, rejection controls and trust boundary

The producer groups the1398 required points into compact bit positions,
builds their phase masks by residues, and enumerates tuples in forward
phase order. The independent checker imports no producer/research
module: it constructs the BASE labels from prime powers, literal physical
2520-point AP masks, divmod-indexed raw tuples, and reverse phase loops.
It compares every word of all942 complete records and every actual
retained tuple before extending it. Each record has38 little-endian
unsigned16-bit words: fixed phases, union size, one marginal for each
remaining original in increasing label order, and the final upper bound.
All integer sizes are checked by encoding/reconstruction; no floating
point arithmetic or native solver is used.

The row-stream SHA256 values are

    root: 73b75edfcff0a70b93879088232935a96021a594897ca850cd5dbbc15f268ca0
    +24:  f2baae7ad760716dbf79e7afefb63e198003487a689428be45a9b52c1a605278
    +36:  c5eb2f028ecf5fc6ed34b5805e157731a55e8a9f75be2447a86b032b22ea52d8

One complete audit evaluates31068 original marginals and8683236 literal
phase intersections. The three numerical kernels were frozen from the first normal/-O audit,
which completed in under3 seconds per audit with complete fields equal
and no cap increase. Producer status fields are advisory; the separate
full checker and ordinary proof establish the author-checked conclusion.

From any working directory, reproduce the coherent frozen artifact with
Python3.11.2/standard library:

    python3 -B /absolute/path/five-productive-tail/reproduce.py \
        --scratch /absolute/own-workspace/scratch/uniform-five-replay

The driver runs10 serial children: both producers, the full checker, and
two groups of semantic controls, normally and with-O. It compares the
complete mathematical fields with [certificate.json](certificate.json),
and the complete control fields between modes. Controls must reject a
changed early cutoff, omitted preceding tuple, duplicated retained tuple,
changed first raw phase, changed last raw upper bound, and a truncated
final stream, each for its intended mathematical reason. Assertions are
not used for proof checks, so optimization cannot disable validation.

All children have a20-second timeout, thread counts1, and at most one CPU
child runs at a time. The producer's retained-frontier300 cap is unchanged.
A timeout, cap failure, malformed record, mismatched full fields or
incomplete enumeration establishes no exclusion. Raw streams, damaged
fixtures, timing receipts and verbose outputs stay in workspace scratch.
The compact frozen certificate and source suffice to regenerate them.

Ordinary completion, union, CRT/lift, two-parent and original-resource
bridges remain unformalized. A different algorithm by the same author is
not independent peer review. The two-class resource argument in section2
is proved directly here and has no sampled-phase or private-data premise.

Primary family context is Zhang--Zhang,
[arXiv2607.19029](https://arxiv.org/html/2607.19029), refreshed live2026-10-02:
its minimum-seven10080 result and divisor-completion/filtering context
motivate this frontier. No minimum-eight endpoint is imported. Historical
priority of the generic counting observation is not claimed.
