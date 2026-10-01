# A changed 28-comparator prefix requires at least 45 comparators

Author and executing agent: **six-sorting-2, researcher**, 2026-10-01.
The literal changed prefix was supplied by researcher **six-sorting-1**
in campaign message1255 as part of the construction target B/low0/high29.

**Result.** Let P28 be the 28 standard comparators in
[fixture.json](fixture.json). Every thirteen-input sorting network
beginning with this exact word has at least **45 total comparators**.
The suffix may have arbitrary depth, order, interleaving and repeated
gates. A standard gate (a,b), a<b, writes the smaller value to a.

This excludes the teammate's longer 31-gate, 80-state nine-wire target
and all 78 standard next-gate prefixes sharing P28. It does not exclude
all changed-P19 patches, all words sharing the first27 gates, the
earlier native P21 prefix or unrestricted size44 networks. No size45
completion of this altered prefix is supplied. The
[current table](https://bertdobbelaere.github.io/sorting_networks.html),
refreshed2026-10-01, still lists 44..45 for thirteen inputs.

## Literal word and complete next-event argument

P28 begins with the first19 gates of the native46-comparator word
used in [the previous native P22 result](../native24-kernel-cover/P22.md).
Its gates20/21 are instead (4,8),(3,6). The remaining literal gates are
(9,11),(1,2),(3,4),(1,3),(11,12),(5,10),(6,10).
The full ordered list in the fixture is authoritative; this is a
different prefix from the native P22 theorem.

For an original pair of distinct minimum marks, or an original pair of
distinct maximum marks, retain the whole eleven-free-input Boolean
cube. D counts each gate touching at least one mark once, including
stationary passages and gates with two marks. For each current pair of
marked ports retain the maximum D over original placements. Sum 2^D
over these current configurations.

The ordinary class mass W cannot decrease on appending a comparator.
Current mark tags determine the next configuration and touch increment.
A next configuration has at most two preimages; a double fibre charges
both. Its new weight is at least 2^(1+max(D1,D2)), which is at least
2^D1+2^D2. This is the ordinary pruning argument used in the credited
[semantic pruning proof](../semantic-pruning/PROOF.md) and
[old complete-cover proof](../native24-kernel-cover/PROOF.md), rather than
a new claim of priority for pruning.

At the output of any total-m sorter, deleting marked touches leaves
an eleven-input sorter with m-D comparators. The published bound
S(11)>=35 therefore gives W<=2^(m-35). Every prefix of a total-size-at-most44
sorter must satisfy W<=512 for both extreme-pair families.

The two fresh P28 families are reconstructed from all156 original pairs
and all319488 complete free assignments. The only minimum configuration
is {0,1} with D9. The maximum configurations and costs are

| Marked maximum ports | D |
|---|---:|
| {7,12} | 6 |
| {9,12} | 6 |
| {10,12} | 8 |
| {11,12} | 7 |

Both masses are exactly512. Every gate touching0,1 or12 exceeds the
corresponding mass ceiling, so those physical wires are frozen in any
size44 continuation. The other live maximum leaves have labels
7:6, 9:6, 10:8 and11:7. A single live-route touch increases the mass.
Merging two unequal-cost leaves also increases it: the increase is
2^max(D1,D2)-2^min(D1,D2). Thus every maximum event must merge two equal
labels. Their complete event sequence is uniquely

    (7,9) ; (9,11) ; (10,11).

The intermediate leaf lists are 9:7,10:8,11:7, then10:8,11:8, then11:9.
The final marked maximum pair must be {11,12}, so all three events must
eventually occur in a sorter.

Before the first such event, every allowable preparation gate avoids
all current live endpoints and frozen0/1/12. It is disjoint from the
event and commutes past it. After that event the same reasoning applies
to the new live set, and then to the third event. The argument allows
any number of preparation gates; it does not commute a gate past an
earlier preparation touching one of its operands.

Consequently every size44 completion can be rearranged into

    P28 ; (7,9) ; (9,11) ; (10,11) ; E = P31 ; E.

[certificate.json](certificate.json) records all78 standard next gates
at each of the four equality states,312 controls in total. Before the
three events, the allowable preparation-wire sets are respectively
{2,3,4,5,6,8}, {2,3,4,5,6,7,8} and {2,3,4,5,6,7,8,9}. Afterwards the only
allowable gates are on the nine wires2..10. This is a complete event
argument at arbitrary depth, not a selected fixed-depth encoding.

Full8192-input Boolean controls give120 full thirteen-bit P28 outputs
with exactly0/1/12 already correct, and84 full P31 outputs with
0/1/11/12 correct. The P31 projection on2..10 has80 states and SHA256
1eb1f208b305e646f34963308548c950af5769446a247a1f7601af313db5e152.
These are three different images. The 80-state image is the literal
teammate target, with a thirteen-comparator remaining budget at size44.

## Seven original domains exclude the forced P31 root

Use the universal nested-class theorem in
[NESTED.md](../native24-kernel-cover/NESTED.md), committed lemma9007,
bafkreieelq5auvzgfgmbfzwzvam5canm3neqjv35ybhmnne76bs5ymswpy,
source e08120d6101f2e03a554c82ac7eb208c386dd0a4.

For each selected original placement of three low and three high marks,
retain the complete seven-free-input cube. Let C=D+R count marked
touches and free gates that are identities on that whole original
domain. Delete those gates while following free carriers. Normalize
the retained oriented seven-wire word Q by its current free-output
order. Take

    B(Q) = max(16, semantic minimum anchor bound, semantic maximum anchor bound),
    lambda = C+B(Q).

The constant16 is the imported S(7) bound. The anchor bounds are defined
and proved in [ANCHORS.md](../semantic-pruning/ANCHORS.md), committed
lemma8604, bafkreidfuz2cnbkhgd7urqenzmv7iiy5tjvj5ghbmxlyhcbxhdkqdoalle.
They use imported S(5)>=9 and S(6)>=12. They are integer extension lower
bounds, invariant under global wire permutations and nondecreasing
under appended oriented gates.

For fixed selected originals, take the largest lambda per current
low/high mask pair and sum 2^lambda. The theorem bounds this sum by2^m
for every total-m sorting extension. It follows each original full
domain separately, rather than identifying conditional Boolean images
that share marker ports. The root inequality permits arbitrary
oriented continuations. Standard comparators are required for the
preceding P28 event cover.

The seven selected current classes are distinct. Their complete records
and seven-wire inner witnesses are in the certificate:

| Original low mask | Original high mask | C | B | lambda |
|---:|---:|---:|---:|---:|
| 2144 | 4736 | 24 | 18 | 42 |
| 6656 | 194 | 24 | 18 | 42 |
| 2144 | 4624 | 23 | 18 | 41 |
| 4736 | 2081 | 24 | 17 | 41 |
| 4736 | 2096 | 23 | 18 | 41 |
| 6145 | 656 | 23 | 18 | 41 |
| 6145 | 896 | 23 | 18 | 41 |

Their sum is 2*2^42+5*2^41 = **36*2^39**, strictly above
2^44 =32*2^39. Hence P31 has no total-size44 completion; the complete
forced-event argument transfers the exclusion to P28.

A private complete34320-domain packed scan found mass51*2^39, then
selected these seven witnesses. That full exploration output is
omitted and is not required by this proof. The public numeric checker
replays every selected original domain and all five inner families;
its certified selected mass is36*2^39.

## Reproduction and trust boundary

From the repository root with Python3.11.2 and its standard library,
run these commands sequentially with solver/BLAS/OpenMP threads1:

    python3 round-two/six-sorting-2/changed-b28-barrier/generate.py
    python3 round-two/six-sorting-2/changed-b28-barrier/verify.py

The producer pins its published Boolean-column, pruning, anchor and
nested-operator dependencies. The standalone numeric checker imports
no producer, profiler, sibling checker or solver. Its general scalar
primitives are copied from the same author's previous p22_verify.py
at source bc3d409028c7cfdc4e773717a1b73eadc6d19386. It uses distinct
numeric marker ranks, full-cube scalar replay, separately checked
carrier functions and heap-based anchor aggregation. This is
algorithmic independence by one researcher, not external independent
review or formalization. Smaller-network literature is imported;
its large proof corpora are not rerun.

Normal and Python -O production bytes and every scalar finite field
agree. The numeric checker verifies319488 cover assignments,
16384 full Boolean controls,896 outer clamping assignments and896
pruning-function assignments,25088 inner assignments and312 complete
next-gate controls. Eight damaged certificates reject.
Normal/optimized checker times are3.955/3.881 seconds,16948/19804KiB
maximum RSS, under the unchanged55-second stage guard and1CPU/2GiB
scope. The certificate is17478 bytes, SHA256
607952c2137ada169547793a0064d538497d8b0b8a909325fbc3d86be1e04bf0.
The fixture SHA256 is
b46d8382fc40a39ffcaad6ed7396318d8efb7efc03692b8bc160568e76dba1bb.

Expected checker status is CHANGED_B28_SCALAR_CERTIFICATE_VERIFIED,
seven selected domains and total lower bound45. SOURCE checks precede
graph submission. The result is author-proved, source-checked and
unformalized, with no external review verdict asserted.

The primary pruning/Huffman literature is
[Harder's proof](https://arxiv.org/html/2012.04400v3).
This new literal-prefix application reuses the universal9007 operator.
The native P22 exclusion9082 is contextual prior art; its native cover
is not transferred to altered roots. Earlier changed-B22 has ordinary
minimum mass448 and its sampled B26 maximum mass448. Those unsaturated
profiles permit extra single-touch/preparation branches and do not
supply the saturated complete cover used here.
