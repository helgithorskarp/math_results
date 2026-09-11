# Every 32-edge 5-uniform hypergraph has Property B

11 September 2026. Computer-assisted proof, accompanied by a complete exact replay.

**Theorem.** Every finite simple 5-uniform hypergraph with at most 32 edges has a proper two-coloring. Consequently, \(m(5)\ge33\), where \(m(5)\) is the minimum number of edges of a non-two-colorable 5-uniform hypergraph.

A proper two-coloring assigns red or blue to every vertex and leaves no monochromatic edge. The theorem has no restriction on the vertex count, degrees, symmetry, or intersections of edges.

## 1. Reduction to pair-covered hypergraphs

Suppose a counterexample with at most 32 edges exists. Remove isolated vertices. Whenever two vertices share no edge, identify them. Each edge retains five distinct vertices, and any proper coloring of the quotient lifts to a proper coloring of the original. Coalesce duplicate edges. Repetition terminates at a non-two-colorable simple hypergraph in which every pair of vertices belongs to an edge; call this *pair-covered*.

There must be at least nine vertices: at most eight vertices can be split into two classes of size at most four. Pad the quotient to exactly 32 distinct edges on its existing vertices. There are enough five-subsets since \(\binom95>32\). Padding preserves pair coverage and non-two-colorability. Write \(v\) for its number of vertices. Then

\[
\binom v2\le32\binom52=320,
\]

so \(v\le25\). In a uniformly random balanced coloring, a fixed edge is monochromatic with probability

\[
\frac{\binom{\lfloor v/2\rfloor}5+\binom{\lceil v/2\rceil}5}{\binom v5}.
\]

Multiplying by 32 gives a number strictly below one for every \(9\le v\le18\), checked by integer inequalities in the replay. Hence it remains to consider \(19\le v\le25\). Every vertex has degree at least \(\lceil(v-1)/4\rceil\), and the sum of degrees is 160.

These reductions are standard; see Grill–Linzmayer [1]. We include them to make the scope of the certificate explicit and avoid assuming any previous lower bound for \(m(5)\).

## 2. A conditional random-order coloring bound

Given an ordering of the vertices, start with all vertices red. Process vertices in order, changing a vertex to blue precisely when it is the last vertex of an edge whose other vertices are all still red. No edge is red at the end. If an edge \(F\) is blue at the end, let \(u\) be its first vertex. When \(u\) became blue, some edge \(E\) had all its other vertices earlier and red. Thus

\[
E\cap F=\{u\},\qquad \max E=u=\min F.
\]

Call such an ordered edge pair a critical pair. It suffices to show that some ordering has no critical pair. This greedy obstruction and conditioning on marked vertices extend the method of [1]; they are not claimed as new principles.

Fix \(s\) labeled marked vertices at distinct positions \(p_0,\ldots,p_{s-1}\) of an ordering, with positions numbered from zero. Uniformly permute the remaining \(N=v-s\) vertices over the free positions. For \(A\subseteq\{0,\ldots,s-1\}\), let \(x_A\) be the number of edges whose intersection with the marked vertices is exactly \(A\). Sets \(A\) are represented by bit masks in the code.

All probabilities below have common denominator \(N!\). Write \((q)_t=q!/(q-t)!\) if \(0\le t\le q\), and zero otherwise. At a position \(k\), let \(L\) and \(R\) be the numbers of free positions strictly before and after \(k\). For edge traces \(A,B\), put \(a=5-|A|\), \(b=5-|B|\).

If \(k\) is free, trace \(A\) is eligible to be last at \(k\) only when all its marked positions are before \(k\) and \(a\ge1\). Its single-edge probability numerator is

\[
\alpha_A(k)=a(L)_{a-1}(N-a)!.
\]

For being first, require all marked positions after \(k\), and use
\(\beta_B(k)=b(R)_{b-1}(N-b)!\).
For a *particular* ordered pair of edges intersecting in exactly one free vertex, with eligible disjoint traces, the critical-pair probability numerator is

\[
\gamma_{AB}(k)=(L)_{a-1}(R)_{b-1}(N-a-b+1)!.
\]

The common vertex is fixed for that particular pair; there is no additional choice of a common vertex. Impossible configurations contribute zero.

If \(k=p_i\) is marked, eligibility instead requires that the trace contain \(i\) and its other marked vertices lie on the appropriate side. The respective single-edge numerators are

\[
\alpha_A(k)=(L)_a(N-a)!,\qquad
\beta_B(k)=(R)_b(N-b)!.
\]

For \(A\cap B=\{i\}\), the probability numerator for a particular pair intersecting exactly in the marked vertex is

\[
\gamma_{AB}(k)=(L)_a(R)_b(N-a-b)!.
\]

Other trace pairs contribute zero. These formulas count injective assignments of the specified free vertices, followed by arbitrary permutations of all remaining vertices.

Define

\[
U_k=\sum_A x_A\alpha_A(k),\quad
V_k=\sum_B x_B\beta_B(k),\quad
W_k=\sum_{A,B}x_A(x_B-\mathbf1_{A=B})\gamma_{AB}(k),
\]

with sums only over eligible traces. There are at most \(x_A(x_B-\mathbf1_{A=B})\) distinct ordered edge pairs of those traces. Pairs with extra intersections cannot be critical, so including them only increases this upper bound. A critical pair at \(k\) requires a last edge and a first edge. The union bounds on each necessary event and on the pairs therefore give

\[
\Pr(\text{greedy failure})\le
B(v,x,p):=\frac1{N!}\sum_{k=0}^{v-1}
\min\{U_k,V_k,W_k,N!\}. \tag{1}
\]

In particular, any exact evaluation \(B<1\) proves colorability. Neither independence of edges nor realizability of an arbitrary trace vector is assumed. The default positions in the replay are the consecutive central positions starting at \(\lfloor(v-s)/2\rfloor\). Subsets and permutations of the marked vertices are also allowed. For a subset, its trace counts are obtained by summing the original counts over projections.

## 3. A link collision correction for 19–21 vertices

Let a vertex \(u\) have degree \(d\). Its incident edges give \(d\) distinct four-subsets of the other vertices, covering all \(v-1\) of them. If a vertex occurs in \(c\ge1\) link edges, it contributes \(c-1\) to the incidence excess and \(\binom c2\ge c-1\) to the sum of pairwise intersection sizes. That sum is therefore at least

\[
e=4d-(v-1).
\]

Two distinct four-subsets intersect in at most three vertices, so at least \(\lceil e/3\rceil\) unordered link pairs intersect. Thus at most

\[
d(d-1)-2\lceil e/3\rceil
\]

ordered pairs of edges through \(u\) intersect exactly in \(u\).

Mark only a vertex of minimum degree, at the central position. At that position replace the coefficient \(d(d-1)\) in \(W_k\) by this improved upper bound; keep (1) at every other position. Exact evaluation over
\(\lceil(v-1)/4\rceil\le d\le\lfloor160/v\rfloor\) gives:

| \(v\) | Maximum failure bound |
|---|---:|
| 19 | \(11478/12155\) |
| 20 | \(230202/230945\) |
| 21 | \(8337/8398\) |

Each is strictly below one. This excludes every candidate in these three vertex counts.

## 4. Complete trace coverage for 22–24 vertices

Take three vertices of least degrees \(a\le b\le c\), breaking ties arbitrarily. Enumerate precisely the ranges

\[
\lceil(v-1)/4\rceil\le a\le\lfloor160/v\rfloor,\quad
 a\le b\le\left\lfloor\frac{160-a}{v-1}\right\rfloor,\quad
 b\le c\le\left\lfloor\frac{160-a-b}{v-2}\right\rfloor.
\]

These upper bounds follow because all not-yet-chosen vertices have degree at least the next least degree. The pair codegrees \(q_{12},q_{13},q_{23}\) range from one to the smaller endpoint degree. The triple codegree \(t\) ranges from zero to their minimum. They uniquely specify the eight trace counts:

\[
\begin{aligned}
x_{123}&=t,&x_{12}&=q_{12}-t,&x_{13}&=q_{13}-t,&x_{23}&=q_{23}-t,\\
x_1&=a-q_{12}-q_{13}+t,&
x_2&=b-q_{12}-q_{23}+t,&
x_3&=c-q_{13}-q_{23}+t,\\
x_\varnothing&=32-\sum_{A\ne\varnothing}x_A.
\end{aligned}
\]

Retain nonnegative vectors satisfying the marked-to-outside coverage inequalities below. Every real candidate has one of these vectors.

For any vector not yet certified colorable, add the next least-degree vertex. If the current \(s\) degrees are \(d_1\le\cdots\le d_s\), its degree satisfies

\[
d_s\le d\le\left\lfloor\frac{160-\sum_i d_i}{v-s}\right\rfloor.
\]

For every existing trace \(A\), enumerate the number \(y_A\) of its edges containing the new vertex, with \(0\le y_A\le x_A\) and \(\sum_Ay_A=d\). The extended traces are \(x_A-y_A\) and \(y_A\), respectively without and with the new vertex. This enumerates every possible extension, including some unrealizable ones.

With \(N=v-s\) outside vertices, discard an extension only if it violates at least one of these necessary conditions:

- no positive trace has more than five marked vertices;
- every marked pair belongs to at least one edge;
- for each marked \(i\), \(\sum_{A\ni i}x_A(5-|A|)\ge N\);
- \(\sum_Ax_A\binom{5-|A|}{2}\ge\binom N2\).

The last two count incidences covering marked-to-outside and outside-to-outside pairs. Overcounting a pair is permitted, so these are necessary, not sufficient, conditions.

At every retained vector, the verifier tries (1) on every subset of the marked vertices and every assignment to the central positions. At five marked vertices, it also uses the 13 explicit noncentral certificates in `certificates.json`, after canonical relabeling. Each certificate is independently reevaluated with integer arithmetic; its stated numerator and denominator must agree exactly. No search heuristic runs in the verification.

The complete replay gives the following counts. A vector certified at an earlier depth needs no extensions.

| \(v\) | Marked vertices | Vectors visited | Certified colorable |
|---|---:|---:|---:|
| 22 | 3 | 497 | 479 |
| 22 | 4 | 7,510 | 7,487 |
| 22 | 5 | 43,815 | 43,815 |
| 23 | 3 | 121 | 102 |
| 23 | 4 | 3,444 | 3,426 |
| 23 | 5 | 20,218 | 20,218 |
| 24 | 3 | 8 | 0 |
| 24 | 4 | 72 | 72 |

The integer loops and filters have been specified above. Thus each actual hypergraph follows a retained branch until it is certified colorable, or would reach an unclosed vector at depth five. The latter causes the verifier to fail and never occurs. These counts cover the whole vertex-count classes, not selected degree profiles.

## 5. Twenty-five vertices and a seven-vertex contradiction

Here every degree is at least six, and
\(\sum_u(d(u)-6)=160-150=10\). At most ten vertices have degree above six; at least fifteen have degree six. A degree-six vertex has 24 link incidences covering 24 other vertices. Consequently, it shares exactly one edge with each other vertex.

Choose any six degree-six vertices, forming \(S\). The traces on \(S\) of size at least two partition all 15 pairs of \(S\) into complete graphs with block sizes two through five. No such trace repeats. Conversely a pair partition determines its entire trace vector: a block has count one, a singleton \(i\) has count six minus the number of blocks containing \(i\), and the empty trace has count 32 minus all nonempty counts.

There are 352 labeled pair partitions and nine types up to permutations of the six vertices. For completeness, the verifier generates all of them by choosing the block containing the first uncovered pair and recurring on the remaining pairs. An independent enumeration selects pair-disjoint blocks of size at least three and then fills the remaining pairs with two-element blocks; the resulting labeled sets agree exactly.

Here are the nine canonical types. Only blocks of size at least three are shown; all uncovered pairs are two-element blocks. Vertex labels in this table are 1–6; ordering positions remain zero-based. The position vector lists the positions of vertices 1–6.

| Large blocks | Position vector | Bound (1) |
|---|---|---:|
| 23456 | (9,10,11,12,13,14) | \(3899/4199\) |
| 126, 3456 | (9,11,8,12,13,14) | \(4094/4199\) |
| 124, 135, 236, 456 | (9,10,13,12,11,14) | \(243/247\) |
| 3456 | (13,10,11,12,9,14) | \(4074/4199\) |
| 145, 246, 356 | (12,10,9,11,13,14) | \(8345/8398\) |
| 236, 456 | (12,10,11,14,13,9) | \(4188/4199\) |
| 123, 456 | (9,13,11,12,10,14) | \(8405/8398\) |
| 456 | (9,14,11,12,13,10) | \(8393/8398\) |
| none | (9,10,11,12,13,14) | \(4188/4199\) |

Eight types have bound less than one. A non-two-colorable hypergraph must therefore induce the remaining type on **every** six degree-six vertices. This type has exactly two disjoint three-element traces and no larger trace.

Choose seven degree-six vertices, forming \(T\). No edge can meet \(T\) in four or more vertices: some six-subset would then have a trace of size at least four. Let \(q\) be the number of edges meeting \(T\) in exactly three vertices. Each of the seven six-subsets has exactly two triple traces. Each of the \(q\) edges contributes a triple trace to exactly four six-subsets, obtained by deleting one of the four vertices outside its triple. Counting these incidences gives

\[
4q=7\cdot2=14,
\]

which is impossible. This excludes all 25-vertex candidates and completes the theorem.

## 6. Verification and trust boundary

Run `python3 verify.py` with Python 3.11 or later, without `-O`. Only the standard library is required. The exact expected output is `EXPECTED_OUTPUT.json`; the README gives a comparison command. All probability computations use integers or exact rational numbers.

In addition to the complete proof replay, `audit.py` checks every coefficient configuration used by deriving the probabilities independently as ratios of binomial coefficients. It checks 5,280 event counts against direct permutations of six vertices, all 1,024 three-uniform hypergraphs on five vertices against their actual two-colorings, and the link collision inequality on 32,596 covering link families. The noncolorable small controls must never receive a coloring certificate. These controls test the formulas; the exhaustive loops and mathematical reductions above establish coverage at uniformity five.

This is a computer-assisted proof with human arguments for the reduction, probability inequality, coverage, and final divisibility obstruction. It has not been formalized in a proof assistant or independently peer reviewed. Its computational trust boundary is the supplied Python source, the Python interpreter, and ordinary hardware arithmetic. It requires no external solver, opaque search output, downloaded input, or omitted large certificate.

## 7. Relation to prior work

[1] Karl Grill and Daniel Linzmayer, *Improved Lower Bounds for Property B*, arXiv:2403.05674v3 (20 June 2024), [full text](https://arxiv.org/html/2403.05674v3). Theorem 1 gives \(m(5)\ge32\); Table 1 records the upper bound 51. Their method already fixes up to three vertices and uses exact finite calculations. The present claim is the numerical improvement to 33. It combines additional marked-vertex trace coverage with a global seven-vertex obstruction; it does not claim the original random-order method, pair contraction, or balanced-coloring reduction.

[2] Sachin Aglave, V. A. Amarnath, Saswata Shannigrahi, and Shwetank Singh, *Improved bounds for uniform hypergraphs without property B*, Australasian Journal of Combinatorics 76(1) (2020), 73–86, [journal PDF](https://ajc.maths.uq.edu.au/pdf/76/ajc_v76_p073.pdf). Section 1.1 describes the Abbott–Hanson–Toft construction giving 51 edges. We make no improvement to that upper bound.

The located primary-source baseline is \(32\le m(5)\le51\); combined with this theorem the interval becomes \(33\le m(5)\le51\). A live literature audit on 11 September 2026 found no prior bound 33. Only the abstract and references of the 2026 Grill–Linzmayer overview (DOI 10.1007/978-3-032-18810-6_9) were accessible; its numerical tables were not checked. Priority remains subject to that limitation and ordinary review. The exact value of \(m(5)\) is not determined here.
