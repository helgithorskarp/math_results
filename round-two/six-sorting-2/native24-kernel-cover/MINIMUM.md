# Third-minimum refinement: 37 residual sorting targets

Author and executing agent: **six-sorting-2**, role **researcher**, 2026-10-01.

Let P be the literal 24-gate prefix pinned in [fixture.json](fixture.json).
Comparators are standard: (a,b), a<b, sends its minimum to a. There is no
restriction on the order or depth of a suffix.

**Theorem.** P has a sorting extension of total size at most 44 if and only
if at least one of the following targets has a standard sorting word:

* the 33 nine-wire images whose IDs are `remaining_nine_wire_ids` in
  [minimum-certificate.json](minimum-certificate.json), at size at most 12;
* the four eight-wire images with IDs 11,17,19,26, at size at most 10.

This refines the [39-target parent theorem](PROOF.md). Six of its kernels
force two further minimum gates and hence reduce from nine wires to eight.
Nested semantic pruning excludes two of those six, IDs 14 and 23, for
every standard sorting suffix, regardless of depth. Thus the native
prefix now has eight excluded kernels out of the complete 45-kernel cover.
The 37 residual existence questions are unresolved by this contribution.
The maintained [sorting-network table](https://bertdobbelaere.github.io/sorting_networks.html),
checked on 2026-10-01, still gives 44 <= S(13) <= 45. This prefix is not
asserted to cover every thirteen-input sorter.

## Dependencies and scope

The parent theorem is graph lemma
`bafkreigxneqt4bxabyiwkznuhldfniqc43ee2ddxrkpvvsdvlwv5nkioyy` (8690),
source commit `68f3f94cca06df709c264d7d72147aa347bef5aa`. Its original
certificate SHA256 is
`21981cab47d3b795b85d9b7c3ab8dbb5a086aba8e059d54154770ec59edcac06`.
Its producer, scalar checker, fixture, proof and certificate are unchanged.

We use the already proved [semantic extreme bound](../semantic-pruning/PROOF.md),
graph8539 `bafkreihtqtmzuzwslaelore2kp6qhixaecubzr3urzioimae2otml3gyx4`,
and [semantic anchor bound](../semantic-pruning/ANCHORS.md), graph8604
`bafkreidfuz2cnbkhgd7urqenzmv7iiy5tjvj5ghbmxlyhcbxhdkqdoalle`.
The former gives m >= S(n-l-h)+ceil(log2 V), where c(z) is the maximum
marked-touch count D plus conditional redundancy count R at ports z and
V=sum_z 2^c(z). Each original conditional domain is kept separately before
forming that maximum. V is nondecreasing along any extension.

The imported lower bound S(9)=25 is established by
[Codish, Cruz-Filipe, Frank and Schneider-Kamp](https://arxiv.org/abs/1405.5754).
The smaller exact values S(7)=16 and S(8)=19 are the classical bounds in
the maintained table and in the background of
[Harder's primary account](https://arxiv.org/html/2012.04400v3#S3.SS2).
The established pruning/Huffman mechanism is credited there. Novelty here
is the concrete third-minimum normal form, its six exact images and the
two nested pruning obstructions; this is not a new proof of S(9)=25.
The native input fixture and the projected-prefix screen are credited in
the parent proof to six-sorting-1, source commits
`b92f5b0bcafc7fffabf245d806bb01ae94b69d61` and
`93d450737aec8538ef62ee0b4de54771f0fe4b42`, graphs8573 and8666.

## Saturation forces (3,4), then (2,3)

The parent normal form is

    P ; (11,12) ; (1,2) ; T ; E,

where T is one of 45 six-gate kernels. At its 32-gate prefix, wires
0,1,11,12 are frozen by saturated pruning bounds. Every later comparator
uses wires 2..10. For each T with ID 11,14,17,19,23,26, the complete
three-minimum/one-maximum semantic envelope is exactly

| Minimum ports | Maximum port | max D | c=max(D+R) |
|---|---:|---:|---:|
| {0,1,2} | 12 | 17 | 18 |
| {0,1,3} | 12 | 16 | 17 |
| {0,1,4} | 12 | 16 | 17 |

Consequently V=2^18+2^17+2^17=2^19. A complete size-at-most-44 sorter
has V<=2^(44-S(9))=2^19 at every prefix. This budget is saturated.
With 0,1,12 frozen, the remaining low mark follows a weighted unary route
on ports 2,3,4, with costs 18,17,17 respectively.

A comparator touching just one live route sends its cost to at least
c+1, strictly increasing V. A comparator merging two live routes sends
the merged cost to at least 1+max(c1,c2). Thus saturation permits such a
merge only when c1=c2. A comparator avoiding live routes preserves their
ports; saturation prevents it from increasing any envelope cost through
conditional redundancy. The first live event is therefore (3,4). All
preceding gates avoid 2,3,4 and commute past it. The remaining live routes
are now 2 and 3, both of cost18, so their next live event must be (2,3).
Intervening gates avoid 2 and 3 and commute past this event as well.
There is then one route at 2 of cost19. Any later touch of wire2 would
increase V beyond its cap, so wire2 is frozen.

This proves the arbitrary-order normal form

    P ; (11,12) ; (1,2) ; T ; (3,4) ; (2,3) ; E8,

where E8 uses only original wires 3..10 and has size at most 10. The
commutation argument allows any number of intervening gates; a fixed
suffix depth or a selected bounded enumeration is not a hypothesis.
The checker separately classifies all 36 standard pairs on wires2..10
at each of the two events and obtains exactly this one complete word.

The exact middle images after the 34-gate prefixes are:

| Kernel ID | Eight-wire states | Status at total size44 |
|---:|---:|---|
| 11 | 51 | unresolved size10 target |
| 14 | 51 | excluded below |
| 17 | 49 | unresolved size10 target |
| 19 | 51 | unresolved size10 target |
| 23 | 52 | excluded below |
| 26 | 49 | unresolved size10 target |

Bit j in each published image denotes original wire j+3. All six lists
are different. Scalar replay verifies that the three lowest and two
highest values are already fixed for every original Boolean input.
A word sorting one of these middle images therefore lifts to a full
size-at-most-44 sorter. Conversely every such extension using one of
these kernels has the stated normal form and sorts that image.

## Two nested pruning obstructions

At each selected 34-gate prefix, clamp three original inputs below all
free values and one original input above them. The exact witnesses are:

| Kernel | Original low inputs | Original high input | D | R | Retained gates |
|---:|---|---:|---:|---:|---:|
| 14 | {0,1,3} | 8 | 17 | 2 | 15 |
| 23 | {0,2,4} | 8 | 17 | 2 | 15 |

After deleting the marked touches and the two gates acting identically
on the complete conditional free-input domain, track each remaining wire
through the deleted marker exchanges and relabel its final physical
output position. This produces the explicit standard nine-input prefixes
Q14 and Q23 in `nested_exclusions[].retained_prefix`. Their free outputs
are original wires3..11, and their input relabels are permutations of all
nine free inputs. The checker compares each pruned function with the
original clamped function on all 512 free assignments.

If the original 34-gate prefix had a full sorting extension N of size m,
this operation would give a nine-input sorting extension of Q_i with
at most m-(17+2)=m-19 comparators. The pruning removes only certified
prefix redundancies; any additional deletions in the suffix can further
reduce this count. Both Q_i have a lower bound of 26 as follows.

For Q14 its mixed-pair envelope has states

    low at0, high at8: c=9;
    low at5, high at8: c=6.

Hence V_mixed=2^9+2^6=576, and the semantic extreme theorem gives
S(7)+ceil(log2 576)=16+10=26. In particular this exceeds the budget25.

For Q23 the unary minimum reaches 0 and 3. At port0 its anchored
two-minimum semantic mass is 288; at port3 it is 32. Its mixed masses
are 256 and32, and its unary masses are 16 and2. The anchor formula gives

    b0=max(19+4, 16+ceil(log2 288), 16+8)=25,
    b3=max(19+1, 16+5, 16+5)=21.

Thus U_low=2^25+2^21>2^25, so ceil(log2 U_low)=26. Equivalently,
the normalized mass with base16 is 544>512. This second obstruction
needs the established anchor aggregation, beyond the individual
semantic-family masses. The complete inner five-family records are
independently enumerated and matched by hashes and literal envelopes.

In both cases m-19>=26, giving m>=45. Therefore kernels14 and23 are
excluded in the original 39-case parent disjunction, including every
possible standard suffix order and depth. Removing these two cases
and substituting the four other eight-wire equivalences proves the
37-target theorem. None of the remaining questions is decided here.

## Reproduction and computational boundary

Python3.11+ and the standard library suffice. From the repository root,
use one CPU job and one thread:

```sh
export OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1 MKL_NUM_THREADS=1 NUMEXPR_NUM_THREADS=1
python3 -B round-two/six-sorting-2/native24-kernel-cover/minimum_generate.py
python3 -B round-two/six-sorting-2/native24-kernel-cover/minimum_verify.py
```

The producer uses the pinned original Boolean-column implementation.
The checker imports only the pinned independent scalar `verify.py`;
it imports no producer or sibling column profiler. It enumerates all
1,464,320 assignments of the 2,860 original four-mark families at P,
compresses each original family's exact tuple image separately, and
extends those images through all six literal minimum reductions.
It compares every original-record-array hash and every envelope/summary
at lengths32,33,34. There are 35,143,680 initial and 6,856,442 continuation
scalar gate evaluations, plus all 8,192 original Boolean inputs for
the middle images. The nested check uses 1,024 conditional function
assignments and 46,080 inner extreme-family assignments, and checks the
unique two-event minimum cover and three damaged certificates.

Expected status is `ALL_THIRD_MINIMUM_REFINEMENT_CHECKS_PASSED`, with
two additional exclusions and37 remaining targets. The complete run
took47.243 seconds and101,460 KiB peak RSS on Python3.11.2. The compact
certificate is31,973 bytes; SHA256 is
`147912afe63dc06c981e2a8e755ad279cb1907f913f6fa1489180ae96e6e39dd`.

The analytic dependencies are the parent normal form, the proved
semantic/anchor transports, the equality-case commutation argument and
the established smaller-network lower bounds. These are not formally
verified in a proof assistant. Algorithmic independence refers to the
two different implementations by this researcher; it is not an external
reviewer verdict. No solver result is used as a proof premise.
