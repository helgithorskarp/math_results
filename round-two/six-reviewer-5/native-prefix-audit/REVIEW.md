# Independent native-prefix kernel audit and a smaller dependency set

Actual reviewer: **six-reviewer-5**, role **independent mathematical reviewer**.
Date: 2026-10-01. The shared signing key is campaign infrastructure; it does
not establish authorship or independent execution.

Target: lemma **8690**, **Native thirteen-input prefix reduces to 39 nine-wire
size-12 targets**, by **six-sorting-2, researcher**, artifact
`bafkreigxneqt4bxabyiwkznuhldfniqc43ee2ddxrkpvvsdvlwv5nkioyy`.
Target source commit: `68f3f94cca06df709c264d7d72147aa347bef5aa`.
The target's complete committed body and directed neighborhood were read.
There was no incoming review or objection at selection.

## Verdict and exact scope

**Confirmed with high confidence in the stated fixed-prefix scope.** The
arbitrary-order argument is sound, all original clamped domains were rebuilt
independently, and the complete published certificate matches reconstruction.
This is an ordinary mathematical proof with exact auxiliary computation,
not a proof-assistant formalization.

Let (P) be the literal first 24 gates of Dobbelaere's `N13L46D9` word,
on wires (0,ldots,12), in the order pinned in the
[target fixture](https://github.com/helgithorskarp/math_results/blob/main/round-two/six-sorting-2/native24-kernel-cover/fixture.json).
Every gate ((a,b)), (a<b), sends its smaller value to (a). We confirmed
all 46 literal gates against the corresponding row of the
[maintained primary table](https://bertdobbelaere.github.io/sorting_networks.html),
including order within each displayed layer.

There is a standard sorting extension of (P) of total size at most 44
if and only if one of the 39 images indexed by `remaining_ids` in the
[target certificate](https://github.com/helgithorskarp/math_results/blob/main/round-two/six-sorting-2/native24-kernel-cover/certificate.json)
is sortable by a standard comparator word of length at most 12. The
normal form is

\[
P;(11,12);(1,2);T;E,
\]

where (T) belongs to the complete 45-kernel cover, six kernels are
impossible at total size 44, and (E) acts only on wires (2,ldots,10).
No restriction on suffix depth, repetitions, or intervening gates is imposed.
The nine-wire inputs are explicit sets of 59 through 68 Boolean states;
they are not the full nine-wire cube. The review establishes the equivalence,
not existence or nonexistence for any of its 39 surviving branches.

Two additional statements are proved here. First, **the entire reduction and
its intermediate minimum-size intervals require only the published lower
bound (S(11)ge35)**. Neither (S(12)=39) nor the global lower bound
(S(13)ge44) is needed. Ordinary paired-extreme anchors already force
the normal form; conditional redundancy is needed for the six final
exclusions. Second, the 39 images form a literal inclusion antichain, and
no reversal-plus-complement image is contained in any surviving image.
This latter fact rules out these two elementary ways to shorten the
disjunction; it is not a general non-subsumption theorem.

## Independent mathematical audit

### Pruning, redundancy and terminal capacities

Fix an original input family with (ell) distinct smallest ranks and
(h) distinct largest ranks. The (13-ell-h) middle inputs are completely
free. Count each gate meeting a marked input once, including stationary
passages and gates meeting two marks, and denote this count by (D_f).
Removing marked paths leaves a circuit sorting all the middle inputs.
Its orientations and wire permutation can be standardized without extra
comparators. This is the established extreme-pruning construction; importantly,
the remaining inputs range over a full cube, not just a selected output image.

An unmarked gate that never swaps on any Boolean assignment of the free
original inputs is an identity for all ordered free inputs. If it swapped
two real values (u>v), thresholding between them would commute with every
preceding minimum/maximum operation in the pruned circuit and produce a
Boolean swap. Thus it can be deleted. Earlier identity deletions preserve
all subsequent functions, so these deletions are valid together. With (R_f)
such deletions counted, any full size-(m) extension satisfies

\[
D_f+R_f\le m-S(13-\ell-h).
\]

No middle domains belonging to different original marked families are
identified. The conditional-identity test must retain the complete domain
of the individual original family even when its marker ports coincide
with those of another family.

For an ordinary envelope (d(z)=\max_{f:z_f=z}D_f), put
(W=\sum_z2^{d(z)}). A single comparator has marker fibres of size at
most two. A double fibre has a marked endpoint in both preimages, so
its new weight is at least (2^{1+\max(d_1,d_2)}\ge2^{d_1}+2^{d_2}).
Singletons cannot lose weight. Hence (W) is nondecreasing. At a full
sorter, there is only one marked port configuration and
(W\le2^{m-S(13-\ell-h)}). The same argument applies to costs (D+R).

The target's pruning dependency is lemma 8539,
`bafkreihtqtmzuzwslaelore2kp6qhixaecubzr3urzioimae2otml3gyx4`,
whose [written proof](https://github.com/helgithorskarp/math_results/blob/main/round-two/six-sorting-2/semantic-pruning/PROOF.md)
and complete graph body were read. We independently checked the universal
bridges used here. We did not re-run every separate strict-prefix application
in that contribution.

### Paired ordinary anchors suffice

For a unary minimum route currently at (p), use just the two-minimum
ordinary profile and define

\[
M_p=\sum_{z:p\in z_{\rm low}}2^{d(z)},\qquad
b_p=35+\lceil\log_2M_p\rceil.
\]

The analogous definition uses two maxima for a unary maximum route. All
reachable unary ports of this instance have positive paired mass, so no
additional unary profile is needed to define a label.

If a comparator touches a tracked minimum port (p), the map on marker
configurations containing a low tag at (p) is injective and every such
family gains a deletion. When (p) is the minimum endpoint its tag remains
there; when it is the other endpoint, exchanging its endpoint tags is
injective on the restricted configurations. Thus the new anchored mass is
at least twice the old one. Without a touch, restricted singleton and
charged double fibres give nondecrease. Maxima are dual. Consequently a
touched route's new label is at least (b_p+1).

Two reachable routes merge at a comparator into a label at least
(1+\max(b_a,b_b)). A touched singleton doubles its dyadic weight;
untouched weights cannot decrease. Therefore
(U=\sum_{p\ {
m reachable}}2^{b_p}) is nondecreasing. At the end of a
sorter all unary routes are at one port and every paired family contains
that port. Its terminal anchored mass is the complete paired profile,
bounded by (2^{m-35}). Hence (U\le2^m) at every prefix.

This rederives the particular ordinary anchor argument needed here. The
general semantic interface was previously supplied by lemma 8604,
`bafkreidfuz2cnbkhgd7urqenzmv7iiy5tjvj5ghbmxlyhcbxhdkqdoalle`,
whose [anchor proof](https://github.com/helgithorskarp/math_results/blob/main/round-two/six-sorting-2/semantic-pruning/ANCHORS.md)
and complete graph body were read. The stronger semantic costs and all
its separate example certificates are not prerequisites for this ordinary
paired specialization.

The independently reconstructed ordinary masses at (P) are:

| Direction | Unary port | Paired anchored mass | Label using only (S(11)\ge35) |
| --- | ---: | ---: | ---: |
| minimum | 0 | 512 | 44 |
| maximum | 11 | 192 | 43 |
| maximum | 12 | 192 | 43 |

Thus both direction potentials are already (2^{44}). This alone proves
every extension of (P) has total size at least 44, without importing a
global thirteen-input lower bound. In a size-at-most-44 extension, the mass
must stay exactly constant. A touched singleton is impossible, and a binary
merge is possible only at equal labels with the smallest allowed new label.

Wire 0 is permanently untouched. A maximum route on 11 must reach output 12,
so a first maximum event exists; it must be ((11,12)). Every preceding
suffix gate avoids both endpoints, so disjoint-gate commutation moves it
immediately after (P). The merged maximum label is 44, permanently freezing
12. This does not assume the original extension began with that gate.

### Saturated second extremes and the complete kernel cover

After ((11,12)), the two-minimum ordinary configurations are precisely
({0,1}) and ({0,2}), each of cost 8. Their mass 512 saturates the
terminal ceiling (2^{44-35}). Wire 0 is forbidden, so the second minimum
must merge routes 1 and 2 by ((1,2)). All earlier remaining gates avoid
these two live endpoints, hence it also commutes to the front. The only
remaining two-minimum configuration has cost 9, permanently freezing 1.

After both forced gates the two-maximum configurations are exactly
({12,q}): cost 6 for (q=5,ldots,10) and cost 7 for (q=11).
Their total mass is (6\cdot2^6+2^7=512). With 12 frozen, every subsequent
event meeting the secondary maximum support must merge two equal-cost live
ports. A single live touch or unequal merge would strictly increase the
mass. The seven routes must finish at 11, requiring exactly six merges;
their final cost is 9, after which 11 is frozen.

Every merge replaces two support ports by one of those same ports. Thus
the support shrinks by inclusion. A gate avoiding the current support
avoids the endpoints of every subsequent merge. Moving the first subsequent
merge past all such gates is valid by disjointness. Repeating moves all six
merges to the front, irrespective of how many non-merge gates were interleaved
or how the original word was layered. Comparators on disjoint subtrees then
commute to their canonical layer order. This closes the arbitrary-length
normalization bridge; no fixed-depth or fixed-interleaving search is involved.

The six cost-6 leaves pair in 15 ways. Their three cost-7 outputs and the
original cost-7 leaf 11 pair in three ways; the two cost-8 outputs merge
last. Hence there are exactly (15\cdot3=45) kernels. Independently, we
constructed the rooted trees backwards: assign capacity one to leaves
5 through 10 and capacity two to leaf 11, split the total capacity eight
recursively into equal halves, and enumerate all topological orders of the
resulting dependency trees. This yields exactly 45 trees and 900 orders.
All 115,200 Boolean order/function comparisons agree. The mathematical
reason for equality on arbitrary values is commutation of disjoint subtrees,
not the Boolean test alone.

### Six exact exclusions and transfer of the residual problems

For kernel IDs (1,13,22,35,43,44), the following independently rebuilt
original two-maximum families have (D=9,R=1). The sole redundant gate
is numbered from one in the complete 32-gate prefix:

| Kernel ID | Original high input set | Redundant gate number |
| --- | --- | ---: |
| 1 | \(\{0,6\}\) | 31 |
| 13 | \(\{1,2\}\) | 31 |
| 22 | \(\{1,2\}\) | 31 |
| 35 | \(\{0,6\}\) | 30 |
| 43 | \(\{1,2\}\) | 31 |
| 44 | \(\{0,6\}\) | 30 |

Each identity was tested on the complete domain of its original family.
Removing ten counted gates from any full extension leaves an eleven-input
sorter. Thus (m\ge35+10=45), ruling out these six kernels at size 44.
The six records include the original and final marker masks, both counts,
and the exact redundancy mask; all seven fields match the target.

For every other kernel, the 32-gate prefix's outer pairs are the globally
smallest and largest sorted pairs on all 8,192 original Boolean inputs.
They are also the frozen ports of every hypothetical size-44 extension.
The residual image on wires (2,ldots,10) is rebuilt as a complete sorted
integer list, with bit (i) referring to original wire (i+2). All 45
lists, weight counts, sizes, and hashes match, and the lists are distinct.

A standard word sorting a surviving middle image lifts by shifting its
wire labels by two. Its concatenation with the corresponding 32-gate prefix
sorts every original Boolean input, so the zero-one principle gives a full
sorting network. Conversely every size-at-most-44 extension is normalized
as above, avoids the six excluded kernels, and leaves at most 12 gates
sorting its precise middle image. These are genuine converse implications;
passing the filter is never treated as existence evidence.

The 143-state eleven-wire image after the first forced gate has minimum
size in (19,\ldots,21), and the 141-state ten-wire image after both has
minimum size in (18,\ldots,20). All published 21- and 20-gate controls
were checked, as were the literal and normalized 46-gate sorters on every
original Boolean input. The lower endpoints follow by lifting any shorter
word to a sorter extending (P), whose paired potential already forces
size at least 44. Thus these intervals also require no global (S(13))
premise. Similarly, every surviving nine-wire image needs at least 12
standard gates; no upper bound of 12 is inferred.

## Reproducible independent evidence and trust boundaries

[audit.py](audit.py) imports neither the target generator, its checker,
the parent profiles nor any solver. Each original clamped family starts
with all of its free assignments. Values are encoded by ordered two-bit
ranks and propagated as an exact reachable set, with duplicate output
states removed after **each** gate. Families remain distinct throughout.
A deterministic gate's activity and output are unchanged by removing
duplicates within one domain; small direct uncompressed controls check
this bridge, including duplicated and reversed gate words.

The author instead used a packed truth-function generator and an independent
scalar checker that starts by replaying every assignment through the entire
prefix before compression, with a forward equal-merge DFS. Our backwards
capacity-split construction is also independent of that DFS. The published
target was read as input and comparison evidence, never imported as executable
code or used to prune our reconstruction.

The complete finite workload reconstructs 338 original family histories,
745,472 free assignments, all three intermediate snapshots and all 45 final
snapshots. Every envelope entry, anchor row, summary field, exclusion record,
image entry and kernel word matches. Full ordered family records are rebuilt;
their digests match every published record-array digest. Those full arrays
are not themselves stored in the target, so that part of the comparison is
cryptographic rather than a direct array-to-array byte comparison. The
resulting complete certificate object also matches exactly.

Four altered certificates change an image, a redundancy mask, a saturated
profile entry and the survivor list; each fails exact comparison. The local
marker audit enumerates endpoint tag fibres and restricted anchor maps,
including both orientations and outside ports. These finite controls support
the local symbolic proof, whose unchanged-port argument covers arbitrary
network length and ambient order.

The two pinned external input files and their byte lengths/hashes are in
[INPUTS.json](INPUTS.json); [fetch_inputs.py](fetch_inputs.py) downloads and
authenticates only those public inputs. Reproduce from repository root:

```sh
OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1 MKL_NUM_THREADS=1 NUMEXPR_NUM_THREADS=1 \
  python3 -B round-two/six-reviewer-5/native-prefix-audit/fetch_inputs.py --dest /tmp/six-reviewer-5-native-inputs
OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1 MKL_NUM_THREADS=1 NUMEXPR_NUM_THREADS=1 \
  python3 -B round-two/six-reviewer-5/native-prefix-audit/audit.py --input-dir /tmp/six-reviewer-5-native-inputs
```

[EXPECTED.json](EXPECTED.json) is the full deterministic receipt and is not
loaded by the checker. [VALIDATION.json](VALIDATION.json) records exact versions,
normal/optimized output agreement, runtime, memory and the output digest.
The final CPython 3.11.2 runs took 22.898 and 23.047 seconds, with peak child
RSS at most 33,672 KiB. The stable output SHA256 is
`3d065e4e98408182d55f8ba418692ccb6bf8efc3d789d7f0279971379449239f`.
There were 11,381,488 packed-state gate steps, 288 small controls and 23,148
local marker/anchor controls. Original displayed snapshots use the number
39 for faithful comparison of unary-family fields; the proved paired-anchor
dependency reduction does not require its interpretation as an S(12) bound.

Arithmetic is Python arbitrary-precision integer arithmetic; floating-point
values do not decide any mathematical claim. Execution uses one CPU job and
one numerical-library thread. No guard failure or incomplete run supplies
an exclusion. No large generated corpus, proof trace, key or private ledger
is published.

Trusted components are the ordinary pruning/threshold/commutation/zero-one
arguments, CPython's integer and set implementations, SHA256 for external
provenance, and Harder's published (S(11)\ge35). Its original large
certificate corpus and Isabelle development were not re-run. Numerical
outputs, theorem prose and published source are not confused with a formal
proof kernel. No unresolved proof gap was found in the scoped target.

## Prior art, provenance and publication assessment

[Harder's primary paper](https://arxiv.org/html/2012.04400v3) establishes
(S(11)=35), obtains (S(12)=39), and develops extreme-route pruning and
the generalized Huffman bound in Section 3.2/Theorem 26. These mechanisms
are prior art and explicitly credited by the target. We rely on the
published eleven-input lower bound, with its verification boundary stated
above. Our dependency reduction is a specialization of established route
methods, not a claim of a new general Huffman or pruning principle.

The [current maintained table](https://bertdobbelaere.github.io/sorting_networks.html)
still lists the thirteen-input size interval as 44 through 45. This is the
located primary status, not a proof that no unlocated later result exists.
Bounded searches for the literal parent identifier with prefix/kernel
terminology and the claimed semantic-anchor interface located no independent
publication of this exact 45-to-39 reduction. Absence from those searches
does not establish historical priority. The concrete reduction appears new
within the inspected campaign graph; general methods and the native parent
remain attributed to their original sources.

The parent literal word is credited to
[six-sorting-1's parent fixtures](https://github.com/helgithorskarp/math_results/blob/main/round-two/six-sorting-1/projection_deletion_barrier/parents.json),
graph 8573, `bafkreierl6ojospabjparr2icxw7iapq7u6lww6vdqkl3eidqxwv5mskhy`,
source `b92f5b0bcafc7fffabf245d806bb01ae94b69d61`. The later
[867-prefix screen](https://github.com/helgithorskarp/math_results/blob/main/round-two/six-sorting-1/projected_prefix_barrier/PROOF.md),
graph 8666, `bafkreie6zhd7cdcyvreier4yy4vtt322fugavuxsvdsuzw35czga76jewi`,
source `93d450737aec8538ef62ee0b4de54771f0fe4b42`, is contextual work.
Neither its global completeness nor its finite exclusion census is a
premise or part of this review. We verify the pinned native word directly,
rather than accepting it because a different screen retained it.

The scoped reduction is ready as reproducible research evidence: the source,
literal inputs, mathematical transfer and finite coverage are explicit.
Its practical value is a small exact disjunction for one surviving prefix.
It does not imply that the prefix is a universal normal form for thirteen
inputs or that unrestricted size 44 is excluded.

## Strengthening and improvement opportunities

**Proved: remove two imported size premises.** The paired ordinary anchor
table above, the saturated two-extreme profiles and the six individual
redundancy witnesses establish every essential step using only
(S(11)\ge35). The optional intermediate intervals and the individual
residual lower bound 12 follow from that same initial saturation. This
narrows the theorem's dependency and trust boundary; it does not improve
the global numerical frontier.

**Proved: elementary inclusion gives no further reduction.** Let
(Y_i) be a surviving nine-wire image and let
(J(x)_j=1-x_{8-j}). For distinct surviving IDs (i,j),
(Y_i\not\subseteq Y_j); for all surviving IDs, including equal IDs,
(J(Y_i)\not\subseteq Y_j). All 3,003 ordered comparisons are exact
on independently reconstructed lists. Literal inclusion would permit
discarding a larger target from an existential disjunction when a smaller
one is retained. The map (J) preserves sorted outputs and conjugates a
standard gate ((a,b)) to ((8-b,8-a)), so its inclusion test has the same
justification. Both possibilities fail here. Arbitrary wire permutations
and other standard-suffix equivalences were not tested; one must prove an
appropriate transfer before using them.

**Unproved next step: exact lower bounds on all 39 partial images.** A
complete arbitrary-order certificate proving that each needs at least
13 standard gates would exclude size 44 for this prefix. A further saturated
route reduction might shorten that task, but would need a new terminal
capacity and complete commutation argument. Checking just selected depths,
selected first gates or a union of the images would not establish the
required disjunction. Conversely, one explicit at-most-12-gate word that
sorts a surviving list would lift to a size-at-most-44 full sorter and could
be verified directly on all 8,192 original inputs.

**Unproved broader step: coverage of unrestricted prefixes.** To transfer a
fixed-prefix exclusion to the global problem requires an exhaustive justified
normal-form or prefix cover. The cited projection screen supplies a finite
specified cohort only. No such global cover is provided or suggested by this
review.
