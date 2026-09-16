# Negative relative trace and a nonforest cross interface are incompatible

Put E = Q(i sqrt(3), i sqrt(11)) and R = Q(sqrt(33)), in their specified
plane embeddings. Use the conjugation-compatible embedding
E -> U = Q_2(omega), omega^2 + omega + 1 = 0, from the
[base-field theorem](../hadwiger_nelson_nonmono_field_obstruction/PROOF.md).
Let v be its valuation, normalized by v(2)=1, and set v(0)=+infinity.

Let u be a complex number of modulus one with [E(u):E]=2. Write its monic
minimal polynomial as X^2 - T X + J. Here T is the **relative algebraic
trace**, not necessarily u + conjugate(u). Assume v(T)<0.

**Corollary of the existing cycle results.** For arbitrary subsets P,Q of E
and any complex translation h, the placement g(q)=u q+h has no simple
alternating unit cycle on pairwise distinct physical points of P and g(Q).
Reflections are included by first conjugating Q. Source connectedness and
point-count bounds are unnecessary for this geometric conclusion.

In particular the bipartite graph of private cross contacts between
P minus g(Q) and g(Q) minus P is a forest. A formal labelled cycle that uses
the same physical point twice does not satisfy the premise. Nor do a cycle
of component labels, a multigraph of contacts, or an internal source cycle.
This is the physical meaning of the cross-interface condition below.

## 1. Direct deduction from the committed cycle classification

A simple bipartite cycle has even length at least four. For length at least
six, the [cross-cycle theorem](../hadwiger_nelson_cross_cycle_forest/PROOF.md)
forces g(E)=E. Since h=g(0) and u=g(1)-g(0), this would imply u in E,
contradicting its quadratic degree.

For a four-cycle let its source diagonals be d=p_1-p_0 and e=q_1-q_0.
They are nonzero. The moving vertices are the two intersections of the
unit circles about p_0 and p_1. Their common midpoint is
m=(p_0+p_1)/2=g((q_0+q_1)/2). The diagonals are perpendicular, so

    Re(conjugate(d) u e) = 0,
    u^2 = -d conjugate(e)/(conjugate(d) e) = W in E.

Consequently the minimal polynomial is X^2-W: it is monic of degree two,
vanishes at u, and u is not in E. Its relative trace T is exactly zero.
That contradicts v(T)<0. These midpoint and perpendicularity facts are
also the first step of the independently reviewed
[cross-four-cycle theorem](../hadwiger_nelson_cross_four_cycle_gluing/PROOF.md).

The two cases exclude every simple alternating cycle, without enumerating
angles, translations, source vertices or cycle lengths. The arbitrary-h
statement imports the committed long-cycle theorem; no independent peer
review of that theorem or of the present note is claimed.

## 2. A direct valuation proof when h belongs to E(u)

This supplementary proof covers the natural translation domain of the
quadratic-trace gluing program without using the classification of long
cycles. It also identifies why negative valuation and periodic cross
incidences conflict.

Write h=m-u n uniquely, with m,n in E. Conjugating and reciprocating the
minimal polynomial gives

    J conjugate(J)=1,       T=J conjugate(T).

The compatible embedding has v(N(z))=2v(z). Therefore v(J)=0.
For any cross edge put x=p-m, y=q-n, c=conjugate(x)y and
S=N(x)+N(y)-1. The distance equation gives

    c u^2 - S u + conjugate(c) = 0.

Independence of 1,u implies

    cT=S,       conjugate(c)=Jc.                         (1)

For nonzero c values their ratios are real. Thus edges sharing a nonzero
centred endpoint put their opposite endpoints on one real line through zero.
Propagating around an alternating simple cycle places its fixed vertices
on one line through m and its moving vertices on another. At most one
physical cycle point equals m; if present, remove it temporarily, propagate
along the remaining nonzero path, and then put it back on both lines. This
avoids division by a zero endpoint.

The two lines cannot coincide: a finite simple unit cycle on a line is
impossible, because its largest coordinate has at most one unit neighbour
among the selected points. Choose nonzero directions a,b in E for the
fixed line and the unmoved source line. Cycle vertices have the forms
m+a r and m+u b s with r,s in R. Set

    A=N(a)>0, B=N(b)>0, H=Re(conjugate(a)u b).

The lines are distinct, so H^2<AB. A cycle edge with nonzero endpoints
exists. Dividing (1) by its nonzero real scalar factors shows, with
c_0=conjugate(a)b,

    conjugate(c_0)=J c_0,     2H=c_0 T.

Hence H belongs to R and

    4H^2/(AB) = T^2/J.                                    (2)

Each cross edge lies on the positive definite conic

    F(r,s)=A r^2+B s^2-2Hrs=1.

Moving to the other fixed neighbour of s and then the other moving
neighbour gives the root-exchange matrix

    M = [ -1       2H/A             ]
        [ -2H/B    4H^2/(AB)-1      ].

It has determinant one and preserves F. A cycle of length 2k returns a
nonzero edge state after k applications of M. If H=0 then M=-I; otherwise
its trace is strictly between -2 and 2, its eigenvalues are distinct complex
conjugates, and a fixed nonzero state of M^k implies both eigenvalues are
k-th roots of unity. In either case its trace tau is an algebraic integer.
Since tau is in E, its image in U has v(tau)>=0: a root of a monic polynomial
with integral coefficients cannot have negative valuation, as its highest
power would be the unique term of least valuation.

But (2) gives

    tau = T^2/J - 2.

Because v(J)=0 and v(T)<0, the two terms have unequal valuations 2v(T)<0
and 1. Therefore v(tau)=2v(T)<0, a contradiction. This proves the no-cycle
conclusion for h in E(u) directly. No source connectivity is used here.

## 3. Consequence for the specified B292/V214 opportunity

The source package defines B=A union nu A, where A is the exact archived
Parts A159 gadget and nu=(5+i sqrt(11))/6. Its complete graph has 292 points
and 1,251 unit edges. V214 has 214 points and 977 unit edges. Both are
connected subsets of E; these source facts were independently checked in
[the cross-four-cycle review](../hadwiger_nelson_cross_four_cycle_review1/README.md).
The formal union has 506 labels and thus fits the 508 cap after collision
merging. The point budget is not the problem.

The requested conjunction is empty:

    quadratic relative trace with v(T)<0
    AND a genuine nonforest private cross interface.

No placement can pass both conditions. Moreover, if negative valuation is
dropped merely to force a cross cycle, the existing cycle and four-cycle
colouring theorems already four-colour the whole strict union of these
connected sources. That would not produce a new admissible candidate.

This is a feasibility stop before selecting coordinates or invoking SAT.
There is no newly constructed 506-point graph, no ordinary chromatic
verdict for a new placement, and no non-four certificate or five-word to
report. The conclusion does **not** colour all negative-trace placements.
Forest interfaces can couple connected, even globally cut-free graphs;
forest is not synonymous with separable. The general negative-trace forest
case remains outside this note and is not searched here. The fixed
rotation (1+i sqrt(15))/4 has its own stronger all-translation closure;
that separate theorem is not used to infer a universal result.

## 4. Evidence and trust boundary

`check_identities.py` uses exact rational Laurent polynomials to verify the
perpendicularity reduction, both root exchanges, determinant, invariant
quadratic form, matrix trace and substitution yielding (2). Small rational
controls distinguish a finite-order integral-trace matrix from a
negative-valuation trace. They check algebra only; they are not an
exhaustive placement search or a substitute for the uniform argument.

The proof is ordinary unformalized mathematics. Its arbitrary-translation
version imports the committed cycle theorem; the h in E(u) derivation
imports only the compatible base-field embedding and its norm-valuation
property. Source geometry and connectivity are imported reviewed facts,
not independently reproduced in this pass. Source pins distinguish those
dependencies and their evidence levels. No solver, floating geometry,
approximate root or failure of a colouring formula enters the conclusion.
