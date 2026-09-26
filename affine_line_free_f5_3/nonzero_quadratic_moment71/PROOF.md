# A nonzero quadratic moment is necessary at 71 points

All vector and polynomial calculations below are over \(\mathbb F_5\).
Plane cardinalities, deficits, and their stated integer sums are ordinary
integers. A line-free set contains no complete five-point affine line.

**Theorem.** If \(S\subseteq\mathbb F_5^3\) is line-free and \(|S|=71\), then,
with
\[
 \mu=\sum_{x\in S}x,\qquad
 M=\sum_{x\in S}(x-\mu)(x-\mu)^{\mathsf T},
\]
one has \(M\ne0\).

The normalization is valid because \(71=1\) in the field. Under an affine
coordinate change \(x\mapsto Ax+t\), \(\mu\mapsto A\mu+t\) and
\(M\mapsto AMA^{\mathsf T}\). Thus the theorem excludes a whole affine
invariant family, without assuming any symmetry of \(S\). Equivalently,
the six upper-triangular entries of
\(\sum xx^{\mathsf T}-\mu\mu^{\mathsf T}\) cannot all vanish.

The proof is computer assisted only at explicitly bounded finite steps.
The package rechecks the planar cap and a small-field quartic
classification from first principles. It imports no 72-point exclusion,
SAT lifting result, earlier moment exclusion, or low-plane certificate.
It does not decide whether any 71-point set exists.

## 1. Elementary incidence facts

There are 31 projective directions, 155 affine planes, 31 planes through
a point, and six planes through two distinct points. The planar census in
`planar_cap.cpp` checks all \(\binom{25}{17}=1,081,575\) subsets of size 17
against all 30 planar lines and finds none line-free. Therefore every
plane section has size at most 16, and every section of a 71-point set has
size at least \(71-4\cdot16=7\).

For a line \(\ell\) containing \(k\) selected points, its six incident
planes satisfy
\[
 \sum_{H\supset\ell}|S\cap H|=71+5k. \tag{1}
\]
Consequently, a plane of size at most ten contains no four-point line:
otherwise (1) gives \(91\le10+5\cdot16=90\).

Let \(f\) be the number of seven-point planes and
\(\epsilon=1_{\{\mu\in S\}}\). A seven-point plane has parallel profile
\((7,16,16,16,16)\). Taking the first moment modulo 5 shows that the
seven-point member contains \(\mu\).

The normal directions of these planes form an arc in the dual
\(\operatorname{PG}(2,5)\): three collinear normals would give three
seven-point planes through one line, and (1) would imply
\(71\le3\cdot7+3\cdot16=69\).

An arc in this projective plane has at most six points. The six lines
through an arc point first give an upper bound of seven. Equality would
make every line meeting the arc a secant; counting the seven arc points
along the six lines through an external point would then give an even
total, a contradiction.

Every arc of at most six points in \(\operatorname{PG}(2,5)\) lies on a
nonsingular conic. Here is a small-field justification, including the
finite part checked by `geometry_audit`.

* Five arc points impose five independent conditions on the six
  quadratic coefficients: for each point, a product of two lines
  pairing the other four vanishes at those four and not at that point.
  Their unique quadratic is nonsingular. A degenerate quadratic has
  its rational zeros on at most two lines or at a single point, and
  cannot contain a five-arc.
* Nonsingular conics with a rational point are projectively equivalent
  to \(xy-z^2=0\), hence to the standard conic
  \(x^2+y^2+z^2=0\). For each of the six five-subsets of the standard
  conic, the only point avoiding all ten pairwise secants is the
  missing sixth conic point. The verifier checks this among all
  31 projective points.
* Four arc points are projectively equivalent to the three coordinate
  points and \((1,1,1)\), which lie on the nonsingular conic
  \(xy+xz+3yz=0\). Smaller arcs extend to a four-arc: there is a point
  outside the finitely many pairwise secants at each step.

Choose a conic \(C\) containing the \(f\) seven-plane normals. Relative
to \(\mu\), let \(h(p)\) be the number of its six central planes
containing the radial line of projective direction \(p\).
There are ten directions with \(h=0\), six with \(h=1\), and fifteen
with \(h=2\). Each conic plane contains exactly one of the six \(h=1\)
radial lines. These assertions follow either from conic polarity or
from the checked 31-point standard model.

Each point other than \(\mu\) has total weight two in the following
sum, whereas \(\mu\) has weight \(6+2\cdot10+6=32\):
\[
 2|S|+30\epsilon
 =\sum_{v\in C}|S\cap v^\perp|
   +2\sum_{h(p)=0}|S\cap\langle p\rangle|
   +\sum_{h(p)=1}|S\cap\langle p\rangle|. \tag{2}
\]
All spaces here are translated through \(\mu\). The central planes
contribute at most \(7f+16(6-f)=96-9f\). Radial lines contain at most
four points; precisely \(f\) of the six \(h=1\) lines belong to the
known seven-point planes and therefore contain at most three.
Thus (2) gives
\[
 142+30\epsilon\le(96-9f)+80+(24-f)=200-10f.
\]
Since \(f\) is integral, this proves the independent incidence lemma
\[
 \boxed{f+3\epsilon\le5.} \tag{3}
\]

## 2. Moment profiles under the assumption \(M=0\)

Translate by \(\mu\), write \(y=x-\mu\), and suppose \(M=0\).
For a projective normal representative \(v\), put
\[
 T(v)=\sum_{x\in S}(v\cdot y)^3,\qquad
 U(v)=\sum_{x\in S}(v\cdot y)^4.
\]
These are homogeneous forms of degrees three and four. The value of
\(U\), and whether \(T=0\), are independent of the choice of nonzero
representative \(v\). Let
\[
 m(v,t)=|\{x\in S:v\cdot y=t\}|,\quad
 \delta(v,t)=16-m(v,t).
\]
Each deficit lies in \(\{0,\ldots,9\}\) and their parallel sum is nine.
Expanding the indicator \(1-(t-v\cdot y)^4\) and using the zero first
and second moments gives
\[
 \delta(v,t)\equiv t^4+tT(v)+U(v)\pmod5. \tag{4}
\]

If \(T(v)\ne0\), rescaling \(v\) makes \(T(v)=1\), without changing
\(U(v)\). The allowed values of \(U\) are \(0,1,2,3\). The sum of the
least residues in (4) is nine, so no additional multiple of five is
possible. The central deficit is \(U\) and the sum of the five squared
deficits is \(29-2U\).

If \(T(v)=0\), the possibilities are:

| \(U\) | Least residues, central coordinate first | Extra five | Central deficit | Sum of squares |
|---:|---|---|---:|---:|
| 0 | \(0,1,1,1,1\) | central | 5 | 29 |
| 0 | \(0,1,1,1,1\) | off center | 0 | 39 |
| 1 | \(1,2,2,2,2\) | none | 1 | 17 |
| 4 | \(4,0,0,0,0\) | central | 9 | 81 |
| 4 | \(4,0,0,0,0\) | off center | 4 | 41 |

These rows follow directly from (4) and the deficit sum nine.
The verifier also enumerates all 715 nonnegative compositions of nine
into five coordinates, imposes zero first and second moments, and
obtains exactly 27 labeled profiles with the stated statistics.

Let \(a,b,c\) count directions with \(T=0\) and \(U=0,1,4\), respectively.
Let \(d\) count the directions where \(T\ne0\), and let \(J\) be the
ordinary integer sum of their values \(U\in\{0,1,2,3\}\).
Let \(g\) count the \(U=0,T=0\) directions whose extra deficit five is
off center. The seven-point planes are exactly the \(U=4,T=0\) profiles
with the extra five at the center. Hence
\[
 a+b+c+d=31,\quad 0\le g\le a,\quad 0\le f\le c.
\]

Double counting gives
\[
 \sum_H m_H=31\cdot71=2201,\qquad
 \sum_H m_H^2=31\cdot71+6\cdot71\cdot70=32021.
\]
Consequently \(\sum_H(16-m_H)^2=1269\).
The sum of deficits of the 31 central planes is \(70-25\epsilon\),
because a noncentral point lies on six central planes.
Using the profile table, these two identities become
\[
 29a+17b+41c+29d-2J+10g+40f=1269, \tag{E}
\]
\[
 5(a-g)+b+4c+J+5f=70-25\epsilon. \tag{C}
\]
Their useful linear combination is
\[
 \boxed{a-b+2c+5(f+\epsilon)=51.} \tag{5}
\]

Every homogeneous quartic \(U\) over this field satisfies
\[
 \sum_{v\in\operatorname{PG}(2,5)}U(v)=
 \sum_{v\in\operatorname{PG}(2,5)}U(v)^2=0
 \quad\hbox{in }\mathbb F_5. \tag{6}
\]
Indeed, the sum over all vectors of a monomial of total degree four or
eight vanishes: a nonzero product of coordinate power sums requires
all three exponents to be positive multiples of four, which would
require total degree at least twelve. A projective sum is one fourth
of the sum over nonzero vectors. The verifier checks the monomial bases.

## 3. Exact quartic lemma

**Finite lemma.** A homogeneous ternary quartic with all 31 projective
values in \(\{0,1,4\}\) is either the square of a homogeneous quadratic
or a form \(F(\ell_1,\ell_2)\), where \(\ell_1,\ell_2\) are independent
linear forms and \(F\) is a square-valued homogeneous binary quartic.
These families overlap. The complete value spectra are:

| Number of zeros | Number of ones | Number of fours | Number of forms |
|---:|---:|---:|---:|
| 1 | 15 | 15 | 620 |
| 6 | 0 | 25 | 31 |
| 6 | 10 | 15 | 3100 |
| 6 | 15 | 10 | 3100 |
| 6 | 25 | 0 | 31 |
| 11 | 10 | 10 | 2790 |
| 21 | 5 | 5 | 930 |
| 31 | 0 | 0 | 1 |

In every form with 21 zeros, the five directions with value four
are collinear.

**Complete finite verification.** A ternary quartic has 15 coefficients.
The verifier constructs the \(31\times15\) monomial evaluation matrix,
selects and exactly inverts a nonsingular \(15\times15\) minor, and
checks its inverse. Any square-valued form is therefore uniquely
specified by an information word in \(\{0,1,4\}^{15}\).
`quartics.cpp` tests all \(3^{15}=14,348,907\) such words at all
31 projective coordinates and retains 10,603.

Separately, `model.py` evaluates all \(5^6\) quadratics and squares
their values, giving 7,813 distinct words. For each of the 31 possible
vertices, it chooses two independent annihilating linear forms and
lifts every square-valued binary quartic. Binary quartic evaluation on
the six projective points is exactly the five-dimensional subspace
whose coordinate sum is zero; a separate direct evaluation of all
\(5^5\) binary forms verifies this. There are 153 square-valued binary
patterns, yielding 4,403 distinct ternary cone words. The two families
intersect in 1,613 words. The verifier compares their full union with
the full exhaustive catalogue, entry for entry, then checks the
collinearity assertion on all 930 relevant forms.

The collinearity also has a structural explanation. A quadratic has
at most eleven projective zeros unless it is zero, so a form with
exactly 21 zeros must be a binary cone. Each nonvertex binary value
has a five-point projective fiber on one line through the vertex.
The five values equal to four form one such fiber.

For additional algorithmic control, direct reconstruction of the
quartic coefficients and monomial evaluation independently checks
19,683 information words, with 73 retained. Counts, full-set equality,
finite geometric checks, and all later integer case reductions are
enforced by explicit exceptions, including when Python runs with `-O`.
The complete sorted catalogue is regenerated locally rather than
published. Its SHA-256, including a newline after each word, is
`78a8dd90d77ae26d420693802ab8ba1271d17ff4d4fe0403e7c8204cc412d42a`.

## 4. Exclude \(T\ne0\)

A nonzero ternary cubic has at most 16 projective zeros. If it has no
rational linear factor, each rational line has at most three zeros;
counting through one zero gives at most \(1+6\cdot2=13\).
If it has a linear factor, the remaining quadratic is a nonsingular
conic, an isolated rational point, a repeated line, or two lines.
The largest possible zero set is the union of three concurrent lines,
of size 16. Thus \(d\ge15\).

Every nonseven profile contributes at most 41 to the deficit square
sum, a direction with \(T\ne0\) contributes at most 29, and a
seven-plane profile contributes 81. Therefore
\[
 1269\le41(31-d-f)+29d+81f=1271-12d+40f.
\]
Together with (3), this forces \(f=5,\epsilon=0\) and \(d=15\) or 16.
Equation (5) gives \(c-2b=d-5\).

If \(d=15\), then \(a=6-3b,\ c=10+2b\), and (E) becomes
\(5g-J=25-6b\). Since \(J\ge0\) and \(g\le a\),
\(25-6b\le30-15b\), hence \(b=0,a=6,c=10\).
The possibilities are \((g,J)=(5,0)\) or \((6,5)\).
For \(J=0\), the full quartic spectrum is \((21,0,10)\).
For \(J=5\), (6) forces the nonzero values among these \(d\) directions
to be five ones: among partitions of five into parts 1, 2, and 3,
only \(1+1+1+1+1\) has square sum zero modulo 5.
The full spectrum is then \((16,5,10)\).
Both are absent from the finite quartic lemma.

If \(d=16\), then \(a=4-3b,\ c=11+2b\), and
\(5g-J=19-6b\). The same inequality gives \(b=0,g=4,J=1\).
Thus \(\sum U(v)^2=11\cdot16+1=177\ne0\pmod5\), contradicting (6).
This excludes every nonzero cubic.

## 5. Exclude \(T=0\)

Now \(d=J=0\), and the quartic takes only the values \(0,1,4\).
For each of the eight spectra in the finite lemma, use (E), (C),
\(0\le g\le a\), \(0\le f\le\min(6,c)\), and
\(\epsilon\in\{0,1\}\). The only integer possibilities are
\[
 (a,b,c;f,g,\epsilon)=(21,5,5;4,21,1)
 \quad\hbox{or}\quad(21,5,5;5,17,0).
\]
This tiny substitution is also checked by `statistics_audit`.
The first violates (3). In the second, all five seven-plane normals
would lie on the line formed by the five \(U=4\) directions.
They cannot form an arc. This is a contradiction.

Both cubic cases are impossible under \(M=0\), proving the theorem.

## Trust boundary and remaining target

This is a human-readable argument with exhaustive exact finite inputs,
not a proof-assistant formalization. The trusted implementation boundary
is the small Python generator/verifier, the C++ enumerators and compiler,
and ordinary exact integer arithmetic. There is no SAT/LP solver,
floating-point inference, unexamined orbit quotient, external census,
or retained search failure used as a proof. Sanitizers and independent
evaluation checks reduce implementation risk; they do not remove this
boundary.

The theorem removes the zero matrix among the possible moment forms
at cardinality 71. Nonzero moment matrices remain. The exact maximum
continues to be unresolved between 70 and 71; this contribution alone
does not satisfy the campaign's exact-value acceptance gate.
