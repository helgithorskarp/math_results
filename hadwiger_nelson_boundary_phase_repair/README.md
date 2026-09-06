# A finite boundary-phase repair colours the full quartic circle support

**Result.** The exact quartic placement in the previously published
[realized phase obstruction](../hadwiger_nelson_realized_phase_obstruction/README.md)
has a proper four-colouring of its **entire infinite union of four unit circles
and their centres**, extending the same four distinct centre colours. Therefore
no finite subgraph of this support can be five-chromatic. Its old owner-group
kernel lists are impossible, so the new extension criterion strictly strengthens
that sufficient method.

The transferable part is a finite necessary-and-sufficient criterion **within
the class of extensions using the two fixed owner-group palettes outside the
kernel**. For any two paired unit segments it uses at most 204 kernel colour
variables and 800 residual orbit bits. It allows arbitrary proper colours on
the kernel, and checks the finitely many actual edges from the kernel to its
complement. The application below has 74 kernel points, 198 kernel edges,
134 boundary root incidences, and 107 residual orbits.

This excludes one exact full support, not every member of the continuous
obstruction family or every paired-circle placement. There is no new
five-chromatic graph on at most 508 vertices and no priority claim. The target
baseline remains the 509-vertex construction in
[Parts's primary paper](https://arxiv.org/abs/2010.12665), also identified as the
record in [Haugland's August 2026 paper](https://arxiv.org/html/2608.04542v4);
these sources were checked live on 6 September 2026.

## 1. Finite extension criterion

Let four distinct centres be
\(d_0=a_0,d_1=a_1,d_2=b_0,d_3=b_1\), with
\(|a_1-a_0|=|b_1-b_0|=1\). Write
\(C_d=\{x:|x-d|=1\}\), \(\omega=(1+i\sqrt3)/2\), and
\(U=\{1,\omega,\ldots,\omega^5\}\). The full support is
\[
 X=\{d_0,d_1,d_2,d_3\}\cup\bigcup_{h=0}^3 C_{d_h}.
\]
A point's owners are the centres at unit distance from it. Group 0 is
\(A=\{a_0,a_1\}\), and group 1 is \(B=\{b_0,b_1\}\).

Use the [paired-circle kernel](../hadwiger_nelson_paired_circle_kernel/README.md):
\[
\begin{split}
 S_A&=U(a_1-a_0)\cup
 \bigcup_{a\in A,b\in B,\ x\in C_a\cap C_b} U(x-a),\\
 S_B&=U(b_1-b_0)\cup
 \bigcup_{a\in A,b\in B,\ x\in C_a\cap C_b} U(x-b),\\
 P&=(a_0+S_A)\cup(a_1+S_A)\cup(b_0+S_B)\cup(b_1+S_B).
\end{split}
\]
All centres and all multiply owned points belong to \(P\), and \(|P|\le204\).
Every noncentre kernel point has its direction from each owner in the
corresponding \(S\). These properties hold even at tangent cross-circle
intersections or unit cross-centre separations.

For completeness, the boundary fact used here follows from elementary circle
geometry. On a unit circle, a unit chord changes the direction by
\(\omega^{\pm1}\). If \(|a-b|=1\), \(x\in C_a\), \(y\in C_b\),
\(|x-y|=1\), and neither point is the opposite centre, then
\(y-b=x-a\): the two intersections of the circles about \(b,x\) are
\(a\) and \(b+x-a\). Hence a noncentre kernel point has no outside neighbour
on a group containing one of its owners. A point owned only by \(A\) can meet
the outside only on \(B\), and conversely; a mixed-owner point has no outside
neighbour. Every point outside \(P\) has a unique owner.

Pin the centre colours to \((2,3,0,1)\). The residual palettes are
\(\{0,1\}\) for group 0 and \(\{2,3\}\) for group 1.
Define the finite incidence set
\[
 \mathcal B=\{(x,h,z):x\in P\setminus\{d_0,d_1,d_2,d_3\},\
 z\in C_{d_h}\setminus P,\ |x-z|=1\}.
\]
There are at most four incidences per noncentre kernel point: only the two
circles of the opposite group can contribute, and each meets \(C_x\) in at
most two points. Thus
\[
 |\mathcal B|\le4(|P|-4)\le800.
\]
The circles in this count have distinct centres because \(x\) is a noncentre.

For each incidence \(e=(x,h,z)\), put \(w_e=z-d_h\) and choose a bit
\(\beta_e\). Bits at the same actual direction must agree, and rotation by
\(\omega\) changes the bit. More precisely, impose
\[
 \beta_e\mathbin\oplus\beta_f=k\pmod2
 \quad\text{whenever }\lfloor h_e/2\rfloor=\lfloor h_f/2\rfloor
 \text{ and }w_e=\omega^k w_f. \tag{1}
\]
Here \(\oplus\) denotes addition modulo two. The finite criterion asks for
an ordinary proper four-colouring \(c\) of the full unit-distance graph on
\(P\), with the centre pins, and bits satisfying (1) and
\[
 c(x)\ne 2\lfloor h/2\rfloor+
       (\beta_e\mathbin\oplus(h\bmod2))
       \qquad(e=(x,h,z)\in\mathcal B). \tag{2}
\]
There is only one free bit per represented residual direction orbit, so at
most 800 residual variables are needed. Kernel vertices have no additional
owner-group lists.

**Theorem.** This criterion is equivalent to the existence of a proper
four-colouring of \(X\) with the prescribed centre pins whose points outside
\(P\) use their owner's residual palette.

**Proof of sufficiency.** Within each owner group, choose a representative
\(w\) for each residual \(U\)-orbit. If it meets the boundary, choose one
boundary direction and take its certified bit \(\alpha=\beta_e\). Equation
(1) makes every other certified direction agree with this choice. For an
orbit not meeting the boundary, choose the representative with argument in
\([0,\pi/3)\) and put \(\alpha=0\). For \(g,j\in\{0,1\}\), define
\[
 c(d_{2g+j}+\omega^k w)=2g+(\alpha+j+k\pmod2)
 \qquad\text{outside }P. \tag{3}
\]
Every such point has one owner, so this is well-defined. Same-circle unit
edges change \(k\) by one. Unit edges between the circles of a pair preserve
the direction and change \(j\). They therefore have different colours.
Outside edges between the groups use disjoint palettes. The kernel edges
are proper by hypothesis, its noncentre boundary edges satisfy (2), and a
centre's outside edges are owner spokes with opposite palettes. These cases
exhaust all edges of \(X\).

**Proof of necessity within the stated class.** A residual orbit disjoint
from the corresponding \(S\) gives twelve distinct points, six on each
circle of its pair. No point is a centre or a circle intersection. Its
same-group unit graph is exactly two six-cycles joined by the direction-
preserving matching. This graph is connected and bipartite. A proper
colouring by the two palette colours is therefore of the form (3), with one
phase bit. Restricting those phases to the boundary gives (1) and (2).

The old owner-group lists make (2) automatic. They are sufficient but are
not necessary for this stronger criterion, as the exact example proves.
The theorem does not claim that all four-colourings of \(X\) use two colours
per group outside \(P\).

## 2. Exact placement and the old obstruction

Let \(\zeta=\omega^2=(-1+i\sqrt3)/2\) and \(\eta=\sqrt{2\sqrt3}>0\).
Set
\[
 u=(\sqrt3-i)/2,\qquad
 y=\frac{u}{2}(1-\sqrt3+i\eta),\qquad
 z=\frac{u}{2}(1-\sqrt3-i\eta),
\]
\[
 a_0=0,\quad a_1=\zeta^2,\quad
 b_0=-1-y,\quad b_1=-\zeta+z.
\]
The vectors \(u,y,z\) are unit, \(b_1-b_0=u\), and the centres are distinct.
The six mixed-owner points are
\[
 -1,\quad-\zeta,\quad-y,\quad\zeta^2-y,\quad z,\quad\zeta^2+z.
\]
Each cross-centre pair has precisely two of these points on both circles.
The direction sets have sizes 18 and 24; the actual kernel has 74 distinct
points and 198 unit edges.

The preceding result proved that the old lists fail throughout a continuous
family containing this member. For this example the obstruction can also
be seen directly. The point \(-1\) is owned by \(a_0,a_1,b_0\) and is forced
to colour 1 under the centre pins; \(-\zeta\) is owned by \(a_0,a_1,b_1\)
and is forced to colour 0. The four-edge unit path
\[
 -1,\quad\zeta,\quad-\zeta^2,\quad1,\quad-\zeta
\]
has three internal points owned only by \(a_0\). The old lists restrict all
three to colours 0 and 1, so an even path would force equal endpoint colours.
This contradiction is a list-colouring obstruction, not a chromatic one.
The boundary repair below permits 18 kernel points to leave those lists.

## 3. Finite positive certificate

All point coordinates lie in \(K^2\), where \(K=\mathbb Q(\eta)\) and
\(\eta^4=12\). The polynomial \(T^4-12\) is Eisenstein at 3, so coefficient
equality in the basis \(1,\eta,\eta^2,\eta^3\) is exact. Points are ordered
lexicographically by their real coefficient tuple followed by their imaginary
coefficient tuple; this is a symbolic ordering, not spatial order.

[certificate.json](certificate.json) contains a 74-character kernel colouring
and 134 rows \([i,h,s,\beta]\). Here \(i\) is the kernel point index, \(h\)
is the outside owner, \(s\in\{-1,1\}\) specifies the root below, and
\(\beta\) is its direction bit. No outside point is rounded or required to
lie in \(K^2\).

For \(v=x-d_h\) and \(q=|v|^2\), a possible outside direction satisfies
\[
 |w|=1,\qquad 2v\cdot w=q.
\]
There are no roots when \(q>4\); for \(0<q<4\) the two distinct roots are
\[
 w_s(v)=\tfrac12 v+\tfrac{s}{2}Jv\sqrt{(4-q)/q},\qquad s=\pm1, \tag{4}
\]
where \(J\) is counterclockwise rotation by \(\pi/2\). The corresponding
point is \(d_h+w_s(v)\). All candidate displacements in this exact instance
have \(q>0\) and \(q\ne4\). The general theorem also covers tangencies;
this instance checker deliberately rejects them rather than using an
untested branch.

| Exact quantity | Value |
| --- | ---: |
| Kernel point pairs checked | 2,701 |
| Boundary direction rotation comparisons | 27,882 |
| Equal-direction comparisons (even / odd rotation parity) | 52 (20 / 32) |
| Kernel unit edges | 198 |
| Opposite-group circle pairs considered | 128 |
| Empty circle pairs | 33 |
| Pairs with two distinct roots | 95 |
| Root incidences already in the kernel | 56 |
| Outside root incidences | 134 |
| Represented residual orbits in group A | 63 |
| Represented residual orbits in group B | 44 |
| Residual orbit phases pinned by this kernel colouring | 41 |
| Represented phases left free and set to zero | 66 |
| Kernel points outside the old lists | 18 |

The centre indices are \((49,24,35,38)\), with colours \((2,3,0,1)\).
The prescribed kernel colouring is

```text
01010122302113022330101030103102122010122032230112010110001122013303132101
```

The point and edge hashes match the earlier kernel exactly. The new evidence
is a verified extension to every point of \(X\), not another ordinary
colouring of the same finite graph. Equations (1)--(4), with the certificate,
are an explicit rule for the entire infinite colouring.

## 4. Exact boundary equality audit

Checking every possible identification of boundary directions is essential.
If \(w_s(v)=\omega^k w_t(v')\), rotate the second displacement first, putting
\(v''=\omega^k v'\). Since \(J\) commutes with this rotation, it suffices to
compare \(w_s(v)\) and \(w_t(v'')\).

The producer uses intersections of the two chord lines. Put
\(q=|v|^2,r=|v''|^2,d=\det(v,v'')\), and
\[
 N=(qv''_y-rv_y,\ rv_x-qv''_x).
\]
If \(d\ne0\), their sole intersection is \(N/(2d)\). It is unit exactly
when \(|N|^2=4d^2\); the signs of
\(\det(v,N)/(2d)\) and \(\det(v'',N)/(2d)\) select the two root branches.
If \(d=0\), two nonzero displacements give identical chord lines only when
\(v=v''\). In that case the roots agree precisely when \(s=t\).

The checker imports no producer or parent code. It represents real field
elements in the different quadratic tower
\(A+\eta B\), \(A,B\in\mathbb Q(\sqrt3)\), \(\eta^2=2\sqrt3\).
It compares roots by substituting (4) into the other chord equation. Let
\(p=v\cdot v''\), \(a=r-p\), and \(b=q-p\). For \(d\ne0\), equality is
equivalent to
\[
 a^2q=d^2(4-q),\qquad
 \operatorname{sgn}(a)=s\operatorname{sgn}(d),\qquad
 \operatorname{sgn}(b)=-t\operatorname{sgn}(d). \tag{5}
\]
Indeed the first substitution is
\(s d\sqrt{(4-q)/q}=a\); its square and sign select the first root.
The reverse substitution selects the second root. Both radicands are
strictly positive. Collinear displacements are handled as above.

Both implementations obtain exact signs through rational isolating intervals
for the specified positive algebraic embedding, refining until the sign is
strict. Exact zero is detected first in the field. Termination follows from
irreducibility and convergence of the intervals. The producer uses a
monomial Horner enclosure; the checker encloses the two positive radicals
separately. No floating-point equality, algebraic square-root extraction,
CAS, or native solver is trusted.

The checker reconstructs all kernel points and edges, and proves completeness
of its boundary list by considering every eligible circle pair. It identifies
internal roots by the unit norm and linear chord equation. It then checks
**all six rotations of every pair of boundary incidences in the same group**,
including pairs placed in different orbit classes by the producer. Every
actual equality must satisfy (1). Finally it checks every inequality in (2).
The orbit partition is reconstructed from these comparisons; class labels
are not accepted from the certificate.

The universal extension argument is written mathematics. The executable audit
checks the exact finite hypotheses for this one algebraic support. This is
author-side verification with distinct representations and derivations,
not an external peer review or a proof-assistant formalization.

## 5. Reproduce and scope

Requirements: Python 3.11 or later, standard library only; tested on Python
3.11.2, one thread per process. Producer replay and each checker took about
18 seconds when the three runs were executed concurrently on the research
host. From this directory, use fresh output directories:

```sh
sha256sum -c SHA256SUMS
python3 -B build.py --out work
python3 -B verify.py --out audit
python3 -O -B verify.py --out optimized
```

The producer uses the fixed positive kernel colour word above, identifies
residual orbits exactly, solves their unary phase requirements, and regenerates
the published certificate byte for byte. It performs no graph-colouring
search. A preliminary floating-point discovery calculation found the colour
word; it is not required for the proof or reproduction. The checker reads
only the compact certificate and expected report. It rejects omitted or
duplicated roots, malformed bits, wrong root signs, wrong embeddings, bad
hashes, monochromatic edges, and a phase inconsistency that leaves all
individual boundary edges proper. All semantic checks use explicit exceptions,
so the assertion-disabled run must produce the same result.

Certificate size: **1,900 bytes**. SHA-256:

```text
5f4d422e963c393cb2a309674a7d0f2112fe4fbbc7b34959307f8b0aa6c8650b
```

[expected.json](expected.json) records the complete exact audit output.
[validation.json](validation.json) records reproduction and rejection controls.
No unpublished input or omitted solver trace is needed.

This completes the fixed-member boundary repair milestone. The whole support
above and all its subgraphs are excluded from the five-chromatic search.
The result does not certify a neighbourhood in parameter space: an internal
boundary root at this member can move outside the kernel under deformation,
creating an additional constraint. Thus continuity of a finite kernel
colouring alone would not prove the same extension for nearby members.
No such additional parameter phase is started here.

The [previous realization and list barrier](../hadwiger_nelson_realized_phase_obstruction/README.md)
and [kernel boundary lemma](../hadwiger_nelson_paired_circle_kernel/README.md)
are the relevant mathematical dependencies. The preceding
[four-clause analysis](../hadwiger_nelson_paired_circle_four_clauses/README.md)
and the realization result's independent-phase transfer concerned prescribed
phases on the kernel's own orbits. The present colouring
instead permits exceptional kernel colours and controls phases of exterior
orbits, so it does not contradict that obstruction. HN-2's separately
[reviewed H560 decision](../hadwiger_nelson_heule560_global_decision_review1/README.md)
is coordination context only and is not used in the proof.
