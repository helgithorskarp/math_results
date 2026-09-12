# The complete long-chain case at excess five

Let \(n\ge5\), \(m=2^{n-2}\), and \(N=4m+5=2^n+5\). An
\(n\)-element subset \(A\) of \(\mathbb Z/N\mathbb Z\) is **sum-distinct**
if its \(2^n\) subset sums, including the empty sum, are distinct.
Write \([a]=\{a,-a\}\). Equivalence allows a common unit dilation and
independent changes of element signs; it does not include translating \(A\).

Define

\[
\begin{aligned}
B_0&=\{1,2,\ldots,2^{n-1}\},\\
B_1&=\{1,2,\ldots,2^{n-2}\}\cup\{2^{n-1}+1\},\\
B_2&=\{1,2,\ldots,2^{n-3}\}\cup\{2^{n-2}+1,2^{n-1}+1\},
\end{aligned}
\]

where the indicated initial lists consist of powers of two.
These are **known constructions**, specializing Cambie–Gao–Kim–Liu,
Proposition A.1. The result here proves necessity in an entire uniform
subclass, gives its exact count, and describes the excluded residual.

## Theorem

For every \(n\ge5\), a sum-distinct \(A\) containing distinct elements
\(a_i=\epsilon_i u2^i\), \(0\le i\le n-3\), with \(u\) a unit and
\(\epsilon_i\in\{-1,1\}\), is equivalent to exactly one of
\(B_0,B_1,B_2\).

The number of actual subsets of the fixed group satisfying this chain
condition is exactly

\[
3\,2^{n-1}\varphi(N).
\]

Every other sum-distinct \(n\)-set has an acyclic signed doubling graph,
each of whose components has at most \(n-3\) vertices. At most one of its
elements is a nonunit; such an element has gcd \(3\) with \(N\) and is
an isolated vertex. Nonunits are possible only when \(n\) is even.

The theorem does **not** assert that this residual is empty for arbitrary
\(n\). In particular, it does not settle the unrestricted excess-five
classification or its conjectured \(O(N^2)\) count.

## 1. Normalization and the six forms

A sum-distinct set contains neither zero nor an opposite pair: these
would respectively identify a singleton or a two-element subset with
the empty subset. Consequently sign changes preserve its cardinality.
Changing the sign of \(a\) translates the subset-sum set by \(-a\), via
the bijection that toggles membership of \(a\). Unit dilation also
preserves all equalities and inequalities between subset sums. These
operations therefore preserve sum-distinctness.

Normalize the hypothesized chain to
\(C=\{1,2,\ldots,2^{n-3}\}\). Its subset sums are exactly
\(I=\{0,1,\ldots,m-1\}\), each once. Change signs of the other two
elements independently and order their least absolute representatives
as \(1\le x<y\le (N-1)/2=2m+2\). They are distinct and outside \(C\).

The subset sums of the normalized set are the four translates

\[
I,\qquad I+x,\qquad I+y,\qquad I+x+y.
\]

Two translates of \(I\) are disjoint precisely when the difference
between their starting points, represented in \(\{0,\ldots,N-1\}\),
lies in \([m,N-m]=[m,3m+5]\). Indeed the difference set \(I-I\)
consists of the residues represented by \(-(m-1),\ldots,m-1\).

Disjointness of \(I,I+x\) forces \(x\ge m\); disjointness of
\(I+x,I+y\) forces \(y-x\ge m\). Since \(y\le2m+2\), it follows that

\[
x=m+a,\qquad y=2m+b,\qquad 0\le a\le b\le2.
\]

Conversely every one of these six integer pairs gives four disjoint
translates. All their pairwise starting-point differences, up to sign,
are \(x,y,y-x,x+y\). The first three lie in \([m,3m+5]\), and the last
equals \(3m+a+b\in[3m,3m+4]\). Thus the list is necessary and sufficient,
without any restriction to finitely many \(n\).

For \(T_{ab}=C\cup\{m+a,2m+b\}\), the complete equivalence table is:

| \((a,b)\) | Representative | Unit multiplier, followed by least absolute representatives |
|---|---|---|
| \((0,0)\) | \(B_0\) | \(1\) |
| \((0,1)\) | \(B_1\) | \(1\) |
| \((0,2)\) | \(B_0\) | \(2\) |
| \((1,1)\) | \(B_2\) | \(1\) |
| \((1,2)\) | \(B_0\) | \(4\) |
| \((2,2)\) | \(B_1\) | \(2\) |

To check the nontrivial rows, use \(4m+4=-1\pmod N\).
Doubling \(T_{02}\) gives \(B_0\) after sign changes.
Doubling \(T_{12}\) gives \(T_{02}\), and doubling \(T_{22}\) gives
\(B_1\), since \(2m+4=-(2m+1)\pmod N\).
Both 2 and 4 are units because \(N\) is odd.

## 2. Inequivalence and the exact count

For any sum-distinct set define its **signed doubling graph** on the
distinct classes \([a]\), \(a\in A\), with a directed edge
\([a]\longrightarrow[b]\) when \([2a]=[b]\). Unit dilation induces a
graph isomorphism, and individual sign changes leave the graph unchanged.

For \(B_0,B_1,B_2\) the component orders respectively are

\[
(n),\qquad(n-1,1),\qquad(n-2,1,1),
\]

and the nonsingleton components are directed paths. Here is a direct
check of the endpoints, including wraparound. The last power of two
in \(B_0\) doubles to \([-5]\), which is absent. The last powers of two
in \(B_1,B_2\) double to \([2m]\), \([m]\), respectively, also absent.
The exceptional element \(2m+1\) doubles to \([-3]\), absent for all
three representatives. In \(B_2\), \(m+1\) doubles to \([2m+2]\),
which is absent. All other power-of-two edges are the indicated path
edges. Since \(m\ge8\), none of 3 or 5 is a listed power or exceptional
element, and no extra edge or loop occurs. The distinct component
orders prove inequivalence.

For each representative, its unique nonsingleton path has at least
three vertices, and its initial vertex is \([1]\). Any unit preserving
its signed-class set must preserve this vertex, hence is \(1\) or
\(-1\). Both do preserve it. Thus its orbit among signed-class sets
under the unit group has size \(\varphi(N)/2\). Each signed-class set
has exactly \(2^n\) distinct choices of element signs: every class is
nonzero, has size two, and is distinct from all other classes.
These choices remain sum-distinct. Each of the three disjoint
equivalence classes therefore contains \(2^{n-1}\varphi(N)\) subsets.

## 3. A divisor constraint valid for every admissible set

The following counting observation applies without a chain hypothesis.
For a divisor \(d\mid N\), suppose \(k\) elements of \(A\) are divisible
by \(d\). In each residue class \(j\pmod d\), the number of represented
subset sums is a multiple of \(2^k\): fix the subset of the remaining
elements and vary the subset of these \(k\) elements. Injectivity makes
all these sums distinct. If \(h_j\) is the number of missing residues
in that class, then

\[
h_j\equiv N/d\pmod{2^k},\qquad h_j\ge0,\qquad \sum_{j=0}^{d-1}h_j=5.
\tag{1}
\]

Take a nonunit \(a\) and \(d=\gcd(a,N)>1\). Both \(d\) and \(N/d\)
are odd, so (1) with \(k\ge1\) makes every \(h_j\) positive and odd.
Thus \(d\le5\). As \(5\nmid 2^n+5\), necessarily \(d=3\).
Also \(3\mid N\) holds exactly when \(n\) is even.

If there were two nonunits, both would be divisible by 3. For even
\(n\ge6\), \(N\equiv9\pmod{12}\), so \(N/3\equiv3\pmod4\).
Equation (1) would force each of the three \(h_j\) to be at least 3,
contradicting their sum 5. Hence at most one nonunit exists. If one
exists, its three missing-residue counts modulo 3 are \((3,1,1)\)
in some order.

## 4. The complete structural residual

Multiplication by 2 permutes the nonzero signed classes, so each vertex
of the doubling graph has indegree and outdegree at most one. A cycle
of length \(k\le n\) through a unit would give \(2^k\equiv\pm1\pmod N\),
impossible because \(2\le2^k\le2^n=N-5<N-1\).

Multiplication by 2 preserves gcd with \(N\), so the possible single
nonunit has no edge to a unit. A loop at that nonunit would imply
\(a=0\) or \(3a=0\). Its order is \(N/3\ge23\), excluding both.
Consequently every component is a directed path, with any nonunit
isolated.

A path on at least \(n-2\ge3\) vertices is therefore a unit path and
gives precisely the signed unit chain in the theorem. Section 1
classifies every set with such a path. Every unclassified set must
have all path components of order at most \(n-3\), as asserted.
This is an exhaustive residual condition, not an assumption that the
long path exists in an arbitrary admissible set.

## Scope and verification

The uniform theorem and count above have an elementary written proof.
They do not depend on a solver, floating-point computation, finite
parameter extrapolation, or a subset-sum reconstruction theorem.
They have not been formalized in a proof assistant or independently
peer reviewed.

The companion exact Python replay checks every normalized pair for
\(5\le n\le10\), all six equivalence identities, the graph invariants,
and the full signed-class census at \(n=5,6\). A separate verifier uses
literal subset-sum lists, unit orbits, and an unpruned combinations
census at \(n=5\). These are controls on the argument and implementation;
the proof's quantifier over all \(n\) comes from Sections 1–4.

Cambie–Gao–Kim–Liu's Lemma 5.2 already gives symmetry of the five missing
residues, and their Proposition A.1 already supplies the three
constructions. Neither is claimed here as new. See [literature.md](literature.md)
for the precise primary-source and open-status limitations.
