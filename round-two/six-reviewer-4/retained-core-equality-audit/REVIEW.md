# Independent retained-core equality audit and sharp exact-retention bounds

Actual reviewer: **six-reviewer-4, independent mathematical reviewer**, 2026-10-02. A shared signing identity does not establish distinct authorship.

## Verdict and precise scope

**Confirmed, with high confidence, as an exact computer-assisted theorem about the specified labeled core.** Target LEMMA9251, `bafkreignuqfdr6llbntn6s6gp7qpfq4fn6oiwzwsofyt7wssxopp3mihgy`, is six-code-2's *A(18,6,5): equality rigidity at the known retained-55 core bound*. Its [complete proof](https://github.com/helgithorskarp/math_results/blob/main/round-two/six-code-2/core_retention_rigidity/PROOF.md) and [source](https://github.com/helgithorskarp/math_results/tree/main/round-two/six-code-2/core_retention_rigidity) have verified source commit **1868799e4a622fd6442485335891adace47a5960**.

Let \(C\) be the 57 literal weight-five words in [CORE.json](CORE.json), on points \(0,\ldots,17\), with integer bit \(p\) representing point \(p\). Let \(B\) be any family of distinct five-subsets with pairwise intersections at most two. The reviewed assertion is
\[
 |B|=69,\quad |B\cap C|\ge55\quad\Longrightarrow\quad C\subseteq B.
\]
There are exactly 84 such labeled size-69 codes, all reconstructed here. They form the complete connected component of the credited seed under admissible one-word size-preserving replacements, with 192 undirected edges and common intersection exactly \(C\). All statements transport under any common coordinate permutation. There is no output symmetry or point-replication assumption.

Prior LEMMA7540, `bafkreiejepv7r32pq45omfybeiapo33mzoaxo77zxz7ljymykko57nbp4y`, already supplied the retained-55 upper69 and the full-core84 component. Those facts are recomputed here and credited, rather than advertised as new. The additional equality/restoration statement in9251 is confirmed. This review also proves the sharper exact-retention classification below. No unrestricted upper69, new lower69 construction, global classification or resolution of the campaign interval69..71 is claimed.

## Complete finite reduction and independent upper proof

Enumerate every one of the \(\binom{18}{5}=8568\) physical words. For each word \(w\), compute
\[
 c(w)=\{i:|w\cap C_i|\ge3\}.
\]
Core words have their own index in this conflict set. Omitting self-conflicts would incorrectly admit retained anchor words as additional words. A separate triple-owner calculation agrees on every word. The 57-word core owns exactly 570 distinct triples. The complete conflict-size histogram, for sizes0 through10, is
\[
(26,73,166,386,1317,2072,2107,1381,690,298,52).
\]
For a deleted pair \(R\), the retained anchor is \(C\setminus R\), of size55. Its complete candidate domain is precisely
\[
 D_R=\{w:c(w)\subseteq R\}.
\]
This includes the two deleted core words and excludes every retained word. Two candidates conflict exactly when their physical intersection has size at least3. Thus any further words are exactly an independent set of this conflict graph. No arbitrary-code word is removed by a symmetry or degree filter.

The independent engine [independent.py](independent.py) splits each candidate graph into two halves. It computes a table for **every** right-half vertex subset \(S\). Choosing its least vertex \(v\), write \(S_0=S\setminus\{v\}\) and \(S_1=S_0\setminus N(v)\). Then
\[
 \alpha(S)=\max(\alpha(S_0),1+\alpha(S_1)).
\]
The numbers of maximum sets are taken from the winning branch, or added on a tie, with empty-set values \((0,1)\). The branches are disjoint. Right halves have at most18 vertices, so each exact right count is at most \(2^{18}\); checked unsigned storage has at least32 bits. Merged counts use Python integers.

The left half independently visits every literal subset and tests its internal independence. For each valid left set \(L\), it looks up the right table on the vertices having no cross-conflict with \(L\). A full independent set has a unique left/right decomposition, so maximizing these sizes and summing their counts gives exhaustive, nonoverlapping coverage. Four optima are computed per pair: unrestricted, first deleted core word forbidden, second forbidden, and both forbidden. Forbidding vertices removes them before the table lookup and excludes forbidden left sets. No lower bound, author maximum inventory or claimed pair cover is search input.

All 1,596 deleted pairs are checked exactly once. Candidate-size counts are:

| Domain size | Number of pairs |
|---:|---:|
|28|1090|
|29|78|
|30|356|
|31|32|
|32|30|
|33|8|
|36|2|

Every unrestricted pair optimum is14, with exactly84 maximum tails. **Forbidding either individual deleted word gives optimum13 in every case.** Therefore every14-word tail restores both core words. This proves equality rigidity directly, independently of an aggregate84 comparison. The separate full-core26-word domain has optimum12 and all84 maximum tails are enumerated. Adding the two deleted core words to these tails supplies84 distinct positive pair maxima; restoration and complete full-core enumeration prove that these are the entire maximum inventory for every puncture.

For any code retaining at least55 core words, choose a pair \(R\) containing all its missing core words. The code contains the55-word anchor and its remaining words lie in \(D_R\), proving upper69. At size69 the strict forbidden-word readouts force all57 core words back. This also covers codes originally retaining56 or57 words; the argument does not assume they retain exactly55.

The 84 full-core codes and all their edges are checked literally. Connectivity is checked by graph traversal and common intersection by actual word sets. A neutral exchange deleting a core word would leave56 retained core words, so rigidity requires that same core word back. Other neutral exchanges keep the full core and hence stay in the complete84 inventory. Consequently the component is closed. No appendable word exists, since a containing-core70-word code would violate the computed bound.

## Strengthening and improvement opportunities

**Proved: sharp classification by the exact omitted core words.** All57 singleton punctures are also computed with the deleted core word forbidden. Every resulting maximum tail has size12, so every code retaining exactly56 core words has size at most68. All57 choices attain68. The maximum-count distribution is53 omitted words with84 completions and four with174: **5,148 distinct labeled size-68 codes with exact retention56**.

For exactly55 retained words, forbid both deleted core words. Precisely **66 deleted pairs** have maximum tail13 and hence sharp maximum68. The other **1,530 pairs** have maximum tail12 and sharp maximum67. [EXACT55_EXCEPTIONS.json](EXACT55_EXCEPTIONS.json) lists every exceptional pair by zero-based positions in CORE.json, followed by its number of size-68 completions. Their counts sum to **3,236 distinct labeled size-68 codes with exact retention55**. No duplicate-code division is needed: a code's omitted core set is unique. Thus there are exactly8,384 labeled size-68 codes retaining55 or56, but not57, core words.

[SHARP_TAILS.json](SHARP_TAILS.json) supplies a physical size-68 witness for each of the66 exceptional pairs, one singleton size-68 witness and a full-core size-69 witness. All lower witnesses are checked independently by [check_witnesses.py](check_witnesses.py), which imports no search code. Sharp67 for every other pair follows by deleting that pair from any full-core69 code. The full exact count distributions are in [expected.json](expected.json). These are restricted finite refinements, with no claim of historical priority.

**A useful larger frontier remains open in this review.** Extending equality rigidity to codes retaining54 core words requires all triple omissions, including words whose core-conflict support has size3. The present1,596-pair carrier omits that sector. Six-code-2's private triple-puncture report is researcher context, not imported evidence or a verdict here. A complete committed source and independent triple-domain check would be needed. More generally, escaping this labeled core obstruction does not construct a70-word code; arbitrary missing-core words and larger trades remain separate obligations. The reviewer does not extend the search to those uncommitted claims.

**Proof simplification opportunity, unproved.** Small explicit conflict-clique covers of the forbidden-word domains could replace the half-table upper computation by direct certificates. A cover of13 cliques for every single-forbidden pair domain, and12 for the1,530 double-forbidden67 domains, would suffice if every physical vertex and every within-clique conflict were verified. Such covers are not asserted to exist, since clique-cover number need not equal independence number.

## Independence, verification and reproducibility

I independently selected9251 after complete signed graph intake, comparison with other committed claims, and the absence of an incoming review. Other reviewers' sufficient and active audits were respected. First the defining statement, ordinary proof and literal INSTANCE were visible. The first engine used **only the57 core words**. Its complete1,082,741-byte result was sealed before inspection of the author's executable, EXPECTED or maximum certificate. This is implementation independence, not blindness to the mathematical claim.

The exhaustive half-table/cross-merge method differs from the author's increasing full-clique DFS and adaptive memoized full-graph deletion-contraction. The elementary recurrence in the right half is shared mathematics and is disclosed. No researcher executable is imported by the independent engine. Complete normal and Python-O records agree bytewise:

`283bc117e5f9a53bb28ec19294619025ab65fb8d6441f432fc854c23cfc6c6ee`.

The pair computation visits34,865,152 literal left masks and37,715,968 right masks;28,113,664 left masks are independent. These count actual table coverage, without symmetry factors. The normal/O [controls](controls.py) compare exact maxima, counts and witnesses with direct full-subset enumeration on all1,100 simple graphs of orders0..5, for all33,867 forbidden domains. Eighteen separate semantic damages are rejected. Three actual point permutations transport all8,568 conflict rows, all84 full-core codes and six entire pair optima/count records; there are258 positive code/pair transports. The controls distinguish true physical relabeling from mere expected-answer comparison.

Only after the first seal did I inspect and separately execute both original programs, in normal and optimized modes, with their unchanged internal60-second whole-frontier guards. The later comparison reconstructs **every physical candidate and every actual maximum-tail bitset** in all1,596 author records from the independently proved restoration theorem and independent full-core inventory. It compares134,064 maximum tails, all84 full codes and the entire8,568-row oracle. The author's full original stable evidence and all11 semantic damages per mode are also compared against its preceding frozen record. This corroboration is additional evidence; it is not the independent upper proof.

The original prior core identification is rechecked from the included credited1,311-byte ACL69 fixture, whose SHA256 is
`cf71ac44391d86eeb244cbf75de3fee5cfbedb36081175a830e7571acf370c7d`.
Delete one-based rows6,9,14,17,22,27,30,32,37,54,55,58 and apply old-to-new map
\[
[7,3,12,0,5,10,2,9,16,15,11,1,8,4,6,14,13,17].
\]
The57 resulting words equal CORE.json as a literal set, and the mapped69 seed belongs to the84 computed states. This imports no earlier numerical upper bound or radius-five trade exclusion.

Offline cold commands and exact costs are in [README.md](README.md) and [VALIDATION.json](VALIDATION.json). The public fixture files are compact; the1.08MB complete mathematical record, all half tables, author traces and operational logs regenerate in scratch and are excluded from publication. SHA values compare whole records; they do not establish the finite reduction or enumeration completeness by themselves.

## Literature, dependencies and limits

Live candidate-specific searches on2026-10-02 covered the parameter, the57-core/84-state description and retained-core trades. Aw, Chee and Ling, *Six New Constant Weight Binary Codes*, Ars Combinatoria67 (2003),313–318, [Theorem1 and AppendixA](https://ymchee66.github.io/home/PDF/6cwc.pdf), already supply lower69. [Brouwer's maintained table](https://aeb.win.tue.nl/codes/Andw.html) still lists69..72; the separately reviewed campaign upper71 is distinct prior work. The [primary literal certificate](https://aeb.win.tue.nl/codes/cwc/d6/a18.6.5.69) is credited and byte-checked. The target's refinement of [prior7540](https://github.com/helgithorskarp/math_results/blob/main/constant_weight_a18_6_5_acl69_trade_barrier/README.md), source0d334e07cfd8161c4ebf0f89cc415143b9b38888, is graph-level progress. Search absence supplies no proof of historical priority.

The involution-family [9047](https://github.com/helgithorskarp/math_results/blob/main/round-two/six-code-2/swapped_pair_five_upper69/PROOF.md), [independent9115](https://github.com/helgithorskarp/math_results/blob/main/round-two/six-reviewer-5/swapped-five-audit/REVIEW.md) and [9135](https://github.com/helgithorskarp/math_results/blob/main/round-two/six-code-2/two_fixed_involution_upper69/PROOF.md) are credited target context, with different hypotheses. This audit neither imports their generic classification nor supplies a blanket verdict on them. Its numerical theorem is self-contained from the literal core, complete physical universe and exact independent finite computation. The original7540 radius-five trade claim is likewise outside the verdict. No solver, floating-point calculation, formal proof assistant or full-code isomorphism quotient is used.

Trust remains in the ordinary core/independent-set/half-table/count/component reductions, literal input decoding, CPython3.11.2 and exact integer/set semantics. The ordinary bridges are unformalized. All mathematical jobs are serial, native numeric threads one, in the unchanged1CPU/2GiB scope. Fixed180-second independent child,45-second fifty-pair chunks,60-second controls and original60-second internal guards are retained. A timeout, kill or incomplete computation would prove no mathematical absence; none is used as an exclusion. The restricted theorem is reproducible and ready for conventional mathematical assessment, with these trust boundaries stated.
