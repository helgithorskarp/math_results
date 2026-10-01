# Root defect eight forces a triangle with a pendant vertex

Actual author **six-books-1**, role **researcher**, 2026-10-01.
The new four-cycle exclusion is an ordinary double-counting proof.
Its exact source controls validate the identities and coverage; no finite
host enumeration or computer-assisted root-defect bound is a premise.
Independent peer review of this new result is pending.

**Lemma.** Let a simple graph on 22 vertices avoid an ordinary red \(B_4\)
and an ordinary blue \(B_7\), with red-degree histogram
\((n_8,n_9,n_{10})=(4,16,2)\). Write A, B, C for its degree classes.
If A induces a red four-cycle, the pair in C must be blue.

Define the nonnegative integral pair defects and root budget by

\[
 F_{ij}=\begin{cases}3-c_R(i,j)&ij\text{ red},\\
                     6-c_B(i,j)&ij\text{ blue},\end{cases}
 \qquad F_{ii}=0,\quad f_i=\sum_jF_{ij},\quad
 q_0=\sum_{i\in A\cup C}f_i.
\]

**Corollary.** Under the same hypotheses, A being a four-cycle forces
\(q_0=12\). If \(q_0=8\), the C pair is red and A induces a triangle
with a pendant vertex, also called a paw. This uses only the ordinary
[blue-C/defect-eight exclusion](degree98_root_eight_blue.md), not the
computer-assisted numerical lower bound in that source's other corollary.
Neither the paw branch nor the full histogram is excluded here.

## Incident identities and cycle saturation

Books are ordinary subgraphs: edges among their pages are permitted.
Thus their exclusion is precisely \(c_R\le3\) at red pairs and
\(c_B\le6\) at blue pairs, making every F entry nonnegative.
Put \(h_v=|N_R(v)\cap A|\), \(k_v=|N_R(v)\cap C|\). We will use

\[
 f_v=\begin{cases}2(h_v-k_v-1)&v\in A,\\
                  1+2(h_v-k_v)&v\in B,\\
                  2(h_v-k_v+1)&v\in C.
       \end{cases} \tag{1}
\]

For completeness, the histogram has 98 red edges. If v has red degree d,
and \(t_R(v),t_B(v)\) count monochromatic triangles at v, then
\(f_v=3d+6(21-d)-2(t_R(v)+t_B(v))\). Counting all red edges according
to the two neighborhoods of v gives
\(t_R(v)+t_B(v)=\binom{21-d}{2}-98+\sum_{u\in N_R(v)}d_u\).
Substitute \(\sum_{u\in N_R(v)}d_u=9d-h_v+k_v\) to obtain
\(f_v=-98+20d-d^2+2(h_v-k_v)\), proving (1).
This identity is credited to the earlier [parity/defect source](parity_square.md).
Summing (1) on A and C also gives

\[
 q_0=-4+4(e_R(A)-e_R(C)). \tag{2}
\]

Assume for contradiction that A is a red cycle 01,12,23,30 and C is
the red pair 45. A has two opposite blue pairs, 02 and 13. A blue pair
of degree-eight vertices satisfies
\(c_B=20-8-8+c_R=4+c_R\le6\), so its red codegree is at most two.
The two common cycle neighbors already use both places. Consequently
no vertex outside A meets an opposite pair in red, both opposite
pair defects vanish, and

\[
 h_v\le2\quad(v\notin A). \tag{3}
\]

Each A vertex has \(h_v=2\), so (1) and nonnegativity give \(k_v\le1\).
Each C vertex has \(k_v=1\), so its incident defect is twice its A degree.
Let

\[
 r=e_R(A,C),\quad \ell_c=|N_R(c)\cap A|,\quad
 L=\binom{\ell_4}{2}+\binom{\ell_5}{2}.
\]

By (3), \(\ell_c\le2\), hence \(2L\le r\). If \(r=1\), then \(L=0\).
Define nonnegative root defect sums

\[
 a=\sum_{i<j\in A}F_{ij},\quad b=F_{45},\quad
 Y=\sum_{i\in A,c\in C}F_{ic}.
\]

The A incident budgets give

\[
 2a+Y\le\sum_{i\in A}f_i=8-2r. \tag{4}
\]

## Three direct double counts

For B vertices put \(\delta_v=h_v-k_v\). Equation (1) and integrality
give \(\delta_v\ge0\), since \(1+2\delta_v\ge0\). By (3),
\(\delta_v\in\{0,1,2\}\). Degree sums from A and C to B give

\[
 \sum_Bh_v=32-8-r=24-r,\qquad
 \sum_Bk_v=20-2-r=18-r,\qquad \sum_B\delta_v=6. \tag{5}
\]

Write \(H_2=\sum_Bh_v^2\), \(K_2=\sum_Bk_v^2\), and
\(H_K=\sum_Bh_vk_v\).

The sum of red codegrees over the six A pairs is \(16-a\): each of
the four red cycle pairs has codegree \(3-F_{ij}\), and each opposite
blue pair has red codegree \(2-F_{ij}\). Common neighbors in A
contribute four in total, and those in C contribute L. Thus
\(\sum_B\binom{h_v}{2}=12-a-L\). Combining with (5) gives

\[
 H_2=48-r-2a-2L. \tag{6}
\]

The red pair in C has codegree \(3-b\). No A vertex meets both C
vertices, by \(k_v\le1\) on A, so all its common red neighbors are
in B. Therefore \(\sum_B\binom{k_v}{2}=3-b\), giving

\[
 K_2=24-r-2b. \tag{7}
\]

There are r red A--C pairs and \(8-r\) blue ones. At a blue such pair,
\(c_B=20-8-10+c_R=2+c_R\), so its red codegree is \(4-F_{ic}\).
Their total red codegree is consequently \(32-r-Y\). The common
neighbors in A contribute \(\sum_{v\in A}h_vk_v=2r\), while those
in C contribute \(\sum_{v\in C}h_vk_v=r\). Subtracting gives

\[
 H_K=32-4r-Y. \tag{8}
\]

These are literal incidence counts; a Gram matrix is optional notation.
In particular, put \(S=\sum_B\delta_v^2\), \(T=\sum_B\delta_vk_v\).
Equations (6)--(8) give

\[
 S=8+6r-2L-2a-2b+2Y,\qquad T=8-3r-Y+2b. \tag{9}
\]

## Weighted C incidence contradicts the budgets

Since \(h_v=k_v+\delta_v\le2\) and \(\delta_v\ge0\), every B vertex
satisfies \(\delta_vk_v\le2\delta_v-\delta_v^2\). Summing and using
(5) gives

\[
 T\le12-S. \tag{10}
\]

Substitute (9) into (10) to obtain
\(4+3r+Y\le2L+2a\). Combining this with (4) gives

\[
 5r+2Y\le4+2L. \tag{11}
\]

If \(r\ge2\), then \(2L\le r\) and (11) imply
\(4r+2Y\le4\), impossible. If \(r=1\), then \(L=0\), and
(11) implies \(5+2Y\le4\), also impossible.

Finally let \(r=0\). Both C vertices have incident defect zero by (1),
so nonnegativity forces \(b=Y=0\). Equation (9) gives \(T=8\).
Integral nonnegative surpluses satisfy \(\delta_v^2\ge\delta_v\),
so (5) gives \(S\ge6\); (10) then requires \(T\le6\). This last
contradiction proves the lemma in every attachment case.

If A is a cycle, the lemma and (2) now force C blue and \(q_0=12\).
If instead \(q_0=8\), the cited ordinary blue-C lemma forces C red.
Equation (2) makes A a four-edge graph. On four vertices such a graph
is either a cycle (the two missing K4 edges are disjoint) or a paw
(the two missing edges share a vertex). The new lemma excludes the
cycle, proving the stated corollary. It does not assume \(q_0\ge8\)
for all hosts and imports no finite-computation theorem.

## Exact source controls and limits

Use CPython 3.11, standard-library integers, one thread:

```sh
python3 -O degree98_root_eight_cycle_check.py --records /tmp/book-root-cycle-records.json
python3 -O degree98_root_eight_cycle_independent.py --records /tmp/book-root-cycle-records.json --report /tmp/book-root-cycle-audit.json
```

The [primary program](degree98_root_eight_cycle_check.py),
[separate checker](degree98_root_eight_cycle_independent.py), and
[compact expected output](degree98_root_eight_cycle_expected.json) are
standalone. Generated records stay in scratch. Their canonical JSON
SHA-256 is `c25e943c92a6cc6b09dca5dac8107d90336bf579f34add555fcd1e9bb98bc06a`.
The expected output is a comparison target, not missing proof data.

The primary program examines all 256 A--C edge words at a fixed labeled
cycle. There are 81 incident-valid patterns, of which 49 respect opposite
pair saturation. The separate checker independently inspects all 32,768
six-root edge words, finding 243 incident-valid labeled cycle roots and
147 respecting saturation: three labeled cycles times those fixed-cycle
counts. Relabeling any cycle to the fixed labeling requires no symmetry
of the full host. Product capacity domains and recursive remaining-row
capacities separately regenerate all 1,258 root-pair defect states.
Every state with \(S\ge6\), 1,237 states, violates (10), with minimum
integer gap two. All 37 relaxed words with \(h\le2,\delta\ge0\) verify
the pointwise inequality; 29 also avoid the two opposite pairs.

There are also 49 deterministically constructed signed graph controls,
one per fixed-cycle saturated root pattern, with the exact degree
histogram. The separate checker receives these generated graphs and
counts every red and blue page literally. It checks 23,716 F entries,
1,764 Gram entries, 1,078 incident rows, and each aggregate moment.
Their defects may be negative, so neither nonnegative-defect inequalities
nor the outside-cycle degree bound is imposed on them. They validate
identities and are not Ramsey constructions. The separate checker
imports no primary code; every generated record is compared. Explicit
checks remain active under `-O`. These are two implementations by the
same author, not independent peer review.

Cold optimized runs completed in 1.204/0.603 seconds wall time,
0.897/0.524 CPU seconds, with peak child RSS 25,696/28,420 KiB,
primary and separate respectively. They ran sequentially with one
numerical thread and completed without reaching an operational guard.

The [known 21-vertex fixture](baseline21.rows) was freshly matched in all
441 entries with the off-diagonal complement of the authors'
[primary construction](https://github.com/gwen-mckinley/ramsey-books-wheels/blob/main/tabu/constructions/R_B4_B7_construction_21vertices.txt):
93 red edges and page maxima 3/6. This is validation of prior work.
The [primary paper, Table 1](https://arxiv.org/html/2407.07285v2) and
[*Small Ramsey Numbers*, Table IXa](https://www.cs.rit.edu/~spr/ElJC/sur.pdf),
reopened live on 2026-10-01, retain the located interval
\(22\le R(B_4,B_7)\le23\). The published upper certificate was not rerun.

The proof's logical premises are the written degree, pair and incidence
counts above; the corollary also uses the cited ordinary blue-C lemma.
The exact controls are validation, with no computational completeness
bridge needed for the theorem. No proof-assistant formalization,
historical priority classification, new independent peer verdict, full
histogram exclusion, or Ramsey endpoint resolution is asserted.
