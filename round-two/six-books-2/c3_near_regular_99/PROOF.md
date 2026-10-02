# A balanced near-regular C3 construction obstruction at99 edges

Actual author **six-books-2**, role **researcher**, 2026-10-02. The campaign
shares one signing identity. This is an author-checked computational theorem,
with different algorithms by the same author. The ordinary mathematical
reductions, relabeling, finite completeness and implementation bridges below
are unformalized. Independent peer review of this result is pending.

**Theorem.** There is no simple graph G on22 vertices with red degree multiset
**8^3,9^16,10^3**, an automorphism of cycle type **3^7 1**, at most three
common red neighbors on every red edge, and at most six common blue neighbors
on every blue pair.

A blue pair is a nonedge of G. These are ordinary, noninduced books; page-to-page
colors are irrelevant. The degree multiset gives99 red edges. No Kneser seed,
edit budget, prescribed local neighborhood, inherited global degree theorem
or preceding nine-regular exclusion is a hypothesis. Other degree profiles,
cycle types, the full99-edge/C3 frontier and the Ramsey endpoint remain open.

**A stronger ordinary local lemma used below.** In any graph22 satisfying the
same ordinary book caps and having99 red edges, a degree-nine vertex cannot
have red-neighbor degree multiset **8^3,9^6**. This lemma has no symmetry
condition and imposes no degree restriction on the twelve blue neighbors.

## 1. Root counting and all four placements

Write the automorphism as seven oriented triples and one fixed point x.
Degrees are constant on each triple. Their multiplicities modulo3 show that
the fixed point has degree9: the degree-eight and degree-ten multiplicities
are divisible by3, whereas the degree-nine multiplicity is1 modulo3.
Each exceptional degree occupies precisely one free triple.

Let A=N_R(x), B=N_B(x), H=G[A], K=G[B]. Their orders are9 and12.
Every local H degree h_a is at most3, because it is the red page count on xa.
For a blue xb spine its blue pages are11-d_K(b), so every K degree is at
least5. The H edge orbits have size3. Consequently

```text
e(H)<=12, e(K)>=30,
D_A=sum_(a in A) d_G(a)=99+e(H)-e(K)<=81.
```

The identity counts the root edges, H edges, cross edges and K edges; it
holds before any search. There are exactly four placements of the two
exceptional triples:

|Placement|Degree-eight triple|Degree-ten triple|A degree sum|
|---|---|---|---:|
|AA|A|A|81|
|AB|B|A|84|
|BA|A|B|78|
|BB|B|B|81|

AB contradicts the displayed cut. Section2 excludes BA with the stronger
ordinary lemma. In both AA and BB, D_A=81 forces e(H)=12, e(K)=30,
cross cut48 and every K degree5. The three H orbit degrees are2,3,3:
their sum is8, each is an integer at most3, and the only such triple is2,3,3.

## 2. A nonsymmetric degree-nine neighborhood obstruction

Here require only99 edges, d(x)=9 and neighbor degrees8^3,9^6, without an
automorphism. Put h=e(H), L=sum h_a over the three global degree-eight
neighbors, and C=sum_a binomial(h_a,2). The root caps give h_a<=3 and L<=9.
Counting A degrees now gives cut c=69-2h and e(K)=21+h. The blue root cap
gives e(K)>=30, hence9<=h<=13, including all integer possibilities.

For each pair a,a' in A let c_H be its common red count inside H, s_a its
red cross-row rank, and t_(a,a') its red cross-row intersection. The pair
cap is

```text
t_(a,a') <= lambda_(a,a'),
lambda=2-c_H on red pairs,
lambda=d_G(a)+d_G(a')-15-c_H on blue pairs.
```

On a red pair the root is one common red page. On a blue pair use the exact
22-point identity c_B=20-d_G(a)-d_G(a')+c_R and again c_R=1+c_H+t.
Summing the36 capacities, the baseline sum of d(a)+d(a')-15 is
8*78-15*36=84. Replacing the baseline on red edges subtracts
sum_a h_a*d(a)-17h=(18h-L)-17h=h-L. The sum of the c_H terms is C.
Thus

```text
sum lambda =84-h+L-C <=120-5h.
```

The last inequality uses L<=9 and C>=4h-27. To prove the latter, sum
binomial(j,2)>=2j-3 over the nine nonnegative integer local degrees j;
the difference is(j-2)(j-3)/2, nonnegative at every integer j>=0.

On the other hand, if k_b counts a B column's red neighbors in A, then
sum t=sum_b binomial(k_b,2), and sum_b k_b=c. Balancing twelve integer
loads minimizes this convex sum: for c=12q+r it is at least
F(c)=12*binomial(q,2)+r*q. This follows by moving one unit from any load
at least two larger than another. All five cases contradict the upper bound:

|h|c|sum lambda at most|F(c) at least|gap|
|---:|---:|---:|---:|---:|
|9|51|75|84|9|
|10|49|70|76|6|
|11|47|65|69|4|
|12|45|60|63|3|
|13|43|55|57|2|

[analytic.py](analytic.py) checks all five scalar cases and matches the
balancing formula against a distinct twelve-column load DP at all109 totals
0..108. The written ordinary bridge establishes the lemma, not the scalar
check alone. BA in the main theorem has exactly the forbidden A degree
multiset and is therefore absent.

The same local obstruction holds for **at most99** red edges. Now
e(K)=e(G)+h-78<=21+h, so e(K)>=30 still implies h>=9. The cross cut,
pair-capacity bounds and upper h<=13 are unchanged. The identical five
contradictions apply. The scalar fixture records the E99 case; this
edge-inequality corollary is a further ordinary counting implication,
without a symmetry or outside-degree assumption.

## 3. Complete marked A templates

For the remaining AA/BB cases label A as0..8 in three oriented triples,
B as9..20 in four, and x=21. A local word has12 bits: the three internal
triangle orbits, followed by the three matching shifts for each A-triple
pair in order01,02,12. Precisely four bits are red because e(H)=12.
There are binomial(12,4)=495 words, with no hidden local-graph hypothesis.

AA fixes the GLOBAL orbit degrees as8,9,10. BB has all A degrees9. Define
s_a=d_G(a)-1-h_a. The pair capacities are exactly those in Section2.
A necessary lower bound on a row intersection is max(0,s_a+s_a'-12).
For every subset T of A of size3..9 also require

```text
sum_(pairs in T) lambda >= F(sum_(a in T) s_a).
```

The same double count and balancing argument applies to the twelve column
loads restricted to T. These are necessary filters, with no claim that the
survivors are whole-host graphs.

|Case|495 edge words|local degree words|pair words|subset words|representatives|
|---|---:|---:|---:|---:|---|
|AA|495|174|169|18|579,1545|
|BB|495|174|174|108|78,92,624|

The declared relabeling group permits independent phase shifts of each A
triple, A-triple permutations preserving GLOBAL degree marks, and the common
multiplier1 or2 on every triple. In AA the global marks are distinct, so
there is no nonidentity A-triple permutation; the two group sizes are9,9.
In BB all six A permutations are allowed; the group sizes are27,54,27.
These are classes under this declared action, not full graph isomorphism
classes. Inverting A extends to inverting ALL four B triples too; inverting
only selected triples is not asserted to preserve the C3 generator.

[projection.py](projection.py) minimizes each surviving word over this action.
[projection_audit.py](projection_audit.py) instead decodes all4096 words by
literal vertex sets, evaluates blue bounds directly, uses a finite load DP,
and expands every reported representative. It compares the entire survivor
sets, transport groups and typed semantic fields, rather than counts alone.
No orbit of the local degree-two triple is silently identified with a
different global mark.

## 4. All A--B incidences, with the exceptional marks retained

One B triple is encoded by its first red A column mask m. Its other columns
are the two translates rho(m),rho^2(m). Rotating that B triple permits
normalizing m to the minimum of these three masks. The complete column-type
counts for ranks3,4,5 are30,42,42. For rank3 the three full-A-triple masks
are fixed by rho and are each retained once, still producing three distinct
B vertices with identical columns. The other81 rank-three masks give27
three-element mask orbits. Ranks4 and5 each have126 masks in42 orbits.

AA has every B global degree9 and K degree5, hence all columns have rank4.
All four B triples may be permuted, so all148,995 four-multisets of42 types
are covered per representative. A row has its exact rank s_a, and every
intersection satisfies its actual marked pair capacity. The results are

|AA H|complete multisets|margin matches|incidence frames|
|---:|---:|---:|---:|
|579|148995|6062|11|
|1545|148995|6062|19|

[incidences_aa.py](incidences_aa.py) enumerates the multisets. The different
[audit_aa.py](audit_aa.py) joins two ordered halves using independently
generated column sets and matches the entire incidence set and all input
fields. The resulting30 native frames have SHA256
`4308c4cfcff5fc934baa9447435f11a1db5e34307ad2643e9708df2fd46e717f`.

BB marks B orbit degrees8,9,9,10, so its column ranks are3,4,4,5.
Only the two degree-nine B triples may be interchanged. An extra structural
equality makes this branch smaller: H degree multiset2^3,3^6 gives
sum c_H=21 and sum lambda=3*36-12-21=75. Its B columns have total overlap
3*(binomial(3,2)+2*binomial(4,2)+binomial(5,2))=75. Therefore EVERY A pair
capacity is tight. Equivalently, with incidence matrix X and H adjacency,

```text
X X^T =5I+3J-H-H^2.
```

The enumeration imposes the equality entrywise; it does not rely on a
floating-point PSD test or the exploratory Gram probe.

|BB H|complete choices|margin matches|tight incidence frames|
|---:|---:|---:|---:|
|78|1137780|81387|0|
|92|1137780|81387|10|
|624|1137780|81387|18|

Each domain is30*binomial(43,2)*42=1,137,780 choices. The nested producer
[incidences_bb.py](incidences_bb.py) checks these complete domains.
[audit_bb.py](audit_bb.py) independently builds the903 middle rank-four
pairs, keys their entire weight/intersection vectors, then joins all1260
ordered rank-three/rank-five pairs against the exact residual vector. It
matches every typed column and incidence field and the entire native input.
The28 BB frames have SHA256
`7562d5767b72307c509f178d8f9f1ccd3976ce9650bc49efbb7dd25e5347c1d8`.

All these normalizations transport every other incidence and the unknown
K graph. Inverting all triples is valid for the common generator; independent
B phases commute with it. K is subsequently enumerated completely under
the transported labels and preserved degree marks. These arguments show
every hypothetical valid host maps to a listed frame; they do not assume
a unique host automorphism group or count unmarked isomorphism classes.

## 5. Re-derived K screens and whole-host completion

K has22 edge-orbit bits: four internal triangles and three matching shifts
for each of its six triple pairs. Every K vertex has degree5. If a B column
has rank s_b, two B columns have at least max(0,9-s_b-s_c) common blue
A points. The root x is a further common blue page. Thus, on a blue K pair,

```text
common blue inside K <=5-max(0,9-s_b-s_c).
```

The red local K cap is at most3. In AA all ranks4 give blue cap4. In BB
the ranks3,4,4,5 give different pair caps, including possible cap5. The
AA uniform cap4 pool is NOT silently reused for BB.

[block.py](block.py) enumerates all16 internal triangle flags and4^6
cross-mask weight patterns:65,536 weight frames,116 degree-compatible,
and16,536 actual five-regular words. Expanding every mask of each weight
and applying the necessary K screens yields15,768 AA candidates and12,690
BB candidates. The independent native [direct.cpp](direct.cpp) enumerates
ALL4,194,304 words separately for each mode and obtains the same entire
sorted candidate streams. A matching digest alone is not the comparison.

For every incidence frame and candidate K word, the component method counts
pages on B--B and A--B spines, adding the assigned A and root contributions.
The earlier filters already check root and A--A spines. The native method
instead rebuilds the WHOLE22-point adjacency matrix, checks every actual
degree and99 edges, then applies the literal colored page predicate to the
whole graph. It may stop at the first bad spine; no claim is made that all231
spines were evaluated for every rejected host. Both methods compare one
outcome byte for every completion choice, in the same frame/K order.

|Case|incidence frames|K candidates|completion choices|valid|
|---|---:|---:|---:|---:|
|AA|30|15768|473040|0|
|BB|28|12690|355320|0|
|Total|58|case-dependent|828360|0|

K stream hashes are
AA `b55ea7aec99edb7b23aeb97d7883d038f633d31f3ac20a42a53f4746d8e9fce6`
and BB `16d4a12d9185a9ca40ef44a7abb8eba6189f27110820feb48ea0778cc214ac6d`.
Outcome hashes are
AA `95221b8d1e0a1014d2a6a9d77eee0c514e2c46c920ab699c700723da0d7b4550`
and BB `1b6b8bcb434382ed013b68aece3341aaab52e323e42b8e8d923b93f4f07ac4e0`.
These are counts of normalized templates and completion choices, not
distinct graphs or full isomorphism classes. Complete AA/BB negative outputs,
AB's cut contradiction and BA's ordinary lemma prove the stated theorem.

## 6. Reproduction, prior art and trust

[README.md](README.md) gives serial cold commands. [reproduce.py](reproduce.py)
regenerates all sources' data from definitions, checks the primary21 fixture,
compares the whole streams and all frozen mathematical fields, then matches
the compact [EXPECTED.json](EXPECTED.json). The fixture was frozen before
the normal and optimized cold replays. Large inventories, binaries and logs
are regenerated into scratch and are not publication inputs.

[validate.py](validate.py) repeats both ENTIRE native finite censuses with
AddressSanitizer/UndefinedBehaviorSanitizer, compares all semantic fields and
both entire streams per mode, checks targeted frame/projection/incidence/
frozen schema damages, and compares literal set, bitset and component page
counts on all14,784 spines of64 varied C3 graphs. Actual complete run
measurements and rejections are in [evidence.json](evidence.json).
All jobs are serial, six numerical thread variables are1, the process
scope is unchanged1CPU/2GiB, program guards25 seconds and child guards30.
The first cold-wrapper attempt had a Path/string error before any mathematical
phase; it was corrected before the completed cold replay. No mathematical
guard, solver UNKNOWN, timeout or killed computation supplies an exclusion.

The primary [Table1](https://arxiv.org/pdf/2407.07285) was live reopened
2026-10-02 and retains22<=R(B4,B7)<=23. The normalized462-byte
[primary21.rows](primary21.rows) has offdiagonal1 RED; the primary repository's
[raw matrix](https://raw.githubusercontent.com/gwen-mckinley/ramsey-books-wheels/main/tabu/constructions/R_B4_B7_construction_21vertices.txt)
has1 BLUE and is complemented offdiagonal. The raw SHA256 is
`3b648b66a5990d0b6ed945ce80d3f546e90f2b233f924775bb02ac2418558a55`.
The cold baseline is exactly93 red edges, page maxima3/6. Its reproduction
is validation, not a new construction. The upper23 flag certificate is
not independently replayed and no exclusive historical priority is claimed.

The public [preceding nine-regular C3 proof](https://github.com/helgithorskarp/math_results/blob/main/round-two/six-books-2/c3_regular_nine_99/PROOF.md),
commit86ab673e6bda70f9bf7d84241c7459e7e6542898, LEMMA9453/0
`bafkreibtcvois3v6qlqth5kw3szy5e65rmopbqxrf5qwcuf6rzyarqetje`, supplies
credited root/subset/phase-incidence and component/native implementation
patterns. Its theorem is not used as a premise. Here the marked AA local
degree-two triple is not fixed by an unrelated mark; BB uses full allowed
A permutations, with92 and624 replacing the previous local-degree-normalized
representatives540 and1616. All changed domains and screens are regenerated.
The earlier8971 root/subset frontier and9392 monotone Kneser boundary lane
are complementary prior art, not theorem premises or transferred verdicts.

The new independent [review9490](https://github.com/helgithorskarp/math_results/blob/main/round-two/six-reviewer-4/regular-nine-audit/REVIEW.md),
source7501f4428ff84a1d58059e532675f5ef5765ddfe,
`bafkreiewraqzrrueihg6dol3ol3ixszbr62rg7bzhvv5mato5r3pgrv3na`, confirms
the preceding9453 regular symmetry exclusion and proves additional
symmetry-free regular page-deficit structure. Its entire signed body and
directions were read before this publication. Those regular matrix/spectral
identities and that verdict do not transfer to the present degree marks;
its executable was not replayed here and its theorem is not a premise.

The complementary [Books1 leaf result9461](https://raw.githubusercontent.com/helgithorskarp/math_results/main/round-two/six-books-1/cross_tagged_leaf/PROOF.md),
sourcee42f7fc4e4a88b2864e73ffa8072178704ff7957,
`bafkreih55sxvuoxd4vbcmgtkquhftlvqysgg3lzdllvobcid2md5ize6ry`, excludes a
specified leaf in the explicit9^4,10^18 model. Its signed committed body
was read as a distinct cohort; its executable was not replayed and its
verdict does not transfer here. Nearby rootless9371 and independent9414
results likewise impose other hypotheses and are not imported.

Correct ordinary bridges, complete declared actions and finite generators,
exact CPython/C++ arithmetic and source-to-statement correspondence remain
trust inputs. These sources and sanitizer/whole-set comparisons make the
calculation reproducible; they do not formalize it or supply independent
peer review. The main Ramsey question remains open.
