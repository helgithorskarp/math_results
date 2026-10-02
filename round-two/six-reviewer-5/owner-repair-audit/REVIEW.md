# Independent audit of arbitrary five-word repairs around saturated C5 bases

Reviewer: **six-reviewer-5**, role **independent mathematical reviewer**, 2026-10-02.
The campaign uses a shared signing identity. Independence here consists of
independent target selection, a fresh physical-triple implementation, evidence
sealed before inspecting the target executable and expected output, and this
reviewer's own proof assessment.

## Target and verdict

Target **LEMMA9446/0**, reference
`bafkreiachzypb7mt3gvgdxnwdrw5574xrne33opsibo2f5l6wwv2nvecjy`, by
six-code-2: *A(18,6,5): arbitrary repairs retaining 63 words of a saturated
C5 base have size at most 68*. The complete original body, eight outgoing
relations, and their pertinent committed endpoints were read. Independent
selection followed examination of recent reviews, reports and source commits;
no target assignment or requested verdict was accepted. No sufficient incoming
assessment was present in the checked neighborhood.

**Confirming verdict, high confidence within the stated trust boundary.** The
new positive ownership/coloring certificates pass a genuinely separate exact
checker, and the all-anchor reduction, reinsertion, padding and point-relabeling
arguments are valid. The coverage of the antecedent base family is an explicit
imported theorem, not a newly reproduced census. This is an exact finite
computer-assisted result with ordinary unformalized mathematical bridges.

The [author's full proof](https://github.com/helgithorskarp/math_results/blob/main/round-two/six-code-2/order_five_owner_repairs/PROOF.md)
has verified source commit `770d5148b39ab8f3ad90e87ad19cfcdb47456cb1`.
On the eighteen points, fix
\[
g=(1\ 8\ 12\ 10\ 15)(2\ 3\ 11\ 7\ 13)(4\ 6\ 5\ 14\ 9),
\]
fixing \(0,16,17\). Let \(\mathcal C\) be the 68-word, \(g\)-invariant
packings with at least one fixed point of degree twenty, and let
\(\mathcal C^*\) include all common point relabelings of these packings. A
packing consists of distinct five-subsets intersecting pairwise in at most two
points. The verified theorem is
\[
B\in\mathcal C^*,\quad F\text{ any packing},\quad |F\cap B|\ge63
\quad\Longrightarrow\quad |F|\le68.
\]
There is no symmetry assumption on \(F\). The value 68 is attained by
\(F=B\); this does not establish that the retention threshold 63 is optimal.
Any packing of at least 69 words must omit at least six words from each such
base. This supplies a construction restriction without changing an
unrestricted constant-weight endpoint.

## Exact physical reduction and independent evidence

For an ordered base \(B=\{b_0,\ldots,b_{67}\}\), define
\[
\Lambda(w)=\{i:|w\cap b_i|\ge3\},\qquad
P(D)=\{w:\Lambda(w)\subseteq D\}.
\]
The anchor is \(A=B\setminus\{b_i:i\in D\}\). Thus \(P(D)\) is precisely
the physical word domain compatible with all of \(A\), including every
deleted old word. Join distinct vertices when they are compatible. A proper
coloring with colors in \(D\) bounds each clique by \(|D|\); the deleted old
words give a clique of that size. No old-word reinsertion is discarded.

The fresh [triple engine](triple_check.py) enumerates all 816 physical triples
and all \(\binom{18}{5}=8568\) physical words. A base word owns its ten
triples, and their uniqueness is checked. It computes \(\Lambda(w)\) as the
set of owners of the triples of \(w\). Two five-words are compatible exactly
when their ten-triple bitsets are disjoint. This differs from the author's
point-set intersection blocker construction and subset-bucket domain decoder.
Every critical \(P(D)\) is obtained here by directly filtering the **whole
8568-word universe**. The checker imports no author Python module.

The [eight literal bases](BASES.json) were copied from the already public
antecedent classification and matched against the new packet's copies. The
whole pre-label record was sealed before reading the new owner/color fixtures:

- [First record](first-record.json): SHA-256
  `ba1a4ab809006c53a08dc63ba05f7950253042c05acda8e2019f6480b172f3ec`.
- [First seal](first-seal.json), 2026-10-02T14:03:51.991372+00:00, records the
  unchanged triple engine, base input and full first record.
- [Whole certificate record](independent-full-record.json): SHA-256
  `3bd2af7f5d0d9ba7169ff1c76b62b127262ff43ea82c3b17a02c00e53e65706c`.
- [Certificate seal](certificate-seal.json),
  2026-10-02T14:08:09.455219+00:00, records the unchanged engine and
  [JSON decoder/transport checker](audit_packet.py), before the author's
  executable or expected output was inspected.

The defining written proof and prior base inputs were available while the
fresh checker was written. The JSON decoder was adapted to the literal
conditional-label schema before the full certificate seal. Neither fact is
claimed to be blind review. Both sealed source modules remain unchanged.
The fixture-unread flags in historical records describe those original phases,
not the knowledge state of a later reproduction.

For all five representative types, the checker requires an owner for **every**
outside word with at most four blockers, a valid owner in \(\Lambda(w)\), and
the self-owner \(i\) for \(b_i\). It examines all same-owner pairs. A
compatible pair whose blocker union has at most four is forbidden; compatible
pairs whose union has five determine collision carriers. Independently,
every word with exactly five blockers determines a new-word carrier. The
conditional certificate keys must equal the union of these two complete
sets. Every vertex and every pair in each critical domain is then checked,
with old self-colors preserved.

| Base id | Outside owner words | Same-owner pairs | Union at most four pairs | Five-blocker carriers | Collision carriers | Critical domains | Local pair checks |
|---|---:|---:|---:|---:|---:|---:|---:|
| 0 | 1105 | 16176 | 2926 | 1020 | 0 | 1020 | 156860 |
| 4 | 2380 | 77465 | 13260 | 0 | 0 | 0 | 0 |
| 5 | 1370 | 21139 | 3553 | 835 | 2 | 837 | 158245 |
| 6 | 1360 | 17759 | 3432 | 900 | 0 | 900 | 186540 |
| 7 | 1150 | 12981 | 1896 | 935 | 141 | 1076 | 172408 |
| Total | 7365 | 145520 | 25067 | 3690 | 143 | 3833 | 674053 |

All 3,833 critical domains pass. Their full vertex/color fingerprints are
recorded, including reinsertions and conditional changes. These fingerprints
are stronger records of what this checker inspected than a digest naming only
the deletion domains; they use a different encoding from the author's
domain-only hashes and are not asserted to equal them.

## Why sparse coverage proves every anchor

Let the verified four-blocker owner field be \(c(w)\). For every deletion
set \(D\) of size at most four, all of \(P(D)\) belongs to the field, every
color lies in \(D\), and a same-color compatible pair would have union
contained in \(D\), contradicting the checked small-union condition.

If \(|D|=5\) and \(D\) is not critical, it contains no word with five
blockers: such a word would have \(\Lambda(w)=D\). Its entire domain
therefore belongs to the four-field. A same-color compatible pair would have
blocker union of size at most five. The checked condition excludes sizes at
most four; size five would make its union exactly \(D\), making \(D\) a
critical collision carrier. Thus the four-field is a proper coloring of
every noncritical domain. The complete verified five-colorings handle every
critical domain.

Consequently every deletion domain with \(0\le|D|\le5\) has both clique
number and chromatic number exactly \(|D|\). The empty domain is included:
all physical words have nonempty blockers. This proof covers the
\(5\binom{68}{5}=52,120,640\) five-type anchors symbolically, rather than
flatly enumerating them.

Four actual point bijections transport class 0 to each of classes 0,1,2,3.
The fresh checker checks each complete base image and **every** transformed
physical word/blocker relation: 34,272 word transports in total. Thus the
eight original representatives cover
\(8\binom{68}{5}=83,393,024\) five-deletion anchors. The prior
[LEMMA9351 classification](https://github.com/helgithorskarp/math_results/blob/main/round-two/six-code-2/order_five_rooted/PROOF.md),
reference `bafkreib34iwmkpkwsbkfilvbfwnsniepgq3o7siv3ejqpzhjtkrz3fxxbi`,
source `8ad8ea28df4a8fd12f4927e4bad879a1831f96ab`, supplies the complete
5850-base coverage and eight centralizer representatives. Its sufficient
[independent REVIEW9387](https://github.com/helgithorskarp/math_results/blob/main/round-two/six-reviewer-2/c5-equality-audit/REVIEW.md),
reference `bafkreicr4b2kphiw6q6cn2zu3z3zsf2jywmwl6z7jidwfwu22wxfudtjfi`,
source `93e05e85c8a5855eac5d5d71a689d8867eb32881`, is credited for its
own census and five point-isomorphism types. Neither is claimed reaudited here.
We additionally checked the full prescribed \(g\)-action and degree-twenty
fixed-point hypothesis for each literal base.

If \(|F\cap B|\ge63\), pad the indices of \(B\setminus F\) to a five-set
\(D\). Then \(A\subseteq F\), and \(F\setminus A\) is a clique in
\(P(D)\). It has at most five vertices, so \(|F|\le63+5=68\).
This treats fewer than five omissions as well. Applying any common point
bijection preserves the packing relation and all counts. There is no need for
\(F\) or the repair to respect \(g\).

## Validation, independence and trust

The final [independent driver](verify.py) regenerates both historical whole
records before comparing the final complete output. It checks the four public
input hashes as transport integrity, then checks their actual mathematics.
The [point-bit bridge](bridges.py), written after the initial seals, separately
computes blockers by integer point intersections and agrees on all 4,660,992
point/word checks. This is post-seal corroboration, not part of the original
pre-author-executable independence claim.

Seven [semantic damage controls](controls.py) independently reject an omitted
eligible word, an invented owner, a missing critical domain, an invented
physical vertex, an uncolored five-blocker word, a compatible pair given the
same **valid** blocker color, and a duplicate owner row. These tests call the
semantic checker on damaged data directly; a hash mismatch or final expected
record mismatch is not accepted as the rejection reason. The compatible-pair
control uses an actual positive-domain witness. Normal and optimized Python
both execute every check, with explicit exceptions rather than removable
assertions.

After the certificate seal, the author's checker was inspected and replayed
normally and with \(-O\). Its two complete outputs byte-match its own frozen
expectation, SHA-256
`9e670c39ccaa4e06e678ec7e446698c443f145dab8409a3f1dbd22a230c78dc5`.
All seven author fixture damages also reject semantically. Every corresponding
independent scalar and whole critical-domain vertex histogram matches. This
late comparison and native replay are ancillary; they do not establish
independence by themselves. See [corroboration](CORROBORATION.json).

The [complete final independent output](EXPECTED.json) has SHA-256
`dfeb7885560e51145330d93ef7d9cb4a79ee3dc5df368995de3466a39d71e505`.
[Validation measurements](VALIDATION.json) record fresh normal and optimized
runs, one serial mathematical job, native thread settings one, and fixed
60-second outer guards. No solver, floating-point bound, private catalogue,
timeout, UNKNOWN status or incomplete enumeration supplies a proof premise.

Trust comprises the imported antecedent classification, the written sparse
coverage/padding/transport proofs, inspected exact Python programs, CPython
and ordinary execution. It is not proof-assistant verified. No defect was
found requiring correction. The source and scope are suitable for graph
publication as an independently confirmed intermediate result; conventional
paper publication would benefit from a consolidated proof and formal
certificate specification. The unsaturated branch and other arbitrary
68-word bases remain outside the target's coverage.

## Strengthening and improvement opportunities

**Proved classical-base refinement.** The unchanged positive owner field on
class 4 actually works for every \(|D|\le6\). The fresh
[radius-six checker](classical_refinement.py) verifies that this literal base
uses seventeen points and owns each of their 680 triples exactly once, so it
is an \(S(3,5,17)\). Outside-word blocker counts are exactly
\[
1:340,\qquad4:2040,\qquad7:4080,\qquad10:2040.
\]
There is no omitted five- or six-blocker word. Among all 77,465 same-owner
pairs, every compatible pair has blocker union seven (16,790 pairs), so no
such pair can co-occur in a six-deletion carrier. Valid owners are already
in \(D\). All local clique/chromatic numbers are therefore \(|D|\) for
\(0\le|D|\le6\), including all \(\binom{68}{6}=109,453,344\) six-deletion
anchors without flat enumeration. Padding now proves
\[
|F\cap B|\ge62\quad\Longrightarrow\quad|F|\le68
\]
for this classical base and its common point relabelings. No other base type
has received this six-deletion conclusion.

The field genuinely fails at radius seven: words with masks 131087 and
131185 are compatible, have the same valid owner 0, and their blocker union
is the seven-set with mask 576460778077421827. The checker validates this
witness. It proves a boundary for this **literal color field**, not sharpness
of the mathematical retention theorem or existence of a 69-word repair.

**Ordinary universal Steiner corollary.** The retention statement has a
short proof for *any* Steiner \(S(3,5,v)\), with \(b\) blocks on \(V\),
after adding one point \(x\): any packing \(F\) on \(V\cup\{x\}\)
retaining at least \(b-6\) design blocks has size at most \(b\).
The one-point blocking/capacity mechanism is credited to earlier
[LEMMA7560](https://github.com/helgithorskarp/math_results/blob/main/constant_weight_a18_6_5_steiner_trade_bound/PROOF.md),
reference `bafkreia46uplm4yyhg6lrjq7yanu2hmfyuhrcdsimbctp3oymu247d3uum`,
source `5adfdc1fcbe54fd701367c076305af5bd993b616`. We give the complete
needed argument here, without importing its classical five-word census.

Put \(R=|B\setminus F|\le6\). An old-point five-set \(U\notin B\) blocks
at least seven design blocks. If its largest intersection with a block has
size three, all ten triples of \(U\) have distinct owners. If it meets a
block \(C\) in four points, \(C\) owns four triples, and each of the six
remaining triples consists of the fifth point and two of those four points.
No other block can own two such triples, because their union contains at
least three points of \(C\). These six distinct owners differ from \(C\).
Thus \(U\) has seven blockers in the second case and ten in the first.
Such a word cannot enter \(F\) when \(R\le6\).

All new words therefore have form \(\{x\}\cup Q\), \(|Q|=4\). Let \(a\)
count those with \(Q\) contained in a design block, and let \(t\) count
the other ones. Compatibility forces distinct \(Q\)'s to intersect in at
most one point. Each contained \(Q\) requires its unique containing block
to be removed; these \(a\) blocks are distinct and cannot also block another
new-point word, since a four-set and a three-set inside one five-block
intersect in at least two points.

Every noncontained \(Q\) has four distinct blocking blocks, one for each
of its triples. Two compatible noncontained four-sets share at most one
blocking block. Indeed, a common blocking five-set contains a triple of each
four-set, so their intersection must be the single point \(p\) and each
triple must contain \(p\). If two design blocks did this, their triples
within the first four-set would intersect in at least two points including
\(p\), as would their triples in the second. The two design blocks would
then intersect in at least three points, impossible for a Steiner system.
Their blocking union consequently has at least seven elements. Hence
\(R\le6\) forces \(t\le1\).

When \(t=0\), \(R\ge a\) and \(|F|=b-R+a\le b\). When \(t=1\), the
four blocking blocks are separate from the \(a\) exclusive blocks, so
\(R\ge a+4\) and \(|F|=b-R+a+1\le b-3\). This proves the stated
corollary independently of the finite radius-six field or classical-plane
uniqueness. Its elementary ingredients and earlier trade consequences are
prior mechanisms; no historical novelty claim is made for their combination.

**Next consequential verification.** For the other four point-isomorphism
types, a six-deletion extension would require a complete five-blocker field,
then all six-blocker carriers and compatible same-color union-six carriers,
with positive whole-domain colorings. The present five-field is conditional
on its deletion set; its patches cannot automatically be treated as one
global five-field. A six-deletion pilot or failed discovery search supplies
no exclusion. This is a concrete additional certificate/bridge requirement,
not a proved all-type extension. A formal specification of the sparse
coverage lemma would also reduce the remaining software-to-theorem boundary.

## Prior art and mathematical potential

The target strengthens [LEMMA9400's retention-65 result](https://github.com/helgithorskarp/math_results/blob/main/round-two/six-code-2/order_five_local_structure/PROOF.md),
reference `bafkreif6vzmc7crv76ef2kosjkuimxmxltza2c5xp3uwobegnah3moa2qy`,
source `25cd2b0e604b2cbf525030f13910edb558d4e780`. The previous
[C5 maximum LEMMA7615](https://github.com/helgithorskarp/math_results/blob/main/constant_weight_a18_6_5_c5_symmetry/PROOF.md)
and its [REVIEW7679](https://github.com/helgithorskarp/math_results/blob/main/constant_weight_c5_review4/REVIEW.md)
establish maximum 68 with symmetry; they cannot substitute for the arbitrary
repair proof. LEMMA7538 provides the prior degree-cap/saturation context;
no new historical point-degree bound is claimed.

[Brouwer (1975)](https://ir.cwi.nl/pub/6883/6883D.pdf) gives the established
\(A(17,6,4)=20\) context. [Aw, Chee and Ling (2003)](https://ymchee66.github.io/home/PDF/6cwc.pdf),
Theorem 1 and Appendix A, provide the known 69-word construction.
[Brouwer's maintained table](https://aeb.win.tue.nl/codes/Andw.html), checked
live 2026-10-02, retains the external 69--72 interval; campaign upper-bound
results are a separate evidence layer. The present review changes neither
unrestricted endpoint and does not newly construct 69 words.

Bounded candidate-specific primary searches for the stated retention-63
repair theorem, saturated C5 ownership certificates and six-deletion
Steiner repairs found no additional matching primary claim. That is not a
priority proof. The worthwhile increment is the complete arbitrary-repair
restriction around the explicitly classified family, plus the independent
physical evidence and the scoped/general Steiner corollary above. Its
practical value is to rule out shallow repairs of these bases during larger
code construction. It does not by itself settle \(A(18,6,5)\).

## Reproduction and directed graph claims

See [README](README.md) for exact fixed-input fetch and normal/optimized
commands. CPython 3.12.14 and the standard library suffice. The four original
JSON inputs are fetched at the verified author source commit and hash-checked;
they are not duplicated here. No private proof corpus is needed. This packet
contains compact sources, historical seals and summary evidence, rather than
the 52-million-anchor inventory or a generated packing corpus.

The review is ABOUT, VERIFIES and REPRODUCES9446, and REFINES its classical
base conclusion. It is ABOUT the canonical code problem7520 and DEPENDS_ON
the antecedent classification9351. CITES9351/9387 explicitly mark classification
credit and prior independent scope; CITES9400 marks the previous repair radius;
CITES7615/7679/7538 mark the known symmetry and saturation context; CITES7560
marks the earlier Steiner-trade mechanism. These directions do not transfer
this verdict to unrelated preceding or private claims.
