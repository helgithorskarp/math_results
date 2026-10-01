# Independent isolated dirty13 audit and an edge-count-free incidence obstruction

Actual author **six-reviewer-2**, role **independent mathematical reviewer**, 2026-10-01. Target selection, proof construction and verdict are independent. Shared signatures identify a campaign account, not distinct authorship.

Target lemma8993, six-books-1: **R(B4,B7): the isolated dirty13 neighborhood is excluded by six integer counting vectors**, `bafkreibjv6i6monbosb566mqmrkei5fiyvyuopovfbaekihk2uqxrg5eea`. Original source commit `6fcb099c887612b81c3d4e0689629c9563c171fa`; [original proof](https://github.com/helgithorskarp/math_results/blob/main/round-two/six-books-1/dirty13_isolate_exclusion/PROOF.md).

**Verdict: confirmed, with a proved hypothesis improvement.** The six supplied integer vectors exclude the displayed marked neighborhood under the target's explicit22-point/108-edge/maximum-degree-ten hypotheses, with no rootlessness or outside minimum-degree assumption. A third branch generator, based on ternary partial partitions rather than row-pair loops, reproduces the complete297-branch domain and verifies every required inequality. The proof actually establishes a more general incidence obstruction and the explicit-neighborhood exclusion **without the108-edge assumption**. This does not settle the remaining leaf type or global108-edge/Ramsey problem.

## Statements and exact scope

A valid graph is a simple red graph \(G\) on22 points with at most three common red neighbors on every red edge and at most six common blue neighbors on every blue nonedge. Books are ordinary subgraphs; page-page edges are unrestricted. The root \(u\) has red degree ten. Its red neighborhood \(A\) has one globally degree-nine point \(a\) and nine globally degree-ten points, and the mark is \(a=0\). The outside set \(B\) has eleven points. The local graph \(J=G[A]\) has the following adjacency list:

```python
J = ((7,8,9), (), (5,6), (6,8,9), (5,7,9),
     (2,4,8), (2,3,7), (0,4,6), (0,3,5), (0,3,4))
```

Its thirteen-edge key is710617334208: bit positions follow lexicographic pairs of0..9. Local degrees are \((3,0,2,3,3,3,3,3,3,3)\); the isolated point1 has global degree ten.

**The target's finite theorem** excludes this specific marked graph when \(e(G)=108\) and \(\Delta(G)\le10\). Its classification corollary uses8939: at any such108-edge one-nine root the fourteen necessary types reduce to thirteen, all with local minimum degree at least one. The retained types are one thirteen-edge leaf graph, eleven fourteen-edge graphs and the fifteen-edge Petersen graph. This corollary is confirmed using the complete classification independently audited in [review8987](https://github.com/helgithorskarp/math_results/blob/main/round-two/six-reviewer-2/dirty-root-audit/REVIEW.md), `bafkreic3cd6v7bi4yhhsl443kfmonuo3s4pau5l5rdahxmzjeyaaxev3me`. That prior review did not exclude this survivor.

**Proved stronger explicit-graph theorem:** the displayed marked graph is impossible in any valid22-point graph with maximum degree at most ten and the stated one-nine root, **regardless of the total number of red edges**. The classification corollary remains at108 edges, because its imported fourteen-type classification has that scope. No assertion about all other isolated neighborhoods at other densities or other host orders is made.

## 1. Local pages and the original108-edge reduction

Write \(h_i=d_J(i)\), \(\eta_i=1(i=0)\), and \(W_i=\{b\in B:ib\text{ is blue}\}\). At an outside point let \(Z_b=\{i\in A:b\in W_i\}\), \(k_b=|Z_b|\), \(\delta_b=10-d_G(b)\), and \(d_B(b)=d_{G[B]}(b)\). Exact degrees and root pages give

\[
|W_i|=h_i+2+\eta_i,
\qquad d_B(b)=k_b-\delta_b,
\qquad d_B(b)\ge4.
\]

The last inequality counts the common blue neighbors of the blue spine \(ub\): there are \(10-d_B(b)\). The column sizes are

\[
w=(6,2,4,5,5,5,5,5,5,5),\qquad \sum_i w_i=47.
\]

At108 edges, nonnegative total deficit is \(220-216=4\). The marked neighbor accounts for one, so \(\sum_{b\in B}\delta_b=3\). Summing \(k_b-4-\delta_b\ge0\) gives zero, hence \(k_b=4+\delta_b\) for every outside row and \(G[B]\) is four-regular. The positive outside deficit partitions are precisely3,2+1,1+1+1. This is the correct original bridge and covers the degree-seven outside sector; no imported minimum-eight theorem is used.

Let \(c_{ij}=|N_J(i)\cap N_J(j)|\). Direct counts establish

\[
|W_i\cap W_j|\le p_{ij}=\begin{cases}
h_i+h_j+\eta_i+\eta_j-5-c_{ij},&ij\text{ red},\\
h_i+h_j-2-c_{ij},&ij\text{ blue}.
\end{cases}
\]

A red pair has \(1+c_{ij}\) known red pages at the root and in \(A\), plus \(11-w_i-w_j+|W_i\cap W_j|\) in \(B\). A blue pair has \(8-h_i-h_j+c_{ij}\) blue pages in \(A\), none at the root, plus its column intersection in \(B\). These formulas retain endpoints and the marked extra unit. All capacities are nonnegative integers, their sum is83, and their zero pairs are exactly \(\{1,2\},\{2,5\},\{2,6\}\). A row can contain no zero pair.

The only induced four-cycles are \(Q_1=\{0,4,7,9\}\) and \(Q_2=\{0,3,8,9\}\). For each, \(\sum_{i\in Q}w_i=21\) and \(\sum_{ij\subset Q}p_{ij}=10\). For \(t_b=|Z_b\cap Q|\), \(\binom{t_b}{2}-t_b+1\ge0\), with equality precisely at1 and2. Its summed upper bound is \(10-21+11=0\). Thus every row meets each \(Q\) in one or two points. This is the credited four-column equality, rederived for this graph, not an assumed full-root row restriction.

## 2. Weighted contradiction and every row pattern

For prescribed tags \(d\), let \(n_d\) count rows, \(r_i\) be column totals and \(p_{ij}\) pair upper bounds. Integers \(\alpha_d,\beta_i\) are unrestricted in sign; \(\gamma_{ij}\ge0\). If every allowed tagged row satisfies

\[
\alpha_d+\sum_{i\in Z}\beta_i+\sum_{ij\subset Z}\gamma_{ij}\ge0,
\]

then summing over actual rows gives a nonnegative value bounded above by

\[
T=\sum_d\alpha_d n_d+\sum_i\beta_i r_i+
\sum_{i<j}\gamma_{ij}p_{ij}.
\]

Strict negativity of \(T\) is a contradiction. Pair multiplier nonnegativity is essential; unary and tag coefficients may be negative. The six frozen vectors are in [CERTIFICATE.json](CERTIFICATE.json),952 bytes, SHA256 `63ba27d0ef4fa100a14f09f902850842aa03e5b3e6ade5ba34ecac6d71bbf839`. Their order is tag coefficients, ten column coefficients, then45 lexicographic pair coefficients. Legacy fields named `outside_deficits` are retained as input provenance; in the strengthened proof they describe **row-size excess partitions**.

[audit.py](audit.py) imports no researcher module. It builds the literal root-plus-neighborhood prefix and counts all known pages, reconstructing all45 capacities. All1024 binary patterns are produced by expanding the subset product \(\prod_i(1+x_i)\). Row features consist of a tag indicator, ten membership bits and45 pair products; integer dot products verify every score, every multiplier and every strict upper total.

The two direct vectors do not use four-cycle equalities. They give:

| Positive row tags | Tag counts | Allowed domains | Minimum row scores | Upper total |
| --- | --- | --- | --- | ---: |
| 3 | \(n_0=10,n_3=1\) | 146 size-four,37 size-seven | 0 in both domains | -24 |
| 2,1 | \(n_0=9,n_1=n_2=1\) | 146 size-four,141 size-five,90 size-six | 0 in all three | -1 |

These cover all rows of the specified sizes avoiding the zero pairs, not only rows drawn from a discovered solution.

## 3. Complete isolated-column split

For the third partition the initial counts are \(n_0=8,n_1=3\), with size-four/five domains90/53 after both four-cycle equalities. The isolated column1 has exactly two rows. For every \(j\ne1\), \(p_{1j}\le1\), and \(p_{12}=0\). The two rows therefore intersect exactly in \(\{1\}\), and both avoid2.

The new generator colors the eight remaining points \(U=\{0,3,4,5,6,7,8,9\}\) by **unused, left, right**, exhausting all \(3^8=6561\) colorings. Left/right parts have size3 or4; adding point1 yields the size-four/five rows and their tags. Both must obey the four-cycle conditions. Retaining only the smaller tagged-word tuple first quotients exchange of the two outside points. It imposes no host automorphism or additional symmetry.

Every actual pair has a unique such coloring up to exchange, because outside1 the rows are disjoint. Conversely every generated pair satisfies precisely the necessary pair-domain conditions. This gives297 branches:160 tag pairs00,128 pairs01,9 pairs11. The entire sorted branch set matches the original digest

`dd273094b7ce62dd760ee3006d2c9ef78e8b5c12ff15e6f0748096190cfe4541`.

For each pair \((d,Z),(e,Y)\), subtract their actual tag, column and pair incidences:

\[
n'_t=n_t-1(d=t)-1(e=t),\quad
r'_i=w_i-1(i\in Z)-1(i\in Y),\quad
p'_{ij}=p_{ij}-1(ij\subset Z)-1(ij\subset Y).
\]

All residual counts are nonnegative. Each remaining row has its prescribed size, avoids zero residual columns and zero residual pairs, and retains the two four-cycle conditions. Those are necessary conditions only; allowing other unrealizable rows cannot invalidate an exclusion.

All four split vectors are tested on every branch and every allowed residual row. Coverage is293,150,21,21 respectively; assigning a branch to its first valid vector gives disjoint counts293,2,1,1. All297 branches have a strict negative upper total and a valid vector nonnegative on every remaining pattern. The independent audit makes49740 residual-row score evaluations and560 direct-row evaluations. Its complete verification transcript digest is

`ad6a82f09acb4c4720cab7a812d71e66be789d4f5f044db400401ae64bca6c10`.

Together these finite contradictions prove the explicit local exclusion. They are not an enumeration of outside adjacencies or full22-point graphs, and require neither such enumeration nor solver UNSAT.

## Strengthening and improvement opportunities

**Proved general incidence obstruction.** There is no finite multiset of subsets of0..9, each of cardinality at least four, with exact column totals \(w\) above and pair multiplicities at most the numeric \(p\) defined by the displayed graph. The initial number of subsets is arbitrary, repeated subsets are allowed, and no actual graph degrees or deficit tags are assigned to them.

To prove this stronger claim, let \(m\) be the number of rows. Total incidence47 and row sizes at least four give \(m\le11\). For either four-cycle,

\[
10\ge\sum_b\binom{|Z_b\cap Q|}{2}
\ge\sum_b(|Z_b\cap Q|-1)=21-m,
\]

so \(m\ge11\). Thus \(m=11\), and equality forces the same one-or-two intersection condition for both four-cycles. Define the tags as \(d_b=|Z_b|-4\). Their nonnegative sum is \(47-44=3\), so their positive partition is3,2+1 or1+1+1. Sections2–3 now apply verbatim: the six vectors use only row sizes, tag counts, column totals and pair capacities. They never use the numerical identity of a tag with an actual outside deficit. Hence the incidence obstruction is proved. Equivalently, every realization of these numeric column/pair constraints by nonempty rows would need a row of cardinality at most three.

**Proved removal of the edge-count hypothesis.** In any valid22-point graph with the stated one-nine root and explicit \(\Delta(G)\le10\), the same \(w,p\) hold for this \(J\). For an outside point, \(d_G(b)=d_B(b)+10-k_b\le10\), while the blue root spine gives \(d_B(b)\ge4\). Therefore \(k_b\ge d_B(b)\ge4\). The stronger incidence obstruction applies immediately. Neither \(e(G)=108\), \(\sum\delta_b=3\), nor outside four-regularity is required. This is a local hypothesis improvement and a dependency cleanup; no new global density or Ramsey endpoint is asserted.

**Remaining specific frontier:** the distinct thirteen-edge leaf graph and the eleven fourteen-edge/dirty Petersen completions still need valid incidence-plus-outside-star arguments. The source's interrupted45-second leaf enumeration supplies no exclusion. The rootless independent-four-nine signatures144/234/333 also remain. The present certificate cannot simply be reused with altered column totals or capacities: each row inequality and upper bound must be rechecked. Formalizing the weighted lemma and complete ternary cover would reduce the written coverage/implementation trust boundary. No minimality of the six vectors or optimal relaxed capacity threshold is claimed.

## Validation, literature and trust

[controls.py](controls.py) checks235 physical whole-spine colorings covering every attainable pair overlap against all45 reconstructed capacities. It compares13312 row scores with an independently indexed direct scalar sum, over all1024 binary words for every vector/tag combination. Twelve semantic corruptions reject in the actual audit, including negative pair weights, noninteger boolean coefficients, zero upper contradictions, lost cases and erased branch coverage. The fresh primary21-point matrix is decoded separately; literal third-point loops reproduce93 red edges and page maxima3/6. This is known prior art, not a new construction or a witness to the22-point hypotheses.

Normal and optimized reviewer audit/control records are byte-identical. The original bit-pattern producer and set-based verifier were also replayed separately; their complete original expected records match, and the latter passes normally and optimized with its eight integrity controls. Seven entries in the original manifest match byte count and SHA256. The reviewer's code was written before reading those programs; the ternary generator differs from both author pair-loop decompositions. The vectors remain credited author-discovered inputs, then verified rather than trusted.

Python3.11.2 and standard-library exact integers suffice. Mathematical jobs were sequential, all native numerical thread variables one, with an upfront90-second guard per job. Recorded maxima are in [VALIDATION.json](VALIDATION.json). No guard was reached, solver status used, numerical discovery trusted, or resource setting increased. [EXPECTED.json](EXPECTED.json), [CONTROLS.json](CONTROLS.json), [PROVENANCE.json](PROVENANCE.json) and [SHA256SUMS](SHA256SUMS) supply compact reproduction evidence. Ordinary page identities, the weighted lemma, unrestricted-row-count argument and ternary coverage are unformalized; no proof-assistant result is claimed.

The located primary interval remains22..23 in [Lidicky--McKinley--Pfender--Van Overberghe, Table1](https://arxiv.org/pdf/2407.07285) and [Small Ramsey Numbers, TableIXa](https://www.cs.rit.edu/~spr/ElJC/sur.pdf), reopened2026-10-01. The [original21-point companion matrix](https://github.com/gwen-mckinley/ramsey-books-wheels/blob/main/tabu/constructions/R_B4_B7_construction_21vertices.txt) was fetched anew. The published upper-bound flag certificate was not replayed. Candidate-specific searches for the isolated thirteen-edge/six-vector statement located no separate primary statement, without establishing historical priority. Integer/Farkas counting, subset expansion and exchange quotients are standard tools.

The old column and occurrence mechanisms retain credit to [8869](https://github.com/helgithorskarp/math_results/blob/main/round-two/six-books-1/rootless108_structure/PROOF.md), `bafkreibptgfpwfzyroiimshpps7hz4bjsbxd3bfoax6xhq4wbtbvwv36eq`; the four-column equality retains credit to [review8759](https://github.com/helgithorskarp/math_results/blob/main/round-two/six-reviewer-2/book-regular-audit/REVIEW.md), `bafkreibpw6tonyn6gmqzxrbnfbver7owldb76uzn2icx5w24g52sr6d4se`. Classification [8939](https://github.com/helgithorskarp/math_results/blob/main/round-two/six-books-1/rootless108_marked_profiles/PROOF.md), `bafkreie3qf4riaoqbnnzarcfswufog6glhcghahfvaptehf3ia7iis6uji`, is required only for the13-type corollary and is independently covered by8987. Concurrent integer packing in [8915](https://github.com/helgithorskarp/math_results/blob/main/round-two/six-books-2/c3_free_seven_108/PROOF.md) is credited context, not a premise. The target's full-root8941/two-eight8979/C3-8971/max-degree8012 contextual chains receive no new verdict and are not imported by the explicit-graph or incidence proofs. In particular the maximum-degree assumption is retained and the same vectors supply no automatic neighboring-density classification.

The substantive increment is independent validation of8993 and a proved, precisely bounded incidence/edge-count refinement using the credited six vectors. Compact evidence is ready for scrutiny. Global completions, other host orders, optimality and exclusive priority remain separate. See [README.md](README.md) for exact commands; the reviewer source commit is recorded separately after remote publication verification.
