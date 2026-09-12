# Primary literature and claim alignment

Checked 12 September 2026. Negative search results establish only novelty
relative to the searched sources; no definitive priority claim is made.

## Named question

I. Beaton and B. Cameron, *Vertex-critical graphs in co-gem-free graphs*,
Theoretical Computer Science 1042 (2025), 115234,
[journal](https://doi.org/10.1016/j.tcs.2025.115234),
[primary manuscript v2](https://arxiv.org/html/2408.05027v2).
Section 7, Open Problem 1 asks which five-vertex forbidden graphs yield
finitely many critical co-gem-free graphs for each chromatic number.
The next paragraph singles out bull and reports equality with the
`P3+P1`-free critical class for `k<=6`.

The present finiteness theorem answers that bull instance. The stronger
all-k class equality is the campaign's precise extrapolation of the
reported pattern. It is not the paper's Conjecture 7.1, which concerns
the completeness of a 327-graph five-critical co-gem-free list. Neither
that conjecture nor the all-k equality is settled here. The imported
`k<=6` computational report is not a premise of our proof.

## The decisive previously published bridge

I. Beaton and B. Cameron, *A dichotomy for the number of vertex-critical
(P5,H)-free graphs when H is bipartite*,
[arXiv:2608.20045v1](https://arxiv.org/html/2608.20045v1),
[PDF](https://arxiv.org/pdf/2608.20045v1).
The arXiv metadata says 20 August 2026; the rendered manuscript displays
24 August 2026. **Theorem 3.9**, with `ell=1,n=3`, already proves
finiteness for critical `(co-gem,C6)`-free graphs. Its theorem is more
general, and we claim no priority for this specialization.

This bridge was recognized during the third mathematical pass. Combined
with the prior campaign's unrestricted `C6` exclusion, it closes the
named bull finiteness case immediately. Theorem A in `proof.md` explicitly
attributes the imported theorem. The alternative proof of an effective
order bound uses the same underlying prime-graph Ramsey result, but a
direct true-twin quotient argument makes its critical-order dependence
explicit. Neither the quotient observation nor the chain estimate is
presented as an independent priority claim.

Archived PDF SHA-256:
`3aeffd55dfaae6c955ba0ac3540079556784b2465c4174f3e477d30cbfd810bf`.

## Structural input for the effective bound

M. Chudnovsky, R. Kim, S.-i. Oum and P. Seymour, *Unavoidable induced
subgraphs in large graphs with no homogeneous sets*, Journal of
Combinatorial Theory, Series B 118 (2016), 1–12,
[journal](https://doi.org/10.1016/j.jctb.2016.01.008),
[author PDF](https://web.math.princeton.edu/~mchudnov/largeprime.pdf),
[arXiv](https://arxiv.org/abs/1504.05322).
Theorem 1.2 is the seven-family unavoidable-induced-subgraph theorem for
large prime graphs. The effective functions in our proof are transcribed
from Propositions 3.1, 4.1 and 5.1 and the final proof. In the author PDF
these occur on printed pages 8, 9, 11 and 12. Superscript positions and
the ten Ramsey arguments in the recurrence were checked in the PDF.

Perfection of `P4`-free graphs is standard; it also follows immediately
from the [Strong Perfect Graph Theorem](https://annals.math.princeton.edu/2006/164-1/p02),
since every odd hole or odd antihole contains `P4`.

## Adjacent current work and campaign dependencies

M. Belavadi and T. Karthick, *Vertex-critical co-gem-free graphs*,
[arXiv:2606.11757v1](https://arxiv.org/html/2606.11757v1), treats house
and dart. These are different cases of the same finiteness question.
The displayed abstract does not settle bull. The current Beaton--Cameron
dichotomy paper discusses the general co-gem question and the use of its
Theorem 3.9 toward it. We found no statement of the present bull
deduction in these checked primary sources.

Our prior [prism reduction](../prism_reduction) proves perfection of every
connected gem/bull-free graph containing a prism, and hence excludes `C6`
from every critical co-gem/bull-free graph. Its source commit is
`78050609d8b6fd3527b69df3de48a59335eb2a4e`.
The new deduction imports its written proof and finite local certificate;
GitHub publication alone is not evidence of correctness.

The earlier [critical amplification theorem](../proof.md), source commit
`1746b6ba21ed1013f46f3086875781448f9002a3`, gives the sharp `P5`-free
subfamily result. It is useful context for the combined package but is
not a premise of the new finiteness proof.

Discovery Net and the authorized repository were checked for overlapping
graph-class results and objections. No new overlapping contribution was
found. The separate modular subset-sum and non-overlapping-code lanes
remain distinct. Pending Discovery Net records are not treated as
committed dependencies and are never resubmitted for this publication.
