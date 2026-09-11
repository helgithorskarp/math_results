# Rigidity of AHT templates with unequal cores

11 September 2026. A general theorem with an ordinary mathematical proof. The accompanying exact code supplies controls and the finite equality classification at uniformity five.

The Abbott–Hanson–Toft (AHT) construction uses a common core hypergraph and matched pairs of new vertices. We allow **every matched pair to have an arbitrary, different core family**, and allow **any transversal family**. We characterize non-two-colorability for this entire template, at every uniformity and on any finite core ground set. A counting theorem, equality characterization, and stability bound follow when the core has size \(2r-3\).

At uniformity five the result is sharp: among all subhypergraphs of the **207-edge template on 17 vertices**, a non-two-colorable example has at least **51 edges**. Every equality example is the classical Fano/parity construction, up to isomorphism. This is a complete construction-template classification. It is **not** a new lower bound for unrestricted \(m(5)\), whose working interval remains \(35\le m(5)\le51\).

## 1. Definition and exact criterion

Let \(r\ge3\), put \(k=r-2\), and let \(X\) be any finite set. Outside \(X\), take disjoint pairs \(P_i=\{a_i,b_i\}\), \(1\le i\le r\). For each \(i\), let \(\mathcal C_i\subseteq\binom Xk\) be an arbitrary simple family, possibly empty. It need not be non-two-colorable. For \(t\in\{0,1\}^r\), let \(E_t\) contain \(a_i\) if \(t_i=0\), and \(b_i\) if \(t_i=1\). Given any \(T\subseteq\{0,1\}^r\), form the \(r\)-uniform hypergraph

\[
 H=\{C\cup P_i:C\in\mathcal C_i,\ 1\le i\le r\}
 \ \cup\ \{E_t:t\in T\}. \tag{1}
\]

These edges are distinct. Let \(F_r\) be the graph on \(\{0,1\}^r\) joining words at Hamming distance one or \(r\): the cube with its antipodal matching added. This explicit definition fixes the graph convention regardless of terminology for folded cubes. Write \(\tau(F_r)\) for its vertex-cover number.

**Theorem 1 (exact decomposition).** The hypergraph (1) is non-two-colorable if and only if both conditions hold:

1. \(T\) is a vertex cover of \(F_r\).
2. For every \(S\subseteq X\) and every ordered pair \(i\ne j\),

\[
 \bigl(\exists C\in\mathcal C_i:C\subseteq S\bigr)
 \quad\text{or}\quad
 \bigl(\exists D\in\mathcal C_j:D\subseteq X\setminus S\bigr). \tag{2}
\]

Each failure gives an explicit proper coloring.

**Proof, necessity.** If \(t\) and its antipode are both outside \(T\), color every pair bichromatically so that its red transversal is \(E_t\). Its blue transversal is the antipode; all other transversals are mixed. Every core edge contains a bichromatic pair. The coloring of \(X\) is arbitrary.

If a cube edge \(t,t\oplus e_i\) is disjoint from \(T\), color \(X\) blue, pair \(P_i\) entirely red, and every other pair bichromatically with its red member chosen according to \(t\). The only monochromatic transversals are the two missing words. Edges using \(P_i\) also contain a nonempty blue \(k\)-set, and all other core edges contain a bichromatic pair. This is proper.

If (2) fails at \(S,i,j\), color \(S\) red and \(X\setminus S\) blue, color \(P_i\) red and \(P_j\) blue, and color the remaining pairs bichromatically. Every transversal sees both colors. A core edge using \(P_i\) or \(P_j\) is mixed by the failed condition, and every other core edge has a bichromatic pair.

**Sufficiency.** Consider any coloring. If all pairs are bichromatic, the two monochromatic transversals are antipodal, and their edge in \(F_r\) meets \(T\). If there are monochromatic pairs of opposite colors, indexed by \(i,j\), condition (2) produces a monochromatic core edge. Otherwise all monochromatic pairs have the same color. The transversals of that color form a nontrivial subcube: their coordinates vary freely at the monochromatic pairs and are fixed elsewhere. This subcube contains a cube edge, which meets \(T\), producing a monochromatic transversal. ∎

The theorem applies to arbitrary core sizes and arbitrary edge counts. It reduces the template's non-two-colorability exactly to a fixed graph-cover condition and cross-cover conditions on its cores. It does not assert that checking (2) is polynomial in an implicit hypergraph input.

## 2. Counting, equality, and stability on a small core ground set

Now assume \(|X|=2k+1=2r-3\). Put

\[
 M=\binom{2r-3}{r-2},\qquad c_i=|\mathcal C_i|,
 \qquad a=\sum_i c_i-M.
\]

**Theorem 2.** If (1) is non-two-colorable, then

\[
 c_i+(r-1)c_j\ge M\quad(i\ne j), \tag{3}
\]

and consequently

\[
 \sum_i c_i\ge M,\qquad |E(H)|\ge M+\tau(F_r). \tag{4}
\]

Moreover the core families satisfy the stability inequality

\[
 \sum_{i<j}|\mathcal C_i\mathbin\triangle\mathcal C_j|
 \le r(r-1)a. \tag{5}
\]

If \(a=0\), all core families are the same family \(\mathcal C\), and \(\mathcal C\) is an **intersecting Steiner system**

\[
 S(k-1,k,2k+1).
\]

Here “Steiner” means that every \((k-1)\)-subset is in exactly one block; “intersecting” means that any two blocks meet. Conversely any such common family satisfies (2).

**Proof of the inequalities.** For every \(k\)-set \(S\subseteq X\), define

\[
 x_i(S)=\mathbf1_{S\in\mathcal C_i},\qquad
 y_j(S)=|\{D\in\mathcal C_j:D\cap S=\varnothing\}|.
\]

Condition (2) implies \(x_i(S)+y_j(S)\ge1\) for \(i\ne j\). Summing over all \(S\) gives (3): an edge of \(\mathcal C_i\) contributes once to the first sum, and an edge of \(\mathcal C_j\) is disjoint from exactly \(k+1=r-1\) such \(S\). Summing (3) over ordered pairs gives

\[
 r(r-1)\sum_i c_i\ge r(r-1)M.
\]

The edges of (1) consist of \(\sum c_i\) core edges and \(|T|\) transversals, proving (4).

For stability, let \(b(S)=\sum_i x_i(S)\), and sum the nonnegative slacks at this \(S\):

\[
 Z(S)=\sum_{i\ne j}(x_i(S)+y_j(S)-1)
 =(r-1)\bigl(b(S)+\sum_jy_j(S)-r\bigr).
\]

We claim \(b(S)(r-b(S))\le Z(S)\). This is immediate if \(b=0\) or \(r\). If \(1\le b\le r-2\), there are at least two indices with \(x_i=0\); hence each \(y_j\ge1\), and \(Z\ge(r-1)b\ge b(r-b)\). If \(b=r-1\), all \(y_j\) except possibly the unique zero index's are at least one, so \(Z\ge(r-1)(r-2)\ge r-1=b(r-b)\). Summing proves (5), since

\[
 \sum_S b(S)(r-b(S))=\sum_{i<j}|\mathcal C_i\triangle\mathcal C_j|,
 \qquad \sum_SZ(S)=r(r-1)a.
\]

**Equality.** If \(a=0\), every slack vanishes. For any two indices \(i,h\), choose \(j\) distinct from both; this is possible because \(r\ge3\). The equalities \(x_i(S)+y_j(S)=x_h(S)+y_j(S)=1\) show that \(x_i(S)=x_h(S)\). Thus all cores coincide, and

\[
 x(S)+y(S)=1\quad\text{for every }S\in\binom Xk. \tag{6}
\]

Two disjoint blocks would violate (6) at one of them. Two distinct blocks meeting in \(k-1\) points have a union of size \(k+1\); its complementary \(k\)-set would have \(y(S)\ge2\), also impossible. Hence every \((k-1)\)-set is in at most one block. Finally

\[
 k|\mathcal C|=\frac{kM}{r}=\binom{2k+1}{k-1},
\]

so every \((k-1)\)-set is in exactly one block.

**Converse.** In an intersecting Steiner system of these parameters, no two blocks can be monochromatic for the same bipartition into a \(k\)-set and a \((k+1)\)-set: opposite-side blocks would be disjoint, and two blocks on the larger side would share \(k-1\) points. Every block is monochromatic in exactly \(k+2=r\) such bipartitions. The block count is \(M/r\), so every balanced bipartition has exactly one monochromatic block.

This also excludes proper unbalanced colorings. If a color class \(A\) has size at most \(k-1\) and its complement contains no block, every \(k\)-set containing \(A\) must be a block, by the balanced case. Two of these \(k\)-sets can be chosen with intersection \(k-1\), contradicting the Steiner property. Thus the common family is non-two-colorable, proving (2). This argument includes \(k=1\): a Steiner system \(S(0,1,3)\) has one singleton block. ∎

For small excess, (5) forces the cores to be close, without assuming that they were identical initially. The constant is an upper bound; optimality of the stability constant is not claimed.

## 3. Odd uniformities and the complete equality form

**Theorem 3.** For odd \(r\ge3\), every non-two-colorable template (1) on a core set of size \(2r-3\) has at least

\[
 B_r=2^{r-1}+\binom{2r-3}{r-2} \tag{7}
\]

edges. Equality holds exactly when all core families coincide with an intersecting \(S(r-3,r-2,2r-3)\), and \(T\) is one of the two parity classes of the \(r\)-cube.

**Proof.** The graph \(F_r\) is connected and \((r+1)\)-regular. For odd \(r\), both distance-one edges and antipodal edges change parity. Either parity class is a vertex cover of size \(2^{r-1}\). Any vertex cover has at least half the vertices, because it must meet every edge and each vertex is in \(r+1\) edges. At equality, every edge has exactly one endpoint in the cover; otherwise the degree sum over the cover would exceed the edge count. Both the cover and its complement are therefore independent, giving a bipartition. Connectivity forces the two parity classes. Combine this with Theorem 2 and its converse. ∎

The theorem does not assert that the Steiner system exists at every odd uniformity. For example, at \(r=9\), equality would require \(S(6,7,15)\). A fixed four-set in that design would lie in

\[
 \frac{\binom{15-4}{6-4}}{\binom{7-4}{6-4}}=\frac{55}{3}
\]

blocks, impossible. Thus every non-two-colorable 9-uniform template in this architecture has at least **6,692** edges, one more than (7). This is a template bound, not a competitive unrestricted bound for \(m(9)\).

For even \(r\), Theorem 1 and Theorem 2 still hold with \(\tau(F_r)\); no formula for that graph parameter is assumed here.

## 4. Uniformity five: 51 edges and one equality type

Set \(r=5\) and \(|X|=7\). There are \(5\binom73=175\) possible core edges and 32 possible transversals, so (1) includes **every subhypergraph of this 207-edge universe**. It permits arbitrary rewiring of all five triple families and arbitrary changes to the transversal family.

Theorem 3 gives \(|E(H)|\ge16+35=51\). Equality forces a common intersecting \(S(2,3,7)\), hence the Fano plane. For completeness, its uniqueness follows directly. The three blocks through a point partition the remaining six points into pairs. Each of the other four blocks meets each pair once. Normalize one such transversal; the pair-cover conditions force the other three transversals, yielding the Fano plane. Equivalently, the four transversals form one parity class on these three pairs.

There are 30 labeled Fano planes on a fixed seven-set, and two parity choices for \(T\), giving exactly **60 equality templates for the fixed labeled decomposition**. All are isomorphic: relabel \(X\), and swap the two vertices of one outer pair to interchange parity. The verifier regenerates the 30 labeled systems by exact pair coverage and checks the entire isomorphism orbit.

The file `witness51.json` is the **classical** construction, included as a positive control, not as a new upper bound. It is a 15-regular 5-uniform hypergraph on 17 vertices. The checker enumerates all 65,536 colorings modulo global color reversal and finds a monochromatic edge in each. It also records a coloring witnessing the necessity of each of its 51 edges through the count of colorings where it is the sole monochromatic edge.

A 50-edge improvement therefore cannot arise merely by making the five seven-point core families unequal or by changing the chosen transversals. It must leave this template, for example by changing the core ground set or the allowed edge forms. This restriction does not cover all known generalizations of AHT.

## 5. Evidence, literature, and scope

`python3 verify.py` uses Python 3.11+ and its standard library. Run without `-O`. It compares the exact criterion to direct coloring coverage for **all 131,072 subtemplates at \(r=3,|X|=3\)**, regenerates all Fano equality types, checks the 51-edge control against every coloring, verifies the counting coefficients and pointwise stability inequalities at several uniformities, and tests explicit coloring witnesses on additional templates. These are controls for the general written proof, not a finite substitute for its arbitrary-parameter quantifiers. `expected.json`, `SHA256SUMS`, and `reproducibility.json` preserve the compact evidence.

The AHT construction and its classical 51-edge example are prior art. Aglave–Amarnath–Shannigrahi–Singh [1], Section 2.2 of the arXiv version (Section 1.1 of the journal article), describe the common-core construction. Their broader constructions and those of Mathews–Panda–Shannigrahi modify allowed edge forms, so our rigidity result is not a claim that such generalizations cannot improve upper bounds. The graph-cover decomposition, unequal-core rigidity, and stability statement here were not located in the primary sources searched. A definitive priority claim is not made. The Fano plane's uniqueness, Steiner counting, cube parity, and the AHT example are not claimed as new.

The unrestricted lower bound \(m(5)\ge35\) from [the preceding package](../gram_incidence/proof.md) is preserved and is not a premise of these theorems. The present work gives neither an unrestricted improvement nor an exact settlement of \(m(5)\). The general proof is unformalized and has not received independent peer review. The finite evidence additionally trusts the supplied Python source, interpreter, and hardware. No solver or omitted large artifact is required to prove or replay this result.

## References

1. S. Aglave, V. A. Amarnath, S. Shannigrahi and S. Singh, *Improved bounds for uniform hypergraphs without property B*, Australasian Journal of Combinatorics 76(1) (2020), 73–86, [journal PDF](https://ajc.maths.uq.edu.au/pdf/76/ajc_v76_p073.pdf); [accessible arXiv full text](https://arxiv.org/html/1602.00218), Sections 2.2–3.
2. K. Grill and D. Linzmayer, *Improved Lower Bounds for Property B*, arXiv:2403.05674v3 (2024), [primary full text](https://arxiv.org/html/2403.05674v3), for the external finite lower-bound context.
