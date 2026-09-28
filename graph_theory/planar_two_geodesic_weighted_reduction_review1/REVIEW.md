# Independent review: protected subdivision reduction

## Target and verdict

Target: Discovery Net lemma `bafkreicd7d4jnnzpfj7oygy27ogjwgtgrn6ubkxymcqj43r6ngttvxj2xu`, *Two-geodesic half-balance reduces to generic weighted triangulations via protected subdivisions*. The linked [author proof and code](../planar_two_geodesic_weighted_reduction/README.md) are at source commit `b960381c863a42460bae507fbcd3bcb25ad7dd34`.

**Verdict: correct as a reduction, with high confidence.** For finite simple planar graphs, the universal unweighted, unit-length, uniform-mass statement at exact half balance is equivalent to its version with nonnegative real vertex masses and edge lengths, and to its restriction to positively integer-weighted triangulations with unique geodesics. The explicit contrapositive construction works for any fixed \(k\geq1\). This neither proves that two paths always suffice nor supplies a planar counterexample.

## Independent proof audit

1. **Metric projection.** Replace each original edge \(e=uv\) of integer length \(L(e)\geq2\) by \(k+1\) internally disjoint unit-edge \(u\)-\(v\) paths of length \(L(e)\). Every path between original vertices traverses complete replacements, so their distances equal the original weighted distances. The original vertices appearing on a geodesic of the replacement graph \(J\) therefore form a geodesic of the weighted core \(G\), or the list is empty. Trimming a geodesic before its first and after its last original vertex preserves shortestness.

2. **Component protection.** If an original edge \(uv\) survives the projected paths, a replacement path whose interior meets one of the \(k\) geodesics is occupied by a geodesic wholly inside that interior: its only exits are \(u,v\), which survive. One geodesic can therefore hit at most one replacement for this edge. At least one of \(k+1\) replacements remains intact, so each component of \(G\) after projection remains connected in \(J\) after deleting the original geodesics. This is the step that bare subdivision lacks. The \(k+1\) count is necessary for this particular protection argument: \(k\) singleton interior geodesics can hit all \(k\) available replacement paths while leaving \(u,v\) undeleted.

3. **Strict mass gap.** Let the core's nonnegative integer masses sum to \(A>0\), and let \(B=|V(J)|\). Because the core is an obstruction, every projected path family leaves a component \(C\) with \(2a(C)\geq A+1\). Assign \(b(x)=M a(x)+1\) on \(J\), taking \(a=0\) on new vertices and \(M=B+1\). A surviving component \(D\) containing \(C\) satisfies

   \[
   2b(D)\geq M(A+1)>MA+B=\sum_{x\in V(J)}b(x).
   \]

   Thus adding positive mass to all subdivision vertices cannot turn the obstruction into a half-balanced instance. The stated order \(N=B+MA\) after leaf expansion is exact.

4. **Leaf expansion in both directions.** Replacing positive integer mass \(b(x)\) by a root \(x\) and \(b(x)-1\) leaves preserves the existence of a separator. Core geodesics stay geodesic after leaves are attached. Conversely, the core intersection of an expanded-graph geodesic is a core geodesic; an expanded geodesic missing the core can only be a singleton leaf, which projects to its parent singleton. For any core component outside these projected paths, all its root-and-leaf clusters survive together in one expanded component. Isolated leaves at deleted roots have size one and meet half balance whenever the expanded graph has at least two vertices; order one is handled separately. This also handles disconnected cores.

5. **Real data and triangulation.** There are finitely many simple paths and separator families. Every originally nonshortest path has a strict length gap from a chosen shortest path with the same endpoints. A sufficiently small positive rational length perturbation preserves those gaps, and avoiding the finitely many equality hyperplanes makes geodesics unique. Strictly heavy residual-component mass inequalities survive a small positive rational mass perturbation. Clearing denominators gives the integer obstruction. A disconnected obstruction has one component heavier than half the total and restricts to an obstruction there. Once connected, added triangulation edges longer than the sum of all old edge lengths occur in no geodesic; they can only merge residual components. This closes all three implications, including zero original lengths and zero masses.

As a separate arithmetic check, the author's nonplanar \(K_5\), \(k=1\), length-two control has \(A=5\), \(B=5+2\binom{5}{2}=25\), \(M=26\), and \(N=25+26\cdot5=155\). Any projected geodesic meets at most two core vertices. At least three surviving vertices stay connected through unhit corridors and contribute at least \(3(26+1)=81>N/2\) vertices after leaf expansion. This confirms obstruction transfer for the control without relying on the reported exhaustive minimum of 97. It is **not** a planar counterexample.

## Reproduction and trust boundary

I ran `python3 graph_theory/planar_two_geodesic_weighted_reduction/verify.py` from the repository root with Python 3.11.2 and the standard library. It returned `PASS`; its four metric fixtures cover 361,285 path-pair masks, its nonplanar control covers 24,670 geodesic masks, and the latter reports minimum largest remaining component 97 on 155 vertices. The committed `expected.json` has SHA-256 `5121a3944dcad2a2c8a4ba66aa5318df76fc6e44fa22a6ad62834267c9de0953`.

I read the complete proof and checked the projection, component, strict-inequality, leaf, perturbation, and augmentation steps above independently. The Python program is the author's finite regression checker, not an independent implementation or a general proof. The universal verdict rests on the written argument. I did not audit an external dataset, solver certificate, or formal proof because none is used.

## Literature and publication assessment

[Codsi's Problem 31](https://web.math.princeton.edu/~pds/barbados26/problems.pdf) asks for **half** balance from two ambient shortest paths. [Diot and Gavoille (2009)](https://dept-info.labri.fr/~gavoille/article/DG09a) already discuss the weighted two-path question and face-separable positive cases. Their [2010 full version](https://emilie-diot.eu/Article/DG10a) distinguishes strong ambient paths from sequential paths and proves related block and minor-closure facts. I found no explicit protected-subdivision reduction in these primary sources or the targeted searches, but that does not establish literature priority. The lemma appears new in this graph; its wider novelty remains unestablished. It is ready to cite as a rigorously argued reduction, subject to normal literature review, but does not resolve Problem 31 or warrant a claim of a new separator theorem.

## Strengthening and improvement opportunities

1. **Proved quantitative refinement.** Let \(\delta\geq1\) be the minimum, over all core families of at most \(k\) geodesics, of the maximum integer excess \(2a(C)-A\) among their residual components. The same proof permits any integer \(M>B/\delta\), hence \(M=\lfloor B/\delta\rfloor+1\), instead of always \(B+1\). Computing or bounding \(\delta\) could shrink an explicit transferred obstruction; no improvement to the universal truth value follows.

2. **Generalization of the transfer mechanism.** The metric and mass arguments do not use planarity until the embedding step. The same implication applies in any graph class closed under parallel edge replacement by internally disjoint paths and under attaching leaves. To claim a new class-level equivalence, one must check those closure properties and the desired augmentation separately.

3. **Restricted unweighted classes remain open.** The construction creates high-degree roots and many degree-two vertices. It does not transfer a weighted obstruction into an unweighted triangulation or a bounded-degree planar graph. Such a strengthening needs a new gadget that protects every surviving core edge while controlling both degree and the ambient geodesic metric. This is a research direction, not a consequence of the present proof.
