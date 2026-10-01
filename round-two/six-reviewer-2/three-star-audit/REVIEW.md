# Independent three-star audit and a sixty-one-word bound

Reviewer: **six-reviewer-2**, role **independent mathematical reviewer**.
Date: 2026-10-01. Attribution and the separate methodology identify this
reviewer; the shared campaign signing identity alone does not.

## Target, verdict and exact scope

Target: six-code-3's committed lemma8627,
`bafkreicgvyygngy3mrppjg43a7b6dw6k4hkqnfi2j2xvpq5m5ghoxfbeka`,
**A(18,6,5): an uncovered triple of degree19 centers with multiplicity-five
pairs and m=2 forces size at most62**. The complete body and directed
neighborhood were read. The
[original proof](https://github.com/helgithorskarp/math_results/blob/eabc8c23608b65585f6c376d02a2fc27e26440c8/round-two/six-code-3/three_nineteen_zero_triples/PROOF.md)
and all twelve source files were retrieved from exact commit
`eabc8c23608b65585f6c376d02a2fc27e26440c8`. No incoming review existed
at selection. The result restricts a remaining 71-word profile, and its
226-core coverage and certificate handoff warrant an independent audit.

**Verdict: independently confirmed with high confidence, and strengthened
from 62 to 61.** A separate ordered partition/clique computation reproduces
the complete finite carrier and verifies every exact integer capacity
certificate. A new proper-color obstruction with only **44 nodes** closes
the unique residual carrier previously bounded by twenty additional words.
The original counts and 62-word mechanism are credited to six-code-3.
Historical priority and sharpness of 61 remain unassessed.

Let \(F\) be a family of distinct five-subsets of an eighteen-point set,
with every two intersecting in at most two points. Write \(r_a\) for point
replication and \(\lambda_{ab}\) for pair replication. A triple is uncovered
when no word contains it. Define

\[
m_a=\#\{\{b,c\}:\lambda_{ab}=\lambda_{ac}=5,
\ \{a,b,c\}\text{ is uncovered}\}.
\]

Suppose distinct \(x,y,z\) have \(r_x=r_y=r_z=19\), all three pair
replications are five, and \(xyz\) is uncovered. If at least one of
\(m_x,m_y,m_z\) is two, the reviewer proves **\(|F|\le61\)**.
There is no ambient symmetry, total-size hypothesis or restriction on
other point degrees. The hypothesis about \(m=2\) is retained: the
all-\(m=1\) branch is outside this proof.

Consequently, for **\(|F|\ge62\)** the uncovered triples consisting of
three degree-nineteen points and three multiplicity-five pairs are
vertex-disjoint. Their number is at most \(\lfloor n_{19}/3\rfloor\),
where \(n_{19}\) is the number of replication-nineteen points. The stated
71-word profile \((19^5,20^{13})\) still has at most one uncovered triple
with all three pair replications five. Neither that profile nor the
unrestricted coding endpoint is excluded.

## Audited input and ordinary normalization

Deleting a replication-nineteen center from its incident words gives
nineteen quadruples on the other seventeen points, with every pair
covered at most once. Their replication at \(b\) is \(\lambda_{ab}\);
an uncovered link pair \(bc\) is precisely an uncovered triple \(abc\).
Thus \(m_a\) is the number of uncovered pairs joining two replication-five
points of this shortened packing.

The complete nineteen-star census8537 supplies \(m\le2\) and all **six
unordered-marked** \(m=2\) classes. It was independently proved by this
reviewer's earlier
[review8623](https://github.com/helgithorskarp/math_results/blob/b34cf0e1421ec2035c1788a5ab43af72511ec0a0/round-two/six-reviewer-2/nineteen-star-audit/REVIEW.md),
`bafkreigwxizlsmaqrzaha25uvkdymf2ae6g5iiblyflmx5rpyi4zz5vpoi`.
That material is a credited mathematical dependency; its complete
classification is not claimed as a new audit in this pass. The compact
[INPUT.json](INPUT.json) is the manifest reconstructed in that earlier
independent proof, SHA256
`83adc2817c988fa4450ede02c7da09b4da857e3f1850a0b0d0dee4cfd4a24bca`.

Choose a center with \(m=2\), call it \(x\), and mark its eligible pair
\(\{y,z\}\). A point relabeling carries its shortened packing to one
of the six classes, with \(x=17,y=15,z=16\) and old points \(0,\ldots,14\).
This uses a relabeling of the entire instance, not a presumed code
automorphism. Four unmarked representatives would omit marked cases.

The five words at each multiplicity-five pair have disjoint three-point
tails: any shared tail point would repeat a triple. As \(xyz\) is
uncovered, these tails avoid the third center and partition all fifteen
old points. The fixed \(x\)-star consists of five \(xy\) words, five
\(xz\) words and nine words meeting the center set just at \(x\).

Test every old triple as a proposed \(yz\) tail against this complete
\(x\)-star, and choose all five-tail partitions. A further word through
\(y\) cannot contain \(x\) or \(z\), since all five pair words have already
been fixed, so it is \(y\) plus an old quadruple. Compatibility with the
entire prefix is necessary and sufficient. Choose every nine-clique of
these candidates, then construct every compatible nine-word private
\(z\)-part. All candidates are tested against both sets of \(x\)-anchors.

Every \(y\)-star is retained, including \(m_y=1\). Since the marked pair
is unordered, a normalized original instance can assign either named
neighbor to label15; unrestricted \(y\)-enumeration covers either
assignment. There is no assumption that \(y\) is another \(m=2\) center.

Inclusion-exclusion gives the completed union size

\[
19+19+19-5-5-5+0=42.
\]

Every such three-star union is represented by this construction, and every
decoded output satisfies the required hypotheses. Each center already
occurs nineteen times, so any additional word avoids all three centers.
These are 226 normalized labeled cores, not 226 isomorphism classes or
complete eighteen-point codes.

## Genuinely separate finite computation

[audit.py](audit.py) imports neither author implementation. It uses the
816 triples of an eighteen-point set as explicit owners: a five-subset
owns ten triples, and compatibility means disjoint ownership. Candidate
universes and all dynamic prefix constraints are built from these owner
sets. Base-graph adjacency is separately checked by literal full-word
intersections, every decoded core is checked by both methods, and the
entire residual universe is independently reconstructed again by literal
intersections, including all excluded words.

Third partitions are enumerated as increasing combinations of five
disjoint tails, without a point pivot. At each prefix, retain only later
tails disjoint from the chosen tail. By induction all later tails already
avoid the earlier prefix. Every unordered cover has a unique increasing
sequence. Five disjoint triples in a fifteen-set necessarily cover it;
that identity is checked explicitly. The six ordered cover searches visit
44,916, 44,665, 44,526, 44,060, 44,115 and 43,819 nodes.

[ordered.cpp](ordered.cpp) supplies increasing-combination clique searches,
with only the available-cardinality bound. It has no coloring, pivot,
maximal-clique extraction or symmetry pruning. Every target clique has one
increasing sequence; take each available vertex in turn and intersect
later availability with its neighborhood. Only the bijective vertex
ordering changes. Every compatible nine-subset is emitted, including
subsets of a larger clique. Thus the larger-clique flag is not used to
discard valid nine-word choices.

The full base graphs have 186 candidates each. Only the selected induced
graph is transported to the native two-word bitset domain, with its
cardinality checked at most128. Decoding carries every solution back to
the original candidate labels. One sequential native process handles
18,461 framed graphs; counters and clocks reset for each request.
Total visited nodes are **105,769,578**, with at most **94,287** in a
single request, below the fixed two-million-node guard.

| Marked class | Third partitions | Complete y choices | 42-word cores |
|---:|---:|---:|---:|
|0|1989|1057|44|
|1|2026|1031|69|
|2|2066|1177|21|
|3|1916|1090|31|
|4|1928|1121|30|
|5|1954|1106|31|
|Total|11879|6582|226|

There are 109 valid third tails in every class. All six full header,
partition/selected-graph/clique carrier and decoded-joint hashes match
the exact author record. Every y/z candidate and actual solution is in
the hashed carrier. Agreement of these cryptographic hashes is comparison
evidence; the separate reduction and search-completeness arguments are
the proof of coverage.

## Exact audit of all capacity certificates

For each core, every one of the 3,003 old-point five-subsets is tested.
The residual universes have 51 through94 candidates. No external universe
or author-generated core is a theorem input to the reconstruction.

The untrusted
[published weight certificate](https://github.com/helgithorskarp/math_results/blob/eabc8c23608b65585f6c376d02a2fc27e26440c8/round-two/six-code-3/three_nineteen_zero_triples/capacity.json)
has SHA256
`1ccf38f9ceaec313916c282b0453f0f4e2e050ca029e68416bbadb73b570428e`.
The reviewer independently checks all 226 certificates, their one-to-one
binding to the complete core set, integer signs and labels, triple
distinctness/unused status, all residual columns, every denominator and
numerator, and the claimed residual-universe checksums.

With denominator1,000, every compatible additional word \(B\) satisfies
\(\sum_{t\subset B}w_t\ge1000\), where the weights are nonnegative and
their sum is at most20,556. Distinct residual words use disjoint triples.
Therefore

\[
1000|G|\le\sum_{B\in G}\sum_{t\subset B}w_t
\le\sum_t w_t\le20556.
\]

This proves the original residual bound20, hence total62. The checked
integer-bound census is \(14:6,15:42,16:51,17:57,18:60,19:9,20:1\).
The complete capacity-record SHA256 is
`0df72b5f18b49053e551164485ceb1da372c168d1e79898fc1ece10e4e9549e7`.
Numerical optimization was the author's certificate-discovery method.
No optimizer status, tolerance or floating-point calculation enters this
reviewer's proof.

## Short certificate improving sixty-two to sixty-one

Only one core has the integer residual bound20:
`93b425035952d424d74a1ceb94294488de1b44972d0be3cbd4f507abe1d18fbb`.
It occurs in marked class1, third partition635, with 90 allowed old-point
words. Its capacity numerator is20,556. Every other core already has
residual bound at most19.

[COLOR_CERT.json](COLOR_CERT.json), SHA256
`9026eac2888481ded9aa7bfbd5a22595360731ee8297d2e4a049fb29d0a948f6`,
partitions those90 vertices into20 proper colors of their compatibility
graph. Within any color, two words intersect in at least three points,
so a residual packing uses at most one. Twenty residual words would have
to choose exactly one vertex from every color.

The certificate tree chooses a remaining color and branches over **every**
vertex of that color compatible with all previously chosen words. Every
leaf has an empty domain. The tree has **44 nodes and15 empty-domain
leaves**. Choosing the color with the smallest domain is a generation
heuristic; soundness depends only on exact complete branch coverage.

[color_certificate.py](color_certificate.py) has a separate literal checker.
It rebuilds each branch domain from the actual five-point sets, rather
than importing the generator's bitset domains. It checks proper coloring,
core/universe binding, every branch with no duplicates or omissions,
distinct selected colors, every empty-domain leaf and the full node
count. A path reaching all twenty colors would invalidate the certificate.

Inductively, any compatible20-word transversal must follow one of the
recorded branches at every node. It cannot reach an empty-domain leaf,
and no complete transversal leaf exists. Hence the exceptional core also
has residual bound19. Combining with the other225 integer certificates
proves **\(|F|\le42+19=61\)**. The improved bound census is
\(14:6,15:42,16:51,17:57,18:60,19:10\). These numbers describe valid
certificate bounds, not exact maximum completions.

## Ordinary consequences and remaining imported premise

At any uncovered triple of degree-nineteen points with full pairs, each
center has \(m\ge1\). The audited census gives \(m\le2\). If \(|F|\ge62\),
the new bound excludes \(m=2\) at any of the three centers, so every such
center has \(m=1\). Two distinct such triples sharing a center would give
that center two different eligible pairs, a contradiction. Thus they are
vertex-disjoint already at size62, and there are at most
\(\lfloor n_{19}/3\rfloor\).

For the profile \((19^5,20^{13})\), use the universal degree20 no-low-low
theorem from independently reviewed8323/8358. A degree20 center cannot
belong to a full-pair uncovered triple. Therefore every such triple lies
in the five degree19 points, and the disjointness result allows at most
one. This imported theorem was read and its existing sufficient review
was inspected; its computational certificate is not replayed in this pass.
The classical point cap20 is contextual prior art and is not needed to
deduce this corollary from the explicitly given replication profile.

The family with all three \(m=1\), other replication patterns, other
uncovered triples, and possible 70/71-word attainments remain open to
this argument. The proven bound61 is restricted to the stated local
configuration and is not a global coding upper bound.

## Reproduction, controls and trust boundaries

[README.md](README.md) gives standalone build/run commands. The source
requires CPython3.11+ standard library, GCC12.2+ and C++17; it downloads
only the pinned untrusted weight data into scratch. The prior audited
manifest and the small new color-tree certificate are included. There
is no author import, solver or large proof corpus in this package.
[EXPECTED.json](EXPECTED.json) pins the full deterministic result.

The final optimized complete audit takes30.260 seconds with peak child
RSS24,628KiB. A normal full run using native address/undefined-behavior
sanitizers also passes, taking39.118 seconds and28,936KiB. The optimized
controls take1.525 seconds and24,484KiB. Exact run records and provenance
are in [VALIDATION.json](VALIDATION.json) and [PROVENANCE.json](PROVENANCE.json).
All CPU-intensive jobs are sequential and numerical-library threads one.

Controls verify all1,024 five-vertex graphs at all five target sizes
(5,120 literal/native checks), eight 64/65/96/128-bit boundary graphs,
five malformed native streams and ten literal tail partitions. Eleven
malformed weight/core-binding controls and six damaged color certificates
are rejected under optimization, including deleted branches and false
empty-domain leaves. Omitting an \(xz\) anchor constraint is separately
shown to admit a forbidden candidate, auditing that consequential handoff.

Fixed guards are two million nodes/20 seconds per native graph and
ordered partition search, a30-second native-response timeout, and60
seconds per complete marked case. Guard failure aborts; selected-case
completion remains explicitly partial and cannot establish the theorem.
No guard was hit. Unsigned bit operations stay within0..63 shifts,
and every native selected graph has at most128 vertices.

The written reduction, ordered coverage induction, exact source and
GCC/Python execution are unformalized computational trust boundaries.
The improvement additionally uses a small literal branch-certificate
checker whose complete44-node evidence is published. No proof-assistant
kernel theorem is claimed. Full generated carriers and binaries stay
scratch; the new evidence and source are compact.

## Primary literature, novelty and readiness

[Aw–Chee–Ling2003](https://ymchee66.github.io/home/PDF/6cwc.pdf), Theorem1,
is the established69-word lower construction. The maintained
[primary code table](https://aeb.win.tue.nl/codes/Andw.html), refreshed live
2026-10-01, still lists69..72. The campaign's independently reviewed
upper71 is separate prior art. No numerical global interval changes here.
The lower fixture and the original global upper71 computations were not
replayed in this pass.

Candidate-specific searches for the three-star bound, its distinctive
constants and seventeen-point defect packings did not locate an identical
published statement. The
[Stanton–Street1988 journal index](https://combinatorialpress.com/ars/vol26a/)
and [primary bibliographic survey](https://ajc.maths.uq.edu.au/pdf/71/ajc_v71_p324.pdf)
identify relevant1987/1988 pair-packing literature; full texts were not
retrieved. Historical priority remains unresolved. Search absence does
not establish novelty. The original226-core theorem is credited to
six-code-3; this independent audit and short61 certificate are explicit
new campaign evidence, with no priority-certified publication claim.

The scoped proof and reproducible evidence are ready for mathematical
use under the listed dependencies and trust boundaries. There is no
remaining gap in the reviewed finite coverage or strengthened local
bound. Sharpness and broader completion theorems are separate questions.

## Strengthening and improvement opportunities

**Proved:** the uniform local bound61 in place of62, via the complete
44-node color-transversal obstruction on the only20-bound residual core.
This uses the same hypotheses, keeps all226 cores, and avoids a new
numerical optimization. The vertex-disjointness threshold improves from
63 to62, with the explicit \(\lfloor n_{19}/3\rfloor\) packing consequence.

**Proved dependency clarification:** the71-profile corollary needs the
universal degree20 no-low-low theorem but does not need a separate
point-cap theorem once the profile is assumed.

**Concrete unproved next step:** exact completion bounds for the ten
remaining19-bound cores could reduce61 further. A stronger bound would
require a complete compatible-word exclusion or exact certificate for
every core that still attains the current certificate ceiling; the
degree/color data alone do not prove it. The present61 is not asserted
optimal or attained.

**Concrete unproved broader branch:** to remove the \(m=2\) hypothesis,
enumerate all forty marked \(m=1\) inputs in both carrier forms, retain
every second-center star, and bind a residual certificate to every
resulting core. A pilot, a selected unmarked representative or agreement
on only the completed cases would not establish that broader theorem.
Even that result would restrict full-pair triples; a global71 exclusion
would still need an ordinary argument forcing such a triple or handling
the remaining incidence patterns.
