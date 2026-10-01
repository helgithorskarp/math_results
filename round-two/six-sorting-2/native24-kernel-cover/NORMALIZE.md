# Three touch budgets exclude ten further native kernels

Author and executing agent: **six-sorting-2, researcher**, 2026-10-01.

The literal native P24 standard size44 question is equivalent to **14
nine-wire Boolean images at budget12**, with arbitrary suffix order and
depth. This refines the separately credited24-target result below. The
ten newly excluded original kernel IDs are

    6,7,10,16,18,25,29,30,37,40.

Every standard sorter starting with any of their literal P32 prefixes
has at least45 gates. The surviving original IDs are

    2,8,15,20,24,31,32,33,34,36,38,39,41,42.

Their existence remains unresolved. The current
[maintained table](https://bertdobbelaere.github.io/sorting_networks.html),
refreshed2026-10-01, records the unrestricted interval44..45. This is a
particular native prefix obstruction; it does not cover every initial
thirteen-input network. The normalization uses standard orientations,
while the imported inner pruning bounds allow oriented comparators.

## Precise dependencies and prior art

Use the pinned [fixture](fixture.json), ports0..12, and the original
zero-based kernel enumeration in [certificate.json](certificate.json).
Write

    P32_i = P24 ; (11,12) ; (1,2) ; T_i.

The complete arbitrary-order kernel cover is [PROOF.md](PROOF.md),
graph8690 `bafkreigxneqt4bxabyiwkznuhldfniqc43ee2ddxrkpvvsdvlwv5nkioyy`,
source `68f3f94cca06df709c264d7d72147aa347bef5aa`. Its subsequent
[minimum](MINIMUM.md) and [endpoint](ENDPOINTS.md) refinements, graphs8747
and8822, leave33 nine-wire/12-gate questions. In every size-at-most44
completion of these P32 prefixes, ports0,1,11,12 are already correct and
frozen; every remaining standard gate uses2..10.

The [paired-clamping result](TOUCH.md), graph8909
`bafkreibfvq5abfuzrwlq7byncp32ro3r7i2eptegh75of6dxaowubiffwe`, source
`e260dd848eb8616697a952840c0027965e5851c3`, proves both a transferable
future-touch budget and a single `(2,3)` root restriction for all33
cases. It excludes six initial kernels. Together with six-sorting-1's
[kernel-zero obstruction](../../six-sorting-1/six_extreme_kernel_barrier/PROOF.md),
graph8877 `bafkreih6m4wh2liw46y6ull6eitam7cv2qcbxxks2qfmojj4w4srsixqwu`,
source `d51e1a1e36e521ecfb40020ef9bde021157beabc`, this gives26 cases.

The preceding24-target equivalence is six-sorting-1's
[oriented two-kernel obstruction](../../six-sorting-1/joint_extreme_kernel_barrier/PROOF.md),
graph8925 `bafkreib7kp2spfixj5s3ossbqyzn5y4pxuusek2laaqr47fm3bc4dyevwu`,
source `4aabebc030d07b01a9dd1689723b96554db810bb`. Its complete
48-node/6864-transition certificate excludes original IDs9 and21 at all
suffix orientations and depths through the entire12-gate budget. This
peer proof, exact9784-byte committed body and all12 initial relations were
read at index8934. Seven published proof/source files were matched byte
for byte to the source commit. Its standalone scalar checker was replayed
successfully in5.869s/32640KiB, including all original cubes, positive
controls and eight corruptions. The two literal kernels match our fixture.
This is researcher dependency intake, not an external reviewer verdict.
The new ten IDs are disjoint from these credited exclusions.

The imported general mathematical bounds are the
[semantic pruning theorem](../semantic-pruning/PROOF.md), graph8539
`bafkreihtqtmzuzwslaelore2kp6qhixaecubzr3urzioimae2otml3gyx4`, and the
[semantic anchor theorem](../semantic-pruning/ANCHORS.md), graph8604
`bafkreidfuz2cnbkhgd7urqenzmv7iiy5tjvj5ghbmxlyhcbxhdkqdoalle`.
Extreme paths, wire permutations, pruning and Huffman aggregation are
established methods, credited to
[Harder, Sections2 and3, especially Theorem26](https://arxiv.org/html/2012.04400v3#S3.SS2).
The inner calculations here require only the established S(5)>=9,
S(6)>=12 and S(7)>=16. Historical small-size proof corpora are not rerun.
No priority claim is made for these methods or disjoint-gate commutation.
The contribution is the new concrete normalization and ten obstructions.
The original fixture is credited in the parent to six-sorting-1's
[projection/deletion packet](../../six-sorting-1/projection_deletion_barrier/README.md),
source `b92f5b0bcafc7fffabf245d806bb01ae94b69d61`, graph8573.

## A general three-domain normalization bridge

Fix a prefix P with the preceding frozen outer ports. For each selected
original clamping keep every assignment of its free Boolean inputs.
Use distinct negative ranks for its low markers and distinct values
above1 for its high markers. D counts marked-touch gates, once per gate;
R counts free/free gates acting identically on that complete original
domain. Delete them and track free carriers through marked exchanges.
Rename carriers by increasing physical free-output order to get the
oriented prefix Q. Let B(Q) be the maximum of the two semantic anchor
lower bounds, invariant under global wire relabeling.

The routing bridge proved in TOUCH.md gives, for any full sorter P;E of
size m,

    m >= C(P) + T_future_marked + B(Q),   C=D+R.

It conjugates the entire pruned word by its fixed final carrier
permutation. No assumption that future markers are stationary is needed.
In particular C+B bounds the number of future gates touching this
original domain's moving markers, even when Q has reversed orientations.

Suppose P has three original clampings whose current marker ports and
nested labels are

| Domain | Current low ports | Current high ports | C+B |
|---|---|---|---:|
| A2 | {0,1,2} | {11,12} | 43 |
| A3 | {0,1,3} | {11,12} | 42 |
| A4 | {0,1,4} | {11,12} | 42 |

Also suppose its exact nine-wire image contains510,509,507, with a unique
middle zero at original2,3,4 respectively. Then every standard sorting
completion of total size at most44 is equivalent, by commuting disjoint
gates, to

    P ; (3,4) ; (2,3) ; E8,

where E8 uses only original3..10 and has at most44-|P|-2 gates.

Here is the full arbitrary-word proof. In A2 the low at2 stays at2 under
every permitted standard comparator. The other four marked ports are
frozen. Thus its at-most-one future marked gate bounds the number of
future2 touches by one. State509 requires such a touch. Before it, its
unique zero cannot leave3: without2, every gate touching3 sends its
minimum to3. A first2 touch with partner greater than3 would leave1
at2 forever. Consequently2 is touched exactly once, by the root
`(2,3)`. State507 requires some `(3,4)` before this root. Its unique zero
cannot first move from4 toward a smaller port through2, since there is
no earlier2 touch; the only smaller available port is3.

In A3 the low at3 cannot leave3 before the root. In particular the
mandatory earlier `(3,4)` and the root each touch its marker. The budget
allows at mosttwo marked gates, so these exhaust it. There is exactly
one `(3,4)` before the root, and **no other pre-root gate touches3**.

In A4, the low at4 cannot move to a larger port under a standard gate.
Before the unique `(3,4)`, it also cannot move to2, whose only touch is
the later root, or to3, which would itself require an earlier `(3,4)`.
Therefore it remains at4 until the mandatory event. That event moves
it4->3, and the root moves it3->2, charging both of the at-mosttwo
future marked gates. **No earlier gate touches4**. Extra gates after
that event may touch4 once it is unmarked; they are not prohibited.

Write the original suffix as A;g34;B;g23;C. Every gate of A avoids2,3,4,
and every gate of B avoids2,3. First commute g23 left over B, then move
the pair g34;g23 left over A. These are exchanges of disjoint gates and
preserve the comparator function and size on every ordered input. All
other suffix gates avoid2, so the remaining word uses3..10. This
proves the claimed normal form for arbitrary preparation length, order
and depth. It is not a depth-restricted enumeration or a constructive
grammar presumed complete. Standard orientation is needed for the
one-zero and moving-low arguments.

## Ten certified applications and required corrections

For all ten stated kernels, A2 is the pinned stationary witness of
touch-certificate.json and is independently recomputed here. A4 uses
the same original input masks5632/3 for each case. Its current lows are
{0,1,4}, highs{11,12}, D20/R0, and B(Q8)=22. A3 uses original masks
11/260, except ID10 uses11/320. For A3, D20/R0/B22 holds except ID10
has D19/R0/B23 and ID29 has D20/R1/B21. Thus all have C+B=42.
Every original five-marker domain retains all256 free assignments.

The checker obtains the exact eight-wire images after the forced word,
with sizes49,48,50,47,51,47,48,50,46,45 in the stated ID order. It checks
on every original Boolean input that ports0,1,2,11,12 already have their
correct sorted values. Hence any word sorting such an eight-wire image
lifts to a full sorter, and the normalization supplies the converse.
Each image would need a word of size at most10.

Now choose one original three-low/three-high clamping for each P34.
Each retains its full128-assignment cube. The independently checked
pruned seven-wire word has the following bounds. Masks name original
input positions, not current marker classes; x and y are full13-bit
input and P34-output integers, with bit p denoting wire p.

| ID | Original low/high masks | D,R | B(Q7) | Marked correction port p | Boolean x->y |
|---:|---|---|---:|---:|---|
| 6 | 7,328 | 26,0 | 18 | 9 | 11->6656 |
| 7 | 7,1048 | 25,0 | 19 | 10 | 14->6208 |
| 10 | 7,328 | 26,0 | 18 | 10 | 14->6176 |
| 16 | 7,1048 | 25,0 | 19 | 10 | 14->6176 |
| 18 | 7,1064 | 26,0 | 18 | 8 | 7->6400 |
| 25 | 21,104 | 27,0 | 17 | 10 | 7->6656 |
| 29 | 11,324 | 25,1 | 18 | 10 | 7->6272 |
| 30 | 7,328 | 26,0 | 18 | 9 | 11->6656 |
| 37 | 7,1064 | 26,0 | 18 | 10 | 14->6272 |
| 40 | 21,104 | 27,0 | 17 | 10 | 7->6656 |

In every row C+B=44. The exact full Boolean input x has the wrong
P34 value on p. Every sorting suffix must therefore touch that physical
port. Until its first touch the port continues to carry this clamping's
current marker; its first touch is a marked gate even if a different
Boolean input motivated the correction. The transferable budget gives

    m >= C + 1 + B(Q7) = 45.

This contradiction excludes every normalized branch. The bridge excludes
every original size-at-most44 standard completion of each of the ten
P32 prefixes. Notice that p may be8 or9 as well as the maximum endpoint10;
the first-touch argument applies to all currently marked wrong ports.

Remove these ten distinct original IDs from the credited24-target
equivalence. No surviving target is presumed feasible. Its forward
direction discards impossible cases, and its reverse lifting direction
is unchanged. This proves the14-target equivalence at arbitrary depth.

## Reproduction and trust boundary

Python3.11+ standard library, one CPU job and one thread, repository root:

```sh
export OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1 MKL_NUM_THREADS=1 NUMEXPR_NUM_THREADS=1
python3 -B round-two/six-sorting-2/native24-kernel-cover/normalize_generate.py
python3 -B round-two/six-sorting-2/native24-kernel-cover/normalize_verify.py
```

Expected `NORMALIZED_CORRECTION_CERTIFICATE_REGENERATED` and
`ALL_NORMALIZED_CORRECTION_CHECKS_PASSED`, ten new exclusions and14
remaining targets. The compact352001-byte
[certificate](normalize-certificate.json) has SHA256
`99bcad813962ff1495a7f9f217b5ec4a8b94b83e71020754ff5eacf6f7abe490`.
The fixture, parent kernel certificate, touch certificate and peer
frontier arithmetic are pinned. The producer additionally checks the
published pruning implementation and its transitive column/anchor pins.
Earlier dependency files are unmodified.

The producer uses exact Boolean columns and dyadic aggregation. The
[standalone checker](normalize_verify.py) imports no producer, sibling
implementation, search or solver. Its scalar primitives are reused from
this author's touch checker, and are included directly for a self-contained
source. It reconstructs every certificate field using distinct numeric
marker ranks, every original free assignment and heap Huffman merges.
It checks81920 full original Boolean inputs (both P32 and P34),8960
outer free assignments,312320 inner assignments and9600 conditional
function assignments including positives. Local controls cover27648
marked-pair rows,18432 allowed disjoint-gate commutations and all24
four-wire permutations. Positive controls include the full8192-input
native46-gate sorter,640 positive clamping/pruned assignments and an
optimal16-gate seven-wire sorter. Six damaged mathematical certificates
and a changed fixture pin are rejected. The producer took0.735s/19216KiB;
the scalar verifier took3.468s/20836KiB.

Both algorithms were authored and executed by this researcher. Algorithmic
independence is not an external reviewer verdict. The universal routing,
anchor and normalization proofs and classical small-size results remain
unformalized mathematical dependencies. The finite checker verifies the
stated original domains and quantities; it does not prove those general
bridges in a proof assistant. No timeout, UNKNOWN, incomplete census,
uncertified UNSAT or heuristic-search failure is a negative premise.
The exploratory pool that found the selected domains is unnecessary for
reproduction; only the literal selected domains in the compact packet
are proof premises. No large omitted corpus is required.
