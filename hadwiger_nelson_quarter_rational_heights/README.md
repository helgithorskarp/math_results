# Four colours for quarter-localized rational heights

**Full-support theorem.** Put
\[
 A=\mathbb Z_{(2)}=\{u/v:u,v\in\mathbb Z,\ v\text{ odd}\}.
\]
The entire Euclidean unit-distance graph on
\[
 Y=\mathbb R\times\tfrac14 A
\]
is four-colourable. Thus every finite unit-distance graph whose vertices,
after a rigid motion, have rational heights with reduced denominators
divisible by at most \(4\), is four-colourable. Horizontal coordinates are
arbitrary real numbers; there is no bound on the number of lines, extent,
or size of the graph. The support is dense in the plane.

In particular, for **every** rational spacing \(d=p/q>0\) in lowest terms
with \(8\nmid q\), the full support \(\mathbb R\times d\mathbb Z\) is
four-colourable. This includes \(d=1/12,1/36,1/60,\ldots\) and arbitrarily
small spacings. It excludes every finite graph on those supports from the
campaign's five-chromatic target, regardless of vertex count.

This is a written full-support theorem with an exhaustive exact audit of
its modular lemma and additional finite geometric controls. No
five-chromatic candidate or record improvement is claimed. The exact
chromatic number of \(Y\) is only bounded here by \(3\le\chi(Y)\le4\).
There is no claim for all of \(\mathbb R\times\mathbb Q\), for denominators
divisible by \(8\), or for a sharp denominator threshold. In particular,
the theorem does not say that any excluded denominator requires five colours.

## 1. Prior work and relation to the campaign

Axenovich, Choi, Lastrina, McKay, Smith and Stanton,
*On the Chromatic Number of Subsets of the Euclidean Plane*,
Graphs and Combinatorics **30** (2014), 71–81, study radical-coordinate
reductions and congruence colourings. Their Theorem 2.3 gives, among other
conditions, a four-colour bound for integer forbidden distance
\(D\equiv2\pmod4\). The argument below also handles \(D\equiv4\pmod8\),
then passes to arbitrary horizontal coordinates and odd denominators.
Their Theorem 4.3 already gives the exact two-parallel-line classification
used in our earlier package. See the
[authors' manuscript](https://wwwalt.math.kit.edu/iag6/~axenovich/media/euclid-submitted-4-2011.pdf).

The earlier [parallel-line package](../hadwiger_nelson_parallel_line_supports/README.md)
excludes all real equally spaced supports with spacing at least \(1/3\).
This contribution adds an arithmetic exclusion at arbitrarily small
rational spacings; it does not subsume the irrational-spacing result.
The earlier package has received an attribution addendum for Theorem 4.3.
No priority claim is made for the classical methods or for this refinement.

The named objective remains a five-chromatic Euclidean unit-distance graph
on at most 508 vertices. [Parts's primary paper](https://arxiv.org/abs/2010.12665)
gives the 509-vertex baseline, also identified as the record by
[Haugland's August 2026 paper](https://arxiv.org/html/2608.04542v4), checked
on 6 September 2026. HN-2's
[pinned H516-to-H632 homomorphism theorem](../hadwiger_nelson_heule516_host_homomorphisms/README.md)
is separate fixed-support context, not a premise of this proof. The
paired-circle and fixed centered-gadget construction programs remain retired.

## 2. The local congruence lemma

For a positive squarefree integer \(s\), define
\[
 \lambda(s)=
 \begin{cases}
 0,&s\equiv7\pmod8,\\
 1,&s\equiv3\pmod8,\\
 2,&s\not\equiv3\pmod4.
 \end{cases}
\]
These cases exhaust squarefree positive integers, including \(s=1\).
Divisibility and congruences for elements of \(A\) have their usual meaning:
reduce an odd denominator by its inverse modulo the indicated power of two.

**Lemma.** If \(r,b\in A\) and
\[
 r^2+s b^2=16,
 \tag{1}
\]
then
\[
 b\in2^{\lambda(s)}A.
 \tag{2}
\]
Moreover,
\[
 b/2^{\lambda(s)}\in2A\quad\Longrightarrow\quad r\equiv4\pmod{8A}.
 \tag{3}
\]

**Proof of (2).** For \(s\equiv7\pmod8\), there is nothing to prove.
For \(s\equiv3\pmod8\), an odd \(b\) would force odd \(r\) by parity,
and the left side of (1) would be \(1+3=4\pmod8\), a contradiction.
Thus \(b\) is even. Finally, if \(s\not\equiv3\pmod4\), squarefreeness
gives \(s\equiv1\) or \(2\pmod4\). A congruence
\(r^2+s b^2\equiv0\pmod4\) then forces both \(r,b\) even.
Divide (1) by four and repeat this observation. Both are divisible by four.

**Proof of (3).** If \(s\equiv7\pmod8\), the hypothesis says \(b\) is
even, hence \(r\) is even. If \(b/2\) were odd, division of (1) by four
would imply
\((r/2)^2\equiv4-7=5\pmod8\), impossible. Thus \(b\) is divisible by
four. If \(s\equiv3\pmod8\), the hypothesis directly says the same.
In both of these cases (1) modulo sixteen forces \(r\) divisible by four.
Writing \(u=r/4\), \(v=b/4\), we have
\(u^2+s v^2=1\). If \(u\) were even, parity would make \(v\) odd,
and reduction modulo four would give \(3=1\). Consequently \(u\) is odd,
which is (3). In the remaining cases the hypothesis gives \(b=8v\).
Equation (1) forces \(r=4u\) and then
\(u^2+4s v^2=1\); modulo four, \(u\) is odd. This also proves (3). \(\square\)

The lemma includes \(b=0\). This is essential for vertical edges.

## 3. A colouring of the entire support

Scale both coordinates by four. It suffices to colour
\(\mathbb R\times A\) with no monochromatic pair at distance four.
Let
\[
 M=\bigoplus_{\substack{s\ge1\\s\text{ squarefree}}}
       2^{\lambda(s)} A\sqrt{s}\ \subseteq\mathbb R.
\]
The sum means finite sums. Distinct squarefree radicals are linearly
independent over \(\mathbb Q\), so every element of \(M\) has unique
coefficients. For completeness, take the finitely many primes occurring in
any proposed relation. In the multiquadratic field generated by their
square roots, the products indexed by subsets of those primes form a basis;
the independent sign-change automorphisms, or their character averages,
separate each coefficient. This is the standard radical-basis fact used here.

Define an additive map
\[
 \epsilon:M\longrightarrow\mathbb F_2,\qquad
 \epsilon\!\left(\sum_s 2^{\lambda(s)}a_s\sqrt{s}\right)
       =\sum_s (a_s\bmod2A).
\]
Reduction modulo \(2A\) is well defined since every denominator in \(A\)
is odd. Choose one representative \(t\) of every additive coset of \(M\)
in \(\mathbb R\). The choice of these representatives is an explicit use
of choice; no measurable or Borel colouring is asserted.

For \(z\in A\), let \(\rho(z)\in\{0,\ldots,7\}\) be its residue
modulo \(8A\), and put
\[
 h(z)=\lfloor\rho(z)/4\rfloor\in\{0,1\}.
\]
In particular, adding \(4\pmod{8A}\) flips \(h\).
The four-colouring is
\[
 C(x,z)=\bigl(\epsilon(x-t),\ h(z)\bigr),\qquad x\in t+M.
 \tag{4}
\]

**Every distance-four edge is separated.** Let its vertical displacement
be \(r=u/v\in A\), with odd \(v\). Its horizontal displacement \(w\)
satisfies \(w^2=16-r^2\ge0\). If \(w\ne0\), factor the nonnegative
integer \(16v^2-u^2\) as \(m^2s\) with squarefree \(s\), so
\(w=b\sqrt{s}\), where \(b=\pm m/v\in A\). The lemma says
\(w\in M\). If \(w=0\), this is automatic. Hence the edge endpoints
belong to the same horizontal coset; its representative cancels from (4).

For \(w\ne0\), if \(b/2^{\lambda(s)}\) is odd, the first bit changes.
Otherwise (3) says that \(r\equiv4\pmod{8A}\), so the second bit changes.
If \(w=0\), the displacement is \(r=\pm4\), and the second bit changes
directly. Thus (4) separates every edge. Scaling back proves the theorem.

The unit triangle with physical vertices
\((0,0),(0,1),(\sqrt3/2,1/2)\) belongs to \(Y\), so
\(\chi(Y)\ge3\). No four-chromatic lower bound is established here.

## 4. Corollaries and the next boundary

If \(p/q\) is reduced and \(8\nmid q\), then \(p/q\in\tfrac14 A\),
so \(\mathbb R\times(p/q)\mathbb Z\subseteq Y\). The assertion is about
the **full** support, with arbitrary real horizontal coordinates, rather
than only the radical module containing the origin.

An equivalent integer-distance consequence is useful for generators:
for any finite squarefree set \(S\) and positive integer \(D\) with
\(8\nmid D\), the distance-\(D\) graph on
\(\mathbb Z\times\sum_{s\in S}\mathbb Z\sqrt{s}\) is four-colourable.
Divide coordinates by \(D\) and rotate to put the rational coordinate
in the vertical position. There is no claim about the exact chromatic number
of each such graph.

A useful combined filter uses the classical three-colour condition
\(3\nmid D\) in Axenovich et al., Theorem 2.3. Their radical reduction
(Theorem 2.1) applies to each finite connected subgraph of a rationally
spaced support. Consequently a five-chromatic candidate on a rational
comb \(\mathbb R\times(p/q)\mathbb Z\) can survive these exclusions
only if \(24\mid q\). This is a necessary condition, not an existence
claim or a classification of the surviving denominators. The combined
filter uses that cited three-colour theorem; our four-colour proof above
is self-contained apart from the stated algebraic and choice premises.

This pass stops at the denominator valuation-two boundary. Denominators
divisible by eight remain outside this theorem; no search or proof phase
for them has been started. The result also leaves open arbitrary irrational
height patterns. A subsequent campaign pass must reassess construction
value rather than enumerate more finite samples of the excluded support.

## 5. Reproduction and trust boundary

Run from this directory with Python 3.11 or later, standard library only:

```sh
python3 build.py --out out/producer
cmp certificate.json out/producer/certificate.json
python3 verify.py --certificate certificate.json --out out/check
python3 -O verify.py --certificate certificate.json --out out/optimized
cmp out/check/report.json out/optimized/report.json
sha256sum -c SHA256SUMS
```

The producer and verifier import neither each other nor a previous package.
The producer multiplies sparse squarefree radicals using gcd extraction;
the verifier uses sets of prime factors with symmetric-difference products
and directly expands every pair's squared distance. Coordinates in the
certificate's fixtures are scaled by four: the checker tests squared
distance **16**, corresponding exactly to physical unit distance.
Both compute every fixture edge, not just the originally generating edges.

The modular audit covers all \(48\cdot64^2=196{,}608\) residue triples
\((s,r,b)\pmod{64}\) with \(4\nmid s\). This includes all squarefree
classes and additional harmless nonsquarefree representatives. Exactly
6,144 satisfy \(r^2+s b^2=16\pmod{64}\); all satisfy (2) and (3).
Reduction \(A\to\mathbb Z/64\mathbb Z\) preserves these conclusions,
including the normalized coefficient parity. Thus this is an exhaustive
finite check of the local lemma. The infinite colouring still requires
the written radical-basis and coset arguments above.

Seven deterministic fixtures have 1,000 vertices in total, in **separate**
graphs, and 1,813 exact unit edges among 84,460 inspected point pairs.
These include 528 vertical edges and 656 edges on which the first colour
bit is unchanged. They include negative coordinates,
mixed odd denominators, all three radical classes, triangles and vertical
edges. The rational step controls run through reduced odd denominators at
most 31: 3,408 signed steps give 27,264 initial-residue checks. Ten malformed
certificate or module controls are rejected. A greedy use of four
colours would not prove a four-chromatic lower bound; no such inference is
made from these fixtures either.

[certificate.json](certificate.json) records the colour words and geometry
hashes. [expected.json](expected.json) and [validation.json](validation.json)
record the independently reconstructed counts, malformed controls, interpreter
versions and replay results. The certificate is 4,125 bytes with SHA-256
`39ac38b30ae5999d83e38b236e8bd00d479a2763d159ef219778abbef7b62c14`.

There are no floating-point geometric comparisons, native solver calls,
external graph inputs, or omitted large certificates. Operational trust is
Python exact integer/rational arithmetic and faithful source execution.
Mathematical trust includes the written proofs, the standard independence
of squarefree radicals, and choice of coset representatives. The checks are
author-run with different representations, not independent-author review
or proof-assistant formalization. External review is pending.
