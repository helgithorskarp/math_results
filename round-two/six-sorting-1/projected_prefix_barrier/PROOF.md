# Exact scope and proof

Author: **six-sorting-1, researcher**, 2026-10-01.

Let T be the canonical word family defined in
[the earlier projection proof](../projection_deletion_barrier/PROOF.md),
source `b92f5b0bcafc7fffabf245d806bb01ae94b69d61`, graph
`bafkreierl6ojospabjparr2icxw7iapq7u6lww6vdqkl3eidqxwv5mskhy` (8573).
Its eight pinned parents are the maintained table's size/depth alternatives
on 13 through 16 inputs. For each parent, clamp exactly n-13 original
inputs independently to fixed minima/maxima, delete marked-touch gates,
bypass their surviving wires, normalize the complete remaining oriented
word, and keep words of length at most 46. Deduplicate identical complete
standard words only. No isomorphism quotient or redundant-gate deletion is
made. The canonical sorted seed-text SHA256 is
`8eaf44524362295a699d0a9aacb13368f0ec9d5a8c7ce4d14bbecf2ad6bf4cd9`.
There are 869 words: one of length 45 and 868 of length 46.

For W in T let P(W) be its literal first 24 comparators, in the pinned
flattened ordering. All 869 prefixes P(W) are distinct. The claim is:

**For every W except canonical indices 396 and 591, every sorting network
beginning with P(W) has size at least 45.** No depth is imposed on the
completion. The two exceptional words are the original thirteen-input
table words `N13L46D9` and `N13L45D10`, respectively. No existence assertion
is made for a size-44 completion of either exceptional prefix.

## Mathematical dependency

Use the proved [semantic anchor bound](../../six-sorting-2/semantic-pruning/ANCHORS.md)
by six-sorting-2, source `b49096c7b4af0920e93e78c489d69bd7105363cb`, committed
lemma `bafkreidfuz2cnbkhgd7urqenzmv7iiy5tjvj5ghbmxlyhcbxhdkqdoalle` (8604).
Its semantic family costs depend on lemma
`bafkreihtqtmzuzwslaelore2kp6qhixaecubzr3urzioimae2otml3gyx4` (8539),
[original proof](../../six-sorting-2/semantic-pruning/PROOF.md).
Harder's published `S(12)=39` and `S(11)=35` are the only imported small-size
bounds used here. The established binary-route/Huffman mechanism is
credited to [Harder, Section 3.2](https://arxiv.org/html/2012.04400v3#S3.SS2).
This contribution applies that published campaign lemma to a construction
family; it does not invent the general mechanism or claim historical priority.

For each original marked family, retain its entire Boolean free-input
domain. At every gate, D counts touches of marks and R counts an identity
on the entire current conditional free-input domain when both endpoints
are unmarked. For each final marker configuration z, take
c(z)=max(D+R) over the original histories reaching z. Families are not
merged merely because marker locations agree.

For every reachable unary minimum port p, let M_2,p be the sum of 2^c(z)
over two-minimum configurations containing p, and let M_mix,p be the
corresponding mixed-family sum. If c_1,p is the unary-minimum cost, the
port contributes

    max(16 * 2^c_1,p, ceilpow2(M_2,p), ceilpow2(M_mix,p)).

Summing these units gives K_low. The maximum formula is dual and gives
K_high. The factor 16 is 2^(39-35); upward power-of-two rounding is
essential. The dependency proves for every sorting extension of total
size m:

    m >= 35 + ceil(log2(max(K_low, K_high))).

It covers arbitrary oriented comparators, repeated gates, interleavings
and allowable depth. Thus a size-44 extension requires both masses <=512.

## Complete finite computation

`generate.py` reconstructs the entire pinned word family with complete-word
normalization, writes its canonical text, then runs `screen_anchors.cpp`.
The C++ program keeps each original clamping separately: 13 one-minimum,
13 one-maximum, 78 two-minimum, 78 two-maximum and 156 mixed histories.
Free truth tables use 64-bit columns; marker positions and D,R are
transported at each comparator. Envelopes and both anchor masses are exact
integer calculations. No numerical approximation or cutoff is used.

`verify.py` independently enumerates surviving input sets and normalizes
on the fly, using the pinned independent projection checker from 8573.
Its reconstructed canonical text matches the full entry-level seed hash.
It then uses six-sorting-2's pinned Python integer truth-column and anchor
implementations to recompute every mass for every word at cuts
8,12,16,20,24. Every one of the 4,345 mass pairs is compared literally;
all indices, coverage counts and prefix distinctness are checked.
These Python implementations have an independent scalar/Huffman checker,
whose complete public certificate was separately rerun here with all
4,473,152 free assignments passing. Written transport and imported primary
small-size bounds remain explicit, unformalized mathematical dependencies.

The final certificate gives 341 prefixes with maximum anchor mass576 and
526 with mass640. Both numbers exceed512 and have logarithm ceiling10;
the bound is therefore45 for all867 prefixes. The remaining two have
mass512 and supply only the bound44. This proves the stated exclusion.
At cut20 the analogous calculation excludes513 words and leaves356.

There is no claim for other wire relabellings, other parent networks,
longer projected words, alternate initial portions of a reordered parent,
or arbitrary thirteen-input prefixes. In particular a construction may
change a gate before the excluded24-gate prefix, or start from an earlier
prefix. The source family is not a completeness theorem for all networks.
The unrestricted problem remains44..45 according to the
[maintained primary table](https://bertdobbelaere.github.io/sorting_networks.html).

## Relation to incumbent work and current construction

The exceptional incumbent prefix contains the known P20 prefix. Its
published completion size is25, so an extension of that literal20-gate
prefix requires45 gates: lemma
`bafkreifrmmc5ztlhitir24jn2lqdy6iekdndejcf2auf7limrwind5ydby` (7813),
[prior proof](https://github.com/helgithorskarp/math_results/blob/main/sorting_networks/thirteen_twenty_prefix_exclusion/PROOF.md).
That fact is prior art, not a new exclusion here. The current unresolved
construction target is therefore the exceptional native46 word's literal
24-gate prefix, with a freely chosen20-gate suffix. The original word
supplies a22-gate completion; the present necessary bounds permit20.

The included beam and fixed invalid examples are construction experiments.
Beam truncation and Boolean-image deduplication lose completeness, and no
absence of a sorter in a beam is a mathematical negative premise. Each
fixture has its entire8192-input failure list and both anchor masses
independently replayed. Passing the bounds remains only necessary. Neither
fixture sorts, and neither resolves the44-versus45 gap.
