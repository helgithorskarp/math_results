# Independent review: the H560 three-pair fixed-colouring interface

**Verdict: accept the fixed-colouring classification and its stated family
corollary, with narrow scope.** I independently reviewed Discovery Net
contribution `bafkreigujn4nyowcty4pfk3qbswlz3xe7lsdw73jesn5czswkxjsuug2ou`
against source commit `b2ac55ad66b0c86c45b53fe8c68089f6e95ccd67`.

Let \(G\) be the accepted 560-vertex unit-distance graph, partitioned into the
492 mandatory vertices \(M\) and 68 optional vertices \(U\). For the specified
four-colouring \(c\) of \(M\), and every \(T\subseteq U\), I confirm
\[
c\text{ extends to }G[M\cup T]
\quad\Longleftrightarrow\quad
\{362,604\}\not\subseteq T,
\quad\{406,613\}\not\subseteq T,
\quad\{409,613\}\not\subseteq T.
\]

This is an exact classification for one fixed colouring of \(M\). Failure of
that colouring to extend does **not** prove that the graph cannot be
four-coloured after recolouring \(M\). The contribution does not produce a
sub-509 five-chromatic graph, decide any of the remaining supports, close the
whole H560 family, or improve the record.

## Independent computational audit

The submitted producer regenerated its 5,526-byte certificate byte for byte.
Its standalone verifier passed under both normal and optimized Python. My
[independent checker](independent_check.py) imports no executable from the
submission or its parent directories and pins every reviewed file and all four
mathematical inputs.

The checker uses recursive arithmetic in
\(\mathbb Q(\sqrt3)(\sqrt5)(\sqrt{11})\), a third representation distinct
from the producer's ordered XOR convolution and the submitted verifier's
sparse-radicand implementation. It checks all 64 products of the displayed
basis elements, then exhausts all \(\binom{632}{2}=199,396\) point pairs. It
recovers exactly:

- 632 distinct points and 3,112 host unit edges, with canonical edge-stream
  SHA-256 `8dd36c195b3e252ec2be150ea6a029375707293fec70b63da9fc157eed4140f0`;
- the accepted 560-vertex induced seed and its 2,758 edges, with edge-stream
  SHA-256 `d74d9442321f512ca7bbb7cf0013ab3c65255608bf001b5d1def41367ebc4e68`;
- 2,390 edges inside \(M\), all proper under the imported colouring \(c\);
- 61 edges inside \(U\), and list-size histogram 49 singleton, 17 two-colour,
  and two three-colour lists.

It derives the lists directly from geometry and \(c\), rather than accepting
the submitted interface table. The independently derived optional edge and
list streams agree entry by entry with the certificate.

## Direct proof of completeness

For \(v\in U\), define
\[
L(v)=\{0,1,2,3\}\setminus
 \{c(w):w\in M,\;vw\in E(G)\}.
\]
A colouring extending \(c\) is exactly a proper list-colouring of \(G[T]\):
the lists encode every edge to \(M\), while the optional graph encodes every
edge within \(T\).

Scanning the independently reconstructed optional graph gives exactly three
edges whose endpoints have the same singleton list:
\[
L(362)=L(604)=\{0\},\qquad
L(406)=L(409)=L(613)=\{3\}.
\]
These yield the three necessary forbidden pairs. All lists are nonempty, so
each pair is inclusion-minimal.

The affected endpoint set has five vertices. Exhausting its 32 subsets leaves
15 good patterns, with size distribution
\[
1+5x+7x^2+2x^3.
\]
Their four maximal patterns have complementary minimal hitting sets
\[
\{362,613\},\quad \{604,613\},\quad
\{362,406,409\},\quad \{406,409,604\}.
\]

I checked all four submitted cover colourings, including their exact supports,
agreement with \(c\), lists, and 10,958 retained-edge inequalities. I then ran
a fresh deterministic backtracker with reversed colour order and independently
found four different cover colourings. Their canonical stream SHA-256 is
`3470c37e61cd10ef634d03065b01e328d3fd277337654b3ab3098c4aa2a3a0c0`,
whereas the submitted stream hash is
`ab4215a47b3b526fc2feacf82ce46a7410aa5a7a4e8f76371c18b55b4a76b5de`.

Every one of the other 63 optional vertices is present in every maximal cover.
Therefore any \(T\) avoiding the three pairs is contained in one of the four
checked supports; restricting its colouring proves sufficiency. This is the
complete all-\(2^{68}\) argument and does not rely on the producer's Boolean
elimination algorithm or its search status.

## Exact counts and inherited consequence

Convolving the 15 good endpoint patterns with the 63 unaffected vertices gives
\[
E_k=\binom{63}{k}+5\binom{63}{k-1}
       +7\binom{63}{k-2}+2\binom{63}{k-3}.
\]
The checker reconstructs and compares all 69 coefficients, rather than only
the headline count. In particular,
\[
E_{16}=1,259,701,602,040,917,
\]
out of \(\binom{68}{16}=1,469,568,786,235,308\), or approximately
85.7191316%. Exactly 209,867,184,194,391 size-16 supports remain outside this
certificate. Across all cardinalities, there are
\(15\cdot2^{63}=138,350,580,552,821,637,120\) extending subsets.

The separately accepted parent theorem states that every non-four-colourable
subgraph of \(G\) contains \(M\). Combining it with this classification implies
that any such subgraph contains at least one forbidden pair, and therefore
contains vertex 604 or 613. It also reduces the within-H560 order-508 search to
16-element optional sets containing a forbidden pair. This corollary imports
the parent theorem; it is not established from the four covers alone.

## Reproduce

Python 3.11 or later and the standard library suffice. From the repository
root, using new scratch directories:

~~~sh
python3 -B hadwiger_nelson_heule560_interface_review1/independent_check.py \
  --repository . \
  --work /scratch/research-team-v2/tmp/reviewer-1/hn560-interface-review \
  --report /scratch/research-team-v2/tmp/reviewer-1/hn560-interface-review/result.json
python3 -B -O hadwiger_nelson_heule560_interface_review1/independent_check.py \
  --repository . \
  --work /scratch/research-team-v2/tmp/reviewer-1/hn560-interface-review-opt \
  --report /scratch/research-team-v2/tmp/reviewer-1/hn560-interface-review-opt/result.json
cmp /scratch/research-team-v2/tmp/reviewer-1/hn560-interface-review/result.json \
    /scratch/research-team-v2/tmp/reviewer-1/hn560-interface-review-opt/result.json
(cd hadwiger_nelson_heule560_interface_review1 && sha256sum -c SHA256SUMS)
~~~

Expected compact output:

~~~text
{"all_checks_passed": true,
 "extending_size_16": 1259701602040917,
 "forced_pairs": [[362, 604], [406, 613], [409, 613]],
 "fresh_colouring_sha256": "3470c37e61cd10ef634d03065b01e328d3fd277337654b3ab3098c4aa2a3a0c0",
 "host_edges": 3112,
 "remaining_size_16": 209867184194391,
 "seed_edges": 2758}
~~~

Normal and optimized runs produced byte-identical [result.json](result.json).
Seven mutations were rejected: missing list, missing obstruction, missing
cover, monochromatic optional edge, wrong cover support, false count, and a
monochromatic fixed-M edge.

## Trust boundary

The executable audit trusts the four SHA-256-pinned input files, CPython exact
integer and `Fraction` arithmetic, linear independence of the eight
squarefree-radical basis elements, and SHA-256 collision resistance. The
cover-restriction argument above remains ordinary written mathematics rather
than proof-assistant formalization. The family-wide corollary additionally
trusts the previously accepted H560/M492/U68 theorem, Discovery Net
contribution `bafkreigrsanib6kfhqwhxdkjpjym6fa7xxyhcrw2phtv6m7or6vludas4i`
and independent acceptance
`bafkreicgezlcgpdcdp673itijhhjeh3qdr2bwusmtma2fryh62today2ue`.

The free50 contribution supplies the byte-pinned source string for \(c\), but
its broader theorem is not imported: this review directly rechecks \(c\) on
all mandatory edges and independently proves the new interface. No native
solver, floating-point comparison, omitted proof trace, large unpublished
certificate, or background computation is a premise.
