# An arithmetic gap in every even-uniform unequal-core AHT template

## 1. Template and statement

Fix an even integer \(r\ge 4\), put

\[
 k=r-2,\qquad |X|=2r-3=2k+1,
 \qquad M=\binom{2r-3}{r-2}.
\]

Outside \(X\), take disjoint pairs \(P_i=\{a_i,b_i\}\),
\(1\le i\le r\).  For every \(i\), let
\(\mathcal C_i\subseteq\binom Xk\) be arbitrary; the families may be
different.  For \(t\in\{0,1\}^r\), let \(E_t\) choose one vertex from each
pair according to \(t\).  Given arbitrary \(T\subseteq\{0,1\}^r\), form

\[
 \mathcal H=
 \{C\cup P_i:C\in\mathcal C_i,\ 1\le i\le r\}
 \cup\{E_t:t\in T\}.                                      \tag{1}
\]

Let \(F_r\) be the graph on \(\{0,1\}^r\) whose edges join words at Hamming
distance one or \(r\).  Thus \(F_r\) is the \(r\)-cube with its antipodal
matching added.  Define

\[
 \varepsilon_r=
 \begin{cases}
 r/2,&r\text{ is a power of two},\\
 1,&r\text{ is not a power of two}.
 \end{cases}                                               \tag{2}
\]

**Theorem.**  If (1) is non-two-colorable, then

\[
 |\mathcal H|\ \ge\
 \binom{2r-3}{r-2}+2^{r-1}
 +\frac12\binom r{r/2}+\varepsilon_r.                      \tag{3}
\]

The result is sharp at \(r=4\): both sides of (3) equal \(23\).

The first three terms in (3) are the earlier counting-plus-vertex-cover
bound.  The contribution here is the positive arithmetic gap
\(\varepsilon_r\), valid uniformly at every even rank.  This is a theorem
about the template (1), not an unrestricted lower bound for the Property B
number \(m(r)\).  Sharpness is not claimed when \(r>4\).

## 2. Two necessary conditions

Write \(c_i=|\mathcal C_i|\).  Non-two-colorability of (1) implies the
following two conditions.

First, \(T\) is a vertex cover of \(F_r\).  Indeed, if an antipodal edge
\(t,\bar t\) is missed, color every pair bichromatically so that the red and
blue transversals are \(E_t\) and \(E_{\bar t}\).  Every core edge contains a
bichromatic pair and every selected transversal is mixed.  If a cube edge
\(t,t\mathbin\oplus e_i\) is missed, color \(P_i\) red, color every other
pair bichromatically so that the only all-red transversals are those two, and
color \(X\) blue.  Again all edges are mixed.  Either omission would give a
proper coloring.

Second, for every \(S\subseteq X\) and every ordered pair \(i\ne j\),

\[
 \text{some }C\in\mathcal C_i\text{ lies in }S
 \quad\text{or}\quad
 \text{some }D\in\mathcal C_j\text{ lies in }X\setminus S. \tag{4}
\]

Otherwise color \(S\) red and its complement blue, color \(P_i\) red and
\(P_j\) blue, and color all other pairs bichromatically.  Every transversal
is mixed; (4)'s failure makes the edges using \(P_i\) and \(P_j\) mixed; and
every remaining core edge contains a bichromatic pair.

For a \(k\)-set \(S\), put

\[
 x_i(S)=\mathbf1_{S\in\mathcal C_i},\qquad
 y_j(S)=|\{D\in\mathcal C_j:D\cap S=\varnothing\}|.
\]

Condition (4) gives \(x_i(S)+y_j(S)\ge1\).  Summing over all \(k\)-sets
\(S\) counts an edge of \(\mathcal C_i\) once and an edge of
\(\mathcal C_j\) exactly \(k+1=r-1\) times.  Hence

\[
 c_i+(r-1)c_j\ge M\qquad(i\ne j).                           \tag{5}
\]

Summing (5) over ordered pairs yields

\[
 \sum_{i=1}^r c_i\ge M.                                    \tag{6}
\]

We will also need the equality case.  If equality holds in (6), the sum of
all pointwise nonnegative slacks \(x_i(S)+y_j(S)-1\) is zero.  Thus

\[
 x_i(S)+y_j(S)=1\qquad(S\in\tbinom Xk,\ i\ne j).            \tag{7}
\]

For any \(i,h\), choose \(j\) distinct from both.  Equation (7) gives
\(x_i(S)=x_h(S)\), so all core families coincide with a family
\(\mathcal C\).  Then \(x(S)+y(S)=1\).  This excludes disjoint blocks and
also excludes two blocks meeting in \(k-1\) points (use the complementary
\(k\)-set of their \((k+1)\)-point union).  Every \((k-1)\)-set is therefore
in at most one block.  Equality in (6) gives \(|\mathcal C|=M/r\), and

\[
 k|\mathcal C|=\binom{2k+1}{k-1},
\]

so every \((k-1)\)-set is in exactly one block.  Consequently equality in
(6) requires an intersecting Steiner system

\[
 S(k-1,k,2k+1).                                             \tag{8}
\]

This recovers, in the amount needed below, the necessary half of the exact
unequal-core criterion and its equality rigidity.

## 3. The classical folded-cube constant

The graph \(F_r\) is the Cayley graph of \(\mathbb F_2^r\) with connection
set \(\{e_1,\ldots,e_r,\mathbf1\}\).  A character indexed by a word of
weight \(s\) is an adjacency eigenvector with eigenvalue

\[
 \lambda_s=r-2s+(-1)^s                                      \tag{9}
\]

and multiplicity \(\binom rs\).  Because \(r\) is even, (9) is positive
for \(s<r/2\), negative for \(s>r/2\), and equals
\((-1)^{r/2}\ne0\) in the middle layer.  Therefore the smaller of the
positive and negative inertia counts is

\[
 2^{r-1}-\frac12\binom r{r/2}.                              \tag{10}
\]

The inertia bound gives \(\alpha(F_r)\) at most (10).  For completeness,
this bound is the elementary consequence of interlacing obtained by taking
the zero principal adjacency submatrix on an independent set: its order
cannot exceed either the number of positive or the number of negative
eigenvalues of the full adjacency matrix.

The bound is attained.  Put \(h=r/2\) and take all words of even weight below
\(h\), together with all words of odd weight above \(h\).  Cube edges reverse
parity.  Antipodal edges preserve parity because \(r\) is even and exchange
the regions below and above \(h\).  The displayed set is therefore
independent.  Complementation pairs the low and high layers while preserving
parity, so its size is the total number of words below the middle layer,
namely (10).  Thus the classical exact formula is

\[
 \alpha(F_r)=2^{r-1}-\frac12\binom r{r/2},\qquad
 \tau(F_r)=2^{r-1}+\frac12\binom r{r/2}.                    \tag{11}
\]

Formula (11) is prior art.  In folded-cube terminology, \(F_r\) is the
folded \((r+1)\)-cube.  The same even-\(r\) transversal count already occurs
in Toft's classical AHT construction; see the literature discussion below.

## 4. Catalan parity and the unavoidable core gap

Let \(C_n=\frac1{n+1}\binom{2n}{n}\) be the \(n\)-th Catalan number.  The
elementary identity

\[
 M=\binom{2r-3}{r-2}
   =\frac12\binom{2r-2}{r-1}
   =\frac r2 C_{r-1}                                       \tag{12}
\]

reduces \(M\bmod r\) to Catalan parity.

We recall a short proof of that parity.  If \(s_2(n)\) is the number of ones
in the binary expansion of \(n\), Legendre's formula gives

\[
 \nu_2\binom{2n}{n}=s_2(n).
\]

Writing \(a=\nu_2(n+1)\), the binary expansion of \(n\) ends in \(a\) ones,
so \(s_2(n+1)=s_2(n)-a+1\).  Hence

\[
 \nu_2(C_n)=s_2(n)-\nu_2(n+1)=s_2(n+1)-1.
\]

Thus \(C_n\) is odd exactly when \(n+1\) is a power of two.  Applied to
\(n=r-1\), (12) yields

\[
 M\equiv
 \begin{cases}
 r/2\pmod r,&r\text{ is a power of two},\\
 0\pmod r,&r\text{ is not a power of two}.
 \end{cases}                                               \tag{13}
\]

Suppose first that \(r\) is a power of two, and write
\(M=rq+r/2\).  Let \(m=\min_i c_i\).  If \(m\ge q+1\), then

\[
 \sum_i c_i\ge r(q+1)=M+r/2.                               \tag{14}
\]

If \(m\le q\), choose \(j\) with \(c_j=m\).  Inequality (5) gives
\(c_i\ge M-(r-1)m\) for every \(i\ne j\), whence

\[
 \sum_i c_i
 \ge m+(r-1)(M-(r-1)m)
 \ge M+\frac{r(r-2)}2
 \ge M+\frac r2.                                           \tag{15}
\]

Therefore the core part has at least \(M+r/2\) edges.

Now suppose that even \(r\) is not a power of two.  Equation (13) says that
\(M\) is divisible by \(r\).  Equality in (6), however, would require the
Steiner system (8).  Such a system cannot exist when \(k=r-2\) is even:
double-counting extensions of a fixed \((k-2)\)-set gives its replication
number

\[
 \frac{\binom{(2k+1)-(k-2)}{(k-1)-(k-2)}}
            {\binom{k-(k-2)}{(k-1)-(k-2)}}
 =\frac{k+3}{2},                                           \tag{16}
\]

which is not an integer.  Hence (6) is strict, and integrality gives

\[
 \sum_i c_i\ge M+1.                                       \tag{17}
\]

Combining (14)--(17) with \(|T|\ge\tau(F_r)\) from (11) proves (3).

## 5. Sharpness at uniformity four

For \(r=4\), we have \(M=\binom52=10\), \(\tau(F_4)=11\), and
\(\varepsilon_4=2\), so (3) gives \(23\).

Take the same triangle graph as each \(\mathcal C_i\), embedded on three of
the five points of \(X\), and take \(T\) to be the complement of the
five-vertex independent set in \(F_4\) constructed in Section 3.  The common
triangle has no proper two-coloring, so condition (4) holds for every
bipartition of \(X\); the chosen \(T\) is a vertex cover.  The exact AHT
criterion then makes (1) non-two-colorable.  It has

\[
 4\cdot3+11=23
\]

edges, proving sharpness at \(r=4\).  This is the classical Toft endpoint,
not a newly claimed 23-edge construction.

## 6. Literature status and scope

The exact folded-cube independence number is classical.  It is commonly
attributed to Chris Godsil's 2006 manuscript *Interesting Graphs and Their
Colourings*, Sections 7.6--7.7; the formula and attribution are recorded on
[MathWorld's folded-cube page](https://mathworld.wolfram.com/FoldedCubeGraph.html).
The spectral proof in Section 3 is included so that this package does not
depend on an inaccessible manuscript.

For Property B provenance, S. Aglave, V. A. Amarnath, S. Shannigrahi and
S. Singh, *Improved bounds for uniform hypergraphs without property B*,
Australasian Journal of Combinatorics 76(1) (2020), 73--86,
[journal PDF](https://ajc.maths.uq.edu.au/pdf/76/ajc_v76_p073.pdf),
Section 1.1, records Toft's even-uniform AHT transversal term
\(2^{r-1}+\frac12\binom r{r/2}\).  Neither that classical constant nor the
Catalan parity fact is claimed new.

The prerequisite unequal-core counting and equality argument is reproduced
above, but its more general exact criterion and stability theorem are in
[Unequal-core AHT templates: exact criterion and rigidity](https://github.com/helgithorskarp/math_results/tree/main/combinatorics/property_b_m5/template_rigidity).

Targeted searches of the cited primary material and current folded-cube/AHT
literature did not locate the combined gap (2)--(3).  Novelty is therefore
search-relative, not a claim of historical priority.  The theorem is
unformalized and awaits independent review.  It does not improve an
unrestricted lower bound for \(m(r)\), and it does not assert attainability of
(3) for even \(r>4\).

No software, finite census, solver, external dataset, or omitted certificate
is used.  The result is the written uniform proof.
