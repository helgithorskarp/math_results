# Original G20: exclude every component-only long vertex

Actual author **six-tammes-2**, role **researcher**, 2026-10-03.
Ordinary conditional computer-assisted proof; unformalized and independently
unreviewed. The alternate arithmetic below is same-author evidence.

**Theorem.** On CLOSED \(t\in I=[14/25,593/1000]\), CLOSED
\(z\in[6/5,7/5]\), the five original regular vertex systems indexed by
\((0,6,7),(1,4,12),(2,8,10),(5,7,9),(6,9,11)\) are infeasible.
Consequently three arbitrary packing additions to an injective original
twelve-label/twenty-contact G20 core force one of **255** unchanged parent
three-variable systems at the same core parameters. Every long vertex of
the parent's closed truncated avoidance polytope has an independent basis
using both core components or at least one cap plane.

This is a necessary reduction. Feasibility of the remaining 255 systems,
whole G20 capacity, lower-chart coverage, motif occurrence and unrestricted
Tammes15 optimality remain open. Extra contacts are allowed; no5-12/1-7
equality, thirteenth point, added-point position, face, degree, cohort,
optimizer neighborhood or occurrence premise is imposed.

## Complete scope and logical imports

Import the ENTIRE [9774 normalization](https://github.com/helgithorskarp/math_results/blob/main/round-two/six-tammes-2/twelve-core-frame/PROOF.md),
including all formal/singular alternatives, and the
[9912 integral lift](https://github.com/helgithorskarp/math_results/blob/main/round-two/six-tammes-2/twelve-core-polynomial-model/PROOF.md).
Import the full [10109 polytope/cap/census reduction](https://github.com/helgithorskarp/math_results/blob/main/round-two/six-tammes-2/g20-inner-vertex-reduction/PROOF.md).
Its compact original system is copied byte-identically as PARENT_SYSTEM.json,
SHA256 `de2b78260162b7b0a4482ba61ddc532c23783ed1e81f9b2e067c3c50badde1de`.
Its old native proof is not rebranded as a new capacity theorem.

The original labels are \(0,1,2,4,5,6,7,8,9,10,11,12\). Contacts are
\((0,5),(0,6),(0,7),(0,11),(1,2),(1,4),(1,10),(1,12),
(2,4),(2,8),(2,10),(4,8),(5,7),(5,9),(5,11),(6,11),
(7,12),(9,10),(9,11),(10,12)\). Every one of the 66 core comparisons
is retained. Three added unit packing points remain arbitrary.

In basis \((p_1,p_2,p_4)\), the metric is
\(H=(1-t)I+t\mathbf1\mathbf1^T\). Write
\(a=1+t,b=1-t,c=1+2t,D=b^2c,C=1+Dz^2,K=t(9t^2-2t-3),
J=a^2+K,h=9t^2-1\), and use the original lift's \(G,R=DG\),
SIGNED \(w>0,w^2=R\), strict \(2G-a^4C^2>0\), numerators \(Y_i\)
and strictly positive denominator \(\Omega\). The original sheet is retained.
Put \(Q=aDz^2-2Dz+2t^2-t+1\). The full identities
\(aQ=D(az-1)^2+4t^2\) and
\(\Omega=hJb^2c^2a^8C(bz+1)^2Q\) prove positive clearing here.
\(J(14/25)=26671/15625\) and
\(J'\ge27(14/25)^2-2(593/1000)-1>0\).

Use the parent's \(P_2\): all twelve inequalities
\(\langle p_i,x\rangle_H\le t\), together with
\(\langle n_{98},x\rangle_H\le9\),
\(\langle n_{99},x\rangle_H\le15\), where
\(n_{98}=(-8,12,-5)\), \(n_{99}=(-5,-14,20)\).
The parent proves boundedness, the arbitrary-three/open-cap implication,
existence of a long vertex, spanning active normals, and its complete
260-case necessary interface. No additional condition on the added points
is introduced by this five-case refinement.

## One intrinsic Gram and the exact active solution

Let \(A=(0,5,6,7,9,11)\), \(B=(1,2,4,8,10,12)\), and
\(k=K/a^2\). The integral lift gives the three A pair products
\(\langle p_6,p_7\rangle_H=\langle p_6,p_9\rangle_H=
\langle p_7,p_9\rangle_H=k\).
These are independently bound to the actual numerator coordinates, in
both radical components. The B products
\(\langle p_4,p_{12}\rangle_H=\langle p_8,p_{10}\rangle_H=k\)
are checked by full integer identities too. All other products used in
the following five Gram matrices are original contacts.

After placing the central label first, each Gram is

\[
\Gamma=\begin{pmatrix}1&t&t\\t&1&k\\t&k&1\end{pmatrix},\qquad
\det\Gamma=\frac{b^4c(3t+1)^2}{a^4}>0.
\]

For an active triple \((j,i,l)\) with central label \(j\), its UNIQUE
solution to all three products being \(t\) is

\[
x=\frac{t}{b^2c}\left[a^2(p_i+p_l)-(7t^2+2t-1)p_j\right].
\]

The complete identities
\(-(7t^2+2t-1)+2ta^2=b^2c\) and
\(-t(7t^2+2t-1)+a^2+K=b^2c\) check the three equations.
Its squared norm is
\(t^2(5t+3)/(bc)\); its excess over one is
\(a(5t^2-1)/(bc)>0\) throughout CLOSED I.
These are therefore actual long candidates, rather than repetitions
of the parent's short equilateral cases. Their strict Gram positivity
handles these five bases completely; no zero-rank geometric placement
is dropped. Other singular active triples remain covered by the
parent's independent-basis argument.

| Triple | Central label | Violated inequality |
|---|---:|---|
|(0,6,7)|0|cap99 product exceeds15|
|(1,4,12)|1|cap99 product is29t>15|
|(2,8,10)|2|cap98 product is25t>9|
|(5,7,9)|5|original point10 product exceeds t|
|(6,9,11)|11|cap98 product exceeds9|

## The two B exclusions are elementary

Put \(r=2t/a\); the entire CLOSED I has \(0<r<1\).
The literal B circuits are
\(p_8=-p_1+r(p_2+p_4)\),
\(p_{10}=-p_4+r(p_1+p_2)\), and
\(p_{12}=(r+r^2)p_1+(r^2-1)p_2-rp_4\).
Their nine coefficient identities are checked without an assumed extra contact.

At an active \((1,4,12)\), write \(q_i=\langle p_i,x\rangle_H\).
The third circuit with \(q_1=q_4=t\) gives
\((r^2-1)(q_2+t)=0\), hence \(q_2=-t\).
Then \(\langle n_{99},x\rangle_H=29t\), with
\(29t-15\ge31/25>0\).

At active \((2,8,10)\), the first two circuits give
\(-q_1+rq_4=(1-r)t\), \(rq_1-q_4=(1-r)t\).
Their sum and difference, with \(r\ne\pm1\), yield
\(q_1=q_4=-t\). Thus
\(\langle n_{98},x\rangle_H=25t\), with \(25t-9\ge5>0\).
Both contradict the actual CLOSED halfspaces of \(P_2\).

## Three affine radical excesses, including the original packing test

Define \(L=7t^2+2t-1\) and
\(T_{j;i,l}=t[a^2(Y_i+Y_l)-LY_j]\).
Then \(x=T_{j;i,l}/(b^2c\Omega)\). Let \(N_{10}=a^2p_{10}\)
be the literal B numerator in frame.py. Full integer identities give

\[
\begin{aligned}
\langle T_{0;6,7},n_{99}\rangle_H-15b^2c\Omega
 &= a^6b^2c^2(3t-1)(bz+1) f_{067},\\
\langle T_{5;7,9},N_{10}\rangle_H-ta^2b^2c\Omega
 &= ta^{10}b^2c^2(3t-1)(bz+1)^2Q f_{579},\\
\langle T_{11;6,9},n_{98}\rangle_H-9b^2c\Omega
 &= a^5b^2c^2(3t-1)(bz+1) f_{6911}.
\end{aligned}
\]

All displayed multipliers are strictly positive. Write \(f=A+Bw\).
The complete factor inputs are in FACTORS.json, bound to these original
coordinate expressions by both checkers. Full square identities are

\[
B_{067}^2R-A_{067}^2=ab^4c^2JQ H_{067},\qquad
B_{579}^2R-A_{579}^2=4a^2b^4c^2J H_{579}.
\]

The six strict sign obligations over the WHOLE CLOSED rectangle are
\(B_{067}>0,H_{067}>0,B_{579}>0,H_{579}>0,A_{6911}>0,B_{6911}>0\).
The primary checker proves every one of the 458 tensor Bernstein
coefficients strictly positive. The alternate proves every complete
translated Taylor enclosure positive on that same whole closed box,
also with 458 translated coefficients. No subdivision or omitted seam
is used. CERTIFICATE.json and AUDIT.json record the full rational
enclosures and ordered-array digests; all defining integer rows are supplied.

For the first two excesses, \(B>0,w>0\) and \(B^2R-A^2>0\) give
\(Bw>|A|\), hence \(f>0\). This implication uses the actual root sign;
it does not assume a sign of A. For the third, \(A,B,w>0\) directly give
\(f>0\). All three actual comparisons in the table are violated.
Neither cap tests nor the point10 test imposes a new contact.

## Complete refinement, replay and trust

The original full 364-triple census is regenerated. Its disjoint
94 pair cuts, one low-A cut, eight required-contact cliques and one
critical short cut give the same 260 parent residuals. Exactly the five
listed residual triples lie entirely in A or entirely in B. Deleting
them leaves ALL 255 literals in SYSTEM.json. Every retained system is
the parent's exact system: 33 equalities, three strict inequalities,
five closed domain predicates and 81 other nonnegative predicates.
The selected Gram determinant remains STRICT. All original core
constraints, halfspaces, signed radical and three variables remain.
No feasibility statement on any remaining system follows from this census.

The primary arithmetic uses entire sparse integer identities and exact
Bernstein conversion. The alternate uses the unchanged credited generic
digit engine from [six-reviewer-3/source52fa998f](https://github.com/helgithorskarp/math_results/blob/main/round-two/six-reviewer-3/g20-outer-audit/digit.py),
with 32 full zero polynomial components and different Taylor arithmetic.
Proved degree/coefficient-l1 bounds make the integer radix injective:
distinct monomials occupy distinct digit positions and each coefficient
has absolute value below the radix. A zero image proves the whole
polynomial zero, rather than testing a sampled point. No primary
expansion/division/Bernstein routine is used by the alternate proof.
Shared inputs are the credited original frame, literal factors and scope.
This reuse supplies no independent verdict on the NEW five exclusions.

The actually committed [10148 independent parent review](https://github.com/helgithorskarp/math_results/blob/main/round-two/six-reviewer-3/inner-vertex-audit/REVIEW.md)
confirms the full necessary260 reduction relative to ENTIRE9774 and9912.
Its [ordinary proof](https://github.com/helgithorskarp/math_results/blob/main/round-two/six-reviewer-3/inner-vertex-audit/PROOF.md)
and [division-free verification addendum](https://github.com/helgithorskarp/math_results/blob/main/round-two/six-reviewer-3/inner-vertex-audit/ADDENDUM.md)
retain the parent domain and case count. That independent review does not
check these new five exclusions. The credited generic digit engine was
published earlier with10115, whose stricter z<1399/1000 upper-chart result
is context only: every new sign here covers the full CLOSED z<=7/5.

The complementary [10150 fourteen-mask result](https://github.com/helgithorskarp/math_results/blob/main/round-two/six-tammes-1/b7-eight-placement/PROOF.md)
excludes fourteen contact-only masks for fifteen distinct unit vectors on
CLOSED J=[7/13,3/5]. Its physical cohort consequence retains ALL9972/9813/
10038/10068/10093 drawing, face, profile and COMPLETE actual A4/B7
component hypotheses, as stated in its [dependencies](https://github.com/helgithorskarp/math_results/blob/main/round-two/six-tammes-1/b7-eight-placement/DEPENDENCIES.md).
This separately scoped result is not a premise or review of the present
original-G20/arbitrary-three chart lemma; no global occurrence or reversed
component cover is imported. Both incoming full original signed bodies,
all eight/twenty-three atomic directed relations, whole canonical ledger/
RPC packets, source manifests and direct proof URLs were read and bound.

Controls reject 30 actual scope/parent damages and 12 actual polynomial
damages across both algorithms, four closed-endpoint zero signs and
negative/zero-root or zero-square guards. The credited exact core
\((t,z,w)=(29/50,5400/3973,454484658996081/225033203125000)\)
passes all twelve units, twenty contacts and 66 packing comparisons.
All five unique candidate vertices are then computed exactly, satisfy
their active equations, share the stated long norm and strictly violate
the listed inequalities. The core's extra5-12 equality is CONTROL ONLY,
neither a hypothesis nor a new construction or packing record.
The exact core is credited to the prior [10012 rational-family source](https://github.com/helgithorskarp/math_results/blob/main/round-two/six-tammes-2/g21-two-cap-capacity/PROOF.md).

The full old normalization and geometric interfaces remain explicit
unformalized imports. Standard-library integers/Fractions, inspected
finite arithmetic and the ordinary positive-clearing/Gram argument form
the trust base. VALIDATION.json records actual normal/optimized and
fresh-directory source-only replay under unchanged resource guards.
No solver, floating point, network, ledger, credential or omitted corpus
is a mathematical runtime input. Literature/credit and exact source pins
are recorded in DEPENDENCIES.json and LITERATURE.md.
