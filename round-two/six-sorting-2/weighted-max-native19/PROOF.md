# Weighted shadows normalize native N19 to an exact eleven-wire target

Actual author and executing agent: **six-sorting-2, researcher**, 2026-10-02.
Status: author proof with distinct exact implementations; unformalized,
without an external independent-review verdict.

Let N19 be the first nineteen ordered gates of the native N13L46D9
network, with wires numbered0..12:

~~~text
(0,11),(1,7),(2,4),(3,5),(8,9),(10,12),
(0,2),(3,6),(4,12),(5,7),(8,10),
(0,8),(1,3),(2,5),(4,9),(6,11),(7,12),
(0,1),(2,10).
~~~

A standard comparator(a,b), a<b, sends the smaller value to a.
Define **H21=N19;(9,11);(11,12)** and let I be its complete Boolean
image projected onto physical wires1..11. Then:

**Theorem.** N19 has a standard sorting completion of total size at most44
if and only if I has a standard eleven-wire sorting network of size at
most23. This equivalence allows arbitrary depth, order, repetitions,
interleaving and preparation length. I contains exactly **244 states**.
Its minimum completion size is in **23..25**, with an explicitly checked
25-gate control. The 23-gate feasibility question remains open.

The unrestricted thirteen-input minimum still lies in44..45 in the
[current primary table](https://bertdobbelaere.github.io/sorting_networks.html),
checked2026-10-02. This result supplies a conditional reduction of one
literal prefix, rather than a native N19 exclusion or a global lower
bound45. Native N19 has the presently established total interval44..46
and suffix interval25..27. No new sorting construction is claimed.

The proof strengthens the shadow hypothesis in the
[six-history maximum lemma, Section0](../native24-kernel-cover/P21.md),
source **dce3955b2880381edb2884b7446d282bf7bdeda5**, graph9207
**bafkreigyiwnzlza2aetdtlaoctzrvsare6jh6onf5mxb7yzftmmm7xqk4u**.
Two distinct cost5 shadows suffice where that lemma used three; more
generally their selected initial class-max weight need only exceed32,
and their secondary ports may be anywhere in0..8. Its existing event
cover and the general pruning/weighted methods are credited prior work.

## 1. Ordinary selected-family and anchored inequalities

For each fixed original pair of HIGH inputs, put distinct ranks2 and3
there and allow every assignment in the eleven other Boolean inputs.
Let D count gates touching at least one marked HIGH, once also for
stationary touches or a gate touching both marks. The current marked
pair and all touch indicators are independent of the free assignment.

For any fixed selected family T of these original domains, define

~~~text
d_T(z) = max{D_f : f in T currently has marked pair z},
W_T = sum over nonempty classes z of 2^d_T(z).
~~~

A standard gate maps each current pair to a new pair, with at most two
preimages per output pair. A double fibre charges both preimages, so

~~~text
2^(1+max(d1,d2)) >= 2^d1 + 2^d2.
~~~

Single fibres have nonnegative increments. Thus W_T never decreases,
including when selected original histories coalesce. Taking class
maxima does not identify their original free domains or images.

Deleting the marked HIGH paths in a total-m sorting network leaves an
eleven-input generalized sorter with at most m-D gates. Standardization
adds no gates. The imported **S(11)>=35** gives D<=m-35 for each original
domain. Every marked pair ends at11/12, so W_T<=2^(m-35) at every prefix.
For m<=44 we may use the common ceiling **512**.

For a reachable unary-HIGH port p, let M_p be the full pair-family mass
of classes containing p. If a gate touches this unary route, the pair
map restricted to those classes is injective, every class is charged,
and every output contains the new unary port. Thus the new anchor is
at least2M_p. An untouched anchor is nondecreasing by the fibre inequality.
Consequently a route with t future touches obeys **2^t M_p<=512**.

These are the ordinary cases of the credited
[pruning proof](../semantic-pruning/PROOF.md), graph8539
**bafkreihtqtmzuzwslaelore2kp6qhixaecubzr3urzioimae2otml3gyx4**, and
[anchored transport](../semantic-pruning/ANCHORS.md), graph8604
**bafkreidfuz2cnbkhgd7urqenzmv7iiy5tjvj5ghbmxlyhcbxhdkqdoalle**.
Pruning, standardization and route-tree/Huffman bounds are established
methods in [Harder, Section3.2 and Theorem26](https://arxiv.org/html/2012.04400v3).
The large S(11) certificate corpus and the unrestricted S(13)>=44 bound
are imported, not rerun. No semantic identity-deletion count is used.

## 2. A weaker, weighted shadow criterion

**Weighted-shadow maximum lemma.** Let P be a standard thirteen-wire
prefix whose unary-HIGH routes occupy exactly9,11,12. Assume its full
ordinary HIGH anchors satisfy

~~~text
M9>32, M11>64, M12>128,
~~~

giving future-touch upper bounds3/2/1 in a size-at-most44 completion.
Suppose three fixed original two-HIGH domains currently have

~~~text
baseline: {9,10}:D>=4, {9,11}:D>=4, {9,12}:D>=5.
~~~

Suppose also a fixed selected shadow family currently has pairs(q,12),
q in0..8, and initial selected class-max weight **W_shadow>32**.
Then every size-at-most44 completion can be rearranged without adding
gates to begin **P;(9,11);(11,12)**. The converse existence implication
is immediate. There is no minimum-event hypothesis.

Here is the complete argument. The original route on12 has only one
touch available, so it joins the other two routes only at the final
binary merge. The routes on9 and11 merge first. Port11's two mandatory
merges exhaust its two touches. The route on9 can have at most one extra
singleton event, before its first merger. Thus the complete HIGH event
word is either

~~~text
(9,11);(11,12),
~~~

or, for exactly the ten partners r in{0,1,2,3,4,5,6,7,8,10},

~~~text
K_r = (min(r,9),max(r,9));(max(r,9),11);(11,12).
~~~

Non-events avoid the currently occupied unary HIGH ports. The subsequent
forced merge events therefore commute left across all intervening
non-events. A singleton branch has normal form **P;F;K_r;E**, where the
arbitrary word F uses only{0..8,10}. The first gate of K_r remains
**after F**, since F can touch its free operand r. After moving the first
forced merge left, the second also commutes across the earlier phase:
both phases avoid11/12. These are disjoint-gate commutations, preserving
the sorting function and the total number of comparators.

Throughout F the three baseline pairs are stationary. Any F touch on10
charges the9/10 baseline without moving it, since10 exceeds every other
permitted F operand. For every r, K_r then supplies three distinct terminal
classes and lower costs

~~~text
{9,12}:7, {10,12}:7, {11,12}:8,
~~~

with mass128+128+256=512. When r=10 the first two baseline histories
exchange their terminal classes. If F touches10, one of their costs is
at least8, so baseline mass is at least640. That already violates the
ceiling. Therefore any surviving F uses only0..8, of arbitrary length.

Each shadow's secondary HIGH remains in0..8 under every such F. Write
its pair(q_i,12) and cost d_i after F. Selected-family transport ensures
its class-max mass is still greater than32. There are two exhaustive cases:

1. Some q_i differs from r. The first two K_r gates avoid that shadow;
   only the final touch on12 is charged. Its terminal pair(q_i,12) is
   different from all three baseline classes. Its positive additional
   weight makes the mass of the union of baselines and shadows exceed512.
2. Every q_i equals r. Necessarily r is in0..8. Their one current shadow
   class has weight2^d>32, hence integer d>=6. All three K_r gates charge
   a history attaining this maximum. Its terminal11/12 class has cost
   at least9 and weight at least512. **Retain the other two baseline
   classes**, each of weight at least128: the selected union has mass
   at least512+128+128=768>512.

Hence all singleton words are impossible. In the direct branch the two
merge events commute to the suffix front across their disjoint preceding
preparations. This proves the lemma for every allowed F and E, without
enumerating or limiting their lengths, functions, or depth.

The strict threshold is deliberate. A single abstract shadow of cost5
at r has weight32 and gives terminal cost8; the three baseline classes
still total512. This is a boundary control for the proof mechanism,
not a feasible prefix/sorter example or a proof of optimality of the
criterion. Two initially distinct cost5 shadows have weight64 and satisfy
the strict criterion. The old three-shadow argument discarded the other
baseline classes and instead forced one cost10 history; retaining them
permits the weaker hypothesis.

## 3. Five original histories at native N19

The complete78 original HIGH domains give unary ports9/11/12 and anchors
**64/72/176**, hence exactly the3/2/1 upper capacities needed above.
Five fixed original domains suffice:

| Original HIGH ports | Original mask | Current HIGH ports | D |
|---|---:|---|---:|
|8,9|768|9,10|4|
|9,11|2560|9,11|4|
|9,12|4608|9,12|5|
|5,7|160|5,12|5|
|7,12|4224|7,12|5|

Each row retains its own full eleven-free-input cube. The two shadow
classes have initial weight64>32. The weighted lemma therefore applies
to literal N19, even though its optional original1/7 shadow has only
cost4 and secondary port3. The old six-history hypothesis was insufficient
at N19; that earlier theorem is not being restated as the new reduction.

At H21 the two ordinary envelopes both have mass448:

| Family and held anchor | Secondary port:cost |
|---|---|
|LOW, anchor0|1:7,2:7,3:5,4:6,6:5,8:6|
|HIGH, anchor12|3:5,5:6,6:5,7:6,9:6,10:6,11:7|

There is no HIGH secondary8. These necessary inequalities do not
establish a completion or an exclusion of H21.

## 4. Exact Boolean-image equivalence and checked upper control

N19's complete Boolean image has269 states; wire0 already holds the
global minimum. H21's full image has246 states and holds minimum0 and
maximum12. Its projection I has244 distinct states. Encode a core state
as an integer with **bit j on physical wire j+1**, j=0..10. The complete
increasing list is in [certificate.json](certificate.json), with compact
JSON SHA256

~~~text
99cee56789817c69f6636ba7e247abb7144e47d61ef072405bfdf3ae9ce69f01
~~~

For a total-size-at-most44 N19 sorter, the weighted lemma moves the two
maximum events to the front. Its remaining suffix has at most23 gates.
Every subsequent gate touching held0 or12 is a standard no-op on every
reachable input, and may be deleted. The remaining eleven-wire word
sorts every state of I. Conversely, an at-most23-gate standard sorter of
all I states lifts after H21 and sorts every original Boolean input.
The zero-one principle then gives a full thirteen-input sorter. This
proves both directions and preserves arbitrary suffix depth.

An at-most22-gate core sorter would lift to total size at most43,
contradicting the imported unrestricted S(13)>=44. Thus S(I)>=23.
The native46 control is rearranged by nine explicitly checked adjacent
disjoint swaps to H21 followed by25 eleven-wire gates, all verified:

~~~text
(2,7),(3,5),(0,2),(1,3),(4,9),(5,7),(6,8),
(0,1),(2,3),(4,7),(5,8),(6,9),
(1,2),(3,6),(4,5),(7,10),(8,9),
(3,4),(5,6),(7,8),(9,10),
(2,3),(4,5),(6,7),(8,9).
~~~

These are core labels0..10. The original native46, its normalized
version and this25-gate word pass all8192 originals and all244 core
states, as applicable. No23- or24-gate witness is supplied.

## 5. Validation, imports and the remaining frontier

[generate.py](generate.py) propagates marked masks and packed Boolean
truth-table columns. [verify.py](verify.py) imports no generator, profiler,
sibling checker, solver or nonstandard package. It reconstructs all312
original pair domains through638976 full free assignments and12779520
literal numeric prefix-gate evaluations. The complete312 rows, both
full Boolean histograms, all244 target states and their original-input
multiplicities are compared entry by entry, not only by count.

The scalar budget DFS audits85 reachable route states and6630 standard
next-gate controls, recovering exactly the eleven event words. It audits
12168 LOW/HIGH pair-gate cases,10452 fibres,2028 anchors, ten saturated
baseline terminals,90 stationary10 overflows,90 shadow alternatives,
324 shadow closures, nine coalesced cost6 overflows and nine cost5
boundary controls. It rejects ten damaged certificates and three
damaged fixtures. Normal and optimized Python agree. These local
controls supplement the analytic arbitrary-length proof; a finite
preparation-word search is not a premise.

Use Python3.11.2 and the standard library, one CPU job at a time and
all solver/BLAS/OpenMP threads1, from the repository root:

~~~sh
export OPENBLAS_NUM_THREADS=1 OMP_NUM_THREADS=1 MKL_NUM_THREADS=1 NUMEXPR_NUM_THREADS=1
python3 -B round-two/six-sorting-2/weighted-max-native19/generate.py
python3 -B round-two/six-sorting-2/weighted-max-native19/verify.py
~~~

Expected status: **WEIGHTED_MAX_NATIVE19_SCALAR_CERTIFICATE_VERIFIED**.
Repeat with python3 -O -B. [checks.json](checks.json) records exact hashes,
counts and measured resources; [source-manifest.json](source-manifest.json)
pins source and compact inputs. The certificate is about21KB. No proof
corpus, private ledger, credential, raw log or generated large dataset is
required. The producer and checker are distinct algorithms by this
author; there is no external-person review or formalization claim.

The already published [native20 exclusion](../native20-finite-cover/PROOF.md),
source **422bed4dd1006c258111610d1bb470868376602e**, graph9341
**bafkreietmz5ud6ohk5a7y22gyioaf6aiw5toflcrcgfnvuaz3v3wbiuqcy**,
excludes the H21;(3,8) branch after disjoint maximum commutation. It
does not exclude all N19 completions. The complementary actual researcher
six-sorting-1's [changed B21 reduction](../../six-sorting-1/changed_b21_core11/PROOF.md),
source **27bc6c4cd42f99da693051edb06ae371da726970**, graph9220
**bafkreidpg5hwu7q2wr3kgoft6sqe7fncrbtqv7agx7l542iahdyr5s7x3a**,
is the H21;(4,8);(3,6) branch after disjoint commutation, with its
177-state,21-gate target. Its
[joint branches](../../six-sorting-1/joint_saturated_core_branches/PROOF.md),
source **2b8d0d2b5766ecb8775c72db231fa5eb06ee512a**, graph9285
**bafkreie2r7aozrslgvdkaivngzoql4g2d6r4o5jzrwypvjtefq7cetfanq**,
and [LOW binary barrier](../../six-sorting-1/one_sided_low_binary_barrier/PROOF.md),
source **941e5f4536f623c47dd3a7e92fe573f0638849ba**, graph9325
**bafkreifpsdztwtsgzzecdi2mwvgzf6cmlnnupveirp3lpq4qjulzome7cu**,
are useful branch context, not logical premises for the present lemma.

The historical [incumbent P19/P20 result](../../../sorting_networks/thirteen_twenty_prefix_exclusion/PROOF.md),
source **c40dcc78d772c2ab1fd1991d8f89e4c270491673**, graph7813
**bafkreifrmmc5ztlhitir24jn2lqdy6iekdndejcf2auf7limrwind5ydby**,
uses a different literal starting word and a two-route phase-closure
maximum proof. Its P19 conclusions are prior art and are not the native
N19 result established here. Targeted graph/literature comparison supports
the stated refinement, not historical-priority claims.

The concrete next step is a structural/certificate analysis of the
remaining first-event or first-slack branches of this exact244-state
target, preserving the peer's changed branch. Passing necessary masses,
an incomplete search, timeout, memory kill or absence of a witness is
not a sorting-completion decision. The pruning/standardization bridge,
primary size bounds and elementary analytic argument remain explicit
unformalized trust boundaries.
