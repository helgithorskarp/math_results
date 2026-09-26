# Two low planes in every 71-point line-free set

**Exact computer-assisted theorem.** If \(S\subseteq\mathbb F_5^3\)
has 71 points and contains no complete affine line, then at least two
affine planes meet \(S\) in at most nine points. Such planes are
nonparallel. This excludes every 71-point candidate having zero or one
such plane.

This result supplies a complete cover of the remaining 71-point problem
by 15 unordered pairs of normalized parallel profiles. It does not
construct or exclude a 71-point set. The separate
[upper bound 71](../upper_bound71/THEOREM.md) is context, not a premise.

All arithmetic in the proof certificates is integral. The finite
bridges are a complete planar census and the explicit matrix checks
below. This is an author proof, not a proof-assistant formalization or
independent peer review.

## 1. Sections and incidence identities

Write \(m_H=|S\cap H|\). The planar census visits all \(2^{25}\)
subsets of \(\mathbb F_5^2\). In particular, all 1,081,575 subsets of
size 17 contain a full line. Thus \(m_H\le16\); four parallel
companions give \(m_H\ge71-4\cdot16=7\).

For an affine line \(\ell\) containing \(k\) selected points, its six
containing planes satisfy
\[
 \sum_{H\supseteq\ell}m_H=71+5k. \tag{1}
\]
A section of size at most ten cannot contain a four-point line:
otherwise (1) gives \(91\le10+5\cdot16=90\).

For a planar section let \(s=(m,f_0,\ldots,f_4)\), where \(f_k\)
counts its lines with \(k\) selected points. The complete census keeps
sections of sizes 7–10 with maximum line intersection three, and of
sizes 11–16 with maximum line intersection four. It gives exactly
91 spectra, including all spectra that an actual section can have.
Multiplicities of labeled planar sets are recorded for reproduction;
they are not used as three-dimensional constraints.

Let \(X_s\) count planes with spectrum \(s\). Let \(P_p\) count
parallel classes with a suitably labeled five-tuple \(p\), defined
in Section 2. Let \(Y_{k,h}\) count lines of size \(k\) whose six
containing plane sizes, sorted in nondecreasing order, form \(h\).
Here
\[
 0\le k\le4,\quad
 h_i\in[\max(7,5k-9),16],\quad \sum_i h_i=71+5k.
\]
The lower endpoint follows by bounding the other five planes by 16.
There are 522 such pencil types.

The following 67 integer equations hold:
\[
\begin{aligned}
 \sum_sX_s&=155,& \sum_s m(s)X_s&=31\cdot71,&
 \sum_s {m(s)\choose2}X_s&=6{71\choose2},\\
 \sum_pP_p&=31,\\
 \sum_{s:m(s)=m}X_s&=\sum_p\#_m(p)P_p &&(7\le m\le16),\\
 \sum_{s:m(s)=m} f_k(s)X_s
 &=\sum_h\#_m(h)Y_{k,h} &&(0\le k\le4,\ 7\le m\le16),\\
 \sum_{k,h}Y_{k,h}&=775,&
 \sum_{k,h}kY_{k,h}&=31\cdot71,&
 \sum_{k,h}{k\choose2}Y_{k,h}&={71\choose2}.
\end{aligned} \tag{2}
\]
For the pair identities, two distinct points lie in six planes and
in one line. The flag identities count incidences between a line
of size \(k\) and a containing plane of size \(m\).

## 2. The global moment constraints

All calculations in this section are in \(\mathbb F_5\). Since
\(71=1\) in this field, the barycenter and centered moment matrix are
\[
 \mu=\sum_{x\in S}x,\qquad
 M=\sum_{x\in S}(x-\mu)(x-\mu)^T.
\]
The centered first moment vanishes. For any nonzero normal \(v\), let
\[
 p_t=|\{x\in S:v\cdot(x-\mu)=t\}|,\qquad Q(v)=v^TMv.
\]
Then
\[
 \sum_t p_t=71,\quad 7\le p_t\le16,\quad
 \sum_t t p_t=0,\quad \sum_t t^2p_t=Q(v). \tag{3}
\]
Scaling \(v\) scales \(Q(v)\) by a square. Each projective direction
therefore admits a representative with \(Q(v)\in\{0,1,2\}\):
zero, nonzero square, or nonsquare, respectively. For each direction
choose one such representative. All ordered profiles satisfying (3)
with these three values are included. There are 85 profiles; no
arbitrary permutation of field labels is imposed on an actual set.

Let \((c_0,c_+,c_-)\) be the numbers of projective normal directions
of the three quadratic characters. Symmetric matrices over
\(\mathbb F_5\) give precisely the following seven possibilities.

| Moment type | Diagonal representative | \((c_0,c_+,c_-)\) |
|---|---|---|
| Zero | \((0,0,0)\) | \((31,0,0)\) |
| Rank one, square | \((1,0,0)\) | \((6,25,0)\) |
| Rank one, nonsquare | \((2,0,0)\) | \((6,0,25)\) |
| Rank two, split | \((1,4,0)\) | \((11,10,10)\) |
| Rank two, anisotropic | \((1,2,0)\) | \((1,15,15)\) |
| Rank three, square determinant | \((1,1,1)\) | \((6,15,10)\) |
| Rank three, nonsquare determinant | \((1,1,2)\) | \((6,10,15)\) |

These follow by diagonalization in odd characteristic and evaluation
on the 31 projective points. The verifier additionally evaluates
every one of the \(5^6=15,625\) symmetric matrices directly, without
using a diagonalization routine, and checks that the table covers
all character distributions.

There are three additional equations:
\[
 \sum_{p:Q(p)=0}P_p=c_0,\qquad
 \sum_{p:Q(p)=1}P_p=c_+,\qquad
 \sum_{p:Q(p)=2}P_p=c_-. \tag{4}
\]
Here \(Q(p)=\sum t^2p_t\), and the values 1 and 2 refer to the
chosen representative normal, not to every vector in its direction.

Put \(\epsilon=1\) if \(\mu\in S\), and zero otherwise. Each other
selected point lies in six planes through \(\mu\), while \(\mu\)
itself lies in 31. The plane of label zero in every parallel class
passes through \(\mu\). Hence
\[
 \sum_p p_0P_p=6\cdot71+25\epsilon. \tag{5}
\]
Equations (2), (4), and (5) form a **71-by-698 integer system**
\(Au=b\), with \(u=(X,P,Y)\ge0\). Every actual candidate gives an
integer solution in one of the seven moment types and one of the
two values of \(\epsilon\). Sufficiency of the equations is never
assumed.

## 3. Exact certificates and the conclusion

Let \(c^Tu=\sum_{s:m(s)\le9}X_s=L\), the number of low planes.
For each of the 14 cases, [certificates.json](certificates.json)
gives an integer vector \(z\) and the positive denominator
\(D=100,000,000\). The verifier checks every column of
\[
 A^Tz\le Dc
\]
and computes \(b^Tz\) using integers. Therefore
\[
 D L \ge z^TAu=z^Tb.
\]
The smallest of the fourteen certified numerators is 117,641,713.
Thus in every case
\[
 L\ge\frac{117641713}{100000000}>1,
\]
and integrality gives \(L\ge2\). Two such planes cannot be parallel,
since their class would contain at most
\(9+9+3\cdot16=66<71\) selected points.

The certificates in fact give the following integer bounds.

| Moment type | \(\mu\notin S\): lower bound for \(L\) | \(\mu\in S\): lower bound for \(L\) |
|---|---:|---:|
| Zero | 2 | 4 |
| Rank one, square | 3 | 3 |
| Rank one, nonsquare | 2 | 2 |
| Rank two, split | 2 | 2 |
| Rank two, anisotropic | 3 | 3 |
| Rank three, square determinant | 2 | 2 |
| Rank three, nonsquare determinant | 2 | 2 |

The optional optimizer only discovers multipliers. After rounding,
the discovery script repairs each column block by decreasing the
multiplier of its constant-one counting row. Its final outputs are
verified as integers. Neither floating-point feasibility nor a
solver's status is used in the proof.

For additional geometry, every seven-plane passes through \(\mu\):
its profile is \((7,16,16,16,16)\), and the first moment puts its
low label at zero in centered coordinates. Its normal also satisfies
\(Q(v)=0\). No three seven-plane normals are collinear in the dual
projective plane, since the corresponding planes all contain a
common affine line and would have total at most
\(3\cdot7+3\cdot16=69\) in (1). Consequently there are at most six
seven-planes. Indeed, an arc in \(\mathrm{PG}(2,5)\) has at most seven
points by the six lines through one of its points; equality would
make every line meeting the arc a secant, and the six lines through
an external point would partition seven points into even-sized
pieces, a contradiction.

When \(M=0\), (3) permits no eight- or nine-plane. Direct enumeration
of the 85 profiles verifies this, or one can check the four sorted
low-profile patterns. Thus the zero-moment case has 2–6 concurrent
seven-planes, and has at least four if their common barycenter is
selected.

## 4. A complete 15-type cover for the remaining problem

Choose two nonparallel low planes and put them at \(x=0,y=0\).
Translation is used only to put the low plane at label zero.
Multiplication of each coordinate by a nonzero field element gives
the following five possible **ordered** parallel profiles.

| Type | Profile at labels \(0,1,2,3,4\) | Barycenter coordinate | Centered quadratic diagonal |
|---|---|---:|---:|
| A | \((7,16,16,16,16)\) | 0 | 0 |
| B | \((8,15,16,16,16)\) | 4 | 3 |
| C | \((9,14,16,16,16)\) | 3 | 4 |
| D | \((9,15,15,16,16)\) | 2 | 1 |
| E | \((9,15,16,16,15)\) | 0 | 3 |

A seven-plane has four 16-companions. An eight-plane has one
15-companion, whose label can be scaled to one. A nine-plane either
has a unique 14-companion, also scaled to one, or has two
15-companions. An unordered pair of distinct nonzero labels is,
under multiplication, equivalent to \(\{1,2\}\) or \(\{1,4\}\).
The verifier checks this cover directly. The last two columns are
\(\sum t p_t\) and \(\sum t^2p_t-(\sum t p_t)^2\) in \(\mathbb F_5\).

Interchanging \(x,y\) leaves 15 unordered pairs of types. These are
a complete cover, not an assertion of 15 disjoint affine orbits:
further identifications can occur by choosing different low planes.

Define the fiber weights and deficits
\[
 w_{xy}=|\{z:(x,y,z)\in S\}|,\qquad d_{xy}=4-w_{xy}.
\]
Every quotient line has weight at most 16, every fiber has weight at
most four, and every fiber on either zero axis has weight at most
three. Put \(m=|S\cap\{x=0\}|\), \(n=|S\cap\{y=0\}|\), and
\[
 K=\left\lfloor\frac{m+n-7}{5}\right\rfloor.
\]
Equation (1) applied to the common fiber gives \(w_{00}\le K\).
The deficit sum is 29. If \(R_i=20-p_i\) and \(C_j=20-q_j\)
are the prescribed row and column deficit margins and \(T\) is
the sum of the interior \(4\times4\) block, then
\[
 d_{i0}=R_i-\sum_{j=1}^4d_{ij},\quad
 d_{0j}=C_j-\sum_{i=1}^4d_{ij},\quad
 d_{00}=11-m-n+T. \tag{6}
\]
Thus
\[
 m+n-7-K\le T\le m+n-7\le11. \tag{7}
\]
The five possibilities by the sum of the low-plane sizes are:

| \(m+n\) | \(w_{00}\) upper bound | Interior deficit total \(T\) |
|---:|---:|---|
| 14 | 1 | 6 or 7 |
| 15 | 1 | 7 or 8 |
| 16 | 1 | 8 or 9 |
| 17 | 2 | 8, 9 or 10 |
| 18 | 2 | 9, 10 or 11 |

These inequalities bound a concrete finite quotient search. Its exact
cover is obtained by choosing the 15 profile pairs, enumerating
interior deficits in \(\{0,1,2,3,4\}^{16}\) satisfying (7),
reconstructing (6), retaining both endpoint bounds
\(1\le d_{i0},d_{0j}\le4\) and \(4-K\le d_{00}\le4\), and
checking deficit at least four on every quotient line. All candidate
projections are retained. No lifting computation is included here.

There is also a valid height normalization for every such projection.
At most 11 of the 16 interior deficits can be positive, so at least
five interior fibers have weight four. Every quotient line contains
at most four interior positions; hence three weight-four fibers have
noncollinear positions. Interpolate their three missing heights by
an affine function \(f(x,y)\). The shear
\((x,y,z)\mapsto(x,y,z-f(x,y))\) makes those three holes have height
zero, preserves every fiber weight, and preserves line-freeness.
No symmetry of the projection is imposed on its lift.

## 5. Scope and reproducibility

[verify.py](verify.py) rebuilds and runs the full planar census, matches
all 91 spectrum records including their labeled multiplicities, rebuilds
the integer system, and checks all 14 dual certificates on all 698
columns. It also checks all symmetric moment matrices, independently
generates profiles by deficit compositions, checks the five-profile
normalization, and tests the geometric identities on 20 arbitrary
71-subsets. Those controls are not claimed to be line-free.

The mathematical premises are established in this directory; no SAT
proofs, external classification dataset, earlier 72-point exclusion,
or prior moment theorem is imported. The planar-spectrum implementation
and incidence template are adapted with attribution from the team's
[earlier 72-point counting package](../low_planes72/README.md).
The global centered-moment refinement and the new census thresholds
are specific to cardinality 71.

The trust boundary is the written reduction, the complete ordinary
C++ enumeration, and the ordinary exact Python verifier. All finite
checks have reproducible source. The remaining question is whether
any 71-point lift exists.
