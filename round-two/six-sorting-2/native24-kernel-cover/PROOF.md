# The native 24-gate prefix reduces to 39 nine-wire targets

Author and executing agent: **six-sorting-2**, role **researcher**, 2026-10-01.

Let P be the literal first 24 standard comparators of Dobbelaere's
`N13L46D9`, pinned in [fixture.json](fixture.json). A standard comparator
(a,b), a<b, sends the minimum to a. The order in this fixture is part of
the hypothesis. No layer or depth restriction is imposed on a suffix.

**Theorem.** P has a sorting extension of total size at most 44 if and only
if at least one of the 39 nine-wire Boolean images indexed by
`remaining_ids` in [certificate.json](certificate.json) has a standard
sorting network of size at most 12. Any such extension can be normalized,
solely by commuting disjoint gates, to

    P ; (11,12) ; (1,2) ; T ; E,

where T is one of 45 explicit six-gate kernels and E uses only wires 2..10.
Six kernels are excluded by exact semantic pruning; the other 39 give
distinct images of 59..68 states. This supplies an exact finite disjunction,
not an exclusion or construction for P, and gives no new global S(13) bound.
The theorem here concerns standard suffix comparators. No claim is made
that the specified prefix is a complete normal form for all 13-input networks.

## Dependencies and prior art

The mathematical dependency is the proved
[semantic anchor Huffman bound](../semantic-pruning/ANCHORS.md), source
`b49096c7b4af0920e93e78c489d69bd7105363cb`, graph lemma
`bafkreidfuz2cnbkhgd7urqenzmv7iiy5tjvj5ghbmxlyhcbxhdkqdoalle` (8604).
It uses [semantic extreme pruning](../semantic-pruning/PROOF.md), graph
`bafkreihtqtmzuzwslaelore2kp6qhixaecubzr3urzioimae2otml3gyx4` (8539).
Both include arbitrary-depth extension proofs. The established route-tree,
pruning, and Huffman mechanisms are credited to
[Harder, Section 3.2](https://arxiv.org/html/2012.04400v3#S3.SS2), which also
establishes S(11)=35 and S(12)=39. We claim the concrete native-prefix
normal form, complete kernel cover and target images, not priority for
the general mechanisms or binary-gate commutation.

The literal parent word comes from six-sorting-1's
[projected parent fixtures](../../six-sorting-1/projection_deletion_barrier/parents.json),
source `b92f5b0bcafc7fffabf245d806bb01ae94b69d61`, graph
`bafkreierl6ojospabjparr2icxw7iapq7u6lww6vdqkl3eidqxwv5mskhy` (8573).
The subsequent [867-prefix screen](../../six-sorting-1/projected_prefix_barrier/PROOF.md),
source `93d450737aec8538ef62ee0b4de54771f0fe4b42`, graph
`bafkreie6zhd7cdcyvreier4yy4vtt322fugavuxsvdsuzw35czga76jewi` (8666),
leaves this native prefix and an already excluded incumbent prefix.
That screen is context, not a completeness assumption or a computation
rerun in this contribution. The earlier incumbent-prefix Y1/Y2 targets
have 146/145 states and are different from the present 143-state image.

The [maintained primary table](https://bertdobbelaere.github.io/sorting_networks.html),
refreshed 2026-10-01, continues to report 44 <= S(13) <= 45. The classical
lower 44 is used only for the optional minimum-size intervals below, not
for the finite-disjunction equivalence.

## Saturation forces the first two gates

For an original clamping family, D counts gates meeting a fixed extreme
and R counts gates acting identically on its complete Boolean free-input
domain when both endpoints are unmarked. A gate meeting two marks is
charged once. Set c(z)=max(D+R) over original families at marker ports z.
The parent proof gives, for each unary extreme direction,

    b_p = max_t [ S(13-l_t-h_t) + ceil(log2 M_t,p) ],
    M_t,p = sum_{z containing p in that direction} 2^c_t(z),
    U = sum_{unary-reachable p} 2^b_p.

Every extension of total size m has U <= 2^m at every prefix. U is
nondecreasing. Touching a single reachable unary port raises its label
by at least one. Merging two reachable ports gives a new label at least
one plus their maximum. Consequently, when U=2^44, touching one reachable
port alone is impossible in a size-at-most-44 extension: it increases U.
The only allowed binary merge has equal labels and preserves U.

The independently checked P data are:

| Direction | Port | Unary mass | Two-extreme anchored mass | Mixed mass | b_p |
|---|---:|---:|---:|---:|---:|
| minimum | 0 | 16 | 512 | 256 | 44 |
| maximum | 11 | 8 | 192 | 128 | 43 |
| maximum | 12 | 8 | 192 | 128 | 43 |

Thus U_low=2^44 and U_high=2^43+2^43=2^44. No suffix gate touches wire 0.
There must be a gate touching a maximum route, since the route at 11 has
to finish on 12. Its first touch must merge 11 and 12. Every preceding
suffix gate avoids both wires, so (11,12) commutes to the front. The
merged label is at least 44; no later suffix gate can touch 12.

Put Q25=P;(11,12). Its two-minimum envelope is exactly

    ports {0,1}: D=c=8,       ports {0,2}: D=c=8.

The ordinary potential W=sum_z 2^d(z), d(z)=max D, is 512. A complete
size-44 sorter has W<=2^(44-S(11))=512. Wire 0 is already forbidden,
so the second minimum follows a weighted unary route on 1 or 2. A
single-route touch increases W, and a merge preserves W only when the
two costs are equal: 2^(1+max(d1,d2))=2^d1+2^d2. The first touch is
therefore (1,2), and it commutes to the front of the remaining suffix.
The sole remaining two-minimum state is {0,1} with cost 9, so every
later comparator on 1 would increase W beyond 512. Wire 1 is frozen.

The exact middle image after Q25 has 143 states on wires 1..11, with
canonical-list SHA256
`c31db68efdfa8d7b935b2c5541ec5d96654d98c0ef66c2733248dc9fec7c759e`.
After Q26=Q25;(1,2), there are 141 states on wires 2..11. Moving the two
forced gates left in the literal 46-gate parent gives checked 21- and
20-gate completions of these images. Conversely such a 19-/18-gate
completion would give a full size-44 network. Hence their minimum sizes
lie in 19..21 and 18..20, respectively, using the known global lower 44.

## A saturated two-maximum tree has exactly 45 kernels

At Q26 every two-maximum family has ports {12,q}, with

    d({12,q})=6 for q=5,6,7,8,9,10;
    d({12,11})=7.

Their ordinary potential is 6*2^6+2^7=512. Wire 12 is forbidden. The
secondary maximum therefore evolves as a weighted unary route on these
seven ports. The same equality argument forbids every single-route
touch and every unequal-cost binary merge. Every event touching a live
secondary-maximum port is an equal-cost binary merge, removing one port
and increasing the merged cost by one. There are exactly six such events;
the final route lies on 11 with cost 9. No later gate can touch 11.

A gate avoiding the current maximum support is disjoint from the next
binary event: both endpoints of that event are occupied. Move each such
gate past that event. Repeating moves all six binary events to the front,
preserving the full network's function. This argument allows any number
of intervening gates and any depth. It does not truncate a kernel search
at a chosen suffix length.

The six cost-6 leaves must pair into three cost-7 nodes. There are 15
perfect matchings of {5,6,7,8,9,10}. These three nodes and the original
cost-7 leaf 11 then pair into two cost-8 nodes, with three possible
matchings. Their final merge has cost 9. Operations on disjoint subtrees
commute, so one may place all three bottom merges first, both upper
merges next and the root last. This gives all 15*3=45 canonical kernels.
The independent checker instead enumerates all equal-merge events in
all orders: its 900 complete words canonicalize to exactly these 45.
For each word, all 128 Boolean assignments on the seven involved wires
also confirm equality with the canonical layered representative.

## Residual images and the six obstructions

Each normalized prefix Q26;T has size 32 and fixes the two smallest
values on 0/1 and the two largest on 11/12. Every suffix gate therefore
uses 2..10. Its exact nine-wire Boolean image is Y_T, published as the
sorted integer list in the certificate. Bit i of a list entry is the
value on original wire i+2. All 45 lists are different and have 59..68
states. Their union is not used as a substitute for the disjunction.

For kernel IDs 1,13,22,35,43,44, a checked original two-maximum clamping
has D=9 and R=1 at this 32-gate prefix. Its complete free-input domain
is retained during the calculation; the record in the certificate
identifies that original family and its redundant gate. Pruning this
family from any total-m sorting extension leaves an eleven-input sorter
with at most m-10 gates. S(11)=35 gives m>=45. These six kernels are
therefore impossible at total size 44, independently of suffix depth.

For the other 39 kernels the present filter supplies no exclusion.
If a nine-wire word of size at most 12 sorts any Y_T, lift its wires
by +2 and append it to Q26;T. Every one of the 8192 original Boolean
inputs then has sorted middle wires and fixed sorted outer pairs, so
the full network sorts by the zero-one principle and has size at most
32+12=44. Conversely every size-at-most-44 standard sorting extension
has the normalized form above, uses one of the 39 nonexcluded kernels,
and leaves a word of size at most 12 sorting its Y_T. This proves the
equivalence. No existence assertion is inferred from a filter passing.

## Exact computation and trust boundaries

The producer uses the pinned Boolean-column profile implementation.
The independent checker imports neither that implementation nor the
generator. It simulates all 745,472 assignments in the five original
clamping families at P, using distinct numeric extreme markers. Only
then does it compress the exact tuple image of each separate original
family. Every subsequent gate's activity and redundancy are tested on
that complete image. It never merges conditional domains by marker ports.

Every family envelope, summary and original-record-array hash is compared
at P, Q25, Q26 and all 45 kernel prefixes. The scalar checker also rebuilds
the exact middle lists, the outer extreme property, the 21/20-gate controls,
the literal and normalized 46-gate full sorters, all kernel representatives,
and the six exclusion witnesses. The check made 17,891,328 prefix and
6,733,113 continuation scalar gate evaluations, 24,576 full-input checks,
and 115,200 kernel-order Boolean controls; three damaged certificates
were rejected. Runtime was 60.535 seconds, peak RSS 48,276 KiB, one CPU
job/thread, Python 3.11.2. Both algorithms were authored and run by this
researcher; this is algorithmic independence, not an external reviewer
verdict or a proof-assistant formalization.

The unformalized analytic dependencies are extreme pruning, the parent
anchor transport proof, equality-case commutation and the imported
smaller-network lower bounds. No solver output, timeout, heuristic beam
or incomplete enumeration is a premise. The next lower-bound target is
an independently checked arbitrary-order exclusion of all 39 residual
size-12 problems, or a further complete structural reduction. The global
44-versus-45 problem and these 39 residual existence questions remain open.
