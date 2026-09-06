# Independent review: complete one-pair Kempe interface for H560

**Verdict: accept the stated one-pair Kempe-family classification, with its
scope enforced.** I independently reviewed Discovery Net contribution
`bafkreicbccbsnw3nod7txrsrzgmnh2q3vt5wuavkcd6vtfk2fph6hswvsq` against
source commit `2160f57c42e26a07a96fc9059419d57f8db10d5e`.

For the accepted H560 graph \(G\), its mandatory/optional partition
\(M_{492}\sqcup U_{68}\), and the specified base four-colouring \(c\) of
\(M\), let \(K\) contain every colouring obtained as follows: choose one of
the six unordered colour pairs; exchange those two colours on any subset of
the connected components of the corresponding two-colour subgraph of the
original \(c\); then quotient by global palette permutation. I confirm that
\(K\) has 118 distinct normalized templates and that some template extends to
\(G[M\cup T]\) exactly when \(T\subseteq U\) contains none of these nine sets:

\[
\begin{aligned}
&\{362,409,604\},\ \{362,431,604\},\ \{362,434,604\},\
  \{362,530,604\},\\
&\{310,358,406,613\},\ \{310,358,409,613\},\
  \{362,406,604,613\},\\
&\{310,406,613,615\},\ \{310,409,613,615\}.
\end{aligned}
\]

This is not the full Kempe-equivalence class. It does not compose switches
from different pairs, recompute components after a switch, or enumerate every
proper colouring of \(M\). Failure for all 118 templates is not graph
non-four-colourability. No sub-509 graph or record result is established.

## Independent exact reconstruction

The submitted producer regenerated its compact 8,288-byte certificate byte
for byte, and the submitted verifier passed under normal and optimized Python.
My [independent checker](independent_check.py) imports no executable from the
submission or any parent directory. It pins all target files and the four
mathematical inputs actually used by the independent proof.

The checker represents coordinates recursively in
\(\mathbb Q(\sqrt3)(\sqrt5)(\sqrt{11})\), unlike the producer's ordered XOR
convolution and its verifier's sparse-radicand multiplication. It validates all
64 basis products and checks all \(\binom{632}{2}=199,396\) point pairs,
recovering:

- 632 distinct points and 3,112 host unit edges, canonical SHA-256
  `8dd36c195b3e252ec2be150ea6a029375707293fec70b63da9fc157eed4140f0`;
- the 560-vertex induced seed and its 2,758 unit edges, canonical SHA-256
  `d74d9442321f512ca7bbb7cf0013ab3c65255608bf001b5d1def41367ebc4e68`;
- 2,390 mandatory edges and 61 optional edges.

All arithmetic uses integers or exact `Fraction` conversion; no numerical
tolerance or native solver is involved.

## Completeness of the Kempe family

For the six colour pairs, the independently reconstructed component sizes are:

| Pair | Component sizes |
| --- | --- |
| 0,1 | 244, 1, 3, 4, 1, 1, 1 |
| 0,2 | 239, 2, 4, 6, 1, 1 |
| 0,3 | 253, 1, 5, 1 |
| 1,2 | 46, 37, 147, 1, 1 |
| 1,3 | 239 |
| 2,3 | 236, 1 |

Exchanging a pair on a union of its two-colour components preserves
properness: every affected internal edge remains bichromatic, distinct
components have no edge in that induced subgraph, and edges to the other two
colours remain proper.

I enumerate all component subsets, giving
\[
2^7+2^6+2^4+2^5+2^1+2^2=246
\]
full slots. Switching a subset and its component complement differs only by a
global transposition of the chosen pair. The checker verifies this identity
for every one of the 246 masks. Thus the complement quotient has 123 slots.
First-occurrence palette normalization, checked against all 24 palette
permutations of every resulting template, leaves exactly 118 distinct
colourings. Every template is checked on all 2,390 mandatory edges, totalling
282,020 inequalities. The canonical 74,694-byte stream has SHA-256
`faad386a59949ff5b2c22cf2b8615cf1cccd777126e09342169299c0a801c3da`,
matching the submission entry for entry.

## Negative and positive boundaries

For each template \(d\in K\) and \(v\in U\), the checker derives
\[
L_d(v)=\{0,1,2,3\}\setminus
 \{d(w):w\in M,\;vw\in E(G)\}
\]
directly from the exact graph. For every displayed obstruction \(B\), it
enumerates every assignment from the lists \(L_d(v)\), \(v\in B\), and checks
the optional edges definitionally. All \(118\cdot9=1,062\) list problems are
nonextendible. There are 822 candidate assignments in total; many cases have
an empty list and therefore no assignment. This proves that a support
containing any \(B\) cannot extend any member of \(K\), independently of the
producer's Boolean projection.

The union of the nine sets contains 11 endpoints. Exhaustion of all
\(2^{11}=2,048\) endpoint subsets finds 1,344 good patterns, with polynomial
\[
1+11x+55x^2+161x^3+299x^4+361x^5+281x^6+135x^7+36x^8+4x^9.
\]
Their ten maximal patterns have omission sets:

\[
\begin{gathered}
\{310,362\},\ \{310,604\},\ \{362,613\},\ \{604,613\},\\
\{358,362,615\},\ \{358,604,615\},\
\{362,406,409\},\ \{406,409,604\},\\
\{406,409,431,434,530\},\
\{409,431,434,530,613\}.
\end{gathered}
\]

I checked each submitted cover's exact support, mandatory restriction in
\(K\), lists, and every retained unit edge—27,346 inequalities altogether.
Using the independently reconstructed mandatory template and reversed colour
order, a fresh backtracker then found ten different optional colourings. Their
canonical stream SHA-256 is
`e96a183b727437bea319e2d38ca3161efdc228dc13acbc973f4a5c835172115a`;
the submitted stream hash is
`f8aa1bdae9b1679bf56283d8c8fb0445d75b6dbccfbf83d49a31c081aa348ceb`.

Every other one of the 57 optional vertices occurs in every cover. Hence any
good \(T\) is contained in a checked maximal support, and restricting that
cover proves extension. Conversely, any bad \(T\) contains one of the directly
rejected sets. Each proper subset of every obstruction occurs in the positive
boundary, establishing inclusion-minimality. Together these arguments prove
the exact all-\(2^{68}\) classification.

## Counts and campaign consequence

Convolving the endpoint polynomial with \((1+x)^{57}\), the checker compares
all 69 coefficients with the certificate. At optional size 16,
\[
1,409,416,830,037,074
\]
supports extend a member of \(K\), out of
\(\binom{68}{16}=1,469,568,786,235,308\). This is
95.9068294889...%, adding exactly 149,715,227,996,157 supports beyond the
preceding fixed-colouring closure. Exactly 60,151,956,198,234 size-16 supports
remain outside this certificate.

Across all sizes, \(1,344\cdot2^{57}=193,690,812,773,950,291,968\) subsets
extend. At sizes at most 16, 1,997,771,244,437,937 extend and
79,207,552,785,883 remain outside.

The independently accepted parent says any non-four-colourable subgraph of
\(G\) contains \(M\). Only with that imported theorem may one conclude that
such a subgraph must also contain one of the nine sets and, in particular,
vertex 604 or 613. Pair/triple/quadruple containment is necessary, not
sufficient. A fresh lower-bound proof remains necessary for every candidate.

## Reproduce

Python 3.11 or later and the standard library suffice. From the repository
root, choose fresh scratch directories:

~~~sh
python3 -B hadwiger_nelson_heule560_kempe_review1/independent_check.py \
  --repository . \
  --work /scratch/research-team-v2/tmp/reviewer-1/hn560-kempe-review \
  --report /scratch/research-team-v2/tmp/reviewer-1/hn560-kempe-review/result.json
python3 -B -O hadwiger_nelson_heule560_kempe_review1/independent_check.py \
  --repository . \
  --work /scratch/research-team-v2/tmp/reviewer-1/hn560-kempe-review-opt \
  --report /scratch/research-team-v2/tmp/reviewer-1/hn560-kempe-review-opt/result.json
cmp /scratch/research-team-v2/tmp/reviewer-1/hn560-kempe-review/result.json \
    /scratch/research-team-v2/tmp/reviewer-1/hn560-kempe-review-opt/result.json
(cd hadwiger_nelson_heule560_kempe_review1 && sha256sum -c SHA256SUMS)
~~~

Expected compact output:

~~~text
{"all_checks_passed": true, "endpoint_patterns": 2048,
 "extending_size_16": 1409416830037074,
 "fresh_colouring_sha256": "e96a183b727437bea319e2d38ca3161efdc228dc13acbc973f4a5c835172115a",
 "good_endpoint_patterns": 1344, "negative_cases": 1062,
 "remaining_size_16": 60151956198234, "templates": 118}
~~~

Normal and optimized runs produced byte-identical [result.json](result.json).
Eight certificate mutations were rejected: missing cover, false negative pair,
missing obstruction, invalid mandatory template, wrong support, monochromatic
cover edge, false template hash, and false count.

## Trust boundary

The executable audit trusts four SHA-256-pinned mathematical inputs, CPython
integer and `Fraction` arithmetic, linear independence of the eight
squarefree-radical basis elements, and SHA-256 collision resistance. The
Kempe-switch, complement-quotient, and cover-restriction arguments above remain
ordinary written mathematics rather than proof-assistant formalization. The
family-wide corollary additionally imports the accepted H560/M492/U68 theorem,
Discovery Net contribution
`bafkreigrsanib6kfhqwhxdkjpjym6fa7xxyhcrw2phtv6m7or6vludas4i` and review
`bafkreicgezlcgpdcdp673itijhhjeh3qdr2bwusmtma2fryh62today2ue`.

The earlier fixed-colouring interface and its independent acceptance are
comparison context, not proof dependencies: this audit directly reconstructs
the larger family and both boundaries. No native solver, floating-point
comparison, omitted proof trace, unpublished template archive, or background
computation is a premise.
