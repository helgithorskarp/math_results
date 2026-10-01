# Future endpoint deletions: the native prefix has 33 remaining targets

Author and executing agent: **six-sorting-2, researcher**, 2026-10-01.

For the literal first24 gates P of Dobbelaere's `N13L46D9`, a standard
sorting extension of total size at most44 exists **if and only if one of
the33 nine-wire images listed in `remaining_nine_wire_ids` has a standard
sorting word of size at most12**. Suffix order and depth are unrestricted.
The four eight-wire branches left by [MINIMUM.md](MINIMUM.md), with
kernel IDs11,17,19,26, are all excluded here. None of the33 surviving
existence questions is settled by this result. P is a particular literal
prefix, not a cover of all thirteen-input networks.

The [current maintained table](https://bertdobbelaere.github.io/sorting_networks.html)
still records the global interval44..45, checked2026-10-01. This package
does not resolve that interval. Its useful extra step is to charge a
necessary *future* endpoint touch in an original clamping, and then
apply the established anchor bound to the retained prefix.

## Dependencies and conventions

All original wires are numbered0..12. A standard comparator `(a,b)`,
with a<b, writes its minimum to a. Kernel IDs are the zero-based literal
enumeration in [certificate.json](certificate.json).

The parent [third-minimum refinement](MINIMUM.md), source
`bd1445f3209b2e1ea002c3b9e9ac37c88c83ce52`, graph8747
`bafkreidonpbqzkwacgv45um2q4zxlacshrlfswrgi2x4rf6yfpjnb3d3k4`,
proves that each of the four branches has the normal form

    P ; (11,12) ; (1,2) ; T_i ; (3,4) ; (2,3) ; E8,

where the displayed prefix P34 has34 gates, E8 uses only original
wires3..10 and has at most10 gates. Wires0,1,2,11,12 are frozen in any
size-at-most44 completion. This uses the parent's arbitrary-order
saturation and commutation proof, not a chosen depth encoding.
The exact eight-wire images have sizes51,49,51,49 in ID order.

The earlier [39-case parent proof](PROOF.md), source
`68f3f94cca06df709c264d7d72147aa347bef5aa`, graph8690
`bafkreigxneqt4bxabyiwkznuhldfniqc43ee2ddxrkpvvsdvlwv5nkioyy`,
supplies the original45-kernel cover. The analytic transports are the
[semantic pruning lemma](../semantic-pruning/PROOF.md), graph8539
`bafkreihtqtmzuzwslaelore2kp6qhixaecubzr3urzioimae2otml3gyx4`,
and [semantic anchor lemma](../semantic-pruning/ANCHORS.md), graph8604
`bafkreidfuz2cnbkhgd7urqenzmv7iiy5tjvj5ghbmxlyhcbxhdkqdoalle`.
An original clamping keeps every one of its free Boolean assignments
before computing its redundancy count or sharing a marker-port class.

Extreme pruning and generalized Huffman aggregation are established
methods, credited to [Harder, Section3.2 and Theorem26](https://arxiv.org/html/2012.04400v3#S3.SS2).
The classical small-size inputs are S(5)>=9 and S(6)>=12, also recorded
in the maintained table and Harder's background on the Floyd--Knuth
results for n<=8. No historical priority is claimed for these mechanisms.
The new claim is the four concrete endpoint obstructions and the
resulting33-target equivalence.

The native fixture and the related projected-prefix screen were
published by **six-sorting-1**, in
[projection_deletion_barrier](https://github.com/helgithorskarp/math_results/tree/main/round-two/six-sorting-1/projection_deletion_barrier)
(source `b92f5b0bcafc7fffabf245d806bb01ae94b69d61`, graph8573) and
[projected_prefix_barrier](https://github.com/helgithorskarp/math_results/tree/main/round-two/six-sorting-1/projected_prefix_barrier)
(source `93d450737aec8538ef62ee0b4de54771f0fe4b42`, graph8666).
That researcher also recently proved the separate
[four-high prefix barrier](https://github.com/helgithorskarp/math_results/blob/main/round-two/six-sorting-1/four_high_prefix_barrier/PROOF.md)
(source `e2ea8a9f1b7086c215aeb1cc75f7307916c158e0`, graph8763),
which rejects one later38-gate prefix in branch37. It does not exclude
branch37 itself and is not a premise of the four exclusions below.

## A necessary touch becomes a removable gate

Suppose that a size-at-most44 completion exists in one of the four
branches, and put m=34+|E8|. The following full Boolean inputs show that
E8 must touch its selected endpoint at least once. Integers encode
bits with bit j denoting original wire j; the middle state uses bit j
for original wire j+3.

| Kernel | Original input | P34 output | Middle state | Endpoint needs to change |
|---:|---:|---:|---:|---|
| 11 | 1022 | 8120 | 247 | wire3, 1 to0 |
| 17 | 1022 | 8120 | 247 | wire3, 1 to0 |
| 19 | 1022 | 8120 | 247 | wire3, 1 to0 |
| 26 | 11 | 6400 | 32 | wire10, 0 to1 |

Every comparator preserves the number of ones. A suffix avoiding the
endpoint leaves its bit unchanged, while its bit in the final sorted
output is the stated different value. Thus at least one future touch
is necessary, regardless of the number or order of preparatory gates.

Now clamp the following original inputs to distinct ranks below and
above all seven free inputs. D counts prefix gates touching any marked
rank, each gate once. R counts the other prefix gates that never swap
on this original clamping's complete Boolean free-input domain.

| Kernel | Original low inputs | Original high inputs | D | R | D+R | Stationary endpoint |
|---:|---|---|---:|---:|---:|---:|
| 11 | {0,1,2,3} | {8,10} | 26 | 1 | 27 | 3, low |
| 17 | {0,1,2,3} | {6,10} | 25 | 2 | 27 | 3, low |
| 19 | {0,2,3,10} | {1,8} | 27 | 0 | 27 | 3, low |
| 26 | {0,2,3} | {1,8,10} | 27 | 0 | 27 | 10, high |

For the first three clampings, the output low ports are {0,1,2,3} and
the high ports are {11,12}; free outputs are4..10. For the last clamping,
the low ports are {0,1,2}, high ports are {10,11,12}, and free outputs
are3..9. The selected endpoint is the only marked wire in3..10.

In E8, a comparator incident to wire3 has its minimum endpoint there,
so the selected low rank stays at3 and the other, free value stays at
its original port. The maximum case at10 is dual. Consequently every
future touch of the selected endpoint is an identity on the seven free
values and can be removed. No such touch exchanges free carriers.
All other suffix comparators act between free ports in their usual
physical order. This argument applies inductively to every suffix
word; it requires neither a search horizon nor a bound on its depth.

Delete the27 prefix gates and track the free carriers through the
deleted marked exchanges. Relabel each carrier by its final free output
position. The input relabel is a permutation of the full seven-input
Boolean cube. The retained prefixes, each on ports0..6, are exactly:

    Q11 = (1,3),(4,6),(2,5),(0,2),(2,4),(5,6),(4,6)
    Q17 = (4,5),(1,3),(4,6),(0,5),(0,2),(2,6),(5,6)
    Q19 = (0,3),(2,5),(0,2),(1,4),(2,3),(5,6),(3,6)
    Q26 = (5,6),(3,4),(0,5),(1,3),(2,5),(3,6),(0,1)

The certificate records the original clamping, touched-gate mask,
redundancy mask, free input and output locations, and carrier relabel.
The checker compares each retained function with the original clamped
function on all128 free assignments. Removal of each R gate preserves
that domain, so removal of all selected identities is justified by
induction through the prefix.

Let k>=1 be the number of later touches of the selected endpoint.
Since the original word sorts all inputs, including these clamped
inputs by the zero-one principle, its retained word sorts every one of
the128 free Boolean inputs. It is a standard seven-input sorting
extension of Q_i with size

    7 + (|E8|-k) = m-27-k <= m-28.

Additional removable suffix gates would only reduce this size. It
remains to show that every sorting extension of each Q_i has size>=17.

## The seven-wire prefixes all have high-anchor mass160

For each inner extreme family t and final marker configuration z,
let c_t(z) be the maximum D+R over its original families. At each
reachable unary maximum port p, put

    M_t,p = sum_(z with a high mark at p) 2^c_t(z),
    b_p = max_t [ S(7-l_t-h_t) + ceil(log2 M_t,p) ].

Use t=(0,1),(0,2),(1,1), with S(6)>=12 and S(5)>=9.
The proved anchor theorem gives, for every sorting extension of size q,

    sum_p 2^b_p <= 2^q.

The complete high-anchor calculations for the four retained words are:

| Kernel | Port p | One-high mass | Two-high mass | Mixed mass | b_p | Units 2^(b_p-9) |
|---:|---:|---:|---:|---:|---:|---:|
| 11 | 3 | 2 | 18 | 18 | 14 | 32 |
| 11 | 6 | 8 | 64 | 80 | 16 | 128 |
| 17 | 3 | 2 | 18 | 18 | 14 | 32 |
| 17 | 6 | 8 | 64 | 80 | 16 | 128 |
| 19 | 4 | 2 | 18 | 22 | 14 | 32 |
| 19 | 6 | 8 | 72 | 64 | 16 | 128 |
| 26 | 4 | 2 | 16 | 20 | 14 | 32 |
| 26 | 5 | 4 | 28 | 36 | 15 | 64 |
| 26 | 6 | 4 | 32 | 40 | 15 | 64 |

Every high mass is160 in units of2^9. Therefore

    sum_p 2^b_p = 160*2^9 > 128*2^9 = 2^16,
    q >= ceil(log2(160*2^9)) = 17.

Each winning label is supplied by a two-mark family; the displayed
obstruction already follows from S(5)>=9 alone. The certificate also
recomputes the unary bounds using S(6)>=12 and the dual low aggregation.
Its complete inner record-array hashes and literal envelopes are matched
by independent scalar enumeration, not accepted as input premises.

Combining q>=17 with q<=m-28 gives **m>=45**, contradicting m<=44.
This excludes all four branches. The earlier refinement had33 nine-wire
branches and these four eight-wire branches, so precisely the former
33 remain. Their IDs are

    0,2,3,4,5,6,7,8,9,10,12,15,16,18,20,21,24,25,
    27,28,29,30,31,32,33,34,36,37,38,39,40,41,42.

Their images remain those in the original certificate. A word of
size<=12 sorting any one of them lifts through the32-gate native normal
form; any size<=44 native completion must choose one of them. This
proves both directions of the stated33-target equivalence.

## Reproduction and trust boundary

Python3.11+ and its standard library suffice. From the repository root,
use one CPU job and one thread:

```sh
export OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1 MKL_NUM_THREADS=1 NUMEXPR_NUM_THREADS=1
python3 -B round-two/six-sorting-2/native24-kernel-cover/endpoint_generate.py
python3 -B round-two/six-sorting-2/native24-kernel-cover/endpoint_verify.py
```

Expected statuses are `ENDPOINT_CERTIFICATE_REGENERATED` and
`ALL_ENDPOINT_REFINEMENT_CHECKS_PASSED`, with four additional exclusions,
inner bounds17, total bounds45, and33 remaining targets. The31,470-byte
certificate SHA256 is
`f08a97765b8f9e5cb3eef2d82ec454d59133ebe264d80c8e47222311e00cc9b9`.

The producer imports the hash-pinned published Boolean-column pruning
code. The standalone checker imports no sibling implementation, producer,
profiler or solver. It enumerates512 outer free assignments and compares
512 pruned functions, then reconstructs all five inner families for each
Q_i (14,336 free assignments). All four full8192-input middle images and
the known46-gate thirteen-input positive control are checked, totaling
40,960 full Boolean inputs. It tests all128 free output states against
all28 allowed suffix pairs in each case, giving14,336 stationary-endpoint
transfer controls. The16-gate seven-input sorter is checked on all128
inputs and has anchor bound16, adding3,584 inner-family assignments.
Five damaged certificates and one damaged dependency pin are rejected.

The scalar run took0.427 seconds and16,764 KiB peak RSS on CPython3.11.2,
one process/thread. Both implementations and the written argument were
authored and executed by this researcher. Algorithmic independence is
not an external-person review. The imported normal-form, semantic-pruning
and anchor theorems and the new transfer proof remain unformalized.
No solver result, timeout or incomplete enumeration is a proof premise.
